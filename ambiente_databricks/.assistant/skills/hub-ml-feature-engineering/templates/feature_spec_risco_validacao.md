# Feature Spec — Risco & Validação

> ≤6 colunas. Complementa o Spec Core com análise de risco e checagens objetivas.

## Instruções de preenchimento
- **feature_name**: mesmo nome do Spec Core (chave de ligação).
- **risco_leakage**: BAIXO/MÉDIO/ALTO com evidência temporal e justificativa, ou NÃO AVALIADO. “Estático” não comprova disponibilidade histórica.
- **custo**: `BAIXO` (tabela disponível, join simples) | `MÉDIO` (agregação pesada ou tabela externa) | `ALTO` (requer pipeline novo ou dado não disponível).
- **validacao**: teste ligado ao domínio e ao contrato temporal; registrar fórmula, população, limite e autoridade. Não exigir normalidade ou impor teto monetário/cap sem fundamento.
- **expectativa_sinal**: direção esperada em relação ao target (ex.: "↑ compras → ↓ churn", "↑ razão uso/limite → ↑ inadimplência").
- **obs**: notas adicionais (premissas, dependências, alternativas).

## Template

| feature_name | risco_leakage | custo | validacao | expectativa_sinal | obs |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Exemplo ilustrativo fictício (hipóteses; risco e custo a avaliar)

| feature_name | risco_leakage | custo | validacao | expectativa_sinal | obs |
|---|---|---|---|---|---|
| feat_qtd_compras_30d | NÃO AVALIADO | A ESTIMAR | Contagem não negativa; janela e disponibilidade conforme contrato | Associação hipotética a testar | Fronteira LT/LE e cutoff confirmados |
| feat_ticket_medio_90d | NÃO AVALIADO | A ESTIMAR | Denominador, moeda, estornos e extremos segundo domínio | Associação hipotética a testar | Sem limite R$50 mil ou cap P99 automático; tratamento só com fundamento |
| feat_razao_uso_limite | NÃO AVALIADO | A ESTIMAR | Denominador zero/nulo e domínio da razão justificados | Associação hipotética a testar | Verificar disponibilidade dos dois componentes até a decisão |
| feat_dias_desde_ultima_compra | NÃO AVALIADO | A ESTIMAR | Diferença temporal conforme cutoff e regra de ausência | Associação hipotética a testar | Confirmar event_time e available_at |
| feat_flag_renda_ausente | NÃO AVALIADO | A ESTIMAR | Binária {0,1}; origem da ausência e comparabilidade por período | Sem direção presumida | Ausência não prova desengajamento |
| feat_woe_uf | MÉDIO | MÉDIO | WoE fit apenas no treino; validar bins e convenção good/bad | varia por UF | Investigar quando PSI exceder o limite aprovado; recalcular só após validação |
