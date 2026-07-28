from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path
from types import UnionType
from typing import Any, get_args, get_origin

import pandas as pd
import yaml

from opltools.schema import (
    Constraint,
    ConstraintType,
    Generator,
    Implementation,
    Library,
    Link,
    OPLType,
    Problem,
    Reference,
    Suite,
    ValueRange,
    Variable,
    VariableType,
    YesNoSome,
)


COL_NAME = "Short name of Suite / Problem / Generator"
COL_TYPE = "Type"
COL_VARIABLE_TYPES = "Types of input variables"
COL_DIM = "Number of Input variables (number or range or 'scalable')"
COL_OBJECTIVES = "Number of Objectives (number or range or 'scalable')"
COL_CONSTRAINED = "Problem Characteristics [Constrained]"
COL_DYNAMIC = "Problem Characteristics [Dynamic]"
COL_NOISY = "Problem Characteristics [Noisy]"
COL_MULTIMODAL = "Problem Characteristics [Multi-modal]"
COL_PARTIAL_EVAL = "Problem Characteristics [Partial evaluations possible]"
COL_MULTI_FIDELITY = "Problem Characteristics [Multiple fidelities]"
COL_OBJECTIVES_INDEPENDENT = "Problem Characteristics [Objectives evaluated independently]"
COL_SOURCE = "Problem Source"
COL_IMPL_LINK = "Link to Implementation"
COL_DESCRIPTION = "Short description of problem(s)"
COL_REFERENCE = "Citation / reference"
COL_FULL_NAME = "Full name of suite"
COL_CONSTRAINT_PROPERTIES = "Constraint Properties"
COL_CONSTRAINT_COUNT = "Number of constraints"
COL_DYNAMIC_TYPE = "Type of Dynamicism"
COL_NOISE_MODEL = "Form of noise model"
COL_NOISE_SPACE = "Type of noise space"
COL_NOISE_OTHER = "Other noise properties"
COL_MULTIMODAL_DESC = "Description of multimodality"
COL_IMPL_LANG = "Implemenation languages"
COL_IMPL_LINKS = "Links to implementations"
COL_EVAL_TIME = "Approximate time to evaluate a single solution (or times if e.g. multi-fidelity)"
COL_OTHER = "Other relevant information"

NO_VALUE_MARKERS = {
    "",
    "-",
    "n/a",
    "na",
    "none",
    "not found",
    "unknown",
    "not public",
    "implementation not freely available",
}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    return str(value).strip()


def is_meaningful(value: Any) -> bool:
    text = normalize_text(value)
    return bool(text) and text.lower() not in NO_VALUE_MARKERS


def split_values(value: Any) -> list[str]:
    text = normalize_text(value)
    if not text:
        return []
    parts = re.split(r"[,;\n|]+", text)
    return [p.strip() for p in parts if p.strip()]


def extract_urls(value: Any) -> list[str]:
    text = normalize_text(value)
    if not text:
        return []
    return re.findall(r"https?://[^\s,\])\"']+", text)


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    return normalized.strip("_") or "entry"


def unique_id(prefix: str, name: str, used_ids: set[str]) -> str:
    base = f"{prefix}{slugify(name)}"
    if base not in used_ids:
        used_ids.add(base)
        return base

    suffix = 2
    while True:
        candidate = f"{base}_{suffix}"
        if candidate not in used_ids:
            used_ids.add(candidate)
            return candidate
        suffix += 1


def parse_yes_no_some(value: Any) -> YesNoSome | None:
    text = normalize_text(value).lower()
    if not text:
        return None

    # Normalize common punctuation variants to make matching robust.
    text = re.sub(r"\s+", " ", text.replace("_", " ").replace("-", " ")).strip().lower()

    if text in {"not present", "not available", "absent", "no", "n", "false", "none"}:
        return YesNoSome.no
    if text in {"present", "available", "yes", "y", "true"}:
        return YesNoSome.yes
    if text in {"some", "partial", "mixed", "depends"}:
        return YesNoSome.some
    if text in {"unknown", "?"}:
        return YesNoSome.unknown

    return None


def parse_type(value: Any) -> OPLType:
    text = normalize_text(value).lower()
    if "suite" in text:
        return OPLType.suite
    if "generator" in text:
        return OPLType.generator
    return OPLType.problem


def parse_scalar_set_or_range(value: Any) -> int | set[int] | ValueRange | None:
    text = normalize_text(value)
    if not text:
        return None

    lowered = text.lower()
    numbers = [int(n) for n in re.findall(r"\d+", text)]

    if "scalable" in lowered:
        if len(numbers) >= 2:
            return ValueRange(min=min(numbers), max=max(numbers))
        if len(numbers) == 1:
            return ValueRange(min=numbers[0], max=None)
        return ValueRange(min=1, max=None)

    if (" to " in lowered or "-" in lowered) and len(numbers) >= 2:
        return ValueRange(min=min(numbers), max=max(numbers))

    if " or " in lowered and numbers:
        vals = set(numbers)
        return next(iter(vals)) if len(vals) == 1 else vals

    if len(numbers) == 1:
        return numbers[0]
    if len(numbers) > 1:
        vals = set(numbers)
        return next(iter(vals)) if len(vals) == 1 else vals
    return None


def parse_objectives(value: Any) -> set[int] | None:
    text = normalize_text(value)
    if not text:
        return None
    numbers = {int(n) for n in re.findall(r"\d+", text)}
    return numbers or None


def parse_variable_type(token: str) -> VariableType:
    lowered = token.strip().lower()
    if any(t in lowered for t in ["continuous", "real"]):
        return VariableType.continuous
    if any(t in lowered for t in ["integer", "ordinal", "int"]):
        return VariableType.integer
    if any(t in lowered for t in ["boolean", "binary", "bool"]):
        return VariableType.binary
    if any(t in lowered for t in ["categorical", "nominal", "category"]):
        return VariableType.categorical
    return VariableType.unknown


def parse_variables(var_types_value: Any, dim_value: Any) -> set[Variable] | None:
    type_tokens = split_values(var_types_value)
    dim = parse_scalar_set_or_range(dim_value)

    if not type_tokens:
        return None

    variables: set[Variable] = set()
    for token in type_tokens:
        variables.add(Variable(type=parse_variable_type(token), dim=dim))
    return variables or None


def parse_constraint_type(token: str) -> ConstraintType:
    lowered = token.lower()
    if "box" in lowered:
        return ConstraintType.box
    if "linear" in lowered:
        return ConstraintType.linear
    if "function" in lowered or "nonlinear" in lowered:
        return ConstraintType.function
    return ConstraintType.unknown


def parse_constraint_yesnosome_from_properties(
    property_tokens: list[str],
    positive_terms: tuple[str, ...],
    negative_terms: tuple[str, ...],
) -> YesNoSome | None:
    if not property_tokens:
        return None

    lowered = [token.lower() for token in property_tokens]

    def _matches_term(token: str, term: str) -> bool:
        # Non-word terms (like <=) are matched as substrings; words use boundaries.
        if not re.search(r"\w", term):
            return term in token
        pattern = rf"\b{re.escape(term.strip())}\b"
        return re.search(pattern, token) is not None

    has_positive = any(any(_matches_term(token, term) for term in positive_terms) for token in lowered)
    has_negative = any(any(_matches_term(token, term) for term in negative_terms) for token in lowered)

    if has_positive and has_negative:
        return YesNoSome.some
    if has_positive:
        return YesNoSome.yes
    if has_negative:
        return YesNoSome.no
    return None


def parse_constraints(row: dict[str, Any]) -> set[Constraint] | None:
    constrained = parse_yes_no_some(row.get(COL_CONSTRAINED))
    if constrained == YesNoSome.no:
        # Explicitly encode unconstrained problems as an empty set.
        return set()
    if constrained is None:
        return None

    number = parse_scalar_set_or_range(row.get(COL_CONSTRAINT_COUNT))
    property_tokens = split_values(row.get(COL_CONSTRAINT_PROPERTIES))

    hard = parse_constraint_yesnosome_from_properties(
        property_tokens=property_tokens,
        positive_terms=("hard",),
        negative_terms=("soft",),
    )
    equality = parse_constraint_yesnosome_from_properties(
        property_tokens=property_tokens,
        positive_terms=("equality", "equal", "==", "eq"),
        negative_terms=("inequality", "inequal", "<", ">", "<=", ">="),
    )

    types = {parse_constraint_type(t) for t in property_tokens if t.strip()}
    if not types:
        types = {ConstraintType.unknown}

    constraints: set[Constraint] = set()
    for ctype in types:
        constraints.add(Constraint(type=ctype, hard=hard, equality=equality, number=number))
    return constraints


def parse_source(value: Any) -> set[str] | None:
    text = normalize_text(value).lower()
    if not text:
        return None
    if "real" in text:
        return {"real-world"}
    if "artificial" in text:
        return {"artificial"}
    return {normalize_text(value)}


def parse_modality(simple_value: Any, detail_value: Any) -> set[str] | None:
    flag = parse_yes_no_some(simple_value)
    if flag == YesNoSome.yes:
        detailed = split_values(detail_value)
        return {d.lower() for d in detailed} or {"multimodal"}
    if flag == YesNoSome.no:
        return {"unimodal"}
    return None


def parse_dynamic_type(simple_value: Any, detail_value: Any) -> set[str] | None:
    flag = parse_yes_no_some(simple_value)
    if flag == YesNoSome.no:
        return {"none"}
    if flag == YesNoSome.yes:
        detailed = split_values(detail_value)
        return {d.lower() for d in detailed} or {"dynamic"}
    return None


def parse_noise_type(simple_value: Any, model_value: Any, space_value: Any, other_value: Any) -> set[str] | None:
    flag = parse_yes_no_some(simple_value)
    if flag == YesNoSome.no:
        return {"none"}
    if flag != YesNoSome.yes:
        return None

    vals = split_values(model_value) + split_values(space_value) + split_values(other_value)
    return {v.lower() for v in vals} or {"noisy"}


def parse_fidelity_levels(value: Any) -> set[int] | None:
    flag = parse_yes_no_some(value)
    if flag == YesNoSome.yes:
        return {1, 2}
    if flag == YesNoSome.no:
        return {1}
    return None


def parse_reference(value: Any, fallback_title: str) -> set[Reference] | None:
    text = normalize_text(value)
    if not is_meaningful(text):
        return None

    urls = extract_urls(text)
    if urls:
        return {Reference(title=fallback_title, authors=[], link=Link(url=urls[0]))}

    return {Reference(title=text, authors=[])}


def _union_contains_type(annotation: Any, target: type) -> bool:
    origin = get_origin(annotation)
    if origin in (UnionType,):
        return any(_union_contains_type(arg, target) for arg in get_args(annotation))
    # typing.Union may still appear depending on runtime typing machinery.
    if str(origin) == "typing.Union":
        return any(_union_contains_type(arg, target) for arg in get_args(annotation))
    return annotation is target


def _field_allows_set_of_str(model_cls: type, field_name: str) -> bool:
    field = model_cls.model_fields.get(field_name)
    if field is None:
        return True

    annotation = field.annotation
    if _union_contains_type(annotation, set):
        return True

    origin = get_origin(annotation)
    if origin is set:
        args = get_args(annotation)
        return not args or args == (str,)

    for arg in get_args(annotation):
        if get_origin(arg) is set:
            sub_args = get_args(arg)
            if not sub_args or sub_args == (str,):
                return True

    return False


def parse_eval_time(value: Any, model_cls: type) -> set[str] | str | None:
    parts = split_values(value)
    cleaned = {p.strip() for p in parts if p.strip()}
    if not cleaned:
        return None

    if _field_allows_set_of_str(model_cls, "evaluation_time"):
        return cleaned

    # Backward compatibility for schema variants where evaluation_time is a string.
    return "; ".join(sorted(cleaned))


def parse_implementation_requirements(primary_link_value: Any) -> str | None:
    text = normalize_text(primary_link_value)
    if not text:
        return None
    if extract_urls(text):
        return None
    if text.lower() in NO_VALUE_MARKERS:
        return None
    return text


def make_implementation(row: dict[str, Any], thing_name: str, used_ids: set[str]) -> tuple[str, Implementation] | None:
    impl_links = extract_urls(row.get(COL_IMPL_LINK)) + extract_urls(row.get(COL_IMPL_LINKS))
    impl_links = list(dict.fromkeys(impl_links))

    links = [Link(type="repository", url=url) for url in impl_links] or None
    language = normalize_text(row.get(COL_IMPL_LANG)) or None
    eval_time = parse_eval_time(row.get(COL_EVAL_TIME), Implementation)
    requirements = parse_implementation_requirements(row.get(COL_IMPL_LINK))

    has_info = any([links, language, eval_time, requirements])
    if not has_info:
        return None

    impl_name = thing_name
    impl_description = normalize_text(row.get(COL_DESCRIPTION)) or f"Implementation for {thing_name}"

    impl = Implementation(
        name=impl_name,
        description=impl_description,
        links=links,
        language=language,
        evaluation_time=eval_time,
        requirements=requirements,
    )
    impl_id = unique_id("impl_", thing_name, used_ids)
    return impl_id, impl


def make_thing(row: dict[str, Any], used_ids: set[str]) -> tuple[str, Problem | Suite | Generator, tuple[str, Implementation] | None] | None:
    name = normalize_text(row.get(COL_NAME))
    if not name:
        return None

    opl_type = parse_type(row.get(COL_TYPE))
    obj = parse_objectives(row.get(COL_OBJECTIVES))
    variables = parse_variables(row.get(COL_VARIABLE_TYPES), row.get(COL_DIM))
    constraints = parse_constraints(row)
    source = parse_source(row.get(COL_SOURCE))
    modality = parse_modality(row.get(COL_MULTIMODAL), row.get(COL_MULTIMODAL_DESC))
    dynamic_type = parse_dynamic_type(row.get(COL_DYNAMIC), row.get(COL_DYNAMIC_TYPE))
    noise_type = parse_noise_type(
        row.get(COL_NOISY), row.get(COL_NOISE_MODEL), row.get(COL_NOISE_SPACE), row.get(COL_NOISE_OTHER)
    )
    partial = parse_yes_no_some(row.get(COL_PARTIAL_EVAL))
    objectives_independent = parse_yes_no_some(row.get(COL_OBJECTIVES_INDEPENDENT))
    fidelity_levels = parse_fidelity_levels(row.get(COL_MULTI_FIDELITY))
    references = parse_reference(row.get(COL_REFERENCE), fallback_title=name)

    long_name = normalize_text(row.get(COL_FULL_NAME)) or None
    description = normalize_text(row.get(COL_DESCRIPTION)) or None

    impl_data = make_implementation(row, name, used_ids)
    implementations = {impl_data[0]} if impl_data else None

    common_kwargs = dict(
        name=name,
        long_name=long_name,
        description=description,
        references=references,
        implementations=implementations,
        objectives=obj,
        variables=variables,
        constraints=constraints,
        dynamic_type=dynamic_type,
        noise_type=noise_type,
        allows_partial_evaluation=partial,
        can_evaluate_objectives_independently=objectives_independent,
        modality=modality,
        fidelity_levels=fidelity_levels,
        evaluation_time=parse_eval_time(row.get(COL_EVAL_TIME), Problem),
        source=source,
    )

    if is_meaningful(row.get(COL_OTHER)):
        common_kwargs["tags"] = {"form-submission"}

    if opl_type == OPLType.problem:
        thing = Problem(**common_kwargs)
        thing_id = unique_id("fn_", name, used_ids)
    elif opl_type == OPLType.suite:
        thing = Suite(**common_kwargs)
        thing_id = unique_id("suite_", name, used_ids)
    else:
        thing = Generator(**common_kwargs)
        thing_id = unique_id("gen_", name, used_ids)

    return thing_id, thing, impl_data


def load_existing_library(path: Path) -> dict[str, Problem | Suite | Generator | Implementation]:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as in_file:
        raw = yaml.safe_load(in_file) or {}

    # PyYAML interprets bare `yes` / `no` as booleans. Also, historical files may
    # encode unknown as either `unknown` or `?` depending on schema version.
    # Normalize values for fields that are modeled as YesNoSome enums.
    yes_no_some_fields = {
        "hard",
        "equality",
        "allows_partial_evaluation",
        "can_evaluate_objectives_independently",
    }

    enum_values = {str(member.value).lower(): str(member.value) for member in YesNoSome}
    unknown_target = enum_values.get("unknown") or enum_values.get("?")

    def _normalize_yes_no_some_value(value: Any) -> Any:
        if isinstance(value, bool):
            return enum_values.get("yes") if value else enum_values.get("no")

        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"yes", "y", "true", "1", "present"}:
                return enum_values.get("yes")
            if lowered in {"no", "n", "false", "0", "not present"}:
                return enum_values.get("no")
            if lowered in {"some", "partial", "mixed", "depends"}:
                return enum_values.get("some")
            if lowered in {"unknown", "?"} and unknown_target is not None:
                return unknown_target

        return value

    def _normalize_yes_no_some_bools(value: Any, key: str | None = None) -> Any:
        if isinstance(value, dict):
            return {k: _normalize_yes_no_some_bools(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [_normalize_yes_no_some_bools(v, key) for v in value]
        if key in yes_no_some_fields:
            normalized = _normalize_yes_no_some_value(value)
            if normalized is not None:
                return normalized
        return value

    raw = _normalize_yes_no_some_bools(raw)

    library = Library.model_validate(raw)
    return dict(library.root)


def dump_library(path: Path, root: dict[str, Problem | Suite | Generator | Implementation]) -> None:
    # model_dump(mode="json") converts enums and nested pydantic models to plain YAML-safe values.
    serializable = {key: value.model_dump(mode="json") for key, value in root.items()}
    with path.open("w", encoding="utf-8") as out_file:
        yaml.safe_dump(serializable, out_file, sort_keys=False, allow_unicode=False)


def convert(
    csv_path: Path,
    existing_yaml_path: Path,
    output_yaml_path: Path,
    dry_run: bool,
    override: bool,
) -> tuple[int, int, int]:
    df = pd.read_csv(csv_path).fillna("")
    existing_root = load_existing_library(existing_yaml_path)

    used_ids = set(existing_root)
    existing_names_to_ids: dict[str, set[str]] = {}
    for existing_id, existing_thing in existing_root.items():
        existing_names_to_ids.setdefault(existing_thing.name.casefold(), set()).add(existing_id)
    new_names: set[str] = set()

    added_things = 0
    added_impls = 0
    skipped_rows = 0

    for row in df.to_dict(orient="records"):
        name = normalize_text(row.get(COL_NAME))
        if not name:
            skipped_rows += 1
            continue

        if name.casefold() == "test":
            skipped_rows += 1
            continue

        key_name = name.casefold()
        if key_name in existing_names_to_ids:
            if not override:
                skipped_rows += 1
                continue

            # Remove previously stored entries with the same name so this row can replace them.
            ids_to_remove = list(existing_names_to_ids[key_name])
            for existing_id in ids_to_remove:
                existing_thing = existing_root.pop(existing_id, None)
                used_ids.discard(existing_id)
                if existing_thing is None:
                    continue

                # Remove old linked implementations so references stay clean when replacing.
                implementations = getattr(existing_thing, "implementations", None)
                if implementations:
                    for impl_id in list(implementations):
                        existing_root.pop(impl_id, None)
                        used_ids.discard(impl_id)

            existing_names_to_ids.pop(key_name, None)
            new_names.discard(key_name)
        elif key_name in new_names:
            skipped_rows += 1
            continue

        result = make_thing(row, used_ids)
        if result is None:
            skipped_rows += 1
            continue

        thing_id, thing, impl_data = result
        existing_root[thing_id] = thing
        existing_names_to_ids.setdefault(key_name, set()).add(thing_id)
        added_things += 1
        new_names.add(key_name)

        if impl_data:
            impl_id, impl = impl_data
            existing_root[impl_id] = impl
            existing_names_to_ids.setdefault(key_name, set()).add(impl_id)
            added_impls += 1

    # Validate merged result before writing.
    Library(root=existing_root)

    if not dry_run:
        dump_library(output_yaml_path, existing_root)

    return added_things, added_impls, skipped_rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert OPL form CSV rows into schema objects and merge into a YAML library."
    )
    parser.add_argument("--csv", default="OPL_form.csv", help="Input CSV file")
    parser.add_argument(
        "--existing-yaml",
        default="../problems.yaml",
        help="Existing OPL library YAML to merge into",
    )
    parser.add_argument(
        "--output-yaml",
        default="../problems.yaml",
        help="Output YAML path (defaults to updating existing file)",
    )
    parser.add_argument(
        "--override",
        action="store_true",
        help="Override existing YAML entries with same name using form data rows",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate conversion without writing")
    args = parser.parse_args()

    added_things, added_impls, skipped = convert(
        csv_path=Path(args.csv),
        existing_yaml_path=Path(args.existing_yaml),
        output_yaml_path=Path(args.output_yaml),
        dry_run=args.dry_run,
        override=args.override,
    )

    print(f"Added entities: {added_things}")
    print(f"Added implementations: {added_impls}")
    print(f"Skipped rows: {skipped}")
    if args.dry_run:
        print("Dry-run mode: output file was not written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())