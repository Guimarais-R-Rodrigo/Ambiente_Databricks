from __future__ import annotations

import importlib
import json
import sys
import uuid
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, loads_strict
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-baseline-ml"
ENTRYPOINT = "skills/hub-ml-baseline-ml/scripts/run.py::run"
PRIMITIVE_ID = "temporal_split"
LOCAL_FILES = {"input.schema.json", "execution_contract.json", "scripts/preflight.py",
               "scripts/run.py", "scripts/verify.py", "tracking_contract.json",
               "scripts/run_tracking.py", "scripts/verify_tracking.py"}
DEPENDENCIES = {"hub_scripts/skill_execution/__init__.py",
                "hub_scripts/skill_execution/skill_execution.py",
                "hub_scripts/skill_execution/receipt/__init__.py",
                "hub_scripts/skill_execution/domain_context/__init__.py",
                "hub_scripts/skill_execution/domain_context/release.py",
                "hub_snippets/ml/split_temporal/__init__.py",
                "hub_snippets/ml/split_temporal/split_temporal.py",
                "hub_snippets/ml/metrics_report/__init__.py",
                "hub_snippets/ml/metrics_report/metrics_report.py",
                "hub_snippets/ml/mlflow_run/__init__.py",
                "hub_snippets/ml/mlflow_run/mlflow_run.py"}
REQUIRED_RELEASE_PATHS = {f"skills/{SKILL}/{name}" for name in LOCAL_FILES} | DEPENDENCIES


def _canonical(module_name: str, symbol: str, implementation: str):
    module = importlib.import_module(module_name)
    if Path(module.__file__).resolve() != (ASSISTANT_ROOT / module_name.replace(".", "/") / "__init__.py").resolve():
        raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
    fn = getattr(module, symbol)
    if Path(fn.__code__.co_filename).resolve() != (ASSISTANT_ROOT / implementation).resolve():
        raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
    return fn


def _disable_autolog_before_fit() -> None:
    """Keep direct in-memory computation from creating ambient MLflow effects."""
    try:
        import mlflow
    except ImportError:
        return
    if mlflow.active_run() is not None:
        raise ValueError("EXISTING_ACTIVE_MLFLOW_RUN_NOT_OWNED")
    mlflow.autolog(disable=True)
    try:
        import mlflow.sklearn
    except ImportError:
        return
    mlflow.sklearn.autolog(disable=True)


def _execute(request: object, *, run_id: str | None = None) -> tuple[dict, object | None]:
    trace = {"trace_version": "0.1", "skill": SKILL, "entrypoint": ENTRYPOINT,
             "run_id": run_id if run_id is not None else str(uuid.uuid4()),
             "status": "BLOCKED", "preflight_status": "NOT_RUN", "manifest": "release_manifest.json",
             "manifest_digest": None, "contract_digest": None, "runner_digest": None,
             "input_digest": None, "output_digest": None, "resources_resolved": [],
             "resources_called": [], "resources_completed": [], "decisions": [],
             "context_provenance": {}, "blocking_issues": [], "fallback_used": False,
             "writes_performed": False}
    preflight_result = None
    try:
        if not isinstance(trace["run_id"], str) or not trace["run_id"].strip():
            raise ValueError("RUN_ID_REQUIRED")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][f"skills/{SKILL}/execution_contract.json"]
        trace["runner_digest"] = release["artifacts"][f"skills/{SKILL}/scripts/run.py"]
        preflight_result = load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser09_preflight").preflight(request)
        trace["preflight_status"] = preflight_result["status"]
        if preflight_result["status"] != "PASS":
            trace["blocking_issues"] = list(preflight_result["issues"])
            return ({"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                     "result": None, "receipt": None}, None)
        import pandas as pd
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        frame = pd.DataFrame(request["rows"], columns=["id", "observed_at", "feature", "target"])
        split = _canonical("hub_snippets.ml.split_temporal", "temporal_split",
                           "hub_snippets/ml/split_temporal/split_temporal.py")
        metrics = _canonical("hub_snippets.ml.metrics_report", "calculate_binary_metrics",
                             "hub_snippets/ml/metrics_report/metrics_report.py")
        trace["input_digest"] = digest(request)
        trace["resources_resolved"] = ["temporal_split", "metrics_report"]
        trace["decisions"] = [{"item_id": x["item_id"], "item_type": "resource",
                               "applicable": x["applicable"], "resolved": x["resolved"]}
                              for x in preflight_result["sef"]["resources"]]
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False,
                                "value": len(frame.select_dtypes(include="number").columns)},
            "population": {"source": "user_intent", "conflict": False},
            "calendar": {"source": "runtime_derived", "conflict": False}}
        trace["resources_called"].append("temporal_split")
        train, validation, holdout = split(frame, date_col="observed_at", train_pct=request["train_pct"],
                                          val_pct=request["val_pct"], gap_periods=request["gap_periods"],
                                          period_unit=request["period_unit"])
        trace["resources_completed"].append("temporal_split")
        partitions = {"train": train, "validation": validation, "holdout": holdout}
        if {name: part["id"].tolist() for name, part in partitions.items()} != preflight_result["partitions_expected"]:
            raise RuntimeError("SPLIT_PARTITION_BINDING_MISMATCH")
        _disable_autolog_before_fit()
        model = Pipeline([("scale", StandardScaler()),
                          ("classifier", LogisticRegression(random_state=request["seed"], max_iter=1000))])
        model.fit(train[request["feature_order"]], train["target"])
        output = {}
        for name, part in partitions.items():
            scores = model.predict_proba(part[request["feature_order"]])[:, 1]
            trace["resources_called"].append("metrics_report")
            report = metrics(part["target"].to_numpy(), scores, threshold=request["threshold"])
            trace["resources_completed"].append("metrics_report")
            output[name] = {"ids": part["id"].tolist(), "targets": part["target"].astype(int).tolist(),
                            "scores": [float(v) for v in scores],
                            "metrics": {"auc_roc": report["auc_roc"], "brier_score": report["brier_score"]}}
        result = {"schema_version": "SER09-RESULT-1", "profile": request["profile"],
                  "population_id": request["population_id"], "unit": request["unit"],
                  "feature_order": request["feature_order"], "target": request["target"],
                  "positive_class": request["positive_class"], "threshold": request["threshold"],
                  "seed": request["seed"], "partitions": output,
                  "fit_partition_sha256": digest(output["train"]["ids"]),
                  "scaler_mean": [float(x) for x in model.named_steps["scale"].mean_],
                  "scaler_scale": [float(x) for x in model.named_steps["scale"].scale_],
                  "coefficient": [float(x) for x in model.named_steps["classifier"].coef_[0]],
                  "intercept": float(model.named_steps["classifier"].intercept_[0]),
                  "promotion_authorized": False, "tracking": "IN_MEMORY_ONLY"}
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL,
                                          expected_entrypoint=ENTRYPOINT, protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return ({"status": "PASS", "preflight": preflight_result, "trace": trace,
                 "result": result, "receipt": receipt}, model)
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [f"{type(exc).__name__}:{exc}"]
        return ({"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                 "result": None, "receipt": None}, None)


def run(request: object, *, run_id: str | None = None) -> dict:
    """Stable computation-only API; tracking uses the exact model returned by _execute."""
    return _execute(request, run_id=run_id)[0]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    payload = run(loads_strict(args.request.read_text(encoding="utf-8")), run_id=args.run_id)
    print(json.dumps(payload, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
