import yaml

import sys
from pathlib import Path

# Add parent directory to sys.path
parent = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent))

# Now you can import normally
from yaml_to_html import default_columns as REQUIRED_FIELDS

OPTIONAL_FIELDS = ["multimodal"]
UNIQUE_FIELDS = ["name"]
UNIQUE_WARNING_FIELDS = ["reference", "implementation"]
PROBLEMS_FILE = "problems.yaml"


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


def check_format(data):
    num_problems = len(data)
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
        values = [entry[k] for entry in unique_fields]
        if len(values) != len(set(values)):
            print(f"::error::Field '{k}' must be unique across all entries.")
            return False
    return True


def check_fields(data):
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
    return True


def check_novelty(data):
    # Load existing problems
    read_status, existing_data = read_data(PROBLEMS_FILE)
    if read_status != 0:
        print("::eror::Could not read existing problems for novelty check.")
        return False
    assert existing_data is not None
    for field in UNIQUE_FIELDS or UNIQUE_WARNING_FIELDS:
        existing_values = {
            entry.get(field) for entry in existing_data if isinstance(entry, dict)
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


def validate_data(data) -> bool:
    if not check_format(data):
        return False

    for i, new_data in enumerate(data):  # Iterate through each top-level entry
        # Check required and unique fields
        if not check_fields(new_data) or not check_novelty(new_data):
            print(f"::error::Validation failed for entry {i+1}.")
            return False

    # YAML is valid if we reach this point
    print("::notice::YAML syntax is valid.")
    return True


def validate_yaml(filepath: str) -> bool:
    status, data = read_data(filepath)
    if status != 0:
        return False
    return validate_data(data)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("::error::Usage: python validate_yaml.py <yourfile.yaml>")
        sys.exit(1)

    filepath = sys.argv[1]
    valid = validate_yaml(filepath)
    if valid:
        sys.exit(0)
    else:
        sys.exit(1)
