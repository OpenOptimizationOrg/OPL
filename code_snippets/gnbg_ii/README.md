# GNBG

Evaluates functions from the **GNBG benchmark suite**, a set of structured multimodal optimization problems defined via parameter files (`.mat`) and evaluated through a Python implementation.

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/) if you don't have it yet:

```bash
   pip install uv
```

No extra setup is needed beyond having `uv` installed. The required dependencies are:

* `numpy`
* `scipy`

These are resolved automatically via the script header.

## Setup

1. Download or clone the GNBG repository:

   ```
   https://github.com/rohitsalgotra/GNBG-II
   ```

2. Extract the Python instances:

   ```
   GNBG_Instances.Python-main.zip
   ```

3. Place the extracted folder in your project directory:

```
project/
│
├── gnbg.py
├── call_gnbg.py
└── GNBG_Instances.Python-main/
    ├── f1.mat
    ├── ...
```

## Usage

```bash
uv run call_gnbg.py
```

## What the Snippet Does

The script:

1. Loads a GNBG problem instance (e.g. `f1.mat`)
2. Constructs the corresponding benchmark function
3. Evaluates it at a given point
4. Prints the result

The implementation is split into:

* **`gnbg.py`** — contains the GNBG class and loader (reusable) 
* **`call_gnbg.py`** — minimal runner script 

`call_gnbg.py` depends on `gnbg.py`, so both files must be present in the same directory.

## Key Parameters

Edit these in `call_gnbg.py`:

* **`problem_index`** — which GNBG function to load (`1`–`24`)
* **`repo_dir`** — path to the folder containing the `.mat` files
* **`eval_point`** — evaluation point

Example:

```python
problem_index = 1
eval_point = np.zeros(problem.Dimension)
```

## Resources

* GNBG repository:
  [https://github.com/rohitsalgotra/GNBG-II](https://github.com/rohitsalgotra/GNBG-II)

* Benchmark description:
  Generalized Numerical Benchmark Generator (GNBG)


