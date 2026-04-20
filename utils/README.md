# OPL YAML utils

This folder contains utility scripts for working with the YAML format to describe problems in context of OPL. They are mainly intended to be run automatically via GitHub Actions to make collaboration easier.

The intended way of adding a new problem to the repository is thus as follows:

* Create a file in 'utils/new_problem.yaml' based on the template (see below).
* Create a PR with the changes (for example with a fork).

What happens in the background then is:

* On PR creation and commits to the PR, the [validate_yaml.py](validate_yaml.py) script is run to check that the YAML file is valid and consistent. It is expecting the changes to be in the [new_problem.yaml](new_problem.yaml) file.
* Then the PR should be reviewed manually.
* When the PR is merged into the main branch, a second script runs (which doesn't exist yet), that adds the content of [new_problem.yaml](new_problem.yaml) to the [problems.yaml](../problems.yaml) file, and reverts the changes to the new_problem.yaml.

:warning: Note that the GitHubActions do not exist yet either, this is a WIP.

## validate_yaml.py

This script checks the new content for the following:

* The YAML syntax is valid and is in expected format
* The required fields are present.
* Specific fields are unique across the new set of problems (e.g. name)

:warning: Execute from root of the repository. Tested with python 3.12

```bash
pip install -r utils/requirements.txt
python utils/validate_yaml.py utils/new_problem.yaml
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
```
