# Databricks notebook source
# MAGIC %md
# MAGIC # `schema_to_yaml` — o schema em texto, sem quebrar no acento
# MAGIC
# MAGIC **O problema.** Documentar o schema de uma tabela costuma virar cópia manual
# MAGIC de nomes e tipos para dentro de um README, que envelhece na primeira coluna
# MAGIC nova. Gerar o texto automaticamente resolve — desde que a geração escape
# MAGIC corretamente comentário com dois-pontos, aspas ou acento, senão o YAML sai
# MAGIC inválido e ninguém percebe até alguém tentar lê-lo.
# MAGIC
# MAGIC **O que este script faz.** Devolve o schema como dicionário serializável e
# MAGIC como YAML escapado, com estatísticas opcionais e limitadas.

# MAGIC
# MAGIC **Guia local completo:** [README deste script](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico |
# MAGIC | Bibliotecas | nenhuma além do runtime. **PyYAML é opcional**: sem ele o script devolve JSON, que é YAML 1.2 válido |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | uma view temporária de sessão |
# MAGIC | Diferença Free × trabalho | a presença do PyYAML pode variar; o retorno continua válido nos dois casos |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_scripts.schema_to_yaml import schema_to_dict, schema_to_yaml
from hub_snippets.testing import fixtures

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. O schema como dicionário

# COMMAND ----------

import json

fixtures.base_tabular(n=300, seed=42).createOrReplaceTempView("vw_exemplo_schema")

payload = schema_to_dict("vw_exemplo_schema")
print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC {
# MAGIC   "table": "vw_exemplo_schema",
# MAGIC   "columns": [
# MAGIC     {
# MAGIC       "name": "id_cliente",
# MAGIC       "type": "string",
# MAGIC       "nullable": true
# MAGIC     },
# MAGIC     {
# MAGIC       "name": "uf",
# MAGIC       "type": "string",
# MAGIC       "nullable": true
# MAGIC     },
# MAGIC     {
# MAGIC       "name": "renda",
# MAGIC       "type": "double",
# MAGIC       "nullable": true
# MAGIC     },
# MAGIC     {
# MAGIC       "name": "dt_referencia",
# MAGIC       "type": "date",
# MAGIC       "nullable": true
# MAGIC     },
# MAGIC     {
# MAGIC ...
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** O retorno é dicionário Python, serializável, e não texto — o
# MAGIC que permite compará-lo entre execuções, versioná-lo ou alimentar outra
# MAGIC ferramenta. A conversão para texto é a segunda função, e é opcional.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O mesmo schema como texto

# COMMAND ----------

texto = schema_to_yaml("vw_exemplo_schema")
print(texto[:600])
print("…" if len(texto) > 600 else "")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Por que o fallback para JSON não é um defeito

# MAGIC ```text
# MAGIC table: vw_exemplo_schema
# MAGIC columns:
# MAGIC - name: id_cliente
# MAGIC   type: string
# MAGIC   nullable: true
# MAGIC - name: uf
# MAGIC   type: string
# MAGIC   nullable: true
# MAGIC - name: renda
# MAGIC   type: double
# MAGIC   nullable: true
# MAGIC - name: dt_referencia
# MAGIC   type: date
# MAGIC   nullable: true
# MAGIC - name: alvo
# MAGIC   type: int
# MAGIC   nullable: true
# MAGIC ```
# MAGIC
# COMMAND ----------

try:
    import yaml  # noqa: F401
    print("PyYAML presente: a saída acima é YAML propriamente dito.")
except ImportError:
    print("PyYAML ausente: a saída acima é JSON.")

# JSON é subconjunto sintático de YAML 1.2 — qualquer leitor de YAML aceita.
print("\nJSON é YAML 1.2 válido, então quem consome não precisa saber qual dos")
print("dois veio. É essa propriedade que torna o fallback seguro em vez de")
print("degradado: nenhum consumidor quebra pela ausência da biblioteca.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Estatísticas são opcionais porque custam varredura

# MAGIC ```text
# MAGIC PyYAML presente: a saída acima é YAML propriamente dito.
# MAGIC
# MAGIC JSON é YAML 1.2 válido, então quem consome não precisa saber qual dos
# MAGIC dois veio. É essa propriedade que torna o fallback seguro em vez de
# MAGIC degradado: nenhum consumidor quebra pela ausência da biblioteca.
# MAGIC ```
# MAGIC
# COMMAND ----------

com_stats = schema_to_dict("vw_exemplo_schema", include_stats=True)
primeira = com_stats["columns"][0]
print("primeira coluna, com estatísticas:")
print(json.dumps(primeira, indent=2, ensure_ascii=False, default=str))

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC primeira coluna, com estatísticas:
# MAGIC {
# MAGIC   "name": "id_cliente",
# MAGIC   "type": "string",
# MAGIC   "nullable": true,
# MAGIC   "stats": {
# MAGIC     "approx_distinct": 311,
# MAGIC     "null_count": 0,
# MAGIC     "null_pct": 0.0
# MAGIC   }
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Sem `include_stats`, o script lê apenas metadados — é
# MAGIC instantâneo e não toca nos dados. Com ele, cada coluna exige agregação.
# MAGIC
# MAGIC O erro de interpretação mais provável: ligar `include_stats=True` por
# MAGIC hábito numa tabela grande e atribuir a lentidão ao Spark. O parâmetro é
# MAGIC opcional exatamente porque a diferença de custo é de ordens de grandeza.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este script
# MAGIC
# MAGIC - **Como catálogo de dados.** Ele descreve estrutura, não significado. O que
# MAGIC   cada coluna quer dizer, quem é dono e com que frequência atualiza são
# MAGIC   assunto do Unity Catalog e da governança, não deste texto.
# MAGIC - **Com `include_stats=True` em tabela grande, sem avaliar custo.**
# MAGIC - **Para detectar mudança de schema em produção.** Comparar dois retornos
# MAGIC   funciona como diagnóstico manual; monitoramento de schema pede mecanismo
# MAGIC   que rode sozinho e alerte.
# MAGIC - **Esperando que o YAML gerado seja o contrato.** Ele é uma fotografia. O
# MAGIC   contrato de uma tabela é o que está declarado no catálogo.
