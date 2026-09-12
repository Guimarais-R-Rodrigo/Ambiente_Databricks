# READMEs de objeto — migração por sprints

Esta iniciativa acrescenta explicações didáticas às pastas de snippets, scripts
e prompts. Não substitui o Manual, não muda os algoritmos e não publica o Hub.
A produção operacional começa somente depois do aceite do contrato e do piloto.

## Estado e próxima ação

Rodrigo aprovou o padrão e a integração em 2026-09-12. O PR nº 7 foi integrado
na main pelo commit `5493f7d`; o [registro de aceite](ACEITE_V1.md) distingue
esse ato da revisão independente ou homologação Databricks.

O contrato vigente é **1.0.0**. A R03-A acrescenta sete guias aos seis pilotos,
sem modificar os algoritmos. Consulte [relatório e checkpoint](RELATORIO_R03A.md),
[matriz de alterações](MATRIZ_ALTERACOES_R03A.md) e [achados](ACHADOS_R03A.md).
Os sete textos novos aguardam seu próprio aceite; a execução autorizada não
significa aprovação antecipada. A próxima leva é R03-B, ainda não iniciada.

Os relatórios R01/R02/R02-I preservam os estados de proposta e de conflito que
examinaram. A [composição R02-I](INTEGRACAO_R02.md) foi integrada pelo PR nº 7;
os PRs nº 5 e nº 6 não devem ser integrados novamente como trabalhos distintos.
A cobertura atual é calculada pelo validador e pelo controle de migração abaixo.

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
foi ratificado pelo usuário em 2026-09-12, com nota anexada sem apagar o relato inicial.

### Conciliação durante a R03-A

A main recebeu a instrumentação V00 em paralelo; o novo PR nº 9 precisa preservar essa entrega. [Registro de conciliação](CONCILIACAO_V00_R03A.md). A matriz final distingue a base integrada original da main V00 e não contabiliza os instrumentos herdados como novos READMEs.
