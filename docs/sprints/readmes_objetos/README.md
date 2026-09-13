# READMEs de objeto — migração por sprints

Esta iniciativa acrescenta explicações didáticas às pastas de snippets, scripts
e prompts. Não substitui o Manual, não muda os algoritmos e não publica o Hub.
A produção operacional começa somente depois do aceite do contrato e do piloto.

## Estado e próxima ação

Rodrigo aprovou o padrão e autorizou a integração das R03-A/R03-B com a V01 em
2026-09-12. O PR nº 13 foi integrado na `main` pelo commit `1be947b`; o
[registro da composição](INTEGRACAO_R03_V01.md) preserva os gates e a V01.

O contrato vigente é **1.0.0**. A R10 foi aceita e integrada pelo PR nº 30 no commit `7ba5d386`. A R11 documenta os nove Hub Prompts restantes em lotes A/B. A candidata busca fechar a migração estrutural em **75/75 operacionais e 3/3 exemplares, com 0 pendências**, sujeita ao validador real.

Consulte o [relatório R11](RELATORIO_R11.md), a [matriz nominal](MATRIZ_ALTERACOES_R11.md) e os [achados](ACHADOS_R11.md). Fechar `pending` encerra a migração estrutural de READMEs, não homologação Databricks nem etapas posteriores da iniciativa.

Os relatórios anteriores preservam o estado observado em cada data. PRs #9/#11
foram supersedidos pela composição integrada do PR #13 e não devem ser tratados
como entregas independentes a mesclar novamente.

## Rotas por objetivo

| Objetivo | Documento |
|---|---|
| Examinar o formato e a linguagem | [Template de objeto](../../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md) |
| Julgar a qualidade, além da estrutura | [Checklist editorial](../../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md) |
| Ver o que mudou além dos READMEs | [Matriz R08](MATRIZ_ALTERACOES_R08.md) |
| Conhecer inconsistências observadas | [Achados R08](ACHADOS_R08.md) |
| Ver o resultado da execução | [Relatório R08](RELATORIO_R08.md) |
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
foi ratificado pelo usuário em 2026-09-12, com nota anexada sem apagar o relato inicial.

### Conciliação durante a R03-A

A main recebeu a instrumentação V00 em paralelo; o novo PR nº 9 precisa preservar essa entrega. [Registro de conciliação](CONCILIACAO_V00_R03A.md). A matriz final distingue a base integrada original da main V00 e não contabiliza os instrumentos herdados como novos READMEs.

### Conciliação R04-B × V03

A R04-B foi recomposta sobre a V03 já presente na `main`. Consulte [CONCILIACAO_R04B_V03.md](CONCILIACAO_R04B_V03.md). A cobertura permanece 32/75; a próxima parada continua sendo o merge da R04-B antes da R05.
