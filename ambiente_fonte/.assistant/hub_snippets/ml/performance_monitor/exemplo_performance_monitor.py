# Databricks notebook source
# MAGIC %md
# MAGIC # `performance_monitor` — acompanhar métrica contra política explícita
# MAGIC
# MAGIC **Guia local completo:** [README.md](README.md)
# MAGIC
# MAGIC **O problema.** Uma série mensal não define sozinha se houve degradação relevante. É preciso baseline, unidade, política e maturação do target.
# MAGIC
# MAGIC **O que este helper faz.** Mantém histórico em memória, compara deterioração com thresholds e devolve **candidato a investigação**. Ele não agenda monitoramento, não persiste a série e não autoriza retreino automático.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico; cálculo local |
# MAGIC | Bibliotecas | pandas para a fixture; Plotly apenas se usar timeline |
# MAGIC | Dados | sintéticos |
# MAGIC | Escrita | nenhuma |
# MAGIC | Diferença Free × trabalho | nenhuma dependência de API do workspace nesta demonstração |

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
for k, v in EXAMPLE_THRESHOLDS.items(): print(f"  {k:20} {v}")
monitor = PerformanceMonitor(baseline_metrics={"auc": 0.78}, model_name="exemplo_propensao", policy=EXAMPLE_THRESHOLDS)

# COMMAND ----------
# MAGIC %md
# MAGIC `EXAMPLE_THRESHOLDS` é compatibilidade/exemplo. Calibre por modelo, escala, população, tamanho amostral e custo de falso alerta. AUC/Gini usam delta absoluto no exemplo; RMSE/MAPE usam delta relativo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Uma série com degradação no fim

# COMMAND ----------
meses = pd.date_range("2026-01-01", periods=8, freq="MS")
aucs = [0.78, 0.77, 0.79, 0.76, 0.77, 0.71, 0.66, 0.61]
for mes, auc in zip(meses, aucs): monitor.add_period(period=str(mes.date()), metrics={"auc": auc})
print(monitor.generate_report())
print()
print(f"status atual: {monitor.get_current_status()}")
print(f"decisão de retreino: {monitor.should_retrain()}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O nome `should_retrain()` é legado. Leia o dicionário: `automatic_retrain_authorized` permanece `False`. Um trigger significa investigar qualidade de dados/rótulo, drift, causa raiz e champion-challenger antes de qualquer decisão de implantação.
# MAGIC
# MAGIC A comparação é contra baseline e política, não simplesmente contra o mês anterior. A persistência é contada sobre períodos consecutivos amarelos/vermelhos conforme `consecutive_alert_periods`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - sem calibrar os thresholds;
# MAGIC - com target ainda não maturado;
# MAGIC - esperando persistência/scheduler/alerta externo;
# MAGIC - como gatilho automático de retreino.
# MAGIC
# MAGIC ### Integração com `metrics_report`
# MAGIC `metrics_report` devolve `auc_roc`, enquanto a política de exemplo usa `auc`. Use `selecionar_metricas_do_relatorio` para traduzir e, quando necessário, `metricas_obrigatorias=["auc", "ks_pct"]`. `ks_pct` permanece em escala 0–100.
