# -*- coding: utf-8 -*-
"""Confere se uma base de campanha sustenta medição, antes de medir.

Material de referência dos padrões do Hub, não helper de produção.

A diferença entre um **script** e um **snippet** do Hub está no papel, não no
tamanho. Snippet é peça de cálculo que entra num fluxo maior e devolve dado.
Script é diagnóstico: roda sozinho, olha um objeto do workspace e devolve um
veredito legível, tipicamente antes de alguém confiar naquele objeto.

Por isso um script recebe **nome de tabela**, não DataFrame: ele existe para ser
apontado a algo que já está lá.
"""

from __future__ import annotations

from typing import Any, Dict

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Política local, não exigência da plataforma: ajuste ao ritmo da sua fonte.
LIMITES_PADRAO = {
    "pct_nulo_alerta": 1.0,
    "min_contatos_por_segmento": 100,
}


def checar_base_campanha(
    tabela: str,
    *,
    coluna_segmento: str = "segmento",
    coluna_resposta: str = "respondeu",
    coluna_chave: str = "id_cliente",
    limites: Dict[str, float] | None = None,
) -> Dict[str, Any]:
    """Devolve um diagnóstico da base, sem alterá-la.

    Args:
        tabela: nome completo, no padrão ``catalogo.schema.tabela``.
        coluna_segmento: coluna de agrupamento a ser avaliada.
        coluna_resposta: coluna binária de resposta.
        coluna_chave: coluna que deveria identificar o contato.
        limites: sobrepõe ``LIMITES_PADRAO``.

    Returns:
        Dicionário com ``status`` (``pass``/``warn``/``fail``), ``checagens`` e
        ``alertas``. **Status ``fail`` não significa base ruim**: significa que
        algo precisa de decisão humana antes de a medição valer.

    Note:
        Não grava nada e não altera a tabela. Faz três varreduras agregadas;
        em tabela muito grande, avalie o custo antes.
    """
    politica = {**LIMITES_PADRAO, **(limites or {})}
    # O global `spark` de notebook não existe dentro de módulo importado.
    sessao = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    dados = sessao.table(tabela)

    faltando = [
        c for c in (coluna_segmento, coluna_resposta, coluna_chave)
        if c not in dados.columns
    ]
    if faltando:
        raise ValueError(f"{tabela}: coluna(s) ausente(s) -> {', '.join(faltando)}")

    geral = dados.agg(
        F.count("*").alias("linhas"),
        F.countDistinct(coluna_chave).alias("chaves_distintas"),
        F.sum(F.col(coluna_resposta).isNull().cast("int")).alias("resposta_nula"),
        F.sum((~F.col(coluna_resposta).isin(0, 1)).cast("int")).alias("resposta_fora_dominio"),
    ).collect()[0]

    pequenos = (
        dados.groupBy(coluna_segmento).count()
        .filter(F.col("count") < politica["min_contatos_por_segmento"])
        .collect()
    )

    alertas = []
    if geral["chaves_distintas"] != geral["linhas"]:
        alertas.append({
            "checagem": "grao",
            "severidade": "fail",
            "mensagem": (
                f"{coluna_chave} não é único: {geral['linhas']} linhas para "
                f"{geral['chaves_distintas']} chaves. A taxa passa a pesar quem "
                "aparece mais vezes."
            ),
        })
    if geral["resposta_nula"] or geral["resposta_fora_dominio"]:
        alertas.append({
            "checagem": "dominio_resposta",
            "severidade": "fail",
            "mensagem": (
                f"{coluna_resposta}: {geral['resposta_nula']} nula(s) e "
                f"{geral['resposta_fora_dominio']} fora de {{0,1}}. Decida o "
                "tratamento; tratar nulo como zero enviesa a taxa para baixo."
            ),
        })
    for linha in pequenos:
        alertas.append({
            "checagem": "base_por_segmento",
            "severidade": "warn",
            "mensagem": (
                f"segmento '{linha[coluna_segmento]}' tem {linha['count']} "
                f"contatos, abaixo de {politica['min_contatos_por_segmento']}: "
                "reporte a taxa, não aloque orçamento por ela."
            ),
        })

    severidades = {a["severidade"] for a in alertas}
    status = "fail" if "fail" in severidades else ("warn" if severidades else "pass")

    return {
        "tabela": tabela,
        "status": status,
        "limites": politica,
        "checagens": {
            "linhas": geral["linhas"],
            "chaves_distintas": geral["chaves_distintas"],
            "resposta_nula": geral["resposta_nula"],
            "resposta_fora_dominio": geral["resposta_fora_dominio"],
            "segmentos_com_base_pequena": len(pequenos),
        },
        "alertas": alertas,
    }
