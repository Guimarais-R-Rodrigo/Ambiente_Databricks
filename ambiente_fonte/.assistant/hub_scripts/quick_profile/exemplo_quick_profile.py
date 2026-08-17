# Databricks notebook source
# MAGIC %md
# MAGIC # `quick_profile` — o perfil, com a origem de cada número
# MAGIC
# MAGIC **O problema.** Perfilar uma tabela grande inteira custa caro, então
# MAGIC amostra-se. E aí o relatório mistura duas coisas que parecem iguais: a
# MAGIC contagem de nulos, que veio da tabela toda, e a cardinalidade, que veio de
# MAGIC 5% dela. Alguém lê "300 valores distintos" e planeja como se fossem 300.
# MAGIC
# MAGIC **O que este script faz.** Devolve cada estatística com o sufixo que diz de
# MAGIC onde ela veio: `_full_table` ou `_sample`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico. Em compute clássico o script usa cache; em serverless ele degrada sem cache, e o resultado é o mesmo |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | uma view temporária de sessão |
# MAGIC | Diferença Free × trabalho | `cache()` é bloqueado em serverless; o script tem guarda e não falha |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_scripts.quick_profile import quick_profile
from hub_snippets.testing import fixtures

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Perfil com fração declarada

# COMMAND ----------

import json

fixtures.base_tabular(n=2000, seed=42).createOrReplaceTempView("vw_exemplo_perfil")

# `sample_fraction` e `seed` são declarados, não sorteados: quem lê o relatório
# precisa saber que 25% foi escolha, e que outra execução com a mesma semente
# devolve exatamente a mesma amostra.
perfil = quick_profile("vw_exemplo_perfil", sample_fraction=0.25, seed=42)
print(json.dumps(
    {k: v for k, v in perfil.items() if not isinstance(v, (dict, list))},
    indent=2, ensure_ascii=False,
))

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O que os sufixos separam

# COMMAND ----------

print("--- da TABELA INTEIRA ---")
for item in perfil["null_summary_full_table"][:3]:
    print(f"  {item['column']:15} nulos: {item['null_count']:4}  ({item['null_pct']}%)")

print("\n--- da AMOSTRA ---")
print(f"  linhas na amostra   : {perfil['sample_rows']} de {perfil['total_rows']}")
print(f"  cardinalidade       : {perfil['cardinality_sample']}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Executado no laboratório:
# MAGIC
# MAGIC ```text
# MAGIC linhas na amostra   : 530 de 2000
# MAGIC cardinalidade       : {'id_cliente': 564, 'uf': 5}
# MAGIC ```
# MAGIC
# MAGIC Dois erros possíveis aqui, e o segundo é mais sutil que o primeiro.
# MAGIC
# MAGIC **O primeiro:** 564 não são os valores distintos da tabela, que tem 2.000
# MAGIC clientes únicos. É a cardinalidade **da amostra**, e reportá-la como se
# MAGIC fosse da tabela é o erro que a nomenclatura existe para evitar.
# MAGIC
# MAGIC **O segundo:** 564 é maior que as 530 linhas amostradas, o que é
# MAGIC aritmeticamente impossível para uma contagem exata. O script usa
# MAGIC `approx_count_distinct`, que troca precisão por custo e erra para mais ou
# MAGIC para menos. Se um número de cardinalidade precisa ser exato, esta não é a
# MAGIC ferramenta.
# MAGIC
# MAGIC Já `null_summary_full_table` foi calculado sobre tudo: contagem de nulos é
# MAGIC barata e não faz sentido estimar.
# MAGIC
# MAGIC O erro de interpretação mais provável aqui não é confundir os dois sufixos —
# MAGIC é **não reparar que existem**. Ao copiar um número deste dicionário para um
# MAGIC relatório, o sufixo costuma ficar para trás.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Com fração 1.0 os dois coincidem — e é aí que se engana

# COMMAND ----------

perfil_completo = quick_profile("vw_exemplo_perfil", sample_fraction=1.0, seed=42)
print(f"fração declarada    : {perfil_completo['sample_fraction']}")
print(f"linhas na amostra   : {perfil_completo['sample_rows']} de {perfil_completo['total_rows']}")
print(f"cardinalidade       : {perfil_completo['cardinality_sample']}")
print(f"\ndemais chaves do retorno: {sorted(perfil_completo)}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Com fração 1.0 os sufixos deixam de distinguir coisa alguma, e
# MAGIC o relatório fica indistinguível de um perfil completo. Quem se acostuma a
# MAGIC rodar assim em tabela pequena e depois aplica em tabela grande com fração
# MAGIC menor carrega a leitura antiga junto.
# MAGIC
# MAGIC Por isso a fração aparece na saída: ela é a primeira coisa a conferir num
# MAGIC relatório que alguém te mandou.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este script
# MAGIC
# MAGIC - **Para estatística que precisa ser exata.** Amostra é amostra. Se a
# MAGIC   decisão depende do número preciso, use fração 1.0 e aceite o custo.
# MAGIC - **Esperando cardinalidade exata.** Dois efeitos se somam e vão em
# MAGIC   direções opostas: a amostra **subestima** o número de categorias raras, e o
# MAGIC   `approx_count_distinct` erra para os dois lados. O resultado é uma
# MAGIC   estimativa, não uma contagem.
# MAGIC - **Como substituto de EDA.** Ele descreve schema e distribuição. Não avalia
# MAGIC   se a tabela serve para a pergunta, que é o trabalho da skill de EDA.
# MAGIC - **Sem declarar a semente**, se o resultado for para um relatório: sem
# MAGIC   `seed`, duas execuções dão números diferentes e ninguém sabe se a
# MAGIC   diferença é do dado ou do sorteio.
