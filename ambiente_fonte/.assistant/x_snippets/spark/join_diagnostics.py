# -*- coding: utf-8 -*-
"""Diagnóstico de junção executado **antes** do join real.

Mede cobertura, não-match, multiplicidade e fator de expansão para que a decisão
de juntar seja tomada com número na mão. O erro que este helper existe para
evitar é o join que duplica linhas em silêncio: a contagem cresce, ninguém
percebe, e a base de treino passa a superrepresentar as entidades com mais
correspondências do lado direito.

Duas escolhas de contagem que mudam a leitura dos números:

- Chave nula é contada **à parte** e sai do denominador de cobertura. Em SQL ela
  nunca casa, e misturá-la com a chave órfã esconde um problema de qualidade que
  tem outra causa e outra correção.
- Multiplicidade e expansão consideram apenas as chaves **presentes à esquerda**.
  Uma chave que só existe do lado direito não afeta o resultado do join e não
  deve inflar a estatística.
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
        Dicionário com as contagens dos dois lados e, separadamente:
        ``expansao_prevista_left`` e ``expansao_prevista_inner`` (razão entre as
        linhas resultantes e as originais, por tipo de junção),
        ``cobertura_pct_chaves_validas`` (denominador exclui chave nula) e
        ``linhas_descartadas_chave_nula``. Expansão ``1,0`` preserva a
        cardinalidade; acima disso, o join duplica.

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

    nulo = F.lit(False)
    for k in chaves:
        nulo = nulo | F.col(k).isNull()

    # Uma passada por lado, em vez de uma ação por métrica: com fonte não
    # determinística (amostra, tabela sob escrita), contagens tiradas de leituras
    # diferentes podem ficar mutuamente incoerentes.
    tot_esq = esquerda.agg(
        F.count(F.lit(1)).alias("total"),
        F.sum(F.when(nulo, 1).otherwise(0)).alias("nulas"),
    ).first()
    tot_dir = direita.agg(
        F.count(F.lit(1)).alias("total"),
        F.sum(F.when(nulo, 1).otherwise(0)).alias("nulas"),
    ).first()

    total_esq = int(tot_esq["total"] or 0)
    nulas_esq = int(tot_esq["nulas"] or 0)
    total_dir = int(tot_dir["total"] or 0)
    nulas_dir = int(tot_dir["nulas"] or 0)
    validas_esq = total_esq - nulas_esq

    esq_valida = esquerda.filter(~nulo)
    dir_valida = direita.filter(~nulo)

    # Multiplicidade restrita às chaves que existem à esquerda: chave que só
    # aparece à direita não participa do join e não deve entrar na estatística.
    chaves_esq = esq_valida.select(*chaves).distinct()
    por_chave = (
        dir_valida.join(chaves_esq, chaves, "left_semi")
        .groupBy(*chaves)
        .agg(F.count(F.lit(1)).alias("__n"))
    )

    casadas = esq_valida.join(por_chave, chaves, "inner")
    resumo = casadas.agg(
        F.count(F.lit(1)).alias("linhas"),
        F.coalesce(F.sum("__n"), F.lit(0)).alias("resultantes"),
        F.max("__n").alias("mult_max"),
        F.avg("__n").alias("mult_media"),
    ).first()

    linhas_casadas = int(resumo["linhas"] or 0)
    resultantes = int(resumo["resultantes"] or 0)
    mult_max = int(resumo["mult_max"] or 0)
    mult_media = float(resumo["mult_media"] or 0.0)

    sem_match_validas = validas_esq - linhas_casadas
    linhas_left = resultantes + sem_match_validas + nulas_esq
    base = validas_esq or 1

    return {
        "linhas_esquerda": total_esq,
        "linhas_direita": total_dir,
        "chaves_nulas_esquerda": nulas_esq,
        "chaves_nulas_direita": nulas_dir,
        "linhas_descartadas_chave_nula": nulas_esq,
        "linhas_com_match": linhas_casadas,
        "linhas_sem_match_chave_valida": sem_match_validas,
        "cobertura_pct_chaves_validas": round(100.0 * linhas_casadas / base, 2),
        "multiplicidade_max_direita": mult_max,
        "multiplicidade_media_direita": round(mult_media, 3),
        "relacao": _classificar(resultantes, linhas_casadas),
        "linhas_apos_join_left": linhas_left,
        "linhas_apos_join_inner": resultantes,
        "expansao_prevista_left": round(linhas_left / (total_esq or 1), 3) if total_esq else 1.0,
        "expansao_prevista_inner": round(resultantes / (total_esq or 1), 3) if total_esq else 1.0,
        "exemplos_sem_match": _orfas(esq_valida, por_chave, chaves, amostra_orfas),
        "exemplos_chave_nula": _amostra_nulas(esquerda, nulo, chaves, amostra_orfas),
    }


def _classificar(resultantes: int, casadas: int) -> str:
    """Deriva a relação da expansão observada, não da multiplicidade bruta."""
    if casadas == 0:
        return "sem correspondencia"
    if resultantes == casadas:
        return "1:1 ou N:1 — join preserva a cardinalidade"
    return "1:N — join duplica linhas da esquerda"


def _orfas(
    esquerda: DataFrame, por_chave: DataFrame, chaves: Sequence[str], limite: int
) -> list:
    if limite == 0:
        return []
    orfas = (
        esquerda.select(*chaves).distinct()
        .join(por_chave, list(chaves), "left_anti")
        .orderBy(*chaves)  # ordenado para que a mesma execução devolva a mesma amostra
    )
    return [linha.asDict() for linha in orfas.limit(limite).collect()]


def _amostra_nulas(esquerda: DataFrame, nulo, chaves: Sequence[str], limite: int) -> list:
    if limite == 0:
        return []
    linhas = esquerda.filter(nulo).select(*chaves).limit(limite).collect()
    return [linha.asDict() for linha in linhas]
