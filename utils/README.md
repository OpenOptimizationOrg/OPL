# OPL YAML utils

This folder contains utility scripts for working with the YAML format to describe problems in context of OPL. Some of them are mainly intended to be run automatically via GitHub Actions to make collaboration easier, others are utility functions for maintainers.

The intended way of adding a new problem to the repository is thus as follows:

* Create a new yaml file based on the template (see below).
* Run the [merge script](merge_yaml.py) locally to update the [problems.yaml](../problems.yaml) file and check that the formatting is correct.
* Create a PR with the changes (for example with a fork).

What happens in the background then is:

* On PR creation and commits to the PR, the [validate_yaml.py](validate_yaml.py) script is run to check that the [problems.yaml](../problems.yaml) file is still valid and consistent.
* Then the PR should be reviewed manually.
* When the PR is merged into the main branch with changes to problems.yaml, the check are run again.

## validate_yaml.py

This script checks the new content for the following:

* The YAML syntax is valid and is in expected format
* The required fields are present.
* Specific fields are unique across the  set of problems (e.g. name)

:warning: Execute from root of the repository. Tested with python 3.12

```bash
pip install -r utils/requirements.txt
python utils/validate_yaml.py problems.yaml
```

## merge_yaml.py

This script merges a new problem description in a separate yaml file into the main [problems.yaml](../problems.yaml) file. It runs the validation checks from the above script before merging and deletes the separate yaml file after merging.

:warning: Execute from root of the repository. Tested with python 3.12

```bash
pip install -r utils/requirements.txt
python utils/merge_yaml.py new_problem.yaml problems.yaml
```

## new problem example

```yaml
- name: example-problem-name
  suite/generator/single: suite
  objectives: '1'
  dimensionality: scalable
  variable type: continuous
  constraints: 'no'
  dynamic: 'no'
  noise: 'no'
  multimodal: 'yes'
  multi-fidelity: 'no'
  reference: ''
  implementation: ''
  source (real-world/artificial): ''
  textual description: 'This is a dummy template'
