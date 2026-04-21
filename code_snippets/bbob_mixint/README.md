# BBOB Mixed-Integer

Evaluates a function from the [COCO](https://github.com/numbbo/coco) **bbob-mixint** suite — benchmark functions with a mix of continuous and integer variables, designed for testing mixed-integer optimization algorithms.

## Prerequisites

No extra setup is needed beyond having `uv` installed. The `coco-experiment` package is resolved automatically.

## Usage

```bash
uv run call_bbob_mixint.py
```

## What the Snippet Does

The script evaluates function 1 (instance 1) from the `bbob-mixint` suite in 5 dimensions at the origin and prints the result. You can adjust the behavior by editing these variables in the script:

- **`function_indices`** — which benchmark function(s) to load (default: `1`)
- **`dimensions`** — problem dimensionality (default: `5`)
- **`instances`** — problem instance(s) (default: `1`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

## Resources

- [COCO documentation](https://numbbo.github.io/coco/)
- [bbob-mixint suite definition](https://numbbo.github.io/coco/testsuites/bbob-mixint)