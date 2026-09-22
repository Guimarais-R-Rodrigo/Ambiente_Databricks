# Databricks notebook source
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


MARKER = "SE05_FREE_PROBE_V1"
SKILL = "hub-ml-eda-profissional"
BASE_CONTEXT = {
    "local_sample_required": False,
    "tabular_preview_required": False,
    "numeric_distributions_requested": False,
    "resolved_theme_selected": False,
    "visual_diagnostics_requested": False,
    "pk_columns": ["id"],
}
HANDOFF = {
    "sources_snapshot": "temporary synthetic Spark view",
    "unit_keys_target": "1 linha por id; chave=id; target=N/A",
    "quality_risks": ["fixture sintético para homologação do gate L4"],
    "feature_candidates_leakage": ["não aplicável ao fixture"],
    "filters_sample": "sem filtros; sem amostra local adicional",
    "open_questions": [],
}

sys.dont_write_bytecode = True


def _current_databricks_user() -> str | None:
    try:
        return str(
            dbutils.notebook.entry_point.getDbutils()
            .notebook()
            .getContext()
            .userName()
            .get()
        )
    except Exception:
        return None


def _resolve_assistant_root() -> Path:
    candidates: list[Path] = []
    for base in (Path.cwd(), *Path.cwd().parents):
        candidate = base / ".assistant"
        if candidate.is_dir():
            candidates.append(candidate)

    user = _current_databricks_user()
    if user:
        candidate = Path("/Workspace/Users") / user / ".assistant"
        if candidate.is_dir():
            candidates.append(candidate)

    users_root = Path("/Workspace/Users")
    if users_root.is_dir():
        candidates.extend(path for path in users_root.glob("*/.assistant") if path.is_dir())

    unique: list[Path] = []
    seen: set[str] = set()
    for path in candidates:
        key = str(path.resolve())
        if key not in seen:
            unique.append(path)
            seen.add(key)

    if not unique:
        raise RuntimeError("nenhuma raiz .assistant publicada foi encontrada")

    if user:
        expected_parent = str((Path("/Workspace/Users") / user).resolve())
        for path in unique:
            if str(path.parent.resolve()) == expected_parent:
                return path

    if len(unique) == 1:
        return unique[0]

    raise RuntimeError(
        "mais de uma raiz .assistant encontrada e não foi possível determinar "
        f"a do usuário atual: {[str(path) for path in unique]}"
    )


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
    result: dict[str, str] = {}
    for artifact in manifest["artifacts"]:
        rel = artifact["path"]
        result[rel] = _git_blob_sha1(assistant_root / rel)
    return result


def _summary(final_payload: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    trace = final_payload.get("trace") or {}
    postflight = final_payload.get("postflight") or {}
    completion = final_payload.get("completion") or {}
    receipt = final_payload.get("receipt") or {}
    return {
        "trace_status": trace.get("status"),
        "enforcement_status": trace.get("enforcement_status"),
        "evidence_gaps": trace.get("evidence_gaps"),
        "receipt_present": isinstance(final_payload.get("receipt"), dict),
        "receipt_id": receipt.get("receipt_id") if isinstance(receipt, dict) else None,
        "postflight_status": postflight.get("status"),
        "postflight_id": postflight.get("postflight_id"),
        "completion_authorized": completion.get("authorized"),
        "completion_status": completion.get("status"),
        "verification_status": verification.get("status"),
        "verification_valid": verification.get("valid"),
        "verification_completion_authorized": verification.get("completion_authorized"),
        "completion_claim_consistent": verification.get("completion_claim_consistent"),
    }


assistant_root = _resolve_assistant_root()
assistant_root_text = str(assistant_root)
if assistant_root_text not in sys.path:
    sys.path.insert(0, assistant_root_text)

skill_dir = assistant_root / "skills" / SKILL
run_enforced = _load_script(skill_dir / "scripts" / "run_enforced.py", "sef_se05_free_enforced")
finalizer = _load_script(skill_dir / "scripts" / "postflight.py", "sef_se05_free_postflight")
core_runner = _load_script(skill_dir / "scripts" / "run.py", "sef_se05_free_core")

published_before = _protected_hashes(assistant_root)
spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
view_name = f"se05_free_probe_{uuid.uuid4().hex[:12]}"
probe_df = spark.createDataFrame(
    [
        (1, "A"),
        (2, "B"),
        (3, "A"),
        (4, "C"),
    ],
    "id INT, categoria STRING",
)
probe_df.createOrReplaceTempView(view_name)

cases: dict[str, dict[str, Any]] = {}

try:
    enforced = run_enforced.run_enforced(
        view_name,
        dict(BASE_CONTEXT),
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    finalized = finalizer.finalize(enforced, HANDOFF, assistant_root=assistant_root)
    verified = finalizer.verify_finalized(finalized, assistant_root=assistant_root)
    cases["P01_l4_happy_path"] = {
        "ok": (
            enforced.get("trace", {}).get("enforcement_status") == "PASS"
            and isinstance(enforced.get("receipt"), dict)
            and finalized.get("postflight", {}).get("status") == "PASS"
            and finalized.get("completion", {}).get("authorized") is True
            and verified.get("status") == "VALID"
            and verified.get("valid") is True
            and verified.get("completion_authorized") is True
            and verified.get("completion_claim_consistent") is True
        ),
        **_summary(finalized, verified),
    }

    core_only = core_runner.run(
        view_name,
        dict(BASE_CONTEXT),
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    core_finalized = finalizer.finalize(core_only, HANDOFF, assistant_root=assistant_root)
    core_verified = finalizer.verify_finalized(core_finalized, assistant_root=assistant_root)
    cases["P02_core_l3_cannot_finalize_l4"] = {
        "ok": (
            isinstance(core_only.get("receipt"), dict)
            and core_finalized.get("completion", {}).get("authorized") is False
            and core_finalized.get("postflight", {}).get("status") != "PASS"
            and core_verified.get("completion_authorized") is False
        ),
        **_summary(core_finalized, core_verified),
    }

    missing_pk_context = dict(BASE_CONTEXT)
    missing_pk_context.pop("pk_columns")
    missing_pk = run_enforced.run_enforced(
        view_name,
        missing_pk_context,
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    missing_pk_final = finalizer.finalize(missing_pk, HANDOFF, assistant_root=assistant_root)
    missing_pk_verified = finalizer.verify_finalized(missing_pk_final, assistant_root=assistant_root)
    cases["P03_missing_required_input_fails_closed"] = {
        "ok": (
            isinstance(missing_pk.get("receipt"), dict)
            and missing_pk.get("trace", {}).get("enforcement_status") == "INCOMPLETE"
            and missing_pk_final.get("completion", {}).get("authorized") is False
            and missing_pk_final.get("postflight", {}).get("status") == "FAIL"
        ),
        **_summary(missing_pk_final, missing_pk_verified),
    }

    incomplete_handoff = dict(HANDOFF)
    incomplete_handoff.pop("quality_risks")
    incomplete_final = finalizer.finalize(enforced, incomplete_handoff, assistant_root=assistant_root)
    incomplete_verified = finalizer.verify_finalized(incomplete_final, assistant_root=assistant_root)
    cases["P04_incomplete_handoff_not_completed"] = {
        "ok": (
            incomplete_final.get("postflight", {}).get("status") == "REVIEW"
            and incomplete_final.get("completion", {}).get("authorized") is False
            and incomplete_verified.get("completion_authorized") is False
        ),
        **_summary(incomplete_final, incomplete_verified),
    }

    tampered = copy.deepcopy(finalized)
    tampered["completion"] = {
        "authorized": False,
        "status": "NOT_COMPLETED",
        "reason": "tampered fixture",
    }
    tampered_verification = finalizer.verify_finalized(tampered, assistant_root=assistant_root)
    cases["P05_completion_claim_tamper_detected"] = {
        "ok": (
            tampered_verification.get("status") == "INVALID"
            and tampered_verification.get("valid") is False
            and tampered_verification.get("completion_authorized") is False
            and tampered_verification.get("completion_claim_consistent") is False
        ),
        "verification": tampered_verification,
    }
finally:
    spark.catalog.dropTempView(view_name)

published_after = _protected_hashes(assistant_root)
published_package_mutated = published_before != published_after
persistent_writes_performed = False

payload = {
    "marker": MARKER,
    "status": (
        "PASS"
        if all(case["ok"] for case in cases.values())
        and not published_package_mutated
        and not persistent_writes_performed
        else "FAIL"
    ),
    "assistant_root": str(assistant_root),
    "cases": cases,
    "published_package_mutated": published_package_mutated,
    "persistent_writes_performed": persistent_writes_performed,
}

print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str))

if payload["status"] != "PASS":
    raise AssertionError("SE05 Free probe reprovou; consulte o JSON acima")
