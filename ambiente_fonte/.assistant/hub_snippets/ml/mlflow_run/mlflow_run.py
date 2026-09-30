# -*- coding: utf-8 -*-
"""Registro MLflow com os campos que as instruções pessoais exigem.

As instruções pedem registrar parâmetros, métricas, dataset/split, artefatos,
assinatura e limitações. Os wrappers de treino registram apenas os dois
primeiros, e o restante depende de alguém lembrar — o que significa que cada
conversa registra de um jeito e as execuções deixam de ser comparáveis.

Este contexto inverte o ônus: a execução **falha ao fechar** se o conjunto
mínimo não tiver sido informado. O valor aqui é a convenção, não o código.

Uso:

    with run_governado(
        "baseline_churn",
        dataset="catalogo.crm.features_churn@2026-08",
        split="temporal: treino <= 2026-05, teste 2026-06/07",
        limitacoes=["sem dados de canal digital", "safra 2026-04 incompleta"],
    ) as run:
        run.parametros({"algoritmo": "lightgbm", "num_leaves": 31})
        run.metricas({"auc_val": 0.78, "ks_val": 0.41})
        run.modelo(modelo, exemplo_entrada=X_val.head(5))
"""

from __future__ import annotations

from contextlib import contextmanager
import json
import math
import re
from typing import Any, Dict, Iterable, Iterator, Optional

try:  # a biblioteca é opcional; o import não pode derrubar o módulo
    import mlflow
except ImportError:  # pragma: no cover - depende do ambiente
    mlflow = None


class _RunGovernado:
    """Coletor que registra no MLflow e sabe o que ainda falta."""

    def __init__(self, dataset: str, split: str, limitacoes: Iterable[str]) -> None:
        self.dataset = dataset
        self.split = split
        self.limitacoes = list(limitacoes)
        self._tem_parametros = False
        self._tem_metricas = False
        self._tem_assinatura = False

    def parametros(self, valores: Dict[str, Any]) -> None:
        """Registra hiperparâmetros e escolhas de modelagem."""
        if not valores:
            raise ValueError("informe ao menos um parâmetro")
        if mlflow is not None:
            mlflow.log_params(valores)
        self._tem_parametros = True

    def metricas(self, valores: Dict[str, float]) -> None:
        """Registra métricas já calculadas na população de avaliação."""
        if not valores:
            raise ValueError("informe ao menos uma métrica")
        if mlflow is not None:
            mlflow.log_metrics({k: float(v) for k, v in valores.items()})
        self._tem_metricas = True

    def modelo(self, modelo: Any, *, exemplo_entrada: Any = None, nome: str = "model") -> None:
        """Registra o modelo com assinatura inferida do exemplo de entrada.

        Sem ``exemplo_entrada`` não há assinatura, e sem assinatura o modelo
        registrado não declara o contrato de entrada — motivo pelo qual o
        parâmetro é cobrado no fechamento.
        """
        if mlflow is not None:
            # O nome do parâmetro mudou entre versões do MLflow: `artifact_path`
            # nas 2.x, `name` a partir da 3. Tentar os dois evita prender o
            # helper a uma versão específica do runtime.
            try:
                mlflow.sklearn.log_model(
                    modelo, artifact_path=nome, input_example=exemplo_entrada
                )
            except TypeError:
                mlflow.sklearn.log_model(
                    modelo, name=nome, input_example=exemplo_entrada
                )
        self._tem_assinatura = exemplo_entrada is not None

    def artefato(self, caminho_local: str) -> None:
        """Anexa um arquivo (gráfico, relatório, amostra de predição)."""
        if mlflow is not None:
            mlflow.log_artifact(caminho_local)

    def pendencias(self) -> list:
        faltando = []
        if not self._tem_parametros:
            faltando.append("parametros")
        if not self._tem_metricas:
            faltando.append("metricas")
        if not self._tem_assinatura:
            faltando.append("assinatura (chame modelo(..., exemplo_entrada=...))")
        return faltando


@contextmanager
def run_governado(
    nome: str,
    *,
    dataset: str,
    split: str,
    limitacoes: Iterable[str],
    experimento: Optional[str] = None,
    exigir_completo: bool = True,
) -> Iterator[_RunGovernado]:
    """Abre um run exigindo o conjunto mínimo de registro.

    Args:
        nome: identificação do run.
        dataset: origem e recorte dos dados, incluindo versão ou data de corte.
            Texto livre, mas deve permitir reconstruir o conjunto.
        split: como treino, validação e teste foram separados. Em problema
            temporal, declare os períodos, não apenas a proporção.
        limitacoes: o que o resultado **não** sustenta. Lista vazia é recusada:
            um modelo sem limitação declarada normalmente significa limitação
            não examinada.
        experimento: caminho do experimento MLflow; usa o padrão se omitido.
        exigir_completo: quando ``True``, fechar o contexto sem parâmetros,
            métricas ou assinatura levanta erro.

    Yields:
        Coletor com ``parametros``, ``metricas``, ``modelo`` e ``artefato``.

    Raises:
        ValueError: campo obrigatório vazio, ou registro incompleto no fechamento.
        ImportError: MLflow ausente no ambiente.
    """
    if mlflow is None:
        raise ImportError("mlflow é necessário para run_governado")
    for campo, valor in (("nome", nome), ("dataset", dataset), ("split", split)):
        if not str(valor).strip():
            raise ValueError(f"{campo} não pode ser vazio")
    limitacoes = [str(item).strip() for item in limitacoes if str(item).strip()]
    if not limitacoes:
        raise ValueError(
            "declare ao menos uma limitação; ausência de limitação costuma "
            "significar limitação não examinada"
        )

    if experimento:
        mlflow.set_experiment(experimento)

    coletor = _RunGovernado(dataset, split, limitacoes)
    with mlflow.start_run(run_name=nome):
        mlflow.set_tags({
            "dataset": dataset,
            "split": split,
            "limitacoes": " | ".join(limitacoes),
        })
        yield coletor
        pendentes = coletor.pendencias()
        if pendentes and exigir_completo:
            raise ValueError(
                "run incompleto segundo a política de registro: "
                + ", ".join(pendentes)
            )


_MM_RUN_TYPES = frozenset({"DEVELOPMENT", "VALIDATION", "SCORING"})
_MM_AGGREGATES = frozenset({"population", "count_true", "count_false",
                            "count_indeterminate", "score_min", "score_max",
                            "score_mean", "score_count"})
_MM_COUNTS = frozenset({"population", "count_true", "count_false",
                        "count_indeterminate"})
_MM_SCORES = frozenset({"score_min", "score_max", "score_mean"})
_MM_PARAMETERS = frozenset({"regra", "versao_regra", "limiar", "janela_dias",
                            "normalizacao", "politica_indeterminado",
                            "score_habilitado"})
_MM_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,63}\Z")
_MM_RULE_LABEL = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{0,99}\Z")
_MM_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _mm_text(value: Any, field: str, maximum: int = 500) -> str:
    if type(value) is not str or not value.strip() or len(value) > maximum:
        raise ValueError(f"{field} inválido")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{field} inválido")
    return value.strip()


def _mm_output_contract(value: Any) -> str:
    """Contrato fechado; resultados individuais não cabem nesta superfície."""
    required = {"grain", "classification_field", "classification_values",
                "score_field", "score_semantics"}
    if type(value) is not dict or set(value) != required:
        raise ValueError("contrato_saida inválido")
    _mm_text(value["grain"], "grain")
    for field in ("classification_field", "score_field"):
        item = value[field]
        if item is None and field == "score_field":
            continue
        if type(item) is not str or _MM_NAME.fullmatch(item) is None:
            raise ValueError("contrato_saida inválido")
    classes = value["classification_values"]
    if type(classes) not in (tuple, list) or len(classes) != 3 or \
            any(type(item) is not str for item in classes) or set(classes) != {
        "TRUE", "FALSE", "INDETERMINADO"
    }:
        raise ValueError("contrato_saida inválido")
    semantics = value["score_semantics"]
    if value["score_field"] is None:
        if semantics is not None:
            raise ValueError("contrato_saida inválido")
    elif semantics != "FORCA_EVIDENCIA":
        raise ValueError("contrato_saida inválido")
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class _RunMicromodelo:
    """Coletor rule-based: configuração e métricas agregadas, sem modelo ou linhas."""

    def __init__(self, *, has_score: bool) -> None:
        self._tem_parametros = False
        self._tem_agregados = False
        self._has_score = has_score
        self._score_enabled: bool | None = None
        self._has_score_metrics = False
        self._active = True

    def _require_active(self) -> None:
        if not self._active:
            raise ValueError("run MM06 já encerrada")

    def parametros(self, valores: Dict[str, Any]) -> None:
        self._require_active()
        if type(valores) is not dict or not valores or not set(valores) <= _MM_PARAMETERS:
            raise ValueError("parametros inválidos")
        clean: dict[str, Any] = {}
        for key, value in valores.items():
            if key in {"regra", "versao_regra"}:
                if type(value) is not str or _MM_RULE_LABEL.fullmatch(value) is None:
                    raise ValueError("parametros inválidos")
                clean[key] = value
            elif key == "limiar":
                if type(value) not in (int, float) or not 0 <= value <= 100 or \
                        (type(value) is float and not math.isfinite(value)):
                    raise ValueError("parametros inválidos")
                clean[key] = value
            elif key == "janela_dias":
                if type(value) is not int or not 1 <= value <= 3650:
                    raise ValueError("parametros inválidos")
                clean[key] = value
            elif key == "normalizacao":
                if type(value) is not str or value not in {
                    "PENDENTE", "SOMA_PONDERADA_0_100", "MIN_MAX_0_100",
                    "LINEAR_0_100", "CUSTOM_APROVADO"
                }:
                    raise ValueError("parametros inválidos")
                clean[key] = value
            elif key == "politica_indeterminado":
                if value != "INDETERMINADO":
                    raise ValueError("parametros inválidos")
                clean[key] = value
            elif key == "score_habilitado" and type(value) is bool:
                clean[key] = value
            else:
                raise ValueError("parametros inválidos")
        if clean.get("score_habilitado") is True and not self._has_score:
            raise ValueError("score habilitado sem campo no contrato de saída")
        if clean.get("score_habilitado") is False and self._has_score_metrics:
            raise ValueError("score desabilitado com métricas de score")
        mlflow.log_params(clean)
        if "score_habilitado" in clean:
            self._score_enabled = clean["score_habilitado"]
        self._tem_parametros = True

    def agregados_medidos(self, valores: Dict[str, Any], *,
                          referencia_execucao: str) -> None:
        self._require_active()
        if self._tem_agregados:
            raise ValueError("agregados já registrados")
        if type(valores) is not dict or not _MM_COUNTS <= set(valores) or \
                not set(valores) <= _MM_AGGREGATES:
            raise ValueError("agregados inválidos")
        for key in _MM_COUNTS:
            if type(valores[key]) is not int or not 0 <= valores[key] <= 2**53:
                raise ValueError("contagens inválidas")
        if sum(valores[key] for key in _MM_COUNTS - {"population"}) != valores["population"]:
            raise ValueError("contagens não reconciliadas")
        scores = set(valores) & _MM_SCORES
        score_count = valores.get("score_count")
        if score_count is not None and (type(score_count) is not int or
                                        not 0 <= score_count <= valores["population"]):
            raise ValueError("score_count inválido")
        if scores and not self._has_score:
            raise ValueError("score não declarado no contrato de saída")
        if score_count is not None and not self._has_score:
            raise ValueError("score não declarado no contrato de saída")
        if scores and self._score_enabled is False:
            raise ValueError("score desabilitado com métricas de score")
        if scores and valores["population"] == 0:
            raise ValueError("score sem população medida")
        if scores and scores != _MM_SCORES:
            raise ValueError("estatísticas de score incompletas")
        if scores and (score_count is None or score_count == 0):
            raise ValueError("score_count necessário para estatísticas de score")
        if not scores and score_count not in (None, 0):
            raise ValueError("score_count sem estatísticas de score")
        if scores:
            low, mean, high = (valores["score_min"], valores["score_mean"],
                               valores["score_max"])
            finite = lambda x: (type(x) is int and abs(x) <= 2**53) or \
                (type(x) is float and math.isfinite(x))
            if any(not finite(x) for x in (low, mean, high)) or \
                    not 0 <= low <= mean <= high <= 100:
                raise ValueError("estatísticas de score inválidas")
        reference = _mm_text(referencia_execucao, "referencia_execucao", 200)
        mlflow.log_metrics({key: float(value) for key, value in valores.items()})
        mlflow.set_tag("mm06.measurement_ref", reference)
        self._has_score_metrics = bool(scores)
        self._tem_agregados = True

    def pendencias(self) -> list[str]:
        result = []
        if not self._tem_parametros:
            result.append("parametros")
        if not self._tem_agregados:
            result.append("agregados_medidos")
        return result


@contextmanager
def run_micromodelo(
    nome: str, *, tipo: str, spec_fingerprint: str, dataset: str,
    split: str, limitacoes: Iterable[str], contrato_saida: dict[str, Any],
    experimento: Optional[str] = None,
) -> Iterator[_RunMicromodelo]:
    """Run MM06 rule-based E0; exige fechamento completo e dados sintéticos.

    ``synthetic:`` é declaração do caller, não detector de dados reais. As
    métricas aceitas são apenas agregados reconciliados; não há API de artifact,
    predição individual, modelo sklearn ou relaxamento de completude.
    """
    if mlflow is None:
        raise ImportError("mlflow é necessário para run_micromodelo")
    name = _mm_text(nome, "nome", 128)
    if type(tipo) is not str or tipo not in _MM_RUN_TYPES:
        raise ValueError("tipo inválido")
    if type(spec_fingerprint) is not str or _MM_SHA256.fullmatch(spec_fingerprint) is None:
        raise ValueError("spec_fingerprint inválido")
    dataset_ref = _mm_text(dataset, "dataset")
    split_ref = _mm_text(split, "split")
    if not dataset_ref.startswith("synthetic:") or not split_ref.startswith("synthetic:"):
        raise ValueError("dataset e split devem declarar escopo sintético")
    if limitacoes is None or type(limitacoes) in (str, bytes):
        raise ValueError("limitacoes inválidas")
    limits = [_mm_text(item, "limitacao") for item in limitacoes]
    if not limits or len(limits) > 20:
        raise ValueError("limitacoes inválidas")
    output_json = _mm_output_contract(contrato_saida)
    if experimento is not None:
        mlflow.set_experiment(_mm_text(experimento, "experimento"))
    collector = _RunMicromodelo(has_score=contrato_saida["score_field"] is not None)
    try:
        with mlflow.start_run(run_name=name):
            mlflow.set_tags({
                "mm06.run_type": tipo,
                "mm06.spec_fingerprint": spec_fingerprint,
                "mm06.dataset": dataset_ref,
                "mm06.split": split_ref,
                "mm06.limitacoes": " | ".join(limits),
                "mm06.output_contract": output_json,
                "mm06.complete": "false",
            })
            yield collector
            pending = collector.pendencias()
            if pending:
                raise ValueError("run MM06 incompleta: " + ", ".join(pending))
            mlflow.set_tag("mm06.complete", "true")
    finally:
        collector._active = False
