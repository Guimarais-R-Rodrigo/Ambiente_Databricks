from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class Decision:
    ready: tuple[str, ...]
    blocked_dependency: tuple[str, ...]
    pending: tuple[str, ...]

def detect_cycle(tasks: list[Mapping[str, Any]]) -> bool:
    deps = {t["task_id"]: set(t.get("depends_on") or []) for t in tasks}
    indegree = {k: len(v) for k, v in deps.items()}
    followers = {k: set() for k in deps}
    for task, requirements in deps.items():
        for dep in requirements:
            if dep in followers:
                followers[dep].add(task)
    queue = [k for k, v in indegree.items() if v == 0]
    seen = 0
    while queue:
        cur = queue.pop(); seen += 1
        for nxt in followers[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return seen != len(tasks)

def decide(tasks: list[Mapping[str, Any]], statuses: Mapping[str, str], *, active_exclusivity: set[str] | None = None, limit: int = 2) -> Decision:
    active_exclusivity = set(active_exclusivity or set())
    ready: list[str] = []; blocked: list[str] = []; pending: list[str] = []
    by_id = {t["task_id"]: t for t in tasks}
    for task_id in sorted(by_id):
        if task_id in statuses:
            continue
        task = by_id[task_id]
        deps = task.get("depends_on") or []
        dep_states = [statuses.get(dep) for dep in deps]
        if any(state in {"FAIL", "BLOCKED_DEPENDENCY", "BLOCKED_ENVIRONMENT"} for state in dep_states):
            blocked.append(task_id); continue
        if not all(state in {"PASS", "NOT_APPLICABLE"} for state in dep_states):
            pending.append(task_id); continue
        key = task.get("exclusivity_key")
        if key in active_exclusivity or len(ready) >= limit:
            pending.append(task_id); continue
        ready.append(task_id); active_exclusivity.add(key)
    return Decision(tuple(ready), tuple(blocked), tuple(pending))
