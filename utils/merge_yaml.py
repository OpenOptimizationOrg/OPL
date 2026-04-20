import yaml
import os
import sys
from pathlib import Path

# Add parent directory to sys.path
parent = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent))

from .validate_yaml import read_data, validate_data, PROBLEMS_FILE


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


def delete_new_file(file_path):
    # Delete the new file after merging
    try:
        os.remove(file_path)
        print(f"::notice::Deleted new problem file {file_path}.")
    except OSError as e:
        print(f"::error::Error deleting file {file_path}: {e}")
        return False
    return True


def merge_new_problems(new_problems_yaml_path: str):
    # Read and validate new data
    new_data_status, new_data = read_data(new_problems_yaml_path)
    if not new_data_status:
        return False
    valid = validate_data(new_data)
    if not valid:
        return False

    # Read existing data
    existing_data_status, existing_data = read_data(PROBLEMS_FILE)
    if not existing_data_status:
        return False

    # All valid, we can now just merge the dicts
    assert existing_data is not None
    assert new_data is not None
    updated = update_existing_data(existing_data, new_data)
    if not updated:
        return False

    # Reset the template content
    reset_status = delete_new_file(new_problems_yaml_path)
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
