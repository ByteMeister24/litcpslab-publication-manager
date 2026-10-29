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
also supported. Author matching ignores case, while filenames use the author
slug: the database name lowercased with spaces replaced by hyphens.
There is no directory or source argument. No API keys or
network access are needed.

## Prepare a review

Normalization produces a file such as:

```text
data/normalized/mainak-majumder-publications-normalized.json
```

Place one reviewed JSON file per author directly in `data/reviewed/`. Keep the
Google app's exported filename, for example:

```text
data/reviewed/mainak-majumder-reviewed-2026-10-29T14-30-00.json
```

The filename identifies the owner through `<author-slug>-reviewed-`, followed
by the export's timestamp and optional collision suffix. Publication coauthors
inside the JSON do not determine ownership. The app exports the latest saved
review for each author, so the workflow expects one matching file per author.
Multiple matching files fail that author without changing their final output;
keep only the review you intend to use in this folder.

You can also copy a normalized dataset here, name it using this pattern, and
review it manually. Correct metadata, add or remove publications, or reorder
them in the reviewed copy. The workflow neither creates these copies nor changes
any input files. Only JSON files directly in `data/reviewed/` are considered;
extension matching ignores case. Unmatched filenames and subdirectories are
ignored. No filesystem timestamp lookup is required.

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
data/final/mainak-majumder-final-2026-10-29.md
```

The filename contains the current date in `Europe/Vienna`, using the default
format `%Y-%m-%d`. `FINAL_MARKDOWN_FILENAME_FORMAT`,
`FINAL_MARKDOWN_DATE_FORMAT`, and `DOWNLOAD_TIMEZONE` in `src/config.py` control
the filename and date. All authors' outputs are saved directly in `data/final/`.

Each publication uses the existing heading, labels, spacing, and field order.
Reviewed publication order and duplicates are retained. Successful generation
atomically replaces the same day's final file. A run on a later date creates a
new file and retains earlier dated outputs.

**A matching reviewed file containing `[]` removes only that author's current-day
final Markdown file.** If the file is already absent, the run succeeds without creating
any directories. Earlier dated outputs and other files and directories are preserved.

Missing reviews skip the author and preserve previous output. Duplicate, invalid,
or unreadable reviews, rendering errors, or storage failures report an error and
preserve previous output. Processing continues with other selected authors.
Normalized files are never used as a fallback.

The console prints generated publication counts and paths, removals, skips, and
failures. Exit codes are `0` for successful processing/skips, `1` for processing
or database validation failures, and `2` for invalid command arguments.
