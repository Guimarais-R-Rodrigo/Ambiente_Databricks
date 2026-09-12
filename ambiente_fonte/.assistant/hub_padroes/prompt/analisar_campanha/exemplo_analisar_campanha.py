# Databricks notebook source
# MAGIC %md
# MAGIC [Conceito, requisitos e limites deste exemplar](README.md).
# MAGIC
# MAGIC # `analisar_campanha` — o prompt sendo usado de verdade
# MAGIC
# MAGIC **Por que este notebook é diferente dos outros.** Um prompt não executa:
# MAGIC ele é um texto para colar num chat do Genie Code, e a resposta vem de uma
# MAGIC interação que notebook nenhum reproduz.
# MAGIC
# MAGIC O formato é, então, de três partes:
# MAGIC
# MAGIC 1. **Preparo executável** — cria a base a que o prompt se refere, para que
# MAGIC    quem lê possa colar o prompt e obter uma resposta de verdade.
# MAGIC 2. **O prompt preenchido** — o texto exato, sem placeholders.
# MAGIC 3. **A resposta real**, capturada num chat, com comentário sobre o que
# MAGIC    observar nela.
# MAGIC
# MAGIC A parte 3 exige uma pessoa. Não há como gerá-la aqui, e resposta inventada
# MAGIC seria pior que resposta nenhuma.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime |
# MAGIC | Dados | reutiliza `workspace.default.hub_exemplo_campanha` |
# MAGIC | Escrita | nenhuma |
# MAGIC | Interação humana | **sim** — a parte 3 exige um chat novo do Genie Code |

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 1 — preparo
# MAGIC
# MAGIC A base é criada pelo notebook do snippet
# MAGIC `hub_padroes/snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha`. Rode-o antes,
# MAGIC ou execute a célula abaixo para conferir que a tabela existe.

# COMMAND ----------

from pyspark.sql import functions as F

TABELA = "workspace.default.hub_exemplo_campanha"

campanha = spark.table(TABELA)
print(f"{TABELA}: {campanha.count()} linhas")
display(
    campanha.groupBy("segmento")
    .agg(F.count("*").alias("contatados"),
         F.round(100 * F.avg("respondeu"), 2).alias("taxa_pct"))
    .orderBy(F.desc("taxa_pct"))
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 2 — o prompt preenchido
# MAGIC
# MAGIC Abra um **chat novo** do Genie Code e cole exatamente isto:
# MAGIC
# MAGIC ```text
# MAGIC Analise o resultado da campanha de relacionamento armazenada em
# MAGIC workspace.default.hub_exemplo_campanha.
# MAGIC
# MAGIC CONTEXTO
# MAGIC - Unidade de análise: um cliente contatado por campanha.
# MAGIC - Colunas: id_cliente, segmento, canal, dt_contato, respondeu (1 = respondeu).
# MAGIC - Período: junho de 2026, campanha única.
# MAGIC - Decisão que depende disto: para onde direcionar o orçamento da próxima
# MAGIC   campanha, que atende cerca de 15.000 clientes.
# MAGIC
# MAGIC O QUE PRECISO
# MAGIC 1. Taxa de resposta por segmento e por canal.
# MAGIC 2. Uma recomendação de priorização: quais segmentos devem receber a maior
# MAGIC    parte dos 15.000 contatos da próxima campanha, e por quê.
# MAGIC 3. O que nestes dados não sustenta a recomendação — o que você não conseguiu
# MAGIC    concluir com o que existe aqui.
# MAGIC
# MAGIC FORMATO
# MAGIC - Código PySpark reproduzível, com a saída que você obteve.
# MAGIC - Uma síntese executiva de no máximo 8 linhas, em português, para quem decide
# MAGIC   orçamento e não lê código.
# MAGIC ```

# COMMAND ----------
# MAGIC %md
# MAGIC ## Parte 3 — a resposta real
# MAGIC
# MAGIC Capturada em 16 ago 2026, no Databricks Free, em chat novo e sem `@menção`.
# MAGIC
# MAGIC ### Roteamento
# MAGIC
# MAGIC O assistente considerou carregar as skills de validação estatística e de
# MAGIC EDA e **decidiu não fazê-lo**, com o argumento de que o pedido era uma
# MAGIC análise direta e não uma EDA completa. Carregou a skill nativa
# MAGIC `data-sampling` da Databricks.
# MAGIC
# MAGIC A decisão é defensável, e é a razão de este prompt declarar a skill
# MAGIC recomendada no cabeçalho: depender do roteamento automático para um pedido
# MAGIC ambíguo é apostar.
# MAGIC
# MAGIC ### O que ele fez bem
# MAGIC
# MAGIC - Validou grão, nulos, período e domínio do alvo **antes** de medir.
# MAGIC - Marcou o segmento de 28 contatos como amostra mínima e **o excluiu da
# MAGIC   recomendação**, com o argumento operacional correto: "apenas 28 clientes,
# MAGIC   insuficiente para alocar orçamento".
# MAGIC - No cruzamento segmento × canal, percebeu sozinho que as células daquele
# MAGIC   segmento tinham de 6 a 9 contatos.
# MAGIC - Listou limitações reais: ausência de custo, de receita por resposta, de
# MAGIC   capacidade de atendimento e de histórico.
# MAGIC
# MAGIC ### O que ficou de fora
# MAGIC
# MAGIC | Lacuna | Consequência |
# MAGIC |---|---|
# MAGIC | Nunca quantificou a precisão | chamou o segmento de "amostra mínima" por julgamento; o leitor fica sem saber onde está o corte, e o segmento de 940 contatos permanece indefinido |
# MAGIC | Assumiu que recontatar as mesmas pessoas reproduz a taxa | recomendou contatar exatamente os já contatados em junho; resposta a um segundo contato não é o mesmo processo, e isso não entrou na lista de limitações |
# MAGIC | Dois números imprecisos | "~955 respostas" onde são 947; "taxa 50% inferior" onde a diferença relativa é 39,4% |
# MAGIC
# MAGIC ### Trecho da síntese executiva que ele produziu
# MAGIC
# MAGIC > Campanha junho/2026: 45.868 clientes contatados, 2.156 respostas (taxa
# MAGIC > geral 4,7%). Recomendação para os 15.000 contatos da próxima campanha:
# MAGIC > priorize Aposentado (2.600), Universitário (4.100) e Massa Alta (8.200),
# MAGIC > totalizando 14.900 clientes. […] Private tem taxa de 42,86%, mas apenas
# MAGIC > 28 clientes na base, insuficiente para alocar orçamento.
# MAGIC
# MAGIC ### O que este registro ensina
# MAGIC
# MAGIC Uma ferramenta competente acertou o essencial e deixou aberta a armadilha
# MAGIC que ninguém vê. É por isso que o prompt tem a seção "o que conferir na
# MAGIC resposta": ela não existe por desconfiança do assistente, e sim porque as
# MAGIC lacunas dele são sistemáticas e previsíveis — e portanto verificáveis por
# MAGIC quem lê.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este prompt
# MAGIC
# MAGIC - **Quando não houver decisão em jogo.** Ele é desenhado em torno de uma
# MAGIC   restrição de orçamento; sem ela, vira pedido de tabela.
# MAGIC - **Para atribuir causa.** Descreve o que aconteceu. Sem grupo de controle,
# MAGIC   nenhuma análise separa o efeito da oferta do efeito de quem foi escolhido.
# MAGIC - **Sobre campanha ainda em curso.** A base precisa estar fechada; taxa
# MAGIC   parcial de campanha em andamento compara períodos de exposição
# MAGIC   diferentes.
