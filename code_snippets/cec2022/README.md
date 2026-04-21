# IOH CEC2022

Evaluates a function from the [IOHexperimenter](https://github.com/IOHprofiler/IOHexperimenter) **CEC2022** benchmark suite — 12 single-objective bound-constrained problems used in the CEC2022 competition on real-parameter optimization.

## Prerequisites

No extra setup is needed beyond having `uv` installed. The `ioh` package is resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_cec2022.py
```

## What the Snippet Does

The script creates the `CEC2022Zakharov` problem (instance 1) in 10 dimensions, evaluates it at the origin, and prints the result. You can adjust the behavior by editing these variables in the script:

- **Problem name** — replace `"CEC2022Zakharov"` with any of the 12 available functions (see table below)
- **`dimension`** — must be **10** or **20**
- **`instance`** — problem instance (default: `1`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

### Available Functions

| # | Name |
|---|------|
| 1 | CEC2022Zakharov |
| 2 | CEC2022Rosenbrock |
| 3 | CEC2022Schaffer |
| 4 | CEC2022StepRastrigin |
| 5 | CEC2022Levy |
| 6 | CEC2022HybridFunction1 |
| 7 | CEC2022HybridFunction2 |
| 8 | CEC2022HybridFunction3 |
| 9 | CEC2022CompositionFunction1 |
| 10 | CEC2022CompositionFunction2 |
| 11 | CEC2022CompositionFunction3 |
| 12 | CEC2022CompositionFunction4 |

> **Note:** The function names above are approximate. Run `ioh.get_problem?` or check the IOHexperimenter docs for the exact strings accepted by `get_problem()`.

## Resources

- [IOHexperimenter documentation](https://iohprofiler.github.io/IOHexperimenter/)
- [CEC2022 competition technical report](https://www3.ntu.edu.sg/home/epnsugan/index_files/CEC2022/CEC2022.htm)