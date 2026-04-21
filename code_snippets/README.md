# OPL Code Snippets

A collection of minimal, self-contained code snippets for evaluating optimization benchmark functions from the OPL library. Each snippet uses [uv](https://docs.astral.sh/uv/) as the script runner and requires no manual virtual-environment setup.

## Repository Structure

Every benchmark problem has its own repository containing:

- **`call_<problem>.py`** — the evaluation script, with inline dependency metadata ([PEP 723](https://peps.python.org/pep-0723/)) so `uv` resolves everything automatically.
- **`README.md`** — problem-specific instructions covering any prerequisites (cloning external repos, running setup scripts, downloading executables, etc.) and the usage example.

**Always start by reading the README inside the problem's repository.** Some benchmarks need extra setup steps before the snippet will run.

## Quick Start

1. Install **uv** if you don't have it yet:

```bash
   pip install uv
```

2. Navigate to the problem's repository and follow its specific README.

3. Run the snippet:

```bash
   uv run call_<problem>.py
```

## Available Benchmarks

| Repository | Benchmark | Description |
|------------|-----------|-------------|
| `cocoex/` | [COCO/BBOB](https://github.com/numbbo/coco) | Evaluates function 1 from the BBOB suite (2-D) |
| `mf2/` | [mf2](https://github.com/sjvrijn/mf2) | Evaluates the Branin function at high and low fidelity |
| … | … | See the full list in the [OPL Library](#) |

## Contributing a New Snippet

1. Create a new repository (or folder) named after the problem.
2. Add a `call_<problem>.py` file with the inline dependency block at the top:
```python
   # /// script
   # dependencies = [
   #   "your-package",
   # ]
   # ///
```
3. Write your evaluation code below the dependency block.
4. Add a `README.md` that documents any setup steps a user must complete before running the script (cloning repos, installing non-Python dependencies, downloading data, etc.).
5. Update the table above to include your new benchmark.