#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Certificador prospectivo da SER, separado dos perfis históricos SE01-SE08.

Perfil inicial: SER01 / hub-ml-criar-objeto / object_validation, pré-promoção.
O certifier executa a rota canônica no checkout atual, inspeciona Receipts reais,
registra o canal histórico SE08 separadamente e nunca altera policy ou produto.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import platform
import re
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT_ROOT = ROOT / "ambiente_fonte" / ".assistant"
POLICY = ASSISTANT_ROOT / "hub_padroes/skill_enforcement/policy.json"
SKILL = "hub-ml-criar-objeto"
SURFACE = "object_validation"
PROFILE = "ser01-object-validation-pre-promotion"
CERTIFIER_VERSION = "SER-CERT-1"
CERTIFIER_ID_PREFIX = "sercert1:"
BRANCH = "ser/SER01-criar-objeto-l3"
DERIVED_ROOT = "Novo_Ambiente_Simulado"


class GateFailed(RuntimeError):
    pass


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_LOAD_FAILED:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
        return module
    finally:
        sys.modules.pop(name, None)


def _process_runner():
    name = "_ser_cert_process_" + uuid.uuid4().hex
    return _load_module(name, ROOT / "tools/skill_enforcement/certify_local.py")


@contextmanager
def _patched_env(values: Mapping[str, str] | None):
    old = {}
    values = dict(values or {})
    try:
        for key, value in values.items():
            old[key] = os.environ.get(key)
            os.environ[key] = value
        yield
    finally:
        for key in values:
            if old[key] is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old[key]


def _write_json(path: Path, value: Any) -> None:
    path.write_bytes(_json_bytes(value) + b"\n")


def _reserve_evidence(path: Path, authorized: bool) -> Path:
    if authorized is not True:
        raise ValueError("EVIDENCE_PERSISTENCE_NOT_AUTHORIZED")
    path = path.absolute()
    if ".." in path.parts or not path.parent.is_dir() or os.path.lexists(path):
        raise ValueError("EVIDENCE_DIRECTORY_MUST_BE_NEW")
    repo = ROOT.resolve(strict=True)
    parent = path.parent.resolve(strict=True)
    if parent.is_relative_to(repo) or repo.is_relative_to(path):
        raise ValueError("EVIDENCE_MUST_BE_EXTERNAL")
    path.mkdir(exist_ok=False)
    (path / "logs").mkdir()
    return path


def _run_step(runner, evidence: Path, steps: list[dict[str, Any]], name: str,
              argv: list[str], *, env: Mapping[str, str] | None = None,
              require_zero: bool = True) -> tuple[int, str]:
    first = len(runner.PROCESS_RECORDS)
    failure = None
    code = 125
    output = ""
    seconds = 0.0
    try:
        with _patched_env(env):
            code, output, seconds = runner._run(argv)
    except BaseException as exc:
        failure = exc
    records = runner.PROCESS_RECORDS[first:]
    observed = copy.deepcopy(records[0]) if len(records) == 1 else {}
    stderr = str(observed.get("stderr", ""))
    stdout = str(observed.get("stdout", output))
    prefix = evidence / "logs" / f"{len(steps)+1:02d}_{name}"
    prefix.with_suffix(".stdout.txt").write_text(stdout, encoding="utf-8")
    prefix.with_suffix(".stderr.txt").write_text(stderr, encoding="utf-8")
    row = {
        "name": name, "argv": list(argv), "exit_code": code,
        "duration_seconds": seconds, "started_at_utc": observed.get("started_at_utc"),
        "ended_at_utc": observed.get("ended_at_utc"),
        "command_started": observed.get("command_started"),
        "process_cleanup": observed.get("cleanup"),
        "process": observed,
    }
    _write_json(prefix.with_suffix(".json"), row)
    steps.append(row)
    if failure is not None:
        raise GateFailed(f"{name}:PROCESS_EXCEPTION:{type(failure).__name__}:{failure}")
    if len(records) != 1 or row["command_started"] is not True or row["process_cleanup"] != "COMPLETE":
        raise GateFailed(f"{name}:PROCESS_EVIDENCE_INCOMPLETE")
    if require_zero and code != 0:
        raise GateFailed(f"{name}:EXIT_{code}")
    return code, stdout


def _git(runner, evidence: Path, steps: list[dict[str, Any]], name: str, *args: str) -> str:
    code, output = _run_step(
        runner, evidence, steps, "git_" + name,
        ["git", "-c", f"core.hooksPath={os.devnull}", "-c", "core.quotepath=false", *args],
    )
    if code:
        raise GateFailed("GIT_FAILED:" + name)
    return output.rstrip("\r\n")


def _git_state(runner, evidence: Path, steps: list[dict[str, Any]]) -> dict[str, Any]:
    counts = _git(runner, evidence, steps, "ahead_behind", "rev-list", "--left-right", "--count", "origin/main...HEAD").split()
    if len(counts) != 2:
        raise GateFailed("GIT_AHEAD_BEHIND_MALFORMED")
    behind, ahead = map(int, counts)
    return {
        "head": _git(runner, evidence, steps, "head", "rev-parse", "HEAD"),
        "tree": _git(runner, evidence, steps, "tree", "rev-parse", "HEAD^{tree}"),
        "branch": _git(runner, evidence, steps, "branch", "rev-parse", "--abbrev-ref", "HEAD"),
        "origin_main": _git(runner, evidence, steps, "origin_main", "rev-parse", "origin/main"),
        "merge_base": _git(runner, evidence, steps, "merge_base", "merge-base", "HEAD", "origin/main"),
        "shallow": _git(runner, evidence, steps, "shallow", "rev-parse", "--is-shallow-repository"),
        "status": _git(runner, evidence, steps, "status", "status", "--porcelain=v1", "--untracked-files=all"),
        "behind": behind,
        "ahead": ahead,
    }


def _policy_entry() -> Mapping[str, Any]:
    raw = json.loads(POLICY.read_text(encoding="utf-8"))
    for item in raw.get("skills", []):
        if isinstance(item, Mapping) and item.get("skill") == SKILL:
            return item
    raise ValueError("POLICY_SKILL_MISSING")


def _route_static_gate() -> dict[str, Any]:
    issues: list[str] = []
    skill_dir = ASSISTANT_ROOT / "skills" / SKILL
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    contract = json.loads((skill_dir / "execution_contract.json").read_text(encoding="utf-8"))
    manifest = json.loads((skill_dir / "release_manifest.json").read_text(encoding="utf-8"))
    policy = _policy_entry()

    for marker in (
        "SER01-OBJECT-VALIDATION-RECEIPT-1",
        "scripts/object_validation.py::verify_receipt",
        "NOT_AVAILABLE",
        "runtime_validation",
    ):
        if marker not in skill_text:
            issues.append("SKILL_ROUTE_MARKER_MISSING:" + marker)

    ov = (((contract.get("metadata") or {}).get("se07") or {}).get("object_validation_contract"))
    expected = {
        "protected_surface": SURFACE,
        "candidate_level": "L3",
        "producer_entrypoint": "tools/skill_enforcement/ser01_object_validation.py::validate_package",
        "verifier_entrypoint": "scripts/object_validation.py::verify_receipt",
        "receipt_version": "SER01-OBJECT-VALIDATION-RECEIPT-1",
        "route": "repo_side_local_structural_validation",
        "supported_operations": ["create"],
        "supported_object_types": ["snippet", "script", "prompt", "notebook", "readme"],
        "unsupported_object_types": ["skill"],
        "original_product_mutation": "forbidden",
        "runtime_validation": "NOT_RUN",
        "missing_or_invalid_receipt": "BLOCK_L3_READY_CLAIM",
        "workspace_without_repo_checkout": "NOT_AVAILABLE",
        "apply_authorized_by_receipt": False,
    }
    if ov != expected:
        issues.append("OBJECT_VALIDATION_CONTRACT_MISMATCH")

    artifacts = manifest.get("artifacts")
    if manifest.get("manifest_version") != "0.1" or manifest.get("skill") != SKILL or not isinstance(artifacts, list):
        issues.append("RELEASE_MANIFEST_INVALID")
        artifacts = []
    observed: dict[str, str] = {}
    seen = set()
    for item in artifacts:
        if not isinstance(item, Mapping) or not isinstance(item.get("path"), str):
            issues.append("RELEASE_ARTIFACT_INVALID")
            continue
        rel = item["path"]
        if rel in seen:
            issues.append("RELEASE_ARTIFACT_DUPLICATE:" + rel)
            continue
        seen.add(rel)
        target = ASSISTANT_ROOT / rel
        if not target.is_file():
            issues.append("RELEASE_ARTIFACT_MISSING:" + rel)
            continue
        actual = _git_blob_sha1(target)
        observed[rel] = actual
        if actual != item.get("git_blob_sha1"):
            issues.append("RELEASE_ARTIFACT_HASH_MISMATCH:" + rel)

    verifier_rel = f"skills/{SKILL}/scripts/object_validation.py"
    if verifier_rel not in seen:
        issues.append("OBJECT_VALIDATION_VERIFIER_NOT_MANIFESTED")

    if policy.get("current_level") != "L2":
        issues.append("PRE_PROMOTION_CURRENT_LEVEL_MUST_BE_L2")
    if policy.get("target_level") != "L3" or policy.get("rollout_mode") != "audit":
        issues.append("POLICY_TARGET_OR_ROLLOUT_MISMATCH")
    surfaces = {
        s.get("id"): s for s in policy.get("protected_surfaces", [])
        if isinstance(s, Mapping)
    }
    surface = surfaces.get(SURFACE)
    if not isinstance(surface, Mapping) or surface.get("level") != "L3" or surface.get("evidence") != "receipt":
        issues.append("POLICY_OBJECT_VALIDATION_SURFACE_MISMATCH")

    return {"status": "PASS" if not issues else "FAIL", "issues": issues,
            "manifest_observed": observed, "current_level": policy.get("current_level"),
            "target_level": policy.get("target_level"), "rollout_mode": policy.get("rollout_mode")}


def _evidence_gate(integration_root: Path, expected_head: str) -> dict[str, Any]:
    issues: list[str] = []
    producer = _load_module("_ser_cert_producer", ROOT / "tools/skill_enforcement/ser01_object_validation.py")
    verifier = _load_module("_ser_cert_verifier", ASSISTANT_ROOT / "skills" / SKILL / "scripts/object_validation.py")
    records = sorted(integration_root.glob("*/validation.json"))
    positives: dict[str, dict[str, Any]] = {}
    negatives = 0

    if len(records) != 7:
        issues.append(f"INTEGRATION_RECORD_COUNT:{len(records)}")

    for path in records:
        record = json.loads(path.read_text(encoding="utf-8"))
        label = path.parent.name
        candidate_path = integration_root / (label + ".candidate.json")
        if not candidate_path.is_file():
            issues.append("CANDIDATE_MISSING:" + label)
            continue
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        status = record.get("status")
        binding = record.get("binding") or {}
        if binding.get("base_sha") != expected_head:
            issues.append("BASE_BINDING_MISMATCH:" + label)

        if status == "PASS":
            kind = binding.get("object_type")
            positives[str(kind)] = record
            receipt = record.get("object_validation_receipt")
            checked = verifier.verify_receipt(
                receipt, local_record=record,
                expected_run_id=record.get("run_id"),
                expected_base_sha=expected_head,
                expected_candidate_sha256=binding.get("candidate_sha256"),
            )
            if checked.get("valid") is not True:
                issues.append("RECEIPT_INVALID:" + label)
            no_record = verifier.verify_receipt(
                receipt,
                expected_run_id=record.get("run_id"),
                expected_base_sha=expected_head,
                expected_candidate_sha256=binding.get("candidate_sha256"),
            )
            if no_record.get("valid") is not False or "LOCAL_RECORD_REQUIRED" not in no_record.get("issues", []):
                issues.append("LOCAL_RECORD_BYPASS_NOT_CLOSED:" + label)
            local_checked = producer.verify_record(
                record, candidate, expected_base_sha=expected_head, expected_run_id=record.get("run_id"))
            if local_checked.get("valid") is not True:
                issues.append("LOCAL_RECORD_VERIFICATION_FAILED:" + label)
            without = copy.deepcopy(record)
            without.pop("object_validation_receipt", None)
            if producer.verify_record(
                without, candidate, expected_base_sha=expected_head,
                expected_run_id=record.get("run_id")).get("valid") is not False:
                issues.append("MISSING_RECEIPT_BYPASS_NOT_CLOSED:" + label)
            tampered = copy.deepcopy(receipt)
            if isinstance(tampered, dict) and isinstance(tampered.get("claims"), dict):
                tampered["claims"]["runtime_validation"] = "PASS"
            if verifier.verify_receipt(
                tampered, local_record=record,
                expected_run_id=record.get("run_id"),
                expected_base_sha=expected_head,
                expected_candidate_sha256=binding.get("candidate_sha256"),
            ).get("valid") is not False:
                issues.append("TAMPER_BYPASS_NOT_CLOSED:" + label)
        elif status == "FAIL":
            negatives += 1
            if "object_validation_receipt" in record:
                issues.append("NEGATIVE_HAS_RECEIPT:" + label)
            if producer.verify_record(
                record, candidate, expected_base_sha=expected_head,
                expected_run_id=record.get("run_id")).get("valid") is not False:
                issues.append("NEGATIVE_LOCAL_RECORD_ACCEPTED:" + label)
        else:
            issues.append("UNEXPECTED_INTEGRATION_STATUS:" + label + ":" + str(status))

    if set(positives) != {"snippet", "script", "prompt", "notebook", "readme"}:
        issues.append("POSITIVE_TYPE_COVERAGE_INVALID:" + ",".join(sorted(positives)))
    if negatives != 2:
        issues.append(f"NEGATIVE_COVERAGE_INVALID:{negatives}")

    return {"status": "PASS" if not issues else "FAIL", "issues": issues,
            "positive_types": sorted(positives), "negative_count": negatives,
            "record_count": len(records), "expected_head": expected_head}


def _seal(summary: dict[str, Any]) -> dict[str, Any]:
    summary.pop("certification_id", None)
    summary["certification_id"] = CERTIFIER_ID_PREFIX + _digest(summary)
    return summary


def verify_certification(payload: Any, *, expected_head: str | None = None) -> dict[str, Any]:
    issues: list[str] = []
    if not isinstance(payload, Mapping):
        return {"valid": False, "issues": ["CERTIFICATION_NOT_MAPPING"]}
    body = {k: copy.deepcopy(v) for k, v in payload.items() if k != "certification_id"}
    try:
        expected_id = CERTIFIER_ID_PREFIX + _digest(body)
    except (TypeError, ValueError, UnicodeError):
        expected_id = None
        issues.append("CERTIFICATION_NOT_CANONICAL_JSON")
    if payload.get("certification_id") != expected_id:
        issues.append("CERTIFICATION_ID_MISMATCH")
    if payload.get("certifier_version") != CERTIFIER_VERSION or payload.get("profile") != PROFILE:
        issues.append("CERTIFIER_IDENTITY_MISMATCH")
    if payload.get("status") != "PASS":
        issues.append("CERTIFICATION_NOT_PASS")
    if payload.get("issues") != []:
        issues.append("CERTIFICATION_ISSUES_NOT_EMPTY")
    if payload.get("historical_se08") != "PASS_SEPARATE_CHANNEL":
        issues.append("HISTORICAL_CHANNEL_INVALID")
    before, after = payload.get("git_before"), payload.get("git_after")
    if not isinstance(before, Mapping) or before != after:
        issues.append("GIT_IDENTITY_NOT_PRESERVED")
    else:
        if expected_head is not None and before.get("head") != expected_head:
            issues.append("HEAD_BINDING_MISMATCH")
        if (before.get("branch") != BRANCH or before.get("status") != ""
                or before.get("shallow") != "false" or before.get("behind") != 0
                or before.get("merge_base") != before.get("origin_main")):
            issues.append("GIT_PRECONDITION_NOT_PROVEN")
    claims = payload.get("claims")
    if claims != {
        "skill": SKILL, "protected_surface": SURFACE,
        "current_level": "L2", "target_level": "L3",
        "policy_promotion_authorized": False, "merge_authorized": False,
        "execution_authenticated": False, "human_authority_authenticated": False,
    }:
        issues.append("CERTIFICATION_CLAIMS_INVALID")
    if (payload.get("route_gate") or {}).get("status") != "PASS":
        issues.append("ROUTE_GATE_NOT_PASS")
    if (payload.get("evidence_gate") or {}).get("status") != "PASS":
        issues.append("EVIDENCE_GATE_NOT_PASS")
    steps = payload.get("steps")
    required_steps = {
        "ser01_object_validation", "ser_certifier_regression", "legacy_create_l3",
        "contracts", "policy", "assistant", "renderer", "render_diff",
        "readme_snapshot", "ci_local", "historical_se08",
    }
    if not isinstance(steps, list) or not steps or any(not isinstance(s, Mapping) for s in steps):
        issues.append("STEP_SET_INVALID")
    else:
        names = [s.get("name") for s in steps]
        if (len(names) != len(set(names)) or not required_steps <= set(names)
                or any(type(s.get("exit_code")) is not int or s.get("exit_code") != 0 for s in steps)
                or any(s.get("command_started") is not True or s.get("process_cleanup") != "COMPLETE"
                       for s in steps)):
            issues.append("STEP_SET_INVALID")
    return {"valid": not issues, "issues": issues,
            "verification_scope": "SER_PROSPECTIVE_CERTIFICATION_INTEGRITY_ONLY"}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, choices=[PROFILE])
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--evidence-authorized", action="store_true")
    args = parser.parse_args(argv)

    evidence = None
    runner = None
    steps: list[dict[str, Any]] = []
    summary: dict[str, Any] = {
        "certifier_version": CERTIFIER_VERSION, "profile": PROFILE,
        "run_id": uuid.uuid4().hex, "started_at_utc": _utc(), "status": "BLOCKED",
        "issues": [], "steps": steps, "route_gate": None, "evidence_gate": None,
        "git_before": None, "git_after": None,
        "host": {"system": platform.system(), "release": platform.release(),
                 "python": sys.version, "platform": platform.platform()},
        "certifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "historical_se08": "NOT_RUN",
        "claims": {
            "skill": SKILL, "protected_surface": SURFACE,
            "current_level": "L2", "target_level": "L3",
            "policy_promotion_authorized": False, "merge_authorized": False,
            "execution_authenticated": False, "human_authority_authenticated": False,
        },
    }

    try:
        evidence = _reserve_evidence(args.evidence_dir, args.evidence_authorized)
        runner = _process_runner()
        runner.REPO_ROOT = ROOT
        summary["git_before"] = _git_state(runner, evidence, steps)
        state = summary["git_before"]
        if state["branch"] != BRANCH or state["status"] != "" or state["shallow"] != "false":
            raise ValueError("GIT_PRECONDITION_FAILED")
        if state["behind"] != 0 or state["merge_base"] != state["origin_main"]:
            raise ValueError("GIT_NOT_RECONCILED_WITH_MAIN")

        route = _route_static_gate()
        summary["route_gate"] = route
        if route["status"] != "PASS":
            raise ValueError("ROUTE_STATIC_GATE_FAILED")

        integration = evidence / "integration"
        _run_step(
            runner, evidence, steps, "ser01_object_validation",
            [sys.executable, "-B", "-m", "unittest", "tools.tests.test_ser01_object_validation", "-v", "-f"],
            env={"SER01_RUN_REPO_INTEGRATION": "1", "SER01_EVIDENCE_ROOT": str(integration)},
        )
        evidence_gate = _evidence_gate(integration, state["head"])
        summary["evidence_gate"] = evidence_gate
        _write_json(evidence / "route_evidence.json", evidence_gate)
        if evidence_gate["status"] != "PASS":
            raise GateFailed("ROUTE_EVIDENCE_GATE_FAILED")

        _run_step(runner, evidence, steps, "ser_certifier_regression",
                  [sys.executable, "-B", "-m", "unittest", "tools.tests.test_ser_certify", "-v", "-f"])
        _run_step(runner, evidence, steps, "legacy_create_l3",
                  [sys.executable, "-B", "-m", "unittest", "tools.tests.test_skill_enforcement_se07_create_l3", "-v", "-f"])
        _run_step(runner, evidence, steps, "contracts",
                  [sys.executable, "-B", "tools/skill_enforcement/validate_contracts.py"])
        _run_step(runner, evidence, steps, "policy",
                  [sys.executable, "-B", "tools/skill_enforcement/se07_policy.py"])
        _run_step(runner, evidence, steps, "assistant",
                  [sys.executable, "-B", "tools/validate_assistant.py"])
        _run_step(runner, evidence, steps, "renderer",
                  [sys.executable, "-B", "tools/render_simulado.py", "--write"])
        _, drift = _run_step(runner, evidence, steps, "render_diff",
                             ["git", "status", "--porcelain", "--untracked-files=all", "--", DERIVED_ROOT])
        if drift.strip():
            raise GateFailed("DERIVED_STALE")
        _run_step(runner, evidence, steps, "readme_snapshot",
                  [sys.executable, "-B", "tools/validate_assistant.py", "--conferir-readme"])
        _run_step(runner, evidence, steps, "ci_local",
                  [sys.executable, "-B", "tools/ci_local.py", "--verbose"])

        historical = evidence / "historical_se08"
        _run_step(
            runner, evidence, steps, "historical_se08",
            [sys.executable, "-B", "tools/skill_enforcement/certify_local.py",
             "--profile", "se08", "--evidence-dir", str(historical)],
        )
        summary["historical_se08"] = "PASS_SEPARATE_CHANNEL"

        summary["git_after"] = _git_state(runner, evidence, steps)
        if summary["git_after"] != summary["git_before"]:
            raise GateFailed("POST_CERTIFICATION_GIT_DRIFT")
        summary["status"] = "PASS"
    except (ValueError, OSError, GateFailed, KeyboardInterrupt, SystemExit) as exc:
        summary["status"] = "FAIL" if isinstance(exc, (GateFailed, KeyboardInterrupt, SystemExit)) else "BLOCKED"
        summary["issues"].append(type(exc).__name__ + ":" + str(exc))
        if evidence is not None and runner is not None:
            try:
                summary["git_after"] = _git_state(runner, evidence, steps)
            except Exception as state_exc:
                summary["issues"].append("POST_STATE_FAILED:" + type(state_exc).__name__)
    finally:
        summary["ended_at_utc"] = _utc()
        _seal(summary)
        if evidence is not None:
            _write_json(evidence / "summary.json", summary)

    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
