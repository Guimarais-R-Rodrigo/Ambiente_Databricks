# Prompt inicial — Codex Autonomous Controller

Runtime canônico no Windows: **Codex CLI/TUI**, nunca Codex Desktop.

O Desktop foi desqualificado para o controller após duas execuções CQ independentes em que uma superfície `codex_app` proibida alcançou o backend apesar de hooks project-local ativos e confiados. Não relaxar a policy para contornar esse resultado.

## 1. Checkout

Use somente o standalone checkout:

```powershell
Set-Location "C:\b1_runtime\b1_p1_4ba7f551_20260924"
```

Linked worktree continua proibido.

## 2. Fresh CLI host preflight

```powershell
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File .\tools\codex_cli_cq_host_preflight.ps1
```

Só continuar se aparecerem simultaneamente:

```text
CQ_HOST_PREFLIGHT = PASS
HOST_VALIDATOR = PASS
HOST_METATESTS = PASS
NETWORK_PROBE_SERIALIZATION_SELFTEST = PASS
NETWORK_PROBE_OFFLINE_RUNTIME_SELFTEST = PASS
EXTERNAL_SURFACE_GUARD_SELFTEST = PASS
SCOPE_GUARDS_SELFTEST = PASS
HOOK_WIRE_RUNTIME_SELFTEST = PASS
EXECPOLICY_HOST_SELFTEST = PASS
A1_PRIVILEGED_BRIDGE_GUARD_SELFTEST = PASS
A1_PATCH_TRANSPORT_SELFTEST = PASS
A1_FILESYSTEM_PROBE_SELFTEST = PASS
A1_GIT_TRANSPORT_SELFTEST = PASS
A1_OPERATIONAL_TRANSPORT_SELFTEST = PASS
WINDOWS_SANDBOX_NETWORK_INTEGRITY = PASS
HOST_NETWORK_BASELINE = PASS
CHECKOUT_MODE = STANDALONE
CLIENT_SURFACE = CODEX_CLI_WINDOWS_TUI
HOOK_TRUST_REVIEW_REQUIRED = true
CQ_READY_TO_RUN = AFTER_PROJECT_HOOK_TRUST
```

O preflight grava `CQ_HOST_PREFLIGHT.json`, `CQ_RUN_REQUEST.json` e `CQ_RUN_PROMPT.md` no scratch externo.

## 3. Trust dos hooks no mesmo standalone

`PROJECT_HOOK_TRUST = REQUIRED_FOR_CURRENT_HASH`. Revisar a definição e os scripts atuais; o preflight não concede trust e nenhum launcher pode fazê-lo pelo usuário.

Inicie o executável explicitamente bound pelo preflight; nesta máquina:

```powershell
& "$env:APPDATA\npm\codex.cmd" --no-daemon --strict-config
```

No TUI execute `/debug-config` e `/hooks`. Exigir a config de projeto do standalone e `PreToolUse 3/3 Active`, `PostToolUse 1/1 Active`. Se houver review pendente, confiar a definição atual. `HOOK_TRUST_REVIEW_REQUIRED = true` não é autorização automática. Se qualquer operação de leitura durante essa sessão mostrar `Hook failed` ou exit não-zero, não confirmar `HOOKS_REVISADOS`: sair e tratar como blocker de runtime.

## 4. Conversa CQ nova

Após o trust, saia da sessão usada para revisão e abra uma **nova** sessão CLI/TUI no mesmo standalone, também com `--no-daemon --strict-config`. Não reutilize/resuma uma thread do shared background server. Copie o conteúdo integral de `CQ_RUN_PROMPT.md` e cole nessa nova conversa. No Windows Terminal, prefira `Ctrl+Shift+V` ou botão direito se `Ctrl+V` for interpretado como imagem.

Não use o Codex Desktop para este CQ.

## 5. Encerramento

Traga o bundle externo de evidências para adjudicação. CQ verde para em `CONTROLLER_MAINTENANCE`; não remove blocker e não autoriza B1 material, A2, G6/Genie/Databricks, promoção, Ready ou merge.

## Retomada assistida no PC

O script externo `RETOMAR_CQ.ps1` entregue com o freeze sincroniza somente os dois checkouts conhecidos por fast-forward, executa o preflight e verifica os hashes antes da revisão humana. Depois da revisão em `/hooks`, exige confirmação explícita `HOOKS_REVISADOS` e abre uma sessão CLI/TUI nova que lê `CQ_RUN_PROMPT.md` pelo caminho e SHA. Não é necessário copiar o prompt pelo clipboard nem retornar ao ChatGPT apenas para confirmar uma saída host verde.

`CQ_LAUNCH_READY.json` é marcador técnico da última tentativa host: `IN_PROGRESS`/`FAIL` nunca libera o prompt antigo; `PASS` atesta somente `HOST_PREFLIGHT_ONLY`. Ele não é trust, autorização, assinatura ou resultado CQ. Request/evidence/marker devem compartilhar `run_id`; source hashes, launcher e freshness continuam obrigatórios.

O helper não corrige erros por retry. Somente expiração da freshness durante a revisão humana permite regeneração única por essa causa. Em falha, um ZIP com logs restritos e diagnóstico é preparado fora do repositório; revisar antes de compartilhar. Não coleta auth.json, user config, chat history ou variáveis de ambiente. O helper não envia arquivos nem concede B1 material/A2/Ready/merge. O bundle final do CQ continua exigindo adjudicação.

Nota de 28/09/2026: uma tentativa pós-trust foi interrompida antes de CQ0 porque a sessão observada reportou versão/source diferentes do launcher preflight. A investigação do Codex 0.157.1 mostrou que o TUI pode reutilizar um shared background server; por isso revisão e CQ passam a exigir `--no-daemon`. `originator`/terminal-name isolado não é oráculo de identidade.


## A1 bridge qualification note — 2026-09-28

Do not expect the executor subagent to carry `ser-b1-a1`. The canonical design
keeps every spawned role on `ser-controller-a0`. Repository mutation is
performed only by the root controller through the exact no-argument
`.codex\transport\a1_patch_transport.ps1` command, which is protected by a
root-origin PreToolUse guard and by an in-script root-session gate. The bridge
then invokes `codex sandbox -P ser-b1-a1` for the actual file effect.
