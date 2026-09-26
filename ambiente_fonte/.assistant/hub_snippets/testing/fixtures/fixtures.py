# -*- coding: utf-8 -*-
"""Geradores determinísticos de dados sintéticos para testar helpers.

Existem para que exemplo de documentação, teste de runtime e demonstração de
skill usem a mesma base reproduzível, sem nenhum dado real. Toda função aceita
``seed`` e devolve o mesmo resultado a cada execução.

Nenhuma função grava tabela: o retorno é DataFrame em memória. Materializar,
quando necessário, é decisão de quem consome — e deve continuar visível.
"""

from __future__ import annotations

import datetime
import random
from typing import List, Optional, Sequence, Tuple

from pyspark.sql import DataFrame, SparkSession


def _sessao() -> SparkSession:
    return SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()


def base_tabular(
    n: int = 500,
    *,
    seed: int = 42,
    pct_nulos_renda: float = 0.04,
    prevalencia_alvo: float = 0.25,
    n_entidades: Optional[int] = None,
) -> DataFrame:
    """Base tabular com chave, categórica, numérica com nulos e alvo binário.

    Args:
        n: número de linhas.
        seed: semente; mesma semente devolve exatamente a mesma base.
        pct_nulos_renda: fração de ``renda`` nula, para exercitar tratamento de
            ausentes.
        prevalencia_alvo: fração aproximada de ``alvo`` igual a 1.
        n_entidades: quantidade de valores distintos de ``id_cliente``. O padrão
            é ``n``, produzindo chave única; valor menor gera duplicidade
            proposital, útil para testar diagnóstico de join.

    Returns:
        DataFrame com ``id_cliente``, ``uf``, ``renda``, ``dt_referencia``, ``alvo``.
    """
    if n <= 0:
        raise ValueError("n deve ser positivo")
    if not 0 <= pct_nulos_renda < 1:
        raise ValueError("pct_nulos_renda deve estar em [0, 1)")
    if not 0 < prevalencia_alvo < 1:
        raise ValueError("prevalencia_alvo deve estar em (0, 1)")

    entidades = n_entidades or n
    if entidades <= 0:
        raise ValueError("n_entidades deve ser positivo")

    rng = random.Random(seed)
    inicio = datetime.date(2026, 1, 1)
    ufs = ["SP", "RJ", "MG", "BA", "RS"]
    linhas = []
    for i in range(n):
        renda = None if rng.random() < pct_nulos_renda else round(rng.uniform(1500, 20000), 2)
        linhas.append((
            f"cli{i % entidades:05d}",
            rng.choice(ufs),
            renda,
            inicio + datetime.timedelta(days=rng.randint(0, 180)),
            1 if rng.random() < prevalencia_alvo else 0,
        ))
    esquema = "id_cliente string, uf string, renda double, dt_referencia date, alvo int"
    return _sessao().createDataFrame(linhas, esquema)


def serie_temporal(
    n_entidades: int = 20,
    n_periodos: int = 24,
    *,
    seed: int = 42,
    tendencia: float = 0.5,
) -> DataFrame:
    """Painel de série temporal por entidade, com tendência e ruído.

    Útil para exercitar lags, janelas móveis, split temporal e walk-forward,
    onde o erro típico é ordenar sem particionar por entidade.

    Returns:
        DataFrame com ``id_entidade``, ``dt_referencia`` (mensal) e ``valor``.
    """
    if n_entidades <= 0 or n_periodos <= 0:
        raise ValueError("n_entidades e n_periodos devem ser positivos")

    rng = random.Random(seed)
    linhas = []
    for e in range(n_entidades):
        nivel = rng.uniform(50, 150)
        for p in range(n_periodos):
            mes = 1 + (p % 12)
            ano = 2025 + (p // 12)
            valor = nivel + tendencia * p + rng.gauss(0, 5)
            linhas.append((f"ent{e:03d}", datetime.date(ano, mes, 1), round(valor, 2)))
    return _sessao().createDataFrame(
        linhas, "id_entidade string, dt_referencia date, valor double"
    )


def fatos_e_features(
    n_decisoes: int = 300,
    *,
    seed: int = 42,
    atraso_real_dias: int = 3,
    pct_feature_futura: float = 0.2,
) -> Tuple[DataFrame, DataFrame]:
    """Par de bases desenhado para tornar o vazamento temporal **detectável**.

    Uma fração das linhas de feature tem instante de referência posterior à
    decisão correspondente: um join point-in-time correto precisa descartá-las.
    Se aparecerem no resultado, houve leakage — é isso que o teste verifica.

    Args:
        n_decisoes: linhas na base de fatos.
        seed: semente.
        atraso_real_dias: atraso de publicação embutido nos dados.
        pct_feature_futura: fração de features publicadas depois da decisão.

    Returns:
        ``(fatos, features)``. ``fatos`` tem ``id_cliente``, ``dt_decisao`` e
        ``alvo``. ``features`` tem ``id_cliente``, ``dt_referencia``,
        ``score_bureau`` e ``eh_futura`` — esta última existe só para o teste
        conferir o que deveria ter sido descartado.

    Note:
        Cada decisão recebe um cliente próprio, de propósito. Se a mesma entidade
        aparecesse em decisões diferentes, uma feature futura para a decisão de
        março seria legitimamente passada para a decisão de junho, e a marca
        ``eh_futura`` deixaria de valer como critério de teste.
    """
    if not 0 <= pct_feature_futura < 1:
        raise ValueError("pct_feature_futura deve estar em [0, 1)")

    rng = random.Random(seed)
    inicio = datetime.date(2026, 3, 1)
    fatos, features = [], []
    for i in range(n_decisoes):
        cliente = f"cli{i:05d}"
        dt_decisao = inicio + datetime.timedelta(days=rng.randint(30, 120))
        fatos.append((cliente, dt_decisao, rng.randint(0, 1)))

        # Duas versões legítimas com datas garantidamente distintas, para
        # exercitar a escolha da mais recente sem produzir empate acidental —
        # empate é situação própria, e a fixture não deve criá-la por sorteio.
        defasagem = rng.randint(1, 20)
        for extra in (0, rng.randint(1, 10)):
            dt_ok = dt_decisao - datetime.timedelta(
                days=atraso_real_dias + defasagem + extra
            )
            features.append((cliente, dt_ok, round(rng.uniform(300, 900), 1), False))

        if rng.random() < pct_feature_futura:
            dt_futura = dt_decisao + datetime.timedelta(days=rng.randint(1, 20))
            features.append((cliente, dt_futura, round(rng.uniform(300, 900), 1), True))

    sessao = _sessao()
    df_fatos = sessao.createDataFrame(
        fatos, "id_cliente string, dt_decisao date, alvo int"
    )
    df_features = sessao.createDataFrame(
        features,
        "id_cliente string, dt_referencia date, score_bureau double, eh_futura boolean",
    )
    return df_fatos, df_features


def safras(
    n_contratos: int = 400,
    *,
    seed: int = 42,
    safras_yyyymm: Sequence[str] = ("202501", "202502", "202503"),
    mob_maximo: int = 12,
) -> DataFrame:
    """Painel contrato × MOB para exercitar curvas de maturação.

    Returns:
        DataFrame com ``id_contrato``, ``safra``, ``mob`` e ``inadimplente``.
        A incidência cresce com o MOB, imitando maturação real.
    """
    if n_contratos <= 0 or mob_maximo <= 0:
        raise ValueError("n_contratos e mob_maximo devem ser positivos")
    if not safras_yyyymm:
        raise ValueError("informe ao menos uma safra")

    rng = random.Random(seed)
    linhas: List[tuple] = []
    for c in range(n_contratos):
        safra = safras_yyyymm[c % len(safras_yyyymm)]
        ja_inadimplente = False
        for mob in range(1, mob_maximo + 1):
            if not ja_inadimplente and rng.random() < 0.01 * mob:
                ja_inadimplente = True
            linhas.append((f"ctr{c:05d}", safra, mob, int(ja_inadimplente)))
    return _sessao().createDataFrame(
        linhas, "id_contrato string, safra string, mob int, inadimplente int"
    )
