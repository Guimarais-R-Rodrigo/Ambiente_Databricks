# -*- coding: utf-8 -*-
"""Diagnóstico de junção executado **antes** do join real.

Mede cobertura, não-match, multiplicidade e fator de expansão para que a decisão
de juntar seja tomada com número na mão. O erro que este helper existe para
evitar é o join que duplica linhas em silêncio: a contagem cresce, ninguém
percebe, e a base de treino passa a superrepresentar as entidades com mais
correspondências do lado direito.

Chaves nulas são tratadas explicitamente: em SQL elas nunca casam, e contá-las
como não-match sem separá-las esconde um problema de qualidade.
"""

from __future__ import annotations

from typing import Any, Dict, Sequence

from pyspark.sql import DataFrame, functions as F


def diagnosticar_join(
    esquerda: DataFrame,
    direita: DataFrame,
    chave: str | Sequence[str],
    *,
    amostra_orfas: int = 5,
) -> Dict[str, Any]:
    """Estima o efeito de um join sem executá-lo.

    Args:
        esquerda: lado preservado da junção (tipicamente os fatos).
        direita: lado consultado (tipicamente o cadastro ou as features).
        chave: coluna(s) de junção, presentes nos dois lados.
        amostra_orfas: quantas chaves sem correspondência devolver como exemplo.

    Returns:
        Dicionário com contagens dos dois lados, cobertura, multiplicidade do
        lado direito, fator de expansão previsto e chaves nulas por lado.
        ``expansao_prevista`` é a razão entre as linhas que o join à esquerda
        produziria e as linhas originais: 1,0 significa que o join preserva a
        cardinalidade; acima disso, duplica.

    Raises:
        ValueError: chave ausente em algum dos lados ou parâmetro inválido.
    """
    chaves = [chave] if isinstance(chave, str) else list(chave)
    if not chaves:
        raise ValueError("chave deve conter ao menos uma coluna")
    if amostra_orfas < 0:
        raise ValueError("amostra_orfas não pode ser negativo")

    for nome, df in (("esquerda", esquerda), ("direita", direita)):
        faltando = set(chaves) - set(df.columns)
        if faltando:
            raise ValueError(f"colunas ausentes em {nome}: {sorted(faltando)}")

    nulo_esq = F.lit(False)
    nulo_dir = F.lit(False)
    for k in chaves:
        nulo_esq = nulo_esq | F.col(k).isNull()
        nulo_dir = nulo_dir | F.col(k).isNull()

    esq_valida = esquerda.filter(~nulo_esq)
    dir_valida = direita.filter(~nulo_dir)

    total_esq = esquerda.count()
    total_dir = direita.count()
    nulas_esq = total_esq - esq_valida.count()
    nulas_dir = total_dir - dir_valida.count()

    # Multiplicidade: quantas linhas do lado direito existem por chave.
    por_chave = dir_valida.groupBy(*chaves).agg(F.count(F.lit(1)).alias("__n"))
    stats = por_chave.agg(
        F.count(F.lit(1)).alias("chaves_distintas"),
        F.max("__n").alias("max"),
        F.avg("__n").alias("media"),
    ).first()
    chaves_dir_distintas = stats["chaves_distintas"] or 0
    mult_max = int(stats["max"] or 0)
    mult_media = float(stats["media"] or 0.0)

    # Linhas da esquerda que encontram ao menos uma correspondência.
    casadas = esq_valida.join(por_chave, chaves, "inner")
    linhas_casadas = casadas.count()
    linhas_resultantes = casadas.agg(F.coalesce(F.sum("__n"), F.lit(0))).first()[0]

    denominador = total_esq or 1
    return {
        "linhas_esquerda": total_esq,
        "linhas_direita": total_dir,
        "chaves_nulas_esquerda": nulas_esq,
        "chaves_nulas_direita": nulas_dir,
        "chaves_distintas_direita": chaves_dir_distintas,
        "linhas_com_match": linhas_casadas,
        "linhas_sem_match": total_esq - linhas_casadas,
        "cobertura_pct": round(100.0 * linhas_casadas / denominador, 2),
        "multiplicidade_max_direita": mult_max,
        "multiplicidade_media_direita": round(mult_media, 3),
        "relacao": _classificar(mult_max),
        "linhas_apos_join_esquerda": int(linhas_resultantes) + (total_esq - linhas_casadas),
        "expansao_prevista": round(
            (int(linhas_resultantes) + (total_esq - linhas_casadas)) / denominador, 3
        ),
        "exemplos_sem_match": _orfas(esq_valida, por_chave, chaves, amostra_orfas),
    }


def _classificar(multiplicidade_max: int) -> str:
    if multiplicidade_max == 0:
        return "sem correspondencia"
    if multiplicidade_max == 1:
        return "1:1 ou N:1 — join preserva a cardinalidade"
    return "1:N — join duplica linhas da esquerda"


def _orfas(
    esquerda: DataFrame, por_chave: DataFrame, chaves: Sequence[str], limite: int
) -> list:
    if limite == 0:
        return []
    orfas = esquerda.select(*chaves).distinct().join(por_chave, list(chaves), "left_anti")
    return [linha.asDict() for linha in orfas.limit(limite).collect()]
