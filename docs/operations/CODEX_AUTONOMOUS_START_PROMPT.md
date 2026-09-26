# Prompt inicial — Codex Autonomous Controller

Use este prompt em uma nova sessão Codex iniciada na raiz do repositório:

```text
Operate this repository in SER Autonomous Controller Mode.

Read AGENTS.md and docs/operations/CODEX_RUNTIME_QUALIFICATION.md. Do not load
the full CHANGELOG; use search/tail only when history is material.

Run CQ0-CQ5 exactly. Do not start material B1 work during qualification.

Expected AC-R2 posture:
- root, explorer and auditors: ser-controller-a0, repository read-only;
- executor: ser-b1-a1, only the ten exact envelope paths writable;
- executor has no direct .git write and no command network;
- no legacy sandbox_mode;
- Windows native sandbox elevated;
- executor granular approvals expose only execpolicy rule prompts;
- executor reviewer = auto_review;
- project does not override [auto_review].policy;
- Git commit/push only through .codex/transport/a1_git_transport.ps1;
- no write-capable MCP/app/hosted surface outside an explicit contract.

Do not use /permissions, --yolo, sandbox widening, request_permissions or another
override to make a failing target pass.

Run strict config/execpolicy checks and:

python -B tools/validate_codex_autonomy.py --json
python -B -m unittest tools.tests.test_codex_autonomy -v

Perform the real spawned-role negative probes in CQ3. The only positive A1 repo
write during qualification is the append-only CQ line in
B1/AUTONOMY/JOURNAL.jsonl. CQ4 must commit/push that delta through the protected
A1 Git transport, not by direct git metadata/network access.

If CQ0-CQ5 is green, do NOT remove
AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION and do NOT write canonical PASS.
Record only REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE for runtime/effective
config, preserve the blocker, and stop at the existing CONTROLLER_MAINTENANCE
Human Gate with the CQ evidence.

If any CQ fails, report the exact failure and stop at CONTROLLER_MAINTENANCE.
Never self-repair controller governance under A1.

A2, residual G6 effects, Genie, policy promotion, Ready and merge are not
authorized by this prompt.
```

B1 envelope:
`docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json`.
