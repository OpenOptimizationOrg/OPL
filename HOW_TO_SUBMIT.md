# How to submit problems to OPL

Thank you for contributing to the Optimisation Problem Library (OPL)!
This guide explains, step by step, how to get your optimisation problem, benchmark suite, or problem generator into the library.

There are two ways to submit:

| | [Option A: Edit `problems.yaml`](#option-a-pull-request-that-edits-problemsyaml) | [Option B: Submit a Python script](#option-b-submit-a-python-script) |
|---|---|---|
| **You write** | YAML entries directly in `problems.yaml` | A Python script that builds your entries using the `opltools` package |
| **Best for** | One problem or a few problems | Suites with many similar problems, entries you want to generate in a loop, or if you prefer Python over YAML |
| **Who generates the YAML** | You | We do. We run your script and merge the output into `problems.yaml` |
| **Requires git / GitHub** | Yes (fork + pull request) | Preferred, but you can also send the script by issue or email |

Both options use the same data model, which is described in [SCHEMA.md](SCHEMA.md).
Read [Step 0](#step-0-before-you-start-applies-to-both-options) first, then follow **one** of the two options.

If you would rather not deal with YAML or Python at all, you can also use the [submission form](https://docs.google.com/forms/d/e/1FAIpQLSehQp24AuFAH2j9jizDhq8K_BYgNGMKXWTMu6s-2RwEJrK59Q/viewform?usp=sharing&ouid=107462254722022409950) (see the [README](README.md#how-to-add-problems)).

---

## Contents

- [Step 0: Before you start (applies to both options)](#step-0-before-you-start-applies-to-both-options)
  - [0.1 Check that your problem isn't already in OPL](#01-check-that-your-problem-isnt-already-in-opl)
  - [0.2 Decide what kinds of entries you need](#02-decide-what-kinds-of-entries-you-need)
  - [0.3 Choose IDs](#03-choose-ids)
  - [0.4 Collect the information](#04-collect-the-information)
  - [0.5 Set up the tools](#05-set-up-the-tools)
- [Option A: Pull request that edits `problems.yaml`](#option-a-pull-request-that-edits-problemsyaml)
- [Option B: Submit a Python script](#option-b-submit-a-python-script)
- [Field cheat sheet](#field-cheat-sheet)
- [Common mistakes](#common-mistakes)
- [Optional: Add a code snippet](#optional-add-a-code-snippet)
- [What happens after you submit](#what-happens-after-you-submit)
- [Getting help](#getting-help)

---

## Step 0: Before you start (applies to both options)

### 0.1 Check that your problem isn't already in OPL

Search the [OPL website](https://openoptimizationorg.github.io/OPL/) or `problems.yaml` for the name of your problem:

```bash
grep -n -i "wind farm" problems.yaml
```

If it is already listed but the entry is incomplete or wrong, please **update the existing entry** instead of adding a new one.
Use the same process described below.

### 0.2 Decide what kinds of entries you need

OPL knows four kinds of entries ("things"). Each entry has a `type` field that says which one it is:

| `type` | Use it for | Example |
|---|---|---|
| `problem` | A single optimisation problem (possibly with several instances) | The Sphere function |
| `suite` | A fixed, curated collection of problems that are listed explicitly | BBOB (24 functions) |
| `generator` | A parametric family that creates problems on demand, so the members are not listed | MPM2, W-model |
| `implementation` | A piece of code that implements one or more problems, suites, or generators | The COCO platform, a PyPI package |

Typical submissions look like one of these:

- **One problem with code:** one `problem` and one `implementation`. The problem refers to the implementation.
- **A benchmark suite:** one `implementation`, one `problem` per function, and one `suite` that lists the problems.
  If listing every problem is not practical, a `suite` without a `problems` field is fine too. Describe its properties (variables, objectives, ...) directly on the suite.
- **A generator:** one `generator` and one `implementation`.

If an implementation already exists in OPL (for example `impl_coco`, `impl_iohexperimenter`, or `impl_pymoo`), **reuse its ID** instead of creating a duplicate.
To list all existing implementation IDs, run:

```bash
grep -n "^impl_" problems.yaml
```

### 0.3 Choose IDs

Every entry is stored under a unique **ID**.
IDs are lower-case, use underscores, and start with a prefix that matches the entry's type:

| Prefix | Type | Example ID |
|---|---|---|
| `fn_` | problem | `fn_wind_farm_layout` |
| `suite_` | suite | `suite_bbob` |
| `gen_` | generator | `gen_mpm2` |
| `impl_` | implementation | `impl_coco` |

Entries refer to each other by ID. For example, a problem lists its implementations in `implementations: [impl_xyz]`, and a suite lists its problems in `problems: [fn_a, fn_b]`.
Every ID you refer to **must exist** in the library, either already in `problems.yaml` or added in your submission.

### 0.4 Collect the information

Collect the following before you start writing. Leave out anything you don't know. Only `name` is required for problems, suites, and generators. `name` and `description` are required for implementations.

- Name, an optional longer name, and a description. The description can be several paragraphs and may use Markdown.
- Number of objectives.
- Decision variables: their types (continuous / integer / binary / categorical) and how many of each.
- Constraints: their types (box / linear / function), whether they are hard or soft, equality or inequality, and how many there are.
- Noise, dynamics, multimodality, multi-fidelity, and whether the problem is real-world or artificial.
- Approximate time to evaluate one solution.
- References: the paper that defines the problem, and optionally papers that use or critique it.
- Links to the code (repository, package, ...) and its language.

The [field cheat sheet](#field-cheat-sheet) below lists every field and what goes in it.

### 0.5 Set up the tools

You need [git](https://git-scm.com/), a GitHub account, and [uv](https://docs.astral.sh/uv/getting-started/installation/), which installs Python and the `opltools` package for you.

1. Fork <https://github.com/OpenOptimizationOrg/OPL> on GitHub. Click **Fork** at the top right of the repository page.
2. Clone your fork and create a branch for your submission:

   ```bash
   git clone https://github.com/<your-github-user>/OPL.git
   cd OPL
   git checkout -b add-wind-farm-layout
   ```

3. Install the project and its dependencies:

   ```bash
   uv sync
   ```

4. Check that everything works by validating the current library:

   ```bash
   uv run opl validate problems.yaml
   ```

   Expected output:

   ```
   problems.yaml: OK
   ```

All commands in this guide are run from the root of the repository, which is the folder that contains `problems.yaml`.

---

## Option A: Pull request that edits `problems.yaml`

Use this option when you want to write the YAML yourself.

### A.1 Write your entries

`problems.yaml` is one big mapping from ID to entry.
Add your entries at the **top level** of the file, so they are not indented. Keep the file sorted alphabetically by ID: `fn_...` entries first, then `gen_...`, `impl_...`, and `suite_...`.

Here is a complete example of a (made-up) problem and its implementation.
Copy it, replace the values with your own, and delete any lines you don't have information for:

```yaml
fn_wind_farm_layout:
  type: problem
  name: Wind farm layout
  long_name: Wind farm layout optimisation with wake effects
  description: >-
    Place a fixed number of turbines inside a polygonal site so that the
    annual energy production is maximised and the cable length is minimised.
    Turbines must keep a minimum distance from each other.
  tags: [energy, layout, expensive]
  objectives: [2]
  variables:
    - {type: continuous, dim: {min: 10, max: 200}}
  constraints:
    - {type: box, hard: yes, number: {min: 10, max: 200}}
    - {type: function, hard: yes, equality: no}
  dynamic_type: [none]
  noise_type: [none]
  allows_partial_evaluation: no
  can_evaluate_objectives_independently: yes
  modality: [multimodal]
  fidelity_levels: [1]
  source: [real-world]
  evaluation_time: [2 seconds]
  instances: [north_sea_30, baltic_60, onshore_120]
  references:
    - title: "A wind farm layout benchmark with wake effects"
      authors: ["Jane Doe", "John Smith"]
      link: {type: doi, url: https://doi.org/10.0000/example.12345}
      type: definition
  implementations: [impl_wind_farm_layout]

impl_wind_farm_layout:
  type: implementation
  name: windfarm-bench
  description: Python package implementing the wind farm layout problem
  language: Python
  links:
    - {type: repository, url: https://github.com/example/windfarm-bench}
    - {type: package, url: https://pypi.org/project/windfarm-bench/}
  requirements: [numpy, scipy]
```

A suite that bundles existing problems looks like this:

```yaml
suite_wind_energy:
  type: suite
  name: Wind energy suite
  description: Collection of wind energy problems.
  problems: [fn_wind_farm_layout, fn_turbine_blade_design]
  objectives: [2]
  source: [real-world]
  implementations: [impl_wind_farm_layout]
```

A generator looks like this:

```yaml
gen_toy_nk:
  type: generator
  name: ToyNK generator
  description: Generates NK landscapes for any N and K < N.
  objectives: [1]
  variables:
    - {type: binary, dim: {min: 2}}
  constraints: []          # empty list = explicitly unconstrained
  modality: [multimodal]
  source: [artificial]
  implementations: [impl_toy_nk]
```

Notes on the YAML format:

- Lists can be written inline (`[a, b]`) or as a block (one `- item` per line). Both mean the same thing.
- You don't need to add fields with value `null`. Many existing entries list every field with `null` because they were generated by a script. Leaving a field out has the same meaning.
- Put strings in quotes if they contain a colon followed by a space (`: `), or start with a special character such as `{`, `[`, `*`, `&`, `#`, `?`, or `-`.
- For long descriptions, use `>-` (folded text) or `|` (keeps line breaks, useful for Markdown) followed by indented text on the next lines.

### A.2 Validate

```bash
uv run opl validate problems.yaml
```

If the output is `problems.yaml: OK`, you're done. Otherwise the validator prints where the problem is, for example:

```
problems.yaml: fn_wind_farm_layout -> Problem -> allows_partial_evaluation: Input should be 'yes', 'no', 'some' or 'unknown'
```

The validator tries to match your entry against every type (`Problem`, `Generator`, `Suite`, `Implementation`). It therefore prints one error per type. **Only look at the line for the type you meant.** In the example above, that is the `Problem` line.

> [!WARNING]
> The validator does **not** catch misspelled field names. For example, `objectivs: [2]` is silently accepted and ignored.
> Compare your field names against the [cheat sheet](#field-cheat-sheet) before you continue.

### A.3 (Optional) Preview the website locally

```bash
uv run yaml_to_html.py
```

This generates `docs/index.html`. Open it in a browser and search for your problem to check that it looks right.
The generated files are ignored by git and are never committed. The website is rebuilt automatically after your submission is merged.

### A.4 Commit, push, and open a pull request

```bash
git add problems.yaml
git commit -m "Add wind farm layout problem"
git push -u origin add-wind-farm-layout
```

Then go to your fork on GitHub. Click **Compare & pull request** and open a pull request against `OpenOptimizationOrg/OPL:main`.
In the description of the pull request, say:

- what you added or changed,
- whether you are an author of the problem or the code (this helps us check details),
- anything you were unsure about when filling in the fields.

---

## Option B: Submit a Python script

Use this option when you have many similar entries (for example a suite with dozens of functions) or prefer to write Python.
Your script builds the entries with the classes from the `opltools` package. These are the same classes that check `problems.yaml`, so mistakes are caught as soon as the script runs.
We then run your script, generate the YAML, and merge it into `problems.yaml` for you.

### B.1 Requirements for the script

Your script must:

1. Be a **single, self-contained `.py` file** that only imports `opltools`, `pydantic_yaml`, and the Python standard library.
2. Put all entries into one dict, keyed by ID (see [Step 0.3](#03-choose-ids)).
3. Wrap that dict in `Library(...)`. This checks the entries and the references between them.
4. **Print the resulting YAML to standard output** with `print(to_yaml_str(library))`.
5. Not read or write any files, use the network, or need any command-line arguments.

You may refer to IDs that already exist in `problems.yaml`, such as `impl_coco`.
In that case `Library(...)` will fail when you run your script by itself, because the existing entry isn't part of your script. Mention this in your pull request and we will take care of it.

### B.2 Write the script

Put the script in the `examples/` folder and name it after your submission, for example `examples/toy_nk.py`.
The following complete example adds one implementation, four problems generated in a loop, a suite containing them, and a generator. Use it as a template:

```python
"""OPL submission: the (fictional) ToyNK suite and generator.

Run from the root of the OPL repository with:

    uv run python examples/toy_nk.py > toy_nk.yaml
    uv run opl validate toy_nk.yaml
"""

from pydantic_yaml import to_yaml_str

from opltools import (
    Generator,
    Implementation,
    Library,
    Link,
    Problem,
    Reference,
    Suite,
    ValueRange,
    Variable,
)

things = {}

# ---------------------------------------------------------------------
# Implementation(s)
# ---------------------------------------------------------------------

things["impl_toy_nk"] = Implementation(
    name="toy-nk",
    description="C++ library with Python bindings for the ToyNK landscapes",
    language="C++/Python",
    links=[
        Link(type="repository", url="https://github.com/example/toy-nk"),
        Link(type="package", url="https://pypi.org/project/toy-nk/"),
    ],
    evaluation_time={"sub second"},
    requirements="https://github.com/example/toy-nk/blob/main/requirements.txt",
)

definition = Reference(
    title="ToyNK: tunable binary landscapes for benchmarking",
    authors=["Jane Doe", "John Smith"],
    link=Link(type="arxiv", url="https://arxiv.org/abs/0000.00000"),
    type="definition",
)

# ---------------------------------------------------------------------
# Problems: one entry per K, generated in a loop
# ---------------------------------------------------------------------

problem_ids = []
for k in [1, 2, 4, 8]:
    id = f"fn_toy_nk_k{k}"
    problem_ids.append(id)
    things[id] = Problem(
        name=f"ToyNK K={k}",
        description=f"NK landscape with epistasis parameter K={k}.",
        objectives={1},
        variables={Variable(type="binary", dim=ValueRange(min=k + 1, max=1000))},
        constraints=set(),  # empty set == explicitly unconstrained
        modality={"unimodal"} if k == 1 else {"multimodal"},
        source={"artificial"},
        instances=ValueRange(min=1, max=100),
        references={definition},
        implementations={"impl_toy_nk"},
    )

# ---------------------------------------------------------------------
# Suite bundling the problems above
# ---------------------------------------------------------------------

things["suite_toy_nk"] = Suite(
    name="ToyNK",
    long_name="ToyNK benchmark suite",
    description="The four ToyNK landscapes with K in {1, 2, 4, 8}.",
    problems=set(problem_ids),
    objectives={1},
    source={"artificial"},
    references={definition},
    implementations={"impl_toy_nk"},
)

# ---------------------------------------------------------------------
# Generator for arbitrary K
# ---------------------------------------------------------------------

things["gen_toy_nk"] = Generator(
    name="ToyNK generator",
    description="Generates ToyNK landscapes for any N and K < N.",
    objectives={1},
    variables={Variable(type="binary", dim=ValueRange(min=2))},
    constraints=set(),
    modality={"multimodal"},
    source={"artificial"},
    references={definition},
    implementations={"impl_toy_nk"},
)

library = Library(things)

if __name__ == "__main__":
    print(to_yaml_str(library))
```

Tips for writing the script:

- You don't have to use `Variable(...)`, `Constraint(...)`, `Link(...)`, `Reference(...)`, or `ValueRange(...)`. Plain dicts and lists work just as well, for example `variables=[{"type": "continuous", "dim": {"min": 1}}]`. See [`examples/cobi.py`](examples/cobi.py) and [`examples/emdo.py`](examples/emdo.py) for that style.
- Fields that hold sets (`objectives`, `tags`, `modality`, `source`, ...) accept either a Python `set` or a `list`.
- Three-valued fields take the strings `"yes"`, `"no"`, `"some"`, or `"unknown"`.
- More examples: [`examples/demo.py`](examples/demo.py) builds the BBOB suite in a loop. [`examples/problems.py`](examples/problems.py) is the script that originally generated most of `problems.yaml`.

### B.3 Run and validate the script

```bash
uv run python examples/toy_nk.py > toy_nk.yaml
uv run opl validate toy_nk.yaml
```

Expected output:

```
toy_nk.yaml: OK
```

If the script fails, Python shows a `ValidationError` that names the field and the problem, for example:

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Problem
allows_partial_evaluation
  Input should be 'yes', 'no', 'some' or 'unknown' [type=enum, input_value='maybe', input_type=str]
```

Open `toy_nk.yaml` and read through it. This is exactly what will end up in OPL.
Then delete it. Only the script is submitted:

```bash
rm toy_nk.yaml
```

> [!WARNING]
> As with YAML, misspelled keyword arguments (for example `objectivs={1}`) are **not** reported as errors. They are stored as extra fields and ignored by the website.
> Check that every field you set shows up in the generated YAML under the name you expected.

### B.4 Submit the script

**Preferred: pull request.**

```bash
git add examples/toy_nk.py
git commit -m "Add ToyNK suite and generator (script)"
git push -u origin add-toy-nk
```

Open a pull request against `OpenOptimizationOrg/OPL:main` as described in [A.4](#a4-commit-push-and-open-a-pull-request).
Write **"Python script submission"** in the title or description, so we know we need to generate and merge the YAML.
Do **not** edit `problems.yaml` yourself in this case.

**Alternative: issue or email.** If you can't open a pull request, [open an issue](https://github.com/OpenOptimizationOrg/OPL/issues/new) and attach the script, or paste it into a code block. You can also email it (see [Getting help](#getting-help)).

---

## Field cheat sheet

The full definitions are in [SCHEMA.md](SCHEMA.md). The table below is a quick reference.
"Set" means a list without duplicates.

### Problem, suite, and generator

| Field | Value | Example |
|---|---|---|
| `type` | `problem`, `suite`, or `generator` | `type: problem` |
| `name` | **required**, short name | `name: Sphere` |
| `long_name` | longer name | `long_name: Black-Box Optimization Benchmarking` |
| `description` | free text, Markdown allowed | see examples above |
| `tags` | set of free-form keywords | `[energy, layout]` |
| `objectives` | set of integers (**not** a range) | `[1]`, `[2, 3]` |
| `variables` | list of `{type, dim}` | `[{type: continuous, dim: {min: 2, max: 40}}]` |
| `constraints` | list of `{type, hard, equality, number}` | `[{type: box, hard: yes, number: 10}]` |
| `dynamic_type` | set of strings | `[none]`, `[time-varying]` |
| `noise_type` | set of strings | `[none]`, `[gaussian]` |
| `allows_partial_evaluation` | `yes` / `no` / `some` / `unknown` | `no` |
| `can_evaluate_objectives_independently` | `yes` / `no` / `some` / `unknown` | `yes` |
| `modality` | set of strings | `[unimodal]`, `[multimodal]` |
| `fidelity_levels` | set of integers | `[1]` = single-fidelity, `[1, 2]` = two fidelities |
| `source` | set of strings | `[artificial]`, `[real-world]` |
| `evaluation_time` | set of free-form strings | `[8 minutes]`, `[sub second]` |
| `references` | list of references (see below) | |
| `implementations` | set of implementation IDs | `[impl_coco]` |
| `code_examples` | set of paths to example scripts | `[code_snippets/bbob/call_bbob.py]` |
| `instances` | **problem only**: a range or a list of names | `{min: 1, max: 15}`, `[small, large]` |
| `problems` | **suite only**: set of problem IDs | `[fn_sphere, fn_rastrigin]` |

### Implementation

| Field | Value | Example |
|---|---|---|
| `type` | `implementation` | |
| `name` | **required** | `name: COCO` |
| `description` | **required** | `description: Comparing Continuous Optimisers` |
| `language` | programming language(s) | `Python`, `C++/Python` |
| `links` | list of `{type, url}` | `[{type: repository, url: https://github.com/numbbo/coco}]` |
| `evaluation_time` | set of free-form strings | `[sub second]` |
| `requirements` | URL to a requirements file, or a list of packages | `[numpy, scipy]` |

### Building blocks

- **Dimensions and counts** (`variables[].dim`, `constraints[].number`, `instances`) can be:
  - a single number: `10`
  - a set of numbers: `[2, 5, 10, 20, 40]`
  - a range: `{min: 2, max: 40}`, `{min: 2}` (2 or more, upper limit unknown), or `{max: 100}`
- **Variable `type`:** `continuous`, `integer`, `binary`, `categorical`, `unknown`.
  For permutations or other combinatorial structures, use `unknown` **and** add a tag such as `permutation`.
- **Constraint `type`:** `box`, `linear`, `function` (non-linear or black-box), `unknown`.
  `hard` and `equality` take `yes` / `no` / `some` / `unknown`.
- **Reference:** needs at least a `title` or a `link`. Optional: `authors` (list of names) and `type`:
  - `definition`: the paper that introduces the problem
  - `use`: a paper that uses the problem
  - `critique`: a paper that discusses whether the problem is suitable for some purpose

  ```yaml
  references:
    - title: "Real-parameter black-box optimization benchmarking 2009: Noiseless functions definitions"
      authors: ["Nikolaus Hansen", "Steffen Finck", "Raymond Ros", "Anne Auger"]
      link: {type: doi, url: https://doi.org/10.xxxx/xxxxx}
      type: definition
  ```
- **Link:** `{type: <free text>, url: <url>}`. Common types are `repository`, `package`, `paper`, `arxiv`, and `doi`.
  For DOIs, always use the full URL (`https://doi.org/10....`), never the bare DOI.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Leaving out `constraints` for an unconstrained problem | Leaving it out means "unknown". To say "unconstrained", write `constraints: []` (YAML) or `constraints=set()` (Python). |
| `objectives: {min: 1, max: 3}` | `objectives` is a set of integers: `objectives: [1, 2, 3]`. |
| `allows_partial_evaluation: "?"` or `maybe` | Use one of `yes`, `no`, `some`, `unknown`. |
| Bare DOI `10.1109/TEVC.2013.2281535` | `https://doi.org/10.1109/TEVC.2013.2281535` |
| Misspelled field name (`objectivs`, `implementation`, `refrences`) | Not reported by the validator. Compare against the [cheat sheet](#field-cheat-sheet). |
| Referring to an ID that doesn't exist (`implementations: [impl_typo]`) | Add the missing entry or fix the ID. For problems, the validator currently fails with a Python `KeyError: 'impl_typo'` traceback instead of a readable message. |
| Reusing an ID that already exists | IDs must be unique. In YAML, a duplicated key silently overwrites the earlier entry. Search first with `grep -n "^fn_my_id:" problems.yaml`. |
| Adding a duplicate implementation for COCO, IOHexperimenter, pymoo, ... | Reuse the existing `impl_...` ID. |

---

## Optional: Add a code snippet

We collect small, runnable examples that show how to evaluate a problem in [`code_snippets/`](code_snippets/README.md).
If you'd like to add one:

1. Create a folder `code_snippets/<problem>/`.
2. Add a `call_<problem>.py` that starts with an inline dependency block, so it runs with `uv run call_<problem>.py`:

   ```python
   # /// script
   # dependencies = [
   #   "windfarm-bench",
   # ]
   # ///
   import numpy as np
   from windfarm_bench import WindFarmLayout

   problem = WindFarmLayout(instance="north_sea_30")
   x = np.zeros(problem.dimension)
   print(problem.evaluate(x))
   ```

3. Add a `README.md` in the same folder that explains any setup steps (cloning repositories, downloading data, ...). See [`code_snippets/bbob/README.md`](code_snippets/bbob/README.md) for an example.
4. Refer to the snippet from your entry: `code_examples: [code_snippets/wind_farm_layout/call_wind_farm_layout.py]`.

---

## What happens after you submit

1. **Automatic checks.** GitHub Actions lints the code, runs the test suite, and checks that the website can be built from your changes.
2. **Review.** A maintainer checks your entries for correctness and consistency with the rest of OPL. We may ask questions or suggest changes in the pull request. Push more commits to the same branch to update it.
3. **Script submissions (Option B).** A maintainer runs your script, merges the generated YAML into `problems.yaml`, and validates the result.
4. **Website update.** Every merge into `main` rebuilds and deploys the website automatically, and your problem appears on the [OPL website](https://openoptimizationorg.github.io/OPL/).

---

## Getting help

- Open an [issue](https://github.com/OpenOptimizationOrg/OPL/issues) if something in this guide is unclear, or if your problem doesn't fit the schema. We are actively looking for cases the schema doesn't cover yet.
- Email: koen.van.der.blom@cwi.nl
