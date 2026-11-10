# Copyright (c) 2026 Mainak Majumder (@ByteMeister24)

"""Source-aligned test suites, importable as ``tests.<package>``."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Keep application imports independent of the test directory used for discovery.
sys.path.insert(0, str(PROJECT_ROOT / "src"))
