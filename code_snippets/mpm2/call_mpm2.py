# /// script
# dependencies = [
#   "numpy",
# ]
# ///

import random
import numpy as np
from mpm2 import MultiplePeaksModel2

### input
seed = 42
random.seed(seed)
np.random.seed(seed)

problem = MultiplePeaksModel2.createInstanceWithExactNumberOfOptima(
    numberOptima=4,
    numberVariables=2,
    topology="random",          # "random" or "funnel"
    shapeHeightCorrelation=0,   # -1, 0, or 1
    rotatedPeaks=True,
    peakShape="ellipse",        # "ellipse" or "sphere"
)

### evaluation point
dim = problem.numberVariables
print(f"Problem dimension: {dim}")
eval_point = [0.0]*dim

### print function value for eval_point
print(problem.objectiveFunction(eval_point))