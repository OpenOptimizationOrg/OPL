import sys
import argparse
from pydantic import ValidationError
from pydantic_yaml import parse_yaml_raw_as

from .schema import Library


def cmd_validate(args):
    try:
        with open(args.file) as f:
            raw = f.read()
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 1

    try:
        parse_yaml_raw_as(Library, raw)
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

    args = parser.parse_args()

    if args.command == "validate":
        sys.exit(cmd_validate(args))


if __name__ == "__main__":
    main()
