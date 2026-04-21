# BBOB Noisy

Evaluates a function from the [COCO](https://github.com/numbbo/coco) **bbob-noisy** suite — a set of 30 noisy benchmark functions that add various noise models (Gaussian, uniform, Cauchy) to the base BBOB problems, designed for testing optimizer robustness under noisy evaluations.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
   pip install uv
```

No extra setup is needed beyond having `uv` installed. The `coco-experiment` package is resolved automatically.

## Usage

```bash
uv run call_bbob_noisy.py
```

## What the Snippet Does

The script evaluates function 1 (instance 1) from the `bbob-noisy` suite in 2 dimensions at the origin and prints the result. Since the functions are noisy, repeated evaluations at the same point may return different values. You can adjust the behavior by editing these variables in the script:

- **`function_indices`** — which benchmark function(s) to load (default: `1`)
- **`dimensions`** — problem dimensionality (default: `2`)
- **`instances`** — problem instance(s) (default: `1`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

## Resources

- [COCO documentation](https://numbbo.github.io/coco/)
- [bbob-noisy suite definition](https://numbbo.github.io/coco/testsuites/bbob-noisy)