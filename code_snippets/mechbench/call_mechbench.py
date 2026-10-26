# /// script
# dependencies = [
#   "numpy",
#   "MECHBench @ git+https://github.com/BayesOptApp/MECHBench.git",
# ]
# ///

import sys
import os
import numpy as np
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "MECHBench__"))
from src import sob

### input
sim_id = 1          # unique ID for this simulation run (used to name results folder)
problem_id = 1      # 1: Star Box, 2: Three-Point Bending, 3: Crash Tube
dim = 5             # number of design variables

runnerOptions = {
    "np": 1,        # number of MPI processes
    "nt": 1,        # number of OpenMP threads
    "h_level": 1,   # mesh refinement level (higher = finer, slower)
    "gmsh_verbosity": 0,
    "write_vtk": False,
}

### create problem instance
f = sob.get_problem(problem_id, dim, runner_options=runnerOptions)

### evaluation point
eval_point = np.zeros(dim).tolist()

### print function value for eval_point
print(f"Problem ID: {problem_id}, dim: {dim}")
print(f"Objective value: {f(eval_point, sim_id)}")