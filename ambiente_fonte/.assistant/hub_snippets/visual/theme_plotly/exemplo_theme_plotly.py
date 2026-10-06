# Databricks notebook source
# MAGIC %md
# MAGIC # `visual.theme_plotly` — o tema, aplicado ao gráfico e não copiado nele
# MAGIC
# MAGIC **O problema.** Cada gráfico com seu `update_layout` produz vinte variações de fonte, margem e cor de fundo no mesmo relatório. E a decisão de mostrar quantos pontos foram plotados, que é a mais importante, ninguém repete.
# MAGIC
# MAGIC **O que este objeto oferece.** Aplica o tema institucional a uma figura Plotly, com subtítulo, fonte e a contagem de pontos declarada no rodapé.

# MAGIC
# MAGIC **Antes de executar:** consulte o [README deste objeto](README.md) para entender o conceito, os requisitos e os efeitos do exemplo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | confira as dependências e a compatibilidade descritas no README; não há equivalência universal entre runtimes |
# MAGIC | Bibliotecas | Plotly e NumPy disponíveis; para o tema explícito, `jsonschema` e `referencing` preparados conforme `hub_snippets/requirements-temas.txt`; o notebook não instala pacotes |
# MAGIC | Dados | sintéticos, gerados aqui |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.visual.theme_plotly import aplicar_tema, get_tema_eda, registrar_template_plotly

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. O mesmo gráfico, sem e com o tema

# COMMAND ----------

import numpy as np
import plotly.graph_objects as go

rng = np.random.default_rng(42)
x = np.arange(24)
y = 100 + np.cumsum(rng.normal(2, 6, 24))

figura = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", name="volume"))
figura.update_layout(title="Sem tema — o padrão do Plotly")
figura.show()

# COMMAND ----------

figura2 = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", name="volume"))
figura2.update_layout(title="Com tema")
aplicar_tema(
    figura2,
    subtitulo="Volume mensal, base sintética",
    fonte="hub_snippets.testing.fixtures",
    n=len(x),
)
figura2.show()

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** As figuras mostram os mesmos dados. O rodapé desta chamada menciona fixtures, mas a série foi gerada por NumPy. Fonte e N são declarações do autor; o helper não verifica procedência nem contagem. Confira esses rótulos antes de compartilhar.
# MAGIC
# MAGIC Um gráfico não informa, por sua aparência, se representa uma amostra
# MAGIC ou toda a base. Declare esse contexto e a unidade de N quando pertinente.
# MAGIC O helper não infere população, contagem ou origem a partir dos traces.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O que há dentro do tema

# COMMAND ----------

tema = get_tema_eda()
for chave, valor in tema.items():
    texto = str(valor)
    print(f"  {chave:20s} {texto[:88]}{'...' if len(texto) > 88 else ''}")

# O print acima corta em 88 caracteres, e o colorway tem 110 — a lista sai
# truncada. Como a afirmacao da leitura e sobre o NUMERO de cores, ele precisa
# ser impresso inteiro.
print("")
print(f"cores no colorway: {len(tema['colorway'])}")
print(f"colorway completo: {tema['colorway']}")

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC template     plotly_white
# MAGIC font         {'family': 'Segoe UI, Roboto, sans-serif', 'size': 12, 'color': '#333333'}
# MAGIC title        {'font': {'size': 16, 'color': '#005CA9'}, 'x': 0.01, 'xanchor': 'left'}
# MAGIC colorway             ['#005CA9', '#F7941D', '#6CBDE1', '#333333', '#8DC63F', '#C4262E', '#7B2D8B', '#00A79D',...
# MAGIC height       450
# MAGIC width        900
# MAGIC margin       {'l': 60, 'r': 30, 't': 70, 'b': 60}
# MAGIC legend               {'orientation': 'h', 'yanchor': 'bottom', 'y': -0.25, 'xanchor': 'center', 'x': 0.5}
# MAGIC
# MAGIC cores no colorway: 10
# MAGIC colorway completo: ['#005CA9', '#F7941D', '#6CBDE1', '#333333', '#8DC63F', '#C4262E', '#7B2D8B', '#00A79D', '#F15A29', '#A7A9AC']
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Repare que o `colorway` sai **truncado** no bloco acima: o
# MAGIC `print` corta em 88 caracteres e a lista tem 110. A segunda célula existe
# MAGIC por isso — a afirmação é sobre o número de cores, e ela precisa ser
# MAGIC conferível. São **dez**, e são as de `PALETA_CATEGORICA`.
# MAGIC
# MAGIC O módulo reutiliza `PALETA_CATEGORICA` e `CINZA_ESCURO` de `constants.colors`. Aplicar tema não substitui cores explicitamente definidas nos traces.
# MAGIC
# MAGIC Duas escolhas de layout merecem nota. O **título alinhado à esquerda**
# MAGIC (`x: 0.01`) segue a leitura da página em vez de centralizar; e a
# MAGIC **legenda horizontal embaixo** (`y: -0.25`) devolve ao gráfico a largura
# MAGIC que uma legenda lateral consome — o que importa quando há série com nome
# MAGIC longo, que é o caso de quase toda categoria de negócio.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Com N sem significado.** Declare qual contagem é pertinente ao gráfico e seu recorte; nem todo gráfico exige N. A função aceita o rótulo, mas não o verifica.
# MAGIC - **Depois de ajustes que precisa preservar.** A aplicação redefine chaves de layout. Aplique o tema primeiro e faça as customizações específicas depois; reaplicar pode desfazê-las e duplicar o rodapé.
# MAGIC - **Sem conferir o destino.** A função pode ser usada fora do Databricks, mas fontes, dimensões e renderização precisam ser avaliadas no ambiente final.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Referência resolvida, aplicação explícita
# MAGIC
# MAGIC A referência notebook empacotada é demonstração, não um tema operacional aprovado.

# COMMAND ----------

import plotly.io as pio
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido, get_tema_plotly

referencia = load_reference_theme("notebook")
default_antes = pio.templates.default

figura3 = go.Figure(go.Bar(x=["A", "B", "C"], y=[10, 12, 9]))
figura3.update_layout(title="Referência V03 — exemplo sintético")
aplicar_tema_resolvido(figura3, referencia, fonte="dados sintéticos", n=3)

config_referencia = get_tema_plotly(referencia)
config_legado = get_tema_eda()
assert config_referencia == config_legado
assert pio.templates.default == default_antes
figura3.show()

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** A referência `legado_notebook` preserva o layout legado. A aplicação afeta apenas `figura3`, sem mudar `pio.templates.default`. Para criar uma proposta, siga o [README](README.md). O adaptador aceita somente `notebook/light`; `dark` e `high_contrast` são recusados.
