from __future__ import annotations

import importlib
import sys
import uuid
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-monitoramento-modelo"
ENTRYPOINT = "skills/hub-ml-monitoramento-modelo/scripts/run_performance.py::run"
PRIMITIVES = ["binary_metrics", "performance_monitor"]
PRIMITIVE_ID = "performance_monitor"
REQUIRED_RELEASE_PATHS = {
    "hub_scripts/skill_execution/__init__.py",
    "hub_scripts/skill_execution/skill_execution.py",
    "hub_scripts/skill_execution/receipt/__init__.py",
    "hub_scripts/skill_execution/postflight/__init__.py",
    "hub_scripts/skill_execution/domain_context/__init__.py",
    "hub_scripts/skill_execution/domain_context/release.py",
    "hub_snippets/ml/drift_detection/__init__.py",
    "hub_snippets/ml/drift_detection/drift_detection.py",
    "hub_snippets/ml/metrics_report/__init__.py",
    "hub_snippets/ml/metrics_report/metrics_report.py",
    "hub_snippets/ml/performance_monitor/__init__.py",
    "hub_snippets/ml/performance_monitor/performance_monitor.py",
    "hub_snippets/constants/colors/__init__.py",
    "hub_snippets/constants/colors/colors.py",
    "hub_snippets/visual/tema/__init__.py",
    "hub_snippets/visual/tema/tema.py",
    "hub_snippets/visual/theme_plotly/__init__.py",
    "hub_snippets/visual/theme_plotly/theme_plotly.py",
} | {f"skills/{SKILL}/{name}" for name in (
    "execution_contract.json", "input.schema.json", "scripts/preflight.py",
    "scripts/run.py", "scripts/verify.py", "performance_contract.json",
    "performance_input.schema.json", "scripts/preflight_performance.py",
    "scripts/run_performance.py", "scripts/verify_performance.py")}


def _canonical():
    metrics = importlib.import_module("hub_snippets.ml.metrics_report")
    monitor = importlib.import_module("hub_snippets.ml.performance_monitor")
    for module, symbol, init, impl in (
        (metrics, "calculate_binary_metrics",
         "hub_snippets/ml/metrics_report/__init__.py",
         "hub_snippets/ml/metrics_report/metrics_report.py"),
        (monitor, "PerformanceMonitor",
         "hub_snippets/ml/performance_monitor/__init__.py",
         "hub_snippets/ml/performance_monitor/performance_monitor.py"),
    ):
        if Path(module.__file__).resolve() != (ASSISTANT_ROOT / init).resolve():
            raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH:" + symbol)
        obj = getattr(module, symbol)
        code = obj.__code__ if hasattr(obj, "__code__") else obj.__init__.__code__
        if Path(code.co_filename).resolve() != (ASSISTANT_ROOT / impl).resolve():
            raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH:" + symbol)
    return metrics.calculate_binary_metrics, monitor.PerformanceMonitor


def run(request: object, *, run_id: str | None = None) -> dict:
    trace = {"trace_version": "0.1", "skill": SKILL, "entrypoint": ENTRYPOINT,
             "run_id": run_id if run_id is not None else str(uuid.uuid4()),
             "status": "BLOCKED", "preflight_status": "NOT_RUN",
             "manifest": "release_manifest.json", "manifest_digest": None,
             "contract_digest": None, "runner_digest": None,
             "input_digest": None, "output_digest": None, "artifacts_digest": None,
             "resources_resolved": [], "resources_imported": [],
             "resources_called": [], "resources_completed": [],
             "templates_loaded": [], "template_digests": {},
             "decisions": [], "context_provenance": {}, "blocking_issues": [],
             "fallback_used": False, "writes_performed": False}
    domain = None
    try:
        if not isinstance(trace["run_id"], str) or not trace["run_id"].strip():
            raise ValueError("RUN_ID_REQUIRED")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][f"skills/{SKILL}/performance_contract.json"]
        trace["runner_digest"] = release["artifacts"][f"skills/{SKILL}/scripts/run_performance.py"]
        domain = load_sibling(SKILL_DIR / "scripts/preflight_performance.py",
                              "_ser12_preflight").preflight(request)
        trace["preflight_status"] = domain["status"]
        if domain["status"] != "PASS":
            trace["blocking_issues"] = domain["issues"]
            return {"status": "BLOCKED", "preflight": domain, "trace": trace,
                    "result": None, "artifacts": {}, "receipt": None,
                    "handoff": None, "postflight": None, "scope_completion_authorized": False}
        import numpy as np
        metric_fn, monitor_type = _canonical()
        trace["input_digest"] = digest(request)
        trace["resources_resolved"] = PRIMITIVES.copy()
        trace["resources_imported"] = PRIMITIVES.copy()
        trace["decisions"] = [{"item_id": x["item_id"], "item_type": "resource",
                               "applicable": x["applicable"], "resolved": x["resolved"]}
                              for x in domain["sef"]["resources"]]
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False, "value": 2},
            "population": {"source": "user_intent", "conflict": False},
            "windows": {"source": "user_intent", "conflict": False},
            "label_maturity": {"source": "runtime_derived", "conflict": False}}
        metrics = {}
        trace["resources_called"] = ["binary_metrics"]
        for name in ("reference", "current"):
            rows = request[name]
            y = np.array([r["label"] for r in rows], dtype=int)
            score = np.array([r["score"] for r in rows], dtype=float)
            measured = metric_fn(y, score)
            metrics[name] = {key: float(measured[key]) for key in
                             ("auc_roc", "ks_pct", "brier_score")}
        trace["resources_completed"] = ["binary_metrics"]
        policy = {"auc": dict(request["auc_thresholds"])}
        trace["resources_called"].append("performance_monitor")
        monitor = monitor_type({"auc": metrics["reference"]["auc_roc"]},
                               model_name=request["model_id"], policy=policy,
                               consecutive_alert_periods=3)
        monitor.add_period(request["current_end"],
                           {"auc": metrics["current"]["auc_roc"]},
                           n_predictions=len(request["current"]))
        status = monitor.get_current_status()
        decision = monitor.should_retrain()["decision"]
        trace["resources_completed"].append("performance_monitor")
        result = {
            "schema_version": "SER12-RESULT-1", "profile": request["profile"],
            "model_id": request["model_id"], "model_version": request["model_version"],
            "population_id": request["population_id"], "score_name": request["score_name"],
            "evaluation_at": request["evaluation_at"],
            "windows": {name: {"start": request[name + "_start"],
                               "end": request[name + "_end"],
                               "ids": domain["windows"][name]["ids"],
                               "count": domain["windows"][name]["count"]}
                        for name in ("reference", "current")},
            "metrics": metrics, "policy": policy,
            "auc_deterioration": float(monitor.history[-1]["auc_delta"]),
            "monitor_status": status, "investigation_decision": decision,
            "performance_evaluated": True, "action_performed": False,
            "automatic_retrain_authorized": False, "promotion_authorized": False}
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        from hub_scripts.skill_execution.postflight import sha256_digest
        artifacts = {PRIMITIVE_ID: result}
        trace["artifacts_digest"] = sha256_digest(artifacts)
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        if Path(build_execution_receipt.__code__.co_filename).resolve() != (
                ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py").resolve():
            raise RuntimeError("RECEIPT_IMPORT_ORIGIN_MISMATCH")
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL,
                                          expected_entrypoint=ENTRYPOINT,
                                          protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return {"status": "PASS", "preflight": domain, "trace": trace,
                "result": result, "artifacts": artifacts, "receipt": receipt,
                "handoff": None, "postflight": None, "scope_completion_authorized": False}
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [f"{type(exc).__name__}:{exc}"]
        return {"status": "BLOCKED", "preflight": domain, "trace": trace,
                "result": None, "artifacts": {}, "receipt": None,
                "handoff": None, "postflight": None, "scope_completion_authorized": False}
