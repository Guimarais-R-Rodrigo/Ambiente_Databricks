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


def verify(payload: object, *, expected_request: dict, expected_run_id: str) -> dict:
    issues = []
    try:
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser09_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        domain = load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser09_verifier_preflight").preflight(expected_request)
        if domain["status"] != "PASS":
            raise ValueError("EXPECTED_REQUEST_INVALID")
        if not isinstance(payload, dict) or set(payload) != {"status", "preflight", "trace", "result", "receipt"} or payload["status"] != "PASS":
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(domain):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        trace, result = payload["trace"], payload["result"]
        if trace.get("input_digest") != digest(expected_request):
            issues.append("INPUT_BINDING_MISMATCH")
        if (trace.get("resources_resolved") != ["temporal_split", "metrics_report"]
                or trace.get("resources_called") != ["temporal_split", "metrics_report", "metrics_report", "metrics_report"]
                or trace.get("resources_completed") != ["temporal_split", "metrics_report", "metrics_report", "metrics_report"]):
            issues.append("RESOURCE_CALL_BINDING_MISMATCH")
        if not isinstance(result, dict) or set(result) != {
                "schema_version", "profile", "population_id", "unit", "feature_order", "target",
                "positive_class", "threshold", "seed", "partitions", "fit_partition_sha256",
                "scaler_mean", "scaler_scale", "coefficient", "intercept", "promotion_authorized", "tracking"}:
            raise ValueError("RESULT_SCHEMA_MISMATCH")
        expected_meta = {"schema_version": "SER09-RESULT-1", "profile": expected_request["profile"],
                         "population_id": expected_request["population_id"], "unit": expected_request["unit"],
                         "feature_order": expected_request["feature_order"], "target": "target",
                         "positive_class": 1, "threshold": 0.5, "seed": 17,
                         "promotion_authorized": False, "tracking": "IN_MEMORY_ONLY"}
        if any(result.get(key) != value for key, value in expected_meta.items()):
            issues.append("RESULT_CONTEXT_BINDING_MISMATCH")
        ordered = sorted(expected_request["rows"], key=lambda r: r["observed_at"])
        n_train, n_val = int(len(ordered)*0.5), int(len(ordered)*0.25)
        parts = {"train": ordered[:n_train], "validation": ordered[n_train:n_train+n_val],
                 "holdout": ordered[n_train+n_val:]}
        if not isinstance(result["partitions"], dict):
            raise ValueError("PARTITIONS_NOT_OBJECT")
        if set(result["partitions"]) != set(parts):
            issues.append("PARTITION_SET_MISMATCH")
        if result["fit_partition_sha256"] != digest([r["id"] for r in parts["train"]]):
            issues.append("FIT_PARTITION_MISMATCH")
        values = [r["feature"] for r in parts["train"]]
        mean = sum(values)/len(values)
        scale = math.sqrt(sum((x-mean)**2 for x in values)/len(values)) or 1.0
        if len(result["scaler_mean"]) != 1 or len(result["scaler_scale"]) != 1 or not math.isclose(result["scaler_mean"][0], mean, abs_tol=1e-12) or not math.isclose(result["scaler_scale"][0], scale, abs_tol=1e-12):
            issues.append("TRAIN_ONLY_SCALER_MISMATCH")
        if len(result["coefficient"]) != 1 or not all(math.isfinite(x) for x in [result["coefficient"][0], result["intercept"]]):
            issues.append("MODEL_PARAMETERS_INVALID")
        else:
            # Refit from the independently held train rows; result parameters are
            # evidence only when they match a train-only fit.
            from sklearn.linear_model import LogisticRegression
            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import StandardScaler
            runner._disable_autolog_before_fit()
            oracle_model = Pipeline([("scale", StandardScaler()),
                                     ("classifier", LogisticRegression(random_state=17, max_iter=1000))])
            oracle_model.fit([[r["feature"]] for r in parts["train"]], [r["target"] for r in parts["train"]])
            if (not math.isclose(result["coefficient"][0], float(oracle_model.named_steps["classifier"].coef_[0][0]), abs_tol=1e-12)
                    or not math.isclose(result["intercept"], float(oracle_model.named_steps["classifier"].intercept_[0]), abs_tol=1e-12)):
                issues.append("TRAIN_ONLY_FIT_ORACLE_MISMATCH")
        for name, rows in parts.items():
            observed = result["partitions"].get(name)
            if not isinstance(observed, dict) or set(observed) != {"ids", "targets", "scores", "metrics"}:
                issues.append("PARTITION_SCHEMA_MISMATCH:" + name)
                continue
            if observed["ids"] != [r["id"] for r in rows] or observed["targets"] != [r["target"] for r in rows]:
                issues.append("PARTITION_ID_TARGET_MISMATCH:" + name)
            if len(observed["scores"]) != len(rows):
                issues.append("SCORE_LENGTH_MISMATCH:" + name)
                continue
            for row, score in zip(rows, observed["scores"]):
                linear = result["intercept"] + result["coefficient"][0]*(row["feature"]-mean)/scale
                oracle = (1/(1+math.exp(-linear)) if linear >= 0
                          else math.exp(linear)/(1+math.exp(linear)))
                if type(score) is not float or not math.isclose(score, oracle, abs_tol=1e-12):
                    issues.append("SCORE_MODEL_BINDING_MISMATCH:" + name)
                    break
            from sklearn.metrics import roc_auc_score, brier_score_loss
            ys = [r["target"] for r in rows]
            metrics = observed["metrics"]
            if not isinstance(metrics, dict) or set(metrics) != {"auc_roc", "brier_score"} or not math.isclose(metrics.get("auc_roc", -1), round(roc_auc_score(ys, observed["scores"]), 4), abs_tol=1e-12) or not math.isclose(metrics.get("brier_score", -1), round(brier_score_loss(ys, observed["scores"]), 4), abs_tol=1e-12):
                issues.append("METRICS_ORACLE_MISMATCH:" + name)
        from hub_scripts.skill_execution.receipt import verify_execution_receipt
        if Path(verify_execution_receipt.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py").resolve():
            raise RuntimeError("RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH")
        check = verify_execution_receipt(payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
                                         protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
                                         expected_release={"manifest_name": "release_manifest.json",
                                                           "manifest_sha256": release["manifest_sha256"],
                                                           "contract_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/execution_contract.json"],
                                                           "runner_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/scripts/run.py"]}).to_dict()
        if not check["valid"]:
            issues.extend(check["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID", "issues": issues,
            "promotion_authorized": False, "completion_authorized": False}
