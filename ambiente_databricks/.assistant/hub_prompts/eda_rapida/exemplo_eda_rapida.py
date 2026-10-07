# Databricks notebook source
# MAGIC %md
# MAGIC # `eda_rapida` — perfil rápido de uma tabela desconhecida
# MAGIC
# MAGIC **O arquivo do prompt não executa por si só.** Ele orienta uma interação
# MAGIC que pode executar ferramentas conforme autorização e configuração. Neste
# MAGIC notebook, só o preparo executa código; o pedido é texto e a resposta real
# MAGIC continua pendente de captura. Isso não é uma limitação universal da plataforma.
# MAGIC
# MAGIC | Parte | O que é | Roda? |
# MAGIC |---|---|---|
# MAGIC | 1 | preparo: cria a base sintética a que o prompt se refere | **sim** |
# MAGIC | 2 | o prompt preenchido, pronto para copiar | não; é texto |
# MAGIC | 3 | a resposta real do Genie Code, colada de um chat | **exige uma pessoa** |

# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. Confira efeitos do preparo e o estado da resposta antes de usar.
# MAGIC
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | sessão Spark e permissões compatíveis com a criação da tabela de exemplo |
# MAGIC | Bibliotecas | PySpark e pacote Hub importável; dependências de análise dependem da rota escolhida |
# MAGIC | Dados | sintéticos, de `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | **sim, overwrite** — sobrescreve `workspace.default.hub_exemplo_clientes` |
# MAGIC | Diferença Free × trabalho | não execute o preparo sobre recurso compartilhado; usar fonte real exige autorização e revisão de dados sensíveis |

# COMMAND ----------
# MAGIC %md
# MAGIC **Antes de executar a Parte 1 ou Run all:** o preparo sobrescreve `workspace.default.hub_exemplo_clientes`
# MAGIC com `mode("overwrite")`. Confira destino e autorização; pode substituir dados
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. O preparo não executa a EDA.
# MAGIC
# MAGIC O nome também é usado por EDA, Baseline, Explainability, Novo Projeto, Pipeline e Stat Check.
# MAGIC
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
# MAGIC **Como ler.** Confira o schema efetivamente impresso. A fixture gera `id_cliente`, `uf`, `renda`, `dt_referencia` e `alvo`: cinco colunas. A base tem 4.000 linhas, com nulos e prevalência solicitados na configuração; o resultado exato depende da geração. Um cenário sintético não homologa sua fonte real.

# COMMAND ----------
# MAGIC %md
# MAGIC **Rota da análise:** ao selecionar a EDA profissional, siga `run_enforced`,
# MAGIC Receipt, handoff e `finalize_or_raise`; conclusão exige Postflight PASS e
# MAGIC `completion.authorized=true`. `PENDING_POSTFLIGHT` ainda não é conclusão.
# MAGIC Helpers/SQL manuais não são bypass. Veja a [skill](../../skills/hub-ml-eda-profissional/SKILL.md).
# MAGIC
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
# MAGIC Evidência    : nenhuma resposta desta interação foi registrada e revisada.
# MAGIC                Não invente conteúdo para completar o exemplo. O preparo
# MAGIC                não prova execução nem conclusão canônica da skill.
# MAGIC Quem preenche : quem tiver acesso ao Genie Code do workspace.
# MAGIC ```
# MAGIC
# MAGIC **Como preencher**, quando for a hora:
# MAGIC
# MAGIC 1. Se o preparo for necessário, confirme destino e autorização: ele sobrescreve `workspace.default.hub_exemplo_clientes`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre o contexto e a skill efetivamente selecionados, com evidência
# MAGIC    da interface quando disponível. Uma afirmação do assistente não prova
# MAGIC    sozinha que um arquivo ou uma skill tenha sido carregado.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-eda-profissional`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Quando uma checagem específica já resolve a pergunta.** Conhecimento anterior não dispensa nova avaliação após mudanças relevantes na fonte.
# MAGIC - **Como aprovação de modelagem.** É um primeiro olhar; uma investigação ampliada também precisa de validação proporcional à decisão.
# MAGIC - **Sem acesso autorizado à fonte.** O assistente deve declarar a limitação; não aceite achados sem evidência como se a leitura tivesse ocorrido.
