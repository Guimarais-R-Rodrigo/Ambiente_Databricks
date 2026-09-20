from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PureWindowsPath
from typing import Any, Mapping


SKILL = "hub-ml-criar-objeto"
OBJECT_TYPES = {"snippet", "script", "prompt", "readme", "notebook", "skill"}
OPERATIONS = {"create", "convert"}
SNIPPET_SECTIONS = {"constants", "display", "ml", "spark", "testing", "visual"}
OVERLAP_RESOLUTIONS = {
    "extend_existing",
    "create_declared_slice",
    "convert_existing",
    "refuse",
}

TEMPLATES = {
    "snippet": "hub_padroes/snippet/template.md",
    "script": "hub_padroes/script/template.md",
    "prompt": "hub_padroes/prompt/template.md",
    "notebook": "hub_padroes/notebook/template.py",
    "skill": "hub_padroes/skill/template.md",
}
README_TEMPLATES = {
    "agregador": "hub_padroes/readme/template.md",
    "objeto": "hub_padroes/readme/template_objeto.md",
}

SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")
SKILL_NAME = re.compile(r"^hub-ml-[a-z0-9]+(?:-[a-z0-9]+)*$")


def _resolve_assistant_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == ".assistant":
            return parent
    raise RuntimeError("não foi possível localizar a raiz .assistant a partir do script")


def _issue(code: str, message: str, field: str) -> dict[str, str]:
    return {"code": code, "message": message, "field": field}


def _safe_relative(raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    text = raw.strip().replace("\\", "/")
    path = Path(text)
    # As entradas viajam entre Windows e Databricks: drive-relative e ADS
    # não podem virar paths relativos aparentemente seguros em outro host.
    if (path.is_absolute() or PureWindowsPath(text).drive or text.startswith("/")
            or ".." in path.parts or ":" in text or "\x00" in text):
        return None
    return path


def _contained_path(root: Path, relative: str | Path) -> Path | None:
    """Confere também links/junctions existentes, inclusive nos ancestrais."""
    safe = _safe_relative(str(relative))
    if safe is None:
        return None
    try:
        resolved_root = root.resolve()
        resolved = (resolved_root / safe).resolve()
    except (OSError, ValueError, RuntimeError):
        # Erros de resolução de path (incluindo loop de links), não do preflight.
        return None
    return resolved if resolved.is_relative_to(resolved_root) else None


def _invalid_input(message: str) -> dict[str, Any]:
    return {
        "schema_version": "SE07-CREATE-OBJECT-PREFLIGHT-1",
        "skill": SKILL,
        "status": "BLOCKED",
        "blocking_issues": [_issue("PREFLIGHT_INPUT_INVALID", message, "$")],
        "writes_performed": False,
        "tools_executed": [],
        "analytics_executed": False,
    }


def _load_context(raw: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"context-json inválido: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("context-json deve ser objeto JSON")
    return parsed


def _template_for(
    object_type: str,
    context: Mapping[str, Any],
    issues: list[dict[str, str]],
) -> str | None:
    if object_type != "readme":
        return TEMPLATES.get(object_type)

    scale = context.get("readme_scale")
    if not isinstance(scale, str) or scale not in README_TEMPLATES:
        issues.append(
            _issue(
                "README_SCALE_REQUIRED",
                "README exige readme_scale='agregador' ou 'objeto'",
                "readme_scale",
            )
        )
        return None
    return README_TEMPLATES[str(scale)]


def _destination_for(
    object_type: str,
    object_name: str,
    context: Mapping[str, Any],
    issues: list[dict[str, str]],
) -> str | None:
    if object_type == "snippet":
        section = context.get("snippet_section")
        if not isinstance(section, str) or not section:
            issues.append(
                _issue(
                    "SNIPPET_SECTION_REQUIRED",
                    "snippet exige snippet_section",
                    "snippet_section",
                )
            )
            return None
        section_path = _safe_relative(section)
        if (section_path is None or section in {".", ".."}
                or "/" in section or "\\" in section or not section_path.parts):
            issues.append(_issue(
                "SNIPPET_SECTION_INVALID",
                "snippet_section deve ser um único componente de caminho seguro",
                "snippet_section",
            ))
            return None
        if section not in SNIPPET_SECTIONS and context.get("new_snippet_section_authorized") is not True:
            issues.append(
                _issue(
                    "NEW_SNIPPET_SECTION_REQUIRES_DECISION",
                    f"seção nova {section!r} exige decisão explícita",
                    "new_snippet_section_authorized",
                )
            )
            return None
        return f"hub_snippets/{section}/{object_name}"

    if object_type == "script":
        return f"hub_scripts/{object_name}"

    if object_type == "prompt":
        return f"hub_prompts/{object_name}"

    if object_type == "skill":
        return f"skills/{object_name}"

    raw_destination = context.get("destination_relative")
    destination = _safe_relative(raw_destination)
    if destination is None:
        issues.append(
            _issue(
                "DESTINATION_REQUIRED",
                f"{object_type} exige destination_relative seguro",
                "destination_relative",
            )
        )
        return None

    text = destination.as_posix()
    if object_type == "readme" and destination.name != "README.md":
        issues.append(
            _issue(
                "README_DESTINATION_INVALID",
                "destino de README deve terminar em README.md",
                "destination_relative",
            )
        )
    if object_type == "notebook" and destination.suffix != ".py":
        issues.append(
            _issue(
                "NOTEBOOK_DESTINATION_INVALID",
                "destino de notebook deve terminar em .py",
                "destination_relative",
            )
        )
    return text


def _validate_name(
    object_type: str,
    object_name: str,
    issues: list[dict[str, str]],
) -> None:
    if object_type in {"snippet", "script", "prompt"} and not SNAKE_CASE.fullmatch(object_name):
        issues.append(
            _issue(
                "OBJECT_NAME_INVALID",
                f"{object_type} exige nome snake_case",
                "object_name",
            )
        )
    elif object_type == "skill" and not SKILL_NAME.fullmatch(object_name):
        issues.append(
            _issue(
                "OBJECT_NAME_INVALID",
                "skill exige nome hub-ml-<tema> em minúsculas e hífens",
                "object_name",
            )
        )


def preflight(context: Mapping[str, Any]) -> dict[str, Any]:
    """Resolve forma e destino do objeto sem criar ou alterar arquivos."""
    if not isinstance(context, Mapping):
        return _invalid_input("context deve ser objeto JSON/mapping")
    root = _resolve_assistant_root()
    issues: list[dict[str, str]] = []

    operation = context.get("operation")
    if not isinstance(operation, str) or operation not in OPERATIONS:
        issues.append(
            _issue(
                "OPERATION_INVALID",
                "operation deve ser 'create' ou 'convert'",
                "operation",
            )
        )

    object_type = context.get("object_type")
    if not isinstance(object_type, str) or object_type not in OBJECT_TYPES:
        issues.append(
            _issue(
                "OBJECT_TYPE_INVALID",
                "object_type deve ser um dos seis tipos fechados",
                "object_type",
            )
        )
        object_type = None

    object_name = context.get("object_name")
    if not isinstance(object_name, str) or not object_name.strip():
        issues.append(
            _issue(
                "OBJECT_NAME_REQUIRED",
                "object_name deve ser string não vazia",
                "object_name",
            )
        )
        object_name = ""
    else:
        object_name = object_name.strip()

    if context.get("type_confirmed") is not True:
        issues.append(
            _issue(
                "OBJECT_TYPE_NOT_CONFIRMED",
                "o tipo deve ser confirmado antes de escrever",
                "type_confirmed",
            )
        )

    if context.get("existing_capability_checked") is not True:
        issues.append(
            _issue(
                "EXISTING_CAPABILITY_CHECK_REQUIRED",
                "é obrigatório registrar a checagem de capacidade existente",
                "existing_capability_checked",
            )
        )

    capability_status = context.get("existing_capability_status")
    if not isinstance(capability_status, str) or capability_status not in {"not_found", "found"}:
        issues.append(
            _issue(
                "EXISTING_CAPABILITY_STATUS_INVALID",
                "existing_capability_status deve ser 'not_found' ou 'found'",
                "existing_capability_status",
            )
        )

    overlap_resolution = context.get("overlap_resolution")
    if capability_status == "found":
        if not isinstance(overlap_resolution, str) or overlap_resolution not in OVERLAP_RESOLUTIONS:
            issues.append(
                _issue(
                    "OVERLAP_RESOLUTION_REQUIRED",
                    "capacidade existente exige decisão explícita de sobreposição",
                    "overlap_resolution",
                )
            )
        elif operation == "create" and overlap_resolution != "create_declared_slice":
            issues.append(
                _issue(
                    "NEW_OBJECT_NOT_AUTHORIZED_BY_OVERLAP_DECISION",
                    f"decisão {overlap_resolution!r} não autoriza objeto novo",
                    "overlap_resolution",
                )
            )
        elif operation == "convert" and overlap_resolution != "convert_existing":
            issues.append(
                _issue(
                    "CONVERSION_NOT_AUTHORIZED_BY_OVERLAP_DECISION",
                    "conversão exige overlap_resolution='convert_existing'",
                    "overlap_resolution",
                )
            )

    if operation == "convert" and capability_status == "not_found":
        issues.append(
            _issue(
                "CONVERSION_SOURCE_NOT_IDENTIFIED",
                "conversão exige capacidade/origem existente identificada",
                "existing_capability_status",
            )
        )

    if isinstance(object_type, str) and object_name:
        _validate_name(object_type, object_name, issues)

    template_rel = (
        _template_for(object_type, context, issues)
        if isinstance(object_type, str)
        else None
    )
    destination_rel = (
        _destination_for(object_type, object_name, context, issues)
        if isinstance(object_type, str) and object_name
        else None
    )

    template_exists = False
    if template_rel is not None:
        template_path = _contained_path(root, template_rel)
        template_exists = template_path is not None and template_path.is_file()
        if not template_exists:
            issues.append(
                _issue(
                    "CANONICAL_TEMPLATE_NOT_FOUND",
                    f"template canônico não encontrado: {template_rel}",
                    "object_type",
                )
            )

    destination_exists = None
    destination_path = None
    if destination_rel is not None:
        destination_path = _contained_path(root, destination_rel)
        if destination_path is None:
            issues.append(_issue(
                "DESTINATION_REQUIRED",
                "destino deve resolver dentro da raiz .assistant",
                "destination_relative",
            ))
        else:
            destination_exists = destination_path.exists()
        if operation == "create" and destination_exists:
            issues.append(
                _issue(
                    "DESTINATION_ALREADY_EXISTS",
                    f"destino já existe: {destination_rel}",
                    "destination_relative",
                )
            )

    source_rel = None
    source_exists = None
    if operation == "convert":
        source = _safe_relative(context.get("source_relative"))
        source_path = _contained_path(root, source) if source is not None else None
        if source_path is None:
            issues.append(
                _issue(
                    "CONVERSION_SOURCE_REQUIRED",
                    "conversão exige source_relative seguro dentro da raiz .assistant",
                    "source_relative",
                )
            )
        else:
            source_rel = source.as_posix()
            source_exists = source_path.exists()
            if not source_exists:
                issues.append(
                    _issue(
                        "CONVERSION_SOURCE_NOT_FOUND",
                        f"origem da conversão não existe: {source_rel}",
                        "source_relative",
                    )
                )
            if destination_path is not None and (
                source_path == destination_path
                or (source_exists and destination_exists and source_path.samefile(destination_path))
            ):
                issues.append(
                    _issue(
                        "CONVERSION_MUST_MOVE",
                        "conversão deve mover para destino distinto; não é alteração comportamental in-place",
                        "destination_relative",
                    )
                )

    return {
        "schema_version": "SE07-CREATE-OBJECT-PREFLIGHT-1",
        "skill": SKILL,
        "status": "BLOCKED" if issues else "PASS",
        "operation": operation,
        "object_type": object_type,
        "object_name": object_name or None,
        "template": {
            "path": template_rel,
            "resolved": bool(template_rel and template_exists),
            "read_status": "NOT_OBSERVABLE",
        },
        "destination_relative": destination_rel,
        "destination_exists": destination_exists,
        "source_relative": source_rel,
        "source_exists": source_exists,
        "conversion_behavior_preservation_required": operation == "convert",
        "blocking_issues": issues,
        "writes_performed": False,
        "tools_executed": [],
        "analytics_executed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight L2 somente leitura da hub-ml-criar-objeto")
    parser.add_argument("--context-json", required=True)
    args = parser.parse_args()

    try:
        context = _load_context(args.context_json)
    except ValueError as exc:
        payload = _invalid_input(str(exc))
    else:
        # Uma falha inesperada de implementação deve continuar visível.
        payload = preflight(context)

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
