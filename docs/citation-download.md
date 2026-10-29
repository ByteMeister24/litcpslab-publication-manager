# Publication download guide

The source collection workflow downloads IEEE Xplore and ScienceDirect publication
lists and saves complete native JSON responses. It prints download confirmations
or errors and a final summary. Normalization and Markdown creation are separate
workflows; downloading does not generate Markdown.

The implementation is in `src/publication_collector/`. See the
[workflow specification](specs/publication-pipelines-specification.md) for
component responsibilities and contracts.

## Setup

From the project root, install the project and its dependencies in editable mode:

```bash
.venv/bin/python -m pip install -e .
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
`Ada Researcher`, retaining the YAML spelling in queries and console output.
Named selection fails if database names are ambiguous under case-insensitive matching.

### Publisher credentials

Configure the project-root `.env` file with the keys for the sources you use:

```dotenv
IEEE_API_KEY=your-ieee-api-key
SCIENCEDIRECT_API_KEY=your-sciencedirect-api-key
```

Normal CLI use reads this file at download time, ignores process environment
API keys, and disables variable interpolation. A missing, unassigned, or blank
key produces a download error before any HTTP request. Imports and CLI help do
not load credentials.

## Run collection

Activate the project environment once per terminal session:

```bash
source .venv/bin/activate
```

Then run the workflow by its command name. These examples use names from the
sample YAML above:

```bash
publication_collector all
publication_collector --author "Ada Researcher"
publication_collector --source ieee
publication_collector --author "ada researcher, René Researcher" --source ieee,sciencedirect
```

The editable install makes the package importable and registers this command in
the environment. Source edits take effect without reinstalling. The command works
from any directory and keeps using this checkout's database, credentials, and
data directory. You can also run `python -m publication_collector` in the activated
environment. Neither invocation requires setting `PYTHONPATH`.

- Provide bare `all` or at least one selection flag.
- Each flag accepts comma-separated values or `all`. An omitted flag means all
  for that dimension.
- Bare `all` selects every author and source and cannot be combined with flags.
- Flag values are required. Positional author/source names are invalid.
- Surrounding whitespace is trimmed. Duplicates are processed once in selection
  order, including author names that differ only in case.
- Source keywords are lowercased. Supported keywords are `ieee` and `sciencedirect`.
- Empty items and `all` mixed with named selections are invalid. Unknown authors
  or sources fail validation before any request.

A search combines the author's full YAML name with any configured affiliation.
There is no year filter. Publications with missing or unmatched affiliations may
be absent from the results.

## Saved files

A completed download produces a file such as:

```text
data/ada-researcher/download/ieee/ada-researcher-ieee-2026-10-27T14-30-00.000000+0100.json
```

The author slug is the YAML name lowercased with spaces replaced by hyphens.
Timestamps use `Europe/Vienna`.

Every complete download creates a new JSON file containing an array of native
response pages, including all original metadata fields. Existing raw files are
retained; timestamp collisions produce a saving error without replacing the existing file.
The collector creates no normalized datasets or Markdown files.

## Results and failures

For each author/source pair, a source returns either:

- `DownloadConfirmation`: canonical author name, source keyword, publication
  count, and saved raw-file path. The CLI prints these details to stdout.
- `DownloadError`: canonical author name, source keyword, and sanitized error.
  The CLI prints these details to stderr.

The manager processes pairs sequentially and preserves their order. A returned
failure does not stop remaining pairs. The CLI prints a final success/failure
summary after processing.

| Outcome | Raw data | Existing files |
| --- | --- | --- |
| Publications found | New complete native JSON saved | Retained |
| Zero publications | New native JSON saved; download succeeds | Retained |
| Partial or failed retrieval | No new dataset published | Retained |
| Raw-save failure | No completed new dataset published | Retained |

Metadata requiring later normalization does not fail an otherwise valid complete
download. Normalization and Markdown creation do not run during collection.

| Exit code | Meaning |
| --- | --- |
| `0` | All downloads succeeded, including successful zero-result searches |
| `1` | Author/source validation, downloading, or raw saving failed |
| `2` | Invalid CLI syntax or selections such as empty items |

Both sources use a 30-second timeout and no automatic retries. Publication PDF
URLs are preserved in native metadata when returned; PDF files are not downloaded.

## Offline verification

```bash
.venv/bin/python -B -m unittest discover -s tests -v
```

Collector tests are split between CLI behavior (`test_collector_cli.py`),
coordination (`test_download_manager.py`), source-specific retrieval, and the
shared download workflow. They use synthetic credentials, temporary directories,
and mocked HTTP. Regressions cover the package entry point,
selection, pagination, credential redaction, raw storage, and continued processing
after failures. Normalization and rendering tests remain separate.

## Normalization

The separate [normalization workflow](publication-normalization.md) now combines
saved IEEE/ScienceDirect JSON, one Springer CSV, and one ACM BibTeX file into
per-author normalized JSON.
