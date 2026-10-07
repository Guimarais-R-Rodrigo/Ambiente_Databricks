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

## Critério do estudo

Registrar definição de relevância, k, grupos, agregação (peso por query ou item),
tratamento de queries sem relevantes, baseline e variabilidade. Aceite depende
do benchmark e critério aprovado pelo responsável, não de faixas universais.
Reportar apenas métricas calculadas; as demais ficam NÃO CALCULADO/NÃO APLICÁVEL.

## Comparação de abordagens

| Abordagem | Algoritmo | NDCG@10 | MAP@10 | Decisão |
|---|---|---|---|---|
| Pointwise | LightGBM regression | [X] | [X] | Baseline |
| Pairwise | LightGBM lambdarank | [X] | [X] | [✅/❌] |
| Classifier reordenado | LightGBM binary | [X] | [X] | [✅/❌] |

## Análise por query group

| Faixa NDCG | N queries | % total | Ação |
|---|---|---|---|
| [faixa definida no estudo] | [N] | [X]% | [recomendação justificada, sem aprovação automática] |

## Feature importance (top-10)

| Rank | Feature | Importance | Split count |
|---|---|---|---|
| 1 | [feature] | [X] | [N] |
| 2 | [feature] | [X] | [N] |
| ... | ... | ... | ... |

## Interpretação executiva

"NDCG@[k] = [X.XX] mede a qualidade da ordenação ponderada pela relevância,
normalizada pela ordenação ideal. Não representa percentual de acertos.
Frente ao baseline [definição], a diferença observada foi [delta na escala da
métrica], com [incerteza]. Hit rate/Precision@k, quando calculados, são relatados
separadamente com seus denominadores."
