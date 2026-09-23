# Databricks notebook source
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Mapping

MARKER = "SER01_A4_FREE_PROBE_V1"
SKILL = "hub-ml-criar-objeto"
SURFACE = "object_validation"
RECEIPT_VERSION = "SER01-OBJECT-VALIDATION-RECEIPT-1"
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


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar módulo: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
        return module
    finally:
        sys.modules.pop(name, None)


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def _manifest_state(assistant_root: Path) -> tuple[dict[str, str], list[str]]:
    manifest_path = assistant_root / "skills" / SKILL / "release_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    issues: list[str] = []
    observed: dict[str, str] = {}
    if manifest.get("manifest_version") != "0.1" or manifest.get("skill") != SKILL:
        issues.append("RELEASE_MANIFEST_INVALID")
    for item in manifest.get("artifacts", []):
        if not isinstance(item, Mapping) or not isinstance(item.get("path"), str):
            issues.append("RELEASE_ARTIFACT_INVALID")
            continue
        rel = item["path"]
        target = assistant_root / rel
        if not target.is_file():
            issues.append("RELEASE_ARTIFACT_MISSING:" + rel)
            continue
        actual = _git_blob_sha1(target)
        observed[rel] = actual
        if actual != item.get("git_blob_sha1"):
            issues.append("RELEASE_ARTIFACT_HASH_MISMATCH:" + rel)
    return observed, issues


def _policy_entry(assistant_root: Path) -> Mapping[str, Any]:
    policy = json.loads(
        (assistant_root / "hub_padroes" / "skill_enforcement" / "policy.json")
        .read_text(encoding="utf-8")
    )
    for item in policy.get("skills", []):
        if isinstance(item, Mapping) and item.get("skill") == SKILL:
            return item
    raise RuntimeError("policy da skill não encontrada")


def _synthetic_record(verifier) -> dict[str, Any]:
    base_sha = "a" * 40
    path = "hub_lab/ser01_a4_fixture.py"
    content = "# Databricks notebook source\n# Fixture sintética A4; não é execução repo-side.\n".encode("utf-8")
    binding = {
        "operation": "create",
        "object_type": "notebook",
        "destination_relative": path,
        "grouped": False,
        "files": [{
            "path": path,
            "sha256": hashlib.sha256(content).hexdigest(),
            "size": len(content),
        }],
        "candidate_sha256": hashlib.sha256(
            b"SER01_A4_FREE_FIXTURE_INTEGRITY_ONLY"
        ).hexdigest(),
        "base_sha": base_sha,
    }
    commands = [
        "identity_before", "status_before", "history", "preflight",
        "baseline_validator", "clone", "checkout", "stage", "validator",
        "overlay_head", "overlay_index", "overlay_diff", "overlay_untracked",
        "identity_after", "status_after",
    ]
    checks = [
        "destination_matches_preflight", "canonical_validator",
        "overlay_head_preserved", "overlay_index_exact",
        "overlay_no_other_changes", "overlay_bytes_exact", "original_preserved",
    ]
    record: dict[str, Any] = {
        "record_version": "SER01-LOCAL-VALIDATION-1",
        "run_id": "ser01-a4-free-fixture",
        "status": "PASS",
        "issues": [],
        "binding": binding,
        "host": {"system": "FIXTURE", "release": "synthetic", "python": "synthetic"},
        "writes_performed_in_original": False,
        "homologated": False,
        "runtime_validation": "NOT_RUN",
        "execution_authenticated": False,
        "policy_promotion_authorized": False,
        "scope": "CREATE_PACKAGE_LOCAL_STRUCTURAL_VALIDATION_ONLY",
        "original_before": {"head": base_sha, "status": ""},
        "original_after": {"head": base_sha, "status": ""},
        "commands": [
            {"name": name, "exit_code": 0, "process_cleanup": "COMPLETE", "command_started": True}
            for name in commands
        ],
        "checks": [{"name": name, "status": "PASS"} for name in checks],
    }
    record["record_id"] = "ser01v1:" + verifier.digest(record)
    return record


assistant_root = _resolve_assistant_root()
skill_dir = assistant_root / "skills" / SKILL
verifier_path = skill_dir / "scripts" / "object_validation.py"
verifier = _load_module("ser01_a4_free_verifier", verifier_path)

published_before, before_issues = _manifest_state(assistant_root)
contract = json.loads((skill_dir / "execution_contract.json").read_text(encoding="utf-8"))
skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
policy = _policy_entry(assistant_root)
ov = (((contract.get("metadata") or {}).get("se07") or {}).get("object_validation_contract") or {})
surfaces = {
    item.get("id"): item
    for item in policy.get("protected_surfaces", [])
    if isinstance(item, Mapping)
}
surface = surfaces.get(SURFACE) or {}

record = _synthetic_record(verifier)
receipt = verifier.build_receipt(record)
if not isinstance(receipt, dict):
    raise AssertionError("fixture sintética não conseguiu produzir Receipt de integridade")

binding = record["binding"]
valid = verifier.verify_receipt(
    receipt,
    local_record=record,
    expected_run_id=record["run_id"],
    expected_base_sha=binding["base_sha"],
    expected_candidate_sha256=binding["candidate_sha256"],
)
alone = verifier.verify_receipt(
    receipt,
    expected_run_id=record["run_id"],
    expected_base_sha=binding["base_sha"],
    expected_candidate_sha256=binding["candidate_sha256"],
)
missing = verifier.verify_receipt(None, local_record=record)
tampered = copy.deepcopy(receipt)
tampered["claims"]["runtime_validation"] = "PASS"
tampered_check = verifier.verify_receipt(
    tampered,
    local_record=record,
    expected_run_id=record["run_id"],
    expected_base_sha=binding["base_sha"],
    expected_candidate_sha256=binding["candidate_sha256"],
)
replayed = verifier.verify_receipt(
    receipt,
    local_record=record,
    expected_run_id="another-run",
    expected_base_sha="b" * 40,
    expected_candidate_sha256="c" * 64,
)

cases: dict[str, dict[str, Any]] = {}

cases["F01_release_and_route_contract"] = {
    "ok": (
        not before_issues
        and ov.get("protected_surface") == SURFACE
        and ov.get("route") == "repo_side_local_structural_validation"
        and ov.get("producer_entrypoint")
            == "tools/skill_enforcement/ser01_object_validation.py::validate_package"
        and ov.get("verifier_entrypoint") == "scripts/object_validation.py::verify_receipt"
        and ov.get("receipt_version") == RECEIPT_VERSION
        and ov.get("workspace_without_repo_checkout") == "NOT_AVAILABLE"
        and ov.get("missing_or_invalid_receipt") == "BLOCK_L3_READY_CLAIM"
        and ov.get("apply_authorized_by_receipt") is False
        and "NOT_AVAILABLE" in skill_text
        and "Sem Receipt válido" in skill_text
        and not any(
            key == "tools/skill_enforcement/ser01_object_validation.py"
            for key in published_before
        )
    ),
    "manifest_issues": before_issues,
    "object_validation_contract": ov,
    "producer_is_published_artifact": any(
        key == "tools/skill_enforcement/ser01_object_validation.py"
        for key in published_before
    ),
}

cases["F02_fixture_receipt_with_record"] = {
    "ok": (
        valid.get("valid") is True
        and valid.get("verification_scope") == "DOMAIN_RECEIPT_INTEGRITY_ONLY"
        and valid.get("execution_reverified") is False
        and valid.get("human_authority_authenticated") is False
        and valid.get("policy_promotion_authorized") is False
        and receipt.get("claims") == {
            "structural_validation": "PASS",
            "runtime_validation": "NOT_RUN",
            "writes_performed_in_original": False,
            "execution_authenticated": False,
            "human_authority_authenticated": False,
            "policy_promotion_authorized": False,
            "homologated": False,
        }
    ),
    "fixture_only": True,
    "execution_proof": False,
    "verification": valid,
    "receipt_claims": receipt.get("claims"),
}

cases["F03_receipt_without_record"] = {
    "ok": (
        alone.get("valid") is False
        and "LOCAL_RECORD_REQUIRED" in alone.get("issues", [])
    ),
    "verification": alone,
}

cases["F04_missing_receipt"] = {
    "ok": (
        missing.get("valid") is False
        and "RECEIPT_NOT_MAPPING" in missing.get("issues", [])
    ),
    "verification": missing,
}

cases["F05_tamper_and_replay"] = {
    "ok": (
        tampered_check.get("valid") is False
        and replayed.get("valid") is False
        and any(
            issue in replayed.get("issues", [])
            for issue in ("RUN_BINDING_MISMATCH", "BASE_BINDING_MISMATCH", "CANDIDATE_BINDING_MISMATCH")
        )
    ),
    "tampered": tampered_check,
    "replayed": replayed,
}

cases["F06_policy_remains_pre_promotion"] = {
    "ok": (
        policy.get("current_level") == "L2"
        and policy.get("target_level") == "L3"
        and policy.get("rollout_mode") == "audit"
        and surface.get("level") == "L3"
        and surface.get("evidence") == "receipt"
    ),
    "current_level": policy.get("current_level"),
    "target_level": policy.get("target_level"),
    "rollout_mode": policy.get("rollout_mode"),
    "surface": surface,
}

published_after, after_issues = _manifest_state(assistant_root)
cases["F07_published_package_unchanged"] = {
    "ok": (
        not after_issues
        and published_before == published_after
    ),
    "manifest_issues_after": after_issues,
    "published_package_mutated": published_before != published_after,
}

payload = {
    "marker": MARKER,
    "status": "PASS" if all(case["ok"] for case in cases.values()) else "FAIL",
    "assistant_root": str(assistant_root),
    "skill": SKILL,
    "protected_surface": SURFACE,
    "fixture_scope": "INTEGRITY_ONLY_NOT_EXECUTION_PROOF",
    "cases": cases,
    "persistent_writes_performed": False,
    "published_package_mutated": published_before != published_after,
}

print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

if payload["status"] != "PASS":
    raise AssertionError("SER01 A4 Free probe reprovou; consulte o JSON acima")
