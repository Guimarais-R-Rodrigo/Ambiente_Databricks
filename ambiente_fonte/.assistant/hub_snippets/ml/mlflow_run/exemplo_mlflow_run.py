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
# MAGIC | Escrita | **tentada** — nenhum run chega a abrir neste runtime; ver a seção 3 |
# MAGIC | Diferença Free × trabalho | **sim** — nenhum run do MLflow abre no serverless do Free; ver a seção 3 |

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
# MAGIC ## 3. O registro completo — e por que ele não abre aqui
# MAGIC
# MAGIC Esta é a seção que importa: o caminho feliz do helper, com parâmetros,
# MAGIC métricas e assinatura. A célula abaixo tenta executá-lo de verdade.

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
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO no laboratório
# MAGIC
# MAGIC O que rodaria : run_governado(...) com parametros, metricas e modelo
# MAGIC Por que não   : AnalysisException: [CONFIG_NOT_AVAILABLE.WITHOUT_SUGGESTION]
# MAGIC                 Configuration spark.mlflow.modelRegistryUri is not available.
# MAGIC                 `mlflow.start_run` instancia um MlflowClient, que resolve o
# MAGIC                 registry URI lendo essa config da sessão Spark. No
# MAGIC                 serverless, o Spark Connect recusa devolvê-la, e a exceção
# MAGIC                 acontece na ABERTURA do bloco — nenhum registro chega a ser
# MAGIC                 tentado.
# MAGIC Onde verificar: .claude/rules/free-vs-trabalho.md, matriz de runtime
# MAGIC O que falta   : compute clássico, ou uma versão do MLflow que não leia essa
# MAGIC                 config. Não é ajustável pelo helper.
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** É impedimento de runtime, não de escopo: a biblioteca não
# MAGIC inicializa aqui. A célula acima captura a exceção em vez de escondê-la,
# MAGIC então o notebook continua sendo executável e se auto-verifica — em compute
# MAGIC clássico, no trabalho, ela imprime `run completo aceito e fechado`.
# MAGIC
# MAGIC **E há um detalhe que vale mais que o erro em si.** Este mesmo caminho foi
# MAGIC testado no laboratório em **14/08/2026** e passou:
# MAGIC `docs/testes/spark/resultados/` registra `mlflow_run.completo` como
# MAGIC `"run completo aceito"`. Três dias depois, no mesmo tipo de compute, ele
# MAGIC não abre. O registro de 14/08 não está errado — descreve o que era verdade
# MAGIC então. O que mudou foi o runtime do Free, por baixo, sem aviso.
# MAGIC
# MAGIC A lição é sobre método: **"foi testado" tem data de validade em ambiente
# MAGIC gerenciado.** Um teste de três dias atrás não é garantia de hoje, e é por
# MAGIC isso que a verificação vale mais que o registro dela.
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
