# Databricks notebook source
# MAGIC %md
# MAGIC # `naming_checker` — política local, não lei da plataforma
# MAGIC
# MAGIC **O problema.** Convenções de nomenclatura circulam como se fossem exigência
# MAGIC do Databricks. Não são: o Unity Catalog não pede `dim_`, não pede `fato_` e
# MAGIC não se importa com `snake_case`. Quando um checador apresenta política da
# MAGIC casa como regra da plataforma, ele para de ser discutível — e convenção que
# MAGIC não pode ser discutida vira burocracia.
# MAGIC
# MAGIC **O que este script faz.** Aponta violações **rotulando a origem de cada
# MAGIC regra**, e exige que os prefixos sejam declarados por quem os adota.

# MAGIC
# MAGIC **Guia local completo:** [README deste script](README.md).
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | apenas metadados: o script lê o schema, nunca as linhas |
# MAGIC | Escrita | uma view temporária de sessão |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_scripts.naming_checker import naming_checker

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparo — uma tabela com nomes deliberadamente irregulares

# COMMAND ----------

# Três problemas plantados: camelCase, maiúscula e nome longo demais.
spark.createDataFrame(
    [("a", 1, "x", "y")],
    "id_cliente string, ValorTotal int, dataDeReferencia string, "
    "coluna_com_nome_absurdamente_longo_que_ninguem_vai_digitar_duas_vezes string",
).createOrReplaceTempView("vw_exemplo_naming")

print("colunas:", spark.table("vw_exemplo_naming").columns)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Só a convenção do projeto, sem prefixo exigido

# MAGIC ```text
# MAGIC colunas: ['id_cliente', 'ValorTotal', 'dataDeReferencia', 'coluna_com_nome_absurdamente_longo_que_ninguem_vai_digitar_duas_vezes']
# MAGIC ```
# MAGIC
# COMMAND ----------

violacoes = naming_checker("vw_exemplo_naming", max_col_length=40)
for v in violacoes:
    print(f"[{v['policy']:32}] {v['object']}")
    print(f"    {v['message']}")

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC [databricks-recommended-context  ] vw_exemplo_naming
# MAGIC     Prefer a fully qualified Unity Catalog name: catalog.schema.table.
# MAGIC [project-custom                  ] ValorTotal
# MAGIC     Column is outside the configured lowercase snake_case convention.
# MAGIC [project-custom                  ] dataDeReferencia
# MAGIC     Column is outside the configured lowercase snake_case convention.
# MAGIC [project-custom                  ] coluna_com_nome_absurdamente_longo_que_ninguem_vai_digitar_duas_vezes
# MAGIC     Column exceeds the configured limit of 40 characters.
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A coluna `policy` é o que importa mais que a mensagem:
# MAGIC
# MAGIC | Valor | Significa |
# MAGIC |---|---|
# MAGIC | `databricks-recommended-context` | recomendação da plataforma, como usar o nome completo `catalog.schema.table` |
# MAGIC | `project-custom` | convenção deste projeto: `snake_case`, limite de tamanho |
# MAGIC | `organization-custom` | política da sua organização, e só existe se você a declarar |
# MAGIC
# MAGIC Repare que a tabela aparece como violação de contexto — a view temporária
# MAGIC não tem nome de três partes. É **aviso**, não erro: view de sessão não tem
# MAGIC catálogo mesmo. O script não sabe distinguir, e por isso todas as
# MAGIC severidades são `warning`.
# MAGIC
# MAGIC O erro de interpretação mais provável é ler a lista como reprovação. Não é
# MAGIC reprovação de nada: é inventário do que difere da convenção declarada.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A recusa: prefixo exigido sem lista de prefixos

# COMMAND ----------

try:
    naming_checker("vw_exemplo_naming", enforce_prefix=True)
except ValueError as erro:
    print(f"recusou, como deveria:\n  {erro}")

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC recusou, como deveria:
# MAGIC   allowed_table_prefixes is required when enforce_prefix=True
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Pedir para exigir prefixo sem dizer **quais** prefixos é
# MAGIC ambíguo, e o script poderia ter escolhido uma lista padrão — `dim_`,
# MAGIC `fato_`, `stg_` — que é o que a maioria das ferramentas faz.
# MAGIC
# MAGIC Ele recusa de propósito. Uma lista padrão embutida vira, na prática, a
# MAGIC convenção do autor da ferramenta aplicada à casa de outra pessoa, e a
# MAGIC primeira tabela que a viola gera discussão sobre uma regra que ninguém
# MAGIC adotou.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Com a política da casa declarada

# COMMAND ----------

violacoes_org = naming_checker(
    "vw_exemplo_naming",
    enforce_prefix=True,
    allowed_table_prefixes=("dim_", "fato_", "vw_"),
    max_col_length=40,
)
por_politica = {}
for v in violacoes_org:
    por_politica.setdefault(v["policy"], 0)
    por_politica[v["policy"]] += 1
print("violações por origem da regra:", por_politica)

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC violações por origem da regra: {'databricks-recommended-context': 1, 'project-custom': 3}
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** `vw_exemplo_naming` começa com `vw_`, que está na lista, então
# MAGIC não há violação de prefixo. As demais permanecem, e continuam separadas por
# MAGIC origem — que é o que permite alguém decidir "a convenção do projeto eu sigo,
# MAGIC a da organização eu discuto".

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este script
# MAGIC
# MAGIC - **Como gate de CI que bloqueia.** Todas as severidades são `warning` de
# MAGIC   propósito. Nomenclatura é convenção, e convenção tem exceção legítima.
# MAGIC - **Para renomear em massa.** Ele aponta; renomear coluna de tabela em uso
# MAGIC   quebra quem consome, e essa decisão não é automatizável.
# MAGIC - **Como fonte da convenção.** Ele aplica a política que você declara. Se a
# MAGIC   sua casa não escreveu a dela, o script não vai inventá-la.
# MAGIC - **Sobre view temporária, esperando silêncio.** Nome de três partes não
# MAGIC   existe aí, e o aviso de contexto vai aparecer sempre.
