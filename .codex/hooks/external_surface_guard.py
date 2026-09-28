from __future__ import annotations

import argparse
import json
import sys


BLOCKED_NON_MCP = {
    "list_mcp_resources",
    "list_mcp_resource_templates",
    "read_mcp_resource",
    "web__run",
}


def decision(tool_name: str) -> str:
    if tool_name.startswith("mcp__node_repl__") and len(tool_name) > len("mcp__node_repl__"):
        return "ALLOW_INTERNAL_NODE_REPL"
    if tool_name.startswith(("codex_app", "cua_repl", "codex_tui")):
        return "DENY"
    if tool_name.startswith("mcp__"):
        return "DENY"
    if tool_name in BLOCKED_NON_MCP:
        return "DENY"
    return "DENY_UNEXPECTED_MATCH"


def deny(tool_name: str, reason: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        assert decision("mcp__node_repl__js") == "ALLOW_INTERNAL_NODE_REPL"
        denied_names = (
            "mcp__cua_repl.js",
            "cua_repljs",
            "mcp__codex_app__get_usage_limits",
            "codex_appget_usage_limits",
            "codex_app__get_usage_limits",
            "codex_tuilist_threads",
            "mcp__example__write",
            "list_mcp_resources",
            "read_mcp_resource",
            "web__run",
        )
        for name in denied_names:
            assert decision(name) == "DENY"
        payload = deny("mcp__example__read", "synthetic denial")
        assert set(payload) == {"hookSpecificOutput"}
        assert payload["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert json.loads(json.dumps(payload)) == payload
        print(json.dumps({
            "schema_version": "SER-CODEX-EXTERNAL-SURFACE-GUARD-SELFTEST-1",
            "result": "PASS",
            "internal_node_repl": "ALLOW",
            "denied_cases": len(denied_names),
        }))
        return 0

    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict):
            raise ValueError("hook input must be an object")
        tool_name = event.get("tool_name")
        if not isinstance(tool_name, str) or not tool_name.strip():
            raise ValueError("tool_name must be a nonempty string")
    except Exception:
        print(json.dumps(deny("<unparseable>", "SER controller surface guard could not parse hook input")))
        return 0

    if decision(tool_name) == "ALLOW_INTERNAL_NODE_REPL":
        return 0
    print(json.dumps(deny(
        tool_name,
        f"SER controller forbids this external/control surface during CQ/A0/A1: {tool_name}",
    )))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
