# Publication download guide

For a double-clickable desktop launcher and portable Linux/Windows build
instructions, see the [desktop app guide](desktop-app.md).

The pipeline downloads IEEE Xplore and ScienceDirect publication metadata, saves
the native JSON responses, and generates Markdown exports. The source keywords
are `ieee` and `sciencedirect`. See the [pipeline specification](specs/publication-pipelines-specification.md)
for component responsibilities and data contracts.

## Setup

From the project root, install the dependencies into the project environment:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Author loading uses PyYAML; credential loading uses python-dotenv. The system
timezone database must include `Europe/Vienna`.

### Authors

The author database is [db/authors.yaml](../db/authors.yaml). Each name maps to
its complete affiliation list:

```yaml
Ada Researcher:
  - University A
  - Institute B

René Researcher:
  - University A
  - Former University C
```

Include shared affiliations under each applicable author. Every author needs a
nonempty list of nonempty affiliation strings. Names and affiliations must
contain nonblank text without control characters. Duplicate YAML keys and
invalid entries fail validation before downloading.

Names are matched case-insensitively. For example, `ada researcher` selects
`Ada Researcher`, retaining the YAML spelling in queries and reports. Named
selection fails if database names are ambiguous under case-insensitive matching.

### IEEE credentials

Configure the project-root `.env` file:

```dotenv
IEEE_API_KEY=your-api-key
```

The IEEE module reads this file when called. It ignores process environment
variables and disables variable interpolation. A missing, unassigned, or blank
key produces a download error before any HTTP request. Imports and CLI help do
not load credentials.

## Run the pipeline

The following examples use the names from the sample YAML above:

```bash
.venv/bin/python src/download_publications.py all
.venv/bin/python src/download_publications.py --author "Ada Researcher"
.venv/bin/python src/download_publications.py --source ieee
.venv/bin/python src/download_publications.py --author "ada researcher, René Researcher" --source ieee
```

- Provide bare `all` or at least one selection flag.
- Each flag accepts comma-separated values or `all`. An omitted flag means all
  for that dimension.
- Bare `all` selects every author and source and cannot be combined with flags.
- Flag values are required. Positional author/source names are invalid.
- Surrounding whitespace is trimmed. Duplicates are processed once in selection
  order, including author names that differ only in case.
- Source keywords are lowercased. Currently `ieee` and `sciencedirect` are supported.
- Empty items and `all` mixed with named selections are invalid. Unknown authors
  or sources fail validation before any request.

A search combines the selected author's full YAML name with any configured
affiliation:

```text
Author Name AND (Affiliation A OR Affiliation B OR ...)
```

There is no year filter. Publications with missing or unmatched affiliations may
be absent from the results.

In VS Code, the `Download publications (IEEE)` launch profile prompts for author
and source selections, each defaulting to `all`.

## Saved files

For an export created on 22 October 2026, an author's output looks like:

```text
data/ada-researcher/
  raw/
    ada-researcher-ieee-2026-10-22T14-30-00.000000+0200.json
  ada-researcher-ieee-2026-10-22.md
```

The author slug is the YAML name lowercased with spaces replaced by hyphens.
All filename dates use `Europe/Vienna`.

Every complete raw download creates a new JSON file containing an array of
native response pages. Existing raw files are retained; timestamp collisions
add a sequence number before the timestamp.

Markdown names end in `YYYY-MM-DD`. Another export on the same date atomically
replaces that day's file after the new document is ready. Earlier dated exports
and existing undated files remain.

Markdown follows the [publication schema](../schema/publication-schema.md).
Publication metadata supplies all returned authors and affiliations. Author
keywords precede IEEE terms, absent values retain empty field labels, and output
uses UTF-8.

## Results and failures

The CLI prints a download result for each author/source pair, Markdown results
for attempted builds, and a summary for each stage.

| Outcome | Raw data | Markdown |
| --- | --- | --- |
| Publications found | New native JSON saved | Dated export built |
| Zero publications | New native JSON saved; download succeeds | Build skipped; existing exports retained |
| Retrieval or raw-save failure | No new complete download published | Build skipped |
| Normalization failure | Completed raw file retained; path included in the error message | Build skipped |
| Markdown generation or saving failure | Completed raw file retained | Previous exports preserved |

Source failures do not stop the remaining author/source pairs. A Markdown
failure leaves the corresponding download successful. Skipped builds include
failed downloads and successful zero-result searches.

| Exit code | Meaning |
| --- | --- |
| `0` | Downloads and all attempted Markdown builds succeeded |
| `1` | Author/source validation, downloading, normalization, or Markdown building failed |
| `2` | Invalid CLI syntax or selections such as empty items |

IEEE requests use a 30-second timeout and are not retried automatically.
Publication PDF URLs are included when returned; PDF files are not downloaded.

## JSON and HTML count report

After the existing Markdown reports are printed, the CLI collects successful
download counts and calls `report_generator.update_download_counts()` once.
[output/report.json](../output/report.json) stores these counts by author and
source, plus an ISO `updated_at` timestamp using `Europe/Vienna`:

```json
{
  "updated_at": "2026-10-22T20:00:00+02:00",
  "Alois Zoitl": {"ieee": 0}
}
```

All 47 members start with integer zero IEEE counts. Equal counts stay unchanged,
increases replace saved counts, and decreases retain the saved count and print
a console warning. Failed and unprocessed downloads leave their saved counts
intact. The timestamp refreshes once per completed pipeline execution, including
runs with no successful downloads.

Next, `report_generator.update_report()` reads JSON and synchronizes
[output/report.html](../output/report.html). Its Current Members and Past Members
tables retain the supplied membership and order; new source columns are added
to both tables as needed. The HTML displays saved counts and the JSON timestamp,
without decrease warnings. Both paths are configured in `config.py`.

Open the HTML file directly in a browser. To refresh an already-open page, click
**Update** and choose `output/report.json`. The button reads the selected file
and refreshes the displayed tables; it does not save changes to disk. Keep
`report.js` beside the HTML. No web server is required.

The updater uses the download records' `publication_count` directly, without
reading publication contents, raw files, or Markdown results. Missing or invalid
files and save errors are reported without replacing the affected file. If JSON
saves but HTML synchronization fails, the saved JSON is retained. Warnings and
report-update errors go to stderr without changing existing pipeline exit codes.

## Offline verification

```bash
.venv/bin/python -B -m unittest discover -s tests -v
```

The suite uses synthetic author data, credentials, temporary output directories,
and mocked HTTP. It covers selection, YAML validation, credentials, pagination,
normalization, rendering, storage, and failure handling. The VS Code
`Debug offline tests` launch profile runs the suite under the debugger.

## CSV conversion

The separate [CSV converter](../src/csv_to_semantic_markdown.py) converts a manual
IEEE CSV export into Markdown:

```bash
.venv/bin/python src/csv_to_semantic_markdown.py input.csv output.md
.venv/bin/python src/csv_to_semantic_markdown.py input.csv output.md --encoding cp1252
```

Its default input encoding is `utf-8-sig`; output is UTF-8. Input columns and
records are validated before writing, and publication order follows the CSV.
The caller supplies the output path; the API pipeline's dated filename policy
does not apply to this command.
