# OPL Schema

The OPL schema catalogs optimization **problems**, **suites**, **generators**, and their **implementations** in a single, machine-readable format. 

Three design choices shape everything below:

1. **One flat library, keyed by ID.** 
   Every entity lives in a `Library` dict. 
   Suites reference problems, problems reference implementations using their respective ID.
   There is no embedding of problems or implementations within suites to facilitate reuse. 
   F.e. an implementation might be referenced by multiple problems or suites.
2. **Numeric fields accept a scalar, a set, or a range.** 
   A problem may have exactly `2` objectives, one of `{2, 3, 5}`, or any value in `{min: 2, max: 50}`. 
   The same union type is used for variable dimensions and constraint counts.
3. **Three-valued logic for yes/no fields.** 
   Many boolean fields (f.e. `hard`, `allows_partial_evaluation`, ...) [`YesNoSome`](#yesnosome) as their value.
   We lose some expressive power but simplify the data entry.
   If we force authors to decide on yes or no, then we would need more complex structures for variables, constraints etc. and that would make the usual case unnecessarily complex.
   
## Contents

- [Library](#library) 
- [Thing types](#thing-types)
  - [Implementation](#implementation)
  - [Reference](#reference)
  - [ProblemLike](#problemlike) (shared fields)
    - [Problem](#problem)
    - [Suite](#suite)
    - [Generator](#generator)
- [Shared building blocks](#shared-building-blocks)
  - [Variable](#variable) / [VariableType](#variabletype)
  - [Constraint](#constraint) / [ConstraintType](#constrainttype)
  - [Link](#link)
  - [ValueRange](#valuerange)
  - [YesNoSome](#yesnosome)

---

## Notation / Conventions

- When an attribute is followed by a `?`, it is optional and can be left out.
- When we refer to a list of unique items, we call them a set. 
  Technically they are a set in Python, but in the YAML representation they are a list.
  However, they _must_ be unique (i.e. obey the set property)

## Library

A `Library` is a dict from ID to a [Thing](#thing-types).
IDs are free-form but must be unique and the convention is to add a prefix marking the type to avoid collisions:

| Prefix  | Type             |
|---------|------------------|
| `impl_` | Implementation   |
| `ref_`  | Reference        |
| `fn_`   | Problem          |
| `suite_`| Suite            |
| `gen_`  | Generator        |

On load the library validates that every ID referenced by a suite (`problems`), problem (`implementations`), or any [ProblemLike](#problemlike) (`references`) exists and has the correct type. Suites also have their `fidelity_levels` auto-populated from their problems.

```yaml
impl_coco:
  type: implementation
  name: COCO
  description: Comparing Continuous Optimisers
ref_bbob:
  type: reference
  title: "Real-Parameter Black-Box Optimization Benchmarking: Experimental Setup"
  link: {type: url, url: "https://numbbo.github.io/coco/"}
fn_sphere:
  type: problem
  name: Sphere
  objectives: [1]
  implementations: [impl_coco]
  references: [ref_bbob]
suite_bbob:
  type: suite
  name: BBOB
  problems: [fn_sphere]
  references: [ref_bbob]
```

---

## Thing types

All entities inherit from `Thing`, which only carries a discriminator:

```yaml
type: problem  # or: suite | generator | implementation
```

We want to have as flat a structure as possible to make exploring and searching OPL as easy as possible. 
That's one of the reasons the top level object is a dictionary of dissimilar things.
But we need to be able to tell them apart so we have a `type` field to discriminate between them.

### Implementation

A pointer to code that implements one or more problems. 
Intentionally minimal so that the schema describes *what* a problem is, not how to run it.
There are separate files which contain curated usage examples for problems or suites keyed by their respective IDs.

| Field             | Type                              | Notes                                        |
|-------------------|-----------------------------------|----------------------------------------------|
| `name`            | str                               | required                                     |
| `description`     | str                               | required                                     |
| `language`        | str? (e.g. `Python`, `C`)         |                                              |
| `links`           | list of [Link](#link)?            | repo, release, docs…                         |
| `evaluation_time` | set of str?                       | free-form list ("8 minutes", "fast")         |
| `requirements`    | str or list of str?               | URL to requirements file or list of packages |

```yaml
impl_coco:
  type: implementation
  name: COCO
  description: Comparing Continuous Optimisers benchmarking platform
  language: c
  links:
    - {type: repository, url: https://github.com/numbbo/coco-experiment}
impl_py_cocoex:
  type: implementation
  name: Python bindings for COCO
  description: The Python bindings for the experimental part of the COCO framework
  language: Python
  links:
    - {type: source, url: https://github.com/numbbo/coco-experiment/tree/main/build/python}
    - {type: package, url: https://pypi.org/project/coco-experiment/}
```

### Reference

A bibliographic pointer stored at the top level of the [Library](#library) so that a single reference can be shared by multiple problems, suites, generators, and implementations.
Requires either a `title` or a `link` and optionally a list of `authors`.

| Field     | Type                   | Notes                                    |
|-----------|------------------------|------------------------------------------|
| `title`   | str?                   | required if `link` is not given          |
| `authors` | list of str?           |                                          |
| `link`    | [Link](#link)?         | required if `title` is not given         |

```yaml
ref_honey_badger:
  type: reference
  title: "Honey Badger Algorithm: New metaheuristic algorithm for solving optimization problems."
  authors:
    - Fatma A. Hashim
    - Essam H. Houssein
    - Kashif Hussain
    - Mai S. Mabrouk
    - Walid Al-Atabany
  link: {type: doi, url: "https://doi.org/10.1016/j.matcom.2021.08.013"}
```

[ProblemLike](#problemlike) entities refer to a reference by its ID in the `references` field.

### ProblemLike

Fields shared by [Problem](#problem), [Suite](#suite), and [Generator](#generator). 
The schema deliberately puts most descriptive fields here so suites can be characterised without explicitly having to add all problems in the suite.

| Field                                    | Type                                           | Notes                                              |
|------------------------------------------|------------------------------------------------|----------------------------------------------------|
| `name`                                   | str                                            | required                                           |
| `long_name`                              | str?                                           |                                                    |
| `description`                            | str? (markdown)                                | longer prose                                       |
| `tags`                                   | set of str?                                    | free-form keywords                                 |
| `references`                             | set of IDs?                                    | must resolve to [Reference](#reference)s           |
| `implementations`                        | set of IDs?                                    | must resolve to [Implementation](#implementation)s |
| `objectives`                             | set of int?                                    | e.g. `{1}`, `{2, 3}` — **not** a ValueRange        |
| `variables`                              | set of [Variable](#variable)?                  |                                                    |
| `constraints`                            | set of [Constraint](#constraint)?              | omit entirely for unconstrained                    |
| `dynamic_type`                           | set of str?                                    | `{"no"}`, `{"time-varying"}`…                      |
| `noise_type`                             | set of str?                                    | `{"none"}`, `{"gaussian"}`…                        |
| `allows_partial_evaluation`              | [YesNoSome](#yesnosome)?                       |                                                    |
| `can_evaluate_objectives_independently`  | [YesNoSome](#yesnosome)?                       |                                                    |
| `modality`                               | set of str?                                    | `{"unimodal"}`, `{"multimodal"}`                   |
| `fidelity_levels`                        | set of int?                                    | `{1}` = single-fidelity, `{1,2}` = multi-fidelity  |
| `code_examples`                          | set of str?                                    | paths to example scripts                           |
| `evaluation_time`                        | set of str?                                    | free-form list ("8 minutes", "fast")         |
| `source`                                 | set of str?                                    | `{"artificial"}`, `{"real-world"}`                 |

> `objectives` is a set of integers because we don't assume extreme scalability in this property so explicit enumeration is fine.
> Dimensions of variables on the other hand are ranges because here problems often are scalable over wide ranges.

When no `evaluation_time` is set, it percolates up from any referenced implementations.
The same is true for the `variables` and `constraints` properties of a suite that has references to problems.

### Problem

One optimization problem (possibly parameterised by instances).

Adds:

| Field       | Type                                       | Notes                                      |
|-------------|--------------------------------------------|--------------------------------------------|
| `instances` | [ValueRange](#valuerange) or list of str?  | e.g. `{min: 1, max: 15}` or named variants |

```yaml
fn_sphere:
  type: problem
  name: Sphere
  objectives: [1]
  variables: [{type: continuous, dim: {min: 2, max: 40}}]
  modality: [unimodal]
  source: [artificial]
  instances: {min: 1, max: 15}
  implementations: [impl_coco]
```

### Suite

A curated, fixed collection of problems.

Adds:

| Field      | Type         | Notes                                         |
|------------|--------------|-----------------------------------------------|
| `problems` | set of IDs?  | must resolve to [Problem](#problem)s          |

`fidelity_levels` is auto-unioned from member problems at validation time.

```yaml
suite_bbob:
  type: suite
  name: BBOB
  problems: [fn_sphere, fn_rosenbrock, fn_rastrigin]
  objectives: [1]
  source: [artificial]
  implementations: [impl_coco]
```

### Generator

A parametric family of problems — unlike a [Suite](#suite), the member problems are not enumerated. Uses the same fields as [ProblemLike](#problemlike) with no additions; the distinction from [Problem](#problem) is that a generator produces instances on demand.

```yaml
gen_mpm2:
  type: generator
  name: MPM2
  description: Multiple peaks model, second instantiation
  objectives: [1]
  variables: [{type: continuous, dim: {min: 1}}]
  modality: [multimodal]
```

---

## Shared building blocks

### Variable

A group of decision variables of the same type. 
Multi-type problems list multiple entries.
While you can have multiple entries of the same type, this should be justified in some way like when you can evaluate the problem on only one subset of variables.

| Field  | Type                                          | Default              |
|--------|-----------------------------------------------|----------------------|
| `type` | [VariableType](#variabletype)                 | `unknown`            |
| `dim`  | int, set of int, [ValueRange](#valuerange), or null | `0`            |

```yaml
variables:
  - {type: continuous, dim: 10}
  - {type: integer, dim: {min: 1, max: 5}}
```

### VariableType

`continuous | integer | binary | categorical | unknown`. 
Use `unknown` for permutation/combinatorial problems the schema doesn't yet distinguish **and** add an appropriate tag.
We are actively watching for unknown variable types and are open to extending the above list if there is a critical mass of problems to justify it.

### Constraint

A group of constraints. 
To indicate that the problem is unconstrained, you need an _empty_ `constraints` field.
A missing `constraints` field or if it is set to `null` means it is not known if unconstrained.

| Field      | Type                                          | Notes                              |
|------------|-----------------------------------------------|------------------------------------|
| `type`     | [ConstraintType](#constrainttype)             | default `unknown`                  |
| `hard`     | [YesNoSome](#yesnosome)?                      | hard vs. soft                      |
| `equality` | [YesNoSome](#yesnosome)?                      | equality vs. inequality            |
| `number`   | int, set of int, [ValueRange](#valuerange), null |                                 |

```yaml
constraints:
  - {type: box, hard: yes, number: 10}
  - {type: linear, hard: some, equality: no, number: {min: 1}}
```

### ConstraintType

`box | linear | function | unknown`. `function` covers non-linear/black-box constraints.

### Link

`{type?: str, url: str}`. 
`type` is free-form (`repository`, `arxiv`, `paper`, `doi`, ...).
`url` is a URL to some resource. 

If `type` is `doi`, please use the full URL (starting with `https://doi.org/...`) instead of the raw DOI.

### ValueRange

An inclusive numeric range type. 
At least one of `min`/`max` must be given.
If `min` is given and `max` is missing, it does not imply that there is no upper bound. 
There might be one, it is just not known.
The same applies for the case where `max` is given and `min` is missing.

```yaml
dim: {min: 2}            # 2 or more
dim: {min: 2, max: 40}   # between 2 and 40
dim: {max: 100}          # up to 100
```

Used by `Variable.dim`, `Constraint.number`, `Problem.instances`.

### YesNoSome

Three-valued flag: `yes | no | some | ?` (the last serialises as the literal `'?'` string, meaning unknown).
`some` captures the common case where *part* of something has some property.
For example only some constraints might hard but we don't know the exact number of hard and soft constraints, only the total number.

```yaml
constraints: [{type: box, hard: some}]
allows_partial_evaluation: "?"
```
