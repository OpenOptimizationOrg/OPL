#!/usr/bin/env python3

import pandas as pd
import yaml
import shutil

yaml_file = "problems.yaml"

html_dir = "docs/"
html_table = f"{html_dir}problems.html"
html_header = f"{html_dir}header.html"
html_scripts = f"{html_dir}javascript.html"
html_footer = f"{html_dir}footer.html"
html_index = f"{html_dir}index.html"

# Load data
with open(yaml_file) as in_file:
    data = pd.json_normalize(yaml.safe_load(in_file))

# Choose desired columns
all_columns = True

if all_columns is False:
    columns = ["name", "objectives"]  # Desired columns
    data = data[columns]

# Generate plain table
table = data.to_html(render_links=True,
                     index=False,
                     table_id="problems",
                     classes=["display compact", "display", "styled-table"],  # Set display style
                     border=0,
                     na_rep="")  # Leave NaN cells empty

# Add footer to facilitate individual column search
idx = table.index('</table>')
final_table = table[:idx] + "<tfoot><tr>" + " ".join(["<th>"+ i +"</th>" for i in data.columns])+"</tr> </tfoot>" + table[idx:]

# Write table to file
with open(html_table, "w") as table_file:
    table_file.write(final_table)

# Merge table and scripts into HTML page
with open(html_index, "wb") as output_file:
    for in_file in [html_header, html_table, html_scripts, html_footer]:
        with open(in_file, "rb") as in_file:
            shutil.copyfileobj(in_file, output_file)
