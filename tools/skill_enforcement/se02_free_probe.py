# Databricks notebook source
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

MARKER = "SE02_FREE_PROBE_V0_1"
SKILL = "hub-ml-eda-profissional"

DEFAULT_CONTEXT = {
    "local_sample_required": True,
    "tabular_preview_required": True,
    "numeric_columns": 4,
    "numeric_distributions_requested": True,
    "resolved_theme_selected": False,
    "visual_diagnostics_requested": True,
}


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


def _decision(payload: dict[str, Any], item_id: str) -> dict[str, Any]:
    for item in payload["resources"]:
        if item.get("item_id") == item_id:
            return item
    raise KeyError(item_id)


def _copy_preflight_fixture(source_root: Path, temp_root: Path) -> tuple[Path, Path]:
    assistant_root = temp_root / ".assistant"
    source_skill = source_root / "skills" / SKILL
    target_skill = assistant_root / "skills" / SKILL
    target_skill.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_skill, target_skill)

    contract_path = target_skill / "execution_contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    for resource in contract["resources"]:
        source_package = source_root.joinpath(*resource["module"].split("."))
        target_package = assistant_root.joinpath(*resource["module"].split("."))
        target_package.parent.mkdir(parents=True, exist_ok=True)
        if not target_package.exists():
            shutil.copytree(source_package, target_package)

    return assistant_root, contract_path


assistant_root = _resolve_assistant_root()
assistant_root_text = str(assistant_root)
if assistant_root_text not in sys.path:
    sys.path.insert(0, assistant_root_text)

from hub_scripts.skill_execution import run_preflight

contract_path = assistant_root / "skills" / SKILL / "execution_contract.json"

cases: dict[str, dict[str, Any]] = {}

p1 = run_preflight(
    contract_path,
    assistant_root=assistant_root,
    context=dict(DEFAULT_CONTEXT),
).to_dict()
cases["F02-P1"] = {
    "ok": (
        p1["status"] == "PASS"
        and not p1["blocking_issues"]
        and p1["writes_performed"] is False
    ),
    "status": p1["status"],
    "blocking_issues": p1["blocking_issues"],
    "writes_performed": p1["writes_performed"],
}

c1_context = dict(DEFAULT_CONTEXT, local_sample_required=False)
c1 = run_preflight(
    contract_path,
    assistant_root=assistant_root,
    context=c1_context,
).to_dict()
smart_sample = _decision(c1, "smart_sample")
cases["F02-C1"] = {
    "ok": (
        c1["status"] == "PASS"
        and smart_sample["applicable"] is False
        and smart_sample["resolved"] is None
    ),
    "status": c1["status"],
    "smart_sample": smart_sample,
    "writes_performed": c1["writes_performed"],
}

with tempfile.TemporaryDirectory(prefix="se02-free-probe-") as tmp:
    fixture_root, fixture_contract = _copy_preflight_fixture(
        assistant_root,
        Path(tmp),
    )
    shutil.rmtree(fixture_root / "hub_scripts" / "quick_profile")
    b1 = run_preflight(
        fixture_contract,
        assistant_root=fixture_root,
        context=dict(DEFAULT_CONTEXT),
    ).to_dict()

cases["F02-B1"] = {
    "ok": (
        b1["status"] == "BLOCKED"
        and any(issue.get("item_id") == "quick_profile" for issue in b1["blocking_issues"])
        and b1["writes_performed"] is False
    ),
    "status": b1["status"],
    "blocking_issues": b1["blocking_issues"],
    "writes_performed": b1["writes_performed"],
    "published_package_mutated": False,
}

payload = {
    "marker": MARKER,
    "status": "PASS" if all(case["ok"] for case in cases.values()) else "FAIL",
    "assistant_root": str(assistant_root),
    "cases": cases,
    "writes_performed": False,
}

print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

if payload["status"] != "PASS":
    raise AssertionError("SE02 Free probe reprovou; consulte o JSON acima")
