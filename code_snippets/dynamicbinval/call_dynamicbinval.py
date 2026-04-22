# /// script
# requires-python = "==3.10"
# dependencies = [
#   "ioh",
# ]
# ///

from ioh import get_problem, ProblemClass

### evaluation point
dim = 32
eval_point = [0]*dim

### input
f = get_problem("DynamicBinValUniform", 1, 32, ProblemClass.INTEGER)

### print function value for eval_point
print(f(eval_point))