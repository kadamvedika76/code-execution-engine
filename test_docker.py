import json
from docker_executor import evaluate_submission




def load_problem(filename):
    with open(filename, "r") as f:
        return json.load(f)

def get_all_test_cases(problem):
    return (
        problem["sample_testcases"] +
        problem["hidden_testcases"]
    )

def run_test(problem_file, language, code, label):
    problem = load_problem(problem_file)
    test_cases = get_all_test_cases(problem)

    print(f"\n{'='*50}")
    print(f"Problem  : {problem['title']}")
    print(f"Language : {language.upper()}")
    print(f"Test     : {label}")
    print(f"{'='*50}")

    result = evaluate_submission(code, language, test_cases)
    print(f"Final Verdict: {result}")
    return result


python_sum_correct = """
a, b = map(int, input().split())
print(a + b)
""".strip()

python_sum_wrong = """
a, b = map(int, input().split())
print(a - b)
""".strip()

python_factorial_correct = """
n = int(input())
result = 1
for i in range(1, n + 1):
    result *= i
print(result)
""".strip()


c_sum_correct = """
#include <stdio.h>
int main() {
    long long a, b;
    scanf("%lld %lld", &a, &b);
    printf("%lld", a + b);
    return 0;
}
""".strip()

c_sum_wrong = """
#include <stdio.h>
int main() {
    long long a, b;
    scanf("%lld %lld", &a, &b);
    printf("%lld", a - b);
    return 0;
}
""".strip()

java_sum_correct = """
import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long a = sc.nextLong();
        long b = sc.nextLong();
        System.out.println(a + b);
    }
}
""".strip()

java_sum_wrong = """
import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long a = sc.nextLong();
        long b = sc.nextLong();
        System.out.println(a - b);
    }
}
""".strip()

python_tle = """
while True:
    pass
""".strip()

c_ce = """
this is not c code
""".strip()

c_re = """
#include <stdio.h>
int main() {
    int a = 10 / 0;
    printf("%d", a);
    return 0;
}
""".strip()

python_attack = """
import os
os.system("rm -rf /")
print("hacked")
""".strip()

print("\n" + "="*50)
print("DOCKER EXECUTION ENGINE TEST SUITE")
print("="*50)


print("\n>>> PYTHON TESTS")
run_test("problems/sum_two_numbers.json", "python", python_sum_correct, "AC expected")
run_test("problems/sum_two_numbers.json", "python", python_sum_wrong, "WA expected")
run_test("problems/factorial.json", "python", python_factorial_correct, "AC expected")
run_test("problems/sum_two_numbers.json", "python", python_tle, "TLE expected")
run_test("problems/sum_two_numbers.json", "python", python_attack, "Security test")

print("\n>>> C TESTS")
run_test("problems/sum_two_numbers.json", "c", c_sum_correct, "AC expected")
run_test("problems/sum_two_numbers.json", "c", c_sum_wrong, "WA expected")
run_test("problems/sum_two_numbers.json", "c", c_ce, "CE expected")
run_test("problems/sum_two_numbers.json", "c", c_re, "RE expected")

print("\n>>> JAVA TESTS")
run_test("problems/sum_two_numbers.json", "java", java_sum_correct, "AC expected")
run_test("problems/sum_two_numbers.json", "java", java_sum_wrong, "WA expected")