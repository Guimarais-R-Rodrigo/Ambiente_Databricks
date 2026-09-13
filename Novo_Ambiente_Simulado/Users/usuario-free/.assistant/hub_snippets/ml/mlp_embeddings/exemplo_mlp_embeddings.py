# Databricks notebook source
# MAGIC %md
# MAGIC # `mlp_embeddings` — embedding para categórica que árvore não resolve bem
# MAGIC
# MAGIC **O problema.** Categóricas com muitos níveis podem tornar one-hot muito largo. Uma embedding oferece outra hipótese: aprender vetores densos por nível e ajustar essa representação junto com a tarefa.
# MAGIC
# MAGIC **O que este helper faz.** Treina uma MLP com camada de *embedding* por categórica, que aprende a representação junto com a tarefa.

# MAGIC
# MAGIC **Guia local completo:** [README deste modelo](README.md).
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
# MAGIC O ponto do notebook não é o placar: o sinal foi construído em grupos latentes de agência e produto. A embedding oferece uma representação densa em que níveis podem aprender vetores semelhantes. Isso é uma capacidade de representação, não prova de que one-hot ou árvores seriam incapazes de modelar a relação; a comparação precisa ser feita no mesmo protocolo.
# MAGIC
# MAGIC **Antes de adotar isso, faça a comparação honesta:** rode um baseline tabular na mesma base, com a mesma partição e métrica. Embeddings se justificam quando a representação aprendida acrescenta valor suficiente para compensar preparo de índices, categorias novas, custo e manutenção.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem baseline comparável.** Primeiro estabeleça uma referência mais simples sob os mesmos dados; só então meça se a embedding acrescenta valor.
# MAGIC - **Quando uma representação simples já é suficiente.** Baixa cardinalidade pode favorecer one-hot ou tratamento nativo, mas não existe um corte universal de níveis.
# MAGIC - **Com poucos exemplos por nível.** Embeddings pouco observadas podem ficar instáveis; avalie cobertura por categoria e desempenho fora da amostra.
# MAGIC - **Sem tratar nível novo.** Categoria que não existia no treino não tem vetor, e a inferência quebra ou inventa.
