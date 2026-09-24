from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


def _resource_snapshot(root: Path) -> dict[str, Any]:
    disk = shutil.disk_usage(root)
    row: dict[str, Any] = {
        "logical_cpus": os.cpu_count(),
        "disk_total_bytes": disk.total,
        "disk_free_bytes": disk.free,
        "memory_total_bytes": None,
        "memory_available_bytes": None,
    }
    if os.name == "nt":
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                row["memory_total_bytes"] = int(status.ullTotalPhys)
                row["memory_available_bytes"] = int(status.ullAvailPhys)
        except (OSError, AttributeError, ValueError):
            pass
    else:
        try:
            page = os.sysconf("SC_PAGE_SIZE")
            total_pages = os.sysconf("SC_PHYS_PAGES")
            avail_pages = os.sysconf("SC_AVPHYS_PAGES")
            row["memory_total_bytes"] = int(page * total_pages)
            row["memory_available_bytes"] = int(page * avail_pages)
        except (AttributeError, OSError, ValueError):
            pass
    return row


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _max_parallel(summary: Mapping[str, Any]) -> int:
    events: list[tuple[datetime, int]] = []
    for row in (summary.get("results") or {}).values():
        if row.get("status") not in {"PASS", "FAIL"} or not row.get("command_records"):
            continue
        events.append((_parse_time(row["started_at_utc"]), 1))
        events.append((_parse_time(row["ended_at_utc"]), -1))
    active = 0
    peak = 0
    for _, delta in sorted(events, key=lambda item: (item[0], item[1])):
        active += delta
        peak = max(peak, active)
    return peak


def _windows_job_object_ok(*summaries: Mapping[str, Any]) -> bool:
    records = []
    for summary in summaries:
        for row in (summary.get("results") or {}).values():
            records.extend(row.get("command_records") or [])
    if os.name != "nt":
        return True
    started = [r for r in records if r.get("command_started") is True]
    return bool(started) and all(
        r.get("supervision") == "WINDOWS_JOB_OBJECT"
        and r.get("timed_out") is False
        and r.get("residual_descendants_detected") is False
        and r.get("cleanup") in {"COMPLETE", "COMPLETE_ALREADY_EXITED"}
        for r in started
    )


def qualify(
    root: Path,
    host: Mapping[str, Any],
    sandbox_probe: Mapping[str, Any],
    selective_summary: Mapping[str, Any],
    global_summary: Mapping[str, Any],
) -> dict[str, Any]:
    filesystem_ok = host.get("os") != "Windows" or (host.get("filesystem") or {}).get("type") == "NTFS"
    sandbox_ok = sandbox_probe.get("status") == "PASS" and all(
        sandbox_probe.get(key) is True
        for key in (
            "scratch_write_allowed",
            "outside_write_blocked",
            "subprocess_blocked",
            "network_blocked",
            "credential_sentinel_absent",
        )
    )
    job_ok = _windows_job_object_ok(selective_summary, global_summary)
    selective_peak = _max_parallel(selective_summary)
    global_peak = _max_parallel(global_summary)
    initial_parallelism_ok = max(selective_peak, global_peak) >= 2
    resources = _resource_snapshot(root)
    resource_observation_ok = (
        type(resources.get("logical_cpus")) is int and resources["logical_cpus"] > 0
        and type(resources.get("disk_free_bytes")) is int and resources["disk_free_bytes"] > 0
        and type(resources.get("memory_total_bytes")) is int and resources["memory_total_bytes"] > 0
        and type(resources.get("memory_available_bytes")) is int and resources["memory_available_bytes"] > 0
    )
    checks = {
        "filesystem_ntfs_or_not_windows": filesystem_ok,
        "sandbox_negative_probe": sandbox_ok,
        "windows_job_object": job_ok,
        "resource_observation_complete": resource_observation_ok,
        "initial_parallelism_2_1_observed": initial_parallelism_ok,
    }
    return {
        "schema_version": "SER-B0-HOST-QUALIFICATION-1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "filesystem": host.get("filesystem"),
        "sandbox_probe": dict(sandbox_probe),
        "resource_snapshot": resources,
        "observed_peak_parallel": {
            "selective": selective_peak,
            "global": global_peak,
        },
        "initial_profile": {
            "max_parallel": 2,
            "max_auditors": 1,
            "status": "QUALIFIED_BY_OBSERVED_PILOTS" if initial_parallelism_ok else "NOT_QUALIFIED",
        },
        "post_pilot_candidate_3_2": "NOT_QUALIFIED_REQUIRES_SEPARATE_HEADROOM_MEASUREMENT",
        "sandbox_scope": "PYTHON_AUDIT_HOOK_ALLOWLISTED_PYTHON_TASKS_ONLY",
        "host_coordination": "SINGLE_LAUNCHER_OS_LEASE",
        "client_model_configuration": host.get("client_model_configuration"),
    }
