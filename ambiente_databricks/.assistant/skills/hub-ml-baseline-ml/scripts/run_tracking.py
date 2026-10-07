"""Authorized ephemeral MLflow tracking of the exact computed Baseline model."""
from __future__ import annotations

import importlib
import json
import math
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))
from hub_scripts.skill_execution.domain_context import digest, loads_strict
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

PROFILE = "SYNTHETIC_PERSONAL_MLFLOW_TRACKING_V1"
AUTH_FIELDS = {"schema_version", "authorized", "effect", "target_experiment",
               "request_sha256", "run_id", "current_user", "retention", "authorization_id"}


def _snapshot(value: object) -> object:
    """Freeze exact JSON inputs before callbacks; refuse lossy key/type coercion."""
    active = set()
    def check(item):
        if isinstance(item, dict):
            if id(item) in active:
                raise ValueError("SNAPSHOT_CYCLE")
            active.add(id(item))
            if any(type(key) is not str for key in item):
                raise ValueError("SNAPSHOT_NONSTRING_KEY")
            for nested in item.values():
                check(nested)
            active.remove(id(item))
        elif isinstance(item, list):
            if id(item) in active:
                raise ValueError("SNAPSHOT_CYCLE")
            active.add(id(item))
            for nested in item:
                check(nested)
            active.remove(id(item))
        elif type(item) not in (str, int, float, bool, type(None)):
            raise ValueError("SNAPSHOT_NON_JSON_VALUE")
    check(value)
    return loads_strict(json.dumps(value, ensure_ascii=False, allow_nan=False))


def _helper():
    module = importlib.import_module("hub_snippets.ml.mlflow_run")
    expected = ASSISTANT_ROOT / "hub_snippets/ml/mlflow_run/__init__.py"
    if Path(module.__file__).resolve() != expected.resolve():
        raise RuntimeError("HELPER_IMPORT_ORIGIN_MISMATCH")
    fn = module.run_governado
    implementation = ASSISTANT_ROOT / "hub_snippets/ml/mlflow_run/mlflow_run.py"
    if Path(fn.__wrapped__.__code__.co_filename).resolve() != implementation.resolve():
        raise RuntimeError("HELPER_IMPLEMENTATION_ORIGIN_MISMATCH")
    return fn


def _identity(spark) -> str:
    user = spark.sql("SELECT current_user() AS user").first()["user"]
    if not isinstance(user, str) or not user or "/" in user or "\\" in user:
        raise ValueError("AUTHENTICATED_USER_INVALID")
    return user


def _authorize(request: object, authorization: object, *, run_id: str, user: str) -> str:
    if not isinstance(run_id, str) or not run_id.strip() or run_id != run_id.strip():
        raise ValueError("RUN_ID_REQUIRED")
    if not isinstance(authorization, dict) or set(authorization) != AUTH_FIELDS:
        raise ValueError("AUTH_RECORD_SHAPE_INVALID")
    target = authorization["target_experiment"]
    prefix = f"/Users/{user}/hub_lab/skills_delivery_"
    if (not isinstance(target, str) or not target.startswith(prefix)
            or re.fullmatch(r"[0-9a-f]{8,32}", target[len(prefix):]) is None):
        raise ValueError("TARGET_NOT_FRESH_PERSONAL_NAMESPACE")
    if (authorization["schema_version"] != "SER10-AUTH-1"
            or authorization["authorized"] is not True
            or authorization["effect"] != "CREATE_EXPERIMENT_RUN_LOG_MODEL_SOFTDELETE"
            or authorization["retention"] != "SOFT_DELETE_AFTER_READBACK"
            or authorization["current_user"] != user
            or authorization["request_sha256"] != digest(request)
            or authorization["run_id"] != run_id
            or not isinstance(authorization["authorization_id"], str)
            or not authorization["authorization_id"].strip()):
        raise ValueError("AUTH_BINDING_MISMATCH")
    return target


def run_tracking(request: object, authorization: object, spark, *, run_id: str) -> dict:
    effect = {"profile": PROFILE, "target_experiment": None,
              "experiment_id": None, "mlflow_run_id": None,
              "authenticated_user": None, "candidate_run_id": None,
              "authorization_sha256": None, "request_sha256": None,
              "compute_receipt_id": None, "release_manifest_sha256": None,
              "readback": None, "live_verification": None,
              "cleanup_observation": {"run": None, "experiment": None},
              "cleanup": {"run": "NOT_CREATED", "experiment": "NOT_CREATED"},
              "residue": "NONE_OBSERVED", "attempts": []}
    payload = {"status": "BLOCKED", "issues": [], "compute": None, "effect": effect,
               "tracking_receipt": None, "promotion_authorized": False}
    client = None
    mlflow_run_id = None
    experiment_id = None
    live_verified = False
    try:
        request = _snapshot(request)
        authorization = _snapshot(authorization)
        user = _identity(spark)
        effect["authenticated_user"] = user
        target = _authorize(request, authorization, run_id=run_id, user=user)
        effect["target_experiment"] = target
        effect["candidate_run_id"] = run_id
        effect["authorization_sha256"] = digest(authorization)
        effect["request_sha256"] = digest(request)
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser10_compute_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        effect["release_manifest_sha256"] = release["manifest_sha256"]
        from hub_scripts.skill_execution import run_preflight
        contract = run_preflight(SKILL_DIR / "tracking_contract.json",
                                 assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        if contract["status"] != "PASS":
            raise ValueError("TRACKING_CONTRACT_BLOCKED")
        helper = _helper()
        import mlflow
        import mlflow.sklearn
        if mlflow.get_tracking_uri() != "databricks":
            raise ValueError("EXPLICIT_DATABRICKS_TRACKING_URI_REQUIRED")
        if mlflow.active_run() is not None:
            raise ValueError("EXISTING_ACTIVE_RUN_NOT_OWNED")
        client = mlflow.tracking.MlflowClient()
        if client.get_experiment_by_name(target) is not None:
            raise ValueError("EXPERIMENT_ALREADY_EXISTS_NOT_OWNED")
        compute, model = runner._execute(request, run_id=run_id)
        payload["compute"] = compute
        if compute["status"] != "PASS" or model is None:
            raise ValueError("BASELINE_COMPUTE_BLOCKED")
        effect["compute_receipt_id"] = compute["receipt"]["receipt_id"]
        check = load_sibling(SKILL_DIR / "scripts/verify.py", "_ser10_compute_verify").verify(
            compute, expected_request=request, expected_run_id=run_id)
        if check["valid"] is not True:
            raise ValueError("BASELINE_COMPUTE_VERIFICATION_FAILED")
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_BEFORE_EFFECT")
        from pandas import DataFrame
        import numpy as np
        frame = DataFrame(request["rows"])
        X = frame[request["feature_order"]]
        expected_proba = model.predict_proba(X)
        expected_params = {"seed": str(request["seed"]),
                           "threshold": str(request["threshold"]),
                           "request_sha256": digest(request)}
        holdout = compute["result"]["partitions"]["holdout"]["metrics"]
        expected_metrics = {"holdout_auc_roc": float(holdout["auc_roc"]),
                            "holdout_brier_score": float(holdout["brier_score"])}
        expected_tags = {
            "dataset": "SYNTHETIC:" + request["population_id"] + ":" + digest(request),
            "split": "temporal train/validation/holdout; train-only fit",
            "limitacoes": "synthetic only | no business readiness | no registry or deployment",
            "compute_receipt_id": compute["receipt"]["receipt_id"],
            "candidate_run_id": run_id,
            "authorization_id": authorization["authorization_id"],
            "release_manifest_sha256": release["manifest_sha256"],
        }
        mlflow.autolog(disable=True)
        mlflow.sklearn.autolog(disable=True)
        effect["attempts"].append("CREATE_EXPERIMENT")
        experiment_id = client.create_experiment(target)
        effect["experiment_id"] = experiment_id
        effect["cleanup"]["experiment"] = "PENDING"
        effect["attempts"].append("CREATE_RUN_AND_LOG")
        with helper("synthetic-baseline-" + run_id, dataset=expected_tags["dataset"],
                    split=expected_tags["split"],
                    limitacoes=["synthetic only", "no business readiness",
                                "no registry or deployment"], experimento=target) as governed:
            active = mlflow.active_run()
            if active is None:
                raise RuntimeError("HELPER_DID_NOT_CREATE_RUN")
            mlflow_run_id = active.info.run_id
            effect["mlflow_run_id"] = mlflow_run_id
            effect["cleanup"]["run"] = "PENDING"
            mlflow.set_tags({key: expected_tags[key] for key in
                             ("compute_receipt_id", "candidate_run_id",
                              "authorization_id", "release_manifest_sha256")})
            governed.parametros(expected_params)
            governed.metricas(expected_metrics)
            governed.modelo(model, exemplo_entrada=X, nome="model")
        effect["attempts"].append("READBACK")
        observed = client.get_run(mlflow_run_id)
        if (observed.info.status != "FINISHED"
                or observed.info.experiment_id != experiment_id
                or any(observed.data.params.get(k) != v for k, v in expected_params.items())
                or any(not math.isclose(observed.data.metrics.get(k, float("nan")), v,
                                        rel_tol=0, abs_tol=1e-12)
                       for k, v in expected_metrics.items())
                or any(observed.data.tags.get(k) != v for k, v in expected_tags.items())):
            raise RuntimeError("RUN_READBACK_MISMATCH")
        model_uri = "runs:/" + mlflow_run_id + "/model"
        info = mlflow.models.get_model_info(model_uri)
        if info.signature is None or info.saved_input_example_info is None:
            raise RuntimeError("MODEL_SIGNATURE_OR_EXAMPLE_MISSING")
        loaded = mlflow.sklearn.load_model(model_uri)
        actual_proba = loaded.predict_proba(X)
        if not np.allclose(actual_proba, expected_proba, rtol=1e-12, atol=1e-12):
            raise RuntimeError("MODEL_PREDICTION_READBACK_MISMATCH")
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_AFTER_EFFECT")
        effect["readback"] = {
            "run_status": "FINISHED", "experiment_id": experiment_id,
            "params": expected_params, "metrics": expected_metrics, "tags": expected_tags,
            "signature": True, "input_example": True,
            "prediction_sha256": digest([float(x) for x in actual_proba[:, 1]]),
            "positive_class_probabilities": [float(x) for x in actual_proba[:, 1]],
            "model_uri": model_uri,
        }
        payload["status"] = "PENDING_VERIFICATION"
        effect["attempts"].append("LIVE_VERIFY")
        live_verifier = load_sibling(SKILL_DIR / "scripts/verify_tracking.py",
                                     "_ser10_live_before_cleanup")
        observed_live = live_verifier.verify_live(
            payload, expected_request=request, expected_authorization=authorization,
            expected_run_id=run_id, authenticated_user=user, client=client,
            mlflow_module=mlflow)
        effect["live_verification"] = observed_live
        if observed_live["valid"] is not True:
            raise RuntimeError("INDEPENDENT_LIVE_VERIFICATION_FAILED")
        live_verified = True
    except Exception as exc:
        payload["status"] = "BLOCKED"
        payload["issues"].append(type(exc).__name__ + ":" + str(exc))
    finally:
        # A timeout after creation can hide an ID. Never infer that no remote
        # residue exists merely because create_experiment/start_run raised.
        if "CREATE_EXPERIMENT" in effect["attempts"] and experiment_id is None:
            effect["cleanup"]["experiment"] = "UNKNOWN_RESIDUE"
        if "CREATE_RUN_AND_LOG" in effect["attempts"] and mlflow_run_id is None:
            effect["cleanup"]["run"] = "UNKNOWN_RESIDUE"
        if client is not None and experiment_id is not None:
            if mlflow_run_id is not None:
                try:
                    effect["attempts"].append("SOFT_DELETE_RUN")
                    client.delete_run(mlflow_run_id)
                    observed_deleted_run = client.get_run(mlflow_run_id)
                    if (observed_deleted_run.info.run_id != mlflow_run_id
                            or observed_deleted_run.info.lifecycle_stage != "deleted"
                            or observed_deleted_run.info.experiment_id != experiment_id):
                        raise RuntimeError("RUN_SOFT_DELETE_READBACK_MISMATCH")
                    effect["cleanup_observation"]["run"] = {
                        "run_id": mlflow_run_id, "experiment_id": experiment_id,
                        "lifecycle_stage": "deleted"}
                    effect["cleanup"]["run"] = "SOFT_DELETED"
                except Exception as exc:
                    effect["cleanup"]["run"] = "UNKNOWN_RESIDUE"
                    payload["issues"].append("RUN_CLEANUP:" + type(exc).__name__ + ":" + str(exc))
            try:
                effect["attempts"].append("SOFT_DELETE_EXPERIMENT")
                client.delete_experiment(experiment_id)
                observed_deleted_experiment = client.get_experiment(experiment_id)
                if (observed_deleted_experiment.experiment_id != experiment_id
                        or observed_deleted_experiment.lifecycle_stage != "deleted"):
                    raise RuntimeError("EXPERIMENT_SOFT_DELETE_READBACK_MISMATCH")
                effect["cleanup_observation"]["experiment"] = {
                    "experiment_id": experiment_id, "lifecycle_stage": "deleted"}
                effect["cleanup"]["experiment"] = "SOFT_DELETED"
            except Exception as exc:
                effect["cleanup"]["experiment"] = "UNKNOWN_RESIDUE"
                payload["issues"].append("EXPERIMENT_CLEANUP:" + type(exc).__name__ + ":" + str(exc))
        if "UNKNOWN_RESIDUE" in effect["cleanup"].values():
            effect["residue"] = "UNKNOWN_RESIDUE"
        # No intermediate status can escape this single-call protocol.
        payload["status"] = "BLOCKED"
        if (live_verified and not payload["issues"]
                and effect["cleanup"] == {"run": "SOFT_DELETED", "experiment": "SOFT_DELETED"}):
            payload["status"] = "PASS"
    return payload
