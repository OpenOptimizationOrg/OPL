# BBOB

Evaluates a function from the [COCO](https://github.com/numbbo/coco) **bbob** suite — the core set of 24 noiseless single-objective benchmark functions widely used for comparing continuous optimizers.

## Prerequisites

No extra setup is needed beyond having `uv` installed. The `coco-experiment` package is resolved automatically.

## Usage

```bash
uv run call_bbob.py
```

## What the Snippet Does

The script evaluates function 1 (instance 1) from the `bbob` suite in 2 dimensions at the origin and prints the result. You can adjust the behavior by editing these variables in the script:

- **`function_indices`** — which benchmark function(s) to load (default: `1`)
- **`dimensions`** — problem dimensionality (default: `2`)
- **`instances`** — problem instance(s) (default: `1`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

## Resources

- [COCO documentation](https://numbbo.github.io/coco/)
- [bbob suite function definitions](https://numbbo.github.io/coco/testsuites/bbob)