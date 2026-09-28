from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

PRIVILEGED_LEAVES = (
    "a1_patch_transport.ps1",
    "a1_git_transport.ps1",
    "a1_operational_git_transport.ps1",
)


def deny(reason: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def is_privileged(command: str) -> bool:
    low = command.casefold()
    return any(leaf.casefold() in low for leaf in PRIVILEGED_LEAVES)


def root_meta_ok(meta: object, session_id: str, cwd: str) -> bool:
    if not isinstance(meta, dict) or meta.get("id") != session_id:
        return False
    if meta.get("source") != "cli":
        return False
    if meta.get("parent_thread_id") not in (None, ""):
        return False
    try:
        return Path(str(meta.get("cwd"))).resolve() == Path(cwd).resolve()
    except Exception:
        return False


def read_session_meta(transcript: str) -> dict | None:
    try:
        path = Path(transcript).resolve(strict=True)
        sessions = (Path.home() / ".codex" / "sessions").resolve(strict=True)
        path.relative_to(sessions)
    except Exception:
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            for index, line in enumerate(handle):
                if index >= 200:
                    break
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                if isinstance(row, dict) and row.get("type") == "session_meta" and isinstance(row.get("payload"), dict):
                    return row["payload"]
    except Exception:
        return None
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        assert is_privileged(r"powershell.exe -File .codex\transport\a1_patch_transport.ps1")
        assert not is_privileged("git status --porcelain")
        assert root_meta_ok(
            {"id": "r", "source": "cli", "cwd": os.getcwd(), "parent_thread_id": None},
            "r",
            os.getcwd(),
        )
        assert not root_meta_ok(
            {"id": "c", "source": {"subagent": {}}, "cwd": os.getcwd()},
            "c",
            os.getcwd(),
        )
        assert deny("x")["hookSpecificOutput"]["permissionDecision"] == "deny"
        print(json.dumps({
            "schema_version": "SER-A1-PRIVILEGED-BRIDGE-GUARD-SELFTEST-1",
            "result": "PASS",
            "privileged_leaf_count": len(PRIVILEGED_LEAVES),
        }))
        return 0

    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict) or event.get("tool_name") != "Bash":
            return 0
        tool_input = event.get("tool_input")
        command = tool_input.get("command") if isinstance(tool_input, dict) else None
        if not isinstance(command, str) or not is_privileged(command):
            return 0
        meta = read_session_meta(str(event.get("transcript_path") or ""))
        if root_meta_ok(meta, str(event.get("session_id") or ""), str(event.get("cwd") or "")):
            return 0
        print(json.dumps(deny("A1 privileged transports are root-controller-only; subagent or unproven origin denied.")))
        return 0
    except Exception:
        print(json.dumps(deny("A1 privileged bridge guard could not prove a root CLI origin.")))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
