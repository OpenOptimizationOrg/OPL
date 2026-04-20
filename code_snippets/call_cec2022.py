# /// script
# requires-python = "==3.10"
# dependencies = [
#   "ioh",
# ]
# ///

from ioh import get_problem, ProblemClass

### evaluation point
dim = 10
eval_point = [0.0]*dim

### input
# CEC2022 functions are numbered 1–12, dimensions must be 10 or 20
f = get_problem("CEC2022Zakharov", instance=1, dimension=10, problem_class=ProblemClass.REAL)

### print function value for eval_point
print(f(eval_point))