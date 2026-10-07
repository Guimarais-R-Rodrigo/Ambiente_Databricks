# Databricks notebook source
# MAGIC %md
# MAGIC # `comparar_tabelas` — duas versões da mesma base, e onde elas divergem
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
# MAGIC | Escrita | **sim, overwrite** — sobrescreve `workspace.default.hub_exemplo_clientes_v1` e `workspace.default.hub_exemplo_clientes_v2` |
# MAGIC | Diferença Free × trabalho | fonte real exige autorização, revisão de dados sensíveis e contrato próprio; este preparo é sintético |

# COMMAND ----------
# MAGIC %md
# MAGIC **Antes de executar a Parte 1 ou Run all:** o preparo sobrescreve `workspace.default.hub_exemplo_clientes_v1` e `workspace.default.hub_exemplo_clientes_v2`
# MAGIC com `mode("overwrite")`. Confira destino e autorização; pode substituir dados
# MAGIC existentes. Você pode usar o briefing sem executar o preparo. O preparo não executa a reconciliação.
# MAGIC
# MAGIC ## Parte 1 — preparo: a base que o prompt vai citar

# COMMAND ----------

import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_snippets.testing import fixtures

# Duas versões da mesma base: a v2 tem mais linhas e mais nulos, como
# aconteceria depois de uma recarga parcial.
v1 = fixtures.base_tabular(n=4000, seed=42, pct_nulos_renda=0.04)
v2 = fixtures.base_tabular(n=4200, seed=42, pct_nulos_renda=0.09)
v1.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes_v1")
v2.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes_v2")

for nome, df in (("v1", v1), ("v2", v2)):
    nulos = df.filter("renda is null").count()
    print(f"{nome}: {df.count()} linhas | renda nula: {nulos} ({100*nulos/df.count():.1f}%)")

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** As duas diferem em volume e em taxa de nulo — e nenhuma das duas diferenças aparece se você só comparar esquema. É por isso que o prompt pede tolerâncias: sem elas, toda diferença vira alerta e nenhuma vira decisão.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC O briefing em branco está em [`comparar_tabelas.md`](./comparar_tabelas.md), com um
# MAGIC placeholder por decisão que o pedido informal costuma esquecer. Abaixo ele
# MAGIC vai **preenchido** para a base da Parte 1 — copie o bloco inteiro e cole
# MAGIC num chat novo do Genie Code.
# MAGIC
# MAGIC Este prompt não declara skill no cabeçalho, de propósito: a comparação pode ser de qualidade ou de distribuição, e a escolha muda conforme o `TIPO_COMPARACAO`. É um bom caso para observar o roteamento.

# COMMAND ----------
# MAGIC %md
# MAGIC ```text
# MAGIC Compare os dois recursos anexados de modo reprodutível e somente leitura.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Recurso A: workspace.default.hub_exemplo_clientes_v1
# MAGIC - Recurso B: workspace.default.hub_exemplo_clientes_v2
# MAGIC - Objetivo/tipo de comparação: conteúdo e distribuição — o esquema é o mesmo
# MAGIC - Unidade de análise: uma linha por cliente e data de referência
# MAGIC - Chaves de correspondência: `id_cliente` + `dt_referencia`
# MAGIC - Coluna temporal e período: `dt_referencia`, 2026-01 a 2026-06
# MAGIC - Colunas críticas: `renda` e `alvo`; as demais em visão geral
# MAGIC - Tolerâncias: proponha, separando o que é ruído de recarga do que é mudança real
# MAGIC - Filtros equivalentes: nenhum
# MAGIC - Restrições: serverless; a comparação precisa rodar em menos de 3 minutos
# MAGIC
# MAGIC FLUXO
# MAGIC 1. Verifique que A e B foram anexadas e confirme schemas, tipos e granularidade.
# MAGIC 2. Compare cobertura temporal, contagens, chaves, duplicidade, colunas ausentes,
# MAGIC    mudanças de tipo, nulos e estatísticas relevantes.
# MAGIC 3. Faça reconciliação por chave com categorias: somente A, somente B, iguais e
# MAGIC    divergentes. Antes, valide que o join não é muitos-para-muitos inesperado.
# MAGIC 4. Para números, use tolerâncias absolutas/relativas explícitas; para timestamps,
# MAGIC    declare timezone e precisão; para strings, não normalize silenciosamente.
# MAGIC 5. Em alto volume, use Spark SQL/PySpark, pruning e agregações. Não colete registros
# MAGIC    completos ao driver e não exponha valores sensíveis.
# MAGIC 6. Não altere tabelas. Qualquer proposta de correção deve ficar separada da análise.
# MAGIC
# MAGIC CONTRATO DE SAÍDA
# MAGIC - Veredito resumido: compatível, compatível com ressalvas ou incompatível.
# MAGIC - Matriz de diferenças de schema e scorecard de conteúdo.
# MAGIC - Métricas de reconciliação com numeradores, denominadores e taxas.
# MAGIC - Top diferenças priorizadas, causas prováveis marcadas como hipóteses.
# MAGIC - Código executável e parametrizado para repetir a comparação.
# MAGIC - Limitações e recomendação de aceite/rejeição sem tomar a decisão pelo usuário.
# MAGIC
# MAGIC VALIDAÇÃO FINAL
# MAGIC - Confirme filtros idênticos e ausência de multiplicação pelo join.
# MAGIC - Inclua nulos nas comparações e explique tolerâncias.
# MAGIC - Declare contagens antes/depois e o escopo efetivamente lido.
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
# MAGIC 1. Se o preparo for necessário, confirme destino e autorização: ele sobrescreve `workspace.default.hub_exemplo_clientes_v1` e `workspace.default.hub_exemplo_clientes_v2`.
# MAGIC 2. Abra um **chat novo** no Genie Code e cole o bloco da Parte 2.
# MAGIC 3. Cole a resposta aqui, em markdown, com a data da captura.
# MAGIC 4. Registre contexto e skill selecionados com evidência disponível.
# MAGIC    Relato do assistente não comprova sozinho leitura, importação, chamada
# MAGIC    ou conclusão; confira os artefatos exigidos pela rota da skill.
# MAGIC 5. Comente: o que o assistente fez bem, e **o que ele deixou de fora**.
# MAGIC    A segunda metade é a que ensina.
# MAGIC
# MAGIC Skill esperada aqui: `hub-ml-eda-profissional` ou `hub-ml-validacao-estatistica`.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Sem tolerância declarada.** Duas cargas nunca são idênticas; sem limite, o resultado é uma lista de diferenças irrelevantes.
# MAGIC - **Para validar migração sem chave.** Se a chave não é confiável, a comparação linha a linha não significa nada.
# MAGIC - **Como prova de que a carga está certa.** Ele mostra o que mudou, não se o que mudou deveria ter mudado.
