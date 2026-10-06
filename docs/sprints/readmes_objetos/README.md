# READMEs de objeto — migração por sprints

Esta iniciativa acrescenta explicações didáticas às pastas de snippets, scripts
e prompts. Não substitui o Manual, não muda os algoritmos e não publica o Hub.
A produção operacional começa somente depois do aceite do contrato e do piloto.

## Estado e próxima ação

O contrato vigente é **1.0.0**. A R13 foi aceita e integrada pelo PR nº 33 no commit `b0e953cc`, encerrando a iniciativa R00–R13 em **75/75 operacionais, 3/3 exemplares e 0 pendências**, com seis índices funcionais de `hub_snippets` e auditoria final local aprovada.

Consulte o [relatório R13](RELATORIO_R13.md), a [matriz de auditoria](MATRIZ_AUDITORIA_R13.md), os [achados](ACHADOS_R13.md) e as evidências em `evidencias_r13/`. O encerramento é documental e local: não equivale a auditoria independente, publicação no workspace ou homologação Databricks/Genie Code.

Os relatórios anteriores preservam o estado observado em cada data. PRs #9/#11
foram supersedidos pela composição integrada do PR #13 e não devem ser tratados
como entregas independentes a mesclar novamente.

## Rotas por objetivo

| Objetivo | Documento |
|---|---|
| Examinar o formato e a linguagem | [Template de objeto](../../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md) |
| Julgar a qualidade, além da estrutura | [Checklist editorial](../../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md) |
| Ver a matriz final da auditoria | [Matriz R13](MATRIZ_AUDITORIA_R13.md) |
| Conhecer achados e limitações finais | [Achados R13](ACHADOS_R13.md) |
| Ver o fechamento técnico | [Relatório R13](RELATORIO_R13.md) |
| Confirmar cobertura e zero pendências | [Controle de migração](CONTROLE_MIGRACAO.json) · [Auditoria R13](evidencias_r13/AUDITORIA_R13.json) |

## Como evitar deriva após o encerramento

O contrato 1.0.0 continua ativo mesmo com a migração encerrada. Todo novo snippet,
script ou prompt deve nascer com README local, e uma alteração estrutural precisa
preservar o template, o checklist e o ratchet de zero pendências. O
`CONTROLE_MIGRACAO.json` é evidência do fechamento, não backlog a reabrir.

O gate automático confere forma, links e cobertura, mas não certifica pedagogia,
correção estatística ou execução no Databricks. Revisão técnica/didática, runtime,
publicação e auditoria independente permanecem dimensões separadas.

## Limites do encerramento

Os exemplares continuam didáticos e não contam como objetos operacionais. A R13
foi uma auditoria local `A0_light`: confirmou coerência e regressões, sem publicar
o workspace nem homologar Databricks Runtime, Spark opcional ou Genie Code. Os
registros abaixo permanecem históricos e não devem ser reescritos para refletir o
estado atual.

## Registros históricos preservados

Rodrigo aprovou o padrão e autorizou a integração das R03-A/R03-B com a V01 em 2026-09-12. O PR nº 13 foi integrado na `main` pelo commit `1be947b`; o [registro da composição](INTEGRACAO_R03_V01.md) preserva os gates e a V01.

### Conciliação durante a R03-A

A main recebeu a instrumentação V00 em paralelo; o novo PR nº 9 precisa preservar essa entrega. [Registro de conciliação](CONCILIACAO_V00_R03A.md). A matriz final distingue a base integrada original da main V00 e não contabiliza os instrumentos herdados como novos READMEs.

### Conciliação R04-B × V03

A R04-B foi recomposta sobre a V03 já presente na `main`. Consulte [CONCILIACAO_R04B_V03.md](CONCILIACAO_R04B_V03.md). A cobertura permanece 32/75; a próxima parada continua sendo o merge da R04-B antes da R05.
