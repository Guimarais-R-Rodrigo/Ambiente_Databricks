# Backlog de Features (Tier A/B/C)

> Classificação por prioridade de implementação. Critérios objetivos para cada tier.

## Critérios de classificação

| Tier | Sinal esperado | Risco leakage | Custo implementação | Ação |
|---|---|---|---|---|
| **A** | Alto (RFV, recência, razões clássicas) | BAIXO | BAIXO (dados disponíveis, join simples) | Implementar primeiro |
| **B** | Provável (derivadas, tendências) | MÉDIO | MÉDIO (agregação pesada ou validação extra) | Segunda onda |
| **C** | Incerto (experimental, alta dimensionalidade) | ALTO | ALTO (pipeline novo, dado externo) | Testar com cautela |

## Instruções de preenchimento
- **tier**: A, B ou C (seguir critérios acima).
- **feature_name**: mesmo nome do Spec Core.
- **motivo**: por que espera-se sinal preditivo (1 linha, linguagem de negócio).
- **risco**: BAIXO | MÉDIO | ALTO (consolidado de leakage + custo).
- **dependencias**: tabelas, features ou decisões das quais depende.
- **status**: `[ ]` (pendente) | `[~]` (em andamento) | `[x]` (implementada) | `[!]` (bloqueada).

## Template

| tier | feature_name | motivo | risco | dependencias | status |
|---|---|---|---|---|---|
| A | ... | ... | ... | ... | [ ] |
| B | ... | ... | ... | ... | [ ] |
| C | ... | ... | ... | ... | [ ] |

## Exemplo (banking — propensão a investimento)

| tier | feature_name | motivo | risco | dependencias | status |
|---|---|---|---|---|---|
| A | feat_saldo_medio_poupanca_90d | Cliente com saldo alto é candidato natural | BAIXO | tabela saldos | [ ] |
| A | feat_qtd_acessos_app_30d | Engajamento digital = propensão a self-service | BAIXO | tabela acessos | [ ] |
| A | feat_razao_saldo_renda | Capacidade de investimento | BAIXO | saldos + cadastro | [ ] |
| B | feat_delta_saldo_30d_vs_90d | Tendência de acumulação | MÉDIO | saldos (histórico 90d) | [ ] |
| B | feat_woe_segmento | Segmentos com maior conversão histórica | MÉDIO | cadastro + target (fit no treino) | [ ] |
| C | feat_cluster_comportamental | Agrupamento não-supervisionado de perfil | ALTO | múltiplas features Tier A | [ ] |
| C | feat_sazonalidade_salario | Pico de saldo pós-crédito de salário | ALTO | saldos diários (volume alto) | [ ] |
