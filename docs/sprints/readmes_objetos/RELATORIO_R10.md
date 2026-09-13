# Relatório R10 — Hub Prompts

## Escopo

Documentar seis prompts do lote R10-A: `comparar_tabelas`, `cross_eda`, `data_quality`, `eda_completa`, `feature_engineering` e `stat_check`. Os briefings `.md` permanecem byte a byte iguais à base `d412acb750ce0f4011f97416c74fe7a685863772`.

## Meta

Base integrada: 60/75 operacionais, 15 pendências. Meta candidata: **66/75 operacionais, 3/3 exemplares e 9 pendências**, sujeita ao validador real.

## Alterações editoriais

Os seis notebooks recebem backlink para o README. `comparar_tabelas`, `cross_eda` e `feature_engineering` corrigem somente a descrição Markdown da escrita persistente: o código já criava duas tabelas, embora a tabela de pré-requisitos citasse apenas uma. Nenhuma célula executável ou saída histórica é alterada.

## Validação

O freeze exige contrato 1.0.0, gate permanente, preservação byte a byte dos seis briefings, equivalência dos notebooks após reversão apenas das edições declaradas, renderer do simulado e conferência do snapshot do README raiz. Interação Genie Code e homologação Databricks permanecem gates separados.

## Estado

Candidata R10 em construção; nenhum aceite editorial ou merge é presumido.
