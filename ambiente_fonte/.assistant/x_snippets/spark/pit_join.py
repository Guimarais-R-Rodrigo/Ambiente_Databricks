# -*- coding: utf-8 -*-
"""Junção point-in-time (as-of) entre fatos de decisão e histórico de features.

Para cada linha de decisão, traz o último valor de feature que já estava
**disponível** naquele instante, descontando o atraso de publicação da fonte.
É a operação que sustenta a exigência anti-leakage das skills: uma feature cujo
valor só ficou conhecido depois da decisão não pode entrar no treino.

O helper devolve o DataFrame juntado e um diagnóstico do que foi descartado por
indisponibilidade temporal — saber quantas decisões ficaram sem feature é parte
da decisão de modelagem, não detalhe de implementação.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, Tuple

from pyspark.sql import DataFrame, Window, functions as F


def pit_join(
    fatos: DataFrame,
    features: DataFrame,
    chave: str | Sequence[str],
    ts_decisao: str,
    ts_feature: str,
    *,
    atraso_publicacao_dias: int = 0,
    janela_maxima_dias: Optional[int] = None,
    colunas_feature: Optional[Sequence[str]] = None,
    sufixo: str = "",
) -> Tuple[DataFrame, Dict[str, Any]]:
    """Junta features ao fato usando apenas informação disponível na decisão.

    Args:
        fatos: linhas de decisão; cada uma recebe no máximo uma versão da feature.
        features: histórico da feature, com uma linha por (chave, ``ts_feature``).
        chave: coluna(s) de entidade presentes nos dois lados.
        ts_decisao: instante da decisão, em ``fatos``.
        ts_feature: instante a que o valor da feature se refere, em ``features``.
        atraso_publicacao_dias: quantos dias a fonte leva para disponibilizar o
            valor. Com ``2``, um valor de referência 10/01 só pode ser usado em
            decisões a partir de 12/01. O default ``0`` assume publicação
            imediata — declare o valor real da fonte em vez de aceitar o default.
        janela_maxima_dias: descarta feature mais antiga que este limite; use
            quando valor muito defasado não representa mais a entidade.
        colunas_feature: colunas a trazer. O padrão é todas, menos chave e
            ``ts_feature``.
        sufixo: sufixo aplicado às colunas trazidas, para evitar colisão de nome.

    Returns:
        ``(df, diagnostico)``. O DataFrame preserva todas as linhas de ``fatos``
        (junção à esquerda); sem feature elegível, as colunas vêm nulas. O
        diagnóstico traz contagens, a taxa de cobertura e
        ``linhas_com_empate_de_instante`` — linhas em que mais de uma versão da
        feature tinha o mesmo instante de disponibilidade. O desempate é
        determinístico (ordem crescente dos valores trazidos), mas empate
        costuma indicar duplicidade na fonte e merece investigação.

    Raises:
        ValueError: coluna ausente, parâmetro negativo ou nenhuma coluna a trazer.
    """
    chaves = [chave] if isinstance(chave, str) else list(chave)
    if not chaves:
        raise ValueError("chave deve conter ao menos uma coluna")
    if atraso_publicacao_dias < 0:
        raise ValueError("atraso_publicacao_dias não pode ser negativo")
    if janela_maxima_dias is not None and janela_maxima_dias <= 0:
        raise ValueError("janela_maxima_dias deve ser positiva quando informada")

    faltando_fatos = set(chaves + [ts_decisao]) - set(fatos.columns)
    if faltando_fatos:
        raise ValueError(f"colunas ausentes em fatos: {sorted(faltando_fatos)}")
    faltando_feats = set(chaves + [ts_feature]) - set(features.columns)
    if faltando_feats:
        raise ValueError(f"colunas ausentes em features: {sorted(faltando_feats)}")

    if colunas_feature is None:
        colunas_feature = [c for c in features.columns if c not in set(chaves) | {ts_feature}]
    colunas_feature = list(colunas_feature)
    if not colunas_feature:
        raise ValueError("nenhuma coluna de feature a trazer")

    # Instante em que o valor passa a ser utilizável: referência + atraso.
    disponivel_em = F.expr(
        f"CAST({ts_feature} AS TIMESTAMP) + INTERVAL {atraso_publicacao_dias} DAYS"
    )
    feats = features.withColumn("__disponivel_em", disponivel_em)

    renomeadas = []
    for coluna in colunas_feature:
        alvo = f"{coluna}{sufixo}" if sufixo else coluna
        if alvo in fatos.columns:
            raise ValueError(
                f"coluna '{alvo}' colidiria com fatos; use o parâmetro sufixo"
            )
        feats = feats.withColumnRenamed(coluna, alvo)
        renomeadas.append(alvo)

    # Identificador por linha de decisão: duas decisões da mesma entidade no
    # mesmo instante são legítimas (produtos distintos, por exemplo) e não podem
    # ser colapsadas pela janela.
    colunas_fato = list(fatos.columns)
    # Resolver a feature por par (chave, instante de decisão) distinto, e só
    # então juntar de volta aos fatos. Evita depender de identificador sintético
    # de linha — `monotonically_increasing_id` não tem estabilidade garantida
    # entre recomputações — e trata naturalmente decisões repetidas da mesma
    # entidade no mesmo instante, que devem receber a mesma feature.
    pares = fatos.select(*chaves, ts_decisao).distinct()

    condicao = [pares[k] == feats[k] for k in chaves]
    condicao.append(feats["__disponivel_em"] <= pares[ts_decisao].cast("timestamp"))
    if janela_maxima_dias is not None:
        limite = F.expr(
            f"CAST({ts_decisao} AS TIMESTAMP) - INTERVAL {janela_maxima_dias} DAYS"
        )
        condicao.append(feats["__disponivel_em"] >= limite)

    candidatos = pares.join(feats, condicao, "left")

    # Desempate determinístico: com dois valores publicados no mesmo instante,
    # ordenar só por data deixaria a escolha a cargo do plano de execução, e o
    # mesmo código devolveria resultados diferentes entre execuções.
    criterio = [F.col("__disponivel_em").desc_nulls_last()]
    criterio += [F.col(c).asc_nulls_last() for c in renomeadas]

    ordem = Window.partitionBy(*[pares[k] for k in chaves], pares[ts_decisao]).orderBy(*criterio)
    empates = Window.partitionBy(
        *[pares[k] for k in chaves], pares[ts_decisao], F.col("__disponivel_em")
    )

    # As colunas de junção são renomeadas antes de voltar aos fatos: `resolvido`
    # descende de `fatos`, e reaproveitar os mesmos nomes faria o Spark tratar a
    # junção como auto-join ambíguo.
    chaves_tmp = {k: f"__pit_{k}" for k in list(chaves) + [ts_decisao]}
    resolvido = (
        candidatos.withColumn("__rank", F.row_number().over(ordem))
        .withColumn("__empatados", F.count(F.lit(1)).over(empates))
        .filter(F.col("__rank") == 1)
        .select(
            *[pares[k].alias(chaves_tmp[k]) for k in chaves],
            pares[ts_decisao].alias(chaves_tmp[ts_decisao]),
            *[F.col(c) for c in renomeadas],
            F.col("__disponivel_em").alias(f"__feature_disponivel_em{sufixo}"),
            F.col("__empatados"),
        )
    )

    condicao_volta = [fatos[k] == resolvido[chaves_tmp[k]] for k in chaves]
    condicao_volta.append(fatos[ts_decisao] == resolvido[chaves_tmp[ts_decisao]])
    saida_completa = fatos.join(resolvido, condicao_volta, "left")
    saida = saida_completa.select(
        *[fatos[c] for c in colunas_fato],
        *[F.col(c) for c in renomeadas],
        F.col(f"__feature_disponivel_em{sufixo}"),
    )

    total = fatos.count()
    com_feature = saida.filter(F.col(f"__feature_disponivel_em{sufixo}").isNotNull()).count()
    com_empate = saida_completa.filter(F.col("__empatados") > 1).count()
    diagnostico = {
        "linhas_fato": total,
        "com_feature": com_feature,
        "sem_feature_elegivel": total - com_feature,
        "cobertura_pct": round(100.0 * com_feature / total, 2) if total else 0.0,
        "linhas_com_empate_de_instante": com_empate,
        "atraso_publicacao_dias": atraso_publicacao_dias,
        "janela_maxima_dias": janela_maxima_dias,
        "colunas_trazidas": renomeadas,
    }
    return saida, diagnostico
