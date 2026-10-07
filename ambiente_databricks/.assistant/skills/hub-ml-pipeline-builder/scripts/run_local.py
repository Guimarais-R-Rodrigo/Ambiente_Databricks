"""Bounded synthetic Spark MERGE; no persistent write or deployment."""
from __future__ import annotations

import importlib
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))
from hub_scripts.skill_execution.domain_context import digest
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-pipeline-builder"
ENTRYPOINT = "skills/hub-ml-pipeline-builder/scripts/run_local.py::run"
PRIMITIVE_ID = "data_quality_check"
REQUIRED_RELEASE_PATHS = {
    "hub_scripts/skill_execution/__init__.py",
    "hub_scripts/skill_execution/skill_execution.py",
    "hub_scripts/skill_execution/receipt/__init__.py",
    "hub_scripts/skill_execution/domain_context/__init__.py",
    "hub_scripts/skill_execution/domain_context/release.py",
    "hub_scripts/data_quality_check/__init__.py",
    "hub_scripts/data_quality_check/data_quality_check.py",
    f"skills/{SKILL}/execution_contract.json",
    f"skills/{SKILL}/input.schema.json",
    f"skills/{SKILL}/templates/pipeline_spec.md",
    f"skills/{SKILL}/scripts/preflight.py",
    f"skills/{SKILL}/local_execution_contract.json",
    f"skills/{SKILL}/scripts/run_local.py",
    f"skills/{SKILL}/scripts/verify_local.py",
    f"skills/{SKILL}/delta_execution_contract.json",
    f"skills/{SKILL}/scripts/run_delta.py",
}
_INSTANT = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z")


def _preflight():
    return load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser13_spec_for_run")


def _primitive():
    module = importlib.import_module("hub_scripts.data_quality_check")
    if Path(module.__file__).resolve() != (ASSISTANT_ROOT / "hub_scripts/data_quality_check/__init__.py").resolve():
        raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
    primitive = module.data_quality_check
    if Path(primitive.__code__.co_filename).resolve() != (ASSISTANT_ROOT / "hub_scripts/data_quality_check/data_quality_check.py").resolve():
        raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
    return primitive


def _rows(rows: object, *, allow_empty: bool) -> list[dict]:
    if not isinstance(rows, list) or len(rows) > 100 or (not allow_empty and not rows):
        raise ValueError("ROWS_BOUNDED_REQUIRED")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"id", "event_at", "value"}:
            raise ValueError("ROW_SCHEMA_INVALID")
        key, value, instant = row["id"], row["value"], row["event_at"]
        if type(key) is not int or not 0 <= key <= 1_000_000 or key in seen:
            raise ValueError("ROW_KEY_INVALID_OR_DUPLICATED")
        if type(value) is not int or not -1_000_000 <= value <= 1_000_000:
            raise ValueError("ROW_VALUE_INVALID")
        if not isinstance(instant, str) or _INSTANT.fullmatch(instant) is None:
            raise ValueError("ROW_EVENT_AT_INVALID")
        try:
            if datetime.strptime(instant, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M:%SZ") != instant:
                raise ValueError()
        except ValueError as exc:
            raise ValueError("ROW_EVENT_AT_INVALID") from exc
        seen.add(key)
    return rows


def _validate(request: object) -> tuple[dict, dict]:
    if not isinstance(request, dict) or set(request) != {
            "schema_version", "synthetic", "operation", "spec", "prior_rows", "batch_rows"}:
        raise ValueError("RUN_REQUEST_SCHEMA_INVALID")
    if request["schema_version"] != "SER13-LOCAL-RUN-1" or request["synthetic"] is not True or request["operation"] != "RUN_LOCAL_SPARK":
        raise ValueError("RUN_REQUEST_PROFILE_INVALID")
    spec = request["spec"]
    domain = _preflight().preflight(spec)
    if domain["status"] != "PASS":
        raise ValueError("SPEC_PREFLIGHT_BLOCKED")
    if (spec["write_mode"] != "MERGE" or spec["idempotency"] != "MERGE_ON_KEYS"
            or spec["incremental"] != "BATCH" or spec["watermark_seconds"] is not None
            or spec["primary_keys"] != ["id"] or spec["columns"] != ["id", "event_at", "value"]
            or spec["event_time"] != "event_at"):
        raise ValueError("RUN_PROFILE_REQUIRES_FIXED_MERGE_SCHEMA")
    _rows(request["prior_rows"], allow_empty=True)
    _rows(request["batch_rows"], allow_empty=False)
    if len({r["id"] for r in request["prior_rows"] + request["batch_rows"]}) > 100:
        raise ValueError("OUTPUT_ROWS_BOUND_EXCEEDED")
    return spec, domain


def _merge(prior: list[dict], batch: list[dict]) -> list[dict]:
    state = {row["id"]: dict(row) for row in prior}
    for row in batch:
        current = state.get(row["id"])
        if current is None or row["event_at"] > current["event_at"]:
            state[row["id"]] = dict(row)
        elif row["event_at"] == current["event_at"] and row != current:
            raise ValueError("EQUAL_EVENT_TIME_CONFLICT")
    return [state[key] for key in sorted(state)]


def run(request: object, spark, *, run_id: str) -> dict:
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
    view_name = None
    view_created = False
    try:
        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError("RUN_ID_REQUIRED")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][f"skills/{SKILL}/local_execution_contract.json"]
        trace["runner_digest"] = release["artifacts"][f"skills/{SKILL}/scripts/run_local.py"]
        spec, domain = _validate(request)
        trace["preflight_status"] = domain["status"]
        trace["input_digest"] = digest(request)
        from hub_scripts.skill_execution import run_preflight
        sef = run_preflight(SKILL_DIR / "local_execution_contract.json", assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        if sef["status"] != "PASS":
            raise ValueError("LOCAL_RUN_CONTRACT_BLOCKED")
        trace["resources_resolved"] = [PRIMITIVE_ID]
        trace["decisions"] = [{"item_id": PRIMITIVE_ID, "item_type": "resource", "applicable": True, "resolved": True}]
        output = _merge(request["prior_rows"], request["batch_rows"])
        from pyspark.sql.types import LongType, StringType, StructField, StructType
        schema = StructType([StructField("id", LongType(), False),
                             StructField("event_at", StringType(), False),
                             StructField("value", LongType(), False)])
        from pyspark.sql import Window, functions as F
        prior = spark.createDataFrame(
            [(r["id"], r["event_at"], r["value"]) for r in request["prior_rows"]], schema)
        batch = spark.createDataFrame(
            [(r["id"], r["event_at"], r["value"]) for r in request["batch_rows"]], schema)
        union = prior.withColumn("_source_order", F.lit(0)).unionByName(
            batch.withColumn("_source_order", F.lit(1)))
        window = Window.partitionBy("id").orderBy(
            F.col("event_at").desc(), F.col("_source_order").desc())
        frame = union.withColumn("_row_number", F.row_number().over(window)).where(
            F.col("_row_number") == 1).drop("_row_number", "_source_order")
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False, "value": 2},
            "synthetic_scope": {"source": "user_intent", "conflict": False},
        }
        candidate_name = "_ser13_" + uuid.uuid4().hex
        if spark.catalog.tableExists(candidate_name):
            raise RuntimeError("TEMP_VIEW_ALREADY_EXISTS")
        view_name = candidate_name
        frame.createTempView(view_name)
        view_created = True
        primitive = _primitive()
        trace["resources_called"] = [PRIMITIVE_ID]
        quality = primitive(view_name, ["id"])
        trace["resources_completed"] = [PRIMITIVE_ID]
        actual = [row.asDict() for row in spark.table(view_name).orderBy("id").collect()]
        if actual != output:
            raise RuntimeError("SPARK_OUTPUT_MISMATCH")
        checks = quality["checks"]
        if (quality["status"] != "pass" or checks["row_count"] != len(actual)
                or checks["pk_uniqueness"]["duplicate_rows"] != 0
                or checks["pk_uniqueness"]["null_key_rows"] != 0):
            raise ValueError("QUALITY_CHECK_FAILED")
        result = {
            "schema_version": "SER13-LOCAL-RESULT-1", "profile": "LOCAL_SYNTHETIC_SPARK_MERGE_V1",
            "spec_sha256": digest(spec), "prior_sha256": digest(request["prior_rows"]),
            "batch_sha256": digest(request["batch_rows"]), "destination": spec["destination"],
            "rows": actual, "output_sha256": digest(actual), "row_count": len(actual),
            "quality": {"status": "pass", "row_count": len(actual), "pk_duplicate_rows": 0, "pk_null_rows": 0},
            "replay_semantics": "MERGE_LATEST_EVENT_TIME_EQUAL_IDENTICAL_ONLY",
            "local_spark_executed": True, "persistent_write": False,
            "deployment_status": "NOT_RUN", "completion_authorized": False, "promotion_authorized": False,
        }
        if not spark.catalog.dropTempView(view_name):
            raise RuntimeError("TEMP_VIEW_CLEANUP_FAILED")
        view_name = None
        view_created = False
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EXECUTION")
        trace["output_digest"] = digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL, expected_entrypoint=ENTRYPOINT,
                                          protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return {"status": "PASS", "preflight": domain, "trace": trace, "result": result, "receipt": receipt}
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [f"{type(exc).__name__}:{exc}"]
        return {"status": "BLOCKED", "preflight": domain, "trace": trace, "result": None, "receipt": None}
    finally:
        if view_created:
            try:
                cleaned = spark.catalog.dropTempView(view_name)
            except Exception:
                cleaned = False
            if not cleaned:
                trace["status"] = "BLOCKED"
                trace["blocking_issues"].append("TEMP_VIEW_CLEANUP_FAILED_RESIDUE_UNKNOWN")
                return {"status": "BLOCKED", "preflight": domain, "trace": trace,
                        "result": None, "receipt": None}
