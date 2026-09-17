#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valida contratos estruturados de execução de Agent Skills do SEF.

SE01 implementa somente o nível L1 (Contract), em modo ``audit``. Este módulo
não executa helpers, não faz preflight e não altera o comportamento das skills.
A resolução é estática e compartilha com o preflight L2 a mesma semântica de
fachada pública, sem importar os helpers analíticos alvo.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

SUPPORTED_SCHEMA_VERSIONS = {"0.1"}
SUPPORTED_POLICIES = {"required", "conditional", "optional"}
SUPPORTED_EVIDENCE = {
    "resolved",
    "loaded",
    "imported",
    "call",
    "result",
    "decision",
    "authorization",
}
SUPPORTED_MODES = {"audit"}
SUPPORTED_CONDITIONS = {
    "local_sample_required": {"value": False},
    "tabular_preview_required": {"value": False},
    "numeric_columns_at_least": {"value": True},
    "numeric_distributions_requested": {"value": False},
    "resolved_theme_selected": {"value": False},
    "visual_diagnostics_requested": {"value": False},
}

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ASSISTANT = REPO_ROOT / "ambiente_fonte" / ".assistant"
SKILLS_ROOT = SOURCE_ASSISTANT / "skills"

if str(SOURCE_ASSISTANT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ASSISTANT))

from hub_scripts.skill_execution.skill_execution import (  # noqa: E402
    canonical_module_parts,
    public_exports,
)


@dataclass(frozen=True)
class ContractIssue:
    code: str
    message: str
    location: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ContractValidation:
    path: str
    skill: str | None
    schema_version: str | None
    mode: str | None
    resources: int
    templates: int
    issues: tuple[ContractIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "skill": self.skill,
            "schema_version": self.schema_version,
            "mode": self.mode,
            "resources": self.resources,
            "templates": self.templates,
            "ok": self.ok,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def _issue(code: str, message: str, location: str) -> ContractIssue:
    return ContractIssue(code=code, message=message, location=location)


def _validate_condition(
    condition: Any, location: str, issues: list[ContractIssue]
) -> None:
    if not isinstance(condition, dict):
        issues.append(_issue("CONDITION_INVALID", "condition deve ser objeto", location))
        return

    allowed = {"kind", "value"}
    extras = sorted(set(condition) - allowed)
    if extras:
        issues.append(
            _issue(
                "CONDITION_INVALID",
                f"campos não suportados em condition: {', '.join(extras)}",
                location,
            )
        )

    kind = condition.get("kind")
    if kind not in SUPPORTED_CONDITIONS:
        issues.append(
            _issue(
                "CONDITION_INVALID",
                f"condition.kind não suportado: {kind!r}",
                location,
            )
        )
        return

    requires_value = SUPPORTED_CONDITIONS[kind]["value"]
    if requires_value:
        value = condition.get("value")
        if not isinstance(value, int) or isinstance(value, bool) or value < 2:
            issues.append(
                _issue(
                    "CONDITION_INVALID",
                    "numeric_columns_at_least exige value inteiro >= 2",
                    location,
                )
            )
    elif "value" in condition:
        issues.append(
            _issue(
                "CONDITION_INVALID",
                f"{kind} não aceita campo value",
                location,
            )
        )


def _validate_resource(
    resource: Any,
    *,
    index: int,
    seen_ids: set[str],
    assistant_root: Path,
    issues: list[ContractIssue],
) -> None:
    location = f"resources[{index}]"
    if not isinstance(resource, dict):
        issues.append(_issue("RESOURCE_INVALID", "recurso deve ser objeto", location))
        return

    allowed = {"id", "module", "symbol", "policy", "evidence", "condition"}
    required = {"id", "module", "symbol", "policy", "evidence"}
    extras = sorted(set(resource) - allowed)
    missing = sorted(required - set(resource))
    if extras:
        issues.append(
            _issue(
                "RESOURCE_INVALID",
                f"campos não suportados: {', '.join(extras)}",
                location,
            )
        )
    if missing:
        issues.append(
            _issue(
                "RESOURCE_INVALID",
                f"campos obrigatórios ausentes: {', '.join(missing)}",
                location,
            )
        )
        return

    rid = resource.get("id")
    if not isinstance(rid, str) or not rid.strip():
        issues.append(_issue("RESOURCE_INVALID", "id deve ser string não vazia", location))
    elif rid in seen_ids:
        issues.append(_issue("RESOURCE_DUPLICATE", f"id duplicado: {rid}", location))
    else:
        seen_ids.add(rid)

    policy = resource.get("policy")
    if policy not in SUPPORTED_POLICIES:
        issues.append(
            _issue("POLICY_INVALID", f"policy não suportada: {policy!r}", location)
        )

    evidence = resource.get("evidence")
    if evidence not in SUPPORTED_EVIDENCE:
        issues.append(
            _issue(
                "EVIDENCE_INVALID", f"evidence não suportada: {evidence!r}", location
            )
        )

    if policy == "conditional":
        if "condition" not in resource:
            issues.append(
                _issue(
                    "CONDITION_REQUIRED",
                    "recurso conditional exige condition objetiva",
                    location,
                )
            )
        else:
            _validate_condition(resource["condition"], f"{location}.condition", issues)
    elif "condition" in resource:
        issues.append(
            _issue(
                "CONDITION_UNEXPECTED",
                "condition só é permitida para policy=conditional",
                location,
            )
        )

    module = resource.get("module")
    symbol = resource.get("symbol")
    module_parts = canonical_module_parts(module)
    if module_parts is None:
        issues.append(
            _issue(
                "RESOURCE_MODULE_INVALID",
                f"module deve ser caminho Python canônico sob hub_snippets.* ou hub_scripts.*: {module!r}",
                location,
            )
        )
        return
    if not isinstance(symbol, str) or not symbol or not symbol.isidentifier():
        issues.append(
            _issue(
                "RESOURCE_INVALID",
                "symbol deve ser identificador público Python simples",
                location,
            )
        )
        return

    package_dir = assistant_root.joinpath(*module_parts)
    init_path = package_dir / "__init__.py"
    if not package_dir.is_dir() or not init_path.is_file():
        issues.append(
            _issue(
                "RESOURCE_MODULE_NOT_FOUND",
                f"fachada pública ausente para {module}: esperado {init_path}",
                location,
            )
        )
        return

    try:
        exports = public_exports(init_path)
    except ValueError as exc:
        issues.append(_issue("RESOURCE_MODULE_UNREADABLE", str(exc), location))
        return
    if symbol not in exports:
        issues.append(
            _issue(
                "RESOURCE_SYMBOL_NOT_EXPORTED",
                f"{module}.{symbol} não está na API pública efetiva de {init_path}",
                location,
            )
        )


def _validate_template(
    template: Any,
    *,
    index: int,
    seen_ids: set[str],
    skill_dir: Path,
    issues: list[ContractIssue],
) -> None:
    location = f"templates[{index}]"
    if not isinstance(template, dict):
        issues.append(_issue("TEMPLATE_INVALID", "template deve ser objeto", location))
        return

    allowed = {"id", "path", "policy", "evidence", "condition"}
    required = {"id", "path", "policy", "evidence"}
    extras = sorted(set(template) - allowed)
    missing = sorted(required - set(template))
    if extras:
        issues.append(
            _issue(
                "TEMPLATE_INVALID",
                f"campos não suportados: {', '.join(extras)}",
                location,
            )
        )
    if missing:
        issues.append(
            _issue(
                "TEMPLATE_INVALID",
                f"campos obrigatórios ausentes: {', '.join(missing)}",
                location,
            )
        )
        return

    tid = template.get("id")
    if not isinstance(tid, str) or not tid.strip():
        issues.append(_issue("TEMPLATE_INVALID", "id deve ser string não vazia", location))
    elif tid in seen_ids:
        issues.append(_issue("TEMPLATE_DUPLICATE", f"id duplicado: {tid}", location))
    else:
        seen_ids.add(tid)

    policy = template.get("policy")
    if policy not in SUPPORTED_POLICIES:
        issues.append(
            _issue("POLICY_INVALID", f"policy não suportada: {policy!r}", location)
        )

    evidence = template.get("evidence")
    if evidence != "loaded":
        issues.append(
            _issue(
                "EVIDENCE_INVALID",
                "templates v0.1 exigem evidence='loaded'",
                location,
            )
        )

    if policy == "conditional":
        if "condition" not in template:
            issues.append(
                _issue(
                    "CONDITION_REQUIRED",
                    "template conditional exige condition objetiva",
                    location,
                )
            )
        else:
            _validate_condition(template["condition"], f"{location}.condition", issues)
    elif "condition" in template:
        issues.append(
            _issue(
                "CONDITION_UNEXPECTED",
                "condition só é permitida para policy=conditional",
                location,
            )
        )

    rel = template.get("path")
    if (
        not isinstance(rel, str)
        or not rel.endswith(".md")
        or rel.startswith(("/", "\\"))
        or ".." in Path(rel).parts
    ):
        issues.append(
            _issue(
                "TEMPLATE_PATH_INVALID",
                f"path deve ser Markdown relativo à pasta da skill: {rel!r}",
                location,
            )
        )
        return

    target = skill_dir / rel
    if not target.is_file():
        issues.append(
            _issue(
                "TEMPLATE_NOT_FOUND",
                f"template não encontrado: {target}",
                location,
            )
        )


def validate_contract(
    contract_path: Path | str,
    *,
    assistant_root: Path | None = None,
) -> ContractValidation:
    contract_path = Path(contract_path)
    assistant_root = Path(assistant_root) if assistant_root else SOURCE_ASSISTANT
    issues: list[ContractIssue] = []

    try:
        raw = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ContractValidation(
            path=str(contract_path),
            skill=None,
            schema_version=None,
            mode=None,
            resources=0,
            templates=0,
            issues=(
                _issue("CONTRACT_UNREADABLE", f"contrato inválido: {exc}", "$"),
            ),
        )

    if not isinstance(raw, dict):
        return ContractValidation(
            path=str(contract_path),
            skill=None,
            schema_version=None,
            mode=None,
            resources=0,
            templates=0,
            issues=(_issue("CONTRACT_UNREADABLE", "raiz deve ser objeto JSON", "$"),),
        )

    allowed_root = {
        "schema_version",
        "skill",
        "mode",
        "metadata",
        "resources",
        "templates",
    }
    extras = sorted(set(raw) - allowed_root)
    if extras:
        issues.append(
            _issue(
                "CONTRACT_FIELDS_UNSUPPORTED",
                f"campos raiz não suportados: {', '.join(extras)}",
                "$",
            )
        )

    schema_version = raw.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        issues.append(
            _issue(
                "SCHEMA_VERSION_UNSUPPORTED",
                f"schema_version não suportada: {schema_version!r}",
                "schema_version",
            )
        )

    skill = raw.get("skill")
    if not isinstance(skill, str) or not skill.startswith("hub-ml-"):
        issues.append(_issue("SKILL_INVALID", f"skill inválida: {skill!r}", "skill"))

    skill_dir = contract_path.parent
    if isinstance(skill, str) and skill_dir.name != skill:
        issues.append(
            _issue(
                "SKILL_FOLDER_MISMATCH",
                f"contrato declara {skill!r}, mas está em {skill_dir.name!r}",
                "skill",
            )
        )

    mode = raw.get("mode")
    if mode not in SUPPORTED_MODES:
        issues.append(
            _issue(
                "MODE_INVALID",
                f"SE01 aceita somente mode='audit'; recebido {mode!r}",
                "mode",
            )
        )

    metadata = raw.get("metadata", {})
    if not isinstance(metadata, dict):
        issues.append(_issue("METADATA_INVALID", "metadata deve ser objeto", "metadata"))

    resources = raw.get("resources")
    if not isinstance(resources, list):
        issues.append(_issue("RESOURCES_INVALID", "resources deve ser array", "resources"))
        resources = []

    templates = raw.get("templates")
    if not isinstance(templates, list):
        issues.append(_issue("TEMPLATES_INVALID", "templates deve ser array", "templates"))
        templates = []

    seen_resources: set[str] = set()
    for idx, resource in enumerate(resources):
        _validate_resource(
            resource,
            index=idx,
            seen_ids=seen_resources,
            assistant_root=assistant_root,
            issues=issues,
        )

    seen_templates: set[str] = set()
    for idx, template in enumerate(templates):
        _validate_template(
            template,
            index=idx,
            seen_ids=seen_templates,
            skill_dir=skill_dir,
            issues=issues,
        )

    return ContractValidation(
        path=str(contract_path),
        skill=skill if isinstance(skill, str) else None,
        schema_version=schema_version if isinstance(schema_version, str) else None,
        mode=mode if isinstance(mode, str) else None,
        resources=len(resources),
        templates=len(templates),
        issues=tuple(issues),
    )


def discover_contracts(skills_root: Path = SKILLS_ROOT) -> list[Path]:
    return sorted(skills_root.glob("*/execution_contract.json"))


def validate_many(paths: Iterable[Path]) -> list[ContractValidation]:
    return [validate_contract(path) for path in paths]


def _format_human(results: list[ContractValidation]) -> str:
    lines: list[str] = []
    for result in results:
        verdict = "PASS" if result.ok else "FAIL"
        lines.append(
            f"{verdict} {result.path} "
            f"(skill={result.skill!r}, resources={result.resources}, templates={result.templates})"
        )
        for issue in result.issues:
            lines.append(f"  - {issue.code} @ {issue.location}: {issue.message}")
    passed = sum(result.ok for result in results)
    lines.append(f"Resumo: {passed}/{len(results)} contratos válidos.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Valida execution_contract.json sem importar ou executar helpers."
    )
    parser.add_argument(
        "--contract",
        action="append",
        type=Path,
        help="Contrato específico; pode ser repetido. Sem a flag, descobre skills/*/execution_contract.json.",
    )
    parser.add_argument("--json", action="store_true", help="Emite resultado JSON.")
    args = parser.parse_args(argv)

    paths = args.contract if args.contract else discover_contracts()
    if not paths:
        payload = {
            "ok": False,
            "code": "NO_CONTRACTS",
            "message": f"nenhum execution_contract.json em {SKILLS_ROOT}",
        }
        print(
            json.dumps(payload, ensure_ascii=False, indent=2)
            if args.json
            else payload["message"]
        )
        return 2

    results = validate_many(paths)
    if args.json:
        print(
            json.dumps(
                {
                    "ok": all(result.ok for result in results),
                    "schema_versions_supported": sorted(SUPPORTED_SCHEMA_VERSIONS),
                    "results": [result.to_dict() for result in results],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(_format_human(results))
    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
