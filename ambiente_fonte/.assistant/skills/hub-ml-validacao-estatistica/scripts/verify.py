from __future__ import annotations

import json
import math
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, loads_strict
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity


def verify(payload: object, *, expected_request: dict, expected_run_id: str,
           expected_statistic: float, expected_p_value: float) -> dict:
    """Receipt/release/request binding plus independent fixed statistical oracle."""
    issues = []
    try:
        runner = load_sibling(SKILL_DIR / "scripts/run.py", "_ser04_verifier_runner")
        release = release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS)
        domain = runner._preflight_module().preflight(expected_request)
        if domain["status"] != "PASS":
            raise ValueError("EXPECTED_REQUEST_INVALID")
        if not isinstance(expected_run_id, str) or not expected_run_id.strip():
            raise ValueError("EXPECTED_RUN_ID_REQUIRED")
        if (not isinstance(payload, dict) or
                set(payload) != {"status", "preflight", "trace", "result", "receipt"} or
                payload["status"] != "PASS"):
            raise ValueError("PAYLOAD_NOT_CANONICAL_PASS")
        if digest(payload["preflight"]) != digest(domain):
            issues.append("PREFLIGHT_BINDING_MISMATCH")
        trace = payload["trace"]
        if not isinstance(trace, dict) or trace.get("input_digest") != digest(expected_request):
            issues.append("INPUT_BINDING_MISMATCH")
        result = payload["result"]
        if not isinstance(result, dict):
            raise ValueError("RESULT_NOT_OBJECT")
        metadata = {
            "schema_version": "SER04-RESULT-1", "profile": domain["profile"],
            "population_id": expected_request["population_id"], "unit": expected_request["unit"],
            "question": expected_request["question"], "hypothesis": expected_request["hypothesis"],
            "estimand": expected_request["estimand"], "independence": expected_request["independence"],
            "multiple_testing": expected_request["multiple_testing"], "alpha": expected_request["alpha"],
            "reference_n": len(expected_request["reference"]),
            "comparison_n": len(expected_request["comparison"]),
            "p_value_method": "SCIPY_KS_2SAMP_AUTO",
            "confidence_interval": None, "confidence_interval_status": "UNSUPPORTED_IN_PROFILE",
            "decision_scope": "DIAGNOSTIC_ONLY_INDEPENDENCE_DECLARED",
            "promotion_authorized": False, "business_readiness": "NOT_EVALUATED",
        }
        values = {"statistic_D", "effect_size_D", "p_value", "decision"}
        if set(result) != set(metadata) | values or digest({k: result[k] for k in metadata}) != digest(metadata):
            issues.append("RESULT_CONTEXT_BINDING_MISMATCH")
        else:
            for key, expected in (("statistic_D", expected_statistic),
                                  ("effect_size_D", expected_statistic),
                                  ("p_value", expected_p_value)):
                value = result[key]
                if (type(value) not in (int, float) or not math.isfinite(value) or
                        not math.isclose(value, expected, rel_tol=1e-12, abs_tol=1e-12)):
                    issues.append("TRUSTED_ORACLE_MISMATCH:" + key)
            expected_decision = ("REJECT_H0" if expected_p_value <= expected_request["alpha"]
                                 else "DO_NOT_REJECT_H0")
            if result["decision"] != expected_decision:
                issues.append("DECISION_MISMATCH")
        from hub_scripts.skill_execution.receipt import verify_execution_receipt
        receipt_path = ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py"
        if Path(verify_execution_receipt.__code__.co_filename).resolve() != receipt_path.resolve():
            raise RuntimeError("RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH")
        receipt_verification = verify_execution_receipt(
            payload, expected_skill=runner.SKILL, expected_entrypoint=runner.ENTRYPOINT,
            protected_primitive=runner.PRIMITIVE_ID, expected_run_id=expected_run_id,
            expected_release={
                "manifest_name": "release_manifest.json",
                "manifest_sha256": release["manifest_sha256"],
                "contract_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/execution_contract.json"],
                "runner_git_blob_sha1": release["artifacts"][f"skills/{runner.SKILL}/scripts/run.py"]},
            release_integrity_ok=True).to_dict()
        if receipt_verification["valid"] is not True:
            issues.extend(receipt_verification["issues"])
        if release_integrity(SKILL_DIR, runner.REQUIRED_RELEASE_PATHS) != release:
            issues.append("RELEASE_CHANGED_DURING_VERIFICATION")
    except Exception as exc:
        issues.append(f"{type(exc).__name__}:{exc}")
    return {"valid": not issues, "status": "VALID" if not issues else "INVALID",
            "issues": issues, "scope": "CURRENT_RELEASE_REQUEST_RECEIPT_AND_TRUSTED_FIXTURE_ORACLE",
            "promotion_authorized": False, "completion_authorized": False}


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Verify a saved SER04 runner payload")
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--expected-statistic", required=True, type=float)
    parser.add_argument("--expected-p-value", required=True, type=float)
    args = parser.parse_args(argv)
    try:
        if not math.isfinite(args.expected_statistic) or not math.isfinite(args.expected_p_value):
            raise ValueError("ORACLE_NONFINITE")
        payload = loads_strict(args.payload.read_text(encoding="utf-8"))
        request = loads_strict(args.request.read_text(encoding="utf-8"))
        result = verify(
            payload, expected_request=request, expected_run_id=args.run_id,
            expected_statistic=args.expected_statistic,
            expected_p_value=args.expected_p_value)
    except (OSError, UnicodeError, ValueError) as exc:
        result = {"valid": False, "status": "INVALID",
                  "issues": [f"{type(exc).__name__}:{exc}"],
                  "scope": "CURRENT_RELEASE_REQUEST_RECEIPT_AND_TRUSTED_FIXTURE_ORACLE",
                  "promotion_authorized": False, "completion_authorized": False}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if result["valid"] is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
