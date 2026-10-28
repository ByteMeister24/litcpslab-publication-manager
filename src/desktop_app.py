"""Desktop launcher for the existing publication-download CLI."""

import os
from pathlib import Path
from queue import Empty, Queue
import subprocess
import sys
from threading import Thread
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

import config
from publication_collector.download_manager import SUPPORTED_SOURCES
from publication_collector.source_downloaders import ieee_xplore, sciencedirect


SOURCE_API_KEYS = {
    ieee_xplore.SOURCE: ieee_xplore.API_KEY_NAME,
    sciencedirect.SOURCE: sciencedirect.API_KEY_NAME,
}
SOURCE_LABELS = {"ieee": "IEEE Xplore", "sciencedirect": "ScienceDirect"}
POLL_INTERVAL_MS = 100


def build_command(authors: str, sources: tuple[str, ...]) -> list[str]:
    """Forward selections without reproducing the CLI's parsing rules."""
    if not authors.strip():
        raise ValueError("Enter an author name, comma-separated names, or all.")
    if not sources:
        raise ValueError("Select at least one source.")
    if any(source not in SUPPORTED_SOURCES for source in sources):
        raise ValueError("An unsupported source was selected.")

    if getattr(sys, "frozen", False):
        suffix = ".exe" if sys.platform == "win32" else ""
        command = [str(Path(sys.executable).parent / f"download_publications{suffix}")]
    else:
        command = [sys.executable, "-u", "-m", "publication_collector"]
    return command + ["--author", authors.strip(), "--source", ",".join(sources)]


def build_environment(sources: tuple[str, ...], api_keys: dict[str, str]) -> dict[str, str]:
    """Copy the environment; only selected, freshly entered keys reach the child."""
    environment = os.environ.copy()
    for variable in SOURCE_API_KEYS.values():
        environment.pop(variable, None)
    for source in sources:
        key = api_keys.get(source, "").strip()
        if not key:
            raise ValueError(f"Enter an API key for {SOURCE_LABELS[source]}.")
        if any(ord(character) < 32 or ord(character) == 127 for character in key):
            raise ValueError(f"The API key for {SOURCE_LABELS[source]} contains a control character.")
        environment[SOURCE_API_KEYS[source]] = key
    environment[config.CREDENTIAL_MODE_VARIABLE] = "environment"
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PYTHONUNBUFFERED"] = "1"
    return environment


def start_download(authors: str, sources: tuple[str, ...], api_keys: dict[str, str]) -> subprocess.Popen[str]:
    command = build_command(authors, sources)
    environment = build_environment(sources, api_keys)
    return subprocess.Popen(
        command,
        cwd=config.PROJECT_ROOT if getattr(sys, "frozen", False) else config.PROJECT_ROOT / "src",
        env=environment,
        shell=False,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )


def collect_output(process: subprocess.Popen[str], events: Queue) -> None:
    """Read pipes off the Tk thread and reap the child before reporting completion."""
    try:
        stream = process.stdout
        if stream is None:
            events.put(("output", "Cannot read process output: no stdout pipe.\n"))
        else:
            with stream:
                for line in stream:
                    events.put(("output", line))
    except OSError as error:
        events.put(("output", f"Cannot read process output ({type(error).__name__}).\n"))
    finally:
        events.put(("finished", process.wait()))


def completion_status(returncode: int) -> str:
    if returncode == 0:
        return "Completed successfully (exit code 0)."
    if returncode == 2:
        return "Invalid selections (exit code 2). See output below."
    return f"Finished with errors (exit code {returncode}). See output below."


class DesktopApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.running = False
        self.events = Queue()
        self.author = tk.StringVar(root)
        self.status = tk.StringVar(root, "Ready.")
        self.selected = {source: tk.BooleanVar(root) for source in SUPPORTED_SOURCES}
        self.api_keys = {source: tk.StringVar(root) for source in SUPPORTED_SOURCES}
        self.source_checks = {}
        self.key_entries = {}

        root.title("Publication Manager")
        root.protocol("WM_DELETE_WINDOW", self.request_close)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        frame = ttk.Frame(root, padding=20)
        frame.grid(sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(8, weight=1)

        ttk.Label(frame, text="Publication Manager", font=("TkDefaultFont", 18, "bold")).grid(sticky="w")
        ttk.Label(frame, text="Authors").grid(row=1, sticky="w", pady=(18, 4))
        self.author_entry = ttk.Entry(frame, textvariable=self.author)
        self.author_entry.grid(row=2, sticky="ew")
        ttk.Label(frame, text="Enter full names separated by commas, or all. Use names from the author database.",
                  wraplength=700).grid(
            row=3, sticky="w", pady=(4, 14)
        )

        sources_frame = ttk.LabelFrame(frame, text="Sources and API keys", padding=12)
        sources_frame.grid(row=4, sticky="ew")
        sources_frame.columnconfigure(1, weight=1)
        for row, source in enumerate(SUPPORTED_SOURCES):
            check = ttk.Checkbutton(
                sources_frame, text=SOURCE_LABELS[source], variable=self.selected[source], command=self.update_controls
            )
            check.grid(row=row, column=0, sticky="w", padx=(0, 20), pady=5)
            entry = ttk.Entry(sources_frame, textvariable=self.api_keys[source], show="*")
            entry.grid(row=row, column=1, sticky="ew", pady=5)
            self.source_checks[source] = check
            self.key_entries[source] = entry
        ttk.Label(frame, text="API keys are used only for this run and are never saved.", wraplength=700).grid(
            row=5, sticky="w", pady=(6, 14)
        )

        actions = ttk.Frame(frame)
        actions.grid(row=6, sticky="ew")
        actions.columnconfigure(1, weight=1)
        self.run_button = ttk.Button(actions, text="Run", command=self.start_run)
        self.run_button.grid(row=0, column=0, padx=(0, 14))
        self.progress = ttk.Progressbar(actions, mode="indeterminate")
        self.progress.grid(row=0, column=1, sticky="ew")
        ttk.Label(frame, textvariable=self.status, wraplength=700).grid(row=7, sticky="w", pady=(10, 6))
        self.output = ScrolledText(frame, width=70, height=10, wrap="word", state="disabled", font="TkFixedFont")
        self.output.grid(row=8, sticky="nsew")
        self.update_controls()
        # Respect the actual font/theme metrics instead of squeezing the output into a fixed window.
        root.update_idletasks()
        width = min(root.winfo_reqwidth(), root.winfo_screenwidth() - 80)
        height = min(root.winfo_reqheight(), root.winfo_screenheight() - 100)
        minimum_height = root.winfo_reqheight() - self.output.frame.winfo_reqheight() + 120
        root.minsize(min(760, width), min(minimum_height, height))
        root.geometry(f"{width}x{height}")
        self.author_entry.focus_set()
        self.poll_after_id = root.after(POLL_INTERVAL_MS, self.poll_events)

    def update_controls(self) -> None:
        state = "disabled" if self.running else "normal"
        self.author_entry.configure(state=state)
        self.run_button.configure(state=state)
        for source in SUPPORTED_SOURCES:
            self.source_checks[source].configure(state=state)
            enabled = self.selected[source].get() and not self.running
            self.key_entries[source].configure(state="normal" if enabled else "disabled")
            if not self.selected[source].get():
                self.api_keys[source].set("")

    def start_run(self) -> None:
        if self.running:
            return
        sources = tuple(source for source in SUPPORTED_SOURCES if self.selected[source].get())
        keys = {source: self.api_keys[source].get() for source in sources}
        try:
            process = start_download(self.author.get(), sources, keys)
        except ValueError as error:
            messagebox.showerror("Cannot run", str(error), parent=self.root)
            return
        except OSError as error:
            # Do not include exception values: credentials must never reach dialogs or logs.
            self.status.set(f"Cannot start download process ({type(error).__name__}).")
            messagebox.showerror(
                "Cannot start", "Check that the application files exist and the folder is accessible.", parent=self.root
            )
            return

        for variable in self.api_keys.values():
            variable.set("")
        keys.clear()
        self.running = True
        self.update_controls()
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")
        self.status.set("Running… Output appears when the download process reports results.")
        self.progress.start()
        Thread(target=collect_output, args=(process, self.events), daemon=True).start()

    def poll_events(self) -> None:
        while True:
            try:
                kind, value = self.events.get_nowait()
            except Empty:
                break
            if kind == "output":
                self.output.configure(state="normal")
                self.output.insert("end", value)
                self.output.see("end")
                self.output.configure(state="disabled")
            elif kind == "finished":
                self.running = False
                self.progress.stop()
                self.status.set(completion_status(value))
                self.update_controls()
        self.poll_after_id = self.root.after(POLL_INTERVAL_MS, self.poll_events)

    def request_close(self) -> None:
        if self.running:
            messagebox.showinfo("Download in progress", "Wait for the current run to finish before closing.", parent=self.root)
        else:
            self.root.after_cancel(self.poll_after_id)
            self.root.destroy()


def main() -> None:
    root = tk.Tk()
    DesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
