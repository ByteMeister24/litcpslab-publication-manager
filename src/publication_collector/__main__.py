# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Run the publication collector with ``python -m publication_collector``."""

import sys

from publication_collector.cli.download_publications import main


if __name__ == "__main__":
    sys.exit(main())
