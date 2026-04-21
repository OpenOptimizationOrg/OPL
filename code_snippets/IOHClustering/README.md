# IOH Clustering

Evaluates a function from the [IOHclustering](https://github.com/IOHprofiler/IOHClustering) benchmark suite — a set of continuous black-box optimization problems derived from data clustering tasks, integrated with the [IOHprofiler](https://github.com/IOHprofiler) framework.

Each problem encodes a k-means-style clustering objective: the search vector represents `k` cluster centers in a 2D feature space (after PCA or feature selection), so the problem dimensionality is `k × 2`. All variables are bounded in `[0, 1]`.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
pip install uv
```

No extra setup is needed beyond having `uv` installed. The `ioh` and `iohclustering` packages are resolved automatically.

> **Note:** This snippet requires **Python 3.10**. The inline metadata enforces this via `requires-python = "==3.10"`. Make sure a Python 3.10 interpreter is available on your system.

## Usage

```bash
uv run call_clustering.py
```

## What the Snippet Does

The script creates clustering problem 5 (`iris_pca`) with `k=2` clusters, evaluates it at the origin, and prints the result. You can adjust the behavior by editing these variables in the script:

- **`fid`** — problem ID (integer) or dataset name (string) passed to `get_problem()` (default: `5`)
- **`k`** — number of cluster centers (default: `2`; available values: `2`, `3`, `5`, `10`)
- **`instance`** — problem instance for transformation-based generalization (default: `1`)
- **`eval_point`** — the point at which the function is evaluated (default: all zeros)

> **Note:** `get_problem()` returns a tuple `(problem, retransform)`. The `retransform` function converts a solution vector back into cluster center coordinates in the original data space.

### Available Datasets

| ID | Name |
|----|------|
| 1 | breast_pca |
| 2 | diabetes_pca |
| 3 | german_postal_selected |
| 4 | glass_pca |
| 5 | iris_pca |
| 6 | kc1_pca |
| 7 | mfeat-fourier_pca |
| 8 | ruspini_selected |
| 9 | segment_pca |
| 10 | wine_pca |

### Available Values of k

| k | Dimensionality |
|---|----------------|
| 2 | 4 |
| 3 | 6 |
| 5 | 10 |
| 10 | 20 |

## Resources

- [IOHClustering GitHub repository](https://github.com/IOHprofiler/IOHClustering)
- [IOHexperimenter GitHub repository](https://github.com/IOHprofiler/IOHexperimenter)
- [Benchmark paper (arXiv)](https://arxiv.org/abs/2505.09233)