# Databricks notebook source
# MAGIC %md
# MAGIC # TEMPLATE — notebook de exemplo do Hub
# MAGIC
# MAGIC Copie este arquivo, troque o conteúdo, mantenha a ordem dos blocos. A
# MAGIC referência completa e executável é
# MAGIC `hub_padroes/snippet/exemplo/exemplo_taxa_resposta_campanha.py`.
# MAGIC
# MAGIC ## Formato-fonte — o que quebra se você errar
# MAGIC
# MAGIC | Elemento | Forma correta |
# MAGIC |---|---|
# MAGIC | Primeira linha do arquivo | `# Databricks notebook source`, sem nada antes |
# MAGIC | Separador de célula | `# COMMAND ----------` |
# MAGIC | Célula de markdown | toda linha prefixada com `# MAGIC ` |
# MAGIC | Magic de shell/pip | `# MAGIC %pip install lib==1.2.3` |
# MAGIC | Nome do arquivo | `exemplo_<nome_do_objeto>.py`, sempre |
# MAGIC
# MAGIC Escrever `%pip install lib==1.2.3` sem o `# MAGIC` faz `ast.parse` estourar
# MAGIC e a validação reprovar o repositório inteiro.

# COMMAND ----------
# MAGIC %md
# MAGIC ## BLOCO 1 (obrigatório) — o problema, antes da solução
# MAGIC
# MAGIC Abra pelo **problema de negócio**, não pela função. Duas ou três frases:
# MAGIC o que alguém está tentando decidir, qual é o caminho natural, e o que esse
# MAGIC caminho esconde.
# MAGIC
# MAGIC Um notebook que abre com "este módulo calcula X" já perdeu o leitor que
# MAGIC não sabe se precisa de X.

# COMMAND ----------
# MAGIC %md
# MAGIC ## BLOCO 2 (obrigatório) — o que este notebook assume do ambiente
# MAGIC
# MAGIC Copie a tabela e preencha. O laboratório é Free; o destino não é.
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless / clássico / indiferente |
# MAGIC | Bibliotecas | nenhuma, **ou** a lista com versão fixada |
# MAGIC | Dados | de onde vêm; sintéticos sempre |
# MAGIC | Escrita | o que é criado, ou "nada é escrito" |
# MAGIC | Diferença Free × trabalho | a conhecida, ou "nenhuma conhecida" |

# COMMAND ----------

# BLOCO 3 (obrigatório) — preâmbulo. Estas três linhas abrem todo notebook do
# Hub: sem elas, o import da biblioteca falha.
import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

# from hub_snippets.<secao>.<objeto> import <api>

# COMMAND ----------
# MAGIC %md
# MAGIC ## BLOCO 4 (repetível) — os quatro movimentos
# MAGIC
# MAGIC Cada trecho de código do notebook segue esta sequência. Repita quantas
# MAGIC vezes o assunto exigir; não pule nenhum.
# MAGIC
# MAGIC 1. **Contexto** — o que este trecho vai fazer e por que alguém precisaria,
# MAGIC    em linguagem de negócio antes da técnica.
# MAGIC 2. **Código comentado** — comentário nas linhas onde a decisão não é
# MAGIC    óbvia. Não comente o que o código já diz.
# MAGIC 3. **Execução real** — a chamada, com dados sintéticos, e a saída de
# MAGIC    verdade. Nunca saída inventada.
# MAGIC 4. **Leitura do resultado** — o que aquele número significa, e **o erro de
# MAGIC    interpretação mais provável ali**. Este quarto item é o que separa um
# MAGIC    notebook didático de uma demonstração.

# COMMAND ----------

# (movimento 2 — código comentado)

# COMMAND ----------
# MAGIC %md
# MAGIC (movimento 4 — leitura do resultado)

# COMMAND ----------
# MAGIC %md
# MAGIC ## VARIANTE — objeto sem dados e sem número
# MAGIC
# MAGIC Constantes, paletas e funções que devolvem HTML não têm o que executar
# MAGIC sobre fixture, e os movimentos 3 e 4 não se aplicam como descritos. Para
# MAGIC esses, a sequência é:
# MAGIC
# MAGIC 1. **Contexto** — igual.
# MAGIC 2. **O valor** — mostre a constante ou chame a função.
# MAGIC 3. **O efeito** — renderize o HTML, exiba a cor, mostre o resultado visual.
# MAGIC 4. **A decisão de design** — por que esta paleta e não outra, por que este
# MAGIC    limite de contraste, o que quebra se alguém mudar.
# MAGIC
# MAGIC O contrato de fixture não se aplica aqui: `hub_snippets.testing.fixtures`
# MAGIC só produz DataFrames.

# COMMAND ----------
# MAGIC %md
# MAGIC ## BLOCO CANÔNICO — quando a execução é impossível
# MAGIC
# MAGIC Notebook que não pode rodar no laboratório **não** sai com célula vazia nem
# MAGIC com saída inventada. Sai com este bloco, preenchido:
# MAGIC
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO
# MAGIC
# MAGIC O que rodaria : <a chamada exata>
# MAGIC Por que não   : <o motivo, com a mensagem de erro se houver>
# MAGIC Onde verificar: <o documento que registra a limitação>
# MAGIC O que falta   : <o que destravaria>
# MAGIC ```
# MAGIC
# MAGIC Sem forma única, cada autor inventa a sua e o leitor não distingue "não
# MAGIC roda" de "ninguém tentou".

# COMMAND ----------
# MAGIC %md
# MAGIC ## BLOCO FINAL (obrigatório) — quando **não** usar
# MAGIC
# MAGIC De três a cinco itens, cada um com o motivo. É a seção que mais economiza
# MAGIC retrabalho, e a única que impede o helper de ser aplicado onde ele mente.
# MAGIC
# MAGIC Fontes boas para esta lista: pressupostos do método que ninguém verifica;
# MAGIC o uso que parece natural e está errado; e a diferença entre o que o helper
# MAGIC descreve e o que alguém vai querer concluir dele.
