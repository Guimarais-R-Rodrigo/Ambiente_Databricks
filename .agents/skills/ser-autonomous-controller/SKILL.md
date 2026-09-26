---
name: ser-autonomous-controller
description: Use when operating a SER/SEF front in Codex Autonomous Controller Mode, including multi-round investigation, implementation, verification, audit and causal repair up to a defined Human Gate.
---

# SER Autonomous Controller

Read, in order:

1. `AGENTS.md`;
2. `docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md`;
3. the active envelope in `docs/operations/autonomy/`;
4. the state file referenced by that envelope;
5. only the documents that own the current gate.

Act as the root controller. Use project roles from `.codex/config.toml`.

Keep one writer. Parallelize read-only investigation/audits. Continue through causal repair rounds while the envelope and budgets permit.

Never infer A2 activation, promotion, Ready or merge. Stop at Human Gates.
