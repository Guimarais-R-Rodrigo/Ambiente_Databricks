# Databricks notebook source
# MAGIC %md
# MAGIC # `constants.format_br` — número no padrão brasileiro, sem `locale`
# MAGIC
# MAGIC **O problema.** Formatar com locale depende da configuração do ambiente. Já `f"{x:,.1f}"` produz `1,234.5`: o número não mudou, mas seus separadores podem ser interpretados incorretamente em um relatório em português.
# MAGIC
# MAGIC **O que este objeto oferece.** Seis funções de formatação que produzem `3.375.674` e `92,8%` sem depender de configuração do sistema.

# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas abaixo são referências sintéticas observadas; não representam execução atual do seu ambiente.
# MAGIC
# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | o helper usa Python padrão; o preparo deste notebook exige sessão Spark disponível |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | valores escalares sintéticos; não lê uma tabela externa |
# MAGIC | Escrita | nenhuma; tudo em memória |
# MAGIC | Diferença Free × trabalho | compatibilidade no destino não homologada por testes Python locais |

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.constants.format_br import fmt_brl, fmt_dec, fmt_delta, fmt_int, fmt_n, fmt_pct

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. As seis funções, com o caso que cada uma resolve

# COMMAND ----------

print("fmt_int   ", fmt_int(3375674))
print("fmt_pct   ", fmt_pct(0.928), "| com casas=2:", fmt_pct(0.928, casas=2))
print("fmt_brl   ", fmt_brl(1234567.89))
print("fmt_dec   ", fmt_dec(0.8536), "| com casas=2:", fmt_dec(0.8536, casas=2))
print("fmt_delta ", fmt_delta(0.032), "|", fmt_delta(-0.017))
print("fmt_n     ", fmt_n(3375674), "|", fmt_n(3375674, sufixo=False))

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC fmt_int    3.375.674
# MAGIC fmt_pct    92,8% | com casas=2: 92,80%
# MAGIC fmt_brl    R$ 1.234.567,89
# MAGIC fmt_dec    0,8536 | com casas=2: 0,85
# MAGIC fmt_delta  +3,2 pp | -1,7 pp
# MAGIC fmt_n      3,4M | 3.375.674
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** Ponto separa milhar, vírgula separa decimal — o inverso do
# MAGIC padrão do Python, e é essa inversão que o módulo existe para resolver sem
# MAGIC `locale`.
# MAGIC
# MAGIC `fmt_n` é o único com duas personalidades: com `sufixo=True` ele abrevia
# MAGIC para **3,4M**, e com `False` escreve **3.375.674**. A abreviação serve para
# MAGIC cartão de KPI, onde o espaço é curto e a ordem de grandeza basta. Para
# MAGIC conferências exatas, preserve o valor original. `fmt_n` e a apresentação
# MAGIC `.0f` usada por `fmt_int` podem perder precisão em inteiros muito grandes.


# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. A armadilha do `input_scale` no percentual

# COMMAND ----------

# A mesma grandeza, escrita de duas formas — e a funcao nao consegue adivinhar
# qual e qual: 0,928 pode ser "92,8%" ou "0,9%".
print("taxa como razão  (0.928) ->", fmt_pct(0.928))
print("taxa como pontos (92.8)  ->", fmt_pct(92.8, input_scale="percent"))
print("")
print("e o erro silencioso, se a escala for declarada errada:")
print("  fmt_pct(92.8)                       ->", fmt_pct(92.8))
print("  fmt_pct(0.928, input_scale='percent') ->", fmt_pct(0.928, input_scale="percent"))
print("")
print("fmt_delta tem a MESMA pegadinha, e a unidade 'pp' engana:")
print("  fmt_delta(0.032) ->", fmt_delta(0.032), " (razão, como o fmt_pct espera)")
print("  fmt_delta(2.4)   ->", fmt_delta(2.4), " (alguém pensando em '2,4 pp')")
print("")
print("e a unidade 'bps' multiplica por 10.000, nao por 100:")
print("  fmt_delta(0.0005, 'bps') ->", fmt_delta(0.0005, "bps"))
print("  fmt_delta(0.005,  'bps') ->", fmt_delta(0.005, "bps"))

# COMMAND ----------
# MAGIC %md
# MAGIC Executado no laboratório, o resultado é:
# MAGIC
# MAGIC ```text
# MAGIC taxa como razão  (0.928) -> 92,8%
# MAGIC taxa como pontos (92.8)  -> 92,8%
# MAGIC
# MAGIC e o erro silencioso, se a escala for declarada errada:
# MAGIC   fmt_pct(92.8)                         -> 9280,0%
# MAGIC   fmt_pct(0.928, input_scale='percent') -> 0,9%
# MAGIC
# MAGIC fmt_delta tem a MESMA pegadinha, e a unidade 'pp' engana:
# MAGIC   fmt_delta(0.032) -> +3,2 pp  (razão, como o fmt_pct espera)
# MAGIC   fmt_delta(2.4)   -> +240,0 pp  (alguém pensando em '2,4 pp')
# MAGIC
# MAGIC e a unidade 'bps' multiplica por 10.000, nao por 100:
# MAGIC   fmt_delta(0.0005, 'bps') -> +5 bps
# MAGIC   fmt_delta(0.005,  'bps') -> +50 bps
# MAGIC ```
# MAGIC
# MAGIC **Como ler.** As duas primeiras linhas produzem o mesmo texto a partir de
# MAGIC entradas cem vezes diferentes. A função não tem como adivinhar qual escala
# MAGIC chegou — e é por isso que `input_scale` existe e não tem padrão silencioso
# MAGIC de detecção.
# MAGIC
# MAGIC **Os dois erros são silenciosos**, e é o que os torna caros: `9280,0%` é
# MAGIC absurdo e alguém percebe; **`0,9%` é plausível**, entra no relatório e
# MAGIC vira decisão. Uma taxa de resposta de 0,9% num material que deveria dizer
# MAGIC 92,8% não parece defeito — parece campanha ruim.
# MAGIC
# MAGIC **`fmt_delta` tem a mesma pegadinha e é mais fácil de errar**, porque a
# MAGIC unidade "pp" sugere que se passe pontos percentuais. Não: ele espera
# MAGIC **razão**, igual ao `fmt_pct`. Passar 2,4 pensando em "2,4 pp" devolve
# MAGIC **+240,0 pp**. A docstring diz (`-0.032 para -3.2pp`); a assinatura, não.
# MAGIC
# MAGIC **E `bps` multiplica por 10.000, não por 100** — o que é correto (um ponto
# MAGIC base é um centésimo de ponto percentual). `fmt_delta(0.0005, "bps")`
# MAGIC produz `+5 bps`; mantenha essa escala de entrada explícita ao conferir a saída.
# MAGIC
# MAGIC A defesa que funciona não é lembrar: é **nunca deixar a escala implícita no
# MAGIC nome da variável**. `taxa_resposta_ratio` e `delta_pp_ratio` são feios e
# MAGIC não deixam dúvida.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar
# MAGIC
# MAGIC - **Sobre coluna de DataFrame, linha a linha.** São funções de driver, para texto de relatório. Formatação em massa vai no Spark ou no `style.format` do pandas.
# MAGIC - **Antes de calcular.** Formatar devolve **string**; somar strings concatena texto, e misturar texto com números pode levantar erro.
# MAGIC - **Para substituir valores numéricos em dados de intercâmbio.** Preserve números para cálculo; texto formatado serve à apresentação ou a um contrato de exportação que o exija explicitamente.
