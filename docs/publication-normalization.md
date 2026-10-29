# Normalize publication lists

Normalization is a separate, offline workflow. It reads saved files, maps them
to the existing `Publication` dataclass, and saves combined JSON for each author.
It does not download metadata, read API keys, or generate Markdown.

## Setup and commands

From the checkout root, refresh the editable installation to register the command:

```bash
.venv/bin/python -m pip install -e .
source .venv/bin/activate
```

Then run from any directory:

```bash
publication_normalizer --author "Mainak Majumder"
publication_normalizer --author "Name One, Name Two"
publication_normalizer --author all
publication_normalizer all
```

Replace example names with names from `db/authors.yaml`. Matching is
case-insensitive and retains the database spelling. Comma-list duplicates are
processed once, in selected order. `all` uses database order. Bare `all` cannot
be combined with `--author`; no arguments or empty selections are usage errors.
All available sources are processed; there is no source-selection flag.

You can also use `python -m publication_normalizer` with the same arguments in
the installed environment. No top-level wrapper or `PYTHONPATH` setting is needed.

## Prepare the raw folders

Each database author's existing directory has this layout:

```text
data/mainak-majumder/
  download/
    ieee/
      mainak-majumder-ieee-2026-10-27T19-16-21.983759+0100.json
    sciencedirect/
      mainak-majumder-sciencedirect-2026-10-27T19-17-00.000000+0100.json
    springer/
      SearchResults.csv
    acm/
      export.bib
  normalized/
    mainak-majumder-publications.json
```

Source folders are optional. Older files directly under `download/` are ignored;
normalization never moves or edits them. Download paths are unchanged.

Each source contributes one file: the matching JSON, CSV, or BibTeX file with
the newest filesystem creation timestamp. All formats use this same rule.
Filenames are unrestricted, and timestamps in their names are visual references.
Modification and metadata-change times are ignored. A malformed selected file
does not cause fallback to an older one. Extensions are matched case-insensitively.

The shared timestamp utility uses native creation-time metadata where available
and GNU `stat` on Linux. If creation time cannot be read, the source is reported
as an error and processing continues with the other sources.

The Springer CSV must contain these headers:

```text
Item Title,Publication Title,Item DOI,Authors,Publication Year,URL
```

The usual additional Springer columns may remain. Required cells can be empty.
Correct the `Authors` cells manually to comma-separated full names. In CSV text,
quote a cell containing commas, for example:

```csv
"Mainak Majumder, Alois Zoitl"
```

A spreadsheet CSV export normally handles that quoting for you. The normalizer
splits on commas and trims names; it does not infer boundaries in concatenated
names such as `Mainak MajumderAlois Zoitl`.

Springer maps title, containing publication, DOI, authors, year, and URL. The
supplied URL is stored in `pdf_url` as agreed, including page links. Other fields
stay empty, even if an additional column has a similarly named value. Collections
and other content types are retained. Input is UTF-8, with an optional BOM.

## Output and partial results

Each output is a plain JSON array with exactly the `Publication` fields. Authors,
affiliations, and keywords are JSON arrays; other fields are strings. Missing
values remain empty. The filename and its containing author directory use the
author slug: the database name lowercased with spaces replaced by hyphens.
The directory and filename templates in `src/config.py` both accept `{author_slug}`.

Records are combined in IEEE, ScienceDirect, Springer, ACM order, preserving
page/file record order. Repeated publications are retained. The workflow assigns
all records in an author's raw folders to that author's output; it does not
match or filter publication author names.

Authors with at least one converted publication have their output rebuilt and
atomically replaced instead of appended. Authors with zero publications are
skipped: no new normalized file or directory is created, and existing normalized
files are left unchanged.

| Situation | Result |
| --- | --- |
| No supported raw files | Author skipped; existing normalized JSON retained |
| Valid inputs produce zero publications | Author skipped; existing normalized JSON retained |
| Some inputs fail and others produce publications | Failed files discarded; successful records saved as partial results |
| Inputs produce zero publications and some fail | Failure reported; existing normalized JSON retained; no empty file saved |
| Every input fails | Existing normalized JSON retained |
| Saving fails | Existing normalized JSON retained; other authors continue |

The console reports counts, paths, skips, partial results, and the failing input
paths. Exit `0` means processing succeeded or skipped; exit `1` means validation,
parsing, source-selection, or saving failed somewhere; exit `2` means invalid CLI
syntax. Zero-publication skips return exit `0` when there are no input errors.
A partial result is saved but returns exit `1`. Raw files remain intact.

For the separate review and Markdown step, manually prepare an `updated/` JSON
copy as described in the [Markdown guide](publication-markdown.md). Markdown
generation reads reviewed copies, not these generated normalized files.

## Verification

```bash
.venv/bin/python -B -m unittest discover -s tests -v
```

Tests cover publisher mappings, creation-time selection for all four formats,
preserved duplicates, partial results, atomic replacement, and
credential-free/network-free execution from another directory. For contracts and
component ownership, see the [workflow specification](specs/publication-pipelines-specification.md).
