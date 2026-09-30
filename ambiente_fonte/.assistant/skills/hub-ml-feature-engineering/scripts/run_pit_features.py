"""Read-only feature view composed from the independently verified Cross-EDA PIT."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, text
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-feature-engineering"
PROFILE = "COMPOSED_PIT_FEATURE_VIEW_V1"
BASE = f"skills/{SKILL}/"
REQUIRED_RELEASE_PATHS = {
    BASE + "execution_contract.json",
    BASE + "pit_view_contract.json",
    BASE + "scripts/run.py",
    BASE + "scripts/verify.py",
    BASE + "scripts/run_pit_features.py",
    BASE + "pit_materialization_contract.json",
    BASE + "scripts/run_pit_materialization.py",
    "skills/hub-ml-pipeline-builder/delta_execution_contract.json",
    "skills/hub-ml-pipeline-builder/scripts/run_delta.py",
    "hub_scripts/skill_execution/__init__.py",
    "hub_scripts/skill_execution/skill_execution.py",
    "hub_scripts/skill_execution/receipt/__init__.py",
    "hub_scripts/skill_execution/domain_context/__init__.py",
    "hub_scripts/skill_execution/domain_context/release.py",
    "hub_snippets/ml/lgbm_temporal/__init__.py",
    "hub_snippets/ml/lgbm_temporal/lgbm_temporal.py",
}

def _upstream():
    path = ASSISTANT_ROOT / "skills/hub-ml-cross-eda-ml/scripts"
    run = load_sibling(path / "run_pit.py", "_ser08_cross_pit_runner")
    verify = load_sibling(path / "verify_pit.py", "_ser08_cross_pit_verifier")
    return run, verify

def _projection(upstream: dict, *, context: dict, datasets: dict,
                window_days: int, view_run_id: str) -> dict:
    source_hashes = {s["id"]: s["content_sha256"] for s in context["sources"]}
    records = upstream["result"]["records"]
    return {
        "schema_version": "SER08-PIT-FEATURE-VIEW-1",
        "profile": PROFILE,
        "view_run_id": view_run_id,
        "source_content_sha256": source_hashes,
        "context_sha256": digest(context),
        "datasets_sha256": digest(datasets),
        "decision_at": context["decision_at"],
        "window_days": window_days,
        "upstream_manifest_sha256": upstream["receipt"]["release"]["manifest_sha256"],
        "upstream_receipt_id": upstream["receipt"]["receipt_id"],
        "upstream_postflight_id": upstream["postflight"]["postflight_id"],
        "upstream_result_sha256": digest(upstream["result"]),
        "features": [
            {"decision_id": row["decision_id"], "entity_id": row["entity_id"],
             "decision_at": row["decision_at"], "feature_value": row["feature_value"],
             "available_at": row["available_at"]}
            for row in records
        ],
        "fit_performed": False,
        "materialization_performed": False,
        "business_readiness": "NOT_EVALUATED",
        "promotion_authorized": False,
    }

def compose(context: dict, datasets: dict, spark, *, window_days: int,
            upstream_run_id: str, view_run_id: str) -> dict:
    """Execute Cross PIT once, finalize it, then expose only its checked projection."""
    try:
        text(upstream_run_id, "upstream_run_id")
        text(view_run_id, "view_run_id")
        if upstream_run_id == view_run_id:
            raise ValueError("RUN_IDS_MUST_DIFFER")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        input_sha256 = digest({"context": context, "datasets": datasets,
                               "window_days": window_days,
                               "upstream_run_id": upstream_run_id})
        from hub_scripts.skill_execution import run_preflight
        sef = run_preflight(SKILL_DIR / "pit_view_contract.json",
                            assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        if sef["status"] != "PASS":
            raise ValueError("PIT_VIEW_CONTRACT_BLOCKED")
        cross_run, cross_verify = _upstream()
        upstream = cross_run.run(context, datasets, spark, window_days=window_days,
                                 run_id=upstream_run_id)
        if upstream["status"] != "PASS":
            raise ValueError("UPSTREAM_PIT_BLOCKED:" + str(upstream["trace"]["blocking_issues"]))
        upstream = cross_verify.finalize(
            upstream, expected_context=context, expected_datasets=datasets,
            expected_window_days=window_days, expected_run_id=upstream_run_id)
        upstream_check = cross_verify.verify_finalized(
            upstream, expected_context=context, expected_datasets=datasets,
            expected_window_days=window_days, expected_run_id=upstream_run_id)
        if not upstream_check["valid"] or upstream.get("scope_completion_authorized") is not True:
            raise ValueError("UPSTREAM_PIT_POSTFLIGHT_INVALID:" + str(upstream_check["issues"]))
        result = _projection(upstream, context=context, datasets=datasets,
                             window_days=window_days, view_run_id=view_run_id)
        if digest({"context": context, "datasets": datasets,
                   "window_days": window_days,
                   "upstream_run_id": upstream_run_id}) != input_sha256:
            raise ValueError("FE_INPUT_CHANGED_DURING_EXECUTION")
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise ValueError("FE_RELEASE_CHANGED_DURING_EXECUTION")
        return {"status": "PASS", "scope": PROFILE, "view_run_id": view_run_id,
                "input_sha256": input_sha256,
                "fe_manifest_sha256": release["manifest_sha256"],
                "upstream_evidence": upstream, "result": result,
                "feature_view_sha256": digest(result),
                "receipt": None, "fit_performed": False,
                "materialization_performed": False, "promotion_authorized": False}
    except Exception as exc:
        return {"status": "BLOCKED", "scope": PROFILE, "view_run_id": view_run_id,
                "issues": [type(exc).__name__ + ":" + str(exc)],
                "upstream_evidence": None, "result": None, "receipt": None,
                "fit_performed": False, "materialization_performed": False,
                "promotion_authorized": False}

def verify(payload: object, *, expected_context: dict, expected_datasets: dict,
           expected_window_days: int, expected_upstream_run_id: str,
           expected_view_run_id: str) -> dict:
    """Recheck Cross's independent PIT oracle and bind every projected feature row."""
    issues = []
    try:
        text(expected_upstream_run_id, "expected_upstream_run_id")
        text(expected_view_run_id, "expected_view_run_id")
        if expected_upstream_run_id == expected_view_run_id:
            raise ValueError("EXPECTED_RUN_IDS_MUST_DIFFER")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        if not isinstance(payload, dict) or payload.get("status") != "PASS" or set(payload) != {
                "status", "scope", "view_run_id", "input_sha256", "fe_manifest_sha256",
                "upstream_evidence", "result", "feature_view_sha256", "receipt",
                "fit_performed", "materialization_performed", "promotion_authorized"}:
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if payload["scope"] != PROFILE or payload["view_run_id"] != expected_view_run_id:
            issues.append("VIEW_ID_OR_SCOPE_MISMATCH")
        expected_input = digest({"context": expected_context, "datasets": expected_datasets,
                                 "window_days": expected_window_days,
                                 "upstream_run_id": expected_upstream_run_id})
        if payload["input_sha256"] != expected_input:
            issues.append("EXTERNAL_INPUT_BINDING_MISMATCH")
        if payload["fe_manifest_sha256"] != release["manifest_sha256"]:
            issues.append("FE_RELEASE_BINDING_MISMATCH")
        _, cross_verify = _upstream()
        upstream = payload["upstream_evidence"]
        check = cross_verify.verify_finalized(
            upstream, expected_context=expected_context,
            expected_datasets=expected_datasets,
            expected_window_days=expected_window_days,
            expected_run_id=expected_upstream_run_id)
        if not check["valid"] or upstream.get("scope_completion_authorized") is not True:
            issues.append("UPSTREAM_PIT_EVIDENCE_INVALID:" + str(check["issues"]))
        else:
            expected = _projection(upstream, context=expected_context,
                                   datasets=expected_datasets,
                                   window_days=expected_window_days,
                                   view_run_id=expected_view_run_id)
            if digest(payload["result"]) != digest(expected):
                issues.append("FEATURE_VIEW_PROJECTION_MISMATCH")
            if payload["feature_view_sha256"] != digest(expected):
                issues.append("FEATURE_VIEW_DIGEST_MISMATCH")
        if payload["receipt"] is not None or payload["fit_performed"] is not False or payload["materialization_performed"] is not False or payload["promotion_authorized"] is not False:
            issues.append("UNAUTHORIZED_EFFECT_OR_RECEIPT_CLAIM")
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            issues.append("FE_RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(type(exc).__name__ + ":" + str(exc))
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "scope": PROFILE, "fit_performed": False,
            "materialization_performed": False, "promotion_authorized": False}
