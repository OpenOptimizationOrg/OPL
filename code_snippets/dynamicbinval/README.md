# IOH DynamicBinVal

Evaluates the **DynamicBinValUniform** problem from the [IOHexperimenter](https://github.com/IOHprofiler/IOHexperimenter) — a dynamic pseudo-Boolean benchmark where bit weights change over time, used for studying the behavior of discrete optimizers under non-static objective functions.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
   pip install uv
```

No extra setup is needed beyond having `uv` installed. The `ioh` package is resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_dynamicbinval.py
```

## What the Snippet Does

The script creates the `DynamicBinValUniform` problem (instance 1, integer problem class) in 32 dimensions, evaluates it at the all-zeros bit string, and prints the result. You can adjust the behavior by editing these variables in the script:

- **Problem name** — replace `"DynamicBinValUniform"` with other dynamic binary-value variants if available
- **`dim`** — number of bits / problem dimensionality (default: `32`)
- **`instance`** — problem instance (default: `1`)
- **`eval_point`** — the bit string at which the function is evaluated (default: all zeros)

## Resources

- [IOHexperimenter documentation](https://iohprofiler.github.io/IOHexperimenter/)
- [IOH problem registry](https://iohprofiler.github.io/IOHexperimenter/python/problem_overview.html)