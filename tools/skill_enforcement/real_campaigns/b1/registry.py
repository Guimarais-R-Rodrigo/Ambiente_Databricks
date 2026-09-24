from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

from tools.skill_enforcement.parallel.registry import RegistryError as B0RegistryError

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_REGISTRY = ROOT / "tools/skill_enforcement/real_campaigns/b1/command_registry.json"
SCHEMA_VERSION = "SER-B1-COMMANDS-1"
_ALLOWED_ROW_KEYS = {"command_id", "argv", "effects", "purpose", "timeout_seconds"}

_ALLOWED_SPECS: dict[str, tuple[str, ...]] = {
    "b1:ser03:preflight:cumulative": (
        "{PYTHON}", "-B",
        "ambiente_fonte/.assistant/skills/hub-ml-analise-safra/scripts/preflight.py",
        "--request", "tools/tests/fixtures/ser_b1/vf_cumulative.json",
    ),
    "b1:ser03:preflight:event": (
        "{PYTHON}", "-B",
        "ambiente_fonte/.assistant/skills/hub-ml-analise-safra/scripts/preflight.py",
        "--request", "tools/tests/fixtures/ser_b1/vf_events.json",
    ),
    "b1:ser03:execute-verify": (
        "{PYTHON}", "-B", "-m",
        "tools.skill_enforcement.real_campaigns.b1.domain_worker",
        "ser03-execute-verify",
    ),
    "b1:ser03:domain-audit": (
        "{PYTHON}", "-B", "-m",
        "tools.skill_enforcement.real_campaigns.b1.domain_audit", "ser03",
    ),
    "b1:ser03:negative-audit": (
        "{PYTHON}", "-B", "-m", "unittest",
        "tools.tests.test_ser_b1_domains.SafraDomainTests.test_vf02_reject_mob_negative_fractional_boolean_null_and_string",
        "tools.tests.test_ser_b1_domains.SafraDomainTests.test_vf03_reject_nonbinary_target",
        "tools.tests.test_ser_b1_domains.SafraDomainTests.test_vf04_reject_cumulative_decrease",
        "tools.tests.test_ser_b1_domains.SafraDomainTests.test_vf05_duplicate_identical_and_conflicting_rejected",
        "tools.tests.test_ser_b1_domains.SafraDomainTests.test_vf08_quarterly_rejected_not_claimed_by_monthly_profile",
        "tools.tests.test_ser_b1_domains.SafraDomainTests.test_vf12_monetary_estimand_rejected",
        "-v",
    ),
    "b1:ser05:preflight:temporal": (
        "{PYTHON}", "-B",
        "ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/scripts/preflight.py",
        "--context", "tools/tests/fixtures/ser_b1/ce_l2_temporal.json",
    ),
    "b1:ser05:preflight:static": (
        "{PYTHON}", "-B",
        "ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/scripts/preflight.py",
        "--context", "tools/tests/fixtures/ser_b1/ce_l2_static.json",
    ),
    "b1:ser05:domain-audit": (
        "{PYTHON}", "-B", "-m",
        "tools.skill_enforcement.real_campaigns.b1.domain_audit", "ser05",
    ),
    "b1:ser05:negative-audit": (
        "{PYTHON}", "-B", "-m", "unittest",
        "tools.tests.test_ser_b1_domains.CrossDomainTests.test_ce02_unknown_pit_never_becomes_false",
        "tools.tests.test_ser_b1_domains.CrossDomainTests.test_ce02_not_applicable_requires_reason",
        "tools.tests.test_ser_b1_domains.CrossDomainTests.test_ce05_timezone_and_tie_policy_fail_closed",
        "tools.tests.test_ser_b1_domains.CrossDomainTests.test_ce06_variable_lag_not_approximated",
        "tools.tests.test_ser_b1_domains.CrossDomainTests.test_ce07_bitemporal_not_claimed",
        "tools.tests.test_ser_b1_domains.CrossDomainTests.test_effect_not_permitted_at_l2",
        "-v",
    ),
    "b1:campaign:coverage-audit": (
        "{PYTHON}", "-B", "-m",
        "tools.skill_enforcement.real_campaigns.b1.coverage",
    ),
}


class RegistryError(B0RegistryError):
    """B1 registry errors remain catchable by the qualified B0 verifier."""


def load_registry(path: Path | str = DEFAULT_REGISTRY) -> dict[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or set(raw) != {"schema_version", "commands"}:
        raise RegistryError("B1_COMMAND_REGISTRY_SHAPE_INVALID")
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise RegistryError("B1_COMMAND_REGISTRY_SCHEMA_INVALID")
    commands = raw.get("commands")
    if not isinstance(commands, list):
        raise RegistryError("B1_COMMAND_REGISTRY_COMMANDS_INVALID")
    seen: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    for row in commands:
        if not isinstance(row, Mapping) or set(row) != _ALLOWED_ROW_KEYS:
            raise RegistryError("B1_COMMAND_ROW_INVALID")
        cid = row.get("command_id")
        argv = row.get("argv")
        if not isinstance(cid, str) or not cid or cid in seen:
            raise RegistryError("B1_COMMAND_ID_INVALID_OR_DUPLICATE")
        if cid not in _ALLOWED_SPECS:
            raise RegistryError("B1_COMMAND_ID_NOT_ALLOWLISTED:" + cid)
        if not isinstance(argv, list) or any(not isinstance(x, str) or not x for x in argv):
            raise RegistryError("B1_COMMAND_ARGV_INVALID:" + cid)
        if tuple(argv) != _ALLOWED_SPECS[cid]:
            raise RegistryError("B1_COMMAND_ARGV_NOT_ALLOWLISTED:" + cid)
        if row.get("effects") != "none":
            raise RegistryError("B1_COMMAND_EFFECT_NOT_ALLOWED:" + cid)
        if not isinstance(row.get("purpose"), str) or not row["purpose"].strip():
            raise RegistryError("B1_COMMAND_PURPOSE_INVALID:" + cid)
        timeout = row.get("timeout_seconds")
        if type(timeout) is not int or not 1 <= timeout <= 1800:
            raise RegistryError("B1_COMMAND_TIMEOUT_INVALID:" + cid)
        seen.add(cid)
        by_id[cid] = dict(row)
    if set(by_id) != set(_ALLOWED_SPECS):
        missing = sorted(set(_ALLOWED_SPECS) - set(by_id))
        extra = sorted(set(by_id) - set(_ALLOWED_SPECS))
        raise RegistryError("B1_COMMAND_ALLOWLIST_MISMATCH:" + ",".join(missing + extra))
    return {"schema_version": raw["schema_version"], "commands": by_id}


def resolve_command(
    command_id: str, path: Path | str = DEFAULT_REGISTRY
) -> tuple[list[str], int]:
    registry = load_registry(path)
    try:
        row = registry["commands"][command_id]
    except KeyError as exc:
        raise RegistryError("B1_COMMAND_UNKNOWN:" + str(command_id)) from exc
    argv = [sys.executable if token == "{PYTHON}" else token for token in row["argv"]]
    return argv, int(row["timeout_seconds"])
