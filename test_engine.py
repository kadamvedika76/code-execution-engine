import json
import os
from code_exe import evaluate_submission

def load_problem(filename):
    with open(filename, "r") as f:
        return json.load(f)

def get_all_test_cases(problem):
    # combine sample and hidden
    return (
        problem["sample_testcases"] + 
        problem["hidden_testcases"]
    )



def run_test(problem_file, language, user_code):
    problem = load_problem(problem_file)
    test_cases = get_all_test_cases(problem)
    
    print(f"\n{'='*50}")
    print(f"Problem  : {problem['title']}")
    print(f"Language : {language.upper()}")
    print(f"Difficulty: {problem['difficulty']}")
    print(f"Total Test Cases: {len(test_cases)}")
    print(f"{'='*50}")
    
    verdict = evaluate_submission(user_code, language, test_cases)
    
    print(f"\nFinal Verdict: {verdict}")
    return verdict

#PYTHON SOLUTIONS
python_two_sum_correct = """
a, b = map(int, input().split())
print(a + b)
""".strip()

python_two_sum_wrong = """
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

python_factorial_wrong = """
n = int(input())
print(n * 2)
""".strip()

#C SOLUTIONS
c_two_sum_correct = """
#include <stdio.h>
int main() {
    long long a, b;
    scanf("%lld %lld", &a, &b);
    printf("%lld", a + b);
    return 0;
}
""".strip()

c_two_sum_wrong = """
#include <stdio.h>
int main() {
    long long a, b;
    scanf("%lld %lld", &a, &b);
    printf("%lld", a - b);
    return 0;
}
""".strip()

c_factorial_correct = """
#include <stdio.h>
int main() {
    long long n, result = 1;
    scanf("%lld", &n);
    for (long long i = 1; i <= n; i++) {
        result *= i;
    }
    printf("%lld", result);
    return 0;
}
""".strip()

#JAVA SOLUTIONS
java_two_sum_correct = """
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

java_two_sum_wrong = """
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

java_factorial_correct = """
import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long n = sc.nextLong();
        long result = 1;
        for (long i = 1; i <= n; i++) {
            result *= i;
        }
        System.out.println(result);
    }
}
""".strip()

#RUN ALL TESTS
print("STARTING COMPLETE TEST SUITE")

#python test
print("\n>>> PYTHON TESTS")

run_test(
    "problems/sum_two_numbers.json",
    "python",
    python_two_sum_correct    #expect AC
)

run_test(
    "problems/sum_two_numbers.json",
    "python",
    python_two_sum_wrong      #expect WA
)

run_test(
    "problems/factorial.json",
    "python",
    python_factorial_correct  #expect AC
)

run_test(
    "problems/factorial.json",
    "python",
    python_factorial_wrong    #expect WA
)

#c test
print("\n>>> C TESTS")

run_test(
    "problems/sum_two_numbers.json",
    "c",
    c_two_sum_correct         #expect AC
)

run_test(
    "problems/sum_two_numbers.json",
    "c",
    c_two_sum_wrong           #expect WA
)

run_test(
    "problems/factorial.json",
    "c",
    c_factorial_correct       #expect AC
)

#java test
print("\n>>> JAVA TESTS")

run_test(
    "problems/sum_two_numbers.json",
    "java",
    java_two_sum_correct      #expect AC
)

run_test(
    "problems/sum_two_numbers.json",
    "java",
    java_two_sum_wrong        #expect WA
)

run_test(
    "problems/factorial.json",
    "java",
    java_factorial_correct    #expect AC
)
