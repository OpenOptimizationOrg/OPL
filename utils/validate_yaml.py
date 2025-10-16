import yaml
import sys

# Define the required fields your YAML must have
REQUIRED_FIELDS = [
    "name",
    "suite/generator/single",
    "objectives",
    "dimensionality",
    "variable type",
    "constraints",
    "dynamic",
    "noise",
    "multimodal",
    "multi-fidelity",
    "reference",
    "implementation",
    "source (real-world/artificial)",
    "textual description",
]

UNIQUE_FIELDS = ["name", "reference", "implementation"]
PROBLEMS_FILE = "problems.yaml"


def read_data(filepath):
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
            return 0, data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return 1, None
    except yaml.YAMLError as e:
        print(f"YAML syntax error: {e}")
        return 1, None


def check_format(data):
    if len(data) != 1:
        print("YAML file should contain exactly one top-level document.")
        return False
    if not isinstance(data[0], dict):
        print("Top-level document should be a dictionary.")
        return False
    return True


def check_fields(data):
    if len(data) != len(REQUIRED_FIELDS):
        print(f"YAML file should contain exactly {len(REQUIRED_FIELDS)} fields.")
        return False
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        print(f"Missing required fields: {', '.join(missing)}")
        return False
    # Check that the name is not still template
    if data.get("name") == "template":
        print("Please change the 'name' field from 'template' to a unique name.")
        return False
    return True


def check_novelty(data):
    # Load existing problems
    read_status, existing_data = read_data(PROBLEMS_FILE)
    if read_status != 0:
        print("Could not read existing problems for novelty check.")
        return False
    assert existing_data is not None
    for field in UNIQUE_FIELDS:
        existing_values = {
            entry.get(field) for entry in existing_data if isinstance(entry, dict)
        }
        if data.get(field) in existing_values:
            print(
                f"Field '{field}' with value '{data.get(field)}' already exists. Please choose a unique value."
            )
            return False
    return True


def validate_yaml(filepath):
    status, data = read_data(filepath)
    if status != 0:
        sys.exit(1)
    if not check_format(data):
        sys.exit(1)
    assert data is not None and len(data) == 1
    new_data = data[0]  # Extract the single top-level entry

    # Check required and unique fields
    if not check_fields(new_data) or not check_novelty(new_data):
        sys.exit(1)

    # YAML is valid if we reach this point
    print("YAML syntax is valid.")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_yaml.py <yourfile.yaml>")
        sys.exit(1)

    filepath = sys.argv[1]
    validate_yaml(filepath)
