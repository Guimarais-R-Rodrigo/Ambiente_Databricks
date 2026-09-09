"""
LightGBM para séries temporais com lag/rolling features automáticas.

Uso:
    from hub_snippets.ml.lgbm_temporal import create_temporal_features
    df_feat = create_temporal_features(df, target_col='saldo', date_col='dt_ref')

A coluna de data é normalizada **antes** da ordenação. Antes da versão 1.1 ela era
ordenada como veio: com data em texto, a ordem era lexicográfica, e '2026-1-10'
vinha antes de '2026-1-2'. O lag resultante trazia informação futura sem nenhum
sinal de erro.

Autor: Rodrigo via assistente
Versão: 1.2
"""

import re
from typing import List, Optional, Sequence

import numpy as np
import pandas as pd


SEED = 42

# Ano-mês-dia com separador '-'. A ordem dos campos é fixa, logo o texto é
# convertível sem inferência. Qualquer outro formato — inclusive dd/mm/aaaa —
# exige ``date_format`` explícito, porque 03/02 pode ser 3 de fevereiro ou
# 2 de março e o helper não escolhe por conta própria.
_TEXTO_ANO_MES_DIA = re.compile(
    r"^\d{4}-\d{1,2}-\d{1,2}(?:[ T]\d{1,2}:\d{2}(?::\d{2}(?:\.\d+)?)?)?$"
)


def _normalizar_datas(valores: pd.Series, date_format: Optional[str]) -> pd.Series:
    """Converta a coluna de data em datetime, recusando o que for ambíguo.

    Args:
        valores: Série com a coluna de data como o chamador a passou.
        date_format: Formato ``strftime`` explícito, ou None para o modo automático.

    Returns:
        Série datetime alinhada ao índice de entrada.

    Raises:
        ValueError: Data nula, formato ambíguo sem ``date_format``, valor que não
            casa com o formato declarado, ou fuso horário misto.
    """
    if valores.isna().any():
        quantidade = int(valores.isna().sum())
        raise ValueError(
            f"date_col contém {quantidade} valor(es) nulo(s); a política de data "
            "ausente é do pipeline consumidor, não deste helper. Remova ou impute "
            "antes de chamar."
        )

    if pd.api.types.is_datetime64_any_dtype(valores):
        return valores

    if date_format is not None:
        convertida = pd.to_datetime(valores, format=date_format, errors="coerce")
        if convertida.isna().any():
            exemplo = valores[convertida.isna()].iloc[0]
            raise ValueError(
                f"date_col não casa com date_format={date_format!r}; primeiro valor "
                f"incompatível: {exemplo!r}"
            )
    elif pd.api.types.is_numeric_dtype(valores):
        raise ValueError(
            "date_col numérica é ambígua (epoch em segundos? em milissegundos? "
            "aaaammdd?). Converta antes de chamar ou informe date_format."
        )
    else:
        texto = valores.astype(str)
        fora_do_padrao = texto[~texto.str.match(_TEXTO_ANO_MES_DIA)]
        if len(fora_do_padrao) > 0:
            raise ValueError(
                "date_col em texto só é convertida automaticamente no formato "
                "ano-mês-dia (YYYY-M-D, com hora opcional), cuja ordem dos campos "
                "não é ambígua. Informe date_format para qualquer outro formato — "
                "por exemplo date_format='%d/%m/%Y'. Primeiro valor fora do "
                f"padrão: {fora_do_padrao.iloc[0]!r}"
            )
        convertida = pd.to_datetime(texto, format="ISO8601", errors="coerce")
        if convertida.isna().any():
            exemplo = texto[convertida.isna()].iloc[0]
            raise ValueError(f"date_col tem data inválida no calendário: {exemplo!r}")

    if not pd.api.types.is_datetime64_any_dtype(convertida):
        raise ValueError(
            "date_col resultou em tipo não-datetime após a conversão; fusos "
            "horários misturados na mesma coluna precisam ser unificados antes."
        )
    return convertida


def create_temporal_features(
    df: pd.DataFrame,
    target_col: str,
    date_col: str,
    lags: Optional[List[int]] = None,
    rolling_windows: Optional[List[int]] = None,
    calendar_features: bool = True,
    entity_cols: Optional[Sequence[str]] = None,
    *,
    date_format: Optional[str] = None,
    on_duplicate_dates: str = "raise",
) -> pd.DataFrame:
    """Gere features temporais (lags, rolling, calendar) em ordem cronológica real.

    ``lag_n`` significa **n observações anteriores** da mesma entidade, não n dias
    nem n meses. Numa série irregular as duas coisas divergem: se o contrato for
    calendário, o caminho é reindexar ou juntar por data antes de chamar.

    A conversão da data acontece antes da ordenação e independe de
    ``calendar_features``.

    Args:
        df: DataFrame com coluna de data e target.
        target_col: Coluna do target.
        date_col: Coluna de data. Aceita datetime, ou texto ano-mês-dia.
        lags: Lista de lags a criar (default: [1,2,3,6,12]).
        rolling_windows: Janelas de rolling stats (default: [3,6,12]).
        calendar_features: Se True, adiciona mês, trimestre, dia da semana.
        entity_cols: Colunas que identificam a entidade do painel.
        date_format: Formato ``strftime`` da data em texto, obrigatório para
            qualquer formato que não seja ano-mês-dia.
        on_duplicate_dates: ``'raise'`` (default) recusa mais de uma linha por
            entidade e data, porque o lag ficaria dependente da ordem de entrada.
            ``'keep'`` mantém os empates e ordena de forma estável, preservando a
            ordem original entre linhas de mesma data.

    Returns:
        DataFrame com features adicionadas, em ordem cronológica. ``date_col``
        preserva o tipo e os valores originais.

    Raises:
        ValueError: Coluna ausente, chave de entidade nula, data
            nula/ambígua/inválida, lag não positivo, janela menor que 2, nome de
            feature já existente, empate de data sob a política ``'raise'``, ou
            ``on_duplicate_dates`` desconhecido.
    """
    if on_duplicate_dates not in {"raise", "keep"}:
        raise ValueError("on_duplicate_dates must be 'raise' or 'keep'")

    if entity_cols is None:
        grao: list[str] = []
    elif isinstance(entity_cols, (str, bytes)):
        raise ValueError("entity_cols must be a sequence of column names, not a string")
    else:
        grao = list(entity_cols)
    if not all(isinstance(column, str) and column for column in grao):
        raise ValueError("entity_cols must contain non-empty column names")
    if len(grao) != len(set(grao)):
        raise ValueError("entity_cols must not contain duplicate columns")

    if lags is None:
        lags = [1, 2, 3, 6, 12]
    if rolling_windows is None:
        rolling_windows = [3, 6, 12]
    if any(isinstance(lag, bool) or not isinstance(lag, int) or lag <= 0 for lag in lags):
        raise ValueError("lags must contain positive integers")
    if len(lags) != len(set(lags)):
        raise ValueError("lags must not contain duplicate values")
    if any(isinstance(w, bool) or not isinstance(w, int) or w < 2 for w in rolling_windows):
        raise ValueError("rolling_windows must contain integers >= 2 for sample std")
    if len(rolling_windows) != len(set(rolling_windows)):
        raise ValueError("rolling_windows must not contain duplicate values")

    generated_names = [f"lag_{lag}" for lag in lags]
    generated_names.extend(
        f"rolling_{stat}_{window}"
        for window in rolling_windows
        for stat in ("mean", "std", "min", "max")
    )
    if calendar_features:
        generated_names.extend(
            ("month", "quarter", "day_of_week", "day_of_year", "is_month_start", "is_month_end")
        )
    generated_names.append("trend")
    collisions = sorted(set(generated_names) & set(df.columns))
    if collisions:
        raise ValueError(
            "generated feature columns already exist; rename or remove them before calling: "
            f"{collisions}"
        )

    required = {target_col, date_col, *grao}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"columns not found: {sorted(missing)}")
    if grao and df[grao].isna().any(axis=None):
        null_counts = {column: int(df[column].isna().sum()) for column in grao if df[column].isna().any()}
        raise ValueError(
            "entity_cols contain null values; impute or remove them explicitly before feature "
            f"generation to avoid silently dropping entities: {null_counts}"
        )

    df = df.copy()

    # A chave de ordenação é derivada, não substitui a coluna do chamador: quem
    # depende do texto original para juntar com outra fonte continua podendo.
    ordem = _normalizar_datas(df[date_col], date_format)

    chaves = df[grao].copy() if grao else pd.DataFrame(index=df.index)
    nome_data = "__hub_data"
    while nome_data in chaves.columns:
        nome_data += "_"
    chaves[nome_data] = ordem
    empates = chaves.duplicated(keep=False)
    if empates.any() and on_duplicate_dates == "raise":
        exemplo = chaves[empates].iloc[0].to_dict()
        rotulo = " + ".join([*grao, "data"]) if grao else "data"
        raise ValueError(
            f"{int(empates.sum())} linha(s) repetem o grão ({rotulo}); o lag ficaria "
            f"dependente da ordem de entrada. Agregue antes de chamar ou use "
            f"on_duplicate_dates='keep' para aceitar empates. Exemplo: {exemplo}"
        )

    nome_ordem = "__hub_ordem"
    while nome_ordem in df.columns:
        nome_ordem += "_"
    df[nome_ordem] = ordem
    sort_cols = [*grao, nome_ordem]
    # mergesort é estável: com on_duplicate_dates='keep', empates preservam a
    # ordem original de entrada em vez de embaralhar em silêncio.
    df = df.sort_values(sort_cols, kind="mergesort")
    ordem_ordenada = df[nome_ordem]
    df = df.drop(columns=nome_ordem)

    groups = df.groupby(grao, sort=False)[target_col] if grao else None
    generated_required: list[str] = []

    # Lag features, always isolated by entity when entity columns are provided.
    for lag in lags:
        name = f"lag_{lag}"
        df[name] = groups.shift(lag) if groups is not None else df[target_col].shift(lag)
        generated_required.append(name)

    # Rolling features
    for w in rolling_windows:
        names = [f"rolling_{stat}_{w}" for stat in ("mean", "std", "min", "max")]
        generated_required.extend(names)
        if groups is None:
            shifted = df[target_col].shift(1)
            df[f"rolling_mean_{w}"] = shifted.rolling(w).mean()
            df[f"rolling_std_{w}"] = shifted.rolling(w).std()
            df[f"rolling_min_{w}"] = shifted.rolling(w).min()
            df[f"rolling_max_{w}"] = shifted.rolling(w).max()
        else:
            shifted = groups.shift(1)
            regrouped = shifted.groupby([df[column] for column in grao], sort=False)
            df[f"rolling_mean_{w}"] = regrouped.transform(lambda series: series.rolling(w).mean())
            df[f"rolling_std_{w}"] = regrouped.transform(lambda series: series.rolling(w).std())
            df[f"rolling_min_{w}"] = regrouped.transform(lambda series: series.rolling(w).min())
            df[f"rolling_max_{w}"] = regrouped.transform(lambda series: series.rolling(w).max())

    # Calendar features derivam da data já normalizada, nunca do texto cru.
    if calendar_features:
        dt = ordem_ordenada.dt
        df["month"] = dt.month
        df["quarter"] = dt.quarter
        df["day_of_week"] = dt.dayofweek
        df["day_of_year"] = dt.dayofyear
        df["is_month_start"] = dt.is_month_start.astype(int)
        df["is_month_end"] = dt.is_month_end.astype(int)

    # Trend
    df["trend"] = df.groupby(grao, sort=False).cumcount() if grao else range(len(df))

    # Remova somente warm-up criado por este helper. Missing preexistente em
    # coluna alheia pertence à política de imputação do pipeline consumidor.
    n_before = len(df)
    if generated_required:
        df = df.dropna(subset=generated_required).reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)
    print(f"Features temporais: {n_before - len(df)} linhas removidas por warm-up das features geradas")

    return df
