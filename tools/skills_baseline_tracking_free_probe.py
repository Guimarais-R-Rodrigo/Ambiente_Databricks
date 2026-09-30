# Databricks notebook source
"""One authorized synthetic SER10 attempt; no retry or model registration."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

MARKER = "SKILLS_BASELINE_TRACKING_FREE_PROBE_V1"
report = {"marker": MARKER, "status": "FAIL", "scope": "PERSONAL_SYNTHETIC_EPHEMERAL_TRACKING",
          "promotion_authorized": False, "effect": None, "verification": None}


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("ADAPTER_MODULE_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fixture():
    return {
        "schema_version": "SER09-REQUEST-1", "profile": "BINARY_TEMPORAL_LOCAL_V1",
        "synthetic": True, "requested_effect": "NONE", "population_id": "SYNTHETIC-P01",
        "target": "target", "positive_class": 1, "unit": "synthetic_entity",
        "date_column": "observed_at", "feature_order": ["feature"],
        "train_pct": 0.5, "val_pct": 0.25, "gap_periods": 0, "period_unit": "M",
        "threshold": 0.5, "seed": 17,
        "rows": [{"id": f"B{i:02d}", "observed_at": f"2024-{i:02d}-01T00:00:00Z",
                  "feature": float(i % 5), "target": i % 2} for i in range(1, 13)],
    }


try:
    dbutils.widgets.text("assistant_root", "", "Published personal .assistant")
    dbutils.widgets.text("authorization_json", "", "Exact external SER10 authorization record")
    root = Path(dbutils.widgets.get("assistant_root")).resolve()
    authenticated_user = spark.sql("SELECT current_user() AS user").first()["user"]
    expected_root = Path("/Workspace/Users") / authenticated_user / ".assistant"
    if root != expected_root or not root.is_dir():
        raise ValueError("PERSONAL_ASSISTANT_ROOT_REQUIRED")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    sys.dont_write_bytecode = True
    from hub_scripts.skill_execution.domain_context import digest, loads_strict
    request = _fixture()
    authorization = loads_strict(dbutils.widgets.get("authorization_json"))
    if not isinstance(authorization, dict):
        raise ValueError("AUTHORIZATION_JSON_OBJECT_REQUIRED")
    import mlflow
    mlflow.set_tracking_uri("databricks")
    mlflow.set_registry_uri("databricks")
    if mlflow.get_tracking_uri() != "databricks":
        raise ValueError("EXPLICIT_DATABRICKS_TRACKING_URI_REQUIRED")
    if mlflow.active_run() is not None:
        raise ValueError("EXISTING_ACTIVE_RUN_NOT_OWNED")
    folder = root / "skills/hub-ml-baseline-ml"
    before = hashlib.sha256((folder / "release_manifest.json").read_bytes()).hexdigest()
    runner = _load(folder / "scripts/run_tracking.py", "_ser10_free_runner")
    verifier = _load(folder / "scripts/verify_tracking.py", "_ser10_free_verifier")
    run_id = authorization.get("run_id")
    report["request_sha256"] = digest(request)
    report["authorization_sha256"] = digest(authorization)
    report["target_experiment"] = authorization.get("target_experiment")
    report["candidate_run_id"] = run_id
    # Validation inside run_tracking compares target, digest, run ID and
    # authenticated user before any remote creation.
    outcome = runner.run_tracking(request, authorization, spark, run_id=run_id)
    report["effect"] = outcome["effect"]
    report["adapter_status"] = outcome["status"]
    report["issues"] = outcome["issues"]
    if outcome["status"] == "PASS":
        client = mlflow.tracking.MlflowClient()
        report["verification"] = verifier.verify_finalized(
            outcome, expected_request=request, expected_authorization=authorization,
            expected_run_id=run_id, authenticated_user=authenticated_user,
            client=client)
    report["release_manifest_sha256_before"] = before
    report["release_manifest_sha256_after"] = hashlib.sha256(
        (folder / "release_manifest.json").read_bytes()).hexdigest()
    if (outcome["status"] == "PASS" and report["verification"]["valid"] is True
            and report["release_manifest_sha256_before"] == report["release_manifest_sha256_after"]):
        report["status"] = "PASS"
except Exception as exc:
    report["error"] = type(exc).__name__ + ":" + str(exc)
    report["traceback"] = traceback.format_exc(limit=3)
output = json.dumps(report, ensure_ascii=False, sort_keys=True, default=str)
print(output)
dbutils.notebook.exit(output)
