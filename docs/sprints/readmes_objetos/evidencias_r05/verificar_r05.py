"""Suíte delimitada R05 para os seis objetos tabulares.

O runner de fechamento usa --require-models e instala dependências fora do produto.
Sem elas, os casos de runtime são pulados em vez de inventar aprovação.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
ASSISTANT = ROOT / "ambiente_fonte/.assistant"
if str(ASSISTANT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT))

# lgbm_ranker importa MLflow de forma obrigatória. A suíte não testa logging e usa
# um stub explícito para isolar treino/métricas sem transformar MLflow em dependência
# permanente desta evidência. A dependência de import é verificada estaticamente.
if "mlflow" not in sys.modules:
    mlflow_stub = types.ModuleType("mlflow")
    mlflow_stub.log_params = lambda *_a, **_k: None
    mlflow_stub.log_metrics = lambda *_a, **_k: None
    sys.modules["mlflow"] = mlflow_stub

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
    "lgbm_ranker",
    "mlp_embeddings",
    "optuna_lgbm",
    "tabnet_wrapper",
    "train_catboost",
    "train_lgbm",
]

MODEL_IMPORT_ERROR: Exception | None = None
try:
    import lightgbm as lgb
    import optuna
    import torch
    import catboost
    import pytorch_tabnet
    import sklearn

    from hub_snippets.ml.lgbm_ranker import evaluate_ranking, train_lgbm_ranker
    from hub_snippets.ml.mlp_embeddings import EmbeddingMLP, train_embedding_mlp
    from hub_snippets.ml.optuna_lgbm import optimize_lgbm
    from hub_snippets.ml.tabnet_wrapper import train_tabnet
    from hub_snippets.ml.train_catboost import train_catboost_baseline
    from hub_snippets.ml.train_lgbm import train_lightgbm_baseline
except Exception as exc:  # pragma: no cover - exercised by dependency-free local run
    MODEL_IMPORT_ERROR = exc

MODELS_AVAILABLE = MODEL_IMPORT_ERROR is None


class StaticCases(unittest.TestCase):
    def test_six_readmes_have_contract_and_exact_section_order(self):
        for obj in OBJECTS:
            path = ASSISTANT / f"hub_snippets/ml/{obj}/README.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("<!-- readme-objeto: 1.0.0 -->", text, obj)
            indexes = [text.index(section) for section in REQUIRED_SECTIONS]
            self.assertEqual(indexes, sorted(indexes), obj)

    def test_readmes_do_not_claim_publication_or_independent_audit(self):
        forbidden = ["auditoria independente concluída", "publicado no Databricks", "homologado no Databricks"]
        for obj in OBJECTS:
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                self.assertNotIn(phrase.lower(), text, (obj, phrase))

    def test_ranker_source_has_hard_mlflow_import_and_no_map_metric(self):
        text = (ASSISTANT / "hub_snippets/ml/lgbm_ranker/lgbm_ranker.py").read_text(encoding="utf-8")
        self.assertIn("import mlflow", text)
        self.assertNotIn("try:\n    import mlflow", text)
        self.assertNotIn('metrics[f"map_at_', text)

    def test_optuna_objective_and_incomplete_best_params_are_explicit_in_source(self):
        text = (ASSISTANT / "hub_snippets/ml/optuna_lgbm/optuna_lgbm.py").read_text(encoding="utf-8")
        self.assertIn("return roc_auc_score(y_val, y_prob)", text)
        self.assertIn("return -np.sqrt(mean_squared_error", text)
        self.assertIn("return -log_loss", text)
        self.assertIn("return study.best_params, study", text)
        self.assertNotIn('"subsample_freq"', text)

    def test_train_lgbm_source_does_not_enable_subsample_frequency(self):
        text = (ASSISTANT / "hub_snippets/ml/train_lgbm/train_lgbm.py").read_text(encoding="utf-8")
        self.assertIn('"subsample": 0.8', text)
        self.assertNotIn('"subsample_freq"', text)

    def test_catboost_task_overrides_are_after_params_override(self):
        text = (ASSISTANT / "hub_snippets/ml/train_catboost/train_catboost.py").read_text(encoding="utf-8")
        self.assertLess(text.index("params.update(params_override)"), text.index('params["loss_function"] = "Logloss"'))


@unittest.skipUnless(MODELS_AVAILABLE, "dependências de ML não instaladas")
class RuntimeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        np.random.seed(42)

    def test_train_lgbm_binary_metrics_and_subsample_frequency(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(240, 4))
        y = (X[:, 0] - 0.5 * X[:, 1] + rng.normal(scale=0.5, size=240) > 0).astype(int)
        model, metrics = train_lightgbm_baseline(
            X[:180], y[:180], X[180:], y[180:],
            task="binary",
            params_override={"n_estimators": 30, "num_leaves": 7, "min_child_samples": 5},
            early_stopping_rounds=5,
            log_mlflow=False,
        )
        self.assertEqual(set(metrics), {"auc_train", "auc_val", "gini_val", "overfit_gap"})
        self.assertAlmostEqual(metrics["gini_val"], 2 * metrics["auc_val"] - 1)
        params = model.get_params()
        self.assertEqual(params["subsample"], 0.8)
        self.assertEqual(params["subsample_freq"], 0)

    def test_train_lgbm_regression_metrics(self):
        rng = np.random.default_rng(2)
        X = rng.normal(size=(180, 3))
        y = 2 * X[:, 0] - X[:, 1] + rng.normal(scale=0.2, size=180)
        _, metrics = train_lightgbm_baseline(
            X[:130], y[:130], X[130:], y[130:],
            task="regression",
            params_override={"n_estimators": 25, "num_leaves": 7, "min_child_samples": 5},
            early_stopping_rounds=5,
            log_mlflow=False,
        )
        self.assertEqual(set(metrics), {"rmse_train", "rmse_val", "overfit_gap"})
        self.assertGreaterEqual(metrics["rmse_val"], 0)

    def test_catboost_binary_preserves_no_file_default_and_task_loss(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(180, 3))
        y = (X[:, 0] + rng.normal(scale=0.6, size=180) > 0).astype(int)
        with tempfile.TemporaryDirectory() as tmp:
            old = os.getcwd()
            os.chdir(tmp)
            try:
                model, metrics = train_catboost_baseline(
                    X[:130], y[:130], X[130:], y[130:],
                    task="binary",
                    params_override={"iterations": 20, "early_stopping_rounds": 5, "loss_function": "CrossEntropy"},
                    log_mlflow=False,
                )
                self.assertFalse(Path("catboost_info").exists())
            finally:
                os.chdir(old)
        self.assertEqual(set(metrics), {"auc_val", "gini_val"})
        self.assertEqual(model.get_params()["loss_function"], "Logloss")
        self.assertFalse(model.get_params()["allow_writing_files"])

    def test_catboost_multiclass_metrics(self):
        rng = np.random.default_rng(4)
        X = rng.normal(size=(210, 4))
        raw = X[:, 0] + 0.5 * X[:, 1]
        y = np.digitize(raw, [-0.5, 0.5])
        _, metrics = train_catboost_baseline(
            X[:150], y[:150], X[150:], y[150:],
            task="multiclass",
            params_override={"iterations": 15, "early_stopping_rounds": 4},
            log_mlflow=False,
        )
        self.assertEqual(set(metrics), {"log_loss_val", "accuracy_val"})

    def test_ranker_evaluator_returns_ndcg_only(self):
        class Dummy:
            def predict(self, X):
                return np.asarray(X)[:, 0]
        X = np.array([[0.9], [0.1], [0.4], [0.8], [0.2]])
        y = np.array([3, 0, 1, 2, 0])
        metrics = evaluate_ranking(Dummy(), X, y, np.array([3, 2]), ks=[1, 2])
        self.assertEqual(set(metrics), {"ndcg_at_1", "ndcg_at_2"})
        self.assertTrue(all(0 <= value <= 1 for value in metrics.values()))

    def test_ranker_training_and_group_validation(self):
        rng = np.random.default_rng(5)
        group_size = 5
        n_train_groups, n_val_groups = 20, 6
        Xtr = rng.normal(size=(n_train_groups * group_size, 3))
        Xva = rng.normal(size=(n_val_groups * group_size, 3))
        ytr = np.clip(np.digitize(Xtr[:, 0], [-0.5, 0.2, 0.8]), 0, 3)
        yva = np.clip(np.digitize(Xva[:, 0], [-0.5, 0.2, 0.8]), 0, 3)
        params = {
            "objective": "lambdarank",
            "metric": "ndcg",
            "ndcg_eval_at": [3],
            "learning_rate": 0.1,
            "num_leaves": 7,
            "min_data_in_leaf": 2,
            "verbose": -1,
            "seed": 42,
        }
        _, metrics = train_lgbm_ranker(
            Xtr, ytr, np.full(n_train_groups, group_size, dtype=int),
            Xva, yva, np.full(n_val_groups, group_size, dtype=int),
            params=params, num_boost_round=15, early_stopping_rounds=4, log_mlflow=False,
        )
        self.assertIn("ndcg_at_5", metrics)
        with self.assertRaisesRegex(ValueError, "sum to len"):
            evaluate_ranking(type("D", (), {"predict": lambda _s, x: np.zeros(len(x))})(), Xva, yva, np.array([2, 2]))

    def test_optuna_binary_returns_only_suggested_best_params(self):
        rng = np.random.default_rng(6)
        X = rng.normal(size=(260, 4))
        y = (X[:, 0] - X[:, 1] + rng.normal(scale=0.8, size=260) > 0).astype(int)
        best, study = optimize_lgbm(X[:190], y[:190], X[190:], y[190:], task="binary", n_trials=2, metric="binary_logloss")
        expected = {"learning_rate", "num_leaves", "max_depth", "min_child_samples", "subsample", "colsample_bytree", "reg_alpha", "reg_lambda"}
        self.assertEqual(set(best), expected)
        self.assertNotIn("n_estimators", best)
        self.assertGreaterEqual(study.best_value, 0)
        self.assertLessEqual(study.best_value, 1)

    def test_mlp_binary_training(self):
        rng = np.random.default_rng(7)
        n = 160
        Xn = rng.normal(size=(n, 2)).astype("float32")
        cat = rng.integers(0, 5, size=n)
        y = (Xn[:, 0] + 0.4 * (cat == 2) + rng.normal(scale=0.7, size=n) > 0).astype(int)
        model, metrics = train_embedding_mlp(
            Xn[:120], [cat[:120]], y[:120],
            Xn[120:], [cat[120:]], y[120:],
            cat_dims=[5], epochs=2, batch_size=32, patience=2, log_mlflow=False,
        )
        self.assertIsInstance(model, EmbeddingMLP)
        self.assertEqual(set(metrics), {"auc_val", "gini_val", "epochs_trained"})
        self.assertGreaterEqual(metrics["auc_val"], 0)
        self.assertLessEqual(metrics["auc_val"], 1)

    def test_embedding_class_short_emb_dims_is_not_rejected(self):
        model = EmbeddingMLP(n_numeric=2, cat_dims=[3, 4], emb_dims=[2], hidden_layers=[4], dropout=0.0)
        self.assertEqual(len(model.embeddings), 1)
        model.eval()
        with torch.no_grad():
            out = model(
                torch.zeros((2, 2), dtype=torch.float32),
                [torch.tensor([0, 1]), torch.tensor([2, 3])],
            )
        self.assertEqual(tuple(out.shape), (2, 1))

    def test_tabnet_binary_metrics_and_importance(self):
        rng = np.random.default_rng(8)
        X = rng.normal(size=(180, 4)).astype("float32")
        y = (1.2 * X[:, 0] - 0.5 * X[:, 1] + rng.normal(scale=0.8, size=180) > 0).astype(int)
        model, metrics, importance = train_tabnet(
            X[:130], y[:130], X[130:], y[130:],
            task="binary", n_d=4, n_a=4, n_steps=2,
            max_epochs=2, patience=2, batch_size=32, log_mlflow=False,
        )
        self.assertEqual(set(metrics), {"auc_val", "gini_val"})
        self.assertEqual(len(importance), X.shape[1])
        self.assertAlmostEqual(float(np.sum(importance)), 1.0, places=5)
        self.assertIsNotNone(model)

    def test_tabnet_regression_metrics(self):
        rng = np.random.default_rng(9)
        X = rng.normal(size=(160, 3)).astype("float32")
        y = (2 * X[:, 0] - X[:, 1] + rng.normal(scale=0.3, size=160)).astype("float32")
        _, metrics, importance = train_tabnet(
            X[:115], y[:115], X[115:], y[115:],
            task="regression", n_d=4, n_a=4, n_steps=2,
            max_epochs=2, patience=2, batch_size=32, log_mlflow=False,
        )
        self.assertEqual(set(metrics), {"rmse_val"})
        self.assertGreaterEqual(metrics["rmse_val"], 0)
        self.assertEqual(len(importance), X.shape[1])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-models", action="store_true")
    args, remaining = parser.parse_known_args()
    if args.require_models and not MODELS_AVAILABLE:
        raise SystemExit(f"dependências de ML obrigatórias ausentes: {MODEL_IMPORT_ERROR!r}")
    unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
    return 0


if __name__ == "__main__":
    main()
