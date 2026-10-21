# Publication Pipelines Specification

## Status and purpose

This document records the requirements agreed during the publication-management
discussion and the subsequently approved architecture reorganization.
The implemented pipeline downloads native metadata and generates Markdown in
one run. This supersedes the previous independent API-download and conversion
workflow. Details that remain undecided are listed at the end.

The project automates collecting publication metadata for individual lab
researchers and converting it into semantic Markdown for a knowledge base.
Titles, authors, affiliations, keywords, abstracts, publication details, and PDF
links support downstream questions about researchers and their work.

The first version supports **IEEE Xplore**, identified by the source keyword
`ieee`. Additional sources, including ScienceDirect and Springer Nature, are
future work. The knowledge-base chatbot is a downstream consumer of the generated
Markdown; its implementation is outside this specification.

## Pipeline architecture

1. **CLI entry point (`main.py`)** parses selections, normalizes them into a
   `DownloadRequest`, calls the Download Manager, and prints returned results and
   the summary. It does not read author files or credentials, issue HTTP requests,
   render Markdown, or save publication files.
2. **Download Manager (`download_manager.py`)** exposes
   `run_download(request: DownloadRequest) -> list[DownloadResult]`. It resolves
   sources, requests selected authors from the Author Builder, and validates all
   selections before requests. For each author/source pair it calls the source
   once, delegates exports to the Markdown Builder, and collects one result.
   It continues after individual failures, performs no file writes, and does not
   print.
3. **Author Builder (`author_builder.py`)** exposes
   `load_authors(selection, path=None) -> list[Author]`, accepting a tuple of full
   names or `"all"`. It uses the Markdown Reader to get H2 sections and their H3
   subsections, validates author definitions, builds the author/affiliation
   dictionary, and constructs selected authors with common plus author-specific
   affiliations. The default path is the configured author file.
4. **Source modules** expose `download(author: Author) -> SourceDownload`. They
   access their credentials, build API queries, retrieve and validate every page,
   save complete native responses through the shared storage helper, and only
   then normalize publications. IEEE is the only implemented source.
5. **Markdown Builder (`markdown_builder.py`)** exposes
   `build_markdown(author, source, publications) -> MarkdownBuildResult`. It
   renders common publication records using the documented schema and saves
   through the shared storage helper. Its result contains the saved Markdown path
   or a stage-specific generation/saving error.

The reusable **Markdown Reader (`markdown_reader.py`)** exposes
`read_markdown(path) -> MarkdownDocument`. It uses `markdown-it-py` and its syntax
tree to group content under headings. The document has `sections` and content
before the first heading. Each section exposes `title`, `level`, `content`, and
`subsections`; content blocks are navigable `SyntaxTreeNode` objects. A section
ends at the next heading of the same or higher level. Duplicate headings remain
distinct in source order. The reader has no author-specific validation.

Shared contracts live in `models.py`. `SourceDownload` contains `publications`
and `raw_file_path`. `Publication` mirrors the Markdown schema: authors,
affiliations, and keywords are tuples of strings; remaining fields are strings.
`DownloadResult` contains author, source, publication count, `raw_file_path`,
`markdown_path`, and an optional error. The manager returns one result for every
attempted pair. Source failures use a credential-safe `DownloadError`; if
normalization fails after raw saving, the error carries `raw_file_path` so the
manager and CLI can report the retained file.

`config.py` centralizes project-wide settings: project/data/author/environment
file paths, author-section names, available-source keywords, Markdown parser
preset, timezone, filename formats, and publication field order. API URLs, page
sizes, timeouts, and credential-key names remain in each source module.

`storage.py` centralizes filename rules and safe writes. Source modules invoke it
for raw downloads; the Markdown Builder invokes it for exports. The Markdown
schema is a documented contract implemented by `config.PUBLICATION_FIELDS`,
not a runtime template loaded from the schema document.

The CSV converter remains an independent manual-export utility with its existing
behavior. CSV is not an intermediate API format. This change adds no standalone
saved-API-response conversion command. Publication PDFs are not downloaded.

## Master author file

The Author Builder uses the fixed project-relative location **`data/authors.md`**.
Author names and affiliations are maintained in this single Markdown file.
Affiliations are not supplied as command arguments.

The file uses H2 sections and H3 author headings, with no H1 title. It contains
three sections:

- `Authors`: the master list of full author names to process.
- `Common Affiliations`: affiliations used for every author in the master list.
- `Additional Affiliations`: optional author-specific additions, grouped under
  headings containing the corresponding full author names.

Example structure:

```markdown
## Authors

- Researcher One Full Name
- Researcher Two Full Name

## Common Affiliations

- Affiliation A
- Affiliation B

## Additional Affiliations

### Researcher Two Full Name

- Affiliation C
- Affiliation D
```

The `Authors` section determines the researchers to query. An author named in
`Additional Affiliations` must match a full name in that master list.

Each author has one configured full name. Name variants and aliases are outside
the agreed requirements. Full names are assumed to be unique; the user maintains
that uniqueness. Automatic duplicate-name disambiguation and `_1`/`_2` suffixes
are explicitly out of scope for this version.

## Author and affiliation search contract

The intended scope is each researcher's full publication history available from
the selected source, including work associated with previous institutions. No
year restriction or restriction to work performed at the current lab has been
requested.

For a particular author, the effective affiliation list consists of:

```text
common affiliations + that author's additional affiliations
```

Additional affiliations extend the common list; they do not replace it or apply
to other authors.

The conceptual query is:

```text
Full Author Name AND (Affiliation A OR Affiliation B OR ...)
```

For the example author file:

```text
Researcher One Full Name AND (Affiliation A OR Affiliation B)

Researcher Two Full Name AND
    (Affiliation A OR Affiliation B OR Affiliation C OR Affiliation D)
```

The implementation must translate this intent into IEEE's documented search
parameters and field-scoped query syntax. The examples above are conceptual
expressions, not executable API request strings.

Some publications may be missed because their affiliations are absent or do not
match the configured list. This is an accepted limitation; complete coverage of
every work by a researcher is not guaranteed.

## Author and source selection

The CLI accepts bare `all` or one or both selection flags:

```text
python3 src/main.py all
python3 src/main.py --author "Author X, Author Y" --source "ieee"
python3 src/main.py --author "Author X"
python3 src/main.py --source "ieee"
```

`--author` accepts comma-separated full names or `all`. `--source` accepts
comma-separated source keywords or `all`. Each dimension expands independently:
`--author all --source ieee` selects all authors from IEEE;
`--author "Author X" --source all` selects that author from every available source.
An omitted flag means all for that dimension. Bare `all` selects every author
and source and cannot be combined with either flag, even if that flag says `all`.
No arguments is a usage error. The old positional-author syntax is removed.

Selections are trimmed and deduplicated in first-occurrence order. Source
keywords are lowercased; author names match the master list exactly. Empty list
items and `all` mixed with named selections are usage errors. Unknown authors or
sources fail validation before any download. `all` expands authors in master
order and sources in configured order; explicit lists retain their order.

The CLI always passes `DownloadRequest(authors, sources)`, with each field
containing a tuple of strings or the literal `all`. The CLI normalizes bare `all`
into `DownloadRequest(authors="all", sources="all")`; the manager accepts only
that dataclass and delegates author selection to the Author Builder. The available-source set
contains only `ieee`. New integrations follow the same source interface and are
added to the available-source configuration and manager dispatch.

## Storage and filenames

Each researcher has an automatically created directory under `data/`. Its name
is derived from the full author name, lowercased with spaces replaced by hyphens.
For example:

```text
Researcher Full Name -> researcher-full-name
```

Each author's directory contains:

- A `raw/` subdirectory for persisted downloaded metadata.
- One generated Markdown file for each source.

Markdown filenames contain the full author slug followed by the source keyword:

```text
<author-slug>-<source>.md
```

Example layout, showing JSON as the native response format:

```text
data/
  authors.md
  publication-schema.md
  researcher-one-full-name/
    raw/
      researcher-one-full-name-ieee-2026-10-21T14-30-00.000000+0200.json
    researcher-one-full-name-ieee.md
  researcher-two-full-name/
    raw/
      researcher-two-full-name-ieee-2026-10-21T14-31-00.000000+0200.json
    researcher-two-full-name-ieee.md
```

IEEE's default API response format is JSON. Native downloaded metadata is
retained alongside generated Markdown without an intermediate CSV transformation. Each
download file is a JSON array of complete native response objects, in retrieval
order, including for a single-page result. Source fields are preserved rather
than flattened or renamed. The manager passes publications from the same source call
to the builder; it does not select or merge historical downloads.

## Download history and failure behavior

Each successful download creates a new file for the author and source. The user
revised the previous replacement policy on 2026-10-21: older downloaded files
must be retained, and new filenames must have the date at the end.

The implementation includes time, microseconds, and UTC offset with that date to
distinguish downloads on the same day. Timestamps use `Europe/Vienna`. Even a
timestamp collision produces a separate file by inserting a sequence number
before the timestamp. Existing download files are never overwritten.

A new file is published only after complete retrieval and serialization succeed.
A failed or partial download leaves previous persisted metadata intact and does
not publish a partial dataset. A successful zero-result search saves a new file
containing the native empty response and explicitly reports zero publications;
previous downloads remain intact.

The current Markdown file is replaced atomically after the complete new document
is ready. If Markdown generation or saving fails, the new raw response is
retained, previous Markdown remains intact, and the failed stage is reported.
Sources save complete raw responses before normalization. If normalization fails,
`DownloadError` retains the saved path and the builder is not called. Raw saving
must succeed before Markdown is built. Successful
zero-result searches save native metadata and an empty Markdown file.

When processing several author/source pairs:

1. A failure for one pair does not stop processing the remaining pairs.
2. Successful pairs are persisted as new dated files.
3. A final report identifies the failed author/source pairs and their errors.

The report includes saved paths and makes partial failures visible. A Markdown
failure identifies the retained raw path. Exit codes are 0 for complete success,
1 for selection/configuration/runtime failures, and 2 for CLI syntax errors.
Requests use the source timeout and are not automatically retried.

## IEEE API authentication

The IEEE source reads **`IEEE_API_KEY` directly from the project `.env` file**
when `download(author)` is called. It uses `dotenv_values(..., interpolate=False)`
and never falls back to process environment variables. Missing files and missing,
unassigned, or blank keys fail the pair before HTTP requests.

Module imports and CLI help do not read credentials. The entry point and
middleware never receive the key. Credential-bearing URLs and source errors are
sanitized within the IEEE module. The author file contains only researcher
definitions. The pipeline does not modify `.env`.

## Publication Markdown contract

The existing [publication schema](../../data/publication-schema.md) defines the
output structure. The heading represents the individual work's title; the
`Publication` field represents its containing journal, conference, book, or
other publication.

Each publication is one H2 section, with fields in this order:

```markdown
## <document title>

Authors: <authors>

Author Affiliations: <affiliations>

Keywords: <keywords>

Abstract: <abstract>

Publication: <publication title>

Year: <publication year>

ISSN: <ISSN>

ISBN: <ISBN>

DOI: <DOI>

Link: <PDF URL>

Publisher: <publisher>
```

Formatting and content rules:

- Repeat the section for each publication in the author/source dataset.
- Include all authors listed in the publication metadata, not just the
  researcher whose search produced it.
- Populate publication affiliations from the returned metadata. The configured
  search affiliations are not a substitute for missing publication affiliations.
- Combine author keywords and IEEE terms into the `Keywords` field, with author
  keywords first. The existing converter joins populated groups with `; `.
- Keep every field label even when its value is unavailable; emit an empty value.
- Put the PDF URL in `Link` when supplied by the source.
- Use blank lines between the heading and fields and between successive fields.
- Keep the document title on one heading line.
- Produce UTF-8 Markdown.

The IEEE documentation identifies logical metadata fields for the mapping:

| Markdown element    | IEEE metadata                                 |
| ------------------- | --------------------------------------------- |
| H2 document title   | `title`                                       |
| Authors             | Author full names, in the listed author order |
| Author Affiliations | Publication author affiliations               |
| Keywords            | Author terms and IEEE terms                   |
| Abstract            | `abstract`                                    |
| Publication         | `publication_title`                           |
| Year                | `publication_year`                            |
| ISSN                | `issn`                                        |
| ISBN                | `isbn`                                        |
| DOI                 | `doi`                                         |
| Link                | `pdf_url`                                     |
| Publisher           | `publisher`                                   |

This table describes the semantic mapping; it does not assert exact nested JSON
paths. IEEE returns only populated fields, so omitted metadata must be handled
as missing values during conversion.

The existing CSV converter preserves input record order. No new requirement to
sort generated Markdown has been agreed. The newest-first rule from the
referenced conversation concerns downstream chatbot answers.

## Existing code and implementation boundaries

The current [CSV converter](../../src/csv_to_semantic_markdown.py) reads IEEE CSV
exports and renders the agreed Markdown field order. It does not implement API
retrieval, the master author file, native API-response parsing, or the new
author/source selection rules.

## Remaining decisions

- Requirements for future sources such as ScienceDirect and Springer Nature.
- Any future standalone command for reconverting historical native downloads.

API request construction and parsing must be checked against IEEE documentation
and the actual response structure during implementation. The author/source
contract must remain the same when later publisher integrations are added.

## IEEE documentation references

- [API query basics](https://developer.ieee.org/docs/read/Searching_the_IEEE_Xplore_Metadata_API):
  request structure, authentication, and the default JSON response format.
- [Search parameters](https://developer.ieee.org/docs/read/Metadata_API_details):
  author, affiliation, and complex-query parameters.
- [Boolean search operators](https://developer.ieee.org/docs/read/metadata_api_details/Leveraging_Boolean_Logic):
  documented `AND`, `OR`, and `NOT` operators.
- [Sorting and paging parameters](https://developer.ieee.org/docs/read/metadata_api_details/Sorting_and_Paging_Parameters):
  `start_record` and `max_records`, with a documented maximum of 200 records per
  response.
- [Returned metadata fields](https://developer.ieee.org/docs/read/Metadata_API_responses):
  available publication fields and omission of unpopulated fields.
- [Quick start guide](https://developer.ieee.org/Quick_Start_Guide): API-key
  registration and issuance.
