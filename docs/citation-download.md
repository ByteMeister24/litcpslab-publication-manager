# Publication download and Markdown generation

The pipeline implements the
[publication-pipelines specification](specs/publication-pipelines-specification.md).
IEEE is the only implemented source. It retrieves publication metadata and links,
saves native JSON, and generates the existing publication Markdown schema.

## Setup

Use the project's virtual environment and install its requirements:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

The pipeline uses `python-dotenv` for direct file credentials and `markdown-it-py`
for Markdown syntax. The system timezone database must include `Europe/Vienna`.

Maintain researcher definitions in `data/authors.md`, keeping all three sections:

```markdown
## Authors

- Researcher One Full Name
- Researcher Two Full Name

## Common Affiliations

- University A
- Institute B

## Additional Affiliations

### Researcher Two Full Name

- Former University C
```

Author names must be unique and author-specific headings must match the master
list. Every author needs at least one common or additional affiliation. Name
directories must be distinct; directory separators in names are rejected.
The file uses H2 sections and H3 author headings, with no H1 title. The reusable
Markdown Reader builds a tree of sections and subsections. The Author Builder
reads that tree, validates the author sections and flat bullet lists, and returns
selected `Author` instances with effective affiliations. Inline formatting is
read as displayed text. Nested
lists, prose outside list items, code blocks, embedded HTML, and images are
rejected rather than silently interpreted as researcher definitions.

The IEEE module reads `IEEE_API_KEY` directly from the project `.env` file when
called. Exported environment values are ignored. Variable interpolation is
disabled, so `${OTHER_VARIABLE}` is treated literally. Missing or blank keys
produce a reported failure before requests. Imports and `--help` do not read
credentials. The pipeline does not modify `.env`.

## Commands

From the project root:

```bash
.venv/bin/python src/main.py all
.venv/bin/python src/main.py --author "Researcher One Full Name"
.venv/bin/python src/main.py --source ieee
.venv/bin/python src/main.py --author "Researcher One Full Name, Researcher Two Full Name" --source ieee
.venv/bin/python src/main.py --author all --source ieee
.venv/bin/python src/main.py --author "Researcher One Full Name" --source all
```

Both flags accept comma-separated values or `all`. Quote author lists containing
spaces. An omitted flag selects all for that dimension. Bare `all` selects every
author and available source; combining bare `all` with either flag is invalid.
Running without arguments is also invalid. The previous positional-author syntax
has been replaced.

Whitespace is trimmed and repeated selections are processed once in first-seen
order. Author names match exactly; source keywords are lowercased. Empty list
items, `all` mixed with names, unknown authors, and unknown sources are rejected.
All selections are validated before any API calls. Source selection examples
with additional publishers remain invalid until those integrations are added.

The debug launch profile prompts separately for author and source lists, using
`all` as each default. Credentials are read by the source module itself.

## Responsibilities

- `main.py`: normalizes every valid CLI selection, including bare `all`, into a
  `DownloadRequest`, calls the manager, prints results, and handles exit codes.
- `download_manager.py`: resolves sources, asks the Author Builder for selected authors,
  calls each source once per author, delegates exports to the builder, and
  collects one `DownloadResult` per pair. It performs no file writes.
- `markdown_reader.py`: exposes `read_markdown(path) -> MarkdownDocument`. The
  document has `sections` and content before the first heading. Sections expose
  `title`, `level`, `content`, and nested `subsections`; content blocks use
  `markdown-it-py` syntax nodes. Heading levels determine the hierarchy, and
  duplicate headings remain distinct. This reader is independent of author rules.
- `author_builder.py`: uses the reader's H2/H3 tree, validates definitions and
  selections, builds the author/affiliation dictionary, and returns `list[Author]`
  with common plus author-specific affiliations. `load_authors` accepts selected
  names or `"all"`.
- `ieee_xplore.py`: implements `download(author: Author) -> SourceDownload`,
  including credentials, queries, paging, validation, native raw saving, and
  normalization, in that order.
- `markdown_builder.py`: renders the publication schema, saves the export, and
  returns `MarkdownBuildResult` with a Markdown path or a stage-specific error.
- `storage.py`: shared filename rules and safe writes, called by source modules
  and the Markdown Builder.
- `models.py`: shared request, author, publication, source-result, builder-result,
  and report types.
- `config.py`: project-wide paths and settings, including publication field order.
  Source API settings stay in their source modules. The schema document remains
  the output contract; it is not parsed as a runtime template.

Each `SourceDownload` contains common `Publication` records and the saved
`raw_file_path`. Complete native pages are saved before normalization. If
normalization fails, `DownloadError` carries that path so the report can identify
the retained download. Source modules sanitize errors before the manager sees
them. The manager and helpers do not print reports.

A future source implements the same per-author function and is added to the
supported-source configuration and manager's explicit dispatch. ScienceDirect
and Springer Nature remain extension points; neither integration is implemented.

## Outputs and failures

```text
data/researcher-one-full-name/
  raw/
    researcher-one-full-name-ieee-2026-10-21T14-30-00.000000+0200.json
  researcher-one-full-name-ieee.md
```

Raw JSON contains an array of complete native page objects, including for one
page. Each successful download creates a new file. Names include completion date,
time, microseconds, and UTC offset in `Europe/Vienna`; collisions insert a sequence
number before the timestamp. Legacy and dated raw files are retained.

The current Markdown file contains all returned publications in the existing
schema and replaces its previous version only after a complete new document is
ready. Authors and affiliations come from publication metadata; configured search
affiliations are never substituted. Author keywords precede IEEE terms. Missing
fields keep empty labels. A successful zero-result search saves raw metadata and
an empty Markdown file.

A failed or incomplete retrieval does not change existing outputs. Raw saving
must succeed before Markdown is updated. If rendering or Markdown saving fails,
the new raw file remains, previous Markdown is preserved, and the report identifies
the failed stage and raw path. Complete raw responses are also retained if
normalization fails after raw saving; the error carries the retained raw path.
Other author/source pairs continue.

Temporary writes prevent partially written final files. Publishing raw history
requires hard-link support in the output filesystem; Markdown uses atomic
replacement. Requests have a source-defined timeout (currently 30 seconds for
IEEE) and are not automatically retried.

The CLI prints one result per pair, with publication count and saved paths on
success, then a summary. Exit status is 0 for complete success, 1 for pipeline
failures, and 2 for invalid CLI syntax. PDFs are not downloaded. The legacy CSV
converter remains a separate utility with its existing behavior.

## Verification

```bash
.venv/bin/python -B -m unittest discover -s tests -v
```

Tests use synthetic author documents, credentials, and IEEE-shaped responses in
temporary directories. HTTP calls are mocked; production data and credentials
are not used. Normalization covers nested authors, affiliations, author keywords,
IEEE terms, and the remaining fields in the
[publication schema](../data/publication-schema.md).

IEEE's [returned-field reference](https://developer.ieee.org/docs/read/Metadata_API_responses)
documents populated fields. The normalizer accepts `authors.authors` (and the
`authors.author` variant), and the `index_terms` keyword groups. Counts accept
`total_records` or the documented `totalfound`. Exact live payload compatibility
still needs a smoke test with a configured researcher; no live IEEE requests are
part of the automated suite.
