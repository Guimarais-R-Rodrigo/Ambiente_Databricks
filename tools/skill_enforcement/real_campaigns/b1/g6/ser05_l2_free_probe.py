# Databricks notebook source
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

MARKER = "SER_B1_G6_SER05_L2_FREE_PROBE_1"
SKILL = "hub-ml-cross-eda-ml"
QUALIFIED_SHA = "08c2a93c4c9dede1e759abe28c07242b4116f47e"
SER05_CONTEXTS = json.loads(r'''{"temporal":{"anchor":"anchor_snapshot","anchor_grain":"ONE_ROW_PER_ENTITY_DECISION","cardinality":"N:1","decision_at":"2026-01-10T00:00:00Z","entity_keys":["entity_id"],"null_key_policy":"REJECT","pit":"APPLICABLE","profile":"CONTEXT_ONLY_PILOT_V1","requested_effect":"NONE","schema_version":"SER05-CONTEXT-1","sources":[{"columns":["entity_id","reference_at","available_at"],"content_sha256":"94444ab59ced9bdfee79fc8ec48536354243cc000436bb2f10e355228e48f056","grain":"ONE_ROW_PER_ENTITY_DECISION","id":"anchor_snapshot","snapshot_id":"anchor_snapshot_synthetic_v1"},{"columns":["entity_id","reference_at","available_at"],"content_sha256":"ee1e053a125aed64b6d65664727da742764683266b2c6a146d332737a88261ed","grain":"ENTITY_SNAPSHOT","id":"attributes_snapshot","snapshot_id":"attributes_snapshot_synthetic_v1"}],"synthetic":true,"temporal":{"availability_column":"available_at","bitemporal":false,"boundary":"LE","lag_days":1,"lag_kind":"CONSTANT","reference_column":"reference_at","tie_break":"REJECT","timezone":"UTC"}},"static":{"anchor":"anchor_snapshot","anchor_grain":"ONE_ROW_PER_ENTITY_DECISION","cardinality":"N:1","decision_at":"2026-01-10T00:00:00Z","entity_keys":["entity_id"],"not_applicable_reason":"Synthetic static attribute declared invariant over the decision period.","null_key_policy":"REJECT","pit":"NOT_APPLICABLE","profile":"CONTEXT_ONLY_PILOT_V1","requested_effect":"NONE","schema_version":"SER05-CONTEXT-1","sources":[{"columns":["entity_id","reference_at","available_at"],"content_sha256":"94444ab59ced9bdfee79fc8ec48536354243cc000436bb2f10e355228e48f056","grain":"ONE_ROW_PER_ENTITY_DECISION","id":"anchor_snapshot","snapshot_id":"anchor_snapshot_synthetic_v1"},{"columns":["entity_id","reference_at","available_at"],"content_sha256":"ee1e053a125aed64b6d65664727da742764683266b2c6a146d332737a88261ed","grain":"ENTITY_SNAPSHOT","id":"attributes_snapshot","snapshot_id":"attributes_snapshot_synthetic_v1"}],"synthetic":true,"temporal":null}}''')
EXPECTED_RELEASE_BINDINGS = json.loads(r'''{"contract_git_blob_sha1":"1c23fdb8a4896a6a5cc94da3734ec0efaf61ca43","preflight_git_blob_sha1":"0717afa2561471ba97a39390f1c3462ecefc9bfc","temporal_owner_git_blob_sha1":"4f2f61fb3221a72d066cf415e49e15b5b6362f66"}''')
sys.dont_write_bytecode = True

def _current_databricks_user():
    try:
        return str(
            dbutils.notebook.entry_point.getDbutils()
            .notebook().getContext().userName().get()
        )
    except Exception:
        return None


def _resolve_assistant_root() -> Path:
    candidates = []
    for base in (Path.cwd(), *Path.cwd().parents):
        candidate = base / ".assistant"
        if candidate.is_dir():
            candidates.append(candidate)
    user = _current_databricks_user()
    if user:
        candidate = Path("/Workspace/Users") / user / ".assistant"
        if candidate.is_dir():
            candidates.append(candidate)
    unique = []
    seen = set()
    for path in candidates:
        key = str(path.resolve())
        if key not in seen:
            unique.append(path)
            seen.add(key)
    if not unique:
        raise RuntimeError("ASSISTANT_ROOT_NOT_FOUND")
    if user:
        expected_parent = str((Path("/Workspace/Users") / user).resolve())
        for path in unique:
            if str(path.parent.resolve()) == expected_parent:
                return path
    if len(unique) == 1:
        return unique[0]
    raise RuntimeError("ASSISTANT_ROOT_AMBIGUOUS")


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_UNAVAILABLE:" + str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _policy_entry(assistant_root: Path, skill: str):
    payload = json.loads(
        (assistant_root / "hub_padroes/skill_enforcement/policy.json").read_text(encoding="utf-8")
    )
    for row in payload.get("skills", []):
        if isinstance(row, dict) and row.get("skill") == skill:
            return row
    raise RuntimeError("POLICY_ENTRY_NOT_FOUND:" + skill)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_probe() -> dict:
    assistant_root = _resolve_assistant_root()
    skill_dir = assistant_root / "skills" / SKILL
    preflight_module = _load_module("_g6_ser05_preflight", skill_dir / "scripts/preflight.py")
    protected = [
        skill_dir / "execution_contract.json",
        skill_dir / "scripts/preflight.py",
        assistant_root / "hub_scripts/skill_execution/domain_context/__init__.py",
    ]
    before = {_sha256(path): str(index) for index, path in enumerate(protected)}
    cases = {}

    for label in ("temporal", "static"):
        context = copy.deepcopy(SER05_CONTEXTS[label])
        payload = preflight_module.preflight(context)
        verification = preflight_module.verify_preflight(payload, expected_context=context)
        cases[label + "_context"] = {
            "ok": (
                payload.get("status") == "PASS"
                and verification.get("valid") is True
                and payload.get("release_bindings") == EXPECTED_RELEASE_BINDINGS
                and payload.get("join_executed") is False
                and payload.get("coverage_measured") is False
                and payload.get("ml_readiness") == "NOT_EVALUATED"
                and payload.get("writes_performed") is False
                and payload.get("promotion_authorized") is False
            ),
            "status": payload.get("status"),
            "verification": verification,
            "release_bindings": payload.get("release_bindings"),
            "join_executed": payload.get("join_executed"),
            "coverage_measured": payload.get("coverage_measured"),
            "ml_readiness": payload.get("ml_readiness"),
        }

    negatives = []
    for mutation in ("VARIABLE_LAG", "BITEMPORAL", "TIMEZONE"):
        context = copy.deepcopy(SER05_CONTEXTS["temporal"])
        if mutation == "VARIABLE_LAG":
            context["temporal"]["lag_kind"] = "VARIABLE"
        elif mutation == "BITEMPORAL":
            context["temporal"]["bitemporal"] = True
        else:
            context["temporal"]["timezone"] = "America/Sao_Paulo"
        payload = preflight_module.preflight(context)
        negatives.append({
            "mutation": mutation,
            "blocked": payload.get("status") == "BLOCKED",
            "issues": payload.get("issues"),
        })
    cases["negative_temporal_limits"] = {
        "ok": all(x["blocked"] for x in negatives),
        "checks": negatives,
    }

    after = {_sha256(path): str(index) for index, path in enumerate(protected)}
    cases["protected_bytes_unchanged"] = {
        "ok": before == after,
        "count": len(protected),
    }

    policy = _policy_entry(assistant_root, SKILL)
    cases["policy_pre_promotion"] = {
        "ok": (
            policy.get("current_level") == "L0"
            and policy.get("target_level") == "L4"
            and policy.get("rollout_mode") == "audit"
        ),
        "current_level": policy.get("current_level"),
        "target_level": policy.get("target_level"),
        "rollout_mode": policy.get("rollout_mode"),
    }

    result = {
        "marker": MARKER,
        "qualified_sha": QUALIFIED_SHA,
        "status": "PASS" if all(x["ok"] for x in cases.values()) else "FAIL",
        "skill": SKILL,
        "scope": "L2_CONTEXT_ONLY_PILOT_V1",
        "cases": cases,
        "persistent_writes_performed": False,
        "join_executed": False,
        "coverage_measured": False,
        "ml_readiness": "NOT_EVALUATED",
        "promotion_authorized": False,
    }
    return result


def main() -> int:
    payload = run_probe()
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
