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
from hub_snippets.ml.performance_monitor import PerformanceMonitor
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
        monitor = PerformanceMonitor({"auc": 0.70, "ks": 0.40})
        with self.assertRaisesRegex(ValueError, "missing monitored metrics"):
            monitor.add_period("p1", {"auc": 0.65})
        with self.assertRaisesRegex(ValueError, "finite"):
            monitor.add_period("p2", {"auc": np.nan, "ks": 0.35})


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


if __name__ == "__main__":
    unittest.main()
