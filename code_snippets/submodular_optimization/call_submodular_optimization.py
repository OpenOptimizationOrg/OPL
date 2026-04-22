# /// script
# requires-python = "==3.10"
# dependencies = [
#   "ioh",
# ]
# ///
 
import ioh

### input
f = ioh.get_problem(2000, problem_class=ioh.ProblemClass.GRAPH)

### evaluation point
dim = f.meta_data.n_variables
print(f"Problem dimension: {dim}")
eval_point = [0]*dim
 
### print function value for eval_point
print(f(eval_point))