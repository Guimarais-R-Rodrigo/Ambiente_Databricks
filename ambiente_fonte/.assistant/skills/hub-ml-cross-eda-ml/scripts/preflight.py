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
    ContextError, closed, text, digest, validate_temporal_context, loads_strict,
)

CONTEXT_SCHEMA = "SER05-CONTEXT-1"
PROFILE = "CONTEXT_ONLY_PILOT_V1"


def validate_context(context: object) -> dict:
    """Validate declared context only; source identities are not authenticated."""
    fields = {"schema_version", "profile", "synthetic", "sources", "anchor", "entity_keys",
              "anchor_grain", "cardinality", "decision_at", "pit", "temporal",
              "null_key_policy", "requested_effect"}
    try:
        data = closed(context, fields, {"not_applicable_reason"}, label="context")
        if data["schema_version"] != CONTEXT_SCHEMA or data["profile"] != PROFILE:
            raise ContextError("CONTEXT:UNSUPPORTED_PROFILE")
        if data["synthetic"] is not True:
            raise ContextError("CONTEXT:SYNTHETIC_PILOT_ONLY")
        if data["requested_effect"] != "NONE":
            raise ContextError("CONTEXT:L2_EFFECT_NOT_ALLOWED")
        if data["anchor_grain"] != "ONE_ROW_PER_ENTITY_DECISION":
            raise ContextError("CONTEXT:ANCHOR_GRAIN_UNRESOLVED")
        if data["cardinality"] not in ("1:1", "N:1"):
            raise ContextError("CONTEXT:CARDINALITY_UNSUPPORTED")
        if data["null_key_policy"] != "REJECT":
            raise ContextError("CONTEXT:NULL_KEY_POLICY_UNSUPPORTED")
        keys = data["entity_keys"]
        if not isinstance(keys, list) or not keys or any(not isinstance(k, str) or not k.strip() for k in keys):
            raise ContextError("CONTEXT:ENTITY_KEYS_REQUIRED")
        if len(keys) != len(set(keys)):
            raise ContextError("CONTEXT:DUPLICATE_KEYS")
        sources = data["sources"]
        if not isinstance(sources, list) or len(sources) != 2:
            raise ContextError("CONTEXT:TWO_SOURCE_PROFILE_ONLY")
        source_ids = set()
        for source in sources:
            source = closed(source, {"id", "snapshot_id", "content_sha256", "grain", "columns"}, label="source")
            sid = text(source["id"], "source_id")
            text(source["snapshot_id"], "snapshot_id")
            text(source["grain"], "source_grain")
            fingerprint = source["content_sha256"]
            if not isinstance(fingerprint, str) or len(fingerprint) != 64 or any(c not in "0123456789abcdef" for c in fingerprint):
                raise ContextError("SOURCE:CONTENT_ID_REQUIRED")
            columns = source["columns"]
            if not isinstance(columns, list) or any(not isinstance(c, str) or not c.strip() for c in columns):
                raise ContextError("SOURCE:COLUMNS_REQUIRED")
            if len(columns) != len(set(columns)) or not set(keys) <= set(columns):
                raise ContextError("SOURCE:KEYS_OR_COLUMNS_INVALID")
            if sid in source_ids:
                raise ContextError("SOURCE:DUPLICATE_ID")
            if sid == data["anchor"] and source["grain"] != data["anchor_grain"]:
                raise ContextError("SOURCE:ANCHOR_GRAIN_MISMATCH")
            source_ids.add(sid)
        if text(data["anchor"], "anchor") not in source_ids:
            raise ContextError("CONTEXT:ANCHOR_NOT_IN_SOURCES")
        temporal = validate_temporal_context(
            pit=data["pit"], temporal=data["temporal"], decision_at=data["decision_at"],
            not_applicable_reason=data.get("not_applicable_reason"))
        if data["pit"] == "APPLICABLE":
            spec = temporal["temporal"]
            for source in sources:
                if source["id"] != data["anchor"] and not {spec["reference_column"], spec["availability_column"]} <= set(source["columns"]):
                    raise ContextError("SOURCE:TEMPORAL_COLUMNS_REQUIRED")
        return {"status": "PASS", "issues": [], "profile": PROFILE,
                "context_status": "RESOLVED_FOR_L2", "context_sha256": digest(data),
                "temporal_context": temporal, "source_identity_status": "DECLARED_NOT_READ",
                "join_executed": False, "coverage_measured": False, "ml_readiness": "NOT_EVALUATED",
                "writes_performed": False, "promotion_authorized": False}
    except (ContextError, TypeError, ValueError, OverflowError) as exc:
        return {"status": "BLOCKED", "issues": [str(exc)], "profile": PROFILE,
                "context_status": "UNRESOLVED", "context_sha256": None,
                "temporal_context": None, "source_identity_status": "DECLARED_NOT_READ",
                "join_executed": False, "coverage_measured": False, "ml_readiness": "NOT_EVALUATED",
                "writes_performed": False, "promotion_authorized": False}


def preflight(context: object) -> dict:
    domain = validate_context(context)
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


def verify_preflight(payload: object, *, expected_context: dict) -> dict:
    try:
        expected = preflight(expected_context)
        valid = expected["status"] == "PASS" and digest(payload) == digest(expected)
    except Exception:
        valid = False
    return {"valid": valid, "status": "VALID" if valid else "INVALID",
            "issues": [] if valid else ["PREFLIGHT_BINDING_MISMATCH"],
            "join_executed": False, "ml_readiness": "NOT_EVALUATED"}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="SER05 candidate: context L2, no join")
    parser.add_argument("--context", required=True, type=Path)
    args = parser.parse_args()
    try:
        output = preflight(loads_strict(args.context.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as exc:
        output = {"status": "BLOCKED", "issues": [type(exc).__name__], "join_executed": False}
    print(json.dumps(output, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
