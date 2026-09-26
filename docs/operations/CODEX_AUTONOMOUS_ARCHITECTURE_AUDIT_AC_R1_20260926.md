# Codex Autonomous Controller — auditoria corretiva AC-R1

Data: 2026-09-26  
Candidata funcional/governança auditada: `3c9db7edec703cb875989430cbb7477d4245c70b`  
Tree: `61f6b300f1910114399664a0b686ef56b63ef478`  
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

## 1. Findings anteriores e disposição

| Finding | Severidade original | Disposição AC-R1 |
|---|---|---|
| custom agents sem `name`/`description` obrigatórios | crítica | FIXED |
| validator aceitava esse schema inválido | crítica | FIXED |
| `CONTROLE_PLANO.json` parecia state vivo B0 | crítica | FIXED |
| executor determinístico e A1 authoring executor ambíguos | alta | FIXED via ADR-0025 + docs 01/02/03/06/07/09 |
| governança autoeditável pelo próprio A1 | alta | FIXED com `CONTROLLER_MAINTENANCE` |
| A1 sem roots machine-readable | alta | FIXED envelope v2 |
| A2 sem contrato estrutural | alta | FIXED schema v2; A2 continua disabled |
| permissões efetivas não provadas pelo TOML | alta | CQ0–CQ5 obrigatório |
| `CLAUDE.md` canônico sem controller/B1 corrente | alta | FIXED |
| Plano Mestre/B0/B1/DAG/runbooks com estado legado | alta | FIXED por precedência/snapshot markers |
| Genie assumia coleta exclusivamente humana | alta | FIXED para coleta controlada/capability-bound |
| defaults de reasoning excessivos | média | FIXED |
| `AGENTS.md` exigia pergunta/teste global por rotina | média | FIXED |
| hooks/delta inexistentes para A1 | média | FIXED defense-in-depth |
| A1 permitia todo `real_campaigns/b1/**` | alta | FIXED: somente `g6_recovery/**` |
| A1 documental permitia reescrever evidência G6/P2 | alta | FIXED: state/changelogs/journal somente |
| MCP/apps poderiam contornar hooks locais para mutar Git | alta | FIXED: A1 local-worktree-only |

A auditoria anterior de `c5d30330...` permanece histórica e está explicitamente
marcada como supersedida; não é release gate.

## 2. Custom agents

Cinco agentes project-scoped, todos com `name`, `description` e
`developer_instructions`:

- explorer — GPT-6 Luna / high / read-only;
- executor — GPT-6 Sol / medium / workspace-write;
- domain-auditor — GPT-6 Astra / high / read-only;
- evidence-auditor — GPT-6 Astra / high / read-only;
- architecture-auditor — GPT-6 Astra / high / read-only.

Cada subagente tem nesting desabilitado. Há exatamente um papel write-capable.

Essa topologia segue a prática atual de agentes estreitos/opinionados, explorer
rápido/read-only e writer único.

## 3. Root controller e approvals

Config versionada esperada:

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
max_concurrent_subagents = 5
```

`auto_review` reduz prompts técnicos de sandbox; não é autoridade SER. A2,
`CONTROLLER_MAINTENANCE`, promoção, Ready e merge continuam exigindo referência
humana no contrato apropriado.

## 4. A1: escopo executável

Write roots atuais:

- `tools/skill_enforcement/real_campaigns/b1/g6_recovery/**`;
- `tools/tests/test_ser_b1_g6_recovery.py`;
- `B1/AUTHORING_STATE.json`;
- `B1/CHANGELOG.md`;
- `B1/AUTONOMY/**`;
- `CHANGELOG.md`.

Protegidos explicitamente:

- produto/mirror/policy;
- B0 shared mechanism;
- micromodelos e `.github`;
- G6 congelado;
- publisher R10;
- evidência histórica G6/P2/CASE_MAP/SOURCE_BINDINGS/B1 README.

A1 não pode mutar o repositório por MCP/app/hosted GitHub/API remota. Autoria
ocorre no worktree local e `git push` é o único transporte Git remoto A1.

## 5. Defense in depth

- `.codex/hooks.json` possui PreToolUse e PostToolUse;
- hooks Python/PowerShell classificam paths pelo envelope;
- `tools/check_codex_autonomy_delta.py` revalida o delta antes de commit/push;
- hooks são guardrail/feedback, não fronteira de segurança completa;
- sandbox permanece a fronteira técnica primária.

Hosted tools não são assumidos como cobertos por hooks; por isso A1 remote repo
mutation foi explicitamente proibida.

## 6. A2

A2 continua:

```text
activation.state = ACTIVE_A0_A1
a2_reference = null
a2_contract = null
A2.autonomous = false
```

O schema v2 exige, antes de A2 ativa:

- target/profile/host/workspace class;
- namespace;
- effects;
- attempts por effect;
- dados sintéticos;
- overwrite;
- readback obrigatório;
- UNKNOWN reconciliation policy;
- cleanup.

Nenhuma autorização anterior do G6 ativa A2 por inferência.

## 7. Estado vivo versus legado

ADR-0025 fixa:

1. `B1/AUTHORING_STATE.json`;
2. índices SER/PARALELO correntes;
3. contratos do gate atual;
4. snapshots/runbooks/tentativas históricas.

Foram desambiguados como não-live:

- `CONTROLE_PLANO.json`;
- DAG;
- blockers/readiness;
- B0 README histórico;
- G6 runbook congelado;
- G6 plano pré-execução;
- partes antigas de Plano Mestre/implantação/checklist.

As restrições “executor não corrige” agora estão qualificadas como regras do
executor determinístico; repair A1 acontece entre rodadas, com novo causal delta.

## 8. Validator e metatestes

O validator:

- usa Draft 2020-12 real para o envelope;
- exige schema dos cinco agents;
- exige exatamente um writer;
- reprova `danger-full-access`;
- exige A1 roots;
- exige A2 reference + contract antes de A2 ativa;
- exige hooks e runtime qualification;
- verifica bindings dos documentos donos.

A suíte possui **21 métodos** definidos estaticamente na candidata auditada,
incluindo regressões para:

- custom-agent governance;
- A2/A3;
- blind retry;
- single-writer;
- concurrency;
- hooks;
- recovery root permitido;
- G6 congelado protegido;
- adapters B1 qualificados fora de A1;
- evidência histórica B1 protegida;
- live state e journal autônomo permitidos.

## 9. Invariância funcional

Compare contra a base B1 pré-controller
`d3871d27e34af3940153b8df47b4dcfd5739ff85`:

- branch permanece ahead, behind 0;
- nenhuma mudança em `ambiente_fonte/**`;
- nenhuma mudança no mirror de produto;
- nenhuma mudança em policy;
- nenhuma mudança no G6 congelado;
- nenhuma mudança no publisher R10.

Logo AC-R1 é camada de governança/coordenação, não uma nova candidata de produto
nem uma nova tentativa G6.

## 10. Limitações desta auditoria

Não foram executados nesta sessão GitHub-side:

- parse/config runtime real pelo cliente Codex;
- project trust;
- `/status`;
- `/debug-config`;
- strict-config quando disponível;
- effective sandbox/approval overrides;
- hooks reais;
- negative permission probes;
- validator Python;
- 21 metatestes.

Esses itens são CQ0–CQ5.

## 11. Fontes oficiais verificadas em 2026-09-26

- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/hooks
- https://learn.chatgpt.com/docs/config-file/config-reference
- https://learn.chatgpt.com/docs/config-file/config-advanced
- https://learn.chatgpt.com/docs/agent-approvals-security
- https://developers.openai.com/pt-BR/docs/sandboxing

## 12. Fechamento

```text
AC_R1_STATIC = PASS
NEXT = CONTROLLER_RUNTIME_QUALIFICATION_CQ0_CQ5
REMOTE_EFFECT = NONE
A2 = NOT_ACTIVE
PROMOTION = NOT_AUTHORIZED
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```

O commit que grava este relatório é documental/state e, por definição, não pode
conter a própria identidade sem circularidade. Após o commit, o integrador deve
revalidar externamente que o delta `3c9db7edec703cb875989430cbb7477d4245c70b` → HEAD contém somente este
fechamento documental/state.
