# Databricks notebook source
# MAGIC %md
# MAGIC # `umap_viz` — ver grupos em duas dimensões sem acreditar demais no desenho
# MAGIC
# MAGIC **O problema.** Cluster em espaço de 30 variáveis não se enxerga, e PCA achata a estrutura local: dois grupos vizinhos mas separados viram uma mancha só. Sem ver, a discussão sobre segmentação vira opinião.
# MAGIC
# MAGIC **O que este helper faz.** Projeta em 2D preservando vizinhança local com UMAP, e desenha os clusters com a identidade visual do Hub.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `umap-learn (com pin de versão)` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação leva ~3 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install "umap-learn==0.5.5"

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

from hub_snippets.ml.umap_viz import compute_umap, plot_umap_clusters

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
# MAGIC ## 1. Três grupos plantados em dez dimensões

# COMMAND ----------

from sklearn.preprocessing import StandardScaler

n_por_grupo = 300
centros = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
], dtype=float)
X = np.vstack([c + rng.normal(0, 1.0, (n_por_grupo, 10)) for c in centros])
rotulos = np.repeat([0, 1, 2], n_por_grupo)

# padronizar ANTES de projetar: sem isso a escala vira a estrutura
X_escalado = StandardScaler().fit_transform(X)
print(f"base {X.shape} | grupos {np.bincount(rotulos).tolist()}")

# COMMAND ----------

projecao = compute_umap(X_escalado, n_components=2, n_neighbors=15, min_dist=0.1)
print(f"projecao: {projecao.shape}")
print(f"amplitude eixo 1: {projecao[:, 0].min():.2f} a {projecao[:, 0].max():.2f}")
print(f"amplitude eixo 2: {projecao[:, 1].min():.2f} a {projecao[:, 1].max():.2f}")

# COMMAND ----------

figura = plot_umap_clusters(
    X_escalado, rotulos, title="Tres grupos plantados, projetados em 2D",
    cluster_names=["base", "alta renda", "alto uso"],
)
figura.show()

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC base (900, 10) | grupos [300, 300, 300]
# MAGIC projecao: (900, 2)
# MAGIC amplitude eixo 1: -3.62 a 9.42
# MAGIC amplitude eixo 2: 0.31 a 8.69
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Dez dimensões viraram duas, e os três grupos aparecem separados
# MAGIC no gráfico. Como plantamos os centros, sabemos que a separação é real.
# MAGIC
# MAGIC Agora o aviso que precisa vir junto do desenho: **os eixos não têm
# MAGIC unidade**. "−3,62 a 9,42" não significa nada — não é renda, não é
# MAGIC desvio-padrão, não é distância. Não são nem comparáveis entre si, e mudam a
# MAGIC cada execução com semente diferente.
# MAGIC
# MAGIC Consequência direta: **a distância entre dois grupos no gráfico não é
# MAGIC proporcional à distância real entre eles.** UMAP preserva vizinhança local
# MAGIC e trata a estrutura global com liberdade. Dois grupos desenhados lado a
# MAGIC lado podem estar mais distantes que dois nos cantos opostos.
# MAGIC
# MAGIC O uso legítimo é responder "existem grupos distintos aqui?" — e para isso
# MAGIC ele é excelente. O uso ilegítimo, e frequente, é medir no gráfico e
# MAGIC concluir que "o segmento A está mais próximo do B do que do C".

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Para medir distância.** A distância no gráfico UMAP **não** é proporcional à distância real. Grupos próximos no desenho podem estar longe.
# MAGIC - **Como método de clusterização.** Ele projeta; quem agrupa é o k-means ou o HDBSCAN. Rodar cluster *sobre* a projeção inventa separação.
# MAGIC - **Sem padronizar antes.** Variável em reais domina variável em anos, e a projeção vira um gráfico de renda.
# MAGIC - **Sem `random_state`.** Duas execuções produzem desenhos diferentes, e a reunião seguinte discute o desenho.
