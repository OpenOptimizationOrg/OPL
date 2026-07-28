# /// script
# dependencies = [
#   "coco-experiment",
# ]
# ///

import cocoex

### evaluation point
dim = 20
eval_point = [0.0]*dim

### input
suite_name = "bbob-largescale"

### prepare
suite = cocoex.Suite(suite_name, 
                     "instances: 1",
                     "function_indices: 1 dimensions: 20")
print(suite)

### go
for problem in suite:  # this loop may take several minutes or more
    print(problem(eval_point))