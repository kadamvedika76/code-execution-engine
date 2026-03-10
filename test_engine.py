import json
from code_exe import evaluate_submission

# Choose problem file
problem_file = "problems/sum_two_numbers.json"

# Load JSON
with open(problem_file, "r") as f:
    problem = json.load(f)

# Extract hidden test cases
test_cases = problem["hidden_testcases"]

# Simulated user code
#Wrong Answer
#python
# user_code="""a, b = map(int, input().split())
# print(a - b)"""

#java
# user_code="""import java.util.*;

# public class Main {
#     public static void main(String[] args) {
#         Scanner sc = new Scanner(System.in);
#         int a = sc.nextInt();
#         int b = sc.nextInt();
#         System.out.println(a - b);
#     }
# }"""

#C
# user_code="""#include <stdio.h>

# int main() {
#     int a, b;
#     scanf("%d %d", &a, &b);
#     printf("%d", a - b);
#     return 0;
# }"""

#Runtime Error
#python
# user_code="""a = int(input())
# print(10 // 0)"""

#java
# user_code="""public class Main {
#     public static void main(String[] args) {
#         int x = 10 / 0;
#         System.out.println(x);
#     }
# }"""

#C
# user_code="""#include <stdio.h>

# int main() {
#     int a = 10 / 0;
#     printf("%d", a);
#     return 0;
# }"""

#Correct Answers
#python
user_code="""a, b = map(int, input().split())
print(a + b)"""

#java
# user_code="""import java.util.*;

# public class Main {
#     public static void main(String[] args){
#         Scanner sc = new Scanner(System.in);
#         int a = sc.nextInt();
#         int b = sc.nextInt();
#         System.out.println(a + b);
#     }
# }"""

#C
# user_code="""#include <stdio.h>

# int main() {
#     int a,b;
#     scanf("%d %d",&a,&b);
#     printf("%d",a+b);
#     return 0;
# }"""


language = "python"

print("Problem:", problem["title"])
print()

# Run the code engine
verdict = evaluate_submission(user_code, language, test_cases)

print("\nFinal Verdict:", verdict)