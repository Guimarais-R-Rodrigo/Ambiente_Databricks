"""Candidate synthetic, read-only temporal feature execution for SER07/08."""
from __future__ import annotations

import importlib
import io
import json
import sys
import uuid
from contextlib import redirect_stdout
from datetime import timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import (
    ContextError, closed, digest, integer, loads_strict, text, utc_instant,
    validate_temporal_context,
)
from hub_scripts.skill_execution.domain_context.release import release_integrity

SKILL = "hub-ml-feature-engineering"
ENTRYPOINT = "skills/hub-ml-feature-engineering/scripts/run.py::run"
PRIMITIVE_ID = "temporal_features"
REQUIRED_RELEASE_PATHS = {
    f"skills/{SKILL}/execution_contract.json",
    f"skills/{SKILL}/scripts/run.py",
    f"skills/{SKILL}/scripts/verify.py",
    f"skills/{SKILL}/pit_view_contract.json",
    f"skills/{SKILL}/scripts/run_pit_features.py",
    f"skills/{SKILL}/pit_materialization_contract.json",
    f"skills/{SKILL}/scripts/run_pit_materialization.py",
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


def preflight(request: object) -> dict:
    """Resolve one fixed-lag UTC profile. No helper call or persistent effect."""
    try:
        data = closed(request, {"schema_version", "profile", "synthetic", "population_id",
                                "decision_at", "window_days", "requested_effect", "temporal", "rows"},
                      label="request")
        if data["schema_version"] != "SER07-REQUEST-1" or data["profile"] != "FIXED_LAG_L1_V1":
            raise ContextError("REQUEST:UNSUPPORTED_PROFILE")
        if data["synthetic"] is not True or data["requested_effect"] != "NONE":
            raise ContextError("REQUEST:SYNTHETIC_READ_ONLY_REQUIRED")
        text(data["population_id"], "population_id")
        decision = utc_instant(data["decision_at"], "decision_at")
        window = integer(data["window_days"], "window_days", minimum=1, maximum=365)
        temporal = validate_temporal_context(pit="APPLICABLE", temporal=data["temporal"],
                                             decision_at=data["decision_at"])
        spec = temporal["temporal"]
        if (spec["reference_column"], spec["availability_column"], spec["boundary"],
                spec["lag_days"]) != ("event_at", "available_at", "LE", 1):
            raise ContextError("TEMPORAL:FIXED_LAG_PROFILE_REQUIRED")
        rows = data["rows"]
        if not isinstance(rows, list) or not 2 <= len(rows) <= 1000:
            raise ContextError("ROWS:COUNT_OUT_OF_RANGE")
        ids, grains, eligible, excluded = set(), set(), [], {"future": 0, "unavailable": 0, "outside_window": 0}
        for row in rows:
            row = closed(row, {"id", "entity_id", "event_at", "available_at", "value"}, label="row")
            rid, entity = text(row["id"], "row_id"), text(row["entity_id"], "entity_id")
            event, available = utc_instant(row["event_at"], "event_at"), utc_instant(row["available_at"], "available_at")
            if rid in ids or (entity, event) in grains:
                raise ContextError("ROWS:DUPLICATE_ID_OR_GRAIN")
            ids.add(rid)
            grains.add((entity, event))
            if available != event + timedelta(days=1):
                raise ContextError("ROWS:AVAILABILITY_CONTRADICTS_DECLARED_LAG")
            if any((event.hour, event.minute, event.second, event.microsecond)):
                raise ContextError("ROWS:MIDNIGHT_UTC_PROFILE_ONLY")
            value = row["value"]
            if type(value) not in (int, float) or not -1e9 <= value <= 1e9:
                raise ContextError("ROWS:FINITE_NUMERIC_VALUE_REQUIRED")
            if event > decision:
                excluded["future"] += 1
            elif available > decision:
                excluded["unavailable"] += 1
            elif event < decision - timedelta(days=window):
                excluded["outside_window"] += 1
            else:
                eligible.append(row)
        if not eligible:
            raise ContextError("ROWS:NO_ELIGIBLE_HISTORY")
        from hub_scripts.skill_execution import run_preflight
        sef = run_preflight(SKILL_DIR / "execution_contract.json", assistant_root=ASSISTANT_ROOT,
                            context={}).to_dict()
        if sef["status"] != "PASS":
            raise ContextError("SEF:BLOCKED")
        return {"status": "PASS", "issues": [], "profile": data["profile"],
                "request_sha256": digest(data), "temporal_context": temporal,
                "eligible_ids": sorted(row["id"] for row in eligible),
                "excluded_counts": excluded, "sef": sef, "helper_called": False,
                "writes_performed": False}
    except (ContextError, TypeError, ValueError, OverflowError) as exc:
        return {"status": "BLOCKED", "issues": [str(exc)], "helper_called": False,
                "writes_performed": False}


def run(request: object, *, run_id: str | None = None) -> dict:
    trace = {"trace_version": "0.1", "skill": SKILL, "entrypoint": ENTRYPOINT,
             "run_id": str(uuid.uuid4()) if run_id is None else run_id, "status": "BLOCKED", "preflight_status": "NOT_RUN",
             "manifest": "release_manifest.json", "manifest_digest": None, "contract_digest": None,
             "runner_digest": None, "input_digest": None, "output_digest": None,
             "resources_resolved": [], "resources_called": [], "resources_completed": [],
             "decisions": [], "context_provenance": {}, "blocking_issues": [],
             "fallback_used": False, "writes_performed": False}
    pre = None
    try:
        if not isinstance(trace["run_id"], str) or not trace["run_id"].strip():
            raise ValueError("RUN_ID_REQUIRED")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][f"skills/{SKILL}/execution_contract.json"]
        trace["runner_digest"] = release["artifacts"][f"skills/{SKILL}/scripts/run.py"]
        pre = preflight(request)
        trace["preflight_status"] = pre["status"]
        if pre["status"] != "PASS":
            trace["blocking_issues"] = list(pre["issues"])
            return {"status": "BLOCKED", "preflight": pre, "trace": trace, "result": None, "receipt": None}
        trace["input_digest"] = digest(request)
        trace["resources_resolved"] = [PRIMITIVE_ID]
        trace["decisions"] = [{"item_id": item["item_id"], "item_type": "resource",
                               "applicable": item["applicable"], "resolved": item["resolved"]}
                              for item in pre["sef"]["resources"]]
        import pandas as pd
        eligible = [row for row in request["rows"] if row["id"] in pre["eligible_ids"]]
        frame = pd.DataFrame([{"id": row["id"], "entity_id": row["entity_id"],
                               "event_at": utc_instant(row["event_at"], "event_at").date().isoformat(), "value": row["value"]}
                              for row in eligible])
        module = importlib.import_module("hub_snippets.ml.lgbm_temporal")
        if Path(module.__file__).resolve() != (ASSISTANT_ROOT / "hub_snippets/ml/lgbm_temporal/__init__.py").resolve():
            raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
        primitive = module.create_temporal_features
        if Path(primitive.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_snippets/ml/lgbm_temporal/lgbm_temporal.py").resolve():
            raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
        trace["context_provenance"] = {"numeric_columns": {"source": "runtime_derived", "conflict": False,
                                                                  "value": len(frame.select_dtypes(include="number").columns)},
                                        "temporal": {"source": "user_intent", "conflict": False}}
        trace["resources_called"] = [PRIMITIVE_ID]
        with redirect_stdout(io.StringIO()):
            output = primitive(frame, target_col="value", date_col="event_at", lags=[1],
                               rolling_windows=[], calendar_features=False,
                               entity_cols=["entity_id"], on_duplicate_dates="raise")
        trace["resources_completed"] = [PRIMITIVE_ID]
        features = [{"id": str(row["id"]), "entity_id": str(row["entity_id"]),
                     "event_at": str(row["event_at"]), "lag_1": float(row["lag_1"])}
                    for _, row in output.sort_values(["entity_id", "event_at"]).iterrows()]
        result = {"schema_version": "SER07-RESULT-1", "profile": pre["profile"],
                  "population_id": request["population_id"], "decision_at": request["decision_at"],
                  "window_days": request["window_days"], "eligible_ids": pre["eligible_ids"],
                  "excluded_counts": pre["excluded_counts"], "features": features,
                  "fit_performed": False, "materialization_performed": False,
                  "promotion_authorized": False}
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL,
                                          expected_entrypoint=ENTRYPOINT, protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return {"status": "PASS", "preflight": pre, "trace": trace, "result": result, "receipt": receipt}
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [f"{type(exc).__name__}:{exc}"]
        return {"status": "BLOCKED", "preflight": pre, "trace": trace, "result": None, "receipt": None}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    payload = run(loads_strict(args.request.read_text(encoding="utf-8")), run_id=args.run_id)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
