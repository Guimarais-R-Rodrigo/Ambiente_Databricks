"""Suíte R08 corrigida: valida contratos públicos, não helpers internos inexistentes."""
from __future__ import annotations

import argparse
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSISTANT = ROOT / "ambiente_fonte/.assistant"
if str(ASSISTANT) not in sys.path:
    sys.path.insert(0, str(ASSISTANT))

OBJECTS = ["autoencoder_anomaly", "cluster_profiling", "clustering_suite", "explainability_report", "shap_explainer", "umap_viz"]
SECTIONS = [
    "## 1. O que é?", "## 2. Que problema este recurso resolve?", "## 3. Quando faz sentido usar?",
    "## 4. Quando não usar?", "## 5. Como funciona, intuitivamente?", "## 6. Exemplo de situação",
    "## 7. O que você precisa antes de usar?", "## 8. O que este recurso entrega?",
    "## 9. Como usar este recurso no Hub?", "## 10. Decisões e configurações que mais importam",
    "## 11. Limitações, riscos e armadilhas", "## 12. Quais são as alternativas?",
    "## 13. Como saber se o resultado faz sentido?", "## 14. Arquivos relacionados e próximos passos",
    "## 15. Referências",
]


class StaticCases(unittest.TestCase):
    def test_contract_order_and_coverage(self):
        for obj in OBJECTS:
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8")
            self.assertIn("<!-- readme-objeto: 1.0.0 -->", text)
            pos = [text.index(s) for s in SECTIONS]
            self.assertEqual(pos, sorted(pos), obj)
        data = json.loads((ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json").read_text(encoding="utf-8"))
        for obj in OBJECTS:
            self.assertNotIn(f"hub_snippets/ml/{obj}", data["pending"])
        idx = (ROOT / "docs/sprints/readmes_objetos/README.md").read_text(encoding="utf-8")
        self.assertIn("55/75 operacionais", idx)
        self.assertIn("20 pendências", idx)

    def test_documented_contracts_match_source(self):
        ae = (ASSISTANT / "hub_snippets/ml/autoencoder_anomaly/autoencoder_anomaly.py").read_text(encoding="utf-8")
        self.assertIn("np.percentile(train_errors, threshold_percentile)", ae)
        self.assertIn("input_center_", ae)
        cp = (ASSISTANT / "hub_snippets/ml/cluster_profiling/cluster_profiling.py").read_text(encoding="utf-8")
        self.assertIn("cluster_means[feat] - global_means[feat]", cp)
        self.assertIn("/ global_stds[feat]", cp)
        cs = (ASSISTANT / "hub_snippets/ml/clustering_suite/clustering_suite.py").read_text(encoding="utf-8")
        self.assertIn('DBSCAN(eps=0.5, min_samples=5)', cs)
        self.assertIn('method == "elbow"', cs)
        er = (ASSISTANT / "hub_snippets/ml/explainability_report/explainability_report.py").read_text(encoding="utf-8")
        self.assertIn("to_markdown", er)
        self.assertIn("rank_shap", er)
        sh = (ASSISTANT / "hub_snippets/ml/shap_explainer/shap_explainer.py").read_text(encoding="utf-8")
        self.assertIn('model_type == "kernel"', sh)
        self.assertIn("max_samples", sh)
        uv = (ASSISTANT / "hub_snippets/ml/umap_viz/umap_viz.py").read_text(encoding="utf-8")
        self.assertIn("random_state=SEED", uv)
        self.assertIn("compute_umap(X_scaled)", uv)

    def test_editorial_corrections_and_backlinks(self):
        markers = {
            "autoencoder_anomaly": "etapa externa é redundante",
            "cluster_profiling": "z-test",
            "clustering_suite": "devolve um **dict**",
            "explainability_report": "Segundo bloqueio",
            "shap_explainer": "sanity check",
            "umap_viz": "O uso seguro é **exploratório**",
        }
        for obj, marker in markers.items():
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/exemplo_{obj}.py").read_text(encoding="utf-8")
            self.assertIn("Guia local completo:", text, obj)
            self.assertIn(marker, text, obj)

    def test_no_false_homologation_claims(self):
        forbidden = ["auditoria independente concluída", "publicado no databricks", "homologado no databricks"]
        for obj in OBJECTS:
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                self.assertNotIn(phrase, text, (obj, phrase))


class CoreRuntimeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import numpy as np
        import pandas as pd
        cls.np, cls.pd = np, pd
        from hub_snippets.ml.cluster_profiling import profile_clusters, top_differentiators
        from hub_snippets.ml.clustering_suite import select_k, run_clustering_pipeline
        from hub_snippets.ml.explainability_report import generate_executive_report, generate_technical_summary
        cls.profile, cls.top = staticmethod(profile_clusters), staticmethod(top_differentiators)
        cls.select_k, cls.pipeline = staticmethod(select_k), staticmethod(run_clustering_pipeline)
        cls.executive, cls.technical = staticmethod(generate_executive_report), staticmethod(generate_technical_summary)

    def test_profile_formula_and_zero_mean_index(self):
        pd = self.pd
        df = pd.DataFrame({"cluster": [0, 0, 1, 1], "x": [-1., 1., 3., 5.], "z": [-1., 1., -2., 2.]})
        out = self.profile(df, ["x", "z"], "cluster")
        row = out[(out.cluster == 1) & (out.feature == "x")].iloc[0]
        self.assertAlmostEqual(float(row.z_score), float((4 - 2) / df.x.std()))
        zero = out[(out.cluster == 1) & (out.feature == "z")].iloc[0]
        self.assertTrue(pd.isna(zero["index"]))
        self.assertEqual(len(self.top(out, 1, 1)), 1)

    def test_k_selection_and_pipeline_contract(self):
        np, pd = self.np, self.pd
        rng = np.random.default_rng(42)
        X = np.vstack([rng.normal((0, 0), .4, (40, 2)), rng.normal((5, 5), .4, (40, 2)), rng.normal((0, 5), .4, (40, 2))])
        self.assertEqual(self.select_k(X, range(2, 5), "silhouette")["best_k"], self.select_k(X, range(2, 5), "both")["best_k"])
        frame = pd.DataFrame(X, columns=["a", "b"])
        out = self.pipeline(frame, ["a", "b"], k=3, log_mlflow=False)
        self.assertEqual(set(out), {"labels", "metrics", "model", "scaler", "X_scaled"})
        self.assertEqual(len(out["labels"]), len(frame))

    def test_reports_keep_order_and_rank_contract(self):
        pd = self.pd
        imp = pd.DataFrame({"feature": ["menor", "maior"], "pct_importance": [1., 99.]})
        text = self.executive(imp, {}, "evento", .7)
        self.assertLess(text.index("menor"), text.index("maior"))
        shap = pd.DataFrame({"rank": [1, 2, 3], "feature": ["a", "b", "c"], "pct_importance": [50., 30., 20.]})
        native = pd.DataFrame({"rank": [1, 3, 2], "feature": ["a", "b", "c"], "pct_importance": [60., 15., 25.]})
        technical = self.technical(shap, native)
        self.assertIn("Spearman ρ", technical)


class TorchRuntimeCases(unittest.TestCase):
    def test_autoencoder_contract(self):
        import numpy as np
        from hub_snippets.ml.autoencoder_anomaly import train_autoencoder_anomaly
        rng = np.random.default_rng(42)
        train = rng.normal(size=(96, 4)).astype("float32")
        test = rng.normal(size=(20, 4)).astype("float32")
        model, threshold, scores = train_autoencoder_anomaly(train, test, encoding_dim=2, epochs=2, batch_size=24, patience=2, log_mlflow=False)
        self.assertEqual(scores.shape, (20,))
        self.assertTrue(math.isfinite(float(threshold)))
        self.assertTrue(hasattr(model, "input_center_") and hasattr(model, "input_scale_"))
        with self.assertRaises(ValueError):
            train_autoencoder_anomaly(train[:4], test[:2], threshold_percentile=100, log_mlflow=False)


class ShapRuntimeCases(unittest.TestCase):
    def test_tree_shap_public_contract_and_multioutput_guard(self):
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        from hub_snippets.ml.shap_explainer import compute_shap, get_feature_importance_shap
        rng = np.random.default_rng(42)
        X = rng.normal(size=(100, 4)); y = (1.5 * X[:, 0] - .5 * X[:, 1] > 0).astype(int)
        model = RandomForestClassifier(n_estimators=15, max_depth=4, random_state=42).fit(X, y)
        with self.assertRaises(ValueError):
            compute_shap(model, X[:20], ["a", "b", "c", "d"], model_type="tree")
        values, base = compute_shap(model, X[:30], ["a", "b", "c", "d"], model_type="tree", output_index=1)
        self.assertEqual(np.asarray(values).shape, (30, 4)); self.assertTrue(math.isfinite(float(base)))
        top = get_feature_importance_shap(values, ["a", "b", "c", "d"], top_n=2)
        self.assertEqual(len(top), 2); self.assertLessEqual(float(top.cumulative_pct.iloc[-1]), 100.0 + 1e-9)


class UmapRuntimeCases(unittest.TestCase):
    def test_umap_repeatability_and_plot(self):
        import numpy as np
        from hub_snippets.ml.umap_viz import compute_umap, plot_umap_clusters
        rng = np.random.default_rng(42); X = rng.normal(size=(50, 5))
        a = compute_umap(X, n_components=2, n_neighbors=10, min_dist=.1)
        b = compute_umap(X, n_components=2, n_neighbors=10, min_dist=.1)
        self.assertEqual(a.shape, (50, 2)); self.assertTrue(np.allclose(a, b))
        labels = np.array([0] * 25 + [1] * 24 + [-1])
        fig = plot_umap_clusters(X, labels, "fixture")
        self.assertGreaterEqual(len(fig.data), 1)
        self.assertTrue(any("N =" in str(x.text) for x in fig.layout.annotations))


GROUPS = {"static": StaticCases, "core": CoreRuntimeCases, "torch": TorchRuntimeCases, "shap": ShapRuntimeCases, "umap": UmapRuntimeCases}


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--group", choices=GROUPS, default="static"); args = ap.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(GROUPS[args.group]))
    if not result.wasSuccessful() or result.skipped:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
