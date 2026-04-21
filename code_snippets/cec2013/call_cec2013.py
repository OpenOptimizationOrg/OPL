# /// script
# requires-python = "==3.10"
# dependencies = [
#   "ioh",
# ]
# ///

import ioh 

### evaluation point
dim = 1
eval_point = [0.0] * dim

# Create a CEC2013 problem (e.g. EqualMaxima)
# {1101: 'FivePeaks1101', 1102: 'EqualMaxima1102', 1103: 'UnevenEqualMaxima1103', 1104: 'Himmelblau1104', 1105: 'SixHumpCamelback1105', 1106: 'Shubert1106', 1107: 'Vincent1107', 1108: 'Shubert1108', 1109: 'Vincent1109', 1110: 'ModifiedRastrigin1110', 1111: 'CompositionFunction1111', 1112: 'CompositionFunction1112', 1113: 'CompositionFunction1113', 1114: 'CompositionFunction1114', 1115: 'CompositionFunction1115', 1116: 'CompositionFunction1116', 1117: 'CompositionFunction1117', 1118: 'CompositionFunction1118', 1119: 'CompositionFunction1119', 1120: 'CompositionFunction1120'}
f = ioh.iohcpp.problem.CEC2013.create("EqualMaxima1102", 1, dim)

print(f"Problem: {f.meta_data}")
print(f"Result:  {f(eval_point)}")
