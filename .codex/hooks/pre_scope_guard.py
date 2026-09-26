from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path


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


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


event = json.load(sys.stdin)
command = str((event.get("tool_input") or {}).get("command") or "")
paths = []
for match in re.finditer(r"(?m)^\*\*\*\s+(?:Add|Update|Delete) File:\s*(.+?)\s*$", command):
    paths.append(match.group(1).strip())
for match in re.finditer(r"(?m)^\*\*\*\s+Move to:\s*(.+?)\s*$", command):
    paths.append(match.group(1).strip())

if not paths:
    raise SystemExit(0)

scope = load_scope(root())
violations = [(p, classify(p, scope)) for p in paths if classify(p, scope) != "ALLOWED_A1"]
if violations:
    deny("A1 scope violation: " + ", ".join(f"{p}={c}" for p, c in violations))
