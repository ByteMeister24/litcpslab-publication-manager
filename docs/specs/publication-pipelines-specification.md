# Publication pipeline specification

## Scope

The pipeline retrieves publication metadata from IEEE Xplore, preserves native
JSON responses, and generates Markdown using the
[publication schema](../../schema/publication-schema.md). IEEE is the only
implemented source. Additional publishers, PDF downloading, and reconversion of
historical raw downloads are outside the current pipeline.

For commands and setup, see the [download guide](../citation-download.md).

## Components and ownership

All implementation paths below are relative to `src/`.

| Component | Responsibility |
| --- | --- |
| `download_publications.py` | Parse CLI arguments into `DownloadRequest`, call the manager, print reports, update HTML counts, and return an exit code |
| `download_manager.py` | Resolve sources, request selected authors, process author/source pairs sequentially, and collect download and Markdown outcomes |
| `author_builder.py` | Define `Author`, validate the complete author database, and return selected `Author` instances |
| `utils/yaml_loader.py` | Parse the complete YAML mapping safely and reject duplicate keys |
| `ieee_xplore.py` | Load IEEE credentials, build queries, retrieve and validate pages, save raw data, normalize publications, and construct download outcomes |
| `markdown_builder.py` | Render publications, save Markdown, and return build feedback |
| `report_generator.py` | Update publication counts in the static current/past member HTML tables and return decrease warnings |
| `utils/storage.py` | Apply filename rules and publish completed files safely |
| `models.py` | Define the shared request, publication, download-outcome, and Markdown-result dataclasses |
| `config.py` | Define project paths, timezone, filename formats, and publication field order |

The manager owns the module-level `SUPPORTED_SOURCES` tuple and `DOWNLOADERS`
dictionary. Source-specific API URLs, page sizes, timeouts, and credential-key
names belong to their source modules.

The CLI handles reporting. The manager, sources, and helpers do not print.
Sources and the Markdown Builder invoke storage directly; the manager performs
no file writes.

## Data contracts

`Selection` is a tuple of strings or the literal string `"all"`.

| Dataclass | Fields |
| --- | --- |
| `Author` | `name: str`, `affiliations: tuple[str, ...]`; defined in `author_builder.py` |
| `DownloadRequest` | `authors: Selection`, `sources: Selection` |
| `Publication` | `title`, `authors`, `affiliations`, `keywords`, `abstract`, `publication_title`, `year`, `issn`, `isbn`, `doi`, `pdf_url`, `publisher` |
| `DownloadRecord` | `author: str`, `source: str`, `publication_count: int`, `publications: list[Publication]`, `raw_file_path: Path` |
| `DownloadError` | `author: str`, `source: str`, `error: str` |
| `MarkdownBuildResult` | `author: str`, `source: str`, optional `markdown_path: Path`, optional `error: str` |

`Publication.authors`, `affiliations`, and `keywords` are tuples of strings
defaulting to empty tuples. Its other fields are strings defaulting to empty
strings. A `DownloadRecord` with count zero and an empty publication list is a
success. `DownloadError` is a returned dataclass, not an exception.

The public coordination interface is:

```python
def run_download(request: DownloadRequest) -> tuple[
    list[DownloadRecord | DownloadError],
    list[MarkdownBuildResult],
]:
    ...
```

The first list contains the source-returned outcome for every author/source
pair. The second contains one result for every attempted Markdown build,
including failed builds. Errors and zero-publication records skip building and
produce no Markdown result. Both lists preserve processing order; associate
records by `(author, source)` rather than list position.

## Author database and selection

`config.AUTHORS_FILE` points to `db/authors.yaml`. Each full author name maps
directly to its complete list of affiliations:

```yaml
Ada Researcher:
  - University A
  - Institute B
```

`convert_yaml_to_dict(filepath)` uses a PyYAML `SafeLoader` subclass, reads
UTF-8 with optional BOM, and returns a nonempty mapping. It rejects non-string
keys, duplicate keys, and invalid YAML.

`get_selected_authors(selection) -> list[Author]` loads and validates the whole
mapping before selection. Names must contain nonblank text without control
characters. Each affiliation value must be a nonempty list of nonblank strings
without control characters. Affiliations are converted to tuples in their
original order, retaining duplicates. No affiliation merging occurs.

For `"all"`, authors follow database order. Named selections use `casefold()`
for matching and deduplication, preserve first-selected order, and return the
original YAML spelling and affiliations. Unknown names fail validation. Named
selection also rejects a database containing multiple names that normalize to
the same lookup key.

`Author.slug` lowercases the name and replaces spaces with hyphens.

## CLI contract

The entry point is `src/download_publications.py`.

- Bare `all` selects every author and available source and is exclusive with
  `--author` and `--source`.
- Each flag accepts comma-separated selections or `all`; an omitted flag means
  all for that dimension.
- No arguments, valueless flags, and positional author/source names are usage
  errors.
- Selections are trimmed and deduplicated. Source keywords are lowercased.
- Empty items and `all` mixed with named selections are usage errors.
- Unknown authors and sources fail validation before requests.

The CLI always passes a `DownloadRequest`. Bare `all` becomes
`DownloadRequest(authors="all", sources="all")`; the manager does not accept a
standalone `"all"` string.

## Download coordination

The manager validates author and source selections and resolves registered
downloaders before making requests. It then calls each source once per selected
author, in author order followed by source order.

Each source implements:

```python
def download(author: Author) -> DownloadRecord | DownloadError:
    ...
```

Sources catch exceptions within `download()` and return sanitized error records.
The manager appends each outcome unchanged. It skips Markdown for
`DownloadError` and for count-zero records; otherwise it passes the author,
source, and normalized publications to `build_markdown()`.

The builder returns `MarkdownBuildResult` with a saved path or an error
identifying Markdown generation or saving. A build failure does not change the
download outcome. The manager continues processing other pairs after returned
source or builder failures.

## IEEE retrieval and normalization

The IEEE module uses Python's standard-library HTTP client with these settings:

| Setting | Value |
| --- | --- |
| Endpoint | `https://ieeexploreapi.ieee.org/api/v1/search/articles` |
| Format | JSON |
| Page size | 200 |
| Start record | 1 initially; then retrieved count + 1 |
| Sort | `article_number`, ascending |
| Timeout | 30 seconds per request |
| Automatic retries | None |

Credentials are loaded inside `download()` using
`dotenv_values(config.ENV_FILE, interpolate=False)`. Only the project-root
`.env` file supplies `IEEE_API_KEY`; process environment variables are not a
fallback. The trimmed key is validated before query execution. Imports do not
load credentials.

Queries use the canonical author name and all configured affiliations, with no
year restriction:

```text
"Authors":"Ada Researcher" AND ("Author Affiliations":"University A" OR "Author Affiliations":"Institute B")
```

Search values must be nonblank literal text without double quotes, backslashes,
wildcards, or control characters. Publications with missing or unmatched
affiliations can be missed.

Every response must be a JSON object with a valid `total_records` or
`totalfound` count and a valid articles list. Zero-count responses may omit the
articles field. Retrieval rejects API error responses, changing totals,
incomplete or oversized pages, excess records, and missing or repeated article
numbers. Short pages advance by their actual length.

After every page is retrieved and validated, the source saves the complete native
pages before normalizing any publication. All native fields remain in the raw
JSON. Normalization converts each article to `Publication` in response order:

- Preserve all returned authors and affiliations. Sort authors by
  `author_order` when every author has that value; otherwise keep returned order.
- Accept nested authors under `authors.authors` or `authors.author`.
- Combine `index_terms.author_terms` before `index_terms.ieee_terms`.
- Treat absent metadata as empty fields and reject malformed values.
- Use returned publication affiliations, without substituting search affiliations.

Errors identify the failed download, raw-saving, or normalization stage.
Credential values are redacted before errors leave the source. If normalization
fails after saving, the error message includes the retained raw-file path.

## Storage and rendering

Paths are rooted at `config.PROJECT_ROOT`, independently of the working
directory. API outputs use these patterns:

```text
data/<author-slug>/raw/<author-slug>-<source><sequence>-<timestamp>.json
data/<author-slug>/<author-slug>-<source>-<YYYY-MM-DD>.md
```

Dates use `Europe/Vienna`. Raw timestamps include date, time, microseconds, and
UTC offset. The sequence is empty for the first filename and becomes `-2`,
`-3`, and so on when a timestamp collides. Raw files are never overwritten.

Markdown exports replace only an existing file for the same author, source,
and date. Earlier dates and undated exports are retained. Storage writes to a
temporary file in the destination directory, then publishes the completed raw
file with a hard link or replaces Markdown atomically with `os.replace()`.
Temporary files are removed after success or failure.

Rendering follows `config.PUBLICATION_FIELDS` and the documented
[publication schema](../../schema/publication-schema.md), in this order:

`Authors`, `Author Affiliations`, `Keywords`, `Abstract`, `Publication`,
`Year`, `ISSN`, `ISBN`, `DOI`, `Link`, `Publisher`.

Each publication has one H2 title on a single line, with blank lines separating
the heading and field labels. Tuple values are joined with `; `; absent values retain empty
labels. Publication order is preserved and output uses UTF-8. `Publication`
denotes the containing publication; `Link` uses `pdf_url`. The schema document
is a reference contract; rendering does not parse it at runtime.

A failed or partial retrieval publishes no new raw dataset and leaves existing
exports intact. Raw saving must succeed before building Markdown. Normalization
or Markdown failures retain completed raw files and preserve existing exports.
Successful zero-result searches save raw metadata and skip Markdown.

## Reporting and extensions

The CLI reports downloads and Markdown builds separately, with publication
counts and saved paths on success or stage-specific errors on failure. The
Markdown summary includes skipped builds. Exit codes are `0` for successful
downloads and attempted builds, `1` for validation or pipeline failures, and
`2` for CLI usage errors.

After printing the Markdown summary, the CLI collects successful
`DownloadRecord.publication_count` values into an author → source → integer
mapping, including count-zero records. It calls
`update_download_counts(counts_by_author: dict[str, dict[str, int]]) -> list[str]`,
prints returned warnings, and calls `update_report() -> None`. The updater
receives no publication list, raw-file path, or Markdown result. Existing console
reports and exit codes are preserved; warnings and update errors go to stderr.

`config.REPORT_JSON_FILE` points to `output/report.json`, the count store. Its
top-level `updated_at` is an ISO datetime with a Europe/Vienna offset; remaining
keys are canonical author names mapped to source keywords and nonnegative
integer publication counts. Initially all 47 members have `ieee: 0`. Equal counts
remain; increases replace the value. Decreases retain the previous count and
return a console warning without persisting warning metadata. Failed or
unprocessed author/source pairs retain their counts. Every completed pipeline
execution refreshes the timestamp once, even if there are no successful records.
Unknown authors are errors; new sources may be added for existing authors.

`config.REPORT_HTML_FILE` points to `output/report.html`. Its fixed Current
Members and Past Members tables are seeded from the supplied Markdown member
list. Each row's `data-author` identifies its database name; `data-source`
identifies source headers and cells. Source columns are added to both tables as
needed. JSON authors must match the HTML member tables.

`update_report()` reads JSON, parses the well-formed HTML with standard-library
`ElementTree`, and writes saved counts into the corresponding cells. HTML values
do not influence saved counts. It removes legacy cell warnings, preserves member
groups and row order, and displays the JSON timestamp using
`REPORT_DATETIME_FORMAT` and `DOWNLOAD_TIMEZONE`.

Both files save through the existing atomic-write helper. Missing or malformed
files and failed saves leave the affected file intact. JSON failure skips HTML
synchronization; HTML failure retains the newly saved JSON.

A small Update button opens a JSON file chooser. The adjacent `report.js` reads
the selected file, validates it before changing the displayed counts, and
refreshes both tables and their timestamp. It changes the open page only, works
without a web server, and displays errors without changing existing counts.

A new publisher supplies the same `download(author)` interface, owns its API
settings and credentials, and is registered in `download_manager.SUPPORTED_SOURCES`
and `DOWNLOADERS`. The existing CSV converter remains a separate utility with
caller-supplied input and output paths; it is not part of the API pipeline.
