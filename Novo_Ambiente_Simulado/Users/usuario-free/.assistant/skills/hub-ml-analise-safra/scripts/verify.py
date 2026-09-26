from __future__ import annotations

import importlib
import io
import json
import sys
import uuid
from contextlib import redirect_stdout
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

import math
from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity


def _equal_table(actual: object, expected: object) -> bool:
    if not isinstance(actual, list) or not isinstance(expected, list) or len(actual) != len(expected):
        return False
    for row, oracle in zip(actual, expected):
        if not isinstance(row, dict) or not isinstance(oracle, dict) or set(row) != set(oracle):
            return False
        for key, reference in oracle.items():
            value = row[key]
            if reference is None:
                if value is not None:
                    return False
            elif key in ("taxa_acumulada", "taxa", "cobertura_observada"):
                if (type(value) not in (int, float) or type(reference) not in (int, float)
                        or not math.isfinite(value) or not math.isfinite(reference)
                        or not math.isclose(value, reference, abs_tol=1e-12, rel_tol=1e-12)):
                    return False
            elif type(value) is not type(reference) or value != reference:
                return False
    return True


def verify(payload: object, *, expected_request: dict, expected_run_id: str,
           expected_table: list[dict]) -> dict:
    """Recheck Receipt V1, current release, trusted request/run and fixture oracle.

    The caller supplies the independently held request/run/oracle, not values
    extracted from the candidate payload. Checksums do not authenticate authors.
    """
    issues = []
    try:
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser03_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        domain = runner._preflight_module().preflight(expected_request)
        if domain["status"] != "PASS":
            raise ValueError("EXPECTED_REQUEST_INVALID")
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        if (not isinstance(payload, dict) or set(payload) != {"status", "preflight", "trace", "result", "receipt"}
                or payload["status"] != "PASS"):
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(domain):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        trace = payload["trace"]
        if not isinstance(trace, dict) or trace.get("input_digest") != digest(expected_request):
            issues.append("INPUT_BINDING_MISMATCH")
        result = payload["result"]
        if not isinstance(result, dict):
            raise ValueError("RESULT_NOT_OBJECT")
        expected_metadata = {"schema_version": "SER03-RESULT-1", "profile": domain["profile"],
                             "population_id": expected_request["population_id"], "cutoff": expected_request["cutoff"],
                             "semantic_mode": expected_request["semantic_mode"], "estimand": expected_request["estimand"],
                             "coverage_grid": domain["coverage_grid"], "promotion_authorized": False,
                             "business_readiness": "NOT_EVALUATED"}
        if set(result) != set(expected_metadata) | {"table"} or digest({k: v for k, v in result.items() if k != "table"}) != digest(expected_metadata):
            issues.append("RESULT_CONTEXT_BINDING_MISMATCH")
        if not _equal_table(result.get("table"), expected_table):
            issues.append("TRUSTED_ORACLE_TABLE_MISMATCH")
        from hub_scripts.skill_execution.receipt import verify_execution_receipt
        if Path(verify_execution_receipt.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py").resolve():
            raise RuntimeError("RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH")
        receipt_verification = verify_execution_receipt(
            payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
            protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
            expected_release={"manifest_name": "release_manifest.json", "manifest_sha256": release["manifest_sha256"],
                              "contract_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/execution_contract.json"],
                              "runner_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/scripts/run.py"]},
            release_integrity_ok=True).to_dict()
        if receipt_verification["valid"] is not True:
            issues.extend(receipt_verification["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID", "issues": issues,
            "scope": "CURRENT_RELEASE_REQUEST_RECEIPT_AND_TRUSTED_FIXTURE_ORACLE",
            "promotion_authorized": False, "completion_authorized": False}
