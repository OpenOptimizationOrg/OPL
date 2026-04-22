import yaml

import sys
from pathlib import Path

# Add parent directory to sys.path
parent = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent))

# Now you can import normally
# from yaml_to_html import default_columns as REQUIRED_FIELDS
REQUIRED_FIELDS = [
    "name",
    "textual description",
    "suite/generator/single",
    "objectives",
    "dimensionality",
    "variable type",
    "constraints",
    "dynamic",
    "noise",
    "multi-fidelity",
    "source (real-world/artificial)",
    "reference",
    "implementation",
]


from pydantic import ValidationError
from pydantic_yaml import parse_yaml_raw_as
from src.opltools.schema import Library


OPTIONAL_FIELDS = ["multimodal"]
UNIQUE_FIELDS = ["name"]
NON_EMPTY_FIELDS = ["name"]
UNIQUE_WARNING_FIELDS = ["reference", "implementation"]


def read_data(filepath):
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
            return 0, data
    except FileNotFoundError:
        print(f"::error::File not found: {filepath}")
        return 1, None
    except yaml.YAMLError as e:
        print(f"::error::YAML syntax error: {e}")
        return 1, None


def update_seen(fields, seen, duplicates, entry):
    entry_type = entry.get("type", "unknown")
    for field in fields:
        value = entry.get(field, None)
        if value is None:
            continue
        seen_value = f"{entry_type}:{value}"
        if seen_value in seen[field]:
            duplicates[field].add(seen_value)
        else:
            seen[field].add(seen_value)
    return seen, duplicates


def check_duplicates(data, warning_fields, error_fields):
    # Run checks for each entry and collect duplicates
    fields = set(warning_fields + error_fields)
    seen = {field: set() for field in fields}
    duplicates = {field: set() for field in fields}
    for _, entry in data.items():
        seen, duplicates = update_seen(fields, seen, duplicates, entry)

    duplicate_warnings = {
        field: list(dups)
        for field, dups in duplicates.items()
        if dups and field in warning_fields
    }
    if len(duplicate_warnings) > 0:
        print(f"::warning::Duplication warnings {duplicate_warnings}")
    duplicate_errors = {
        field: list(dups)
        for field, dups in duplicates.items()
        if dups and field in error_fields
    }
    if len(duplicate_errors) > 0:
        print(f"::error::Duplication errors {duplicate_errors}")
    return len(duplicate_errors) == 0


def check_parsing(filepath):
    try:
        with open(filepath, "r") as f:
            raw = f.read()
        parse_yaml_raw_as(Library, raw)
        return True
    except ValidationError as e:
        print(f"::error::YAML parsing error: {e}")
        return False


def validate_yaml(filepath):
    status = check_parsing(filepath)
    if not status:
        sys.exit(1)

    status, data = read_data(filepath)
    if status != 0 or data is None:
        sys.exit(1)
    if not check_duplicates(
        data, warning_fields=UNIQUE_WARNING_FIELDS, error_fields=UNIQUE_FIELDS
    ):
        sys.exit(1)

    # YAML is valid if we reach this point
    print("YAML syntax is valid.")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("::error::Usage: python validate_yaml.py <yourfile.yaml>")
        sys.exit(1)

    filepath = sys.argv[1]
    validate_yaml(filepath)
