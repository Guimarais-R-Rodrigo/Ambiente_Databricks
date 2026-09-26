# Codex Autonomous Controller — auditoria corretiva AC-R1

Data: 2026-09-26  
Candidata estática auditada: `9a1ec4e7425ac7d411f81e83da6cf919235fa7a5`  
Escopo: ADR-0024 + ADR-0025 / SER B1

## Veredito

```text
AC_R1_STATIC_ARCHITECTURE_AUDIT = PASS
MATERIAL_FINDINGS_OPEN = 0
RUNTIME_QUALIFICATION = NOT_RUN
EFFECTIVE_CONFIG_OBSERVATION = NOT_RUN
A0 = ACTIVE
A1 = ACTIVE_SCOPED
A2 = PENDING_EXPLICIT_ACTIVATION_AND_CONTRACT
A3 = HUMAN_ONLY
READY_FOR_RUNTIME_QUALIFICATION = YES
READY_FOR_MATERIAL_B1_WORK = NO_UNTIL_RUNTIME_QUALIFICATION
```

Este PASS prova somente a arquitetura versionada. O primeiro Codex deve executar
`CODEX_RUNTIME_QUALIFICATION.md` e os validators no checkout real.

## Findings da auditoria anterior e disposição

| Finding | Severidade | Disposição AC-R1 |
|---|---|---|
| custom agents sem `name`/`description` obrigatórios | crítica | FIXED |
| validator aceitava esse schema inválido | crítica | FIXED |
| `CONTROLE_PLANO.json` parecia state vivo B0 | crítica | FIXED |
| executor determinístico e A1 authoring executor ambíguos | alta | FIXED via ADR-0025 |
| governança autoeditável pelo próprio A1 | alta | FIXED com CONTROLLER_MAINTENANCE |
| A1 sem roots machine-readable | alta | FIXED envelope v2 |
| A2 sem contrato estrutural | alta | FIXED schema v2; A2 continua disabled |
| permissões efetivas não provadas pelo TOML | alta | RUNTIME GATE CQ0–CQ5 |
| `CLAUDE.md` canônico sem controller/B1 corrente | alta | FIXED |
| Plano Mestre/B0/B1/DAG/runbooks com estado legado | alta | FIXED por precedence/snapshot markers |
| Genie assumia coleta exclusivamente humana | alta | FIXED para coleta controlada/capability-bound |
| defaults de reasoning excessivos | média | FIXED |
| `AGENTS.md` exigia pergunta/teste global por rotina | média | FIXED |
| hooks/delta inexistentes para A1 | média | FIXED defense-in-depth |

## Custom agents

Os cinco arquivos em `.codex/agents/` possuem:

- `name`;
- `description`;
- `developer_instructions`;
- sandbox por papel;
- nesting desabilitado.

Topologia:

- explorer: GPT-6 Luna / high / read-only;
- executor: GPT-6 Sol / medium / workspace-write;
- domain-auditor: GPT-6 Astra / high / read-only;
- evidence-auditor: GPT-6 Astra / high / read-only;
- architecture-auditor: GPT-6 Astra / high / read-only.

Há exatamente um papel write-capable.

## Root controller

Project config esperado:

```text
model = gpt-6-astra
reasoning = high
sandbox = workspace-write
approval_policy = on-request
approvals_reviewer = auto_review
sandboxed command network = false
multi_agent = true
goals = true
hooks = true
max concurrent subagents = 5
```

Auto-review reduz interrupções técnicas, mas não é autoridade SER. Human Gates
continuam exigindo referência humana no envelope/contrato.

## Autoridade e self-modification

Envelope v2 introduz:

- `write_roots`;
- `protected_roots`;
- `shared_roots_requiring_human_gate`;
- `CONTROLLER_MAINTENANCE`;
- `a2_contract`.

A1 não pode modificar a camada de governança para corrigir sua própria falha.

## Defense in depth

Além do envelope:

- `.codex/hooks.json` habilita PreToolUse para patches e PostToolUse para
  shell/patch;
- hooks Python e PowerShell classificam paths contra o envelope;
- `tools/check_codex_autonomy_delta.py` bloqueia delta A1 fora dos roots.

Hooks são guardrail e feedback, não fronteira absoluta. O sandbox é a fronteira
técnica principal. Em `workspace-write`, `.git`, `.codex` e `.agents`
são protegidos read-only pelo cliente atual; isso ainda deve ser observado no
runtime.

## Estado e documentação legada

ADR-0025 fixa precedência:

1. `B1/AUTHORING_STATE.json`;
2. índices correntes;
3. contratos do gate;
4. snapshots/runbooks/tentativas históricas.

Foram marcados como não-live:

- `CONTROLE_PLANO.json`;
- `catalogos/DAG.json`;
- `catalogos/BLOQUEIOS.json`;
- `catalogos/PRONTIDAO.json`;
- G6 runbook congelado;
- G6 plano pré-execução.

B0 README registra `INTEGRATED_CLOSED`; B1 README possui bloco corrente.

## Invariância funcional B1

A AC-R1 não altera:

- `ambiente_fonte/**`;
- mirror de produto em `Novo_Ambiente_Simulado/.../.assistant/**`;
- pacote G6 congelado;
- publisher R10;
- policy.

Portanto a AC-R1 é mudança de governança/coordenação, não nova candidata de
produto nem nova tentativa G6.

## Validator

`tools/validate_codex_autonomy.py` agora:

- valida o envelope com Draft 2020-12 real;
- exige `name`/`description`/`developer_instructions` dos agents;
- exige exatamente um writer;
- reprova `danger-full-access`;
- exige A2 reference + contract para ativação;
- exige roots A1;
- exige hooks;
- exige runtime qualification/documentos donos.

A suíte tem 16 métodos definidos estaticamente na candidata auditada.

## Limitações obrigatórias

Não foram executados nesta sessão GitHub-side:

- parse/runtime local dos TOMLs pelo cliente Codex;
- project trust;
- `/status`;
- `/debug-config`;
- `--strict-config`;
- sandbox negative probes;
- hooks reais;
- validator Python;
- 16 metatestes.

Esses itens pertencem ao gate runtime CQ0–CQ5.

## Fontes oficiais verificadas em 2026-09-26

- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/hooks
- https://learn.chatgpt.com/docs/developer-settings
- https://learn.chatgpt.com/docs/config-file/config-advanced
- https://learn.chatgpt.com/docs/agent-approvals-security
- https://learn.chatgpt.com/docs/sandboxing/auto-review

## Próximo gate

```text
NEXT = CONTROLLER_RUNTIME_QUALIFICATION
REMOTE_EFFECT = NONE
A2 = NOT_ACTIVE
PROMOTION = NOT_AUTHORIZED
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```
