from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = ROOT / "tools/skill_enforcement/parallel/command_registry.json"
_ALLOWED_ROW_KEYS = {"command_id", "argv", "effects", "purpose", "timeout_seconds"}
_FORBIDDEN_EXECUTABLES = {"sh", "bash", "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe"}

class RegistryError(ValueError):
    pass


def load_registry(path: Path | str = DEFAULT_REGISTRY) -> dict[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or set(raw) != {"schema_version", "commands"} or raw.get("schema_version") != "SER-PARALLEL-COMMANDS-2":
        raise RegistryError("COMMAND_REGISTRY_SCHEMA_INVALID")
    commands = raw.get("commands")
    if not isinstance(commands, list):
        raise RegistryError("COMMAND_REGISTRY_COMMANDS_INVALID")
    seen: set[str] = set(); by_id: dict[str, Any] = {}
    for row in commands:
        if not isinstance(row, Mapping) or set(row) - _ALLOWED_ROW_KEYS:
            raise RegistryError("COMMAND_ROW_INVALID")
        cid = row.get("command_id"); argv = row.get("argv")
        if not isinstance(cid, str) or not cid or cid in seen:
            raise RegistryError("COMMAND_ID_INVALID_OR_DUPLICATE")
        if not isinstance(argv, list) or not argv or any(not isinstance(x, str) or not x for x in argv):
            raise RegistryError("COMMAND_ARGV_INVALID:" + cid)
        executable = argv[0].lower()
        if executable in _FORBIDDEN_EXECUTABLES or "-c" in argv:
            raise RegistryError("COMMAND_SHELL_OR_INLINE_CODE_FORBIDDEN:" + cid)
        if any("{" in token or "}" in token for token in argv if token != "{PYTHON}"):
            raise RegistryError("COMMAND_PLACEHOLDER_FORBIDDEN:" + cid)
        if row.get("effects") not in {"none"}:
            raise RegistryError("COMMAND_EFFECT_NOT_ALLOWED_IN_B0:" + cid)
        timeout = row.get("timeout_seconds", 120)
        if type(timeout) is not int or timeout < 1 or timeout > 1800:
            raise RegistryError("COMMAND_TIMEOUT_INVALID:" + cid)
        seen.add(cid); by_id[cid] = dict(row)
    return {"schema_version": raw["schema_version"], "commands": by_id}


def resolve_command(command_id: str, path: Path | str = DEFAULT_REGISTRY) -> tuple[list[str], int]:
    registry = load_registry(path)
    try: row = registry["commands"][command_id]
    except KeyError as exc: raise RegistryError("COMMAND_UNKNOWN:" + command_id) from exc
    argv = [sys.executable if token == "{PYTHON}" else token for token in row["argv"]]
    return argv, int(row.get("timeout_seconds", 120))
