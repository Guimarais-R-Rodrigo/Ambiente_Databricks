# Databricks notebook source
# MAGIC %md
# MAGIC # `arima_wrapper` — ARIMA com a ordem escolhida por busca, não por chute
# MAGIC
# MAGIC **O problema.** Escolher (p, d, q) no olho leva a modelo que passa no teste e falha fora dele. E ARIMA aplicado a série não estacionária produz previsão que diverge com confiança.
# MAGIC
# MAGIC **O que este helper faz.** Roda `auto_arima`, que busca a ordem por critério de informação e já resolve a diferenciação necessária.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `pmdarima (com pin de numpy)` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~1 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install "pmdarima==2.0.4" "numpy==1.23.5"

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

from hub_snippets.ml.arima_wrapper import train_arima

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
# MAGIC ## 1. Uma série com raiz unitária, que é o caso difícil

# COMMAND ----------

# Passeio aleatorio com deriva: NAO e estacionario. E o caso em que a
# diferenciacao importa, e em que ARIMA aplicado cru produz besteira.
n = 120
serie = np.cumsum(rng.normal(0.5, 2.0, n)) + 100
print(f"periodos: {n} | primeiro {serie[0]:.1f} | ultimo {serie[-1]:.1f}")
print(f"media da primeira metade {serie[:60].mean():.1f} | segunda metade {serie[60:].mean():.1f}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC periodos: 120 | primeiro 101.1 | ultimo 145.5
# MAGIC media da primeira metade 117.2 | segunda metade 142.4
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** As médias das duas metades diferem em 25 unidades. Isso é o
# MAGIC sintoma de **não estacionariedade**: a série não oscila em torno de um nível
# MAGIC fixo, ela caminha. ARIMA aplicado direto sobre isso, sem diferenciar,
# MAGIC produz previsão que volta para a média histórica — que é justamente o que
# MAGIC uma série com deriva não faz.


# COMMAND ----------

# O retorno tem TRES elementos, nao dois: modelo, previsao e metricas.
modelo, previsao, metricas = train_arima(
    serie, m=12, forecast_periods=6, seasonal=False, log_mlflow=False,
)
print(f"ordem escolhida: {modelo.order}")
print(f"previsao dos proximos 6 periodos: {np.round(np.asarray(previsao), 1).tolist()}")
print("")
print("metricas do ajuste:")
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC ordem escolhida: (0, 1, 0)
# MAGIC previsao dos proximos 6 periodos: [145.9, 146.2, 146.6, 147.0, 147.4, 147.7]
# MAGIC
# MAGIC aic                      448.8110
# MAGIC bic                      454.3693
# MAGIC rmse_insample            9.3276
# MAGIC mape_insample            1.8345
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A ordem escolhida é **(0, 1, 0)** — zero termos autorregressivos,
# MAGIC **uma** diferenciação, zero médias móveis. Traduzindo: a busca concluiu que
# MAGIC a melhor descrição desta série é "passeio aleatório com deriva", e que
# MAGIC **não há estrutura a modelar** além da tendência.
# MAGIC
# MAGIC Está certo — foi assim que a série foi gerada. E é o resultado mais útil
# MAGIC que o `auto_arima` pode dar, porque é o que ninguém escolheria à mão. Quem
# MAGIC ajusta ordem no olho tende a pôr termos AR e MA "para melhorar", e cada um
# MAGIC deles ajusta ruído.
# MAGIC
# MAGIC Repare na previsão: **145,9 → 147,7**, uma reta. Passeio aleatório com
# MAGIC deriva prevê exatamente isso — o último valor mais a deriva acumulada. Se
# MAGIC a sua previsão de série temporal parece uma reta, pode não ser preguiça do
# MAGIC modelo: pode ser a resposta honesta.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem olhar os resíduos.** ARIMA que passou no AIC e deixou autocorrelação nos resíduos ainda tem sinal na mesa.
# MAGIC - **Com sazonalidade forte e `seasonal=False`.** A busca vai compensar com ordem alta e ajustar ruído.
# MAGIC - **Para horizonte longo.** O intervalo de confiança abre rápido; a partir de certo ponto ele cobre qualquer coisa e deixa de informar.
