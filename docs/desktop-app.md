# Portable desktop app

Extract the archive for your operating system into a writable folder. Open
`PublicationManager.exe` on Windows or `PublicationManager` on Linux by
double-clicking it. Keep the other files beside the application. Python and
the required packages are included; recipients do not install them.

1. Enter a full author name, comma-separated names, or `all`. Names must already
   exist in the supplied author database, as with the CLI.
2. Check the sources to use and enter an API key beside each selected source.
3. Click **Run**. The output area shows the download and Markdown results.

API keys are masked and used only for that run. They are passed to the download
process in memory, never written to `.env` or other application files, and
cleared from the fields when the process starts. Enter them again for every run.

The window stays responsive during downloads. Inputs and closing are disabled
until the run finishes; cancellation is not provided. The running indicator
does not estimate completion. The existing CLI reports its collected results
after processing the selected author/source pairs, so output can take time to
appear. A successful exit can still include report warnings; read the output.

Raw metadata and Markdown are saved under `data/`, and counts and HTML reports
under `output/`, beside the executables. These files remain after the app closes.
Open `output/report.html` in a browser to view the report. Moving the entire
folder preserves its data. New release archives begin with zero counts and no
downloaded publications. Do not extract an upgrade over a folder containing
downloads you want to keep.

## Run from the checkout

Use the existing project environment, with Tkinter available:

```bash
.venv/bin/python src/desktop_app.py
```

The launcher runs `src/download_publications.py` with the entered author and
source arguments in a separate process. The original CLI remains available and
continues reading credentials from the project `.env` unless the explicit
launcher credential mode is enabled.

## Build portable archives

Build tools are needed only on the build computer. Build on each target OS;
the Linux build cannot produce the Windows executable. The current targets are
x64 Windows and x64 Ubuntu-compatible Linux. Linux bundles depend on the host's
glibc baseline: build on the oldest distribution you intend to support and test
there. A bundle built on Ubuntu 26.04 does not establish support for older releases.

Use Python 3.14 with Tkinter on both build machines. Confirm Tkinter is available
by running `python -m tkinter` in the build environment. Use a dedicated build
environment so unrelated installed packages are not collected.

Linux:

```bash
python3 -m venv .build-venv
.build-venv/bin/python -m pip install -r tools/requirements-build.txt
.build-venv/bin/python tools/build_portable.py
```

Windows (PowerShell):

```powershell
py -3.14 -m venv .build-venv
.build-venv\Scripts\python.exe -m pip install -r tools\requirements-build.txt
.build-venv\Scripts\python.exe tools\build_portable.py
```

The build creates `dist/PublicationManager/` and an OS-specific archive:

- Linux: `dist/PublicationManager-linux-x64.tar.gz` (preserves executable permissions).
- Windows: `dist/PublicationManager-windows-x64.zip`.

Share the archive. Recipients must extract it before starting the application;
running directly from an archive is not supported. Linux desktop/file-manager
policies can require allowing the executable to run on first use.

The build copies only the author database, schema, report HTML/JavaScript, and
this guide, alongside the packaged code and runtime. It regenerates zero-count
JSON and HTML in the bundle. It does not include `.env`, existing downloads,
or the checkout's saved report counts, and does not change those original files.
Timezone data is included for `Europe/Vienna`, including on Windows.

Existing build destinations are refused to protect any generated data. Use a
different output folder for another build:

```bash
python tools/build_portable.py --output dist-next
```

## Verification before sharing

Run the offline tests in the build environment:

```bash
python -B -m unittest discover -s tests
```

On **each** target operating system:

1. Extract the archive on a computer without Python installed, using a writable
   path containing spaces. Double-click the desktop executable.
2. Check blank inputs, multiple authors (including accented names), and both
   source checkboxes. Confirm required-key feedback before execution.
3. Run a download with valid credentials. Confirm the UI remains responsive,
   the key fields clear, closing is blocked while running, and results appear.
4. Verify raw JSON, Markdown, and count reports are written inside the extracted
   folder. Close and reopen the app; keys must be empty and outputs retained.
5. Try invalid author selections and invalid credentials; confirm the reported
   failures and that no API key appears in output or newly created text files.
6. Move the entire folder and run it again. Confirm saved data stays intact.

Record the tested OS versions before claiming compatibility. A build on one
platform does not verify the other, and an automated offline test does not
verify live publisher access.

### Validation recorded on 23 October 2026

- The 171 offline tests passed, including launcher lifecycle, subprocess argument
  forwarding, both credential modes, key redaction, and portable resource staging.
- Built on Ubuntu 26.04.1 x64 with Python 3.14.4 and PyInstaller 6.22.3.
- Real Tk widgets were checked for initial state, usable output height, input
  validation, child startup, key clearing, close protection, and completion.
- An extracted Linux archive ran from a path containing spaces and an accented
  character, with Python search paths unavailable and bundled timezone fallback
  forced. Local mock HTTPS publisher responses produced both raw JSON and
  Markdown exports and updated reports. Fake keys were absent from generated
  files; the packaged GUI opened, and outputs survived closing it.
- Live publisher access, a separate clean machine without Python installed, and
  the Windows build/GUI still require target-machine verification. No Windows
  binary is supplied by the Linux build.
