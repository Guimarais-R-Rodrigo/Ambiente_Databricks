# Databricks notebook source
# MAGIC %md
# MAGIC # `train_xgboost` — o segundo baseline, para conferir o primeiro
# MAGIC
# MAGIC **O problema.** Comparar modelos sob o mesmo desenho ajuda a investigar sensibilidade à escolha do estimador. Resultados próximos, porém, não provam ausência de viés ou vazamento: os dois podem compartilhar o mesmo erro de preparação.
# MAGIC
# MAGIC **O que este helper faz.** Treina XGBoost com a mesma interface e as mesmas métricas do baseline LightGBM, para comparação direta.

# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas históricas abaixo foram preservadas; a revisão R02 não as transforma em execução recente.
# MAGIC
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | requer ambiente Python e pacotes compatíveis; confirmar o compute da execução |
# MAGIC | Bibliotecas | **instala `xgboost` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | sem escrita explícita de tabela; logging do helper desligado, mas verificar autologging da sessão |
# MAGIC | Diferença Free × trabalho | confirmar dependências, tracking e política de instalação; não há prazo universal de execução |

# COMMAND ----------
# MAGIC %pip install xgboost

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

from hub_snippets.ml.train_xgboost import DEFAULT_PARAMS, train_xgboost_baseline

# COMMAND ----------
# MAGIC %md
# MAGIC ## Por que `log_mlflow=False` em tudo
# MAGIC
# MAGIC Os treinadores registram no MLflow por padrão. Este exemplo desliga somente
# MAGIC o logging explícito do helper. Uma falha histórica de configuração de
# MAGIC tracking não comprova que MLflow seja indisponível em todo serverless Free.
# MAGIC
# MAGIC Confirme experimento, permissões, dependências e autologging da sessão antes
# MAGIC de ligar o registro. `log_mlflow=False` não desativa autologging previamente
# MAGIC configurado. Consulte o [README](README.md#11-limitações-riscos-e-armadilhas)
# MAGIC para o alcance do wrapper e as referências oficiais de tracking.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. A mesma base do baseline LightGBM

# COMMAND ----------

n = 6000
X = rng.normal(0, 1, (n, 8))
logito = 1.2 * X[:, 0] - 0.8 * X[:, 1] + 0.5 * X[:, 2] + rng.normal(0, 0.8, n)
y = (logito > 1.0).astype(int)

corte = 4500
X_tr, y_tr = X[:corte], y[:corte]
X_va, y_va = X[corte:], y[corte:]
print(f"treino {X_tr.shape} | validacao {X_va.shape} | prevalencia {y.mean():.3f}")

# COMMAND ----------

modelo, metricas = train_xgboost_baseline(X_tr, y_tr, X_va, y_va, task="binary", log_mlflow=False)
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC auc_val                  0.9302
# MAGIC gini_val                 0.8603
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O baseline LightGBM, sobre **a mesma base e a mesma partição**,
# MAGIC deu `auc_val` **0,9268**. O XGBoost dá **0,9302**. A diferença é de
# MAGIC **0,0034** — três milésimos e meio.
# MAGIC
# MAGIC Essa diferença descreve a execução histórica acima. Para escolher uma
# MAGIC biblioteca, avalie estabilidade, custo e relevância da diferença sob um
# MAGIC desenho apropriado. Uma partição não demonstra superioridade universal.
# MAGIC
# MAGIC Métricas próximas não excluem vazamento compartilhado; métricas diferentes
# MAGIC podem refletir configuração, implementação ou características do problema.
# MAGIC Não há regra geral de que uma feature nova sempre mude mais a métrica que
# MAGIC a troca de estimador. As saídas antigas foram preservadas, não recertificadas.


# COMMAND ----------

print("parametros padrao do XGBoost neste helper:")
for chave, valor in DEFAULT_PARAMS.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** `max_depth=6` limita a profundidade nesta configuração. Os
# MAGIC parâmetros de capacidade e crescimento das duas bibliotecas não têm uma
# MAGIC correspondência automática. Leia os defaults reais de cada helper e a
# MAGIC configuração usada; uma escolha do exemplo não define todos os modos
# MAGIC possíveis de crescimento de uma biblioteca.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Para declarar um vencedor universal a partir desta partição.** Avalie estabilidade e adequação operacional.
# MAGIC - **Com categorias sem preparação compatível.** Confira as opções realmente suportadas pelo wrapper e compare alternativas sob o mesmo desenho.
# MAGIC - **Sem registrar fontes, partição e configuração.** A semente ajuda a repetir um experimento, mas não torna diferentes bibliotecas idênticas nem substitui validação.
