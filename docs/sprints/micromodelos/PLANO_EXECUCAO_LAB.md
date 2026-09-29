# Execução de laboratório de micromodelos

**Base conferida em 2026-09-29:** `origin/main@4ba7f551`; PR #110/MM03 `MERGED` em `3214a131`. Branch de trabalho: `micromodelos/autonomia-local-v2`. Estado desta candidata: `E0_VALIDADO` para o escopo sintético descrito em `RELATORIO_ENTREGA_LAB.md`; kit r4 revisado, adapter metadata e MLflow sintético `E1_EXECUTADO` via CLI com [readback e três jobs SUCCESS](REVISAO_PARALELA_LAB_2026-09-29.md); skill corrigida instalada no Free e três casos Genie E1 respondidos com [vereditos e limites próprios](RESULTADOS_GENIE_E1_2026-09-29.md); `E2_NAO_EXECUTADO`.

## Autoridade e revisão processual

Este plano é o estado operacional da candidata de laboratório. Os ADRs 0014–0020, o schema MM01, a proveniência, o fingerprint MM02, o contrato metadata MM03, a policy SEF integrada e os entrypoints protegidos continuam como contratos de produto. Documentos de auditoria, FAILs e certificações anteriores preservam seu valor histórico.

Nesta missão, o desenvolvimento avança por entregas incrementais com smoke focal, casos positivos e negativos, integração sintética e revisão por autor diferente. Freeze, FULL, bundle, contraditório, novo freeze e aceite humano por alteração deixam de ser pré-requisitos automáticos deste fluxo de desenvolvimento. A mudança não altera políticas gerais de SER/SEF nem autoriza publicação, conexão corporativa ou mudança material de contrato.

## Reuso e interfaces

| Componente | Autoridade atual | Uso nesta candidata |
|---|---|---|
| Especificação e estados | `docs/sprints/micromodelos/MM01/micromodelo.schema.json`, template e `tools/micromodelo_mm01_contract.py` | Um único `micromodelo.yaml`; validar transições e proveniência. |
| Fingerprint material | `tools/micromodelo_mm02_fingerprint.py` | Identidade de especificação, sem inferir execução ou aprovação. |
| Metadata-only | `tools/micromodelo_mm03_metadata.py` | Descoberta sintética, escopo observado e texto não confiável; sem linhas, SQL ou `count(*)`. |
| Produto e skills | `ambiente_fonte/.assistant/`; policy em `hub_padroes/skill_enforcement/policy.json` | Nova skill e prompts passam pelo registro e pela validação canônicos. |
| Tracking e transporte | `hub_snippets.ml.mlflow_run`, `tools/render_simulado.py`, `tools/publicar_free.py` | Reuso em MM06; simulado só via renderer, Free somente pacote nesta missão. |

MM04–MM05 definem dois modos: `OBJETIVO_CONHECIDO` gera especificação preliminar válida e próximo estudo; `DESCOBRIR_OPORTUNIDADES` gera shortlist limitada e deduplicada. Observação de metadata, hipótese, decisão e medição têm campos e linguagem distintos. O código E0 em `tools/` é ferramenta de desenvolvimento; uma execução do produto renderizado precisa de dependências transportadas por mecanismo canônico, sem import implícito de `tools/`.

## Entregas e correspondência

| Onda | Sprints | Entrega e prova mínima | Estado em 2026-09-29 |
|---|---|---|---|
| 0 | MM00–MM03 reuso | Base conciliada, docs vivos corrigidos, smoke de contratos. | E0 PASS |
| 1 | MM04–MM05 | Skill, prompts, fluxo E0 até YAML e shortlist; casos positivos/negativos e revisão focal. | E0 PASS; três casos Genie E1 da skill corrigida PASS de resposta com ressalvas; briefings P1/P2c PASS de resposta com ressalvas; P2/P2b FAIL históricos; revisão editorial independente pendente |
| 2 | MM06 + MM10 preparo | Notebook, README, política de runs DEVELOPMENT/VALIDATION/SCORING e handoff sem autopublicação. | E0 PASS; MLflow local e Free sintético PASS |
| 3 | MM09–MM10-LAB | Piloto greenfield sintético com evidência, contra-evidência, indeterminado, scoring e reconciliação. | E0 PASS; aprovação/publicação pendente |
| 4 | MM07–MM08-LAB | Pacote Free, adapter/capability check, roteiro de execução pelo usuário e plano E2. | Adapter E0 fake PASS; código e adapter Free PASS; Genie Free com vereditos separados de resposta, sem homologação E2 |
| 5 | MM11–MM13-LAB | Temas, catálogo/impacto e ensaio conservador com legado fictício; migração não promovida. | Catálogo e equivalência fictícia E0 PASS; scoring sintético sem tema; integração visual e monitoramento pós-publicação NOT_RUN |

O planejamento MAC00–MAC05 anterior é absorvido por bootstrap, seleção de componentes, contratos/estado, testes adversariais, piloto E0 e pacote E1 nas ondas acima. Não será criado controller de execução. MM08–MM13 de laboratório não equivalem a sprints corporativas concluídas.

## Fronteiras de integração

O integrador é dono de policy, índices, changelog, schema compartilhado e renderer. Escritas em paralelo usam arquivos disjuntos; operações Git e geração transversal são seriais. A frente B1/SER pode mudar policy, roteamento e empacotamento: antes de integrar cada onda, comparar somente essas interfaces com a `main` atual. PR draft não comprova implementação integrada.

## Retomada

A candidata E0 está implementada, revisada focalmente e testada; `RELATORIO_ENTREGA_LAB.md` contém comandos e evidência. O kit revisado foi importado; código sintético, adapter metadata e MLflow foram executados no Free via CLI. A skill corrigida foi instalada na home pessoal Free e conferida por readback; os três casos manuais Genie E1 passaram nos critérios de resposta, com ressalvas registradas. O B1 recebeu a mesma revisão do `SKILL.md` na fonte, ainda sem commit ou certificação. Os [pré-gates MM04](RECONCILIACAO_B1_PRE_GATES_MM04_2026-09-29.md) continuam separados desta candidata de laboratório. E2 exige autorização institucional própria e permanece fora desta missão.
