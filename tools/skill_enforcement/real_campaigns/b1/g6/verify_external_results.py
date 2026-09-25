from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[5]
G6 = Path(__file__).resolve().parent
QUALIFIED_SHA = "08c2a93c4c9dede1e759abe28c07242b4116f47e"
TERMINAL = {"PASS", "FAIL", "ERROR", "BLOCKED", "NOT_APPLICABLE", "NOT_OBSERVABLE"}

EXPECTED_FREE = {
    "SER03": {
        "marker": "SER_B1_G6_SER03_FREE_PROBE_1",
        "skill": "hub-ml-analise-safra",
        "cases": {
            "cumulative_real_core", "event_real_core", "negative_monetary_estimand",
            "release_unchanged", "policy_pre_promotion",
        },
    },
    "SER05": {
        "marker": "SER_B1_G6_SER05_L2_FREE_PROBE_1",
        "skill": "hub-ml-cross-eda-ml",
        "cases": {
            "temporal_context", "static_context", "negative_temporal_limits",
            "protected_bytes_unchanged", "policy_pre_promotion",
        },
    },
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_free_output(path: Path, key: str) -> dict:
    issues: list[str] = []
    expected = EXPECTED_FREE[key]
    try:
        payload = _load_json(path)
    except Exception as exc:
        return {"valid": False, "issues": ["FREE_OUTPUT_UNREADABLE:" + type(exc).__name__]}
    if not isinstance(payload, dict):
        return {"valid": False, "issues": ["FREE_OUTPUT_NOT_OBJECT"]}
    if payload.get("marker") != expected["marker"]:
        issues.append("FREE_MARKER_MISMATCH")
    if payload.get("qualified_sha") != QUALIFIED_SHA:
        issues.append("FREE_QUALIFIED_SHA_MISMATCH")
    if payload.get("skill") != expected["skill"]:
        issues.append("FREE_SKILL_MISMATCH")
    if payload.get("status") != "PASS":
        issues.append("FREE_STATUS_NOT_PASS")
    if payload.get("persistent_writes_performed") is not False:
        issues.append("FREE_PERSISTENT_WRITE_CLAIM_INVALID")
    if payload.get("promotion_authorized") is not False:
        issues.append("FREE_PROMOTION_AUTHORITY_INVALID")
    cases = payload.get("cases")
    if not isinstance(cases, dict) or set(cases) != expected["cases"]:
        issues.append("FREE_CASE_SET_MISMATCH")
    else:
        for case_id, row in cases.items():
            if not isinstance(row, dict) or row.get("ok") is not True:
                issues.append("FREE_CASE_NOT_PASS:" + case_id)
    if key == "SER03" and payload.get("published_package_mutated") is not False:
        issues.append("FREE_SER03_PACKAGE_MUTATED")
    if key == "SER05":
        if payload.get("join_executed") is not False:
            issues.append("FREE_SER05_JOIN_EXECUTED")
        if payload.get("coverage_measured") is not False:
            issues.append("FREE_SER05_COVERAGE_MEASURED")
        if payload.get("ml_readiness") != "NOT_EVALUATED":
            issues.append("FREE_SER05_ML_READINESS_OVERCLAIM")
    return {
        "valid": not issues,
        "issues": sorted(set(issues)),
        "sha256": _sha256(path),
        "marker": payload.get("marker"),
        "status": payload.get("status"),
    }


def verify_genie_results(path: Path) -> dict:
    issues: list[str] = []
    manifest = _load_json(G6 / "genie_manifest.json")
    try:
        results = _load_json(path)
    except Exception as exc:
        return {"valid": False, "aggregate_status": "FAIL", "issues": ["GENIE_RESULTS_UNREADABLE:" + type(exc).__name__]}
    if not isinstance(results, dict):
        return {"valid": False, "aggregate_status": "FAIL", "issues": ["GENIE_RESULTS_NOT_OBJECT"]}
    if results.get("schema_version") != "SER-B1-G6-GENIE-RESULTS-1":
        issues.append("GENIE_RESULTS_SCHEMA")
    if results.get("qualified_candidate_sha") != QUALIFIED_SHA:
        issues.append("GENIE_RESULTS_QUALIFIED_SHA")
    frozen = {
        (v["case_id"], v["variant_id"]): (skill["skill"], v)
        for skill in manifest["skills"] for v in skill["variants"]
    }
    raw_rows = results.get("variants")
    if not isinstance(raw_rows, list):
        raw_rows = []
        issues.append("GENIE_RESULTS_VARIANTS_NOT_LIST")
    observed = {}
    for row in raw_rows:
        if not isinstance(row, dict):
            issues.append("GENIE_RESULT_ROW_NOT_OBJECT")
            continue
        key = (row.get("case_id"), row.get("variant_id"))
        if key in observed:
            issues.append("GENIE_RESULT_DUPLICATE:" + str(key))
            continue
        observed[key] = row
        basis = frozen.get(key)
        if basis is None:
            issues.append("GENIE_RESULT_UNKNOWN_VARIANT:" + str(key))
            continue
        expected_skill, frozen_variant = basis
        if row.get("skill") != expected_skill:
            issues.append("GENIE_RESULT_SKILL_MISMATCH:" + str(key))
        if row.get("prompt_literal") != frozen_variant.get("prompt_literal"):
            issues.append("GENIE_RESULT_PROMPT_DRIFT:" + str(key))
        if not isinstance(row.get("response_literal"), str) or not row["response_literal"].strip():
            issues.append("GENIE_RESULT_LITERAL_RESPONSE_MISSING:" + str(key))
        for field in ("task_correctness", "agent_adherence", "canonical_compliance", "verdict", "execution_status"):
            if row.get(field) not in TERMINAL:
                issues.append("GENIE_RESULT_STATE_INVALID:" + field + ":" + str(key))
        if row.get("verdict") == "PASS":
            axes = (
                row.get("task_correctness"),
                row.get("agent_adherence"),
                row.get("canonical_compliance"),
            )
            if axes != ("PASS", "PASS", "PASS"):
                issues.append("GENIE_PASS_AXES_INCONSISTENT:" + str(key))
        if row.get("skill_indicator") == "NOT_OBSERVABLE" and row.get("canonical_compliance") == "PASS":
            if str(key[0]).endswith("-G01") or str(key[0]).endswith("-G02"):
                issues.append("GENIE_ROUTE_PASS_WITHOUT_INDICATOR:" + str(key))
    if set(observed) != set(frozen):
        issues.append("GENIE_RESULT_SET_MISMATCH")
    aggregate = "PASS" if not issues and all(row.get("verdict") == "PASS" for row in observed.values()) else "FAIL"
    return {
        "valid": not issues,
        "aggregate_status": aggregate,
        "issues": sorted(set(issues)),
        "variant_count": len(observed),
        "sha256": _sha256(path),
    }


def verify_all(ser03_output: Path, ser05_output: Path, genie_results: Path) -> dict:
    ser03 = verify_free_output(ser03_output, "SER03")
    ser05 = verify_free_output(ser05_output, "SER05")
    genie = verify_genie_results(genie_results)
    issues = []
    if not ser03["valid"]:
        issues.append("SER03_FREE_INVALID")
    if not ser05["valid"]:
        issues.append("SER05_FREE_INVALID")
    if not genie["valid"]:
        issues.append("GENIE_RESULTS_INVALID")
    status = "PASS" if not issues and genie.get("aggregate_status") == "PASS" else "FAIL"
    return {
        "schema_version": "SER-B1-G6-EXTERNAL-VERIFICATION-1",
        "status": status,
        "issues": issues,
        "qualified_candidate_sha": QUALIFIED_SHA,
        "ser03_free": ser03,
        "ser05_free": ser05,
        "genie": genie,
        "promotion_authorized": False,
        "policy_change_authorized": False,
        "merge_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify literal G6 Free + Genie evidence")
    parser.add_argument("--ser03-output", required=True, type=Path)
    parser.add_argument("--ser05-output", required=True, type=Path)
    parser.add_argument("--genie-results", required=True, type=Path)
    args = parser.parse_args()
    result = verify_all(args.ser03_output, args.ser05_output, args.genie_results)
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
