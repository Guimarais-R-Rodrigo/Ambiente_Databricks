# Databricks notebook source
# MAGIC %md
# MAGIC # `checar_base_campanha` — o que conferir antes de confiar num número
# MAGIC
# MAGIC **O problema.** Alguém aponta uma tabela nova e pede a taxa de resposta.
# MAGIC O cálculo sai em trinta segundos e parece certo. Se a chave estiver
# MAGIC duplicada, a taxa passa a pesar quem aparece mais vezes; se houver nulo na
# MAGIC coluna de resposta, a taxa cai sem que nada avise. Os dois erros produzem
# MAGIC um número plausível.
# MAGIC
# MAGIC **O que este script faz.** Roda antes da medição e devolve um veredito
# MAGIC legível sobre o que precisa de decisão humana.
# MAGIC
# MAGIC > Exemplo dos **padrões do Hub**, não script de produção.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | lê `workspace.default.hub_exemplo_campanha`, criada pelo exemplo de snippet |
# MAGIC | Escrita | cria uma tabela temporária de demonstração; nada mais |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_padroes.script.checar_base_campanha import LIMITES_PADRAO, checar_base_campanha

print(f"limites padrão: {LIMITES_PADRAO}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Base saudável — e o alerta que ainda assim aparece

# COMMAND ----------

import json

diagnostico = checar_base_campanha("workspace.default.hub_exemplo_campanha")
print(json.dumps(diagnostico, indent=2, ensure_ascii=False))

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC limites padrão: {'pct_nulo_alerta': 1.0, 'min_contatos_por_segmento': 100}
# MAGIC {
# MAGIC   "tabela": "workspace.default.hub_exemplo_campanha",
# MAGIC   "status": "warn",
# MAGIC   "checagens": {
# MAGIC     "linhas": 45868,
# MAGIC     "chaves_distintas": 45868,
# MAGIC     "resposta_nula": 0,
# MAGIC     "resposta_fora_dominio": 0,
# MAGIC     "segmentos_com_base_pequena": 1
# MAGIC   },
# MAGIC   "alertas": [
# MAGIC     {
# MAGIC       "checagem": "base_por_segmento",
# MAGIC       "severidade": "warn",
# MAGIC       "mensagem": "segmento 'Private' tem 28 contatos, abaixo de 100:
# MAGIC                    reporte a taxa, não aloque orçamento por ela."
# MAGIC     }
# MAGIC   ]
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O status sai `warn`, não `pass`, e isso é o comportamento
# MAGIC certo: a chave é única e a resposta está no domínio, mas um segmento tem
# MAGIC 28 contatos — abaixo do mínimo para sustentar decisão.
# MAGIC
# MAGIC Repare que o script **não remove** esse segmento nem o esconde. Ele
# MAGIC informa e devolve a decisão a quem analisa. Helper que filtra sozinho
# MAGIC produz relatório limpo e conclusão errada.
# MAGIC
# MAGIC O erro de leitura mais provável aqui: tratar `warn` como "pode ignorar".
# MAGIC O limite de 100 contatos é **política local**, está em `LIMITES_PADRAO`
# MAGIC para ser visível, e uma campanha com muitos segmentos pequenos por desenho
# MAGIC precisa de outro limite — não de silêncio.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Base com chave duplicada — o erro que passa despercebido

# COMMAND ----------

from pyspark.sql import functions as F

# Duplica 5% das linhas: é o que acontece quando um join anterior expandiu a base
# sem ninguém notar. A taxa continua saindo, e continua errada.
base = spark.table("workspace.default.hub_exemplo_campanha")
duplicada = base.unionByName(base.sample(0.05, seed=42))
duplicada.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_campanha_dup")

diagnostico_dup = checar_base_campanha("workspace.default.hub_exemplo_campanha_dup")
print(f"status: {diagnostico_dup['status']}")
for alerta in diagnostico_dup["alertas"]:
    if alerta["severidade"] == "fail":
        print(f"  [{alerta['checagem']}] {alerta['mensagem']}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o caso que **falha**:
# MAGIC
# MAGIC ```text
# MAGIC status: fail
# MAGIC   [grao] id_cliente não é único: 48206 linhas para 45868 chaves.
# MAGIC          A taxa passa a pesar quem aparece mais vezes.
# MAGIC
# MAGIC original    45868 linhas | taxa 4.7%
# MAGIC duplicada   48192 linhas | taxa 4.746%
# MAGIC ```
# MAGIC
# MAGIC **A diferença de 0,046 ponto percentual é o ponto.** Ela é pequena demais
# MAGIC para parecer defeito num relatório e grande o bastante para mudar uma
# MAGIC decisão de orçamento — e é por isso que o script **reprova** em vez de
# MAGIC avisar. Duplicata na chave não é ruído: é a taxa passando a pesar quem
# MAGIC aparece mais vezes.

# COMMAND ----------

# O tamanho do estrago, medido: a taxa muda sem que nada no cálculo acuse.
for nome, df in [("original", base), ("duplicada", duplicada)]:
    taxa = df.agg(F.round(100 * F.avg("respondeu"), 3)).first()[0]
    print(f"{nome:10} {df.count():6} linhas | taxa {taxa}%")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A diferença na taxa é pequena — décimos de ponto — e é
# MAGIC exatamente isso que torna o erro perigoso: nada parece anormal. Numa base
# MAGIC onde a duplicação atinge um segmento em particular, o efeito se concentra
# MAGIC e a comparação entre segmentos deixa de valer.
# MAGIC
# MAGIC O script pega isso comparando `count(*)` com `count(distinct chave)`, que é
# MAGIC a verificação mais barata que existe e a que mais gente pula.

# COMMAND ----------

# Limpeza: a tabela de demonstração não precisa sobreviver ao notebook.
spark.sql("DROP TABLE IF EXISTS workspace.default.hub_exemplo_campanha_dup")
print("tabela de demonstração removida")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este script
# MAGIC
# MAGIC - **Como garantia de qualidade.** Ele confere grão, domínio e base mínima.
# MAGIC   Não olha viés de seleção, não sabe se a campanha atingiu quem deveria, e
# MAGIC   não substitui Lakeflow expectations num pipeline.
# MAGIC - **Em tabela muito grande, sem avaliar custo.** São três varreduras
# MAGIC   agregadas; barato em milhões de linhas, não em bilhões.
# MAGIC - **Como bloqueio automático.** `fail` é sinal para uma pessoa decidir,
# MAGIC   não para um job abortar. A decisão sobre nulo ambíguo é de negócio.
