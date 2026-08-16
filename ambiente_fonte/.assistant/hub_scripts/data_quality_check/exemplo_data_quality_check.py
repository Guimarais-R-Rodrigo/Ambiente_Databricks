# Databricks notebook source
# MAGIC %md
# MAGIC # `data_quality_check` — o veredito antes da análise
# MAGIC
# MAGIC **O problema.** Alguém aponta uma tabela e pede um número. O número sai em
# MAGIC trinta segundos e parece certo. Se a chave estiver duplicada, toda média
# MAGIC passa a pesar quem aparece mais vezes; se a tabela estiver parada há três
# MAGIC meses, o número descreve um passado que ninguém checou. Os dois erros
# MAGIC produzem resultado plausível, e é isso que os torna caros.
# MAGIC
# MAGIC **O que este script faz.** Roda antes da análise e devolve um veredito
# MAGIC legível sobre unicidade da chave, taxa de nulos e atualidade.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | uma view temporária de sessão; nenhuma tabela é criada |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

# Preâmbulo do Hub: resolve o caminho da biblioteca pelo usuário logado.
import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_scripts.data_quality_check import DEFAULT_THRESHOLDS, data_quality_check
from hub_snippets.testing import fixtures

print(f"limites padrão: {DEFAULT_THRESHOLDS}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Uma base saudável — e por que ela reprova
# MAGIC
# MAGIC A fixture tem chave única e 4% de nulos em `renda`, dentro do limite. Ainda
# MAGIC assim o veredito não sai `pass`.

# COMMAND ----------

base = fixtures.base_tabular(n=500, seed=42, pct_nulos_renda=0.04)
base.createOrReplaceTempView("vw_exemplo_dq")

import json

resultado = data_quality_check("vw_exemplo_dq", ["id_cliente"], "dt_referencia")
print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O status sai `fail`, e **não por causa dos dados**: a chave é
# MAGIC única e os nulos estão dentro do limite. A reprovação vem do prazo de
# MAGIC atualização, comparado contra o padrão de dois dias — e a fixture gera datas
# MAGIC no primeiro semestre de 2026.
# MAGIC
# MAGIC Este é o ponto mais importante do helper: **`status: "fail"` não significa
# MAGIC dado ruim.** Significa que algo precisa de decisão humana antes de o número
# MAGIC valer. Uma tabela mensal reprovaria todo dia sob um limite de dois dias.
# MAGIC
# MAGIC O erro de leitura mais provável aqui é tratar `fail` como bloqueio
# MAGIC automático. Ajuste `thresholds` ao ritmo real da fonte **antes** de tratar o
# MAGIC resultado como alerta — e repare que a política aplicada volta na saída, em
# MAGIC `thresholds`, justamente para que ninguém precise abrir o código para saber
# MAGIC contra o que foi comparado.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A mesma base com limite ajustado ao ritmo da fonte

# COMMAND ----------

resultado_calibrado = data_quality_check(
    "vw_exemplo_dq",
    ["id_cliente"],
    "dt_referencia",
    thresholds={"null_warn": 5.0, "null_fail": 20.0, "freshness_days": 400},
)
print(f"status: {resultado_calibrado['status']}")
print(f"score : {resultado_calibrado['score']}")
for alerta in resultado_calibrado["alerts"]:
    print(f"  [{alerta['severity']}] {alerta['message']}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Com o limite ajustado, o mesmo dado passa. O `score` é
# MAGIC aritmética simples sobre o número de checks reprovados — serve para
# MAGIC acompanhar tendência entre execuções, não como nota absoluta de qualidade.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Chave duplicada — o erro que passa despercebido
# MAGIC
# MAGIC `n_entidades` menor que `n` faz a fixture repetir clientes, que é o que
# MAGIC acontece quando um join anterior expandiu a base sem ninguém notar.

# COMMAND ----------

from pyspark.sql import functions as F

duplicada = fixtures.base_tabular(n=500, seed=42, n_entidades=350)
duplicada.createOrReplaceTempView("vw_exemplo_dq_dup")

diag = data_quality_check("vw_exemplo_dq_dup", ["id_cliente"], "dt_referencia",
                          thresholds={"freshness_days": 400})
pk = diag["checks"]["pk_uniqueness"]
print(f"linhas             : {diag['checks']['row_count']}")
print(f"chaves duplicadas  : {pk['duplicate_rows']}  (status: {pk['status']})")

for nome, df in [("única", base), ("duplicada", duplicada)]:
    media = df.agg(F.round(F.avg("alvo"), 4)).first()[0]
    print(f"prevalência do alvo, base {nome:10}: {media}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A prevalência muda entre as duas bases, e a diferença é
# MAGIC pequena — décimos. É exatamente isso que torna o erro perigoso: nada parece
# MAGIC anormal. Numa base onde a duplicação atinge um segmento em particular, o
# MAGIC efeito se concentra e a comparação entre grupos deixa de valer.
# MAGIC
# MAGIC A verificação que pega isso é a mais barata que existe — comparar
# MAGIC `count(*)` com `count(distinct chave)` — e é a que mais gente pula.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este script
# MAGIC
# MAGIC - **Como garantia de qualidade.** Ele confere unicidade, nulos e atualidade.
# MAGIC   Não olha viés de seleção, não sabe se a tabela cobre a população certa, e
# MAGIC   não substitui Lakeflow expectations dentro de um pipeline.
# MAGIC - **Como bloqueio automático em job.** `fail` é sinal para uma pessoa
# MAGIC   decidir. O limite de atualidade é política local, não exigência da
# MAGIC   plataforma.
# MAGIC - **Em tabela muito grande, sem avaliar custo.** São varreduras agregadas:
# MAGIC   baratas em milhões de linhas, não em bilhões.
# MAGIC - **Para escolher entre duas tabelas.** O `score` compara execuções da
# MAGIC   mesma tabela ao longo do tempo; entre tabelas diferentes, com políticas
# MAGIC   diferentes, ele não significa nada.
