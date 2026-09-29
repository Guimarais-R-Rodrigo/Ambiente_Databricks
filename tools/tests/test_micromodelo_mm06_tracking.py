"""Prova de contrato com MLflow simulado; não demonstra backend Databricks."""
from __future__ import annotations

import importlib
import json
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "ambiente_fonte/.assistant"))
tracking = importlib.import_module("hub_snippets.ml.mlflow_run.mlflow_run")
facade = importlib.import_module("hub_snippets.ml.mlflow_run")


class FakeMlflow:
    def __init__(self):
        self.calls = []
        self.status = None

    @contextmanager
    def start_run(self, *, run_name):
        self.calls.append(("start_run", run_name))
        try:
            yield object()
        except Exception:
            self.status = "FAILED"
            raise
        else:
            self.status = "FINISHED"

    def set_experiment(self, value):
        self.calls.append(("set_experiment", value))

    def set_tags(self, value):
        self.calls.append(("set_tags", value))

    def set_tag(self, key, value):
        self.calls.append(("set_tag", key, value))

    def log_params(self, value):
        self.calls.append(("log_params", value))

    def log_metrics(self, value):
        self.calls.append(("log_metrics", value))


class TrackingMM06Tests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeMlflow()
        self.patch = patch.object(tracking, "mlflow", self.fake)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.kwargs = {
            "tipo": "DEVELOPMENT", "spec_fingerprint": "a" * 64,
            "dataset": "synthetic:crm_fixture@2026-09",
            "split": "synthetic:treino agosto; teste setembro",
            "limitacoes": ["sem dados reais", "janela curta"],
            "contrato_saida": {
                "grain": "uma entidade sintética por data",
                "classification_field": "classificacao",
                "classification_values": ["TRUE", "FALSE", "INDETERMINADO"],
                "score_field": "score",
                "score_semantics": "FORCA_EVIDENCIA",
            },
        }

    def complete(self, tipo="DEVELOPMENT"):
        with tracking.run_micromodelo("lab_sintetico", **{**self.kwargs, "tipo": tipo}) as run:
            run.parametros({"regra": "sintetica_v1", "limiar": 70})
            run.agregados_medidos({"population": 4, "count_true": 1,
                                   "count_false": 1, "count_indeterminate": 2,
                                   "score_min": 0, "score_mean": 45, "score_max": 100},
                                  referencia_execucao="exec_sintetica_001")

    def test_all_run_types_are_complete_without_sklearn_or_individual_results(self):
        self.assertIs(facade.run_micromodelo, tracking.run_micromodelo)
        self.assertIs(facade.run_governado, tracking.run_governado)
        for kind in ("DEVELOPMENT", "VALIDATION", "SCORING"):
            with self.subTest(kind=kind):
                self.fake = FakeMlflow()
                with patch.object(tracking, "mlflow", self.fake):
                    self.complete(kind)
                self.assertEqual("FINISHED", self.fake.status)
                names = [x[0] for x in self.fake.calls]
                self.assertEqual(["start_run", "set_tags", "log_params", "log_metrics",
                                  "set_tag", "set_tag"], names)
                tags = self.fake.calls[1][1]
                self.assertEqual(kind, tags["mm06.run_type"])
                self.assertEqual("a" * 64, tags["mm06.spec_fingerprint"])
                self.assertEqual("classificacao", json.loads(tags["mm06.output_contract"])
                                 ["classification_field"])
                self.assertEqual(("set_tag", "mm06.complete", "true"), self.fake.calls[-1])
                self.assertFalse(any("artifact" in name or "model" in name for name in names))

    def test_incomplete_run_fails_and_does_not_claim_complete(self):
        with self.assertRaisesRegex(ValueError, "agregados_medidos"):
            with tracking.run_micromodelo("lab", **self.kwargs) as run:
                run.parametros({"regra": "x"})
        self.assertEqual("FAILED", self.fake.status)
        self.assertNotIn(("set_tag", "mm06.complete", "true"), self.fake.calls)

    def test_invalid_aggregates_do_not_log_metrics(self):
        for metrics in (
            {"population": 4, "count_true": 1, "count_false": 1,
             "count_indeterminate": 1},
            {"population": 1, "count_true": 1, "count_false": 0,
             "count_indeterminate": 0, "client_id": 123},
            {"population": 1, "count_true": 1, "count_false": 0,
             "count_indeterminate": 0, "score_min": 30},
            {"population": 10**100, "count_true": 10**100, "count_false": 0,
             "count_indeterminate": 0},
            {"population": 0, "count_true": 0, "count_false": 0,
             "count_indeterminate": 0, "score_min": 0,
             "score_mean": 0, "score_max": 0},
        ):
            with self.subTest(metrics=metrics):
                self.fake = FakeMlflow()
                with patch.object(tracking, "mlflow", self.fake):
                    with self.assertRaises(ValueError):
                        with tracking.run_micromodelo("lab", **self.kwargs) as run:
                            run.parametros({"regra": "x"})
                            run.agregados_medidos(metrics,
                                                  referencia_execucao="exec_sintetica")
                self.assertFalse(any(call[0] == "log_metrics" for call in self.fake.calls))

    def test_individual_id_cannot_be_logged_as_parameter(self):
        with self.assertRaisesRegex(ValueError, "parametros inválidos"):
            with tracking.run_micromodelo("lab", **self.kwargs) as run:
                run.parametros({"regra": "sintetica_v1", "client_id": "c_123"})
        self.assertFalse(any(call[0] == "log_params" for call in self.fake.calls))
        self.assertNotIn(("set_tag", "mm06.complete", "true"), self.fake.calls)

    def test_zero_population_without_scores_is_valid(self):
        with tracking.run_micromodelo("lab", **self.kwargs) as run:
            run.parametros({"regra": "sintetica_v1", "janela_dias": 30,
                            "politica_indeterminado": "INDETERMINADO"})
            run.agregados_medidos({"population": 0, "count_true": 0,
                                   "count_false": 0, "count_indeterminate": 0},
                                  referencia_execucao="exec_vazia")
        self.assertEqual("FINISHED", self.fake.status)

    def test_invalid_contract_or_non_synthetic_scope_fails_before_run(self):
        for update in (
            {"dataset": "catalogo_real.tabela"},
            {"tipo": "PUBLICACAO"},
            {"spec_fingerprint": "not-a-sha"},
            {"contrato_saida": {**self.kwargs["contrato_saida"], "rows": []}},
            {"contrato_saida": {**self.kwargs["contrato_saida"],
                                 "score_semantics": "PROBABILIDADE_CALIBRADA"}},
        ):
            with self.subTest(update=update), self.assertRaises(ValueError):
                with tracking.run_micromodelo("lab", **{**self.kwargs, **update}):
                    pass
        self.assertEqual([], self.fake.calls)

    def test_mlflow_absent_raises_import_error(self):
        with patch.object(tracking, "mlflow", None):
            with self.assertRaises(ImportError):
                with tracking.run_micromodelo("lab", **self.kwargs):
                    pass

    def test_score_metrics_require_output_score_field(self):
        contract = {**self.kwargs["contrato_saida"], "score_field": None,
                    "score_semantics": None}
        with self.assertRaisesRegex(ValueError, "score não declarado"):
            with tracking.run_micromodelo(
                "lab", **{**self.kwargs, "contrato_saida": contract}
            ) as run:
                run.parametros({"regra": "x"})
                run.agregados_medidos({"population": 1, "count_true": 1,
                                       "count_false": 0, "count_indeterminate": 0,
                                       "score_min": 50, "score_mean": 50,
                                       "score_max": 50},
                                      referencia_execucao="exec_sintetica")
        self.assertFalse(any(call[0] == "log_metrics" for call in self.fake.calls))

    def test_collector_cannot_log_after_context_closes(self):
        with tracking.run_micromodelo("lab", **self.kwargs) as run:
            run.parametros({"regra": "x"})
            run.agregados_medidos({"population": 1, "count_true": 1,
                                   "count_false": 0, "count_indeterminate": 0},
                                  referencia_execucao="exec_sintetica")
        calls_before = list(self.fake.calls)
        with self.assertRaisesRegex(ValueError, "encerrada"):
            run.agregados_medidos({"population": 1, "count_true": 1,
                                   "count_false": 0, "count_indeterminate": 0},
                                  referencia_execucao="outra")
        self.assertEqual(calls_before, self.fake.calls)

    def test_legacy_run_governado_signature_and_behavior_remain(self):
        with self.assertRaisesRegex(ValueError, "assinatura"):
            with tracking.run_governado("baseline", dataset="synthetic:dataset",
                                        split="synthetic:treino-teste",
                                        limitacoes=["teste"] ) as run:
                run.parametros({"algoritmo": "x"})
                run.metricas({"auc": 0.5})


if __name__ == "__main__":
    unittest.main()
