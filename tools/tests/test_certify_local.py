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


def wait_for_file(path, seconds=5):
    """Readiness is an observed event, never an elapsed-time assumption."""
    deadline = time.monotonic() + seconds
    while not path.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError(f"READY_NOT_OBSERVED: {path.name}")
        time.sleep(.01)


def main_cli_probe(mode, target, root, directory):
    """Subprocess entry point: main's SystemExit deliberately remains uncaught."""
    directory = Path(directory)
    ready, executed = directory / "ready", directory / "executed"
    code = ("import os,time;from pathlib import Path;"
            f"Path({str(executed)!r}).write_text(str(os.getpid()));"
            "print('CLI_BEFORE_INTERRUPT',flush=True);"
            f"Path({str(ready)!r}).write_text('ready');"
            + ("time.sleep(30)" if mode != "normal" and target != "finalization" else ""))
    command = [sys.executable, "-B", "-c", code]
    cert.REPO_ROOT = Path(root)
    cert.PROFILE_STEPS["se02"] = [("observed_gate", command), ("later", [sys.executable, "-c", "print('later')"])]
    requested = ["git", "branch", "--show-current"] if target == "optional_git" else command
    original_wait = subprocess.Popen.wait
    original_write, original_summary = cert._write_json, cert._build_summary
    injected = []
    built = []
    def cancel():
        if mode == "keyboard": raise KeyboardInterrupt()
        raise SystemExit({"zero": 0, "none": None, "nonzero": 8}[mode])
    def write(path, payload):
        if target == "finalization" and path.name == "environment.json" and not injected:
            injected.append({"boundary": path.name}); cancel()
        return original_write(path, payload)
    def capture(**kwargs):
        data = original_summary(**kwargs); built.append(data); return data
    def interrupt(process, *args, **kwargs):
        # On Windows process.args names the Python launcher even for Git.
        # Select the requested invocation, not the launcher's executable name.
        record = next((r for r in reversed(cert.PROCESS_RECORDS)
                       if r.get("launcher_pid", r.get("pid")) == process.pid), None)
        if target != "finalization" and mode != "normal" and not injected and record and record["command"] == requested:
            injected.append({"requested_argv": list(record["command"]), "supervised_pid": process.pid})
            if target == "gate":
                wait_for_file(ready)
            else:
                original_wait(process, timeout=5)
            cancel()
        return original_wait(process, *args, **kwargs)
    with mock.patch.object(subprocess.Popen, "wait", interrupt), mock.patch.object(cert, "_write_json", side_effect=write), mock.patch.object(cert, "_build_summary", side_effect=capture):
        try:
            raise SystemExit(cert.main(["--profile", "se02", "--evidence-dir", str(directory / "bundle")]))
        finally:
            (directory / "observations.json").write_text(json.dumps({
                "injected": injected, "processes": cert.PROCESS_RECORDS,
                "executed": executed.exists(), "ready": ready.exists(),
                "child_pid": int(executed.read_text()) if executed.exists() else None,
                "summary_in_memory": built[-1] if built else None,
            }, indent=2), encoding="utf8")


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
        sentinel = Path(self.tmp.name) / "later-not-executed"
        command = [str(self.root / "missing-executable")]
        later = [sys.executable, "-c", f"from pathlib import Path;Path({str(sentinel)!r}).touch()"]
        self.assertNotEqual(0, self.run_main(plan=[("missing", command), ("synthetic", later)]))
        data = self.summary()
        self.assertFalse(sentinel.exists())
        self.assertEqual(["missing"], [s["name"] for s in data["steps"]])
        self.assertEqual([{"name": "missing", "command": command}], json.loads((self.out / "commands.json").read_text()))
        process = data["steps"][0]["process"]
        self.assertIsNone(process["observed_exit_code"])
        self.assertIsNone(process["pid"], "a Windows launcher is not the requested command")
        if process.get("launcher_pid"): self.assertFalse(alive(process["launcher_pid"]))
        self.assertEqual(["missing", "synthetic"], data["not_started_steps"])
        self.assertEqual(0, data["gate_failure_count"])

    @unittest.skipUnless(os.name == "nt", "Windows launcher metadata boundary")
    def test_main_missing_child_metadata_is_not_proof_of_no_start(self):
        marker = Path(self.tmp.name) / "metadata-gate-executed"
        command = [sys.executable, "-B", "-c",
                   f"import os;from pathlib import Path;Path({str(marker)!r}).write_text(str(os.getpid()));print('METADATA_GATE_EXECUTED',flush=True)"]
        original = Path.read_text
        injected = []
        def missing(path, *args, **kwargs):
            if path.name == "child.json" and cert.PROCESS_RECORDS[-1]["command"] == command:
                injected.append(str(path)); return "{}"
            return original(path, *args, **kwargs)
        with mock.patch.object(Path, "read_text", missing):
            self.assertNotEqual(0, self.run_main(plan=[("metadata_gate", command), *self.plan]))
        self.assertTrue(injected)
        self.assertTrue(marker.exists(), "external execution oracle must fire")
        self.assertFalse(alive(int(marker.read_text())))
        data = self.summary()
        self.assertEqual("FAIL", data["LOCAL_CERTIFICATION"])
        self.assertEqual(["metadata_gate"], [s["name"] for s in data["steps"]])
        self.assertEqual(["synthetic"], data["not_started_steps"], "missing metadata cannot prove no start")
        self.assertEqual(["metadata_gate"], data.get("unknown_start_steps", []))
        process = data["steps"][0]["process"]
        self.assertIsNone(process["pid"])
        self.assertIsNone(process["observed_exit_code"])
        self.assertIn("metadata_error", process)
        self.assertFalse(alive(process["launcher_pid"]))
        self.assertEqual([{"name": "metadata_gate", "command": command}], json.loads((self.out / "commands.json").read_text()))

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

    def test_cleanup_pre_remove_observation_is_diagnostic_only(self):
        directory = Path(self.tmp.name) / "cleanup-observation"
        directory.mkdir()
        (directory / "stderr").write_bytes(b"")
        record = {
            "result": "INFRASTRUCTURE_ERROR",
            "cleanup": "COMPLETE",
            "process_cleanup": "COMPLETE",
            "pid": 123,
            "launcher_pid": 456,
            "observed_exit_code": None,
            "exit_after_cleanup": 1,
            "command_started": True,
            "metadata_error": None,
            "start_error": None,
            "utf8_valid": True,
        }
        observation = cert._temporary_cleanup_observation(record, directory)
        self.assertTrue(observation["exists"])
        self.assertEqual(["stderr"], observation["entries"])
        self.assertEqual("COMPLETE", observation["process_cleanup"])
        self.assertEqual(123, observation["pid"])
        self.assertEqual(456, observation["launcher_pid"])
        self.assertTrue(observation["command_started"])
        self.assertTrue(observation["utf8_valid"])
        self.assertIsNone(observation["metadata_error"])
        self.assertEqual("COMPLETE", record["cleanup"], "telemetry must not mutate verdict state")

    @unittest.skipIf(os.name == "nt", "non-Windows loader regression")
    def test_native_observer_providers_load_from_sibling_when_file_loaded(self):
        observation = cert._restart_manager_file_users([Path(self.tmp.name) / "unused"])
        self.assertEqual("NOT_APPLICABLE_NON_WINDOWS", observation["status"])
        owners = cert._file_process_ids_using_file(Path(self.tmp.name) / "unused")
        self.assertEqual("NOT_APPLICABLE_NON_WINDOWS", owners["status"])

    def test_winerror32_failure_observer_is_single_shot_and_diagnostic_only(self):
        directory = Path(self.tmp.name) / "winerror32-observation"
        directory.mkdir()
        stderr = directory / "stderr"
        stdout = directory / "stdout"
        child = directory / "child.json"
        stderr.write_bytes(b"")
        stdout.write_bytes(b"partial")
        child.write_text('{"pid": 123}', encoding="utf-8")
        record = {"cleanup": "FAILED", "launcher_pid": 456, "pid": 123}
        error = PermissionError(13, "synthetic native sharing violation", str(stderr))
        error.winerror = 32
        file_calls = []
        owner_calls = []
        call_order = []
        pid_calls = []

        def users(paths):
            call_order.append("restart_manager")
            file_calls.append([str(path) for path in paths])
            return {"status": "MATCHES_REPORTED", "processes": [{"pid": 999}]}

        def owners(path):
            call_order.append("owner:" + Path(path).name)
            owner_calls.append(str(path))
            return {"status": "OBSERVED", "path": str(path),
                    "process_ids": [os.getpid(), 456, 123, 999]}

        def pid_state(pid):
            pid_calls.append(pid)
            return {"status": "OBSERVED", "running": False, "exit_code": 1}

        before = dict(record)
        observation = cert._windows_cleanup_failure_observation(
            record, directory, error,
            file_users_provider=users,
            file_process_ids_provider=owners,
            pid_state_provider=pid_state,
        )
        self.assertEqual(before, record, "observer must not mutate verdict state")
        self.assertEqual("OBSERVED_AFTER_NATIVE_WINERROR32", observation["status"])
        self.assertEqual("MATCHES_REPORTED", observation["restart_manager"]["status"])
        self.assertEqual([456, 123], pid_calls)
        self.assertEqual(1, len(file_calls))
        self.assertEqual([str(stderr), str(stdout), str(child)], file_calls[0])
        self.assertEqual([str(stderr), str(stdout), str(child)], owner_calls)
        self.assertEqual(
            ["owner:stderr", "restart_manager", "owner:stdout", "owner:child.json"],
            call_order,
        )
        self.assertEqual(
            "PRIORITY_FAILED_RESOURCE",
            observation["file_process_ids_using_file"][0]["observer_phase"],
        )
        self.assertGreaterEqual(
            observation["restart_manager"]["query_start_delta_from_cleanup_error_ns"],
            observation["file_process_ids_using_file"][0]["query_start_delta_from_cleanup_error_ns"],
        )
        owner_rows = observation["file_process_ids_using_file"][0]["relations"]
        self.assertIn({"pid": os.getpid(),
                       "relation": "OBSERVER_PID_QUERY_HANDLE_OR_EXISTING_HANDLE"}, owner_rows)
        self.assertIn({"pid": 456, "relation": "LAUNCHER_PID"}, owner_rows)
        self.assertIn({"pid": 123, "relation": "CHILD_PID"}, owner_rows)
        self.assertIn({"pid": 999, "relation": "OTHER_PID"}, owner_rows)

    def test_parent_streams_are_closed_before_temporary_directory_exit(self):
        code, output, _ = cert._run([sys.executable, "-B", "-c", "print('stream-boundary')"])
        self.assertEqual(0, code, output)
        streams = cert.PROCESS_RECORDS[-1]["parent_streams_before_temporary_exit"]
        self.assertTrue(streams["stdout_closed"])
        self.assertTrue(streams["stderr_closed"])
        self.assertIn("stdout", streams["stdout_name"])
        self.assertIn("stderr", streams["stderr_name"])

    def test_non_winerror32_does_not_invoke_native_failure_observer(self):
        directory = Path(self.tmp.name) / "non-winerror32"
        directory.mkdir()
        error = PermissionError(13, "different failure", str(directory / "stderr"))
        calls = []
        self.assertIsNone(cert._windows_cleanup_failure_observation(
            {"launcher_pid": 1, "pid": 2}, directory, error,
            file_users_provider=lambda paths: calls.append(paths),
            file_process_ids_provider=lambda path: calls.append(path),
            pid_state_provider=lambda pid: calls.append(pid),
        ))
        self.assertEqual([], calls)

    def test_winerror32_observer_errors_are_recorded_without_retry(self):
        directory = Path(self.tmp.name) / "observer-error"
        directory.mkdir()
        stderr = directory / "stderr"
        stderr.write_bytes(b"")
        error = PermissionError(13, "synthetic native sharing violation", str(stderr))
        error.winerror = 32
        calls = []

        def fail_users(paths):
            calls.append("rm")
            raise OSError("synthetic RM failure")

        def fail_owners(path):
            calls.append(("owners", str(path)))
            raise OSError("synthetic owner query failure")

        def fail_pid(pid):
            calls.append(("pid", pid))
            raise OSError("synthetic PID failure")

        observation = cert._windows_cleanup_failure_observation(
            {"launcher_pid": 7, "pid": 8}, directory, error,
            file_users_provider=fail_users,
            file_process_ids_provider=fail_owners,
            pid_state_provider=fail_pid,
        )
        self.assertEqual(["rm", ("owners", str(stderr)), ("pid", 7), ("pid", 8)], calls)
        self.assertEqual("UNOBSERVABLE", observation["restart_manager"]["status"])
        self.assertEqual("UNOBSERVABLE", observation["file_process_ids_using_file"][0]["status"])
        self.assertEqual("UNOBSERVABLE", observation["pid_states"]["launcher_pid"]["status"])
        self.assertEqual("UNOBSERVABLE", observation["pid_states"]["pid"]["status"])

    def test_keyboard_interrupt_cleanup_and_output(self):
        code, output, record = self.interrupt_fixture("after_output")
        self.assertEqual(130, code)
        self.assertIn("before-interrupt", output)
        self.assertEqual("INTERRUPTED", record["result"])

    def interrupt_fixture(self, phase):
        ready = Path(self.tmp.name) / "ready"
        started = Path(self.tmp.name) / "started"
        release = Path(self.tmp.name) / "release-never-created"
        source = ("import os,time;from pathlib import Path;"
                  f"Path({str(started)!r}).write_text(str(os.getpid()));\n")
        if phase == "after_output":
            source += f"print('before-interrupt',flush=True);Path({str(ready)!r}).write_text('ready');time.sleep(30)"
        else:
            source += f"while not Path({str(release)!r}).exists(): time.sleep(.01)\nprint('after-release',flush=True)"
        original = subprocess.Popen.wait
        first = True
        def interrupt(process, *args, **kwargs):
            nonlocal first
            if first:
                first = False
                wait_for_file(started)
                wait_for_file(ready, .3 if phase == "never_ready" else 5) if phase != "before_output" else None
                raise KeyboardInterrupt()
            return original(process, *args, **kwargs)
        try:
            with mock.patch.object(subprocess.Popen, "wait", interrupt):
                code, output, _ = cert._run([sys.executable, "-B", "-c", source])
        finally:
            # _run's finally must also clean up a failed readiness handshake.
            pids = [int(started.read_text())] if started.exists() else []
            pids += [r[k] for r in cert.PROCESS_RECORDS for k in ("pid", "launcher_pid") if r.get(k)]
            running = [pid for pid in set(pids) if alive(pid)]
            try:
                self.assertEqual([], running, "fixture left owned processes alive")
            finally:
                for pid in running: os.kill(pid, 9)
        record = cert.PROCESS_RECORDS[-1]
        self.assertEqual("COMPLETE", record["cleanup"])
        return code, output, record

    def test_keyboard_interrupt_before_first_output(self):
        code, output, record = self.interrupt_fixture("before_output")
        self.assertEqual(130, code)
        self.assertEqual("", output)
        self.assertEqual("INTERRUPTED", record["result"])

    def test_never_ready_has_finite_diagnostic_and_cleanup(self):
        started = time.monotonic()
        code, output, record = self.interrupt_fixture("never_ready")
        self.assertNotEqual(0, code)
        self.assertEqual("", output)
        self.assertIn("READY_NOT_OBSERVED", record["error"])
        self.assertLess(time.monotonic() - started, 12)

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

    @unittest.skipUnless(os.name == "nt", "Windows launcher metadata boundary")
    def test_missing_empty_or_invalid_child_metadata_cannot_pass(self):
        original_exists, original_read = Path.exists, Path.read_text
        for payload in (None, "{}", "[]", '{"pid": true}', '{"pid": 0}'):
            with self.subTest(payload=payload):
                def exists(path):
                    return False if path.name == "child.json" and payload is None else original_exists(path)
                def read(path, *args, **kwargs):
                    return payload if path.name == "child.json" else original_read(path, *args, **kwargs)
                with mock.patch.object(Path, "exists", exists), mock.patch.object(Path, "read_text", read):
                    code, output, _ = cert._run([sys.executable, "-c", "print('REAL_GATE_METADATA_PROBE')"])
                self.assertNotEqual(0, code)
                self.assertIn("REAL_GATE_METADATA_PROBE", output)
                self.assertIn("metadata_error", cert.PROCESS_RECORDS[-1])
                self.assertEqual("INFRASTRUCTURE_ERROR", cert.PROCESS_RECORDS[-1]["result"])

    def test_log_persistence_failure_preserves_executed_step(self):
        original_open = Path.open
        def fail_log(path, *args, **kwargs):
            if path.suffix == ".log": raise OSError("injected gate log persistence failure")
            return original_open(path, *args, **kwargs)
        with mock.patch.object(Path, "open", fail_log):
            self.assertNotEqual(0, self.run_main())
        summary = self.summary()
        self.assertEqual("FAIL", summary["LOCAL_CERTIFICATION"])
        self.assertEqual([], summary["not_started_steps"])
        self.assertEqual("synthetic", summary["steps"][0]["name"])
        self.assertEqual(0, summary["steps"][0]["exit_code"])
        self.assertIn("synthetic-ok", summary["steps"][0]["process"]["stdout"])
        self.assertIsNone(summary["steps"][0]["log_file"])

    def test_cleanup_failure_count_distinguishes_actual_gate_failure(self):
        for observed in (0, 7):
            with self.subTest(observed=observed):
                step = cert.StepResult("synthetic", ["gate"], 125, 0, "FAIL", "cleanup failed", process={"result": "EXITED", "cleanup": "FAILED", "observed_exit_code": observed})
                summary = cert._build_summary(profile="se02", scope="FULL_SE02_LOCAL", before=self.good, after=self.good, results=[step], expected_steps=["synthetic"])
                self.assertEqual("FAIL", summary["LOCAL_CERTIFICATION"])
                self.assertEqual(1, summary["failure_count"])
                self.assertEqual(int(observed != 0), summary["gate_failure_count"])
                self.assertGreater(summary["infrastructure_error_count"], 0)

    def persistence_boundary(self, boundary):
        """Only persistence is injected; Git, child execution and exits are real."""
        marker = Path(self.tmp.name) / "observed-gate"
        later = Path(self.tmp.name) / "later-gate"
        command = [sys.executable, "-B", "-c",
                   f"import os;from pathlib import Path;print('OBSERVED_GATE',flush=True);Path({str(marker)!r}).write_text(str(os.getpid()))"]
        later_command = [sys.executable, "-B", "-c",
                         f"from pathlib import Path;Path({str(later)!r}).write_text('later');print('LATER_GATE')"]
        plan = [("observed", command), ("later", later_command)]
        original_write, original_open = cert._write_json, Path.open
        original_summary = cert._build_summary
        built, faults = [], []
        journal_state = {"before_start": "STARTING", "after_start": "RUNNING", "final_journal": "EXITED"}.get(boundary)
        def fail_json(path, payload):
            matching = (path.name == "processes.json" and journal_state and payload
                        and payload[-1].get("command") == command
                        and payload[-1].get("result") == journal_state)
            if matching and not faults:
                if boundary == "after_start": wait_for_file(marker)
                faults.append(json.loads(json.dumps(payload[-1])))
                raise OSError("FAULT_" + boundary)
            if path.name == boundary + ".json":
                faults.append(path.name)
                raise OSError("FAULT_" + boundary)
            return original_write(path, payload)
        def fail_log(path, *args, **kwargs):
            if boundary == "log" and path.suffix == ".log":
                faults.append(str(path)); raise OSError("FAULT_log")
            return original_open(path, *args, **kwargs)
        def capture(**kwargs):
            data = original_summary(**kwargs); built.append(data); return data
        with mock.patch.object(cert, "_write_json", side_effect=fail_json), mock.patch.object(Path, "open", fail_log), mock.patch.object(cert, "_build_summary", side_effect=capture):
            exit_code = self.run_main(plan=plan)
        data = built[-1]
        (Path(self.tmp.name) / "persistence-oracle.json").write_text(json.dumps({
            "boundary": boundary, "exit": exit_code, "faults": faults,
            "marker_exists": marker.exists(), "later_exists": later.exists(), "summary": data,
        }, indent=2), encoding="utf8")
        completed = boundary in ("environment", "summary", "positive")
        expected_names = ["observed", "later"] if completed else ["observed"]
        self.assertEqual(boundary != "before_start", marker.exists())
        self.assertEqual(completed, later.exists())
        self.assertEqual(expected_names, [s["name"] for s in data["steps"]])
        not_started = [] if completed else (["observed", "later"] if boundary == "before_start" else ["later"])
        self.assertEqual(not_started, data["not_started_steps"])
        self.assertEqual(command, data["steps"][0]["command"])
        process = data["steps"][0]["process"]
        self.assertEqual(command, process["command"], "must not attach an adjacent Git invocation")
        if boundary == "before_start":
            self.assertIsNone(process["pid"])
            self.assertIsNone(process["observed_exit_code"])
            self.assertNotEqual("EXITED", process["result"])
        else:
            self.assertFalse(alive(int(marker.read_text())))
            self.assertEqual("COMPLETE", process["cleanup"])
            self.assertIn("OBSERVED_GATE", process["stdout"])
            if boundary != "after_start":
                self.assertEqual(0, process["observed_exit_code"])
                self.assertEqual(0, data["steps"][0]["exit_code"])
                self.assertEqual(0, data["failure_count"])
        self.assertEqual(0, data["gate_failure_count"])
        commands_path = self.out / "commands.json"
        if boundary != "environment":
            commands = json.loads(commands_path.read_text())
            self.assertEqual(expected_names, [c["name"] for c in commands])
            self.assertEqual(command, commands[0]["command"])
        if boundary == "positive":
            self.assertEqual(0, exit_code)
            self.assertEqual("PASS", data["LOCAL_CERTIFICATION"])
            self.assertEqual([], faults)
        else:
            self.assertTrue(faults, "fault injection must actually execute")
            self.assertNotEqual(0, exit_code)
            self.assertEqual("FAIL", data["LOCAL_CERTIFICATION"])
            self.assertFalse(data["release_clean_certification"])
            self.assertGreater(data["infrastructure_error_count"], 0)
        if boundary in ("environment", "summary"):
            self.assertFalse((self.out / "summary.json").exists(), "a failed essential write must not leave a durable PASS")

    def test_journal_failure_before_start_preserves_attempt(self):
        self.persistence_boundary("before_start")

    def test_journal_failure_after_start_preserves_execution(self):
        self.persistence_boundary("after_start")

    def test_final_journal_failure_preserves_observed_exit_and_command(self):
        self.persistence_boundary("final_journal")

    def test_log_failure_external_execution_oracle(self):
        self.persistence_boundary("log")

    def test_environment_failure_external_execution_oracle(self):
        self.persistence_boundary("environment")

    def test_summary_failure_external_execution_oracle(self):
        self.persistence_boundary("summary")

    def test_persistence_positive_external_execution_oracle(self):
        self.persistence_boundary("positive")

    def cli_cancellation(self, mode, target):
        directory = Path(self.tmp.name) / (mode + "_" + target)
        directory.mkdir()
        source = "import runpy,sys;runpy.run_path(sys.argv[1])['main_cli_probe'](*sys.argv[2:])"
        command = [sys.executable, "-B", "-c", source, str(Path(__file__).resolve()), mode, target, str(self.root), str(directory)]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=30)
        (directory / "external-exit.json").write_text(json.dumps({"argv": command, "exit": completed.returncode,
            "stdout": completed.stdout, "stderr": completed.stderr}, indent=2), encoding="utf8")
        observed = json.loads((directory / "observations.json").read_text())
        summary_path = directory / "bundle/summary.json"
        summary = json.loads(summary_path.read_text()) if summary_path.exists() else observed["summary_in_memory"]
        records = observed["processes"]
        pids = [r[k] for r in records for k in ("pid", "launcher_pid") if r.get(k)]
        if observed["child_pid"]: pids.append(observed["child_pid"])
        self.assertTrue(all(not alive(pid) for pid in pids), pids)
        commands_path = directory / "bundle/commands.json"
        commands = json.loads(commands_path.read_text()) if commands_path.exists() else None
        if mode == "normal":
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual("PASS", summary["LOCAL_CERTIFICATION"])
            self.assertEqual([], observed["injected"])
            self.assertEqual([], summary["not_started_steps"])
            self.assertEqual(["observed_gate", "later"], [s["name"] for s in summary["steps"]])
            return
        self.assertEqual(1, len(observed["injected"]), observed)
        self.assertNotEqual(0, completed.returncode, completed.stdout)
        self.assertEqual(8 if mode == "nonzero" else 130, completed.returncode)
        self.assertEqual("FAIL", summary["LOCAL_CERTIFICATION"])
        self.assertFalse(summary["release_clean_certification"])
        if target == "finalization":
            self.assertTrue(observed["executed"] and observed["ready"])
            self.assertEqual(["observed_gate", "later"], [s["name"] for s in summary["steps"]])
            self.assertEqual([], summary["not_started_steps"])
            self.assertEqual(0, summary["gate_failure_count"])
            self.assertGreater(summary["infrastructure_error_count"], 0)
            return
        if target == "gate":
            self.assertTrue(observed["executed"] and observed["ready"])
            self.assertEqual(["observed_gate"], [s["name"] for s in summary["steps"]])
            self.assertEqual(["observed_gate"], [s["name"] for s in commands])
            self.assertEqual(["later"], summary["not_started_steps"])
            process = summary["steps"][0]["process"]
            self.assertEqual("INTERRUPTED", process["result"])
            self.assertIn("CLI_BEFORE_INTERRUPT", process["stdout"])
            self.assertIsNone(process["observed_exit_code"])
        else:
            self.assertEqual(["git", "branch", "--show-current"], observed["injected"][0]["requested_argv"])
            self.assertFalse(observed["executed"])
            self.assertEqual([], summary["steps"])
            self.assertEqual([], commands)
            self.assertEqual(["observed_gate", "later"], summary["not_started_steps"])

    def test_main_subprocess_cancellations_during_gate(self):
        for mode in ("zero", "none", "nonzero", "keyboard"):
            with self.subTest(mode=mode): self.cli_cancellation(mode, "gate")

    def test_main_subprocess_cancellations_during_optional_git(self):
        for mode in ("zero", "none", "nonzero", "keyboard"):
            with self.subTest(mode=mode): self.cli_cancellation(mode, "optional_git")

    def test_main_subprocess_normal_exit_zero(self):
        self.cli_cancellation("normal", "gate")

    def test_main_subprocess_cancellations_during_finalization(self):
        for mode in ("zero", "none", "nonzero", "keyboard"):
            with self.subTest(mode=mode): self.cli_cancellation(mode, "finalization")

    def test_cli_help_and_parse_error_before_campaign(self):
        for flag, expected in (("--help", 0), ("--not-a-certifier-option", 2)):
            completed = subprocess.run([sys.executable, "-B", str(SOURCE), flag], capture_output=True, text=True, timeout=10)
            self.assertEqual(expected, completed.returncode, completed.stderr)
            self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
