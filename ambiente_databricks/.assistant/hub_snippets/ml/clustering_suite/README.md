# `clustering_suite` — comparar agrupamentos e selecionar configuração sem tratar heurística como verdade

<!-- readme-objeto: 1.0.0 -->

Este objeto padroniza features, ajusta K-Means, Gaussian Mixture ou DBSCAN e calcula métricas internas quando elas são definidas. Também oferece `select_k`, que compara candidatos de K-Means. O `best_k` é uma **heurística implementada**, não prova de que aquele número de segmentos seja o único correto.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Pipeline pandas/NumPy + scikit-learn para clustering e métricas internas. |
| Para que serve? | Comparar `k`, ajustar agrupamentos e devolver labels, modelo, scaler e métricas. |
| Use quando... | Features numéricas finitas e objetivo exploratório de agrupamento estão claros. |
| Evite quando... | Há categóricas brutas, necessidade de escala distribuída ou exigência de segmento de negócio já validado. |
| Precisa de... | pandas, NumPy, scikit-learn e `mlflow` importável; pelo menos 3 linhas finitas. |
| Entrega... | Dict com `labels`, `metrics`, `model`, `scaler` e `X_scaled`; `select_k` devolve scores + `best_k`. |

Consulte a [implementação](clustering_suite.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_clustering_suite.py).

## 1. O que é?

Clustering agrupa observações sem target supervisionado. Esta pasta reúne três algoritmos e uma rotina de comparação de `k` para K-Means.

A implementação não é um “auto-clustering” geral: DBSCAN usa parâmetros fixos, GMM/K-Means recebem `k`, e a seleção automática de `k` é baseada nas métricas implementadas.

## 2. Que problema este recurso resolve?

Ele organiza uma pergunta recorrente: “com estas features e esta escala, como ficam diferentes configurações de agrupamento e quais métricas internas elas produzem?”. Isso evita espalhar scaler, ajuste e cálculo de métricas por notebooks diferentes.

## 3. Quando faz sentido usar?

Use como baseline exploratório em dados tabulares numéricos, com poucas/médias dimensões e tamanho que caiba no processo Python.

É útil para comparar K-Means/GMM sob um `k` explicitamente escolhido e para experimentar DBSCAN quando os defaults locais fizerem sentido como ponto de partida.

## 4. Quando não usar?

Não use IDs de categorias como se fossem distâncias numéricas. Não use métricas internas para declarar sozinho um número “verdadeiro” de segmentos.

Para grandes volumes Spark, este helper é driver-side e não distribui o ajuste. Para densidades muito diferentes ou DBSCAN que exige tuning de `eps/min_samples`, a assinatura atual é limitada.

## 5. Como funciona, intuitivamente?

`run_clustering_pipeline` seleciona as `feature_cols`, exige valores finitos e aplica `StandardScaler` ou `RobustScaler`. Se `k=None` para K-Means/GMM, chama `select_k`.

`select_k` ajusta K-Means para cada candidato e calcula inércia, silhouette, Calinski-Harabasz e Davies-Bouldin. Com `method="elbow"` e pelo menos três candidatos, usa a maior segunda diferença da inércia; nos modos `"silhouette"` e `"both"`, `best_k` é o maior silhouette.

Depois o pipeline ajusta o algoritmo escolhido e calcula métricas internas excluindo label `-1` do DBSCAN.

## 6. Exemplo de situação

Uma equipe planta três grupos sintéticos bem separados e quer conferir se a heurística encontra `k=3`. O notebook mostra a tabela de scores e depois ajusta K-Means com `k=3`.

Em dados reais, concordância das métricas é evidência útil, mas não substitui estabilidade, interpretabilidade e capacidade de operar os segmentos.

## 7. O que você precisa antes de usar?

`df` precisa conter todas as `feature_cols`, sem NaN/inf nas features usadas e com pelo menos três linhas. O helper espera features numéricas.

O módulo importa `mlflow` no topo, portanto `mlflow` precisa ser importável mesmo quando `log_mlflow=False`. Com `log_mlflow=True`, a função registra parâmetros e métricas no contexto MLflow disponível.

Para seleção automática, todos os valores de `k_range` devem estar entre 2 e `n_samples - 1`.

## 8. O que este recurso entrega?

`select_k` retorna `{"scores": DataFrame, "best_k": ...}`. A tabela contém `k`, `inertia`, `silhouette`, `calinski` e `davies_bouldin`.

`run_clustering_pipeline` retorna labels, dicionário de métricas, modelo ajustado, scaler ajustado e matriz transformada. Para DBSCAN, `n_noise` conta label `-1` e `n_clusters` exclui esse ruído.

Se houver menos de dois clusters não-ruído, silhouette/Calinski/Davies não são adicionados.

## 9. Como usar este recurso no Hub?

Para escolher `k` em amostra pequena, limite os candidatos depois de aplicar a escala escolhida:

```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from hub_snippets.ml.clustering_suite import select_k

X_scaled = StandardScaler().fit_transform(df[["f1", "f2"]])
n = len(X_scaled)
assert n >= 3 and np.isfinite(X_scaled).all()
assert len(np.unique(X_scaled, axis=0)) >= 2
resultado_k = select_k(X_scaled, k_range=range(2, min(11, n)))
```

O intervalo evita `k >= n`, mas não garante silhouette válida: pontos repetidos podem produzir menos rótulos distintos que o solicitado. Verifique diversidade e os rótulos efetivos de cada ajuste; a função pode falhar durante a seleção. Três linhas finitas não tornam o default `range(2,11)` apropriado.

```python
from hub_snippets.ml.clustering_suite import run_clustering_pipeline

out = run_clustering_pipeline(
    df,
    feature_cols=["f1", "f2"],
    k=3,
    algorithm="kmeans",
    scaler="standard",
    log_mlflow=False,
)
```

O [notebook](exemplo_clustering_suite.py) usa dados sintéticos e desliga MLflow explicitamente.

## 10. Decisões e configurações que mais importam

Para `algorithm="gmm"` com `k=None`, a escolha automática continua sendo feita por **KMeans/silhouette**, não por AIC/BIC de misturas gaussianas. Isso escolhe um candidato segundo outra geometria; justifique a transferência do k ou passe um k avaliado especificamente para GMM.

`algorithm` aceita `kmeans`, `gmm` ou `dbscan`; `scaler` aceita `standard` ou `robust`.

`k` explícito evita a seleção automática. `k_range` importa apenas quando `k=None` e o algoritmo não é DBSCAN. O parâmetro `method` existe em `select_k`, não em `run_clustering_pipeline`.

Na implementação atual, DBSCAN usa `eps=0.5` e `min_samples=5` fixos; a API não expõe esses dois valores.

## 11. Limitações, riscos e armadilhas

KMeans e GMM permitem aplicar `out["scaler"].transform(X_novo)` e depois `out["model"].predict(...)`, mantendo features/ordem e sem novo fit. DBSCAN não oferece `predict` out-of-sample nessa rota, e o wrapper não implementa atribuição de novas observações. Reajustar DBSCAN pode mudar todos os grupos; não o apresente como scoring estável de um modelo já ajustado.

Silhouette, Calinski-Harabasz e Davies-Bouldin avaliam geometria interna sob determinadas noções de distância/separação. Elas não medem automaticamente valor de negócio, fairness ou estabilidade temporal.

`method="both"` não cria votação entre métricas: o `best_k` continua sendo o maior silhouette. O texto impresso “Melhor silhouette” também aparece no modo elbow usando o índice escolhido pelo cotovelo, portanto leia a tabela, não apenas a frase.

O scaler é ajustado na mesma base entregue para clusterização. Para aplicar o agrupamento a novos dados, preserve `scaler` e `model` e defina uma política de inferência compatível com o algoritmo.

## 12. Quais são as alternativas?

[`cluster_profiling`](../cluster_profiling/README.md) descreve grupos já formados. [`umap_viz`](../umap_viz/README.md) projeta para exploração visual.

Para densidade com hiperparâmetros controláveis, use uma implementação que exponha `eps/min_samples` ou considere HDBSCAN quando fizer sentido. Para escala distribuída, procure algoritmos compatíveis com o runtime distribuído em vez de coletar tudo ao driver.

## 13. Como saber se o resultado faz sentido?

Compare várias sementes/configurações, tamanhos dos grupos e métricas. Perfile os clusters e verifique se diferenças são estáveis em outra amostra/período.

Cheque também se a escolha é operacional: um `k` com silhouette ligeiramente maior pode ser pior para uma área incapaz de agir sobre tantos segmentos.

## 14. Arquivos relacionados e próximos passos

A [implementação](clustering_suite.py) contém seleção, scaler e ajuste; a [fachada](__init__.py) exporta `SEED`, `select_k` e `run_clustering_pipeline`; o [notebook](exemplo_clustering_suite.py) exercita K-Means.

Use o resultado com [`cluster_profiling`](../cluster_profiling/README.md) antes de nomear grupos.

## 15. Referências

Consulte as APIs silhouette_score, calinski_harabasz_score e davies_bouldin_score do scikit-learn. Essas métricas descrevem geometria na amostra; a seleção de k deve ser validada por estabilidade e uso dos grupos.

Referências primárias de conceito/API: [Documentação primária de clustering_suite](https://scikit-learn.org/stable/api/sklearn.metrics.html).
