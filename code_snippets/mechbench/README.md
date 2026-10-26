# MECHBench

Evaluates a function from [MECHBench](https://github.com/BayesOptApp/MECHBench) — a benchmark suite of structural mechanics optimisation problems powered by [OpenRadioss](https://openradioss.org) finite element simulations. It provides three real-world crash and bending test cases with continuous design variables, supporting single-objective, multi-objective, constrained, and unconstrained problem formulations.

> [!WARNING]
> MECHBench only runs on **Linux** and **Windows**. OpenRadioss provides no macOS binaries, and MECHBench raises `ValueError: Unsupported platform` on startup.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
pip install uv
```

2. Clone the MECHBench repository into the same folder as `call_mechbench.py`:

```bash
git clone https://github.com/BayesOptApp/MECHBench.git
```

Your directory should look like:

```
├── call_mechbench.py
└── MECHBench/
    ├── main.py
    ├── src/
    │   └── sob/
    │       └── ...
    └── requirements.txt
```

## Usage

```bash
uv run call_mechbench.py
```

OpenRadioss binaries are downloaded automatically on first run if not already present.

## What the Snippet Does

The script instantiates a MECHBench problem, evaluates it at the zero vector, and prints the objective value. You can adjust the behaviour by editing these variables in the script:

- **`problem_id`** — selects the mechanical test case:
  - `1` — Star Box (crash box with a star-shaped cross-section)
  - `2` — Three-Point Bending (structural beam under transverse load)
  - `3` — Crash Tube (thin-walled tube with trigger geometry optimisation)
- **`dim`** — number of design variables (problem dimensionality)
- **`sim_id`** — unique integer ID for the simulation run; results are stored in a folder named after this ID
- **`eval_point`** — the design vector at which the objective is evaluated (default: all zeros)
- **`runnerOptions`** — dictionary controlling the FEM solver:
  - `np` — number of MPI processes (default: `1`)
  - `nt` — number of OpenMP threads per process (default: `1`)
  - `h_level` — mesh refinement level; higher values increase resolution and cost (default: `1`)
  - `gmsh_verbosity` — GMSH output verbosity; `0` = silent (default: `0`)
  - `write_vtk` — export results in VTK format for visualisation (default: `False`)
  - `open_radioss_main_path` *(optional)* — path to a custom OpenRadioss installation

### How MECHBench Works

Each problem wraps an explicit FEM simulation. The design vector is mapped to geometric or material parameters of a structural model. MECHBench then: generates a mesh via GMSH, assembles the FEM model, runs an OpenRadioss simulation, and post-processes the output to return one or more scalar metrics (e.g., absorbed energy, intrusion, peak force). The objective function is a callable `f` obtained via `sob.get_problem(problem_id, dim)` and evaluated as `f(vector, sim_id)`.

### Available Metrics

| Metric | Requires FEM Simulation | Notes |
|---|---|---|
| `mass` | No | |
| `absorbed_energy` | No | |
| `specific_energy_absorbed` | No | Derived from `mass` and `absorbed_energy` |
| `intrusion` | Yes | |
| `mean_impact_force` | Yes | |
| `peak_impact_force` | Yes | |
| `usage_ratio` | Yes | Derived from impact forces |
| `load_uniformity` | Yes | Derived from impact forces |
| `penalized_sea` | Yes | Only for Problem 1 |
| `penalized_mass` | Yes | Only for Problem 2 |

By default `sob.get_problem` returns a single-objective function. To access multiple metrics or define constrained problems, pass a `target_metric` argument (string or list of strings) to `sob.get_problem`.

## Resources

- [MECHBench GitHub repository](https://github.com/BayesOptApp/MECHBench)
- [OpenRadioss](https://openradioss.org)