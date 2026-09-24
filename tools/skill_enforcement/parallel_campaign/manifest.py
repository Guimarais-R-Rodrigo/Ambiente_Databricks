from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .model import CommandSpec, TaskSpec

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_DIR = Path(__file__).with_name("schemas")

class ManifestError(ValueError): pass

def _validator(schema_name: str):
    try:
        import jsonschema
    except ImportError as exc:
        raise ManifestError("JSONSCHEMA_DEPENDENCY_MISSING") from exc
    schema=json.loads((SCHEMA_DIR/schema_name).read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)

def validate_document(value: Any, schema_name: str) -> list[str]:
    try: validator=_validator(schema_name)
    except (OSError, json.JSONDecodeError, ManifestError) as exc: return [f"SCHEMA_UNAVAILABLE:{exc}"]
    issues=[]
    for error in sorted(validator.iter_errors(value), key=lambda e:list(e.path)):
        loc=".".join(map(str,error.path)) or "$"
        issues.append(f"SCHEMA:{loc}:{error.message}")
    return issues

def validate_registry(raw: Any) -> list[str]:
    issues=validate_document(raw,"command_registry.schema.json")
    if issues: return issues
    ids=[x["command_id"] for x in raw["commands"]]
    if len(ids)!=len(set(ids)): issues.append("COMMAND_ID_DUPLICATE")
    for cmd in raw["commands"]:
        if any("{" in arg or "}" in arg for arg in cmd["argv"]):
            allowed={"{python}","{repo}","{evidence}","{task_id}"}
            bad=[arg for arg in cmd["argv"] if ("{" in arg or "}" in arg) and arg not in allowed]
            if bad: issues.append(f"COMMAND_PLACEHOLDER_INVALID:{cmd['command_id']}:{bad}")
    return issues

def validate_campaign(raw: Any, registry: Any) -> list[str]:
    issues=validate_document(raw,"campaign.schema.json")+validate_registry(registry)
    if issues: return issues
    command_ids={x["command_id"] for x in registry["commands"]}
    tasks=raw["tasks"]; ids=[x["task_id"] for x in tasks]
    if len(ids)!=len(set(ids)): issues.append("TASK_ID_DUPLICATE")
    idset=set(ids)
    for task in tasks:
        if task["command_id"] not in command_ids:
            issues.append(f"COMMAND_UNKNOWN:{task['task_id']}:{task['command_id']}")
        else:
            command=next(x for x in registry["commands"] if x["command_id"]==task["command_id"])
            if command["effect_class"]=="read_only" and task["repo_write_paths"]:
                issues.append(f"READ_ONLY_COMMAND_HAS_REPO_WRITE_ALLOWLIST:{task['task_id']}")
            disallowed=sorted(set((task.get("env") or {}))-set(command["env_allowlist"]))
            if disallowed:
                issues.append(f"ENV_NOT_ALLOWED:{task['task_id']}:{','.join(disallowed)}")
        for dep in task["depends_on"]:
            if dep not in idset: issues.append(f"DEPENDENCY_UNKNOWN:{task['task_id']}:{dep}")
            if dep==task["task_id"]: issues.append(f"DEPENDENCY_SELF:{task['task_id']}")
        if any(Path(p).is_absolute() or ".." in Path(p).parts for p in task["repo_write_paths"]+task["protected_paths"]):
            issues.append(f"REPO_PATH_INVALID:{task['task_id']}")
    # cycle check
    deps={x["task_id"]:set(x["depends_on"]) for x in tasks}; pending=set(deps)
    while pending:
        ready={x for x in pending if not (deps[x]&pending)}
        if not ready: issues.append("DAG_CYCLE"); break
        pending-=ready
    return issues

def load_registry(path: Path) -> tuple[dict[str,CommandSpec], dict]:
    raw=json.loads(path.read_text(encoding="utf-8")); issues=validate_registry(raw)
    if issues: raise ManifestError(";".join(issues))
    out={}
    for row in raw["commands"]:
        out[row["command_id"]]=CommandSpec(row["command_id"],tuple(row["argv"]),frozenset(row["env_allowlist"]),float(row["timeout_seconds"]),row["effect_class"])
    return out,raw

def load_campaign(path: Path, registry_raw: dict) -> tuple[dict[str,TaskSpec], dict]:
    raw=json.loads(path.read_text(encoding="utf-8")); issues=validate_campaign(raw,registry_raw)
    if issues: raise ManifestError(";".join(issues))
    out={}
    for row in raw["tasks"]:
        out[row["task_id"]]=TaskSpec(row["task_id"],row["command_id"],tuple(row["depends_on"]),row["resource_class"],tuple(row["exclusivity_keys"]),row["required"],tuple(row["expected_exit_codes"]),tuple(row["protected_paths"]),tuple(row["repo_write_paths"]),dict(row["outcome_assertion"]),dict(row.get("env") or {}))
    return out,raw


def validate_authorization(raw: Any, campaign: dict, commands: dict[str, CommandSpec]) -> list[str]:
    from datetime import datetime, timezone
    issues=validate_document(raw,"authorization.schema.json")
    if issues: return issues
    if raw.get("campaign_id")!=campaign.get("campaign_id"): issues.append("AUTH_CAMPAIGN_MISMATCH")
    if raw.get("candidate_sha")!=campaign.get("candidate_sha"): issues.append("AUTH_CANDIDATE_MISMATCH")
    try:
        expires=datetime.fromisoformat(str(raw.get("expires_at_utc")).replace("Z","+00:00"))
        if expires.tzinfo is None or expires <= datetime.now(timezone.utc): issues.append("AUTH_EXPIRED_OR_NAIVE")
    except ValueError:
        issues.append("AUTH_EXPIRY_INVALID")
    allowed_ids=set(raw.get("allowed_command_ids") or [])
    allowed_effects=set(raw.get("allowed_effects") or [])
    for task in campaign.get("tasks",[]):
        spec=commands.get(task.get("command_id"))
        if spec and spec.effect_class!="read_only":
            if spec.command_id not in allowed_ids: issues.append("AUTH_COMMAND_NOT_ALLOWED:"+spec.command_id)
            if spec.effect_class not in allowed_effects: issues.append("AUTH_EFFECT_NOT_ALLOWED:"+spec.effect_class)
    return issues
