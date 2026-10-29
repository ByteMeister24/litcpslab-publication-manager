# Publication workflow specification

## Scope

The project has three separate workflows:

1. **Source collection:** retrieve publication lists from publisher APIs, store
   complete native JSON, and print download confirmations or errors.
2. **Normalization:** read saved IEEE/ScienceDirect JSON, Springer CSV, and ACM
   BibTeX into the existing `Publication` dataclass and save one JSON array per author.
3. **Markdown creation:** accept one or more database author names or `all`, read
   their latest manually reviewed JSON datasets, and generate the predefined
   Markdown format. Missing reviews skip the author; an empty review removes
   that author's exact final Markdown file.

The implemented source collection workflow supports IEEE Xplore and ScienceDirect.
It does not normalize metadata or create Markdown.
Additional publishers and PDF downloading are outside its current scope.

IEEE and ScienceDirect conversion helpers belong to the normalization package;
the collector does not import them. Markdown rendering belongs to the third
workflow.

For commands and setup, see the [download guide](../citation-download.md).
For normalization commands and manual-input preparation, see the
[normalization guide](../publication-normalization.md).
For review preparation and final Markdown commands, see the
[Markdown guide](../publication-markdown.md).
For a shared browser-based review page, see the
[Google Apps Script setup guide](../publication-review-google-apps-script.md).

## Components and ownership

Implementation paths below are relative to `src/`.

| Component | Responsibility |
| --- | --- |
| `publication_collector/cli/download_publications.py` | Parse CLI arguments into `DownloadRequest`, call the manager, print outcomes and a console summary, and return an exit code |
| `publication_collector/download_manager.py` | Validate selections, resolve sources, process author/source pairs sequentially, and collect returned outcomes |
| `publication_collector/models.py` | Define `DownloadRequest`, `DownloadConfirmation`, and `DownloadError`; reuse the shared `helpers.selection.Selection` type |
| `publication_collector/source_downloaders/ieee_xplore.py` | Own IEEE settings, query construction, retrieval, page validation, and publication counting |
| `publication_collector/source_downloaders/sciencedirect.py` | Own ScienceDirect settings, query construction, retrieval, page validation, and publication counting |
| `publication_collector/source_downloaders/common.py` | Load credentials, run the supplied source functions, construct the download filepath and JSON content, save complete raw pages, and construct a confirmation or sanitized error |
| `publication_collector/__main__.py` | Run the collector as a Python module |
| `publication_normalizer/cli/normalize_publications.py` | Parse author selections and print normalization outcomes, paths, errors, and exit status |
| `publication_normalizer/normalization_manager.py` | Define per-author `NormalizationResult` outcomes, select inputs in source order, collect file-level results, and save complete or partial per-author datasets |
| `publication_normalizer/source_normalizers/` | Read IEEE/ScienceDirect native pages, map Springer CSV fields, and convert ACM BibTeX |
| `publication_normalizer/__main__.py` | Run normalization as a Python module |
| `publication_markdown/cli/generate_markdown.py` | Parse author selections and print generated, removed, skipped, and failed outcomes |
| `publication_markdown/markdown_manager.py` | Select reviewed inputs, coordinate generation, and remove the exact final file for empty reviews |
| `publication_markdown/json_reader.py` | Validate a complete reviewed JSON array and construct `Publication` instances |
| `publication_markdown/markdown_builder.py` | Render publications using the existing schema and save combined final Markdown |
| `publication_markdown/models.py` | Define `MarkdownBuildResult` and per-author `MarkdownResult` outcomes |
| `publication_markdown/__main__.py` | Run Markdown generation as a Python module |
| `publication_model.py` | Define the shared `Publication` dataclass |
| `helpers/author_builder.py` | Define `Author`, validate the complete author database, and return selected authors |
| `helpers/selection.py` | Define shared selection types and comma-list CLI parsing |
| `utils/yaml_loader.py` | Parse the complete YAML mapping safely and reject duplicate keys |
| `utils/storage.py` | Publish completed files safely and apply raw-download filename rules; remains shared under `src/` |
| `utils/file_timestamps.py` | Read filesystem creation timestamps for uniform normalization input selection |
| `config.py` | Define shared project paths, timezone, and filename formats |

The manager owns `SUPPORTED_SOURCES` and `DOWNLOADERS`. Source API URLs, page
sizes, timeouts, and credential-key names belong to their source modules.
The CLI owns console output; the manager and sources do not print. The shared
source workflow invokes storage directly; the manager performs no file writes.
The collector does not import normalization or Markdown modules.

## Data contracts

`Selection` is a tuple of strings or the literal string `"all"`.

| Dataclass | Fields |
| --- | --- |
| `Author` | `name: str`, `affiliations: tuple[str, ...]`; defined in `helpers/author_builder.py` |
| `DownloadRequest` | `authors: Selection`, `sources: Selection` |
| `DownloadConfirmation` | `author: str`, `source: str`, `publication_count: int`, `raw_file_path: Path` |
| `DownloadError` | `author: str`, `source: str`, `error: str` |

The collector's public coordination interface is:

```python
from publication_collector.models import DownloadConfirmation, DownloadError, DownloadRequest


def run_download(request: DownloadRequest) -> list[DownloadConfirmation | DownloadError]:
    ...
```

Each selected author/source pair produces one source-returned outcome, unchanged,
in author order followed by source order. A confirmation contains no normalized
publication objects. A zero-publication download is successful and saves its native
response pages. `DownloadError` is a returned dataclass, not an exception.

## Author database and selection

`config.AUTHORS_FILE` points to `db/authors.yaml`. Each full name maps directly
to its complete affiliation list:

```yaml
Ada Researcher:
  - University A
  - Institute B
```

`convert_yaml_to_dict(filepath)` uses a PyYAML `SafeLoader` subclass, accepts
UTF-8 with an optional BOM, and requires a nonempty mapping. It rejects
non-string keys, duplicate keys, and invalid YAML.

`get_selected_authors(selection)` validates the whole mapping before selection.
Names must contain nonblank text without control characters. Each affiliation
value must be a nonempty list of nonblank strings without control characters.
Affiliations become tuples in their original order, retaining duplicates.

For `"all"`, authors follow database order. Named selections use `casefold()`
for matching and deduplication, preserve first-selected order, and retain the
original YAML spelling and affiliations. Unknown names fail validation. Named
selection rejects database names that collide under case-insensitive matching.
`Author.slug` lowercases the name and replaces spaces with hyphens.

## CLI contract

The collection workflow has its own installed console entry point:
`publication_collector ...`. The project-root `pyproject.toml` registers it as
`publication_collector.cli.download_publications:main`.

Installing with `python -m pip install -e .` in the project environment makes the
checkout importable. After activating that environment, both
`publication_collector ...` and `python -m publication_collector ...` work without
setting `PYTHONPATH`. The editable installation retains shared `config.py` in the
checkout, so configured data and credential paths remain independent of the
current working directory.

- Bare `all` selects every author and supported source and is exclusive with
  `--author` and `--source`.
- Each flag accepts comma-separated selections or `all`; an omitted flag means
  all for that dimension.
- No arguments, valueless flags, and positional author/source names are usage errors.
- Selections are trimmed and deduplicated. Source keywords are lowercased.
- Empty items and `all` mixed with named selections are usage errors.
- Unknown authors and sources fail validation before requests.

The CLI always passes a `DownloadRequest`. The manager does not accept a bare
`"all"` string. Successful outcomes print the author, source, count, and raw path
to stdout. Errors print the author, source, and sanitized error to stderr.
A final console summary counts successes and failures.

Exit codes are `0` when all downloads succeed, `1` for validation or download/raw
storage failures, and `2` for CLI usage errors. A successful zero-result search
returns `0`.

## Source download coordination

The manager validates author and source selections and resolves registered
downloaders before making requests. It calls each source once per selected
author, sequentially. Every source implements:

```python
def download(author: Author) -> DownloadConfirmation | DownloadError:
    ...
```

Each source delegates to
`publication_collector.source_downloaders.common.download_source()`, passing its
source identifiers, credential-key name, query builder, page downloader, and
publication counter. The common workflow:

1. Loads and validates credentials.
2. Builds the source-specific query and retrieves every validated native page.
3. Gets the source-specific publication count.
4. Constructs the configured download filepath, serializes complete native pages
   unchanged as a JSON array, and calls `storage.save_file()` with `replace=False`.
5. Returns `DownloadConfirmation` with the saved path and count.

Exceptions become sanitized `DownloadError` outcomes identifying the Download
or Raw saving stage. Failures do not stop the remaining author/source pairs.
No normalization or Markdown function runs during collection.

## Credentials

Normal CLI use reads `IEEE_API_KEY` and `SCIENCEDIRECT_API_KEY` only from the
project-root `.env` file with `dotenv_values(..., interpolate=False)`. Imports
and CLI help do not load credentials. Keys are trimmed and validated before
requests. Missing, unassigned, or blank keys return download errors; process
environment keys are not a fallback.

Credential values are redacted before errors leave the source.

## Publisher retrieval

| Setting | IEEE Xplore | ScienceDirect |
| --- | --- | --- |
| Endpoint | `https://ieeexploreapi.ieee.org/api/v1/search/articles` | `https://api.elsevier.com/content/metadata/article` |
| Response format | JSON | JSON with `view=COMPLETE` |
| Page size | 200 | 25 |
| Initial position | Record 1 | Offset 0 |
| Next position | Retrieved count + 1 | Retrieved count |
| Credentials | `apikey` query parameter | `X-ELS-APIKey` header |
| Timeout | 30 seconds per request | 30 seconds per request |
| Automatic retries | None | None |

Both sources combine the canonical author name with any configured affiliation,
without a year filter. Search values must be nonblank literal text without
unsupported query syntax or control characters. Missing or unmatched affiliations
can exclude publications.

IEEE uses the scoped query:

```text
"Authors":"Ada Researcher" AND ("Author Affiliations":"University A" OR "Author Affiliations":"Institute B")
```

IEEE sorts by ascending article number. It validates total counts and article
lists and rejects changing totals, API errors, incomplete or oversized pages,
excess records, and missing or repeated article numbers. Zero results may omit
the articles field. Short pages advance by their actual length.

ScienceDirect builds `authfirst`/`authlastname` clauses for each possible
given/family name split and groups configured affiliations with `aff` clauses.
It validates total counts, page offsets, and entries and rejects changing totals,
API errors, incomplete or oversized pages, excess records, and missing or
repeated PII identifiers. Its empty-result sentinel is accepted while preserving
the original response page in storage.

These checks establish complete retrieval; publication metadata is not normalized
or validated against a normalized schema during collection.

## Storage

Paths are rooted at shared `config.PROJECT_ROOT`, independently of the current
working directory. Raw output uses:

```text
data/<author-slug>/download/<source>/<author-slug>-<source>-<timestamp>.json
```

`config.DOWNLOAD_DIRECTORY_FORMAT` defaults to `{author_slug}/download/{source}`,
relative to `config.DATA_DIRECTORY`. The shared download workflow and normalization
format it with the author slug and source at runtime. `config.DOWNLOAD_FILENAME_FORMAT`
controls the filename.

Dates use `Europe/Vienna`. Timestamps include date, time, microseconds, and UTC
offset. Filename collisions return a raw-saving error, preserving the existing file.

Storage writes to a temporary file in the destination directory, then atomically
publishes the completed raw file with a hard link. Temporary files are cleaned
up after success or failure. Failed or partial retrieval publishes no new raw
dataset. Existing downloads, normalized files, and Markdown are untouched.

## Adding a publisher

Add a module under `publication_collector/source_downloaders/` with its own
settings, query, retrieval/validation, and publication-count functions. Expose
`download(author)` by delegating to the common workflow, then register the source
in `publication_collector.download_manager.SUPPORTED_SOURCES` and `DOWNLOADERS`.
Normalization and Markdown generation belong to their separate workflows.

## Normalization inputs and selection

The installed command is `publication_normalizer`; its module entry point is
`python -m publication_normalizer`. Both call the normalization CLI.
Use bare `all`, `--author all`, or `--author "Name One, Name Two"`. No arguments,
positional author names, source flags, empty comma-list entries, or bare `all`
combined with `--author` are usage errors. Database author matching and validation
use `helpers.author_builder`. Shared comma-list parsing lives in `helpers.selection`;
the normalizer does not import the collector package.

Only source directories defined by `config.DOWNLOAD_DIRECTORY_FORMAT` are read.
The default layout uses source subfolders under `data/<author-slug>/download/`:

| Source folder | Matching extensions |
| --- | --- |
| `ieee` | `.json` |
| `sciencedirect` | `.json` |
| `springer` | `.csv` |
| `acm` | `.bib`, `.bibtex` |

Extension matching is case-insensitive. Other extensions and older flat files
directly under `download/` are ignored. Sources are processed in the table order;
records retain their order within pages/files. Duplicates are retained, and
publication authors are not used to filter or assign records: the containing
database author's directory determines the output owner.

Every source uses the same rule: select the matching file with the newest
filesystem creation timestamp. Each source contributes at most one input file.
Filenames are unrestricted; embedded timestamps are visual references.
Modification and metadata-change times do not determine
which version is selected. A malformed selected file is reported; older files
are not substituted.

`utils.file_timestamps.get_creation_timestamp()` reads native `st_birthtime`
metadata when available and otherwise uses GNU `stat` to read filesystem birth
time. Missing creation-time support or a failed timestamp lookup is a
source-selection error; other sources continue processing.

## Normalization field mappings

IEEE and ScienceDirect files contain a nonempty JSON array of native page objects.
Flatten each page's articles or entries and use the existing publisher mappings,
including author order, missing metadata defaults, identifiers, keywords, and
dates. Accept zero-result responses with omitted entries and ScienceDirect's
empty-result sentinel. Malformed pages or publication metadata fail that file.
The readers do not repeat API requests or load credentials.

ACM converts BibTeX in `publication_normalizer/source_normalizers/acm.py`,
including field, author, LaTeX-text, and identifier handling. Invalid BibTeX
rejects the whole file.

Springer CSV is read as UTF-8 with an optional BOM. The following columns are
required; their values may be empty:

| CSV column | `Publication` field |
| --- | --- |
| `Item Title` | `title` |
| `Publication Title` | `publication_title` |
| `Item DOI` | `doi` |
| `Authors` | `authors` |
| `Publication Year` | `year` |
| `URL` | `pdf_url` |

Authors are comma-separated and trimmed, with empty items omitted. The user
corrects undelimited author cells manually; the parser does not infer name
boundaries. By agreement, `URL` is copied into `pdf_url` even when it is a Springer
page link. Keep every nonempty row, including collections. Map only the six
columns above; all other `Publication` fields retain empty defaults. Unmapped
columns do not enrich the output. Duplicate headers, missing required columns,
extra row values, or malformed CSV are errors for that file.

## Normalized output and failures

`run_normalization(selection: Selection) -> list[NormalizationResult]` validates
the entire author selection before processing. Each result contains `author`,
`status` (`success`, `partial`, `failed`, or `skipped`), `publication_count`,
optional `normalized_path`, and a tuple of `errors`.

Output uses the canonical database name in the filename and the existing slug in
the directory:

```text
data/<author-slug>/normalized/<canonical author name>-publications.json
```

`config.NORMALIZED_DIRECTORY_FORMAT` defines the directory relative to
`config.DATA_DIRECTORY`, using the author slug. `config.NORMALIZED_FILENAME_FORMAT`
defines the filename using the canonical author name. The document is a plain
array of `Publication` objects with exactly the dataclass fields: `title`,
`authors`, `affiliations`, `keywords`, `abstract`, `publication_title`, `year`,
`issn`, `isbn`, `doi`, `pdf_url`, and `publisher`. Tuple fields serialize as JSON
arrays. Missing strings are empty strings; missing tuple fields are empty arrays.
JSON preserves Unicode, uses two-space indentation, and ends with a newline.

Every run rebuilds the file from the selected raw inputs; it does not append to
the previous normalized output. The normalization manager constructs the filepath,
serializes the publications, and calls `storage.save_file()` with `replace=True`.
The shared atomic-write helper replaces the file only after serialization and
writing succeed. Raw files and paths remain
unchanged. The workflow creates no Markdown.

- No supported inputs: skip the author without creating/replacing a file.
- At least one input parses successfully: save its results, including an empty
  array for successful zero-result inputs.
- A file fails: discard all of its records, report its path/error, and continue.
  If another file succeeds, save those results with `partial` status.
- Every input fails: retain existing JSON and return `failed` status.
- Saving fails: retain existing JSON, report the failure, and continue other authors.

The CLI prints completed/partial/skipped author outcomes and saved counts/paths
to stdout, with file and saving errors on stderr. Its final summary counts all
four statuses. Exit codes are `0` for successful/skipped processing, `1` when any
author has partial/failed results or database validation fails, and `2` for CLI
usage errors. No credentials or downloads are invoked by normalization.

## Reviewed JSON to final Markdown

The installed command is `publication_markdown`; its module entry point is
`python -m publication_markdown`. Accept bare `all`, `--author all`, or
`--author "Name One, Name Two"`. Reuse shared comma-list parsing and the existing
database author selection, including case-insensitive matching, canonical
spelling, selection order, and deduplication. There is no directory argument,
source flag, or top-level wrapper. Invalid CLI usage returns `2`; author/database
validation failures return `1` before any outputs are changed.

### Reviewed input selection

`config.UPDATED_JSON_DIRECTORY_FORMAT` defaults to `{author_slug}/updated/`.
`{author_slug}` is the existing author slug. Relative templates are rooted at
`config.DATA_DIRECTORY`, independently of the working directory. Absolute templates
are also supported. The final output location is independent of this input setting.

Review creation and editing are manual. The workflow reads only JSON files in the
configured author review directory. Filenames are unrestricted; for example:

```text
data/<author-slug>/updated/reviewed-publications.json
```

Use `utils.file_timestamps.get_creation_timestamp` to select the JSON file with
the greatest filesystem creation timestamp. Extension matching is
case-insensitive; other extensions and subdirectories are ignored. Filename
timestamps and modification times do not affect selection. For equal creation
times, select the first filename in sorted order. An unavailable or unreadable
creation timestamp fails the author without selecting another file. Only the
selected file's contents are read; malformed older contents do not affect a
valid latest review.

A missing review directory or no matching files skips the author and preserves
existing final Markdown. An unreadable directory or selected file fails the
author. Invalid latest JSON never falls back to an earlier review or to
normalized/raw data. The workflow never creates, copies, or edits review inputs.

### JSON contract and rendering

`read_publications(path)` requires a JSON array of publication objects. Only the
existing `Publication` fields are accepted. The `authors`, `affiliations`, and
`keywords` values must be arrays containing only strings; they become tuples.
Every other supplied field must be a string. Missing fields use the dataclass
defaults. Unknown keys, non-object records, incorrect types (including `null`,
numeric years, and mixed arrays), malformed JSON, or invalid encoding reject the
whole review before writing. UTF-8 with an optional BOM is supported.

Retain reviewed record order and duplicates. Manually added records appear in
the final output; removed records disappear. Do not filter by publication author
names or supplement the review from another dataset.

The existing renderer lives in `publication_markdown/markdown_builder.py`, with
the interface `build_markdown(author, publications) -> MarkdownBuildResult`.
Its result contains `author`, optional `markdown_path`, and optional `error`,
without a source field. Preserve single-line headings, Unicode, schema field
order, labels, blank lines, empty field labels, and the final newline.

### Final output and failures

The combined final path is:

```text
data/<author-slug>/final/<canonical author name>-final.md
```

`config.FINAL_MARKDOWN_FILENAME_FORMAT` defines the filename. For a nonempty
validated review, render all publications and use the shared atomic storage
helper to replace the final file only after a complete UTF-8 write. Repeated
runs replace that fixed file rather than creating dated or per-source outputs.

For a valid empty review (`[]`), remove only that exact final file. An absent
file is a successful no-op; do not create/remove directories or remove other
files. Missing or invalid reviews never trigger deletion.

`run_markdown(selection) -> list[MarkdownResult]` validates all selected authors
before processing them. Results contain `author`, `status` (`generated`,
`removed`, `skipped`, or `failed`), `publication_count`, optional `markdown_path`,
optional `reviewed_path`, and optional `error`. The `removed` status includes an
already absent final file. Reading, validation, rendering, replacement, and
removal failures preserve previous final content and do not stop other authors.

The CLI prints generated counts/paths, removal outcomes (including already
absent files), and missing-input skips to stdout. Failures and their paths/stages
are printed to stderr. Return `0` for successful processing/skips and `1` if any
author fails. Generation does not load credentials, contact APIs, normalize data,
or modify raw, normalized, or reviewed inputs. It
imports `helpers.author_builder` without depending on the collector package.

## Shared browser review app

The optional `publication_review` package provides a Google Apps Script app
between normalization and Markdown generation. It does not change the three
existing workflow entry points or make them depend on Google services.

The coordinator uploads an `authors.json` manifest and normalized JSON files to
a private input folder on Google Drive. The manifest maps canonical database
names and author slugs to input filenames. `prepare_upload.py` optionally
assembles those copies and the manifest from local configuration; users can
instead upload existing JSON files and create the manifest manually. Originals
and the author database remain unchanged.

The installed `prepare_upload --output <new-directory> --author <names-or-all>`
command calls `publication_review.prepare_upload:main`. It uses the same
arguments as `python -m publication_review.prepare_upload`; omitting `--author`
selects all authors. Output paths may be absolute or relative to the working
directory. This preparation command does not contact Google services.

Apps Script hosts `google_apps_script/Index.html` and runs `Code.gs` as the
deploying account. Script Properties identify separate input and saved-review
folders. One shared anonymous-access link displays an author selector and an
editable table. The agreed name-only access model permits anyone with the link
to select, edit, and download any listed author's publications.

Reviewers can include/exclude records, add publications, search the list,
and edit every `Publication` field. Search does not limit which included records
are saved. List fields use one item per line when edited; untouched values,
Unicode, order, and duplicates are preserved. Save is explicit, including for
unchanged lists and empty reviews. Cancelling a new publication adds no record.

The server validates complete publication arrays using the existing field
contract and fills missing defaults. A save creates a new plain-JSON revision in
the author's saved-review subfolder. Script locking and an expected-revision
token prevent stale browsers from overwriting newer saves. Source fingerprints
bind reviews to the source folder, author, and source content; changed inputs
require a new review round. Sources and prior saved revisions are not overwritten.

New saved filenames use `<author-slug>-reviewed-YYYY-MM-DDTHH-MM-SS.json` in the
Apps Script project's timezone (default `Europe/Vienna`). Saves within the same
second use collision suffixes starting at `-2`. The fingerprint is stored as
versioned JSON metadata in the Drive file's description, outside the publication
array. A temporary name keeps a new file out of selection until its description
is set and its final name published. Failed publication moves that new temporary
file to trash; any cleanup failure is reported and the temporary file remains
ignored. Existing hash/UUID filenames remain readable without modifying them.
An invalid description on the latest readable review fails loading and export
without falling back to older history. The catalog can still list other authors.

The catalog reports saved status. Batch export includes only the latest saved
review per author, selected by Drive creation time, including explicit empty
reviews. ZIP entries follow `data/<author-slug>/updated/<readable-review-name>.json`
and contain only `Publication` fields, so the existing Markdown reader can use
them after extraction. New reviews retain their saved filename; older hash-named
reviews get a readable export name derived from Drive creation time. Unsaved
authors and unsaved browser edits are excluded.
The app does not synchronize local files automatically or deploy itself.
