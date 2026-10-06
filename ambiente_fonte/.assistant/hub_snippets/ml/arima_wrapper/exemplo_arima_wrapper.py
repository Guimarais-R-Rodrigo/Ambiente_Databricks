# Databricks notebook source
# MAGIC %md
# MAGIC # `arima_wrapper` — ARIMA com a ordem escolhida por busca, não por chute
# MAGIC
# MAGIC **O problema.** Escolher (p, d, q) sem protocolo explícito torna a comparação difícil. Não estacionariedade e diferenciação também precisam ser tratadas de acordo com a série e verificadas fora da amostra.
# MAGIC
# MAGIC **O que este helper faz.** Roda `auto_arima`, que pesquisa uma especificação segundo o procedimento/configuração da biblioteca e pode selecionar diferenciação. A ordem escolhida continua sendo um candidato a validar fora da amostra.

# MAGIC
# MAGIC **Guia local completo:** [README deste objeto](README.md).
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
# MAGIC Este exemplo passa log_mlflow=False para desativar apenas o registro explícito do helper. Antes de habilitar tracking, confirme dependência, experimento, permissões, configuração do runtime e autologging da sessão. Uma falha numa configuração de serverless não determina o suporte em outras configurações.

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
# MAGIC **Como ler.** Nesta execução a busca selecionou **(0, 1, 0)**: zero termos
# MAGIC autorregressivos, uma diferenciação e zero médias móveis. Isso é a especificação
# MAGIC escolhida pelo procedimento para esta amostra e este espaço de busca; não prova
# MAGIC que o processo gerador real foi identificado nem que termos adicionais seriam
# MAGIC necessariamente ruído. A coincidência com a forma usada para gerar este exemplo
# MAGIC sintético é uma checagem didática, não uma garantia geral do método.
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
# MAGIC - **Quando o horizonte excede a evidência disponível.** Incerteza tende a crescer com o horizonte; meça cobertura e erro por horizonte em backtest em vez de assumir um ponto universal de inutilidade.
