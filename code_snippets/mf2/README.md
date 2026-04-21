# mf2 Multi-Fidelity

Evaluates multi-fidelity benchmark functions from the [mf2](https://github.com/sjvrijn/mf2) library — a collection of analytical multi-fidelity test functions commonly used for benchmarking surrogate-based and multi-fidelity optimization methods.

## Prerequisites

No extra setup is needed beyond having `uv` installed. The `mf2` and `setuptools` packages are resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_mf2.py
```

## What the Snippet Does

The script evaluates the **Branin** function at both high and low fidelity in 2 dimensions at the origin and prints both results. You can adjust the behavior by editing these variables in the script:

- **Function** — replace `mf2.branin` with any available multi-fidelity function (see list below)
- **Fidelity level** — `.high()` for the expensive/accurate version, `.low()` for the cheap/approximate one
- **`dim`** — problem dimensionality (must match the chosen function's expected input dimension)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

### Available Functions

Some of the functions provided by mf2 include: `branin`, `bohachevsky`, `booth`, `currin`, `himmelblau`, `six_hump_camelback`, `hartmann3`, `hartmann6`, `park91a`, `park91b`, `borehole`, and `forrester`.

Each function exposes `.high()` and `.low()` fidelity levels, and some offer additional intermediate fidelities.

> Run `dir(mf2)` for the full list available in your installed version.

## Resources

- [mf2 documentation](https://mf2.readthedocs.io/)
- [mf2 GitHub repository](https://github.com/sjvrijn/mf2)