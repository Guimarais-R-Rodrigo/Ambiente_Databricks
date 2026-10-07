from __future__ import annotations

import math
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity


def _close(actual, expected):
    return (type(actual) in (int, float) and math.isfinite(actual)
            and math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-10))


def verify(payload: object, *, expected_request: dict, expected_model,
           expected_X, expected_background, expected_run_id: str) -> dict:
    issues = []
    try:
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser02_explainability_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        domain = runner._preflight_module().preflight(expected_request)
        if domain["status"] != "PASS":
            raise ValueError("EXPECTED_REQUEST_INVALID")
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        X, background = runner._bound_arrays(expected_request, expected_model, expected_X, expected_background)
        if (not isinstance(payload, dict)
                or set(payload) != {"status", "preflight", "trace", "result", "receipt"}
                or payload["status"] != "PASS"):
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(domain):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        trace = payload["trace"]
        if not isinstance(trace, dict) or trace.get("input_digest") != digest(expected_request):
            issues.append("INPUT_BINDING_MISMATCH")
        result = payload["result"]
        if not isinstance(result, dict):
            raise ValueError("RESULT_NOT_OBJECT")
        metadata = {"schema_version": "SER02-EXPLAINABILITY-RESULT-1",
                    "profile": domain["profile"], "model_id": expected_request["model"]["model_id"],
                    "feature_names": expected_request["feature_names"],
                    "row_ids": expected_request["row_ids"],
                    "sample_ids": expected_request["sample_ids"],
                    "promotion_authorized": False, "business_readiness": "NOT_EVALUATED"}
        if (set(result) != set(metadata) | {"base_value", "shap_values"}
                or any(result.get(key) != value for key, value in metadata.items())):
            issues.append("RESULT_CONTEXT_BINDING_MISMATCH")
        coefficients = [float(c) for c in expected_model.coef_]
        mean_background = [float(background[:, index].mean()) for index in range(X.shape[1])]
        oracle_base = float(expected_model.intercept_) + sum(c * b for c, b in zip(coefficients, mean_background))
        oracle_values = [[c * (float(value) - b) for c, value, b in zip(coefficients, row, mean_background)]
                         for row in X]
        actual_values = result.get("shap_values")
        if (not _close(result.get("base_value"), oracle_base)
                or not isinstance(actual_values, list) or len(actual_values) != len(oracle_values)
                or any(not isinstance(row, list) or len(row) != len(reference)
                       or any(not _close(value, expected) for value, expected in zip(row, reference))
                       for row, reference in zip(actual_values, oracle_values))):
            issues.append("ANALYTIC_ORACLE_MISMATCH")
        from hub_scripts.skill_execution.receipt import verify_execution_receipt
        if Path(verify_execution_receipt.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py").resolve():
            raise RuntimeError("RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH")
        receipt = verify_execution_receipt(
            payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
            protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
            expected_release={"manifest_name": "release_manifest.json",
                              "manifest_sha256": release["manifest_sha256"],
                              "contract_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/execution_contract.json"],
                              "runner_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/scripts/run.py"]},
            release_integrity_ok=True).to_dict()
        if receipt["valid"] is not True:
            issues.extend(receipt["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID", "issues": issues,
            "scope": "CURRENT_RELEASE_REQUEST_MODEL_ARRAYS_RECEIPT_AND_ANALYTIC_ORACLE",
            "promotion_authorized": False, "completion_authorized": False}

