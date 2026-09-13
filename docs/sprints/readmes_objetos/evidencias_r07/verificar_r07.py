"""Suíte delimitada R07 para score, vintage e sobrevivência.

Sem dependências opcionais, os testes de runtime são pulados no uso local. O
freeze usa --require-runtime e transforma qualquer ausência/skip em falha.
"""
from __future__ import annotations

import argparse
import math
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
ASSISTANT = ROOT / "ambiente_fonte/.assistant"
if str(ASSISTANT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT))

OBJECTS = [
    "kaplan_meier",
    "score_bands",
    "scorecard_builder",
    "survival_cox",
    "vintage_analysis",
    "woe_iv_calculator",
]
REQUIRED_SECTIONS = [
    "## 1. O que é?",
    "## 2. Que problema este recurso resolve?",
    "## 3. Quando faz sentido usar?",
    "## 4. Quando não usar?",
    "## 5. Como funciona, intuitivamente?",
    "## 6. Exemplo de situação",
    "## 7. O que você precisa antes de usar?",
    "## 8. O que este recurso entrega?",
    "## 9. Como usar este recurso no Hub?",
    "## 10. Decisões e configurações que mais importam",
    "## 11. Limitações, riscos e armadilhas",
    "## 12. Quais são as alternativas?",
    "## 13. Como saber se o resultado faz sentido?",
    "## 14. Arquivos relacionados e próximos passos",
    "## 15. Referências",
]

RUNTIME_IMPORT_ERROR: Exception | None = None
try:
    import lifelines  # noqa: F401
    import plotly  # noqa: F401
    from pyspark.sql import SparkSession
    from hub_snippets.ml.kaplan_meier import plot_kaplan_meier, log_rank_test
    from hub_snippets.ml.score_bands import generate_score_bands
    from hub_snippets.ml.scorecard_builder import build_scorecard
    from hub_snippets.ml.survival_cox import train_cox_ph, validate_proportionality
    from hub_snippets.ml.vintage_analysis import build_vintage_table, compare_safras
    from hub_snippets.ml.woe_iv_calculator import calculate_woe_iv, classify_iv
except Exception as exc:  # pragma: no cover
    RUNTIME_IMPORT_ERROR = exc

RUNTIME_AVAILABLE = RUNTIME_IMPORT_ERROR is None


class StaticCases(unittest.TestCase):
    def test_six_readmes_have_contract_and_exact_section_order(self):
        for obj in OBJECTS:
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8")
            self.assertIn("<!-- readme-objeto: 1.0.0 -->", text, obj)
            indexes = [text.index(section) for section in REQUIRED_SECTIONS]
            self.assertEqual(indexes, sorted(indexes), obj)

    def test_readmes_do_not_claim_publication_homologation_or_independent_audit(self):
        forbidden = ["auditoria independente concluída", "publicado no databricks", "homologado no databricks"]
        for obj in OBJECTS:
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                self.assertNotIn(phrase, text, (obj, phrase))

    def test_km_plot_source_has_no_censor_marker_trace(self):
        text = (ASSISTANT / "hub_snippets/ml/kaplan_meier/kaplan_meier.py").read_text(encoding="utf-8")
        self.assertNotIn("show_censors", text)
        self.assertNotIn('mode="markers"', text)
        self.assertIn("pairwise_holm", text)

    def test_score_bands_default_direction_and_quantile_policy_are_explicit(self):
        text = (ASSISTANT / "hub_snippets/ml/score_bands/score_bands.py").read_text(encoding="utf-8")
        self.assertIn("higher_score_is_better: bool = True", text)
        self.assertIn('duplicates="drop"', text)
        self.assertIn('"aprovacao_acum": cumulative * 100', text)

    def test_scorecard_is_table_builder_not_row_scorer(self):
        text = (ASSISTANT / "hub_snippets/ml/scorecard_builder/scorecard_builder.py").read_text(encoding="utf-8")
        self.assertIn('"pontos": round(points, 0)', text)
        self.assertNotIn("def score_", text)
        self.assertIn("event_is_bad", text)

    def test_cox_metrics_are_fitted_model_metrics(self):
        text = (ASSISTANT / "hub_snippets/ml/survival_cox/survival_cox.py").read_text(encoding="utf-8")
        self.assertIn('"c_index": model.concordance_index_', text)
        self.assertIn('"aic": model.AIC_partial_', text)
        self.assertIn('.dropna().copy()', text)
        self.assertIn('summary["p"] < 0.05', text)

    def test_vintage_complete_cell_policy_is_in_source(self):
        text = (ASSISTANT / "hub_snippets/ml/vintage_analysis/vintage_analysis.py").read_text(encoding="utf-8")
        self.assertIn('complete_cell = agg["n_contratos_observados"] == agg["n_contratos_safra"]', text)
        self.assertIn("np.nan", text)
        self.assertIn("cummax()", text)

    def test_woe_has_spark_actions_and_no_binning_implementation(self):
        text = (ASSISTANT / "hub_snippets/ml/woe_iv_calculator/woe_iv_calculator.py").read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count(".collect()"), 2)
        self.assertIn("grouped.count()", text)
        self.assertNotIn("QuantileDiscretizer", text)


@unittest.skipUnless(RUNTIME_AVAILABLE, "lifelines/PySpark/Plotly não instalados")
class RuntimeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = (
            SparkSession.builder.master("local[1]")
            .appName("r07-readmes")
            .config("spark.ui.enabled", "false")
            .getOrCreate()
        )
        cls.spark.sparkContext.setLogLevel("ERROR")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_score_bands_respects_direction_and_cumulative_ends_at_100(self):
        scores = np.array([0.1, 0.2, 0.3, 0.8, 0.9, 1.0])
        y = np.array([0, 0, 0, 1, 1, 1])
        low_is_better = generate_score_bands(scores, y, n_bands=2, higher_score_is_better=False)
        high_is_better = generate_score_bands(scores, y, n_bands=2, higher_score_is_better=True)
        self.assertLess(low_is_better.iloc[0]["score_max"], low_is_better.iloc[-1]["score_min"])
        self.assertGreater(high_is_better.iloc[0]["score_min"], high_is_better.iloc[-1]["score_max"])
        self.assertAlmostEqual(float(low_is_better.iloc[-1]["aprovacao_acum"]), 100.0)

    def test_score_bands_can_collapse_tied_quantiles(self):
        scores = np.array([0.0] * 10 + [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        y = np.array([0] * 10 + [0, 0, 1, 1, 1, 1])
        out = generate_score_bands(scores, y, n_bands=5, higher_score_is_better=False)
        self.assertLess(len(out), 5)
        self.assertAlmostEqual(float(out["pct_base"].sum()), 100.0)

    def test_scorecard_orientation_and_rounding(self):
        table = {"x": pd.DataFrame({"faixa": ["baixo", "alto"], "woe": [-1.0, 1.0]})}
        out = build_scorecard(np.array([1.0]), 0.0, ["x"], table, pdo=20, base_score=600, base_odds=50, event_is_bad=True)
        self.assertEqual(len(out), 2)
        self.assertGreater(float(out.loc[out["faixa"] == "baixo", "pontos"].iloc[0]), float(out.loc[out["faixa"] == "alto", "pontos"].iloc[0]))
        self.assertTrue((out["pontos"] == out["pontos"].round(0)).all())

    def test_km_plot_uses_censoring_but_has_no_marker_trace(self):
        df = pd.DataFrame({"t": [1, 2, 3, 4, 1, 2, 3, 4], "e": [1, 0, 1, 0, 1, 1, 0, 0], "g": ["A"] * 4 + ["B"] * 4})
        fig = plot_kaplan_meier(df, "t", "e", "g", ci=False)
        self.assertEqual(len(fig.data), 2)
        self.assertTrue(all(trace.mode == "lines" for trace in fig.data))

    def test_logrank_return_shape_changes_for_two_vs_three_groups(self):
        two = pd.DataFrame({"t": [1, 2, 3, 4, 2, 3, 4, 5], "e": [1, 1, 0, 1, 1, 0, 1, 1], "g": ["A"] * 4 + ["B"] * 4})
        r2 = log_rank_test(two, "t", "e", "g")
        self.assertEqual(set(r2), {"statistic", "p_value"})
        three = pd.concat([two, pd.DataFrame({"t": [1.5, 2.5, 3.5, 5.5], "e": [1, 0, 1, 1], "g": ["C"] * 4})], ignore_index=True)
        r3 = log_rank_test(three, "t", "e", "g")
        self.assertEqual(set(r3), {"global", "pairwise_holm"})
        self.assertEqual(len(r3["pairwise_holm"]), 3)
        for item in r3["pairwise_holm"].values():
            self.assertGreaterEqual(item["p_value_holm"] + 1e-15, item["p_value_raw"])

    def test_cox_complete_case_and_ph_output(self):
        rng = np.random.default_rng(7)
        n = 220
        x = rng.normal(size=n)
        hazard = np.exp(0.45 * x)
        raw_t = rng.exponential(8.0 / hazard)
        duration = np.minimum(raw_t, 10.0)
        event = (raw_t <= 10.0).astype(int)
        df = pd.DataFrame({"duration": duration, "event": event, "x": x})
        df.loc[0, "x"] = np.nan
        model, metrics = train_cox_ph(df, "duration", "event", ["x"], log_mlflow=False)
        self.assertEqual(metrics["n_observations"], n - 1)
        self.assertTrue(math.isfinite(float(metrics["c_index"])))
        ph = validate_proportionality(model, df, "duration", "event")
        self.assertIn("violates_at_0_05", ph.columns)
        self.assertIn("p", ph.columns)

    def test_vintage_partial_cell_stays_nan(self):
        df = pd.DataFrame({
            "id": ["A", "B", "A", "B", "A"],
            "orig": ["2025-01-01"] * 5,
            "ref": ["2025-01-01", "2025-01-01", "2025-02-01", "2025-02-01", "2025-03-01"],
            "mob": [0, 0, 1, 1, 2],
            "event": [0, 0, 1, 0, 1],
        })
        out = build_vintage_table(df, "id", "orig", "ref", "event", mob_col="mob")
        mob1 = out[out["mob"] == 1].iloc[0]
        mob2 = out[out["mob"] == 2].iloc[0]
        self.assertAlmostEqual(float(mob1["taxa_acumulada"]), 0.5)
        self.assertAlmostEqual(float(mob2["cobertura_observada"]), 0.5)
        self.assertTrue(pd.isna(mob2["taxa_acumulada"]))

    def test_vintage_rejects_decreasing_cumulative_target(self):
        df = pd.DataFrame({"id": ["A", "A"], "orig": ["2025-01-01"] * 2, "ref": ["2025-01-01", "2025-02-01"], "mob": [0, 1], "event": [1, 0]})
        with self.assertRaises(ValueError):
            build_vintage_table(df, "id", "orig", "ref", "event", mob_col="mob", target_is_cumulative=True)

    def test_compare_safras_keeps_missing_checkpoint_as_nan(self):
        vintage = pd.DataFrame({
            "safra": ["2025-01", "2025-01", "2025-02"],
            "mob": [3, 6, 3],
            "n_contratos_safra": [100, 100, 100],
            "taxa_acumulada": [0.1, 0.2, 0.12],
        })
        out = compare_safras(vintage, [3, 6])
        self.assertTrue(pd.isna(out.loc[out["safra"] == "2025-02", "taxa_mob_6"].iloc[0]))

    def test_woe_runtime_returns_spark_table_and_finite_iv(self):
        sdf = self.spark.createDataFrame([
            ("A", 0), ("A", 0), ("A", 1),
            ("B", 0), ("B", 1), ("B", 1),
        ], ["faixa", "target"])
        out, iv = calculate_woe_iv(sdf, "faixa", "target", smoothing=0.5)
        self.assertEqual(out.count(), 2)
        self.assertTrue(math.isfinite(float(iv)))
        self.assertTrue({"faixa", "n_bom", "n_mau", "pct_bom", "pct_mau", "woe", "iv_partial"} <= set(out.columns))

    def test_woe_rejects_invalid_target(self):
        sdf = self.spark.createDataFrame([("A", 0), ("B", 2), ("C", 1)], ["faixa", "target"])
        with self.assertRaises(ValueError):
            calculate_woe_iv(sdf, "faixa", "target")

    def test_iv_classification_boundaries_and_invalid_values(self):
        self.assertIn("Inútil", classify_iv(0.0))
        self.assertIn("Fraca", classify_iv(0.02))
        self.assertIn("Média", classify_iv(0.10))
        self.assertIn("Forte", classify_iv(0.30))
        self.assertIn("Elevada", classify_iv(0.50))
        for bad in (-0.1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                classify_iv(bad)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-runtime", action="store_true")
    args = parser.parse_args()
    if args.require_runtime and not RUNTIME_AVAILABLE:
        raise SystemExit(f"runtime R07 obrigatório indisponível: {RUNTIME_IMPORT_ERROR!r}")
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.require_runtime and result.skipped:
        raise SystemExit(f"runtime R07 obrigatório teve skips: {result.skipped}")
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
