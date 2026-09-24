from __future__ import annotations

import hashlib
import json
import os
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
            h.update(b"MISSING\0"); continue
        if p.is_symlink():
            h.update(b"SYMLINK\0" + os.readlink(p).encode("utf-8", "surrogateescape") + b"\0"); continue
        if p.is_file():
            h.update(b"FILE\0" + hashlib.sha256(p.read_bytes()).digest()); continue
        h.update(b"DIR\0")
        for child in sorted(x for x in p.rglob("*") if x.is_file() or x.is_symlink()):
            child_rel = child.relative_to(root).as_posix()
            h.update(child_rel.encode("utf-8") + b"\0")
            if child.is_symlink():
                h.update(b"L\0" + os.readlink(child).encode("utf-8", "surrogateescape") + b"\0")
            else:
                h.update(hashlib.sha256(child.read_bytes()).digest())
    return h.hexdigest()

def run_argv(argv: list[str], evidence_dir: Path, name: str, *, timeout: float = 120.0) -> dict:
    if not argv or any(not isinstance(x, str) or not x for x in argv):
        raise ValueError("ARGV_INVALID")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    started = _utc(); t0 = time.monotonic()
    env = {
        "PATH": os.environ.get("PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        "WINDIR": os.environ.get("WINDIR", ""),
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    env = {k: v for k, v in env.items() if v}
    timed_out = False
    try:
        p = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, timeout=timeout, shell=False)
        code = p.returncode
        stdout = (p.stdout or b"").decode("utf-8", errors="replace")
        stderr = (p.stderr or b"").decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired as exc:
        timed_out = True; code = 124
        stdout = (exc.stdout or b"").decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else str(exc.stdout or "")
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else str(exc.stderr or "")
    ended = _utc()
    prefix = evidence_dir / name
    prefix.with_suffix(".stdout.txt").write_text(stdout, encoding="utf-8")
    prefix.with_suffix(".stderr.txt").write_text(stderr, encoding="utf-8")
    row = {
        "name": name, "argv": argv, "exit_code": code, "timed_out": timed_out,
        "duration_seconds": time.monotonic() - t0, "started_at_utc": started, "ended_at_utc": ended,
        "stdout_sha256": hashlib.sha256(stdout.encode("utf-8")).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode("utf-8")).hexdigest(),
    }
    prefix.with_suffix(".json").write_text(json.dumps(row, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return row
