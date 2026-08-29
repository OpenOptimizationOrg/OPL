import yaml

import sys
from pathlib import Path
from typing import List, Dict, Tuple

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


def read_data(filepath: str) -> Tuple[int, List[Dict] | None]:
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


def check_format(data: List[Dict]) -> bool:
    num_problems = len(data)
    if not isinstance(data, list):
        print("::error::YAML file should contain a list of entries.")
        return False
    if len(data) < 1:
        print("::error::YAML file should contain at least one top level entry.")
        return False
    print(f"::notice::YAML file contains {num_problems} top-level entries.")
    unique_fields = []
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            print(f"::error::Entry {i} is not a dictionary.")
            return False
        unique_fields.append({k: v for k, v in entry.items() if k in UNIQUE_FIELDS})
    for k in UNIQUE_FIELDS:
        values = [
            entry[k] for entry in unique_fields if k in entry and entry[k] is not None
        ]
        if len(values) != len(set(values)):
            print(f"::error::Field '{k}' must be unique across all entries.")
            return False
    return True


def check_fields(data: Dict) -> bool:
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        print(f"::error::Missing required fields: {', '.join(missing)}")
        return False
    new_fields = [
        field for field in data if field not in REQUIRED_FIELDS + OPTIONAL_FIELDS
    ]
    if new_fields:
        print(f"::warning::New field added: {', '.join(new_fields)}")
    # Check that the name is not still template
    if data.get("name") == "template":
        print(
            "::error::Please change the 'name' field from 'template' to a unique name."
        )
        return False
    # Check non-empty fields
    empty_fields = [
        field
        for field in NON_EMPTY_FIELDS
        if data.get(field, None) is None or data.get(field, "").strip() == ""
    ]
    if empty_fields:
        print(
            f"::error::The following fields cannot be empty: {', '.join(empty_fields)}"
        )
        return False
    return True


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
    if not check_format(data):
        sys.exit(1)
    for i, entry in enumerate(data):
        if not check_fields(entry):
            print(f"::error::Validation failed for entry {i+1}.")
            sys.exit(1)
    print("YAML syntax is valid.")


def check_novelty(data: Dict, checked_data: List[Dict]) -> bool:
    for field in UNIQUE_FIELDS + UNIQUE_WARNING_FIELDS:
        # skip empty fields
        if not data.get(field):
            continue
        existing_values = {
            entry.get(field) for entry in checked_data if isinstance(entry, dict)
        }
        if data.get(field) in existing_values:
            if field in UNIQUE_WARNING_FIELDS:
                print(
                    f"::warning::Field '{field}' with value '{data.get(field)}' already exists. Consider choosing a unique value."
                )
                continue
            elif field in UNIQUE_FIELDS:
                print(
                    f"::error::Field '{field}' with value '{data.get(field)}' already exists. Please choose a unique value."
                )
                return False
    return True


def validate_data(data: List[Dict]) -> bool:
    assert data is not None
    if not check_format(data):
        return False

    checked_data = []

    for i, new_data in enumerate(data):  # Iterate through each top-level entry
        # Check required and unique fields
        if not check_fields(new_data) or not check_novelty(new_data, checked_data):
            print(f"::error::Validation failed for entry {i+1}.")
            return False
        checked_data.append(new_data)  # Add to checked data for novelty checks

    # YAML is valid if we reach this point
    print("YAML syntax is valid.")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("::error::Usage: python validate_yaml.py <yourfile.yaml>")
        sys.exit(1)

    filepath = sys.argv[1]
    validate_yaml(filepath)
