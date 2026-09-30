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

SKILL = "hub-ml-monitoramento-modelo"
ENTRYPOINT = "skills/hub-ml-monitoramento-modelo/scripts/run.py::run"
PRIMITIVE_ID = "drift_numeric"
LOCAL_FILES = {"input.schema.json", "execution_contract.json", "scripts/preflight.py",
               "scripts/run.py", "scripts/verify.py"}
DEPENDENCIES = {"hub_scripts/skill_execution/__init__.py",
                "hub_scripts/skill_execution/skill_execution.py",
                "hub_scripts/skill_execution/receipt/__init__.py",
                "hub_scripts/skill_execution/domain_context/__init__.py",
                "hub_scripts/skill_execution/domain_context/release.py",
                "hub_snippets/ml/drift_detection/__init__.py",
                "hub_snippets/ml/drift_detection/drift_detection.py"}
REQUIRED_RELEASE_PATHS = {f"skills/{SKILL}/{name}" for name in LOCAL_FILES} | DEPENDENCIES
REQUIRED_RELEASE_PATHS |= {f"skills/{SKILL}/{name}" for name in {'performance_input.schema.json', 'scripts/run_performance.py', 'scripts/verify_performance.py', 'scripts/preflight_performance.py', 'performance_contract.json'}} | {'hub_scripts/skill_execution/postflight/__init__.py', 'hub_snippets/visual/tema/tema.py', 'hub_snippets/visual/theme_plotly/theme_plotly.py', 'hub_snippets/ml/performance_monitor/performance_monitor.py', 'hub_snippets/ml/metrics_report/__init__.py', 'hub_snippets/visual/tema/__init__.py', 'hub_snippets/visual/theme_plotly/__init__.py', 'hub_snippets/ml/performance_monitor/__init__.py', 'hub_snippets/ml/metrics_report/metrics_report.py', 'hub_snippets/constants/colors/colors.py', 'hub_snippets/constants/colors/__init__.py'}


def _canonical():
    module = importlib.import_module("hub_snippets.ml.drift_detection")
    if Path(module.__file__).resolve() != (ASSISTANT_ROOT / "hub_snippets/ml/drift_detection/__init__.py").resolve():
        raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
    for name in ("calculate_psi", "calculate_ks"):
        if Path(getattr(module, name).__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_snippets/ml/drift_detection/drift_detection.py").resolve():
            raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
    return module.calculate_psi, module.calculate_ks


def run(request: object, *, run_id: str | None = None) -> dict:
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
        preflight_result = load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser11_preflight").preflight(request)
        trace["preflight_status"] = preflight_result["status"]
        if preflight_result["status"] != "PASS":
            trace["blocking_issues"] = list(preflight_result["issues"])
            return {"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                    "result": None, "receipt": None}
        import pandas as pd
        import numpy as np
        frame = pd.DataFrame(request["reference"] + request["current"], columns=["id", "observed_at", "score"])
        psi_fn, ks_fn = _canonical()
        trace["input_digest"] = digest(request)
        trace["resources_resolved"] = [PRIMITIVE_ID]
        trace["decisions"] = [{"item_id": x["item_id"], "item_type": "resource",
                               "applicable": x["applicable"], "resolved": x["resolved"]}
                              for x in preflight_result["sef"]["resources"]]
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False,
                                "value": len(frame.select_dtypes(include="number").columns)},
            "population": {"source": "user_intent", "conflict": False},
            "windows": {"source": "user_intent", "conflict": False}}
        ref = np.array([row["score"] if row["score"] is not None else np.nan for row in request["reference"]], dtype=float)
        cur = np.array([row["score"] if row["score"] is not None else np.nan for row in request["current"]], dtype=float)
        trace["resources_called"] = [PRIMITIVE_ID]
        psi = psi_fn(ref, cur, n_bins=request["n_bins"], eps=request["eps"])
        ks, pvalue = ks_fn(ref, cur)
        trace["resources_completed"] = [PRIMITIVE_ID]
        internal = np.unique(np.quantile(ref[np.isfinite(ref)], np.linspace(0, 1, request["n_bins"] + 1)[1:-1]))
        result = {"schema_version": "SER11-RESULT-1", "profile": request["profile"],
                  "model_id": request["model_id"], "model_version": request["model_version"],
                  "population_id": request["population_id"], "score_name": request["score_name"],
                  "windows": {name: {"start": request[f"{name}_start"], "end": request[f"{name}_end"],
                                    "ids": [r["id"] for r in request[name]],
                                    "count": len(request[name]),
                                    "missing_count": sum(r["score"] is None for r in request[name])}
                              for name in ("reference", "current")},
                  "n_bins": request["n_bins"], "eps": request["eps"],
                  "bin_edges_internal": [float(x) for x in internal],
                  "bin_policy": "REFERENCE_QUANTILES_UNIQUE_MINUS_INF_PLUS_INF_MISSING_BUCKET",
                  "psi": float(psi), "ks_statistic": float(ks), "ks_pvalue": float(pvalue),
                  "interpretation": "DISTRIBUTION_DIAGNOSTIC_ONLY",
                  "performance_evaluated": False, "action_performed": False}
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL,
                                          expected_entrypoint=ENTRYPOINT, protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return {"status": "PASS", "preflight": preflight_result, "trace": trace,
                "result": result, "receipt": receipt}
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [f"{type(exc).__name__}:{exc}"]
        return {"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                "result": None, "receipt": None}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    payload = run(loads_strict(args.request.read_text(encoding="utf-8")), run_id=args.run_id)
    print(json.dumps(payload, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
