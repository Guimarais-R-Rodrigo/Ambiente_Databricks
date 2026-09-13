"""Suíte delimitada R08 para clusters, anomalias e explicabilidade."""
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

OBJECTS = [
    "autoencoder_anomaly",
    "cluster_profiling",
    "clustering_suite",
    "explainability_report",
    "shap_explainer",
    "umap_viz",
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


class StaticCases(unittest.TestCase):
    def test_contract_and_section_order(self):
        for obj in OBJECTS:
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8")
            self.assertIn("<!-- readme-objeto: 1.0.0 -->", text, obj)
            idx = [text.index(s) for s in REQUIRED_SECTIONS]
            self.assertEqual(idx, sorted(idx), obj)

    def test_six_waivers_retired(self):
        data = json.loads((ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json").read_text(encoding="utf-8"))
        for obj in OBJECTS:
            self.assertNotIn(f"hub_snippets/ml/{obj}", data["exemptions"])

    def test_expected_coverage_is_documented(self):
        text = (ROOT / "docs/sprints/readmes_objetos/README.md").read_text(encoding="utf-8")
        self.assertIn("55/75 operacionais", text)
        self.assertIn("20 pendências", text)
        self.assertIn("RELATORIO_R08.md", text)

    def test_readmes_do_not_claim_homologation_publication_or_independent_audit(self):
        forbidden = ["auditoria independente concluída", "publicado no databricks", "homologado no databricks"]
        for obj in OBJECTS:
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8").lower()
            for phrase in forbidden:
                self.assertNotIn(phrase, text, (obj, phrase))

    def test_autoencoder_contract_is_described_from_source(self):
        source = (ASSISTANT / "hub_snippets/ml/autoencoder_anomaly/autoencoder_anomaly.py").read_text(encoding="utf-8")
        readme = (ASSISTANT / "hub_snippets/ml/autoencoder_anomaly/README.md").read_text(encoding="utf-8")
        self.assertIn("np.percentile(train_errors, threshold_percentile)", source)
        self.assertIn("input_center_", source)
        self.assertIn("percentil dos erros do próprio treino", readme)
        self.assertIn("padronização", readme.lower())

    def test_cluster_profiling_documents_noninferential_z_score(self):
        source = (ASSISTANT / "hub_snippets/ml/cluster_profiling/cluster_profiling.py").read_text(encoding="utf-8")
        readme = (ASSISTANT / "hub_snippets/ml/cluster_profiling/README.md").read_text(encoding="utf-8")
        self.assertIn("(cluster_mean - global_mean) / global_std", source)
        self.assertIn("não um z-test", readme)

    def test_clustering_documents_heuristics_and_fixed_dbscan(self):
        source = (ASSISTANT / "hub_snippets/ml/clustering_suite/clustering_suite.py").read_text(encoding="utf-8")
        readme = (ASSISTANT / "hub_snippets/ml/clustering_suite/README.md").read_text(encoding="utf-8")
        self.assertIn('DBSCAN(eps=0.5, min_samples=5)', source)
        self.assertIn('method == "elbow"', source)
        self.assertIn("`eps=0.5`", readme)
        self.assertIn('`method="both"` não cria votação', readme)

    def test_explainability_hidden_contracts_documented(self):
        source = (ASSISTANT / "hub_snippets/ml/explainability_report/explainability_report.py").read_text(encoding="utf-8")
        readme = (ASSISTANT / "hub_snippets/ml/explainability_report/README.md").read_text(encoding="utf-8")
        self.assertIn("to_markdown", source)
        self.assertIn("rank_shap", source)
        self.assertIn("`tabulate`", readme)
        self.assertIn("coluna `rank`", readme)
        self.assertIn("não reordena", readme)

    def test_shap_contracts_documented(self):
        source = (ASSISTANT / "hub_snippets/ml/shap_explainer/shap_explainer.py").read_text(encoding="utf-8")
        readme = (ASSISTANT / "hub_snippets/ml/shap_explainer/README.md").read_text(encoding="utf-8")
        self.assertIn('model_type == "kernel"', source)
        self.assertIn("max_samples", source)
        self.assertIn("normaliza formatos multi-output", readme)
        self.assertIn("KernelSHAP", readme)
        self.assertIn("cumulative_pct", readme)

    def test_umap_current_visual_contract_documented(self):
        source = (ASSISTANT / "hub_snippets/ml/umap_viz/umap_viz.py").read_text(encoding="utf-8")
        readme = (ASSISTANT / "hub_snippets/ml/umap_viz/README.md").read_text(encoding="utf-8")
        self.assertIn("random_state=SEED", source)
        self.assertIn("compute_umap(X_scaled)", source)
        self.assertIn("TEMA_BASE", source)
        self.assertIn("não recebe `ResolvedTheme`", readme)
        self.assertIn("defaults", readme)

    def test_editorial_corrections_and_backlinks_present(self):
        expected = {
            "autoencoder_anomaly": "etapa externa é redundante",
            "cluster_profiling": "não é",
            "clustering_suite": "devolve um **dict**",
            "explainability_report": "Segundo bloqueio",
            "shap_explainer": "sanity check",
            "umap_viz": "O uso seguro é **exploratório**",
        }
        for obj, marker in expected.items():
            text = (ASSISTANT / f"hub_snippets/ml/{obj}/exemplo_{obj}.py").read_text(encoding="utf-8")
            self.assertIn("Guia local completo:", text, obj)
            self.assertIn(marker, text, obj)


class CoreRuntimeCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import numpy as np
        import pandas as pd
        cls.np = np
        cls.pd = pd
        from hub_snippets.ml.cluster_profiling import profile_clusters, top_differentiators
        from hub_snippets.ml.clustering_suite import select_k, run_clustering_pipeline
        from hub_snippets.ml.explainability_report import generate_executive_report, generate_technical_summary
        cls.profile_clusters = staticmethod(profile_clusters)
        cls.top_differentiators = staticmethod(top_differentiators)
        cls.select_k = staticmethod(select_k)
        cls.run_clustering_pipeline = staticmethod(run_clustering_pipeline)
        cls.generate_executive_report = staticmethod(generate_executive_report)
        cls.generate_technical_summary = staticmethod(generate_technical_summary)

    def test_cluster_profile_formula_and_zero_mean_index(self):
        pd = self.pd
        df = pd.DataFrame({"cluster": [0, 0, 1, 1], "x": [-1.0, 1.0, 3.0, 5.0], "zero_mean": [-1.0, 1.0, -2.0, 2.0]})
        out = self.profile_clusters(df, ["x", "zero_mean"], "cluster")
        row = out[(out["cluster"] == 1) & (out["feature"] == "x")].iloc[0]
        expected = (4.0 - 2.0) / df["x"].std()
        self.assertAlmostEqual(float(row["z_score"]), float(expected))
        zero = out[(out["cluster"] == 1) & (out["feature"] == "zero_mean")].iloc[0]
        self.assertTrue(pd.isna(zero["index"]))
        self.assertEqual(len(self.top_differentiators(out, 1, top_n=1)), 1)

    def test_select_k_both_equals_silhouette_on_same_fixture(self):
        np = self.np
        rng = np.random.default_rng(42)
        X = np.vstack([rng.normal((0, 0), 0.4, (50, 2)), rng.normal((5, 5), 0.4, (50, 2)), rng.normal((0, 5), 0.4, (50, 2))])
        a = self.select_k(X, range(2, 5), method="silhouette")
        b = self.select_k(X, range(2, 5), method="both")
        self.assertEqual(int(a["best_k"]), int(b["best_k"]))
        self.assertEqual(int(a["best_k"]), 3)

    def test_pipeline_returns_contract_without_mlflow_side_effect(self):
        pd, np = self.pd, self.np
        rng = np.random.default_rng(7)
        df = pd.DataFrame(np.vstack([rng.normal(0, .3, (30, 2)), rng.normal(3, .3, (30, 2))]), columns=["a", "b"])
        out = self.run_clustering_pipeline(df, ["a", "b"], k=2, algorithm="kmeans", scaler="standard", log_mlflow=False)
        self.assertEqual(set(out), {"labels", "metrics", "model", "scaler", "X_scaled"})
        self.assertEqual(len(out["labels"]), len(df))
        self.assertEqual(int(out["metrics"]["n_clusters"]), 2)

    def test_executive_report_keeps_input_order(self):
        pd = self.pd
        imp = pd.DataFrame({"feature": ["menor", "maior"], "pct_importance": [1.0, 99.0]})
        text = self.generate_executive_report(imp, {}, "evento", 0.7)
        self.assertLess(text.index("menor"), text.index("maior"))

    def test_technical_summary_with_rank_columns(self):
        pd = self.pd
        shap = pd.DataFrame({"rank": [1, 2, 3], "feature": ["a", "b", "c"], "pct_importance": [50., 30., 20.]})
        native = pd.DataFrame({"rank": [1, 3, 2], "feature": ["a", "b", "c"], "pct_importance": [60., 15., 25.]})
        text = self.generate_technical_summary(shap, native)
        self.assertIn("Correlação Spearman", text)
        self.assertIn("|", text)


class TorchRuntimeCases(unittest.TestCase):
    def test_autoencoder_runtime_contract(self):
        import numpy as np
        from hub_snippets.ml.autoencoder_anomaly import train_autoencoder_anomaly
        rng = np.random.default_rng(42)
        train = rng.normal(size=(128, 4)).astype("float32")
        test = np.vstack([rng.normal(size=(16, 4)), rng.normal(4, 1, size=(4, 4))]).astype("float32")
        model, threshold, scores = train_autoencoder_anomaly(train, test, encoding_dim=2, epochs=3, batch_size=32, patience=2, log_mlflow=False)
        self.assertEqual(scores.shape, (20,))
        self.assertTrue(math.isfinite(float(threshold)))
        self.assertTrue(hasattr(model, "input_center_"))
        self.assertTrue(hasattr(model, "input_scale_"))

    def test_autoencoder_rejects_invalid_percentile(self):
        import numpy as np
        from hub_snippets.ml.autoencoder_anomaly import train_autoencoder_anomaly
        with self.assertRaises(ValueError):
            train_autoencoder_anomaly(np.ones((4, 2)), np.ones((2, 2)), threshold_percentile=100, log_mlflow=False)


class ShapRuntimeCases(unittest.TestCase):
    def test_tree_shap_and_topn_percentages(self):
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        from hub_snippets.ml.shap_explainer import compute_shap, get_feature_importance_shap
        rng = np.random.default_rng(42)
        X = rng.normal(size=(120, 4))
        y = (1.5 * X[:, 0] - .5 * X[:, 1] > 0).astype(int)
        model = RandomForestClassifier(n_estimators=20, max_depth=4, random_state=42).fit(X, y)
        values, base = compute_shap(model, X[:40], ["a", "b", "c", "d"], model_type="tree", output_index=1)
        self.assertEqual(np.asarray(values).shape, (40, 4))
        self.assertTrue(math.isfinite(float(base)))
        top = get_feature_importance_shap(values, ["a", "b", "c", "d"], top_n=2)
        self.assertEqual(len(top), 2)
        self.assertLessEqual(float(top["cumulative_pct"].iloc[-1]), 100.0 + 1e-9)

    def test_multioutput_requires_index_helper_contract(self):
        import numpy as np
        from hub_snippets.ml.shap_explainer.shap_explainer import _select_shap_output
        arr = np.zeros((5, 3, 2))
        with self.assertRaises(ValueError):
            _select_shap_output(arr, base_value=np.array([0.4, 0.6]), n_features=3, output_index=None)


class UmapRuntimeCases(unittest.TestCase):
    def test_umap_shape_and_repeatability(self):
        import numpy as np
        from hub_snippets.ml.umap_viz import compute_umap
        rng = np.random.default_rng(42)
        X = rng.normal(size=(80, 5))
        a = compute_umap(X, n_components=2, n_neighbors=10, min_dist=0.1)
        b = compute_umap(X, n_components=2, n_neighbors=10, min_dist=0.1)
        self.assertEqual(a.shape, (80, 2))
        self.assertTrue(np.allclose(a, b))

    def test_plot_contract_and_noise_count(self):
        import numpy as np
        from hub_snippets.ml.umap_viz import plot_umap_clusters
        rng = np.random.default_rng(7)
        X = rng.normal(size=(40, 4))
        labels = np.array([0] * 20 + [1] * 19 + [-1])
        fig = plot_umap_clusters(X, labels, "fixture")
        self.assertGreaterEqual(len(fig.data), 1)
        self.assertTrue(any("N=" in str(a.text) for a in fig.layout.annotations))


GROUPS = {
    "static": StaticCases,
    "core": CoreRuntimeCases,
    "torch": TorchRuntimeCases,
    "shap": ShapRuntimeCases,
    "umap": UmapRuntimeCases,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=GROUPS, default="static")
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GROUPS[args.group])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful() or result.skipped:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
