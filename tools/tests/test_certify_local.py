"""Focused F-04 fixtures. Never invokes a real certification profile recursively."""
from __future__ import annotations

import contextlib
import ctypes
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tools/skill_enforcement/certify_local.py"
spec = importlib.util.spec_from_file_location("certifier_under_test", SOURCE)
cert = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cert
spec.loader.exec_module(cert)


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True, timeout=10).stdout.rstrip("\r\n")


def alive(pid):
    """External OS oracle, independent of certifier cleanup/clean properties."""
    if os.name == "nt":
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        k.OpenProcess.restype = ctypes.c_void_p
        k.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
        k.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
        k.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = k.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        try:
            code = ctypes.c_uint32()
            if not k.GetExitCodeProcess(handle, ctypes.byref(code)):
                raise ctypes.WinError(ctypes.get_last_error())
            return code.value == 259
        finally:
            k.CloseHandle(handle)
    proc = Path(f"/proc/{pid}/stat")
    if proc.exists() and proc.read_text().rsplit(")", 1)[1].split()[0] == "Z":
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


class CertifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="sef-cert-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        git(self.root, "init", "-q")
        (self.root / "tracked.txt").write_text("base\n", encoding="utf8")
        git(self.root, "add", "tracked.txt")
        git(self.root, "-c", "user.name=Synthetic", "-c", "user.email=synthetic@example.invalid", "commit", "-qm", "fixture")
        self.sha = git(self.root, "rev-parse", "HEAD")
        self.out = Path(self.tmp.name) / "evidence"
        self.patch = mock.patch.object(cert, "REPO_ROOT", self.root)
        self.patch.start(); self.addCleanup(self.patch.stop)
        cert.ACTIVE_EVIDENCE = None
        cert.PROCESS_RECORDS.clear()
        cert.RESERVATIONS.clear()
        cert.GIT_TIMEOUT_SECONDS = 5
        cert.STEP_TIMEOUT_SECONDS = 5
        self.good = cert.GitState(self.sha, None, None, None, "")
        self.plan = [("synthetic", [sys.executable, "-B", "-c", "print('synthetic-ok')"])]

    def tearDown(self):
        # Optional external campaign artifacts; default test runs remain isolated.
        target = os.environ.get("SEF_CERTIFIER_TEST_ARTIFACT_DIR")
        if target:
            destination = Path(target) / self._testMethodName
            destination.mkdir(parents=True, exist_ok=False)
            (destination / "processes.json").write_text(json.dumps(cert.PROCESS_RECORDS, indent=2), encoding="utf8")
            for entry in Path(self.tmp.name).iterdir():
                if entry.is_dir():
                    shutil.copytree(entry, destination / entry.name, ignore=shutil.ignore_patterns(".git"))
                else:
                    shutil.copy2(entry, destination / entry.name)
            oracle = {"head": git(self.root, "rev-parse", "HEAD"), "status": git(self.root, "status", "--porcelain", "--untracked-files=all")}
            (destination / "external_git.json").write_text(json.dumps(oracle, indent=2), encoding="utf8")

    def run_main(self, flags=(), plan=None):
        with mock.patch.dict(cert.PROFILE_STEPS, {"se02": self.plan if plan is None else plan}), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return cert.main(["--profile", "se02", "--evidence-dir", str(self.out), *flags])

    def summary(self):
        return json.loads((self.out / "summary.json").read_text(encoding="utf8"))

    def test_initial_head_and_status_fail_before_mutable_step(self):
        for failed in ("head", "status"):
            with self.subTest(failed=failed):
                cert.PROCESS_RECORDS.clear()
                def fake(command):
                    if command[1] == "rev-parse": return (1, "failure", 0) if failed == "head" else (0, self.sha, 0)
                    if "status" in command: return (1, "failure", 0) if failed == "status" else (0, "", 0)
                    return 0, "", 0
                with mock.patch.object(cert, "_run", side_effect=fake) as calls:
                    self.assertNotEqual(0, self.run_main(["--no-evidence", "--allow-dirty"]))
                    self.assertTrue(all(c.args[0][0] == "git" for c in calls.call_args_list))

    def test_invalid_head_status_and_decoding_fail_closed(self):
        for head, status in [("bogus", ""), (self.sha, "not-porcelain")]:
            def fake(*args):
                if args[0] == "rev-parse" and args[-1] == "HEAD": return head
                if "status" in args: return status
                return None
            with mock.patch.object(cert, "_git_output", side_effect=fake):
                self.assertFalse(cert._git_state().valid)
        cert._run([sys.executable, "-c", "import sys;sys.stdout.buffer.write(b'\\xff')"])
        self.assertFalse(cert.PROCESS_RECORDS[-1]["utf8_valid"])
        def bad_decode(command):
            cert.PROCESS_RECORDS.append({"utf8_valid": False, "stdout": self.sha})
            return 0, self.sha, 0
        with mock.patch.object(cert, "_run", side_effect=bad_decode):
            self.assertIsNone(cert._git_output("rev-parse", "HEAD"))

    def test_final_unobservable_head_and_status_block(self):
        for error in ("HEAD_UNOBSERVABLE_OR_INVALID", "STATUS_UNOBSERVABLE"):
            bad = cert.GitState(self.sha, None, None, None, "", (error,))
            with mock.patch.object(cert, "_git_state", side_effect=[self.good, bad]):
                self.assertNotEqual(0, self.run_main(["--no-evidence"]))

    def test_head_change_detected_with_green_steps(self):
        code = "import subprocess;subprocess.run(['git','-c','user.name=Synthetic','-c','user.email=synthetic@example.invalid','commit','--allow-empty','-qm','change'],check=True)"
        self.assertNotEqual(0, self.run_main(plan=[("change", [sys.executable, "-c", code])]))
        self.assertNotEqual(self.sha, git(self.root, "rev-parse", "HEAD"))
        self.assertIn("HEAD_CHANGED", self.summary()["infrastructure_errors"])
        self.assertEqual(0, self.summary()["failure_count"])

    def test_final_dirty_outside_derived_detected(self):
        self.assertNotEqual(0, self.run_main(plan=[("dirty", [sys.executable, "-c", "from pathlib import Path;Path('foreign.txt').write_text('dirty')"])]))
        self.assertIn("foreign.txt", git(self.root, "status", "--porcelain"))
        self.assertIn("WORKTREE_NOT_CLEAN", self.summary()["infrastructure_errors"])

    def test_detached_no_origin_new_bundle_positive_external_oracle(self):
        git(self.root, "checkout", "--detach", "-q")
        self.assertEqual(0, self.run_main())
        data = self.summary()
        self.assertEqual("PASS", data["LOCAL_CERTIFICATION"])
        self.assertTrue(data["release_clean_certification"])
        self.assertEqual(self.sha, git(self.root, "rev-parse", "HEAD"))
        self.assertEqual("", git(self.root, "status", "--porcelain", "--untracked-files=all"))
        self.assertEqual(["synthetic"], data["expected_steps"])
        self.assertEqual([], data["not_started_steps"])
        self.assertIn("synthetic-ok", (self.out / "logs/01_synthetic.log").read_text())
        records = json.loads((self.out / "processes.json").read_text())
        self.assertTrue(all(r["ended_at_utc"] and r["cleanup"] == "COMPLETE" for r in records))
        self.assertEqual(1, len(json.loads((self.out / "commands.json").read_text())))

    def test_existing_empty_and_populated_evidence_never_changed(self):
        self.out.mkdir()
        self.assertNotEqual(0, self.run_main())
        self.assertEqual([], list(self.out.iterdir()))
        sentinel = self.out / "summary.json"; sentinel.write_bytes(b"SEALED")
        self.assertNotEqual(0, self.run_main())
        self.assertEqual(b"SEALED", sentinel.read_bytes())
        self.assertEqual([sentinel], list(self.out.iterdir()))

    def test_evidence_alias_parent_and_repository_are_rejected(self):
        sealed = Path(self.tmp.name) / "sealed"; sealed.mkdir()
        sentinel = sealed / "sentinel"; sentinel.write_bytes(b"SEALED")
        alias = Path(self.tmp.name) / "alias"
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "mklink", "/J", str(alias), str(sealed)], capture_output=True, check=True, timeout=10)
        else:
            alias.symlink_to(sealed, target_is_directory=True)
        try:
            for target in (alias, alias / "new", self.root / "inside"):
                with self.subTest(target=target), self.assertRaises(ValueError):
                    cert._resolve_evidence_dir(str(target), self.sha)
            self.assertEqual(b"SEALED", sentinel.read_bytes())
            self.assertEqual([sentinel], list(sealed.iterdir()))
        finally:
            if os.name == "nt": alias.rmdir()
            else: alias.unlink()

    def test_reservation_required_and_default_unique(self):
        self.out.mkdir()
        with self.assertRaises(OSError): cert._persist_bundle(self.out, {}, [])
        self.assertNotEqual(cert._resolve_evidence_dir(None, self.sha), cert._resolve_evidence_dir(None, self.sha))

    def test_two_processes_race_only_one_reserves(self):
        source = "import importlib.util,sys,time,pathlib;s=importlib.util.spec_from_file_location('c',sys.argv[1]);m=importlib.util.module_from_spec(s);sys.modules['c']=m;s.loader.exec_module(m);p=pathlib.Path(sys.argv[2]);\ntry:m._reserve_evidence(p)\nexcept FileExistsError:sys.exit(3)\n(p/'winner').write_text(sys.argv[3]);time.sleep(.1)"
        processes = [subprocess.Popen([sys.executable, "-B", "-c", source, str(SOURCE), str(self.out), str(i)], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for i in range(2)]
        outputs = [p.communicate(timeout=10) for p in processes]
        self.assertEqual([0, 3], sorted(p.returncode for p in processes), outputs)
        self.assertEqual(1, len(list(self.out.iterdir())))
        self.assertIn((self.out / "winner").read_text(), ("0", "1"))

    def test_failure_is_observed_exit_and_other_gates_still_run(self):
        plan = [("bad", [sys.executable, "-c", "import sys;print('bad-output');sys.exit(7)"]), *self.plan]
        self.assertNotEqual(0, self.run_main(plan=plan))
        data = self.summary(); self.assertEqual(1, data["failure_count"])
        self.assertEqual(7, data["steps"][0]["process"]["observed_exit_code"])
        self.assertEqual([], data["not_started_steps"])

    def test_start_error_stops_and_records_unstarted_steps(self):
        self.assertNotEqual(0, self.run_main(plan=[("missing", [str(self.root / "missing-executable")]), *self.plan]))
        data = self.summary(); self.assertEqual(["synthetic"], data["not_started_steps"])
        self.assertIsNone(data["steps"][0]["process"]["observed_exit_code"])

    def test_timeout_real_parent_child_external_oracle_and_partial_streams(self):
        pidfile = Path(self.tmp.name) / "pids.json"
        source = "import json,os,subprocess,sys,time,pathlib;p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']);pathlib.Path(sys.argv[1]).write_text(json.dumps([os.getpid(),p.pid]));print('partial-out',flush=True);print('partial-err',file=sys.stderr,flush=True);time.sleep(30)"
        cert.STEP_TIMEOUT_SECONDS = 1.5
        started = time.monotonic()
        code, output, _ = cert._run([sys.executable, "-B", "-c", source, str(pidfile)])
        self.assertEqual(124, code)
        self.assertLess(time.monotonic() - started, 12)
        self.assertIn("partial-out", output); self.assertIn("partial-err", output)
        record = cert.PROCESS_RECORDS[-1]
        self.assertEqual("TIMEOUT", record["result"])
        self.assertIsNone(record["observed_exit_code"])
        self.assertEqual("COMPLETE", record["cleanup"])
        pids = json.loads(pidfile.read_text())
        self.assertEqual(2, len(pids))
        self.assertTrue(all(not alive(pid) for pid in pids), pids)
        print("TIMEOUT_ORACLE", json.dumps({"pids": pids, "alive_after": [alive(p) for p in pids], "process": record}))

    def test_timeout_main_does_not_promote_absent_gate(self):
        self.assertNotEqual(0, self.run_main(["--step-timeout-seconds", "0.5"], plan=[("timeout", [sys.executable, "-c", "import time;print('started',flush=True);time.sleep(30)"]), *self.plan]))
        data = self.summary()
        self.assertEqual(["synthetic"], data["not_started_steps"])
        self.assertEqual("TIMEOUT", data["steps"][0]["process"]["result"])

    def test_keyboard_interrupt_cleanup_and_output(self):
        original = subprocess.Popen.wait
        first = True
        def interrupt(process, *args, **kwargs):
            nonlocal first
            if first:
                first = False; time.sleep(.35); raise KeyboardInterrupt()
            return original(process, *args, **kwargs)
        with mock.patch.object(subprocess.Popen, "wait", interrupt):
            code, output, _ = cert._run([sys.executable, "-c", "import time;print('before-interrupt',flush=True);time.sleep(30)"])
        self.assertEqual(130, code)
        self.assertIn("before-interrupt", output)
        record = cert.PROCESS_RECORDS[-1]
        self.assertEqual("INTERRUPTED", record["result"])
        self.assertFalse(alive(record["pid"]))

    def test_system_exit_not_swallowed(self):
        original = subprocess.Popen.wait
        first = True
        def interrupt(process, *args, **kwargs):
            nonlocal first
            if first: first = False; raise SystemExit(8)
            return original(process, *args, **kwargs)
        with mock.patch.object(subprocess.Popen, "wait", interrupt), self.assertRaises(SystemExit):
            cert._run([sys.executable, "-c", "import time;time.sleep(30)"])
        self.assertEqual("INTERRUPTED", cert.PROCESS_RECORDS[-1]["result"])

    def test_partial_ci_flags_no_evidence_diagnostic(self):
        (self.root / "dirty").write_text("diagnostic")
        self.assertEqual(0, self.run_main(["--allow-dirty", "--skip-render", "--no-evidence"]))
        self.assertFalse(self.out.exists())
        self.assertTrue(cert._scope("se02", True, True).startswith("DIAGNOSTIC_"))
        self.assertFalse(cert._scope("se02", True).startswith("FULL_"))

    def test_empty_missing_duplicate_steps_never_full(self):
        step = cert.StepResult("synthetic", ["true"], 0, 0, "PASS", "")
        for results, expected in [([], []), ([], ["synthetic"]), ([step, step], ["synthetic"]), ([step], ["synthetic", "missing"])]:
            data = cert._build_summary(profile="se02", scope="FULL_SE02_LOCAL", before=self.good, after=self.good, results=results, expected_steps=expected)
            self.assertEqual("FAIL", data["LOCAL_CERTIFICATION"])
        self.assertNotEqual(0, self.run_main(["--no-evidence"], plan=[]))

    def test_profiles_preserve_gates_and_add_only_dedicated_suite(self):
        for profile in ("se02", "se03", "se04", "se05", "se06", "se07"):
            names = [n for n, _ in cert.PROFILE_STEPS[profile]]
            for name in ("contract_v0_1", "se01_regression", "assistant_structure", "render_simulado", "render_diff", "readme_snapshot"):
                self.assertIn(name, names)
            self.assertEqual(len(names), len(set(names)))
        self.assertIn("certifier_regression", [n for n, _ in cert.PROFILE_STEPS["se07"]])
        self.assertNotIn("certifier_regression", [n for n, _ in cert.PROFILE_STEPS["se06"]])

    def test_persistence_failure_never_leaves_pass_summary(self):
        original = cert._write_json
        def fail(path, payload):
            if path.name == "environment.json": raise OSError("synthetic disk failure")
            return original(path, payload)
        built = []
        original_summary = cert._build_summary
        def capture(**kwargs):
            data = original_summary(**kwargs); built.append(data); return data
        with mock.patch.object(cert, "_write_json", side_effect=fail), mock.patch.object(cert, "_build_summary", side_effect=capture):
            self.assertNotEqual(0, self.run_main())
        self.assertFalse((self.out / "summary.json").exists())
        self.assertEqual(len(built[0]["infrastructure_errors"]), built[0]["infrastructure_error_count"])
        self.assertEqual("FAIL", built[0]["LOCAL_CERTIFICATION"])
        self.assertFalse(built[0]["release_clean_certification"])

    def test_cleanup_failure_cannot_pass(self):
        metadata = {"result": "EXITED", "cleanup": "FAILED"}
        step = cert.StepResult("synthetic", ["true"], 0, 0, "PASS", "", process=metadata)
        data = cert._build_summary(profile="se02", scope="FULL_SE02_LOCAL", before=self.good, after=self.good, results=[step], expected_steps=["synthetic"])
        self.assertEqual("FAIL", data["LOCAL_CERTIFICATION"])

    def test_git_timeout_budget_is_applied_and_blocks_observation(self):
        original = subprocess.Popen.wait
        first = True
        observed_timeouts = []
        def expire(process, *args, **kwargs):
            nonlocal first
            if first:
                first = False
                observed_timeouts.append(kwargs["timeout"])
                raise subprocess.TimeoutExpired(process.args, kwargs["timeout"])
            return original(process, *args, **kwargs)
        cert.GIT_TIMEOUT_SECONDS = .4
        with mock.patch.object(subprocess.Popen, "wait", expire):
            self.assertIsNone(cert._git_output("rev-parse", "HEAD"))
        self.assertLessEqual(observed_timeouts[0], .4)
        self.assertEqual("TIMEOUT", cert.PROCESS_RECORDS[-1]["result"])
        self.assertIsNone(cert.PROCESS_RECORDS[-1]["observed_exit_code"])

    def test_cleanup_os_error_real_boundary_fails(self):
        if os.name == "nt":
            target = mock.patch.object(cert._WindowsJob, "terminate", side_effect=OSError("injected cleanup failure"))
        else:
            target = mock.patch.object(cert, "_posix_group_alive", side_effect=OSError("injected cleanup failure"))
        with target:
            code, _, _ = cert._run([sys.executable, "-c", "print('done')"])
        self.assertNotEqual(0, code)
        self.assertEqual("FAILED", cert.PROCESS_RECORDS[-1]["cleanup"])

    def test_evidence_replaced_and_hardlink_json_fail_closed(self):
        cert._reserve_evidence(self.out)
        old = self.out.with_name("old-evidence")
        self.out.rename(old); self.out.mkdir()
        with self.assertRaises(OSError): cert._persist_bundle(self.out, {}, [])
        sentinel = Path(self.tmp.name) / "sealed.json"; sentinel.write_bytes(b"SEALED")
        linked = self.out / "summary.json"
        os.link(sentinel, linked)
        with self.assertRaises(OSError): cert._write_json(linked, {"changed": True})
        self.assertEqual(b"SEALED", sentinel.read_bytes())

    @unittest.skipUnless(os.name == "nt", "Windows launcher metadata boundary")
    def test_truncated_child_metadata_preserves_streams_and_fails(self):
        original = Path.read_text
        def truncate(path, *args, **kwargs):
            if path.name == "child.json": return "{"
            return original(path, *args, **kwargs)
        with mock.patch.object(Path, "read_text", truncate):
            code, output, _ = cert._run([sys.executable, "-c", "print('before-metadata-read')"])
        self.assertEqual(125, code)
        self.assertIn("before-metadata-read", output)
        self.assertIn("metadata_error", cert.PROCESS_RECORDS[-1])
        self.assertIsNone(cert.PROCESS_RECORDS[-1]["observed_exit_code"])

    def test_interrupt_optional_git_stops_before_mutable_gate(self):
        original = cert._run
        calls = []
        def interrupt_branch(command):
            calls.append(list(command))
            if command[:2] == ["git", "branch"]:
                cert.PROCESS_RECORDS.append({"command": list(command), "result": "INTERRUPTED", "cleanup": "COMPLETE", "utf8_valid": True, "stdout": "", "stderr": "", "observed_exit_code": None})
                return 130, "", 0
            return original(command)
        with mock.patch.object(cert, "_run", side_effect=interrupt_branch):
            self.assertEqual(130, self.run_main(["--no-evidence"]))
        self.assertTrue(all(command[0] == "git" for command in calls))

    def test_timeout_configuration_positive_finite_only(self):
        for value in ("0", "-1", "nan", "inf"):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                cert.main(["--no-evidence", "--step-timeout-seconds", value])


if __name__ == "__main__":
    unittest.main()
