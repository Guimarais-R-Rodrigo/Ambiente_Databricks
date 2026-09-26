from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tools.skill_enforcement.real_campaigns.b1.registry import load_registry

ROOT = Path(__file__).resolve().parents[4]
REGISTRY = ROOT / "tools/skill_enforcement/real_campaigns/b1/coverage_registry.json"
TEST_MODULE = ROOT / "tools/tests/test_ser_b1_domains.py"
SCHEMA_VERSION = "SER-B1-COVERAGE-1"
_REQUIRED = {
    "VF01", "VF02", "VF03", "VF04", "VF05", "VF06", "VF07", "VF08", "VF09", "VF10", "VF11", "VF12",
    "CE01", "CE02", "CE05", "CE06", "CE07", "CE08", "CE10",
}
_EXPECTED_OUT = {"CE03", "CE04", "CE09", "CE11", "CE12"}
_ORACLES = {
    "manual_monthly_binary_v1", "negative_preflight", "receipt_and_replay",
    "declared_context_only", "pit_tristate", "pit_boundary", "negative_context", "context_identity",
}


def _test_symbols() -> set[str]:
    text = TEST_MODULE.read_text(encoding="utf-8")
    current_class = None
    out: set[str] = set()
    for line in text.splitlines():
        cls = re.match(r"class\s+([A-Za-z0-9_]+)\(", line)
        if cls:
            current_class = cls.group(1)
            continue
        method = re.match(r"\s+def\s+(test_[A-Za-z0-9_]+)\(", line)
        if method and current_class:
            out.add(current_class + "." + method.group(1))
    return out


def build_report() -> dict[str, Any]:
    issues: list[str] = []
    try:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "FAIL", "issues": ["COVERAGE_UNREADABLE:" + type(exc).__name__]}
    if not isinstance(payload, dict) or set(payload) != {
        "schema_version", "campaign_scope", "p1_evidence_binding", "cases", "out_of_scope"
    }:
        issues.append("COVERAGE_SHAPE_INVALID")
        payload = payload if isinstance(payload, dict) else {}
    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append("COVERAGE_SCHEMA_INVALID")
    commands = set(load_registry()["commands"])
    tests = _test_symbols()
    seen: set[str] = set()
    for row in payload.get("cases", []):
        if not isinstance(row, dict) or set(row) != {"case_id", "test_ids", "oracle_id", "command_ids", "evidence"}:
            issues.append("COVERAGE_CASE_SHAPE_INVALID")
            continue
        cid = row.get("case_id")
        if not isinstance(cid, str) or cid in seen:
            issues.append("COVERAGE_CASE_ID_INVALID")
            continue
        seen.add(cid)
        if not isinstance(row.get("test_ids"), list) or not row["test_ids"]:
            issues.append("COVERAGE_TESTS_EMPTY:" + cid)
        else:
            for test_id in row["test_ids"]:
                if test_id not in tests:
                    issues.append("COVERAGE_TEST_UNKNOWN:" + cid + ":" + str(test_id))
        if row.get("oracle_id") not in _ORACLES:
            issues.append("COVERAGE_ORACLE_UNKNOWN:" + cid)
        if not isinstance(row.get("command_ids"), list) or not row["command_ids"]:
            issues.append("COVERAGE_COMMANDS_EMPTY:" + cid)
        else:
            for command_id in row["command_ids"]:
                if command_id not in commands:
                    issues.append("COVERAGE_COMMAND_UNKNOWN:" + cid + ":" + str(command_id))
        if row.get("evidence") != "P1_SHA_BOUND_TEST_PLUS_P2_SANDBOX_COMMAND":
            issues.append("COVERAGE_EVIDENCE_KIND_INVALID:" + cid)
    if seen != _REQUIRED:
        issues.append("COVERAGE_REQUIRED_SET_MISMATCH")
    out_rows = payload.get("out_of_scope", [])
    out_ids = {x.get("case_id") for x in out_rows if isinstance(x, dict)}
    if out_ids != _EXPECTED_OUT:
        issues.append("COVERAGE_OUT_OF_SCOPE_SET_MISMATCH")
    if any(not isinstance(x, dict) or set(x) != {"case_id", "reason"} or not isinstance(x.get("reason"), str) or not x["reason"].strip() for x in out_rows):
        issues.append("COVERAGE_OUT_OF_SCOPE_ROW_INVALID")
    binding = payload.get("p1_evidence_binding")
    if not isinstance(binding, dict) or binding != {
        "commit": "d2b6079ee2e6ecec628d14411afbdbdb878a5fb9",
        "domain_suite": "PASS_47_OF_47",
        "public_integration": "PASS_2_OF_2",
    }:
        issues.append("COVERAGE_P1_BINDING_INVALID")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": sorted(set(issues)),
        "required_cases": len(_REQUIRED),
        "out_of_scope_cases": len(_EXPECTED_OUT),
        "command_ids": len(commands),
        "p1_commit": (binding or {}).get("commit") if isinstance(binding, dict) else None,
    }


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=True, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
