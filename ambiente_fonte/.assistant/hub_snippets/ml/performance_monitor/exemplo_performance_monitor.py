# Databricks notebook source
# MAGIC %md
# MAGIC # `performance_monitor` — acompanhar métrica contra política, não contra o passado
# MAGIC
# MAGIC **O problema.** Monitorar um modelo costuma virar um gráfico de AUC por mês, e o gráfico não responde a pergunta que importa: isto é degradação ou variação normal? Sem um limite declarado antes, cada queda vira discussão e cada alta vira comemoração.
# MAGIC
# MAGIC **O que este helper faz.** Registra métricas ao longo do tempo e as compara contra limites **calibrados e declarados**, devolvendo o veredito.

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
import pandas as pd

rng = np.random.default_rng(42)

from hub_snippets.ml.performance_monitor import EXAMPLE_THRESHOLDS, PerformanceMonitor

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. A política vem antes da série

# COMMAND ----------

print("limites de EXEMPLO (não use em produção sem calibrar):")
for k, v in EXAMPLE_THRESHOLDS.items():
    print(f"  {k:20} {v}")

# O baseline e a política são exigidos na construção: o monitor não tem
# como decidir "caiu" sem saber de onde partiu nem quanto pode cair.
monitor = PerformanceMonitor(
    baseline_metrics={"auc": 0.78},
    model_name="exemplo_propensao",
    policy=EXAMPLE_THRESHOLDS,
)

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC auc         {'warning': 0.03, 'critical': 0.05, 'direction': 'higher', 'delta': 'absolute'}
# MAGIC ks_pct      {'warning': 3.0,  'critical': 5.0,  'direction': 'higher', 'delta': 'absolute'}
# MAGIC gini        {'warning': 0.05, 'critical': 0.08, 'direction': 'higher', 'delta': 'absolute'}
# MAGIC rmse        {'warning': 0.1,  'critical': 0.2,  'direction': 'lower',  'delta': 'relative'}
# MAGIC mape        {'warning': 0.1,  'critical': 0.2,  'direction': 'lower',  'delta': 'relative'}
# MAGIC ndcg_at_10  {'warning': 0.05, 'critical': 0.1,  'direction': 'higher', 'delta': 'absolute'}
# MAGIC c_index     {'warning': 0.03, 'critical': 0.05, 'direction': 'higher', 'delta': 'absolute'}
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O nome da constante é o aviso: são limites de **exemplo**. Um
# MAGIC AUC mínimo de 0,65 pode ser folgado para um modelo de propensão e
# MAGIC inaceitável para um de fraude.
# MAGIC
# MAGIC Calibrar significa olhar a variação histórica do próprio modelo e escolher
# MAGIC o limite abaixo do qual a decisão muda. Sem isso, o monitor vira gerador de
# MAGIC alerta que ninguém lê.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Uma série com degradação no fim

# COMMAND ----------

meses = pd.date_range("2026-01-01", periods=8, freq="MS")
aucs = [0.78, 0.77, 0.79, 0.76, 0.77, 0.71, 0.66, 0.61]

for mes, auc in zip(meses, aucs):
    monitor.add_period(period=str(mes.date()), metrics={"auc": auc})

print(monitor.generate_report())
print()
print(f"status atual: {monitor.get_current_status()}")
print(f"decisão de retreino: {monitor.should_retrain()}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A série cai de 0,78 para 0,61 nos três últimos meses. O
# MAGIC ponto do monitor é que essa leitura **não depende de alguém olhar o
# MAGIC gráfico**: o limite estava declarado antes, e o veredito sai por
# MAGIC comparação.
# MAGIC
# MAGIC O erro de interpretação mais provável é comparar cada mês com o anterior.
# MAGIC Variação mês a mês é ruído; o que decide retreino é a comparação contra o
# MAGIC limite, e a persistência abaixo dele.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem calibrar os limites.** `EXAMPLE_THRESHOLDS` é ponto de partida, não política.
# MAGIC - **Comparando mês contra mês.** A referência é o limite, não o mês anterior.
# MAGIC - **Com alvo ainda não realizado.** Métrica de performance exige rótulo; em produto de crédito ele chega meses depois.
# MAGIC - **Como gatilho automático de retreino.** O monitor informa; retreinar é decisão com custo e risco próprios.

# COMMAND ----------
# MAGIC %md
# MAGIC ### Contrato atualizado em 09/09/2026
# MAGIC Seleção de métricas: valores inválidos selecionados pela política agora geram erro. Use metricas_obrigatorias para exigir auc e ks_pct; para excluir uma métrica deliberadamente, forneça uma política sem essa chave. KS antigo em 0–100 mantém o valor ao migrar para ks_pct.
