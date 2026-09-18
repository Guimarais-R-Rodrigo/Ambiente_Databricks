# Databricks notebook source
# MAGIC %md
# MAGIC # SE06 — correction probe
# MAGIC
# MAGIC Probe funcional da candidata corrigida após o early-stop P1.
# MAGIC Usa somente view temporária sintética e não realiza escrita persistente.

# COMMAND ----------

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import uuid
from pathlib import Path
from typing import Any

from pyspark.sql import SparkSession


MARKER = "SE06_CORRECTION_FREE_PROBE_V1"
SKILL = "hub-ml-eda-profissional"

HANDOFF_NO_PK = {
    "sources_snapshot": "temp view sintética SE06",
    "unit_keys_target": "1 linha por evento; PK não confirmada; target=N/A",
    "quality_risks": ["fixture sintético"],
    "feature_candidates_leakage": ["não aplicável no fixture"],
    "filters_sample": "sem filtro persistente; amostragem apenas interna dos helpers",
    "open_questions": [],
}


def _resolve_assistant_root() -> Path:
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    try:
        current_user = spark.sql("SELECT current_user() AS user").first()["user"]
    except Exception as exc:
        raise RuntimeError(
            f"não foi possível resolver o usuário atual do workspace: {exc}"
        ) from exc

    if not isinstance(current_user, str) or not current_user.strip():
        raise RuntimeError("current_user() retornou identidade vazia")

    candidate = Path("/Workspace/Users") / current_user.strip() / ".assistant"
    if not candidate.is_dir():
        raise RuntimeError(
            "raiz .assistant publicada não encontrada para o usuário atual"
        )
    return candidate


def _load_script(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar script: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def _protected_hashes(assistant_root: Path) -> dict[str, str]:
    manifest_path = assistant_root / "skills" / SKILL / "release_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return {
        artifact["path"]: _git_blob_sha1(assistant_root / artifact["path"])
        for artifact in manifest["artifacts"]
    }


def _decision(trace: dict[str, Any], item_id: str) -> dict[str, Any] | None:
    for item in trace.get("decisions", []):
        if item.get("item_type") == "resource" and item.get("item_id") == item_id:
            return item
    return None


assistant_root = _resolve_assistant_root()
assistant_root_text = str(assistant_root)
if assistant_root_text not in sys.path:
    sys.path.insert(0, assistant_root_text)

skill_dir = assistant_root / "skills" / SKILL
enforced = _load_script(skill_dir / "scripts" / "run_enforced.py", "sef_se06_corrected_enforced")
finalizer = _load_script(skill_dir / "scripts" / "postflight.py", "sef_se06_corrected_postflight")

before_hashes = _protected_hashes(assistant_root)

spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
view_name = f"se06_corrected_{uuid.uuid4().hex[:12]}"
spark.createDataFrame(
    [
        (1, 10.0),
        (2, 12.0),
        (3, 11.0),
        (4, 15.0),
    ],
    "id INT, valor DOUBLE",
).createOrReplaceTempView(view_name)

cases: dict[str, dict[str, Any]] = {}

try:
    # C01 — caso P1-like: contexto omitido e nenhuma PK inventada.
    minimal = enforced.run_enforced(
        view_name,
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    minimal_trace = minimal.get("trace", {})
    dq_decision = _decision(minimal_trace, "data_quality_check")
    finalized = finalizer.finalize_or_raise(
        minimal,
        HANDOFF_NO_PK,
        assistant_root=assistant_root,
    )
    verified = finalizer.verify_finalized(
        finalized,
        assistant_root=assistant_root,
    )
    cases["C01_minimal_context_no_fake_pk"] = {
        "ok": (
            minimal_trace.get("status") == "PASS"
            and minimal_trace.get("preflight_status") == "PASS"
            and minimal_trace.get("enforcement_status") == "PASS"
            and isinstance(dq_decision, dict)
            and dq_decision.get("applicable") is False
            and "data_quality_check" not in minimal_trace.get("resources_called", [])
            and minimal.get("completion", {}).get("status") == "PENDING_POSTFLIGHT"
            and finalized.get("completion", {}).get("authorized") is True
            and verified.get("status") == "VALID"
            and verified.get("completion_authorized") is True
        ),
        "trace_status": minimal_trace.get("status"),
        "preflight_status": minimal_trace.get("preflight_status"),
        "enforcement_status": minimal_trace.get("enforcement_status"),
        "data_quality_check_decision": dq_decision,
        "resources_called": minimal_trace.get("resources_called"),
        "resources_completed": minimal_trace.get("resources_completed"),
        "templates_loaded": minimal_trace.get("templates_loaded"),
        "postflight_status": finalized.get("postflight", {}).get("status"),
        "completion_authorized": finalized.get("completion", {}).get("authorized"),
        "verification_status": verified.get("status"),
    }

    # C02 — PK explícita mantém data_quality_check aplicável.
    with_pk = enforced.run_enforced(
        view_name,
        {"pk_columns": ["id"]},
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    with_pk_trace = with_pk.get("trace", {})
    with_pk_decision = _decision(with_pk_trace, "data_quality_check")
    cases["C02_explicit_pk_keeps_dq_applicable"] = {
        "ok": (
            with_pk_trace.get("enforcement_status") == "PASS"
            and isinstance(with_pk_decision, dict)
            and with_pk_decision.get("applicable") is True
            and "data_quality_check" in with_pk_trace.get("resources_completed", [])
        ),
        "decision": with_pk_decision,
        "resources_completed": with_pk_trace.get("resources_completed"),
    }

    # C03 — falha de entrada objetiva deve interromper; não devolver payload silencioso.
    strict_stopped = False
    strict_payload: dict[str, Any] = {}
    try:
        enforced.run_enforced(
            view_name,
            {"resolved_theme_selected": True},
            assistant_root=assistant_root,
            sample_fraction=1.0,
            resolved_theme=None,
        )
    except enforced.CanonicalExecutionBlocked as exc:
        strict_stopped = True
        strict_payload = exc.payload
    cases["C03_strict_block_stops_route"] = {
        "ok": (
            strict_stopped
            and strict_payload.get("trace", {}).get("enforcement_status") == "INCOMPLETE"
            and strict_payload.get("completion", {}).get("authorized") is False
        ),
        "strict_stopped": strict_stopped,
        "trace_status": strict_payload.get("trace", {}).get("status"),
        "enforcement_status": strict_payload.get("trace", {}).get("enforcement_status"),
        "completion": strict_payload.get("completion"),
    }

    # C04 — handoff incompleto deve falhar por exceção de finalização.
    rejected = False
    rejected_final: dict[str, Any] = {}
    bad_handoff = dict(HANDOFF_NO_PK)
    bad_handoff.pop("quality_risks")
    try:
        finalizer.finalize_or_raise(
            minimal,
            bad_handoff,
            assistant_root=assistant_root,
        )
    except finalizer.CompletionNotAuthorized as exc:
        rejected = True
        rejected_final = exc.final_payload
    cases["C04_finalize_or_raise_rejects_review"] = {
        "ok": (
            rejected
            and rejected_final.get("completion", {}).get("authorized") is False
            and rejected_final.get("postflight", {}).get("status") != "PASS"
        ),
        "rejected": rejected,
        "postflight_status": rejected_final.get("postflight", {}).get("status"),
        "completion": rejected_final.get("completion"),
    }
finally:
    spark.catalog.dropTempView(view_name)

after_hashes = _protected_hashes(assistant_root)
published_package_mutated = before_hashes != after_hashes

payload = {
    "marker": MARKER,
    "status": (
        "PASS"
        if all(item["ok"] for item in cases.values())
        and not published_package_mutated
        else "FAIL"
    ),
    "assistant_root": str(assistant_root),
    "cases": cases,
    "published_package_mutated": published_package_mutated,
    "persistent_writes_performed": False,
}

print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str))

if payload["status"] != "PASS":
    raise AssertionError("SE06 correction Free probe reprovou")
