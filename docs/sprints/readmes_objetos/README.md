# READMEs de objeto — migração por sprints

Esta iniciativa acrescenta explicações didáticas às pastas de snippets, scripts
e prompts. Não substitui o Manual, não muda os algoritmos e não publica o Hub.
A produção operacional começa somente depois do aceite do contrato e do piloto.

## Estado e próxima ação

R01 entrega uma **fundação candidata**, com três exemplares e controles locais.
O próximo marco é o aceite humano deste lote; R02 ainda não começou. O
[checkpoint](CHECKPOINT_R01.md) registra execução e limitações. O
[plano R00](PLANO_R00.md) é histórico: suas afirmações de “não executado” descrevem
aquela entrega, não o estado posterior.

## Rotas por objetivo

| Objetivo | Documento |
|---|---|
| Examinar o formato e a linguagem | [Template de objeto](../../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md) |
| Julgar a qualidade, além da estrutura | [Checklist editorial](../../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md) |
| Ver o que mudou além dos READMEs | [Matriz efetiva de alterações](MATRIZ_ALTERACOES_R01.md) |
| Conhecer inconsistências observadas | [Achados R01](ACHADOS_R01.md) |
| Ver o resultado da execução | [Relatório R01](RELATORIO_R01.md) |
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
instruções executáveis. O [ADR-0011](../../decisions/ADR-0011-readmes-de-objeto.md)
continua proposto até decisão humana, sem reescrever ADRs já aceitos.
