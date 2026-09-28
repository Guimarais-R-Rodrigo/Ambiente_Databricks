---
name: ser-autonomous-controller
description: Use when operating a SER/SEF front in Codex Autonomous Controller Mode, including multi-round investigation, implementation, verification, audit and causal repair up to a defined Human Gate.
---

# SER Autonomous Controller

Read, in order:

1. `docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md`;
2. the active envelope in `docs/operations/autonomy/`;
3. the state file referenced by that envelope;
4. only the documents that own the current gate.

Act as the root controller. Use project roles from `.codex/config.toml`.

Keep one effective writer: the root-controller-only A1 capability bridge. All spawned roles, including executor, stay A0 and may only author proposals in external scratch. Parallelize read-only investigation/audits. Continue through causal repair rounds while the envelope and budgets permit.

Never infer A2 activation, promotion, Ready or merge. Stop at Human Gates.


Controller governance is protected from A1 self-modification. A controller-layer
failure stops at `CONTROLLER_MAINTENANCE`. Apply ADR-0025 state precedence and
treat frozen runbooks/snapshots as historical unless the live state points to them.
