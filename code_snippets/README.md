# OPL Code Snippets

A collection of code snippets for evaluating optimization benchmark functions from the OPL library using [uv](https://docs.astral.sh/uv/) as the script runner.

## Prerequisites

Install **uv** (if not already installed):

```bash
pip install uv
```

## Usage

Each snippet is a self-contained script with inline dependency metadata ([PEP 723](https://peps.python.org/pep-0723/)). No virtual environment setup is needed — `uv` resolves dependencies automatically.

Run any snippet with:

```bash
uv run call_<problem>.py
```

## Available Snippets

| Script | Benchmark | Description |
|--------|-----------|-------------|
| `call_cocoex.py` | [COCO/BBOB](https://github.com/numbbo/coco) | Evaluates function 1 from the BBOB suite (2D) |
| `call_mf2.py` | [mf2](https://github.com/sjvrijn/mf2) | Evaluates the Branin function at high and low fidelity |
| All other problems from the OPL Library |

## Example

```bash
# Run the COCO/BBOB snippet
uv run call_cocoex.py

# Run the multi-fidelity mf2 snippet
uv run call_mf2.py
```

## Adding New Snippets

1. Create a new file named `call_<problem>.py`.
2. Add the inline dependency block at the top of the file:
   ```python
   # /// script
   # dependencies = [
   #   "your-package",
   # ]
   # ///
   ```
3. Write your evaluation code below it.
4. Run with `uv run call_<problem>.py`.