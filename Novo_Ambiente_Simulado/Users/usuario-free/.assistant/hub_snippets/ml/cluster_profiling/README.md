# `cluster_profiling` — descrever clusters por médias e desvios sem inventar personas

<!-- readme-objeto: 1.0.0 -->

Este helper recebe **clusters já atribuídos** e resume como cada grupo difere da população nas features escolhidas. Ele ajuda a inspecionar tamanho, média, razão contra a média global e diferença padronizada; **não cria os clusters e não demonstra que uma persona de negócio existe**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Profiling pandas de grupos já rotulados. |
| Para que serve? | Identificar diferenças descritivas entre clusters e priorizar features para interpretação. |
| Use quando... | Os labels já existem e as features numéricas têm significado revisado. |
| Evite quando... | Você quer validar `k`, provar separação ou inferir causalidade/persona. |
| Precisa de... | pandas/NumPy, coluna de cluster e features numéricas presentes no DataFrame. |
| Entrega... | Tabela longa por cluster × feature e ranking por `abs(z_score)`. |

Consulte a [implementação](cluster_profiling.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_cluster_profiling.py).

## 1. O que é?

`profile_clusters` calcula estatísticas descritivas de cada cluster em relação ao DataFrame completo. Para cada feature, produz média do cluster, média global, razão entre as duas e uma diferença padronizada.

`top_differentiators` apenas ordena essas diferenças. O objeto não ajusta K-Means, GMM, DBSCAN ou qualquer algoritmo de agrupamento.

## 2. Que problema este recurso resolve?

Depois de receber rótulos como 0, 1 e 2, a pergunta útil é: “em que variáveis esses grupos realmente diferem, e qual o tamanho de cada grupo?”. O helper transforma rótulos abstratos em uma tabela consultável antes de alguém atribuir nomes de negócio.

## 3. Quando faz sentido usar?

Use após uma clusterização para revisão exploratória, quando as features são numéricas e comparáveis em significado. É especialmente útil para detectar dois clusters que receberam IDs diferentes mas apresentam perfis muito semelhantes.

Também pode apoiar uma discussão com especialistas de negócio, desde que a distribuição completa e o tamanho dos grupos sejam verificados além das médias.

## 4. Quando não usar?

Não use para decidir se a clusterização “é boa”: o helper não mede silhouette, estabilidade, separação fora da amostra ou utilidade operacional.

Não transforme o maior `abs(z_score)` em nome de persona automaticamente. Um ranking sempre ordena os valores disponíveis; posição 1 não implica efeito grande ou relevante.

## 5. Como funciona, intuitivamente?

Primeiro calcula média e desvio-padrão globais. Depois percorre cada valor distinto de `cluster_col`, calcula tamanho e médias do grupo e cria uma linha para cada feature.

`index = cluster_mean / global_mean`. O chamado `z_score` é `(cluster_mean - global_mean) / global_std`. Neste helper, **ele é uma diferença de médias expressa em desvios-padrão globais**, não um z-test, p-value ou estatística inferencial.

## 6. Exemplo de situação

Uma segmentação produziu três grupos de clientes. Dois parecem ter renda, idade e produtos quase iguais; o terceiro é claramente diferente. O profiling permite mostrar essa semelhança antes de criar nomes distintos para os dois primeiros.

O notebook R08 usa exatamente esse cenário sintético.

## 7. O que você precisa antes de usar?

O DataFrame precisa conter `cluster_col` e todas as `feature_cols`. As operações são pandas e rodam no processo Python/driver.

A implementação não faz uma camada explícita de validação de tipos, vazio, NaN ou IDs heterogêneos. Erros de colunas chegam pelo pandas e valores ausentes podem propagar para as estatísticas. IDs precisam ser ordenáveis entre si porque o loop usa `sorted(...)`.

## 8. O que este recurso entrega?

`profile_clusters` retorna DataFrame longo com `cluster`, `n`, `pct_total`, `feature`, `cluster_mean`, `global_mean`, `index` e `z_score`. A função também imprime uma tabela de distribuição dos clusters.

Quando a média global é zero, `index` vira `None` para aquela feature. Quando o desvio global não é positivo, `z_score` é definido como zero.

`top_differentiators` devolve `feature`, `cluster_mean`, `global_mean`, `index` e `z_score` para as maiores magnitudes absolutas.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.cluster_profiling import profile_clusters, top_differentiators

profiles = profile_clusters(df, ["renda", "idade"], cluster_col="cluster")
top = top_differentiators(profiles, cluster_id=1, top_n=5)
```

O [notebook](exemplo_cluster_profiling.py) é somente leitura e usa dados sintéticos.

## 10. Decisões e configurações que mais importam

`feature_cols` define o que pode aparecer como “diferenciador”; excluir uma dimensão relevante muda a história do cluster.

`cluster_col` precisa representar o agrupamento correto. `top_n` controla apenas quantas linhas do ranking são exibidas, não um limiar de relevância.

## 11. Limitações, riscos e armadilhas

A razão `index` é difícil de interpretar quando a média global está perto de zero e pode mudar de sentido com médias negativas. Nesses casos, prefira diferenças em unidade original ou outra escala apropriada.

Médias escondem assimetria, multimodalidade e sobreposição. Grupos pequenos geram médias instáveis. O `z_score` local não leva tamanho amostral para um teste inferencial e não deve ser lido como significância estatística.

A função calcula estatísticas na própria população usada para descrever os clusters; ela não mede estabilidade temporal.

## 12. Quais são as alternativas?

[`clustering_suite`](../clustering_suite/README.md) avalia/ajusta agrupamentos e métricas internas. Visualizações como [`umap_viz`](../umap_viz/README.md) ajudam a explorar geometria em 2D, com outras limitações.

Para distribuição completa, use histogramas/quantis por cluster ou testes desenhados para a pergunta, em vez de depender apenas de médias.

## 13. Como saber se o resultado faz sentido?

Confira que `n` e `pct_total` batem com uma contagem independente por cluster. Inspecione features com média global próxima de zero antes de usar `index`. Compare o ranking com diferenças em unidade original e gráficos de distribuição.

Repita o profiling em outra janela/amostra. Se a descrição muda muito, o nome operacional do segmento precisa ser tratado com cautela.

## 14. Arquivos relacionados e próximos passos

A [implementação](cluster_profiling.py) faz os cálculos; a [fachada](__init__.py) exporta `profile_clusters` e `top_differentiators`; o [notebook](exemplo_cluster_profiling.py) mostra por que ranking não substitui magnitude.

Depois do profiling, valide estabilidade e utilidade de negócio antes de consolidar nomes de segmentos.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base da R08. As métricas aqui são cálculos locais definidos no código; não há uma norma estatística externa que transforme o campo chamado `z_score` em teste de hipótese.

A revisão R08 não presume publicação Databricks, homologação de segmentação nem auditoria independente.
