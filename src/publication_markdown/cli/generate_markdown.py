# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Select authors and print final Markdown outcomes."""

import argparse
import sys

from publication_markdown.markdown_manager import run_markdown
from helpers.selection import Selection, parse_selection


def parse_request(argv: list[str] | None = None) -> Selection:
    parser = argparse.ArgumentParser(description="Generate final Markdown from reviewed publication JSON.")
    parser.add_argument("selection", nargs="?", choices=("all",), help="All database authors; exclusive with --author.")
    parser.add_argument("--author", help="Comma-separated full author names, or all.")
    args = parser.parse_args(argv)
    if args.selection is not None:
        if args.author is not None:
            parser.error("all cannot be combined with --author.")
        return "all"
    if args.author is None:
        parser.error("Provide all or --author.")
    try:
        return parse_selection(args.author)
    except ValueError as error:
        parser.error(str(error))


def main(argv: list[str] | None = None) -> int:
    selection = parse_request(argv)
    try:
        results = run_markdown(selection)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    for result in results:
        if result.status == "generated":
            print(f"Markdown generated: {result.author}: {result.publication_count} publication(s); "
                  f"saved: {result.markdown_path}")
        elif result.status == "removed":
            print(f"Markdown removed: {result.author}: empty review; final file absent: {result.markdown_path}")
        elif result.status == "skipped":
            print(f"Markdown skipped: {result.author}: no reviewed JSON files.")
        else:
            print(f"Markdown failed: {result.author}: {result.error}; previous final file retained.", file=sys.stderr)
    return 1 if any(result.status == "failed" for result in results) else 0
