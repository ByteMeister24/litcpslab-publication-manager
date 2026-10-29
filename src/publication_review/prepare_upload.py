"""Prepare one upload folder with canonical author names and validated JSON."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

import config
from helpers.author_builder import get_selected_authors
from helpers.selection import Selection, parse_selection
from publication_markdown.json_reader import read_publications


def prepare_upload(output: Path, selection: Selection = "all") -> tuple[int, list[str]]:
    if output.exists():
        raise ValueError(f"Output directory already exists: {output}. Choose a new directory.")
    
    authors = get_selected_authors(selection)
    manifest = {"version": 1, "authors": []}
    contents = {}
    skipped = []
    
    for author in authors:
        slug = author.slug
        if slug in (".", "..") or any(character in slug for character in ("/", "\\")):
            raise ValueError(f"Author slug cannot be used as a folder name: {slug!r}.")
        
        normalized_filename = config.NORMALIZED_FILENAME_FORMAT.format(author=author.name, author_slug=slug)
        normalized_directory = config.DATA_DIRECTORY / "normalized"
        source = normalized_directory / normalized_filename
        
        if not source.exists():
            skipped.append(author.name)
            continue
        
        if not source.is_file():
            raise ValueError(f"Normalized input must be a file: {source}.")
        
        if slug in contents:
            raise ValueError(f"Duplicate author slug: {slug!r}.")
        
        publications = read_publications(source)
        upload_name = f"{slug}-publications.json"
        contents[slug] = (upload_name, json.dumps([asdict(item) for item in publications], ensure_ascii=False, indent=2) + "\n")
        manifest["authors"].append({"id": slug, "name": author.name, "sourceFile": upload_name})
    
    if not contents:
        raise ValueError("No normalized publication files found for the selected authors.")

    # Validate every source before creating the upload folder; existing inputs are read-only.
    output.mkdir(parents=True, exist_ok=False)
    for upload_name, content in contents.values():
        (output / upload_name).write_text(content, encoding="utf-8")
    (output / "authors.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(contents), skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare normalized JSON files for the Google review app.")
    parser.add_argument("--output", required=True, type=Path, help="A new folder to create for uploading to Google Drive.")
    parser.add_argument("--author", default="all", help="Comma-separated database author names, or all (default).")
    args = parser.parse_args(argv)
    try:
        selection = parse_selection(args.author)
    except ValueError as error:
        parser.error(str(error))
    try:
        count, skipped = prepare_upload(args.output, selection)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Review preparation failed: {error}", file=sys.stderr)
        return 1
    print(f"Prepared {count} author(s) in {args.output.resolve()}")
    for name in skipped:
        print(f"Skipped {name}: no normalized JSON file.")
    print("Upload every file in this folder, including authors.json, into the app's input folder on Google Drive.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
