"""One owned synthetic Delta table probe; effect evidence is separate from Receipt V1."""
from __future__ import annotations

import json
import re
import sys
import uuid
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSISTANT_ROOT = SKILL_DIR.parents[1]
if str(ASSISTANT_ROOT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_scripts.skill_execution.domain_context import digest, loads_strict, text
from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity

SKILL = "hub-ml-pipeline-builder"
BASE = "skills/" + SKILL + "/"
PROFILE = "FREE_SYNTHETIC_DELTA_MERGE_V1"
REQUIRED_RELEASE_PATHS = {
    "hub_scripts/skill_execution/__init__.py",
    "hub_scripts/skill_execution/skill_execution.py",
    "hub_scripts/skill_execution/receipt/__init__.py",
    "hub_scripts/skill_execution/domain_context/__init__.py",
    "hub_scripts/skill_execution/domain_context/release.py",
    "hub_scripts/data_quality_check/__init__.py",
    "hub_scripts/data_quality_check/data_quality_check.py",
    BASE + "execution_contract.json",
    BASE + "input.schema.json",
    BASE + "templates/pipeline_spec.md",
    BASE + "scripts/preflight.py",
    BASE + "local_execution_contract.json",
    BASE + "scripts/run_local.py",
    BASE + "scripts/verify_local.py",
    BASE + "delta_execution_contract.json",
    BASE + "scripts/run_delta.py",
}
_TARGET = re.compile(r"workspace\.default\.skills_delivery_[0-9a-f]{32}\Z")
_TOKEN = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
_HEX32 = re.compile(r"[0-9a-f]{32}\Z")
_HEX64 = re.compile(r"[0-9a-f]{64}\Z")



def _snapshot(value: object, label: str):
    """Detach caller-owned mutable graphs and reject lossy/non-JSON input."""
    try:
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False)
        return loads_strict(raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("NONCANONICAL_" + label) from exc

def _local():
    path = SKILL_DIR / "scripts"
    return (load_sibling(path / "run_local.py", "_ser14_delta_local_runner"),
            load_sibling(path / "verify_local.py", "_ser14_delta_local_verifier"))


def _authorization(value: object, *, request: dict, run_id: str,
                   effect_name: str = "SYNTHETIC_DELTA_PROBE") -> dict:
    fields = {"authorized", "effect", "target_table", "request_digest", "run_id",
              "nonce", "cleanup", "expected_principal", "expected_catalog",
              "expected_schema"}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError("AUTHORIZATION_SHAPE_INVALID")
    if value["authorized"] is not True or value["effect"] != effect_name:
        raise ValueError("EFFECT_NOT_AUTHORIZED")
    if value["run_id"] != run_id or not isinstance(run_id, str) or _TOKEN.fullmatch(run_id) is None:
        raise ValueError("RUN_ID_BINDING_INVALID")
    if (not isinstance(value["target_table"], str) or
            _TARGET.fullmatch(value["target_table"]) is None):
        raise ValueError("TARGET_OUTSIDE_FREE_SYNTHETIC_NAMESPACE")
    if (not isinstance(value["request_digest"], str) or
            _HEX64.fullmatch(value["request_digest"]) is None or
            value["request_digest"] != digest(request)):
        raise ValueError("REQUEST_DIGEST_MISMATCH")
    if not isinstance(value["nonce"], str) or _HEX32.fullmatch(value["nonce"]) is None:
        raise ValueError("NONCE_INVALID")
    if value["cleanup"] != "DROP_OWNED":
        raise ValueError("OWNED_CLEANUP_REQUIRED")
    if value["expected_catalog"] != "workspace" or value["expected_schema"] != "default":
        raise ValueError("FREE_NAMESPACE_REQUIRED")
    text(value["expected_principal"], "expected_principal")
    return value


def _quoted_target(value: str) -> str:
    if _TARGET.fullmatch(value) is None:
        raise ValueError("TARGET_INVALID")
    return "`workspace`.`default`.`" + value.rsplit(".", 1)[1] + "`"


def _markers(auth: dict, provenance: dict | None = None) -> dict[str, str]:
    markers = {
        "skills_delivery.run_id": auth["run_id"],
        "skills_delivery.request_digest": auth["request_digest"],
        "skills_delivery.nonce": auth["nonce"],
    }
    if provenance is not None:
        for key, value in provenance.items():
            if not isinstance(value, str) or _HEX64.fullmatch(value) is None:
                raise ValueError("PROVENANCE_DIGEST_INVALID")
            markers["skills_delivery." + key] = value
    return markers


def _properties(spark, qualified: str) -> dict[str, str]:
    rows = spark.sql("SHOW TBLPROPERTIES " + qualified).collect()
    result = {}
    for row in rows:
        item = row.asDict()
        if not {"key", "value"} <= set(item):
            raise RuntimeError("PROPERTY_RESULT_UNSUPPORTED")
        result[item["key"]] = item["value"]
    return result


def _assert_owned(spark, qualified: str, auth: dict,
                  provenance: dict | None = None) -> None:
    if spark.catalog.tableExists(auth["target_table"]) is not True:
        raise RuntimeError("OWNED_TABLE_ABSENT")
    observed = _properties(spark, qualified)
    if any(observed.get(key) != value for key, value in _markers(auth, provenance).items()):
        raise RuntimeError("TABLE_OWNERSHIP_MARKERS_MISMATCH")


def _rows(spark, qualified: str, *, profile: str = "PIPELINE") -> list[dict]:
    if profile == "FE_PIT":
        fields = ("decision_id", "entity_id", "decision_at", "feature_value", "available_at")
        out = []
        for row in spark.sql("SELECT " + ", ".join(fields) + " FROM " + qualified).collect():
            item = row.asDict()
            if set(item) != set(fields):
                raise RuntimeError("FE_READBACK_SCHEMA_INVALID")
            if (not isinstance(item["decision_id"], str) or
                    not isinstance(item["entity_id"], str) or
                    not isinstance(item["decision_at"], str) or
                    (item["feature_value"] is not None and
                     (type(item["feature_value"]) is not int or
                      not -(2**63) <= item["feature_value"] < 2**63)) or
                    (item["available_at"] is not None and
                     not isinstance(item["available_at"], str))):
                raise RuntimeError("FE_READBACK_TYPE_INVALID")
            out.append({key: item[key] for key in fields})
        return sorted(out, key=lambda row: row["decision_id"])
    out = []
    for row in spark.sql("SELECT id, event_at, value FROM " + qualified).collect():
        item = row.asDict()
        if set(item) != {"id", "event_at", "value"}:
            raise RuntimeError("READBACK_SCHEMA_INVALID")
        if not isinstance(item["id"], str) or not item["id"].isdigit():
            raise RuntimeError("READBACK_ID_INVALID")
        out.append({"id": int(item["id"]), "event_at": item["event_at"],
                    "value": item["value"]})
    return sorted(out, key=lambda row: row["id"])


def _temp_view(spark, rows: list[dict], name: str,
               *, profile: str = "PIPELINE") -> None:
    from pyspark.sql.types import LongType, StringType, StructField, StructType
    if profile == "FE_PIT":
        schema = StructType([
            StructField("decision_id", StringType(), False),
            StructField("entity_id", StringType(), False),
            StructField("decision_at", StringType(), False),
            StructField("feature_value", LongType(), True),
            StructField("available_at", StringType(), True),
        ])
        frame = spark.createDataFrame(
            [tuple(row[key] for key in ("decision_id", "entity_id", "decision_at",
                                        "feature_value", "available_at")) for row in rows], schema)
        frame.createTempView(name)
        return
    schema = StructType([StructField("id", StringType(), False),
                         StructField("event_at", StringType(), False),
                         StructField("value", LongType(), False)])
    frame = spark.createDataFrame(
        [(str(row["id"]), row["event_at"], row["value"]) for row in rows], schema)
    frame.createTempView(name)


def _delta_version(spark, qualified: str) -> int:
    rows = spark.sql("DESCRIBE HISTORY " + qualified + " LIMIT 1").collect()
    if len(rows) != 1:
        raise RuntimeError("DELTA_HISTORY_UNAVAILABLE")
    version = rows[0].asDict().get("version")
    if type(version) is not int or version < 0:
        raise RuntimeError("DELTA_VERSION_INVALID")
    return version


def _delta_table_id(spark, qualified: str) -> str:
    rows = spark.sql("DESCRIBE DETAIL " + qualified).collect()
    if len(rows) != 1:
        raise RuntimeError("DELTA_DETAIL_UNAVAILABLE")
    table_id = rows[0].asDict().get("id")
    if not isinstance(table_id, str) or not table_id:
        raise RuntimeError("DELTA_TABLE_ID_INVALID")
    return table_id


def _assert_fe_table_id(spark, qualified: str, expected_id: str | None) -> None:
    if expected_id is not None and _delta_table_id(spark, qualified) != expected_id:
        raise RuntimeError("DELTA_TABLE_ID_CHANGED")


def _execute_owned(request: dict, expected_rows: list[dict], spark, authorization: dict,
                   *, run_id: str, compute_payload: dict | None = None,
                   profile: str = "PIPELINE", provenance: dict | None = None) -> dict:
    """CREATE/MERGE/readback/replay/DROP only for a freshly owned Free table."""
    effect = {
        "schema_version": "SER08-FE-DELTA-EFFECT-1" if profile == "FE_PIT" else "SER14-DELTA-EFFECT-1",
        "profile": "FREE_SYNTHETIC_PIT_FEATURE_MATERIALIZATION_V1" if profile == "FE_PIT" else PROFILE,
        "status": "BLOCKED", "phase": "NOT_RUN", "run_id": run_id,
        "target_table": None, "request_digest": None,
        "compute_receipt_id": None, "compute_manifest_sha256": None,
        "delta_manifest_sha256": None, "create_attempted": False,
        "create_acknowledged": False, "ownership_checks": 0,
        "initial_rows_sha256": None, "first_merge_rows_sha256": None,
        "replay_rows_sha256": None, "expected_rows_sha256": None,
        "cleanup": "NOT_RUN", "table_absent_after_cleanup": None,
        "persistent_write_performed": False, "issues": [],
    }
    if profile == "FE_PIT":
        effect.update({"first_delta_version": None, "replay_delta_version": None,
                       "table_id": None, "provenance": None})
    created = False
    cleaned = False
    temp_views = []
    qualified = None
    auth = None
    try:
        request = _snapshot(request, "REQUEST")
        expected_rows = _snapshot(expected_rows, "EXPECTED_ROWS")
        authorization = _snapshot(authorization, "AUTHORIZATION")
        compute_payload = (_snapshot(compute_payload, "COMPUTE_PAYLOAD")
                           if compute_payload is not None else None)
        provenance = (_snapshot(provenance, "PROVENANCE")
                      if provenance is not None else None)
        if profile not in {"PIPELINE", "FE_PIT"}:
            raise ValueError("PROFILE_UNSUPPORTED")
        if profile == "FE_PIT" and (
                not isinstance(provenance, dict) or
                set(provenance) != {"view_sha256", "source_sha256", "context_sha256",
                                    "cutoff_sha256", "receipt_sha256", "postflight_sha256"}):
            raise ValueError("FE_PROVENANCE_INVALID")
        auth = _authorization(
            authorization, request=request, run_id=run_id,
            effect_name="SYNTHETIC_FEATURE_MATERIALIZATION_PROBE"
            if profile == "FE_PIT" else "SYNTHETIC_DELTA_PROBE")
        effect["target_table"] = auth["target_table"]
        effect["request_digest"] = auth["request_digest"]
        effect["phase"] = "AUTH_VALIDATED"
        release = release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS)
        effect["delta_manifest_sha256"] = release["manifest_sha256"]
        if profile == "PIPELINE":
            from hub_scripts.skill_execution import run_preflight
            sef = run_preflight(SKILL_DIR / "delta_execution_contract.json",
                                assistant_root=ASSISTANT_ROOT, context={}).to_dict()
            if sef["status"] != "PASS":
                raise ValueError("DELTA_EXECUTION_CONTRACT_BLOCKED")
            local_run, local_verify = _local()
            if expected_rows != local_run._merge(request["prior_rows"], request["batch_rows"]):
                raise ValueError("EXPECTED_ROWS_NOT_MERGE_ORACLE")
            if compute_payload is None:
                compute_payload = local_run.run(request, spark, run_id=run_id + "-compute")
            verified = local_verify.verify(
                compute_payload, expected_request=request, expected_rows=expected_rows,
                expected_run_id=run_id + "-compute")
            if not verified["valid"]:
                raise ValueError("COMPUTE_RECEIPT_OR_OUTPUT_INVALID:" + str(verified["issues"]))
            effect["compute_receipt_id"] = compute_payload["receipt"]["receipt_id"]
            effect["compute_manifest_sha256"] = compute_payload["receipt"]["release"]["manifest_sha256"]
        else:
            if compute_payload is not None or not isinstance(request, dict) or set(request) != {
                    "schema_version", "profile", "feature_view_sha256", "external_input_sha256",
                    "upstream_receipt_id", "upstream_postflight_id", "rows"}:
                raise ValueError("FE_REQUEST_INVALID")
            if request["schema_version"] != "SER08-FE-MATERIALIZATION-REQUEST-1" or request["profile"] != "FE_PIT":
                raise ValueError("FE_PROFILE_INVALID")
            if request["rows"] != expected_rows:
                raise ValueError("FE_EXPECTED_ROWS_MISMATCH")
            effect["provenance"] = provenance
            effect["compute_receipt_id"] = request["upstream_receipt_id"]
        effect["expected_rows_sha256"] = digest(expected_rows)
        effect["phase"] = "COMPUTE_VALIDATED"
        session = spark.sql(
            "SELECT current_catalog() AS catalog, current_schema() AS schema, "
            "current_user() AS principal").collect()[0].asDict()
        if (session.get("catalog") != auth["expected_catalog"] or
                session.get("schema") != auth["expected_schema"] or
                session.get("principal") != auth["expected_principal"]):
            raise ValueError("SESSION_AUTHORITY_MISMATCH")
        if profile == "FE_PIT" and spark.conf.get("spark.sql.session.timeZone") != "UTC":
            raise ValueError("UTC_SPARK_SESSION_REQUIRED")
        effect["phase"] = "SESSION_VALIDATED"
        if spark.catalog.tableExists(auth["target_table"]) is not False:
            raise ValueError("TARGET_ALREADY_EXISTS")
        qualified = _quoted_target(auth["target_table"])
        markers = _markers(auth, provenance)
        columns = ("(decision_id STRING NOT NULL, entity_id STRING NOT NULL, decision_at STRING NOT NULL, "
                   "feature_value BIGINT, available_at STRING) " if profile == "FE_PIT" else
                   "(id STRING NOT NULL, event_at STRING NOT NULL, value BIGINT NOT NULL) ")
        ddl = (
            "CREATE TABLE " + qualified +
            " " + columns +
            "USING DELTA TBLPROPERTIES (" +
            ", ".join("'" + key + "' = '" + value + "'" for key, value in markers.items()) + ")"
        )
        effect["create_attempted"] = True
        effect["phase"] = "CREATE_ATTEMPTED"
        spark.sql(ddl)
        created = True
        effect["create_acknowledged"] = True
        effect["persistent_write_performed"] = True
        effect["phase"] = "CREATED"
        _assert_owned(spark, qualified, auth, provenance)
        effect["ownership_checks"] += 1
        effect["phase"] = "OWNERSHIP_VALIDATED"
        if profile == "PIPELINE":
            prior_view = "_skills_delta_prior_" + uuid.uuid4().hex
            _temp_view(spark, request["prior_rows"], prior_view)
            temp_views.append(prior_view)
            spark.sql("INSERT INTO " + qualified +
                      " SELECT id, event_at, value FROM `" + prior_view + "`")
        initial = _rows(spark, qualified, profile=profile)
        if initial != (sorted(request["prior_rows"], key=lambda row: row["id"])
                       if profile == "PIPELINE" else []):
            raise RuntimeError("INITIAL_READBACK_MISMATCH")
        effect["initial_rows_sha256"] = digest(initial)
        effect["phase"] = "PRIOR_LOADED"
        batch_view = "_skills_delta_batch_" + uuid.uuid4().hex
        if profile == "PIPELINE":
            _temp_view(spark, request["batch_rows"], batch_view)
        else:
            _temp_view(spark, request["rows"], batch_view, profile=profile)
        temp_views.append(batch_view)
        merge = (
            "MERGE INTO " + qualified + " AS t USING `" + batch_view + "` AS s "
            "ON t.id = s.id "
            "WHEN MATCHED AND s.event_at > t.event_at THEN "
            "UPDATE SET t.event_at = s.event_at, t.value = s.value "
            "WHEN NOT MATCHED THEN INSERT (id, event_at, value) "
            "VALUES (s.id, s.event_at, s.value)"
        ) if profile == "PIPELINE" else (
            "MERGE INTO " + qualified + " AS t USING `" + batch_view + "` AS s "
            "ON t.decision_id = s.decision_id "
            "WHEN NOT MATCHED THEN INSERT (decision_id, entity_id, decision_at, feature_value, available_at) "
            "VALUES (s.decision_id, s.entity_id, s.decision_at, s.feature_value, s.available_at)"
        )
        spark.sql(merge)
        first = _rows(spark, qualified, profile=profile)
        if first != expected_rows or (profile == "FE_PIT" and digest(first) != digest(expected_rows)):
            raise RuntimeError("MERGE_READBACK_MISMATCH")
        effect["first_merge_rows_sha256"] = digest(first)
        if profile == "FE_PIT":
            effect["first_delta_version"] = _delta_version(spark, qualified)
            effect["table_id"] = _delta_table_id(spark, qualified)
        effect["phase"] = "MERGED"
        spark.sql(merge)
        replay = _rows(spark, qualified, profile=profile)
        if (replay != expected_rows or replay != first or
                (profile == "FE_PIT" and
                 (digest(replay) != digest(expected_rows) or digest(replay) != digest(first)))):
            raise RuntimeError("MERGE_REPLAY_NOT_IDEMPOTENT")
        effect["replay_rows_sha256"] = digest(replay)
        if profile == "FE_PIT":
            effect["replay_delta_version"] = _delta_version(spark, qualified)
            if effect["replay_delta_version"] < effect["first_delta_version"]:
                raise RuntimeError("DELTA_VERSION_REGRESSED")
            _assert_fe_table_id(spark, qualified, effect["table_id"])
        effect["phase"] = "REPLAYED"
        if release_integrity(SKILL_DIR, REQUIRED_RELEASE_PATHS) != release:
            raise RuntimeError("RELEASE_CHANGED_DURING_EFFECT")
        _assert_owned(spark, qualified, auth, provenance)
        effect["ownership_checks"] += 1
        if profile == "FE_PIT":
            _assert_fe_table_id(spark, qualified, effect["table_id"])
        spark.sql("DROP TABLE " + qualified)
        cleaned = True
        effect["cleanup"] = "PASS"
        effect["table_absent_after_cleanup"] = spark.catalog.tableExists(auth["target_table"]) is False
        if effect["table_absent_after_cleanup"] is not True:
            raise RuntimeError("TABLE_STILL_EXISTS_AFTER_DROP")
        effect["phase"] = "CLEANED"
        effect["status"] = "PASS"
    except Exception as exc:
        effect["issues"].append(type(exc).__name__ + ":" + str(exc))
        if created and not cleaned and auth is not None and qualified is not None:
            try:
                _assert_owned(spark, qualified, auth, provenance)
                effect["ownership_checks"] += 1
                if profile == "FE_PIT":
                    _assert_fe_table_id(spark, qualified, effect["table_id"])
                spark.sql("DROP TABLE " + qualified)
                cleaned = True
                effect["cleanup"] = "PASS_AFTER_FAILURE"
                effect["table_absent_after_cleanup"] = spark.catalog.tableExists(auth["target_table"]) is False
            except Exception as cleanup_exc:
                effect["cleanup"] = "BLOCKED_OWNERSHIP_OR_DROP_UNKNOWN"
                effect["issues"].append("CLEANUP:" + type(cleanup_exc).__name__)
        if effect["create_attempted"] and not (cleaned and effect["table_absent_after_cleanup"] is True):
            effect["status"] = "UNKNOWN"
        else:
            effect["status"] = "BLOCKED"
    finally:
        for view in reversed(temp_views):
            try:
                if spark.catalog.dropTempView(view) is not True:
                    effect["issues"].append("TEMP_VIEW_CLEANUP_UNCONFIRMED")
            except Exception as exc:
                effect["issues"].append("TEMP_VIEW_CLEANUP:" + type(exc).__name__)
        if any(item.startswith("TEMP_VIEW_CLEANUP") for item in effect["issues"]):
            if effect["status"] == "PASS":
                effect["status"] = "BLOCKED"
    return effect


def execute(request: dict, expected_rows: list[dict], spark, authorization: dict,
            *, run_id: str, compute_payload: dict | None = None) -> dict:
    """Public Pipeline profile; the owned lifecycle is shared with the closed FE profile."""
    return _execute_owned(request, expected_rows, spark, authorization,
                          run_id=run_id, compute_payload=compute_payload)
