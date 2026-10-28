"""Launcher behavior without requiring a graphical display or live publisher API."""

import os
from pathlib import Path
from queue import Queue
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

from support import PROJECT_ROOT
import config
import desktop_app


class LauncherProcessTests(unittest.TestCase):
    def test_author_text_and_source_arguments_are_forwarded_unchanged(self):
        command = desktop_app.build_command(" René Researcher, Ada Researcher ", ("ieee", "sciencedirect"))
        self.assertEqual(command, [sys.executable, "-u", "-m", "publication_collector",
                                   "--author", "René Researcher, Ada Researcher", "--source", "ieee,sciencedirect"])
        self.assertEqual(desktop_app.build_command("all", ("ieee",))[-4:], ["--author", "all", "--source", "ieee"])
        # Parsing, including invalid comma lists, belongs to the existing CLI.
        self.assertIn("all,A", desktop_app.build_command("all,A", ("ieee",)))

    def test_frozen_launcher_uses_sibling_cli_executable_on_each_platform(self):
        for system, suffix in (("linux", ""), ("win32", ".exe")):
            with self.subTest(system=system), patch.object(sys, "frozen", True, create=True), \
                    patch.object(sys, "platform", system), patch.object(sys, "executable", "/portable app/PublicationManager" + suffix):
                command = desktop_app.build_command("all", ("ieee",))
                self.assertEqual(command[0], "/portable app/download_publications" + suffix)
                self.assertNotIn("-u", command)

    def test_blank_author_no_sources_and_unknown_sources_do_not_start_a_process(self):
        for authors, sources in ((" ", ("ieee",)), ("all", ()), ("all", ("unknown",))):
            with self.subTest(authors=authors, sources=sources), patch("desktop_app.subprocess.Popen") as spawn:
                with self.assertRaises(ValueError):
                    desktop_app.start_download(authors, sources, {})
                spawn.assert_not_called()

    def test_selected_source_requires_a_nonblank_key(self):
        for keys in ({}, {"ieee": ""}, {"ieee": "  "}, {"ieee": "bad\nkey"}):
            with self.subTest(keys=keys), patch("desktop_app.subprocess.Popen") as spawn:
                with self.assertRaises(ValueError):
                    desktop_app.start_download("all", ("ieee",), keys)
                spawn.assert_not_called()

    def test_only_selected_keys_enter_child_environment_and_parent_is_unchanged(self):
        with patch.dict(os.environ, {"IEEE_API_KEY": "old-ieee", "SCIENCEDIRECT_API_KEY": "old-science"}, clear=True):
            before = os.environ.copy()
            environment = desktop_app.build_environment(("ieee",), {"ieee": " fresh-key ", "sciencedirect": "unused-key"})
            self.assertEqual(environment["IEEE_API_KEY"], "fresh-key")
            self.assertNotIn("SCIENCEDIRECT_API_KEY", environment)
            self.assertEqual(environment[config.CREDENTIAL_MODE_VARIABLE], "environment")
            self.assertEqual(os.environ.copy(), before)

    def test_spawn_uses_argument_list_pipes_utf8_and_no_shell_without_creating_files(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(config, "PROJECT_ROOT", Path(directory)), \
                patch("desktop_app.subprocess.Popen") as spawn:
            desktop_app.start_download("René Researcher", ("ieee",), {"ieee": "run-only-key"})
            command = spawn.call_args.args[0]
            options = spawn.call_args.kwargs
            self.assertNotIn("run-only-key", repr(command))
            self.assertEqual(options["env"]["IEEE_API_KEY"], "run-only-key")
            self.assertFalse(options["shell"])
            self.assertEqual(options["cwd"], Path(directory) / "src")
            self.assertEqual(options["encoding"], "utf-8")
            self.assertEqual(options["stdin"], subprocess.DEVNULL)
            self.assertEqual(options["stdout"], subprocess.PIPE)
            self.assertEqual(options["stderr"], subprocess.STDOUT)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_windows_child_has_no_console_window(self):
        with patch.object(sys, "platform", "win32"), \
                patch.object(subprocess, "CREATE_NO_WINDOW", 0x08000000, create=True), \
                patch("desktop_app.subprocess.Popen") as spawn:
            desktop_app.start_download("all", ("ieee",), {"ieee": "key"})
            self.assertEqual(spawn.call_args.kwargs["creationflags"], 0x08000000)

    def test_stdout_stderr_and_exit_code_reach_the_event_queue(self):
        process = subprocess.Popen(
            [sys.executable, "-u", "-c", "import sys; print('René'); print('warning', file=sys.stderr); sys.exit(1)"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
        )
        events = Queue()
        desktop_app.collect_output(process, events)
        self.assertEqual([events.get_nowait() for _ in range(events.qsize())],
                         [("output", "René\n"), ("output", "warning\n"), ("finished", 1)])
        self.assertEqual(process.returncode, 1)

    def test_missing_stdout_pipe_reports_an_error_and_still_reaps_the_process(self):
        process = Mock(stdout=None)
        process.wait.return_value = 1
        events = Queue()
        desktop_app.collect_output(process, events)
        self.assertEqual(events.get_nowait(), ("output", "Cannot read process output: no stdout pipe.\n"))
        self.assertEqual(events.get_nowait(), ("finished", 1))
        process.wait.assert_called_once_with()

    def test_actual_cli_returns_usage_failure_without_exposing_key(self):
        events = Queue()
        process = desktop_app.start_download("all,A", ("ieee",), {"ieee": "run-only-key"})
        desktop_app.collect_output(process, events)
        values = [events.get_nowait() for _ in range(events.qsize())]
        self.assertEqual(values[-1], ("finished", 2))
        output = "".join(value for kind, value in values if kind == "output")
        self.assertIn("all cannot be mixed", output)
        self.assertNotIn("run-only-key", output)


class DesktopLifecycleTests(unittest.TestCase):
    def setUp(self):
        # Exercise UI state transitions without constructing Tk or needing a display.
        self.app = desktop_app.DesktopApp.__new__(desktop_app.DesktopApp)
        self.app.root = Mock()
        self.app.poll_after_id = "poll"
        self.app.running = False
        self.app.events = Queue()
        self.app.author = Mock()
        self.app.author.get.return_value = "René Researcher"
        self.app.status = Mock()
        self.app.selected = {source: Mock() for source in desktop_app.SUPPORTED_SOURCES}
        self.app.api_keys = {source: Mock() for source in desktop_app.SUPPORTED_SOURCES}
        self.app.source_checks = {source: Mock() for source in desktop_app.SUPPORTED_SOURCES}
        self.app.key_entries = {source: Mock() for source in desktop_app.SUPPORTED_SOURCES}
        for source in desktop_app.SUPPORTED_SOURCES:
            self.app.selected[source].get.return_value = source == "ieee"
            self.app.api_keys[source].get.return_value = "run-only-key"
        for name in ("author_entry", "run_button", "output", "progress"):
            setattr(self.app, name, Mock())

    def test_successful_start_clears_keys_locks_inputs_and_prevents_duplicate_runs(self):
        with patch("desktop_app.start_download") as start, patch("desktop_app.Thread") as thread:
            self.app.start_run()
            self.app.start_run()
        start.assert_called_once()
        self.assertTrue(self.app.running)
        for variable in self.app.api_keys.values():
            variable.set.assert_called_with("")
        self.app.run_button.configure.assert_called_with(state="disabled")
        for entry in self.app.key_entries.values():
            entry.configure.assert_called_with(state="disabled")
        self.app.progress.start.assert_called_once()
        thread.return_value.start.assert_called_once()

    def test_invalid_inputs_keep_keys_and_do_not_start_worker(self):
        with patch("desktop_app.start_download", side_effect=ValueError("Enter author text.")), \
                patch("desktop_app.messagebox.showerror") as dialog, patch("desktop_app.Thread") as thread:
            self.app.start_run()
        self.assertFalse(self.app.running)
        self.app.api_keys["ieee"].set.assert_not_called()
        dialog.assert_called_once()
        thread.assert_not_called()

    def test_spawn_failure_is_reported_without_logging_exception_values(self):
        with patch("desktop_app.start_download", side_effect=OSError("secret value")), \
                patch("desktop_app.messagebox.showerror") as dialog:
            self.app.start_run()
        self.assertFalse(self.app.running)
        self.assertNotIn("secret value", str(self.app.status.mock_calls) + str(dialog.mock_calls))
        self.app.status.set.assert_called_with("Cannot start download process (OSError).")

    def test_output_and_completion_restore_controls_for_another_run(self):
        for code in (0, 1, 2, -9):
            with self.subTest(code=code):
                self.app.running = True
                self.app.events.put(("output", "result\n"))
                self.app.events.put(("finished", code))
                self.app.poll_events()
                self.assertFalse(self.app.running)
                self.app.output.insert.assert_called_with("end", "result\n")
                self.app.status.set.assert_called_with(desktop_app.completion_status(code))
                self.app.run_button.configure.assert_called_with(state="normal")
                self.app.key_entries["ieee"].configure.assert_called_with(state="normal")
                self.app.key_entries["sciencedirect"].configure.assert_called_with(state="disabled")

    def test_closing_is_blocked_only_during_a_run(self):
        self.app.running = True
        with patch("desktop_app.messagebox.showinfo") as dialog:
            self.app.request_close()
        self.app.root.destroy.assert_not_called()
        dialog.assert_called_once()
        self.app.running = False
        self.app.request_close()
        self.app.root.after_cancel.assert_called_once_with("poll")
        self.app.root.destroy.assert_called_once()
