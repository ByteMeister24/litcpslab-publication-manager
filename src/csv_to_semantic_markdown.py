#!/usr/bin/env python3
"""Convert an IEEE publication CSV into one semantic Markdown entry per row.

Requires Python 3.9+ and the standard library only.

Usage:
    python3 csv_to_semantic_markdown.py input.csv output.md
    python3 csv_to_semantic_markdown.py input.csv output.md --encoding cp1252
"""

import argparse
import csv
import sys
from pathlib import Path


# Output label and source CSV column(s), in the requested presentation order.
FIELDS = (
    ("Authors", ("Authors",)),
    ("Author Affiliations", ("Author Affiliations",)),
    ("Keywords", ("Author Keywords", "IEEE Terms")),
    ("Abstract", ("Abstract",)),
    ("Publication", ("Publication Title",)),
    ("Year", ("Publication Year",)),
    ("ISSN", ("ISSN",)),
    ("ISBN", ("ISBNs",)),
    ("DOI", ("DOI",)),
    ("Link", ("PDF Link",)),
    ("Publisher", ("Publisher",)),
)


def cell(row: dict, column: str) -> str:
    """Keep cell text, trimming surrounding whitespace; missing values are empty."""
    return (row.get(column) or "").strip()


def publication_to_markdown(row: dict) -> str:
    """Create an H2 heading and labelled fields, separated by blank lines."""
    # A Markdown heading must occupy one line, including for multiline CSV titles.
    title = " ".join(cell(row, "Document Title").splitlines())
    paragraphs = [f"## {title}"]

    for label, columns in FIELDS:
        values = [cell(row, column) for column in columns]
        # For Keywords this combines Author Keywords followed by IEEE Terms.
        # Empty values add no separators; existing keyword text is preserved.
        value = "; ".join(value for value in values if value)
        paragraphs.append(f"{label}: {value}" if value else f"{label}:")

    return "\n\n".join(paragraphs)


def convert_csv(input_csv: Path, output_md: Path, encoding: str) -> int:
    """Validate and convert the CSV, returning the number of publications."""
    if input_csv.resolve() == output_md.resolve():
        raise ValueError("Input and output must be different files.")
    if output_md.exists() and input_csv.samefile(output_md):
        raise ValueError("Input and output must be different files.")

    required = {"Document Title"}
    required.update(column for _, columns in FIELDS for column in columns)
    publications = []

    # newline="" lets csv handle quoted commas, quotes, and multiline cells.
    # utf-8-sig (the default) reads UTF-8 files both with and without a BOM.
    with input_csv.open("r", encoding=encoding, newline="") as source:
        reader = csv.DictReader(source, strict=True)
        if reader.fieldnames is None:
            raise ValueError("The CSV is empty or has no header row.")

        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("The CSV contains duplicate column headers.")

        missing = required.difference(reader.fieldnames)
        if missing:
            raise ValueError("Missing required column(s): " + ", ".join(sorted(missing)))

        for row in reader:
            if None in row:
                raise ValueError(
                    f"CSV record ending at line {reader.line_num} has more values "
                    "than the header. Check its commas and quotation marks."
                )
            if not any(cell(row, column) for column in reader.fieldnames):
                continue  # Ignore completely empty records.
            publications.append(publication_to_markdown(row))

    markdown = "\n\n".join(publications)
    if markdown:
        markdown += "\n"

    # Parse and validate all records before opening the output for writing.
    output_md.parent.mkdir(parents=True, exist_ok=True)
    with output_md.open("w", encoding="utf-8", newline="\n") as destination:
        destination.write(markdown)

    return len(publications)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert an IEEE publication CSV into semantic Markdown."
    )
    parser.add_argument("input_csv", type=Path, help="Path to the input CSV file.")
    parser.add_argument("output_md", type=Path, help="Path to the output Markdown file.")
    parser.add_argument(
        "--encoding", default="utf-8-sig",
        help="Input encoding (default: utf-8-sig). Output is always UTF-8.",
    )
    args = parser.parse_args()

    try:
        count = convert_csv(args.input_csv, args.output_md, args.encoding)
    except (OSError, UnicodeError, csv.Error, ValueError, LookupError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Converted {count} publication(s) to {args.output_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
