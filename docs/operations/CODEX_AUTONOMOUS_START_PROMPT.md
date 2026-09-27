# Prompt inicial — Codex Autonomous Controller

Para Codex Desktop Windows, **não montar manualmente HEAD/tree/hash em chat**.

1. No worktree dedicado, executar:

```powershell
Set-Location "C:\b1_worktrees\b1_p1_4ba7f551_20260924"
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File .\tools\codex_desktop_cq_host_preflight.ps1
```

2. Só continuar se a saída contiver simultaneamente:

```text
CQ_HOST_PREFLIGHT = PASS
HOST_VALIDATOR = PASS
HOST_METATESTS = PASS
NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS
NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST = PASS
MCP_GUARD_SELFTEST = PASS
SCOPE_GUARDS_SELFTEST = PASS
A1_GIT_TRANSPORT_SELFTEST = PASS
HOST_NETWORK_BASELINE = PASS
CQ_READY_TO_RUN = PASS
```

3. O preflight v6 grava no scratch:

- `CQ_HOST_PREFLIGHT.json` + sidecar SHA256;
- `CQ_RUN_REQUEST.json` + sidecar SHA256;
- `CQ_RUN_PROMPT.md`.

4. Antes da conversa CQ, abrir **Settings > Hooks** no Codex app e revisar/confiar os hooks do projeto para a definição atual. O preflight imprime `PROJECT_HOOKS_SHA256`; hooks alterados não devem ser bypassados. Se já estiverem trusted no hash atual, nenhuma ação adicional é necessária.

5. Só depois do trust, abrir **uma conversa nova** no Codex Desktop do mesmo projeto e colar o conteúdo de `CQ_RUN_PROMPT.md`. O prompt manda o Codex validar diretamente o request machine-readable. Não é necessário voltar ao ChatGPT apenas para interpolar hashes.

6. Ao final do CQ, trazer o bundle de evidências para adjudicação independente. Se CQ0-CQ5 estiver verde, o CQ para em `CONTROLLER_MAINTENANCE`; não remove blocker e não faz B1 material.

Browser/CUA integrado pode aparecer na lista de tools. Sua presença não é blocker. `mcp__node_repl__*` interno pode operar; Browser/CUA, Codex-app, MCP externos/resources e web não são rotas autorizadas. `HOOK_TRUST_REVIEW_REQUIRED` e `PROJECT_HOOK_TRUST` são pré-condições explícitas do handoff.

No B1 material, A2, residual G6, Genie, policy promotion, Ready ou merge é autorizado por este bootstrap.
