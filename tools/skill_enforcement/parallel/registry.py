from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY = ROOT / "tools/skill_enforcement/parallel/command_registry.json"
_REQUIRED_ROW_KEYS = {"command_id", "argv", "effects", "purpose", "timeout_seconds"}

# B0 is intentionally closed. Expanding this map is a repo-side design change,
# not something a campaign or local executor may improvise.
_B0_ALLOWED_ARGV: dict[str, tuple[str, ...]] = {
    "b0:pilot:pass": (
        "{PYTHON}", "-B", "-m", "tools.skill_enforcement.parallel.pilot_worker", "pass",
    ),
    "b0:pilot:fail": (
        "{PYTHON}", "-B", "-m", "tools.skill_enforcement.parallel.pilot_worker", "fail",
    ),
    "b0:pilot:global-fail": (
        "{PYTHON}", "-B", "-m", "tools.skill_enforcement.parallel.pilot_worker", "global_fail",
    ),
    "b0:host:probe": (
        "{PYTHON}", "-B", "-m", "tools.skill_enforcement.parallel.host_probe",
    ),
    "b0:meta:tests": (
        "{PYTHON}", "-B", "-m", "unittest", "tools.tests.test_ser_parallel_b0", "-v",
    ),
    "b0:coverage:inventory": (
        "{PYTHON}", "-B", "-m", "tools.skill_enforcement.parallel.coverage",
    ),
}


class RegistryError(ValueError):
    pass


def _validate_row(row: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
    if set(row) != _REQUIRED_ROW_KEYS:
        raise RegistryError("COMMAND_ROW_KEYS_INVALID")

    cid = row.get("command_id")
    argv = row.get("argv")
    if not isinstance(cid, str) or cid not in _B0_ALLOWED_ARGV:
        raise RegistryError("COMMAND_ID_NOT_ALLOWLISTED")
    if not isinstance(argv, list) or any(not isinstance(x, str) or not x for x in argv):
        raise RegistryError("COMMAND_ARGV_INVALID:" + cid)
    if tuple(argv) != _B0_ALLOWED_ARGV[cid]:
        raise RegistryError("COMMAND_ARGV_NOT_ALLOWLISTED:" + cid)
    if row.get("effects") != "none":
        raise RegistryError("COMMAND_EFFECT_NOT_ALLOWED_IN_B0:" + cid)
    if not isinstance(row.get("purpose"), str) or not row["purpose"].strip():
        raise RegistryError("COMMAND_PURPOSE_INVALID:" + cid)
    timeout = row.get("timeout_seconds")
    if type(timeout) is not int or timeout < 1 or timeout > 1800:
        raise RegistryError("COMMAND_TIMEOUT_INVALID:" + cid)
    return cid, dict(row)


def load_registry(path: Path | str = DEFAULT_REGISTRY) -> dict[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if (
        not isinstance(raw, dict)
        or set(raw) != {"schema_version", "commands"}
        or raw.get("schema_version") != "SER-PARALLEL-COMMANDS-2"
    ):
        raise RegistryError("COMMAND_REGISTRY_SCHEMA_INVALID")
    commands = raw.get("commands")
    if not isinstance(commands, list):
        raise RegistryError("COMMAND_REGISTRY_COMMANDS_INVALID")

    seen: set[str] = set()
    by_id: dict[str, Any] = {}
    for row in commands:
        if not isinstance(row, Mapping):
            raise RegistryError("COMMAND_ROW_INVALID")
        cid, normalized = _validate_row(row)
        if cid in seen:
            raise RegistryError("COMMAND_ID_DUPLICATE:" + cid)
        seen.add(cid)
        by_id[cid] = normalized

    missing = sorted(set(_B0_ALLOWED_ARGV) - seen)
    extra = sorted(seen - set(_B0_ALLOWED_ARGV))
    if missing or extra:
        raise RegistryError(
            "COMMAND_REGISTRY_ALLOWLIST_SET_MISMATCH:"
            + "missing=" + ",".join(missing)
            + ";extra=" + ",".join(extra)
        )
    return {"schema_version": raw["schema_version"], "commands": by_id}


def command_template(command_id: str, path: Path | str = DEFAULT_REGISTRY) -> list[str]:
    registry = load_registry(path)
    try:
        row = registry["commands"][command_id]
    except KeyError as exc:
        raise RegistryError("COMMAND_UNKNOWN:" + command_id) from exc
    return list(row["argv"])


def command_effect(command_id: str, path: Path | str = DEFAULT_REGISTRY) -> str:
    registry = load_registry(path)
    try:
        return str(registry["commands"][command_id]["effects"])
    except KeyError as exc:
        raise RegistryError("COMMAND_UNKNOWN:" + command_id) from exc


def resolve_command(command_id: str, path: Path | str = DEFAULT_REGISTRY) -> tuple[list[str], int]:
    registry = load_registry(path)
    try:
        row = registry["commands"][command_id]
    except KeyError as exc:
        raise RegistryError("COMMAND_UNKNOWN:" + command_id) from exc
    argv = [sys.executable if token == "{PYTHON}" else token for token in row["argv"]]
    return argv, int(row["timeout_seconds"])
