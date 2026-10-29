#!/usr/bin/env python3
"""Generate text queries for manual searching in ACM's Edit Query field."""

import argparse
from pathlib import Path
import sys

import config
from helpers.author_builder import Author, get_selected_authors
from helpers.selection import Selection, parse_selection
from utils.storage import save_file


SPECIAL_CHARACTERS = frozenset('+-&|!(){}[]^"~*?:/\\')


def _quote_phrase(value: str) -> str:
    escaped = "".join(
        f"\\{character}" if character in SPECIAL_CHARACTERS else character
        for character in value
    )
    return f'"{escaped}"'


def build_query(author: Author) -> str:
    affiliations = " OR ".join(_quote_phrase(value) for value in author.affiliations)
    return f"ContribAuthor:({_quote_phrase(author.name)}) AND Affiliation:({affiliations})"


def generate_queries(selection: Selection) -> Path:
    authors = get_selected_authors(selection)
    content = "\n".join(build_query(author) for author in authors) + "\n"
    output_path = config.DATA_DIRECTORY / "acm-queries" / "queries.txt"
    save_file(output_path, content, replace=True)
    return output_path


def parse_request(argv: list[str] | None = None) -> Selection:
    parser = argparse.ArgumentParser(
        description="Write manual ACM search queries to data/acm-queries/queries.txt."
    )
    parser.add_argument("selection", nargs="?", choices=("all",),
                        help="All database authors; exclusive with --author.")
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
        output_path = generate_queries(selection)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"ACM queries saved: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
