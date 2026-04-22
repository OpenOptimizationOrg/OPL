# IOH PBO

Evaluates a function from the [IOHexperimenter](https://github.com/IOHprofiler/IOHexperimenter) **PBO** (Pseudo-Boolean Optimization) problem class — a suite of 25 test functions defined on {0, 1}^n. All problems are maximization problems.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
pip install uv
```

No extra setup is needed beyond having `uv` installed. The `ioh` package is resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_pbo.py
```

## What the Snippet Does

The script creates PBO problem 1 (OneMax, instance 1) in 16 dimensions, evaluates it at the all-zeros bitstring, and prints the result. You can adjust the behavior by editing these variables in the script:

- **Problem ID** — the first argument to `ioh.get_problem()` selects which of the 25 functions to load (default: `1`)
- **`dim`** — problem dimensionality, i.e. bitstring length (default: `16`)
- **`instance`** — problem instance; controls transformations such as objective scaling (default: `1`)
- **`eval_point`** — the bitstring at which the function is evaluated (default: all zeros)

> **Note:** PBO problems take **integer** inputs in {0, 1}^n (not floats). The evaluation point should be a list of `0`s and `1`s.

### Available Functions

| ID | Name | ID | Name |
|----|------|----|------|
| 1 | OneMax | 14 | LeadingOnesEpistasis |
| 2 | LeadingOnes | 15 | LeadingOnesRuggedness1 |
| 3 | Linear | 16 | LeadingOnesRuggedness2 |
| 4 | OneMaxDummy1 | 17 | LeadingOnesRuggedness3 |
| 5 | OneMaxDummy2 | 18 | LABS |
| 6 | OneMaxNeutrality | 19 | IsingRing |
| 7 | OneMaxEpistasis | 20 | IsingTorus |
| 8 | OneMaxRuggedness1 | 21 | IsingTriangular |
| 9 | OneMaxRuggedness2 | 22 | MIS |
| 10 | OneMaxRuggedness3 | 23 | NQueens |
| 11 | LeadingOnesDummy1 | 24 | ConcatenatedTrap |
| 12 | LeadingOnesDummy2 | 25 | NKLandscapes |
| 13 | LeadingOnesNeutrality | | |

## Resources

- [PBO problem descriptions](https://iohprofiler.github.io/IOHproblem/PBO)
- [PBO class documentation](https://iohprofiler.github.io/IOHexperimenter/python/pbo.html)
- [PBO source code](https://github.com/IOHprofiler/IOHexperimenter/tree/master/include/ioh/problem/pbo)
- [IOHexperimenter GitHub repository](https://github.com/IOHprofiler/IOHexperimenter)