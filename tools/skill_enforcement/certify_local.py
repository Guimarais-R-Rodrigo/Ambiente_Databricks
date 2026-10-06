#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Certificação local reproduzível do Skill Enforcement Framework.

Uso principal:

    python -B tools/skill_enforcement/certify_local.py --profile se02
    python -B tools/skill_enforcement/certify_local.py --profile se03
    python -B tools/skill_enforcement/certify_local.py --profile se04
    python -B tools/skill_enforcement/certify_local.py --profile se05
    python -B tools/skill_enforcement/certify_local.py --profile se06
    python -B tools/skill_enforcement/certify_local.py --profile se07
    python -B tools/skill_enforcement/certify_local.py --profile se08

O certifier é o gate determinístico de desenvolvimento do SEF. Ele não usa
credenciais Databricks nem rede por conta própria. GitHub Actions deve chamar o
mesmo entrypoint somente na release candidate/Ready-for-review e pós-merge.

Por padrão a execução exige worktree limpo, materializa o simulado pelo renderer
canônico e confere paths, bytes/hashes e tipos sem depender de git diff. Isso
transforma drift do derivado em evidência explícita (`DERIVED_STALE`) em vez de
permitir uma cópia manual ou deixar arquivos novos invisíveis ao gate.

A precondição de worktree limpo é uma barreira de segurança: se ela falhar, o
certifier encerra antes de qualquer step mutável, especialmente antes do renderer.
"""

from __future__ import annotations

import argparse
import json
import locale
import os
import math
import re
import signal
import tempfile
import traceback
import uuid
import platform
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = Path.home() / ".ambiente_databricks" / "sef_certifications"
sys.path.insert(0, str(REPO_ROOT / "tools"))
from project_policy import SIMULATED_ROOT
DERIVED_ROOT = SIMULATED_ROOT.as_posix()


@dataclass(frozen=True)
class StepResult:
    name: str
    command: list[str]
    exit_code: int
    duration_seconds: float
    status: str
    last_line: str
    log_file: str | None = None
    process: dict[str, object] | None = None


@dataclass(frozen=True)
class GitState:
    head_sha: str | None
    branch: str | None
    origin_main_sha: str | None
    merge_base_sha: str | None
    status_short: str

    observation_errors: tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return not self.observation_errors and bool(re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", self.head_sha or ""))

    @property
    def clean(self) -> bool:
        return self.valid and not self.status_short.strip()


_CONTRACT_STEP = (
    "contract_v0_1",
    [sys.executable, "-B", "tools/skill_enforcement/validate_contracts.py"],
)
_SE01_STEP = (
    "se01_regression",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se01.py"],
)
_SE02_STEP = (
    "se02_regression",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se02.py", "-v"],
)
_SE03_STEP = (
    "se03_regression",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se03.py", "-v"],
)
_SE04_RECEIPT_STEP = (
    "se04_receipt_tests",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se04.py", "-v"],
)
_SE04_RUNNER_STEP = (
    "se04_runner_tests",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se04_runner.py", "-v"],
)
_SE05_POSTFLIGHT_STEP = (
    "se05_postflight_tests",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se05.py", "-v"],
)
_SE05_RUNNER_STEP = (
    "se05_runner_tests",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se05_runner.py", "-v"],
)
_SE06_EVAL_STEP = (
    "se06_eval_tests",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se06.py", "-v"],
)
_SE07_POLICY_STEP = (
    "se07_policy_validation",
    [sys.executable, "-B", "tools/skill_enforcement/se07_policy.py"],
)
_SE07_TEST_STEP = (
    "se07_policy_tests",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se07.py", "-v"],
)
_SE08_POLICY_IO_STEP = (
    "se08_policy_io_tests",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_policy_io.py", "-v"],
)
_SE08_TEST_STEP = (
    "se08_operational_tests",
    [sys.executable, "-B", "tools/tests/test_skill_enforcement_se08.py", "-v"],
)
_SE08_STORAGE_CLEANUP_STEP = (
    "se08_storage_cleanup_tests",
    [sys.executable, "-B", "tools/tests/test_certify_storage_cleanup.py", "-v"],
)
_SE08_WINDOWS_CORRECTIVE_STEP = (
    "se08_windows_corrective_tests",
    [sys.executable, "-B", "tools/tests/test_se08_windows_corrective.py", "-v"],
)
_SE08_CLEANUP_DIAGNOSTICS_STEP = (
    "se08_cleanup_diagnostics_tests",
    [sys.executable, "-B", "tools/tests/test_se08_cleanup_diagnostics.py", "-v"],
)
_COMMON_FINAL_STEPS = [
    (
        "assistant_structure",
        [sys.executable, "tools/validate_assistant.py"],
    ),
    (
        "render_simulado",
        [sys.executable, "tools/render_simulado.py", "--write"],
    ),
    (
        "render_diff",
        [sys.executable, "tools/render_simulado.py", "--check"],
    ),
    (
        "readme_snapshot",
        [sys.executable, "tools/validate_assistant.py", "--conferir-readme"],
    ),
]

PROFILE_STEPS: dict[str, list[tuple[str, list[str]]]] = {
    "se02": [
        _CONTRACT_STEP,
        _SE01_STEP,
        (
            "se02_tests",
            [sys.executable, "-B", "tools/tests/test_skill_enforcement_se02.py", "-v"],
        ),
        *_COMMON_FINAL_STEPS,
    ],
    "se03": [
        _CONTRACT_STEP,
        _SE01_STEP,
        _SE02_STEP,
        _SE03_STEP,
        *_COMMON_FINAL_STEPS,
    ],
    "se04": [
        _CONTRACT_STEP,
        _SE01_STEP,
        _SE02_STEP,
        _SE03_STEP,
        _SE04_RECEIPT_STEP,
        _SE04_RUNNER_STEP,
        *_COMMON_FINAL_STEPS,
    ],
    "se05": [
        _CONTRACT_STEP,
        _SE01_STEP,
        _SE02_STEP,
        _SE03_STEP,
        _SE04_RECEIPT_STEP,
        _SE04_RUNNER_STEP,
        _SE05_POSTFLIGHT_STEP,
        _SE05_RUNNER_STEP,
        *_COMMON_FINAL_STEPS,
    ],
    "se06": [
        _CONTRACT_STEP,
        _SE01_STEP,
        _SE02_STEP,
        _SE03_STEP,
        _SE04_RECEIPT_STEP,
        _SE04_RUNNER_STEP,
        _SE05_POSTFLIGHT_STEP,
        _SE05_RUNNER_STEP,
        _SE06_EVAL_STEP,
        *_COMMON_FINAL_STEPS,
    ],
    "se07": [
        _CONTRACT_STEP,
        _SE01_STEP,
        _SE02_STEP,
        _SE03_STEP,
        _SE04_RECEIPT_STEP,
        _SE04_RUNNER_STEP,
        _SE05_POSTFLIGHT_STEP,
        _SE05_RUNNER_STEP,
        _SE06_EVAL_STEP,
        _SE07_POLICY_STEP,
        _SE07_TEST_STEP,
        ("certifier_regression", [sys.executable, "-B", "tools/tests/test_certify_local.py", "-v"]),
        *_COMMON_FINAL_STEPS,
    ],
    "se08": [
        _CONTRACT_STEP,
        _SE01_STEP,
        _SE02_STEP,
        _SE03_STEP,
        _SE04_RECEIPT_STEP,
        _SE04_RUNNER_STEP,
        _SE05_POSTFLIGHT_STEP,
        _SE05_RUNNER_STEP,
        _SE06_EVAL_STEP,
        _SE07_POLICY_STEP,
        _SE07_TEST_STEP,
        _SE08_POLICY_IO_STEP,
        _SE08_TEST_STEP,
        _SE08_STORAGE_CLEANUP_STEP,
        _SE08_WINDOWS_CORRECTIVE_STEP,
        _SE08_CLEANUP_DIAGNOSTICS_STEP,
        ("certifier_regression", [sys.executable, "-B", "tools/tests/test_certify_local.py", "-v"]),
        *_COMMON_FINAL_STEPS,
    ],
}


def _decode(data: bytes) -> str:
    for encoding in ("utf-8", locale.getpreferredencoding(False)):
        try:
            return data.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", errors="replace")


# Per-process budgets, not a campaign deadline. No budget is extended after failure.
GIT_TIMEOUT_SECONDS = 30.0
STEP_TIMEOUT_SECONDS = 900.0
CLEANUP_TIMEOUT_SECONDS = 10.0
PROCESS_RECORDS: list[dict[str, object]] = []
ACTIVE_EVIDENCE: Path | None = None
RESERVATIONS: dict[Path, tuple[int, int]] = {}


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class _WindowsJob:
    """Own only processes assigned to this job; close also kills descendants.

    A Python launcher waits on stdin before spawning the requested argv, so job
    assignment precedes any gate child. No process-name kill or privileges used.
    """
    def __init__(self) -> None:
        import ctypes
        from ctypes import wintypes as w
        self.ctypes = ctypes
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        class Basic(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong),
                        ("PerJobUserTimeLimit", ctypes.c_longlong), ("LimitFlags", w.DWORD),
                        ("MinimumWorkingSetSize", ctypes.c_size_t), ("MaximumWorkingSetSize", ctypes.c_size_t),
                        ("ActiveProcessLimit", w.DWORD), ("Affinity", ctypes.c_size_t),
                        ("PriorityClass", w.DWORD), ("SchedulingClass", w.DWORD)]
        class Limits(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", Basic), ("IoInfo", ctypes.c_ulonglong * 6),
                        ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                        ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]
        class Accounting(ctypes.Structure):
            _fields_ = [("Times", ctypes.c_longlong * 4), ("TotalPageFaultCount", w.DWORD),
                        ("TotalProcesses", w.DWORD), ("ActiveProcesses", w.DWORD),
                        ("TotalTerminatedProcesses", w.DWORD)]
        class ProcessIds(ctypes.Structure):
            _fields_ = [("AssignedProcesses", w.DWORD), ("Count", w.DWORD),
                        ("Pids", ctypes.c_size_t * 256)]
        self.accounting = Accounting
        self.process_ids = ProcessIds
        for name, restype, argtypes in [
            ("CreateJobObjectW", w.HANDLE, [ctypes.c_void_p, w.LPCWSTR]),
            ("SetInformationJobObject", w.BOOL, [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD]),
            ("AssignProcessToJobObject", w.BOOL, [w.HANDLE, w.HANDLE]),
            ("TerminateJobObject", w.BOOL, [w.HANDLE, w.UINT]),
            ("QueryInformationJobObject", w.BOOL, [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.c_void_p]),
            ("CloseHandle", w.BOOL, [w.HANDLE]),
        ]:
            fn = getattr(self.k, name); fn.restype = restype; fn.argtypes = argtypes
        self.handle = self.k.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = Limits(); limits.BasicLimitInformation.LimitFlags = 0x2000
        if not self.k.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.WinError(ctypes.get_last_error()); self.close(); raise error

    def assign(self, process: subprocess.Popen) -> None:
        if not self.k.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise self.ctypes.WinError(self.ctypes.get_last_error())

    def snapshot(self) -> dict[str, object]:
        """Single diagnostic snapshot; never waits, terminates or changes the job."""
        if not self.handle:
            return {"status": "NO_OPEN_OWNED_JOB"}
        info = self.accounting()
        if not self.k.QueryInformationJobObject(
            self.handle, 1, self.ctypes.byref(info), self.ctypes.sizeof(info), None
        ):
            return {"status": "UNOBSERVABLE", "winerror": self.ctypes.get_last_error()}
        result: dict[str, object] = {
            "status": "OBSERVED",
            "active": info.ActiveProcesses,
            "total": info.TotalProcesses,
            "terminated": info.TotalTerminatedProcesses,
        }
        pids = self.process_ids()
        ok = self.k.QueryInformationJobObject(
            self.handle, 3, self.ctypes.byref(pids), self.ctypes.sizeof(pids), None
        )
        if ok and pids.Count <= len(pids.Pids):
            result["pid_list"] = {
                "status": "OBSERVED",
                "assigned": pids.AssignedProcesses,
                "pids": list(pids.Pids[:pids.Count]),
            }
        else:
            result["pid_list"] = {
                "status": "INCOMPLETE",
                "assigned": pids.AssignedProcesses,
                "winerror": 0 if ok else self.ctypes.get_last_error(),
            }
        return result

    def terminate(self) -> None:
        if not self.k.TerminateJobObject(self.handle, 1):
            raise self.ctypes.WinError(self.ctypes.get_last_error())
        until = time.monotonic() + CLEANUP_TIMEOUT_SECONDS
        while True:
            info = self.accounting()
            if not self.k.QueryInformationJobObject(self.handle, 1, self.ctypes.byref(info), self.ctypes.sizeof(info), None):
                raise self.ctypes.WinError(self.ctypes.get_last_error())
            if info.ActiveProcesses == 0:
                return
            if time.monotonic() >= until:
                raise OSError("job still has active processes after cleanup deadline")
            time.sleep(0.02)

    def close(self) -> None:
        if self.handle:
            handle, self.handle = self.handle, None
            if not self.k.CloseHandle(handle):
                raise self.ctypes.WinError(self.ctypes.get_last_error())


# This launcher is used only on Windows; the job is assigned before stdin opens.
_WINDOWS_LAUNCHER = """import json, pathlib, subprocess, sys
if sys.stdin.buffer.read(1) != b'1': sys.exit(125)
try:
 p = subprocess.Popen(json.loads(sys.argv[1]), stdin=subprocess.DEVNULL)
except OSError as exc:
 pathlib.Path(sys.argv[2]).write_text(json.dumps({'start_error': repr(exc)}), encoding='utf8')
 sys.exit(125)
pathlib.Path(sys.argv[2]).write_text(json.dumps({'pid': p.pid}), encoding='utf8')
sys.exit(p.wait())
"""


def _flush_process_records() -> None:
    if ACTIVE_EVIDENCE is not None:
        _assert_reserved(ACTIVE_EVIDENCE)
        _write_json(ACTIVE_EVIDENCE / "processes.json", PROCESS_RECORDS)


def _persist_process_observation(record: dict[str, object]) -> None:
    try:
        _flush_process_records()
    except (OSError, ValueError) as exc:
        # The in-memory observation remains true even if its journal is stale.
        record["journal_error"] = repr(exc)
        raise


def _posix_group_alive(group: int) -> bool:
    # Linux zombies have terminated but may wait on their external reaper. Only
    # live group members matter. Other POSIX hosts conservatively query killpg.
    procfs = Path("/proc")
    if sys.platform.startswith("linux") and procfs.is_dir():
        for entry in procfs.iterdir():
            if not entry.name.isdigit():
                continue
            try:
                fields = (entry / "stat").read_text().rsplit(")", 1)[1].split()
                if int(fields[2]) == group and fields[0] != "Z":
                    return True
            except FileNotFoundError:
                continue
        return False
    try:
        os.killpg(group, 0)
        return True
    except ProcessLookupError:
        return False


def _exception_details(exc: BaseException) -> dict[str, object]:
    """Observed exception details; never infer a Win32 code from its message."""
    return {"type": type(exc).__name__, "message": str(exc),
            "errno": getattr(exc, "errno", None), "winerror": getattr(exc, "winerror", None),
            "filename": getattr(exc, "filename", None), "filename2": getattr(exc, "filename2", None),
            "traceback": "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))}


def _cleanup_diagnostics_runtime():
    """Load the sibling observer even when this module was file-loaded."""
    if __package__:
        from . import cleanup_diagnostics
        return cleanup_diagnostics

    import importlib.util
    module_name = "_sef_cleanup_diagnostics_runtime"
    module = sys.modules.get(module_name)
    if module is None:
        source = Path(__file__).with_name("cleanup_diagnostics.py")
        spec = importlib.util.spec_from_file_location(module_name, source)
        if spec is None or spec.loader is None:
            raise ImportError("cleanup diagnostics loader unavailable")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    return module


def _restart_manager_file_users(paths: list[Path]) -> dict[str, object]:
    return _cleanup_diagnostics_runtime().file_users(paths)


def _file_process_ids_using_file(path: Path) -> dict[str, object]:
    return _cleanup_diagnostics_runtime().file_process_ids_using_file(path)


def _windows_process_state(pid: object) -> dict[str, object]:
    """Zero-wait snapshot of one PID; never terminates or waits for completion."""
    if os.name != "nt":
        return {"status": "NOT_APPLICABLE_NON_WINDOWS"}
    if type(pid) is not int or pid <= 0:
        return {"status": "INVALID_PID"}
    import ctypes
    from ctypes import wintypes as w

    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.OpenProcess.restype = w.HANDLE
    k.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
    k.GetExitCodeProcess.restype = w.BOOL
    k.GetExitCodeProcess.argtypes = [w.HANDLE, ctypes.POINTER(w.DWORD)]
    k.WaitForSingleObject.restype = w.DWORD
    k.WaitForSingleObject.argtypes = [w.HANDLE, w.DWORD]
    k.CloseHandle.restype = w.BOOL
    k.CloseHandle.argtypes = [w.HANDLE]

    handle = k.OpenProcess(0x00100000 | 0x1000, False, pid)
    if not handle:
        return {"status": "OPEN_FAILED", "winerror": ctypes.get_last_error()}
    try:
        code = w.DWORD()
        if not k.GetExitCodeProcess(handle, ctypes.byref(code)):
            return {"status": "EXIT_CODE_UNOBSERVABLE", "winerror": ctypes.get_last_error()}
        wait_result = int(k.WaitForSingleObject(handle, 0))
        return {
            "status": "OBSERVED",
            "exit_code": int(code.value),
            "wait_result": wait_result,
            "running": code.value == 259,
        }
    finally:
        k.CloseHandle(handle)


def _windows_cleanup_failure_observation(
    record: dict[str, object],
    directory: Path,
    cleanup_error: BaseException,
    *,
    file_users_provider=None,
    file_process_ids_provider=None,
    pid_state_provider=None,
) -> dict[str, object] | None:
    """Observe one native sharing violation as early as possible after failure.

    The failing resource is queried before Restart Manager or secondary files.
    No retry, sleep, delete, handle close or verdict mutation is performed.
    """
    if getattr(cleanup_error, "winerror", None) != 32:
        return None

    observer_started_ns = time.monotonic_ns()
    error_ns = record.get("temporary_cleanup_error_monotonic_ns")
    resources: list[Path] = []
    filename = getattr(cleanup_error, "filename", None)
    if filename:
        resources.append(Path(filename))
    for name in ("stdout", "stderr", "child.json"):
        candidate = directory / name
        if os.path.lexists(candidate):
            resources.append(candidate)
    unique_resources = list(dict.fromkeys(resources))
    priority_resource = Path(filename) if filename else (unique_resources[0] if unique_resources else None)

    observation: dict[str, object] = {
        "status": "OBSERVED_AFTER_NATIVE_WINERROR32",
        "observed_at_utc": _utc(),
        "observer_started_monotonic_ns": observer_started_ns,
        "observer_pid": os.getpid(),
        "warning": "Post-failure diagnostic only; observation may perturb later timing.",
        "resources": [str(path) for path in unique_resources],
        "priority_failed_resource": str(priority_resource) if priority_resource else None,
        "launcher_pid": record.get("launcher_pid"),
        "pid": record.get("pid"),
        "observer_order": [],
    }
    if type(error_ns) is int:
        observation["observer_start_delta_from_cleanup_error_ns"] = observer_started_ns - error_ns

    if file_process_ids_provider is None and os.name == "nt":
        file_process_ids_provider = _file_process_ids_using_file

    file_pid_observations: list[dict[str, object]] = []

    def observe_file_owner(resource: Path, phase: str) -> None:
        started_ns = time.monotonic_ns()
        observation["observer_order"].append({
            "event": "file_process_ids_begin",
            "path": str(resource),
            "phase": phase,
            "monotonic_ns": started_ns,
        })
        if file_process_ids_provider is None:
            item: dict[str, object] = {
                "status": "NOT_APPLICABLE_NON_WINDOWS",
                "path": str(resource),
                "process_ids": [],
            }
        else:
            try:
                item = dict(file_process_ids_provider(resource))
            except Exception as exc:
                item = {
                    "status": "UNOBSERVABLE",
                    "path": str(resource),
                    "error": _exception_details(exc),
                    "process_ids": [],
                }
        finished_ns = time.monotonic_ns()
        item["observer_phase"] = phase
        item["query_started_monotonic_ns"] = started_ns
        item["query_finished_monotonic_ns"] = finished_ns
        item["query_duration_ns"] = finished_ns - started_ns
        if type(error_ns) is int:
            item["query_start_delta_from_cleanup_error_ns"] = started_ns - error_ns
        relations = []
        for owner_pid in item.get("process_ids", []):
            if owner_pid == observation["observer_pid"]:
                relation = "OBSERVER_PID_QUERY_HANDLE_OR_EXISTING_HANDLE"
            elif owner_pid == observation["launcher_pid"]:
                relation = "LAUNCHER_PID"
            elif owner_pid == observation["pid"]:
                relation = "CHILD_PID"
            else:
                relation = "OTHER_PID"
            relations.append({"pid": owner_pid, "relation": relation})
        item["relations"] = relations
        file_pid_observations.append(item)
        observation["observer_order"].append({
            "event": "file_process_ids_end",
            "path": str(resource),
            "phase": phase,
            "monotonic_ns": finished_ns,
            "status": item.get("status"),
        })

    # First discriminant: query exactly the resource whose unlink just failed.
    if priority_resource is not None:
        observe_file_owner(priority_resource, "PRIORITY_FAILED_RESOURCE")

    # Only after the priority per-file query do the broader Restart Manager scan.
    rm_started_ns = time.monotonic_ns()
    observation["observer_order"].append({
        "event": "restart_manager_begin",
        "monotonic_ns": rm_started_ns,
    })
    if file_users_provider is None and os.name == "nt":
        file_users_provider = _restart_manager_file_users
    if file_users_provider is None:
        rm_observation: dict[str, object] = {"status": "NOT_APPLICABLE_NON_WINDOWS"}
    else:
        try:
            rm_observation = dict(file_users_provider(unique_resources))
        except Exception as exc:
            rm_observation = {
                "status": "UNOBSERVABLE",
                "error": _exception_details(exc),
            }
    rm_finished_ns = time.monotonic_ns()
    rm_observation["query_started_monotonic_ns"] = rm_started_ns
    rm_observation["query_finished_monotonic_ns"] = rm_finished_ns
    rm_observation["query_duration_ns"] = rm_finished_ns - rm_started_ns
    if type(error_ns) is int:
        rm_observation["query_start_delta_from_cleanup_error_ns"] = rm_started_ns - error_ns
    observation["restart_manager"] = rm_observation
    observation["observer_order"].append({
        "event": "restart_manager_end",
        "monotonic_ns": rm_finished_ns,
        "status": rm_observation.get("status"),
    })

    # Secondary resources are lower priority and cannot delay the primary sample.
    for resource in unique_resources:
        if priority_resource is not None and resource == priority_resource:
            continue
        observe_file_owner(resource, "SECONDARY_RESOURCE_AFTER_RESTART_MANAGER")
    observation["file_process_ids_using_file"] = file_pid_observations

    if pid_state_provider is None and os.name == "nt":
        pid_state_provider = _windows_process_state
    pid_states: dict[str, object] = {}
    if pid_state_provider is None:
        pid_states["status"] = "NOT_APPLICABLE_NON_WINDOWS"
    else:
        for role in ("launcher_pid", "pid"):
            value = record.get(role)
            try:
                pid_states[role] = pid_state_provider(value)
            except Exception as exc:
                pid_states[role] = {"status": "UNOBSERVABLE", "error": _exception_details(exc)}
    observation["pid_states"] = pid_states
    observation["observer_finished_monotonic_ns"] = time.monotonic_ns()
    return observation

def _temporary_cleanup_observation(record: dict[str, object], directory: Path) -> dict[str, object]:
    """Snapshot observacional imediatamente antes da remoção do diretório.

    Não espera, não fecha handles, não tenta remover e não altera o veredito.
    O objetivo é tornar reproduções Windows/NTFS causalmente auditáveis.
    """
    observation: dict[str, object] = {
        "observed_at_utc": _utc(),
        "directory": str(directory),
        "exists": os.path.lexists(directory),
        "process_result": record.get("result"),
        "process_cleanup": record.get("process_cleanup", record.get("cleanup")),
        "pid": record.get("pid"),
        "launcher_pid": record.get("launcher_pid"),
        "observed_exit_code": record.get("observed_exit_code"),
        "exit_after_cleanup": record.get("exit_after_cleanup"),
        "command_started": record.get("command_started"),
        "metadata_error": record.get("metadata_error"),
        "start_error": record.get("start_error"),
        "utf8_valid": record.get("utf8_valid"),
    }
    try:
        observation["entries"] = sorted(item.name for item in directory.iterdir()) if directory.is_dir() else []
    except OSError as exc:
        observation["entries_error"] = _exception_details(exc)
    return observation


class _ProcessTemporaryDirectory(tempfile.TemporaryDirectory):
    """Observe filesystem cleanup separately from termination of owned processes.

    Do not retry or ignore removal errors. A failed cleanup remains a failure,
    even if a later inspection finds no residual directory. The original
    interruption/timeout and observed child exit remain separate observations.
    """
    def __init__(self, record):
        self.record = record
        super().__init__(prefix="sef-process-")

    def __enter__(self):
        path = super().__enter__()
        self.record["temporary_directory"] = path
        self.record["temporary_cleanup"] = "PENDING"
        return path

    def __exit__(self, exc_type, exc, tb):
        record = self.record
        record["process_cleanup"] = record.get("process_cleanup", record["cleanup"])
        record["temporary_cleanup"] = "RUNNING"
        if record["process_cleanup"] == "COMPLETE":
            record["cleanup"] = "PENDING"
        if exc is not None:
            record["body_exception"] = _exception_details(exc)
        record["temporary_cleanup_pre_remove"] = _temporary_cleanup_observation(
            record, Path(self.name)
        )
        try:
            result = super().__exit__(exc_type, exc, tb)
            if os.path.lexists(self.name):
                raise OSError("PROCESS_TEMPORARY_DIRECTORY_REMAINS", self.name)
        except (OSError, ValueError) as cleanup_error:
            record["temporary_cleanup"] = "FAILED"
            record["cleanup"] = "FAILED"
            record["temporary_cleanup_error_monotonic_ns"] = time.monotonic_ns()
            try:
                native_observation = _windows_cleanup_failure_observation(
                    record, Path(self.name), cleanup_error
                )
            except Exception as diagnostic_error:
                native_observation = {
                    "status": "OBSERVER_FAILED_WITHOUT_REPLACING_CLEANUP_ERROR",
                    "error": _exception_details(diagnostic_error),
                }
            if native_observation is not None:
                record["windows_cleanup_failure_observation"] = native_observation
            # Expensive traceback/filesystem serialization comes after the
            # priority native sample so it cannot consume the transient window.
            record["temporary_cleanup_exception"] = _exception_details(cleanup_error)
            record["temporary_directory_exists_after_cleanup"] = os.path.lexists(self.name)
            record["conventional_exit_code"] = (130 if record["result"] == "INTERRUPTED" else
                                                124 if record["result"] == "TIMEOUT" else 125)
            try:
                _persist_process_observation(record)
            except (OSError, ValueError) as journal_error:
                # Retain both errors in memory and preserve the original failure.
                record["cleanup_journal_exception"] = _exception_details(journal_error)
            raise
        else:
            record["temporary_cleanup"] = "COMPLETE"
            record["temporary_directory_exists_after_cleanup"] = False
            record["cleanup"] = record["process_cleanup"]
            try:
                # COMPLETE may only be persisted after filesystem cleanup.
                _persist_process_observation(record)
            except (OSError, ValueError) as journal_error:
                record["cleanup_journal_exception"] = _exception_details(journal_error)
                raise
            return result


def _open_process_stream(path: Path):
    """Open one process stream with delete sharing on Windows.

    The certifier closes its own Python streams before TemporaryDirectory cleanup,
    but the Windows launcher/child receive duplicated standard handles. A process
    can be terminated while a duplicated file handle is still completing kernel
    teardown. Opening the original stream with FILE_SHARE_DELETE makes that late
    inherited handle compatible with unlink/rename; it does not delete anything,
    retry cleanup, wait, or convert a cleanup error into PASS.
    """
    if os.name != "nt":
        return path.open("w+b")

    import ctypes
    import msvcrt
    from ctypes import wintypes as w

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.restype = w.HANDLE
    kernel32.CreateFileW.argtypes = [
        w.LPCWSTR, w.DWORD, w.DWORD, ctypes.c_void_p,
        w.DWORD, w.DWORD, w.HANDLE,
    ]
    kernel32.CloseHandle.restype = w.BOOL
    kernel32.CloseHandle.argtypes = [w.HANDLE]

    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    FILE_SHARE_DELETE = 0x00000004
    CREATE_ALWAYS = 2
    FILE_ATTRIBUTE_NORMAL = 0x00000080
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    handle = kernel32.CreateFileW(
        str(path),
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )
    if handle == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())

    flags = os.O_RDWR | getattr(os, "O_BINARY", 0)
    try:
        fd = msvcrt.open_osfhandle(int(handle), flags)
    except (OSError, ValueError):
        kernel32.CloseHandle(handle)
        raise
    try:
        return os.fdopen(fd, "w+b")
    except BaseException:
        os.close(fd)
        raise


def _run(command: Sequence[str]) -> tuple[int, str, float]:
    """Compatibility tuple; full observed metadata is appended to processes.json.

    124/125/130 are conventions for timeout/infrastructure/interruption, never
    fabricated observed child exits. File-backed streams preserve partial output.
    """
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    timeout = GIT_TIMEOUT_SECONDS if Path(command[0]).stem.lower() == "git" else STEP_TIMEOUT_SECONDS
    start = time.monotonic()
    record = {"invocation_id": uuid.uuid4().hex, "command": list(command), "cwd": str(REPO_ROOT), "started_at_utc": _utc(),
              "started_monotonic": start, "timeout_seconds": timeout, "pid": None,
              "spawn_attempted": False, "command_started": False,
              "observed_exit_code": None, "result": "STARTING", "cleanup": "NOT_STARTED"}
    PROCESS_RECORDS.append(record)
    _persist_process_observation(record)  # Must work before attempting a process start.
    process = None
    job = None
    code = 125
    pending_exit = None
    with _ProcessTemporaryDirectory(record) as temporary:
        path = Path(temporary)
        with _open_process_stream(path / "stdout") as stdout, _open_process_stream(path / "stderr") as stderr:
            try:
                kwargs = {"cwd": REPO_ROOT, "stdout": stdout, "stderr": stderr, "env": env}
                if os.name == "nt":
                    job = _WindowsJob()
                    launcher = [sys.executable, "-B", "-c", _WINDOWS_LAUNCHER, json.dumps(list(command)), str(path / "child.json")]
                    record["spawn_attempted"] = True
                    process = subprocess.Popen(launcher, stdin=subprocess.PIPE, **kwargs)
                    record["launcher_pid"] = process.pid
                    job.assign(process)
                    # Releasing the launcher permits a child; only its metadata
                    # can confirm whether the requested command actually started.
                    record["command_started"] = None
                    process.stdin.write(b"1"); process.stdin.close()
                else:
                    record["spawn_attempted"] = True
                    process = subprocess.Popen(list(command), stdin=subprocess.DEVNULL, start_new_session=True, **kwargs)
                    record["pid"] = process.pid
                    record["command_started"] = True
                record["result"] = "RUNNING"
                _persist_process_observation(record)
                code = process.wait(timeout=max(0.001, timeout - (time.monotonic() - start)))
                record["observed_exit_code"] = code
                record["result"] = "EXITED"
            except subprocess.TimeoutExpired:
                code = 124; record["result"] = "TIMEOUT"
            except KeyboardInterrupt:
                code = 130; record["result"] = "INTERRUPTED"
                record["interruption_exit_code"] = 130
            except SystemExit as exc:
                code = 130; record["result"] = "INTERRUPTED"; pending_exit = exc
                record["interruption_exit_code"] = _interruption_exit(exc)
            except OSError as exc:
                code = 125; record["result"] = "INFRASTRUCTURE_ERROR"; record["error"] = repr(exc)
            finally:
                try:
                    if job is not None:
                        job.terminate()
                        try:
                            record["windows_job_after_terminate"] = job.snapshot()
                        except Exception as diagnostic_error:
                            record["windows_job_after_terminate"] = {
                                "status": "UNOBSERVABLE",
                                "error": _exception_details(diagnostic_error),
                            }
                    elif process is not None:
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    if process is not None:
                        # Assignment can fail while the launcher is still waiting.
                        if process.poll() is None:
                            process.kill()
                        record["exit_after_cleanup"] = process.wait(timeout=CLEANUP_TIMEOUT_SECONDS)
                    if os.name != "nt" and process is not None:
                        until = time.monotonic() + CLEANUP_TIMEOUT_SECONDS
                        while _posix_group_alive(process.pid):
                            if time.monotonic() >= until:
                                raise OSError("process group still active after cleanup deadline")
                            time.sleep(0.02)
                    record["cleanup"] = "COMPLETE"
                except (OSError, subprocess.TimeoutExpired) as exc:
                    record["cleanup"] = "FAILED"; record["cleanup_error"] = repr(exc); code = 125
                finally:
                    if job is not None:
                        try:
                            record["windows_job_before_close"] = job.snapshot()
                        except Exception as diagnostic_error:
                            record["windows_job_before_close"] = {
                                "status": "UNOBSERVABLE",
                                "error": _exception_details(diagnostic_error),
                            }
                        try:
                            job.close()
                        except OSError as exc:
                            record["cleanup"] = "FAILED"; record["cleanup_error"] = repr(exc); code = 125
                    if process is not None and process.stdin is not None and not process.stdin.closed:
                        process.stdin.close()
                if os.name == "nt":
                    try:
                        metadata = path / "child.json"
                        if not metadata.exists():
                            raise ValueError("launcher metadata missing")
                        child = json.loads(metadata.read_text(encoding="utf8"))
                        if not isinstance(child, dict):
                            raise ValueError("launcher metadata must be an object")
                        if set(child) == {"pid"} and type(child["pid"]) is int and child["pid"] > 0:
                            record["pid"] = child["pid"]
                            record["command_started"] = True
                        elif set(child) == {"start_error"} and isinstance(child["start_error"], str) and child["start_error"]:
                            record["start_error"] = child["start_error"]
                            record["command_started"] = False
                            record["result"] = "START_ERROR"; record["observed_exit_code"] = None; code = 125
                        else:
                            raise ValueError("launcher metadata requires positive pid or start_error")
                    except (OSError, UnicodeError, ValueError) as exc:
                        # An unobservable child can never certify a successful gate.
                        # Preserve timeout/interruption classification and partial streams.
                        record["metadata_error"] = repr(exc)
                        if record["result"] == "EXITED":
                            record["result"] = "INFRASTRUCTURE_ERROR"
                            record["observed_exit_code"] = None
                            code = 125
                stdout.seek(0); stderr.seek(0)
                raw_stdout, raw_stderr = stdout.read(), stderr.read()
                record["stdout"], record["stderr"] = _decode(raw_stdout), _decode(raw_stderr)
                try:
                    raw_stdout.decode("utf-8"); raw_stderr.decode("utf-8")
                    record["utf8_valid"] = True
                except UnicodeDecodeError:
                    record["utf8_valid"] = False
                record["ended_at_utc"] = _utc()
                record["ended_monotonic"] = time.monotonic()
                record["conventional_exit_code"] = code
                record["process_cleanup"] = record["cleanup"]
                if record["cleanup"] == "COMPLETE":
                    record["cleanup"] = "PENDING"  # TemporaryDirectory has not exited yet.
                _persist_process_observation(record)
        # We are outside the stdout/stderr context but still inside the process
        # TemporaryDirectory. This proves whether the certifier's own Python file
        # objects were already closed immediately before directory cleanup.
        record["parent_streams_before_temporary_exit"] = {
            "observed_at_utc": _utc(),
            "monotonic_ns": time.monotonic_ns(),
            "stdout_closed": bool(stdout.closed),
            "stderr_closed": bool(stderr.closed),
            "stdout_name": str(path / "stdout"),
            "stderr_name": str(path / "stderr"),
        }
        _persist_process_observation(record)
    if pending_exit is not None:
        raise pending_exit
    return code, record["stdout"] + record["stderr"], time.monotonic() - start


def _run_render_diff_gate() -> tuple[int, str, float]:
    """Exact parity is independent of whether the generated output is tracked."""
    return _run([sys.executable, "tools/render_simulado.py", "--check"])


def _git_output(*args: str) -> str | None:
    previous = len(PROCESS_RECORDS)
    code, output, _ = _run(["git", *args])
    record = PROCESS_RECORDS[-1] if len(PROCESS_RECORDS) > previous else None
    if record is not None and record.get("result") == "INTERRUPTED":
        raise KeyboardInterrupt()  # Optional Git metadata cannot swallow cancellation.
    if code != 0 or (record is not None and not record.get("utf8_valid", False)):
        return None
    # stderr is retained separately as evidence, never mixed into Git data.
    return str(record["stdout"]).rstrip("\r\n") if record is not None else output.rstrip("\r\n")


def _git_state() -> GitState:
    head = _git_output("rev-parse", "--verify", "HEAD")
    branch = _git_output("branch", "--show-current")
    origin_main = _git_output("rev-parse", "--verify", "origin/main")
    merge_base = _git_output("merge-base", head, origin_main) if head and origin_main else None
    status = _git_output("-c", "core.quotepath=true", "status", "--porcelain=v1", "--untracked-files=all")
    errors = []
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head or ""):
        errors.append("HEAD_UNOBSERVABLE_OR_INVALID")
    if any(r.get("cleanup") == "FAILED" for r in PROCESS_RECORDS):
        errors.append("PROCESS_CLEANUP_FAILED")
    if status is None:
        errors.append("STATUS_UNOBSERVABLE")
    elif any(len(line) < 4 or line[0] not in " MADRCU?!" or line[1] not in " MADRCU?!" or line[2] != " " for line in status.splitlines()):
        errors.append("STATUS_INVALID")
    return GitState(head, branch or None, origin_main, merge_base, status or "", tuple(errors))


def _last_nonempty_line(text: str) -> str:
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()[:240]
    return ""


def _step_process(previous: int, command: Sequence[str]) -> dict[str, object] | None:
    # Both a normal gate and render_diff invoke exactly one process. Bind its
    # record by this call's boundary and requested argv, never the last Git read.
    if len(PROCESS_RECORDS) == previous + 1:
        record = PROCESS_RECORDS[previous]
        if record.get("command") == list(command):
            return dict(record)
    return None


def _interruption_exit(exc: SystemExit) -> int:
    # Help/parsing happen before the campaign's try block. Inside a campaign,
    # zero/None mean cancellation, not success; preserve ordinary nonzero exits.
    if exc.code is None or exc.code == 0:
        return 130
    return exc.code if isinstance(exc.code, int) else 1


def _reject_aliases(target: Path) -> None:
    for item in (target, *target.parents):
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ValueError("evidence-dir não pode atravessar symlink/junction")


def _resolve_evidence_dir(raw: str | None, head_sha: str | None) -> Path:
    if raw:
        supplied = Path(raw).expanduser()
        if ".." in supplied.parts:
            raise ValueError("evidence-dir não aceita componentes ..")
        target = Path(os.path.abspath(supplied))
    else:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        target = DEFAULT_EVIDENCE_ROOT / f"{timestamp}_{(head_sha or 'unknown')[:12]}_{uuid.uuid4().hex}"
    _reject_aliases(target)
    target = target.resolve()
    root = REPO_ROOT.resolve()
    if target == root or target.is_relative_to(root):
        raise ValueError("evidence-dir deve ficar fora da árvore do repositório")
    return target


def _reserve_evidence(target: Path) -> None:
    _reject_aliases(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir()  # Atomic exclusive acquisition; existing even empty is rejected.
    _reject_aliases(target)
    stat = target.stat()
    RESERVATIONS[target] = (stat.st_dev, stat.st_ino)


def _assert_reserved(target: Path) -> None:
    _reject_aliases(target)
    stat = target.stat()
    if RESERVATIONS.get(target) != (stat.st_dev, stat.st_ino):
        raise OSError("evidence reservation missing or replaced")


def _write_json(path: Path, payload: object) -> None:
    _reject_aliases(path.parent)
    if path.exists() and (path.is_symlink() or path.stat().st_nlink > 1):
        raise OSError("evidence file aliases another object")
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    with temporary.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def _filtered_steps(profile: str, skip_render: bool) -> list[tuple[str, list[str]]]:
    steps = list(PROFILE_STEPS[profile])
    if not skip_render:
        return steps
    return [
        item
        for item in steps
        if item[0] not in {"render_simulado", "render_diff"}
    ]


def _persist_bundle(
    evidence_dir: Path | None,
    summary: dict[str, object],
    results: list[StepResult],
) -> None:
    if evidence_dir is None:
        return
    _assert_reserved(evidence_dir)
    _write_json(
        evidence_dir / "environment.json",
        {
            "python": sys.version,
            "platform": platform.platform(),
            "executable": sys.executable,
            "cwd": str(REPO_ROOT),
        },
    )
    _write_json(
        evidence_dir / "commands.json",
        [{"name": result.name, "command": result.command} for result in results],
    )
    # Summary is the final essential write, so incomplete bundles cannot retain PASS.
    _write_json(evidence_dir / "summary.json", summary)


def _build_summary(
    *, profile: str, scope: str, before: GitState, after: GitState,
    results: list[StepResult], expected_steps: list[str] | None = None,
    allow_dirty: bool = False, infrastructure_errors: list[str] | None = None,
) -> dict[str, object]:
    expected = expected_steps if expected_steps is not None else [name for name, _ in PROFILE_STEPS[profile]]
    failed_steps = [result for result in results if result.exit_code != 0]
    # Existing failure_count remains the number of failed steps. Explicit gate
    # exits and infrastructure failures are additionally counted separately.
    failures = failed_steps
    gate_failures = [r for r in failed_steps if r.process is None or (
        r.process.get("result") == "EXITED" and (
            r.process.get("cleanup") == "COMPLETE" or
            (type(r.process.get("observed_exit_code")) is int and r.process["observed_exit_code"] != 0)
        )
    )]
    errors = list(infrastructure_errors or [])
    if not before.valid: errors.append("INITIAL_GIT_UNOBSERVABLE")
    if not after.valid: errors.append("FINAL_GIT_UNOBSERVABLE")
    if before.head_sha != after.head_sha: errors.append("HEAD_CHANGED")
    if not allow_dirty and (not before.clean or not after.clean): errors.append("WORKTREE_NOT_CLEAN")
    if not expected or [result.name for result in results] != expected: errors.append("INCOMPLETE_STEP_COVERAGE")
    for result in results:
        if result.status != "PASS" and result.exit_code == 0:
            errors.append("INCONSISTENT_STEP_RESULT")
        if result.process and (result.process.get("cleanup") != "COMPLETE" or result.process.get("result") != "EXITED"):
            errors.append("PROCESS_INFRASTRUCTURE_FAILURE:" + result.name)
    errors = list(dict.fromkeys(errors))
    return {
        "schema_version": "1.0", "generated_at_utc": _utc(), "profile": profile,
        "certification_scope": scope, "LOCAL_CERTIFICATION": "FAIL" if failures or errors else "PASS",
        "DERIVED_STALE": any(r.name == "render_diff" and r.exit_code != 0 for r in results),
        "GITHUB_ACTIONS": "NOT_EVALUATED_BY_LOCAL_CERTIFIER",
        "databricks_free": "NOT_EVALUATED_BY_LOCAL_CERTIFIER",
        "synthetic_agent_screening": "NOT_EVALUATED_BY_LOCAL_CERTIFIER",
        "environment": {"python": sys.version, "platform": platform.platform(), "executable": sys.executable},
        "git_before": asdict(before), "git_after": asdict(after),
        "steps": [asdict(result) for result in results], "failure_count": len(failures),
        "gate_failure_count": len(gate_failures),
        "scope_complete": bool(expected) and [r.name for r in results] == expected,
        "infrastructure_errors": errors, "infrastructure_error_count": len(errors),
        # Absence of launcher metadata is unknown, not proof of a failed start.
        # Legacy results without this observation retain compatibility semantics.
        "expected_steps": expected, "not_started_steps": [n for n in expected if n not in {
            r.name for r in results if r.process is None or r.process.get("command_started") is not False
        }],
        "unknown_start_steps": [r.name for r in results if r.process is not None
                                and "command_started" in r.process and r.process["command_started"] is None],
        "diagnostic_allow_dirty": allow_dirty,
        "release_clean_certification": not allow_dirty and scope == f"FULL_{profile.upper()}_LOCAL" and not failures and not errors,
        "timeout_policy": {"git_process_seconds": GIT_TIMEOUT_SECONDS, "gate_process_seconds": STEP_TIMEOUT_SECONDS,
                           "cleanup_seconds": CLEANUP_TIMEOUT_SECONDS, "campaign_deadline": None},
    }


def _scope(profile: str, skip_render: bool, allow_dirty: bool = False) -> str:
    if allow_dirty:
        return f"DIAGNOSTIC_{profile.upper()}" + ("_NO_RENDER" if skip_render else "")
    return f"PARTIAL_{profile.upper()}_NO_RENDER" if skip_render else f"FULL_{profile.upper()}_LOCAL"


def _positive_seconds(value: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("timeout deve ser positivo e finito")
    return number


def main(argv: list[str] | None = None) -> int:
    global GIT_TIMEOUT_SECONDS, STEP_TIMEOUT_SECONDS, ACTIVE_EVIDENCE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(PROFILE_STEPS), default="se02")
    parser.add_argument("--evidence-dir", help="Diretório externo NOVO, reservado exclusivamente pela execução.")
    parser.add_argument("--no-evidence", action="store_true")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true", help="Diagnóstico; nunca certificação limpa de release.")
    parser.add_argument("--git-timeout-seconds", type=_positive_seconds, default=30.0)
    parser.add_argument("--step-timeout-seconds", type=_positive_seconds, default=900.0)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)
    GIT_TIMEOUT_SECONDS, STEP_TIMEOUT_SECONDS = args.git_timeout_seconds, args.step_timeout_seconds
    PROCESS_RECORDS.clear()
    ACTIVE_EVIDENCE = None
    evidence_dir = None
    results: list[StepResult] = []
    errors: list[str] = []
    expected = _filtered_steps(args.profile, args.skip_render)
    before = GitState(None, None, None, None, "", ("NOT_OBSERVED",))
    after = before
    scope = _scope(args.profile, args.skip_render, args.allow_dirty)
    interrupted = False
    interruption_exit = 130
    try:
        if not args.no_evidence:
            evidence_dir = _resolve_evidence_dir(args.evidence_dir, None)
            _reserve_evidence(evidence_dir)
            ACTIVE_EVIDENCE = evidence_dir
        before = _git_state()
        print("== SKILL ENFORCEMENT LOCAL CERTIFICATION ==")
        print(f"profile={args.profile} HEAD={before.head_sha} scope={scope}")
        if not before.valid or (not args.allow_dirty and not before.clean):
            errors.append("PRECHECK_GIT_FAILED_NO_MUTABLE_STEPS")
            scope = "PRECHECK_ONLY"
        else:
            if evidence_dir is not None:
                (evidence_dir / "logs").mkdir()
            for index, (name, command) in enumerate(expected, 1):
                print(f"-- {index:02d} {name}", flush=True)
                previous = len(PROCESS_RECORDS)
                try:
                    code, output, duration = _run_render_diff_gate() if name == "render_diff" else _run(command)
                except (OSError, ValueError, KeyboardInterrupt, SystemExit):
                    process = _step_process(previous, command)
                    if process is not None:
                        # Preserve the invocation even when _run cannot return:
                        # STARTING is an attempt, not an observed child execution.
                        code = process.get("conventional_exit_code", 125)
                        output = str(process.get("stdout", "")) + str(process.get("stderr", ""))
                        duration = process.get("ended_monotonic", time.monotonic()) - process["started_monotonic"]
                        results.append(StepResult(name, list(command), code, round(duration, 4),
                                                  "PASS" if code == 0 else "FAIL", _last_nonempty_line(output), None, process))
                    raise
                process = _step_process(previous, command)
                log_file = None
                status = "PASS" if code == 0 else "FAIL"
                # Record the observed step before essential log persistence can fail.
                results.append(StepResult(name, list(command), code, round(duration, 4), status, _last_nonempty_line(output), None, process))
                if evidence_dir is not None:
                    _assert_reserved(evidence_dir)
                    target = evidence_dir / "logs" / f"{index:02d}_{name}.log"
                    _reject_aliases(target.parent)
                    with target.open("x", encoding="utf-8", newline="\n") as stream:
                        stream.write(output)
                    log_file = str(target)
                results[-1] = StepResult(name, list(command), code, round(duration, 4), status, _last_nonempty_line(output), log_file, process)
                if args.verbose or code != 0: print(output.rstrip())
                print(f"   {status} ({duration:.2f}s) {_last_nonempty_line(output)}")
                if process and (process.get("result") != "EXITED" or process.get("cleanup") != "COMPLETE"):
                    errors.append("PROCESS_ABORTED:" + name)
                    interrupted = process.get("result") == "INTERRUPTED"
                    break
        after = _git_state()
    except KeyboardInterrupt:
        interrupted = True; errors.append("INTERRUPTED")
    except SystemExit as exc:
        interrupted = True; interruption_exit = _interruption_exit(exc)
        errors.append("INTERRUPTED:SystemExit:" + repr(exc.code))
    except (OSError, ValueError) as exc:
        errors.append("INFRASTRUCTURE_ERROR:" + repr(exc))
        # PROCESS_RECORDS is reset for this campaign. The last invocation owns
        # the failure boundary: cleanup/journal errors must not mask its cancel.
        observed = PROCESS_RECORDS[-1] if PROCESS_RECORDS else None
        if observed is not None and observed.get("result") == "INTERRUPTED":
            interrupted = True
            interruption_exit = observed.get("interruption_exit_code", 130)
            errors.append("INTERRUPTED_WITH_INFRASTRUCTURE_ERROR")
        print("FAIL infrastructure:", exc, file=sys.stderr)
    finally:
        summary = _build_summary(profile=args.profile, scope=scope, before=before, after=after, results=results,
                                 expected_steps=[name for name, _ in expected], allow_dirty=args.allow_dirty, infrastructure_errors=errors)
        # A failed reservation must never touch the existing winner's namespace.
        if evidence_dir is not None and ACTIVE_EVIDENCE == evidence_dir:
            try:
                _persist_bundle(evidence_dir, summary, results)
            except (OSError, ValueError, KeyboardInterrupt, SystemExit) as exc:
                if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                    interrupted = True
                    interruption_exit = _interruption_exit(exc) if isinstance(exc, SystemExit) else 130
                summary["LOCAL_CERTIFICATION"] = "FAIL"
                summary["release_clean_certification"] = False
                summary["infrastructure_errors"].append("PERSISTENCE_FAILED:" + repr(exc))
                summary["infrastructure_error_count"] = len(summary["infrastructure_errors"])
                print("FAIL essential persistence:", exc, file=sys.stderr)
        ACTIVE_EVIDENCE = None
    print("LOCAL_CERTIFICATION =", summary["LOCAL_CERTIFICATION"])
    print("scope =", scope)
    print("infrastructure_errors =", summary["infrastructure_errors"])
    if evidence_dir is not None: print("evidence:", evidence_dir)
    if interrupted: return interruption_exit
    return 0 if summary["LOCAL_CERTIFICATION"] == "PASS" else (2 if summary["infrastructure_errors"] else 1)


if __name__ == "__main__":
    raise SystemExit(main())
