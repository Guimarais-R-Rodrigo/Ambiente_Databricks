"""Regression tests for critical driver-side helpers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


ASSISTANT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_snippets.constants.format_br import fmt_brl, fmt_pct
from hub_snippets.ml.lgbm_temporal import create_temporal_features
from hub_snippets.ml.metrics_report import calculate_binary_metrics, calculate_regression_metrics
from hub_snippets.ml.performance_monitor import (
    EXAMPLE_THRESHOLDS,
    PerformanceMonitor,
    selecionar_metricas_do_relatorio,
)
from hub_snippets.ml.curves_plotly import plot_lift_curve
from hub_snippets.ml.score_bands import generate_score_bands
from hub_snippets.ml.scorecard_builder import build_scorecard
from hub_snippets.ml.split_temporal import temporal_split
from hub_snippets.ml.vintage_analysis import build_vintage_table


class FormatTests(unittest.TestCase):
    def test_currency_rounding_carries_to_integer(self) -> None:
        self.assertEqual(fmt_brl(1.999), "R$ 2,00")
        self.assertEqual(fmt_brl(-1.999), "-R$ 2,00")

    def test_percent_scale_is_explicit(self) -> None:
        self.assertEqual(fmt_pct(1.0), "100,0%")
        self.assertEqual(fmt_pct(1.0, input_scale="percent"), "1,0%")


class MonitoringTests(unittest.TestCase):
    def test_improvement_does_not_trigger_retraining(self) -> None:
        monitor = PerformanceMonitor({"auc": 0.70})
        monitor.add_period("p1", {"auc": 0.80})
        self.assertEqual(monitor.get_current_status(), "🟢 Saudável")
        self.assertEqual(monitor.should_retrain()["decision"], "NO_TRIGGER")

    def test_incomplete_or_non_finite_period_is_rejected(self) -> None:
        monitor = PerformanceMonitor({"auc": 0.70, "ks_pct": 40.0})
        with self.assertRaisesRegex(ValueError, "missing monitored metrics"):
            monitor.add_period("p1", {"auc": 0.65})
        with self.assertRaisesRegex(ValueError, "finite"):
            monitor.add_period("p2", {"auc": np.nan, "ks_pct": 35.0})

    def test_metrics_report_ks_composes_with_monitor_in_percent_points(self) -> None:
        baseline = calculate_binary_metrics(
            np.array([0, 0, 1, 1]), np.array([0.1, 0.2, 0.8, 0.9])
        )
        monitor = PerformanceMonitor(
            {"ks_pct": baseline["ks_pct"]},
            policy={"ks_pct": EXAMPLE_THRESHOLDS["ks_pct"]},
        )
        monitor.add_period("p1", {"ks_pct": baseline["ks_pct"] - 1.0})
        self.assertEqual(monitor.get_current_status(), "🟢 Saudável")
        monitor.add_period("p2", {"ks_pct": baseline["ks_pct"] - 6.0})
        self.assertEqual(monitor.get_current_status(), "🔴 Crítico")

    def test_booleans_are_not_accepted_as_numeric_monitoring_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite numeric"):
            PerformanceMonitor({"auc": True})
        with self.assertRaisesRegex(ValueError, "positive"):
            PerformanceMonitor({"auc": 0.7}, consecutive_alert_periods=True)
        with self.assertRaisesRegex(ValueError, "boolean"):
            PerformanceMonitor({"auc": 0.7}, require_complete_metrics=1)

        monitor = PerformanceMonitor({"auc": 0.7})
        with self.assertRaisesRegex(ValueError, "finite numeric"):
            monitor.add_period("p1", {"auc": False})
        with self.assertRaisesRegex(ValueError, "non-negative integer"):
            monitor.add_period("p1", {"auc": 0.7}, n_predictions=True)

    def test_policy_thresholds_reject_booleans_and_non_finite_values(self) -> None:
        base_rule = {"warning": 0.03, "critical": 0.05, "direction": "higher", "delta": "absolute"}
        for key, value in (("warning", True), ("critical", float("inf"))):
            rule = dict(base_rule)
            rule[key] = value
            with self.subTest(key=key, value=value), self.assertRaisesRegex(ValueError, "finite numeric"):
                PerformanceMonitor({"auc": 0.7}, policy={"auc": rule})


class ScoreBandTests(unittest.TestCase):
    def test_best_scores_appear_first(self) -> None:
        result = generate_score_bands(
            np.arange(100, dtype=float),
            np.array([1] * 50 + [0] * 50),
            n_bands=5,
            higher_score_is_better=True,
        )
        self.assertGreater(result.iloc[0]["score_min"], result.iloc[-1]["score_min"])
        self.assertLess(result.iloc[0]["taxa_default"], result.iloc[-1]["taxa_default"])

    def test_constant_scores_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "must vary"):
            generate_score_bands(np.ones(4), np.array([0, 1, 0, 1]))


class MetricTests(unittest.TestCase):
    def test_binary_metrics_reject_one_class(self) -> None:
        with self.assertRaisesRegex(ValueError, "both classes"):
            calculate_binary_metrics(np.zeros(3), np.array([0.1, 0.2, 0.3]))

    def test_small_sample_lift_uses_at_least_one_row(self) -> None:
        metrics = calculate_binary_metrics(np.array([0, 1]), np.array([0.1, 0.9]))
        self.assertEqual(metrics["lift_10pct"], 2.0)

    def test_all_zero_actuals_report_undefined_mape(self) -> None:
        metrics = calculate_regression_metrics(np.zeros(3), np.ones(3))
        self.assertTrue(np.isnan(metrics["mape"]))


class ScorecardTests(unittest.TestCase):
    def test_bad_event_logit_reduces_score(self) -> None:
        table = pd.DataFrame({"faixa": ["low", "high"], "woe": [-1.0, 1.0]})
        result = build_scorecard(np.array([1.0]), 0.0, ["x"], {"x": table}, event_is_bad=True)
        points = result.set_index("faixa")["pontos"]
        self.assertGreater(points["low"], points["high"])

    def test_non_finite_coefficients_and_woe_are_rejected(self) -> None:
        table = pd.DataFrame({"faixa": ["x"], "woe": [1.0]})
        with self.assertRaisesRegex(ValueError, "finite"):
            build_scorecard(np.array([np.inf]), 0.0, ["x"], {"x": table})
        with self.assertRaisesRegex(ValueError, "finite"):
            build_scorecard(
                np.array([1.0]), 0.0, ["x"],
                {"x": pd.DataFrame({"faixa": ["x"], "woe": [np.nan]})},
            )


class TemporalTests(unittest.TestCase):
    def test_calendar_gap_is_respected(self) -> None:
        frame = pd.DataFrame(
            {"date": pd.date_range("2024-01-01", periods=24, freq="MS"), "value": range(24)}
        )
        train, validation, test = temporal_split(frame, "date", gap_periods=1, period_unit="M")
        self.assertLess(train["date"].max() + pd.offsets.MonthBegin(2), validation["date"].min() + pd.offsets.MonthBegin(1))
        self.assertLess(validation["date"].max(), test["date"].min())

    def test_entity_lags_do_not_cross_entities(self) -> None:
        frame = pd.DataFrame(
            {
                "entity": ["a"] * 4 + ["b"] * 4,
                "date": list(pd.date_range("2024-01-01", periods=4, freq="MS")) * 2,
                "target": [1, 2, 3, 4, 100, 200, 300, 400],
            }
        )
        result = create_temporal_features(
            frame,
            "target",
            "date",
            lags=[1],
            rolling_windows=[],
            calendar_features=False,
            entity_cols=["entity"],
        )
        b_first = result[result["entity"] == "b"].iloc[0]
        self.assertEqual(b_first["lag_1"], 100)

    def test_unrelated_missing_values_are_preserved(self) -> None:
        frame = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=4),
                "target": [1.0, 2.0, 3.0, 4.0],
                "aux": [None, 2.0, 3.0, 4.0],
            }
        )
        result = create_temporal_features(
            frame, "target", "date", lags=[1], rolling_windows=[], calendar_features=False
        )
        self.assertEqual(len(result), 3)

    def test_rolling_window_one_is_rejected(self) -> None:
        frame = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=4), "target": range(4)})
        with self.assertRaisesRegex(ValueError, ">= 2"):
            create_temporal_features(
                frame, "target", "date", lags=[], rolling_windows=[1], calendar_features=False
            )

    def test_null_entity_keys_are_rejected_instead_of_silently_dropped(self) -> None:
        frame = pd.DataFrame(
            {
                "entity": ["a", "a", None, None],
                "date": pd.to_datetime(["2026-01-01", "2026-01-02"] * 2),
                "target": [1.0, 2.0, 10.0, 20.0],
            }
        )
        with self.assertRaisesRegex(ValueError, "entity_cols contain null"):
            create_temporal_features(
                frame, "target", "date", lags=[1], rolling_windows=[],
                calendar_features=False, entity_cols=["entity"],
            )

    def test_generated_feature_name_collisions_are_rejected(self) -> None:
        base = {"date": pd.date_range("2026-01-01", periods=4), "target": range(4)}
        for existing in ("lag_1", "rolling_mean_2", "month", "trend"):
            frame = pd.DataFrame({**base, existing: 999})
            with self.subTest(existing=existing), self.assertRaisesRegex(ValueError, "already exist"):
                create_temporal_features(
                    frame, "target", "date", lags=[1], rolling_windows=[2],
                    calendar_features=True,
                )

    def test_temporal_parameters_reject_boolean_duplicate_and_string_sequences(self) -> None:
        frame = pd.DataFrame(
            {"entity": ["a"] * 4, "date": pd.date_range("2026-01-01", periods=4), "target": range(4)}
        )
        invalid = (
            ({"lags": [True], "rolling_windows": []}, "positive integers"),
            ({"lags": [1, 1], "rolling_windows": []}, "duplicate"),
            ({"lags": [], "rolling_windows": [2, 2]}, "duplicate"),
            ({"lags": [], "rolling_windows": [], "entity_cols": "entity"}, "not a string"),
        )
        for kwargs, message in invalid:
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, message):
                create_temporal_features(
                    frame, "target", "date", calendar_features=False, **kwargs
                )


    def test_textual_dates_are_ordered_chronologically_not_lexicographically(self) -> None:
        # '2026-1-10' precede '2026-1-2' na ordem lexicografica: sem normalizar a
        # data antes de ordenar, o lag do dia 2 recebia o valor do dia 10.
        frame = pd.DataFrame({"date": ["2026-1-1", "2026-1-2", "2026-1-10"], "target": [1, 2, 10]})
        result = create_temporal_features(
            frame, "target", "date", lags=[1], rolling_windows=[], calendar_features=False
        )
        lags = dict(zip(result["date"], result["lag_1"]))
        self.assertEqual(lags["2026-1-2"], 1)
        self.assertEqual(lags["2026-1-10"], 2)

    def test_typed_and_textual_dates_produce_the_same_sequence(self) -> None:
        valores = [1, 2, 10]
        textual = pd.DataFrame({"date": ["2026-1-1", "2026-1-2", "2026-1-10"], "target": valores})
        tipado = pd.DataFrame(
            {"date": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-10"]), "target": valores}
        )
        kwargs = dict(lags=[1], rolling_windows=[], calendar_features=False)
        esperado = create_temporal_features(tipado, "target", "date", **kwargs)["lag_1"].tolist()
        obtido = create_temporal_features(textual, "target", "date", **kwargs)["lag_1"].tolist()
        self.assertEqual(obtido, esperado)

    def test_explicit_day_first_format_crosses_months_correctly(self) -> None:
        # dd/mm/aaaa ordenado como texto agrupa pelo dia: 01/02 viria antes de
        # 02/01. O erro nao produz valor futuro, produz o passado errado.
        frame = pd.DataFrame(
            {"date": ["02/01/2026", "01/02/2026", "03/02/2026"], "target": [2, 100, 300]}
        )
        result = create_temporal_features(
            frame,
            "target",
            "date",
            lags=[1],
            rolling_windows=[],
            calendar_features=False,
            date_format="%d/%m/%Y",
        )
        lags = dict(zip(result["date"], result["lag_1"]))
        self.assertEqual(lags["01/02/2026"], 2)
        self.assertEqual(lags["03/02/2026"], 100)

    def test_shuffled_input_yields_the_same_features(self) -> None:
        frame = pd.DataFrame({"date": ["2026-1-1", "2026-1-2", "2026-1-10"], "target": [1, 2, 10]})
        kwargs = dict(lags=[1], rolling_windows=[], calendar_features=False)
        ordenado = create_temporal_features(frame, "target", "date", **kwargs)
        embaralhado = create_temporal_features(
            frame.iloc[[2, 0, 1]].reset_index(drop=True), "target", "date", **kwargs
        )
        pd.testing.assert_frame_equal(ordenado, embaralhado)

    def test_calendar_features_use_the_normalized_date(self) -> None:
        frame = pd.DataFrame({"date": ["2026-1-1", "2026-1-2", "2026-1-10"], "target": [1, 2, 10]})
        result = create_temporal_features(
            frame, "target", "date", lags=[1], rolling_windows=[], calendar_features=True
        )
        dia = dict(zip(result["date"], result["day_of_year"]))
        self.assertEqual(dia["2026-1-10"], 10)

    def test_ambiguous_textual_format_requires_explicit_date_format(self) -> None:
        frame = pd.DataFrame({"date": ["02/01/2026", "01/02/2026"], "target": [1, 2]})
        with self.assertRaisesRegex(ValueError, "date_format"):
            create_temporal_features(
                frame, "target", "date", lags=[1], rolling_windows=[], calendar_features=False
            )

    def test_date_format_that_does_not_match_is_rejected(self) -> None:
        frame = pd.DataFrame({"date": ["02/01/2026", "01/02/2026"], "target": [1, 2]})
        with self.assertRaisesRegex(ValueError, "nao casa|não casa"):
            create_temporal_features(
                frame,
                "target",
                "date",
                lags=[1],
                rolling_windows=[],
                calendar_features=False,
                date_format="%Y-%m-%d",
            )

    def test_null_and_invalid_dates_are_rejected(self) -> None:
        nulo = pd.DataFrame({"date": ["2026-01-01", None], "target": [1, 2]})
        with self.assertRaisesRegex(ValueError, "nulo"):
            create_temporal_features(
                nulo, "target", "date", lags=[1], rolling_windows=[], calendar_features=False
            )
        invalido = pd.DataFrame({"date": ["2026-02-30", "2026-03-01"], "target": [1, 2]})
        with self.assertRaisesRegex(ValueError, "calend"):
            create_temporal_features(
                invalido, "target", "date", lags=[1], rolling_windows=[], calendar_features=False
            )

    def test_numeric_date_column_is_rejected(self) -> None:
        frame = pd.DataFrame({"date": [20260101, 20260102], "target": [1, 2]})
        with self.assertRaisesRegex(ValueError, "date_format"):
            create_temporal_features(
                frame, "target", "date", lags=[1], rolling_windows=[], calendar_features=False
            )

    def test_duplicate_grain_is_rejected_unless_opted_in(self) -> None:
        frame = pd.DataFrame(
            {"date": ["2026-01-01", "2026-01-01", "2026-01-02"], "target": [1, 2, 3]}
        )
        with self.assertRaisesRegex(ValueError, "grão|grao"):
            create_temporal_features(
                frame, "target", "date", lags=[1], rolling_windows=[], calendar_features=False
            )
        aceito = create_temporal_features(
            frame,
            "target",
            "date",
            lags=[1],
            rolling_windows=[],
            calendar_features=False,
            on_duplicate_dates="keep",
        )
        # Ordenacao estavel: entre as duas linhas de 2026-01-01 a ordem de
        # entrada e preservada, logo o lag do dia 2 e o segundo empate.
        self.assertEqual(aceito.iloc[-1]["lag_1"], 2)


class VintageTests(unittest.TestCase):
    def test_cumulative_incidence_is_not_sum_of_rates(self) -> None:
        rows = []
        for contract, event_mob in [("a", 1), ("b", None)]:
            for mob in range(3):
                rows.append(
                    {
                        "contract": contract,
                        "origin": "2024-01-01",
                        "reference": pd.Timestamp("2024-01-01") + pd.DateOffset(months=mob),
                        "event": int(event_mob == mob),
                    }
                )
        result = build_vintage_table(
            pd.DataFrame(rows),
            "contract",
            "origin",
            "reference",
            "event",
        )
        self.assertTrue((result["taxa_acumulada"] <= 1).all())
        self.assertEqual(result.loc[result["mob"] == 2, "taxa_acumulada"].iloc[0], 0.5)

    def test_immature_ragged_cells_are_not_counted_as_non_events(self) -> None:
        frame = pd.DataFrame(
            [
                {"contract": "a", "origin": "2024-01-01", "reference": "2024-01-01", "event": 0},
                {"contract": "a", "origin": "2024-01-01", "reference": "2024-02-01", "event": 1},
                {"contract": "a", "origin": "2024-01-01", "reference": "2024-03-01", "event": 0},
                {"contract": "b", "origin": "2024-01-01", "reference": "2024-01-01", "event": 0},
            ]
        )
        result = build_vintage_table(frame, "contract", "origin", "reference", "event")
        self.assertEqual(result.loc[result["mob"] == 0, "taxa_acumulada"].iloc[0], 0.0)
        self.assertTrue(result.loc[result["mob"] == 1, "taxa_acumulada"].isna().iloc[0])
        self.assertEqual(result.loc[result["mob"] == 1, "cobertura_observada"].iloc[0], 0.5)

    def test_internal_snapshot_gap_is_not_fabricated(self) -> None:
        frame = pd.DataFrame(
            [
                {"contract": "a", "origin": "2024-01-01", "reference": "2024-01-01", "event": 1, "mob": 0},
                {"contract": "a", "origin": "2024-01-01", "reference": "2024-03-01", "event": 1, "mob": 2},
                {"contract": "b", "origin": "2024-01-01", "reference": "2024-01-01", "event": 0, "mob": 0},
                {"contract": "b", "origin": "2024-01-01", "reference": "2024-02-01", "event": 0, "mob": 1},
                {"contract": "b", "origin": "2024-01-01", "reference": "2024-03-01", "event": 0, "mob": 2},
            ]
        )
        result = build_vintage_table(
            frame, "contract", "origin", "reference", "event",
            mob_col="mob", target_is_cumulative=True,
        )
        middle = result.loc[result["mob"] == 1].iloc[0]
        self.assertTrue(pd.isna(middle["taxa_acumulada"]))
        self.assertEqual(middle["cobertura_observada"], 0.5)
        observed = result["taxa_acumulada"].dropna().to_numpy()
        self.assertTrue((np.diff(observed) >= 0).all())

    def test_late_entry_and_null_target_are_not_fabricated(self) -> None:
        late = pd.DataFrame(
            [{"contract": "a", "origin": "2024-01-01", "reference": "2024-02-01", "event": 0, "mob": 1}]
        )
        result = build_vintage_table(late, "contract", "origin", "reference", "event", mob_col="mob")
        self.assertEqual(result["mob"].min(), 1)
        with self.assertRaisesRegex(ValueError, "target cannot contain null"):
            build_vintage_table(
                late.assign(event=None), "contract", "origin", "reference", "event", mob_col="mob"
            )


class CurveTests(unittest.TestCase):
    def test_lift_requires_both_classes(self) -> None:
        with self.assertRaisesRegex(ValueError, "both classes"):
            plot_lift_curve(np.zeros(10), np.linspace(0.1, 0.9, 10))


class ReferenceChainTests(unittest.TestCase):
    """Cadeia sintética de referência: split -> features -> métricas -> monitor.

    Cada helper tem teste próprio. O que nenhum deles cobre é a costura: as
    unidades e os nomes que atravessam a fronteira entre um e o outro. Foi ali
    que o KS em escala errada passou despercebido.
    """

    def _painel(self) -> pd.DataFrame:
        datas = pd.date_range("2024-01-01", periods=24, freq="MS")
        linhas = []
        for entidade in ("a", "b"):
            for indice, data in enumerate(datas):
                linhas.append({"entity": entidade, "date": data, "value": float(indice)})
        return pd.DataFrame(linhas)

    def _relatorio(self) -> dict:
        rng = np.random.default_rng(42)
        y_true = np.repeat([0, 1], 200)
        y_prob = np.clip(
            np.where(y_true == 1, rng.normal(0.70, 0.12, 400), rng.normal(0.30, 0.12, 400)),
            0.001,
            0.999,
        )
        return calculate_binary_metrics(y_true, y_prob)

    def test_chain_runs_end_to_end_with_declared_units(self) -> None:
        painel = self._painel()
        treino, validacao, teste = temporal_split(painel, "date", gap_periods=1, period_unit="M")
        self.assertTrue(len(treino) and len(validacao) and len(teste))

        features = create_temporal_features(
            treino, "value", "date", lags=[1], rolling_windows=[], entity_cols=["entity"]
        )
        self.assertIn("lag_1", features.columns)

        selecionadas = selecionar_metricas_do_relatorio(self._relatorio())
        monitor = PerformanceMonitor(
            selecionadas, policy={chave: EXAMPLE_THRESHOLDS[chave] for chave in selecionadas}
        )
        monitor.add_period("p1", {**selecionadas, "auc": selecionadas["auc"] - 0.08})
        self.assertEqual(monitor.history[0]["auc_status"], "🔴")

    def test_raw_report_is_rejected_loudly_by_the_monitor(self) -> None:
        with self.assertRaisesRegex(ValueError, "policy is missing monitored metrics"):
            PerformanceMonitor(self._relatorio())

    def test_naive_name_matching_loses_auc_but_selection_keeps_it(self) -> None:
        relatorio = self._relatorio()
        ingenua = {c: v for c, v in relatorio.items() if c in EXAMPLE_THRESHOLDS}
        self.assertNotIn("auc", ingenua, "o relatório chama a métrica de auc_roc")

        selecionadas = selecionar_metricas_do_relatorio(relatorio)
        self.assertIn("auc", selecionadas)
        self.assertAlmostEqual(selecionadas["auc"], relatorio["auc_roc"])

    def test_ks_keeps_percent_points_across_the_boundary(self) -> None:
        relatorio = self._relatorio()
        selecionadas = selecionar_metricas_do_relatorio(relatorio)
        self.assertAlmostEqual(selecionadas["ks_pct"], relatorio["ks_pct"])
        self.assertGreater(selecionadas["ks_pct"], 1.0, "KS em pontos percentuais, não fração")

    def test_selection_without_any_policy_match_fails_instead_of_returning_empty(self) -> None:
        with self.assertRaisesRegex(ValueError, "nenhuma métrica"):
            selecionar_metricas_do_relatorio({"metrica_inventada": 1.0})

    def test_invalid_selected_metrics_fail_loudly(self) -> None:
        for value in (float("nan"), float("inf"), True, "0.8"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "inválida"):
                selecionar_metricas_do_relatorio({"auc_roc": value, "ks_pct": 40.0})

    def test_required_metrics_and_alias_conflicts(self) -> None:
        with self.assertRaisesRegex(ValueError, "obrigatórias ausentes"):
            selecionar_metricas_do_relatorio({"ks_pct": 40.0}, metricas_obrigatorias=["auc"])
        with self.assertRaisesRegex(ValueError, "conflitantes"):
            selecionar_metricas_do_relatorio({"auc": .5, "auc_roc": .8})
        result = selecionar_metricas_do_relatorio({"auc": .8, "auc_roc": .8})
        self.assertEqual(result, {"auc": .8})

    def test_explicit_metric_exclusion_is_allowed(self) -> None:
        policy = {"ks_pct": EXAMPLE_THRESHOLDS["ks_pct"]}
        result = selecionar_metricas_do_relatorio({"auc_roc": float("nan"), "ks_pct": 40.0}, policy)
        self.assertEqual(result, {"ks_pct": 40.0})

    def test_temporal_internal_names_preserve_user_columns_and_grain(self) -> None:
        frame = pd.DataFrame({
            "date": ["2026-1-10", "2026-1-1", "2026-1-2"] * 2,
            "target": [10, 1, 2, 100, 10, 20],
            "__hub_data": ["a"] * 3 + ["b"] * 3,
            "__hub_ordem": list("abcdef"),
            "__hub_ordem_": list(range(6)),
        })
        original = frame.copy(deep=True)
        result = create_temporal_features(frame, "target", "date", lags=[1],
            rolling_windows=[], calendar_features=False, entity_cols=["__hub_data"])
        self.assertEqual(result["lag_1"].tolist(), [1, 2, 10, 20])
        self.assertEqual(result["__hub_ordem"].tolist(), ["c", "a", "f", "d"])
        self.assertEqual(result["__hub_ordem_"].tolist(), [2, 0, 5, 3])
        pd.testing.assert_frame_equal(frame, original)



if __name__ == "__main__":
    unittest.main()
