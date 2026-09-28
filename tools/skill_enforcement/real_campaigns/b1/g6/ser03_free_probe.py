# Databricks notebook source
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

MARKER = "SER_B1_G6_SER03_FREE_PROBE_1"
SKILL = "hub-ml-analise-safra"
QUALIFIED_SHA = "08c2a93c4c9dede1e759abe28c07242b4116f47e"
SER03_CASES = json.loads(r'''{"cumulative":{"request":{"absence_policy":"MISSING_ROW_NOT_ZERO","cohort_roster":[{"id":"a1","originated_at":"2026-01-01T00:00:00Z"},{"id":"a2","originated_at":"2026-01-01T00:00:00Z"},{"id":"b1","originated_at":"2026-02-01T00:00:00Z"},{"id":"b2","originated_at":"2026-02-01T00:00:00Z"}],"cutoff":"2026-03-01T00:00:00Z","denominator":"MOB0_UNIQUE_IDS_FIXED_PER_COHORT","duplicate_policy":"REJECT","estimand":"BINARY_CUMULATIVE_INCIDENCE","max_mob":2,"periodicity":"MONTH","population_id":"synthetic-VF-F01-CUMULATIVE","profile":"MONTHLY_BINARY_PILOT_V1","requested_effect":"NONE","rows":[{"id":"a1","mob":0,"observed_at":"2026-01-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a2","mob":0,"observed_at":"2026-01-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a1","mob":1,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":1},{"id":"a2","mob":1,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a1","mob":2,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":1},{"id":"b1","mob":0,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":0},{"id":"b2","mob":0,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":1},{"id":"b1","mob":1,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":0},{"id":"b2","mob":1,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":1}],"schema_version":"SER03-REQUEST-1","semantic_mode":"CUMULATIVE","synthetic":true},"expected_table":[{"cobertura_observada":1,"mob":0,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":0,"safra":"2026-01","taxa":0,"taxa_acumulada":0},{"cobertura_observada":1,"mob":1,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-01","taxa":0.5,"taxa_acumulada":0.5},{"cobertura_observada":0.5,"mob":2,"n_contratos_observados":1,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-01","taxa":null,"taxa_acumulada":null},{"cobertura_observada":1,"mob":0,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-02","taxa":0.5,"taxa_acumulada":0.5},{"cobertura_observada":1,"mob":1,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-02","taxa":0.5,"taxa_acumulada":0.5}],"run_id":"B1-G6-FREE-SER03-CUMULATIVE"},"event":{"request":{"absence_policy":"MISSING_ROW_NOT_ZERO","cohort_roster":[{"id":"a1","originated_at":"2026-01-01T00:00:00Z"},{"id":"a2","originated_at":"2026-01-01T00:00:00Z"},{"id":"b1","originated_at":"2026-02-01T00:00:00Z"},{"id":"b2","originated_at":"2026-02-01T00:00:00Z"}],"cutoff":"2026-03-01T00:00:00Z","denominator":"MOB0_UNIQUE_IDS_FIXED_PER_COHORT","duplicate_policy":"REJECT","estimand":"BINARY_CUMULATIVE_INCIDENCE","max_mob":2,"periodicity":"MONTH","population_id":"synthetic-VF-F01-EVENT","profile":"MONTHLY_BINARY_PILOT_V1","requested_effect":"NONE","rows":[{"id":"a1","mob":0,"observed_at":"2026-01-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a2","mob":0,"observed_at":"2026-01-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a1","mob":1,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":1},{"id":"a2","mob":1,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"a1","mob":2,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-01-01T00:00:00Z","target":0},{"id":"b1","mob":0,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":0},{"id":"b2","mob":0,"observed_at":"2026-02-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":1},{"id":"b1","mob":1,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":0},{"id":"b2","mob":1,"observed_at":"2026-03-01T00:00:00Z","originated_at":"2026-02-01T00:00:00Z","target":0}],"schema_version":"SER03-REQUEST-1","semantic_mode":"EVENT","synthetic":true},"expected_table":[{"cobertura_observada":1,"mob":0,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":0,"safra":"2026-01","taxa":0,"taxa_acumulada":0},{"cobertura_observada":1,"mob":1,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-01","taxa":0.5,"taxa_acumulada":0.5},{"cobertura_observada":0.5,"mob":2,"n_contratos_observados":1,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-01","taxa":null,"taxa_acumulada":null},{"cobertura_observada":1,"mob":0,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-02","taxa":0.5,"taxa_acumulada":0.5},{"cobertura_observada":1,"mob":1,"n_contratos_observados":2,"n_contratos_safra":2,"n_eventos_acumulados":1,"safra":"2026-02","taxa":0.5,"taxa_acumulada":0.5}],"run_id":"B1-G6-FREE-SER03-EVENT"}}''')
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


def run_probe() -> dict:
    assistant_root = _resolve_assistant_root()
    skill_dir = assistant_root / "skills" / SKILL
    runner = _load_module("_g6_ser03_runner", skill_dir / "scripts/run.py")
    verifier = _load_module("_g6_ser03_verifier", skill_dir / "scripts/verify.py")
    before = runner.release_integrity(skill_dir, runner.REQUIRED_RELEASE_PATHS)
    cases = {}

    for label in ("cumulative", "event"):
        row = SER03_CASES[label]
        payload = runner.run(copy.deepcopy(row["request"]), run_id=row["run_id"])
        verification = verifier.verify(
            payload,
            expected_request=row["request"],
            expected_run_id=row["run_id"],
            expected_table=row["expected_table"],
        )
        incomplete_rows = [
            x for x in (payload.get("result") or {}).get("table", [])
            if x.get("n_contratos_observados") != x.get("n_contratos_safra")
        ]
        cases[label + "_real_core"] = {
            "ok": (
                payload.get("status") == "PASS"
                and verification.get("valid") is True
                and payload.get("receipt") is not None
                and (payload.get("result") or {}).get("promotion_authorized") is False
                and (payload.get("result") or {}).get("business_readiness") == "NOT_EVALUATED"
                and (payload.get("trace") or {}).get("writes_performed") is False
                and all(x.get("taxa") is None and x.get("taxa_acumulada") is None for x in incomplete_rows)
            ),
            "status": payload.get("status"),
            "verification": verification,
            "receipt_present": payload.get("receipt") is not None,
            "incomplete_rows": incomplete_rows,
            "writes_performed": (payload.get("trace") or {}).get("writes_performed"),
        }

    bad = copy.deepcopy(SER03_CASES["cumulative"]["request"])
    bad["estimand"] = "MONETARY_LOSS"
    negative = runner._preflight_module().preflight(bad)
    cases["negative_monetary_estimand"] = {
        "ok": negative.get("status") == "BLOCKED",
        "status": negative.get("status"),
        "issues": negative.get("issues"),
    }

    after = runner.release_integrity(skill_dir, runner.REQUIRED_RELEASE_PATHS)
    cases["release_unchanged"] = {
        "ok": before == after,
        "manifest_sha256": before.get("manifest_sha256"),
    }

    policy = _policy_entry(assistant_root, SKILL)
    cases["policy_pre_promotion"] = {
        "ok": (
            policy.get("current_level") == "L0"
            and policy.get("target_level") == "L3"
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
        "scope": "L3_MONTHLY_BINARY_PILOT_V1",
        "cases": cases,
        "persistent_writes_performed": False,
        "published_package_mutated": before != after,
        "promotion_authorized": False,
    }
    return result


def main() -> int:
    payload = run_probe()
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
