# Databricks notebook source
"""Synthetic MLflow helper probe; does not certify Baseline L4."""
import hashlib
import json
import sys
import uuid
from pathlib import Path

MARKER = "SKILLS_TRACKING_FREE_PROBE_V1"
report = {"marker": MARKER, "status": "FAIL", "scope": "SYNTHETIC_HELPER_CAPABILITY_ONLY",
          "baseline_l4_certified": False, "effects": [], "cleanup": "NOT_REQUIRED"}
experiment_id = None
run_id = None
client = None
try:
    dbutils.widgets.text("assistant_root", "")
    dbutils.widgets.text("authorized_experiment", "")
    root = Path(dbutils.widgets.get("assistant_root")).resolve()
    experiment = dbutils.widgets.get("authorized_experiment")
    user = spark.sql("SELECT current_user() AS user").first()["user"]
    prefix = "/Users/" + user + "/hub_lab/skills_delivery_"
    if not experiment.startswith(prefix) or "/" in experiment[len(prefix):] or not experiment[len(prefix):].isalnum():
        raise ValueError("EXPLICIT_ISOLATED_PERSONAL_EXPERIMENT_REQUIRED")
    if root != Path("/Workspace/Users") / user / ".assistant":
        raise ValueError("PERSONAL_ASSISTANT_ROOT_REQUIRED")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root))
    import numpy as np
    import pandas as pd
    import mlflow
    import mlflow.sklearn
    from sklearn.linear_model import LogisticRegression
    import importlib
    helper_module = importlib.import_module("hub_snippets.ml.mlflow_run")
    run_governado = helper_module.run_governado
    implementation = root / "hub_snippets/ml/mlflow_run/mlflow_run.py"
    if (Path(helper_module.__file__).resolve() != implementation.with_name("__init__.py").resolve()
            or Path(run_governado.__wrapped__.__code__.co_filename).resolve() != implementation.resolve()):
        raise ValueError("HELPER_IMPORT_ORIGIN_MISMATCH")
    before = hashlib.sha256(implementation.read_bytes()).hexdigest()
    report["helper_sha256"] = before
    mlflow.autolog(disable=True)
    mlflow.sklearn.autolog(disable=True)
    if mlflow.active_run() is not None:
        raise ValueError("EXISTING_ACTIVE_RUN_NOT_OWNED")
    mlflow.set_tracking_uri("databricks")
    mlflow.set_registry_uri("databricks")
    client = mlflow.tracking.MlflowClient()
    if client.get_experiment_by_name(experiment) is not None:
        raise ValueError("EXPERIMENT_ALREADY_EXISTS_NOT_OWNED")
    experiment_id = client.create_experiment(experiment)
    report["effects"].append({"operation": "CREATE_EXPERIMENT", "experiment_id": experiment_id})
    X = pd.DataFrame({"synthetic_feature": [0.0, 1.0, 2.0, 3.0]})
    y = [0, 0, 1, 1]
    model = LogisticRegression(random_state=17).fit(X, y)
    with run_governado("synthetic-capability", dataset="SYNTHETIC_FOUR_ROWS",
                       split="fixed four-row helper probe; no model-quality claim",
                       limitacoes=["synthetic only", "helper capability is not Baseline L4"],
                       experimento=experiment) as run:
        run_id = mlflow.active_run().info.run_id
        report["effects"].append({"operation": "CREATE_RUN", "run_id": run_id})
        run.parametros({"seed": 17, "synthetic": True})
        run.metricas({"synthetic_metric": 0.5})
        run.modelo(model, exemplo_entrada=X, nome="model")
    observed = client.get_run(run_id)
    assert observed.info.status == "FINISHED"
    assert observed.info.experiment_id == experiment_id
    assert observed.data.params.get("seed") == "17"
    assert observed.data.metrics.get("synthetic_metric") == 0.5
    assert observed.data.tags.get("dataset") == "SYNTHETIC_FOUR_ROWS"
    uri = "runs:/" + run_id + "/model"
    info = mlflow.models.get_model_info(uri)
    assert info.signature is not None and info.saved_input_example_info is not None
    loaded = mlflow.sklearn.load_model(uri)
    assert np.allclose(loaded.predict_proba(X), model.predict_proba(X), rtol=1e-12, atol=1e-12)
    assert hashlib.sha256(implementation.read_bytes()).hexdigest() == before
    report["readback"] = {"run": True, "params": True, "metrics": True,
                          "signature": True, "model_predictions": True}
    report["status"] = "PASS"
except Exception as exc:
    report["error"] = type(exc).__name__ + ":" + str(exc)
finally:
    if experiment_id is not None and client is not None:
        try:
            if run_id is not None:
                client.delete_run(run_id)
                assert client.get_run(run_id).info.lifecycle_stage == "deleted"
            client.delete_experiment(experiment_id)
            assert client.get_experiment(experiment_id).lifecycle_stage == "deleted"
            report["cleanup"] = "SOFT_DELETED_NOT_PHYSICALLY_ERASED"
        except Exception as exc:
            report["cleanup"] = "UNKNOWN_RESIDUE"
            report["cleanup_error"] = type(exc).__name__ + ":" + str(exc)
            report["status"] = "FAIL"
output = json.dumps(report, sort_keys=True, default=str)
print(output)
dbutils.notebook.exit(output)
