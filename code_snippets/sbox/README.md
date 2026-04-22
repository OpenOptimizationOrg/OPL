# IOH BBOB (SBOX)

Evaluates a function from the [IOHexperimenter](https://github.com/IOHprofiler/IOHexperimenter) **SBOX** problem class(strict box-constrained problems) — a re-implementation of the 24 noiseless real-valued BBOB test functions supported on [-5, 5]^n.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
   pip install uv
```

No extra setup is needed beyond having `uv` installed. The `ioh` package is resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_sbox.py
```

## What the Snippet Does

The script creates SBOX problem 1 (instance 1) in 2 dimensions, evaluates it at the origin, and prints the result. You can adjust the behavior by editing these variables in the script:

- **Problem ID** — the first argument to `ioh.get_problem()` selects which of the 24 functions to load (default: `1`)
- **`dim`** — problem dimensionality (default: `2`)
- **`instance`** — problem instance (default: `1`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

### Available Functions

| ID | Name |
|----|------|
| 1 | Sphere |
| 2 | Ellipsoid |
| 3 | Rastrigin |
| 4 | BuecheRastrigin |
| 5 | LinearSlope |
| 6 | AttractiveSector |
| 7 | StepEllipsoid |
| 8 | Rosenbrock |
| 9 | RosenbrockRotated |
| 10 | EllipsoidRotated |
| 11 | Discus |
| 12 | BentCigar |
| 13 | SharpRidge |
| 14 | DifferentPowers |
| 15 | RastriginRotated |
| 16 | Weierstrass |
| 17 | Schaffers10 |
| 18 | Schaffers1000 |
| 19 | GriewankRosenbrock |
| 20 | Schwefel |
| 21 | Gallagher101 |
| 22 | Gallagher21 |
| 23 | Katsuura |
| 24 | LunacekBiRastrigin |

## Resources

- [SBOX class documentation](https://iohprofiler.github.io/IOHexperimenter/api/ioh.iohcpp.problem.SBOX.html)
- [IOHexperimenter BBOB & SBOX overview](https://iohprofiler.github.io/IOHexperimenter/python/bbob.html)
- [IOHexperimenter GitHub repository](https://github.com/IOHprofiler/IOHexperimenter)