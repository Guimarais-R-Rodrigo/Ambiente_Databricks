"""Read-only verification of compute, exact authority binding and soft-delete."""
from __future__ import annotations

import math
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))
from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity


def verify_live(payload: object, *, expected_request: dict, expected_authorization: dict,
                expected_run_id: str, authenticated_user: str, client,
                mlflow_module=None) -> dict:
    """Independent remote readback while experiment and model remain live."""
    issues = []
    binding = None
    observation = None
    try:
        tracker = load_sibling(SKILL_DIR / "scripts/run_tracking.py", "_ser10_verify_tracker")
        expected_request = tracker._snapshot(expected_request)
        expected_authorization = tracker._snapshot(expected_authorization)
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser10_verify_compute_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        target = tracker._authorize(expected_request, expected_authorization,
                                    run_id=expected_run_id, user=authenticated_user)
        if (not isinstance(payload, dict) or set(payload) !=
                {"status", "issues", "compute", "effect", "tracking_receipt",
                 "promotion_authorized"} or payload["status"] != "PENDING_VERIFICATION"
                or payload["issues"] != [] or payload["tracking_receipt"] is not None
                or payload["promotion_authorized"] is not False):
            raise ValueError("TRACKING_PAYLOAD_NOT_CANONICAL_PASS")
        compute = payload["compute"]
        check = load_sibling(SKILL_DIR / "scripts/verify.py", "_ser10_verify_compute").verify(
            compute, expected_request=expected_request, expected_run_id=expected_run_id)
        if check["valid"] is not True:
            issues.append("COMPUTE_RECEIPT_OR_ORACLE_INVALID")
        effect = payload["effect"]
        if not isinstance(effect, dict) or set(effect) != {
                "profile", "target_experiment", "experiment_id", "mlflow_run_id",
                "authenticated_user", "candidate_run_id", "authorization_sha256",
                "request_sha256", "compute_receipt_id", "release_manifest_sha256",
                "readback", "live_verification", "cleanup_observation",
                "cleanup", "residue", "attempts"}:
            raise ValueError("EFFECT_RECORD_SCHEMA_INVALID")
        expected_binding = {
            "profile": tracker.PROFILE, "target_experiment": target,
            "authenticated_user": authenticated_user, "candidate_run_id": expected_run_id,
            "authorization_sha256": digest(expected_authorization),
            "request_sha256": digest(expected_request),
            "compute_receipt_id": compute["receipt"]["receipt_id"],
            "release_manifest_sha256": release["manifest_sha256"],
            "cleanup": {"run": "PENDING", "experiment": "PENDING"},
            "residue": "NONE_OBSERVED",
            "attempts": ["CREATE_EXPERIMENT", "CREATE_RUN_AND_LOG", "READBACK", "LIVE_VERIFY"],
            "live_verification": None,
            "cleanup_observation": {"run": None, "experiment": None},
        }
        if any(effect.get(key) != value for key, value in expected_binding.items()):
            issues.append("EFFECT_BINDING_MISMATCH")
        exp_id, mlflow_run_id = effect["experiment_id"], effect["mlflow_run_id"]
        if not isinstance(exp_id, str) or not exp_id or not isinstance(mlflow_run_id, str) or not mlflow_run_id:
            raise ValueError("REMOTE_IDS_INVALID")
        observed_run = client.get_run(mlflow_run_id)
        observed_experiment = client.get_experiment(exp_id)
        if (observed_run.info.experiment_id != exp_id
                or observed_run.info.status != "FINISHED"
                or observed_run.info.lifecycle_stage != "active"
                or observed_experiment.name != target
                or observed_experiment.experiment_id != exp_id
                or observed_experiment.lifecycle_stage != "active"):
            issues.append("REMOTE_LIVE_READBACK_MISMATCH")
        expected_params = {"seed": str(expected_request["seed"]),
                           "threshold": str(expected_request["threshold"]),
                           "request_sha256": digest(expected_request)}
        holdout = compute["result"]["partitions"]["holdout"]["metrics"]
        expected_metrics = {"holdout_auc_roc": float(holdout["auc_roc"]),
                            "holdout_brier_score": float(holdout["brier_score"])}
        expected_tags = {
            "dataset": "SYNTHETIC:" + expected_request["population_id"] + ":" + digest(expected_request),
            "split": "temporal train/validation/holdout; train-only fit",
            "limitacoes": "synthetic only | no business readiness | no registry or deployment",
            "compute_receipt_id": compute["receipt"]["receipt_id"],
            "candidate_run_id": expected_run_id,
            "authorization_id": expected_authorization["authorization_id"],
            "release_manifest_sha256": release["manifest_sha256"],
        }
        if (any(observed_run.data.params.get(k) != v for k, v in expected_params.items())
                or any(not math.isclose(observed_run.data.metrics.get(k, float("nan")), v,
                                        rel_tol=0, abs_tol=1e-12)
                       for k, v in expected_metrics.items())
                or any(observed_run.data.tags.get(k) != v for k, v in expected_tags.items())):
            issues.append("REMOTE_RUN_CONTENT_MISMATCH")
        readback = effect["readback"]
        if not isinstance(readback, dict) or set(readback) != {
                "run_status", "experiment_id", "params", "metrics", "tags",
                "signature", "input_example", "prediction_sha256",
                "positive_class_probabilities", "model_uri"}:
            raise ValueError("READBACK_SCHEMA_INVALID")
        if (readback["run_status"] != "FINISHED"
                or readback["experiment_id"] != exp_id
                or readback["params"] != expected_params
                or readback["metrics"] != expected_metrics
                or readback["tags"] != expected_tags
                or readback["signature"] is not True
                or readback["input_example"] is not True
                or readback["model_uri"] != "runs:/" + mlflow_run_id + "/model"):
            issues.append("RECORDED_READBACK_MISMATCH")
        if mlflow_module is None:
            import mlflow as mlflow_module
        if mlflow_module.get_tracking_uri() != "databricks":
            raise ValueError("EXPLICIT_DATABRICKS_TRACKING_URI_REQUIRED")
        remote_info = mlflow_module.models.get_model_info(readback["model_uri"])
        if remote_info.signature is None or remote_info.saved_input_example_info is None:
            issues.append("REMOTE_MODEL_SIGNATURE_OR_EXAMPLE_MISSING")
        from pandas import DataFrame
        remote_model = mlflow_module.sklearn.load_model(readback["model_uri"])
        remote_proba = remote_model.predict_proba(
            DataFrame(expected_request["rows"])[expected_request["feature_order"]])
        remote_scores = [float(x) for x in remote_proba[:, 1]]
        if readback["prediction_sha256"] != digest(remote_scores):
            issues.append("REMOTE_PREDICTION_DIGEST_MISMATCH")
        scores = readback["positive_class_probabilities"]
        if readback["prediction_sha256"] != digest(scores):
            issues.append("PREDICTION_DIGEST_MISMATCH")
        rows = expected_request["rows"]
        if not isinstance(scores, list) or len(scores) != len(rows):
            issues.append("PREDICTION_COUNT_MISMATCH")
        else:
            if len(remote_scores) != len(scores) or any(
                    not math.isclose(a, b, rel_tol=0, abs_tol=1e-12)
                    for a, b in zip(remote_scores, scores)):
                issues.append("REMOTE_PREDICTION_RECORD_MISMATCH")
            mean = compute["result"]["scaler_mean"][0]
            scale = compute["result"]["scaler_scale"][0]
            coefficient = compute["result"]["coefficient"][0]
            intercept = compute["result"]["intercept"]
            for row, score in zip(rows, scores):
                linear = intercept + coefficient * ((row["feature"] - mean) / scale)
                oracle = (1 / (1 + math.exp(-linear)) if linear >= 0
                          else math.exp(linear) / (1 + math.exp(linear)))
                if type(score) is not float or not math.isclose(score, oracle, rel_tol=0, abs_tol=1e-12):
                    issues.append("PREDICTION_ORACLE_MISMATCH")
                    break
            for row, score in zip(rows, remote_scores):
                linear = intercept + coefficient * ((row["feature"] - mean) / scale)
                oracle = (1 / (1 + math.exp(-linear)) if linear >= 0
                          else math.exp(linear) / (1 + math.exp(linear)))
                if not math.isclose(score, oracle, rel_tol=0, abs_tol=1e-12):
                    issues.append("REMOTE_MODEL_ORACLE_MISMATCH")
                    break
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
        binding = {
            "request_sha256": digest(expected_request),
            "authorization_sha256": digest(expected_authorization),
            "candidate_run_id": expected_run_id,
            "compute_receipt_id": compute["receipt"]["receipt_id"],
            "release_manifest_sha256": release["manifest_sha256"],
            "experiment_id": exp_id, "mlflow_run_id": mlflow_run_id,
            "target_experiment": target,
        }
        observation = {
            "run_status": observed_run.info.status,
            "run_lifecycle_stage": observed_run.info.lifecycle_stage,
            "experiment_lifecycle_stage": observed_experiment.lifecycle_stage,
            "experiment_name": observed_experiment.name,
            "signature": remote_info.signature is not None,
            "input_example": remote_info.saved_input_example_info is not None,
            "prediction_sha256": digest(remote_scores),
        }
    except Exception as exc:
        issues.append(type(exc).__name__ + ":" + str(exc))
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "scope": "PERSONAL_SYNTHETIC_EPHEMERAL_TRACKING",
            "binding": binding, "observation": observation,
            "authority_authenticated": False, "model_readback_phase": "BEFORE_CLEANUP",
            "promotion_authorized": False}


def verify_finalized(payload: object, *, expected_request: dict,
                     expected_authorization: dict, expected_run_id: str,
                     authenticated_user: str, client) -> dict:
    """Check bindings and cleanup; model API is unavailable after experiment deletion."""
    issues = []
    try:
        tracker = load_sibling(SKILL_DIR / "scripts/run_tracking.py", "_ser10_final_tracker")
        expected_request = tracker._snapshot(expected_request)
        expected_authorization = tracker._snapshot(expected_authorization)
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser10_final_compute_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        target = tracker._authorize(expected_request, expected_authorization,
                                    run_id=expected_run_id, user=authenticated_user)
        if (not isinstance(payload, dict) or set(payload) != {
                "status", "issues", "compute", "effect", "tracking_receipt",
                "promotion_authorized"} or payload["status"] != "PASS"
                or payload["issues"] != [] or payload["tracking_receipt"] is not None
                or payload["promotion_authorized"] is not False):
            raise ValueError("FINAL_PAYLOAD_NOT_CANONICAL_PASS")
        compute = payload["compute"]
        compute_check = load_sibling(
            SKILL_DIR / "scripts/verify.py", "_ser10_final_compute_verify").verify(
                compute, expected_request=expected_request, expected_run_id=expected_run_id)
        if compute_check["valid"] is not True:
            issues.append("COMPUTE_RECEIPT_OR_ORACLE_INVALID")
        effect = payload["effect"]
        if not isinstance(effect, dict) or set(effect) != {
                "profile", "target_experiment", "experiment_id", "mlflow_run_id",
                "authenticated_user", "candidate_run_id", "authorization_sha256",
                "request_sha256", "compute_receipt_id", "release_manifest_sha256",
                "readback", "live_verification", "cleanup_observation",
                "cleanup", "residue", "attempts"}:
            raise ValueError("FINAL_EFFECT_SCHEMA_INVALID")
        binding = {
            "request_sha256": digest(expected_request),
            "authorization_sha256": digest(expected_authorization),
            "candidate_run_id": expected_run_id,
            "compute_receipt_id": compute["receipt"]["receipt_id"],
            "release_manifest_sha256": release["manifest_sha256"],
            "experiment_id": effect["experiment_id"],
            "mlflow_run_id": effect["mlflow_run_id"],
            "target_experiment": target,
        }
        readback = effect["readback"]
        if not isinstance(readback, dict) or set(readback) != {
                "run_status", "experiment_id", "params", "metrics", "tags",
                "signature", "input_example", "prediction_sha256",
                "positive_class_probabilities", "model_uri"}:
            raise ValueError("FINAL_READBACK_SCHEMA_INVALID")
        expected_params = {"seed": str(expected_request["seed"]),
                           "threshold": str(expected_request["threshold"]),
                           "request_sha256": digest(expected_request)}
        holdout = compute["result"]["partitions"]["holdout"]["metrics"]
        expected_metrics = {"holdout_auc_roc": float(holdout["auc_roc"]),
                            "holdout_brier_score": float(holdout["brier_score"])}
        expected_tags = {
            "dataset": "SYNTHETIC:" + expected_request["population_id"] + ":" + digest(expected_request),
            "split": "temporal train/validation/holdout; train-only fit",
            "limitacoes": "synthetic only | no business readiness | no registry or deployment",
            "compute_receipt_id": compute["receipt"]["receipt_id"],
            "candidate_run_id": expected_run_id,
            "authorization_id": expected_authorization["authorization_id"],
            "release_manifest_sha256": release["manifest_sha256"],
        }
        if (readback["run_status"] != "FINISHED"
                or readback["experiment_id"] != effect["experiment_id"]
                or readback["params"] != expected_params
                or readback["metrics"] != expected_metrics
                or readback["tags"] != expected_tags
                or readback["signature"] is not True
                or readback["input_example"] is not True
                or readback["model_uri"] != "runs:/" + effect["mlflow_run_id"] + "/model"):
            issues.append("FINAL_RECORDED_READBACK_MISMATCH")
        scores = readback["positive_class_probabilities"]
        rows = expected_request["rows"]
        if (not isinstance(scores, list) or len(scores) != len(rows)
                or readback["prediction_sha256"] != digest(scores)):
            issues.append("FINAL_PREDICTION_BINDING_MISMATCH")
        else:
            mean = compute["result"]["scaler_mean"][0]
            scale = compute["result"]["scaler_scale"][0]
            coefficient = compute["result"]["coefficient"][0]
            intercept = compute["result"]["intercept"]
            for row, score in zip(rows, scores):
                linear = intercept + coefficient * ((row["feature"] - mean) / scale)
                oracle = (1 / (1 + math.exp(-linear)) if linear >= 0
                          else math.exp(linear) / (1 + math.exp(linear)))
                if type(score) is not float or not math.isclose(score, oracle, rel_tol=0, abs_tol=1e-12):
                    issues.append("FINAL_RECORDED_PREDICTION_ORACLE_MISMATCH")
                    break
        if (effect["profile"] != tracker.PROFILE
                or effect["authenticated_user"] != authenticated_user
                or effect["target_experiment"] != target
                or effect["candidate_run_id"] != expected_run_id
                or effect["authorization_sha256"] != binding["authorization_sha256"]
                or effect["request_sha256"] != binding["request_sha256"]
                or effect["compute_receipt_id"] != binding["compute_receipt_id"]
                or effect["release_manifest_sha256"] != binding["release_manifest_sha256"]):
            issues.append("FINAL_EFFECT_BINDING_MISMATCH")
        live = effect["live_verification"]
        if (not isinstance(live, dict) or live.get("valid") is not True
                or live.get("status") != "VALID" or live.get("issues") != []
                or live.get("binding") != binding
                or live.get("model_readback_phase") != "BEFORE_CLEANUP"):
            issues.append("LIVE_VERIFICATION_RECORD_MISMATCH")
        expected_observation = {
            "run_status": "FINISHED", "run_lifecycle_stage": "active",
            "experiment_lifecycle_stage": "active", "experiment_name": target,
            "signature": True, "input_example": True,
            "prediction_sha256": effect["readback"]["prediction_sha256"],
        }
        if not isinstance(live, dict) or live.get("observation") != expected_observation:
            issues.append("LIVE_OBSERVATION_BINDING_MISMATCH")
        if (effect["cleanup"] != {"run": "SOFT_DELETED", "experiment": "SOFT_DELETED"}
                or effect["residue"] != "NONE_OBSERVED"
                or effect["attempts"] != ["CREATE_EXPERIMENT", "CREATE_RUN_AND_LOG",
                                          "READBACK", "LIVE_VERIFY",
                                          "SOFT_DELETE_RUN", "SOFT_DELETE_EXPERIMENT"]):
            issues.append("CLEANUP_SEQUENCE_MISMATCH")
        exp_id, mlflow_run_id = effect["experiment_id"], effect["mlflow_run_id"]
        if not isinstance(exp_id, str) or not exp_id or not isinstance(mlflow_run_id, str) or not mlflow_run_id:
            raise ValueError("FINAL_REMOTE_IDS_INVALID")
        if effect["cleanup_observation"] != {
                "run": {"run_id": mlflow_run_id, "experiment_id": exp_id,
                        "lifecycle_stage": "deleted"},
                "experiment": {"experiment_id": exp_id, "lifecycle_stage": "deleted"}}:
            issues.append("CLEANUP_OBSERVATION_BINDING_MISMATCH")
        # MLflow Free may rename the deleted experiment to Trash and reject
        # runs/get for its children. The immutable ID + lifecycle is observable.
        experiment = client.get_experiment(exp_id)
        if (experiment.experiment_id != exp_id
                or experiment.lifecycle_stage != "deleted"):
            issues.append("EXPERIMENT_FINAL_STATE_MISMATCH")
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_FINAL_VERIFICATION")
    except Exception as exc:
        issues.append(type(exc).__name__ + ":" + str(exc))
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "scope": "FINAL_RECORD_AND_EXPERIMENT_CLEANUP_CONSISTENCY",
            "model_readback_phase": "BEFORE_CLEANUP_RECORDED_BY_RUNNER",
            "model_rechecked_after_cleanup": False,
            "historical_live_proof_authenticated": False,
            "promotion_authorized": False}
