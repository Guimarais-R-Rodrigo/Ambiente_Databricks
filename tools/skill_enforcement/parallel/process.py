from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

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


def _clean_env() -> dict[str, str]:
    allowed = {
        "PATH": os.environ.get("PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        "WINDIR": os.environ.get("WINDIR", ""),
        "TEMP": os.environ.get("TEMP", ""),
        "TMP": os.environ.get("TMP", ""),
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    return {key: value for key, value in allowed.items() if value}


def _terminate_tree(process: subprocess.Popen[bytes]) -> str:
    if process.poll() is not None:
        return "COMPLETE_ALREADY_EXITED"
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                capture_output=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            try:
                process.kill()
            except OSError:
                pass
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except OSError:
            pass
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except OSError:
                pass
    try:
        process.wait(timeout=10)
        return "COMPLETE"
    except (subprocess.TimeoutExpired, OSError):
        return "INCOMPLETE"


def _evidence_path(evidence_dir: Path, name: str, suffix: str) -> Path:
    if not name or any(sep in name for sep in ("/", "\\")) or name in {".", ".."}:
        raise ValueError("EVIDENCE_NAME_INVALID")
    return evidence_dir / f"{name}{suffix}"


def _persist_record(evidence_dir: Path, name: str, stdout_b: bytes, stderr_b: bytes, row: dict) -> None:
    # RAW means exact child bytes: do not decode/re-encode and do not let the
    # platform translate newlines on Windows.
    _evidence_path(evidence_dir, name, ".stdout.txt").write_bytes(stdout_b)
    _evidence_path(evidence_dir, name, ".stderr.txt").write_bytes(stderr_b)
    _evidence_path(evidence_dir, name, ".json").write_bytes(
        (json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    )


def run_argv(
    argv: list[str],
    evidence_dir: Path,
    name: str,
    *,
    timeout: float = 120.0,
    command_id: str | None = None,
    argv_template: list[str] | None = None,
) -> dict:
    if not argv or any(not isinstance(x, str) or not x for x in argv):
        raise ValueError("ARGV_INVALID")
    if timeout <= 0 or not isinstance(timeout, (int, float)):
        raise ValueError("TIMEOUT_INVALID")
    if command_id is not None and (not isinstance(command_id, str) or not command_id):
        raise ValueError("COMMAND_ID_INVALID")
    if argv_template is not None and (
        not isinstance(argv_template, list)
        or not argv_template
        or any(not isinstance(x, str) or not x for x in argv_template)
    ):
        raise ValueError("ARGV_TEMPLATE_INVALID")

    evidence_dir.mkdir(parents=True, exist_ok=True)
    started = _utc()
    t0 = time.monotonic()
    flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    try:
        process = subprocess.Popen(
            argv,
            cwd=ROOT,
            env=_clean_env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            start_new_session=(os.name != "nt"),
            creationflags=flags,
        )
    except OSError as exc:
        stdout_b = b""
        stderr_b = str(exc).encode("utf-8", errors="surrogateescape")
        row = {
            "name": name,
            "command_id": command_id,
            "argv_template": argv_template,
            "argv": argv,
            "command_started": False,
            "pid": None,
            "exit_code": 125,
            "timed_out": False,
            "cleanup": "NOT_STARTED",
            "duration_seconds": time.monotonic() - t0,
            "started_at_utc": started,
            "ended_at_utc": _utc(),
            "stdout_sha256": hashlib.sha256(stdout_b).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr_b).hexdigest(),
            "spawn_error": f"{type(exc).__name__}:{exc}",
        }
        _persist_record(evidence_dir, name, stdout_b, stderr_b, row)
        return row

    timed_out = False
    cleanup = "COMPLETE_ALREADY_EXITED"
    try:
        stdout_b, stderr_b = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        cleanup = _terminate_tree(process)
        try:
            stdout_b, stderr_b = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            stdout_b, stderr_b = b"", b"cleanup did not finish"

    stdout_b = stdout_b or b""
    stderr_b = stderr_b or b""
    code = process.returncode if process.returncode is not None else 124
    if timed_out and code == 0:
        code = 124
    row = {
        "name": name,
        "command_id": command_id,
        "argv_template": argv_template,
        "argv": argv,
        "command_started": True,
        "pid": process.pid,
        "exit_code": int(code),
        "timed_out": timed_out,
        "cleanup": cleanup,
        "duration_seconds": time.monotonic() - t0,
        "started_at_utc": started,
        "ended_at_utc": _utc(),
        "stdout_sha256": hashlib.sha256(stdout_b).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr_b).hexdigest(),
    }
    _persist_record(evidence_dir, name, stdout_b, stderr_b, row)
    return row
