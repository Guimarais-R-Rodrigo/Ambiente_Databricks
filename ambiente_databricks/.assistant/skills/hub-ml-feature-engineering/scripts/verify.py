"""Independent binding check for the fixed-lag synthetic profile."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity
from hub_scripts.skill_execution.receipt import verify_execution_receipt


def verify(payload: object, *, expected_request: dict, expected_run_id: str,
           expected_features: list[dict]) -> dict:
    issues = []
    try:
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser07_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        expected_pre = runner.preflight(expected_request)
        if expected_pre["status"] != "PASS":
            raise ValueError("EXPECTED_REQUEST_INVALID")
        if not isinstance(payload, dict) or set(payload) != {"status", "preflight", "trace", "result", "receipt"} or payload["status"] != "PASS":
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(expected_pre):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        if payload["trace"].get("input_digest") != digest(expected_request):
            issues.append("INPUT_BINDING_MISMATCH")
        result = payload["result"]
        if not isinstance(result, dict) or set(result) != {"schema_version", "profile", "population_id", "decision_at",
                                                      "window_days", "eligible_ids", "excluded_counts", "features",
                                                      "fit_performed", "materialization_performed", "promotion_authorized"}:
            raise ValueError("RESULT_SCHEMA_MISMATCH")
        expected_meta = {"schema_version": "SER07-RESULT-1", "profile": expected_pre["profile"],
                         "population_id": expected_request["population_id"], "decision_at": expected_request["decision_at"],
                         "window_days": expected_request["window_days"], "eligible_ids": expected_pre["eligible_ids"],
                         "excluded_counts": expected_pre["excluded_counts"], "fit_performed": False,
                         "materialization_performed": False, "promotion_authorized": False}
        if digest({key: value for key, value in result.items() if key != "features"}) != digest(expected_meta):
            issues.append("RESULT_CONTEXT_BINDING_MISMATCH")
        if digest(result["features"]) != digest(expected_features):
            issues.append("TRUSTED_ORACLE_FEATURE_MISMATCH")
        rv = verify_execution_receipt(payload, expected_skill=runner.SKILL,
                                      expected_entrypoint=runner.ENTRYPOINT,
                                      protected_primitive=runner.PRIMITIVE_ID,
                                      expected_run_id=expected_run_id,
                                      expected_release={"manifest_name": "release_manifest.json",
                                                        "manifest_sha256": release["manifest_sha256"],
                                                        "contract_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/execution_contract.json"],
                                                        "runner_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/scripts/run.py"]}).to_dict()
        if not rv["valid"]:
            issues.extend(rv["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID", "issues": issues,
            "completion_authorized": False, "promotion_authorized": False}
