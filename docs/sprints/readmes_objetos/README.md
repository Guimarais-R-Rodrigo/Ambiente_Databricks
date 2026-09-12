# READMEs de objeto — migração por sprints

Esta iniciativa acrescenta explicações didáticas às pastas de snippets, scripts
e prompts. Não substitui o Manual, não muda os algoritmos e não publica o Hub.
A produção operacional começa somente depois do aceite do contrato e do piloto.

## Estado e próxima ação

Rodrigo aprovou o padrão e a integração em 2026-09-12. O PR nº 7 foi integrado
na main pelo commit `5493f7d`; o [registro de aceite](ACEITE_V1.md) distingue
esse ato da revisão independente ou homologação Databricks.

O contrato vigente é **1.0.0**, preservado nesta rodada. A R03-A está no PR nº 9,
sem merge; sua base revisada `c60f1e5` sustenta a R03-B em branch separada.
O pedido “Siga” autorizou executar a próxima leva, não aprovação editorial
antecipada nem integração automática das duas branches.

A R03-B entrega seis guias de apresentação e navegação. Consulte o
[relatório e checkpoint](RELATORIO_R03B.md), a
[matriz nominal](MATRIZ_ALTERACOES_R03B.md) e os [achados](ACHADOS_R03B.md).
A cobertura estrutural da candidata é 19/74 operacionais e 3/3 exemplares,
com 55 pendências. Não representa 19 objetos já publicados ou aceitos pelo usuário.
A próxima parada é a revisão desta leva, antes da R04-A.

Os relatórios R01/R02/R02-I preservam os estados de proposta e de conflito que
examinaram. A [composição R02-I](INTEGRACAO_R02.md) foi integrada pelo PR nº 7;
os PRs nº 5 e nº 6 não devem ser integrados novamente como trabalhos distintos.
A cobertura atual é calculada pelo validador e pelo controle de migração abaixo.

## Rotas por objetivo

| Objetivo | Documento |
|---|---|
| Examinar o formato e a linguagem | [Template de objeto](../../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md) |
| Julgar a qualidade, além da estrutura | [Checklist editorial](../../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md) |
| Ver o que mudou além dos READMEs | [Matriz R03-B](MATRIZ_ALTERACOES_R03B.md) · [Matriz R03-A](MATRIZ_ALTERACOES_R03A.md) |
| Conhecer inconsistências observadas | [Achados R03-B](ACHADOS_R03B.md) · [Achados R03-A](ACHADOS_R03A.md) |
| Ver o resultado da execução | [Relatório R03-B](RELATORIO_R03B.md) · [Relatório R03-A](RELATORIO_R03A.md) |
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
