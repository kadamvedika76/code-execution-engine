import docker
import tempfile
import os
import shutil
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("docker_judge.log")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

client = docker.from_env()
JUDGE_IMAGE = "judge:latest"


def clean_output(text):
    return text.strip()

def clean_code(code):
    code = code.strip()
    logger.debug(f"Code cleaned: {len(code)} characters")
    return code


def run_container(command, temp_dir, timeout=5):
    """
    Creates container, runs it, waits with timeout
    Returns: output, error, runtime, exit_code
    """
    container = None
    start = time.time()
    try:
        container = client.containers.create(
            JUDGE_IMAGE,
            command,
            mem_limit="256m",
            memswap_limit="256m",
            network_disabled=True,
            volumes={
                temp_dir: {
                    "bind": "/code",
                    "mode": "rw"
                }
            },
            working_dir="/code",
        )

        container.start()

       
        result = container.wait(timeout=timeout)
        runtime = (time.time() - start) * 1000

        logs = container.logs(stdout=True, stderr=False)
        errors = container.logs(stdout=False, stderr=True)

        output = logs.decode().strip() if logs else ""
        error = errors.decode().strip() if errors else ""
        exit_code = result.get("StatusCode", 0)

        return output, error, runtime, exit_code

    except Exception as e:
        runtime = (time.time() - start) * 1000
        error_msg = str(e)
        if "timed out" in error_msg.lower():
            return "TIMEOUT", None, runtime, -1
        return None, error_msg, runtime, -1

    finally:
        if container:
            try:
                container.kill()
            except:
                pass
            try:
                container.remove(force=True)
            except:
                pass

def run_python_docker(code, input_data):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()

       
        with open(os.path.join(temp_dir, "solution.py"), "w") as f:
            f.write(code)
        with open(os.path.join(temp_dir, "input.txt"), "w") as f:
            f.write(input_data)

        
        output, error, runtime, exit_code = run_container(
            "sh -c 'python3 solution.py < input.txt'",
            temp_dir,
            timeout=5
        )

        if output == "TIMEOUT":
            logger.warning("Python TLE")
            return "TLE", None, 5000

        if exit_code != 0:
            logger.error(f"Python RE: {error}")
            return "RE", error, runtime

        return output, None, runtime

    except Exception as e:
        return "RE", str(e), 0

    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

def run_c_docker(code, input_data):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()

        with open(os.path.join(temp_dir, "solution.c"), "w") as f:
            f.write(code)
        with open(os.path.join(temp_dir, "input.txt"), "w") as f:
            f.write(input_data)

        output, error, runtime, exit_code = run_container(
            "gcc solution.c -o solution",
            temp_dir,
            timeout=30  
        )

        if exit_code != 0:
            logger.error(f"C CE: {error}")
            return "CE", error, 0

        logger.debug("C compilation successful")

        output, error, runtime, exit_code = run_container(
            "sh -c './solution < input.txt'",
            temp_dir,
            timeout=5
        )

        if output == "TIMEOUT":
            logger.warning("C TLE")
            return "TLE", None, 5000

        if exit_code != 0:
            logger.error(f"C RE: {error}")
            return "RE", error, runtime

        return output, None, runtime

    except Exception as e:
        return "RE", str(e), 0

    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


def run_java_docker(code, input_data):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()

        
        with open(os.path.join(temp_dir, "Main.java"), "w") as f:
            f.write(code)
        with open(os.path.join(temp_dir, "input.txt"), "w") as f:
            f.write(input_data)

       
        output, error, runtime, exit_code = run_container(
            "javac Main.java",
            temp_dir,
            timeout=30  
        )

        if exit_code != 0:
            logger.error(f"Java CE: {error}")
            return "CE", error, 0

        logger.debug("Java compilation successful")

       
        output, error, runtime, exit_code = run_container(
            "sh -c 'java Main < input.txt'",
            temp_dir,
            timeout=5
        )

        if output == "TIMEOUT":
            logger.warning("Java TLE")
            return "TLE", None, 5000

        if exit_code != 0:
            logger.error(f"Java RE: {error}")
            return "RE", error, runtime

        return output, None, runtime

    except Exception as e:
        return "RE", str(e), 0

    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


def evaluate_submission(code, language, test_cases):

    if not code or not code.strip():
        return {"verdict": "Error", "message": "No code submitted"}

    if language not in ["python", "c", "java"]:
        return {"verdict": "Error",
                "message": f"Unsupported language: {language}"}

    if not test_cases or len(test_cases) == 0:
        return {"verdict": "Error", "message": "No test cases found"}

   
    try:
        client.ping()
        logger.debug("Docker is running")
    except Exception:
        logger.error("Docker is not running!")
        return {
            "verdict": "Error",
            "message": "Docker not running"
        }

    code = clean_code(code)
    total_runtime = 0

    for i, case in enumerate(test_cases, start=1):
        input_data = case["input"]
        expected_output = case["output"]

        if language == "python":
            output, error, runtime = run_python_docker(
                code, input_data
            )
        elif language == "c":
            output, error, runtime = run_c_docker(
                code, input_data
            )
        elif language == "java":
            output, error, runtime = run_java_docker(
                code, input_data
            )

        total_runtime += runtime

        if output == "TLE":
            logger.warning(f"Test Case {i} -> TLE")
            return {
                "verdict": "TLE",
                "test_case": i,
                "time_ms": 5000
            }

        if output == "CE":
            logger.error(f"Compilation Error: {error}")
            return {
                "verdict": "CE",
                "error": error,
                "test_case": i
            }

        if output == "RE":
            logger.error(f"Test Case {i} -> RE: {error}")
            return {
                "verdict": "RE",
                "error": error,
                "test_case": i
            }

        if clean_output(output) == clean_output(expected_output):
            logger.info(f"Test Case {i} -> PASS ({runtime:.1f}ms)")
        else:
            logger.warning(f"Test Case {i} -> WA")
            return {
                "verdict": "WA",
                "test_case": i,
                "expected": expected_output,
                "got": output,
                "time_ms": round(runtime, 2)
            }

    return {"verdict": "AC", "time_ms": round(total_runtime, 2)}
