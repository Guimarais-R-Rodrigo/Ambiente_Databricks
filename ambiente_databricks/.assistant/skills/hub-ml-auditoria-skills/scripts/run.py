from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import uuid
from pathlib import Path
from typing import Any, Mapping


SKILL = "hub-ml-auditoria-skills"
TRACE_VERSION = "0.1"
RECEIPT_VERSION = "SE07-AUDIT-RECEIPT-1"
MANIFEST_VERSION = "0.1"
CANONICAL_ENTRYPOINT = "skills/hub-ml-auditoria-skills/scripts/run.py::run"
PROTECTED_STEP_ID = "audit_evidence_classifier"
LADDER_KEYS = (
    "citado",
    "localizado",
    "lido",
    "importado",
    "chamado",
    "concluido",
)


def _resolve_assistant_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".assistant":
            return parent
    raise RuntimeError("não foi possível localizar a raiz .assistant a partir do runner")


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _safe_rel(raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw:
        return None
    p = Path(raw)
    if p.is_absolute() or raw.startswith(("/", "\\")) or ".." in p.parts:
        return None
    return p


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"manifest ilegível: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("manifest deve ser objeto JSON")
    if raw.get("manifest_version") != MANIFEST_VERSION:
        raise ValueError("manifest_version não suportada")
    if raw.get("skill") != SKILL:
        raise ValueError("skill do manifest inválida")
    if raw.get("algorithm") != "git_blob_sha1":
        raise ValueError("algoritmo do manifest inválido")
    artifacts = raw.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("manifest.artifacts deve ser lista não vazia")
    return raw


def _verify_release(
    assistant_root: Path,
    manifest_path: Path,
) -> tuple[bool, list[dict[str, str]], dict[str, str]]:
    issues: list[dict[str, str]] = []
    observed: dict[str, str] = {}
    try:
        manifest = _load_manifest(manifest_path)
    except ValueError as exc:
        return False, [{"code": "RELEASE_MANIFEST_INVALID", "message": str(exc)}], observed

    seen: set[str] = set()
    for item in manifest["artifacts"]:
        if not isinstance(item, Mapping):
            issues.append({"code": "RELEASE_MANIFEST_INVALID", "message": "artifact deve ser objeto"})
            continue
        rel = _safe_rel(item.get("path"))
        expected = item.get("git_blob_sha1")
        if rel is None or not isinstance(expected, str) or len(expected) != 40:
            issues.append({"code": "RELEASE_MANIFEST_INVALID", "message": f"artifact inválido: {item!r}"})
            continue
        key = rel.as_posix()
        if key in seen:
            issues.append({"code": "RELEASE_MANIFEST_INVALID", "message": f"path duplicado: {key}"})
            continue
        seen.add(key)
        target = assistant_root / rel
        if not target.is_file():
            issues.append({"code": "RELEASE_INTEGRITY_MISMATCH", "message": f"ausente: {key}"})
            continue
        actual = _git_blob_sha1(target)
        observed[key] = actual
        if actual != expected:
            issues.append({"code": "RELEASE_INTEGRITY_MISMATCH", "message": f"fingerprint divergente: {key}"})
    return not issues, issues, observed


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar módulo: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_preflight(skill_dir: Path):
    return _load_module("sef_audit_preflight_runtime", skill_dir / "scripts" / "preflight.py")


def _producer_verifier_path(
    assistant_root: Path,
    producer_skill: str,
) -> Path | None:
    if producer_skill != "hub-ml-eda-profissional":
        return None
    return (
        assistant_root
        / "skills"
        / producer_skill
        / "scripts"
        / "postflight.py"
    )


def _load_producer_verifier(
    assistant_root: Path,
    producer_skill: str,
):
    path = _producer_verifier_path(assistant_root, producer_skill)
    if path is None or not path.is_file():
        return None, None
    module = _load_module("sef_audit_producer_postflight", path)
    verifier = getattr(module, "verify_finalized", None)
    if not callable(verifier):
        return None, None
    return verifier, f"skills/{producer_skill}/scripts/postflight.py::verify_finalized"


def _producer_verification_base() -> dict[str, Any]:
    return {
        "verifier_name": None,
        "verifier_located": False,
        "verifier_imported": False,
        "verifier_called": False,
        "verifier_completed": False,
        "result_well_formed": False,
        "conclusion_validated": False,
        "executed": False,
        "status": "NOT_RUN",
        "valid": False,
        "completion_authorized": False,
        "completion_claim_consistent": False,
        "issues": [],
    }


def _malformed_verifier_result(
    base: Mapping[str, Any],
    *,
    verifier_name: str,
    code: str,
) -> dict[str, Any]:
    return {
        **base,
        "verifier_name": verifier_name,
        "verifier_called": True,
        "verifier_completed": True,
        "executed": True,
        "status": "MALFORMED",
        "issues": [code],
        "reason": "CANONICAL_VERIFIER_MALFORMED",
    }


def _normalize_ladder(raw: Any) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    issues: list[dict[str, str]] = []
    out: dict[str, dict[str, str]] = {}
    if not isinstance(raw, Mapping) or not raw:
        return {}, [{"code": "STATE_LADDER_REQUIRED", "message": "state_ladder deve ser mapping não vazio"}]

    for item_id, states in raw.items():
        if not isinstance(item_id, str) or not item_id or not isinstance(states, Mapping):
            issues.append({"code": "STATE_LADDER_INVALID", "message": f"item inválido: {item_id!r}"})
            continue
        normalized: dict[str, str] = {}
        for key in LADDER_KEYS:
            if key not in states:
                issues.append({"code": "STATE_LADDER_INCOMPLETE", "message": f"{item_id}: ausente {key}"})
                continue
            value = states.get(key)
            if value is True:
                normalized[key] = "DEMONSTRATED"
            elif value is False:
                normalized[key] = "NOT_DEMONSTRATED"
            elif value is None:
                normalized[key] = "NOT_OBSERVABLE"
            else:
                issues.append({"code": "STATE_LADDER_INVALID", "message": f"{item_id}.{key}: use true, false ou null"})
        out[item_id] = normalized
    return out, issues


def _normalize_applicability(raw: Any) -> tuple[dict[str, str], list[dict[str, str]]]:
    if raw is None:
        return {}, []
    if not isinstance(raw, Mapping):
        return {}, [{"code": "APPLICABILITY_INVALID", "message": "conditional_applicability deve ser mapping"}]
    out: dict[str, str] = {}
    issues: list[dict[str, str]] = []
    for item_id, value in raw.items():
        if not isinstance(item_id, str) or not item_id:
            issues.append({"code": "APPLICABILITY_INVALID", "message": "id de aplicabilidade inválido"})
        elif value is True:
            out[item_id] = "APPLICABLE"
        elif value is False:
            out[item_id] = "NOT_APPLICABLE"
        elif value is None:
            out[item_id] = "NOT_OBSERVABLE"
        else:
            issues.append({"code": "APPLICABILITY_INVALID", "message": f"{item_id}: use true, false ou null"})
    return out, issues


def _producer_verification(
    *,
    assistant_root: Path,
    producer_skill: str | None,
    producer_final_payload: Mapping[str, Any] | None,
) -> dict[str, Any]:
    base = _producer_verification_base()
    if producer_final_payload is None:
        return {**base, "reason": "PRODUCER_FINAL_PAYLOAD_NOT_PROVIDED"}
    if not producer_skill:
        return {**base, "reason": "PRODUCER_SKILL_NOT_RESOLVED"}

    verifier_path = _producer_verifier_path(assistant_root, producer_skill)
    if verifier_path is None or not verifier_path.is_file():
        return {**base, "reason": "NO_CANONICAL_VERIFIER_ADAPTER"}

    verifier_name = f"skills/{producer_skill}/scripts/postflight.py::verify_finalized"
    located = {**base, "verifier_located": True, "verifier_name": verifier_name}
    try:
        verifier, name = _load_producer_verifier(assistant_root, producer_skill)
    except Exception as exc:
        return {
            **located,
            "status": "IMPORT_FAILED",
            "issues": [f"VERIFIER_IMPORT_ERROR:{type(exc).__name__}:{exc}"],
            "reason": "CANONICAL_VERIFIER_IMPORT_FAILED",
        }

    if verifier is None:
        return {
            **located,
            "verifier_imported": True,
            "reason": "CANONICAL_VERIFIER_ENTRYPOINT_UNAVAILABLE",
        }

    imported = {
        **located,
        "verifier_name": name,
        "verifier_imported": True,
    }

    try:
        result = verifier(producer_final_payload, assistant_root=assistant_root)
    except Exception as exc:
        return {
            **imported,
            "verifier_called": True,
            "executed": True,
            "status": "BLOCKED",
            "issues": [f"VERIFIER_RUNTIME_ERROR:{type(exc).__name__}:{exc}"],
            "reason": "CANONICAL_VERIFIER_RAISED",
        }

    if not isinstance(result, Mapping):
        return _malformed_verifier_result(
            imported,
            verifier_name=name,
            code="VERIFIER_RESULT_NOT_MAPPING",
        )

    required_fields = (
        "status",
        "valid",
        "completion_authorized",
        "completion_claim_consistent",
        "issues",
    )
    for field in required_fields:
        if field not in result:
            return _malformed_verifier_result(
                imported,
                verifier_name=name,
                code=f"VERIFIER_RESULT_REQUIRED_FIELD_MISSING:{field}",
            )

    if not isinstance(result["status"], str) or not result["status"]:
        return _malformed_verifier_result(
            imported,
            verifier_name=name,
            code="VERIFIER_RESULT_STATUS_INVALID",
        )
    for field in ("valid", "completion_authorized", "completion_claim_consistent"):
        if not isinstance(result[field], bool):
            return _malformed_verifier_result(
                imported,
                verifier_name=name,
                code=f"VERIFIER_RESULT_FIELD_INVALID:{field}",
            )
    raw_issues = result["issues"]
    if not isinstance(raw_issues, (list, tuple)) or not all(
        isinstance(item, str) for item in raw_issues
    ):
        return _malformed_verifier_result(
            imported,
            verifier_name=name,
            code="VERIFIER_RESULT_ISSUES_INVALID",
        )

    return {
        **imported,
        "verifier_called": True,
        "verifier_completed": True,
        "result_well_formed": True,
        "conclusion_validated": (
            result["status"] == "VALID"
            and result["valid"] is True
            and result["completion_authorized"] is True
            and result["completion_claim_consistent"] is True
            and not raw_issues
        ),
        "executed": True,
        "status": result["status"],
        "valid": result["valid"],
        "completion_authorized": result["completion_authorized"],
        "completion_claim_consistent": result["completion_claim_consistent"],
        "issues": list(raw_issues),
        "reason": "CANONICAL_VERIFIER_EXECUTED",
    }


def _producer_compliance(verification: Mapping[str, Any]) -> str:
    if verification.get("verifier_called") is not True:
        return "NOT_REVERIFIED"
    if (
        verification.get("verifier_completed") is True
        and verification.get("result_well_formed") is True
        and verification.get("conclusion_validated") is True
    ):
        return "PASS_REVERIFIED"
    return "NOT_PASS_REVERIFIED"


def _base_trace(
    *,
    run_id: str,
    manifest_path: Path,
    manifest_digest: str | None,
    observed: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "trace_version": TRACE_VERSION,
        "run_id": run_id,
        "skill": SKILL,
        "entrypoint": CANONICAL_ENTRYPOINT,
        "manifest": manifest_path.name,
        "manifest_digest": manifest_digest,
        "contract_digest": observed.get(f"skills/{SKILL}/execution_contract.json"),
        "runner_digest": observed.get(f"skills/{SKILL}/scripts/run.py"),
        "input_digest": None,
        "output_digest": None,
        "preflight_status": "NOT_RUN",
        "protected_steps_called": [],
        "protected_steps_completed": [],
        "producer_verifier": {},
        "blocking_issues": [],
        "writes_performed": False,
        "analytics_executed": False,
        "status": "BLOCKED",
    }


def _receipt_body(trace: Mapping[str, Any], result: Any) -> dict[str, Any] | None:
    if trace.get("trace_version") != TRACE_VERSION:
        return None
    if trace.get("skill") != SKILL or trace.get("entrypoint") != CANONICAL_ENTRYPOINT:
        return None
    if trace.get("status") != "PASS" or trace.get("preflight_status") != "PASS":
        return None
    if PROTECTED_STEP_ID not in trace.get("protected_steps_called", []):
        return None
    if PROTECTED_STEP_ID not in trace.get("protected_steps_completed", []):
        return None
    if trace.get("blocking_issues") != []:
        return None
    if trace.get("writes_performed") is not False or trace.get("analytics_executed") is not False:
        return None

    for key, length in (
        ("manifest_digest", 64),
        ("contract_digest", 40),
        ("runner_digest", 40),
        ("input_digest", 64),
        ("output_digest", 64),
    ):
        value = trace.get(key)
        if not isinstance(value, str) or len(value) != length:
            return None

    if trace.get("output_digest") != _digest(result):
        return None

    verification = trace.get("producer_verifier")
    if not isinstance(verification, Mapping):
        return None

    return {
        "receipt_version": RECEIPT_VERSION,
        "run_id": trace["run_id"],
        "skill": SKILL,
        "entrypoint": CANONICAL_ENTRYPOINT,
        "audit_runner_compliance": "PASS",
        "preflight_status": "PASS",
        "producer_canonical_compliance": (
            result.get("producer_canonical_compliance")
            if isinstance(result, Mapping)
            else None
        ),
        "release": {
            "manifest_name": trace["manifest"],
            "manifest_sha256": trace["manifest_digest"],
            "contract_git_blob_sha1": trace["contract_digest"],
            "runner_git_blob_sha1": trace["runner_digest"],
        },
        "bindings": {
            "trace_sha256": _digest(trace),
            "input_sha256": trace["input_digest"],
            "output_sha256": trace["output_digest"],
        },
        "protected_step": PROTECTED_STEP_ID,
        "producer_verifier": dict(verification),
        "writes_performed": False,
        "analytics_executed": False,
    }


def _build_receipt(trace: Mapping[str, Any], result: Any) -> dict[str, Any] | None:
    body = _receipt_body(trace, result)
    if body is None:
        return None
    return {**body, "receipt_id": "audit-er1:" + _digest(body)}


def run(
    context: Mapping[str, Any],
    evidence: Mapping[str, Any],
    *,
    producer_final_payload: Mapping[str, Any] | None = None,
    assistant_root: Path | str | None = None,
    manifest_path: Path | str | None = None,
) -> dict[str, Any]:
    """Executa o envelope L3 determinístico da auditoria sem julgamento editorial."""
    run_id = uuid.uuid4().hex
    root = Path(assistant_root) if assistant_root is not None else _resolve_assistant_root()
    skill_dir = root / "skills" / SKILL
    manifest = Path(manifest_path) if manifest_path is not None else skill_dir / "release_manifest.json"

    integrity_ok, integrity_issues, observed = _verify_release(root, manifest)
    manifest_digest = _sha256_file(manifest) if manifest.is_file() else None
    trace = _base_trace(
        run_id=run_id,
        manifest_path=manifest,
        manifest_digest=manifest_digest,
        observed=observed,
    )

    if not integrity_ok:
        trace["blocking_issues"].extend(integrity_issues)
        return {"trace": trace, "receipt": None, "result": None}

    if not isinstance(context, Mapping) or not isinstance(evidence, Mapping):
        trace["blocking_issues"].append(
            {"code": "RUN_INPUT_INVALID", "message": "context e evidence devem ser mappings"}
        )
        return {"trace": trace, "receipt": None, "result": None}

    preflight = _load_preflight(skill_dir).preflight(context)
    trace["preflight_status"] = preflight.get("status")
    if preflight.get("status") != "PASS":
        trace["blocking_issues"].extend(preflight.get("blocking_issues") or [])
        return {"trace": trace, "receipt": None, "result": None}

    ladder, ladder_issues = _normalize_ladder(evidence.get("state_ladder"))
    applicability, applicability_issues = _normalize_applicability(
        evidence.get("conditional_applicability")
    )
    persisted = evidence.get("persisted_mechanical_state", {})
    if not isinstance(persisted, Mapping):
        applicability_issues.append(
            {"code": "PERSISTED_STATE_INVALID", "message": "persisted_mechanical_state deve ser mapping"}
        )

    issues = [*ladder_issues, *applicability_issues]
    if issues:
        trace["blocking_issues"].extend(issues)
        return {"trace": trace, "receipt": None, "result": None}

    trace["input_digest"] = _digest(
        {
            "context": dict(context),
            "evidence": dict(evidence),
            "producer_final_payload_sha256": (
                _digest(producer_final_payload)
                if producer_final_payload is not None
                else None
            ),
        }
    )

    trace["protected_steps_called"].append(PROTECTED_STEP_ID)

    producer_skill = preflight.get("producer_skill")
    verification = _producer_verification(
        assistant_root=root,
        producer_skill=producer_skill if isinstance(producer_skill, str) else None,
        producer_final_payload=producer_final_payload,
    )
    trace["producer_verifier"] = verification

    result = {
        "state_ladder": ladder,
        "conditional_applicability": applicability,
        "persisted_mechanical_state": dict(persisted),
        "producer_verification": verification,
        "producer_canonical_compliance": _producer_compliance(verification),
        "audit_runner_status": "PASS",
    }

    trace["protected_steps_completed"].append(PROTECTED_STEP_ID)
    trace["output_digest"] = _digest(result)
    trace["status"] = "PASS"

    receipt = _build_receipt(trace, result)
    if receipt is None:
        trace["status"] = "FAIL"
        trace["blocking_issues"].append(
            {"code": "RECEIPT_EMISSION_FAILED", "message": "receipt L3 não pôde ser emitido"}
        )
        return {"trace": trace, "receipt": None, "result": result}

    return {"trace": trace, "receipt": receipt, "result": result}


def verify_receipt(
    payload: Mapping[str, Any],
    *,
    expected_run_id: str | None = None,
    assistant_root: Path | str | None = None,
    manifest_path: Path | str | None = None,
) -> dict[str, Any]:
    """Reverifica o Receipt da auditoria e sua vinculação ao release atual."""
    if not isinstance(payload, Mapping):
        return {"status": "MALFORMED", "valid": False, "issues": ["PAYLOAD_NOT_MAPPING"]}
    receipt = payload.get("receipt")
    if receipt is None:
        return {"status": "ABSENT", "valid": False, "issues": ["RECEIPT_ABSENT"]}
    if not isinstance(receipt, Mapping):
        return {"status": "MALFORMED", "valid": False, "issues": ["RECEIPT_NOT_MAPPING"]}

    run_id = receipt.get("run_id")
    if expected_run_id is not None and run_id != expected_run_id:
        return {"status": "STALE_REPLAYED", "valid": False, "issues": ["RUN_ID_STALE"]}

    receipt_body = dict(receipt)
    receipt_id = receipt_body.pop("receipt_id", None)
    if receipt_id != "audit-er1:" + _digest(receipt_body):
        return {"status": "INVALID", "valid": False, "issues": ["RECEIPT_ID_MISMATCH"]}

    expected = _build_receipt(payload.get("trace", {}), payload.get("result"))
    if expected is None or expected != dict(receipt):
        return {"status": "INCOMPATIBLE", "valid": False, "issues": ["RECEIPT_BINDING_MISMATCH"]}

    root = Path(assistant_root) if assistant_root is not None else _resolve_assistant_root()
    skill_dir = root / "skills" / SKILL
    manifest = Path(manifest_path) if manifest_path is not None else skill_dir / "release_manifest.json"
    integrity_ok, issues, observed = _verify_release(root, manifest)
    if not integrity_ok:
        return {
            "status": "INCOMPATIBLE",
            "valid": False,
            "issues": [item["code"] for item in issues],
        }

    release = receipt.get("release")
    if not isinstance(release, Mapping):
        return {"status": "MALFORMED", "valid": False, "issues": ["RELEASE_BINDING_MISSING"]}

    expected_release = {
        "manifest_name": manifest.name,
        "manifest_sha256": _sha256_file(manifest),
        "contract_git_blob_sha1": observed.get(f"skills/{SKILL}/execution_contract.json"),
        "runner_git_blob_sha1": observed.get(f"skills/{SKILL}/scripts/run.py"),
    }
    if dict(release) != expected_release:
        return {"status": "INCOMPATIBLE", "valid": False, "issues": ["CURRENT_RELEASE_MISMATCH"]}

    return {
        "status": "VALID",
        "valid": True,
        "issues": [],
        "run_id": run_id,
        "audit_runner_compliance": "PASS",
        "producer_canonical_compliance": receipt.get("producer_canonical_compliance"),
    }


def _load_json(raw: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} inválido: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} deve ser objeto JSON")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Runner L3 da hub-ml-auditoria-skills")
    parser.add_argument("--context-json", required=True)
    parser.add_argument("--evidence-json", required=True)
    parser.add_argument("--producer-final-payload-json")
    args = parser.parse_args()

    try:
        context = _load_json(args.context_json, "context-json")
        evidence = _load_json(args.evidence_json, "evidence-json")
        producer = (
            _load_json(args.producer_final_payload_json, "producer-final-payload-json")
            if args.producer_final_payload_json
            else None
        )
        payload = run(context, evidence, producer_final_payload=producer)
    except (RuntimeError, ValueError) as exc:
        payload = {
            "trace": {
                "status": "BLOCKED",
                "blocking_issues": [{"code": "RUN_INPUT_INVALID", "message": str(exc)}],
                "writes_performed": False,
                "analytics_executed": False,
            },
            "receipt": None,
            "result": None,
        }

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0 if payload.get("receipt") is not None else 2


if __name__ == "__main__":
    raise SystemExit(main())
