"""V11 — projeção fail-closed do Sistema de Temas para Databricks AI/BI.

Este módulo não chama Databricks, não publica dashboards e não inventa o schema
do JSON nativo de tema. Ele parte exclusivamente de um ``ResolvedTheme`` íntegro,
classifica a correspondência das capacidades e, opcionalmente, aplica apenas
mapeamentos diretos a um template nativo explicitamente exportado e fixado por
SHA-256 com um binding revisado.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from hub_snippets.visual.tema import ResolvedTheme, export_theme, resolve_theme

_MAX_BYTES = 262_144
_MAPPING_SHA256 = "98dba3149203a174c7ef76f5aac5636e9c3ab34fcd37ae120200347da831996f"
_ALLOWED_CLASSES = {"translated", "approximated", "unsupported"}
_ALLOWED_BINDING = {"direct", "manual", "none"}
_POINTER_RE = re.compile(r"^(?:/(?:[^~/]|~[01])*)+$")


class AibiThemeError(ValueError):
    """Erro seguro do bridge V11, sem ecoar conteúdo arbitrário da entrada."""

    def __init__(self, code: str, message: str, *, action: str = "Revise a matriz V11 e tente novamente."):
        self.code = code
        self.action = action
        super().__init__(f"{code}: {message} {action}")


def _fail(code: str, message: str, *, action: str = "Revise a matriz V11 e tente novamente.") -> None:
    raise AibiThemeError(code, message, action=action) from None


def _copy_json(value: Any, *, depth: int = 0) -> Any:
    if depth > 20:
        _fail("AIBI_JSON_DEPTH", "O JSON excede o limite de profundidade.")
    if type(value) is dict:
        result: dict[str, Any] = {}
        for key, item in value.items():
            if type(key) is not str or key in result:
                _fail("AIBI_JSON_OBJECT", "O objeto JSON contém chave inválida ou duplicada.")
            result[key] = _copy_json(item, depth=depth + 1)
        return result
    if type(value) is list:
        return [_copy_json(item, depth=depth + 1) for item in value]
    if type(value) is str:
        if len(value.encode("utf-8")) > _MAX_BYTES:
            _fail("AIBI_JSON_SIZE", "Um texto excede o limite permitido.")
        return value
    if type(value) is int or value is None or type(value) is bool:
        return value
    if type(value) is float:
        if not math.isfinite(value):
            _fail("AIBI_JSON_NUMBER", "Números precisam ser finitos.")
        return value
    _fail("AIBI_JSON_TYPE", "Use somente tipos JSON simples.")


def _strict_json(raw: bytes) -> Any:
    if type(raw) is not bytes:
        _fail("AIBI_JSON_INPUT", "Forneça bytes UTF-8.")
    if len(raw) > _MAX_BYTES:
        _fail("AIBI_JSON_SIZE", "O arquivo excede 262.144 bytes.")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        _fail("AIBI_JSON_ENCODING", "Use UTF-8 sem BOM.")
    if text.startswith("\ufeff"):
        _fail("AIBI_JSON_ENCODING", "Use UTF-8 sem BOM.")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                _fail("AIBI_JSON_DUPLICATE", "Uma propriedade foi declarada mais de uma vez.")
            result[key] = value
        return result

    def constant(_):
        _fail("AIBI_JSON_NUMBER", "NaN e infinito não são aceitos.")

    try:
        parsed = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, RecursionError) as exc:
        if isinstance(exc, AibiThemeError):
            raise
        _fail("AIBI_JSON_SYNTAX", "O JSON não pôde ser interpretado.")
    return _copy_json(parsed)


def _canonical(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _mapping_path() -> Path:
    return Path(__file__).absolute().with_name("aibi_mapping.json")


def _load_mapping() -> dict[str, Any]:
    raw = _mapping_path().read_bytes()
    if hashlib.sha256(raw).hexdigest() != _MAPPING_SHA256:
        _fail(
            "AIBI_MAPPING_HASH",
            "A matriz de correspondência difere da versão esperada.",
            action="Restaure fonte e espelho; não ajuste o hash para esconder divergência.",
        )
    value = _strict_json(raw)
    if type(value) is not dict or value.get("contract_version") != 1:
        _fail("AIBI_MAPPING_CONTRACT", "A matriz não atende ao contrato V11.")
    if value.get("source_context") != "notebook":
        _fail("AIBI_MAPPING_CONTEXT", "A matriz V11 deve partir do contexto notebook.")
    capabilities = value.get("capabilities")
    rows = value.get("mappings")
    if type(capabilities) is not dict or type(rows) is not list or len(rows) != 48:
        _fail("AIBI_MAPPING_SHAPE", "A matriz precisa declarar capacidades e 48 tokens.")
    seen: set[str] = set()
    for row in rows:
        if type(row) is not dict:
            _fail("AIBI_MAPPING_SHAPE", "Cada linha da matriz precisa ser um objeto.")
        token = row.get("hub_token")
        classification = row.get("classification")
        target = row.get("target_capability")
        strategy = row.get("binding_strategy")
        if type(token) is not str or token in seen:
            _fail("AIBI_MAPPING_TOKEN", "Token ausente ou duplicado na matriz.")
        seen.add(token)
        if classification not in _ALLOWED_CLASSES or strategy not in _ALLOWED_BINDING:
            _fail("AIBI_MAPPING_CLASS", "Classificação ou estratégia de binding inválida.")
        if classification == "unsupported":
            if target is not None or strategy != "none":
                _fail("AIBI_MAPPING_UNSUPPORTED", "Token não suportado não pode receber alvo ou binding.")
        else:
            if type(target) is not str or target not in capabilities:
                _fail("AIBI_MAPPING_TARGET", "Capacidade-alvo não registrada.")
        if classification != "translated" and strategy == "direct":
            _fail("AIBI_MAPPING_DIRECT", "Somente correspondências traduzidas podem ser aplicadas automaticamente.")
    return value


@dataclass(frozen=True)
class AibiThemeProjection:
    """Projeção auditável. Não é JSON nativo de importação do Databricks."""

    source_theme_id: str
    source_theme_version: str
    source_fingerprint: str
    source_content_sha256: str
    source_mode: str
    mappings: tuple[Mapping[str, Any], ...] = field(repr=False)
    mapping_sha256: str = _MAPPING_SHA256
    native_schema_status: str = "unverified"
    native_import_ready: bool = False
    warnings: tuple[str, ...] = (
        "AIBI_NATIVE_JSON_SCHEMA_UNVERIFIED",
        "AIBI_NO_WORKSPACE_MUTATION",
        "AIBI_APPROXIMATIONS_REQUIRE_REVIEW",
    )

    def to_dict(self) -> dict[str, Any]:
        rows = [dict(row) for row in self.mappings]
        counts = {name: sum(1 for row in rows if row["classification"] == name) for name in sorted(_ALLOWED_CLASSES)}
        return {
            "format": "hub-aibi-theme-projection",
            "version": 1,
            "source": {
                "theme_id": self.source_theme_id,
                "theme_version": self.source_theme_version,
                "fingerprint": self.source_fingerprint,
                "content_sha256": self.source_content_sha256,
                "context": "notebook",
                "mode": self.source_mode,
            },
            "target": {
                "product": "Databricks AI/BI dashboards",
                "native_schema_status": self.native_schema_status,
                "native_import_ready": self.native_import_ready,
            },
            "mapping_sha256": self.mapping_sha256,
            "summary": counts,
            "mappings": rows,
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class AibiNativeCandidate:
    """Bytes derivados de template fixado; ainda não homologados pelo Databricks."""

    content: bytes = field(repr=False)
    template_sha256: str
    candidate_sha256: str
    applied_capabilities: tuple[str, ...]
    omitted_capabilities: tuple[str, ...]
    validation_status: str = "locally_bound_not_databricks_validated"


def project_theme(theme: ResolvedTheme) -> AibiThemeProjection:
    """Traduz um tema notebook íntegro para uma matriz AI/BI auditável."""
    if type(theme) is not ResolvedTheme:
        _fail("AIBI_THEME_TYPE", "Forneça um ResolvedTheme produzido pelo núcleo V02.")
    canonical = export_theme(theme)
    verified = resolve_theme(canonical, expected_context="notebook")
    if verified.fingerprint != theme.fingerprint:
        _fail("AIBI_THEME_INTEGRITY", "O tema não corresponde ao fingerprint revalidado.")
    source = verified.to_dict()
    mapping = _load_mapping()
    source_tokens = source["tokens"]
    rows = mapping["mappings"]
    expected = {row["hub_token"] for row in rows}
    if set(source_tokens) != expected:
        _fail(
            "AIBI_TOKEN_COVERAGE",
            "A matriz V11 não cobre exatamente os tokens do tema notebook.",
            action="Atualize a matriz de forma explícita; não ignore tokens novos.",
        )
    projected = []
    for row in rows:
        item = dict(row)
        token = item["hub_token"]
        item["source_value"] = _copy_json(source_tokens[token])
        projected.append(MappingProxyType(item))
    return AibiThemeProjection(
        source_theme_id=source["theme_id"],
        source_theme_version=source["theme_version"],
        source_fingerprint=verified.fingerprint,
        source_content_sha256=verified.content_sha256,
        source_mode=source["mode"],
        mappings=tuple(projected),
    )


def export_projection(projection: AibiThemeProjection) -> bytes:
    """Exporta a projeção V11; o resultado NÃO é arquivo de tema nativo AI/BI."""
    if type(projection) is not AibiThemeProjection:
        _fail("AIBI_PROJECTION_TYPE", "Forneça uma projeção V11 válida.")
    return _canonical(projection.to_dict())


def _pointer_parts(pointer: str) -> tuple[str, ...]:
    if type(pointer) is not str or len(pointer) > 512 or _POINTER_RE.fullmatch(pointer) is None:
        _fail("AIBI_BINDING_POINTER", "Use JSON Pointer absoluto, não vazio e normalizado.")
    parts = []
    for part in pointer.split("/")[1:]:
        parts.append(part.replace("~1", "/").replace("~0", "~"))
    if not parts:
        _fail("AIBI_BINDING_POINTER", "O binding não pode substituir a raiz inteira.")
    return tuple(parts)


def _set_existing_pointer(document: Any, pointer: str, value: Any) -> None:
    parts = _pointer_parts(pointer)
    current = document
    for part in parts[:-1]:
        if type(current) is dict:
            if part not in current:
                _fail("AIBI_BINDING_PATH", "O caminho do binding não existe no template.")
            current = current[part]
        elif type(current) is list:
            if not part.isdigit() or int(part) >= len(current):
                _fail("AIBI_BINDING_PATH", "O índice do binding não existe no template.")
            current = current[int(part)]
        else:
            _fail("AIBI_BINDING_PATH", "O caminho atravessa um valor escalar.")
    leaf = parts[-1]
    if type(current) is dict:
        if leaf not in current:
            _fail("AIBI_BINDING_PATH", "O campo final do binding não existe no template.")
        old = current[leaf]
        target = _copy_json(value)
        if type(old) is not type(target):
            _fail("AIBI_BINDING_TYPE", "O valor projetado não possui o mesmo tipo do campo nativo.")
        current[leaf] = target
    elif type(current) is list:
        if not leaf.isdigit() or int(leaf) >= len(current):
            _fail("AIBI_BINDING_PATH", "O índice final não existe no template.")
        index = int(leaf)
        target = _copy_json(value)
        if type(current[index]) is not type(target):
            _fail("AIBI_BINDING_TYPE", "O valor projetado não possui o mesmo tipo do campo nativo.")
        current[index] = target
    else:
        _fail("AIBI_BINDING_PATH", "O destino do binding não é editável.")


def bind_native_template(
    projection: AibiThemeProjection,
    template_raw: bytes,
    binding_raw: bytes,
) -> AibiNativeCandidate:
    """Aplica somente mapeamentos ``translated/direct`` a um template explicitamente fixado.

    A função não conhece nem deduz o schema nativo. ``binding_raw`` precisa declarar
    o SHA-256 exato do template e JSON Pointers para campos já existentes.
    """
    if type(projection) is not AibiThemeProjection:
        _fail("AIBI_PROJECTION_TYPE", "Forneça uma projeção V11 válida.")
    template_sha = hashlib.sha256(template_raw).hexdigest()
    template = _strict_json(template_raw)
    binding = _strict_json(binding_raw)
    if type(template) is not dict or type(binding) is not dict:
        _fail("AIBI_BINDING_SHAPE", "Template e binding precisam ser objetos JSON.")
    if binding.get("binding_version") != 1 or binding.get("template_sha256") != template_sha:
        _fail("AIBI_BINDING_HASH", "O binding não está fixado aos bytes exatos do template.")
    paths = binding.get("paths")
    if type(paths) is not dict or not paths:
        _fail("AIBI_BINDING_SHAPE", "O binding precisa declarar ao menos uma capacidade.")

    rows = [dict(row) for row in projection.mappings]
    direct = {
        row["target_capability"]: row
        for row in rows
        if row["classification"] == "translated" and row["binding_strategy"] == "direct"
    }
    if len(direct) != 3:
        _fail("AIBI_DIRECT_CONTRACT", "A matriz V11 não contém o conjunto direto esperado.")

    pointers_seen: set[str] = set()
    applied: list[str] = []
    for capability, pointer in paths.items():
        if capability not in direct:
            _fail("AIBI_BINDING_CAPABILITY", "O binding tentou automatizar capacidade aproximada ou não suportada.")
        if pointer in pointers_seen:
            _fail("AIBI_BINDING_COLLISION", "Duas capacidades apontam para o mesmo campo nativo.")
        pointers_seen.add(pointer)
        row = direct[capability]
        _set_existing_pointer(template, pointer, row["source_value"])
        applied.append(capability)

    omitted = sorted(set(direct) - set(applied))
    content = _canonical(template)
    return AibiNativeCandidate(
        content=content,
        template_sha256=template_sha,
        candidate_sha256=hashlib.sha256(content).hexdigest(),
        applied_capabilities=tuple(sorted(applied)),
        omitted_capabilities=tuple(omitted),
    )


def workspace_theme_policy() -> Mapping[str, Any]:
    """Contrato local baseado na documentação oficial; não consulta permissões reais."""
    return MappingProxyType({
        "workspace_admin_required_for_manage": True,
        "new_dashboards_inherit_workspace_theme": True,
        "existing_dashboard_apply_is_snapshot": True,
        "workspace_updates_auto_propagate_to_existing": False,
        "manual_reapply_required_for_existing": True,
        "delete_workspace_theme_preserves_applied_snapshot": True,
    })


def dashboard_theme_policy() -> Mapping[str, Any]:
    """Regras de superfície do dashboard; publicação continua fora da V11."""
    return MappingProxyType({
        "draft_required_for_settings": True,
        "theme_import_export_available": True,
        "color_mappings_scope": "dashboard_only",
        "publish_separate_from_theme_selection": True,
        "publish_implemented_by_v11": False,
        "workspace_api_write_implemented_by_v11": False,
    })


def authorize_local_operation(operation: str, *, workspace_admin: bool, draft: bool) -> None:
    """Guarda sintética de papéis para testes/guia; não autentica usuário real."""
    if operation == "manage_workspace_theme":
        if not workspace_admin:
            _fail("AIBI_ADMIN_REQUIRED", "Gerenciar tema do workspace exige administrador do workspace.")
        return
    if operation == "edit_dashboard_theme":
        if not draft:
            _fail("AIBI_DRAFT_REQUIRED", "Configurações de tema exigem dashboard em draft.")
        return
    if operation in {"publish_dashboard", "workspace_api_write"}:
        _fail("AIBI_OPERATION_NOT_IMPLEMENTED", "A V11 não implementa esta operação.")
    _fail("AIBI_OPERATION_UNKNOWN", "Operação desconhecida.")


def synthetic_dashboard_semantic_fingerprint(spec: Mapping[str, Any]) -> str:
    """Fingerprint de queries/filtros do fixture V11; não interpreta dashboard nativo."""
    if not isinstance(spec, Mapping) or spec.get("kind") != "hub_v11_synthetic_dashboard_draft":
        _fail("AIBI_DASHBOARD_FIXTURE", "Forneça o fixture sintético V11.")
    if spec.get("databricks_importable") is not False:
        _fail("AIBI_DASHBOARD_FIXTURE", "O fixture V11 nunca pode se declarar importável.")
    semantic = {
        "datasets": _copy_json(spec.get("datasets")),
        "queries": _copy_json(spec.get("queries")),
        "filters": _copy_json(spec.get("filters")),
        "widgets": [
            {
                key: _copy_json(widget.get(key))
                for key in ("id", "type", "query_id", "fields")
                if key in widget
            }
            for widget in spec.get("widgets", [])
        ],
    }
    return hashlib.sha256(_canonical(semantic)).hexdigest()
