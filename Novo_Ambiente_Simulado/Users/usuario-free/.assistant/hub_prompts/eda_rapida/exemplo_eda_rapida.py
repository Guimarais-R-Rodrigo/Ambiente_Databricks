# Databricks notebook source
# MAGIC %md
# MAGIC # `eda_rapida` — perfil rápido de uma tabela desconhecida
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
# MAGIC | Escrita | **sim** — cria a tabela `workspace.default.hub_exemplo_clientes` para o chat poder consultá-la |
# MAGIC | Diferença Free × trabalho | no trabalho, aponte o prompt para uma tabela real governada em vez da sintética |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

base = fixtures.base_tabular(n=4000, seed=42, pct_nulos_renda=0.06,
                             prevalencia_alvo=0.18)
base.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes")

print(f"linhas: {base.count()}")
base.printSchema()
base.show(5, truncate=False)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Cinco colunas, 4.000 linhas, `renda` com cerca de 6% de nulos e `alvo` em torno de 18%. Os nulos e o desbalanceamento são deliberados: um prompt que produz resposta boa numa base perfeita não diz nada sobre a base que você tem.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`eda_rapida.md`](./eda_rapida.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC Repare no que foi preenchido com **"não informado"**: é informação também. Dizer que você não sabe a chave é diferente de omitir a linha, porque o assistente passa a ter de descobri-la em vez de assumir.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-eda-profissional para produzir um perfil rápido, objetivo e
# MAGIC reprodutível do recurso anexado.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Tabela/DataFrame: workspace.default.hub_exemplo_clientes
# MAGIC - Objetivo de negócio: entender se esta base sustenta um modelo de propensão antes de investir em feature engineering
# MAGIC - Foco: qualidade das colunas, granularidade e força do sinal de `alvo`
# MAGIC - Chave esperada: suspeita de `id_cliente`, não confirmada
# MAGIC - Coluna temporal: dt_referencia
# MAGIC - Filtros/período: nenhum
# MAGIC - Limite de execução: até 2 minutos de compute serverless; se algo passar disso, proponha em vez de executar
# MAGIC
# MAGIC MODO DE TRABALHO
# MAGIC 1. Confirme que o contexto anexado corresponde ao recurso informado; não invente
# MAGIC    catálogo, schema, colunas, tipos nem regras de negócio.
# MAGIC 2. Antes de executar, apresente um plano curto e identifique campos ausentes que
# MAGIC    impedem conclusão confiável.
# MAGIC 3. Inspecione schema, volume aproximado, completude, cardinalidade, duplicidade da
# MAGIC    chave, período coberto e distribuição das variáveis relevantes.
# MAGIC 4. Para alto volume, use agregações PySpark/Spark SQL e uma amostra declarada apenas
# MAGIC    para visualização; evite `toPandas()` irrestrito e varreduras repetidas.
# MAGIC 5. Não exiba valores identificáveis. Masque ou agregue PII e sinalize acesso indevido.
# MAGIC 6. Não escreva, altere ou apague dados. Solicite confirmação separada caso alguma
# MAGIC    ação mutável se torne necessária.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Resumo executivo com até 8 achados priorizados.
# MAGIC - Quadro: dimensão verificada, evidência, severidade, impacto e ação sugerida.
# MAGIC - Código PySpark/Spark SQL executável em células pequenas e comentadas, somente se
# MAGIC   solicitado ou autorizado.
# MAGIC - Limitações, pressupostos, custo estimado e checagens que ficaram pendentes.
# MAGIC - Próximos passos, distinguindo correções obrigatórias de investigações opcionais.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Declare filtros, período, contagens e amostragem realmente usados.
# MAGIC - Diferencie evidência observada de hipótese.
# MAGIC - Confirme que o código não coleta dados em excesso nem altera a origem.
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
# MAGIC 1. Rode a Parte 1 deste notebook — ela cria `workspace.default.hub_exemplo_clientes`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre **qual skill foi carregada** — é a única forma de saber se o
# MAGIC    roteamento está fazendo o que se espera fora da bateria de forward
# MAGIC    tests. Se não souber, pergunte no mesmo chat.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-eda-profissional`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Quando a tabela é conhecida.** Se você já sabe granularidade, chave e qualidade, este prompt gasta tempo confirmando o que você sabe.
# MAGIC - **Como substituto de EDA completa.** Ele é o primeiro olhar; `eda_completa` é o que sustenta decisão de modelagem.
# MAGIC - **Em tabela que você não pode ler.** Antes de qualquer prompt, confirme que tem permissão — a resposta que vem sem acesso é plausível e inventada.
