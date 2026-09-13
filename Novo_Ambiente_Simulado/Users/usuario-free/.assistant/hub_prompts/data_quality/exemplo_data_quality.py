# Databricks notebook source
# MAGIC %md
# MAGIC # `data_quality` — diagnóstico de qualidade antes de confiar na base
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
# MAGIC | Escrita | **sim** — cria a tabela `workspace.default.hub_exemplo_clientes_dup` para o chat poder consultá-la |
# MAGIC | Diferença Free × trabalho | no trabalho, aponte o prompt para uma tabela real governada em vez da sintética |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

# `n_entidades` menor que `n` produz duplicidade proposital na chave — que é
# exatamente o defeito que um diagnóstico de qualidade precisa achar.
base = fixtures.base_tabular(n=4000, seed=42, n_entidades=3200,
                             pct_nulos_renda=0.06)
base.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes_dup")

print(f"linhas: {base.count()} | id_cliente distintos: {base.select('id_cliente').distinct().count()}")
base.show(5, truncate=False)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A contagem de linhas e a de chaves distintas **não batem**, e isso é de propósito: 4.000 linhas para 3.200 clientes. É o defeito mais comum e o mais fácil de não ver — uma taxa calculada sobre essa base pesa quem aparece mais vezes.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`data_quality.md`](./data_quality.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC O `USO_DOWNSTREAM` é o campo que muda a resposta inteira: duplicidade que não atrapalha um relatório de contagem quebra um modelo.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-eda-profissional para avaliar a qualidade do recurso anexado e propor
# MAGIC um contrato verificável. Não modifique dados nem pipeline nesta etapa.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Tabela/view/DataFrame/pipeline: workspace.default.hub_exemplo_clientes_dup
# MAGIC - Unidade de análise: deveria ser uma linha por cliente e data
# MAGIC - Chave(s): `id_cliente` + `dt_referencia`
# MAGIC - Coluna de evento/atualização: dt_referencia
# MAGIC - Partições: não informado
# MAGIC - Uso e consumidores downstream: base de treino de um modelo de propensão
# MAGIC - Regras já acordadas: nenhuma regra formal; é a primeira vez que esta base é auditada
# MAGIC - SLOs/thresholds e justificativas: proponha, e diga de onde saiu cada limite
# MAGIC - Período: 2026-01 a 2026-06
# MAGIC - Restrições: serverless; nada de `cache()`
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Confirme schema, comentários do Unity Catalog, volume e granularidade.
# MAGIC 2. Proponha checks de completude, unicidade, validade, consistência, integridade
# MAGIC    referencial, atualidade e volume. Diferencie regra de negócio de regra técnica.
# MAGIC 3. Execute somente leituras autorizadas, consolidando agregações para reduzir scans.
# MAGIC 4. Para cada falha, mostre numerador, denominador, taxa, período e exemplos somente
# MAGIC    anonimizados/agregados.
# MAGIC 5. Se o recurso for Lakeflow Spark Declarative Pipelines, proponha expectations com
# MAGIC    comportamento explícito (monitorar, descartar ou falhar), sem aplicá-las ainda.
# MAGIC 6. Priorize regras por impacto downstream e risco de falso positivo.
# MAGIC
# MAGIC SEGURANÇA E CUSTO
# MAGIC - Não exponha PII; não liste registros brutos como evidência.
# MAGIC - Não grave quarentena, não altere DDL e não reinicie pipeline sem confirmação.
# MAGIC - Para tabelas grandes, use pruning por partição e agregações; declare o escopo lido.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Scorecard por dimensão com resultado, limite, evidência e severidade.
# MAGIC - Catálogo de regras: ID, descrição, expressão, nível, ação e proprietário sugerido.
# MAGIC - Código PySpark/Spark SQL ou expectations proposto em bloco separado.
# MAGIC - Riscos, falsos positivos possíveis, lacunas de metadados e plano de implantação.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme chaves, granularidade, timezone e período de referência.
# MAGIC - Valide que taxas usam denominadores corretos e que nulos não foram omitidos.
# MAGIC - Não declare conformidade quando uma dimensão não foi testada.
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
# MAGIC 1. Rode a Parte 1 deste notebook — ela cria `workspace.default.hub_exemplo_clientes_dup`.
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
# MAGIC - **Sem declarar o uso downstream.** A mesma duplicata é irrelevante num relatório e fatal num treino.
# MAGIC - **Aceitando limiares sem fonte.** Se o assistente propuser 5% de nulos como corte, pergunte de onde veio.
# MAGIC - **Uma vez só.** Qualidade não é estado, é série temporal: o que passou hoje pode falhar no mês que vem.
