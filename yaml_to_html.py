#!/usr/bin/env python3

import pandas as pd
import yaml
import shutil
from html import escape

import re

URL_RE = re.compile(r'\b((?:https?://|www\.)[^\s<>"\']+)', re.IGNORECASE)


def linkify_cell(value):
    if not isinstance(value, str):
        return value

    def repl(m):
        url = m.group(1)
        href = url if url.lower().startswith(("http://", "https://")) else f"https://{url}"
        return f'<a href="{href}">{url}</a>'

    return URL_RE.sub(repl, value)

yaml_file = "problems.yaml"

html_dir = "docs/"
html_table = f"{html_dir}problems.html"
html_header = f"{html_dir}header.html"
html_scripts = f"{html_dir}javascript.html"
html_footer = f"{html_dir}footer.html"
html_index = f"{html_dir}index.html"

# Load data
with open(yaml_file) as yaml_input:
    data = pd.json_normalize(yaml.safe_load(yaml_input))

# Choose desired columns
all_columns = False
default_columns = ["name",
                   "textual description",
                   "suite/generator/single",
                   "objectives",
                   "dimensionality",
                   "variable type",
                   "constraints",
                   "dynamic",
                   "noise",
                   "multi-fidelity",
                   "source (real-world/artificial)",
                   "reference",
                   "implementation"]

if all_columns is False:
    columns = default_columns
    data = data[columns]

data = data.map(linkify_cell)

# Generate plain table
table = data.to_html(render_links=False,
                     escape=False,  # Don't escape HTML in cells (to allow links)
                     index=False,
                     table_id="problems",
                     classes=["display compact", "display", "styled-table"],  # Set display style
                     border=0,
                     na_rep="")  # Leave NaN cells empty

# Add footer to facilitate individual column search
idx = table.index('</table>')
final_table = table[:idx] + "<tfoot><tr>" + " ".join(["<th>"+ i +"</th>" for i in data.columns])+"</tr> </tfoot>" + table[idx:]

default_hidden_columns = {"textual description", "reference", "implementation"}

column_toggles = "".join(
    [
        (
            f'<label class="column-chip">'
            f'<input class="col-toggle" type="checkbox" data-column="{i}"'
            f'{" checked" if col not in default_hidden_columns else ""}>'
            f'<span>{escape(col)}</span>'
            f'</label>'
        )
        for i, col in enumerate(data.columns)
    ]
)

modern_table_block = f"""
<section class="table-shell">
    <div class="table-toolbar">
        <div class="toolbar-title">Visible columns</div>
        <div class="toolbar-actions">
            <button type="button" class="toolbar-btn" id="show-all-columns">Show all</button>
            <button type="button" class="toolbar-btn" id="hide-all-columns">Hide all</button>
        </div>
        <div class="column-controls">
            {column_toggles}
        </div>
    </div>
    <div class="table-wrap">
        {final_table}
    </div>
</section>

<section class="details-shell" id="problem-details" aria-live="polite">
    <h3 class="details-title">Problem details</h3>
    <p class="details-hint" id="problem-details-hint">Click a table row to inspect full details.</p>
    <dl class="details-grid" id="problem-details-content"></dl>
</section>
"""

# Write table to file
with open(html_table, "w") as table_file:
    table_file.write(modern_table_block)

# Merge table and scripts into HTML page
with open(html_index, "wb") as output_file:
    for part_path in [html_header, html_table, html_scripts, html_footer]:
        with open(part_path, "rb") as part_file:
            shutil.copyfileobj(part_file, output_file)
