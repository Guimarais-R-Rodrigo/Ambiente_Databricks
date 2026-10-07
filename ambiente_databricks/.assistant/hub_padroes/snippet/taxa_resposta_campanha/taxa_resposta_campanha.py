# -*- coding: utf-8 -*-
"""Taxa de resposta de campanha por segmento, com a precisão da estimativa.

Este módulo é **material de referência dos padrões do Hub**, não um helper de
produção: ele existe para demonstrar a forma de um snippet. O tema é real o
bastante para que a demonstração não seja vazia, e simples o bastante para que a
atenção de quem lê sobre para a estrutura.

Por que uma taxa de resposta precisa de intervalo de confiança: a decisão que ela
sustenta é para onde mandar o orçamento da próxima campanha. Duas taxas iguais
apoiadas em 28 e em 30.000 contatos não sustentam a mesma decisão, e a tabela de
taxas sozinha não mostra essa diferença — as duas aparecem como um número com uma
casa decimal.

O intervalo usado é o de **Wilson**, e não o normal simples. Com taxa baixa e base
pequena, o normal produz limite inferior negativo, que é impossível para uma
proporção. Wilson não tem esse defeito e continua correto quando `p` se aproxima
de 0 ou 1 — situação comum em resposta de campanha, onde 4% é uma taxa boa.
"""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

# Base mínima abaixo da qual a estimativa não sustenta decisão de alocação. Não é
# uma lei estatística: é política, calibrável, e está aqui em vez de embutida na
# função justamente para que quem usa saiba que existe e possa mudar.
MINIMO_PARA_DECISAO = 100


def taxa_resposta_campanha(
    dados: DataFrame,
    *,
    coluna_segmento: str,
    coluna_resposta: str = "respondeu",
    z: float = 1.96,
    minimo_para_decisao: int = MINIMO_PARA_DECISAO,
) -> DataFrame:
    """Taxa de resposta por segmento, com intervalo de Wilson e marca de decisão.

    Args:
        dados: base com uma linha por contato.
        coluna_segmento: coluna que define os grupos comparados.
        coluna_resposta: coluna binária 0/1; 1 significa que respondeu.
        z: escore normal do nível de confiança. 1,96 é 95%.
        minimo_para_decisao: base abaixo da qual `decidivel` sai como falso.

    Returns:
        Uma linha por segmento, com ``contatados``, ``respostas``, ``taxa_pct``,
        ``ic_inferior_pct``, ``ic_superior_pct``, ``largura_ic_pp`` e
        ``decidivel``, ordenada da maior taxa para a menor.

    Raises:
        ValueError: se a coluna de resposta contiver valor fora de {0, 1} ou
            nulo. Tratar nulo como zero silenciosamente transformaria falha de
            registro em não-resposta, o que enviesa a taxa para baixo sem deixar
            rastro.

    Note:
        ``largura_ic_pp`` costuma ser mais acionável que o próprio intervalo:
        é a resposta direta para "com que precisão eu sei esta taxa?".
    """
    if not 0 < z <= 5:
        raise ValueError("z deve estar em (0, 5]")
    if minimo_para_decisao < 1:
        raise ValueError("minimo_para_decisao deve ser positivo")
    for coluna in (coluna_segmento, coluna_resposta):
        if coluna not in dados.columns:
            raise ValueError(f"coluna ausente na base: {coluna}")

    invalidas = dados.filter(
        F.col(coluna_resposta).isNull() | ~F.col(coluna_resposta).isin(0, 1)
    ).count()
    if invalidas:
        raise ValueError(
            f"{coluna_resposta}: {invalidas} linha(s) com valor nulo ou fora de "
            "{0, 1}. Decida explicitamente o que fazer com elas antes de medir."
        )

    agregado = dados.groupBy(F.col(coluna_segmento).alias("segmento")).agg(
        F.count("*").alias("contatados"),
        F.sum(F.col(coluna_resposta)).alias("respostas"),
    )

    n = F.col("contatados")
    p = F.col("respostas") / n
    # Wilson: centro deslocado em direção a 0,5 e margem que encolhe com n.
    denominador = 1 + F.lit(z * z) / n
    centro = (p + F.lit(z * z) / (2 * n)) / denominador
    margem = (
        F.lit(z) * F.sqrt(p * (1 - p) / n + F.lit(z * z) / (4 * n * n))
    ) / denominador

    return (
        agregado.withColumn("taxa_pct", F.round(100 * p, 2))
        .withColumn("ic_inferior_pct", F.round(100 * (centro - margem), 2))
        .withColumn("ic_superior_pct", F.round(100 * (centro + margem), 2))
        .withColumn(
            "largura_ic_pp",
            F.round(100 * 2 * margem, 2),
        )
        .withColumn("decidivel", n >= F.lit(minimo_para_decisao))
        .orderBy(F.desc("taxa_pct"))
    )
