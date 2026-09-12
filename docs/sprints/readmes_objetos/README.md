# READMEs de objeto — migração por sprints

Esta iniciativa acrescenta explicações didáticas às pastas de snippets, scripts
e prompts. Não substitui o Manual, não muda os algoritmos e não publica o Hub.
A produção operacional começa somente depois do aceite do contrato e do piloto.

## Estado e próxima ação

R02 entregou seis pilotos e sua revisão editorial. A composição candidata
**R02-I** reúne esse conteúdo e o Concierge da main em branch separada, sem
merge nos PRs originais ou na main. Veja o [registro de integração](INTEGRACAO_R02.md),
a [matriz de alterações](MATRIZ_INTEGRACAO_R02.md) e o
[checkpoint da composição](CHECKPOINT_INTEGRACAO_R02.md).

O contrato permanece `0.1.0-candidata`; aceite editorial, auditoria independente,
congelamento 1.0 e publicação não foram presumidos. R03 não iniciada.
O [checkpoint R02](CHECKPOINT_R02.md), a [revisão](REVISAO_FECHAMENTO_R02.md)
e o [diagnóstico anterior](DIAGNOSTICO_INTEGRACAO_R02.md) preservam o estado
histórico das bases que examinaram. Os conflitos lá descritos foram tratados
somente na candidata R02-I; os PRs nº 5 e nº 6 não foram reescritos.

## Rotas por objetivo

| Objetivo | Documento |
|---|---|
| Examinar o formato e a linguagem | [Template de objeto](../../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md) |
| Julgar a qualidade, além da estrutura | [Checklist editorial](../../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md) |
| Ver o que mudou além dos READMEs | [Matriz R02](MATRIZ_ALTERACOES_R02.md) · [Matriz R01](MATRIZ_ALTERACOES_R01.md) |
| Conhecer inconsistências observadas | [Achados R02](ACHADOS_R02.md) · [Achados R01](ACHADOS_R01.md) |
| Ver o resultado da execução | [Relatório R02](RELATORIO_R02.md) · [Relatório R01](RELATORIO_R01.md) |
| Saber quais legados faltam | [Controle de migração](CONTROLE_MIGRACAO.json) |

## Como evitar deriva na continuação

Cada sprint parte de um commit conferido e da versão do template registrada.
Redatores trabalham em caminhos disjuntos; um integrador cuida de documentos
compartilhados. Cada objeto entregue sai de `pending` no mesmo commit do README.
Não há dispensa automática para novos objetos. O histórico Git impede que uma
dispensa retirada seja reintroduzida sem reprovação do gate.

A última contagem gerada pelo validador distingue operacional, exemplar e
pendência. O gate confere forma e existência, não certifica a pedagogia.
Registre revisão técnica, didática e aceite humano separadamente. Um revisor
não se torna independente por fazer uma segunda leitura do próprio texto.

## Limites desta etapa

Os exemplares ensinam os padrões e não contam como helpers operacionais.
Os notebooks podem escrever tabelas sintéticas: os READMEs alertam antes de
encaminhar à execução. R01 não os executa no Databricks e não modifica suas
instruções executáveis. O [ADR-0012](../../decisions/ADR-0012-readmes-de-objeto.md)
continua proposto até decisão humana, sem reescrever ADRs já aceitos.
