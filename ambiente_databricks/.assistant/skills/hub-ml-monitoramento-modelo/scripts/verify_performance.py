from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity


def _metrics(rows: list[dict]) -> dict:
    """Independent rank/ECDF/Brier oracle, including tied scores."""
    positives = [r["score"] for r in rows if r["label"] == 1]
    negatives = [r["score"] for r in rows if r["label"] == 0]
    n_pairs = len(positives) * len(negatives)
    wins = sum((1 if pos > neg else 0.5 if pos == neg else 0)
               for pos in positives for neg in negatives)
    auc = wins / n_pairs
    points = sorted(set(positives + negatives))
    ks = max(abs(sum(x <= p for x in positives)/len(positives) -
                 sum(x <= p for x in negatives)/len(negatives))
             for p in points) * 100
    brier = sum((r["score"] - r["label"])**2 for r in rows) / len(rows)
    return {"auc_roc": auc, "ks_pct": ks, "brier_score": brier}


def _reported_metrics(reported: object, raw: dict) -> bool:
    """Check the helper's decimal grid against independent unrounded oracles.

    Binary floating arithmetic can land on either side of a half-unit boundary.
    Both nearest grid points are admissible; the exact reported grid value
    drives policy status after this check.
    """
    if not isinstance(reported, dict) or set(reported) != set(raw):
        return False
    for key, expected in raw.items():
        value = reported[key]
        scale = 10 if key == "ks_pct" else 10000
        bound = 100 if key == "ks_pct" else 1
        if (type(value) is not float or not math.isfinite(value)
                or not 0 <= value <= bound
                or abs(value * scale - round(value * scale)) > 1e-8
                or abs(value - expected) > 0.5 / scale + 1e-12):
            return False
    return True


def verify(payload: object, *, expected_request: dict, expected_run_id: str) -> dict:
    issues = []
    receipt = {"status": "INVALID", "valid": False}
    try:
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        runner = load_sibling(SKILL_DIR / "scripts/run_performance.py",
                              "_ser12_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        preflight = load_sibling(SKILL_DIR / "scripts/preflight_performance.py",
                                 "_ser12_verifier_preflight").preflight(expected_request)
        if preflight["status"] != "PASS":
            raise ValueError("EXPECTED_REQUEST_INVALID")
        if (not isinstance(payload, dict) or
                set(payload) != {"status", "preflight", "trace", "result", "artifacts", "receipt",
                                 "handoff", "postflight", "scope_completion_authorized"}
                or payload["status"] != "PASS"):
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(preflight):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        trace = payload["trace"]
        if trace.get("input_digest") != digest(expected_request):
            issues.append("INPUT_BINDING_MISMATCH")
        if (trace.get("resources_resolved") != runner.PRIMITIVES or
                trace.get("resources_called") != runner.PRIMITIVES or
                trace.get("resources_completed") != runner.PRIMITIVES):
            issues.append("RESOURCE_CALL_BINDING_MISMATCH")
        ref, cur = _metrics(expected_request["reference"]), _metrics(expected_request["current"])
        policy = {"auc": dict(expected_request["auc_thresholds"])}
        result = payload["result"]
        reported = result.get("metrics") if isinstance(result, dict) else None
        metrics_valid = (
            isinstance(reported, dict)
            and set(reported) == {"reference", "current"}
            and _reported_metrics(reported["reference"], ref)
            and _reported_metrics(reported["current"], cur))
        if not metrics_valid:
            issues.append("RESULT_ORACLE_MISMATCH:metrics")
        # The monitor consumes the helper's rounded AUC. Once checked against
        # independent raw oracles, use those exact reported values for policy.
        bound_metrics = reported if metrics_valid else {"reference": ref, "current": cur}
        delta = bound_metrics["reference"]["auc_roc"] - bound_metrics["current"]["auc_roc"]
        rule = policy["auc"]
        color = "🔴" if delta >= rule["critical"] else "🟡" if delta >= rule["warning"] else "🟢"
        status = {"🔴": "🔴 Crítico", "🟡": "🟡 Atenção", "🟢": "🟢 Saudável"}[color]
        decision = "INVESTIGATE_RETRAINING_CANDIDATE" if color == "🔴" else "NO_TRIGGER"
        expected = {
            "schema_version": "SER12-RESULT-1", "profile": expected_request["profile"],
            "model_id": expected_request["model_id"],
            "model_version": expected_request["model_version"],
            "population_id": expected_request["population_id"],
            "score_name": expected_request["score_name"],
            "evaluation_at": expected_request["evaluation_at"],
            "windows": {name: {"start": expected_request[name + "_start"],
                               "end": expected_request[name + "_end"],
                               "ids": preflight["windows"][name]["ids"],
                               "count": preflight["windows"][name]["count"]}
                        for name in ("reference", "current")},
            "metrics": bound_metrics, "policy": policy,
            "auc_deterioration": delta, "monitor_status": status,
            "investigation_decision": decision,
            "performance_evaluated": True, "action_performed": False,
            "automatic_retrain_authorized": False, "promotion_authorized": False}
        if not isinstance(payload["artifacts"], dict) or payload["artifacts"] != {runner.PRIMITIVE_ID: result}:
            issues.append("ARTIFACT_BINDING_MISMATCH")
        if not isinstance(result, dict) or set(result) != set(expected):
            issues.append("RESULT_SCHEMA_MISMATCH")
        else:
            for key in expected:
                if key == "auc_deterioration":
                    if (type(result[key]) is not float or not math.isfinite(result[key]) or
                            not math.isclose(result[key], expected[key],
                                             abs_tol=1e-12, rel_tol=1e-12)):
                        issues.append("AUC_DELTA_ORACLE_MISMATCH")
                elif key != "metrics" and digest(result[key]) != digest(expected[key]):
                    issues.append("RESULT_ORACLE_MISMATCH:" + key)
        from hub_scripts.skill_execution.receipt import verify_execution_receipt
        if Path(verify_execution_receipt.__code__.co_filename).resolve() != (
                ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py").resolve():
            raise RuntimeError("RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH")
        receipt = verify_execution_receipt(
            payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
            protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
            expected_release={
                "manifest_name": "release_manifest.json",
                "manifest_sha256": release["manifest_sha256"],
                "contract_git_blob_sha1": release["artifacts"][
                    f"skills/{runner.SKILL}/performance_contract.json"],
                "runner_git_blob_sha1": release["artifacts"][
                    f"skills/{runner.SKILL}/scripts/run_performance.py"]}).to_dict()
        if not receipt["valid"]:
            issues.extend(receipt["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "receipt_verification": receipt,
            "promotion_authorized": False,
            "completion_authorized": False}


def _contract() -> dict:
    return json.loads((SKILL_DIR / "performance_contract.json").read_text(encoding="utf-8"))


def _handoff(request: dict, result: dict) -> dict:
    return {
        "scope": "LOCAL_SYNTHETIC_MATURE_PERFORMANCE_V1",
        "model_id": request["model_id"],
        "model_version": request["model_version"],
        "population_id": request["population_id"],
        "reference_count": result["windows"]["reference"]["count"],
        "current_count": result["windows"]["current"]["count"],
        "evaluation_at": request["evaluation_at"],
        "limitations": ["synthetic labels", "read-only diagnostic",
                        "no alert/retrain/promotion", "no business readiness"],
    }


def finalize(payload: object, *, expected_request: dict, expected_run_id: str) -> dict:
    """Complete only the local read-only diagnostic after independent verification."""
    from hub_scripts.skill_execution.postflight import build_postflight
    if not isinstance(payload, dict) or payload.get("status") != "PASS":
        raise ValueError("FINALIZE_REQUIRES_PASS")
    checked = verify(payload, expected_request=expected_request, expected_run_id=expected_run_id)
    final = copy.deepcopy(payload)
    final["handoff"] = _handoff(expected_request, final["result"])
    receipt_check = checked["receipt_verification"] if checked["valid"] else {
        "status": "INVALID", "valid": False}
    final["postflight"] = build_postflight(
        final, contract=_contract(), receipt_verification=receipt_check,
        handoff=final["handoff"])
    final["scope_completion_authorized"] = (
        checked["valid"] and final["postflight"]["status"] == "PASS"
        and final["postflight"]["completion_authorized"] is True)
    return final


def verify_finalized(payload: object, *, expected_request: dict,
                     expected_run_id: str) -> dict:
    from hub_scripts.skill_execution.postflight import verify_postflight
    checked = verify(payload, expected_request=expected_request,
                     expected_run_id=expected_run_id)
    issues = list(checked["issues"])
    try:
        if not isinstance(payload, dict) or not isinstance(payload.get("handoff"), dict):
            raise ValueError("HANDOFF_MISSING")
        expected = _handoff(expected_request, payload["result"])
        if digest(payload["handoff"]) != digest(expected):
            issues.append("HANDOFF_ORACLE_MISMATCH")
        post = verify_postflight(
            payload, contract=_contract(),
            receipt_verification=checked["receipt_verification"]).to_dict()
        if not post["valid"] or not post["completion_authorized"]:
            issues.extend(post["issues"] or ["POSTFLIGHT_NOT_PASS"])
        if payload.get("scope_completion_authorized") is not True:
            issues.append("SCOPE_COMPLETION_NOT_AUTHORIZED")
    except Exception as exc:
        issues.append(type(exc).__name__ + ":" + str(exc))
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "scope": "LOCAL_SYNTHETIC_MATURE_PERFORMANCE_V1",
            "business_readiness": "NOT_EVALUATED", "promotion_authorized": False}
