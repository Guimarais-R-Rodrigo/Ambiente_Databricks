from __future__ import annotations

import fnmatch
import json
import subprocess
from pathlib import Path


IGNORED_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def root() -> Path:
    p = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(0)
    return Path(p.stdout.strip())


def load_scope(repo: Path) -> dict:
    return json.loads(
        (repo / "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json").read_text(encoding="utf-8")
    )["repo_scope"]


def matches(path: str, patterns: list[str]) -> bool:
    value = path.replace("\\", "/").lstrip("./")
    return any(fnmatch.fnmatchcase(value, pat) for pat in patterns)


def classify(path: str, scope: dict) -> str:
    if matches(path, scope["protected_roots"]):
        return "PROTECTED"
    if matches(path, scope["shared_roots_requiring_human_gate"]):
        return "HUMAN_GATE_REQUIRED"
    if matches(path, scope["write_roots"]):
        return "ALLOWED_A1"
    return "OUTSIDE_A1"


def ignored(path: str) -> bool:
    parts = set(path.replace("\\", "/").split("/"))
    return bool(parts & IGNORED_PARTS) or path.endswith((".pyc", ".pyo"))


repo = root()
commands = [
    ["git", "diff", "--name-only", "HEAD"],
    ["git", "diff", "--cached", "--name-only", "HEAD"],
    ["git", "ls-files", "--others", "--exclude-standard"],
]
paths: set[str] = set()
for argv in commands:
    p = subprocess.run(argv, cwd=repo, capture_output=True, text=True)
    if p.returncode == 0:
        paths.update(line.strip() for line in p.stdout.splitlines() if line.strip())

scope = load_scope(repo)
violations = [
    (p, classify(p, scope))
    for p in sorted(paths)
    if not ignored(p) and classify(p, scope) != "ALLOWED_A1"
]
if violations:
    print(json.dumps({
        "decision": "block",
        "reason": "A1 worktree scope violation after tool use: "
        + ", ".join(f"{p}={c}" for p, c in violations),
    }))
