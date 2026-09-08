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
from hub_snippets.ml.performance_monitor import EXAMPLE_THRESHOLDS, PerformanceMonitor
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


if __name__ == "__main__":
    unittest.main()
