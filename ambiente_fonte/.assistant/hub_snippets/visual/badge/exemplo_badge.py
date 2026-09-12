# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.badge` — o selo que resume um veredito
# MAGIC
# MAGIC **O problema.** Um relatório com trinta números pede que o leitor decida, número a número, se aquilo é bom. A maior parte das pessoas não decide: rola até o fim e pergunta "e aí, passou?".
# MAGIC
# MAGIC **O que este objeto oferece.** Três selos em HTML — status com semáforo, score com faixa e destaque em linha — para responder essa pergunta antes que ela seja feita.

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
# MAGIC | Dados | textos e valores definidos nas células; nenhuma tabela externa |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |

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
# MAGIC   badge_score( 95) -> <span style="...background:#EAF7EC; color:#2E7D32;...">Score: 95/100</span>
# MAGIC   badge_score( 80) -> <span style="...background:#EAF7EC; color:#2E7D32;...">Score: 80/100</span>
# MAGIC   badge_score( 62) -> <span style="...background:#FFF8E1; color:#B26A00;...">Score: 62/100</span>
# MAGIC   badge_score( 45) -> <span style="...background:#FDECEC; color:#B71C1C;...">Score: 45/100</span>
# MAGIC   badge_score( 10) -> <span style="...background:#FDECEC; color:#B71C1C;...">Score: 10/100</span>
# MAGIC
# MAGIC (o `style` completo foi encurtado com reticências; o resto é literal)
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Os cortes são `valor/max >= 0.8` para verde e `>= 0.5` para
# MAGIC amarelo — com o `max=100` do padrão, **80 e 50**. Um score 79 sai amarelo;
# MAGIC 80 sai verde.
# MAGIC
# MAGIC **E eles não estão declarados em constante nomeada**: quem quiser saber
# MAGIC onde a cor muda lê o corpo da função. Isso importa porque um selo de score
# MAGIC é um **veredito**, do mesmo tipo que o `psi_threshold` do monitoramento —
# MAGIC e lá o módulo se recusa a decidir sozinho, exigindo a política declarada.
# MAGIC Aqui ele decide, em silêncio, e a decisão fica a duas casas decimais de
# MAGIC distância de quem lê o selo.
# MAGIC
# MAGIC O texto é arredondado, mas o corte usa o valor original: `79.6` pode
# MAGIC aparecer como “80/100” ainda no estilo de atenção. Verifique o número
# MAGIC sem arredondamento antes de interpretar uma faixa. O helper também não
# MAGIC recusa máximo zero ou valores fora do intervalo; o chamador deve validar.
# MAGIC O contraste do estilo de atenção é uma limitação documentada no README,
# MAGIC não corrigida por esta sprint documental.
# MAGIC
# MAGIC ## Dívida registrada: as cores não vêm de `constants`
# MAGIC
# MAGIC O verde daqui é `#2E7D32`; o `VERDE` de `constants.colors` é `#8DC63F`.
# MAGIC São **três sítios de declaração e dois valores**: `constants.styles`
# MAGIC (`STYLE_BADGE_OK`) tem estilos de mesma finalidade, escritos separadamente, e
# MAGIC nenhum dos dois usa o `VERDE` oficial.
# MAGIC
# MAGIC A distinção importa para quem for unificar: uma unificação de `styles` e `badge` precisa
# MAGIC conferir contratos e apresentação; alinhar os dois ao `VERDE` de `colors`
# MAGIC **troca as cores dos estados alinhados**. Ambas exigem revisão de produto.
# MAGIC
# MAGIC O inventário dos doze módulos com cor redeclarada está em
# MAGIC `PLANO_HUB.md` §12.2.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sem o número ao lado.** O selo resume; ele não substitui a evidência. "🔴 Crítico" sem o valor é opinião com cor.
# MAGIC - **Escolhendo o tipo na mão, caso a caso.** Se o limiar é decisão, ele vira constante nomeada — não argumento decidido no calor da análise.
# MAGIC - **Em série longa.** Trinta selos numa página deixam de destacar. Selo é para o que precisa ser visto primeiro.
