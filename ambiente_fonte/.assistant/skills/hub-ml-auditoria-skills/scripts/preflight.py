from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


SKILL = "hub-ml-auditoria-skills"
VALID_MODES = {"OUTPUT", "IMPLEMENTACAO"}


def _resolve_assistant_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".assistant":
            return parent
    raise RuntimeError("não foi possível localizar a raiz .assistant a partir do script")


def _normalize_mode(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip().upper()
    aliases = {
        "OUTPUT": "OUTPUT",
        "IMPLEMENTACAO": "IMPLEMENTACAO",
        "IMPLEMENTAÇÃO": "IMPLEMENTACAO",
    }
    return aliases.get(normalized)


def _issue(code: str, message: str, field: str) -> dict[str, str]:
    return {"code": code, "message": message, "field": field}


def _load_context(raw: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"context-json inválido: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("context-json deve ser objeto JSON")
    return parsed


def _skill_exists(assistant_root: Path, skill: str) -> bool:
    return (assistant_root / "skills" / skill / "SKILL.md").is_file()


def preflight(context: Mapping[str, Any]) -> dict[str, Any]:
    """Resolve pré-condições da auditoria sem executar análise, verifier ou escrita."""
    assistant_root = _resolve_assistant_root()
    assistant_root_text = str(assistant_root)
    if assistant_root_text not in sys.path:
        sys.path.insert(0, assistant_root_text)

    from hub_scripts.skill_execution import (
        EnforcementPolicyError,
        get_skill_enforcement_policy,
    )

    issues: list[dict[str, str]] = []
    gaps: list[dict[str, str]] = []
    mode = _normalize_mode(context.get("audit_mode"))
    producer_skill: str | None = None
    target_skills: list[str] = []
    producer_policy: dict[str, Any] | None = None

    if mode is None:
        issues.append(
            _issue(
                "AUDIT_MODE_INVALID",
                "audit_mode deve ser OUTPUT ou IMPLEMENTACAO",
                "audit_mode",
            )
        )
    elif mode == "OUTPUT":
        raw_producer = context.get("producer_skill")
        if not isinstance(raw_producer, str) or not raw_producer.strip():
            issues.append(
                _issue(
                    "PRODUCER_SKILL_REQUIRED",
                    "Modo OUTPUT exige producer_skill explícita",
                    "producer_skill",
                )
            )
        else:
            producer_skill = raw_producer.strip()
            if not _skill_exists(assistant_root, producer_skill):
                issues.append(
                    _issue(
                        "PRODUCER_SKILL_NOT_FOUND",
                        f"SKILL.md da produtora não encontrado: {producer_skill}",
                        "producer_skill",
                    )
                )
            else:
                try:
                    policy = get_skill_enforcement_policy(
                        producer_skill,
                        assistant_root=assistant_root,
                    )
                    producer_policy = {
                        "resolution": "RESOLVED",
                        "current_level": policy.current_level,
                        "target_level": policy.target_level,
                        "rollout_mode": policy.rollout_mode,
                    }
                except EnforcementPolicyError as exc:
                    gaps.append(
                        _issue(
                            "PRODUCER_SEF_POLICY_NOT_REGISTERED",
                            str(exc),
                            "producer_skill",
                        )
                    )
                    producer_policy = {"resolution": "NOT_REGISTERED"}

        for field, code, label in (
            (
                "original_request_present",
                "ORIGINAL_REQUEST_REQUIRED",
                "pedido original",
            ),
            (
                "artifact_present",
                "AUDIT_ARTIFACT_REQUIRED",
                "artefato auditado",
            ),
        ):
            value = context.get(field)
            if value is not True:
                issues.append(
                    _issue(
                        code,
                        f"Modo OUTPUT exige {label} observável",
                        field,
                    )
                )

    elif mode == "IMPLEMENTACAO":
        raw_targets = context.get("target_skills")
        if not isinstance(raw_targets, list) or not raw_targets:
            issues.append(
                _issue(
                    "TARGET_SKILLS_REQUIRED",
                    "Modo IMPLEMENTACAO exige target_skills não vazio",
                    "target_skills",
                )
            )
        elif any(not isinstance(item, str) or not item.strip() for item in raw_targets):
            issues.append(
                _issue(
                    "TARGET_SKILLS_INVALID",
                    "target_skills deve conter somente strings não vazias",
                    "target_skills",
                )
            )
        else:
            target_skills = [item.strip() for item in raw_targets]
            missing = [
                item for item in target_skills if not _skill_exists(assistant_root, item)
            ]
            for item in missing:
                issues.append(
                    _issue(
                        "TARGET_SKILL_NOT_FOUND",
                        f"SKILL.md não encontrado: {item}",
                        "target_skills",
                    )
                )

    return {
        "schema_version": "SE07-AUDIT-PREFLIGHT-1",
        "skill": SKILL,
        "audit_mode": mode,
        "status": "BLOCKED" if issues else "PASS",
        "producer_skill": producer_skill,
        "producer_policy": producer_policy,
        "target_skills": target_skills,
        "blocking_issues": issues,
        "evidence_gaps": gaps,
        "writes_performed": False,
        "analytics_executed": False,
        "verifier_executed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preflight L2 somente leitura da skill hub-ml-auditoria-skills"
    )
    parser.add_argument("--context-json", required=True)
    args = parser.parse_args()

    try:
        context = _load_context(args.context_json)
        payload = preflight(context)
    except (RuntimeError, ValueError) as exc:
        payload = {
            "schema_version": "SE07-AUDIT-PREFLIGHT-1",
            "skill": SKILL,
            "status": "BLOCKED",
            "blocking_issues": [
                _issue("PREFLIGHT_INPUT_INVALID", str(exc), "$")
            ],
            "evidence_gaps": [],
            "writes_performed": False,
            "analytics_executed": False,
            "verifier_executed": False,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
