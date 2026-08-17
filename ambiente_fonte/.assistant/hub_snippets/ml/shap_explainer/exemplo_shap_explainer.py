# Databricks notebook source
# MAGIC %md
# MAGIC # `shap_explainer` — por que este cliente, e não só quais variáveis importam
# MAGIC
# MAGIC **O problema.** Importância de variável de árvore responde "quantas vezes o modelo usou isso", que não é o que o negócio pergunta. E não responde de jeito nenhum a pergunta que chega do atendimento: *por que este cliente foi recusado?*
# MAGIC
# MAGIC **O que este helper faz.** Calcula valores SHAP — contribuição por linha e por variável — e resume em importância global comparável.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `shap (com pin de versão)` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma — este módulo não registra em lugar nenhum |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~1 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install "shap==0.44.1"

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

from hub_snippets.ml.shap_explainer import compute_shap, get_feature_importance_shap


# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Um modelo com sinal conhecido, para conferir a explicação

# COMMAND ----------

from sklearn.ensemble import RandomForestClassifier

n = 3000
nomes = ["uso_limite", "renda", "atraso_medio", "tempo_relacao", "ruido"]
X = rng.normal(0, 1, (n, 5))
# construimos o sinal: uso_limite pesa o dobro de renda, e ruido nao entra
logito = 1.4 * X[:, 0] - 0.7 * X[:, 1] + 0.4 * X[:, 2] + rng.normal(0, 0.6, n)
y = (logito > 0.8).astype(int)

modelo = RandomForestClassifier(n_estimators=60, max_depth=6, random_state=42).fit(X, y)
print(f"base {X.shape} | prevalencia {y.mean():.3f} | acuracia treino {modelo.score(X, y):.3f}")

# COMMAND ----------

# ATENCAO ao que `max_samples` NAO faz: ele so tem efeito no ramo
# `model_type="kernel"`. Com `model_type="tree"`, como aqui, o TreeSHAP roda
# sobre a BASE INTEIRA — as 3.000 linhas. O parametro fica inerte, e passa-lo
# nao limita custo nenhum.
#
# `output_index` NAO e opcional aqui, e a recusa e deliberada: um classificador
# binario de arvore devolve SHAP para as duas classes, e explicar "a classe 0"
# quando se queria a 1 inverte todo o sinal sem erro nenhum. O modulo se recusa
# a escolher por voce — 1 e a classe positiva.
valores_shap, valor_base = compute_shap(
    modelo, X, feature_names=nomes, model_type="tree", output_index=1,
)
print(f"forma dos valores SHAP: {np.asarray(valores_shap).shape}")
print(f"valor base (previsao media): {valor_base:.4f}")

# COMMAND ----------

importancia = get_feature_importance_shap(valores_shap, feature_names=nomes)
print(importancia.to_string(index=False))

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC base (3000, 5) | prevalencia 0.316 | acuracia treino 0.918
# MAGIC SHAP calculado: 3000 observações × 5 features
# MAGIC   Base value (E[f(x)]): 0.3168
# MAGIC   Mean |SHAP| top-5: {'uso_limite': 0.2546, 'renda': 0.0988,
# MAGIC                       'atraso_medio': 0.0447, 'tempo_relacao': 0.0053,
# MAGIC                       'ruido': 0.0049}
# MAGIC forma dos valores SHAP: (3000, 5)
# MAGIC valor base (previsao media): 0.3168
# MAGIC
# MAGIC  rank       feature  mean_abs_shap  pct_importance  cumulative_pct
# MAGIC     1    uso_limite       0.254587       62.344765       62.344765
# MAGIC     2         renda       0.098828       24.201638       86.546403
# MAGIC     3  atraso_medio       0.044698       10.945951       97.492353
# MAGIC     4 tempo_relacao       0.005336        1.306725       98.799079
# MAGIC     5         ruido       0.004904        1.200921      100.000000
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Construímos o sinal com pesos 1,4 / −0,7 / 0,4 para as três
# MAGIC primeiras variáveis, e zero para as duas últimas. O SHAP devolve
# MAGIC **62,3% / 24,2% / 10,9%** — a mesma ordem e proporções próximas. A
# MAGIC explicação recuperou o que plantamos, o que é a única forma de verificar
# MAGIC um método de explicabilidade.
# MAGIC
# MAGIC **O detalhe que ensina mais está no fim da lista.** `ruido` não entra no
# MAGIC sinal e mesmo assim recebe **1,2%** — não zero. Nenhuma variável recebe
# MAGIC zero: o modelo usa qualquer coluna para dividir alguma folha em algum
# MAGIC lugar, e o SHAP atribui essa contribuição honestamente.
# MAGIC
# MAGIC A leitura prática: **importância pequena e não nula é a assinatura de
# MAGIC "não tem sinal"**, e a linha de corte é sua, não do método. Quem ordena a
# MAGIC tabela e pega o top-10 sempre acha dez variáveis importantes, inclusive
# MAGIC numa base de puro ruído.
# MAGIC
# MAGIC O `valor base` de **0,3168** é a previsão média — igual à prevalência,
# MAGIC como se espera. Todo valor SHAP é uma partida desse ponto.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como prova de causalidade.** SHAP explica a **previsão do modelo**, não o fenômeno. "Reduzir o uso do limite reduz a inadimplência" não se conclui daqui.
# MAGIC - **Sobre a base inteira, esperando que `max_samples` proteja.** Ele só age em `model_type="kernel"`. Em `"tree"`, o cálculo roda sobre tudo — amostre você mesmo antes de chamar.
# MAGIC - **Com features correlacionadas, sem ressalva.** A contribuição se divide entre elas de um jeito que depende do algoritmo, e a leitura individual fica instável.
