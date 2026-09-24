from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .contract import COMMAND_RECORD_SCHEMA_VERSION

ROOT = Path(__file__).resolve().parents[3]


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def fingerprint_paths(root: Path, paths: Iterable[str]) -> str:
    h = hashlib.sha256()
    for rel in sorted(set(paths)):
        p = root / rel
        h.update(rel.encode("utf-8") + b"\0")
        if not p.exists() and not p.is_symlink():
            h.update(b"MISSING\0")
            continue
        if p.is_symlink():
            h.update(b"SYMLINK\0" + os.readlink(p).encode("utf-8", "surrogateescape") + b"\0")
            continue
        if p.is_file():
            h.update(b"FILE\0" + hashlib.sha256(p.read_bytes()).digest())
            continue
        h.update(b"DIR\0")
        for child in sorted(x for x in p.rglob("*") if x.is_file() or x.is_symlink()):
            child_rel = child.relative_to(root).as_posix()
            h.update(child_rel.encode("utf-8") + b"\0")
            if child.is_symlink():
                h.update(b"L\0" + os.readlink(child).encode("utf-8", "surrogateescape") + b"\0")
            else:
                h.update(hashlib.sha256(child.read_bytes()).digest())
    return h.hexdigest()


_RUNTIME_ENV_KEYS = (
    "PATH", "SYSTEMROOT", "WINDIR", "SYSTEMDRIVE", "COMSPEC", "PATHEXT", "OS",
    "TEMP", "TMP", "HOME", "USERPROFILE", "HOMEDRIVE", "HOMEPATH",
    "APPDATA", "LOCALAPPDATA", "PROGRAMDATA",
    "PROGRAMFILES", "PROGRAMFILES(X86)", "COMMONPROGRAMFILES", "COMMONPROGRAMFILES(X86)",
    "PROCESSOR_ARCHITECTURE", "PROCESSOR_IDENTIFIER", "NUMBER_OF_PROCESSORS",
    "LANG", "LC_ALL", "LC_CTYPE", "TZ",
)


def _clean_env() -> dict[str, str]:
    allowed = {key: os.environ.get(key, "") for key in _RUNTIME_ENV_KEYS}
    allowed.update({
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    return {key: value for key, value in allowed.items() if value}


def _group_alive(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _wait_group_gone(pgid: int, timeout: float) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not _group_alive(pgid):
            return True
        time.sleep(0.05)
    return not _group_alive(pgid)


def _terminate_posix_group(pgid: int) -> str:
    if not _group_alive(pgid):
        return "COMPLETE_ALREADY_EXITED"
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return "COMPLETE_ALREADY_EXITED"
    if _wait_group_gone(pgid, 2.0):
        return "COMPLETE"
    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        return "COMPLETE"
    return "COMPLETE" if _wait_group_gone(pgid, 8.0) else "INCOMPLETE"


class _WindowsJob:
    def __init__(self) -> None:
        import ctypes
        from ctypes import wintypes as w

        self.ctypes = ctypes
        self.w = w
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.handle = self.kernel32.CreateJobObjectW(None, None)
        if not self.handle:
            raise OSError(ctypes.get_last_error(), "CreateJobObjectW failed")

        class BasicLimit(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", w.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", w.DWORD),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", w.DWORD),
                ("SchedulingClass", w.DWORD),
            ]

        class IoCounters(ctypes.Structure):
            _fields_ = [
                ("ReadOperationCount", ctypes.c_ulonglong),
                ("WriteOperationCount", ctypes.c_ulonglong),
                ("OtherOperationCount", ctypes.c_ulonglong),
                ("ReadTransferCount", ctypes.c_ulonglong),
                ("WriteTransferCount", ctypes.c_ulonglong),
                ("OtherTransferCount", ctypes.c_ulonglong),
            ]

        class ExtendedLimit(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", BasicLimit),
                ("IoInfo", IoCounters),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        class BasicAccounting(ctypes.Structure):
            _fields_ = [
                ("TotalUserTime", ctypes.c_longlong),
                ("TotalKernelTime", ctypes.c_longlong),
                ("ThisPeriodTotalUserTime", ctypes.c_longlong),
                ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
                ("TotalPageFaultCount", w.DWORD),
                ("TotalProcesses", w.DWORD),
                ("ActiveProcesses", w.DWORD),
                ("TotalTerminatedProcesses", w.DWORD),
            ]

        self.BasicAccounting = BasicAccounting
        info = ExtendedLimit()
        info.BasicLimitInformation.LimitFlags = 0x00002000
        ok = self.kernel32.SetInformationJobObject(self.handle, 9, ctypes.byref(info), ctypes.sizeof(info))
        if not ok:
            err = ctypes.get_last_error()
            self.close()
            raise OSError(err, "SetInformationJobObject failed")

    def assign(self, process: subprocess.Popen[bytes]) -> None:
        handle = self.w.HANDLE(int(process._handle))
        if not self.kernel32.AssignProcessToJobObject(self.handle, handle):
            raise OSError(self.ctypes.get_last_error(), "AssignProcessToJobObject failed")

    def active_processes(self) -> int:
        info = self.BasicAccounting()
        ok = self.kernel32.QueryInformationJobObject(
            self.handle, 1, self.ctypes.byref(info), self.ctypes.sizeof(info), None
        )
        if not ok:
            raise OSError(self.ctypes.get_last_error(), "QueryInformationJobObject failed")
        return int(info.ActiveProcesses)

    def terminate(self) -> bool:
        return bool(self.kernel32.TerminateJobObject(self.handle, 1))

    def wait_empty(self, timeout: float) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                if self.active_processes() == 0:
                    return True
            except OSError:
                return False
            time.sleep(0.05)
        try:
            return self.active_processes() == 0
        except OSError:
            return False

    def close(self) -> None:
        handle = getattr(self, "handle", None)
        if handle:
            self.kernel32.CloseHandle(handle)
            self.handle = None


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _write_record(prefix: Path, row: dict) -> None:
    prefix.with_suffix(".json").write_bytes(
        (json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    )


_WINDOWS_LAUNCHER = """import json, pathlib, subprocess, sys
if sys.stdin.buffer.read(1) != b'1': sys.exit(125)
try:
 p = subprocess.Popen(json.loads(sys.argv[1]), stdin=subprocess.DEVNULL)
except OSError as exc:
 pathlib.Path(sys.argv[2]).write_text(json.dumps({'start_error': repr(exc)}), encoding='utf-8')
 sys.exit(125)
pathlib.Path(sys.argv[2]).write_text(json.dumps({'pid': p.pid}), encoding='utf-8')
sys.exit(p.wait())
"""


def _read_windows_child(path: Path) -> tuple[int | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None, "WINDOWS_CHILD_START_UNOBSERVED"
    pid = payload.get("pid")
    if type(pid) is int and pid > 0:
        return pid, None
    error = payload.get("start_error")
    return None, "WINDOWS_CHILD_START_ERROR:" + str(error or "UNKNOWN")


def run_argv(argv: list[str], evidence_dir: Path, name: str, *, timeout: float = 120.0) -> dict:
    if not argv or any(not isinstance(x, str) or not x for x in argv):
        raise ValueError("ARGV_INVALID")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ValueError("TIMEOUT_INVALID")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    started = _utc()
    t0 = time.monotonic()
    prefix = evidence_dir / name
    stdout_path = prefix.with_suffix(".stdout.txt")
    stderr_path = prefix.with_suffix(".stderr.txt")
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    job: _WindowsJob | None = None
    process: subprocess.Popen[bytes] | None = None
    supervision = "WINDOWS_JOB_OBJECT" if os.name == "nt" else "POSIX_PROCESS_GROUP"

    with stdout_path.open("wb", buffering=0) as stdout_f, stderr_path.open("wb", buffering=0) as stderr_f:
        try:
            windows_child_path = evidence_dir / f"{name}.child.json"
            if os.name == "nt":
                job = _WindowsJob()
                process = subprocess.Popen(
                    [sys.executable, "-c", _WINDOWS_LAUNCHER, json.dumps(argv), str(windows_child_path)],
                    cwd=ROOT,
                    env=_clean_env(),
                    stdin=subprocess.PIPE,
                    stdout=stdout_f,
                    stderr=stderr_f,
                    shell=False,
                    start_new_session=False,
                    creationflags=flags,
                )
                try:
                    job.assign(process)
                    if process.stdin is None:
                        raise OSError("WINDOWS_LAUNCHER_STDIN_MISSING")
                    process.stdin.write(b"1")
                    process.stdin.flush()
                    process.stdin.close()
                except OSError:
                    try:
                        process.kill()
                        process.wait(timeout=5)
                    except (OSError, subprocess.SubprocessError):
                        pass
                    raise
            else:
                process = subprocess.Popen(
                    argv,
                    cwd=ROOT,
                    env=_clean_env(),
                    stdout=stdout_f,
                    stderr=stderr_f,
                    shell=False,
                    start_new_session=True,
                    creationflags=flags,
                )
        except OSError as exc:
            if job is not None:
                job.close()
            stderr_f.write(str(exc).encode("utf-8", errors="replace"))
            row = {
                "record_schema": COMMAND_RECORD_SCHEMA_VERSION,
                "name": name, "argv": argv, "command_started": False, "pid": None,
                "exit_code": 125, "timed_out": False, "cleanup": "NOT_STARTED",
                "residual_descendants_detected": False, "supervision": "NOT_STARTED",
                "duration_seconds": time.monotonic() - t0, "started_at_utc": started, "ended_at_utc": _utc(),
                "stdout_sha256": "", "stderr_sha256": "",
                "spawn_error": f"{type(exc).__name__}:{exc}",
            }
        else:
            timed_out = False
            residual = False
            cleanup = "COMPLETE_ALREADY_EXITED"
            try:
                process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                if os.name == "nt" and job is not None:
                    residual = job.active_processes() > 1
                    job.terminate()
                    cleanup = "COMPLETE" if job.wait_empty(10.0) else "INCOMPLETE"
                else:
                    cleanup = _terminate_posix_group(process.pid)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    cleanup = "INCOMPLETE"
            else:
                if os.name == "nt" and job is not None:
                    try:
                        active = job.active_processes()
                    except OSError:
                        active = 1
                        cleanup = "INCOMPLETE"
                    if active > 0:
                        residual = True
                        job.terminate()
                        cleanup = "COMPLETE_DESCENDANTS_TERMINATED" if job.wait_empty(10.0) else "INCOMPLETE"
                elif _group_alive(process.pid):
                    residual = True
                    tree_cleanup = _terminate_posix_group(process.pid)
                    cleanup = "COMPLETE_DESCENDANTS_TERMINATED" if tree_cleanup in {"COMPLETE", "COMPLETE_ALREADY_EXITED"} else "INCOMPLETE"
            code = process.returncode if process.returncode is not None else 124
            if timed_out and code == 0:
                code = 124
            observed_pid = process.pid
            child_start_error = None
            if os.name == "nt":
                observed_pid, child_start_error = _read_windows_child(windows_child_path)
            if child_start_error is not None:
                row = {
                    "record_schema": COMMAND_RECORD_SCHEMA_VERSION,
                    "name": name, "argv": argv, "command_started": False, "pid": None,
                    "exit_code": int(code) if type(code) is int else 125, "timed_out": timed_out,
                    "cleanup": "NOT_STARTED", "residual_descendants_detected": False,
                    "supervision": "NOT_STARTED",
                    "duration_seconds": time.monotonic() - t0, "started_at_utc": started, "ended_at_utc": _utc(),
                    "stdout_sha256": "", "stderr_sha256": "", "spawn_error": child_start_error,
                }
            else:
                row = {
                    "record_schema": COMMAND_RECORD_SCHEMA_VERSION,
                    "name": name, "argv": argv, "command_started": True, "pid": observed_pid,
                    "exit_code": int(code), "timed_out": timed_out, "cleanup": cleanup,
                    "residual_descendants_detected": residual, "supervision": supervision,
                    "duration_seconds": time.monotonic() - t0, "started_at_utc": started, "ended_at_utc": _utc(),
                    "stdout_sha256": "", "stderr_sha256": "",
                }
        finally:
            if job is not None:
                job.close()
            for fh in (stdout_f, stderr_f):
                try:
                    fh.flush()
                    os.fsync(fh.fileno())
                except OSError:
                    pass

    row["stdout_sha256"] = _hash_file(stdout_path)
    row["stderr_sha256"] = _hash_file(stderr_path)
    _write_record(prefix, row)
    return row
