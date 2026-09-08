# Feature Spec — Risco & Validação

> ≤6 colunas. Complementa o Spec Core com análise de risco e checagens objetivas.

## Instruções de preenchimento
- **feature_name**: mesmo nome do Spec Core (chave de ligação).
- **risco_leakage**: `BAIXO` (dado estático ou anterior por construção) | `MÉDIO` (depende de janela correta) | `ALTO` (usa dado próximo ao evento, investigar).
- **custo**: `BAIXO` (tabela disponível, join simples) | `MÉDIO` (agregação pesada ou tabela externa) | `ALTO` (requer pipeline novo ou dado não disponível).
- **validacao**: checagem objetiva e executável (ex.: "count > 0 para ativos", "distribuição ~normal", "sem valores negativos").
- **expectativa_sinal**: direção esperada em relação ao target (ex.: "↑ compras → ↓ churn", "↑ razão uso/limite → ↑ inadimplência").
- **obs**: notas adicionais (premissas, dependências, alternativas).

## Template

| feature_name | risco_leakage | custo | validacao | expectativa_sinal | obs |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Exemplo (banking — churn de cartão)

| feature_name | risco_leakage | custo | validacao | expectativa_sinal | obs |
|---|---|---|---|---|---|
| feat_qtd_compras_30d | BAIXO | BAIXO | count ≥ 0; mediana > 0 para ativos | ↑ compras → ↓ churn | Usar apenas transações < data_ref |
| feat_ticket_medio_90d | BAIXO | BAIXO | > 0 para quem tem compras; sem outliers > R$50k | ↑ ticket → ↓ churn (engajamento) | Cap em p99 se outliers |
| feat_razao_uso_limite | MÉDIO | BAIXO | entre 0 e 1 (pode >1 se rotativo) | ↑ uso/limite → ↑ churn | Verificar se limite atualiza antes do evento |
| feat_dias_desde_ultima_compra | BAIXO | BAIXO | ≥ 0; sem negativos | ↑ recência → ↑ churn | — |
| feat_flag_renda_ausente | BAIXO | BAIXO | binária {0,1}; % nulos consistente com EDA | nulo → ↑ churn (perfil menos engajado) | — |
| feat_woe_uf | MÉDIO | MÉDIO | WoE fit apenas no treino; validar bins e convenção good/bad | varia por UF | Investigar quando PSI exceder o limite aprovado; recalcular só após validação |
