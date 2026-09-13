# READMEs de objeto — migração por sprints

Esta iniciativa acrescenta explicações didáticas às pastas de snippets, scripts e prompts. Não substitui o Manual, não muda os algoritmos e não publica o Hub.

## Estado e próxima ação

O contrato vigente é **1.0.0**. A R08 foi aceita e integrada na `main` pelo PR nº 27, commit `d5945e0`, com seis CIs pós-merge verdes. A R09 documenta `curves_plotly`, `drift_detection`, `metrics_report`, `mlflow_run` e `performance_monitor`, preservando suas implementações/fachadas.

A cobertura candidata da R09 é **60/75 operacionais e 3/3 exemplares, com 15 pendências**. Essa contagem só se torna integrada após freeze, revisão humana e merge; o validador da árvore fechada é a fonte de verdade.

Consulte o [relatório R09](RELATORIO_R09.md), a [matriz nominal](MATRIZ_ALTERACOES_R09.md), os [achados](ACHADOS_R09.md) e o [controle de migração](CONTROLE_MIGRACAO.json).

## Rotas por objetivo

| Objetivo | Documento |
|---|---|
| Examinar o formato e a linguagem | [Template de objeto](../../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md) |
| Julgar a qualidade, além da estrutura | [Checklist editorial](../../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md) |
| Ver o que mudou além dos READMEs | [Matriz R09](MATRIZ_ALTERACOES_R09.md) |
| Conhecer inconsistências observadas | [Achados R09](ACHADOS_R09.md) |
| Ver o estado da execução | [Relatório R09](RELATORIO_R09.md) |
| Saber quais legados faltam | [Controle de migração](CONTROLE_MIGRACAO.json) |

## Como evitar deriva na continuação

Cada sprint parte de um commit conferido e da versão do template registrada. Redatores trabalham em caminhos disjuntos; documentos compartilhados são integrados em uma única árvore. Cada objeto entregue sai de `pending` no mesmo candidato do README. Não há dispensa automática para novos objetos.

A contagem gerada pelo validador distingue operacional, exemplar e pendência. O gate confere forma e existência, não certifica pedagogia. Revisão técnica, didática e aceite humano são registrados separadamente.

## Limites

Os exemplares não contam como helpers operacionais. Notebooks e READMEs não equivalem a homologação do runtime de trabalho. O simulado é derivado pelo renderer; alterações manuais nele não são fonte canônica.

Os relatórios históricos R01–R08 permanecem no diretório para preservar o estado observado em cada etapa e suas conciliações com as frentes V00–V04.
