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

PROFILE = "TWO_SAMPLE_KS_PILOT_V1"
FIELDS = {"schema_version", "profile", "synthetic", "population_id", "unit", "question",
          "hypothesis", "estimand", "independence", "multiple_testing", "alpha",
          "reference", "comparison", "requested_effect"}
FIXED = {"schema_version": "SER04-REQUEST-1", "profile": PROFILE, "synthetic": True,
         "hypothesis": "TWO_SIDED_DISTRIBUTION_DIFFERENCE",
         "estimand": "MAX_ABSOLUTE_ECDF_DIFFERENCE",
         "independence": "TWO_INDEPENDENT_IID_CONTINUOUS_SAMPLES_NO_TIES",
         "multiple_testing": "ONE_PREREGISTERED_COMPARISON_NOT_APPLICABLE",
         "requested_effect": "NONE"}


def validate_request(request: object) -> dict:
    """Only a bounded, preregistered synthetic KS comparison is supported."""
    try:
        data = closed(request, FIELDS, label="request")
        for key, expected in FIXED.items():
            if type(data[key]) is not type(expected) or data[key] != expected:
                raise ContextError("PROFILE:UNSUPPORTED:" + key)
        for key in ("population_id", "unit", "question"):
            text(data[key], key)
        alpha = data["alpha"]
        if type(alpha) not in (int, float) or not math.isfinite(alpha) or not 0 < alpha < 1:
            raise ContextError("ALPHA:INVALID")
        for key in ("reference", "comparison"):
            values = data[key]
            if not isinstance(values, list) or not 4 <= len(values) <= 10000:
                raise ContextError(key.upper() + ":BOUNDED_SAMPLE_REQUIRED")
            if any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
                raise ContextError(key.upper() + ":FINITE_NUMBERS_REQUIRED")
            converted = [float(value) for value in values]
            if any(type(value) is int and converted[index] != value
                   for index, value in enumerate(values)):
                raise ContextError(key.upper() + ":FLOAT64_PRECISION_LOSS")
            if len(set(converted)) != len(converted):
                raise ContextError(key.upper() + ":FLOAT64_TIES_UNSUPPORTED")
        if set(map(float, data["reference"])) & set(map(float, data["comparison"])):
            raise ContextError("POOLED_FLOAT64_TIES_UNSUPPORTED")
        digest(data)
        return {"status": "PASS", "issues": [], "profile": PROFILE,
                "request_sha256": digest(data), "reference_n": len(data["reference"]),
                "comparison_n": len(data["comparison"]), "helper_called": False,
                "writes_performed": False}
    except (ContextError, TypeError, ValueError, OverflowError) as exc:
        return {"status": "BLOCKED", "issues": [str(exc)], "profile": PROFILE,
                "request_sha256": None, "helper_called": False, "writes_performed": False}


def preflight(request: object) -> dict:
    domain = validate_request(request)
    if domain["status"] != "PASS":
        return {**domain, "sef": None}
    try:
        from hub_scripts.skill_execution import run_preflight
        if Path(run_preflight.__code__.co_filename).resolve() != (
            ASSISTANT_ROOT / "hub_scripts/skill_execution/skill_execution.py").resolve():
            raise RuntimeError("SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH")
        sef = run_preflight(SKILL_DIR / "execution_contract.json",
                            assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        bindings = {"contract_git_blob_sha1": blob(SKILL_DIR / "execution_contract.json"),
                    "preflight_git_blob_sha1": blob(Path(__file__)),
                    "context_git_blob_sha1": blob(
                        ASSISTANT_ROOT / "hub_scripts/skill_execution/domain_context/__init__.py")}
        if sef["status"] != "PASS":
            return {**domain, "status": "BLOCKED",
                    "issues": [x["code"] for x in sef["blocking_issues"]],
                    "sef": sef, "release_bindings": bindings}
        return {**domain, "sef": sef, "release_bindings": bindings}
    except Exception as exc:
        return {**domain, "status": "BLOCKED",
                "issues": ["SEF_ADAPTER:" + type(exc).__name__ + ":" + str(exc)], "sef": None}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()
    try:
        payload = preflight(loads_strict(args.request.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as exc:
        payload = {"status": "BLOCKED", "issues": [type(exc).__name__], "helper_called": False}
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
