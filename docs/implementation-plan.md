# Reorganize the pipeline around the architecture diagram

## Summary

Use `main.py` as the CLI entry point, a Download Manager for coordination, a
Author Builder using a reusable Markdown Reader, source modules for retrieval and raw
storage, and a Markdown Builder for formatting and saving exports.

Preserve current CLI syntax, credentials policy, file layout, and failure
behavior. Implement IEEE only.

## Component changes

- Rename the CLI module to `main.py`. Keep argument parsing, normalization into
  `DownloadRequest`, report printing, and exit-code handling there.
- Rename the middleware module to `download_manager.py`, retaining
  `run_download(request: DownloadRequest)`. Resolve sources, request selected
  authors from the Author Builder, invoke each source once per author, and delegate
  Markdown generation. The manager performs no file writes.
- Rename the author-specific reader to `author_builder.py`. Its public
  `load_authors` function accepts selected names or `"all"` and returns
  `list[Author]`. It interprets H2 sections and their H3 subsections, validates
  author definitions, and combines common and additional affiliations.
- Keep `markdown_reader.py` reusable: `read_markdown(path)` returns a navigable
  document with sections, subsection hierarchy, and syntax-block content, using
  `markdown-it-py`. It does not interpret author definitions. The author file
  uses H2/H3 headings without an H1 title.
- Move rendering from `publication_markdown.py` into `markdown_builder.py` and add
  export saving with stage-specific feedback.
- Source modules and Markdown Builder invoke the shared `storage.py` helper.
  Filename rules and safe-write behavior remain centralized.
- Keep source credentials and API settings inside their respective source
  modules. Keep project-wide settings in `config.py`.

## Data flow and failure handling

- Each source exposes `download(author: Author) -> SourceDownload`.
- Change `SourceDownload` to contain common `publications` and `raw_file_path`.
- Sources retrieve and validate every page, save the complete raw response, and
  then normalize publications. A normalization failure carries the saved
  raw-file path back through `DownloadError`.
- Markdown Builder receives the author, source, and common publication records.
  It renders the documented schema, saves through the storage helper, and returns
  `MarkdownBuildResult` containing the Markdown path or a stage-specific error.
- The manager assembles one `DownloadResult` per author/source pair and returns
  the list to `main.py`.
- Preserve previous Markdown on source or builder failure, retain completed raw
  downloads, and continue other pairs. Successful empty searches save raw
  metadata and empty Markdown.
- The schema remains a documented contract implemented by Python configuration.

## Verification and migration

- Update imports, tests, documentation, and the debug launcher for renamed entry
  point and modules. Remove superseded modules after their responsibilities have
  moved; do not add compatibility wrappers.
- Test that the CLI passes only `DownloadRequest`, the generic reader preserves
  section hierarchy and content, the Author Builder returns the correct authors
  and affiliations, and the manager delegates rather than writes files.
- Test source-owned raw saving before normalization, retained paths on
  normalization failure, builder success/failure feedback, per-pair results, and
  continuation after failures.
- Preserve CLI selection validation, pagination, exact Markdown formatting,
  native metadata retention, safe writes, and legacy CSV-renderer behavior.
- Run the complete offline suite using synthetic documents, credentials, and
  mocked HTTP.
- Preserve existing author data, historical downloads, `.env`, `.gitignore`, and
  legacy CSV-converter behavior. ScienceDirect and Springer Nature remain
  extension points. PDF downloading remains outside this change.
