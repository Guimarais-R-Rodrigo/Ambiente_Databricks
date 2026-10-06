# Databricks notebook source
# MAGIC %md
# MAGIC # `novo_projeto` — começar um projeto sem repetir o que já existe
# MAGIC
# MAGIC 📘 Guia local: [`README.md`](./README.md)
# MAGIC
# MAGIC **O arquivo do prompt não executa por si só.** Aqui somente o preparo
# MAGIC executa código. O briefing é texto para a interação autorizada, e a
# MAGIC resposta real deve ser registrada com evidência; continua pendente neste exemplo.
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
# MAGIC | Compute | sessão Spark compatível com as fixtures e permissões de escrita no destino confirmado |
# MAGIC | Bibliotecas | PySpark e pacote Hub importável; dependências de análise dependem da rota escolhida |
# MAGIC | Dados | sintéticos, de `hub_snippets.testing.fixtures` |
# MAGIC | Escrita | **sim, overwrite** — sobrescreve `workspace.default.hub_exemplo_clientes` |
# MAGIC | Diferença Free × trabalho | fonte real exige autorização, revisão de dados sensíveis e contrato próprio; este preparo é sintético |

# COMMAND ----------
# MAGIC %md
# MAGIC **Antes de executar a Parte 1 ou Run all:** o preparo sobrescreve `workspace.default.hub_exemplo_clientes`
# MAGIC com `mode("overwrite")`. Confira destino e autorização; pode substituir dados
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. Pedir somente plano no chat não neutraliza esta escrita.
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
# MAGIC **Como ler.** Cinco colunas, 4.000 linhas, `renda` com cerca de 6% de nulos e `alvo` em torno de 18%. Os nulos e o desbalanceamento são deliberados: um prompt que produz resposta boa numa base perfeita não diz nada sobre a base que você tem.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`novo_projeto.md`](./novo_projeto.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC Este prompt não recomenda skill no cabeçalho. Ele é o de estruturação, e serve como caso interessante de roteamento: veja qual skill o Genie Code escolhe, se escolher alguma.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Estruture um novo projeto analítico no Databricks com documentação mínima,
# MAGIC governança, plano de validação e contexto reutilizável.
# MAGIC
# MAGIC BRIEFING
# MAGIC - Nome curto: propensao-campanha-crm
# MAGIC - Problema/decisão: priorizar clientes para a próxima campanha de relacionamento, com estimativa de resposta por segmento
# MAGIC - Dono e stakeholders: time de CRM analítico; interlocutor de negócio é o gestor da campanha
# MAGIC - Critério de sucesso e guardrails: AUC no teste temporal; taxa de resposta observada por decil de score
# MAGIC - Fontes conhecidas: workspace.default.hub_exemplo_clientes; nenhum pipeline ainda; notebooks de EDA a fazer
# MAGIC - Entidade/target/horizonte: cliente; `alvo` = resposta em até 30 dias; horizonte de 30 dias
# MAGIC - Entregáveis e prazo: EDA em 1 semana, baseline em 2, decisão de seguir ou parar em 3
# MAGIC - Ambientes: não informado
# MAGIC - Segurança, PII e compliance: serverless; dados sintéticos nesta fase; nenhum dado real até a aprovação de governança
# MAGIC - Repositório/Git folder: não informado
# MAGIC - Modo: somente plano
# MAGIC
# MAGIC INSTRUÇÕES
# MAGIC 1. Verifique o contexto anexado e liste dúvidas que impedem definição segura.
# MAGIC 2. Proponha uma árvore simples de projeto, separando código, testes, configuração e
# MAGIC    documentação. Não invente nomes de catálogos, credenciais ou owners.
# MAGIC 3. Gere um `AGENTS.md` do zero, com apenas instruções
# MAGIC    aplicáveis aos arquivos daquele diretório e descendentes.
# MAGIC 4. Para implantação, proponha Declarative Automation Bundles com targets separados
# MAGIC    quando fizer sentido; não faça deploy nem crie recursos sem autorização.
# MAGIC 5. Inclua riscos, decisões, definition of done, validações, rollback e observabilidade.
# MAGIC 6. Não armazene segredos, PII, tokens ou caminhos pessoais em arquivos versionados.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Project charter curto e mensurável.
# MAGIC - Estrutura proposta com finalidade de cada item.
# MAGIC - `AGENTS.md` pronto para revisão, sem duplicar preferências globais.
# MAGIC - Backlog inicial priorizado, dependências e responsáveis sugeridos.
# MAGIC - Critérios de aceite/teste e plano de ambientes.
# MAGIC - Lista explícita de ações que exigem autorização.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme que `AGENTS.md` será colocado no diretório ancestral correto.
# MAGIC - Diferencie estrutura oficial Databricks das convenções do Hub (`hub_`/`hub-`).
# MAGIC - Verifique que nenhum placeholder, segredo ou path pessoal ficou no artefato final.
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
# MAGIC 4. Registre contexto e skill selecionados com evidência disponível.
# MAGIC    Relato do assistente não comprova sozinho leitura, importação, chamada
# MAGIC    ou conclusão; confira os artefatos exigidos pela rota da skill.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: nenhuma em especial — é um prompt de organização, e o roteamento observado aqui é informação útil.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Como substituto de conversa com o negócio.** Ele organiza o que você já sabe; não descobre o que ninguém contou.
# MAGIC - **Assumindo compromisso sem dono.** Dono pendente pode constar no plano; execução dependente exige responsável confirmado.
# MAGIC - **Tratando prazo proposto como compromisso.** Registre prazo pendente ou estimado até decisão do responsável.
