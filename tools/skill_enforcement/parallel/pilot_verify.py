from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from .verifier import verify_campaign_run

_SCENARIOS = {
    "selective": {
        "campaign_id": "SER-B0-PILOT-SELECTIVE",
        "first_failure": "pilot.beta.fail",
        "global_stop": None,
        "tasks": {
            "pilot.alpha.pass": {
                "status": "PASS", "wave": 0, "role": "executor", "depends_on": [],
                "failure_scope": "LOCAL_CHAIN", "command_ids": ["b0:pilot:pass"],
            },
            "pilot.beta.fail": {
                "status": "FAIL", "wave": 0, "role": "executor", "depends_on": [],
                "failure_scope": "LOCAL_CHAIN", "command_ids": ["b0:pilot:fail"],
            },
            "pilot.beta.dependent": {
                "status": "BLOCKED_DEPENDENCY", "wave": 1, "role": "executor",
                "depends_on": ["pilot.beta.fail"], "failure_scope": "LOCAL_CHAIN",
                "command_ids": ["b0:pilot:pass"], "blocked_by": ["pilot.beta.fail"],
            },
            "pilot.gamma.independent": {
                "status": "PASS", "wave": 1, "role": "executor",
                "depends_on": ["pilot.alpha.pass"], "failure_scope": "LOCAL_CHAIN",
                "command_ids": ["b0:pilot:pass"],
            },
            "pilot.publication.blocked": {
                "status": "BLOCKED_DEPENDENCY", "wave": 2, "role": "integrator",
                "depends_on": ["pilot.beta.dependent", "pilot.gamma.independent"],
                "failure_scope": "LOCAL_CHAIN", "command_ids": ["b0:pilot:pass"],
                "blocked_by": ["pilot.beta.dependent"],
            },
        },
    },
    "global": {
        "campaign_id": "SER-B0-PILOT-GLOBAL",
        "first_failure": "pilot.global.fail",
        "global_stop": "pilot.global.fail",
        "tasks": {
            "pilot.global.arm": {
                "status": "PASS", "wave": 0, "role": "executor", "depends_on": [],
                "failure_scope": "LOCAL_CHAIN", "command_ids": ["b0:pilot:pass"],
            },
            "pilot.global.fail": {
                "status": "FAIL", "wave": 1, "role": "executor",
                "depends_on": ["pilot.global.arm"], "failure_scope": "GLOBAL_CAMPAIGN",
                "command_ids": ["b0:pilot:global-fail"],
            },
            "pilot.global.anchor": {
                "status": "PASS", "wave": 1, "role": "executor",
                "depends_on": ["pilot.global.arm"], "failure_scope": "LOCAL_CHAIN",
                "command_ids": ["b0:pilot:pass"],
            },
            "pilot.global.must_not_start": {
                "status": "BLOCKED_GLOBAL_STOP", "wave": 2, "role": "executor",
                "depends_on": ["pilot.global.anchor"], "failure_scope": "LOCAL_CHAIN",
                "command_ids": ["b0:pilot:pass"], "blocked_by": ["pilot.global.fail"],
            },
        },
    },
}


def _task_map(campaign: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    tasks = campaign.get("tasks")
    if not isinstance(tasks, list):
        return {}
    return {
        task["task_id"]: task
        for task in tasks
        if isinstance(task, Mapping) and isinstance(task.get("task_id"), str)
    }


def verify(
    summary: dict,
    scenario: str = "selective",
    *,
    campaign: Mapping[str, Any] | None = None,
    evidence_root: Path | None = None,
) -> dict:
    if scenario not in _SCENARIOS:
        return {"valid": False, "issues": ["PILOT_SCENARIO_UNKNOWN"], "classification": "B0_PILOT_FAIL"}
    spec = _SCENARIOS[scenario]
    issues: list[str] = []
    if not isinstance(summary, dict):
        return {"valid": False, "issues": ["PILOT_SUMMARY_INVALID"], "classification": f"B0_{scenario.upper()}_PILOT_FAIL"}
    if campaign is None:
        return {"valid": False, "issues": ["PILOT_CAMPAIGN_REQUIRED"], "classification": f"B0_{scenario.upper()}_PILOT_FAIL"}

    if campaign.get("campaign_id") != spec["campaign_id"]:
        issues.append("PILOT_CAMPAIGN_ID_INVALID")
    if summary.get("campaign_id") != spec["campaign_id"]:
        issues.append("PILOT_SUMMARY_CAMPAIGN_ID_INVALID")
    if summary.get("candidate_sha") != campaign.get("candidate_sha"):
        issues.append("PILOT_CANDIDATE_BINDING_INVALID")
    if summary.get("status") != "FAIL":
        issues.append("PILOT_NORMAL_CAMPAIGN_MUST_FAIL")

    results = summary.get("results")
    if not isinstance(results, dict):
        return {
            "valid": False,
            "issues": [*issues, "PILOT_RESULTS_MISSING"],
            "classification": f"B0_{scenario.upper()}_PILOT_FAIL",
        }

    campaign_tasks = _task_map(campaign)
    expected_tasks = spec["tasks"]
    if set(results) != set(expected_tasks):
        issues.append("PILOT_RESULT_TASK_SET_MISMATCH")
    if set(campaign_tasks) != set(expected_tasks):
        issues.append("PILOT_CAMPAIGN_TASK_SET_MISMATCH")

    for task_id, expected in expected_tasks.items():
        task = campaign_tasks.get(task_id) or {}
        for key in ("role", "depends_on", "failure_scope", "command_ids"):
            if task.get(key) != expected[key]:
                issues.append(f"PILOT_TOPOLOGY:{task_id}:{key}")
        result = results.get(task_id) or {}
        if result.get("status") != expected["status"]:
            issues.append(f"PILOT_STATUS:{task_id}:{result.get('status')}:{expected['status']}")
        if result.get("wave_index") != expected["wave"]:
            issues.append(f"PILOT_WAVE:{task_id}:{result.get('wave_index')}:{expected['wave']}")
        if "blocked_by" in expected and result.get("blocked_by") != expected["blocked_by"]:
            issues.append(f"PILOT_BLOCKED_BY:{task_id}")
        if expected["status"].startswith("BLOCKED") and result.get("command_records"):
            issues.append(f"PILOT_BLOCKED_TASK_EXECUTED:{task_id}")
        if expected["status"] in {"PASS", "FAIL"} and not result.get("command_records"):
            issues.append(f"PILOT_EXECUTED_TASK_MISSING_RECORD:{task_id}")

    independent = verify_campaign_run(campaign, results, evidence_root=evidence_root)
    if not independent["valid"]:
        issues.extend("PILOT_INDEPENDENT:" + issue for issue in independent["issues"])
    embedded = summary.get("verification")
    if not isinstance(embedded, Mapping):
        issues.append("PILOT_EMBEDDED_VERIFICATION_MISSING")
    else:
        if embedded.get("valid") is not True or embedded.get("issues") != []:
            issues.append("PILOT_EMBEDDED_VERIFICATION_NOT_PASS")
        if dict(embedded) != independent:
            issues.append("PILOT_EMBEDDED_VERIFICATION_MISMATCH")

    if summary.get("first_failure") != spec["first_failure"]:
        issues.append("PILOT_FIRST_FAILURE_INVALID")
    if independent.get("first_failure") != spec["first_failure"]:
        issues.append("PILOT_INDEPENDENT_FIRST_FAILURE_INVALID")
    if summary.get("global_stop") != spec["global_stop"]:
        issues.append("PILOT_GLOBAL_STOP_INVALID")
    if independent.get("global_stop") != spec["global_stop"]:
        issues.append("PILOT_INDEPENDENT_GLOBAL_STOP_INVALID")

    return {
        "valid": not issues,
        "issues": sorted(set(issues)),
        "classification": (
            f"B0_{scenario.upper()}_PILOT_PASS"
            if not issues
            else f"B0_{scenario.upper()}_PILOT_FAIL"
        ),
        "independent_verification": independent,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--campaign", required=True, type=Path)
    parser.add_argument("--scenario", choices=sorted(_SCENARIOS), default="selective")
    args = parser.parse_args()
    result = verify(
        json.loads(args.summary.read_text(encoding="utf-8")),
        args.scenario,
        campaign=json.loads(args.campaign.read_text(encoding="utf-8")),
        evidence_root=args.summary.parent,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
