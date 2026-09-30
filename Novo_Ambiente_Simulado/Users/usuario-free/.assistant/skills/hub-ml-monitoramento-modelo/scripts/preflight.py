from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, integer, text, utc_instant
from hub_scripts.skill_execution.domain_context.release import blob

PROFILE = "DRIFT_NUMERIC_LOCAL_V1"
FIELDS = {"schema_version", "profile", "synthetic", "requested_effect", "model_id",
          "model_version", "population_id", "score_name", "reference_start", "reference_end",
          "current_start", "current_end", "n_bins", "eps", "reference", "current"}
ROW_FIELDS = {"id", "observed_at", "score"}


def validate_request(request: object) -> dict:
    try:
        data = closed(request, FIELDS, label="request")
        if data["schema_version"] != "SER11-REQUEST-1" or data["profile"] != PROFILE:
            raise ContextError("REQUEST:UNSUPPORTED_PROFILE")
        if data["synthetic"] is not True or data["requested_effect"] != "NONE":
            raise ContextError("REQUEST:SYNTHETIC_NO_EFFECT_ONLY")
        for key in ("model_id", "model_version", "population_id"):
            text(data[key], key)
        if data["score_name"] != "score" or type(data["n_bins"]) is not int or data["n_bins"] != 4:
            raise ContextError("PROFILE:SCORE_OR_BINS_UNSUPPORTED")
        if type(data["eps"]) is not float or data["eps"] != 1e-6:
            raise ContextError("PROFILE:SMOOTHING_UNSUPPORTED")
        starts = [utc_instant(data[key], key) for key in
                  ("reference_start", "reference_end", "current_start", "current_end")]
        if not starts[0] <= starts[1] < starts[2] <= starts[3]:
            raise ContextError("WINDOW:NOT_ORDERED_DISJOINT")
        ids = set()
        for partition, lower, upper in (("reference", starts[0], starts[1]),
                                        ("current", starts[2], starts[3])):
            rows = data[partition]
            if not isinstance(rows, list) or len(rows) < 4:
                raise ContextError("WINDOW:AT_LEAST_FOUR_REQUIRED:" + partition)
            finite = 0
            for row in rows:
                row = closed(row, ROW_FIELDS, label="row")
                uid = text(row["id"], "id")
                if uid in ids:
                    raise ContextError("ROW:DUPLICATE_ID")
                ids.add(uid)
                when = utc_instant(row["observed_at"], "observed_at")
                if not lower <= when <= upper:
                    raise ContextError("ROW:OUTSIDE_WINDOW")
                score = row["score"]
                if score is not None:
                    if type(score) not in (int, float) or not 0 <= score <= 1:
                        raise ContextError("ROW:SCORE_OUT_OF_RANGE")
                    finite += 1
            if finite < 2:
                raise ContextError("WINDOW:TOO_FEW_FINITE_SCORES")
        return {"status": "PASS", "issues": [], "profile": PROFILE,
                "request_sha256": digest(data), "helper_called": False, "writes_performed": False}
    except (ContextError, KeyError, TypeError, ValueError, OverflowError) as exc:
        return {"status": "BLOCKED", "issues": [str(exc)], "profile": PROFILE,
                "request_sha256": None, "helper_called": False, "writes_performed": False}


def preflight(request: object) -> dict:
    domain = validate_request(request)
    if domain["status"] != "PASS":
        return {**domain, "sef": None}
    try:
        from hub_scripts.skill_execution import run_preflight
        if Path(run_preflight.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_scripts/skill_execution/skill_execution.py").resolve():
            raise RuntimeError("SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH")
        sef = run_preflight(SKILL_DIR / "execution_contract.json", assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        bindings = {"contract_git_blob_sha1": blob(SKILL_DIR / "execution_contract.json"),
                    "preflight_git_blob_sha1": blob(Path(__file__))}
        if sef["status"] != "PASS":
            return {**domain, "status": "BLOCKED", "issues": [i["code"] for i in sef["blocking_issues"]],
                    "sef": sef, "release_bindings": bindings}
        return {**domain, "sef": sef, "release_bindings": bindings}
    except Exception as exc:
        return {**domain, "status": "BLOCKED", "issues": [f"SEF_ADAPTER:{type(exc).__name__}:{exc}"], "sef": None}
