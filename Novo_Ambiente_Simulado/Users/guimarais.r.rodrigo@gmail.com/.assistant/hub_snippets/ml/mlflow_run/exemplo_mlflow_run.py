# Databricks notebook source
# MAGIC %md
# MAGIC # `mlflow_run` — registro que recusa ficar incompleto
# MAGIC
# MAGIC **O problema.** Registrar um experimento no MLflow é fácil e registrar **o suficiente** não é. Meses depois, o que falta nunca é a métrica: é qual base foi usada, como o split foi feito e o que o modelo não cobre. E há uma armadilha de runtime — dois wrappers de treino na mesma sessão colidem na chave `algorithm`, que o MLflow trata como imutável.
# MAGIC
# MAGIC **O que este helper faz.** Abre um run isolado e **recusa fechá-lo** sem dataset, split, assinatura e limitações declaradas.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side** |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np

rng = np.random.default_rng(42)

from hub_snippets.ml.mlflow_run import run_governado

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. A recusa é o comportamento principal

# COMMAND ----------

try:
    with run_governado(
        "exemplo_incompleto",
        dataset="tabela sintética do notebook",
        split="temporal, corte em 2026-06",
        limitacoes="",  # vazio de propósito
    ):
        pass
except ValueError as erro:
    print(f"recusou antes de abrir:\n  {erro}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** `limitacoes` vazio é recusado na entrada. Não é rigor
# MAGIC decorativo: a seção de limitações é a que responde "onde este modelo não
# MAGIC vale", e é a primeira a ser omitida quando alguém está com pressa.
# MAGIC
# MAGIC Um registro sem ela produz, seis meses depois, um modelo que ninguém sabe
# MAGIC se pode aplicar naquele segmento novo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Por que o run precisa ser isolado
# MAGIC
# MAGIC Os wrappers de treino registram no run **ativo** do MLflow. Dois deles na
# MAGIC mesma sessão gravam `algorithm` duas vezes, e o MLflow trata parâmetro como
# MAGIC imutável — o segundo levanta erro no meio do treino, depois do custo já
# MAGIC ter sido pago.
# MAGIC
# MAGIC `run_governado` abre um run próprio por bloco, o que resolve a colisão e,
# MAGIC de quebra, deixa cada experimento com fronteira clara.
# MAGIC
# MAGIC A alternativa, quando não se quer registrar nada, é `log_mlflow=False` no
# MAGIC wrapper.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Um registro completo
# MAGIC
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO
# MAGIC
# MAGIC O que rodaria : with run_governado("baseline_churn", dataset=...,
# MAGIC                 split=..., limitacoes=...) as run: run.log_params(...)
# MAGIC Por que não   : o registro criaria um experimento permanente no workspace,
# MAGIC                 e este notebook declara "escrita: nenhuma". Um notebook
# MAGIC                 didático que suja o MLflow de quem o executa é pior que um
# MAGIC                 notebook incompleto.
# MAGIC Onde verificar: docs/testes/spark/ registra a execução real, na rodada 9
# MAGIC O que falta   : nada — é decisão de escopo, não impedimento técnico
# MAGIC ```

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Para registrar tudo.** Ele existe para o registro que sustenta decisão; log exploratório polui o experimento.
# MAGIC - **Sem assinatura do modelo.** Sem ela, quem for servir não sabe o esquema de entrada, e o erro aparece em produção.
# MAGIC - **Dentro de outro run ativo.** Aninhar runs confunde a leitura; feche o de fora antes.
# MAGIC - **Como substituto de governança.** Ele força campos; quem decide se o modelo pode ir para produção é o processo, não o registro.
