# /// script
# requires-python = "==3.10"
# dependencies = [
#   "ioh",
# ]
# ///

import ioh

problem = ioh.problem.ManyAffine(instance = 1, n_variables = 5)

### evaluation point
dim = problem.meta_data.n_variables
eval_point = [0.0]*dim

### print function value for eval_point
print(problem(eval_point))