# Databricks notebook source
# MAGIC %md
# MAGIC # `prophet_wrapper` — série temporal com sazonalidade e feriado brasileiro
# MAGIC
# MAGIC **O problema.** Prever série com tendência, sazonalidade anual e feriado móvel à mão dá muito trabalho e erra no Carnaval. E validar previsão com sorteio aleatório de linhas mede a capacidade de interpolar, não de prever.
# MAGIC
# MAGIC **O que este helper faz.** Ajusta Prophet com sazonalidade declarada e feriados do país, devolvendo previsão e componentes separados.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `prophet` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação leva ~3 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install prophet

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

from hub_snippets.ml.prophet_wrapper import train_prophet

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
# MAGIC ## 1. Três anos de série mensal com tendência e sazonalidade

# COMMAND ----------

import pandas as pd

meses = pd.date_range("2023-01-01", periods=36, freq="MS")
tendencia = np.linspace(1000, 1600, 36)
sazonal = 120 * np.sin(2 * np.pi * np.arange(36) / 12)
serie = tendencia + sazonal + rng.normal(0, 40, 36)

base = pd.DataFrame({"ds": meses, "y": serie.round(1)})
print(f"periodos: {len(base)} | de {base['ds'].min().date()} a {base['ds'].max().date()}")
print(base.head(4).to_string(index=False))

# COMMAND ----------

# O retorno tem TRES elementos, nao dois: modelo, previsao e metricas.
modelo, previsao, metricas = train_prophet(
    base, ds_col="ds", y_col="y", periods=6, freq="MS",
    yearly=True, weekly=False, country_holidays="BR", log_mlflow=False,
)
print(f"linhas na previsao: {len(previsao)} (36 historicas + 6 futuras)")
colunas = [c for c in ["ds", "yhat", "yhat_lower", "yhat_upper", "trend"] if c in previsao.columns]
print(previsao[colunas].tail(6).to_string(index=False))
print("")
print("metricas do ajuste:")
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC linhas na previsao: 42 (36 historicas + 6 futuras)
# MAGIC
# MAGIC         ds        yhat  yhat_lower  yhat_upper       trend
# MAGIC 2026-01-01 1625.711761 1605.980552 1646.767072 -861.356104
# MAGIC 2026-02-01 1699.203587 1678.988683 1719.650987 -843.204985
# MAGIC 2026-03-01 1799.243729 1779.797934 1819.171708 -826.810427
# MAGIC 2026-04-01 1830.531285 1810.150896 1850.051121 -808.659308
# MAGIC 2026-05-01 1765.388006 1744.136678 1786.523799 -791.093709
# MAGIC 2026-06-01 1753.362525 1732.896312 1774.166786 -772.942591
# MAGIC
# MAGIC mape_insample            1.0214
# MAGIC rmse_insample            15.9480
# MAGIC mae_insample             13.2339
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O ajuste é bom: MAPE de **1,02%** sobre a própria amostra, e a
# MAGIC previsão continua a subida da série com a ondulação anual no lugar certo.
# MAGIC
# MAGIC **Agora olhe a coluna `trend`: ela sai negativa — −861 — enquanto o `yhat`
# MAGIC do mesmo mês é 1.626.** Os componentes somam ao valor previsto, então o
# MAGIC resto (sazonalidade e feriados) está carregando quase 2.500 para cima. A
# MAGIC previsão fecha; a decomposição não descreve a série que geramos, que tem
# MAGIC tendência crescente e sazonalidade de amplitude 120.
# MAGIC
# MAGIC Não vou explicar isso como se soubesse a causa. Com 36 pontos mensais e
# MAGIC sazonalidade anual ligada, Prophet tem pouca informação para separar
# MAGIC tendência de ciclo, e escolhe uma decomposição entre muitas que ajustam
# MAGIC igualmente bem. **O registro aqui é o achado, não a explicação.**
# MAGIC
# MAGIC E é exatamente por isso que o "quando não usar" abaixo diz para não tratar
# MAGIC os componentes como leitura de negócio sem conferi-los. Uma apresentação
# MAGIC que mostrasse este `trend` como "a tendência do produto" estaria contando
# MAGIC uma história que o dado não sustenta — com um MAPE de 1% na mesma página
# MAGIC para dar credibilidade.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Em série curta.** Sem dois ciclos completos, a sazonalidade anual é chute com intervalo de confiança.
# MAGIC - **Como caixa-preta de negócio.** O valor dele está nos componentes separados — tendência, sazonalidade, feriado. Olhar só o `yhat` desperdiça o método.
# MAGIC - **Para série com quebra estrutural conhecida.** Mudança de política ou de produto pede `changepoints` declarados, não descobertos.
