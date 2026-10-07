"""Verify local Spark MERGE with trusted request, expected rows and run ID."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))
from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity


def verify(payload: object, *, expected_request: dict, expected_rows: list[dict],
           expected_run_id: str) -> dict:
    issues = []
    try:
        runner = load_sibling(SKILL_DIR / "scripts/run_local.py", "_ser13_local_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        spec, domain = runner._validate(expected_request)
        runner._rows(expected_rows, allow_empty=False)
        if (expected_rows != sorted(expected_rows, key=lambda row: row["id"])
                or len(expected_rows) != len({row["id"] for row in expected_rows})):
            raise ValueError("EXPECTED_ROWS_NOT_CANONICAL")
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        if (not isinstance(payload, dict) or set(payload) !=
                {"status", "preflight", "trace", "result", "receipt"} or payload["status"] != "PASS"):
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(domain):
            issues.append("SPEC_PREFLIGHT_MISMATCH")
        trace = payload["trace"]
        if not isinstance(trace, dict) or trace.get("input_digest") != digest(expected_request):
            issues.append("INPUT_BINDING_MISMATCH")
        result = payload["result"]
        expected = {
            "schema_version": "SER13-LOCAL-RESULT-1", "profile": "LOCAL_SYNTHETIC_SPARK_MERGE_V1",
            "spec_sha256": digest(spec), "prior_sha256": digest(expected_request["prior_rows"]),
            "batch_sha256": digest(expected_request["batch_rows"]), "destination": spec["destination"],
            "rows": expected_rows, "output_sha256": digest(expected_rows), "row_count": len(expected_rows),
            "quality": {"status": "pass", "row_count": len(expected_rows),
                        "pk_duplicate_rows": 0, "pk_null_rows": 0},
            "replay_semantics": "MERGE_LATEST_EVENT_TIME_EQUAL_IDENTICAL_ONLY",
            "local_spark_executed": True, "persistent_write": False,
            "deployment_status": "NOT_RUN", "completion_authorized": False, "promotion_authorized": False,
        }
        if not isinstance(result, dict) or digest(result) != digest(expected):
            issues.append("TRUSTED_OUTPUT_ORACLE_MISMATCH")
        if not isinstance(trace, dict) or (trace.get("resources_called") != [runner.PRIMITIVE_ID]
                                           or trace.get("resources_completed") != [runner.PRIMITIVE_ID]
                                           or trace.get("writes_performed") is not False):
            issues.append("CALL_OR_EFFECT_TRACE_MISMATCH")
        from hub_scripts.skill_execution.receipt import verify_execution_receipt
        receipt = verify_execution_receipt(
            payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
            protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
            expected_release={
                "manifest_name": "release_manifest.json",
                "manifest_sha256": release["manifest_sha256"],
                "contract_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/local_execution_contract.json"],
                "runner_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/scripts/run_local.py"],
            }, release_integrity_ok=True).to_dict()
        if not receipt["valid"]:
            issues.extend(receipt["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "scope": "SYNTHETIC_LOCAL_SPARK_MERGE_WITH_TRUSTED_ROWS",
            "completion_authorized": False, "promotion_authorized": False}
