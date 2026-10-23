"""Two entry points sharing a one-folder runtime; application data stays outside it."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files


project = Path(SPECPATH).parent
source = project / "src"
timezone_data = collect_data_files("tzdata")

desktop = Analysis([str(source / "desktop_app.py")], pathex=[str(source)], datas=timezone_data)
desktop_exe = EXE(
    PYZ(desktop.pure),
    desktop.scripts,
    [],
    exclude_binaries=True,
    name="PublicationManager",
    console=False,
    contents_directory="_internal",
    upx=False,
)

cli = Analysis([str(source / "download_publications.py")], pathex=[str(source)], datas=timezone_data)
cli_exe = EXE(
    PYZ(cli.pure),
    cli.scripts,
    [("u", None, "OPTION"), ("X utf8", None, "OPTION")],
    exclude_binaries=True,
    name="download_publications",
    console=True,
    contents_directory="_internal",
    upx=False,
)

COLLECT(
    desktop_exe,
    cli_exe,
    desktop.binaries,
    desktop.datas,
    cli.binaries,
    cli.datas,
    name="PublicationManager",
    upx=False,
)
