# Databricks notebook source
# MAGIC %md
# MAGIC # `kaplan_meier` — quanto tempo até acontecer, com quem ainda não aconteceu
# MAGIC
# MAGIC **O problema.** Perguntar *quantos* clientes cancelaram joga fora a informação de **quando**, e trata quem entrou ontem como quem está há três anos. Pior: quem ainda não cancelou não é caso negativo — é caso **censurado**, e descartá-lo enviesa tudo.
# MAGIC
# MAGIC **O que este helper faz.** Estima a curva de sobrevivência de Kaplan-Meier, que usa a informação parcial de quem ainda não teve o evento, e compara grupos com log-rank.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | **instala `lifelines` na primeira célula** |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; `log_mlflow=False` em todas as chamadas |
# MAGIC | Diferença Free × trabalho | a instalação leva ~3 min no Free; no trabalho, confirme a política do workspace |

# COMMAND ----------
# MAGIC %pip install lifelines

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

from hub_snippets.ml.kaplan_meier import log_rank_test, plot_kaplan_meier

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
# MAGIC ## 1. Uma carteira com censura à direita

# COMMAND ----------

import pandas as pd

n = 800
grupo = rng.choice(["padrao", "premium"], n, p=[0.6, 0.4])
# premium demora mais para cancelar: escala maior na exponencial
escala = np.where(grupo == "premium", 30.0, 16.0)
tempo_ate_evento = rng.exponential(escala)
# a janela de observacao tem 24 meses: quem passa disso e CENSURADO
fim_observacao = 24.0
duracao = np.minimum(tempo_ate_evento, fim_observacao)
evento = (tempo_ate_evento <= fim_observacao).astype(int)

base = pd.DataFrame({"duracao": duracao.round(2), "evento": evento, "grupo": grupo})
print(f"contratos: {len(base)}")
print(f"eventos observados: {evento.sum()} ({100 * evento.mean():.1f}%)")
print(f"censurados a direita: {(1 - evento).sum()} ({100 * (1 - evento).mean():.1f}%)")
print(base.groupby("grupo")["evento"].agg(["count", "sum", "mean"]).round(3).to_string())

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC contratos: 800
# MAGIC eventos observados: 557 (69.6%)
# MAGIC censurados a direita: 243 (30.4%)
# MAGIC
# MAGIC          count  sum   mean
# MAGIC grupo
# MAGIC padrao     482  371  0.770
# MAGIC premium    318  186  0.585
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Trinta por cento da base é **censurada**: são contratos que
# MAGIC chegaram ao fim da janela de 24 meses sem cancelar. Eles não são "não
# MAGIC cancelou" — são "ainda não cancelou até onde eu vi", e a diferença é o
# MAGIC assunto inteiro deste notebook.
# MAGIC
# MAGIC A análise ingênua olharia a coluna `mean` e diria: padrão cancela 77%,
# MAGIC premium 58,5%. Mas essa conta trata o censurado como não-evento, o que
# MAGIC subestima a taxa real dos dois grupos — e subestima **mais** o grupo que
# MAGIC tem mais censura. Kaplan-Meier existe para usar a informação parcial em
# MAGIC vez de descartá-la.


# COMMAND ----------

figura = plot_kaplan_meier(base, duration_col="duracao", event_col="evento", group_col="grupo")
figura.show()

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** As duas curvas descem, e a do premium desce mais devagar. O que
# MAGIC vale reparar são os **degraus**: a curva só cai quando há evento, e fica
# MAGIC plana entre eles. As marcas de censura aparecem sem produzir queda — o
# MAGIC contrato sai do denominador sem contar como evento, que é exatamente o
# MAGIC tratamento correto.
# MAGIC
# MAGIC A faixa de confiança abre à direita. Não é defeito do desenho: no fim da
# MAGIC janela restam poucos contratos sob risco, e cada evento move muito a
# MAGIC estimativa. **A cauda da curva é a parte em que menos se deve confiar**, e
# MAGIC é justamente a que costuma ser citada na reunião.


# COMMAND ----------

teste = log_rank_test(base, duration_col="duracao", event_col="evento", group_col="grupo")
for chave, valor in teste.items():
    print(f"  {chave:24s} {valor}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC statistic                32.7339
# MAGIC p_value                  1.0568e-08
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O log-rank compara as curvas inteiras, não um ponto delas. Com
# MAGIC χ² de **32,73** e p de **1,06 × 10⁻⁸**, a diferença entre padrão e premium
# MAGIC não é acaso de amostra.
# MAGIC
# MAGIC O que o teste **não** diz: que ser premium *causa* a permanência. Quem
# MAGIC contrata premium é diferente de quem contrata padrão em várias dimensões, e
# MAGIC a curva não separa isso. Para estimar o efeito de uma variável mantendo as
# MAGIC outras constantes, o helper é `hub_snippets.ml.survival_cox`.
# MAGIC
# MAGIC E cuidado com o p tão pequeno: com 800 contratos ele reflete tanto a
# MAGIC diferença quanto o tamanho da amostra. Um p de 10⁻⁸ não significa efeito
# MAGIC oito vezes maior que um p de 0,05.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Com covariável contínua.** Kaplan-Meier compara grupos; para efeito de variável contínua, use Cox — está em `hub_snippets.ml.survival_cox`.
# MAGIC - **Com censura informativa.** O método assume que quem saiu da observação saiu por motivo alheio ao evento. Se o cliente some *porque* vai cancelar, a curva mente.
# MAGIC - **Comparando grupos de tamanhos muito diferentes.** O log-rank tem pouca potência quando um braço é pequeno; p alto vira "não sei", não "não há diferença".
