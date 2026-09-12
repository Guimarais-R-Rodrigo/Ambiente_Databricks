# Databricks notebook source
# MAGIC %md
# MAGIC # `constants.colors` — a paleta, e por que ela é fechada
# MAGIC
# MAGIC **O problema.** Cada notebook escolhendo cor por conta própria produz um relatório onde a mesma categoria muda de cor entre páginas, e onde 'vermelho' às vezes significa alerta e às vezes é só a terceira série do gráfico.
# MAGIC
# MAGIC **O que este objeto oferece.** Vinte e duas constantes: cores institucionais, paletas prontas e cores com significado declarado.

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
# MAGIC | Diferença Free × trabalho | compatibilidade do destino não revalidada nesta rodada |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.constants.colors import COR_ALERTA, COR_NEGATIVO, COR_NEUTRO, COR_POSITIVO, PALETA_CATEGORICA, PALETA_DIVERGENTE, PALETA_SEQUENCIAL

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. As três paletas, e para que serve cada uma

# COMMAND ----------

for nome, paleta in [("CATEGORICA", PALETA_CATEGORICA),
                     ("SEQUENCIAL", PALETA_SEQUENCIAL),
                     ("DIVERGENTE", PALETA_DIVERGENTE)]:
    print(f"{nome:12s} {len(paleta):2d} cores  {paleta}")

# COMMAND ----------

# O valor de uma paleta so aparece quando ela e vista. displayHTML existe no
# notebook; num modulo importado, nao — e por isso o helper devolve string.
def amostra(paleta, rotulo):
    quadrados = "".join(
        f'<span style="display:inline-block;width:44px;height:44px;'
        f'background:{c};border:1px solid #ccc;" title="{c}"></span>'
        for c in paleta
    )
    return f'<div style="margin:8px 0"><b>{rotulo}</b><br>{quadrados}</div>'

displayHTML(
    amostra(PALETA_CATEGORICA, "PALETA_CATEGORICA — séries sem ordem")
    + amostra(PALETA_SEQUENCIAL, "PALETA_SEQUENCIAL — intensidade crescente")
    + amostra(PALETA_DIVERGENTE, "PALETA_DIVERGENTE — desvio em torno de um centro")
)

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC CATEGORICA   10 cores  ['#005CA9', '#F7941D', '#6CBDE1', '#333333', '#8DC63F',
# MAGIC                         '#C4262E', '#7B2D8B', '#00A79D', '#F15A29', '#A7A9AC']
# MAGIC SEQUENCIAL    5 cores  ['#E6F0FA', '#99C2E8', '#4D94D6', '#005CA9', '#003D73']
# MAGIC DIVERGENTE    5 cores  ['#C4262E', '#F7941D', '#FFB800', '#8DC63F', '#005CA9']
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** As três não são intercambiáveis, e trocar uma pela outra muda a
# MAGIC afirmação do gráfico:
# MAGIC
# MAGIC | Paleta | Quando | O que ela afirma |
# MAGIC |---|---|---|
# MAGIC | **Categórica** (10) | séries sem ordem — UF, produto, canal | "estas coisas são diferentes" |
# MAGIC | **Sequencial** (5) | intensidade que só cresce — volume, contagem | "isto é mais que aquilo" |
# MAGIC | **Divergente** (5) | desvio em torno de um centro — variação, resíduo | "isto está acima e aquilo abaixo" |
# MAGIC
# MAGIC Para desvios em torno de zero, uma escala divergente pode comunicar os
# MAGIC lados do centro melhor que uma sequência de intensidade. O código que
# MAGIC monta o gráfico precisa definir domínio e centro: a lista não faz isso.
# MAGIC
# MAGIC A categórica oferece dez cores. Com quinze categorias, o consumidor precisa
# MAGIC decidir a estratégia: agrupar, dividir o gráfico ou acrescentar codificação
# MAGIC textual. O módulo não repete cores nem agrupa automaticamente.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. As cores semânticas são um contrato, não uma sugestão

# COMMAND ----------

for nome, valor in [("COR_POSITIVO", COR_POSITIVO), ("COR_NEGATIVO", COR_NEGATIVO),
                    ("COR_NEUTRO", COR_NEUTRO), ("COR_ALERTA", COR_ALERTA)]:
    print(f"  {nome:16s} {valor}")

# O texto NAO e branco em todos: dois destes fundos reprovam contraste com
# branco. A celula seguinte mede.
def contraste_ok(hexa):
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
    canal = [(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4) for c in (r, g, b)]
    lum = 0.2126 * canal[0] + 0.7152 * canal[1] + 0.0722 * canal[2]
    return (1.05 / (lum + 0.05)) >= 4.5  # branco sobre a cor, mínimo AA

displayHTML("".join(
    f'<span style="background:{v};color:{"#fff" if contraste_ok(v) else "#1A1A1A"};'
    f'padding:6px 14px;margin-right:8px;border-radius:4px;font-family:Segoe UI">{n}</span>'
    for n, v in [("POSITIVO", COR_POSITIVO), ("NEGATIVO", COR_NEGATIVO),
                 ("NEUTRO", COR_NEUTRO), ("ALERTA", COR_ALERTA)]
))

print("contraste do branco sobre cada fundo (mínimo AA = 4,5:1):")
for n, v in [("COR_POSITIVO", COR_POSITIVO), ("COR_NEGATIVO", COR_NEGATIVO),
             ("COR_NEUTRO", COR_NEUTRO), ("COR_ALERTA", COR_ALERTA)]:
    r, g, b = (int(v[i:i + 2], 16) / 255 for i in (1, 3, 5))
    canal = [(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4) for c in (r, g, b)]
    lum = 0.2126 * canal[0] + 0.7152 * canal[1] + 0.0722 * canal[2]
    razao = 1.05 / (lum + 0.05)
    print(f"  {n:14s} {v}  {razao:5.2f}:1  {'ok' if razao >= 4.5 else 'REPROVA'}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC   COR_POSITIVO     #8DC63F
# MAGIC   COR_NEGATIVO     #C4262E
# MAGIC   COR_NEUTRO       #6C757D
# MAGIC   COR_ALERTA       #FFB800
# MAGIC contraste do branco sobre cada fundo (mínimo AA = 4,5:1):
# MAGIC   COR_POSITIVO   #8DC63F   2.04:1  REPROVA
# MAGIC   COR_NEGATIVO   #C4262E   5.73:1  ok
# MAGIC   COR_NEUTRO     #6C757D   4.69:1  ok
# MAGIC   COR_ALERTA     #FFB800   1.73:1  REPROVA
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Estas quatro existem para que "verde" signifique a mesma coisa em
# MAGIC todo o material. É um contrato barato de manter e caro de perder: um
# MAGIC relatório em que vermelho às vezes é alerta e às vezes é só a sexta série
# MAGIC da paleta categórica ensina o leitor a ignorar a cor.
# MAGIC
# MAGIC **E há uma decisão de design que faltava neste notebook: contraste.**
# MAGIC Duas das quatro cores **reprovam** o mínimo AA (4,5:1) com texto branco —
# MAGIC `COR_ALERTA` em 1,73:1 e `COR_POSITIVO` em 2,04:1. São amarelo e verde
# MAGIC claros; branco em cima deles é praticamente ilegível.
# MAGIC
# MAGIC A regra que decorre disso: **`COR_ALERTA` e `COR_POSITIVO` são cores de
# MAGIC preenchimento — barra, ponto, borda —, nunca fundo para texto branco.**
# MAGIC Para selo ou chip com essas duas, o texto vai em `TEXTO_PRINCIPAL`. A
# MAGIC célula acima faz essa escolha sozinha, medindo antes de pintar.
# MAGIC
# MAGIC Isso é diferente de daltonismo, que o "quando não usar" menciona: contraste
# MAGIC é aferível no valor, e portanto não tem desculpa para ficar sem verificação.
# MAGIC
# MAGIC Repare, por fim, que `COR_POSITIVO` **é** o `VERDE` da paleta categórica, e
# MAGIC `COR_NEGATIVO` **é** o `VERMELHO`. Ou seja, um gráfico categórico com seis
# MAGIC ou mais séries vai usar as duas cores semânticas como cor qualquer. Não há
# MAGIC como o módulo evitar isso — mas vale saber, porque é onde o contrato se
# MAGIC rompe sozinho.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Como distinção exclusivamente cromática de muitas categorias.** A lista tem dez cores; avalie agrupamento ou outra codificação antes de atribuí-las.
# MAGIC - **Para destacar desvios positivos e negativos sem centro definido.** Avalie a divergente e configure o centro no gráfico; nenhum desses passos é automático.
# MAGIC - **Como sistema de acessibilidade.** Nenhuma destas paletas foi verificada para daltonismo. Cor sozinha nunca deve carregar a informação.
