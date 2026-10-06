# Databricks notebook source
# MAGIC %md
# MAGIC # `safe_display` — limitar a prévia antes de chamar o renderer
# MAGIC
# MAGIC > **Comece pelo conceito:** [README.md](README.md) explica quando usar, quando evitar,
# MAGIC > entradas, saídas e limitações antes da execução deste exemplo.
# MAGIC
# MAGIC **O problema.** `display(df)` numa tabela grande parece inofensivo porque a
# MAGIC interface mostra só as primeiras linhas. Dependendo do que veio antes na
# MAGIC cadeia, o Spark precisa materializar bem mais do que aparece — e um
# MAGIC `toPandas()` esquecido no meio de uma exploração derruba o notebook com um
# MAGIC erro que não menciona a linha culpada.
# MAGIC
# MAGIC **O que este helper faz.** Aplica `limit` **antes** de exibir e avisa
# MAGIC quando há mais linhas do que o mostrado.

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
# MAGIC | Diferença Free × trabalho | não usar cache não garante equivalência; confira plano, runtime e renderer |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.spark.safe_display import safe_display
from hub_snippets.testing import fixtures

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. A chamada mais óbvia **não funciona** — e o motivo importa

# COMMAND ----------

base = fixtures.base_tabular(n=5000, seed=42)

try:
    safe_display(base, limit=10)
except RuntimeError as erro:
    print(f"recusou:\n  {erro}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Executado no laboratório, isto levanta:
# MAGIC
# MAGIC ```text
# MAGIC RuntimeError: Databricks display() is unavailable; pass display_fn explicitly
# MAGIC ```
# MAGIC
# MAGIC E o motivo é a coisa mais útil deste notebook. O helper procura a função
# MAGIC `display` em `globals()` — mas ele é um **módulo importado**, e os
# MAGIC `globals()` de um módulo são os dele, não os do notebook. A `display` que
# MAGIC o Databricks injeta vive no escopo do notebook e nunca é visível de dentro
# MAGIC da biblioteca.
# MAGIC
# MAGIC Globais do notebook não são herdados por um módulo importado. Passe `display_fn=display` explicitamente. A ausência do renderer só é detectada depois da contagem limitada; a tentativa pode ter custo mesmo ao falhar.
# MAGIC
# MAGIC A recusa é o comportamento certo. A alternativa seria não exibir nada em
# MAGIC silêncio, e aí o helper pareceria funcionar.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A forma que funciona

# COMMAND ----------

# `display` existe no escopo do notebook: passe-a explicitamente.
safe_display(base, limit=10, display_fn=display)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A mensagem de truncamento aparece na **saída da célula**, e
# MAGIC não só na interface. Parece redundante e não é: a saída da célula sobrevive
# MAGIC quando alguém exporta o notebook, cola um trecho num relatório ou lê o
# MAGIC `.py` versionado. O aviso visual da interface não sobrevive a nada disso.
# MAGIC
# MAGIC O erro que isso evita é específico: alguém copia a tabela exibida para um
# MAGIC slide e a apresenta como "a base", sem perceber que via dez linhas.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Por que `limit` antes, e não `display` direto

# COMMAND ----------

# O helper injeta um limit no plano ANTES de qualquer ação. A diferença aparece
# no plano de execução, não no resultado.
base.limit(10).explain(mode="simple")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O plano mostra o `LocalLimit`/`GlobalLimit` empurrado para
# MAGIC perto da fonte. Numa cadeia com join ou agregação antes, é essa posição que
# MAGIC decide se o Spark processa dez linhas ou a base inteira para depois jogar
# MAGIC fora.
# MAGIC
# MAGIC O helper não faz mágica: ele insere o limite no DataFrame entregue ao
# MAGIC renderer e evita uma contagem integral **apenas para descobrir o truncamento**.
# MAGIC Transformações anteriores que exigem processamento amplo continuam custando.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. A função de exibição é injetável, e é o que o torna testável

# COMMAND ----------

# Fora de notebook — num job, num teste — `display` não existe. O parâmetro
# `display_fn` existe para isso, e é o que torna o helper testável.
capturado = []
safe_display(base, limit=3, display_fn=lambda d: capturado.append(d.count()))
print(f"linhas que a função de exibição recebeu: {capturado}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Três linhas chegaram à função injetada, não 5.000. É a prova
# MAGIC de que o limite acontece antes, e é também o mecanismo que permite testar
# MAGIC este helper numa suíte que roda sem interface.
# MAGIC
# MAGIC Vale como princípio de projeto: helper que chama `display` diretamente é
# MAGIC helper que só funciona em notebook e nunca é testado.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Esperando que ele barateie a consulta.** O limite ajuda quando a
# MAGIC   cadeia permite empurrá-lo para baixo. Depois de uma agregação global, o
# MAGIC   trabalho já foi feito.
# MAGIC - **Para inspecionar linha específica.** Limite não é filtro: para achar
# MAGIC   um caso, filtre por ele.
# MAGIC - **Como garantia contra estouro de memória.** Ele reduz o risco mais
# MAGIC   comum, não todos. `collect()` e `toPandas()` continuam disponíveis e
# MAGIC   continuam perigosos.
# MAGIC - **Em DataFrame já pequeno.** Aí ele só acrescenta uma linha de aviso sem
# MAGIC   informação.
