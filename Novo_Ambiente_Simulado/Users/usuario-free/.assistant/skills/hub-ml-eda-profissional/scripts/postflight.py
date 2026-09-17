from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Mapping


SKILL = "hub-ml-eda-profissional"
FINALIZER_VERSION = "1.0"
ENFORCED_ENTRYPOINT = "skills/hub-ml-eda-profissional/scripts/run_enforced.py::run_enforced"


def _resolve_assistant_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".assistant":
            return parent
    raise RuntimeError("não foi possível localizar a raiz .assistant a partir do postflight")


def _load_runner(skill_dir: Path):
    path = skill_dir / "scripts" / "run.py"
    spec = importlib.util.spec_from_file_location("sef_se05_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar runner canônico: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_contract(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"execution_contract ilegível: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("execution_contract deve ser objeto JSON")
    if payload.get("skill") != SKILL:
        raise ValueError(f"skill do contrato inválida: {payload.get('skill')!r}")
    return payload


def _blocked_finalization(
    payload: Mapping[str, Any] | None,
    *,
    code: str,
    message: str,
    handoff: Mapping[str, Any] | None,
) -> dict[str, Any]:
    result = dict(payload) if isinstance(payload, Mapping) else {}
    result["handoff"] = dict(handoff) if isinstance(handoff, Mapping) else {}
    result["postflight"] = {
        "postflight_version": FINALIZER_VERSION,
        "status": "BLOCKED",
        "completion_authorized": False,
        "issues": [
            {
                "severity": "BLOCKED",
                "code": code,
                "message": message,
                "item_type": None,
                "item_id": None,
            }
        ],
        "writes_performed": False,
    }
    result["completion"] = {
        "authorized": False,
        "status": "NOT_COMPLETED",
        "reason": "postflight != PASS",
    }
    return result


def _enforced_route_ok(payload: Mapping[str, Any]) -> bool:
    trace = payload.get("trace")
    return bool(
        isinstance(trace, Mapping)
        and trace.get("enforcement_entrypoint") == ENFORCED_ENTRYPOINT
    )


def finalize(
    payload: Mapping[str, Any],
    handoff: Mapping[str, Any],
    *,
    assistant_root: Path | str | None = None,
) -> dict[str, Any]:
    """Finaliza a execução somente se Receipt, rota L4, contrato e handoff satisfizerem o postflight."""
    if not isinstance(payload, Mapping):
        return _blocked_finalization(
            None,
            code="POSTFLIGHT_INPUT_INVALID",
            message="payload deve ser mapping",
            handoff=handoff,
        )
    if not _enforced_route_ok(payload):
        return _blocked_finalization(
            payload,
            code="ENFORCED_ENTRYPOINT_MISSING",
            message=f"trace não comprova a rota L4 canônica {ENFORCED_ENTRYPOINT}",
            handoff=handoff,
        )

    root = Path(assistant_root) if assistant_root is not None else _resolve_assistant_root()
    skill_dir = root / "skills" / SKILL
    contract_path = skill_dir / "execution_contract.json"
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    try:
        runner = _load_runner(skill_dir)
        contract = _load_contract(contract_path)
        receipt_verification = runner.verify_receipt(payload, assistant_root=root)
        from hub_scripts.skill_execution.postflight import build_postflight

        postflight = build_postflight(
            payload,
            contract=contract,
            receipt_verification=receipt_verification,
            handoff=handoff,
        )
    except (RuntimeError, ValueError) as exc:
        return _blocked_finalization(
            payload,
            code="POSTFLIGHT_RUNTIME_ERROR",
            message=str(exc),
            handoff=handoff,
        )

    result = dict(payload)
    result["handoff"] = dict(handoff)
    result["postflight"] = postflight
    authorized = bool(
        postflight.get("status") == "PASS"
        and postflight.get("completion_authorized") is True
    )
    result["completion"] = {
        "authorized": authorized,
        "status": "COMPLETED" if authorized else "NOT_COMPLETED",
        "reason": "postflight PASS" if authorized else "postflight != PASS",
    }
    return result


def verify_finalized(
    final_payload: Mapping[str, Any],
    *,
    assistant_root: Path | str | None = None,
) -> dict[str, Any]:
    """Reverifica a finalização sem confiar no campo completion autodeclarado."""
    if not isinstance(final_payload, Mapping):
        return {
            "status": "MALFORMED",
            "valid": False,
            "issues": ["FINAL_PAYLOAD_NOT_MAPPING"],
            "completion_authorized": False,
            "completion_claim_consistent": False,
        }
    if not _enforced_route_ok(final_payload):
        return {
            "status": "BLOCKED",
            "valid": False,
            "issues": ["ENFORCED_ENTRYPOINT_MISSING"],
            "completion_authorized": False,
            "completion_claim_consistent": False,
        }

    root = Path(assistant_root) if assistant_root is not None else _resolve_assistant_root()
    skill_dir = root / "skills" / SKILL
    contract_path = skill_dir / "execution_contract.json"
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    try:
        runner = _load_runner(skill_dir)
        contract = _load_contract(contract_path)
        receipt_verification = runner.verify_receipt(final_payload, assistant_root=root)
        from hub_scripts.skill_execution.postflight import verify_postflight

        verification = verify_postflight(
            final_payload,
            contract=contract,
            receipt_verification=receipt_verification,
        ).to_dict()
    except (RuntimeError, ValueError) as exc:
        return {
            "status": "BLOCKED",
            "valid": False,
            "issues": [f"POSTFLIGHT_RUNTIME_ERROR:{exc}"],
            "completion_authorized": False,
            "completion_claim_consistent": False,
        }

    completion = final_payload.get("completion")
    declared_authorized = (
        isinstance(completion, Mapping)
        and completion.get("authorized") is True
        and completion.get("status") == "COMPLETED"
    )
    verification["completion_claim_consistent"] = bool(
        declared_authorized == verification.get("completion_authorized")
    )
    if not verification["completion_claim_consistent"]:
        verification["status"] = "INVALID"
        verification["valid"] = False
        verification["completion_authorized"] = False
        verification["issues"] = tuple(verification.get("issues", ())) + (
            "COMPLETION_CLAIM_MISMATCH",
        )
    return verification


def _load_json(raw: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} inválido: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} deve ser objeto JSON")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Postflight fail-closed SE05 da hub-ml-eda-profissional")
    parser.add_argument("--payload-json", required=True, help="payload JSON emitido pelo executor L4")
    parser.add_argument("--handoff-json", required=True, help="handoff final estruturado")
    args = parser.parse_args()

    try:
        payload = _load_json(args.payload_json, "payload-json")
        handoff = _load_json(args.handoff_json, "handoff-json")
        final_payload = finalize(payload, handoff)
    except (RuntimeError, ValueError) as exc:
        final_payload = _blocked_finalization(
            None,
            code="POSTFLIGHT_INPUT_INVALID",
            message=str(exc),
            handoff=None,
        )

    print(json.dumps(final_payload, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    completion = final_payload.get("completion")
    return 0 if isinstance(completion, Mapping) and completion.get("authorized") is True else 3


if __name__ == "__main__":
    raise SystemExit(main())
