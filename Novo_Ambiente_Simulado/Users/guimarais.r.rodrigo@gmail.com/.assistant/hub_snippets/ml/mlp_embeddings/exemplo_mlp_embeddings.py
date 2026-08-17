# Databricks notebook source
# MAGIC %md
# MAGIC # `mlp_embeddings` — embedding para categórica que árvore não resolve bem
# MAGIC
# MAGIC **O problema.** Categórica com milhares de níveis — CEP, agência, produto — vira one-hot gigante ou codificação que perde a relação entre níveis. Árvore lida, mas não aprende que duas agências vizinhas se parecem.
# MAGIC
# MAGIC **O que este helper faz.** Treina uma MLP com camada de *embedding* por categórica, que aprende a representação junto com a tarefa.

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
# MAGIC | Diferença Free × trabalho | a instalação leva ~3 min no Free; no trabalho, confirme a política do workspace |

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

from hub_snippets.ml.mlp_embeddings import EmbeddingMLP, train_embedding_mlp

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
# MAGIC ## 1. Duas numéricas e duas categóricas de cardinalidade alta

# COMMAND ----------

n = 8000
n_agencias, n_produtos = 150, 40

agencia = rng.integers(0, n_agencias, n)
produto = rng.integers(0, n_produtos, n)
X_num = rng.normal(0, 1, (n, 2)).astype("float32")

# o sinal da categorica esta num agrupamento LATENTE, nao no codigo:
# agencias do mesmo resto-de-5 se comportam igual. E o que o embedding pode
# aprender e o one-hot nao expressa.
efeito = 0.7 * (agencia % 5) - 0.5 * (produto % 4)
y = ((1.0 * X_num[:, 0] + efeito / 2 + rng.normal(0, 1.0, n)) > 1.0).astype(int)

corte = 6000
Xn_tr, Xn_va = X_num[:corte], X_num[corte:]
Xc_tr = [agencia[:corte], produto[:corte]]
Xc_va = [agencia[corte:], produto[corte:]]
y_tr, y_va = y[:corte], y[corte:]
print(f"treino {Xn_tr.shape} | validacao {Xn_va.shape} | prevalencia {y.mean():.3f}")
print(f"cardinalidades: agencia {n_agencias}, produto {n_produtos}")

# COMMAND ----------

modelo, metricas = train_embedding_mlp(
    Xn_tr, Xc_tr, y_tr, Xn_va, Xc_va, y_va,
    cat_dims=[n_agencias, n_produtos], epochs=20, batch_size=512, log_mlflow=False,
)
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC treino (6000, 2) | validacao (2000, 2) | prevalencia 0.333
# MAGIC cardinalidades: agencia 150, produto 40
# MAGIC
# MAGIC auc_val                  0.8413
# MAGIC gini_val                 0.6826
# MAGIC epochs_trained           19
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** AUC de **0,8413** com 19 épocas — o early stopping parou antes
# MAGIC das 20 pedidas, o que indica que a validação já não melhorava.
# MAGIC
# MAGIC O ponto do notebook não é o placar: é que o sinal estava em
# MAGIC `agencia % 5` e `produto % 4`, um agrupamento **latente** que o código
# MAGIC numérico não revela. Agências 3, 8 e 13 se comportam igual, e nada na
# MAGIC ordem delas diz isso. One-hot criaria 150 colunas independentes e teria de
# MAGIC descobrir o padrão trinta vezes; o embedding aprende um vetor por nível e
# MAGIC pode colocar as três no mesmo lugar do espaço.
# MAGIC
# MAGIC **Antes de adotar isso, a comparação honesta:** rode
# MAGIC `hub_snippets.ml.train_lgbm` na mesma base. Em problema tabular do banco,
# MAGIC a árvore empata ou ganha na maior parte das vezes, treina em segundos e
# MAGIC não exige tratar nível novo na inferência. O embedding se justifica quando
# MAGIC a cardinalidade é alta **e** há estrutura entre os níveis **e** há volume
# MAGIC para aprendê-la — as três coisas juntas.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Antes de tentar árvore.** Na maioria dos problemas tabulares do banco, LightGBM empata ou ganha, e treina em minutos.
# MAGIC - **Com categórica de baixa cardinalidade.** Abaixo de ~20 níveis, one-hot resolve e é auditável.
# MAGIC - **Sem base grande.** Embedding precisa de exemplos por nível; com poucos, cada vetor é ruído aprendido.
# MAGIC - **Sem tratar nível novo.** Categoria que não existia no treino não tem vetor, e a inferência quebra ou inventa.
