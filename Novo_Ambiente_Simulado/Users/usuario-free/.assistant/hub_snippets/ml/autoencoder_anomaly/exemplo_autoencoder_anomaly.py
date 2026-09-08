# Databricks notebook source
# MAGIC %md
# MAGIC # `autoencoder_anomaly` — detectar o estranho aprendendo só o normal
# MAGIC
# MAGIC **O problema.** Detecção de fraude por classificação supervisionada exige rótulo de fraude — que é raro, chega tarde e só cobre o que já se sabia procurar. O padrão novo não tem rótulo nenhum.
# MAGIC
# MAGIC **O que este helper faz.** Treina um autoencoder apenas sobre casos normais; o que ele não consegue reconstruir bem é o candidato a anomalia.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `torch` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~5 min no Free (o `torch` é pesado); no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install torch

# COMMAND ----------
# MAGIC %restart_python

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparação
# MAGIC
# MAGIC `%restart_python` reinicia o interpretador, então tudo — inclusive o
# MAGIC `sys.path` — precisa vir **depois** dele.

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np

rng = np.random.default_rng(42)

from hub_snippets.ml.autoencoder_anomaly import Autoencoder, train_autoencoder_anomaly

# COMMAND ----------
# MAGIC %md
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. **Nenhum run do MLflow abre
# MAGIC no serverless do Free**: `mlflow.start_run` instancia um `MlflowClient` que
# MAGIC lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config.
# MAGIC
# MAGIC No trabalho, com compute clássico, deixe o padrão `True` — é justamente o
# MAGIC registro que torna o baseline rastreável. Aqui ele é desligado para que o
# MAGIC notebook rode, e a limitação está na matriz de `free-vs-trabalho`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma população normal e um punhado de estranhos plantados

# COMMAND ----------

from sklearn.preprocessing import StandardScaler

n_normal, n_teste, n_estranhos = 4000, 1000, 50

# o "normal" tem estrutura: as colunas sao correlacionadas
base_normal = rng.normal(0, 1, (n_normal, 6))
base_normal[:, 1] += 0.8 * base_normal[:, 0]
base_normal[:, 3] += 0.6 * base_normal[:, 2]

teste_normal = rng.normal(0, 1, (n_teste - n_estranhos, 6))
teste_normal[:, 1] += 0.8 * teste_normal[:, 0]
teste_normal[:, 3] += 0.6 * teste_normal[:, 2]

# os estranhos NAO seguem a correlacao: e isso que o autoencoder nao reconstroi
estranhos = rng.normal(0, 1.2, (n_estranhos, 6))

X_teste = np.vstack([teste_normal, estranhos])
verdade = np.concatenate([np.zeros(len(teste_normal)), np.ones(n_estranhos)])

escalador = StandardScaler().fit(base_normal)
X_treino_s = escalador.transform(base_normal).astype("float32")
X_teste_s = escalador.transform(X_teste).astype("float32")
print(f"treino so-normal: {X_treino_s.shape} | teste: {X_teste_s.shape}")
print(f"estranhos plantados no teste: {int(verdade.sum())} ({100 * verdade.mean():.1f}%)")

# COMMAND ----------

modelo, limiar, erros = train_autoencoder_anomaly(
    X_treino_s, X_teste_s, encoding_dim=3, epochs=25, batch_size=256,
    threshold_percentile=95.0, log_mlflow=False,
)
marcados = (erros > limiar).astype(int)
print(f"limiar (percentil 95 do treino): {limiar:.5f}")
print(f"marcados como anomalia: {marcados.sum()} de {len(marcados)}")
print(f"destes, realmente estranhos: {int(((marcados == 1) & (verdade == 1)).sum())}")
print(f"estranhos que passaram: {int(((marcados == 0) & (verdade == 1)).sum())}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC treino so-normal: (4000, 6) | teste: (1000, 6)
# MAGIC estranhos plantados no teste: 50 (5.0%)
# MAGIC
# MAGIC limiar (percentil 95 do treino): 0.70588
# MAGIC marcados como anomalia: 81 de 1000
# MAGIC destes, realmente estranhos: 19
# MAGIC estranhos que passaram: 31
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O resultado é **ruim**, e é assim que ele deve ser reportado:
# MAGIC de 81 marcados, só **19 eram estranhos de verdade** — 23% de precisão. E
# MAGIC **31 dos 50 estranhos passaram** despercebidos, o que dá 38% de cobertura.
# MAGIC Uma fila de análise construída sobre isso desperdiçaria três de cada
# MAGIC quatro visitas e ainda deixaria a maioria das anomalias passar.
# MAGIC
# MAGIC Deixar o número ruim aqui é deliberado. Um notebook didático que só mostra
# MAGIC o caso em que o método brilha ensina a confiar nele, que é o oposto do que
# MAGIC serve.
# MAGIC
# MAGIC **Por que foi mal:** os estranhos foram gerados com desvio 1,2 contra 1,0
# MAGIC do normal, sem seguir as correlações — uma anomalia sutil, de estrutura e
# MAGIC não de escala. Com 25 épocas e código de dimensão 3, o autoencoder aprendeu
# MAGIC a reconstruir bem o normal e razoavelmente bem o estranho também.
# MAGIC
# MAGIC **E repare no limiar:** `threshold_percentile=95` marca 5% do *treino* por
# MAGIC construção, e no teste marcou 8,1%. O número de marcados é decidido pelo
# MAGIC percentil que você escolheu, **não** pela quantidade de anomalias que
# MAGIC existe. Aumentar para 99 marcaria menos e acharia menos; o método não sabe
# MAGIC quantas anomalias há.
# MAGIC
# MAGIC **E o alternativo óbvio vai pior aqui.** Medido sobre esta mesma fixture:
# MAGIC
# MAGIC ```text
# MAGIC                                    marcados  acertos  precisão  cobertura
# MAGIC autoencoder (acima)                      81       19     23,5%      38,0%
# MAGIC IsolationForest contamination=0.05       61        7     11,5%      14,0%
# MAGIC IsolationForest contamination=0.081      91       10     11,0%      20,0%
# MAGIC IsolationForest contamination=0.10      109       12     11,0%      24,0%
# MAGIC
# MAGIC AUC do escore do IsolationForest (sem limiar): 0.6804
# MAGIC ```
# MAGIC
# MAGIC Em todo ponto de operação comparável o Isolation Forest tem **metade** da
# MAGIC precisão e metade ou menos da cobertura. Não é surpresa depois de olhar: a
# MAGIC anomalia aqui é **estrutural** — quebra de correlação, na mesma escala do
# MAGIC normal —, e árvore de isolamento corta eixo a eixo. O autoencoder aprende
# MAGIC a correlação e sente a quebra.
# MAGIC
# MAGIC Onde o Isolation Forest ganha é no caso oposto, de anomalia grosseira de
# MAGIC escala, que é o cenário do `exemplo_isolation_forest` — lá ele acerta 30
# MAGIC de 30. **Os dois notebooks reportam números que não se comparam**, porque
# MAGIC as bases são diferentes de propósito. Escolher entre os métodos depende do
# MAGIC tipo de anomalia que você espera, e essa é a decisão de verdade.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Com o "normal" contaminado.** Se o treino já tem fraude dentro, o modelo aprende a reconstruí-la e ela deixa de se destacar.
# MAGIC - **Como decisão automática.** O erro de reconstrução é um ranking de suspeita, não um veredito; ele alimenta fila de análise.
# MAGIC - **Sem padronizar.** O erro fica dominado pela variável de maior escala, e a anomalia vira "quem tem valor alto".
# MAGIC - **Em base pequena.** Rede neural com poucos milhares de linhas decora; Isolation Forest resolve melhor e mais barato.
