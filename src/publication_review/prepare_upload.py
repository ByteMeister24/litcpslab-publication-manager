# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Index existing normalized JSON files with their canonical author names."""

import argparse
import json
import sys

import config
from helpers.author_builder import get_selected_authors
from helpers.selection import Selection, parse_selection
from publication_markdown.json_reader import read_publications
from utils import storage


def prepare_upload(selection: Selection = "all") -> tuple[int, list[str]]:
    authors = get_selected_authors(selection)
    normalized_directory = config.DATA_DIRECTORY / "normalized"
    manifest = {"version": 1, "authors": []}
    seen_slugs = set()
    skipped = []

    for author in authors:
        slug = author.slug
        if slug in (".", "..") or any(character in slug for character in ("/", "\\")):
            raise ValueError(f"Author slug cannot be used as a folder name: {slug!r}.")

        normalized_filename = config.NORMALIZED_FILENAME_FORMAT.format(
            author=author.name, author_slug=slug
        )
        source = normalized_directory / normalized_filename

        if not source.exists():
            skipped.append(author.name)
            continue

        if not source.is_file():
            raise ValueError(f"Normalized input must be a file: {source}.")

        if slug in seen_slugs:
            raise ValueError(f"Duplicate author slug: {slug!r}.")

        read_publications(source)
        seen_slugs.add(slug)
        manifest["authors"].append(
            {"id": slug, "name": author.name, "sourceFile": source.name}
        )

    if not manifest["authors"]:
        raise ValueError(
            "No normalized publication files found for the selected authors."
        )

    # Publish only after every selected input validates, preserving any existing index on failure.
    content = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    storage.save_file(normalized_directory / "authors.json", content, replace=True)
    return len(manifest["authors"]), skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create authors.json beside the normalized JSON files for the Google review app."
    )
    parser.add_argument(
        "--author",
        default="all",
        help="Comma-separated database author names, or all (default).",
    )
    args = parser.parse_args(argv)
    try:
        selection = parse_selection(args.author)
    except ValueError as error:
        parser.error(str(error))
    try:
        count, skipped = prepare_upload(selection)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Review preparation failed: {error}", file=sys.stderr)
        return 1
    index_path = config.DATA_DIRECTORY / "normalized" / "authors.json"
    print(f"Prepared index for {count} author(s): {index_path.resolve()}")
    for name in skipped:
        print(f"Skipped {name}: no normalized JSON file.")
    print(
        "Upload authors.json and the publication files it references from this folder to the app's input folder on Google Drive."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
