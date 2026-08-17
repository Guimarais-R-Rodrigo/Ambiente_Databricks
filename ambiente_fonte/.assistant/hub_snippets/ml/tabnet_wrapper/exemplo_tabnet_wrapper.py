# Databricks notebook source
# MAGIC %md
# MAGIC # `tabnet_wrapper` — rede neural tabular que diz onde olhou
# MAGIC
# MAGIC **O problema.** Rede neural em dado tabular costuma perder para árvore e, quando ganha, não explica. Isso a torna difícil de defender em contexto que exige justificar decisão.
# MAGIC
# MAGIC **O que este helper faz.** Treina TabNet, que seleciona features por passo com máscaras esparsas — o que dá uma explicação nativa, sem SHAP por cima.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `pytorch-tabnet` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~5 min no Free (o `torch` é pesado); no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install pytorch-tabnet

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

from hub_snippets.ml.tabnet_wrapper import train_tabnet

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
# MAGIC ## 1. Um problema binário pequeno, para caber no laboratório

# COMMAND ----------

n = 5000
X = rng.normal(0, 1, (n, 8)).astype("float32")
logito = 1.3 * X[:, 0] - 0.9 * X[:, 1] + 0.6 * X[:, 2] * X[:, 3] + rng.normal(0, 0.7, n)
y = (logito > 0.9).astype(int)

corte = 3800
X_tr, y_tr = X[:corte], y[:corte]
X_va, y_va = X[corte:], y[corte:]
print(f"treino {X_tr.shape} | validacao {X_va.shape} | prevalencia {y.mean():.3f}")

# COMMAND ----------

# max_epochs baixo de proposito: o ponto e ver o mecanismo, nao o placar.
modelo, metricas, importancias = train_tabnet(
    X_tr, y_tr, X_va, y_va, task="binary",
    n_d=8, n_a=8, n_steps=3, max_epochs=15, patience=5, batch_size=512,
    log_mlflow=False,
)
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")
print("")
ordem = np.argsort(importancias)[::-1]
print("importancia por feature, do maior para o menor:")
for posicao in ordem:
    print(f"  coluna {posicao}  {importancias[posicao]:.4f}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC treino (3800, 8) | validacao (1200, 8) | prevalencia 0.307
# MAGIC
# MAGIC auc_val                  0.9242
# MAGIC gini_val                 0.8483
# MAGIC
# MAGIC importancia por feature, do maior para o menor:
# MAGIC   coluna 0  0.3957
# MAGIC   coluna 1  0.2588
# MAGIC   coluna 3  0.1229
# MAGIC   coluna 2  0.0940
# MAGIC   coluna 5  0.0577
# MAGIC   coluna 4  0.0411
# MAGIC   coluna 6  0.0153
# MAGIC   coluna 7  0.0145
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** AUC de **0,9242** parando no limite de 15 épocas — ou seja, ele
# MAGIC ainda estava melhorando quando o orçamento acabou.
# MAGIC
# MAGIC A importância recupera o sinal plantado: colunas **0** (peso 1,3) e **1**
# MAGIC (peso −0,9) lideram com 0,396 e 0,259, e as colunas **2 e 3**, que entram
# MAGIC só pelo produto `X[:,2] * X[:,3]`, aparecem juntas logo atrás. O termo de
# MAGIC interação foi encontrado sem que ninguém o declarasse.
# MAGIC
# MAGIC **A importância aqui não vem de SHAP.** Ela sai das máscaras de atenção:
# MAGIC o TabNet decide, a cada passo, em quais features olhar, e a soma dessas
# MAGIC decisões é a importância. Isso é mais barato que SHAP e mede outra coisa —
# MAGIC "onde o modelo olhou", não "quanto cada variável moveu a previsão".
# MAGIC
# MAGIC As colunas 4 a 7 são ruído puro e receberam de 0,0145 a 0,0577. Como no
# MAGIC SHAP, **nada recebe zero**, e a leitura útil continua sendo a mesma:
# MAGIC o degrau entre 0,094 e 0,058 é onde o sinal acaba.
# MAGIC
# MAGIC Para comparar com um baseline honesto, `hub_snippets.ml.train_lgbm` dá
# MAGIC 0,9268 num problema parecido, em uma fração do tempo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como primeira tentativa.** É o último recurso da lista tabular, não o primeiro. Comece pelo baseline de árvore.
# MAGIC - **Com poucos dados.** Precisa de volume para as máscaras convergirem; abaixo disso, a explicação é instável entre execuções.
# MAGIC - **Confiando na máscara como explicação suficiente.** Ela diz onde o modelo olhou, não por que aquilo importa.
# MAGIC - **Sem orçamento de tempo.** É o mais lento dos treinadores desta biblioteca, por larga margem.
