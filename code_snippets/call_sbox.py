# /// script
# dependencies = [
#   "ioh",
# ]
# ///

import ioh

### evaluation point
dim = 2
eval_point = [0.0]*dim

### input
f = ioh.get_problem(1, instance=1, dimension=dim, problem_class=ioh.ProblemClass.SBOX)

### print function value for eval_point
print(f(eval_point))