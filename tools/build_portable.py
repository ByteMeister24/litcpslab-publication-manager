"""Build a relocatable desktop/CLI bundle on the current operating system."""

import argparse
from datetime import datetime
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import config
from publication_collector.download_manager import SUPPORTED_SOURCES
from utils.yaml_loader import convert_yaml_to_dict


REPORT_INITIALIZER = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import config
config.REPORT_HTML_FILE = Path(sys.argv[2]) / 'output' / 'report.html'
config.REPORT_JSON_FILE = Path(sys.argv[2]) / 'output' / 'report.json'
from report_generator import update_report
update_report()
"""


def stage_resources(bundle: Path, project: Path = PROJECT_ROOT) -> None:
    """Copy only distribution inputs, then render fresh report state in isolation."""
    for relative in ("db/authors.yaml", "schema/publication-schema.md", "output/report.html", "output/report.js"):
        destination = bundle / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(project / relative, destination)
    (bundle / "data").mkdir(exist_ok=True)
    authors = convert_yaml_to_dict(bundle / "db" / "authors.yaml")
    report = {
        "updated_at": datetime.now(ZoneInfo(config.DOWNLOAD_TIMEZONE)).isoformat(timespec="seconds"),
        **{author: {source: 0 for source in SUPPORTED_SOURCES} for author in authors},
    }
    (bundle / "output" / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    # Run the existing renderer with staged paths, leaving checkout reports untouched.
    subprocess.run(
        [sys.executable, "-B", "-c", REPORT_INITIALIZER, str(PROJECT_ROOT / "src"), str(bundle)], check=True
    )
    shutil.copyfile(project / "docs" / "desktop-app.md", bundle / "README.md")


def build(output: Path) -> tuple[Path, Path]:
    system = platform.system()
    if system not in ("Linux", "Windows") or platform.machine().lower() not in ("x86_64", "amd64"):
        raise ValueError("Build on x64 Linux or x64 Windows to create the matching portable app.")
    for module in ("PyInstaller", "tzdata"):
        if importlib.util.find_spec(module) is None:
            raise ValueError("Install tools/requirements-build.txt into the build environment first.")

    archive_name = f"PublicationManager-{system.lower()}-x64"
    extension = ".zip" if system == "Windows" else ".tar.gz"
    destination = output / "PublicationManager"
    archive_destination = output / (archive_name + extension)
    if destination.exists() or archive_destination.exists():
        raise FileExistsError("The output already contains a bundle. Choose a new --output folder.")

    with tempfile.TemporaryDirectory(prefix="publication-build-") as temporary:
        working = Path(temporary)
        environment = os.environ.copy()
        environment["PYINSTALLER_CONFIG_DIR"] = str(working / "cache")
        subprocess.run(
            [sys.executable, "-B", "-m", "PyInstaller", str(PROJECT_ROOT / "tools" / "portable.spec"),
             "--distpath", str(working / "dist"), "--workpath", str(working / "work"), "--noconfirm"],
            check=True,
            cwd=PROJECT_ROOT,
            env=environment,
        )
        bundle = working / "dist" / "PublicationManager"
        stage_resources(bundle)
        archive = shutil.make_archive(
            str(working / archive_name), "zip" if system == "Windows" else "gztar",
            root_dir=bundle.parent, base_dir=bundle.name,
        )
        output.mkdir(parents=True, exist_ok=True)
        shutil.copytree(bundle, destination)
        shutil.copyfile(archive, archive_destination)
    return destination, archive_destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "dist", help="Destination for the app and archive.")
    arguments = parser.parse_args()
    try:
        bundle, archive = build(arguments.output.resolve())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Build failed: {error}\n")
    print(f"App: {bundle}\nArchive: {archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
