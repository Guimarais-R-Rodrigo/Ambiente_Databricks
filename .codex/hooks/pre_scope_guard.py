from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    raise SystemExit(0)


def root() -> Path:
    proc = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if proc.returncode != 0 or not proc.stdout.strip():
        deny("A1 scope guard cannot resolve repository root")
    return Path(proc.stdout.strip()).resolve()


def normalize(path: str) -> str:
    value = path.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def load_scope(repo: Path) -> dict:
    try:
        return json.loads((repo / "docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json").read_text(encoding="utf-8"))["repo_scope"]
    except Exception:
        deny("A1 scope guard cannot load autonomy envelope")


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


try:
    event = json.load(sys.stdin)
except Exception:
    deny("A1 scope guard cannot parse hook input")

tool_input = event.get("tool_input") or {}
paths: list[str] = []
for key in ("path", "file_path", "target_path", "target_file"):
    value = tool_input.get(key)
    if isinstance(value, str) and value.strip():
        paths.append(value.strip())

command = str(tool_input.get("command") or "")
for pattern in (
    r"(?m)^\*\*\*\s+(?:Add|Update|Delete) File:\s*(.+?)\s*$",
    r"(?m)^\*\*\*\s+Move to:\s*(.+?)\s*$",
):
    paths.extend(match.group(1).strip() for match in re.finditer(pattern, command))

if not paths:
    deny("A1 scope guard could not resolve target path for tool " + str(event.get("tool_name") or ""))

scope = load_scope(root())
violations = [(path, classify(path, scope)) for path in paths if classify(path, scope) != "ALLOWED_A1"]
if violations:
    deny("A1 scope violation: " + ", ".join(f"{path}={category}" for path, category in violations))
