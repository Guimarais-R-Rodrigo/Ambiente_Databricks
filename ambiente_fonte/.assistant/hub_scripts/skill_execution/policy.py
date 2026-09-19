from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

LEVELS = ("L0", "L1", "L2", "L3", "L4")
ROLLOUT_MODES = {"guidance", "audit", "warn", "enforce"}
RISK_CLASSES = {"low", "medium", "high", "critical"}
POLICY_STATUSES = {"defined", "implemented"}
EVIDENCE_KINDS = {"static", "preflight", "receipt", "postflight", "authorization"}

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
        value["protected_surfaces"] = [item.to_dict() for item in self.protected_surfaces]
        value["known_debt"] = list(self.known_debt)
        return value

def _default_assistant_root() -> Path:
    return Path(__file__).resolve().parents[2]

def _policy_path(assistant_root: Path) -> Path:
    return assistant_root / "hub_padroes" / "skill_enforcement" / "policy.json"

def _level_index(level: str) -> int:
    try:
        return LEVELS.index(level)
    except ValueError as exc:
        raise EnforcementPolicyError(f"nível SEF não suportado: {level!r}") from exc

def _require_string(raw: Mapping[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise EnforcementPolicyError(f"{key} deve ser string não vazia")
    return value

def _surface(raw: Any) -> EnforcementSurface:
    if not isinstance(raw, Mapping):
        raise EnforcementPolicyError("protected_surface deve ser objeto")
    sid = _require_string(raw, "id")
    level = _require_string(raw, "level")
    evidence = _require_string(raw, "evidence")
    rationale = _require_string(raw, "rationale")
    _level_index(level)
    if evidence not in EVIDENCE_KINDS:
        raise EnforcementPolicyError(f"evidence não suportada: {evidence!r}")
    return EnforcementSurface(sid, level, evidence, rationale)

def _policy(raw: Any) -> SkillEnforcementPolicy:
    if not isinstance(raw, Mapping):
        raise EnforcementPolicyError("skill policy deve ser objeto")
    skill = _require_string(raw, "skill")
    risk_class = _require_string(raw, "risk_class")
    current_level = _require_string(raw, "current_level")
    target_level = _require_string(raw, "target_level")
    scope_mode = _require_string(raw, "scope_mode")
    rollout_mode = _require_string(raw, "rollout_mode")
    policy_status = _require_string(raw, "policy_status")
    rationale = _require_string(raw, "rationale")
    current_index = _level_index(current_level)
    target_index = _level_index(target_level)
    if target_index < current_index:
        raise EnforcementPolicyError(f"{skill}: target_level não pode ser inferior a current_level")
    if risk_class not in RISK_CLASSES:
        raise EnforcementPolicyError(f"{skill}: risk_class inválida: {risk_class!r}")
    if rollout_mode not in ROLLOUT_MODES:
        raise EnforcementPolicyError(f"{skill}: rollout_mode inválido: {rollout_mode!r}")
    if policy_status not in POLICY_STATUSES:
        raise EnforcementPolicyError(f"{skill}: policy_status inválido: {policy_status!r}")
    if scope_mode not in {"whole_skill", "stage_specific"}:
        raise EnforcementPolicyError(f"{skill}: scope_mode inválido: {scope_mode!r}")
    artifacts = raw.get("implemented_artifacts")
    debt = raw.get("known_debt")
    surfaces = raw.get("protected_surfaces")
    if not isinstance(artifacts, list) or any(not isinstance(x, str) or not x for x in artifacts):
        raise EnforcementPolicyError(f"{skill}: implemented_artifacts inválido")
    if not isinstance(debt, list) or any(not isinstance(x, str) or not x for x in debt):
        raise EnforcementPolicyError(f"{skill}: known_debt inválido")
    if not isinstance(surfaces, list) or not surfaces:
        raise EnforcementPolicyError(f"{skill}: protected_surfaces deve ser lista não vazia")
    parsed_surfaces = tuple(_surface(item) for item in surfaces)
    if any(_level_index(item.level) > target_index for item in parsed_surfaces):
        raise EnforcementPolicyError(f"{skill}: protected_surface excede target_level")
    if policy_status == "implemented" and current_level != target_level:
        raise EnforcementPolicyError(f"{skill}: policy_status=implemented exige current_level == target_level")
    if rollout_mode == "enforce" and current_level != "L4":
        raise EnforcementPolicyError(f"{skill}: rollout_mode=enforce exige L4 implementado")
    return SkillEnforcementPolicy(
        skill=skill,risk_class=risk_class,current_level=current_level,target_level=target_level,
        scope_mode=scope_mode,rollout_mode=rollout_mode,policy_status=policy_status,rationale=rationale,
        implemented_artifacts=tuple(artifacts),protected_surfaces=parsed_surfaces,known_debt=tuple(debt),
    )

def load_enforcement_policy_registry(*, assistant_root: Path | str | None = None, policy_path: Path | str | None = None) -> dict[str, SkillEnforcementPolicy]:
    """Carrega a política SE07 sem executar helpers analíticos nem escrever arquivos."""
    root = Path(assistant_root) if assistant_root is not None else _default_assistant_root()
    path = Path(policy_path) if policy_path is not None else _policy_path(root)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EnforcementPolicyError(f"policy registry ilegível: {exc}") from exc
    if not isinstance(raw, Mapping):
        raise EnforcementPolicyError("policy registry deve ser objeto")
    if raw.get("schema_version") != "1.0":
        raise EnforcementPolicyError(f"schema_version não suportada: {raw.get('schema_version')!r}")
    skills = raw.get("skills")
    if not isinstance(skills, list):
        raise EnforcementPolicyError("skills deve ser lista")
    result: dict[str, SkillEnforcementPolicy] = {}
    for item in skills:
        policy = _policy(item)
        if policy.skill in result:
            raise EnforcementPolicyError(f"skill duplicada: {policy.skill}")
        result[policy.skill] = policy
    return result

def get_skill_enforcement_policy(skill: str, *, assistant_root: Path | str | None = None, policy_path: Path | str | None = None) -> SkillEnforcementPolicy:
    """Retorna a política canônica de uma skill; skill desconhecida falha fechado."""
    policies = load_enforcement_policy_registry(assistant_root=assistant_root, policy_path=policy_path)
    try:
        return policies[skill]
    except KeyError as exc:
        raise EnforcementPolicyError(f"skill sem política SEF: {skill}") from exc

def list_skill_enforcement_policies(*, assistant_root: Path | str | None = None, policy_path: Path | str | None = None) -> tuple[SkillEnforcementPolicy, ...]:
    policies = load_enforcement_policy_registry(assistant_root=assistant_root, policy_path=policy_path)
    return tuple(policies[name] for name in sorted(policies))
