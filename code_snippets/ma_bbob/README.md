# IOH MA-BBOB (ManyAffine)

Evaluates a function from the [IOHexperimenter](https://github.com/IOHprofiler/IOHexperimenter) **MA-BBOB** problem generator — a method for creating arbitrary affine combinations of the 24 noiseless BBOB test functions, supported on [-5, 5]^n.

MA-BBOB extends the classic BBOB suite by blending its base functions with random weights, shifts, and per-function instance transformations. The `instance` parameter seeds this generation procedure, so the same instance ID always produces the same function.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
pip install uv
```

No extra setup is needed beyond having `uv` installed. The `ioh` package is resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_ma_bbob.py
```

## What the Snippet Does

The script creates an MA-BBOB problem (instance 1) in 5 dimensions, evaluates it at the origin, and prints the result. You can adjust the behavior by editing these variables in the script:

- **`instance`** — seeds the random generation of weights, sub-problem instances, and optimum location (default: `1`)
- **`n_variables`** — problem dimensionality (default: `5`; the GECCO competition uses `2` and `5`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

### Advanced Constructor

In addition to the simple `(instance, n_variables)` constructor, `ManyAffine` also accepts explicit control over the combination:

```python
ioh.problem.ManyAffine(
    xopt,           # list[float]     — location of the optimum
    weights,        # list[float, 24] — weight per BBOB base function
    instances,      # list[int, 24]   — instance ID per base function
    n_variables,    # int             — search space dimensionality
    scale_factors,  # list[float, 24] — (optional) scaling per base function
)
```

### Readable Properties

| Property | Description |
|---|---|
| `weights` | The 24 combination weights |
| `instances` | The 24 sub-problem instance IDs |
| `scale_factors` | The 24 per-function scaling factors |
| `sub_problems` | The 24 underlying BBOB problem objects |
| `function_values` | Current function values of the sub-problems |

### Underlying BBOB Base Functions

| ID | Name | ID | Name |
|----|------|----|------|
| 1 | Sphere | 13 | SharpRidge |
| 2 | Ellipsoid | 14 | DifferentPowers |
| 3 | Rastrigin | 15 | RastriginRotated |
| 4 | BuecheRastrigin | 16 | Weierstrass |
| 5 | LinearSlope | 17 | Schaffers10 |
| 6 | AttractiveSector | 18 | Schaffers1000 |
| 7 | StepEllipsoid | 19 | GriewankRosenbrock |
| 8 | Rosenbrock | 20 | Schwefel |
| 9 | RosenbrockRotated | 21 | Gallagher101 |
| 10 | EllipsoidRotated | 22 | Gallagher21 |
| 11 | Discus | 23 | Katsuura |
| 12 | BentCigar | 24 | LunacekBiRastrigin |

## Resources

- [MA-BBOB paper (arXiv:2312.11083)](https://arxiv.org/abs/2312.11083)
- [GECCO 2025 MA-BBOB Competition](https://iohprofiler.github.io/competitions/mabbob25)
- [Example notebook](https://github.com/IOHprofiler/IOHexperimenter/blob/master/example/Competitions/MA-BBOB/Example_MABBOB.ipynb)
- [IOHexperimenter GitHub repository](https://github.com/IOHprofiler/IOHexperimenter)