#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Certificação prospectiva pós-promoção da SER01.

A policy já deve declarar L3. O certifier preserva os oráculos históricos
pré-promoção como canais temporais explícitos; não reescreve SE07/SE08 nem o
SER-CERT-1 para fazê-los acompanhar a árvore nova.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT = ROOT / "ambiente_fonte" / ".assistant"
POLICY = ASSISTANT / "hub_padroes/skill_enforcement/policy.json"
SKILL = "hub-ml-criar-objeto"
SURFACE = "object_validation"
PROFILE = "ser01-object-validation-post-promotion"
VERSION = "SER-PROMOTION-CERT-2"
ID_PREFIX = "serprom2:"
BRANCH = "ser/SER01-criar-objeto-l3"

SUPPORTED_TYPES = ["snippet", "script", "prompt", "notebook", "readme"]
HISTORICAL_EXPECTATIONS = {
    "historical_ser_certifier": {"test_current_tree_route_is_coherent_pre_promotion"},
    "historical_se07": {"test_current_level_is_evidence_based", "test_runtime_resolver"},
    "historical_se08": {"test_create_object_global_level_is_not_promoted_by_se08"},
}
CI_NON_SEF_STAGES = (
    "temas", "validacao", "biblioteca", "ferramentas", "transicao",
    "readmes", "concierge-pacote", "concierge-regressoes", "concierge-integracao",
)


def _load(name: str, path: Path):
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


ser = _load("_ser_promotion_base", ROOT / "tools/skill_enforcement/ser_certify.py")


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def _write(path: Path, value: Any) -> None:
    path.write_bytes(_json_bytes(value) + b"\n")


def _seal(value: dict[str, Any]) -> dict[str, Any]:
    value.pop("certification_id", None)
    value["certification_id"] = ID_PREFIX + _digest(value)
    return value


def _policy_entry() -> Mapping[str, Any]:
    raw = json.loads(POLICY.read_text(encoding="utf-8"))
    for item in raw.get("skills", []):
        if isinstance(item, Mapping) and item.get("skill") == SKILL:
            return item
    raise RuntimeError("POLICY_SKILL_MISSING")


def _promotion_gate() -> dict[str, Any]:
    policy = _policy_entry()
    issues: list[str] = []
    required = {
        f"skills/{SKILL}/SKILL.md",
        f"skills/{SKILL}/execution_contract.json",
        f"skills/{SKILL}/scripts/preflight.py",
        f"skills/{SKILL}/scripts/run.py",
        f"skills/{SKILL}/scripts/object_validation.py",
        f"skills/{SKILL}/release_manifest.json",
    }
    if policy.get("current_level") != "L3" or policy.get("target_level") != "L3":
        issues.append("POLICY_LEVEL_NOT_L3")
    if policy.get("policy_status") != "implemented":
        issues.append("POLICY_STATUS_NOT_IMPLEMENTED")
    if policy.get("rollout_mode") != "audit" or policy.get("scope_mode") != "stage_specific":
        issues.append("POLICY_MODE_OR_SCOPE_CHANGED")
    if not required <= set(policy.get("implemented_artifacts") or []):
        issues.append("IMPLEMENTED_ARTIFACTS_INCOMPLETE")

    surfaces = {
        item.get("id"): item
        for item in policy.get("protected_surfaces", [])
        if isinstance(item, Mapping)
    }
    object_shape = surfaces.get("object_shape")
    object_validation = surfaces.get(SURFACE)
    if (
        not isinstance(object_shape, Mapping)
        or object_shape.get("level") != "L2"
        or object_shape.get("evidence") != "preflight"
    ):
        issues.append("OBJECT_SHAPE_SURFACE_INVALID")
    if (
        not isinstance(object_validation, Mapping)
        or object_validation.get("level") != "L3"
        or object_validation.get("evidence") != "receipt"
    ):
        issues.append("OBJECT_VALIDATION_SURFACE_INVALID")

    for rel in sorted(required):
        if not (ASSISTANT / rel).is_file():
            issues.append("REQUIRED_ARTIFACT_MISSING:" + rel)

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "current_level": policy.get("current_level"),
        "target_level": policy.get("target_level"),
        "policy_status": policy.get("policy_status"),
        "rollout_mode": policy.get("rollout_mode"),
        "scope_mode": policy.get("scope_mode"),
        "implemented_artifacts": sorted(policy.get("implemented_artifacts") or []),
    }


def _route_gate_post_promotion() -> dict[str, Any]:
    """Reuse A3's route/manifest oracle while isolating its temporal L2 assertion."""
    raw = ser._route_static_gate()
    raw_issues = list(raw.get("issues") or [])
    temporal = "PRE_PROMOTION_CURRENT_LEVEL_MUST_BE_L2"
    issues = [item for item in raw_issues if item != temporal]
    if raw.get("current_level") != "L3":
        issues.append("POST_PROMOTION_CURRENT_LEVEL_MUST_BE_L3")
    if raw.get("target_level") != "L3" or raw.get("rollout_mode") != "audit":
        issues.append("POLICY_TARGET_OR_ROLLOUT_MISMATCH")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "pre_promotion_oracle_issues": raw_issues,
        "temporal_pre_promotion_issue_observed": temporal in raw_issues,
        "manifest_observed": raw.get("manifest_observed"),
        "current_level": raw.get("current_level"),
        "target_level": raw.get("target_level"),
        "rollout_mode": raw.get("rollout_mode"),
    }


def _historical_result(
    name: str, code: int, output: str, expected: set[str]
) -> dict[str, Any]:
    failures = set(re.findall(r"(?m)^FAIL: (test_[A-Za-z0-9_]+)", output))
    errors = set(re.findall(r"(?m)^ERROR: (test_[A-Za-z0-9_]+)", output))
    summary = re.search(r"FAILED \(([^)]*)\)", output)
    counts: dict[str, int] = {}
    if summary:
        for key, value in re.findall(r"(failures|errors|skipped)=(\d+)", summary.group(1)):
            counts[key] = int(value)
    unexpected = sorted(failures - expected)
    missing = sorted(expected - failures)
    error_count = counts.get("errors", 0)
    failure_count = counts.get("failures")
    ok = (
        code == 1
        and not unexpected
        and not missing
        and not errors
        and error_count == 0
        and (failure_count is None or failure_count == len(expected))
    )
    return {
        "name": name,
        "status": "EXPECTED_TEMPORAL_FAIL" if ok else "UNEXPECTED_RESULT",
        "exit_code": code,
        "expected_failures": sorted(expected),
        "observed_failures": sorted(failures),
        "observed_errors": sorted(errors),
        "summary_counts": counts,
        "unexpected_failures": unexpected,
        "missing_failures": missing,
    }


def _combined_step_output(row: Mapping[str, Any], stdout: str) -> str:
    process = row.get("process")
    stderr = process.get("stderr", "") if isinstance(process, Mapping) else ""
    return str(stdout) + "\n" + str(stderr)


def _run_historical(
    runner, evidence: Path, steps: list[dict[str, Any]],
    name: str, module: str, expected: set[str],
) -> dict[str, Any]:
    code, stdout = ser._run_step(
        runner, evidence, steps, name,
        [sys.executable, "-B", "-m", "unittest", module, "-v"],
        require_zero=False,
    )
    combined = _combined_step_output(steps[-1], stdout)
    result = _historical_result(name, code, combined, expected)
    _write(evidence / f"{name}.classification.json", result)
    if result["status"] != "EXPECTED_TEMPORAL_FAIL":
        raise ser.GateFailed(name + ":UNEXPECTED_HISTORICAL_RESULT")
    return result


def _claims() -> dict[str, Any]:
    return {
        "skill": SKILL,
        "protected_surface": SURFACE,
        "current_level": "L3",
        "target_level": "L3",
        "rollout_mode": "audit",
        "scope_mode": "stage_specific",
        "supported_operations": ["create"],
        "supported_object_types": SUPPORTED_TYPES,
        "unsupported_object_types": ["skill"],
        "runtime_validation": "NOT_RUN",
        "apply_authorized_by_receipt": False,
        "merge_authorized": False,
        "human_authority_authenticated": False,
    }


def _required_zero_steps() -> set[str]:
    return {
        *(f"git_{phase}_{component}" for phase in ("before", "after")
          for component in ser.GIT_STATE_COMPONENTS),
        "promotion_certifier_regression",
        "ser01_object_validation",
        "legacy_create_l3",
        "contracts",
        "policy",
        "assistant",
        "renderer",
        "render_diff",
        "readme_snapshot",
        "policy_io_regression",
        "local_certifier_regression",
        *(f"ci_{stage}" for stage in CI_NON_SEF_STAGES),
    }


def verify_certification(payload: Any, *, expected_head: str | None = None) -> dict[str, Any]:
    issues: list[str] = []
    if not isinstance(payload, Mapping):
        return {"valid": False, "issues": ["CERTIFICATION_NOT_MAPPING"]}

    body = {k: copy.deepcopy(v) for k, v in payload.items() if k != "certification_id"}
    try:
        expected_id = ID_PREFIX + _digest(body)
    except (TypeError, ValueError, UnicodeError):
        expected_id = None
        issues.append("CERTIFICATION_NOT_CANONICAL_JSON")
    if payload.get("certification_id") != expected_id:
        issues.append("CERTIFICATION_ID_MISMATCH")
    if payload.get("version") != VERSION or payload.get("profile") != PROFILE:
        issues.append("CERTIFIER_IDENTITY_MISMATCH")
    if payload.get("status") != "PASS" or payload.get("issues") != []:
        issues.append("CERTIFICATION_NOT_CLEAN_PASS")
    if (payload.get("promotion_gate") or {}).get("status") != "PASS":
        issues.append("PROMOTION_GATE_NOT_PASS")
    if (payload.get("route_gate") or {}).get("status") != "PASS":
        issues.append("ROUTE_GATE_NOT_PASS")
    if (payload.get("evidence_gate") or {}).get("status") != "PASS":
        issues.append("EVIDENCE_GATE_NOT_PASS")
    if payload.get("claims") != _claims():
        issues.append("CERTIFICATION_CLAIMS_INVALID")

    before, after = payload.get("git_before"), payload.get("git_after")
    if not isinstance(before, Mapping) or before != after:
        issues.append("GIT_IDENTITY_NOT_PRESERVED")
    else:
        if expected_head is not None and before.get("head") != expected_head:
            issues.append("HEAD_BINDING_MISMATCH")
        if (
            before.get("branch") != BRANCH
            or before.get("status") != ""
            or before.get("shallow") != "false"
            or before.get("behind") != 0
            or before.get("merge_base") != before.get("origin_main")
        ):
            issues.append("GIT_PRECONDITION_NOT_PROVEN")

    historical = payload.get("historical_channels")
    by_name = {
        row.get("name"): row
        for row in historical
        if isinstance(row, Mapping)
    } if isinstance(historical, list) else {}
    if set(by_name) != set(HISTORICAL_EXPECTATIONS):
        issues.append("HISTORICAL_CHANNEL_SET_INVALID")
    else:
        for name, expected in HISTORICAL_EXPECTATIONS.items():
            row = by_name[name]
            if (
                row.get("status") != "EXPECTED_TEMPORAL_FAIL"
                or row.get("exit_code") != 1
                or set(row.get("observed_failures") or []) != expected
                or row.get("observed_errors") != []
            ):
                issues.append("HISTORICAL_CHANNEL_INVALID:" + name)

    steps = payload.get("steps")
    zero_required = _required_zero_steps()
    if not isinstance(steps, list) or not steps or any(not isinstance(row, Mapping) for row in steps):
        issues.append("STEP_SET_INVALID")
    else:
        names = [row.get("name") for row in steps]
        by_step = {row.get("name"): row for row in steps}
        if len(names) != len(set(names)) or not zero_required <= set(names):
            issues.append("STEP_SET_INVALID")
        else:
            for name in sorted(zero_required):
                row = by_step[name]
                if (
                    type(row.get("exit_code")) is not int
                    or row.get("exit_code") != 0
                    or row.get("command_started") is not True
                    or row.get("process_cleanup") != "COMPLETE"
                ):
                    issues.append("ZERO_STEP_INVALID:" + name)
            for name in HISTORICAL_EXPECTATIONS:
                row = by_step.get(name)
                if (
                    not isinstance(row, Mapping)
                    or row.get("exit_code") != 1
                    or row.get("command_started") is not True
                    or row.get("process_cleanup") != "COMPLETE"
                ):
                    issues.append("HISTORICAL_STEP_INVALID:" + name)

    for field in ("certifier_sha256", "policy_sha256"):
        value = payload.get(field)
        if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
            issues.append(field.upper() + "_INVALID")

    return {
        "valid": not issues,
        "issues": issues,
        "verification_scope": "SER_POLICY_PROMOTION_CERTIFICATION",
    }


def _attempt_final_git_state(
    runner, evidence: Path, steps: list[dict[str, Any]], summary: dict[str, Any]
) -> None:
    if summary.get("git_before") is None or summary.get("git_after") is not None:
        return
    if any(str(row.get("name", "")).startswith("git_after_") for row in steps):
        summary["issues"].append("FINAL_GIT_STATE_PARTIAL")
        return
    try:
        summary["git_after"] = ser._git_state(runner, evidence, steps, phase="after")
    except BaseException as exc:
        summary["issues"].append(
            "FINAL_GIT_STATE_FAILED:" + type(exc).__name__ + ":" + str(exc)
        )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, choices=[PROFILE])
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--evidence-authorized", action="store_true")
    args = parser.parse_args(argv)

    evidence = ser._reserve_evidence(args.evidence_dir, args.evidence_authorized)
    runner = ser._process_runner()
    runner.REPO_ROOT = ROOT
    steps: list[dict[str, Any]] = []
    summary: dict[str, Any] = {
        "version": VERSION,
        "profile": PROFILE,
        "run_id": uuid.uuid4().hex,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "ended_at_utc": None,
        "status": "BLOCKED",
        "issues": [],
        "steps": steps,
        "promotion_gate": None,
        "route_gate": None,
        "evidence_gate": None,
        "historical_channels": [],
        "git_before": None,
        "git_after": None,
        "claims": _claims(),
        "certifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "policy_sha256": hashlib.sha256(POLICY.read_bytes()).hexdigest(),
    }

    try:
        summary["git_before"] = ser._git_state(runner, evidence, steps, phase="before")
        state = summary["git_before"]
        if (
            state["branch"] != BRANCH
            or state["status"] != ""
            or state["shallow"] != "false"
            or state["behind"] != 0
            or state["merge_base"] != state["origin_main"]
        ):
            raise ser.GateFailed("GIT_PRECONDITION_FAILED")

        ser._run_step(
            runner, evidence, steps, "promotion_certifier_regression",
            [sys.executable, "-B", "-m", "unittest", "tools.tests.test_ser_promotion_certify", "-v"],
        )

        promotion = _promotion_gate()
        summary["promotion_gate"] = promotion
        _write(evidence / "promotion_gate.json", promotion)
        if promotion["status"] != "PASS":
            raise ser.GateFailed("PROMOTION_GATE_FAILED")

        route = _route_gate_post_promotion()
        summary["route_gate"] = route
        _write(evidence / "route_gate.json", route)
        if route["status"] != "PASS":
            raise ser.GateFailed("ROUTE_GATE_FAILED")

        integration = evidence / "integration"
        ser._run_step(
            runner, evidence, steps, "ser01_object_validation",
            [sys.executable, "-B", "-m", "unittest", "tools.tests.test_ser01_object_validation", "-v", "-f"],
            env={"SER01_RUN_REPO_INTEGRATION": "1", "SER01_EVIDENCE_ROOT": str(integration)},
        )
        evidence_gate = ser._evidence_gate(integration, state["head"])
        summary["evidence_gate"] = evidence_gate
        _write(evidence / "route_evidence.json", evidence_gate)
        if evidence_gate["status"] != "PASS":
            raise ser.GateFailed("EVIDENCE_GATE_FAILED")

        ser._run_step(
            runner, evidence, steps, "legacy_create_l3",
            [sys.executable, "-B", "-m", "unittest", "tools.tests.test_skill_enforcement_se07_create_l3", "-v", "-f"],
            env={"SE07_L3_EVIDENCE_DIR": str(evidence / "legacy_create")},
        )
        ser._run_step(
            runner, evidence, steps, "contracts",
            [sys.executable, "-B", "tools/skill_enforcement/validate_contracts.py"],
        )
        ser._run_step(
            runner, evidence, steps, "policy",
            [sys.executable, "-B", "tools/skill_enforcement/se07_policy.py"],
        )
        ser._run_step(
            runner, evidence, steps, "assistant",
            [sys.executable, "-B", "tools/validate_assistant.py"],
        )
        ser._run_step(
            runner, evidence, steps, "renderer",
            [sys.executable, "-B", "tools/render_simulado.py", "--write"],
        )
        ser._run_step(
            runner, evidence, steps, "render_diff",
            [sys.executable, "-B", "tools/render_simulado.py", "--check"],
        )
        ser._run_step(
            runner, evidence, steps, "readme_snapshot",
            [sys.executable, "-B", "tools/validate_assistant.py", "--conferir-readme"],
        )
        ser._run_step(
            runner, evidence, steps, "policy_io_regression",
            [sys.executable, "-B", "-m", "unittest", "tools.tests.test_skill_enforcement_policy_io", "-v"],
        )
        ser._run_step(
            runner, evidence, steps, "local_certifier_regression",
            [sys.executable, "-B", "-m", "unittest", "tools.tests.test_certify_local", "-v"],
        )

        for stage in CI_NON_SEF_STAGES:
            ser._run_step(
                runner, evidence, steps, "ci_" + stage,
                [sys.executable, "-B", "tools/ci_local.py", "--etapa", stage, "--verbose"],
            )

        for name, module in (
            ("historical_ser_certifier", "tools.tests.test_ser_certify"),
            ("historical_se07", "tools.tests.test_skill_enforcement_se07"),
            ("historical_se08", "tools.tests.test_skill_enforcement_se08"),
        ):
            result = _run_historical(
                runner, evidence, steps, name, module, HISTORICAL_EXPECTATIONS[name]
            )
            summary["historical_channels"].append(result)

        summary["git_after"] = ser._git_state(runner, evidence, steps, phase="after")
        if summary["git_after"] != summary["git_before"]:
            raise ser.GateFailed("GIT_IDENTITY_NOT_PRESERVED")
        summary["status"] = "PASS"

    except BaseException as exc:
        summary["status"] = "FAIL"
        summary["issues"].append(type(exc).__name__ + ":" + str(exc))
        _attempt_final_git_state(runner, evidence, steps, summary)

    finally:
        summary["ended_at_utc"] = datetime.now(timezone.utc).isoformat()
        _seal(summary)
        if summary["status"] == "PASS":
            checked = verify_certification(
                summary, expected_head=(summary.get("git_before") or {}).get("head")
            )
            _write(evidence / "self_verification.json", checked)
            if checked.get("valid") is not True:
                summary["status"] = "FAIL"
                summary["issues"].append(
                    "SELF_VERIFICATION_FAILED:" + ",".join(checked.get("issues") or ["UNKNOWN"])
                )
                _seal(summary)
        _write(evidence / "summary.json", summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
