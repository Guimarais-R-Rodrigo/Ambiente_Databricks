from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = {
    "pilot.alpha.pass": "PASS",
    "pilot.beta.fail": "FAIL",
    "pilot.beta.dependent": "BLOCKED_DEPENDENCY",
    "pilot.publication.blocked": "BLOCKED_DEPENDENCY",
}

def verify(summary: dict) -> dict:
    issues = []
    results = summary.get("results") if isinstance(summary, dict) else None
    if not isinstance(results, dict):
        return {"valid": False, "issues": ["PILOT_RESULTS_MISSING"]}
    if set(results) != set(EXPECTED):
        issues.append("PILOT_TASK_SET_MISMATCH")
    for task_id, expected in EXPECTED.items():
        observed = (results.get(task_id) or {}).get("status")
        if observed != expected:
            issues.append(f"PILOT_STATUS:{task_id}:{observed}:{expected}")
    beta = results.get("pilot.beta.dependent") or {}
    if beta.get("blocked_by") != ["pilot.beta.fail"]:
        issues.append("PILOT_DEPENDENCY_PROPAGATION_INVALID")
    publication = results.get("pilot.publication.blocked") or {}
    if "pilot.beta.dependent" not in (publication.get("blocked_by") or []):
        issues.append("PILOT_PUBLICATION_NOT_BLOCKED")
    if summary.get("first_failure") != "pilot.beta.fail":
        issues.append("PILOT_FIRST_FAILURE_INVALID")
    return {
        "valid": not issues,
        "issues": issues,
        "classification": "B0_MECHANISM_PILOT_PASS" if not issues else "B0_MECHANISM_PILOT_FAIL",
    }

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--summary",required=True,type=Path)
    a=p.parse_args()
    result=verify(json.loads(a.summary.read_text(encoding="utf-8")))
    print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
    return 0 if result["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
