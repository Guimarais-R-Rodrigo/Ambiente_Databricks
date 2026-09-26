# Databricks notebook source
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

from pyspark.sql import SparkSession


MARKER = "SE03_FREE_PROBE_V0_1"
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
    spec = importlib.util.spec_from_file_location("sef_se03_free_runner", path)
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


def _case_summary(payload: dict[str, Any]) -> dict[str, Any]:
    trace = payload["trace"]
    return {
        "status": trace.get("status"),
        "run_id": trace.get("run_id"),
        "preflight_status": trace.get("preflight_status"),
        "resources_called": trace.get("resources_called"),
        "fallback_used": trace.get("fallback_used"),
        "writes_performed": trace.get("writes_performed"),
        "blocking_issues": trace.get("blocking_issues"),
        "context_provenance": trace.get("context_provenance"),
        "output_digest": trace.get("output_digest"),
    }


assistant_root = _resolve_assistant_root()
assistant_root_text = str(assistant_root)
if assistant_root_text not in sys.path:
    sys.path.insert(0, assistant_root_text)

runner = _load_runner(assistant_root)
published_before = _protected_hashes(assistant_root)

spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
view_name = f"se03_free_probe_{uuid.uuid4().hex[:12]}"
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
    e01 = runner.run(
        view_name,
        dict(BASE_CONTEXT),
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    e01_trace = e01["trace"]
    e01_numeric = e01_trace.get("context_provenance", {}).get("numeric_columns", {})
    cases["E01"] = {
        "ok": (
            e01_trace.get("status") == "PASS"
            and e01_trace.get("preflight_status") == "PASS"
            and e01_numeric.get("source") == "runtime_derived"
            and e01_numeric.get("value") == 3
            and e01_trace.get("resources_called") == [runner.PROTECTED_PRIMITIVE_ID]
            and runner.is_canonically_compliant(
                e01,
                expected_run_id=e01_trace.get("run_id"),
            )
        ),
        **_case_summary(e01),
    }

    with tempfile.TemporaryDirectory(prefix="se03-free-e04-") as tmp:
        fixture_root = _copy_integrity_fixture(assistant_root, Path(tmp))
        shutil.rmtree(fixture_root / "hub_scripts" / "quick_profile")
        e04 = runner.run(
            view_name,
            dict(BASE_CONTEXT),
            assistant_root=fixture_root,
            sample_fraction=1.0,
        )
    e04_trace = e04["trace"]
    cases["E04"] = {
        "ok": (
            e04_trace.get("status") == "BLOCKED"
            and e04_trace.get("preflight_status") == "NOT_RUN"
            and any(
                issue.get("code") == "RELEASE_INTEGRITY_MISMATCH"
                for issue in e04_trace.get("blocking_issues", [])
            )
            and not e04_trace.get("resources_called")
        ),
        **_case_summary(e04),
        "fixture_only": True,
    }

    e06 = runner.run(
        view_name,
        dict(BASE_CONTEXT),
        assistant_root=assistant_root,
        sample_fraction=0.0,
    )
    e06_trace = e06["trace"]
    cases["E06"] = {
        "ok": (
            e06_trace.get("status") == "FAIL"
            and e06_trace.get("preflight_status") == "PASS"
            and e06_trace.get("fallback_used") is False
            and e06_trace.get("resources_called") == [runner.PROTECTED_PRIMITIVE_ID]
            and any(
                issue.get("code") == "REQUIRED_PRIMITIVE_FAILED"
                for issue in e06_trace.get("blocking_issues", [])
            )
        ),
        **_case_summary(e06),
    }

    e10_context = dict(BASE_CONTEXT, numeric_columns=0)
    e10 = runner.run(
        view_name,
        e10_context,
        assistant_root=assistant_root,
        sample_fraction=1.0,
    )
    e10_trace = e10["trace"]
    e10_numeric = e10_trace.get("context_provenance", {}).get("numeric_columns", {})
    cases["E10"] = {
        "ok": (
            e10_trace.get("status") == "BLOCKED"
            and e10_trace.get("preflight_status") == "NOT_RUN"
            and e10_numeric.get("source") == "runtime_derived"
            and e10_numeric.get("value") == 3
            and e10_numeric.get("declared_value") == 0
            and e10_numeric.get("conflict") is True
            and any(
                issue.get("code") == "CONTEXT_PROVENANCE_CONFLICT"
                for issue in e10_trace.get("blocking_issues", [])
            )
            and not e10_trace.get("resources_called")
        ),
        **_case_summary(e10),
    }
finally:
    spark.catalog.dropTempView(view_name)

published_after = _protected_hashes(assistant_root)
published_package_mutated = published_before != published_after

payload = {
    "marker": MARKER,
    "status": (
        "PASS"
        if all(case["ok"] for case in cases.values()) and not published_package_mutated
        else "FAIL"
    ),
    "assistant_root": str(assistant_root),
    "cases": cases,
    "published_package_mutated": published_package_mutated,
    "persistent_writes_performed": False,
}

print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str))

if payload["status"] != "PASS":
    raise AssertionError("SE03 Free probe reprovou; consulte o JSON acima")
