# SE02 — checkpoint

## Veredito atual

**CANDIDATA L2 EM RECONCILIAÇÃO LOCAL-FIRST / NÃO HOMOLOGADA / NÃO INTEGRADA.**

A SE02 implementa exclusivamente L2 (`Preflight`) para `hub-ml-eda-profissional`. O contrato permanece `mode="audit"`; SE03, runner determinístico, `ExecutionTraceV0`, Execution Receipt formal e postflight não foram iniciados.

A partir de 2026-09-17, a frente segue a revisão `../REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`.

## Estado Git de referência

- `main`: `ae9337204a7c769c0b28b33321c8b81afdff6bae`;
- branch: `sef/SE02-preflight`;
- HEAD imediatamente anterior à consolidação deste checkpoint: `e5f44074a3bb79e12abaa6388e1db6b3fdab975c`;
- merge-base: `ae9337204a7c769c0b28b33321c8b81afdff6bae`;
- comparação imediatamente anterior: `ahead_by=54`, `behind_by=0`;
- PR #74: aberta, Draft e mergeável.

A `main` avançou após a integração da SE01 por uma correção transversal da V08 (PR #75). A branch SE02 foi reconciliada com essa `main` por merge normal, sem force-push.

## Estados separados de certificação

```text
LOCAL_CERTIFICATION        = NOT_RUN
SYNTHETIC_AGENT_SCREENING = MIXED
DATABRICKS_FREE            = NOT_RUN
GITHUB_ACTIONS             = DEFERRED_CREDIT
FULLY_CERTIFIED            = false
```

Interpretação:

- `LOCAL_CERTIFICATION=NOT_RUN`: o novo HEAD consolidado ainda precisa ser executado em clone/worktree local limpo pelo certifier canônico;
- `SYNTHETIC_AGENT_SCREENING=MIXED`: o laboratório externo isolado produziu evidência útil de priorização arquitetural, mas não testou o projeto real nem o Genie Code/Databricks;
- `DATABRICKS_FREE=NOT_RUN`: os casos da candidata revisada ainda não foram publicados/verificados no Free;
- `GITHUB_ACTIONS=DEFERRED_CREDIT`: não é PASS nem failure funcional. O orçamento de Actions está sendo preservado para release candidate/pós-merge;
- `FULLY_CERTIFIED=false`: nenhum estado acima pode ser escondido por um PASS parcial.

## Implementado na SE02

- [x] contrato canônico v0.1 em `mode="audit"`;
- [x] API pública `hub_scripts.skill_execution.run_preflight`;
- [x] script fino `skills/hub-ml-eda-profissional/scripts/preflight.py`;
- [x] instrução mínima no `SKILL.md` para executar o preflight antes do core;
- [x] `PASS`/`BLOCKED` estruturados;
- [x] required/conditional/optional tratados;
- [x] contexto condicional fail-closed quando condição necessária está ausente ou inválida;
- [x] templates relativos com proteção contra traversal;
- [x] `writes_performed=false`;
- [x] hardening contra `__all__` fictício;
- [x] hardening contra module path não canônico/path-like;
- [x] resolução estática compartilhada entre L1 e L2 em `hub_scripts.skill_execution.resource_resolution`;
- [x] suíte SE02 ampliada para 22 casos, incluindo consistência L1/L2;
- [x] `tools/skill_enforcement/certify_local.py` como certifier reproduzível;
- [x] `tools/ci_local.py` com subgate SEF parcial/read-only;
- [x] workflow SE02 chama o mesmo certifier, com `concurrency.cancel-in-progress=true`;
- [x] job dedicado SE02 é `skipped` enquanto a PR está Draft;
- [x] revisão formal do Plano Mestre incorporada de forma aditiva;
- [ ] renderer materializado para o novo resolver/refactor;
- [ ] certificação local completa do HEAD revisado;
- [ ] gate geral `ci_local.py --verbose` do HEAD revisado;
- [ ] Databricks Free publicado/verificado para a candidata revisada;
- [ ] casos Free/Genie Code revisados;
- [ ] CHANGELOG final reconciliado;
- [ ] aceite explícito do usuário;
- [ ] Actions finais da release candidate quando houver crédito/necessidade;
- [ ] merge.

## Evidência histórica preservada

Os resultados abaixo pertencem a HEADs anteriores e continuam históricos; não são promovidos automaticamente para a candidata atual.

### Run `35147659671`

- contrato v0.1: PASS;
- regressão SE01: 14/14 PASS;
- suíte SE02 histórica: 18/18 PASS;
- validação estrutural: FAIL por quatro convenções estruturais do novo objeto.

### Run `35148053257`

- contrato: PASS;
- SE01: 14/14 PASS;
- SE02: 18/18 PASS;
- validação estrutural: PASS;
- renderer: PASS;
- artifact: PASS;
- diff do derivado: FAIL porque a saída do renderer ainda não estava materializada.

O derivado foi materializado exclusivamente pelo renderer no workflow transitório `SE02 Materialize Simulado`, run `35148184892`.

### Run `35148293591`

- contrato: PASS;
- SE01: 14/14 PASS;
- SE02: 18/18 PASS;
- validação estrutural: PASS;
- renderer: 555 arquivos;
- artifact: PASS;
- derivado sem diff: PASS;
- snapshot: FAIL exclusivamente por métricas antigas no README.

As métricas dessa árvore foram posteriormente reconciliadas para 1516 arquivos / 1985 links.

### Hardening posterior

Antes da revisão local-first, a matriz SE02 foi ampliada de 18 para 20 casos para cobrir:

- `__all__` declarando símbolo inexistente;
- module path não canônico.

Uma reprodução isolada desses 20 casos passou 20/20. Depois disso foram adicionados dois casos cruzados L1/L2, totalizando 22. **Os 22 casos ainda não foram executados como certificação da árvore consolidada atual**, portanto não há alegação de 22/22 PASS neste checkpoint.

## Laboratório sintético e consequência arquitetural

O laboratório externo isolado executou 52 runs reais de coding agent e 31/31 testes do próprio harness/evaluator. Nos casos discriminantes de caminho canônico adulterado/falhando, reinforcement textual/contratual/procedural não mostrou ganho mensurável frente ao baseline, enquanto o entrypoint estrutural passou 7/7 tanto em V4 quanto em V5.

Limites preservados:

- Claude Code/CLI local, não Genie Code;
- uma tarefa sintética;
- n pequeno em algumas variantes;
- legacy/reimplementation saudável não foram provocados de forma discriminante;
- não é prova de transfer para Databricks.

Decisão: fechar SE02 como L2 correto e priorizar SE03 como experimento estrutural, sem iniciar SE03 dentro desta PR.

## Achado operacional de GitHub Actions

O workflow dedicado SE02 foi alterado para não alocar runner em Draft. Essa regra foi observada no run `35212239257`, com conclusão `skipped`.

Porém, a mesma sincronização da PR disparou workflows transversais históricos do repositório (CI geral e várias frentes V00–V14). Logo, **manter uma PR Draft não elimina o consumo transversal de Actions**.

Regra para SE03 em diante: desenvolver a branch sem PR aberta; abrir a PR somente na release candidate. A SE02 não reescreverá dezenas de workflows históricos para resolver um problema de orçamento transversal.

## Gate atual — renderer

A fonte canônica mudou novamente com:

- `resource_resolution.py` compartilhado;
- refactor de `skill_execution.py`;
- alinhamento do validador L1.

O `Novo_Ambiente_Simulado` ainda não foi rematerializado para essa árvore. Portanto:

```text
RENDER_GATE = BLOCKED / DERIVED_STALE
```

Não editar o derivado manualmente.

## Próximo gate local

Em clone local limpo, na branch atualizada:

```powershell
git fetch origin --prune
git switch sef/SE02-preflight
git pull --ff-only origin sef/SE02-preflight
git status --short
python -B tools/skill_enforcement/certify_local.py --profile se02 --verbose
git status --short
git diff -- Novo_Ambiente_Simulado
```

A primeira execução completa pode reprovar corretamente em `render_diff` com `DERIVED_STALE`, pois o renderer materializará o novo arquivo/refactor. Nesse caso:

1. revisar o diff derivado;
2. confirmar que ele é somente consequência mecânica de `ambiente_fonte/`;
3. versionar a saída canônica do renderer;
4. voltar a worktree limpo;
5. executar novamente o certifier até `LOCAL_CERTIFICATION=PASS`.

Depois:

```powershell
python tools/ci_local.py --verbose
```

Somente após os gates locais estabilizarem, seguir para publicação/verify no Databricks Free e F02-P1/F02-B1/F02-C1/F02-A1/F02-A2.

## Limites preservados

- `mode="audit"`;
- sem runner determinístico;
- sem `ExecutionTraceV0` funcional;
- sem Execution Receipt formal;
- sem postflight;
- sem `mode="enforce"`;
- sem promoção corporativa;
- `.assistant_instructions.md` não alterado;
- SE03 não iniciada.
