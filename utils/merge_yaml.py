import yaml
import os
import sys
from pathlib import Path
from typing import List, Dict

# Add parent directory to sys.path
parent = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent))

from utils.validate_yaml import read_data, validate_data


def write_data(filepath: str, data: List[Dict]) -> bool:
    try:
        with open(filepath, "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)
        print(f"::notice::Wrote data to {filepath}.")
    except FileNotFoundError:
        print(f"::error::File not found: {filepath}")
        return False
    except OSError as e:
        print(f"::error::Error writing file {filepath}: {e}")
        return False
    except yaml.YAMLError as e:
        print(f"::error::YAML syntax error: {e}")
        return False
    return True


def update_existing_data(
    existing_data: List[Dict], new_data: List[Dict], out_file: str
) -> bool:
    existing_data.extend(new_data)
    write_success = write_data(out_file, existing_data)
    return write_success


def delete_new_file(file_path: str) -> bool:
    # Delete the new file after merging
    try:
        os.remove(file_path)
        print(f"::notice::Deleted new problem file {file_path}.")
    except OSError as e:
        print(f"::error::Error deleting file {file_path}: {e}")
        return False
    return True


def merge_new_problems(new_problems_yaml_path: str, big_yaml_path: str) -> bool:
    # Read and validate new data
    new_data_status, new_data = read_data(new_problems_yaml_path)
    if new_data_status != 0 or new_data is None:
        print(
            f"::error::New problems data could not be read from {new_problems_yaml_path}."
        )
        return False
    valid = validate_data(new_data)
    if not valid:
        print(f"::error::New problems data in {new_problems_yaml_path} is not valid.")
        return False

    # Read existing data
    existing_data_status, existing_data = read_data(big_yaml_path)
    if existing_data_status != 0 or existing_data is None:
        print(
            f"::error::Existing problems data could not be read from {big_yaml_path}."
        )
        return False

    # All valid, we can now just merge the dicts
    assert existing_data is not None
    assert new_data is not None
    updated = update_existing_data(existing_data, new_data, big_yaml_path)
    if not updated:
        print(f"::error::Failed to update existing problems data in {big_yaml_path}.")
        return False

    # Remove the new file after merging
    rm_status = delete_new_file(new_problems_yaml_path)
    if not rm_status:
        print(
            f"::warning::Merged data into {big_yaml_path}, but failed to delete "
            f"new problem file {new_problems_yaml_path}."
        )

    print(f"::notice::Merged {len(new_data)} new problems into {big_yaml_path}.")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python merge_yaml.py <new_problems.yaml> <big_yaml_path>")
        sys.exit(1)
    new_problems_yaml_path = sys.argv[1]
    big_yaml_path = sys.argv[2]
    status = merge_new_problems(new_problems_yaml_path, big_yaml_path)
    if not status:
        sys.exit(1)
    else:
        sys.exit(0)
