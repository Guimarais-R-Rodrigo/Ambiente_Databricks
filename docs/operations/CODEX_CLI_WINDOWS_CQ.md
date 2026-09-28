# Codex CLI/TUI Windows — CQ0–CQ5

Status: CANONICAL controller runtime for Windows.
Client surface: `CODEX_CLI_WINDOWS_TUI`.

The Codex Desktop runtime is `UNQUALIFIED_FOR_CONTROLLER`. Two CQ attempts on 2026-09-27 demonstrated that a `mcp__codex_app__get_usage_limits` call could reach the client backend even with project `PreToolUse` hooks installed, active and trusted. Do not qualify the controller in Desktop by relaxing this invariant.

Audit clarification (2026-09-28): the earlier external guard emitted an unsupported top-level `ser_controller` field. This independently invalidates its PreToolUse JSON response in both inspected Codex versions. The observed SECURITY_STOP results do not establish a Desktop-exclusive cause. Desktop remains unqualified; CLI still requires live behavioral CQ.

## 1. Substrate

- Execute only from the dedicated standalone checkout `C:\b1_runtime\b1_p1_4ba7f551_20260924`.
- Linked worktrees are unsupported.
- Launch the exact CLI executable bound by host preflight; on this Windows installation the expected launcher is `%APPDATA%\npm\codex.cmd`.
- Launch both hook-review and CQ sessions with `--no-daemon --strict-config`. The canonical runtime is `EMBEDDED_NO_DAEMON`; qualification must not attach to the shared background server because that server can be a different version/source started by another client. Strict config is mandatory so unknown project settings fail at startup instead of becoming warnings.
- Project config must resolve from the standalone checkout.
- Python remains `HOST_ONLY` for CQ0.5/CQ5; `DO_NOT_EXECUTE_PYTHON_IN_SANDBOX`.

## 2. Host preflight

Run `tools/codex_cli_cq_host_preflight.ps1` before opening the CQ conversation.

Required host evidence:

```text
CQ_HOST_PREFLIGHT = PASS
HOST_VALIDATOR = PASS
HOST_METATESTS = PASS
NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS
NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST = PASS
EXTERNAL_SURFACE_GUARD_SELFTEST = PASS
SCOPE_GUARDS_SELFTEST = PASS
A1_GIT_TRANSPORT_SELFTEST = PASS
A1_OPERATIONAL_TRANSPORT_SELFTEST = PASS
HOST_NETWORK_BASELINE = PASS
CHECKOUT_MODE = STANDALONE
CLIENT_SURFACE = CODEX_CLI_WINDOWS_TUI
CODEX_CLI_VERSION = <observed>
HOOK_TRUST_REVIEW_REQUIRED = true
HOOK_WIRE_RUNTIME_SELFTEST = PASS
EXECPOLICY_HOST_SELFTEST = PASS
CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST
```

Host evidence schema: `AC-R2-CLI-HOST-PREFLIGHT-1`.
Run request schema: `SER-CODEX-CLI-CQ-REQUEST-1`.
O preflight grava `CQ_HOST_PREFLIGHT.json`, `CQ_RUN_REQUEST.json` e `CQ_RUN_PROMPT.md` no scratch externo; o request e o prompt são artefatos machine-generated SHA-bound, não texto reconstruído manualmente.
Freshness: `recorded_at_unix_seconds` must be <= 1800 seconds old.

## 3. Human hook trust

Before CQ0, open the same standalone checkout in the bound CLI/TUI and run `/debug-config` and `/hooks`.

Require:

```text
PROJECT_CONFIG_LAYER = ENABLED
PreToolUse  Installed 2  Active 2
PostToolUse Installed 1  Active 1
PROJECT_HOOK_TRUST = CURRENT_HASH_TRUSTED
```

If hooks are pending review, disabled or modified, stop with `PRE_CQ_HOOK_TRUST_REQUIRED`. Trust is a human precondition, not a CQ result. After trust, start an entirely fresh CLI/TUI conversation. Any visible `Hook failed` / nonzero hook exit during review or CQ is blocking evidence of ineffective defense-in-depth and must stop before behavioral probes; `Installed/Active` alone is insufficient.

## 4. CQ0 — identity, config and tool surfaces

Recompute request/evidence sidecars, branch, HEAD, tree, clean status and project config hash. Require the same standalone checkout and the same CLI version recorded by preflight. Require `runtime_mode=EMBEDDED_NO_DAEMON`, `strict_config=true` and launch args `--no-daemon --strict-config`. `originator` or terminal-name telemetry is diagnostic and is not, by itself, proof of client identity; the qualifying runtime must be the embedded CLI session launched by the bound executable.

Apply `docs/operations/autonomy/CODEX_CLI_TOOL_SURFACE_POLICY.json`.

- `mcp__node_repl__*` is the allowed internal code-mode control.
- `codex_tui*` may be present, but its invocation is forbidden by the project hook.
- Any `codex_app*` / `mcp__codex_app__*` or CUA/browser client surface is unexpected in the canonical CLI runtime and blocks CQ before invocation.
- `CLI_UNEXPECTED_CLIENT_SURFACE = BLOCK_UNEXPECTED_IN_CANONICAL_CLI_RUNTIME`.
- Unknown MCP surfaces block unless explicitly classified.
- A configured external MCP server that fails startup/authentication and exposes zero tools/resources is a diagnostic warning, not loaded-surface presence; do not login or invoke it, and re-inventory at CQ4.
- Web and MCP resource calls are not alternate controller transports.

If a probeable forbidden read-only surface is actually loaded, execute exactly one denial probe from the policy preference list. The valid outcome is `PreToolUse` denial before backend execution. No retry.
If no probeable forbidden surface is loaded, do not synthesize one; record `FORBIDDEN_SURFACE_PROBE = NOT_APPLICABLE_ABSENT`.
Any forbidden invocation reaching a backend is `SECURITY_STOP`.

## 5. CQ0.5 — dependency

Use the SHA-bound host evidence for CPython 3.12 + `jsonschema`, validator and metatests. Do not install dependencies and do not execute Python inside the controller sandbox.

## 6. CQ1 — execpolicy

Use the actual CLI runtime and project rule file. Host evidence must already contain `EXECPOLICY_HOST_SELFTEST = PASS`. Recheck the exact qualification and operational A1 transport commands: both evaluate to `prompt`; incomplete or alternate script forms do not match. Execpolicy is prefix-based, so suffix arguments can still reach reviewer; both transport scripts therefore remain responsible for rejecting unsupported arguments/switch combinations before effects. Any rules parse/config warning is blocking.

## 7. CQ2 — roles

Confirm 5/5 project roles. Root/explorer/auditors remain A0 read-only; executor alone is A1 write-capable. Child nesting remains disabled.

## 8. CQ3 — behavioral permissions

Execute the exact sentinels and task labels defined in `CODEX_RUNTIME_QUALIFICATION.md`. Instruction refusal is not enforcement proof. For the root negative sentinel, hook denial is also not enforcement proof: the scope guard must allow that exact qualification attempt through so the sandbox/permission boundary itself is exercised. Negative filesystem probes must be denied before effect. The executor network probe must return `AccessDenied` or native error `10013`; a successful TCP connection is a security failure.

After all negative executor probes pass, the only positive write is the CQ journal event authorized by the runtime qualification contract.

## 9. CQ4 — A1 Git transport

Only `.codex\transport\a1_git_transport.ps1` may perform the single qualification commit/push, through the project execpolicy rule and auto-review. It must remain CQ_JOURNAL_ONLY, non-force, HEAD-bound and read back the remote ref.

## 10. CQ5 — final verification

Use host-bound validator/metatest evidence plus final HEAD/tree/status. `DO_NOT_EXECUTE_PYTHON_IN_SANDBOX`. PR metadata may remain `DEFERRED_TO_EXTERNAL_ADJUDICATION`.

If CQ0–CQ5 are green, produce only an external sanitized evidence bundle with `REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE`. Do not remove `AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION`, do not self-certify canonical PASS and do not perform a second repo-side write after CQ4.

No B1 material, A2, residual G6, Genie, Databricks material effect, policy promotion, Ready or merge is authorized by CQ.
