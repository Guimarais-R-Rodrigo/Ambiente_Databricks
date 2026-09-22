# PSEF00 — reconciliação, inventário, baseline e freeze

**Data:** 2026-09-22  
**Base reconciliada:** `main@17640a6a31f562e9979d235ede27cf44cef9ebbf`  
**Branch candidata:** `psef/PSEF00-reconciliacao-inventario`  
**Escopo:** documental; nenhum prompt produtivo alterado.

## Objetivo

Fotografar o estado real de `hub_prompts`, relacioná-lo às skills e à policy SEF vigente, identificar riscos de bypass/overclaim e congelar o escopo antes de qualquer mudança behavior-bearing.

## Reconciliação de partida

A HEAD real de `main` é `17640a6a31f562e9979d235ede27cf44cef9ebbf`, merge da PR #96, correspondente ao fechamento documental final da SE08.

PRs abertas relevantes na data do freeze:

| PR | Head | Situação para PSEF00 |
|---|---|---|
| #51 MM01 | `micromodelos/mm01-contrato-canonico@8e7c7a8d…` | aberta; não toca `hub_prompts`, policy, instruções ou Manual |
| #91 SE08 R6 | `sef/SE08-r6-final-documentation@65d75dca…` | branch histórica ainda aberta; toca documentação SEF/Manual, mas a SE08 já foi integrada e fechada em `main` |
| #6 READMEs R02 | `codex/readmes-r02@5996574a…` | draft histórico; toca `hub_prompts`, inclusive `eda_rapida`, mas não integra a baseline atual |
| #5 READMEs R01 | `codex/readmes-r01@af1efd14…` | draft histórico; toca `hub_prompts/README.md` e `.assistant_instructions.md`, mas não integra a baseline atual |

Não foi encontrada branch existente com prefixo/nome `psef`. Nenhuma branch com “hub” foi encontrada na busca nominal; a concorrência material é representada pelas PRs antigas #5/#6.

## Fontes canônicas observadas

- `ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json`
- `ambiente_fonte/.assistant/skills/README.md`
- `ambiente_fonte/.assistant/skills/*/SKILL.md` e artefatos estruturais existentes
- `ambiente_fonte/.assistant_instructions.md`
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md`
- `ambiente_fonte/.assistant/hub_prompts/README.md`
- `docs/sprints/skill_enforcement/` e checkpoints SE07/SE08

A policy observada possui 14 skills. Nenhum nível foi recalculado ou promovido nesta sprint.

## Inventário

O Git tree recursivo de `main` retornou 16 diretórios de família e 49 blobs sob `ambiente_fonte/.assistant/hub_prompts/`:
- 1 README raiz;
- 16 READMEs locais;
- 16 briefings `.md`;
- 16 notebooks `exemplo_*.py`.

## Limites da sprint

PSEF00 **não altera**:
- `ambiente_fonte/.assistant/hub_prompts/**`;
- `ambiente_fonte/.assistant/skills/**`;
- `policy.json`;
- `.assistant_instructions.md`;
- `MANUAL_TECNICO.md`;
- `Novo_Ambiente_Simulado/**`;
- níveis SEF;
- resultados históricos da SE08.

## Regime de execução

```text
EXECUTION_REGIME               = LOCAL_FIRST
LOCAL_DOCUMENTATION_VALIDATION = PASS
GITHUB_ACTIONS                  = DEFERRED_NO_CREDITS
DATABRICKS_FREE                 = NOT_RUN
GENIE_BEHAVIOR                  = NOT_RUN
PSEF01                          = BLOCKED_PENDING_HUMAN_ACCEPTANCE
```

O PASS local é apenas da documentação criada pela PSEF00; não é certificação de prompts produtivos nem de comportamento do Genie Code.
