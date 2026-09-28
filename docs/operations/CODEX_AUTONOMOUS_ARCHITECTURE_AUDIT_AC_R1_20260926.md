# Codex Autonomous Controller — auditoria corretiva AC-R1

Data: 2026-09-26  
Candidata funcional/governança auditada: `6abd7a12b60a042f0e219d4cca3a810a6c919d9a`  
Tree: `e83b8c329f17d15de1c477204c2a82e07e32d1bd`  
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
READY_FOR_MATERIAL_B1_WORK = NO_UNTIL_CQ0_CQ5
```

Este PASS é estático e repo-side. O primeiro Codex deve executar
`docs/operations/CODEX_RUNTIME_QUALIFICATION.md` e os validators no checkout
real antes de assumir trabalho material de B1.

## Findings e disposição

| Finding | Disposição AC-R1 |
|---|---|
| custom agents sem `name`/`description` obrigatórios | FIXED |
| validator com risco de false-green | FIXED |
| `CONTROLE_PLANO.json`/DAG pareciam state vivo | FIXED |
| executor determinístico versus A1 authoring executor ambíguos | FIXED via ADR-0025 |
| governança autoeditável pelo próprio A1 | FIXED com `CONTROLLER_MAINTENANCE` |
| A1 sem roots machine-readable | FIXED envelope v2 |
| A2 sem contrato estrutural | FIXED schema v2; A2 continua disabled |
| permissões efetivas não provadas pelo TOML | CQ0–CQ5 obrigatório |
| `CLAUDE.md` canônico sem controller/B1 corrente | FIXED |
| Plano Mestre/B0/B1/checklist/runbooks legados | FIXED por precedência/snapshot markers |
| Genie assumia coleta exclusivamente humana | FIXED para coleta controlada |
| defaults de reasoning excessivos | FIXED |
| `AGENTS.md` induzia pergunta/teste global por rotina | FIXED |
| A1 permitia todo `real_campaigns/b1/**` | FIXED; somente recovery |
| A1 documental permitia reescrever evidência histórica | FIXED; state/changelog/journal apenas |
| MCP/apps/hosted tools poderiam contornar hooks locais | FIXED; A1 local-worktree-only |
| dependência `jsonschema` não declarada | FIXED em requirements dedicado |
| Apps/remote-plugin ampliavam superfície sem necessidade | FIXED; disabled |
| worktree dirty poderia causar atribuição ambígua | FIXED; CQ0 exige clean |

A auditoria antiga de `c5d30330...` permanece histórica e explicitamente
supersedida; não é release gate.

## Custom agents e topologia

Cinco agents project-scoped com `name`, `description` e
`developer_instructions`:

- explorer — GPT-6 Luna / high / read-only;
- executor — GPT-6 Sol / medium / workspace-write;
- domain-auditor — GPT-6 Astra / high / read-only;
- evidence-auditor — GPT-6 Astra / high / read-only;
- architecture-auditor — GPT-6 Astra / high / read-only.

Há exatamente um writer e nesting de subagentes está desabilitado.

## Root controller

Config versionada esperada:

```text
model = gpt-6-astra
reasoning = high
sandbox = workspace-write
approval_policy = on-request
approvals_reviewer = auto_review
sandboxed command network = false
apps = false
remote_plugin = false
multi_agent = true
goals = true
hooks = true
max_concurrent_subagents = 5
```

Auto-review trata apenas approvals técnicos do sandbox. Não cria autoridade SER.

## A1

Write roots:

- `tools/skill_enforcement/real_campaigns/b1/g6_recovery/**`;
- `tools/tests/test_ser_b1_g6_recovery.py`;
- `B1/AUTHORING_STATE.json`;
- `B1/CHANGELOG.md`;
- `B1/AUTONOMY/**`;
- `CHANGELOG.md`.

G6 congelado, publisher R10, evidências históricas G6/P2, produto, mirror, policy,
B0, micromodelos e governança do controller estão fora do write scope.

A1 escreve somente pelo worktree local; MCP/apps/hosted remote APIs não podem
mutar repo/refs. Normal `git push` é o único transporte remoto Git A1.

## Hooks e delta

- PreToolUse para patches;
- PostToolUse para Bash/patch;
- implementações Python + PowerShell;
- `tools/check_codex_autonomy_delta.py` antes de commit/push.

Hooks são defense-in-depth e feedback, não fronteira de segurança completa.

## A2

A2 permanece inativa:

```text
activation.state = ACTIVE_A0_A1
a2_reference = null
a2_contract = null
A2.autonomous = false
```

O schema exige target, namespace, effects, budgets, synthetic-only, overwrite,
readback, UNKNOWN policy e cleanup antes de A2 poder ficar ativa.

## Estado vivo versus legado

ADR-0025 fixa:

1. `B1/AUTHORING_STATE.json`;
2. índices correntes;
3. contrato do gate;
4. snapshots/runbooks/tentativas históricas.

B0/DAG/blockers/readiness e G6 pre-execution runbooks foram marcados como
snapshots/histórico quando aplicável. Proibições de patch durante campanha foram
qualificadas como regras do executor determinístico; repair A1 ocorre entre
rodadas em novo causal delta.

## Dependency/runtime bootstrap

O validator usa Draft 2020-12 por `jsonschema`. A dependência está isolada em:

`tools/requirements-codex-autonomy.txt`

e não altera `tools/requirements-dev.txt` nem seus digests históricos.

CQ0.5 permite apenas sincronizar esse requirements dedicado no ambiente isolado
do controller se o import estiver ausente; a operação de rede continua sujeita
ao sandbox/auto-review.

## Validator e metatestes

O validator:

- valida envelope com Draft 2020-12;
- exige os campos obrigatórios dos cinco agents;
- exige exatamente um writer;
- reprova `danger-full-access`;
- exige A1 roots;
- exige A2 reference + contract para ativação;
- exige hooks/runtime qualification/requirements dedicado;
- exige apps/remote-plugin disabled;
- verifica bindings de documentos donos.

A suíte possui **22 métodos** definidos estaticamente.

## Invariância funcional

Compare contra a base B1 pré-controller
`d3871d27e34af3940153b8df47b4dcfd5739ff85`:

- branch ahead, behind 0;
- nenhuma mudança em `ambiente_fonte/**`;
- nenhuma mudança no mirror de produto;
- nenhuma mudança em policy;
- nenhuma mudança no G6 congelado;
- nenhuma mudança no publisher R10.

Logo AC-R1 é governança/coordenação, não nova candidata de produto nem tentativa G6.

## Limitações

Ainda NOT_RUN no runtime real:

- project trust;
- effective config;
- clean-worktree preflight;
- `/status`/`/debug-config` quando disponíveis;
- strict config quando observável;
- sandbox/approval overrides;
- hooks reais e negative probes;
- dependency bootstrap se necessário;
- validator Python;
- 22 metatestes.

## Fontes oficiais verificadas em 2026-09-26

- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/hooks
- https://learn.chatgpt.com/docs/config-file/config-reference
- https://learn.chatgpt.com/docs/config-file/config-advanced
- https://learn.chatgpt.com/docs/agent-approvals-security
- https://developers.openai.com/pt-BR/docs/sandboxing

## Fechamento

```text
AC_R1_STATIC = PASS
NEXT = CONTROLLER_RUNTIME_QUALIFICATION_CQ0_CQ5
REMOTE_EFFECT = NONE
A2 = NOT_ACTIVE
PROMOTION = NOT_AUTHORIZED
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```

O commit que grava este relatório é apenas docs/state/changelog e não contém a
própria identidade para evitar circularidade. Após o commit, deve ser revalidado
externamente que `6abd7a12b60a042f0e219d4cca3a810a6c919d9a` → HEAD contém somente o fechamento.
