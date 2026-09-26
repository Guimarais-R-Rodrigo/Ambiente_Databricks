# Codex Autonomous Controller — auditoria estática repo-side

Data: 2026-09-26  
Escopo: ADR-0024 / piloto SER B1  
Candidata auditada: `c5d30330e8dd03f2eb6587f627553f2a6d010416`

## Veredito

```text
STATIC_ARCHITECTURE_AUDIT = PASS
RUNTIME_VALIDATION = NOT_RUN
A0 = ACTIVE
A1 = ACTIVE
A2 = PENDING_EXPLICIT_ACTIVATION
A3 = HUMAN_ONLY
FINDINGS_MATERIAL = 0
```

Este PASS é deliberadamente **estático**. O validator Python e seus metatestes
devem rodar no checkout real no início da primeira sessão Codex autônoma.

## Delta Git

Base funcional anterior ao controller:

`d3871d27e34af3940153b8df47b4dcfd5739ff85`

Candidata auditada:

`c5d30330e8dd03f2eb6587f627553f2a6d010416`

O compare GitHub mostra:

- status: ahead;
- 28 arquivos no delta da camada;
- zero mudanças em `ambiente_fonte/`;
- zero mudanças em `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/`;
- zero mudanças em `tools/skill_enforcement/real_campaigns/b1/g6/`;
- zero mudanças em `tools/skill_enforcement/real_campaigns/b1/g6_publication/`;
- zero mudança em policy.

O commit intermediário `ff47a83c...` que usou base tree incorreta permanece
histórico, mas o commit restaurador `9942f8a7...` recompôs a tree integralmente.
O delta líquido contra a base acima não contém deleções ou alterações funcionais
acidentais da B1.

## Autoridade

Envelope:

`docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json`

Estado observado:

- activation = `ACTIVE_A0_A1`;
- A0 autonomous = true;
- A1 autonomous = true;
- A2 autonomous = false;
- A2 authorization reference = null;
- A3 autonomous = false;
- max causal repair rounds/gate = 4;
- max hypotheses/root cause = 2;
- same-state same-command retries = 0;
- max unresolved UNKNOWN before human = 1;
- max concurrent subagents = 5;
- max write-capable agents = 1.

Portanto a aprovação da arquitetura não foi convertida em autorização remota A2.

## Configuração Codex

`.codex/config.toml`:

- root model = `gpt-6-astra`;
- root effort = `max`;
- sandbox = `workspace-write`;
- approval policy = `on-request`;
- approvals reviewer = `user`;
- `features.multi_agent = true`;
- `features.goals = true`;
- `agents.max_concurrent_threads_per_session = 5`;
- default subagent model = `gpt-6-sol`;
- default subagent effort = `high`.

Papéis declarados:

1. explorer — read-only;
2. executor — workspace-write;
3. domain-auditor — read-only;
4. evidence-auditor — read-only;
5. architecture-auditor — read-only.

Cada `config_file` é uma camada TOML normal; papel e descrição permanecem na
declaração `[agents.<role>]`. Cada subagente define `[agents] enabled=false`,
impedindo delegação recursiva.

## Compatibilidade com documentação oficial consultada

A referência vigente confirma:

- `agents.<name>.config_file` e `agents.<name>.description`;
- `agents.default_subagent_model`;
- `agents.default_subagent_reasoning_effort`;
- `agents.enabled`;
- `agents.max_concurrent_threads_per_session`;
- `features.multi_agent`;
- `features.goals`;
- `sandbox_mode`;
- `approval_policy`;
- `approvals_reviewer`;
- `model_reasoning_effort` incluindo `xhigh` e `max` quando suportados.

GPT-6 Astra é documentado como modelo principal para trabalho complexo e suporta
`low/medium/high/xhigh/max`.

Referências:

- https://learn.chatgpt.com/docs/config-file/config-reference
- https://developers.openai.com/api/docs/models/gpt-6-astra
- https://developers.openai.com/api/docs/guides/latest-model

## Validator

Implementado:

- `tools/validate_codex_autonomy.py`;
- `tools/tests/test_codex_autonomy.py`.

O validator reprova, entre outros:

- A2 ativo sem referência explícita;
- A3 autônomo;
- blind retry diferente de zero;
- mais de um writer;
- concurrency do envelope maior que a configuração;
- `danger-full-access`;
- papel sem `developer_instructions`;
- nesting de subagentes habilitado;
- documentos donos ausentes;
- adapter `AGENTS.md` sem binding;
- ADR-0024 ausente do índice.

A suíte contém 7 métodos de metateste.

## Limitação desta auditoria

Esta sessão opera o repositório pelo conector GitHub, não pelo checkout Windows
ENV04. Portanto não há claim de execução de:

```text
python -B tools/validate_codex_autonomy.py --json
python -B -m unittest tools.tests.test_codex_autonomy -v
```

Esses dois comandos constituem o primeiro gate fail-closed do prompt de
bootstrap.

## Próximo passo

Abrir uma única sessão Codex na raiz do repositório com o prompt de
`docs/operations/CODEX_AUTONOMOUS_START_PROMPT.md`.

O controller deve primeiro:

1. sincronizar branch;
2. executar validator + metatestes;
3. corrigir causalmente a própria camada se necessário dentro de A1;
4. só então retomar B1 a partir do state source.

A2, promoção, Ready e merge permanecem Human Gates.
