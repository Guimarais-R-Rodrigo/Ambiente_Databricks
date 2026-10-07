from __future__ import annotations

import math
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, text, utc_instant
from hub_scripts.skill_execution.domain_context.release import blob, loads_strict

PROFILE = "BINARY_MATURE_PERFORMANCE_V1"
FIELDS = {"schema_version", "profile", "synthetic", "requested_effect", "model_id",
          "model_version", "population_id", "score_name", "evaluation_at",
          "reference_start", "reference_end", "current_start", "current_end",
          "auc_thresholds", "reference", "current"}
ROW_FIELDS = {"id", "observed_at", "label_available_at", "score", "label"}
RULE_FIELDS = {"warning", "critical", "direction", "delta"}


def validate_request(request: object) -> dict:
    try:
        data = closed(request, FIELDS, label="request")
        from jsonschema import Draft202012Validator
        schema = loads_strict((SKILL_DIR / "performance_input.schema.json").read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(data))
        if errors:
            raise ContextError("REQUEST:SCHEMA_INVALID:" + str(errors[0].validator))
        if data["synthetic"] is not True or data["requested_effect"] != "NONE":
            raise ContextError("REQUEST:SYNTHETIC_NO_EFFECT_ONLY")
        for key in ("model_id", "model_version", "population_id"):
            text(data[key], key)
        for key in ("schema_version", "profile", "score_name"):
            expected = {"schema_version": "SER12-REQUEST-1", "profile": PROFILE,
                        "score_name": "score"}[key]
            if data[key] != expected:
                raise ContextError("REQUEST:UNSUPPORTED:" + key)
        rule = closed(data["auc_thresholds"], RULE_FIELDS, label="auc_thresholds")
        for key in ("warning", "critical"):
            value = rule[key]
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ContextError("THRESHOLD:FINITE_NUMBER_REQUIRED")
        if not 0 <= rule["warning"] < rule["critical"] <= 1:
            raise ContextError("THRESHOLD:ORDER_INVALID")
        if rule["direction"] != "higher" or rule["delta"] != "absolute":
            raise ContextError("THRESHOLD:AUC_HIGHER_ABSOLUTE_ONLY")
        spans = {}
        for name in ("reference", "current"):
            start = utc_instant(data[name + "_start"], name + "_start")
            end = utc_instant(data[name + "_end"], name + "_end")
            if start >= end:
                raise ContextError("WINDOW:START_NOT_BEFORE_END:" + name)
            spans[name] = (start, end)
        evaluation = utc_instant(data["evaluation_at"], "evaluation_at")
        if not spans["reference"][1] < spans["current"][0] or spans["current"][1] > evaluation:
            raise ContextError("WINDOW:NOT_DISJOINT_OR_EVALUATION_EARLY")
        all_ids = set()
        windows = {}
        for name in ("reference", "current"):
            rows = data[name]
            if not isinstance(rows, list) or not 4 <= len(rows) <= 1000:
                raise ContextError("ROWS:BOUNDED_AT_LEAST_FOUR:" + name)
            labels = set()
            for item in rows:
                row = closed(item, ROW_FIELDS, label="row")
                rid = text(row["id"], "id")
                if rid in all_ids:
                    raise ContextError("ROW:DUPLICATE_ID")
                all_ids.add(rid)
                observed = utc_instant(row["observed_at"], "observed_at")
                label_at = utc_instant(row["label_available_at"], "label_available_at")
                if not spans[name][0] <= observed <= spans[name][1]:
                    raise ContextError("ROW:OUTSIDE_WINDOW")
                if not observed <= label_at <= evaluation:
                    raise ContextError("ROW:LABEL_NOT_MATURE_OR_PRECEDES_PREDICTION")
                score = row["score"]
                if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
                    raise ContextError("ROW:INVALID_SCORE")
                if type(row["label"]) is not int or row["label"] not in (0, 1):
                    raise ContextError("ROW:BINARY_LABEL_REQUIRED")
                labels.add(row["label"])
            if labels != {0, 1}:
                raise ContextError("WINDOW:BOTH_CLASSES_REQUIRED:" + name)
            windows[name] = {"ids": [r["id"] for r in rows], "count": len(rows)}
        return {"status": "PASS", "issues": [], "profile": PROFILE,
                "request_sha256": digest(data), "windows": windows,
                "helper_called": False, "writes_performed": False}
    except (ContextError, KeyError, TypeError, ValueError, OverflowError) as exc:
        return {"status": "BLOCKED", "issues": [str(exc)], "profile": PROFILE,
                "request_sha256": None, "windows": None,
                "helper_called": False, "writes_performed": False}


def preflight(request: object) -> dict:
    domain = validate_request(request)
    if domain["status"] != "PASS":
        return {**domain, "sef": None}
    try:
        from hub_scripts.skill_execution import run_preflight
        implementation = ASSISTANT_ROOT / "hub_scripts/skill_execution/skill_execution.py"
        if Path(run_preflight.__code__.co_filename).resolve() != implementation.resolve():
            raise RuntimeError("SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH")
        sef = run_preflight(SKILL_DIR / "performance_contract.json",
                            assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        if sef["status"] != "PASS":
            return {**domain, "status": "BLOCKED",
                    "issues": [x["code"] for x in sef["blocking_issues"]], "sef": sef}
        return {**domain, "sef": sef,
                "release_bindings": {
                    "contract_git_blob_sha1": blob(SKILL_DIR / "performance_contract.json"),
                    "preflight_git_blob_sha1": blob(Path(__file__))}}
    except Exception as exc:
        return {**domain, "status": "BLOCKED",
                "issues": ["SEF_ADAPTER:" + type(exc).__name__ + ":" + str(exc)], "sef": None}
