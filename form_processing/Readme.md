# CSV to YAML import

This folder contains a small Python script that merges the content of the form-response CSV into the main OPL YAML file.

## What it does

- reads `OPL_form.csv`
- converts each row into OPL schema objects
- merges new entries into `../problems.yaml`
- skips duplicate names and empty rows
- validates the merged YAML before writing

## Usage

Run the script from the repository root or from this folder:

```bash
python form_processing/formresponse_to_yaml.py --csv form_processing/OPL_form.csv --existing-yaml problems.yaml --output-yaml problems.yaml
```

If you run it from inside `form_processing`, the defaults also work:

```bash
python formresponse_to_yaml.py
```

## Dry run

Use dry-run mode to check the import without changing any files:

```bash
python form_processing/formresponse_to_yaml.py --dry-run
```

## Notes

- The script keeps existing entries and only adds new ones.
- It prints how many entries were added, how many implementations were added, and how many rows were skipped.
