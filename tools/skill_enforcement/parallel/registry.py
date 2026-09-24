from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = ROOT / "tools/skill_enforcement/parallel/command_registry.json"

class RegistryError(ValueError):
    pass

def load_registry(path: Path | str = DEFAULT_REGISTRY) -> dict[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema_version") != "SER-PARALLEL-COMMANDS-1":
        raise RegistryError("COMMAND_REGISTRY_SCHEMA_INVALID")
    commands = raw.get("commands")
    if not isinstance(commands, list):
        raise RegistryError("COMMAND_REGISTRY_COMMANDS_INVALID")
    seen: set[str] = set()
    by_id: dict[str, Any] = {}
    for row in commands:
        if not isinstance(row, Mapping):
            raise RegistryError("COMMAND_NOT_MAPPING")
        cid = row.get("command_id")
        argv = row.get("argv")
        if not isinstance(cid, str) or not cid or cid in seen:
            raise RegistryError("COMMAND_ID_INVALID_OR_DUPLICATE")
        if not isinstance(argv, list) or not argv or any(not isinstance(x, str) or not x for x in argv):
            raise RegistryError("COMMAND_ARGV_INVALID:" + cid)
        if any(x in {"sh", "bash", "cmd", "powershell", "pwsh"} for x in argv[:1]):
            raise RegistryError("COMMAND_SHELL_FORBIDDEN:" + cid)
        seen.add(cid)
        by_id[cid] = dict(row)
    return {"schema_version": raw["schema_version"], "commands": by_id}

def resolve_command(command_id: str, path: Path | str = DEFAULT_REGISTRY) -> list[str]:
    registry = load_registry(path)
    try:
        row = registry["commands"][command_id]
    except KeyError as exc:
        raise RegistryError("COMMAND_UNKNOWN:" + command_id) from exc
    return list(row["argv"])
