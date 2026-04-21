import yaml
import sys
from pathlib import Path
from typing import List, Dict

# Add parent directory to sys.path
parent = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent))

from utils.validate_yaml import read_data, validate_data, validate_yaml


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
    # validate merged data before writing
    valid = validate_data(existing_data)
    if not valid:
        print(f"::error::Merged data is not valid, cannot write to {out_file}.")
        return False
    write_success = write_data(out_file, existing_data)
    return write_success


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

    # Validate resulting data
    final_status, final_data = validate_yaml(big_yaml_path)
    if final_status != 0 or final_data is None:
        print(
            f"::error::Merged data in {big_yaml_path} is not valid after merging new problems."
        )
        return False

    print(
        f"::notice::Merged {len(new_data)} new problems into {big_yaml_path}. {new_problems_yaml_path} can now be deleted."
    )
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
