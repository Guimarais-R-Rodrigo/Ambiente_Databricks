# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.badge` — o selo que resume um veredito
# MAGIC
# MAGIC **O problema.** Um relatório com trinta números pede que o leitor decida, número a número, se aquilo é bom. A maior parte das pessoas não decide: rola até o fim e pergunta "e aí, passou?".
# MAGIC
# MAGIC **O que este objeto oferece.** Três selos em HTML — status com semáforo, score com faixa e destaque em linha — para responder essa pergunta antes que ela seja feita.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | nenhum — este objeto não recebe dados |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.visual.badge import badge_inline, badge_score, badge_status

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Os três, renderizados

# COMMAND ----------

# As funcoes devolvem STRING de HTML. Quem renderiza e o notebook — o modulo
# nao pode chamar displayHTML, porque ela nao existe dentro de modulo importado.
html = " ".join([
    badge_status("cobertura suficiente", "ok"),
    badge_status("multiplicidade acima do esperado", "warn"),
    badge_status("chave duplicada", "fail"),
])
displayHTML(f'<div style="font-family:Segoe UI">{html}</div>')

print("o que a funcao devolve, em texto:")
print(" ", badge_status("cobertura suficiente", "ok"))

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC <span style="display:inline-block; background:#EAF7EC; color:#2E7D32;
# MAGIC       padding:2px 8px; border-radius:10px; font-size:11px;">cobertura suficiente</span>
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** A função devolve **string**, e quem renderiza é o notebook. Não é
# MAGIC escolha de estilo: `displayHTML` é um global do notebook e **não existe
# MAGIC dentro de um módulo importado** — a mesma armadilha que o `safe_display`
# MAGIC documenta do lado do `display`.
# MAGIC
# MAGIC Um helper que tentasse renderizar sozinho funcionaria enquanto colado numa
# MAGIC célula e quebraria ao virar biblioteca. Devolver string é o que permite as
# MAGIC duas coisas.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. `badge_score` decide a cor sozinho — e é preciso saber onde

# COMMAND ----------

valores = [95, 80, 62, 45, 10]
displayHTML('<div style="font-family:Segoe UI">'
            + " ".join(badge_score(v) for v in valores) + "</div>")

for v in valores:
    print(f"  badge_score({v:3d}) -> {badge_score(v)}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC badge_score( 95) -> verde   (#EAF7EC / #2E7D32)
# MAGIC badge_score( 80) -> verde
# MAGIC badge_score( 62) -> amarelo (#FFF8E1 / #B26A00)
# MAGIC badge_score( 45) -> vermelho(#FDECEC / #B71C1C)
# MAGIC badge_score( 10) -> vermelho
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Os cortes ficam entre 80 e 62, e entre 62 e 45 — **e não estão
# MAGIC declarados em constante nomeada**. Quem quiser saber onde muda a cor lê o
# MAGIC corpo da função.
# MAGIC
# MAGIC Isso importa porque um selo de score é um **veredito**: 62 saindo amarelo
# MAGIC e 68 saindo verde é uma decisão de política, do mesmo tipo que o
# MAGIC `psi_threshold` do monitoramento — e lá o módulo se recusa a escolher
# MAGIC sozinho. Aqui ele escolhe, em silêncio.
# MAGIC
# MAGIC ## Dívida registrada: as cores não vêm de `constants`
# MAGIC
# MAGIC O verde daqui é `#2E7D32`; o `VERDE` de `constants.colors` é `#8DC63F`. São
# MAGIC cores diferentes, e existe ainda um terceiro conjunto em
# MAGIC `constants.styles` (`STYLE_BADGE_OK`), que este módulo também não usa.
# MAGIC
# MAGIC **Três definições de "verde de selo" convivendo na mesma biblioteca.** Como
# MAGIC em `styles`, unificar muda o que já está publicado, e fica para a etapa 2 —
# MAGIC mas quem for escolher precisa saber que são três, não duas.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem o número ao lado.** O selo resume; ele não substitui a evidência. "🔴 Crítico" sem o valor é opinião com cor.
# MAGIC - **Escolhendo o tipo na mão, caso a caso.** Se o limiar é decisão, ele vira constante nomeada — não argumento decidido no calor da análise.
# MAGIC - **Em série longa.** Trinta selos numa página deixam de destacar. Selo é para o que precisa ser visto primeiro.
