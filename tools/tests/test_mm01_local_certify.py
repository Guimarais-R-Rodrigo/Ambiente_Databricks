from __future__ import annotations

import contextlib
import gc
import io
import sys
import warnings
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import mm01_local_certify as cert

REPO = Path(__file__).resolve().parents[2]


class TestMM01LocalCertification(unittest.TestCase):
    def _result(
        self,
        step_id: str,
        *,
        status: str = "PASS",
        exit_code: int | None = 0,
    ) -> cert.StepResult:
        return cert.StepResult(
            step_id=step_id,
            source="test",
            command=["test"],
            started_utc="2026-01-01T00:00:00Z",
            ended_utc="2026-01-01T00:00:00Z",
            duration_seconds=0.0,
            exit_code=exit_code,
            status=status,
            log_file=None,
            log_sha256=None,
        )

    def _complete_results(self) -> list[cert.StepResult]:
        results = []
        for step_id in sorted(cert.REQUIRED_STEP_IDS):
            if step_id in cert.ALLOWED_SKIP_IDS:
                results.append(
                    self._result(step_id, status="SKIP_ALLOWED", exit_code=None)
                )
            else:
                results.append(self._result(step_id))
        return results

    def test_safe_stdout_write_survives_unencodable_console(self) -> None:
        raw = io.BytesIO()
        console = io.TextIOWrapper(raw, encoding="cp1252", errors="strict")
        try:
            with mock.patch.object(cert.sys, "stdout", console):
                cert._safe_stdout_write("unicode replacement: \ufffd\n")
                console.flush()
            rendered = raw.getvalue().decode("cp1252")
            self.assertIn(r"\ufffd", rendered)
        finally:
            console.close()

    def test_run_step_forces_python_utf8_stdio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs = root / "logs"
            logs.mkdir()
            step = cert.Step(
                "UTF8_TEST",
                "test",
                (
                    sys.executable,
                    "-c",
                    "import os,sys; print(os.environ.get('PYTHONUTF8')); "
                    "print(os.environ.get('PYTHONIOENCODING')); "
                    "print(sys.stdout.encoding)",
                ),
            )
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                result = cert.run_step(step, root, logs)

            self.assertEqual(result.status, "PASS")
            output = (logs / "UTF8_TEST.log").read_text(encoding="utf-8")
            self.assertIn("\n1\n", output)
            self.assertIn("\nutf-8\n", output.lower())

    def test_run_step_keyboard_interrupt_is_structured_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs = root / "logs"
            logs.mkdir()
            step = cert.Step(
                "INTERRUPT_TEST",
                "test",
                (sys.executable, "-c", "print('never completes')"),
            )
            with mock.patch.object(cert.subprocess, "Popen", side_effect=KeyboardInterrupt):
                with contextlib.redirect_stdout(io.StringIO()):
                    result = cert.run_step(step, root, logs)

            self.assertEqual(result.status, "INTERRUPTED")
            self.assertIsNone(result.exit_code)
            self.assertEqual(
                result.reason,
                "KeyboardInterrupt during subprocess execution",
            )
            self.assertIsNotNone(result.log_sha256)
            self.assertTrue((logs / "INTERRUPT_TEST.log").is_file())
            self.assertIn(
                "MM01_LOCAL_CERTIFICATION_STEP_INTERRUPTED=KeyboardInterrupt",
                (logs / "INTERRUPT_TEST.log").read_text(encoding="utf-8"),
            )

    def test_run_step_streams_and_persists_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs = root / "logs"
            logs.mkdir()
            step = cert.Step(
                "STREAM_TEST",
                "test",
                (sys.executable, "-c", "print('stream-ok')"),
            )
            captured = io.StringIO()
            with warnings.catch_warnings():
                warnings.simplefilter("error", ResourceWarning)
                with contextlib.redirect_stdout(captured):
                    result = cert.run_step(step, root, logs)
                gc.collect()

            self.assertEqual(result.status, "PASS")
            self.assertEqual(result.exit_code, 0)
            self.assertIn("stream-ok", captured.getvalue())
            self.assertIn(
                "stream-ok",
                (logs / "STREAM_TEST.log").read_text(encoding="utf-8"),
            )

    def test_resolve_argv_uses_windows_cmd_for_cmd_shim(self) -> None:
        npm_cmd = r"C:\\Program Files\\nodejs\\npm.CMD"
        cmd_exe = r"C:\\Windows\\System32\\cmd.exe"
        with (
            mock.patch.object(cert.shutil, "which", return_value=npm_cmd),
            mock.patch.dict(cert.os.environ, {"COMSPEC": cmd_exe}, clear=False),
        ):
            self.assertEqual(
                cert.resolve_argv(("npm", "--version"), windows=True),
                [cmd_exe, "/d", "/c", "call", npm_cmd, "--version"],
            )

    def test_resolve_argv_fails_closed_when_executable_is_missing(self) -> None:
        with mock.patch.object(cert.shutil, "which", return_value=None):
            with self.assertRaises(cert.CertificationError):
                cert.resolve_argv(("definitely-not-a-real-command-mm01",), windows=False)

    def test_sanitize_text_redacts_escaped_windows_path_variants(self) -> None:
        home = str(Path.home())
        repo = str(REPO)
        home_escaped = home.replace("\\", "\\\\")
        home_double_escaped = home.replace("\\", "\\\\\\\\")
        repo_escaped = repo.replace("\\", "\\\\")

        rendered = cert.sanitize_text(
            "\n".join(
                (
                    home,
                    home_escaped,
                    home_double_escaped,
                    repo,
                    repo_escaped,
                )
            ),
            REPO,
        )

        self.assertNotIn(home, rendered)
        self.assertNotIn(home_escaped, rendered)
        self.assertNotIn(home_double_escaped, rendered)
        self.assertNotIn(repo, rendered)
        self.assertNotIn(repo_escaped, rendered)
        self.assertGreaterEqual(rendered.count("<HOME>"), 3)
        self.assertGreaterEqual(rendered.count("<REPO>"), 2)

    def test_sanitize_argv_redacts_repository_and_home_paths(self) -> None:
        command = cert.sanitize_argv(
            (str(REPO / "tool.py"), str(Path.home() / "venv" / "python.exe")),
            REPO,
        )
        self.assertIn("<REPO>", command[0])
        self.assertIn("<HOME>", command[1])

    def test_remote_normalization_accepts_canonical_forms(self) -> None:
        self.assertEqual(
            cert.normalize_remote(
                "https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks.git"
            ),
            cert.REPOSITORY,
        )
        self.assertEqual(
            cert.normalize_remote(
                "git@github.com:Guimarais-R-Rodrigo/Ambiente_Databricks.git"
            ),
            cert.REPOSITORY,
        )

    def test_remote_normalization_rejects_other_repo(self) -> None:
        self.assertIsNone(cert.normalize_remote("https://github.com/example/other.git"))

    def test_output_must_be_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            with self.assertRaises(cert.CertificationError):
                cert.require_outside_repo(root / "evidence", root)
            outside = Path(tmp) / "evidence"
            cert.require_outside_repo(outside, root)

    def test_complete_result_requires_exact_required_set(self) -> None:
        results = self._complete_results()
        self.assertTrue(cert.result_is_complete(results, True, True))
        self.assertFalse(cert.result_is_complete(results[:-1], True, True))

    def test_required_failure_blocks_certification(self) -> None:
        results = self._complete_results()
        target = next(r for r in results if r.step_id not in cert.ALLOWED_SKIP_IDS)
        target.status = "FAIL"
        target.exit_code = 1
        self.assertFalse(cert.result_is_complete(results, True, True))

    def test_only_v12_scope_may_be_skipped(self) -> None:
        results = self._complete_results()
        other = next(r for r in results if r.step_id not in cert.ALLOWED_SKIP_IDS)
        other.status = "SKIP_ALLOWED"
        other.exit_code = None
        self.assertFalse(cert.result_is_complete(results, True, True))

    def test_preflight_and_postflight_are_mandatory(self) -> None:
        results = self._complete_results()
        self.assertFalse(cert.result_is_complete(results, False, True))
        self.assertFalse(cert.result_is_complete(results, True, False))

    def test_command_plan_covers_all_executable_required_steps(self) -> None:
        ids = {step.step_id for step in cert.command_plan("python")}
        self.assertEqual(ids | cert.ALLOWED_SKIP_IDS, cert.REQUIRED_STEP_IDS)
        self.assertFalse(ids & cert.ALLOWED_SKIP_IDS)

    def test_workflow_pins_cover_exact_source_set(self) -> None:
        self.assertEqual(set(cert.WORKFLOW_EXPECTED_BLOBS), set(cert.WORKFLOW_SOURCES))
        self.assertEqual(set(cert.WORKFLOW_REQUIRED_SNIPPETS), set(cert.WORKFLOW_SOURCES))

    def test_current_workflow_definitions_match_frozen_blob_pins(self) -> None:
        report = cert.check_workflow_drift(REPO)
        self.assertEqual(set(report), set(cert.WORKFLOW_SOURCES))
        self.assertTrue(all(item["blob_matches"] for item in report.values()))


if __name__ == "__main__":
    unittest.main()
