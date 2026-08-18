# Databricks notebook source
# MAGIC %md
# MAGIC # `auditoria_skills` — auditar uma skill contra o próprio contrato
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
# MAGIC | Escrita | **sim** — cria a tabela `nenhuma — o insumo é uma pasta de skill` para o chat poder consultá-la |
# MAGIC | Diferença Free × trabalho | no trabalho, aponte o prompt para uma tabela real governada em vez da sintética |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

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
# MAGIC **Como ler.** A skill escolhida é a mais nova, e é a que menos histórico tem. É de propósito: auditar a skill que já passou por revisão humana mede pouco. E há um detalhe honesto — ela é a única cuja `description` ainda não passou por forward test.

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
# MAGIC Por que não   : prompt produz resposta de assistente, e nenhum job
# MAGIC                 reproduz isso. Resposta inventada é pior que resposta
# MAGIC                 nenhuma — ensina que o assistente faz algo que ele não faz.
# MAGIC Quem preenche : quem tiver acesso ao Genie Code do workspace.
# MAGIC ```
# MAGIC
# MAGIC **Como preencher**, quando for a hora:
# MAGIC
# MAGIC 1. Rode a Parte 1 deste notebook — ela cria `nenhuma — o insumo é uma pasta de skill`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre **qual skill foi carregada** — é a única forma de saber se o
# MAGIC    roteamento está fazendo o que se espera fora da bateria de forward
# MAGIC    tests. Se não souber, pergunte no mesmo chat.
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
