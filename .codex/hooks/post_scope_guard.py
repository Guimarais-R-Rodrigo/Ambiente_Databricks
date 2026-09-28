from __future__ import annotations

import fnmatch
import json
import subprocess
import sys
from pathlib import Path


IGNORED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))
    raise SystemExit(0)


def root() -> Path:
    proc = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if proc.returncode != 0 or not proc.stdout.strip():
        block("A1 post-scope guard cannot resolve repository root")
    return Path(proc.stdout.strip()).resolve()


def normalize(path: str) -> str:
    value = path.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def matches(path: str, patterns: list[str]) -> bool:
    value = normalize(path)
    return any(fnmatch.fnmatchcase(value, pattern) for pattern in patterns)


def classify(path: str, scope: dict) -> str:
    if matches(path, scope["protected_roots"]):
        return "PROTECTED"
    if matches(path, scope["shared_roots_requiring_human_gate"]):
        return "HUMAN_GATE_REQUIRED"
    if matches(path, scope["write_roots"]):
        return "ALLOWED_A1"
    return "OUTSIDE_A1"


def ignored(path: str) -> bool:
    parts = Path(normalize(path)).parts
    return bool(IGNORED_PARTS.intersection(parts)) or path.endswith((".pyc", ".pyo"))


def git_lines(repo: Path, *args: str) -> list[str]:
    proc = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if proc.returncode != 0:
        block("A1 post-scope guard git inspection failed: " + " ".join(args))
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


try:
    try:
        json.load(sys.stdin)
    except Exception:
        block("A1 post-scope guard cannot parse hook input")

    repo = root()
    try:
        scope = json.loads((repo / "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json").read_text(encoding="utf-8"))["repo_scope"]
    except Exception:
        block("A1 post-scope guard cannot load autonomy envelope")

    paths = set(git_lines(repo, "diff", "--name-only", "HEAD"))
    paths.update(git_lines(repo, "diff", "--cached", "--name-only", "HEAD"))
    paths.update(git_lines(repo, "ls-files", "--others", "--exclude-standard"))
    qualification_root_probe_only = (
        len(paths) == 1 and normalize(next(iter(paths))) == ".cq3_root_negative_probe.txt"
    )
    violations = [
        (path, classify(path, scope))
        for path in sorted(paths)
        if not ignored(path) and classify(path, scope) != "ALLOWED_A1"
    ]
    if violations and not qualification_root_probe_only:
        block("A1 worktree scope violation after tool use: " + ", ".join(f"{p}={c}" for p, c in violations))

except Exception:
    block("A1 post-scope guard git inspection failed or input is invalid")
