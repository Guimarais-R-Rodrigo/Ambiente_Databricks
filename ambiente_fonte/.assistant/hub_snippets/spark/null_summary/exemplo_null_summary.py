# Databricks notebook source
# MAGIC %md
# MAGIC # `null_summary` — nulo por coluna, com semáforo
# MAGIC
# MAGIC **O problema.** Contar nulos é trivial e por isso costuma ser feito de
# MAGIC improviso, coluna a coluna, numa célula que ninguém revisa. O resultado é
# MAGIC uma lista de números sem referência: 4% de nulos é muito ou pouco? Depende
# MAGIC da coluna, e a lista não diz.
# MAGIC
# MAGIC **O que este helper faz.** Devolve uma linha por coluna, com contagem,
# MAGIC percentual e um status comparado contra limiares declarados.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, gerados por `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.spark.null_summary import null_summary
from hub_snippets.testing import fixtures

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. O resumo sobre uma base com ausentes declarados

# COMMAND ----------

base = fixtures.base_tabular(n=500, seed=42, pct_nulos_renda=0.04)
display(null_summary(base))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Executado no laboratório, `renda` aparece com **13 nulos**
# MAGIC (2,6%) e status verde; as demais colunas com zero.
# MAGIC
# MAGIC Repare na diferença entre o parâmetro e o realizado: a fixture foi chamada
# MAGIC com `pct_nulos_renda=0.04`, e saíram 2,6%. Não é erro — o gerador sorteia
# MAGIC linha a linha, então a fração é uma probabilidade, não uma cota. Base real
# MAGIC também não tem percentual redondo.
# MAGIC
# MAGIC O erro de interpretação mais provável aqui é ler o status como veredito
# MAGIC sobre a qualidade da coluna. Ele é a comparação contra um limiar que **você**
# MAGIC passou; a próxima célula mostra o que isso significa.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O semáforo é seu, não do dado

# COMMAND ----------

# A mesma base, com um limiar apertado: o que era verde passa a alertar.
display(null_summary(base, threshold_warn=1.0, threshold_fail=10.0))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Nada mudou nos dados — `renda` continua com 13 nulos em 500.
# MAGIC O que mudou foi o limiar, e com ele o status.
# MAGIC
# MAGIC Isso parece óbvio numa célula ao lado da outra, e deixa de ser quando o
# MAGIC resumo chega num relatório sem os limiares junto. Uma coluna "vermelha"
# MAGIC numa tabela mensal sob limiar diário não diz nada sobre o dado.
# MAGIC
# MAGIC **Ausente não é sempre defeito.** `data_de_cancelamento` nula significa que
# MAGIC o cliente não cancelou; preencher com zero destruiria a informação. O
# MAGIC helper conta e classifica — decidir o que fazer exige saber o que a coluna
# MAGIC representa.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Onde ele entra num fluxo

# COMMAND ----------

# Uso típico: rodar antes de qualquer agregação e olhar só o que não está verde.
resumo = null_summary(base, threshold_warn=1.0, threshold_fail=10.0)
suspeitas = resumo.filter("status != 'ok'")
print(f"colunas fora do limiar: {suspeitas.count()} de {len(base.columns)}")
display(suspeitas)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Uma coluna de cinco. Em base larga — dezenas ou centenas de
# MAGIC colunas — é este filtro que torna o resumo utilizável: olhar a tabela
# MAGIC inteira em cada execução não escala, e olhar nenhuma é o que acontece na
# MAGIC prática.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como medida de qualidade.** Ausência é uma dimensão entre várias.
# MAGIC   Valor presente e errado passa despercebido aqui.
# MAGIC - **Tratando todo nulo como problema.** Em muitas colunas o nulo é a
# MAGIC   informação: não cancelou, não teve segunda compra, não respondeu.
# MAGIC - **Sem declarar os limiares no relatório.** O status sem o limiar ao lado
# MAGIC   é opinião apresentada como fato.
# MAGIC - **Sobre DataFrame já filtrado.** Filtrar antes de medir esconde
# MAGIC   exatamente as linhas que costumam concentrar ausência.
