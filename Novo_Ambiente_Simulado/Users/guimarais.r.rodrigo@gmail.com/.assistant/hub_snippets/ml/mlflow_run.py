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
