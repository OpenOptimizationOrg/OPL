import yaml

import sys
from pathlib import Path

# Add parent directory to sys.path
parent = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent))

from .validate_yaml import read_data, validate_data, PROBLEMS_FILE

TEMPLATE_FILE = "template.yaml"


def validity_check(old_data, new_data):
    # Check there are not duplicate keys
    duplicates = len(set(old_data[0].keys()) & set(new_data[0].keys())) > 0
    if duplicates:
        print(
            "::error::Duplicate problem names found between existing and new problems."
        )
        return False

    # Validate new data
    is_valid = validate_data(new_data)
    if not is_valid:
        print("::error::New problems YAML validation failed")
        return False

    return True


def write_data(filepath, data):
    try:
        with open(filepath, "w") as f:
            yaml.safe_dump(data, f)
        print(f"::notice::Wrote data to {filepath}.")
    except FileNotFoundError:
        print(f"::error::File not found: {filepath}")
        return False
    except yaml.YAMLError as e:
        print(f"::error::YAML syntax error: {e}")
        return False
    return True


def update_existing_data(existing_data, new_data):
    existing_data.update(new_data)

    write_success = write_data(PROBLEMS_FILE, existing_data)
    return write_success


def reset_to_template(file_path):
    # Reset the content of the file to a template
    template_data_status, template_data = read_data(TEMPLATE_FILE)
    if template_data_status != 0:
        return template_data_status
    write_success = write_data(file_path, template_data)
    return write_success


def merge_new_problems(new_problems_yaml_path: str):
    existing_data_status, existing_data = read_data(PROBLEMS_FILE)
    if not existing_data_status:
        return False
    new_data_status, new_data = read_data(new_problems_yaml_path)
    if not new_data_status:
        return False
    # Validate data
    is_valid = validity_check(existing_data, new_data)
    if not is_valid:
        return False

    # All valid, we can now just merge the dicts
    assert existing_data is not None
    assert new_data is not None
    updated = update_existing_data(existing_data, new_data)
    if not updated:
        return False

    # Reset the template content
    reset_status = reset_to_template(new_problems_yaml_path)
    if not reset_status:
        return False

    print(f"::notice::Merged {len(new_data)} new problems into {PROBLEMS_FILE}.")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python merge_yaml.py <new_problems.yaml>")
        sys.exit(1)
    new_problems_yaml_path = sys.argv[1]
    status = merge_new_problems(new_problems_yaml_path)
    if not status:
        sys.exit(1)
    else:
        sys.exit(0)
