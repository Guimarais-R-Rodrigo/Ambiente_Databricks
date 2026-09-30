from __future__ import annotations

import importlib
import io
import json
import sys
import uuid
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, loads_strict
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-explainability"
ENTRYPOINT = "skills/hub-ml-explainability/scripts/run.py::run"
PRIMITIVE_ID = "shap_explainer"
PRIMITIVE_MODULE = "hub_snippets.ml.shap_explainer"
LOCAL_FILES = {"input.schema.json", "execution_contract.json", "scripts/preflight.py",
               "scripts/run.py", "scripts/verify.py"}
DEPENDENCIES = {"hub_scripts/skill_execution/__init__.py",
                "hub_scripts/skill_execution/skill_execution.py",
                "hub_scripts/skill_execution/receipt/__init__.py",
                "hub_scripts/skill_execution/domain_context/__init__.py",
                "hub_scripts/skill_execution/domain_context/release.py",
                "hub_snippets/ml/shap_explainer/__init__.py",
                "hub_snippets/ml/shap_explainer/shap_explainer.py"}
REQUIRED_RELEASE_PATHS = {f"skills/{SKILL}/{name}" for name in LOCAL_FILES} | DEPENDENCIES


def _preflight_module():
    return load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser02_explainability_preflight")


def _canonical_primitive():
    module = importlib.import_module(PRIMITIVE_MODULE)
    expected = ASSISTANT_ROOT / "hub_snippets/ml/shap_explainer/__init__.py"
    if Path(module.__file__).resolve() != expected.resolve():
        raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
    primitive = getattr(module, "compute_shap", None)
    if not callable(primitive):
        raise RuntimeError("CANONICAL_PRIMITIVE_UNAVAILABLE")
    implementation = ASSISTANT_ROOT / "hub_snippets/ml/shap_explainer/shap_explainer.py"
    if Path(primitive.__code__.co_filename).resolve() != implementation.resolve():
        raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
    return primitive


def _float64_copy(value, label):
    import numpy as np
    source = np.asarray(value)
    if source.dtype.kind not in "iuf":
        raise ValueError(label + ":NUMERIC_ARRAY_REQUIRED")
    if not np.isfinite(source).all():
        raise ValueError(label + ":FINITE_ARRAY_REQUIRED")
    converted = np.array(source, dtype=np.float64, copy=True)
    if not np.isfinite(converted).all():
        raise ValueError(label + ":FLOAT64_OVERFLOW")
    if source.dtype.kind in "iu":
        if any(int(float(value)) != int(value) for value in source.flat):
            raise ValueError(label + ":INTEGER_FLOAT64_PRECISION_LOSS")
    elif not np.array_equal(converted.astype(source.dtype), source):
        raise ValueError(label + ":FLOAT64_PRECISION_LOSS")
    return converted


def _model_snapshot(model):
    import numpy as np
    return {"coefficients": np.asarray(model.coef_).tolist(),
            "intercept": np.asarray(model.intercept_).item(),
            "hub_model_id": getattr(model, "hub_model_id", None),
            "feature_names_in": (np.asarray(model.feature_names_in_).tolist()
                                 if hasattr(model, "feature_names_in_") else None)}


def _bound_arrays(request, model, X, background):
    import numpy as np
    from sklearn.linear_model import LinearRegression
    if type(model) is not LinearRegression:
        raise ValueError("MODEL:SKLEARN_LINEAR_REGRESSION_REQUIRED")
    if (getattr(model, "n_features_in_", None) != len(request["feature_names"])
            or np.asarray(model.coef_).shape != (len(request["feature_names"]),)
            or np.asarray(model.intercept_).ndim != 0):
        raise ValueError("MODEL:RAW_SCALAR_OUTPUT_REQUIRED")
    if (hasattr(model, "feature_names_in_")
            and np.asarray(model.feature_names_in_).tolist() != request["feature_names"]):
        raise ValueError("MODEL:FEATURE_NAMES_ORDER_MISMATCH")
    coefficients = _float64_copy(model.coef_, "MODEL:COEFFICIENTS")
    intercept = _float64_copy(model.intercept_, "MODEL:INTERCEPT").item()
    declared = request["model"]
    if getattr(model, "hub_model_id", None) != declared["model_id"]:
        raise ValueError("MODEL:IDENTITY_BINDING_MISMATCH")
    if (not np.allclose(coefficients, declared["coefficients"], atol=1e-12, rtol=1e-12)
            or not np.isclose(intercept, declared["intercept"], atol=1e-12, rtol=1e-12)):
        raise ValueError("MODEL:PARAMETER_BINDING_MISMATCH")
    source_X = np.asarray(X)
    source_background = np.asarray(background)
    if (source_X.ndim != 2 or source_background.ndim != 2
            or source_X.tolist() != request["X"]
            or source_background.tolist() != request["background"]):
        raise ValueError("INPUT:ARRAY_BINDING_MISMATCH")
    array = _float64_copy(source_X, "X")
    reference = _float64_copy(source_background, "BACKGROUND")
    return array, reference


def run(request: object, *, model, X, background, run_id: str | None = None) -> dict:
    trace = {"trace_version": "0.1", "skill": SKILL, "entrypoint": ENTRYPOINT,
             "run_id": run_id if run_id is not None else str(uuid.uuid4()),
             "status": "BLOCKED", "preflight_status": "NOT_RUN",
             "manifest": "release_manifest.json", "manifest_digest": None,
             "contract_digest": None, "runner_digest": None,
             "input_digest": None, "output_digest": None,
             "resources_resolved": [], "resources_called": [], "resources_completed": [],
             "decisions": [], "context_provenance": {}, "blocking_issues": [],
             "fallback_used": False, "writes_performed": False, "primitive_stdout": ""}
    preflight_result = None
    try:
        if not isinstance(trace["run_id"], str) or not trace["run_id"].strip():
            raise ValueError("RUN_ID_REQUIRED")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][f"skills/{SKILL}/execution_contract.json"]
        trace["runner_digest"] = release["artifacts"][f"skills/{SKILL}/scripts/run.py"]
        preflight_result = _preflight_module().preflight(request)
        trace["preflight_status"] = preflight_result["status"]
        if preflight_result["status"] != "PASS":
            trace["blocking_issues"] = list(preflight_result["issues"])
            return {"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                    "result": None, "receipt": None}
        array, reference = _bound_arrays(request, model, X, background)
        input_before = digest(request)
        originals_before = digest({"X": np.asarray(X).tolist(),
                                   "background": np.asarray(background).tolist()})
        copies_before = digest({"X": array.tolist(), "background": reference.tolist()})
        model_before = digest(_model_snapshot(model))
        trace["input_digest"] = input_before
        trace["resources_resolved"] = [PRIMITIVE_ID]
        trace["decisions"] = [{"item_id": item["item_id"], "item_type": "resource",
                               "applicable": item["applicable"], "resolved": item["resolved"]}
                              for item in preflight_result["sef"]["resources"]]
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False, "value": int(array.shape[1])},
            "model": {"source": "user_intent", "conflict": False},
            "background": {"source": "user_intent", "conflict": False}}
        primitive = _canonical_primitive()
        trace["resources_called"] = [PRIMITIVE_ID]
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            values, base = primitive(model, array, request["feature_names"], model_type="linear",
                                     task="regression", background=reference)
        trace["primitive_stdout"] = buffer.getvalue()
        trace["resources_completed"] = [PRIMITIVE_ID]
        values = np.asarray(values)
        if values.shape != array.shape or not np.isfinite(values).all() or not np.isfinite(base):
            raise RuntimeError("PRIMITIVE_OUTPUT_INVALID")
        result = {"schema_version": "SER02-EXPLAINABILITY-RESULT-1",
                  "profile": preflight_result["profile"],
                  "model_id": request["model"]["model_id"],
                  "feature_names": list(request["feature_names"]),
                  "row_ids": list(request["row_ids"]), "sample_ids": list(request["sample_ids"]),
                  "base_value": float(base), "shap_values": values.astype(float).tolist(),
                  "promotion_authorized": False, "business_readiness": "NOT_EVALUATED"}
        if (digest(request) != input_before
                or digest({"X": np.asarray(X).tolist(),
                           "background": np.asarray(background).tolist()}) != originals_before
                or digest({"X": array.tolist(), "background": reference.tolist()}) != copies_before
                or digest(_model_snapshot(model)) != model_before):
            raise RuntimeError("INPUT_CHANGED_DURING_EXECUTION")
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        if Path(build_execution_receipt.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py").resolve():
            raise RuntimeError("RECEIPT_IMPORT_ORIGIN_MISMATCH")
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

