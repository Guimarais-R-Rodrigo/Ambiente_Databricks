# Databricks notebook source
# MAGIC %md
# MAGIC # `auditoria_skills` — auditar uma skill contra o próprio contrato
# MAGIC
# MAGIC 📘 Guia local: [`README.md`](./README.md)
# MAGIC
# MAGIC **O arquivo do prompt não executa por si só.** Aqui somente o preparo
# MAGIC executa código. O briefing é texto para a interação autorizada, e a
# MAGIC resposta real deve ser registrada com evidência; continua pendente neste exemplo.
# MAGIC
# MAGIC | Parte | O que é | Roda? |
# MAGIC |---|---|---|
# MAGIC | 1 | preparo: localiza a skill real a que o prompt se refere | **sim** |
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
# MAGIC | Dados | nenhum; o insumo é um arquivo `SKILL.md` já publicado |
# MAGIC | Escrita | **não** — apenas lê a skill selecionada |
# MAGIC | Diferença Free × trabalho | confirme caminho, permissão e versão da skill; acesso no Free não prova acesso corporativo |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

# O insumo deste prompt é uma SKILL, não uma tabela. Use uma das publicadas.
alvo = f"/Workspace/Users/{usuario}/.assistant/skills/hub-ml-criar-objeto/SKILL.md"

with open(alvo, "r", encoding="utf-8") as fh:
    conteudo = fh.read()

frontmatter = conteudo.split("---")[1] if conteudo.startswith("---") else ""
print(f"skill alvo: {alvo}")
print(f"linhas: {len(conteudo.splitlines())}")
print("\n--- frontmatter ---")
print(frontmatter.strip()[:400])

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O alvo é uma skill real publicada. Audite o estado atual do arquivo e dos testes, sem assumir que histórico de revisão ou palavras-chave substituem evidência de roteamento.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`auditoria_skills.md`](./auditoria_skills.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `AUDITORIA_PLANO_DE_CORRECAO_OU_CORRIGIR_AUTORIZADO` é o campo que define se você recebe um diagnóstico ou um arquivo alterado. Para skill, prefira diagnóstico: mudar `description` invalida a certificação de roteamento.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-auditoria-skills no modo implementação. No modo
# MAGIC IMPLEMENTAÇÃO, audite a pasta da skill contra a documentação oficial atual da
# MAGIC Databricks e o padrão Agent Skills. No modo OUTPUT, audite o artefato anexado contra
# MAGIC o pedido original e o contrato no SKILL.md da skill produtora. Não edite no modo
# MAGIC AUDITORIA.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Skill/pasta alvo: hub-ml-criar-objeto
# MAGIC - Output alvo (modo OUTPUT): não aplicável
# MAGIC - Pedido original (modo OUTPUT): não aplicável
# MAGIC - Casos de uso esperados: criar snippet novo; criar script novo; converter objeto existente ao padrão
# MAGIC - Exemplos de prompts: "quero criar um snippet para calcular taxa de resposta"; "como calculo PSI entre duas safras?"
# MAGIC - Ambiente user/workspace: Agent Skill em `.assistant/skills/hub-ml-criar-objeto/`, anexada com Add context
# MAGIC - Dependências/scripts: `hub_padroes/` (os seis templates), `tools/api_publica.py`, `tools/validate_assistant.py`
# MAGIC - Riscos prioritários: conformidade ao template de skill, veracidade das afirmações sobre o repositório, e risco de colisão de roteamento
# MAGIC - Modo: auditoria e plano de correção; **não** altere a `description`
# MAGIC
# MAGIC CHECKLIST
# MAGIC 1. Estrutura: `.assistant/skills/<skill>/SKILL.md`, pasta dedicada e referências
# MAGIC    relativas à raiz da skill.
# MAGIC 2. Frontmatter: `name` e `description` obrigatórios; nome válido, descrição que
# MAGIC    explique o que faz e quando usar, e campos opcionais somente se suportados.
# MAGIC 3. Descoberta: escopo focal, gatilhos inequívocos e possibilidade de `@` mention.
# MAGIC 4. Conteúdo: passos claros, exemplos, casos de borda e contexto mínimo necessário.
# MAGIC 5. Recursos: scripts executáveis, documentação separada, links/caminhos válidos e
# MAGIC    ausência de imports/APIs fantasma.
# MAGIC 6. Segurança: sem segredos, PII, paths pessoais ou ações mutáveis sem limites.
# MAGIC 7. Correção: APIs atuais, claims suportados e distinção entre recurso Databricks e
# MAGIC    convenção customizada.
# MAGIC 8. Testes: validação estrutural, parsing, execução segura de scripts e prompts
# MAGIC    representativos. Registre o que não pôde ser executado.
# MAGIC 9. No modo OUTPUT: contrato da skill produtora, matriz requisito→evidência, correção
# MAGIC    técnica dos resultados, reprodutibilidade, rastreabilidade e adequação ao pedido.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Inventário e veredito de descobribilidade.
# MAGIC - No modo OUTPUT, veredito do artefato e separação entre defeito do output,
# MAGIC   limitação da skill e entrada ausente.
# MAGIC - Achados P0/P1/P2/P3 com arquivo, evidência, impacto e correção proposta.
# MAGIC - Matriz requisito→evidência→status.
# MAGIC - Plano de testes e prompts de forward test.
# MAGIC - No modo CORRIGIR, diff e validações; preserve funcionalidade e não altere outras
# MAGIC   skills sem autorização.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Não declare sucesso apenas porque o Markdown abre.
# MAGIC - Verifique referências e scripts de ponta a ponta quando seguro.
# MAGIC - Cite a documentação oficial usada e sinalize inferências.
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
# MAGIC 1. Rode a Parte 1 deste notebook — ela não cria tabela; apenas lê o `SKILL.md` selecionado.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre contexto e skill selecionados com evidência disponível.
# MAGIC    Relato do assistente não comprova sozinho leitura, importação, chamada
# MAGIC    ou conclusão; confira os artefatos exigidos pela rota da skill.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-auditoria-skills`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Para aprovar skill por palavra-chave.** Conter o vocabulário certo não significa que o fluxo é executável.
# MAGIC - **Autorizando correção da `description`.** Mudá-la invalida a certificação de roteamento das vizinhas.
# MAGIC - **Sem anexar a pasta.** Auditoria de memória sobre skill que o assistente não leu é opinião.
