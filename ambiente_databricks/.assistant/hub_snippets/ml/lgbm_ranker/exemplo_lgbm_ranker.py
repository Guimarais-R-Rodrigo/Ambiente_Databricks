# Databricks notebook source
# MAGIC %md
# MAGIC # `lgbm_ranker` — ordenar dentro do grupo, não classificar a linha
# MAGIC
# MAGIC **O problema.** Recomendar produto para cliente não é decidir se cada par é bom — é ordenar as opções **daquele cliente**. Um classificador otimiza o acerto médio global e pode acertar muito sem nunca pôr a melhor opção em primeiro.
# MAGIC
# MAGIC **O que este helper faz.** Treina LambdaRank com grupos declarados e avalia com NDCG. Nesta versão, MAP não é calculado pelo helper.

# MAGIC
# MAGIC **Guia local completo:** [README deste modelo](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `lightgbm` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação e a execução levam ~1 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install lightgbm

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

from hub_snippets.ml.lgbm_ranker import evaluate_ranking, train_lgbm_ranker

# COMMAND ----------
# MAGIC %md
# MAGIC Este exemplo passa log_mlflow=False para desativar apenas o registro explícito do helper. Antes de habilitar tracking, confirme dependência, experimento, permissões, configuração do runtime e autologging da sessão. Uma falha numa configuração de serverless não determina o suporte em outras configurações.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Um painel de consultas com relevância graduada

# COMMAND ----------

n_grupos, por_grupo = 400, 10
X, y, grupos = [], [], []
for _ in range(n_grupos):
    feats = rng.normal(0, 1, (por_grupo, 5))
    # relevancia de 0 a 3, dirigida pelas duas primeiras features
    escore = 1.5 * feats[:, 0] + 0.8 * feats[:, 1] + rng.normal(0, 0.5, por_grupo)
    rel = np.clip(np.digitize(escore, [-0.5, 0.5, 1.5]), 0, 3)
    X.append(feats)
    y.append(rel)
    grupos.append(por_grupo)
X = np.vstack(X)
y = np.concatenate(y)
grupos = np.array(grupos)

corte_g = 300
corte_l = corte_g * por_grupo
X_tr, y_tr, g_tr = X[:corte_l], y[:corte_l], grupos[:corte_g]
X_va, y_va, g_va = X[corte_l:], y[corte_l:], grupos[corte_g:]
distintos, contagens = np.unique(y, return_counts=True)
print(f"{n_grupos} grupos de {por_grupo} | relevancias: {dict(zip(distintos.tolist(), contagens.tolist()))}")

# COMMAND ----------

modelo, metricas = train_lgbm_ranker(
    X_tr, y_tr, g_tr, X_va, y_va, g_va, num_boost_round=80, log_mlflow=False,
)
for chave, valor in metricas.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------

avaliacao = evaluate_ranking(modelo, X_va, y_va, g_va, ks=[1, 3, 5])
for chave, valor in avaliacao.items():
    print(f"  {chave:24s} {valor:.4f}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC 400 grupos de 10 | relevancias: {0: 1549, 1: 875, 2: 755, 3: 821}
# MAGIC
# MAGIC ndcg_at_1                0.9548
# MAGIC ndcg_at_3                0.9543
# MAGIC ndcg_at_5                0.9634
# MAGIC ndcg_at_10               0.9764
# MAGIC ```
# MAGIC
# MAGIC **Como ler — e o erro de leitura mais caro está aqui.** `ndcg_at_1` de
# MAGIC **0,9548** **não** quer dizer "acertamos a primeira posição em 95% dos
# MAGIC grupos". NDCG@1 é uma **razão de ganho**:
# MAGIC
# MAGIC ```text
# MAGIC NDCG@1 = (2^relevância_do_topo − 1) / (2^melhor_relevância_do_grupo − 1)
# MAGIC ```
# MAGIC
# MAGIC Com a escala de relevância deste notebook (0 a 3), um ranker que **nunca**
# MAGIC acerta o topo — põe sempre um item de relevância 2 onde havia um de 3 —
# MAGIC ainda tira **0,4286**. E a taxa de acerto que corresponde a 0,9548 é de
# MAGIC cerca de **92%**, não 95%.
# MAGIC
# MAGIC Levado a uma reunião como "acertamos a oferta em 95% dos casos", é um
# MAGIC número inflado que ninguém na sala tem como conferir. **Se a pergunta é
# MAGIC taxa de acerto, meça taxa de acerto** — `hit-rate@1` é uma linha de código
# MAGIC e não se confunde com nada.
# MAGIC
# MAGIC Sobre a série 0,9548 → 0,9543 → 0,9634 → 0,9764: repare que ela **desce**
# MAGIC de @1 para @3 antes de subir. NDCG@k **não é monotônico em k**, e a
# MAGIC intuição de que "k maior dá número maior" já falha na primeira transição
# MAGIC desta tabela. A tendência geral de alta existe — com 10 posições em grupos
# MAGIC de 10, basta ordenar aproximadamente certo —, mas não é uma regra.
# MAGIC **Comparar modelos com k diferentes não diz nada.**

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem grupos.** Sem `groups`, ele vira classificador com nome bonito; a ordenação relativa é o ponto inteiro.
# MAGIC - **Com grupo de tamanho 1.** Não há o que ordenar; a linha só adiciona ruído ao gradiente.
# MAGIC - **Para prever probabilidade.** A saída é score de ordenação, não probabilidade calibrada — não a interprete como chance.
