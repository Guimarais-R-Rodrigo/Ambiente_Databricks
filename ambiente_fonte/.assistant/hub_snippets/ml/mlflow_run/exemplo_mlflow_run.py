# Databricks notebook source
# MAGIC %md
# MAGIC # `mlflow_run` — registro que recusa ficar incompleto
# MAGIC
# MAGIC **Guia local completo:** [README.md](README.md)
# MAGIC
# MAGIC **O problema.** Um run pode ter métricas e ainda ser impossível de reconstruir. Dataset, split, limitações e contrato de entrada precisam acompanhar a evidência.
# MAGIC
# MAGIC **O que este helper faz.** Abre um run MLflow e, por padrão, recusa fechá-lo sem parâmetros, métricas e assinatura. O registro continua dependendo do tracking/runtime MLflow disponível no ambiente.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | runtime com MLflow funcional |
# MAGIC | Bibliotecas | MLflow; scikit-learn para `run.modelo()` e para esta fixture |
# MAGIC | Dados | sintéticos |
# MAGIC | Escrita | sim — quando o tracking abre, cria run e registra dados/artefatos |
# MAGIC | Diferença Free × trabalho | **revalidar no momento da execução**; o bloco histórico abaixo descreve uma observação datada, não regra permanente |

# COMMAND ----------
import sys
usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")
import numpy as np
rng = np.random.default_rng(42)
from hub_snippets.ml.mlflow_run import run_governado

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. A recusa é parte do contrato

# COMMAND ----------
try:
    with run_governado("exemplo_incompleto", dataset="tabela sintética do notebook", split="temporal, corte em 2026-06", limitacoes=""):
        pass
except ValueError as erro:
    print(f"recusou antes de abrir:\n  {erro}")

# COMMAND ----------
# MAGIC %md
# MAGIC `limitacoes` vazio é recusado antes da abertura do run. No fechamento, `exigir_completo=True` também exige parâmetros, métricas e assinatura.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Um run por bloco
# MAGIC
# MAGIC `run_governado` abre um run próprio. Isso delimita o experimento e reduz colisões com parâmetros já registrados em outro run. Evite colocá-lo dentro de um run ativo sem uma política explícita de nesting.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Caminho completo e evidência histórica de runtime

# COMMAND ----------
from sklearn.linear_model import LogisticRegression
X = rng.normal(0, 1, (600, 3))
y = (X[:, 0] + rng.normal(0, 0.5, 600) > 0).astype(int)
modelo = LogisticRegression(max_iter=200).fit(X, y)
try:
    with run_governado(
        "baseline_propensao",
        dataset="sintética, 600 linhas, gerada nesta célula com seed 42",
        split="sem split — é demonstração de registro, não de avaliação",
        limitacoes=["dados sintéticos", "métrica de treino", "fixture com três features contínuas"],
    ) as run:
        run.parametros({"algorithm": "logistic_regression", "max_iter": 200})
        run.metricas({"acuracia_treino": float(modelo.score(X, y))})
        run.modelo(modelo, exemplo_entrada=X[:2])
    print("run completo aceito e fechado")
except Exception as erro:
    print("o run não abriu neste runtime:")
    print(f"  {type(erro).__name__}: {str(erro).splitlines()[0]}")

# COMMAND ----------
# MAGIC %md
# MAGIC O notebook registrou historicamente uma `AnalysisException` relacionada a `spark.mlflow.modelRegistryUri` em um serverless Free e também possui evidência anterior de sucesso. Essas observações mostram justamente que **runtime gerenciado muda**: verifique novamente no workspace atual; não conclua que todo serverless Free falha ou que todo compute clássico funciona.
# MAGIC
# MAGIC `run.modelo()` usa `mlflow.sklearn.log_model`. Portanto, este atalho é adequado ao flavor sklearn; LightGBM, PyTorch e outros modelos devem usar o flavor apropriado ou registro específico.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - como substituto do processo de governança;
# MAGIC - sem tracking/experimento autorizado;
# MAGIC - para modelo não-sklearn esperando que `run.modelo()` escolha flavor automaticamente;
# MAGIC - como garantia de reprodutibilidade se dataset/split não identificarem de fato a população usada.
