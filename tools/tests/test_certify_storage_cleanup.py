"""Synthetic storage failures after real owned processes; no native Win32 claim.

The CLI remains a real subprocess. Readiness, OS liveness, external exit, raw
exception and filesystem observations are independent of certification PASS.
SEF_STORAGE_CLEANUP_ARTIFACT_DIR retains exclusive fixture/evidence directories.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("storage_cleanup_test_support", ROOT / "tools/tests/test_certify_local.py")
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)
cert = support.cert


def cli_probe(mode, target, root, directory, fault):
    """Fault only our process temporary directory; never retry the tested gate."""
    directory = Path(directory)
    original_exit = tempfile.TemporaryDirectory.__exit__
    original_persist = cert._persist_process_observation
    injections, complete_writes = [], []
    # Test-only ownership: an exception injected before cleanup() leaves the
    # weakref finalizer armed. Keep the object alive until the external oracle
    # has recorded/copied the residue; never change the production finalizer.
    retained_temporaries = {}
    def cleanup(temporary, *args):
        # The record is in the direct caller for both the original implementation
        # and the corrective observer. This is a test injection, not production.
        record = sys._getframe(1).f_locals.get("record", {})
        eligible = (Path(temporary.name).name.startswith("sef-process-") and not injections
                    and record.get("result") == ("EXITED" if mode == "normal" else "INTERRUPTED"))
        if mode == "normal":
            eligible = eligible and "CLI_BEFORE_INTERRUPT" in record.get("stdout", "")
        if not eligible or fault == "none":
            return original_exit(temporary, *args)
        if fault != "before_removal":
            original_exit(temporary, *args)
        else:
            retained_temporaries[temporary.name] = temporary
        injections.append({"path": temporary.name, "kind": "SYNTHETIC_" + fault.upper(),
                           "exists_before_error": os.path.lexists(temporary.name)})
        error = PermissionError(13, "SYNTHETIC_STORAGE_CLEANUP", str(Path(temporary.name) / "stderr"))
        error.winerror = 32  # Deliberate fixture code, not an observed native error.
        raise error
    def persist(record):
        if record.get("cleanup") == "COMPLETE" and record.get("temporary_directory"):
            exists = os.path.lexists(record["temporary_directory"])
            complete_writes.append({"path": record["temporary_directory"], "exists": exists})
            if exists:
                raise AssertionError("COMPLETE_WRITTEN_BEFORE_TEMPORARY_CLEANUP")
        if fault == "journal" and record.get("temporary_cleanup") == "FAILED":
            raise OSError("SYNTHETIC_CLEANUP_JOURNAL")
        return original_persist(record)
    try:
        with mock.patch.object(tempfile.TemporaryDirectory, "__exit__", cleanup), mock.patch.object(cert, "_persist_process_observation", persist):
            support.main_cli_probe(mode, target, root, str(directory))
    finally:
        # Snapshot residue before explicit test-only cleanup. Never call it PASS.
        for item in injections:
            path = Path(item["path"])
            item["exists_at_oracle"] = path.exists()
            owner = retained_temporaries.get(str(path))
            if owner is not None:
                item["test_owner_retained_at_oracle"] = True
                item["finalizer_alive_at_oracle"] = owner._finalizer.alive
            if path.exists():
                item["files_at_oracle"] = sorted(p.name for p in path.iterdir())
                shutil.copytree(path, directory / "retained-temporary", dirs_exist_ok=False)
            if owner is not None:
                # First explicit test disposal, AFTER the independent snapshot.
                # cleanup() disarms this test object's finalizer normally.
                owner.cleanup()
                item["test_disposal_after_oracle"] = not path.exists()
            elif path.exists():
                shutil.rmtree(path)
        (directory / "storage-oracles.json").write_text(json.dumps({"injections": injections, "complete_writes": complete_writes}, indent=2), encoding="utf8")


class StorageCleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="sef-storage-test-")
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        support.git(self.root, "init", "-q")
        support.git(self.root, "-c", "user.name=Synthetic", "-c", "user.email=synthetic@example.invalid", "commit", "--allow-empty", "-qm", "fixture")
        self.patch = mock.patch.object(cert, "REPO_ROOT", self.root)
        self.patch.start()
        cert.ACTIVE_EVIDENCE = None
        cert.PROCESS_RECORDS.clear()
        cert.RESERVATIONS.clear()

    def tearDown(self):
        self.patch.stop()
        destination = os.environ.get("SEF_STORAGE_CLEANUP_ARTIFACT_DIR")
        if destination:
            target = Path(destination) / self._testMethodName
            shutil.copytree(self.tmp.name, target, ignore=shutil.ignore_patterns(".git"))
        self.tmp.cleanup()

    def run_cli(self, mode="keyboard", target="gate", fault="after_removal"):
        directory = Path(self.tmp.name) / (mode + "_" + target + "_" + fault)
        directory.mkdir()
        command = [sys.executable, "-B", str(Path(__file__).resolve()), "--probe", mode, target, str(self.root), str(directory), fault]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        (directory / "external.json").write_text(json.dumps({"exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr}, indent=2), encoding="utf8")
        observed = json.loads((directory / "observations.json").read_text(encoding="utf8"))
        oracle = json.loads((directory / "storage-oracles.json").read_text(encoding="utf8"))
        summary_file = directory / "bundle/summary.json"
        summary = json.loads(summary_file.read_text(encoding="utf8")) if summary_file.exists() else observed["summary_in_memory"]
        pids = {r[k] for r in observed["processes"] for k in ("pid", "launcher_pid") if r.get(k)}
        if observed["child_pid"]:
            pids.add(observed["child_pid"])
        alive_after = {pid: support.alive(pid) for pid in pids}
        (directory / "external-liveness.json").write_text(json.dumps(alive_after, indent=2), encoding="utf8")
        self.assertFalse(any(alive_after.values()), alive_after)
        self.assertTrue(oracle["complete_writes"])
        self.assertFalse(any(item["exists"] for item in oracle["complete_writes"]))
        if fault == "none":
            self.assertEqual([], oracle["injections"])
        else:
            self.assertEqual(1, len(oracle["injections"]))
        records = [r for r in observed["processes"] if r.get("result") == "INTERRUPTED" or "CLI_BEFORE_INTERRUPT" in r.get("stdout", "")]
        record = records[0]
        return result, summary, observed, oracle, record

    def assert_cancel(self, mode, target, fault):
        result, summary, observed, oracle, record = self.run_cli(mode, target, fault)
        self.assertEqual(8 if mode == "nonzero" else 130, result.returncode, result.stderr)
        self.assertEqual("FAIL", summary["LOCAL_CERTIFICATION"])
        self.assertFalse(summary["release_clean_certification"])
        self.assertEqual("INTERRUPTED", record["result"])
        self.assertIsNone(record["observed_exit_code"])
        self.assertEqual("COMPLETE", record["process_cleanup"])
        self.assertEqual("COMPLETE" if fault == "none" else "FAILED", record["temporary_cleanup"])
        self.assertEqual(record["temporary_cleanup"], record["cleanup"])
        if target == "gate":
            self.assertTrue(observed["ready"] and observed["executed"])
            self.assertIn("CLI_BEFORE_INTERRUPT", record["stdout"])
            self.assertEqual(["observed_gate"], [step["name"] for step in summary["steps"]])
        else:
            self.assertFalse(observed["executed"])
            self.assertEqual([], summary["steps"])
        self.assertIn("later", summary["not_started_steps"])
        if fault != "none":
            details = record["temporary_cleanup_exception"]
            self.assertEqual(32, details["winerror"])
            self.assertEqual("PermissionError", details["type"])
            self.assertEqual(str(Path(oracle["injections"][0]["path"]) / "stderr"), details["filename"])
            self.assertIn("SYNTHETIC_STORAGE_CLEANUP", details["traceback"])
            self.assertIn("INTERRUPTED_WITH_INFRASTRUCTURE_ERROR", summary["infrastructure_errors"])
        return record, oracle

    def test_gate_cancellation_with_storage_error(self):
        for mode in ("keyboard", "zero", "none", "nonzero"):
            with self.subTest(mode=mode):
                self.assert_cancel(mode, "gate", "after_removal")

    def test_optional_git_cancellation_with_storage_error(self):
        for mode in ("keyboard", "zero", "none", "nonzero"):
            with self.subTest(mode=mode):
                self.assert_cancel(mode, "optional_git", "after_removal")

    def test_cancellation_positive_controls(self):
        for mode in ("keyboard", "zero", "none", "nonzero"):
            with self.subTest(mode=mode):
                self.assert_cancel(mode, "gate", "none")

    def test_successful_command_with_storage_error_is_not_pass(self):
        result, summary, _, _, record = self.run_cli("normal")
        self.assertEqual(2, result.returncode)
        self.assertEqual("FAIL", summary["LOCAL_CERTIFICATION"])
        self.assertFalse(summary["release_clean_certification"])
        self.assertEqual(0, summary["gate_failure_count"])
        self.assertEqual(0, record["observed_exit_code"])
        self.assertEqual("EXITED", record["result"])
        self.assertEqual("COMPLETE", record["process_cleanup"])
        self.assertEqual("FAILED", record["cleanup"])
        self.assertEqual(125, record["conventional_exit_code"])
        self.assertEqual(["later"], summary["not_started_steps"])

    def test_successful_control_remains_pass(self):
        result, summary, _, _, record = self.run_cli("normal", fault="none")
        self.assertEqual(0, result.returncode)
        self.assertEqual("PASS", summary["LOCAL_CERTIFICATION"])
        self.assertEqual("COMPLETE", record["cleanup"])

    def test_residue_is_observed_not_deleted_or_certified_by_recovery(self):
        record, oracle = self.assert_cancel("keyboard", "gate", "before_removal")
        self.assertTrue(oracle["injections"][0]["exists_at_oracle"])
        self.assertTrue(record["temporary_directory_exists_after_cleanup"])
        self.assertIn("stderr", oracle["injections"][0]["files_at_oracle"])
        self.assertTrue(oracle["injections"][0]["test_owner_retained_at_oracle"])
        self.assertTrue(oracle["injections"][0]["finalizer_alive_at_oracle"])
        self.assertTrue(oracle["injections"][0]["test_disposal_after_oracle"])

    def test_cleanup_and_journal_failures_are_both_preserved(self):
        record, _ = self.assert_cancel("nonzero", "gate", "journal")
        self.assertIn("SYNTHETIC_CLEANUP_JOURNAL", record["cleanup_journal_exception"]["traceback"])
        self.assertIn("SYNTHETIC_STORAGE_CLEANUP", record["temporary_cleanup_exception"]["traceback"])

    def test_timeout_retains_partial_output_when_storage_fails(self):
        ready = Path(self.tmp.name) / "timeout-ready"
        command = [sys.executable, "-B", "-c", "import time;from pathlib import Path;"
                   "print('STORAGE_TIMEOUT_READY',flush=True);"
                   f"Path({str(ready)!r}).write_text('ready');time.sleep(30)"]
        original_exit = tempfile.TemporaryDirectory.__exit__
        original_wait = subprocess.Popen.wait
        observed_ready = []
        def wait(process, *args, **kwargs):
            if not observed_ready:
                support.wait_for_file(ready)
                observed_ready.append(process.pid)
                # Exercise a real timeout only after child readiness is observed.
                return original_wait(process, timeout=.1)
            return original_wait(process, *args, **kwargs)
        def fail(temporary, *args):
            original_exit(temporary, *args)
            raise PermissionError("SYNTHETIC_TIMEOUT_CLEANUP")
        with mock.patch.object(subprocess.Popen, "wait", wait), mock.patch.object(tempfile.TemporaryDirectory, "__exit__", fail):
            with self.assertRaisesRegex(PermissionError, "SYNTHETIC_TIMEOUT_CLEANUP"):
                cert._run(command)
        record = cert.PROCESS_RECORDS[-1]
        self.assertTrue(observed_ready)
        self.assertEqual("TIMEOUT", record["result"])
        self.assertIsNone(record["observed_exit_code"])
        self.assertEqual(124, record["conventional_exit_code"])
        self.assertEqual("COMPLETE", record["process_cleanup"])
        self.assertEqual("FAILED", record["temporary_cleanup"])
        self.assertIn("STORAGE_TIMEOUT_READY", record["stdout"])
        self.assertFalse(support.alive(record["pid"]))
        (Path(self.tmp.name) / "timeout-observation.json").write_text(json.dumps(record, indent=2), encoding="utf8")

    def test_failed_command_retains_observed_exit_when_cleanup_fails(self):
        original_exit = tempfile.TemporaryDirectory.__exit__
        def fail(temporary, *args):
            original_exit(temporary, *args)
            raise PermissionError("SYNTHETIC_FAILED_GATE_CLEANUP")
        with mock.patch.object(tempfile.TemporaryDirectory, "__exit__", fail):
            with self.assertRaisesRegex(PermissionError, "SYNTHETIC_FAILED_GATE_CLEANUP"):
                cert._run([sys.executable, "-B", "-c", "raise SystemExit(7)"])
        record = cert.PROCESS_RECORDS[-1]
        self.assertEqual(7, record["observed_exit_code"])
        self.assertEqual("EXITED", record["result"])
        self.assertEqual("FAILED", record["cleanup"])
        self.assertFalse(support.alive(record["pid"]))
        (Path(self.tmp.name) / "observation.json").write_text(json.dumps(record, indent=2), encoding="utf8")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--probe":
        cli_probe(*sys.argv[2:])
    else:
        unittest.main()
