"""Strict context checks shared by candidate SER03/SER05 adapters.

This module validates metadata; it does not execute a join, issue a Receipt,
change enforcement policy, or decide operational authorization.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

TEMPORAL_VERSION = "SER-TEMPORAL-CONTEXT-1"


class ContextError(ValueError):
    """Machine-readable domain rejection before protected computation."""


def closed(value: Any, required: set[str], optional: set[str] | None = None, *, label: str) -> dict:
    if not isinstance(value, dict):
        raise ContextError(label + ":NOT_OBJECT")
    if any(not isinstance(key, str) for key in value):
        raise ContextError(label + ":KEY_NOT_STRING")
    absent = required - value.keys()
    extra = value.keys() - required - (optional or set())
    if absent:
        raise ContextError(label + ":MISSING:" + ",".join(sorted(absent)))
    if extra:
        raise ContextError(label + ":UNKNOWN:" + ",".join(sorted(extra)))
    return value


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ContextError(label + ":NONEMPTY_TEXT_REQUIRED")
    return value


def integer(value: Any, label: str, *, minimum: int = 0, maximum: int = 1200) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ContextError(label + ":INTEGER_OUT_OF_RANGE")
    return value


def loads_strict(content: str) -> Any:
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContextError("JSON:DUPLICATE_KEY:" + key)
            result[key] = value
        return result

    def reject_constant(value):
        raise ContextError("JSON:NONFINITE:" + value)

    return json.loads(content, object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def digest(value: Any) -> str:
    # No default=str, NaN, or Infinity: unsupported inputs must not acquire
    # an apparently valid identity through lossy stringification.
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def utc_instant(value: Any, label: str) -> datetime:
    value = text(value, label)
    try:
        instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContextError(label + ":INVALID_TIMESTAMP") from exc
    if instant.tzinfo is None or instant.utcoffset() != timezone.utc.utcoffset(instant):
        raise ContextError(label + ":UTC_AWARE_REQUIRED")
    return instant.astimezone(timezone.utc)


def month_start(value: Any, label: str) -> datetime:
    instant = utc_instant(value, label)
    if (instant.day, instant.hour, instant.minute, instant.second, instant.microsecond) != (1, 0, 0, 0, 0):
        raise ContextError(label + ":MONTH_START_REQUIRED")
    return instant


def validate_temporal_context(*, pit: Any, temporal: Any, decision_at: Any,
                              not_applicable_reason: Any = None) -> dict:
    """Resolve explicit temporal intent; never assess rows or execute PIT."""
    decision = utc_instant(decision_at, "decision_at")
    if pit == "UNKNOWN" or pit is None:
        raise ContextError("PIT:UNKNOWN_BLOCKS")
    if pit == "NOT_APPLICABLE":
        reason = text(not_applicable_reason, "not_applicable_reason")
        if temporal is not None:
            raise ContextError("PIT:NOT_APPLICABLE_WITH_TEMPORAL_CONFIG")
        return {"schema_version": TEMPORAL_VERSION, "pit": pit,
                "decision_at": decision.isoformat(), "reason": reason,
                "temporal": None, "join_executed": False}
    if pit != "APPLICABLE":
        raise ContextError("PIT:INVALID_STATE")
    if not_applicable_reason is not None:
        raise ContextError("PIT:APPLICABLE_WITH_NONAPPLICABILITY_REASON")
    fields = {"reference_column", "availability_column", "lag_kind", "lag_days",
              "boundary", "timezone", "tie_break", "bitemporal"}
    config = closed(temporal, fields, label="temporal")
    reference = text(config["reference_column"], "reference_column")
    availability = text(config["availability_column"], "availability_column")
    if reference == availability:
        raise ContextError("TEMPORAL:CLOCKS_MUST_BE_DISTINCT")
    if config["lag_kind"] != "CONSTANT":
        raise ContextError("TEMPORAL:VARIABLE_LATENCY_UNSUPPORTED")
    integer(config["lag_days"], "lag_days", maximum=36500)
    if config["timezone"] != "UTC":
        raise ContextError("TEMPORAL:UTC_PROFILE_ONLY")
    if config["boundary"] not in ("LE", "LT"):
        raise ContextError("TEMPORAL:EXPLICIT_BOUNDARY_REQUIRED")
    if config["tie_break"] != "REJECT":
        raise ContextError("TEMPORAL:TIE_POLICY_UNSUPPORTED")
    if config["bitemporal"] is not False:
        raise ContextError("TEMPORAL:BITEMPORAL_UNSUPPORTED")
    return {"schema_version": TEMPORAL_VERSION, "pit": pit,
            "decision_at": decision.isoformat(), "reason": None,
            "temporal": dict(config), "join_executed": False}


__all__ = ["TEMPORAL_VERSION", "ContextError", "closed", "text", "integer", "digest",
           "utc_instant", "month_start", "validate_temporal_context", "loads_strict"]
