# Template: Métricas de Ranking

> **[NDCG@10]** NDCG | **[MAP]** MAP | **[MRR]** MRR | **[N queries]** grupos avaliados


## Uso
Reportar performance de modelos Learning-to-Rank com métricas posicionais.

## Performance geral

| Métrica | Valor | Baseline (random) | Melhoria |
|---|---|---|---|
| NDCG@5 | [X.XXX] | [X.XXX] | +[X]% |
| NDCG@10 | [X.XXX] | [X.XXX] | +[X]% |
| NDCG@20 | [X.XXX] | [X.XXX] | +[X]% |
| MAP@10 | [X.XXX] | [X.XXX] | +[X]% |
| MRR | [X.XXX] | [X.XXX] | +[X]% |
| Precision@5 | [X.XXX] | [X.XXX] | +[X]% |

## Faixas de referência

| Métrica | Excelente | Bom | Aceitável | Fraco |
|---|---|---|---|---|
| NDCG@10 | > 0.85 | 0.70-0.85 | 0.50-0.70 | < 0.50 |
| MAP@10 | > 0.60 | 0.40-0.60 | 0.25-0.40 | < 0.25 |
| MRR | > 0.80 | 0.60-0.80 | 0.40-0.60 | < 0.40 |

## Comparação de abordagens

| Abordagem | Algoritmo | NDCG@10 | MAP@10 | Decisão |
|---|---|---|---|---|
| Pointwise | LightGBM regression | [X] | [X] | Baseline |
| Pairwise | LightGBM lambdarank | [X] | [X] | [✅/❌] |
| Classifier reordenado | LightGBM binary | [X] | [X] | [✅/❌] |

## Análise por query group

| Faixa NDCG | N queries | % total | Ação |
|---|---|---|---|
| > 0.8 (excelente) | [N] | [X]% | Manter |
| 0.5 - 0.8 (ok) | [N] | [X]% | Monitorar |
| < 0.5 (fraco) | [N] | [X]% | Investigar |

## Feature importance (top-10)

| Rank | Feature | Importance | Split count |
|---|---|---|---|
| 1 | [feature] | [X] | [N] |
| 2 | [feature] | [X] | [N] |
| ... | ... | ... | ... |

## Interpretação executiva

"O modelo de ranking posiciona o item mais relevante no top-[k] em [X]%
dos casos (NDCG@[k] = [X.XX]). Comparado com o baseline de classificação
reordenada, o ranker dedicado melhora em [X]pp, especialmente para queries
com [característica]."
