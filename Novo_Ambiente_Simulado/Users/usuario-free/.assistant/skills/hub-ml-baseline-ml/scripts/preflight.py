from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, integer, text, utc_instant
from hub_scripts.skill_execution.domain_context.release import blob

PROFILE = "BINARY_TEMPORAL_LOCAL_V1"
FIELDS = {"schema_version", "profile", "synthetic", "requested_effect", "population_id",
          "target", "positive_class", "unit", "date_column", "feature_order", "train_pct",
          "val_pct", "gap_periods", "period_unit", "threshold", "seed", "rows"}
ROW_FIELDS = {"id", "observed_at", "feature", "target"}


def validate_request(request: object) -> dict:
    try:
        data = closed(request, FIELDS, label="request")
        if data["schema_version"] != "SER09-REQUEST-1" or data["profile"] != PROFILE:
            raise ContextError("REQUEST:UNSUPPORTED_PROFILE")
        if data["synthetic"] is not True or data["requested_effect"] != "NONE":
            raise ContextError("REQUEST:SYNTHETIC_NO_EFFECT_ONLY")
        for key in ("population_id", "unit"):
            text(data[key], key)
        for key, expected in {"target": "target", "positive_class": 1, "date_column": "observed_at",
                              "feature_order": ["feature"], "train_pct": 0.5, "val_pct": 0.25,
                              "gap_periods": 0, "period_unit": "M", "threshold": 0.5, "seed": 17}.items():
            if type(data[key]) is not type(expected) or data[key] != expected:
                raise ContextError("PROFILE:UNSUPPORTED:" + key)
        rows = data["rows"]
        if not isinstance(rows, list) or len(rows) < 12:
            raise ContextError("ROWS:AT_LEAST_12_REQUIRED")
        ids, months = set(), set()
        for row in rows:
            row = closed(row, ROW_FIELDS, label="row")
            uid = text(row["id"], "id")
            if uid in ids:
                raise ContextError("ROW:DUPLICATE_ID")
            ids.add(uid)
            instant = utc_instant(row["observed_at"], "observed_at")
            if instant.day != 1 or any((instant.hour, instant.minute, instant.second, instant.microsecond)):
                raise ContextError("ROW:MONTH_START_REQUIRED")
            month = instant.strftime("%Y-%m")
            if month in months:
                raise ContextError("ROW:DUPLICATE_MONTH")
            months.add(month)
            value = row["feature"]
            if type(value) not in (int, float) or not -1e9 <= value <= 1e9:
                raise ContextError("ROW:FINITE_FEATURE_REQUIRED")
            if type(row["target"]) is not int or row["target"] not in (0, 1):
                raise ContextError("ROW:BINARY_TARGET_REQUIRED")
        ordered = sorted(rows, key=lambda r: r["observed_at"])
        n_train, n_val = int(len(rows) * 0.5), int(len(rows) * 0.25)
        for label, part in (("train", ordered[:n_train]), ("validation", ordered[n_train:n_train+n_val]),
                            ("holdout", ordered[n_train+n_val:])):
            if len({row["target"] for row in part}) != 2:
                raise ContextError("PARTITION:BOTH_CLASSES_REQUIRED:" + label)
        return {"status": "PASS", "issues": [], "profile": PROFILE, "request_sha256": digest(data),
                "partitions_expected": {"train": [r["id"] for r in ordered[:n_train]],
                                        "validation": [r["id"] for r in ordered[n_train:n_train+n_val]],
                                        "holdout": [r["id"] for r in ordered[n_train+n_val:]]},
                "helper_called": False, "writes_performed": False}
    except (ContextError, KeyError, TypeError, ValueError, OverflowError) as exc:
        return {"status": "BLOCKED", "issues": [str(exc)], "profile": PROFILE,
                "request_sha256": None, "partitions_expected": None,
                "helper_called": False, "writes_performed": False}


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
