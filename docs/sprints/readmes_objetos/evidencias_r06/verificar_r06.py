"""Suíte delimitada R06 para séries, features e validação temporal.

Sem pmdarima/Prophet, os casos dessas bibliotecas são pulados. O fechamento remoto
usa --require-models e instala dependências somente no ambiente isolado do runner.
"""
from __future__ import annotations

import argparse
import ast
import math
import sys
import types
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
ASSISTANT = ROOT / "ambiente_fonte/.assistant"
if str(ASSISTANT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT))

# arima_wrapper e prophet_wrapper importam MLflow no topo. Os testes usam
# log_mlflow=False e isolam esse efeito externo com um stub explícito.
if "mlflow" not in sys.modules:
    mlflow_stub = types.ModuleType("mlflow")
    mlflow_stub.log_params = lambda *_a, **_k: None
    mlflow_stub.log_metrics = lambda *_a, **_k: None
    sys.modules["mlflow"] = mlflow_stub

from hub_snippets.ml.lgbm_temporal import create_temporal_features
from hub_snippets.ml.split_temporal import temporal_split
from hub_snippets.ml.walk_forward import walk_forward_cv

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
OBJECTS = [
    "arima_wrapper",
    "lgbm_temporal",
    "prophet_wrapper",
    "split_temporal",
    "walk_forward",
]

MODEL_IMPORT_ERROR: Exception | None = None
try:
    import pmdarima  # noqa: F401
    import prophet  # noqa: F401
    from hub_snippets.ml.arima_wrapper import train_arima
    from hub_snippets.ml.prophet_wrapper import train_prophet
except Exception as exc:  # pragma: no cover - dependency-free local run
    MODEL_IMPORT_ERROR = exc

MODELS_AVAILABLE = MODEL_IMPORT_ERROR is None


def imports_in(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


class StaticCases(unittest.TestCase):
    def test_five_readmes_have_contract_and_exact_section_order(self):
        for obj in OBJECTS:
            path = ASSISTANT / f"hub_snippets/ml/{obj}/README.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("<!-- readme-objeto: 1.0.0 -->", text, obj)
            indexes = [text.index(section) for section in REQUIRED_SECTIONS]
            self.assertEqual(indexes, sorted(indexes), obj)

    def test_readmes_do_not_claim_publication_or_independent_audit(self):
        forbidden = [
            "auditoria independente concluída",
            "publicado no databricks",
            "homologado no databricks",
        ]
        for obj in OBJECTS:
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                self.assertNotIn(phrase, text, (obj, phrase))

    def test_lgbm_temporal_does_not_import_lightgbm(self):
        path = ASSISTANT / "hub_snippets/ml/lgbm_temporal/lgbm_temporal.py"
        imported = imports_in(path)
        self.assertFalse(any(name.startswith("lightgbm") for name in imported), imported)
        self.assertIn("create_temporal_features", path.read_text(encoding="utf-8"))

    def test_arima_current_path_is_stepwise_and_does_not_return_conf_int(self):
        text = (ASSISTANT / "hub_snippets/ml/arima_wrapper/arima_wrapper.py").read_text(encoding="utf-8")
        self.assertIn("stepwise=True", text)
        self.assertIn("random_state=SEED", text)
        self.assertIn("n_fits=50", text)
        self.assertIn("forecast, conf_int = model.predict", text)
        self.assertIn("return model, forecast, metrics", text)
        self.assertNotIn("return model, forecast, conf_int", text)

    def test_prophet_seed_is_declared_but_not_consumed_by_function(self):
        text = (ASSISTANT / "hub_snippets/ml/prophet_wrapper/prophet_wrapper.py").read_text(encoding="utf-8")
        self.assertEqual(text.count("SEED"), 1)
        self.assertIn("make_future_dataframe(periods=periods, freq=freq)", text)
        self.assertIn('merged["y"]', text)

    def test_split_uses_observed_periods_and_entity_disjoint_filter(self):
        text = (ASSISTANT / "hub_snippets/ml/split_temporal/split_temporal.py").read_text(encoding="utf-8")
        self.assertIn('result["__period"].dropna().unique()', text)
        self.assertIn("val = val[~val[group_col].isin(train_groups)]", text)
        self.assertIn("test = test[~test[group_col].isin(earlier_groups)]", text)

    def test_walk_forward_observed_periods_and_metadata_overwrite(self):
        text = (ASSISTANT / "hub_snippets/ml/walk_forward/walk_forward.py").read_text(encoding="utf-8")
        self.assertIn('data["__period"].dropna().unique()', text)
        self.assertIn("fold_metrics.update(", text)
        self.assertIn('"n_train": len(train_df)', text)
        self.assertIn("return results", text)


class PandasRuntimeCases(unittest.TestCase):
    def test_temporal_features_entity_isolation_and_warmup(self):
        df = pd.DataFrame({
            "id": ["B", "A", "B", "A", "B", "A"],
            "dt": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-02-01", "2026-02-01", "2026-03-01", "2026-03-01"]),
            "valor": [100.0, 10.0, 101.0, 11.0, 102.0, 12.0],
        })
        out = create_temporal_features(
            df,
            target_col="valor",
            date_col="dt",
            lags=[1],
            rolling_windows=[],
            calendar_features=False,
            entity_cols=["id"],
        )
        self.assertEqual(len(out), 4)
        a = out[out["id"] == "A"].sort_values("dt")
        b = out[out["id"] == "B"].sort_values("dt")
        self.assertEqual(a["lag_1"].tolist(), [10.0, 11.0])
        self.assertEqual(b["lag_1"].tolist(), [100.0, 101.0])

    def test_temporal_features_without_entity_rejects_duplicate_dates_by_default(self):
        df = pd.DataFrame({
            "id": ["A", "B", "A", "B"],
            "dt": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-02-01", "2026-02-01"]),
            "valor": [1.0, 10.0, 2.0, 11.0],
        })
        with self.assertRaisesRegex(ValueError, "repetem o grão"):
            create_temporal_features(
                df,
                target_col="valor",
                date_col="dt",
                lags=[1],
                rolling_windows=[],
                calendar_features=False,
            )

    def test_temporal_features_lag_is_previous_observation_not_calendar_duration(self):
        df = pd.DataFrame({
            "dt": pd.to_datetime(["2026-01-01", "2026-03-01", "2026-04-01"]),
            "valor": [1.0, 2.0, 3.0],
        })
        out = create_temporal_features(
            df,
            target_col="valor",
            date_col="dt",
            lags=[1],
            rolling_windows=[],
            calendar_features=False,
        )
        self.assertEqual(str(out.iloc[0]["dt"].date()), "2026-03-01")
        self.assertEqual(out.iloc[0]["lag_1"], 1.0)

    def test_temporal_features_ambiguous_text_requires_format(self):
        df = pd.DataFrame({"dt": ["03/02/2026", "04/02/2026"], "valor": [1.0, 2.0]})
        with self.assertRaisesRegex(ValueError, "date_format"):
            create_temporal_features(
                df,
                target_col="valor",
                date_col="dt",
                lags=[1],
                rolling_windows=[],
                calendar_features=False,
            )
        out = create_temporal_features(
            df,
            target_col="valor",
            date_col="dt",
            lags=[1],
            rolling_windows=[],
            calendar_features=False,
            date_format="%d/%m/%Y",
        )
        self.assertEqual(len(out), 1)

    def test_split_gap_counts_observed_periods_not_elapsed_months(self):
        dates = pd.to_datetime([
            "2026-01-01", "2026-02-01", "2026-04-01", "2026-05-01", "2026-06-01",
            "2026-08-01", "2026-09-01", "2026-10-01", "2026-12-01", "2027-01-01",
        ])
        df = pd.DataFrame({"dt": dates, "x": range(len(dates))})
        train, val, test = temporal_split(
            df,
            date_col="dt",
            train_pct=0.50,
            val_pct=0.20,
            gap_periods=1,
            period_unit="M",
        )
        self.assertEqual(str(train["dt"].max().date()), "2026-06-01")
        self.assertEqual(str(val["dt"].min().date()), "2026-09-01")
        self.assertEqual(str(test["dt"].min().date()), "2027-01-01")
        self.assertNotIn(pd.Timestamp("2026-08-01"), set(pd.concat([train, val, test])["dt"]))
        self.assertNotIn(pd.Timestamp("2026-12-01"), set(pd.concat([train, val, test])["dt"]))

    def test_split_null_date_is_omitted_from_all_outputs(self):
        dates = list(pd.date_range("2026-01-01", periods=8, freq="MS")) + [pd.NaT]
        df = pd.DataFrame({"dt": dates, "x": range(len(dates))})
        train, val, test = temporal_split(
            df,
            date_col="dt",
            train_pct=0.50,
            val_pct=0.25,
            gap_periods=0,
        )
        self.assertEqual(len(train) + len(val) + len(test), len(df) - 1)
        self.assertFalse(pd.concat([train, val, test])["dt"].isna().any())

    def test_split_group_col_produces_entity_disjoint_outputs(self):
        dates = pd.date_range("2026-01-01", periods=10, freq="MS")
        groups = ["A"] * 5 + ["B"] * 2 + ["C"] * 3
        df = pd.DataFrame({"dt": dates, "id": groups, "x": range(10)})
        train, val, test = temporal_split(
            df,
            date_col="dt",
            train_pct=0.50,
            val_pct=0.20,
            gap_periods=0,
            group_col="id",
        )
        tg, vg, sg = set(train["id"]), set(val["id"]), set(test["id"])
        self.assertFalse(tg & vg)
        self.assertFalse(tg & sg)
        self.assertFalse(vg & sg)
        self.assertTrue(train.shape[0] and val.shape[0] and test.shape[0])

    def test_walk_forward_fold_count_gap_and_metadata(self):
        dates = pd.date_range("2026-01-01", periods=8, freq="MS")
        df = pd.DataFrame({"dt": dates, "y": np.arange(8, dtype=float)})

        def callback(train_df, test_df):
            return {"metric": float(test_df["y"].mean()), "fold": 999, "n_train": -1}

        results = walk_forward_cv(
            df,
            date_col="dt",
            target_col="y",
            model_fn=callback,
            min_train_periods=3,
            test_periods=1,
            step=1,
            gap=1,
            period_unit="M",
        )
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["train_end"], "2026-03")
        self.assertEqual(results[0]["test_start"], "2026-05")
        self.assertEqual(results[0]["fold"], 1)
        self.assertEqual(results[0]["n_train"], 3)

    def test_walk_forward_gap_uses_observed_period_positions(self):
        dates = pd.to_datetime(["2026-01-01", "2026-03-01", "2026-04-01", "2026-05-01", "2026-06-01", "2026-07-01"])
        df = pd.DataFrame({"dt": dates, "y": range(6)})
        results = walk_forward_cv(
            df,
            date_col="dt",
            target_col="y",
            model_fn=lambda _tr, te: {"mean": float(te["y"].mean())},
            min_train_periods=2,
            test_periods=1,
            step=1,
            gap=1,
        )
        self.assertEqual(results[0]["train_end"], "2026-03")
        self.assertEqual(results[0]["test_start"], "2026-05")

    def test_walk_forward_can_return_empty_list_for_insufficient_history(self):
        df = pd.DataFrame({
            "dt": pd.date_range("2026-01-01", periods=2, freq="MS"),
            "y": [1.0, 2.0],
        })
        results = walk_forward_cv(
            df,
            date_col="dt",
            target_col="y",
            model_fn=lambda _tr, _te: {"metric": 0.0},
            min_train_periods=12,
        )
        self.assertEqual(results, [])


@unittest.skipUnless(MODELS_AVAILABLE, "pmdarima/Prophet não instalados")
class ForecastRuntimeCases(unittest.TestCase):
    def test_arima_real_fit_returns_point_forecast_and_insample_metrics(self):
        rng = np.random.default_rng(42)
        series = np.cumsum(rng.normal(0.2, 0.7, 36)) + 20
        model, forecast, metrics = train_arima(
            series,
            m=1,
            forecast_periods=3,
            seasonal=False,
            log_mlflow=False,
        )
        self.assertEqual(len(forecast), 3)
        self.assertEqual(
            set(metrics),
            {"aic", "bic", "order", "seasonal_order", "rmse_insample", "mape_insample"},
        )
        self.assertTrue(math.isfinite(float(metrics["rmse_insample"])))
        self.assertIsInstance(metrics["order"], str)
        self.assertIsNotNone(model)

    def test_prophet_real_fit_includes_history_plus_future(self):
        dates = pd.date_range("2024-01-01", periods=18, freq="MS")
        y = 100 + np.arange(18) * 2 + 5 * np.sin(2 * np.pi * np.arange(18) / 12)
        df = pd.DataFrame({"dt": dates, "valor": y})
        model, forecast, metrics = train_prophet(
            df,
            ds_col="dt",
            y_col="valor",
            periods=2,
            freq="MS",
            yearly=False,
            weekly=False,
            country_holidays="",
            log_mlflow=False,
        )
        self.assertEqual(len(forecast), 20)
        self.assertEqual(set(metrics), {"mape_insample", "rmse_insample", "mae_insample"})
        self.assertTrue(all(math.isfinite(float(v)) for v in metrics.values()))
        self.assertEqual(pd.Timestamp(forecast["ds"].min()), dates.min())
        self.assertGreater(pd.Timestamp(forecast["ds"].max()), dates.max())
        self.assertIsNotNone(model)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-models", action="store_true")
    args, remaining = parser.parse_known_args()
    if args.require_models and not MODELS_AVAILABLE:
        raise SystemExit(f"dependências de forecasting obrigatórias ausentes: {MODEL_IMPORT_ERROR!r}")
    unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
    return 0


if __name__ == "__main__":
    main()
