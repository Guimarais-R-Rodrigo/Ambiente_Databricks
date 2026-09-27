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
    if tool_name.startswith("mcp__node_repl__"):
        return "ALLOW_INTERNAL_NODE_REPL"
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
        "ser_controller": {
            "tool_name": tool_name,
            "policy": "DENY_EXTERNAL_SURFACES_ALLOW_INTERNAL_NODE_REPL",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        assert decision("mcp__node_repl__js") == "ALLOW_INTERNAL_NODE_REPL"
        for name in (
            "mcp__cua_repl.js",
            "mcp__codex_app__get_usage_limits",
            "mcp__example__write",
            "list_mcp_resources",
            "read_mcp_resource",
            "web__run",
        ):
            assert decision(name) == "DENY"
        print(json.dumps({
            "schema_version": "SER-CODEX-EXTERNAL-SURFACE-GUARD-SELFTEST-1",
            "result": "PASS",
            "internal_node_repl": "ALLOW",
            "denied_cases": 6,
        }))
        return 0

    try:
        event = json.load(sys.stdin)
        tool_name = str(event.get("tool_name") or "")
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
