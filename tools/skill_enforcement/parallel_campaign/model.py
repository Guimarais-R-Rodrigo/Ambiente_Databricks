from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

TERMINAL = {"PASS","FAIL","BLOCKED_DEPENDENCY","BLOCKED_LOCK","BLOCKED_DESIGN","REPORTING_FAILURE"}
EFFECT_STATES = {"NONE","CREATED","MODIFIED","PARTIAL","UNKNOWN","CLEANUP_REQUIRED"}

@dataclass(frozen=True)
class CommandSpec:
    command_id: str
    argv: tuple[str, ...]
    env_allowlist: frozenset[str]
    timeout_seconds: float
    effect_class: str

@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    command_id: str
    depends_on: tuple[str, ...]
    resource_class: str
    exclusivity_keys: tuple[str, ...]
    required: bool
    expected_exit_codes: tuple[int, ...]
    protected_paths: tuple[str, ...]
    repo_write_paths: tuple[str, ...]
    outcome_assertion: dict[str, Any] = field(default_factory=lambda: {"kind":"exit_only"})
    env: dict[str, str] = field(default_factory=dict)

@dataclass
class TaskResult:
    task_id: str
    command_id: str
    status: str
    exit_code: int | None
    expected_exit_codes: list[int]
    command_started: bool
    cleanup_complete: bool
    started_at_utc: str
    ended_at_utc: str
    stdout_sha256: str
    stderr_sha256: str
    repo_mutations: list[str]
    protected_changes: list[str]
    effect_state: str = "NONE"
    outcome_observed: dict[str, Any] = field(default_factory=lambda: {"kind":"exit_only","failures":[],"errors":[]})
    issues: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {"schema_version":"SER-PARALLEL-TASK-RESULT-1", **self.__dict__}
