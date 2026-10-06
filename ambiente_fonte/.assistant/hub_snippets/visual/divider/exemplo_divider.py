# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.divider` — separadores com hierarquia declarada
# MAGIC
# MAGIC **O problema.** `<hr>` puro tem um peso só, então uma página com três níveis de assunto fica com três traços iguais — e a estrutura que existe na cabeça de quem escreveu não chega a quem lê.
# MAGIC
# MAGIC **O que este objeto oferece.** Quatro separadores para reforçar visualmente a hierarquia. Eles complementam títulos, mas não explicam o assunto por si.

# MAGIC
# MAGIC Antes de executar, consulte o [guia do objeto](README.md): conceito, requisitos, efeitos e limites.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | exemplo usa sessão Spark para localizar usuário; renderização conforme notebook |
# MAGIC | Bibliotecas | biblioteca padrão Python e módulos locais do Hub; confira a preparação da sessão |
# MAGIC | Dados | nenhum — este objeto não recebe dados |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | confira compatibilidade e renderização no destino; a demonstração não homologa todo runtime |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.visual.divider import divider_heavy, divider_light, divider_medium, divider_section

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Os quatro pesos, lado a lado

# COMMAND ----------

displayHTML(f"""
<div style="font-family:Segoe UI">
  <p>divider_light — separa itens de uma mesma lista</p>
  {divider_light()}
  <p>divider_medium — separa blocos de um mesmo assunto</p>
  {divider_medium()}
  <p>divider_heavy — separa assuntos</p>
  {divider_heavy()}
  <p>divider_section — abre uma seção nova</p>
  {divider_section()}
  <p>fim</p>
</div>
""")

# COMMAND ----------

for nome, fn in [("divider_light", divider_light), ("divider_medium", divider_medium),
                 ("divider_heavy", divider_heavy), ("divider_section", divider_section)]:
    print(f"  {nome:18s} {fn()}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC   divider_light      <hr style="border:none; border-top:1px solid #D9DEE3; margin:10px 0;"/>
# MAGIC   divider_medium     <hr style="border:none; border-top:1.5px solid #BFC7D1; margin:14px 0;"/>
# MAGIC   divider_heavy      <hr style="border:none; border-top:2px solid #005CA9; margin:18px 0;"/>
# MAGIC   divider_section    <div style="margin:20px 0;"><hr style="border:none; border-top:2px solid #005CA9; margin:0;"/><hr style="border:none; border-top:1px solid #D9DEE3; margin:4px 0 0 0;"/></div>
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A hierarquia está em **três dimensões ao mesmo tempo**, e é isso
# MAGIC que oferece pistas visuais complementares: a espessura cresce (1 → 1,5 → 2px), o tom
# MAGIC escurece (cinza claro → cinza médio → azul institucional) e o espaço em
# MAGIC volta aumenta (10 → 14 → 18px).
# MAGIC
# MAGIC A legibilidade depende da tela, do zoom e do contexto. Esta demonstração
# MAGIC permite comparar os estilos, mas não é um teste de percepção com usuários.
# MAGIC Mantenha títulos que expliquem cada fronteira.
# MAGIC
# MAGIC `divider_section` quebra o padrão de propósito: são **dois** traços
# MAGIC empilhados, o que produz um sinal que nenhum dos outros três produz. É o
# MAGIC estilo sugerido para seção nova; o nome da função não impõe essa escolha.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como substituto de título.** Separador marca fronteira; ele não diz o que vem depois.
# MAGIC - **Mais de um nível por página sem critério.** Se todo bloco leva `divider_heavy`, voltou a existir um peso só.
# MAGIC - **Em Markdown puro.** São HTML para `displayHTML`; numa célula `%md` o traço de `---` já resolve.
