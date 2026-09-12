# Databricks notebook source
# MAGIC %md
# MAGIC [Conceito, requisitos e limites deste exemplar](README.md).
# MAGIC
# MAGIC # `taxa_resposta_campanha` — taxa de resposta com a precisão junto
# MAGIC
# MAGIC **O problema.** Uma campanha terminou e alguém precisa decidir para onde
# MAGIC vai o orçamento da próxima. A tabela de taxas por segmento parece resolver:
# MAGIC ordena, olha o topo, prioriza. É o caminho que quase todo mundo segue, e
# MAGIC ele esconde uma diferença que muda a decisão — duas taxas com a mesma cara
# MAGIC podem estar apoiadas em 28 e em 30.000 contatos.
# MAGIC
# MAGIC **O que este helper faz.** Devolve a taxa acompanhada do intervalo de
# MAGIC confiança e da largura dele, que é a resposta direta para "com que precisão
# MAGIC eu sei este número?".
# MAGIC
# MAGIC > Este é um exemplo dos **padrões do Hub**, não um helper de produção.
# MAGIC > Serve de referência de forma para quem vai criar um snippet novo.

# COMMAND ----------
# MAGIC %md
# MAGIC ## O que este notebook assume do ambiente
# MAGIC
# MAGIC | Item | Exigência |
# MAGIC |---|---|
# MAGIC | Compute | serverless ou clássico, indiferente |
# MAGIC | Bibliotecas | nenhuma além do runtime — **não instale nada** |
# MAGIC | Dados | tabela sintética criada pela célula de preparo, 100% gerada aqui |
# MAGIC | Escrita | cria `workspace.default.hub_exemplo_campanha`; nada mais é tocado |
# MAGIC | Diferença Free × trabalho | nenhuma conhecida |

# COMMAND ----------

# Preâmbulo do Hub: resolve o caminho da biblioteca pelo usuário logado. Estas
# três linhas abrem todo notebook do Hub — sem elas o import abaixo falha.
import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_padroes.snippet.taxa_resposta_campanha import MINIMO_PARA_DECISAO, taxa_resposta_campanha

print(f"biblioteca: /Workspace/Users/{usuario}/.assistant")
print(f"base mínima para decisão (padrão): {MINIMO_PARA_DECISAO}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Preparo — a base sintética
# MAGIC
# MAGIC Seis segmentos com tamanhos deliberadamente desiguais: de 28 a 30.000
# MAGIC contatos. É a desigualdade que torna o problema visível.

# COMMAND ----------

import datetime
import random

TABELA = "workspace.default.hub_exemplo_campanha"

# (segmento, contatados, taxa real de resposta usada no sorteio)
PERFIL = [
    ("Massa", 30000, 0.039),
    ("Massa alta", 8200, 0.052),
    ("Universitario", 4100, 0.071),
    ("Aposentado", 2600, 0.088),
    ("PJ pequeno", 940, 0.061),
    ("Private", 28, 0.320),
]

rng = random.Random(42)
inicio = datetime.date(2026, 6, 1)
linhas = []
i = 0
for segmento, n, taxa in PERFIL:
    for _ in range(n):
        i += 1
        linhas.append((
            f"cli{i:07d}",
            segmento,
            rng.choice(["app", "sms", "email", "telefone"]),
            inicio + datetime.timedelta(days=rng.randint(0, 29)),
            1 if rng.random() < taxa else 0,
        ))
rng.shuffle(linhas)

esquema = "id_cliente string, segmento string, canal string, dt_contato date, respondeu int"
spark.createDataFrame(linhas, esquema).write.mode("overwrite").saveAsTable(TABELA)
print(f"{TABELA}: {len(linhas)} linhas")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. O caminho que quase todo mundo segue
# MAGIC
# MAGIC Agrupa, calcula a taxa, ordena. Nada de errado no cálculo.

# COMMAND ----------

from pyspark.sql import functions as F

campanha = spark.table(TABELA)

ingenuo = (
    campanha.groupBy("segmento")
    .agg(
        F.count("*").alias("contatados"),
        F.sum("respondeu").alias("respostas"),
        F.round(100 * F.avg("respondeu"), 2).alias("taxa_pct"),
    )
    .orderBy(F.desc("taxa_pct"))
)
display(ingenuo)

# COMMAND ----------
# MAGIC %md
# MAGIC **Como ler.** O topo diz que `Private` responde a 42,9%, contra 3,9% de
# MAGIC `Massa` — onze vezes mais. Lido assim, a conclusão é óbvia e errada: mandar
# MAGIC o orçamento para `Private`.
# MAGIC
# MAGIC A tabela não é falsa. Ela é **incompleta**: a coluna `contatados` está ali,
# MAGIC mas nada no formato obriga a olhá-la antes de decidir, e nada indica quanto
# MAGIC de confiança cada linha merece.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. O mesmo cálculo, com a precisão junto

# COMMAND ----------

resultado = taxa_resposta_campanha(
    campanha,
    coluna_segmento="segmento",
    coluna_resposta="respondeu",
)
display(resultado)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. O que a precisão mostra — e o que ela **não** mostra
# MAGIC
# MAGIC Aqui está a parte que costuma ser ensinada errado.
# MAGIC
# MAGIC O intervalo de `Private` vai de aproximadamente **26,5% a 60,9%**. Ele
# MAGIC **não se sobrepõe** ao de nenhum outro segmento. Ou seja: a diferença é
# MAGIC estatisticamente real, mesmo com 28 contatos. Quem esperava que o intervalo
# MAGIC "derrubasse" a comparação estava errado — e essa expectativa é comum.
# MAGIC
# MAGIC O que o intervalo mostra é outra coisa: a **precisão**. A largura vai de
# MAGIC 0,4 ponto percentual no maior segmento a mais de 34 pontos no menor. Você
# MAGIC não sabe se a taxa de `Private` é 27% ou 61%, e planejar com 42,9% é
# MAGIC planejar com um número que a base não sustenta.
# MAGIC
# MAGIC E há um terceiro nível, que nenhuma estatística responde: **há 28 clientes
# MAGIC nesse segmento.** Mesmo a 61%, são 17 respostas. Numa campanha de 15.000
# MAGIC contatos, isso é irrelevante.
# MAGIC
# MAGIC | Leitura | Conclusão |
# MAGIC |---|---|
# MAGIC | Ingênua | "onze vezes melhor, mande tudo para lá" |
# MAGIC | Estatística | a diferença é real, mas a estimativa é imprecisa |
# MAGIC | Operacional | são 28 pessoas; o teto absoluto é ~17 respostas |
# MAGIC
# MAGIC **Significância não é relevância.** O efeito existe, é mensurável, e não
# MAGIC muda a decisão. É por isso que a coluna `decidivel` existe: ela responde à
# MAGIC pergunta operacional, que é a que interessa a quem aloca orçamento.

# COMMAND ----------

display(
    resultado.filter("decidivel")
    .select("segmento", "contatados", "taxa_pct", "largura_ic_pp")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. A recusa é comportamento, não acidente
# MAGIC
# MAGIC Nulo na coluna de resposta é ambíguo: pode ser "não respondeu" ou "falha de
# MAGIC registro". Tratá-lo como zero enviesa a taxa para baixo sem deixar rastro,
# MAGIC então o helper **falha** em vez de decidir sozinho.

# COMMAND ----------

from pyspark.sql import Row

suja = campanha.limit(100).unionByName(
    spark.createDataFrame([Row(
        id_cliente="cli9999999", segmento="Massa", canal="app",
        dt_contato=datetime.date(2026, 6, 15), respondeu=None,
    )], schema=campanha.schema)
)

try:
    taxa_resposta_campanha(suja, coluna_segmento="segmento")
except ValueError as erro:
    print(f"recusou, como deveria:\n  {erro}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Bloco canônico — quando a execução é impossível
# MAGIC
# MAGIC Nem todo notebook do Hub consegue executar no laboratório. Quando for o
# MAGIC caso, a célula **não** sai vazia nem com saída inventada: sai com este
# MAGIC bloco, dizendo o que seria executado e por que não foi.
# MAGIC
# MAGIC ```text
# MAGIC ⚠️ NÃO EXECUTADO
# MAGIC
# MAGIC O que rodaria : train_prophet(serie, horizonte=12)
# MAGIC Por que não   : prophet 1.1.5 falha em serverless com
# MAGIC                 "'Prophet' object has no attribute 'stan_backend'".
# MAGIC                 Não é defeito do módulo: o backend de inferência não
# MAGIC                 inicializa neste runtime.
# MAGIC Onde verificar: docs/testes/spark/README.md
# MAGIC O que falta   : uma combinação de versões que funcione no ambiente alvo.
# MAGIC ```
# MAGIC
# MAGIC Sem forma única, cada autor inventa a sua e o leitor não consegue
# MAGIC distinguir "não roda" de "ninguém tentou".

# COMMAND ----------
# MAGIC %md
# MAGIC ## Quando **não** usar este helper
# MAGIC
# MAGIC - **Quando os grupos não são independentes.** O intervalo pressupõe
# MAGIC   contatos independentes. Se a mesma pessoa aparece duas vezes, ou se o
# MAGIC   contato foi feito em ondas que se influenciam, a precisão sai otimista.
# MAGIC - **Para comparar mais de dois segmentos formalmente.** Olhar seis
# MAGIC   intervalos e escolher o maior é comparação múltipla disfarçada. Para
# MAGIC   afirmar diferença entre pares, use teste com correção.
# MAGIC - **Para projetar a próxima campanha sobre as mesmas pessoas.** Resposta a
# MAGIC   um segundo contato em poucas semanas não é o mesmo processo que a
# MAGIC   primeira. Esta é a armadilha que mais passa despercebida, inclusive por
# MAGIC   assistentes de código.
# MAGIC - **Como substituto de teste A/B.** Isto descreve o que aconteceu; não
# MAGIC   isola o efeito da oferta, do canal ou do momento.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Nota de revisão documental R01
# MAGIC
# MAGIC O limite superior do intervalo estima a taxa; não é teto absoluto de
# MAGIC respostas. `decidivel` verifica apenas o tamanho do grupo contra o
# MAGIC mínimo configurado. Não equivale a teste de hipótese, alocação ótima ou
# MAGIC autorização de uso. A interpretação histórica acima não foi usada
# MAGIC como evidência de execução nova nesta rodada; veja o README.
