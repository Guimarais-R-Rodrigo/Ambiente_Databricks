# Databricks notebook source
# MAGIC %md
# MAGIC # `metrics_report` — métricas sob uma população e um threshold declarados
# MAGIC
# MAGIC **Guia local completo:** [README.md](README.md)
# MAGIC
# MAGIC **O problema.** Uma métrica isolada não define qualidade de modelo. Em classificação desbalanceada, acurácia pode ser pouco informativa; métricas hard dependem do threshold e métricas de ranking/calibração respondem outras perguntas.
# MAGIC
# MAGIC **O que este helper faz.** Devolve dez métricas binárias e quatro métricas de regressão. `ks_pct` usa escala 0–100; `auc_pr` é Average Precision.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico; cálculo local no driver |
# MAGIC | Bibliotecas | NumPy, SciPy e scikit-learn disponíveis |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma |
# MAGIC | Diferença Free × trabalho | revalide versões do runtime |

# COMMAND ----------
import sys
usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")
import numpy as np
rng = np.random.default_rng(42)
from hub_snippets.ml.metrics_report import calculate_binary_metrics

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base desbalanceada

# COMMAND ----------
n = 5000
y = (rng.random(n) < 0.05).astype(int)
p = np.clip(0.03 + 0.35 * y + rng.normal(0, 0.10, n), 0.001, 0.999)
m = calculate_binary_metrics(y, p)
for k, v in m.items():
    print(f"  {k:24} {v}")

# COMMAND ----------
# MAGIC %md
# MAGIC O bloco histórico desta fixture mostra prevalência próxima de 5%, AUC/KS altos e recall baixo no threshold 0,5. Leia `ks_pct=92.1` como **92,1 pontos percentuais**, não 0,921. A ausência de acurácia é parte da API atual, mas não transforma qualquer outra métrica em decisão suficiente.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O threshold é uma escolha

# COMMAND ----------
for corte in (0.10, 0.30, 0.50, 0.70):
    r = calculate_binary_metrics(y, p, threshold=corte)
    print(f"  limiar {corte:.2f} -> precisão {r['precision']:.3f} | "
          f"recall {r['recall']:.3f} | f1 {r['f1']:.3f}")

# COMMAND ----------
# MAGIC %md
# MAGIC F1, precisão e recall mudam com o corte. AUC ROC, Gini, Average Precision e Brier usam os scores/probabilidades sem esse threshold. Comparações entre modelos precisam manter população, target, horizonte e protocolo de avaliação comparáveis; usar o mesmo threshold é necessário apenas para comparar as métricas hard sob a mesma regra operacional.
# MAGIC
# MAGIC Para regressão, consulte o guia: MAPE exclui observações cujo `y_true` é zero e devolve `NaN` quando todos os valores reais são zero.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - sobre DataFrame Spark sem coleta/amostra consciente;
# MAGIC - como escolha automática de threshold;
# MAGIC - como prova de ausência de leakage ou de calibração;
# MAGIC - comparando números produzidos em populações/protocolos incompatíveis.
