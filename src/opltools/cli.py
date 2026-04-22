import sys
import argparse
from pydantic import ValidationError
import yaml

from opltools.schema import Library

UNIQUE_FIELDS = ["name"]
UNIQUE_WARNING_FIELDS = ["reference", "implementation"]


def cmd_validate(args):

    try:
        with open(args.file, "r") as f:
            lib = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except yaml.YAMLError as e:
        print(f"Error: YAML syntax error in {args.file}: {e}", file=sys.stderr)
        return 1

    try:
        Library.model_validate(
            lib,
            context={
                "unique_error_fields": args.unique_error_field,
                "unique_warning_fields": args.unique_warning_field,
            },
        )
        print(f"{args.file}: OK")
        return 0
    except ValidationError as e:
        for error in e.errors():
            loc = (
                " -> ".join(str(p) for p in error["loc"]) if error["loc"] else "(root)"
            )
            print(f"{args.file}: {loc}: {error['msg']}")
        return 1


def main():
    parser = argparse.ArgumentParser(prog="opl", description="OPL tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a YAML file against the Library schema"
    )
    validate_parser.add_argument("file", help="YAML file to validate")
    # Add unique error fields
    validate_parser.add_argument(
        "--unique-error-field",
        action="append",
        help="Field that must be unique across all entries (can be specified multiple times)",
    )
    validate_parser.add_argument(
        "--unique-warning-field",
        action="append",
        help="Field that should be unique across all entries (can be specified multiple times)",
    )
    # specify default unique fields if not provided
    validate_parser.set_defaults(
        unique_error_field=UNIQUE_FIELDS, unique_warning_field=UNIQUE_WARNING_FIELDS
    )

    args = parser.parse_args()

    if args.command == "validate":
        sys.exit(cmd_validate(args))


if __name__ == "__main__":
    main()
