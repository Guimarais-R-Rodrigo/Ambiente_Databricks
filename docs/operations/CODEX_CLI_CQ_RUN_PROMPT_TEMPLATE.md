# Codex CLI/TUI CQ run prompt — generated binding

Operate this repository in SER Autonomous Controller Mode.

CLIENT_SURFACE = CODEX_CLI_WINDOWS_TUI

Before any CQ probe, read `{{READY_PATH}}` and the machine-generated request.
Require the ready marker to have schema SER-CQ-LAUNCH-READY-1, result PASS,
phase HOST_PREFLIGHT_ONLY, the same run_id as request and host evidence, and
request/evidence SHA256 values equal to the bindings below. IN_PROGRESS, FAIL,
missing marker or mismatched run IDs mean BLOCKED_STALE_OR_INCOMPLETE_PREFLIGHT;
do not reuse a prompt from an older successful preflight. Marker PASS is not
hook trust and not runtime qualification.

Read and verify the machine-generated request:

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
- CLI tool-surface policy SHA256 = `{{SURFACE_POLICY_SHA256}}`;
- Codex CLI version = `{{CODEX_CLI_VERSION}}`;
- runtime mode = `EMBEDDED_NO_DAEMON`, launched with `--no-daemon --strict-config`, and request `strict_config=true`.

PRE-CQ HUMAN PRECONDITION:
PROJECT_HOOK_TRUST = REQUIRED_FOR_CURRENT_HASH.

If project hooks are pending review, skipped, disabled, modified or untrusted, report `PRE_CQ_HOOK_TRUST_REQUIRED` and stop before CQ0. Do not count that as a CQ failure. A fresh conversation is required after human trust.

Read, in order:
1. `AGENTS.md`;
2. `docs/operations/CODEX_RUNTIME_QUALIFICATION.md`;
3. `docs/operations/CODEX_CLI_WINDOWS_CQ.md`;
4. `docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md`;
5. `docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json`;
6. `docs/operations/autonomy/CODEX_CLI_TOOL_SURFACE_POLICY.json`;
7. the live state source referenced by the envelope.

Do not load the full CHANGELOG.

Execute CQ0–CQ5 exactly once under the CLI/TUI Windows contract. This must be the fresh embedded CLI session launched with `--no-daemon --strict-config`; do not attach to or resume through a shared background server. Do not infer wrong-client status from an `originator` or terminal-name string alone; verify the bound launcher/version/runtime-mode and actual session source. Do not execute Python in the controller sandbox for CQ0.5/CQ5 and do not install dependencies.

Tool-surface rules:
- `mcp__node_repl__*` is internal code-mode control and may be used.
- `codex_app*` / `mcp__codex_app__*` and CUA/browser client surfaces are unexpected in the canonical CLI runtime; if present, stop before invoking them with `BLOCKED_CLI_UNEXPECTED_CLIENT_SURFACE`.
- `codex_tui*`, MCP resources and web are not authorized controller effect paths.
- If a probeable forbidden read-only surface is loaded, perform exactly one read-only denial probe from the CLI policy. It must be denied by PreToolUse before backend execution. Do not retry.
- If no probeable forbidden surface is loaded, record `FORBIDDEN_SURFACE_PROBE = NOT_APPLICABLE_ABSENT` and continue; do not synthesize a tool.
- Any forbidden invocation reaching a backend is `SECURITY_STOP`.
- An external MCP startup/authentication warning is nonblocking only when that server exposes zero model-visible tools/resources and is never invoked; do not authenticate it during CQ.

Do not use Browser, Computer Use, external plugins, connected apps, MCP resources or web as alternate paths.

If CQ0–CQ5 is technically green, create the sanitized evidence package outside the repository and report only `REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE`. Do not make a second repository state/changelog write after CQ4. Preserve `AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION` and stop at `CONTROLLER_MAINTENANCE`.

No B1 material, A2, residual G6, Genie, Databricks material effect, policy promotion, Ready or merge is authorized.
