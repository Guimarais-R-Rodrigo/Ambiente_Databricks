# Databricks notebook source
# MAGIC %md
# MAGIC # `comentar_notebook` — documentar o notebook para quem vai lê-lo em seis meses
# MAGIC
# MAGIC 📘 Guia local: [`README.md`](./README.md)
# MAGIC
# MAGIC **O arquivo do prompt não executa por si só.** Aqui somente o preparo
# MAGIC executa código. O briefing é texto para a interação autorizada, e a
# MAGIC resposta real deve ser registrada com evidência; continua pendente neste exemplo.
# MAGIC
# MAGIC | Parte | O que é | Roda? |
# MAGIC |---|---|---|
# MAGIC | 1 | preparo: localiza o notebook real a que o prompt se refere | **sim** |
# MAGIC | 2 | o prompt preenchido, pronto para copiar | não; é texto |
# MAGIC | 3 | a resposta real do Genie Code, colada de um chat | **exige uma pessoa** |

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | Spark para resolver current_user() e acesso de leitura ao arquivo publicado |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | nenhum; o insumo é um notebook já publicado |
# MAGIC | Escrita | **não** — apenas lê um trecho do notebook selecionado |
# MAGIC | Diferença Free × trabalho | confirme caminho, permissão e versão do notebook; acesso no Free não prova acesso corporativo |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

# O insumo deste prompt é um NOTEBOOK, não uma tabela. Use um dos exemplos da
# biblioteca, que já estão publicados no workspace e são conhecidos.
alvo = f"/Workspace/Users/{usuario}/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py"

with open(alvo, "r", encoding="utf-8") as fh:
    linhas = fh.read().splitlines()

celulas_codigo = sum(1 for l in linhas if l.startswith("# COMMAND"))
celulas_md = sum(1 for l in linhas if l.startswith("# MAGIC %md"))
print(f"notebook alvo: {alvo}")
print(f"linhas: {len(linhas)} | células: {celulas_codigo} | markdown: {celulas_md}")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** Abra o notebook alvo e confira as células efetivamente disponíveis. O exercício avalia clareza documental; marque outputs não observados como pendentes, sem inventá-los.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`comentar_notebook.md`](./comentar_notebook.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `REVISAO_EDICAO_OU_DOCUMENTACAO` decide se o assistente devolve sugestões ou o notebook reescrito. É a diferença entre uma revisão que você avalia e um arquivo que você precisa conferir linha a linha.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-comentar-notebook para documentar o notebook anexado.
# MAGIC
# MAGIC BRIEFING
# MAGIC - Notebook/células: `.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py`, anexado com Add context
# MAGIC - Modo: revisão — devolva sugestões, não o arquivo reescrito
# MAGIC - Público: analista de dados com experiência em SQL e pouca em Spark
# MAGIC - Profundidade: didática
# MAGIC - Objetivo de negócio: deixar claro, para quem chega, por que o join point-in-time existe e o que quebra sem ele
# MAGIC - Convenções/idioma: PT-BR na prosa, inglês nos identificadores; célula markdown antes de cada bloco de código
# MAGIC - Partes que não podem mudar: não altere código; só a documentação
# MAGIC - Dados sensíveis presentes: NÃO INFORMADO; confirme no conteúdo antes de reproduzir exemplos
# MAGIC - Permissão editorial: pode sugerir novas células Markdown; não aplicar edições neste modo REVISÃO
# MAGIC
# MAGIC INSTRUÇÕES
# MAGIC 1. Resuma o fluxo atual e identifique células, entradas, saídas e efeitos colaterais.
# MAGIC 2. No modo REVISÃO, não edite: entregue proposta e exemplos.
# MAGIC 3. No modo EDIÇÃO, preserve ordem, lógica, parâmetros, nomes públicos e resultados;
# MAGIC    não execute, refatore ou formate além do necessário sem autorização.
# MAGIC 4. Use células Markdown para objetivo, pré-requisitos, parâmetros, etapas, validações,
# MAGIC    limitações e próximos passos. Comentários inline devem explicar intenção e risco,
# MAGIC    não repetir literalmente o código.
# MAGIC 5. Marque pressupostos, TODOs e decisões pendentes; não invente regra de negócio.
# MAGIC 6. Remova de exemplos segredos, tokens, caminhos pessoais e valores de PII.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Resumo das mudanças ou recomendações.
# MAGIC - Proposta de organização com sumário proporcional, sem reescrever o notebook em modo REVISÃO.
# MAGIC - Descrição de inputs/outputs, compute/dependências e forma segura de execução.
# MAGIC - Alertas de qualidade, custo, segurança e idempotência encontrados.
# MAGIC - Lista explícita do que foi preservado e do que não foi possível validar.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme que nenhuma lógica foi alterada inadvertidamente.
# MAGIC - Confirme que referências entre células continuam válidas.
# MAGIC - Diferencie comentário factual de recomendação.
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
# MAGIC 1. Rode a Parte 1 deste notebook — ela não cria tabela; apenas lê o notebook selecionado.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre contexto e skill selecionados com evidência disponível.
# MAGIC    Relato do assistente não comprova sozinho leitura, importação, chamada
# MAGIC    ou conclusão; confira os artefatos exigidos pela rota da skill.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-comentar-notebook`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Em notebook que ainda vai mudar muito.** Documentar rascunho é trabalho jogado fora.
# MAGIC - **Como substituto de nome bom.** Comentário que explica uma variável mal nomeada trata o sintoma.
# MAGIC - **Sem declarar o público.** Documentação para quem já sabe e para quem não sabe são textos diferentes.
