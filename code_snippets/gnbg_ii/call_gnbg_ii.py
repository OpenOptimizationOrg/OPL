# /// script
# dependencies = [
#   "numpy",
#   "scipy",
# ]
# ///

import numpy as np
from gnbg import load_gnbg_instance

### input
repo_dir = "GNBG_Instances.Python-main"
problem_index = 1

### prepare
problem = load_gnbg_instance(repo_dir, problem_index)
print(problem)

### evaluation point
eval_point = np.zeros(problem.Dimension)

### go
print(problem(eval_point))