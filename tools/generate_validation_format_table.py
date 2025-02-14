#!/usr/bin/env python3

import json

# Read JSON data from input file
input_file = "../app/data/field-format.json"
output_file = "../design/A03-data-object-field-formats.md"

with open(input_file, 'r') as file:
    json_data = file.read()

# Parse JSON
data = json.loads(json_data)

# Extract validation formats
validation_formats = data['validation_formats']

# Generate Markdown table
markdown_table = "| **Format Type** | **Description** | **Regex Pattern** | **Min Length** | **Max Length** |\n"
markdown_table += "|------------------|-----------------|-------------------|----------------|----------------|\n"

for fmt in validation_formats:
    format_type = fmt['format_type']
    description = fmt['description']
    regex_pattern = fmt['regex_pattern'].replace('\\', '\\\\')  # Escape backslashes for Markdown
    min_length = str(fmt['min_length'])
    max_length = str(fmt['max_length']) if fmt['max_length'] is not None else "N/A"

    markdown_table += f"| {format_type} | {description} | `{regex_pattern}` | {min_length} | {max_length} |\n"

# Save the Markdown table to output file

with open(output_file, 'w') as file:
    file.write(markdown_table)

print(f"Markdown table has been saved to {output_file}")
