from __future__ import annotations

import importlib
import json
import math
import sys
import uuid
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, loads_strict
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-validacao-estatistica"
ENTRYPOINT = "skills/hub-ml-validacao-estatistica/scripts/run.py::run"
PRIMITIVE_ID = "two_sample_ks"
PRIMITIVE_MODULE = "hub_snippets.ml.drift_detection"
LOCAL_FILES = {"SKILL.md", "input.schema.json", "execution_contract.json",
               "fixtures/ks_separated_request.json", "scripts/README.md",
               "scripts/preflight.py", "scripts/run.py", "scripts/verify.py"}
DEPENDENCIES = {
    "hub_scripts/skill_execution/__init__.py",
    "hub_scripts/skill_execution/skill_execution.py",
    "hub_scripts/skill_execution/receipt/__init__.py",
    "hub_scripts/skill_execution/domain_context/__init__.py",
    "hub_scripts/skill_execution/domain_context/release.py",
    "hub_snippets/ml/drift_detection/__init__.py",
    "hub_snippets/ml/drift_detection/drift_detection.py",
}
REQUIRED_RELEASE_PATHS = {f"skills/{SKILL}/{name}" for name in LOCAL_FILES} | DEPENDENCIES


def _preflight_module():
    return load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser04_domain_preflight")


def _canonical_primitive():
    module = importlib.import_module(PRIMITIVE_MODULE)
    expected = ASSISTANT_ROOT / "hub_snippets/ml/drift_detection/__init__.py"
    if Path(module.__file__).resolve() != expected.resolve():
        raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
    primitive = getattr(module, "calculate_ks", None)
    implementation = ASSISTANT_ROOT / "hub_snippets/ml/drift_detection/drift_detection.py"
    if not callable(primitive) or Path(primitive.__code__.co_filename).resolve() != implementation.resolve():
        raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
    return primitive


def run(request: object, *, run_id: str | None = None) -> dict:
    trace = {"trace_version": "0.1", "skill": SKILL, "entrypoint": ENTRYPOINT,
             "run_id": run_id if run_id is not None else str(uuid.uuid4()),
             "status": "BLOCKED", "preflight_status": "NOT_RUN",
             "manifest": "release_manifest.json", "manifest_digest": None,
             "contract_digest": None, "runner_digest": None,
             "input_digest": None, "output_digest": None,
             "resources_resolved": [], "resources_called": [], "resources_completed": [],
             "decisions": [], "context_provenance": {}, "blocking_issues": [],
             "fallback_used": False, "writes_performed": False}
    preflight_result = None
    try:
        if not isinstance(trace["run_id"], str) or not trace["run_id"].strip():
            raise ValueError("RUN_ID_REQUIRED")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][f"skills/{SKILL}/execution_contract.json"]
        trace["runner_digest"] = release["artifacts"][f"skills/{SKILL}/scripts/run.py"]
        preflight_result = _preflight_module().preflight(request)
        trace["preflight_status"] = preflight_result["status"]
        if preflight_result["status"] != "PASS":
            trace["blocking_issues"] = list(preflight_result["issues"])
            return {"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                    "result": None, "receipt": None}
        trace["input_digest"] = digest(request)
        trace["resources_resolved"] = [PRIMITIVE_ID]
        trace["decisions"] = [{"item_id": item["item_id"], "item_type": "resource",
                               "applicable": item["applicable"], "resolved": item["resolved"]}
                              for item in preflight_result["sef"]["resources"]]
        primitive = _canonical_primitive()
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False, "value": 2},
            "population": {"source": "user_intent", "conflict": False},
            "independence": {"source": "user_intent", "conflict": False},
            "test_family": {"source": "agent_declared", "conflict": False},
        }
        trace["resources_called"] = [PRIMITIVE_ID]
        statistic, pvalue = primitive(request["reference"], request["comparison"])
        trace["resources_completed"] = [PRIMITIVE_ID]
        if any(type(x) not in (float, int) or not math.isfinite(x) for x in (statistic, pvalue)):
            raise RuntimeError("PRIMITIVE_NONFINITE_RESULT")
        if not 0 <= statistic <= 1 or not 0 <= pvalue <= 1:
            raise RuntimeError("PRIMITIVE_RESULT_RANGE")
        result = {
            "schema_version": "SER04-RESULT-1", "profile": preflight_result["profile"],
            "population_id": request["population_id"], "unit": request["unit"],
            "question": request["question"], "hypothesis": request["hypothesis"],
            "estimand": request["estimand"], "independence": request["independence"],
            "multiple_testing": request["multiple_testing"], "alpha": request["alpha"],
            "reference_n": len(request["reference"]), "comparison_n": len(request["comparison"]),
            "statistic_D": float(statistic), "effect_size_D": float(statistic),
            "p_value": float(pvalue), "p_value_method": "SCIPY_KS_2SAMP_AUTO",
            "confidence_interval": None, "confidence_interval_status": "UNSUPPORTED_IN_PROFILE",
            "decision": "REJECT_H0" if pvalue <= request["alpha"] else "DO_NOT_REJECT_H0",
            "decision_scope": "DIAGNOSTIC_ONLY_INDEPENDENCE_DECLARED",
            "promotion_authorized": False, "business_readiness": "NOT_EVALUATED",
        }
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        receipt_path = ASSISTANT_ROOT / "hub_scripts/skill_execution/receipt/__init__.py"
        if Path(build_execution_receipt.__code__.co_filename).resolve() != receipt_path.resolve():
            raise RuntimeError("RECEIPT_IMPORT_ORIGIN_MISMATCH")
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL,
                                          expected_entrypoint=ENTRYPOINT,
                                          protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return {"status": "PASS", "preflight": preflight_result, "trace": trace,
                "result": result, "receipt": receipt}
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [f"{type(exc).__name__}:{exc}"]
        return {"status": "BLOCKED", "preflight": preflight_result, "trace": trace,
                "result": None, "receipt": None}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    try:
        payload = run(loads_strict(args.request.read_text(encoding="utf-8")), run_id=args.run_id)
    except (OSError, UnicodeError, ValueError) as exc:
        payload = {"status": "BLOCKED", "issues": [type(exc).__name__], "receipt": None}
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
