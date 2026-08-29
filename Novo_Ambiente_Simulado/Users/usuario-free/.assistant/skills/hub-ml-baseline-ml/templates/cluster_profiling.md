# Template: Profiling de Clusters

> **[N]** observações | **[K]** clusters | **[Sil]** silhouette | **[algoritmo]** método


## Uso
Documentar características, diferenças e acionabilidade de clusters identificados.

## Resumo da segmentação

| Cluster | Nome sugestivo | N | % total | Silhouette |
|---|---|---|---|---|
| 0 | [Nome descritivo] | [N] | [X]% | [X.XX] |
| 1 | [Nome descritivo] | [N] | [X]% | [X.XX] |
| ... | ... | ... | ... | ... |

**Silhouette global**: [X.XX]
**Algoritmo**: [K-Means / DBSCAN / GMM]
**k selecionado por**: [Elbow + Silhouette / Gap Statistic]

## Perfil por cluster

### Cluster 0: [Nome]

| Feature | Média cluster | Média global | Índice (cluster/global) | Interpretação |
|---|---|---|---|---|
| [feature_1] | [X] | [X] | [X.XX] | [acima/abaixo da média] |
| [feature_2] | [X] | [X] | [X.XX] | [acima/abaixo da média] |
| ... | ... | ... | ... | ... |

**Características dominantes**: [lista das 3-5 features mais diferenciadoras]
**Interpretação de negócio**: [descrição acionável do perfil]
**Ação sugerida**: [o que fazer com esse segmento]

### Cluster 1: [Nome]
(mesmo formato)

## Features mais discriminantes (global)

| Rank | Feature | F-statistic (ANOVA) | Importância relativa |
|---|---|---|---|
| 1 | [feature] | [X] | [X]% |
| 2 | [feature] | [X] | [X]% |
| ... | ... | ... | ... |

## Validação de estabilidade

| Teste | Resultado | Aceitável? |
|---|---|---|
| Bootstrap 80% (10 runs) | Concordância [X]% | [✅/❌] (limiar: 70%) |
| Sensibilidade ao k±1 | Silhouette Δ = [X] | [✅/❌] |

## Interpretação executiva

"A base foi segmentada em [N] grupos distintos. O segmento mais relevante
para [objetivo] é o Cluster [X] ([nome]), que representa [Y]% da base e
se diferencia por [característica principal]. Recomendamos [ação] para esse segmento."
