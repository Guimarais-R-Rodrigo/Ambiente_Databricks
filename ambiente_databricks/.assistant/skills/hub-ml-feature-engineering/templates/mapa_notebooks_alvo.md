# Mapa de Notebooks-Alvo (Corpus)

> Preencher 1 linha por notebook analisado. Este inventário é a base para todas as etapas subsequentes.

## Instruções de preenchimento
- **Notebook**: nome do arquivo (sem path completo).
- **Papel no corpus**: classificar como `ETL`, `EDA`, `Regras`, `Modelagem`, `Exploração`, `Agregação` ou combinação.
- **Entradas**: tabelas/DFs lidos (formato `catalog.schema.tabela` quando disponível).
- **Saídas**: tabelas/DFs escritos ou variáveis finais.
- **Granularidade**: o que é 1 linha (ex.: "1 linha por cliente", "1 linha por transação/dia").
- **Obs**: achados relevantes para FE (janelas, agregações, regras de negócio, alertas de qualidade).

## Template

| Notebook | Papel no corpus | Entradas | Saídas | Granularidade | Obs |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Exemplo ilustrativo fictício (banking — propensão a CDB)

| Notebook | Papel no corpus | Entradas | Saídas | Granularidade | Obs |
|---|---|---|---|---|---|
| `01_ETL_Carteira` | ETL + Regras | `gold.clientes`, `gold.saldos` | `df_carteira_ativa` | 1 linha/cliente | Filtro: saldo > 0 e status = ativo |
| `02_EDA_Perfil` | EDA | `df_carteira_ativa` | — (exploratório) | 1 linha/cliente | Identificou: 23% nulos em renda, UF concentrada em SP/RJ |
| `03_Agregacoes_Transacionais` | Agregação | `silver.transacoes` | `df_rfv_30_90d` | 1 linha/cliente | Janelas 30d e 90d, métricas: qtd, soma, média, max |
