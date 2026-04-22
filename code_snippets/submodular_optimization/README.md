# IOH Submodular Optimization

Evaluates a function from the [IOHexperimenter](https://github.com/IOHprofiler/IOHexperimenter) **Submodular** problem class — a suite of submodular optimization problems on graphs, including Maximum Cut, Maximum Coverage, Maximum Influence, and Pack While Travel. All problems are binary maximization problems on {0, 1}^n.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
pip install uv
```

No extra setup is needed beyond having `uv` installed. The `ioh` package is resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_submodular_optimization.py
```

## What the Snippet Does

The script creates GRAPH problem 2000 (MaxCut), evaluates it at the all-zeros bitstring, and prints the result. You can adjust the behavior by editing these variables in the script:

- **Problem ID** — the first argument to `ioh.get_problem()` selects which problem to load (default: `2000`)
- **`eval_point`** — the bitstring at which the function is evaluated (default: all zeros)

> **Note:** GRAPH problems take **integer** inputs in {0, 1}^n (not floats). The dimensionality is determined by the problem (i.e. the underlying graph) and cannot be set manually.

### Available Functions

| ID Range | Problem Type | Count | Dimensions |
|---|---|---|---|
| 2000 – 2004 | MaxCut | 5 | 800 |
| 2100 – 2139 | MaxCoverage | 40 | 204 – 760 |
| 2200 – 2223 | MaxInfluence | 24 | 4039 |
| 2300 – 2308 | PackWhileTravel | 9 | 279 – 338090 |

## Resources

- [Submodular competition example notebook](https://github.com/IOHprofiler/IOHexperimenter/blob/master/example/Competitions/Submodular/example_submodular.ipynb)
- [GECCO 2025 Evolutionary Submodular Optimisation Competition](https://cs.adelaide.edu.au/~optlog/CompetitionESO2025.php)
- [Benchmarking paper (Neumann et al.)](https://scholarlypublications.universiteitleiden.nl/access/item:3731696/view)
- [IOHexperimenter GitHub repository](https://github.com/IOHprofiler/IOHexperimenter)