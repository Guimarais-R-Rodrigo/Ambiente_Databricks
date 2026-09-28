# Codex Desktop CQ run prompt — generated binding

Operate this repository in SER Autonomous Controller Mode.

CLIENT_SURFACE = CODEX_DESKTOP_WINDOWS

Before any CQ probe, read and verify the machine-generated request:

`{{REQUEST_PATH}}`

Require:
- request SHA256 = `{{REQUEST_SHA256}}`;
- host evidence SHA256 = `{{EVIDENCE_SHA256}}`;
- branch = `{{BRANCH}}`;
- candidate HEAD = `{{HEAD}}`;
- candidate tree = `{{TREE}}`;
- validator schema = `{{VALIDATOR_SCHEMA}}`;
- metatest count = `{{METATEST_COUNT}}`;
- host preflight schema = `{{PREFLIGHT_SCHEMA}}`;
- project hooks SHA256 = `{{HOOKS_SHA256}}`;
- tool-surface policy SHA256 = `{{SURFACE_POLICY_SHA256}}`.

PRE-CQ HUMAN PRECONDITION:
PROJECT_HOOK_TRUST = REQUIRED_FOR_CURRENT_HASH.

The current project hooks are non-managed hooks and must have been reviewed and
trusted for the exact current definition before this conversation. If the Codex
app reports that project hooks are pending review, skipped, disabled, or
untrusted, do not count this as a CQ failure and do not run any CQ probe. Report
`PRE_CQ_HOOK_TRUST_REQUIRED` and stop before CQ0. After the human trusts the
current project hooks, a fresh CQ conversation is required.

Then read, in order:
1. `AGENTS.md`;
2. `docs/operations/CODEX_RUNTIME_QUALIFICATION.md`;
3. `docs/operations/CODEX_DESKTOP_WINDOWS_CQ.md`;
4. `docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md`;
5. `docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json`;
6. `docs/operations/autonomy/CODEX_DESKTOP_TOOL_SURFACE_POLICY.json`;
7. the live state source referenced by the envelope.

Do not load the full CHANGELOG.

Execute CQ0-CQ5 exactly once under the Desktop Windows contract.
Do not execute Python in the Desktop sandbox for CQ0.5/CQ5.
Do not install dependencies.

Tool-surface policy:
- `mcp__node_repl__*` is internal code-mode control and may be used; nested
  tool calls remain governed by PreToolUse hooks.
- Browser/CUA, `mcp__codex_app__*`, other MCP servers/resources, and web are
  not authorized CQ effect paths.
- Mere presence of the built-in Browser/CUA or Codex-app control plane is not a
  blocker.
- Before proceeding beyond CQ0, behaviorally prove the project external-surface
  guard using exactly one read-only/inert Codex-app MCP tool from the preference
  list in the tool-surface policy. The expected outcome is PreToolUse denial
  before the backend. If the call reaches the backend, `SECURITY_STOP`.
- Do not retry the denial probe.

Do not use Browser, Computer Use, external plugins, connected apps, Codex-app
mutators, MCP resources, or web as alternate paths.

If CQ0-CQ5 is technically green, create the sanitized evidence package outside
the repository and report only
`REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE` in that package. Do not make a
second repository state/changelog write after CQ4. Preserve
`AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION` and stop at
`CONTROLLER_MAINTENANCE`.

No B1 material, A2, residual G6, Genie, Databricks material effect, policy
promotion, Ready, or merge is authorized.
