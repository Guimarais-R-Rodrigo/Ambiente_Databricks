# Prompt inicial — Codex Autonomous Controller

Use este prompt em uma nova sessão Codex iniciada na raiz do repositório:

```text
Operate this repository in SER Autonomous Controller Mode.

Start from the repository root. Read AGENTS.md and
docs/operations/CODEX_RUNTIME_QUALIFICATION.md.

First inspect the effective Codex configuration. When supported by the client,
use /status and /debug-config to prove the project .codex layer is loaded from a
trusted project and that no higher-precedence override defeats the expected
sandbox/approval settings.

Before the validator, check `import jsonschema`. If it is missing, follow CQ0.5
exactly: install only `tools/requirements-codex-autonomy.txt` into the isolated
controller Python environment, subject to normal sandbox/auto-review. Do not edit
requirements to make the install pass.

Then run:

python -B tools/validate_codex_autonomy.py --json
python -B -m unittest tools.tests.test_codex_autonomy -v

If either fails, diagnose the controller defect and stop at the
CONTROLLER_MAINTENANCE Human Gate with an exact patch proposal. Do NOT modify the
controller governance, validator, envelope/schema or agent configuration under A1.

Only after runtime qualification and controller validation are acceptable, read docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md, the active autonomy envelope for the current front, and the state file referenced by that envelope. Apply ADR-0025 state precedence; historical B0/DAG/runbooks are not live state. Load only the normative documents needed for the current gate.

Verify mutable Git identities from the repository; do not trust this prompt for current SHA, tree, branch state or remote state.

Act as the root controller. Use the configured subagents aggressively for independent investigation and audit, but keep exactly one write-capable executor at a time. Subagents must not spawn subagents.

Continue autonomously through investigation → implementation → deterministic verification → independent audit → causal repair → reverification while every action remains within the active autonomy envelope.

Never retry the same material command on the same state merely to seek green. A new attempt requires a recorded causal delta. Preserve every failed or blocked historical attempt.

For external effects, separate process status from effect status and verification status. After any failure that could have started a write, reconcile read-only before considering another mutation. UNKNOWN is not absence.

Do not ask me for actions already covered by active A0/A1/A2 authority. Stop only at a Human Gate defined by the protocol/envelope, unresolved UNKNOWN effect, security/evidence boundary, material scope change, or repair-budget exhaustion.

Do not infer policy promotion, Ready or merge from technical PASS. Those remain human gates.

Begin by reconciling the repository and campaign state and tell me only the current controller state, material blockers and next autonomous action. Then execute.
```

Para B1, o envelope inicial é:

`docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json`.
