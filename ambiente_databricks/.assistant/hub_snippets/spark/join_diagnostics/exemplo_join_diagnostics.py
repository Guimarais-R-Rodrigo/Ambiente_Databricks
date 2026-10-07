# Databricks notebook source
# MAGIC %md
# MAGIC # Junção: medir antes de juntar
# MAGIC
# MAGIC > **Comece pelo conceito:** [README.md](README.md) explica quando usar, quando evitar,
# MAGIC > entradas, saídas e limitações antes da execução deste exemplo.
# MAGIC
# MAGIC > **Material didático do Hub — não é auto-descoberto pelo Genie Code.**
# MAGIC > Dados sintéticos apenas. Inventário completo da biblioteca no
# MAGIC > [catálogo de helpers](../../../MANUAL_TECNICO_V2.md#catalogo-helpers).
# MAGIC
# MAGIC ## O problema
# MAGIC
# MAGIC Juntar duas tabelas parece a operação mais banal do dia. É também uma das
# MAGIC que mais silenciosamente estraga uma base de treino, porque o Spark faz
# MAGIC exatamente o que você pediu e nada avisa quando o que você pediu não era
# MAGIC o que você queria.
# MAGIC
# MAGIC Três coisas podem acontecer sem nenhuma mensagem de erro: a base cresce,
# MAGIC a base encolhe, ou parte dela some por chave nula.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | sessão Spark e APIs compatíveis; confira runtime, permissões e comportamento no destino |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

current_user = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{current_user}/.assistant")

from pyspark.sql import functions as F
from hub_snippets.testing import fixtures
from hub_snippets.spark.join_diagnostics import diagnosticar_join

print("biblioteca acessível")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. O caso que preserva a base
# MAGIC
# MAGIC ```text
# MAGIC biblioteca acessível
# MAGIC ```
# MAGIC
# MAGIC Cada cliente aparece uma única vez do lado direito. É o caso confortável,
# MAGIC e é bom saber reconhecê-lo pelos números.

# COMMAND ----------

clientes = fixtures.base_tabular(n=500, seed=3)
cadastro = clientes.select("id_cliente").distinct().withColumn("segmento", F.lit("varejo"))

d = diagnosticar_join(clientes, cadastro, "id_cliente")

for chave in ["linhas_esquerda", "linhas_direita", "linhas_com_match",
              "multiplicidade_max_direita", "expansao_prevista_left", "relacao"]:
    print(f"{chave:>28}: {d[chave]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ```text
# MAGIC              linhas_esquerda: 500
# MAGIC               linhas_direita: 500
# MAGIC             linhas_com_match: 500
# MAGIC   multiplicidade_max_direita: 1
# MAGIC       expansao_prevista_left: 1.0
# MAGIC                      relacao: 1:1 ou N:1 — join preserva a cardinalidade
# MAGIC ```
# MAGIC
# MAGIC `expansao_prevista = 1.0` é a leitura que importa: o join devolve tantas
# MAGIC linhas quantas entraram. `multiplicidade_max_direita = 1` explica por quê
# MAGIC — nenhuma chave se repete do lado direito.
# MAGIC
# MAGIC ## 2. O caso que infla a base
# MAGIC
# MAGIC Agora o lado direito tem duas linhas por cliente. Situação corriqueira:
# MAGIC uma tabela de contratos, de endereços, de telefones. Cada cliente tem
# MAGIC mais de um.

# COMMAND ----------

base = clientes.select("id_cliente").distinct()
contratos = (
    base.withColumn("contrato", F.lit("A"))
        .union(base.withColumn("contrato", F.lit("B")))
)

d = diagnosticar_join(clientes, contratos, "id_cliente")

print(f"linhas antes do join   : {d['linhas_esquerda']}")
print(f"linhas depois do join  : {d['linhas_apos_join_left']}")
print(f"fator de expansão      : {d['expansao_prevista_left']}")
print(f"leitura                : {d['relacao']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ```text
# MAGIC linhas antes do join   : 500
# MAGIC linhas depois do join  : 1000
# MAGIC fator de expansão      : 2.0
# MAGIC leitura                : 1:N — join duplica linhas da esquerda
# MAGIC ```
# MAGIC
# MAGIC A base dobrou. Se isso for uma tabela de treino, cada cliente passa a
# MAGIC valer o dobro no aprendizado do modelo, sem que ninguém tenha decidido
# MAGIC dar esse peso.
# MAGIC
# MAGIC E o efeito é desigual: clientes com cinco contratos pesariam cinco vezes,
# MAGIC clientes com um pesariam uma. O modelo aprende preferencialmente sobre
# MAGIC quem tem mais contratos — que costuma ser justamente o perfil menos
# MAGIC representativo da base.
# MAGIC
# MAGIC **O que fazer:** agregue o lado direito antes de juntar (um contrato por
# MAGIC cliente, ou uma contagem, ou o mais recente), ou aceite a expansão
# MAGIC conscientemente porque a unidade de análise realmente é contrato, não
# MAGIC cliente. O erro não é expandir; é expandir sem perceber.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. O caso que encolhe a base
# MAGIC
# MAGIC Cadastro incompleto: metade dos clientes não tem correspondência.

# COMMAND ----------

cadastro_parcial = cadastro.limit(250)

d = diagnosticar_join(clientes, cadastro_parcial, "id_cliente")

print(f"linhas na esquerda   : {d['linhas_esquerda']}")
print(f"encontraram par      : {d['linhas_com_match']}")
print(f"ficaram sem par      : {d['linhas_sem_match_chave_valida']}")
print(f"cobertura            : {d['cobertura_pct_chaves_validas']}%")
print()
print("exemplos de chaves órfãs:", d["exemplos_sem_match"][:3])

# COMMAND ----------

# MAGIC %md
# MAGIC ```text
# MAGIC linhas na esquerda   : 500
# MAGIC encontraram par      : 250
# MAGIC ficaram sem par      : 250
# MAGIC cobertura            : 50.0%
# MAGIC
# MAGIC exemplos de chaves órfãs: [{'id_cliente': 'cli00250'}, {'id_cliente': 'cli00251'}, {'id_cliente': 'cli00252'}]
# MAGIC ```
# MAGIC
# MAGIC Com `left join`, essas linhas permanecem e as colunas do lado direito vêm
# MAGIC nulas — o que costuma ser o comportamento desejado. Com `inner join`,
# MAGIC elas somem, e a base encolhe pela metade sem aviso.
# MAGIC
# MAGIC A cobertura é a informação que decide entre um e outro. Cobertura de 50%
# MAGIC pode ser aceitável (a fonte só cobre parte do público) ou sintoma de
# MAGIC chave errada. Os exemplos de chaves órfãs servem exatamente para isso:
# MAGIC olhe alguns e veja se fazem sentido.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Chave nula: o caso que ninguém conta
# MAGIC
# MAGIC Em SQL, `NULL` nunca é igual a `NULL`. Duas linhas com chave nula não
# MAGIC casam entre si — e também não casam com nada. Elas simplesmente somem do
# MAGIC resultado de um `inner join`, ou ficam órfãs num `left`.
# MAGIC
# MAGIC O helper conta essas linhas **separadamente**, porque misturá-las com as
# MAGIC órfãs legítimas esconde um problema de qualidade que tem outra causa e
# MAGIC outra correção.

# COMMAND ----------

com_nulos = clientes.withColumn(
    "id_cliente",
    F.when(F.rand(seed=42) < 0.1, F.lit(None)).otherwise(F.col("id_cliente")),
)

d = diagnosticar_join(com_nulos, cadastro, "id_cliente")

print(f"linhas na esquerda      : {d['linhas_esquerda']}")
print(f"com chave nula          : {d['chaves_nulas_esquerda']}  <- nunca casam")
print(f"cobertura sobre o total : {d['cobertura_pct_chaves_validas']}%")

# COMMAND ----------

# MAGIC %md
# MAGIC ```text
# MAGIC linhas na esquerda      : 500
# MAGIC com chave nula          : 48  <- nunca casam
# MAGIC cobertura sobre o total : 100.0%
# MAGIC ```
# MAGIC
# MAGIC Leitura didática do campo: `cobertura_pct_chaves_validas` exclui as 48 linhas
# MAGIC de chave nula do denominador. Se a célula impressa disser “sobre o total”,
# MAGIC interprete-a pelo campo real: 100% das chaves válidas, não de toda a esquerda.
# MAGIC
# MAGIC Chave nula costuma ter causa distinta da chave órfã: erro de extração,
# MAGIC campo opcional na origem, cliente sem documento. A correção também é
# MAGIC outra — não adianta procurar a chave faltante no cadastro.
# MAGIC
# MAGIC ## Resumo para levar
# MAGIC
# MAGIC | Número | O que ele responde |
# MAGIC |---|---|
# MAGIC | `expansao_prevista_left` | o join vai inflar a base? `1,0` preserva |
# MAGIC | `multiplicidade_max_direita` | quantas linhas por chave existem à direita |
# MAGIC | `cobertura_pct_chaves_validas` | quanto da esquerda encontra par |
# MAGIC | `chaves_nulas_*` | quanto não casa por motivo diferente |
# MAGIC | `exemplos_sem_match` | amostra para conferir se a chave está certa |
# MAGIC
# MAGIC O diagnóstico antecipa uma pergunta que frequentemente aparece só depois do
# MAGIC join. O custo, porém, depende de volume, distribuição das chaves e plano: há
# MAGIC agregações e joins Spark, portanto não existe promessa de tempo fixo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como substituto do join.** Ele mede o que vai acontecer; não junta
# MAGIC   nada, e a decisão de juntar continua sendo sua.
# MAGIC - **Em chave composta, passando só uma coluna.** A multiplicidade sai
# MAGIC   errada — informe a chave inteira.
# MAGIC - **Sobre tabela grande, sem avaliar custo.** Há contagens, agregações,
# MAGIC   `left_semi`, `inner` e `left_anti`; o custo depende do volume, das partições
# MAGIC   e da distribuição das chaves.
# MAGIC - **Esperando que ele decida o tipo de join.** Inner, left e anti
# MAGIC   respondem a perguntas diferentes de negócio, e o diagnóstico só informa
# MAGIC   o custo de cada uma.
