import subprocess
import tempfile
import os
import time

def clean_output(text):
    return text.strip()

def run_python(code, input_data):
    filename = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(code.encode())
            filename = f.name

        start = time.time()
        result = subprocess.run(
            ["python", filename],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=2
        )
        runtime = (time.time() - start) * 1000

        if result.returncode != 0:
            return "RE", result.stderr, runtime

        return result.stdout.strip(), result.stderr, runtime

    except subprocess.TimeoutExpired:
        return "TLE", None, 2000

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

def run_c(code, input_data):
    c_file = None
    exe_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as f:
            f.write(code.encode())
            c_file = f.name

        exe_file = c_file[:-2] + ".exe"

        compile_process = subprocess.run(
            ["gcc", c_file, "-o", exe_file],
            capture_output=True,
            text=True
        )

        if compile_process.returncode != 0:
            return "CE", compile_process.stderr, 0

        start = time.time()
        run_process = subprocess.run(
            [exe_file],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=2
        )
        runtime = (time.time() - start) * 1000

        if run_process.returncode != 0:
            return "RE", run_process.stderr, runtime

        return run_process.stdout.strip(), run_process.stderr, runtime

    except subprocess.TimeoutExpired:
        return "TLE", None, 2000

    finally:
        if c_file and os.path.exists(c_file): os.remove(c_file)
        if exe_file and os.path.exists(exe_file): os.remove(exe_file)

def run_java(code, input_data):
    try:
        with open("Main.java", "w") as f:
            f.write(code)

        compile_process = subprocess.run(
            ["javac", "Main.java"],
            capture_output=True,
            text=True
        )

        if compile_process.returncode != 0:
            return "CE", compile_process.stderr, 0

        start = time.time()
        run_process = subprocess.run(
            ["java", "Main"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=2
        )
        runtime = (time.time() - start) * 1000

        if run_process.returncode != 0:
            return "RE", run_process.stderr, runtime

        return run_process.stdout.strip(), run_process.stderr, runtime

    except subprocess.TimeoutExpired:
        return "TLE", None, 2000

    finally:
        if os.path.exists("Main.java"): os.remove("Main.java")
        if os.path.exists("Main.class"): os.remove("Main.class")

def evaluate_submission(code, language, test_cases):
    total_runtime = 0

    for i, case in enumerate(test_cases, start=1):
        input_data = case["input"]
        expected_output = case["output"]

        if language == "python":
            output, error, runtime = run_python(code, input_data)
        elif language == "c":
            output, error, runtime = run_c(code, input_data)
        elif language == "java":
            output, error, runtime = run_java(code, input_data)
        else:
            return {"verdict": "Unsupported Language"}

        total_runtime += runtime

        if output == "TLE":
            return {"verdict": "TLE", "test_case": i, "time_ms": 2000}

        if output == "CE":
            return {"verdict": "CE", "error": error, "test_case": i}

        if output == "RE":
            return {"verdict": "RE", "error": error, "test_case": i}

        if clean_output(output) == clean_output(expected_output):
            print(f"Test Case {i} → PASS ({runtime:.1f}ms)")
        else:
            return {
                "verdict": "WA",
                "test_case": i,
                "expected": expected_output,
                "got": output,
                "time_ms": round(runtime, 2)
            }

    return {"verdict": "AC", "time_ms": round(total_runtime, 2)}