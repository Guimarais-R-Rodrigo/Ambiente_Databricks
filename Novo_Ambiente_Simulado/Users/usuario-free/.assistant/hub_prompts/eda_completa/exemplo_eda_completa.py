# Databricks notebook source
# MAGIC %md
# MAGIC # `eda_completa` — EDA que sustenta decisão de modelagem
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
# MAGIC O briefing em branco está em [`eda_completa.md`](./eda_completa.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC A diferença para o `eda_rapida` está em duas linhas: aqui o **target está definido** e o **entregável é declarado**. As duas mudam o que o assistente produz, não só o tamanho da resposta.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-eda-profissional para construir uma EDA completa, auditável e adequada
# MAGIC ao volume, sem alterar os dados de origem.
# MAGIC
# MAGIC BRIEFING
# MAGIC - Recurso principal: workspace.default.hub_exemplo_clientes
# MAGIC - Contexto de negócio/decisão: campanha de relacionamento em CRM bancário; queremos priorizar quem abordar no próximo ciclo
# MAGIC - Unidade de análise: uma linha por cliente e data de referência
# MAGIC - Chave primária/candidata: `id_cliente` + `dt_referencia`, a confirmar
# MAGIC - Coluna temporal: dt_referencia
# MAGIC - Target e evento positivo: `alvo` = 1 quando o cliente respondeu à campanha em até 30 dias
# MAGIC - Período e filtros: 2026-01 a 2026-06, sem filtro
# MAGIC - Volume estimado: 4.000 linhas
# MAGIC - Foco prioritário: qualidade, granularidade e relação de cada variável com o target
# MAGIC - Restrições de compute, prazo e bibliotecas: serverless, sem `cache()`; nada de `toPandas()` sem limite
# MAGIC - Entregável: notebook, com células markdown antes de cada bloco de código
# MAGIC
# MAGIC PRÉ-REQUISITOS
# MAGIC 1. Verifique o recurso anexado, schema, comentários do Unity Catalog e permissões.
# MAGIC 2. Liste ambiguidades que mudariam a análise; faça perguntas somente sobre bloqueios.
# MAGIC 3. Declare plano, número esperado de varreduras e estratégia de amostragem.
# MAGIC
# MAGIC ESCOPO MÍNIMO
# MAGIC 1. Estrutura: schema, tipos, volume, duplicidade, chaves e granularidade observada.
# MAGIC 2. Qualidade: nulos, valores inválidos, cardinalidade, extremos, consistência e
# MAGIC    cobertura temporal. Não confunda ausência permitida com erro.
# MAGIC 3. Univariada: estatísticas robustas e distribuições adequadas ao tipo de variável.
# MAGIC 4. Bivariada/multivariada: relações relevantes, segmentos, tempo e target, quando
# MAGIC    aplicável; correlação não implica causalidade.
# MAGIC 5. Risco de modelagem: leakage temporal/alvo, viés de seleção, drift, desbalanceamento
# MAGIC    e representatividade, se houver finalidade de ML.
# MAGIC 6. Visualização: Plotly quando útil; agregue/amostre antes de coletar ao driver.
# MAGIC
# MAGIC SEGURANÇA E CUSTO
# MAGIC - Priorize PySpark/Spark SQL. Não faça `toPandas()` ou `collect()` irrestrito.
# MAGIC - Não revele PII, segredos ou valores individuais; use agregação/mascaramento.
# MAGIC - Não escreva tabelas, não sobrescreva notebooks e não instale dependências sem
# MAGIC   apresentar o impacto e obter autorização explícita.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Resumo executivo orientado à decisão.
# MAGIC - Inventário de qualidade com evidência, severidade, impacto e recomendação.
# MAGIC - Notebook/código organizado por células idempotentes, com parâmetros no início.
# MAGIC - Tabelas e gráficos com títulos, unidade, período, base e observações.
# MAGIC - Conclusões ligadas às evidências, limitações e backlog priorizado.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Registre recursos, filtros, período, contagens e amostra efetivamente usados.
# MAGIC - Valide que joins não multiplicaram linhas e que denominadores são explícitos.
# MAGIC - Separe achados observados, hipóteses e recomendações.
# MAGIC - Liste o que não foi possível verificar e por quê.
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
# MAGIC - **Sem target definido.** Metade do valor da EDA completa é a relação com o alvo; sem ele, use `eda_rapida`.
# MAGIC - **Em base que ainda vai mudar.** EDA sobre esquema instável envelhece antes de ser lida.
# MAGIC - **Como entregável final.** Ela informa a decisão de modelagem; quem decide é você.
