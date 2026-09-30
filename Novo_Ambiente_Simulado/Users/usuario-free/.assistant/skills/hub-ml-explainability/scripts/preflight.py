from __future__ import annotations

import json
import math
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, loads_strict, text
from hub_scripts.skill_execution.domain_context.release import blob

PROFILE = "LINEAR_REGRESSION_SYNTHETIC_V1"
REQUEST_SCHEMA = "SER02-EXPLAINABILITY-REQUEST-1"
FIELDS = {"schema_version", "profile", "synthetic", "requested_effect", "model",
          "feature_names", "row_ids", "sample_ids", "X", "background"}
MAX_ROWS = 10000
MAX_FEATURES = 100


def _number(value, label):
    if type(value) not in (int, float):
        raise ContextError(label + ":FINITE_EXACT_FLOAT64_REQUIRED")
    try:
        converted = float(value)
    except (OverflowError, ValueError) as exc:
        raise ContextError(label + ":FINITE_EXACT_FLOAT64_REQUIRED") from exc
    if not math.isfinite(converted) or (type(value) is int and int(converted) != value):
        raise ContextError(label + ":FINITE_EXACT_FLOAT64_REQUIRED")
    return converted


def _matrix(value, label, width):
    if not isinstance(value, list) or not 1 <= len(value) <= MAX_ROWS:
        raise ContextError(label + ":NONEMPTY_BOUNDED_MATRIX_REQUIRED")
    for row in value:
        if not isinstance(row, list) or len(row) != width:
            raise ContextError(label + ":WIDTH_MISMATCH")
        for number in row:
            _number(number, label)
    return value


def validate_request(request: object) -> dict:
    try:
        data = closed(request, FIELDS, label="request")
        if data["schema_version"] != REQUEST_SCHEMA or data["profile"] != PROFILE:
            raise ContextError("REQUEST:UNSUPPORTED_PROFILE")
        if data["synthetic"] is not True or data["requested_effect"] != "NONE":
            raise ContextError("REQUEST:SYNTHETIC_READ_ONLY_REQUIRED")
        model = closed(data["model"], {"model_id", "model_type", "task", "estimator", "intercept", "coefficients"}, label="model")
        text(model["model_id"], "model_id")
        if (model["model_type"], model["task"], model["estimator"]) != ("linear", "regression", "sklearn.LinearRegression"):
            raise ContextError("MODEL:UNSUPPORTED_PROFILE")
        names = data["feature_names"]
        if not isinstance(names, list) or not 1 <= len(names) <= MAX_FEATURES or any(not isinstance(x, str) or not x.strip() or x != x.strip() for x in names) or len(set(names)) != len(names):
            raise ContextError("FEATURES:ORDERED_UNIQUE_NAMES_REQUIRED")
        width = len(names)
        _number(model["intercept"], "MODEL:INTERCEPT")
        coef = model["coefficients"]
        if not isinstance(coef, list) or len(coef) != width:
            raise ContextError("MODEL:COEFFICIENT_WIDTH_MISMATCH")
        for number in coef:
            _number(number, "MODEL:COEFFICIENT")
        X = _matrix(data["X"], "X", width)
        background = _matrix(data["background"], "BACKGROUND", width)
        if len(background) != 1:
            raise ContextError("BACKGROUND:SINGLE_ROW_REQUIRED")
        ids = data["row_ids"]
        samples = data["sample_ids"]
        if not isinstance(ids, list) or len(ids) != len(X) or any(not isinstance(x, str) or not x.strip() or x != x.strip() for x in ids) or len(set(ids)) != len(ids):
            raise ContextError("ROWS:UNIQUE_IDS_REQUIRED")
        if not isinstance(samples, list) or not samples or len(set(samples)) != len(samples) or any(type(x) is not str or x not in ids for x in samples):
            raise ContextError("SAMPLES:EXPLICIT_ROW_IDS_REQUIRED")
        digest(data)
        return {"status": "PASS", "issues": [], "profile": PROFILE, "request_sha256": digest(data),
                "helper_called": False, "writes_performed": False}
    except (ContextError, TypeError, ValueError, OverflowError) as exc:
        return {"status": "BLOCKED", "issues": [str(exc)], "profile": PROFILE,
                "request_sha256": None, "helper_called": False, "writes_performed": False}


def preflight(request: object) -> dict:
    domain = validate_request(request)
    if domain["status"] != "PASS":
        return {**domain, "sef": None}
    try:
        from hub_scripts.skill_execution import run_preflight
        expected = ASSISTANT_ROOT / "hub_scripts/skill_execution/skill_execution.py"
        if Path(run_preflight.__code__.co_filename).resolve() != expected.resolve():
            raise RuntimeError("SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH")
        sef = run_preflight(SKILL_DIR / "execution_contract.json", assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        bindings = {"contract_git_blob_sha1": blob(SKILL_DIR / "execution_contract.json"),
                    "preflight_git_blob_sha1": blob(Path(__file__)),
                    "temporal_owner_git_blob_sha1": blob(ASSISTANT_ROOT / "hub_scripts/skill_execution/domain_context/__init__.py")}
        if sef["status"] != "PASS":
            return {**domain, "status": "BLOCKED", "issues": [x["code"] for x in sef["blocking_issues"]], "sef": sef, "release_bindings": bindings}
        return {**domain, "sef": sef, "release_bindings": bindings}
    except Exception as exc:
        return {**domain, "status": "BLOCKED", "issues": ["SEF_ADAPTER:" + type(exc).__name__ + ":" + str(exc)], "sef": None}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = preflight(loads_strict(args.request.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as exc:
        result = {"status": "BLOCKED", "issues": [type(exc).__name__], "helper_called": False}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
