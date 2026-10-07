"""Local synthetic pipeline specification gate; never deploys or issues Receipt."""
from __future__ import annotations
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))
from hub_scripts.skill_execution.domain_context import digest, loads_strict
from hub_scripts.skill_execution.domain_context.release import blob


def preflight(request: object) -> dict:
    result = {"status": "BLOCKED", "issues": [], "profile": "LOCAL_SYNTHETIC_SPEC_V1",
              "input_digest": None, "bindings": None, "sef": None,
              "spec_validated": False, "template_loaded": False,
              "permissions_verified": False, "effects_authorized": False,
              "deployment_status": "NOT_RUN", "writes_performed": False,
              "receipt": None, "completion": {"authorized": False}}
    try:
        from jsonschema import Draft202012Validator
        from hub_scripts.skill_execution import run_preflight
        schema = loads_strict((SKILL_DIR / "input.schema.json").read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema).iter_errors(request), key=lambda e: str(e.path))
        if errors:
            raise ValueError("SPEC_SCHEMA_INVALID:" + str(errors[0].validator))
        # JSON Schema integers can include 1.0; this interface requires exact JSON integers.
        if request["watermark_seconds"] is not None and type(request["watermark_seconds"]) is not int:
            raise ValueError("WATERMARK_INTEGER_REQUIRED")
        names = [request["source"], request["destination"], request["event_time"],
                 *request["primary_keys"], *request["columns"]]
        if any(name != name.strip() for name in names):
            raise ValueError("IDENTIFIER_WHITESPACE_FORBIDDEN")
        if request["source"] == request["destination"]:
            raise ValueError("SOURCE_DESTINATION_MUST_DIFFER")
        if not set(request["primary_keys"]) <= set(request["columns"]):
            raise ValueError("KEY_NOT_IN_SCHEMA")
        if request["event_time"] not in request["columns"]:
            raise ValueError("EVENT_TIME_NOT_IN_SCHEMA")
        expected = "MERGE_ON_KEYS" if request["write_mode"] == "MERGE" else "REJECT_DUPLICATES"
        if request["idempotency"] != expected:
            raise ValueError("IDEMPOTENCY_MODE_MISMATCH")
        if (request["incremental"] == "BATCH") != (request["watermark_seconds"] is None):
            raise ValueError("INCREMENTAL_WATERMARK_MISMATCH")
        engine = ASSISTANT_ROOT / "hub_scripts/skill_execution/skill_execution.py"
        if Path(run_preflight.__code__.co_filename).resolve() != engine.resolve():
            raise ValueError("PREFLIGHT_IMPORT_ORIGIN_MISMATCH")
        paths = [SKILL_DIR / "execution_contract.json", SKILL_DIR / "input.schema.json",
                 Path(__file__), SKILL_DIR / "templates/pipeline_spec.md", engine,
                 ASSISTANT_ROOT / "hub_scripts/skill_execution/__init__.py",
                 ASSISTANT_ROOT / "hub_scripts/skill_execution/domain_context/__init__.py",
                 ASSISTANT_ROOT / "hub_scripts/skill_execution/domain_context/release.py"]
        before = {str(p.relative_to(ASSISTANT_ROOT)).replace("\\", "/"): blob(p) for p in paths}
        sef = run_preflight(SKILL_DIR / "execution_contract.json",
                            assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        result["sef"] = sef
        if sef["status"] != "PASS":
            raise ValueError("SEF_PREFLIGHT_BLOCKED")
        template = (SKILL_DIR / "templates/pipeline_spec.md").read_text(encoding="utf-8")
        if not template.strip():
            raise ValueError("TEMPLATE_EMPTY")
        after = {str(p.relative_to(ASSISTANT_ROOT)).replace("\\", "/"): blob(p) for p in paths}
        if before != after:
            raise ValueError("RELEASE_CHANGED_DURING_PREFLIGHT")
        result.update(status="PASS", input_digest=digest(request), bindings=before,
                      spec_validated=True, template_loaded=True)
    except Exception as exc:
        result["issues"] = [type(exc).__name__ + ":" + str(exc)]
    return result


def verify_preflight(payload: object, *, expected_request: dict) -> dict:
    """Recheck trusted request and current source; validation does not authorize effects."""
    try:
        expected = preflight(expected_request)
        valid = expected["status"] == "PASS" and digest(payload) == digest(expected)
    except Exception:
        valid = False
    return {"valid": valid, "issues": [] if valid else ["SPEC_BINDING_MISMATCH"],
            "effects_authorized": False, "deployment_status": "NOT_RUN"}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Validate synthetic pipeline spec; no deploy")
    parser.add_argument("--request", required=True, type=Path)
    args = parser.parse_args()
    try:
        payload = preflight(loads_strict(args.request.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, ValueError) as exc:
        payload = {"status": "BLOCKED", "issues": [type(exc).__name__],
                   "effects_authorized": False, "deployment_status": "NOT_RUN"}
    print(json.dumps(payload, sort_keys=True, allow_nan=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

