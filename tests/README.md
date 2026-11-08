# Tests

Test directories follow the package and subpackage layout under `src/`:

```text
tests/
├── helpers/
├── publication_collector/
│   ├── cli/
│   └── source_downloaders/
├── publication_finder/
│   ├── cli/
│   └── source_downloaders/
├── publication_markdown/
│   └── cli/
├── publication_normalizer/
│   ├── cli/
│   └── source_normalizers/
├── publication_review/
│   └── google_apps_script/
├── scripts/
├── utils/
└── support.py
```

Shared synthetic fixtures are in `tests/support.py`. Tests that exercise a
workflow across components stay with the package coordinating that workflow.
The test package makes `src/` importable; test modules use `tests.support` for
shared fixtures rather than importing a top-level `support` module.

Run commands from the repository root. For all Python tests:

```bash
.venv/bin/python -B -m unittest discover -s tests -t . -v
```

For one package or subpackage:

```bash
.venv/bin/python -B -m unittest discover -s tests/publication_finder -t . -v
.venv/bin/python -B -m unittest discover -s tests/publication_collector/source_downloaders -t . -v
```

Keep `-t .` when using discovery. This imports suites as `tests.<package>` so
directories such as `tests/helpers/` do not shadow application packages.
Individual modules can also be run by their full test-package name:

```bash
.venv/bin/python -B -m unittest tests.publication_finder.test_finder_queries -v
```

The browser review application's Apps Script tests run separately:

```bash
node tests/publication_review/google_apps_script/google_apps_script_review.test.cjs
```

The Python suites use temporary directories, synthetic credentials, and mocked
HTTP. The Apps Script suite uses simulated Google services and needs no npm
dependencies.
