# Final Markdown from reviewed publications

This workflow converts your manually reviewed publication JSON into the existing
Markdown format. It runs independently of downloading and normalization.

For colleagues to review lists through one shared browser link, use the
[Google Apps Script review app](publication-review-google-apps-script.md).
Its batch export supplies the reviewed JSON files used by this workflow.

## Install and run

From the project directory, activate the project environment and refresh its
editable installation:

```bash
source .venv/bin/activate
python -m pip install -e .
```

The command then works from any directory in that environment:

```bash
publication_markdown --author "Mainak Majumder"
publication_markdown --author "Name One, Name Two"
publication_markdown all
```

`python -m publication_markdown` accepts the same arguments. `--author all` is
also supported. Author matching ignores case, while filenames use the canonical
database spelling. There is no directory or source argument. No API keys or
network access are needed.

## Prepare a review

Normalization produces a file such as:

```text
data/mainak-majumder/normalized/Mainak Majumder-publications.json
```

Manually copy the dataset you want to review into the author's `updated/` folder.
You can choose any JSON filename, for example:

```text
data/mainak-majumder/updated/reviewed-publications.json
```

Edit this reviewed copy yourself. You can correct metadata, add publications,
remove publications, or reorder them. The workflow neither creates reviewed
copies nor changes any input files. It selects the JSON file with the newest
filesystem creation time using `utils.file_timestamps.get_creation_timestamp`.
Filenames and modification times do not determine which review is latest. Only
JSON files directly in this folder are considered; extension matching ignores
case. Equal creation times use the first filename in alphabetical order. If a
creation time cannot be read, or the selected review is malformed, the author
fails without choosing an older review.

The configurable input template is `UPDATED_JSON_DIRECTORY_FORMAT` in
`src/config.py`, defaulting to `{author_slug}/updated/`. `{author_slug}` means
the author slug, such as `mainak-majumder`. Relative paths start at the configured
data directory; absolute templates work too.

## Reviewed JSON format

The file contains a JSON array. Missing fields use empty defaults:

```json
[
  {
    "title": "A reviewed publication",
    "authors": ["Mainak Majumder", "Another Author"],
    "affiliations": [],
    "keywords": ["systems"],
    "year": "2026",
    "doi": "10.example/publication"
  }
]
```

The allowed fields are `title`, `authors`, `affiliations`, `keywords`, `abstract`,
`publication_title`, `year`, `issn`, `isbn`, `doi`, `pdf_url`, and `publisher`.
`authors`, `affiliations`, and `keywords` must be arrays of strings. All other
values must be strings, including `year`. Unknown fields, `null`, numbers, and
incorrect record structures are rejected before output changes. Keep JSON
syntax valid and use UTF-8.

## Output and outcomes

For the example author, the combined output is:

```text
data/mainak-majumder/final/Mainak Majumder-final.md
```

Each publication uses the existing heading, labels, spacing, and field order.
Reviewed publication order and duplicates are retained. Successful generation
atomically replaces the same final file, so review additions and removals are
reflected on the next run.

**A latest reviewed file containing `[]` removes that exact final Markdown
file.** If the file is already absent, the run succeeds without creating any
directories. Other files and directories are preserved.

Missing reviews skip the author and preserve previous output. Invalid or
unreadable reviews, rendering errors, or storage failures report an error and
preserve previous output. Processing continues with other selected authors.
Normalized files are never used as a fallback.

The console prints generated publication counts and paths, removals, skips, and
failures. Exit codes are `0` for successful processing/skips, `1` for processing
or database validation failures, and `2` for invalid command arguments.
