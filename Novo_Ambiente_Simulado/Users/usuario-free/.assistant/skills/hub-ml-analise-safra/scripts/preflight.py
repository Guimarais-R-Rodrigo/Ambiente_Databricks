from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import (
    ContextError, closed, text, integer, digest, month_start, loads_strict,
)

REQUEST_SCHEMA = "SER03-REQUEST-1"
PROFILE = "MONTHLY_BINARY_PILOT_V1"
EXPECTED_PARAMETERS = {
    "periodicity": "MONTH",
    "duplicate_policy": "REJECT",
    "absence_policy": "MISSING_ROW_NOT_ZERO",
    "denominator": "MOB0_UNIQUE_IDS_FIXED_PER_COHORT",
    "estimand": "BINARY_CUMULATIVE_INCIDENCE",
    "requested_effect": "NONE",
}


def validate_request(request: object) -> dict:
    """Pure domain check. No pandas import, helper call or persistent write."""
    fields = {"schema_version", "profile", "synthetic", "population_id", "cutoff",
              "max_mob", "semantic_mode", "cohort_roster", "rows", *EXPECTED_PARAMETERS}
    try:
        data = closed(request, fields, label="request")
        if data["schema_version"] != REQUEST_SCHEMA or data["profile"] != PROFILE:
            raise ContextError("REQUEST:UNSUPPORTED_PROFILE")
        if data["synthetic"] is not True:
            raise ContextError("REQUEST:SYNTHETIC_PILOT_ONLY")
        text(data["population_id"], "population_id")
        cutoff = month_start(data["cutoff"], "cutoff")
        max_mob = integer(data["max_mob"], "max_mob")
        for key, expected in EXPECTED_PARAMETERS.items():
            if data[key] != expected:
                raise ContextError("PROFILE:UNSUPPORTED:" + key)
        if data["semantic_mode"] not in ("CUMULATIVE", "EVENT"):
            raise ContextError("TARGET:SEMANTICS_REQUIRED")
        roster = data["cohort_roster"]
        if not isinstance(roster, list) or not roster:
            raise ContextError("ROSTER:NONEMPTY_LIST_REQUIRED")
        origins = {}
        cohort_sizes = {}
        for row in roster:
            row = closed(row, {"id", "originated_at"}, label="roster_row")
            uid = text(row["id"], "roster_id")
            origin = month_start(row["originated_at"], "originated_at")
            if uid in origins:
                raise ContextError("ROSTER:DUPLICATE_ID")
            if origin > cutoff:
                raise ContextError("ROSTER:ORIGIN_AFTER_CUTOFF")
            origins[uid] = origin
            cohort = origin.strftime("%Y-%m")
            cohort_sizes[cohort] = cohort_sizes.get(cohort, 0) + 1
        if not isinstance(data["rows"], list) or not data["rows"]:
            raise ContextError("ROWS:NONEMPTY_LIST_REQUIRED")
        by_unit = {uid: {} for uid in origins}
        cells = {}
        for row in data["rows"]:
            row = closed(row, {"id", "originated_at", "observed_at", "mob", "target"}, label="row")
            uid = text(row["id"], "id")
            if uid not in origins:
                raise ContextError("ROW:ID_OUTSIDE_ROSTER")
            origin = month_start(row["originated_at"], "originated_at")
            observed = month_start(row["observed_at"], "observed_at")
            mob = integer(row["mob"], "mob", maximum=max_mob)
            if origin != origins[uid]:
                raise ContextError("ROW:ORIGIN_ROSTER_MISMATCH")
            if observed < origin or observed > cutoff:
                raise ContextError("ROW:OBSERVATION_OUTSIDE_WINDOW")
            calendar_mob = (observed.year - origin.year) * 12 + observed.month - origin.month
            if calendar_mob != mob:
                raise ContextError("ROW:MOB_CALENDAR_MISMATCH")
            if type(row["target"]) is not int or row["target"] not in (0, 1):
                raise ContextError("TARGET:BINARY_INTEGER_REQUIRED")
            if mob in by_unit[uid]:
                raise ContextError("ROW:DUPLICATE_ID_MOB")
            by_unit[uid][mob] = row["target"]
            key = (origin.strftime("%Y-%m"), mob)
            cells[key] = cells.get(key, 0) + 1
        for values in by_unit.values():
            if 0 not in values:
                raise ContextError("ROSTER:MOB0_INCOMPLETE")
            sequence = [values[k] for k in sorted(values)]
            if data["semantic_mode"] == "CUMULATIVE" and any(b < a for a, b in zip(sequence, sequence[1:])):
                raise ContextError("TARGET:CUMULATIVE_DECREASE")
            if data["semantic_mode"] == "EVENT" and sorted(values) != list(range(max(values) + 1)):
                raise ContextError("TARGET:EVENT_GAP_WITH_REENTRY")
        grid = []
        for cohort, size in sorted(cohort_sizes.items()):
            year, month = map(int, cohort.split("-"))
            age = (cutoff.year-year)*12 + cutoff.month-month
            for mob in range(max_mob + 1):
                count = cells.get((cohort, mob), 0)
                state = ("IMMATURE" if mob > age else "NO_OBSERVATIONS" if not count
                         else "COMPLETE" if count == size else "INCOMPLETE")
                grid.append({"safra": cohort, "mob": mob, "n_contratos_safra": size,
                             "n_contratos_observados": count, "maturity": "IMMATURE" if mob > age else "MATURE",
                             "coverage_status": state})
        return {"status": "PASS", "issues": [], "profile": PROFILE,
                "request_sha256": digest(data), "roster_sha256": digest(roster),
                "coverage_grid": grid, "helper_called": False, "writes_performed": False}
    except (ContextError, TypeError, ValueError, OverflowError) as exc:
        return {"status": "BLOCKED", "issues": [str(exc)], "profile": PROFILE,
                "request_sha256": None, "roster_sha256": None, "coverage_grid": [],
                "helper_called": False, "writes_performed": False}


def preflight(request: object) -> dict:
    domain = validate_request(request)
    if domain["status"] != "PASS":
        return {**domain, "sef": None}
    try:
        from hub_scripts.skill_execution import run_preflight
        from hub_scripts.skill_execution.domain_context.release import blob
        implementation = ASSISTANT_ROOT / "hub_scripts/skill_execution/skill_execution.py"
        if Path(run_preflight.__code__.co_filename).resolve() != implementation.resolve():
            raise RuntimeError("SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH")
        sef = run_preflight(SKILL_DIR / "execution_contract.json",
                            assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        bindings = {
            "contract_git_blob_sha1": blob(SKILL_DIR / "execution_contract.json"),
            "preflight_git_blob_sha1": blob(Path(__file__)),
            "temporal_owner_git_blob_sha1": blob(ASSISTANT_ROOT / "hub_scripts/skill_execution/domain_context/__init__.py"),
        }
        if sef["status"] != "PASS":
            return {**domain, "status": "BLOCKED", "issues": [x["code"] for x in sef["blocking_issues"]], "sef": sef,
                    "release_bindings": bindings}
        return {**domain, "sef": sef, "release_bindings": bindings}
    except Exception as exc:
        return {**domain, "status": "BLOCKED", "issues": ["SEF_ADAPTER:" + type(exc).__name__ + ":" + str(exc)], "sef": None}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="SER03 candidate: monthly binary preflight only")
    parser.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()
    try:
        output = preflight(loads_strict(args.request.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as exc:
        output = {"status": "BLOCKED", "issues": [type(exc).__name__], "helper_called": False}
    print(json.dumps(output, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
