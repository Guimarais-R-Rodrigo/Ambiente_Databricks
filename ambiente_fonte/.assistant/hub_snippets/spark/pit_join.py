# -*- coding: utf-8 -*-
"""Junção point-in-time (as-of) entre fatos de decisão e histórico de features.

Para cada linha de decisão, traz o último valor de feature que já estava
**disponível** naquele instante, descontando o atraso de publicação da fonte.
É a operação que sustenta a exigência anti-leakage das skills: uma feature cujo
valor só ficou conhecido depois da decisão não pode entrar no treino.

Semântica de tempo, que precisa estar clara antes do uso:

- ``ts_feature`` é o instante **a que o valor se refere**.
- ``ts_feature + atraso_publicacao_dias`` é o instante em que ele passou a ser
  utilizável, e é isso que se compara com ``ts_decisao``.
- Se ``ts_feature`` for do tipo data, o Spark o converte para a meia-noite
  daquele dia **no fuso da sessão**. Snapshot diário que descreve o fechamento
  do dia precisa de ``atraso_publicacao_dias >= 1``: com zero, a decisão das
  14h do dia 12 enxergaria o fechamento do próprio dia 12.
- ``janela_maxima_dias`` limita a **idade do valor**, medida em ``ts_feature``.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, Tuple

from pyspark.sql import DataFrame, SparkSession, Window, functions as F

POLITICAS_EMPATE = ("erro", "menor", "maior")


def _q(nome: str) -> str:
    """Protege nome de coluna em expressão SQL."""
    return "`" + nome.replace("`", "``") + "`"


def pit_join(
    fatos: DataFrame,
    features: DataFrame,
    chave: str | Sequence[str],
    ts_decisao: str,
    ts_feature: str,
    *,
    atraso_publicacao_dias: int,
    janela_maxima_dias: Optional[int] = None,
    colunas_feature: Optional[Sequence[str]] = None,
    sufixo: str = "",
    politica_empate: str = "erro",
    devolver_disponibilidade: bool = False,
) -> Tuple[DataFrame, Dict[str, Any]]:
    """Junta features ao fato usando só informação disponível na decisão.

    Args:
        fatos: linhas de decisão; cada uma recebe no máximo uma versão da feature.
        features: histórico da feature, com uma linha por (chave, ``ts_feature``).
        chave: coluna(s) de entidade presentes nos dois lados.
        ts_decisao: instante da decisão, em ``fatos``.
        ts_feature: instante a que o valor da feature se refere, em ``features``.
        atraso_publicacao_dias: dias entre a referência do dado e sua
            disponibilidade real. **Obrigatório e sem default**: o valor correto
            é característica da fonte, e presumir zero é a forma mais comum de
            criar vazamento sem gerar erro.
        janela_maxima_dias: descarta feature cuja **referência** seja mais antiga
            que este limite. Recomendado em volume: sem ele, a junção considera
            todo o histórico de cada entidade.
        colunas_feature: colunas a trazer. O padrão é todas, menos chave e
            ``ts_feature``.
        sufixo: sufixo aplicado às colunas trazidas, para evitar colisão.
        politica_empate: o que fazer quando duas versões têm o mesmo instante de
            disponibilidade. ``"erro"`` (padrão) interrompe, porque empate
            costuma ser duplicidade na origem; ``"menor"`` e ``"maior"`` escolhem
            de forma determinística pelos valores trazidos.
        devolver_disponibilidade: inclui no resultado a coluna com o instante de
            disponibilidade da feature escolhida. Falso por padrão, para que
            chamadas encadeadas não colidam.

    Returns:
        ``(df, diagnostico)``. O DataFrame preserva todas as linhas de ``fatos``;
        sem feature elegível, as colunas vêm nulas. O diagnóstico separa as três
        causas de ausência — chave nula, entidade sem histórico e histórico
        existente porém indisponível na data —, porque a correção de cada uma é
        diferente.

    Raises:
        ValueError: parâmetro inválido, coluna ausente, colisão de nome, ou
            empate de instante sob ``politica_empate="erro"``.
    """
    chaves = [chave] if isinstance(chave, str) else list(chave)
    if not chaves:
        raise ValueError("chave deve conter ao menos uma coluna")
    if isinstance(atraso_publicacao_dias, bool) or not isinstance(atraso_publicacao_dias, int):
        raise ValueError("atraso_publicacao_dias deve ser inteiro")
    if atraso_publicacao_dias < 0:
        raise ValueError("atraso_publicacao_dias não pode ser negativo")
    if janela_maxima_dias is not None:
        if isinstance(janela_maxima_dias, bool) or not isinstance(janela_maxima_dias, int):
            raise ValueError("janela_maxima_dias deve ser inteiro")
        if janela_maxima_dias <= 0:
            raise ValueError("janela_maxima_dias deve ser positiva quando informada")
    if politica_empate not in POLITICAS_EMPATE:
        raise ValueError(f"politica_empate deve ser um de {POLITICAS_EMPATE}")

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

    col_disponibilidade = f"__feature_disponivel_em{sufixo}"
    reservadas = set(fatos.columns) & {col_disponibilidade}
    if reservadas:
        raise ValueError(
            f"coluna {sorted(reservadas)} já existe em fatos; use o parâmetro "
            "sufixo (acontece ao encadear duas chamadas de pit_join)"
        )

    feats = features.withColumn(
        "__disponivel_em",
        F.expr(
            f"CAST({_q(ts_feature)} AS TIMESTAMP) + INTERVAL {atraso_publicacao_dias} DAYS"
        ),
    ).withColumn("__ts_feature_ref", F.col(ts_feature).cast("timestamp"))

    renomeadas = []
    for coluna in colunas_feature:
        alvo = f"{coluna}{sufixo}" if sufixo else coluna
        if alvo in fatos.columns:
            raise ValueError(f"coluna '{alvo}' colidiria com fatos; use o parâmetro sufixo")
        feats = feats.withColumnRenamed(coluna, alvo)
        renomeadas.append(alvo)

    pares = fatos.select(*chaves, ts_decisao).distinct()

    condicao = [pares[k] == feats[k] for k in chaves]
    condicao.append(feats["__disponivel_em"] <= pares[ts_decisao].cast("timestamp"))
    if janela_maxima_dias is not None:
        # A janela limita a IDADE DO VALOR: compara a referência, não a
        # disponibilidade. Compará-la com `__disponivel_em` produziria janela
        # efetiva de `janela + atraso`, aceitando dados mais velhos que o pedido.
        condicao.append(
            feats["__ts_feature_ref"]
            >= F.expr(
                f"CAST({_q(ts_decisao)} AS TIMESTAMP) - INTERVAL {janela_maxima_dias} DAYS"
            )
        )

    candidatos = pares.join(feats, condicao, "left")

    criterio = [F.col("__disponivel_em").desc_nulls_last()]
    if politica_empate == "maior":
        criterio += [F.col(c).desc_nulls_last() for c in renomeadas]
    else:
        criterio += [F.col(c).asc_nulls_last() for c in renomeadas]

    ordem = Window.partitionBy(*[pares[k] for k in chaves], pares[ts_decisao]).orderBy(*criterio)
    empates = Window.partitionBy(
        *[pares[k] for k in chaves], pares[ts_decisao], F.col("__disponivel_em")
    )

    chaves_tmp = {k: f"__pit_{k}" for k in list(chaves) + [ts_decisao]}
    resolvido = (
        candidatos.withColumn("__rank", F.row_number().over(ordem))
        .withColumn("__empatados", F.count(F.lit(1)).over(empates))
        .filter(F.col("__rank") == 1)
        .select(
            *[pares[k].alias(chaves_tmp[k]) for k in chaves],
            pares[ts_decisao].alias(chaves_tmp[ts_decisao]),
            *[F.col(c) for c in renomeadas],
            F.col("__disponivel_em").alias(col_disponibilidade),
            F.col("__empatados"),
        )
    )

    condicao_volta = [fatos[k] == resolvido[chaves_tmp[k]] for k in chaves]
    condicao_volta.append(fatos[ts_decisao] == resolvido[chaves_tmp[ts_decisao]])
    saida_completa = fatos.join(resolvido, condicao_volta, "left")

    com_empate = saida_completa.filter(F.col("__empatados") > 1).count()
    if com_empate and politica_empate == "erro":
        raise ValueError(
            f"{com_empate} decisão(ões) têm duas versões de feature com o mesmo "
            "instante de disponibilidade. Isso costuma indicar duplicidade na "
            "origem: investigue, ou escolha politica_empate='menor'/'maior' "
            "declarando o critério."
        )

    colunas_saida = [fatos[c] for c in fatos.columns]
    colunas_saida += [F.col(c) for c in renomeadas]
    if devolver_disponibilidade:
        colunas_saida.append(F.col(col_disponibilidade))
    saida = saida_completa.select(*colunas_saida)

    nulo_chave = F.lit(False)
    for k in chaves:
        nulo_chave = nulo_chave | F.col(k).isNull()
    nulo_chave = nulo_chave | F.col(ts_decisao).isNull()

    total = fatos.count()
    sem_chave = fatos.filter(nulo_chave).count()
    com_feature = saida_completa.filter(F.col(col_disponibilidade).isNotNull()).count()
    entidades_com_historico = (
        pares.filter(~nulo_chave).join(features.select(*chaves).distinct(), chaves, "inner").count()
    )
    pares_validos = pares.filter(~nulo_chave).count()
    validos_totais = total - sem_chave

    # `conf.get(chave, default)` valida o segundo argumento como se fosse valor
    # de configuração e falha quando ele não é um fuso real.
    sessao = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    try:
        fuso = sessao.conf.get("spark.sql.session.timeZone")
    except Exception:
        fuso = "desconhecido"

    diagnostico = {
        "linhas_fato": total,
        "com_feature": com_feature,
        "sem_chave_ou_data": sem_chave,
        "entidade_sem_historico": max(pares_validos - entidades_com_historico, 0),
        "sem_feature_disponivel_na_data": max(validos_totais - com_feature - sem_chave, 0),
        "cobertura_pct_linhas_validas": (
            round(100.0 * com_feature / validos_totais, 2) if validos_totais else 0.0
        ),
        "linhas_feature_com_ts_nulo": features.filter(F.col(ts_feature).isNull()).count(),
        "linhas_com_empate_de_instante": com_empate,
        "atraso_publicacao_dias": atraso_publicacao_dias,
        "janela_maxima_dias": janela_maxima_dias,
        "fuso_da_sessao": fuso,
        "colunas_trazidas": renomeadas,
    }
    return saida, diagnostico
