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


def _ks_oracle(reference: list[float], current: list[float]) -> float:
    points = sorted(set(reference + current))
    return max(abs(sum(x <= p for x in reference)/len(reference) -
                   sum(x <= p for x in current)/len(current)) for p in points)


def verify(payload: object, *, expected_request: dict, expected_run_id: str) -> dict:
    issues = []
    try:
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        import numpy as np
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser11_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        domain = load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser11_verifier_preflight").preflight(expected_request)
        if domain["status"] != "PASS":
            raise ValueError("EXPECTED_REQUEST_INVALID")
        if not isinstance(payload, dict) or set(payload) != {"status", "preflight", "trace", "result", "receipt"} or payload["status"] != "PASS":
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(domain):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        if payload["trace"].get("input_digest") != digest(expected_request):
            issues.append("INPUT_BINDING_MISMATCH")
        if (payload["trace"].get("resources_resolved") != ["drift_numeric"]
                or payload["trace"].get("resources_called") != ["drift_numeric"]
                or payload["trace"].get("resources_completed") != ["drift_numeric"]):
            issues.append("RESOURCE_CALL_BINDING_MISMATCH")
        result = payload["result"]
        if not isinstance(result, dict) or set(result) != {
                "schema_version", "profile", "model_id", "model_version", "population_id",
                "score_name", "windows", "n_bins", "eps", "bin_edges_internal", "bin_policy",
                "psi", "ks_statistic", "ks_pvalue", "interpretation", "performance_evaluated", "action_performed"}:
            raise ValueError("RESULT_SCHEMA_MISMATCH")
        for key in ("model_id", "model_version", "population_id", "score_name", "n_bins", "eps"):
            if result[key] != expected_request[key]:
                issues.append("RESULT_CONTEXT_BINDING_MISMATCH:" + key)
        if (result["schema_version"] != "SER11-RESULT-1" or result["profile"] != expected_request["profile"]
                or result["interpretation"] != "DISTRIBUTION_DIAGNOSTIC_ONLY"
                or result["performance_evaluated"] is not False or result["action_performed"] is not False):
            issues.append("RESULT_SCOPE_MISMATCH")
        if not isinstance(result["windows"], dict):
            raise ValueError("WINDOWS_NOT_OBJECT")
        if set(result["windows"]) != {"reference", "current"}:
            issues.append("WINDOW_SET_MISMATCH")
        for name in ("reference", "current"):
            expected_window = {"start": expected_request[f"{name}_start"], "end": expected_request[f"{name}_end"],
                               "ids": [r["id"] for r in expected_request[name]],
                               "count": len(expected_request[name]),
                               "missing_count": sum(r["score"] is None for r in expected_request[name])}
            if result["windows"].get(name) != expected_window:
                issues.append("WINDOW_BINDING_MISMATCH:" + name)
        raw_ref = [r["score"] for r in expected_request["reference"]]
        raw_cur = [r["score"] for r in expected_request["current"]]
        ref = [float(x) for x in raw_ref if x is not None]
        cur = [float(x) for x in raw_cur if x is not None]
        edges = sorted(set(float(x) for x in np.quantile(ref, [0.25, 0.5, 0.75])))
        if result["bin_edges_internal"] != edges or result["bin_policy"] != "REFERENCE_QUANTILES_UNIQUE_MINUS_INF_PLUS_INF_MISSING_BUCKET":
            issues.append("BIN_BINDING_MISMATCH")
        # Independent counting: numpy.histogram's interior edges send ties right.
        def counts(values):
            out = [0]*(len(edges)+2)
            for value in values:
                if value is None:
                    out[-1] += 1
                else:
                    out[sum(float(value) >= edge for edge in edges)] += 1
            return out
        a, b = counts(raw_ref), counts(raw_cur)
        eps = expected_request["eps"]
        expected_psi = sum((max(y/len(raw_cur), eps)-max(x/len(raw_ref), eps)) *
                           math.log(max(y/len(raw_cur), eps)/max(x/len(raw_ref), eps))
                           for x, y in zip(a, b))
        if not math.isclose(result["psi"], expected_psi, abs_tol=1e-12):
            issues.append("PSI_ORACLE_MISMATCH")
        if not math.isclose(result["ks_statistic"], _ks_oracle(ref, cur), abs_tol=1e-12):
            issues.append("KS_ORACLE_MISMATCH")
        from scipy.stats import ks_2samp
        if type(result["ks_pvalue"]) is not float or not math.isclose(
                result["ks_pvalue"], float(ks_2samp(ref, cur).pvalue), abs_tol=1e-12):
            issues.append("KS_PVALUE_ORACLE_MISMATCH")
        from hub_scripts.skill_execution.receipt import verify_execution_receipt
        if Path(verify_execution_receipt.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py").resolve():
            raise RuntimeError("RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH")
        check = verify_execution_receipt(payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
                                         protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
                                         expected_release={"manifest_name": "release_manifest.json",
                                                           "manifest_sha256": release["manifest_sha256"],
                                                           "contract_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/execution_contract.json"],
                                                           "runner_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/scripts/run.py"]}).to_dict()
        if not check["valid"]:
            issues.extend(check["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID", "issues": issues,
            "promotion_authorized": False, "completion_authorized": False}
