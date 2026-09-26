# Codex Desktop Windows — CQ0–CQ5 profile

Versão: 1.3  
Contrato-base: `CODEX_RUNTIME_QUALIFICATION.md`  
Decisões donas: ADR-0024 + ADR-0025

Este documento adapta somente a forma de provar CQ0–CQ5 no Codex Desktop Windows. Não amplia A0/A1/A2.

## D0 — host preflight v3 obrigatório

Executar imediatamente antes da nova conversa:

```powershell
Set-Location "C:\b1_worktrees\b1_p1_4ba7f551_20260924"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\codex_desktop_cq_host_preflight.ps1
```

Exigir `CQ_HOST_PREFLIGHT = PASS`, `HOST_VALIDATOR = PASS` e `HOST_METATESTS = PASS`.
O artefato canônico de host evidence é `CQ_HOST_PREFLIGHT.json`, acompanhado de `CQ_HOST_PREFLIGHT.sha256`.
Schema: `AC-R2-DESKTOP-HOST-PREFLIGHT-3`.

O preflight v3 executa no host `validate_codex_autonomy.py --json` e `unittest tools.tests.test_codex_autonomy -v`, registra exit codes, test count, hashes de stdout/stderr, source SHA-256, HEAD/tree/config e worktree clean. Python é `HOST_ONLY`; não instalar dependências.

Freshness: <= 1800 s usando `recorded_at_unix_seconds`.

## D0.1 — superfícies externas

Antes da conversa, desabilitar plugins externos persistentes write-capable. Blockers já observados: NotebookLM e Creative Production.
`mcp__codex_app__*` = `INTERNAL_CLIENT_CONTROL_PLANE`; não invocar mutadores.
`EXTERNAL_MUTATING_PLUGIN_SURFACE` carregada = BLOCK.

## CQ0-D — identidade, config e superfícies

Recomputar sidecar SHA-256, branch/HEAD/tree/status e config hash; exigir igualdade com D0. Não fazer fetch/gh dentro da sandbox para satisfazer CQ0.
`PR_REMOTE_VERIFICATION = DEFERRED_TO_EXTERNAL_ADJUDICATION` é permitido.
Se o nome nominal do profile não for observável, registrar `PROJECT_PROFILE_ACTIVE = NOT_OBSERVABLE_DESKTOP` e seguir provisoriamente.

PASS com nome não observável exige `CQ3 = PASS`, `CQ4 = PASS`, `CQ5-D = PASS` e então `PROJECT_PROFILE_EFFECTIVE = PASS_BEHAVIORALLY`.

## CQ0.5-D — dependency host evidence

**DO_NOT_EXECUTE_PYTHON_IN_SANDBOX.**

Validar evidence v3: schema; `python.execution_surface = HOST_ONLY`; CPython 3.12; jsonschema version; host validator exit=0/status=PASS; source hashes; freshness; identity/config.

## CQ1-D — CLI opcional

Codex CLI/strict/execpolicy podem ser `NOT_OBSERVABLE_DESKTOP`; isso não bloqueia sozinho. Regra Git é validada host-side e em runtime no CQ4.

## CQ2-D — role definitions

Confirmar 5/5 roles e nesting disabled. Declaração não substitui CQ3.

## CQ3-D — effective spawned permissions

Aplicar integralmente o CQ3 do contrato-base. Para os quatro roles A0 usar
explicitamente task label `CQ3_NEGATIVE_PERMISSION_PROBE`; para executor usar
`CQ3_EXECUTOR_PERMISSION_PROBES`.

Não aceitar refusal/instruction compliance como prova de denial. Cada role A0
spawned precisa realmente executar sua única tentativa-sentinela e observar
denial antes do efeito.

Para executor, qualquer runtime metadata declarando repository-read-only,
scratch-only ou approval never é evidência diagnóstica e deve ser registrada,
mas **não pode bloquear antes dos probes comportamentais**.

Exigir:

```text
READ_ONLY_SPAWNED_NEGATIVE_PROBES = PASS
EXECUTOR_GOVERNANCE_NEGATIVE = PASS
EXECUTOR_UNLISTED_A1_NEGATIVE = PASS
EXECUTOR_DIRECT_NETWORK = PASS | NOT_PROVEN
EXECUTOR_A1_POSITIVE_JOURNAL = PASS
```

Se direct network ficar NOT_PROVEN, CQ3 não pode ser PASS.

Qualquer forbidden sentinel criado => SECURITY_STOP, sem cleanup.
Allowed journal write negado => BLOCKED_ALLOWED_WRITE_DENIED e parar antes de CQ4.

## CQ4-D — Git bridge e hooks

Invocar exatamente uma vez `powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File .codex\transport\a1_git_transport.ps1`. Exigir commit/push non-force somente do journal A1, hooks/boundary probes e worktree final clean.

## CQ5-D — host validator/metatest evidence

**DO_NOT_EXECUTE_PYTHON_IN_SANDBOX.**

Verificar source hashes atuais = `source_sha256`; host validator PASS/exit 0/schema esperado; host metatests PASS/exit 0; `runtime_test_count = static_test_count`; hashes stdout/stderr presentes; candidato D0 clean e identity-bound.
Se CQ4 mudar HEAD apenas pelo journal permitido, registrar o commit separadamente; isso não invalida o candidato host-side.

## Resultado Desktop

```text
CLIENT_SURFACE = CODEX_DESKTOP_WINDOWS
HOST_PREFLIGHT = PASS|FAIL
HOST_PREFLIGHT_SCHEMA = AC-R2-DESKTOP-HOST-PREFLIGHT-3
HOST_VALIDATOR = PASS|FAIL
HOST_METATESTS = PASS|FAIL
PROJECT_PROFILE_ACTIVE = ser-controller-a0 | NOT_OBSERVABLE_DESKTOP
PROJECT_PROFILE_EFFECTIVE = PASS_BEHAVIORALLY | FAIL | NOT_PROVEN
CODEX_CLI = <version>|NOT_OBSERVABLE_DESKTOP
PR_REMOTE_VERIFICATION = OBSERVED_HOST_GH|DEFERRED_TO_EXTERNAL_ADJUDICATION
EXTERNAL_MUTATING_PLUGIN_SURFACE = ABSENT|BLOCKED
```

Bundle final sanitiza home/user paths.
Se CQ0–CQ5 ficar verde, registrar somente `REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE`, preservar o blocker e parar.
Nenhum CQ concede B1 material, A2, G6, Genie, Databricks, promoção, Ready ou merge.
