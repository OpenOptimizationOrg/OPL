# OPL YAML utils

This folder contains utility scripts for working with the YAML format to describe problems in context of OPL. They are mainly intended to be run automatically via GitHub Actions to make collaboration easier.

The intended way of adding a new problem to the repository is thus as follows:

* Change the [new_problem.yaml](new_problem.yaml) template file to fit the new problem.
* Create a PR which modifies with the changes (for example with a fork).

What happens in the background then is:

* On PR creation and commits to the PR, the [validate_yaml.py](validate_yaml.py) script is run to check that the YAML file is valid and consistent. It is expecting the changes to be in the [new_problem.yaml](new_problem.yaml) file.
* Then the PR should be reviewed manually.
* When the PR is merged into the main branch, a second script runs (which doesn't exist yet), that adds the content of [new_problem.yaml](new_problem.yaml) to the [problems.yaml](../problems.yaml) file, and returns it to its previous version.

:alert: Note that the GitHubActions do not exist yet either, this is a WIP.

## validate_yaml.py

This script checks the new content for the following:

* The YAML syntax is valid and is in expected format
* The required fields are present.
* Specific fields are unique across the new set of problems (e.g. name)

:alert: Execute from root of the repository. Tested with python 3.12

```bash
pip install -r utils/requirements.txt
python utils/validate_yaml.py utils/new_problem.yaml
```
