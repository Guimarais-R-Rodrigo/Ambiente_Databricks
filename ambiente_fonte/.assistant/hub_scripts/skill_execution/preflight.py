from __future__ import annotations

import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping


SUPPORTED_SCHEMA_VERSIONS = {"0.1"}
SUPPORTED_MODES = {"audit"}
SUPPORTED_POLICIES = {"required", "conditional", "optional"}

_CONDITION_KEYS = {
    "local_sample_required": "local_sample_required",
    "tabular_preview_required": "tabular_preview_required",
    "numeric_columns_at_least": "numeric_columns",
    "numeric_distributions_requested": "numeric_distributions_requested",
    "resolved_theme_selected": "resolved_theme_selected",
    "visual_diagnostics_requested": "visual_diagnostics_requested",
}


@dataclass(frozen=True)
class PreflightIssue:
    code: str
    message: str
    item_type: str
    item_id: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class PreflightDecision:
    item_type: str
    item_id: str
    policy: str
    applicable: bool | None
    resolved: bool | None
    target: str
    reason: str
    condition: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PreflightResult:
    skill: str | None
    schema_version: str | None
    mode: str | None
    status: str
    assistant_root_resolved: bool
    resources: tuple[PreflightDecision, ...]
    templates: tuple[PreflightDecision, ...]
    blocking_issues: tuple[PreflightIssue, ...]
    condition_context: dict[str, Any]
    writes_performed: bool = False

    @property
    def ok(self) -> bool:
        return self.status == "PASS"

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill": self.skill,
            "schema_version": self.schema_version,
            "mode": self.mode,
            "status": self.status,
            "assistant_root_resolved": self.assistant_root_resolved,
            "resources": [item.to_dict() for item in self.resources],
            "templates": [item.to_dict() for item in self.templates],
            "blocking_issues": [issue.to_dict() for issue in self.blocking_issues],
            "condition_context": dict(self.condition_context),
            "writes_performed": self.writes_performed,
        }


class PreflightContractError(ValueError):
    """Contrato ou contexto insuficiente para um preflight seguro."""


def _public_exports(init_path: Path) -> set[str]:
    tree = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
    explicit_all: set[str] | None = None
    imported: set[str] = set()
    defined: set[str] = set()

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                defined.add(node.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                if not name.startswith("_"):
                    imported.add(name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".", 1)[0]
                if not name.startswith("_"):
                    imported.add(name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    try:
                        value = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        value = None
                    if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
                        explicit_all = set(value)

    return explicit_all if explicit_all is not None else imported | defined


def _load_contract(contract_path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PreflightContractError(f"contrato ilegível: {exc}") from exc
    if not isinstance(raw, dict):
        raise PreflightContractError("a raiz do contrato deve ser objeto JSON")
    return raw


def _require_bool(context: Mapping[str, Any], key: str) -> bool:
    if key not in context:
        raise PreflightContractError(f"contexto obrigatório ausente: {key}")
    value = context[key]
    if not isinstance(value, bool):
        raise PreflightContractError(f"{key} deve ser booleano")
    return value


def _evaluate_condition(condition: Any, context: Mapping[str, Any]) -> tuple[bool, str]:
    if not isinstance(condition, dict):
        raise PreflightContractError("condition deve ser objeto")
    kind = condition.get("kind")
    if kind not in _CONDITION_KEYS:
        raise PreflightContractError(f"condition.kind não suportado: {kind!r}")

    if kind == "numeric_columns_at_least":
        threshold = condition.get("value")
        if not isinstance(threshold, int) or isinstance(threshold, bool) or threshold < 2:
            raise PreflightContractError("numeric_columns_at_least exige value inteiro >= 2")
        if "numeric_columns" not in context:
            raise PreflightContractError("contexto obrigatório ausente: numeric_columns")
        observed = context["numeric_columns"]
        if not isinstance(observed, int) or isinstance(observed, bool) or observed < 0:
            raise PreflightContractError("numeric_columns deve ser inteiro >= 0")
        return observed >= threshold, f"numeric_columns={observed}; limiar={threshold}"

    key = _CONDITION_KEYS[kind]
    value = _require_bool(context, key)
    return value, f"{key}={str(value).lower()}"


def _safe_template_target(skill_dir: Path, rel: Any) -> tuple[Path | None, str | None]:
    if not isinstance(rel, str) or not rel.endswith(".md"):
        return None, "path deve ser Markdown relativo à pasta da skill"
    candidate = Path(rel)
    if candidate.is_absolute() or rel.startswith(("/", "\\")) or ".." in candidate.parts:
        return None, "path de template inseguro"
    return skill_dir / candidate, None


def _resolve_resource(resource: Mapping[str, Any], assistant_root: Path) -> tuple[bool, str]:
    module = resource.get("module")
    symbol = resource.get("symbol")
    if not isinstance(module, str) or not module.startswith(("hub_snippets.", "hub_scripts.")):
        return False, "module fora de hub_snippets.* / hub_scripts.*"
    if not isinstance(symbol, str) or not symbol or "." in symbol:
        return False, "symbol público inválido"

    package_dir = assistant_root.joinpath(*module.split("."))
    init_path = package_dir / "__init__.py"
    if not package_dir.is_dir() or not init_path.is_file():
        return False, f"fachada pública ausente para {module}"
    try:
        exports = _public_exports(init_path)
    except (OSError, SyntaxError) as exc:
        return False, f"fachada pública ilegível: {exc}"
    if symbol not in exports:
        return False, f"{module}.{symbol} não exportado pela fachada pública"
    return True, "API pública resolvida estaticamente"


def _base_applicability(
    item: Mapping[str, Any], context: Mapping[str, Any]
) -> tuple[bool | None, str, PreflightIssue | None]:
    item_id = str(item.get("id", "<sem-id>"))
    policy = item.get("policy")
    if policy not in SUPPORTED_POLICIES:
        return None, "policy inválida", PreflightIssue(
            "POLICY_INVALID", f"policy não suportada: {policy!r}", "contract", item_id
        )
    if policy == "required":
        return True, "requisito obrigatório", None
    if policy == "optional":
        return False, "recurso opcional; disponibilidade apenas informativa", None
    try:
        applicable, reason = _evaluate_condition(item.get("condition"), context)
    except PreflightContractError as exc:
        return None, str(exc), PreflightIssue(
            "CONDITION_CONTEXT_INVALID", str(exc), "contract", item_id
        )
    return applicable, reason, None


def run_preflight(
    contract_path: Path | str,
    *,
    assistant_root: Path | str,
    context: Mapping[str, Any],
) -> PreflightResult:
    """Resolve contrato e pré-condições sem importar helpers nem executar análise."""
    contract_path = Path(contract_path)
    assistant_root = Path(assistant_root)
    context_dict = dict(context)
    issues: list[PreflightIssue] = []
    resource_decisions: list[PreflightDecision] = []
    template_decisions: list[PreflightDecision] = []

    try:
        raw = _load_contract(contract_path)
    except PreflightContractError as exc:
        issue = PreflightIssue("CONTRACT_UNREADABLE", str(exc), "contract", "$")
        return PreflightResult(
            skill=None,
            schema_version=None,
            mode=None,
            status="BLOCKED",
            assistant_root_resolved=assistant_root.is_dir(),
            resources=(),
            templates=(),
            blocking_issues=(issue,),
            condition_context=context_dict,
        )

    skill = raw.get("skill")
    schema_version = raw.get("schema_version")
    mode = raw.get("mode")
    skill_dir = contract_path.parent

    if not assistant_root.is_dir():
        issues.append(PreflightIssue("ASSISTANT_ROOT_NOT_FOUND", "raiz .assistant ausente", "contract", "$"))
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        issues.append(PreflightIssue("SCHEMA_VERSION_UNSUPPORTED", f"schema_version não suportada: {schema_version!r}", "contract", "$"))
    if mode not in SUPPORTED_MODES:
        issues.append(PreflightIssue("MODE_INVALID", f"mode não suportado pelo preflight SE02: {mode!r}", "contract", "$"))
    if not isinstance(skill, str) or skill_dir.name != skill:
        issues.append(PreflightIssue("SKILL_MISMATCH", f"skill do contrato não corresponde à pasta: {skill!r}", "contract", "$"))

    resources = raw.get("resources")
    templates = raw.get("templates")
    if not isinstance(resources, list):
        issues.append(PreflightIssue("RESOURCES_INVALID", "resources deve ser lista", "contract", "$"))
        resources = []
    if not isinstance(templates, list):
        issues.append(PreflightIssue("TEMPLATES_INVALID", "templates deve ser lista", "contract", "$"))
        templates = []

    for item in resources:
        if not isinstance(item, dict):
            issues.append(PreflightIssue("RESOURCE_INVALID", "resource deve ser objeto", "resource", "<sem-id>"))
            continue
        item_id = str(item.get("id", "<sem-id>"))
        policy = str(item.get("policy", "<sem-policy>"))
        target = f"{item.get('module')}.{item.get('symbol')}"
        applicable, reason, applicability_issue = _base_applicability(item, context_dict)
        if applicability_issue:
            issues.append(PreflightIssue(applicability_issue.code, applicability_issue.message, "resource", item_id))
            resource_decisions.append(PreflightDecision("resource", item_id, policy, None, None, target, reason, item.get("condition")))
            continue

        resolved: bool | None
        resolution_reason: str
        if policy == "conditional" and applicable is False:
            resolved = None
            resolution_reason = f"não aplicável: {reason}"
        else:
            resolved, resolution_reason = _resolve_resource(item, assistant_root)
            if applicable is True and not resolved:
                issues.append(PreflightIssue("RESOURCE_REQUIRED_UNAVAILABLE", resolution_reason, "resource", item_id))
        resource_decisions.append(
            PreflightDecision("resource", item_id, policy, applicable, resolved, target, resolution_reason if resolved is not None else reason, item.get("condition"))
        )

    for item in templates:
        if not isinstance(item, dict):
            issues.append(PreflightIssue("TEMPLATE_INVALID", "template deve ser objeto", "template", "<sem-id>"))
            continue
        item_id = str(item.get("id", "<sem-id>"))
        policy = str(item.get("policy", "<sem-policy>"))
        target_rel = item.get("path")
        target = str(target_rel)
        applicable, reason, applicability_issue = _base_applicability(item, context_dict)
        if applicability_issue:
            issues.append(PreflightIssue(applicability_issue.code, applicability_issue.message, "template", item_id))
            template_decisions.append(PreflightDecision("template", item_id, policy, None, None, target, reason, item.get("condition")))
            continue

        resolved: bool | None
        resolution_reason: str
        if policy == "conditional" and applicable is False:
            resolved = None
            resolution_reason = f"não aplicável: {reason}"
        else:
            template_target, path_error = _safe_template_target(skill_dir, target_rel)
            if path_error:
                resolved = False
                resolution_reason = path_error
            else:
                assert template_target is not None
                resolved = template_target.is_file()
                resolution_reason = "template resolvido" if resolved else "template ausente"
            if applicable is True and not resolved:
                issues.append(PreflightIssue("TEMPLATE_REQUIRED_UNAVAILABLE", resolution_reason, "template", item_id))
        template_decisions.append(
            PreflightDecision("template", item_id, policy, applicable, resolved, target, resolution_reason if resolved is not None else reason, item.get("condition"))
        )

    return PreflightResult(
        skill=skill if isinstance(skill, str) else None,
        schema_version=schema_version if isinstance(schema_version, str) else None,
        mode=mode if isinstance(mode, str) else None,
        status="BLOCKED" if issues else "PASS",
        assistant_root_resolved=assistant_root.is_dir(),
        resources=tuple(resource_decisions),
        templates=tuple(template_decisions),
        blocking_issues=tuple(issues),
        condition_context=context_dict,
    )
