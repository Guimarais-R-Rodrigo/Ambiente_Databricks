# Prompt inicial — Codex Autonomous Controller

Use este prompt em uma nova sessão Codex iniciada na raiz do repositório:

```text
Operate this repository in SER Autonomous Controller Mode.

Start from the repository root. Read AGENTS.md and
docs/operations/CODEX_RUNTIME_QUALIFICATION.md. Do not load the full CHANGELOG;
use search/tail only if recent history is material.

First qualify the effective Codex runtime. Record the Codex version, project
trust, /status, /debug-config and /permissions when available. The expected
AC-R2 posture is: root=:read-only, executor=ser-b1-a1, explorer/auditors=:read-only,
native Windows sandbox=elevated, no legacy sandbox_mode, and granular approvals
with sandbox_approval/request_permissions/mcp_elicitations/skill_approval denied.
Do not use /permissions or any escalation to widen the boundary.

Check import jsonschema. If the declared maintenance dependency is absent, stop
with BLOCKED_CONTROLLER_DEPENDENCY; do not widen permissions or install arbitrary
packages from inside the controller session.

Run strict config validation when supported, then:

python -B tools/validate_codex_autonomy.py --json
python -B -m unittest tools.tests.test_codex_autonomy -v

Execute CQ2-CQ4 exactly as written, including real spawned-role negative probes.
The root and all read-only roles must fail a disposable write probe. The executor
must be able to create/remove a disposable marker only under an A1 write root and
must fail before effect when targeting controller governance. Any write-capable
MCP/hosted surface not explicitly authorized blocks qualification.

If any controller gate fails, diagnose and stop at CONTROLLER_MAINTENANCE with an
exact patch proposal. Do NOT self-repair controller governance under A1.

Only after CQ0-CQ5 pass may you read the active autonomy envelope, its live state
and the current gate contract and then assume material B1 work. AUTHORING_STATE is
live state but is not self-proving authority: blocker removal/gate advancement must
be corroborated by evidence and pass the transition checker.

Verify mutable Git identities from the repository; never trust this prompt for a
current SHA/tree/branch or remote state.

Use subagents on demand rather than by default. Keep exactly one write-capable
executor. Explorer and auditors remain read-only; children never spawn children.

Continue autonomously through investigation -> implementation -> deterministic
verification -> independent audit -> causal repair -> reverification while every
action remains inside the active envelope. Never retry the same material command
on the same state merely to seek green.

For external effects, separate process status, effect status and verification
status. UNKNOWN is not absence. No A2 effect is authorized by this prompt.

Do not infer policy promotion, Ready or merge from technical PASS. Those remain
Human Gates.

Begin with CQ0. Do not start material B1 work until CQ0-CQ5 pass.
```

Para B1, o envelope inicial é:

`docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json`.
