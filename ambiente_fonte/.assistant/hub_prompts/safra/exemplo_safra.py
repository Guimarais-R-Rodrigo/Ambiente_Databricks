# Databricks notebook source
# MAGIC %md
# MAGIC # `safra` — comparar safras sem comparar coisas diferentes
# MAGIC
# MAGIC 📘 Guia local: [`README.md`](./README.md)
# MAGIC
# MAGIC **Prompt não executa.** Ele é um briefing para colar num chat, e a
# MAGIC resposta vem de uma interação que notebook nenhum reproduz. Este notebook
# MAGIC tem três partes, e só as duas primeiras rodam:
# MAGIC
# MAGIC | Parte | O que é | Roda? |
# MAGIC |---|---|---|
# MAGIC | 1 | preparo: cria a base sintética a que o prompt se refere | **sim** |
# MAGIC | 2 | o prompt preenchido, pronto para copiar | não; é texto |
# MAGIC | 3 | a resposta real do Genie Code, colada de um chat | **exige uma pessoa** |

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | sintéticos, de `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | **sim** — cria a tabela `workspace.default.hub_exemplo_safras` para o chat poder consultá-la |
# MAGIC | Diferença Free × trabalho | no trabalho, aponte o prompt para uma tabela real governada em vez da sintética |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

base = fixtures.safras(n_contratos=1200, seed=42,
                       safras_yyyymm=("202501", "202502", "202503"),
                       mob_maximo=12)
base.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_safras")

print(f"linhas: {base.count()}")
# `agg` com dicionário não aceita `countDistinct` — o nome não resolve como
# rotina SQL. A forma que funciona é a função de `pyspark.sql.functions`.
from pyspark.sql import functions as F

base.groupBy("safra").agg(
    F.countDistinct("id_contrato").alias("contratos"),
    F.max("mob").alias("mob_maximo"),
).orderBy("safra").show()

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Três safras, e a mais antiga tem MOB maior — é assim que a base é por construção, e é a armadilha inteira: comparar safras pelo calendário compara a de janeiro com 12 meses de exposição contra a de março com 10. A resposta precisa alinhar por MOB.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`safra.md`](./safra.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `CENSURA_E_MATURIDADE` é o campo que quase todo pedido informal esquece. Safra imatura não é safra boa: é safra que ainda não teve tempo de ficar ruim.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-analise-safra para realizar análise de safra reproduzível e comparável,
# MAGIC com denominadores e maturação explícitos.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Dataset: workspace.default.hub_exemplo_safras
# MAGIC - Entidade/contrato e chave: contrato; `id_contrato`
# MAGIC - Data de entrada na safra: safra (formato AAAAMM)
# MAGIC - Frequência da safra: mensal
# MAGIC - Data de observação e idade: `mob` — meses desde a originação
# MAGIC - Evento/numerador: `inadimplente` = 1 na primeira vez que o contrato atinge o critério; depois disso permanece 1
# MAGIC - Exposição/denominador: contratos distintos originados na safra
# MAGIC - Métrica: taxa cumulativa de contratos afetados
# MAGIC - Censura/maturidade mínima: a safra de 202503 tem menos MOB observado; não a compare com 202501 no calendário
# MAGIC - Segmentos e período: sem segmentação; as três safras
# MAGIC - Referência normativa, se houver: não aplicável — base sintética
# MAGIC - Restrições: serverless; use `hub_snippets.ml.vintage_analysis`
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Confirme granularidade, calendário, timezone e regra de entrada/saída da coorte.
# MAGIC 2. Crie grade safra × idade, preservando células imaturas como não observáveis; não
# MAGIC    converta ausência de maturação em zero.
# MAGIC 3. Calcule numerador, denominador e taxa por célula. Para acumulados, deduplicate
# MAGIC    eventos/entidades conforme a definição; não some taxas cumulativas.
# MAGIC 4. Compare safras somente em idades equivalentes e destaque mix, exposição e volume.
# MAGIC 5. Faça sanity checks de monotonicidade apenas quando a própria métrica exigir.
# MAGIC 6. Use agregações Spark em alto volume, sem expor registros individuais.
# MAGIC 7. Não grave tabela ou atribua conformidade normativa sem autorização e validação.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Dicionário formal da métrica e linha do tempo.
# MAGIC - Matriz safra × maturidade com volume, numerador, denominador e taxa.
# MAGIC - Curvas/heatmap, achados comparáveis e intervalos/alertas de baixo volume.
# MAGIC - Limitações por censura, composição e dados incompletos.
# MAGIC - Código reprodutível, se solicitado, e testes de reconciliação.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Reconcilie totais e entidades únicas.
# MAGIC - Confirme células imaturas, denominadores e duplicidade.
# MAGIC - Separe tendência observada, hipótese causal e afirmação normativa.
# MAGIC ```

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 3 — a resposta real
# MAGIC
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO — depende de uma pessoa
# MAGIC
# MAGIC O que falta   : colar aqui a resposta que o Genie Code deu ao prompt
# MAGIC                 da Parte 2, num chat novo, com a base da Parte 1 criada.
# MAGIC Por que não   : prompt produz resposta de assistente, e nenhum job
# MAGIC                 reproduz isso. Resposta inventada é pior que resposta
# MAGIC                 nenhuma — ensina que o assistente faz algo que ele não faz.
# MAGIC Quem preenche : quem tiver acesso ao Genie Code do workspace.
# MAGIC ```
# MAGIC
# MAGIC **Como preencher**, quando for a hora:
# MAGIC
# MAGIC 1. Rode a Parte 1 deste notebook — ela cria `workspace.default.hub_exemplo_safras`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre **qual skill foi carregada** — é a única forma de saber se o
# MAGIC    roteamento está fazendo o que se espera fora da bateria de forward
# MAGIC    tests. Se não souber, pergunte no mesmo chat.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-analise-safra`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Somando taxas por MOB.** O acumulado passa de 100% e ninguém percebe. Conte contratos distintos afetados.
# MAGIC - **Comparando safras pelo calendário.** A antiga sempre parece pior porque teve mais tempo.
# MAGIC - **Com safra imatura no mesmo gráfico, sem marcar.** Ela desce menos porque viveu menos, não porque é melhor.
