# Databricks notebook source
# MAGIC %md
# MAGIC # `isolation_forest` — contaminação é premissa, não descoberta
# MAGIC
# MAGIC **O problema.** O modelo ordena observações pelos padrões aprendidos nos dados. `contamination` numérico calibra o corte usado para rotulá-las; não descobre sozinho a prevalência real de anomalias. Empates e discretização podem impedir que a fração marcada seja exatamente a informada.
# MAGIC
# MAGIC **O que este helper faz.** Treina Isolation Forest e oferece uma função separada de perfil. Este notebook exercita o treinamento e a mudança do corte, mas não chama `profile_anomalies`.

# MAGIC Leia o README do objeto antes de executar. As saídas ilustram a fixture; não medem eficácia em produção e não garantem os mesmos valores em outro ambiente.
# MAGIC
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | execução local em pandas/scikit-learn; conferir pacotes e memória do ambiente |
# MAGIC | Bibliotecas | NumPy, pandas, scikit-learn e MLflow; o import de MLflow é obrigatório mesmo com `log_mlflow=False` |
# MAGIC | Dados | sintéticos, gerados aqui — o módulo opera **driver-side** |
# MAGIC | Escrita | sem tabela persistente; chamadas desabilitam logging explícito do helper; conferir autologging externo |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

from hub_snippets.ml.isolation_forest import profile_anomalies, train_isolation_forest

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base com 1% de pontos realmente estranhos

# COMMAND ----------

normal = rng.normal(0, 1, size=(2970, 3))
estranhos = rng.normal(7, 0.5, size=(30, 3))
base = pd.DataFrame(np.vstack([normal, estranhos]), columns=["a", "b", "c"])
base["eh_estranho"] = [0] * 2970 + [1] * 30
print(f"{len(base)} linhas | estranhos plantados: {int(base.eh_estranho.sum())} (1,0%)")

# COMMAND ----------

saida = train_isolation_forest(
    base, feature_cols=["a", "b", "c"], contamination=0.01, log_mlflow=False,
)
labels = saida["labels"] if isinstance(saida, dict) else saida[1]
detectados = int((np.asarray(labels) == -1).sum())
print(f"marcados como anomalia: {detectados}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC 3000 linhas | estranhos plantados: 30 (1,0%)
# MAGIC   contamination=0.01 ->  30 marcados, 30 deles realmente estranhos
# MAGIC   contamination=0.05 -> 150 marcados, 30 deles realmente estranhos
# MAGIC   contamination=0.10 -> 300 marcados, 30 deles realmente estranhos
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Nesta execução histórica, o número marcado acompanhou a fração
# MAGIC informada. A fixture contém grupos artificialmente bem separados; acertar
# MAGIC esse cenário não demonstra desempenho em uma população real. A seleção e
# MAGIC a ordenação dos pontos dependem dos dados, além da escolha do corte.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A mesma base, com a premissa errada

# COMMAND ----------

for c in (0.01, 0.05, 0.10):
    s = train_isolation_forest(base, feature_cols=["a", "b", "c"],
                               contamination=c, log_mlflow=False)
    lab = np.asarray(s["labels"] if isinstance(s, dict) else s[1])
    marcados = int((lab == -1).sum())
    acertos = int(((lab == -1) & (base.eh_estranho == 1)).sum())
    print(f"  contamination={c:.2f} -> {marcados:3} marcados, "
          f"{acertos} deles realmente estranhos")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Com a fração de 10%, a saída histórica marca mais observações
# MAGIC normais da fixture. Isso ensina a separar a ordenação estatística da regra
# MAGIC que transforma scores em rótulos.
# MAGIC
# MAGIC Justifique o corte por evidência ou por um objetivo operacional declarado,
# MAGIC como capacidade de investigação; não apresente uma política operacional
# MAGIC como estimativa da prevalência verdadeira. Examine sensibilidade e falsos
# MAGIC positivos com evidência adicional. Avalie também os casos não marcados;
# MAGIC os números desta fixture não estimam a prevalência verdadeira.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem justificar a regra de corte.** Ela não é uma descoberta automática da frequência real de anomalias.
# MAGIC - **Como detector de fraude homologado.** Anomalia estatística não comprova fraude; a relação exige investigação.
# MAGIC - **Pressupondo que padronização seja exigência universal de árvores de isolamento.** Este wrapper a oferece; não confunda default com pressuposto do método.
# MAGIC - **Como verdade de referência sem validação.** Pseudorrótulos reproduzem escolhas do detector e não equivalem a rótulos observados independentemente.
