# IOH CEC2013 Niching

Evaluates a function from the [IOHexperimenter](https://github.com/IOHprofiler/IOHexperimenter) **CEC2013 niching** benchmark suite — a set of 20 multimodal problems used for testing niching and multi-modal optimization algorithms.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
   pip install uv
```

No extra setup is needed beyond having `uv` installed. The `ioh` package is resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_cec2013.py
```

## What the Snippet Does

The script creates the `EqualMaxima1102` problem from the CEC2013 suite in 1 dimension, evaluates it at the origin, and prints the result. You can adjust the behavior by editing these variables in the script:

- **Problem name** — replace `"EqualMaxima1102"` with any of the 20 available functions (see table below)
- **`dim`** — problem dimensionality (default: `1`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

### Available Functions

| ID | Name |
|----|------|
| 1101 | FivePeaks |
| 1102 | EqualMaxima |
| 1103 | UnevenEqualMaxima |
| 1104 | Himmelblau |
| 1105 | SixHumpCamelback |
| 1106 | Shubert |
| 1107 | Vincent |
| 1108 | Shubert |
| 1109 | Vincent |
| 1110 | ModifiedRastrigin |
| 1111–1120 | CompositionFunction |

## Resources

- [IOHexperimenter documentation](https://iohprofiler.github.io/IOHexperimenter/)
- [CEC2013 niching competition](https://bee22.com/resources/CEC%202013-Niching%20Methods%20for%20Multimodal%20Optimization.pdf)