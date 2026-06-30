#!/usr/bin/env python3

import json
import re
import shutil
from html import escape

import pandas as pd
from pydantic_yaml import parse_yaml_raw_as

from opltools.schema import ConstraintType, Implementation, Library, ProblemLike

URL_RE = re.compile(r'\b((?:https?://|www\.)[^\s<>"\']+)', re.IGNORECASE)
VISIBLE_VARIABLE_TYPES = ["binary", "categorical", "continuous", "integer"]
VARIABLE_COLUMN_NAME_BY_TYPE = {
    "binary": "binary Variables",
    "categorical": "categorical Variables",
    "continuous": "continuous Variables",
    "integer": "integer Variables",
}
COLUMN_DISPLAY_NAMES = {
    "problem_id": "ID",
    "long_name": "Full Name",
    "description": "Description",
    "tags": "Tags",
    "references": "References",
    "implementations": "Implementations",
    "dynamic_type": "Dynamics",
    "noise_type": "Noise",
    "allows_partial_evaluation": "Partial Evaluations",
    "can_evaluate_objectives_independently": "Independent Objectives",
    "modality": "Modality",
    "fidelity_levels": "Fidelity Levels",
    "code_examples": "Examples",
    "source": "Source",
    "binary Variables": "Binary Vars",
    "categorical Variables": "Categorical Vars",
    "continuous Variables": "Continuous Vars",
    "integer Variables": "Integer Vars",
    "Total Variables": "Total Variables",
    "Hard box Constraints": "Hard Box Constraints",
    "Soft box Constraints": "Soft Box Constraints",
    "Hard linear Constraints": "Hard Linear Constraints",
    "Soft linear Constraints": "Soft Linear Constraints",
    "Hard function Constraints": "Hard Function Constraints",
    "Soft function Constraints": "Soft Function Constraints",
    "Total Constraints": "Total Constraints",
    "Variable Types": "Variable Types",
    "Constraint Types": "Constraint Types",
    "Properties": "Properties",
    "Implementation Names": "Implementation Names",
    "Implementation Languages": "Implementation Languages",
    "Implementation Evaluation Times": "Implementation Evaluation Times",
    "Implementation Links": "Implementation Links",
    "Implementation Descriptions": "Implementation Descriptions",
    "Implementation Requirements": "Implementation Requirements",
}
DEFAULT_VISIBLE_COLUMNS = {
    "Name",
    "Type",
    "Objectives",
    "Dynamics",
    "Noise",
    "Partial Evaluations",
    "Independent Objectives",
    "Fidelity Levels",
    "Variable Types",
    "Constraint Types",
    "Properties",
    "Total Variables",
    "Total Constraints",
}


def linkify_cell(value):
    if not isinstance(value, str):
        return value

    def repl(match):
        url = match.group(1)
        href = url if url.lower().startswith(("http://", "https://")) else f"https://{url}"
        return f'<a href="{href}">{url}</a>'

    return URL_RE.sub(repl, value)


def to_problem_id(value):
    if not isinstance(value, str):
        return ""

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    normalized = re.sub(r"[^a-z0-9_]", "", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized


def display_column_name(column):
    mapped = COLUMN_DISPLAY_NAMES.get(column)
    if mapped:
        return mapped

    text = str(column or "").replace("_", " ").strip()
    if not text:
        return str(column)

    words = []
    for word in text.split():
        words.append("ID" if word.lower() == "id" else word.capitalize())
    return " ".join(words)


def add_problem_id_row_attributes(table_html, problem_ids):
    marker = "<tbody>"
    if marker not in table_html:
        return table_html

    body_start = table_html.index(marker) + len(marker)
    prefix = table_html[:body_start]
    body = table_html[body_start:]

    for problem_id in problem_ids:
        safe_id = escape(problem_id, quote=True)
        body = body.replace("<tr>", f'<tr data-problem-id="{safe_id}">', 1)

    return prefix + body


def format_type(value):
    text = str(value or "").strip().lower()
    if text == "opltype.problem":
        return "Problem"
    if text == "opltype.generator":
        return "Generator"
    if text == "opltype.suite":
        return "Suite"
    return str(value or "")


def format_references(refs):
    if not refs:
        return ""

    parts = []
    for ref in refs:
        ref_dict = ref.model_dump() if hasattr(ref, "model_dump") else ref
        if not isinstance(ref_dict, dict):
            parts.append(str(ref_dict))
            continue

        title = str(ref_dict.get("title") or "").strip()
        authors = ref_dict.get("authors") or []
        if isinstance(authors, list):
            authors_txt = "; ".join(str(author) for author in authors if author)
        else:
            authors_txt = str(authors).strip()

        link = ref_dict.get("link") or {}
        if hasattr(link, "model_dump"):
            link = link.model_dump()
        if isinstance(link, dict):
            url = str(link.get("url") or "").strip()
        else:
            url = str(link).strip()

        triplet = ", ".join(part for part in [title, authors_txt, url] if part)
        if triplet:
            parts.append(triplet)

    return " | ".join(parts)


def normalize_variable_type_name(raw_type):
    text = str(raw_type or "").strip().lower().split(".")[-1]
    if text in VISIBLE_VARIABLE_TYPES:
        return text
    return "unknown"


def format_dim(dim):
    if dim is None:
        return ""
    if isinstance(dim, (int, float)):
        return str(dim)
    if hasattr(dim, "model_dump"):
        dim = dim.model_dump()
    if isinstance(dim, set):
        dim = sorted(dim)
    if isinstance(dim, list):
        return "{" + ", ".join(str(item) for item in dim) + "}"
    if isinstance(dim, dict):
        dmin = dim.get("min")
        dmax = dim.get("max")
        if dmin is not None and dmax is not None:
            return f"{dmin}-{dmax}"
        if dmin is not None:
            return f">={dmin}"
        if dmax is not None:
            return f"<={dmax}"
        return ""
    return str(dim)


def format_total_bounds(total_min, total_max):
    if total_min is None and total_max is None:
        return ""
    if total_min is not None and total_max is not None and total_min == total_max:
        return str(total_min)
    if total_min is not None and total_max is not None:
        return f"{total_min}-{total_max}"
    if total_min is not None:
        return f">={total_min}"
    if total_max is not None:
        return f"<={total_max}"
    return ""


def unique_preserve_order(values):
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def dim_domain(dim):
    if dim is None:
        return None

    if hasattr(dim, "model_dump"):
        dim = dim.model_dump()

    if isinstance(dim, (int, float)):
        return {"kind": "set", "values": [int(dim)]}

    if isinstance(dim, set):
        dim = sorted(dim)

    if isinstance(dim, list):
        numeric = [int(item) for item in dim if isinstance(item, (int, float))]
        if not numeric:
            return None
        return {"kind": "set", "values": unique_preserve_order(numeric)}

    if isinstance(dim, dict):
        dmin = dim.get("min")
        dmax = dim.get("max")
        dmin = int(dmin) if isinstance(dmin, (int, float)) else None
        dmax = int(dmax) if isinstance(dmax, (int, float)) else None
        if dmin is None and dmax is None:
            return None
        return {"kind": "range", "min": dmin, "max": dmax}

    return None


def combine_domains_for_total(domains):
    if not domains:
        return ""

    if any(domain["kind"] == "range" for domain in domains):
        total_min = 0
        total_max = 0
        open_upper = False
        for domain in domains:
            if domain["kind"] == "set":
                values = domain["values"]
                if not values:
                    continue
                total_min += min(values)
                total_max += max(values)
                continue

            dmin = domain.get("min")
            dmax = domain.get("max")
            total_min += dmin or 0
            if dmax is None:
                open_upper = True
            else:
                total_max += dmax

        return format_total_bounds(total_min, None if open_upper else total_max)

    totals = [0]
    for domain in domains:
        new_totals = []
        for base in totals:
            for value in domain["values"]:
                new_totals.append(base + value)
        totals = unique_preserve_order(new_totals)

    if not totals:
        return ""
    if len(totals) == 1:
        return str(totals[0])
    return "{" + ", ".join(str(value) for value in totals) + "}"


def format_variables_by_type(variables):
    values = {variable_type: [] for variable_type in VISIBLE_VARIABLE_TYPES}
    domains = []

    if not variables:
        return values, ""

    for variable in variables:
        variable_dict = variable.model_dump() if hasattr(variable, "model_dump") else variable
        if not isinstance(variable_dict, dict):
            continue

        variable_type = normalize_variable_type_name(variable_dict.get("type"))
        dim = variable_dict.get("dim")
        dim_text = format_dim(dim)
        if variable_type in values and dim_text:
            values[variable_type].append(dim_text)

        domain = dim_domain(dim)
        if domain is not None:
            domains.append(domain)

    for variable_type in sorted(list(values.keys())):
        values[variable_type] = " | ".join(sorted(values[variable_type]))

    return values, combine_domains_for_total(domains)


def normalize_constraint_type(raw_type):
    text = str(raw_type or "").strip().lower().split(".")[-1]
    return text if text else "unknown"


def normalize_constraint_hard(raw_hard):
    text = str(raw_hard or "").strip().lower().split(".")[-1]
    if text in {"yes", "hard", "true"}:
        return "hard"
    if text in {"no", "soft", "false"}:
        return "soft"
    if text in {"some", "mixed", "both"}:
        return "mixed"
    return "unknown"


def list_variable_types(variables):
    if not variables:
        return ""

    types = []
    for variable in variables:
        variable_dict = variable.model_dump() if hasattr(variable, "model_dump") else variable
        if not isinstance(variable_dict, dict):
            continue
        types.append(normalize_variable_type_name(variable_dict.get("type")))

    types = [v for v in unique_preserve_order(types) if v]
    if not types:
        return ""
    return " | ".join(sorted(types))


def list_constraint_types(constraints):
    if not constraints:
        return ""

    types = []
    for constraint in constraints:
        constraint_dict = constraint.model_dump() if hasattr(constraint, "model_dump") else constraint
        if not isinstance(constraint_dict, dict):
            continue
        types.append(normalize_constraint_type(constraint_dict.get("type")))

    types = [c for c in unique_preserve_order(types) if c]
    if not types:
        return ""
    return " | ".join(sorted(types))


def has_nonzero_info(value, yes_only=False):
    if value is None:
        return False

    if isinstance(value, (set, list, tuple, dict)):
        if len(value) == 1:
            return has_nonzero_info(next(iter(value)), yes_only=yes_only)
        else:
            return len(value) > 0

    text = str(value).strip().lower()
    if not text:
        return False

    if yes_only:
        return text in {"yes", "some", "true", "1"}

    return text not in {"no", "none", "null", "unknown", "?", "0", "false", "[]", "{}"}


def build_properties(item):
    properties = []
    if has_nonzero_info(getattr(item, "dynamic_type", None)):
        properties.append("dynamic")
    if has_nonzero_info(getattr(item, "noise_type", None)):
        properties.append("noisy")
    if has_nonzero_info(getattr(item, "allows_partial_evaluation", None), yes_only=True):
        properties.append("partial evaluations allowed")
    if has_nonzero_info(getattr(item, "can_evaluate_objectives_independently", None), yes_only=True):
        properties.append("independent objective evaluations")
    if has_nonzero_info(getattr(item, "fidelity_levels", None)):
        if getattr(item, "fidelity_levels", None) != {1}:
            properties.append("multi-fidelity")
    if not properties:
        return ""
    return " | ".join(sorted(properties))


def format_implementation_links(links):
    if not links:
        return ""

    urls = []
    for link in links:
        link_dict = link.model_dump() if hasattr(link, "model_dump") else link
        if isinstance(link_dict, dict):
            url = str(link_dict.get("url") or "").strip()
            if url:
                urls.append(url)
        elif link_dict:
            urls.append(str(link_dict))

    if not urls:
        return ""
    return " | ".join(unique_preserve_order(urls))


def normalize_requirements(requirements):
    if requirements is None:
        return ""
    if isinstance(requirements, list):
        values = [str(item).strip() for item in requirements if str(item).strip()]
        if not values:
            return ""
        return " | ".join(unique_preserve_order(values))
    return str(requirements).strip()


def extract_implementation_fields(implementation_ids, library_items):
    result = {
        "Implementation Names": "",
        "Implementation Languages": "",
        "Implementation Evaluation Times": "",
        "Implementation Links": "",
        "Implementation Descriptions": "",
        "Implementation Requirements": "",
    }

    if not implementation_ids:
        return result

    names = []
    languages = []
    evaluation_times = []
    links = []
    descriptions = []
    requirements = []

    for implementation_id in implementation_ids:
        implementation = library_items.get(implementation_id)
        if not isinstance(implementation, Implementation):
            continue

        if implementation.name:
            names.append(str(implementation.name).strip())
        if implementation.language:
            languages.append(str(implementation.language).strip())
        if implementation.evaluation_time:
            evaluation_times.append(str(implementation.evaluation_time).strip())
        if implementation.description:
            descriptions.append(str(implementation.description).strip())

        req = normalize_requirements(implementation.requirements)
        if req:
            requirements.append(req)

        impl_links = format_implementation_links(implementation.links)
        if impl_links:
            links.extend(impl_links.split(" | "))

    result["Implementation Names"] = " | ".join(unique_preserve_order([v for v in names if v]))
    result["Implementation Languages"] = " | ".join(unique_preserve_order([v for v in languages if v]))
    result["Implementation Evaluation Times"] = " | ".join(unique_preserve_order([v for v in evaluation_times if v]))
    result["Implementation Links"] = " | ".join(unique_preserve_order([v for v in links if v]))
    result["Implementation Descriptions"] = " | ".join(unique_preserve_order([v for v in descriptions if v]))
    result["Implementation Requirements"] = " | ".join(unique_preserve_order([v for v in requirements if v]))

    return result


def format_constraint_count(number_value):
    if number_value is None:
        return ">=1"
    return format_dim(number_value)


def constraint_count_domain(number_value):
    if number_value is None:
        return {"kind": "range", "min": 1, "max": None}
    return dim_domain(number_value)


def format_constraints_by_type(constraints, constraint_types):
    hard_values = {constraint_type: [] for constraint_type in constraint_types}
    soft_values = {constraint_type: [] for constraint_type in constraint_types}
    hard_domains = []
    soft_domains = []
    total_domains = []

    if not constraints:
        return (
            {constraint_type: "" for constraint_type in constraint_types},
            {constraint_type: "" for constraint_type in constraint_types},
            "",
            "",
            "",
        )

    for constraint in constraints:
        constraint_dict = constraint.model_dump() if hasattr(constraint, "model_dump") else constraint
        if not isinstance(constraint_dict, dict):
            continue

        constraint_type = normalize_constraint_type(constraint_dict.get("type"))
        count_text = format_constraint_count(constraint_dict.get("number"))
        count_domain = constraint_count_domain(constraint_dict.get("number"))
        hardness = normalize_constraint_hard(constraint_dict.get("hard"))
        if count_domain is not None:
            total_domains.append(count_domain)

        if hardness == "hard":
            if constraint_type in hard_values:
                hard_values[constraint_type].append(count_text)
            if count_domain is not None:
                hard_domains.append(count_domain)
        elif hardness == "soft":
            if constraint_type in soft_values:
                soft_values[constraint_type].append(count_text)
            if count_domain is not None:
                soft_domains.append(count_domain)
        else:
            if constraint_type in hard_values:
                hard_values[constraint_type].append(count_text)
            if constraint_type in soft_values:
                soft_values[constraint_type].append(count_text)
            if count_domain is not None:
                hard_domains.append(count_domain)
                soft_domains.append(count_domain)

    for constraint_type in constraint_types:
        hard_values[constraint_type] = " | ".join(sorted(hard_values[constraint_type]))
        soft_values[constraint_type] = " | ".join(sorted(soft_values[constraint_type]))

    hard_total = combine_domains_for_total(hard_domains)
    soft_total = combine_domains_for_total(soft_domains)
    total_constraints = combine_domains_for_total(total_domains)
    return hard_values, soft_values, hard_total, soft_total, total_constraints


def normalize_scalar(value):
    if value is None:
        return ""
    if hasattr(value, "value") and not isinstance(value, (str, int, float, bool)):
        return normalize_scalar(value.value)
    if isinstance(value, (str, int, float, bool)):
        return value
    return value


def normalize_recursive(value):
    value = normalize_scalar(value)
    if value in (None, ""):
        return ""

    if hasattr(value, "model_dump"):
        value = value.model_dump()

    if isinstance(value, dict):
        normalized = {key: normalize_recursive(item) for key, item in value.items()}
        return {key: item for key, item in normalized.items() if item not in ["", [], {}, set()]}

    if isinstance(value, set):
        normalized_items = [normalize_recursive(item) for item in value]
        normalized_items = [item for item in normalized_items if item not in ["", [], {}, set()]]
        normalized_items = sorted(normalized_items, key=str)
        if len(normalized_items) == 1:
            return normalized_items[0]
        return normalized_items

    if isinstance(value, list):
        normalized_items = [normalize_recursive(item) for item in value]
        normalized_items = [item for item in normalized_items if item not in ["", [], {}, set()]]
        if len(normalized_items) == 1:
            return normalized_items[0]
        return normalized_items

    return value


def to_cell(value):
    normalized = normalize_recursive(value)
    if normalized in ("", None):
        return ""
    if isinstance(normalized, (str, int, float, bool)):
        return str(normalized)
    return json.dumps(normalized, ensure_ascii=False)


def load_library(path):
    with open(path, encoding="utf-8") as yaml_input:
        raw = yaml_input.read()
    return parse_yaml_raw_as(Library, raw)


def build_problemlike_dataframe(library):
    library_items = library.root if hasattr(library, "root") else {}
    problemlike_items = {
        item_key: item
        for item_key, item in library_items.items()
        if isinstance(item, ProblemLike)
    }
    problemlike_fields = list(ProblemLike.model_fields.keys())
    constraint_types = [constraint_type.value for constraint_type in ConstraintType if constraint_type.value != "unknown"]

    rows = []
    for item_key, item in problemlike_items.items():
        row = {"problem_id": item_key or to_problem_id(getattr(item, "name", ""))}
        raw_variables = getattr(item, "variables", None)
        raw_constraints = getattr(item, "constraints", None)
        raw_implementations = getattr(item, "implementations", None)
        variable_values, variable_total = format_variables_by_type(raw_variables)
        hard_constraints, soft_constraints, hard_total, soft_total, total_constraints = format_constraints_by_type(
            raw_constraints,
            constraint_types,
        )

        for field in problemlike_fields:
            value = getattr(item, field, None)
            if field == "references":
                row[field] = format_references(value)
            elif field == "type":
                row[field] = format_type(value)
            elif field in {"variables", "constraints"}:
                continue
            else:
                row[field] = to_cell(value)

        for variable_type in VISIBLE_VARIABLE_TYPES:
            row[VARIABLE_COLUMN_NAME_BY_TYPE[variable_type]] = variable_values.get(variable_type, "")
        row["Total Variables"] = variable_total
        row["Variable Types"] = list_variable_types(raw_variables)
        row["Constraint Types"] = list_constraint_types(raw_constraints)
        row["Properties"] = build_properties(item)
        row.update(extract_implementation_fields(raw_implementations, library_items))

        for constraint_type in constraint_types:
            row[f"Hard {constraint_type} Constraints"] = hard_constraints.get(constraint_type, "")
            row[f"Soft {constraint_type} Constraints"] = soft_constraints.get(constraint_type, "")
        row["Total Constraints"] = total_constraints
        rows.append(row)

    base_columns = ["problem_id"] + [field for field in problemlike_fields if field not in {"variables", "constraints"}]
    split_variable_columns = [
        "Variable Types",
        "binary Variables",
        "categorical Variables",
        "continuous Variables",
        "integer Variables",
        "Total Variables",
    ]
    split_implementation_columns = [
        "Implementation Names",
        "Implementation Languages",
        "Implementation Evaluation Times",
        "Implementation Links",
        "Implementation Descriptions",
        "Implementation Requirements",
    ]
    split_constraint_columns = []
    for constraint_type in constraint_types:
        split_constraint_columns.append(f"Hard {constraint_type} Constraints")
        split_constraint_columns.append(f"Soft {constraint_type} Constraints")
    split_constraint_columns += ["Constraint Types", "Total Constraints", "Properties"]

    all_columns = base_columns + split_variable_columns + split_implementation_columns + split_constraint_columns

    # Keep id/type before name, then enforce the requested high-priority reading order.
    preferred_order = [
        "problem_id",
        "name",
        "type",
        "Variable Types",
        "Total Variables",
        "objectives",
        "Properties",
        "Constraint Types",
        "Total Constraints",
        "dynamic_type",
        "noise_type",
        "allows_partial_evaluation",
        "can_evaluate_objectives_independently",
        "fidelity_levels",
    ]
    table_columns = [column for column in preferred_order if column in all_columns]
    table_columns += [column for column in all_columns if column not in table_columns]
    dataframe = pd.DataFrame(rows, columns=table_columns)
    dataframe = dataframe.fillna("")
    return dataframe.rename(columns=display_column_name)


def render_table(dataframe):
    linked_data = dataframe.map(linkify_cell)
    table_html = linked_data.to_html(
        render_links=False,
        escape=False,
        index=False,
        table_id="problems",
        classes=["display compact", "display", "styled-table"],
        border=0,
        na_rep="",
    )
    table_html = add_problem_id_row_attributes(table_html, dataframe["ID"].astype(str).tolist())
    footer = "<tfoot><tr>" + " ".join(f"<th>{escape(column)}</th>" for column in dataframe.columns) + "</tr></tfoot>"
    idx = table_html.index("</table>")
    return table_html[:idx] + footer + table_html[idx:]


def render_column_toggles(columns):
    return "".join(
        (
            f'<label class="column-chip">'
            f'<input class="col-toggle" type="checkbox" data-column="{index}"'
            f'{" checked" if column in DEFAULT_VISIBLE_COLUMNS else ""}>'
            f'<span>{escape(column)}</span>'
            f'</label>'
        )
        for index, column in enumerate(columns)
    )


def build_html_page(table_markup, docs_dir):
    html_table = f"{docs_dir}problems.html"
    html_header = f"{docs_dir}header.html"
    html_scripts = f"{docs_dir}javascript.html"
    html_footer = f"{docs_dir}footer.html"
    html_index = f"{docs_dir}index.html"

    with open(html_table, "w", encoding="utf-8") as table_file:
        table_file.write(table_markup)

    with open(html_index, "wb") as output_file:
        for part_path in [html_header, html_table, html_scripts, html_footer]:
            with open(part_path, "rb") as part_file:
                shutil.copyfileobj(part_file, output_file)


if __name__ == "__main__":
    yaml_file = "problems.yaml"
    html_dir = "docs/"
    html_table_template = f"{html_dir}table_template.html"

    try:
        library = load_library(yaml_file)
    except Exception as exc:
        raise SystemExit(f"Error parsing YAML file '{yaml_file}': {exc}") from exc

    data = build_problemlike_dataframe(library)
    final_table = render_table(data)
    column_toggles = render_column_toggles(data.columns)

    with open(html_table_template, encoding="utf-8") as template_file:
        table_template = template_file.read()

    table_markup = (
        table_template
        .replace("__COLUMN_TOGGLES__", column_toggles)
        .replace("__TABLE__", final_table)
    )
    build_html_page(table_markup, html_dir)
