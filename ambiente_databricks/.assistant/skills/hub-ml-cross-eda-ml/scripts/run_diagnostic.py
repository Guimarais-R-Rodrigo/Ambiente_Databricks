from __future__ import annotations

import hashlib
import importlib
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-cross-eda-ml"
ENTRYPOINT = "skills/hub-ml-cross-eda-ml/scripts/run_diagnostic.py::run"
PRIMITIVE_ID = "join_diagnostics"
REQUIRED_RELEASE_PATHS = {
    "hub_scripts/skill_execution/__init__.py",
    "hub_scripts/skill_execution/skill_execution.py",
    "hub_scripts/skill_execution/receipt/__init__.py",
    "hub_scripts/skill_execution/domain_context/__init__.py",
    "hub_scripts/skill_execution/domain_context/release.py",
    "hub_scripts/skill_execution/postflight/__init__.py",
    "hub_snippets/spark/pit_join/__init__.py",
    "hub_snippets/spark/pit_join/pit_join.py",
    "hub_snippets/spark/join_diagnostics/__init__.py",
    "hub_snippets/spark/join_diagnostics/join_diagnostics.py",
    f"skills/{SKILL}/execution_contract.json",
    f"skills/{SKILL}/diagnostic_contract.json",
    f"skills/{SKILL}/pit_contract.json",
    f"skills/{SKILL}/input.schema.json",
    f"skills/{SKILL}/scripts/preflight.py",
    f"skills/{SKILL}/scripts/run_diagnostic.py",
    f"skills/{SKILL}/scripts/verify_diagnostic.py",
    f"skills/{SKILL}/scripts/run_pit.py",
    f"skills/{SKILL}/scripts/verify_pit.py",
}


def _preflight():
    return load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser05_l2_for_diagnostic")


def _primitive():
    module = importlib.import_module("hub_snippets.spark.join_diagnostics")
    expected = ASSISTANT_ROOT / "hub_snippets/spark/join_diagnostics/__init__.py"
    if Path(module.__file__).resolve() != expected.resolve():
        raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
    primitive = module.diagnosticar_join
    implementation = ASSISTANT_ROOT / "hub_snippets/spark/join_diagnostics/join_diagnostics.py"
    if Path(primitive.__code__.co_filename).resolve() != implementation.resolve():
        raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
    return primitive


def _rows(context: dict, datasets: object) -> tuple[list[dict], list[dict], dict]:
    if not isinstance(datasets, dict) or set(datasets) != {s["id"] for s in context["sources"]}:
        raise ValueError("DATASETS:SOURCE_IDS_MISMATCH")
    rows_by_id = {}
    hashes = {}
    key_types = {}
    for source in context["sources"]:
        sid = source["id"]
        rows = datasets[sid]
        if not isinstance(rows, list) or not rows or len(rows) > 1000:
            raise ValueError("DATASETS:BOUNDED_NONEMPTY_ROWS_REQUIRED")
        columns = set(source["columns"])
        if any(not isinstance(row, dict) or set(row) != columns for row in rows):
            raise ValueError("DATASETS:SCHEMA_MISMATCH")
        if any(any(row[key] is None for key in context["entity_keys"]) for row in rows):
            raise ValueError("DATASETS:NULL_KEY_REJECTED")
        for key in context["entity_keys"]:
            observed_types = {type(row[key]) for row in rows}
            if len(observed_types) != 1 or next(iter(observed_types)) not in (str, int):
                raise ValueError("DATASETS:KEY_TYPE_UNSUPPORTED_OR_MIXED:" + key)
            observed_type = next(iter(observed_types))
            if key in key_types and key_types[key] is not observed_type:
                raise ValueError("DATASETS:KEY_TYPE_MISMATCH:" + key)
            key_types[key] = observed_type
        actual = digest(rows)
        if actual != source["content_sha256"]:
            raise ValueError("DATASETS:CONTENT_SHA256_MISMATCH:" + sid)
        rows_by_id[sid] = rows
        hashes[sid] = actual
    anchor = context["anchor"]
    other = next(s["id"] for s in context["sources"] if s["id"] != anchor)
    left = rows_by_id[anchor]
    if len({tuple(row[k] for k in context["entity_keys"]) for row in left}) != len(left):
        raise ValueError("DATASETS:ANCHOR_KEY_NOT_UNIQUE")
    return left, rows_by_id[other], hashes


def run(context: object, datasets: object, spark, *, run_id: str) -> dict:
    trace = {
        "trace_version": "0.1", "skill": SKILL, "entrypoint": ENTRYPOINT,
        "run_id": run_id, "status": "BLOCKED", "preflight_status": "NOT_RUN",
        "manifest": "release_manifest.json", "manifest_digest": None,
        "contract_digest": None, "runner_digest": None, "input_digest": None,
        "output_digest": None, "resources_resolved": [], "resources_called": [],
        "resources_completed": [], "decisions": [], "context_provenance": {},
        "blocking_issues": [], "fallback_used": False, "writes_performed": False,
    }
    domain = None
    try:
        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError("RUN_ID_REQUIRED")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][f"skills/{SKILL}/diagnostic_contract.json"]
        trace["runner_digest"] = release["artifacts"][f"skills/{SKILL}/scripts/run_diagnostic.py"]
        domain = _preflight().preflight(context)
        trace["preflight_status"] = domain["status"]
        if domain["status"] != "PASS":
            raise ValueError("L2_PREFLIGHT_BLOCKED:" + ",".join(domain["issues"]))
        if context["pit"] != "NOT_APPLICABLE":
            raise ValueError("PIT_APPLICABLE_REQUIRES_SER06")
        left_rows, right_rows, hashes = _rows(context, datasets)
        trace["input_digest"] = digest({"context": context, "datasets": datasets})
        from hub_scripts.skill_execution import run_preflight
        sef = run_preflight(SKILL_DIR / "diagnostic_contract.json", assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        if sef["status"] != "PASS":
            raise ValueError("DIAGNOSTIC_CONTRACT_BLOCKED")
        trace["resources_resolved"] = [PRIMITIVE_ID]
        trace["decisions"] = [{"item_id": PRIMITIVE_ID, "item_type": "resource",
                               "applicable": True, "resolved": True}]
        from pyspark.sql.types import NumericType
        left = spark.createDataFrame(left_rows)
        right = spark.createDataFrame(right_rows)
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False,
                                "value": sum(isinstance(f.dataType, NumericType) for f in left.schema.fields)},
            "population": {"source": "user_intent", "conflict": False},
            "calendar": {"source": "user_intent", "conflict": False},
        }
        primitive = _primitive()
        trace["resources_called"] = [PRIMITIVE_ID]
        diagnostic = primitive(left, right, context["entity_keys"], amostra_orfas=5)
        trace["resources_completed"] = [PRIMITIVE_ID]
        if diagnostic["multiplicidade_max_direita"] > 1 or diagnostic["expansao_prevista_left"] > 1.0:
            raise ValueError("OBSERVED_CARDINALITY_CONTRADICTS_CONTEXT")
        result = {
            "schema_version": "SER05-DIAGNOSTIC-1", "context_sha256": digest(context),
            "source_content_sha256": hashes, "diagnostic": diagnostic,
            "join_executed": False, "coverage_measured": True,
            "pit_executed": False, "ml_readiness": "NOT_EVALUATED",
            "completion_authorized": False, "promotion_authorized": False,
        }
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL,
                                          expected_entrypoint=ENTRYPOINT,
                                          protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return {"status": "PASS", "preflight": domain, "trace": trace, "result": result, "receipt": receipt}
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [f"{type(exc).__name__}:{exc}"]
        return {"status": "BLOCKED", "preflight": domain, "trace": trace, "result": None, "receipt": None}
