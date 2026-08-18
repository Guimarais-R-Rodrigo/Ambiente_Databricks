# Databricks notebook source
# MAGIC %md
# MAGIC # `stat_check` — a pergunta estatística antes do teste estatístico
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
# MAGIC O briefing em branco está em [`stat_check.md`](./stat_check.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `PREDICAO_INFERENCIA_EXPERIMENTO` é o primeiro campo por um motivo: a mesma base responde perguntas diferentes conforme a finalidade, e o teste certo para uma é o teste errado para a outra.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-validacao-estatistica para avaliar se o método pretendido é adequado ao
# MAGIC desenho e aos dados anexados. Não transforme automaticamente um teste significativo
# MAGIC em causalidade ou relevância prática.
# MAGIC
# MAGIC BRIEFING
# MAGIC - Dataset/recurso: workspace.default.hub_exemplo_clientes
# MAGIC - Unidade, chave e grupos repetidos: uma linha por cliente e data; grupos por `uf`
# MAGIC - Target/desfecho e tipo: `alvo` binário
# MAGIC - Objetivo: inferência — queremos entender, não prever
# MAGIC - Método pretendido: proponha, e justifique a escolha contra as alternativas descartadas
# MAGIC - População, amostra e seleção: amostra de conveniência — os clientes que estavam na base de campanha
# MAGIC - Tempo, horizonte e split: não aplicável nesta análise
# MAGIC - Hipóteses primária/secundárias: a taxa de resposta difere entre UFs; e `renda` se relaciona com a resposta
# MAGIC - Alfa, potência/MDE e correção múltipla: proponha, incluindo correção para múltiplas comparações se houver
# MAGIC - Volume: 4.000 linhas
# MAGIC - Restrições/dependências: serverless; declare os pressupostos de cada teste e como verificá-los
# MAGIC - Modo: diagnóstico e código; não execute
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Confirme desenho, unidade independente, mecanismo de amostragem e disponibilidade
# MAGIC    temporal. Identifique pseudorreplicação, leakage e seleção pós-tratamento.
# MAGIC 2. Mapeie cada pergunta a estimando, método, pressupostos e diagnóstico. Não execute
# MAGIC    uma bateria indiscriminada de testes.
# MAGIC 3. Avalie tamanho de efeito e incerteza, não apenas p-valor. Quando houver múltiplas
# MAGIC    comparações, proponha correção e diferencie análise confirmatória de exploratória.
# MAGIC 4. Em grandes volumes, evite testes que detectam efeitos irrelevantes só pelo N;
# MAGIC    combine relevância prática, gráficos e amostra computacional quando apropriado.
# MAGIC 5. Em séries/tempo, preserve ordem e avalie dependência/estacionariedade conforme o
# MAGIC    método. Em grupos/entidades repetidas, use validação ou erros compatíveis.
# MAGIC 6. Não alegue causalidade sem desenho de identificação e pressupostos defensáveis.
# MAGIC
# MAGIC SEGURANÇA E CUSTO
# MAGIC - Faça somente leitura; não exponha PII nem exemplos de linhas identificáveis.
# MAGIC - Explique dependências antes de instalar bibliotecas ou executar análise pesada.
# MAGIC - Aguarde autorização para executar; código proposto deve ser reprodutível e ter seed.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Pergunta, estimando, método e pressupostos em uma matriz.
# MAGIC - Diagnósticos com evidências, tamanho de efeito e incerteza.
# MAGIC - Resultado interpretado em linguagem de negócio, sem extrapolação indevida.
# MAGIC - Código/testes somente no nível solicitado.
# MAGIC - Limitações, ameaças à validade e decisão técnica recomendada.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme direção do target e unidades.
# MAGIC - Declare tratamento de nulos/outliers e todas as exclusões.
# MAGIC - Separe significância estatística, relevância prática e poder preditivo.
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
# MAGIC Skill esperada aqui: `hub-ml-validacao-estatistica`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Para justificar uma conclusão já tomada.** O teste escolhido depois do resultado não testa nada.
# MAGIC - **Sem declarar a finalidade.** Inferência e predição pedem métodos diferentes sobre a mesma base.
# MAGIC - **Ignorando múltiplas comparações.** Cinco UFs testadas duas a duas produzem significância por acaso.
