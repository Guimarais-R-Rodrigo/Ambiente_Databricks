from __future__ import annotations

import importlib
import sys
from datetime import timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import closed, digest, integer, text, utc_instant
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity
from hub_scripts.skill_execution.postflight import sha256_digest

SKILL = "hub-ml-cross-eda-ml"
ENTRYPOINT = "skills/hub-ml-cross-eda-ml/scripts/run_pit.py::run"
PRIMITIVE_ID = "point_in_time_join"
BASE = "skills/" + SKILL + "/"
REQUIRED_RELEASE_PATHS = {
    "hub_scripts/skill_execution/__init__.py",
    "hub_scripts/skill_execution/skill_execution.py",
    "hub_scripts/skill_execution/receipt/__init__.py",
    "hub_scripts/skill_execution/postflight/__init__.py",
    "hub_scripts/skill_execution/domain_context/__init__.py",
    "hub_scripts/skill_execution/domain_context/release.py",
    "hub_snippets/spark/pit_join/__init__.py",
    "hub_snippets/spark/pit_join/pit_join.py",
    "hub_snippets/spark/join_diagnostics/__init__.py",
    "hub_snippets/spark/join_diagnostics/join_diagnostics.py",
    BASE + "execution_contract.json",
    BASE + "diagnostic_contract.json",
    BASE + "pit_contract.json",
    BASE + "input.schema.json",
    BASE + "scripts/preflight.py",
    BASE + "scripts/run_diagnostic.py",
    BASE + "scripts/verify_diagnostic.py",
    BASE + "scripts/run_pit.py",
    BASE + "scripts/verify_pit.py",
}

def _preflight():
    return load_sibling(SKILL_DIR / "scripts/preflight.py", "_ser06_l2_for_pit")

def _primitive():
    module = importlib.import_module("hub_snippets.spark.pit_join")
    expected = ASSISTANT_ROOT / "hub_snippets/spark/pit_join/__init__.py"
    if Path(module.__file__).resolve() != expected.resolve():
        raise RuntimeError("PRIMITIVE_IMPORT_ORIGIN_MISMATCH")
    primitive = module.pit_join
    implementation = ASSISTANT_ROOT / "hub_snippets/spark/pit_join/pit_join.py"
    if Path(primitive.__code__.co_filename).resolve() != implementation.resolve():
        raise RuntimeError("PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH")
    return primitive

def prepare(context: object, datasets: object, *, window_days: int) -> dict:
    domain = _preflight().preflight(context)
    if domain["status"] != "PASS":
        raise ValueError("L2_PREFLIGHT_BLOCKED:" + ",".join(domain["issues"]))
    if context["pit"] != "APPLICABLE":
        raise ValueError("PIT_APPLICABLE_REQUIRED")
    spec = context["temporal"]
    if spec["boundary"] != "LE":
        raise ValueError("PIT_LT_UNSUPPORTED_BY_HELPER")
    if context["cardinality"] != "N:1":
        raise ValueError("PIT_N_TO_ONE_PROFILE_REQUIRED")
    integer(window_days, "window_days", minimum=1, maximum=36500)
    if not isinstance(datasets, dict) or set(datasets) != {s["id"] for s in context["sources"]}:
        raise ValueError("DATASETS:SOURCE_IDS_MISMATCH")
    if context["entity_keys"] != ["entity_id"]:
        raise ValueError("PIT_PROFILE_ENTITY_ID_ONLY")
    if spec["reference_column"] != "reference_at" or spec["availability_column"] != "available_at":
        raise ValueError("PIT_PROFILE_COLUMN_NAMES_REQUIRED")
    if context["decision_at"] != utc_instant(context["decision_at"], "decision_at").isoformat().replace("+00:00", "Z"):
        raise ValueError("DECISION_AT_CANONICAL_UTC_REQUIRED")
    sources = {s["id"]: s for s in context["sources"]}
    anchor = context["anchor"]
    historical = next(s for s in sources if s != anchor)
    facts, features = datasets[anchor], datasets[historical]
    if not isinstance(facts, list) or not 1 <= len(facts) <= 500 or not isinstance(features, list) or not 1 <= len(features) <= 500:
        raise ValueError("DATASETS:BOUNDED_NONEMPTY_ROWS_REQUIRED")
    if set(sources[anchor]["columns"]) != {"decision_id", "entity_id", "decision_at"}:
        raise ValueError("FACT_SCHEMA_UNSUPPORTED")
    if set(sources[historical]["columns"]) != {"entity_id", "reference_at", "available_at", "feature_value"}:
        raise ValueError("FEATURE_SCHEMA_UNSUPPORTED")
    for sid, rows in datasets.items():
        if any(not isinstance(row, dict) or set(row) != set(sources[sid]["columns"]) for row in rows):
            raise ValueError("DATASETS:SCHEMA_MISMATCH")
        if digest(rows) != sources[sid]["content_sha256"]:
            raise ValueError("DATASETS:CONTENT_SHA256_MISMATCH:" + sid)
    ids = set()
    pairs = set()
    for row in facts:
        rid = text(row["decision_id"], "decision_id")
        entity = text(row["entity_id"], "entity_id")
        decision_time = utc_instant(row["decision_at"], "row.decision_at")
        if rid in ids or (entity, decision_time) in pairs:
            raise ValueError("FACT_DUPLICATE_ID_OR_GRAIN")
        ids.add(rid)
        pairs.add((entity, decision_time))
        if decision_time != utc_instant(context["decision_at"], "decision_at"):
            raise ValueError("FACT_DECISION_OUTSIDE_DECLARED_CUT")
    refs = set()
    for row in features:
        entity = text(row["entity_id"], "entity_id")
        ref = utc_instant(row["reference_at"], "reference_at")
        availability = utc_instant(row["available_at"], "available_at")
        if row["reference_at"] != ref.isoformat().replace("+00:00", "Z") or row["available_at"] != availability.isoformat().replace("+00:00", "Z"):
            raise ValueError("FEATURE_CLOCKS_CANONICAL_UTC_REQUIRED")
        if availability != ref + timedelta(days=spec["lag_days"]):
            raise ValueError("AVAILABLE_AT_CONTRADICTS_CONSTANT_LAG")
        value = row["feature_value"]
        if type(value) is not int or not -1000000 <= value <= 1000000:
            raise ValueError("FEATURE_VALUE_BOUNDED_INT_REQUIRED")
        pair = (entity, ref)
        if pair in refs:
            raise ValueError("FEATURE_REFERENCE_TIE_REJECTED")
        refs.add(pair)
    return {"domain": domain, "facts": facts, "features": features,
            "source_hashes": {sid: sources[sid]["content_sha256"] for sid in sorted(sources)}}

def run(context: object, datasets: object, spark, *, window_days: int, run_id: str) -> dict:
    trace = {
        "trace_version": "0.1", "skill": SKILL, "entrypoint": ENTRYPOINT,
        "run_id": run_id, "status": "BLOCKED", "preflight_status": "NOT_RUN",
        "manifest": "release_manifest.json", "manifest_digest": None,
        "contract_digest": None, "runner_digest": None, "input_digest": None,
        "output_digest": None, "resources_resolved": [], "resources_called": [],
        "resources_completed": [], "resources_imported": [], "templates_loaded": [],
        "template_digests": {}, "decisions": [], "context_provenance": {},
        "blocking_issues": [], "fallback_used": False, "writes_performed": False,
        "artifacts_digest": None,
    }
    try:
        text(run_id, "run_id")
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        trace["manifest_digest"] = release["manifest_sha256"]
        trace["contract_digest"] = release["artifacts"][BASE + "pit_contract.json"]
        trace["runner_digest"] = release["artifacts"][BASE + "scripts/run_pit.py"]
        prepared = prepare(context, datasets, window_days=window_days)
        trace["preflight_status"] = "PASS"
        trace["input_digest"] = digest({"context": context, "datasets": datasets, "window_days": window_days})
        from hub_scripts.skill_execution import run_preflight
        sef = run_preflight(SKILL_DIR / "pit_contract.json", assistant_root=ASSISTANT_ROOT, context={}).to_dict()
        if sef["status"] != "PASS":
            raise ValueError("PIT_CONTRACT_BLOCKED")
        if spark.conf.get("spark.sql.session.timeZone") != "UTC":
            raise ValueError("SPARK_UTC_SESSION_REQUIRED")
        trace["resources_resolved"] = [PRIMITIVE_ID]
        trace["decisions"] = [{"item_id": PRIMITIVE_ID, "item_type": "resource", "applicable": True, "resolved": True}]
        trace["context_provenance"] = {
            "numeric_columns": {"source": "runtime_derived", "conflict": False, "value": 1},
            "population": {"source": "user_intent", "conflict": False},
            "calendar": {"source": "user_intent", "conflict": False},
        }
        from pyspark.sql.types import StringType, StructField, StructType, TimestampType, LongType
        fs = StructType([StructField("decision_id", StringType(), False),
                         StructField("entity_id", StringType(), False),
                         StructField("decision_at", TimestampType(), False)])
        hs = StructType([StructField("entity_id", StringType(), False),
                         StructField("reference_at", TimestampType(), False),
                         StructField("available_at", TimestampType(), False),
                         StructField("feature_value", LongType(), False)])
        fact_rows = [(r["decision_id"], r["entity_id"], utc_instant(r["decision_at"], "decision_at")) for r in prepared["facts"]]
        hist_rows = [(r["entity_id"], utc_instant(r["reference_at"], "reference_at"),
                      utc_instant(r["available_at"], "available_at"), r["feature_value"]) for r in prepared["features"]]
        facts = spark.createDataFrame(fact_rows, fs)
        history = spark.createDataFrame(hist_rows, hs)
        trace["resources_called"] = [PRIMITIVE_ID]
        joined, diagnostic = _primitive()(
            facts, history, "entity_id", "decision_at", "reference_at",
            atraso_publicacao_dias=context["temporal"]["lag_days"],
            janela_maxima_dias=window_days, colunas_feature=["feature_value"],
            politica_empate="erro", devolver_disponibilidade=True)
        from pyspark.sql import functions as F
        time_format = "yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'"
        selected = joined.select(
            "decision_id", "entity_id", "feature_value",
            F.date_format(F.col("decision_at"), time_format).alias("decision_at_utc"),
            F.date_format(F.col("__feature_disponivel_em"), time_format).alias("available_at_utc"))
        records = []
        for row in selected.collect():
            records.append({"decision_id": row["decision_id"], "entity_id": row["entity_id"],
                            "decision_at": row["decision_at_utc"],
                            "feature_value": row["feature_value"],
                            "available_at": row["available_at_utc"]})
        records.sort(key=lambda r: r["decision_id"])
        trace["resources_completed"] = [PRIMITIVE_ID]
        if len(records) != len(prepared["facts"]) or {r["decision_id"] for r in records} != {r["decision_id"] for r in prepared["facts"]}:
            raise ValueError("POST_JOIN_CARDINALITY_MISMATCH")
        result = {"schema_version": "SER06-PIT-1", "scope": "LOCAL_SYNTHETIC_PIT_V1",
                  "context_sha256": digest(context), "source_content_sha256": prepared["source_hashes"],
                  "window_days": window_days, "records": records, "diagnostic": diagnostic,
                  "pit_executed": True, "writes_performed": False,
                  "ml_readiness": "NOT_EVALUATED", "promotion_authorized": False}
        if digest({"context": context, "datasets": datasets, "window_days": window_days}) != trace["input_digest"]:
            raise ValueError("INPUT_CHANGED_DURING_EXECUTION")
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise ValueError("RELEASE_CHANGED_DURING_EXECUTION")
        artifacts = {PRIMITIVE_ID: result}
        trace["artifacts_digest"] = sha256_digest(artifacts)
        trace["output_digest"] = sha256_digest(result)
        trace["status"] = "PASS"
        from hub_scripts.skill_execution.receipt import build_execution_receipt
        receipt = build_execution_receipt(trace, result, expected_skill=SKILL,
                                          expected_entrypoint=ENTRYPOINT, protected_primitive=PRIMITIVE_ID)
        if receipt is None:
            raise RuntimeError("CANONICAL_RECEIPT_NOT_ISSUED")
        return {"status": "PASS", "preflight": prepared["domain"], "trace": trace,
                "result": result, "artifacts": artifacts, "receipt": receipt,
                "handoff": None, "postflight": None, "scope_completion_authorized": False}
    except Exception as exc:
        trace["status"] = "BLOCKED"
        trace["blocking_issues"] = [type(exc).__name__ + ":" + str(exc)]
        return {"status": "BLOCKED", "preflight": None, "trace": trace, "result": None,
                "artifacts": {}, "receipt": None, "handoff": None,
                "postflight": None, "scope_completion_authorized": False}
