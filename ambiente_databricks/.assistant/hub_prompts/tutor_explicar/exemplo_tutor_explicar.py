# Databricks notebook source
# MAGIC %md
# MAGIC # `tutor_explicar` — entender o que o código faz, e por que ele faz assim
# MAGIC
# MAGIC 📘 Guia local: [`README.md`](./README.md)
# MAGIC
# MAGIC **O arquivo do prompt não executa por si só.** Aqui somente o preparo
# MAGIC executa código. O briefing é texto para a interação autorizada, e a
# MAGIC resposta real deve ser registrada com evidência; continua pendente neste exemplo.
# MAGIC
# MAGIC | Parte | O que é | Roda? |
# MAGIC |---|---|---|
# MAGIC | 1 | preparo: localiza o código real a que o prompt se refere | **sim** |
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
# MAGIC | Dados | nenhum; o insumo é um módulo Python já publicado |
# MAGIC | Escrita | **não** — apenas lê o código selecionado |
# MAGIC | Diferença Free × trabalho | confirme caminho, permissão e versão do módulo; acesso no Free não prova acesso corporativo |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

# O insumo deste prompt é CÓDIGO, não tabela. Use um módulo real da biblioteca,
# que está publicado e que você pode abrir ao lado.
alvo = f"/Workspace/Users/{usuario}/.assistant/hub_snippets/spark/pit_join/pit_join.py"

with open(alvo, "r", encoding="utf-8") as fh:
    codigo = fh.read()

print(f"módulo alvo: {alvo}")
print(f"linhas: {len(codigo.splitlines())}")
print("\n--- as 20 primeiras linhas, para você ver do que se trata ---")
print("\n".join(codigo.splitlines()[:20]))

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O preparo lê o módulo, mas imprime apenas as 20 primeiras linhas. Para explicar o arquivo inteiro, anexe o conteúdo integral autorizado; esta impressão não prova que o chat o recebeu. O objetivo é entender a razão do atraso de publicação.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`tutor_explicar.md`](./tutor_explicar.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC `INICIANTE_INTERMEDIARIO_AVANCADO` não é sobre inteligência: é sobre qual vocabulário pode ser assumido. Declarar errado produz uma explicação que não ensina nem para cima nem para baixo.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Use @hub-ml-tutor-databricks para explicar o objeto anexado de forma progressiva,
# MAGIC tecnicamente precisa e conectada ao meu contexto.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Objeto/pergunta: `.assistant/hub_snippets/spark/pit_join/pit_join.py`, anexado com Add context
# MAGIC - Meu nível atual: intermediário em SQL, iniciante em Spark
# MAGIC - Profundidade: passo a passo, com o porquê de cada decisão
# MAGIC - Objetivo prático: entender por que a janela do join precisa do atraso de publicação, e o que aconteceria sem ele
# MAGIC - Ambiente/compute/runtime: Databricks Free, serverless; confirme a versão efetiva do Spark antes de depender de comportamento específico
# MAGIC - Contexto de negócio: CRM bancário; a decisão é abordar ou não um cliente numa campanha
# MAGIC - Restrições: comece com uma resposta conceitual curta; explique o raciocínio antes de uma adaptação pronta; use analogia quando ajudar, sem executar ou alterar recursos
# MAGIC
# MAGIC MÉTODO
# MAGIC 1. Confirme o objeto anexado e destaque pré-requisitos ou versão que afetam a resposta.
# MAGIC 2. Comece com um mapa mental curto; depois explique do conceito ao detalhe solicitado.
# MAGIC 3. Use um exemplo mínimo e um exemplo aplicado ao contexto, sem inventar schema/dados.
# MAGIC 4. Diferencie comportamento documentado, boa prática, escolha de arquitetura e opinião.
# MAGIC 5. Ao explicar código, cubra entradas, saídas, execução lazy/eager, shuffle, custo,
# MAGIC    falhas comuns e como validar o resultado.
# MAGIC 6. Não execute nem altere recursos. Se um experimento ajudar, proponha um teste pequeno,
# MAGIC    reversível e sem dados sensíveis, aguardando autorização.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Resposta direta em primeiro lugar.
# MAGIC - Explicação em camadas com termos definidos.
# MAGIC - Exemplo mínimo reproduzível.
# MAGIC - Armadilhas e checklist de verificação.
# MAGIC - Duas perguntas de autoavaliação com respostas recolhidas em seção separada.
# MAGIC - Referências oficiais da Databricks quando a versão ou o produto importar.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Não afirme que uma funcionalidade existe sem distingui-la de convenção personalizada.
# MAGIC - Declare incertezas e dependências de versão.
# MAGIC - Verifique que o exemplo não usa APIs obsoletas nem coleta dados em excesso.
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
# MAGIC 1. Rode a Parte 1 deste notebook — ela não cria tabela; apenas lê o módulo Python selecionado.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre contexto e skill selecionados com evidência disponível.
# MAGIC    Relato do assistente não comprova sozinho leitura, importação, chamada
# MAGIC    ou conclusão; confira os artefatos exigidos pela rota da skill.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-tutor-databricks`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Para revisar código.** Tutor explica o que está lá; revisão diz o que deveria mudar.
# MAGIC - **Sem anexar o código.** Explicação de memória sobre código que o assistente não viu é ficção plausível.
# MAGIC - **Como fonte única.** Confirme na documentação oficial o que for afirmação sobre a plataforma.
