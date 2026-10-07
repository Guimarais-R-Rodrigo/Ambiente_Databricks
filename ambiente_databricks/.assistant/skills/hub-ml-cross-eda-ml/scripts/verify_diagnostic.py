from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity


def verify(payload: object, *, expected_context: dict, expected_datasets: dict,
           expected_run_id: str, expected_diagnostic: dict) -> dict:
    issues = []
    try:
        runner = load_sibling(SKILL_DIR / "scripts/run_diagnostic.py", "_ser05_diag_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        domain = runner._preflight().preflight(expected_context)
        if domain["status"] != "PASS" or expected_context["pit"] != "NOT_APPLICABLE":
            raise ValueError("EXPECTED_CONTEXT_INVALID")
        runner._rows(expected_context, expected_datasets)
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        if (not isinstance(payload, dict) or set(payload) !=
                {"status", "preflight", "trace", "result", "receipt"} or payload["status"] != "PASS"):
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(domain):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        trace = payload["trace"]
        if not isinstance(trace, dict) or trace.get("input_digest") != digest(
                {"context": expected_context, "datasets": expected_datasets}):
            issues.append("INPUT_BINDING_MISMATCH")
        result = payload["result"]
        if not isinstance(result, dict):
            raise ValueError("RESULT_NOT_OBJECT")
        _, _, hashes = runner._rows(expected_context, expected_datasets)
        expected = {
            "schema_version": "SER05-DIAGNOSTIC-1",
            "context_sha256": digest(expected_context),
            "source_content_sha256": hashes,
            "diagnostic": expected_diagnostic,
            "join_executed": False, "coverage_measured": True,
            "pit_executed": False, "ml_readiness": "NOT_EVALUATED",
            "completion_authorized": False, "promotion_authorized": False,
        }
        if digest(result) != digest(expected):
            issues.append("TRUSTED_DIAGNOSTIC_ORACLE_MISMATCH")
        from hub_scripts.skill_execution.receipt import verify_execution_receipt
        receipt = verify_execution_receipt(
            payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
            protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
            expected_release={
                "manifest_name": "release_manifest.json",
                "manifest_sha256": release["manifest_sha256"],
                "contract_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/diagnostic_contract.json"],
                "runner_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/scripts/run_diagnostic.py"],
            }, release_integrity_ok=True).to_dict()
        if receipt["valid"] is not True:
            issues.extend(receipt["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "scope": "STATIC_SYNTHETIC_SPARK_DIAGNOSTIC_AND_TRUSTED_ORACLE",
            "completion_authorized": False, "promotion_authorized": False}
