# /// script
# requires-python = "==3.10"
# dependencies = [
#   "mf2",
#   "setuptools == 80",
# ]
# ///

import mf2

### evaluation point
dim = 2
eval_point = [0.0]*dim

# dir(mf2)

print(mf2.branin.high(eval_point))
print(mf2.branin.low(eval_point))