"""Owned, synthetic Delta probe for an independently verified FE PIT view."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, loads_strict, text, utc_instant
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

PROFILE = "FREE_SYNTHETIC_PIT_FEATURE_MATERIALIZATION_V1"
BASE = "skills/hub-ml-feature-engineering/"
REQUIRED_RELEASE_PATHS = {
    BASE + "execution_contract.json",
    BASE + "pit_view_contract.json",
    BASE + "pit_materialization_contract.json",
    BASE + "scripts/run.py",
    BASE + "scripts/verify.py",
    BASE + "scripts/run_pit_features.py",
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


def _snapshot(value, label):
    try:
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False)
        return loads_strict(raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("NONCANONICAL_" + label) from exc


def _modules():
    fe = load_sibling(SKILL_DIR / "scripts/run_pit_features.py", "_ser08_fe_view_materializer")
    delta = load_sibling(ASSISTANT_ROOT / "skills/hub-ml-pipeline-builder/scripts/run_delta.py",
                         "_ser08_owned_delta_engine")
    return fe, delta


def _rows(features):
    if not isinstance(features, list):
        raise ValueError("FEATURE_ROWS_NOT_LIST")
    keys = {"decision_id", "entity_id", "decision_at", "feature_value", "available_at"}
    seen = set()
    rows = []
    for row in features:
        if not isinstance(row, dict) or set(row) != keys:
            raise ValueError("FEATURE_ROW_SHAPE_INVALID")
        decision_id = text(row["decision_id"], "decision_id")
        entity_id = text(row["entity_id"], "entity_id")
        if decision_id in seen:
            raise ValueError("DUPLICATE_DECISION_ID")
        seen.add(decision_id)
        decision = utc_instant(row["decision_at"], "decision_at")
        if row["decision_at"] != decision.isoformat(timespec="microseconds").replace("+00:00", "Z"):
            raise ValueError("DECISION_TIMESTAMP_NOT_CANONICAL")
        value = row["feature_value"]
        availability = row["available_at"]
        if value is None:
            if availability is not None:
                raise ValueError("NULL_FEATURE_WITH_AVAILABILITY")
        else:
            if type(value) is not int or not -(2**63) <= value < 2**63:
                raise ValueError("FEATURE_NOT_INT64")
            available = utc_instant(availability, "available_at")
            if availability != available.isoformat(timespec="microseconds").replace("+00:00", "Z"):
                raise ValueError("AVAILABILITY_TIMESTAMP_NOT_CANONICAL")
            if available > decision:
                raise ValueError("FEATURE_AVAILABLE_AFTER_DECISION")
        rows.append({key: row[key] for key in
                     ("decision_id", "entity_id", "decision_at", "feature_value", "available_at")})
    return sorted(rows, key=lambda row: row["decision_id"])


def _bound_request(payload, context, datasets, window_days, upstream_run_id, view_run_id):
    fe, _ = _modules()
    checked = fe.verify(payload, expected_context=context, expected_datasets=datasets,
                        expected_window_days=window_days,
                        expected_upstream_run_id=upstream_run_id,
                        expected_view_run_id=view_run_id)
    if not checked["valid"]:
        raise ValueError("FEATURE_VIEW_INVALID:" + str(checked["issues"]))
    result = payload["result"]
    rows = _rows(result["features"])
    provenance = {
        "view_sha256": payload["feature_view_sha256"],
        "source_sha256": digest(result["source_content_sha256"]),
        "context_sha256": result["context_sha256"],
        "cutoff_sha256": digest({"decision_at": result["decision_at"],
                                 "window_days": result["window_days"]}),
        "receipt_sha256": digest(result["upstream_receipt_id"]),
        "postflight_sha256": digest(result["upstream_postflight_id"]),
    }
    request = {
        "schema_version": "SER08-FE-MATERIALIZATION-REQUEST-1", "profile": "FE_PIT",
        "feature_view_sha256": payload["feature_view_sha256"],
        "external_input_sha256": digest({"context": context, "datasets": datasets,
                                         "window_days": window_days,
                                         "upstream_run_id": upstream_run_id,
                                         "view_run_id": view_run_id}),
        "upstream_receipt_id": result["upstream_receipt_id"],
        "upstream_postflight_id": result["upstream_postflight_id"],
        "rows": rows,
    }
    return request, provenance


def _materialization_preflight():
    from hub_scripts.skill_execution import run_preflight
    return run_preflight(SKILL_DIR / "pit_materialization_contract.json",
                         assistant_root=ASSISTANT_ROOT, context={}).to_dict()


def effect_request(payload: dict, *, expected_context: dict, expected_datasets: dict,
                   expected_window_days: int, expected_upstream_run_id: str,
                   expected_view_run_id: str) -> dict:
    """Read-only preparation; caller binds authorization.request_digest to this exact result."""
    values = [_snapshot(value, label) for value, label in (
        (payload, "VIEW_PAYLOAD"), (expected_context, "CONTEXT"),
        (expected_datasets, "DATASETS"), (expected_window_days, "WINDOW"),
        (expected_upstream_run_id, "UPSTREAM_RUN_ID"),
        (expected_view_run_id, "VIEW_RUN_ID"))]
    return _bound_request(*values)[0]


def execute(payload: dict, spark, authorization: dict, *, run_id: str,
            expected_context: dict, expected_datasets: dict, expected_window_days: int,
            expected_upstream_run_id: str, expected_view_run_id: str) -> dict:
    """Verify source PIT and view, then run the one owned Delta lifecycle and cleanup."""
    effect = {"schema_version": "SER08-FE-DELTA-EFFECT-1", "profile": PROFILE,
              "status": "BLOCKED", "phase": "NOT_RUN", "issues": [],
              "promotion_authorized": False, "business_readiness": "NOT_EVALUATED"}
    try:
        values = [_snapshot(value, label) for value, label in (
            (payload, "VIEW_PAYLOAD"), (expected_context, "CONTEXT"),
            (expected_datasets, "DATASETS"), (expected_window_days, "WINDOW"),
            (expected_upstream_run_id, "UPSTREAM_RUN_ID"),
            (expected_view_run_id, "VIEW_RUN_ID"), (authorization, "AUTHORIZATION"))]
        payload, context, datasets, window, upstream_id, view_id, auth = values
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        sef = _materialization_preflight()
        if sef["status"] != "PASS":
            raise ValueError("FE_MATERIALIZATION_CONTRACT_BLOCKED")
        request, provenance = _bound_request(payload, context, datasets,
                                             window, upstream_id, view_id)
        _, delta = _modules()
        effect = delta._execute_owned(request, request["rows"], spark, auth,
                                      run_id=run_id, profile="FE_PIT",
                                      provenance=provenance)
        effect["fe_manifest_sha256"] = release["manifest_sha256"]
        effect["feature_view_sha256"] = payload["feature_view_sha256"]
        effect["upstream_postflight_id"] = request["upstream_postflight_id"]
        effect["promotion_authorized"] = False
        effect["business_readiness"] = "NOT_EVALUATED"
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            effect["issues"].append("FE_RELEASE_CHANGED_DURING_EFFECT")
            effect["status"] = "BLOCKED" if effect.get("table_absent_after_cleanup") else "UNKNOWN"
    except Exception as exc:
        effect["issues"].append(type(exc).__name__ + ":" + str(exc))
        if effect.get("create_attempted") and effect.get("table_absent_after_cleanup") is not True:
            effect["status"] = "UNKNOWN"
        else:
            effect["status"] = "BLOCKED"
    return effect
