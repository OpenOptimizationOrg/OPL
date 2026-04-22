# BBOB Large-Scale

Evaluates a function from the [COCO](https://github.com/numbbo/coco) **bbob-largescale** suite — a set of large-scale benchmark functions designed for testing optimizers in higher dimensions.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
   pip install uv
```

No extra setup is needed beyond having `uv` installed. The `coco-experiment` package is resolved automatically.

## Usage

```bash
uv run call_bbob_largescale.py
```

## What the Snippet Does

The script evaluates function 1 (instance 1) from the `bbob-largescale` suite in 20 dimensions at the origin and prints the result. You can adjust the behavior by editing these variables in the script:

- **`function_indices`** — which benchmark function(s) to load (default: `1`)
- **`dimensions`** — problem dimensionality (default: `20`)
- **`instances`** — problem instance(s) (default: `1`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

## Resources

- [COCO documentation](https://numbbo.github.io/coco/)
- [bbob-largescale suite definition](https://coco.gforge.inria.fr/downloads/download16.00/bbob-largescale-functions.pdf)