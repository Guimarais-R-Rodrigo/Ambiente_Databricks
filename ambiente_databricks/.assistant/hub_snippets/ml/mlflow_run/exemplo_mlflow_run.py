# Databricks notebook source
# MAGIC %md
# MAGIC # `mlflow_run` — registro que recusa ficar incompleto
# MAGIC
# MAGIC **O problema.** Registrar um experimento no MLflow é fácil e registrar **o suficiente** não é. Meses depois, o que falta nunca é a métrica: é qual base foi usada, como o split foi feito e o que o modelo não cobre. E há uma armadilha de runtime — dois wrappers de treino na mesma sessão colidem na chave `algorithm`, que o MLflow trata como imutável.
# MAGIC
# MAGIC **O que este helper faz.** Abre um run isolado e **recusa fechá-lo** sem o conjunto mínimo de registro. O efeito depende do tracking MLflow disponível no ambiente.
# MAGIC
# MAGIC **Guia local completo:** [README deste objeto](README.md).

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | runtime com tracking MLflow funcional; revalidar no destino |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side** |
# MAGIC | Escrita | **tentada** — nenhum run chega a abrir neste runtime; ver a seção 3 |
# MAGIC | Diferença Free × trabalho | a seção 3 preserva observação histórica datada; não é regra universal do Free nem garantia sobre compute clássico |

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
# MAGIC Registro completo: confirme primeiro tracking, experimento e permissões. O bloco seguinte registra parâmetros, métricas e modelo no backend configurado; não é uma operação só em memória.

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
        limitacoes=[
            "dados sintéticos: não sustenta nenhuma conclusão de negócio",
            "sem validação temporal: a métrica abaixo é de treino",
            "três features contínuas; não cobre categórica nem faltante",
        ],
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
# MAGIC Exceção registrada no ensaio de referência do Free em 17/08/2026;
# MAGIC descreve aquela configuração, sem determinar suporte no seu runtime:
# MAGIC
# MAGIC ```text
# MAGIC AnalysisException: [CONFIG_NOT_AVAILABLE.WITHOUT_SUGGESTION]
# MAGIC Configuration spark.mlflow.modelRegistryUri is not available.
# MAGIC ```
# MAGIC
# MAGIC Se o registro falhar por configuração do tracking, anote a exceção e confira a configuração/versionamento do runtime. Não conclua que todo serverless ou todo compute clássico tem o mesmo suporte. Uma falha após abrir o run pode deixar artefatos parciais; consulte o backend antes de repetir. O histórico de ensaios e seus links estão nas referências do [README](README.md).
# MAGIC
# MAGIC **Uma dependência que não aparece no `import`:** quando o run abre,
# MAGIC `run.modelo()` chama `mlflow.sklearn.log_model`, e `import mlflow` **não**
# MAGIC traz o `scikit-learn` junto — o *flavor* é resolvido na hora da chamada.
# MAGIC Está registrado em `hub_snippets/requirements-optional.txt`.
# MAGIC
# MAGIC E o *flavor* é fixo: qualquer modelo vai registrado como sklearn, mesmo um
# MAGIC Booster do LightGBM. Para esses, registre à mão com o flavor correto.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Para registrar tudo.** Ele existe para o registro que sustenta decisão; log exploratório polui o experimento.
# MAGIC - **Sem assinatura do modelo.** Sem ela, quem for servir não sabe o esquema de entrada, e o erro aparece em produção.
# MAGIC - **Dentro de outro run ativo.** Aninhar runs confunde a leitura; feche o de fora antes.
# MAGIC - **Como substituto de governança.** Ele força campos; quem decide se o modelo pode ir para produção é o processo, não o registro.
