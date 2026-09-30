from __future__ import annotations

import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping


SUPPORTED_SCHEMA_VERSIONS = {"0.1"}
SUPPORTED_MODES = {"audit"}
SUPPORTED_POLICIES = {"required", "conditional", "optional"}

_ALLOWED_ROOT_PACKAGES = {"hub_snippets", "hub_scripts"}

_CONDITION_KEYS = {
    "local_sample_required": "local_sample_required",
    "tabular_preview_required": "tabular_preview_required",
    "numeric_columns_at_least": "numeric_columns",
    "numeric_distributions_requested": "numeric_distributions_requested",
    "resolved_theme_selected": "resolved_theme_selected",
    "visual_diagnostics_requested": "visual_diagnostics_requested",
    "pk_columns_available": "pk_columns_available",
}


def _canonical_module_parts(module: Any) -> tuple[str, ...] | None:
    """Valida e decompõe um caminho Python canônico de recurso do Hub."""
    if not isinstance(module, str):
        return None
    parts = tuple(module.split("."))
    if len(parts) < 2 or parts[0] not in _ALLOWED_ROOT_PACKAGES:
        return None
    if any(not part or not part.isidentifier() for part in parts):
        return None
    return parts


def _public_exports(init_path: Path) -> set[str]:
    """Extrai exports realmente disponíveis na fachada sem executar código.

    Se ``__all__`` existir, ele funciona como filtro dos nomes que também foram
    importados ou definidos no próprio ``__init__.py``. Um nome apenas declarado
    em ``__all__`` não é considerado uma API pública resolvida.
    """
    try:
        tree = ast.parse(
            init_path.read_text(encoding="utf-8"),
            filename=str(init_path),
        )
    except (OSError, SyntaxError) as exc:
        raise ValueError(f"não foi possível analisar {init_path}: {exc}") from exc

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
                    if isinstance(value, (list, tuple)) and all(
                        isinstance(item, str) for item in value
                    ):
                        explicit_all = set(value)

    available = imported | defined
    if explicit_all is None:
        return available
    return explicit_all & available


def _resolve_public_symbol(
    assistant_root: Path | str,
    module: Any,
    symbol: Any,
) -> tuple[bool, str]:
    """Resolve uma API pública do Hub sem importar o módulo-alvo."""
    assistant_root = Path(assistant_root)
    module_parts = _canonical_module_parts(module)
    if module_parts is None:
        return (
            False,
            "module deve ser caminho Python canônico sob hub_snippets.* / hub_scripts.*",
        )
    if not isinstance(symbol, str) or not symbol or not symbol.isidentifier():
        return False, "symbol público inválido"

    package_dir = assistant_root.joinpath(*module_parts)
    init_path = package_dir / "__init__.py"
    if not package_dir.is_dir() or not init_path.is_file():
        return False, f"fachada pública ausente para {module}"

    try:
        exports = _public_exports(init_path)
    except ValueError as exc:
        return False, f"fachada pública ilegível: {exc}"

    if symbol not in exports:
        return False, f"{module}.{symbol} não exportado pela fachada pública"
    return True, "API pública resolvida estaticamente"


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
        issues.append(
            PreflightIssue(
                "ASSISTANT_ROOT_NOT_FOUND", "raiz .assistant ausente", "contract", "$"
            )
        )
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        issues.append(
            PreflightIssue(
                "SCHEMA_VERSION_UNSUPPORTED",
                f"schema_version não suportada: {schema_version!r}",
                "contract",
                "$",
            )
        )
    if mode not in SUPPORTED_MODES:
        issues.append(
            PreflightIssue(
                "MODE_INVALID",
                f"mode não suportado pelo preflight SE02: {mode!r}",
                "contract",
                "$",
            )
        )
    if not isinstance(skill, str) or skill_dir.name != skill:
        issues.append(
            PreflightIssue(
                "SKILL_MISMATCH",
                f"skill do contrato não corresponde à pasta: {skill!r}",
                "contract",
                "$",
            )
        )

    resources = raw.get("resources")
    templates = raw.get("templates")
    if not isinstance(resources, list):
        issues.append(
            PreflightIssue("RESOURCES_INVALID", "resources deve ser lista", "contract", "$")
        )
        resources = []
    if not isinstance(templates, list):
        issues.append(
            PreflightIssue("TEMPLATES_INVALID", "templates deve ser lista", "contract", "$")
        )
        templates = []

    for item in resources:
        if not isinstance(item, dict):
            issues.append(
                PreflightIssue(
                    "RESOURCE_INVALID", "resource deve ser objeto", "resource", "<sem-id>"
                )
            )
            continue
        item_id = str(item.get("id", "<sem-id>"))
        policy = str(item.get("policy", "<sem-policy>"))
        target = f"{item.get('module')}.{item.get('symbol')}"
        applicable, reason, applicability_issue = _base_applicability(item, context_dict)
        if applicability_issue:
            issues.append(
                PreflightIssue(
                    applicability_issue.code,
                    applicability_issue.message,
                    "resource",
                    item_id,
                )
            )
            resource_decisions.append(
                PreflightDecision(
                    "resource",
                    item_id,
                    policy,
                    None,
                    None,
                    target,
                    reason,
                    item.get("condition"),
                )
            )
            continue

        resolved: bool | None
        resolution_reason: str
        if policy == "conditional" and applicable is False:
            resolved = None
            resolution_reason = f"não aplicável: {reason}"
        else:
            resolved, resolution_reason = _resolve_public_symbol(
                assistant_root,
                item.get("module"),
                item.get("symbol"),
            )
            if applicable is True and not resolved:
                issues.append(
                    PreflightIssue(
                        "RESOURCE_REQUIRED_UNAVAILABLE",
                        resolution_reason,
                        "resource",
                        item_id,
                    )
                )
        resource_decisions.append(
            PreflightDecision(
                "resource",
                item_id,
                policy,
                applicable,
                resolved,
                target,
                resolution_reason if resolved is not None else reason,
                item.get("condition"),
            )
        )

    for item in templates:
        if not isinstance(item, dict):
            issues.append(
                PreflightIssue(
                    "TEMPLATE_INVALID", "template deve ser objeto", "template", "<sem-id>"
                )
            )
            continue
        item_id = str(item.get("id", "<sem-id>"))
        policy = str(item.get("policy", "<sem-policy>"))
        target_rel = item.get("path")
        target = str(target_rel)
        applicable, reason, applicability_issue = _base_applicability(item, context_dict)
        if applicability_issue:
            issues.append(
                PreflightIssue(
                    applicability_issue.code,
                    applicability_issue.message,
                    "template",
                    item_id,
                )
            )
            template_decisions.append(
                PreflightDecision(
                    "template",
                    item_id,
                    policy,
                    None,
                    None,
                    target,
                    reason,
                    item.get("condition"),
                )
            )
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
                issues.append(
                    PreflightIssue(
                        "TEMPLATE_REQUIRED_UNAVAILABLE",
                        resolution_reason,
                        "template",
                        item_id,
                    )
                )
        template_decisions.append(
            PreflightDecision(
                "template",
                item_id,
                policy,
                applicable,
                resolved,
                target,
                resolution_reason if resolved is not None else reason,
                item.get("condition"),
            )
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

# ---------------------------------------------------------------------------
# SE07 — política transversal de enforcement por skill
# ---------------------------------------------------------------------------

_POLICY_LEVELS = ("L0", "L1", "L2", "L3", "L4")
_POLICY_ROLLOUT_MODES = {"guidance", "audit", "warn", "enforce"}
_POLICY_RISK_CLASSES = {"low", "medium", "high", "critical"}
_POLICY_STATUSES = {"defined", "implemented"}
_POLICY_EVIDENCE_KINDS = {
    "static", "preflight", "receipt", "postflight", "authorization"
}


class EnforcementPolicyError(ValueError):
    """Política SEF ausente, ilegível ou estruturalmente inválida."""


@dataclass(frozen=True)
class EnforcementSurface:
    id: str
    level: str
    evidence: str
    rationale: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class SkillEnforcementPolicy:
    skill: str
    risk_class: str
    current_level: str
    target_level: str
    scope_mode: str
    rollout_mode: str
    policy_status: str
    rationale: str
    implemented_artifacts: tuple[str, ...]
    protected_surfaces: tuple[EnforcementSurface, ...]
    known_debt: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["implemented_artifacts"] = list(self.implemented_artifacts)
        value["protected_surfaces"] = [
            item.to_dict() for item in self.protected_surfaces
        ]
        value["known_debt"] = list(self.known_debt)
        return value


def _policy_assistant_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _policy_registry_path(assistant_root: Path) -> Path:
    return assistant_root / "hub_padroes" / "skill_enforcement" / "policy.json"


def _policy_level_index(level: str) -> int:
    try:
        return _POLICY_LEVELS.index(level)
    except ValueError as exc:
        raise EnforcementPolicyError(
            f"nível SEF não suportado: {level!r}"
        ) from exc


def _policy_string(raw: Mapping[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise EnforcementPolicyError(f"{key} deve ser string não vazia")
    return value


def _policy_surface(raw: Any) -> EnforcementSurface:
    if not isinstance(raw, Mapping):
        raise EnforcementPolicyError("protected_surface deve ser objeto")
    level = _policy_string(raw, "level")
    evidence = _policy_string(raw, "evidence")
    _policy_level_index(level)
    if evidence not in _POLICY_EVIDENCE_KINDS:
        raise EnforcementPolicyError(f"evidence não suportada: {evidence!r}")
    return EnforcementSurface(
        id=_policy_string(raw, "id"),
        level=level,
        evidence=evidence,
        rationale=_policy_string(raw, "rationale"),
    )


def _skill_policy(raw: Any) -> SkillEnforcementPolicy:
    if not isinstance(raw, Mapping):
        raise EnforcementPolicyError("skill policy deve ser objeto")
    skill = _policy_string(raw, "skill")
    risk = _policy_string(raw, "risk_class")
    current = _policy_string(raw, "current_level")
    target = _policy_string(raw, "target_level")
    scope = _policy_string(raw, "scope_mode")
    rollout = _policy_string(raw, "rollout_mode")
    status = _policy_string(raw, "policy_status")
    rationale = _policy_string(raw, "rationale")

    current_i = _policy_level_index(current)
    target_i = _policy_level_index(target)
    if target_i < current_i:
        raise EnforcementPolicyError(
            f"{skill}: target_level não pode ser inferior a current_level"
        )
    if risk not in _POLICY_RISK_CLASSES:
        raise EnforcementPolicyError(f"{skill}: risk_class inválida: {risk!r}")
    if scope not in {"whole_skill", "stage_specific"}:
        raise EnforcementPolicyError(f"{skill}: scope_mode inválido: {scope!r}")
    if rollout not in _POLICY_ROLLOUT_MODES:
        raise EnforcementPolicyError(
            f"{skill}: rollout_mode inválido: {rollout!r}"
        )
    if status not in _POLICY_STATUSES:
        raise EnforcementPolicyError(
            f"{skill}: policy_status inválido: {status!r}"
        )

    artifacts = raw.get("implemented_artifacts")
    debt = raw.get("known_debt")
    surfaces = raw.get("protected_surfaces")
    if not isinstance(artifacts, list) or any(
        not isinstance(item, str) or not item for item in artifacts
    ):
        raise EnforcementPolicyError(f"{skill}: implemented_artifacts inválido")
    if not isinstance(debt, list) or any(
        not isinstance(item, str) or not item for item in debt
    ):
        raise EnforcementPolicyError(f"{skill}: known_debt inválido")
    if not isinstance(surfaces, list) or not surfaces:
        raise EnforcementPolicyError(
            f"{skill}: protected_surfaces deve ser lista não vazia"
        )

    parsed = tuple(_policy_surface(item) for item in surfaces)
    if any(_policy_level_index(item.level) > target_i for item in parsed):
        raise EnforcementPolicyError(
            f"{skill}: protected_surface excede target_level"
        )
    if status == "implemented" and current != target:
        raise EnforcementPolicyError(
            f"{skill}: policy_status=implemented exige current_level == target_level"
        )
    if rollout == "enforce" and current != "L4":
        raise EnforcementPolicyError(
            f"{skill}: rollout_mode=enforce exige L4 implementado"
        )

    return SkillEnforcementPolicy(
        skill=skill,
        risk_class=risk,
        current_level=current,
        target_level=target,
        scope_mode=scope,
        rollout_mode=rollout,
        policy_status=status,
        rationale=rationale,
        implemented_artifacts=tuple(artifacts),
        protected_surfaces=parsed,
        known_debt=tuple(debt),
    )


def load_enforcement_policy_registry(
    *,
    assistant_root: Path | str | None = None,
    policy_path: Path | str | None = None,
) -> dict[str, SkillEnforcementPolicy]:
    """Carrega o registry SE07 sem executar helpers nem escrever arquivos."""
    root = (
        Path(assistant_root)
        if assistant_root is not None
        else _policy_assistant_root()
    )
    target = (
        Path(policy_path)
        if policy_path is not None
        else _policy_registry_path(root)
    )
    try:
        raw = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EnforcementPolicyError(
            f"policy registry ilegível: {exc}"
        ) from exc
    if not isinstance(raw, Mapping):
        raise EnforcementPolicyError("policy registry deve ser objeto")
    if raw.get("schema_version") != "1.0":
        raise EnforcementPolicyError(
            f"schema_version não suportada: {raw.get('schema_version')!r}"
        )
    skills = raw.get("skills")
    if not isinstance(skills, list):
        raise EnforcementPolicyError("skills deve ser lista")

    result: dict[str, SkillEnforcementPolicy] = {}
    for item in skills:
        policy = _skill_policy(item)
        if policy.skill in result:
            raise EnforcementPolicyError(
                f"skill duplicada: {policy.skill}"
            )
        result[policy.skill] = policy
    return result


def get_skill_enforcement_policy(
    skill: str,
    *,
    assistant_root: Path | str | None = None,
    policy_path: Path | str | None = None,
) -> SkillEnforcementPolicy:
    """Retorna a política canônica; skill desconhecida falha fechado."""
    policies = load_enforcement_policy_registry(
        assistant_root=assistant_root,
        policy_path=policy_path,
    )
    try:
        return policies[skill]
    except KeyError as exc:
        raise EnforcementPolicyError(
            f"skill sem política SEF: {skill}"
        ) from exc


def list_skill_enforcement_policies(
    *,
    assistant_root: Path | str | None = None,
    policy_path: Path | str | None = None,
) -> tuple[SkillEnforcementPolicy, ...]:
    policies = load_enforcement_policy_registry(
        assistant_root=assistant_root,
        policy_path=policy_path,
    )
    return tuple(policies[name] for name in sorted(policies))

