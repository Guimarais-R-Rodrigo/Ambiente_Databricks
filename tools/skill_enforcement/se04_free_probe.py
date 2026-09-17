# Databricks notebook source
from __future__ import annotations

import copy
import hashlib
import importlib
import importlib.util
import json
import shutil
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

from pyspark.sql import SparkSession


MARKER = "SE04_FREE_PROBE_V1"
SKILL = "hub-ml-eda-profissional"
BASE_CONTEXT = {
    "local_sample_required": True,
    "tabular_preview_required": True,
    "numeric_distributions_requested": True,
    "resolved_theme_selected": False,
    "visual_diagnostics_requested": True,
}

# Evita resíduos __pycache__ dentro do pacote publicado durante o probe.
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


def _load_runner(assistant_root: Path):
    path = assistant_root / "skills" / SKILL / "scripts" / "run.py"
    spec = importlib.util.spec_from_file_location("sef_se04_free_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar runner canônico: {path}")
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
        path = assistant_root / rel
        result[rel] = _git_blob_sha1(path)
    return result


def _copy_integrity_fixture(source_root: Path, target_root: Path) -> Path:
    assistant_root = target_root / ".assistant"

    source_skill = source_root / "skills" / SKILL
    target_skill = assistant_root / "skills" / SKILL
    target_skill.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_skill, target_skill)

    for package in (
        ("hub_scripts", "skill_execution"),
        ("hub_scripts", "quick_profile"),
    ):
        source = source_root.joinpath(*package)
        target = assistant_root.joinpath(*package)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)

    return assistant_root


def _verification_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": payload.get("status"),
        "valid": payload.get("valid"),
        "issues": payload.get("issues"),
        "receipt_version": payload.get("receipt_version"),
        "receipt_id": payload.get("receipt_id"),
        "run_id": payload.get("run_id"),
        "canonical_compliance": payload.get("canonical_compliance"),
    }


def _trace_summary(payload: dict[str, Any]) -> dict[str, Any]:
    trace = payload.get("trace") or {}
    receipt = payload.get("receipt")
    return {
        "status": trace.get("status"),
        "run_id": trace.get("run_id"),
        "preflight_status": trace.get("preflight_status"),
        "resources_called": trace.get("resources_called"),
        "resources_completed": trace.get("resources_completed"),
        "fallback_used": trace.get("fallback_used"),
        "writes_performed": trace.get("writes_performed"),
        "blocking_issues": trace.get("blocking_issues"),
        "context_provenance": trace.get("context_provenance"),
        "receipt_present": isinstance(receipt, dict),
        "receipt_id": receipt.get("receipt_id") if isinstance(receipt, dict) else None,
    }


assistant_root = _resolve_assistant_root()
assistant_root_text = str(assistant_root)
if assistant_root_text not in sys.path:
    sys.path.insert(0, assistant_root_text)

runner = _load_runner(assistant_root)
published_before = _protected_hashes(assistant_root)

spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
view_name = f"se04_free_probe_{uuid.uuid4().hex[:12]}"
probe_df = spark.createDataFrame(
    [
        (1, 10.0, 100.0, "A"),
        (2, 20.0, 200.0, "B"),
        (3, None, 300.0, "A"),
        (4, 40.0, 400.0, "C"),
    ],
    "id INT, valor_a DOUBLE, valor_b DOUBLE, categoria STRING",
)
probe_df.createOrReplaceTempView(view_name)

cases: dict[str, dict[str, Any]] = {}

try:
    canonical = runner.run(
        view_name,
        dict(BASE_CONTEXT),
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    canonical_trace = canonical["trace"]
    canonical_verification = runner.verify_receipt(
        canonical,
        expected_run_id=canonical_trace.get("run_id"),
        assistant_root=assistant_root,
    )
    cases["R01_valid_receipt"] = {
        "ok": (
            canonical_trace.get("status") == "PASS"
            and canonical_trace.get("preflight_status") == "PASS"
            and canonical_trace.get("resources_called") == [runner.PROTECTED_PRIMITIVE_ID]
            and canonical_trace.get("resources_completed") == [runner.PROTECTED_PRIMITIVE_ID]
            and isinstance(canonical.get("receipt"), dict)
            and canonical_verification.get("status") == "VALID"
            and canonical_verification.get("valid") is True
        ),
        **_trace_summary(canonical),
        "verification": _verification_summary(canonical_verification),
    }

    tampered_receipt = copy.deepcopy(canonical)
    tampered_receipt["receipt"]["writes_performed"] = True
    tampered_receipt_verification = runner.verify_receipt(
        tampered_receipt,
        assistant_root=assistant_root,
    )
    cases["R05_tampered_receipt"] = {
        "ok": tampered_receipt_verification.get("status") == "INVALID",
        "verification": _verification_summary(tampered_receipt_verification),
    }

    tampered_output = copy.deepcopy(canonical)
    tampered_output["result"] = {"tampered": True}
    tampered_output_verification = runner.verify_receipt(
        tampered_output,
        assistant_root=assistant_root,
    )
    cases["R06_tampered_output"] = {
        "ok": tampered_output_verification.get("status") == "INCOMPATIBLE",
        "verification": _verification_summary(tampered_output_verification),
    }

    current = runner.run(
        view_name,
        dict(BASE_CONTEXT),
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    stale_verification = runner.verify_receipt(
        canonical,
        expected_run_id=current["trace"].get("run_id"),
        assistant_root=assistant_root,
    )
    cases["R07_stale_receipt"] = {
        "ok": (
            current["trace"].get("run_id") != canonical_trace.get("run_id")
            and stale_verification.get("status") == "STALE_REPLAYED"
        ),
        "verification": _verification_summary(stale_verification),
    }

    manual_output = {"result": copy.deepcopy(canonical.get("result"))}
    manual_verification = runner.verify_receipt(
        manual_output,
        assistant_root=assistant_root,
    )
    cases["R02_R04_manual_without_receipt"] = {
        "ok": (
            manual_verification.get("status") == "ABSENT"
            and manual_verification.get("valid") is False
        ),
        "verification": _verification_summary(manual_verification),
    }

    quick_profile_module = importlib.import_module("hub_scripts.quick_profile")
    direct_result = quick_profile_module.quick_profile(
        view_name,
        sample_fraction=1.0,
        max_categories=20,
        seed=42,
    )
    direct_verification = runner.verify_receipt(
        {"result": direct_result},
        assistant_root=assistant_root,
    )
    cases["R03_direct_primitive_without_receipt"] = {
        "ok": direct_verification.get("status") == "ABSENT",
        "verification": _verification_summary(direct_verification),
    }

    with tempfile.TemporaryDirectory(prefix="se04-free-r11-") as tmp:
        fixture_root = _copy_integrity_fixture(assistant_root, Path(tmp))
        receipt_engine = fixture_root / "hub_scripts" / "skill_execution" / "receipt.py"
        receipt_engine.write_text(
            receipt_engine.read_text(encoding="utf-8") + "\n# tampered fixture\n",
            encoding="utf-8",
        )
        release_broken = runner.run(
            view_name,
            dict(BASE_CONTEXT),
            assistant_root=fixture_root,
            sample_fraction=1.0,
        )
    cases["R11_release_integrity_broken"] = {
        "ok": (
            release_broken["trace"].get("status") == "BLOCKED"
            and release_broken.get("receipt") is None
            and any(
                issue.get("code") == "RELEASE_INTEGRITY_MISMATCH"
                for issue in release_broken["trace"].get("blocking_issues", [])
            )
        ),
        **_trace_summary(release_broken),
        "fixture_only": True,
    }

    conflict = runner.run(
        view_name,
        dict(BASE_CONTEXT, numeric_columns=0),
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    conflict_numeric = conflict["trace"].get("context_provenance", {}).get("numeric_columns", {})
    cases["R10_provenance_conflict"] = {
        "ok": (
            conflict["trace"].get("status") == "BLOCKED"
            and conflict.get("receipt") is None
            and conflict_numeric.get("source") == "runtime_derived"
            and conflict_numeric.get("conflict") is True
            and not conflict["trace"].get("resources_called")
        ),
        **_trace_summary(conflict),
    }

    primitive_failure = runner.run(
        view_name,
        dict(BASE_CONTEXT),
        assistant_root=assistant_root,
        sample_fraction=0.0,
    )
    cases["R12_primitive_failure_no_fallback"] = {
        "ok": (
            primitive_failure["trace"].get("status") == "FAIL"
            and primitive_failure.get("receipt") is None
            and primitive_failure["trace"].get("fallback_used") is False
            and primitive_failure["trace"].get("resources_called") == [runner.PROTECTED_PRIMITIVE_ID]
            and primitive_failure["trace"].get("resources_completed") == []
            and any(
                issue.get("code") == "REQUIRED_PRIMITIVE_FAILED"
                for issue in primitive_failure["trace"].get("blocking_issues", [])
            )
        ),
        **_trace_summary(primitive_failure),
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
        if (
            all(case["ok"] for case in cases.values())
            and not published_package_mutated
            and not persistent_writes_performed
        )
        else "FAIL"
    ),
    "assistant_root": str(assistant_root),
    "cases": cases,
    "published_package_mutated": published_package_mutated,
    "persistent_writes_performed": persistent_writes_performed,
}

print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str))

if payload["status"] != "PASS":
    raise AssertionError("SE04 Free probe reprovou; consulte o JSON acima")
