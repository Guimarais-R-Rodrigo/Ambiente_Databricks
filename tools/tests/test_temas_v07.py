"""V07 — consumidores runtime e formatos de saída; sem Databricks/rede."""
from __future__ import annotations

import ast
import inspect
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ASSISTANT_ROOT = ROOT / "ambiente_fonte/.assistant"
sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_snippets.ml.curves_plotly import (
    plot_ks_curve,
    plot_ks_curve_resolvido,
    plot_lift_curve,
    plot_lift_curve_resolvido,
    plot_pr_curve,
    plot_pr_curve_resolvido,
    plot_roc_curve,
    plot_roc_curve_resolvido,
)
from hub_snippets.ml.performance_monitor import PerformanceMonitor
from hub_snippets.ml.shap_explainer import plot_shap_global
from hub_snippets.ml.umap_viz import plot_umap_clusters, plot_umap_clusters_resolvido
from hub_snippets.ml.vintage_analysis import (
    plot_vintage_curves,
    plot_vintage_curves_resolvido,
    plot_vintage_heatmap,
    plot_vintage_heatmap_resolvido,
)
from hub_snippets.visual.tema import ThemeError, load_reference_theme, resolve_theme
from hub_snippets.visual.theme_plotly import get_tokens_plotly

REGISTRY = ROOT / "docs/sprints/sistema_temas/V07/CONSUMIDORES.json"
HEX = re.compile(r"#[0-9A-Fa-f]{6}")


def proposta(**tokens):
    data = load_reference_theme("notebook").to_dict()
    data["theme_id"] = "hub-v07-proposta"
    data["display_name"] = "V07 proposta sintética"
    data["description"] = "Configuração sintética para testes de consumidores V07."
    data["tokens"].update(tokens)
    return resolve_theme(data, expected_context="notebook")


def plotly_data(fig):
    return json.loads(fig.to_json())["data"]


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.consumers = {item["id"]: item for item in self.registry["consumers"]}

    def test_all_runtime_consumers_are_classified(self):
        expected = {
            "display.dataframe_styled",
            "display.correlation_matrix",
            "display.distribution_grid",
            "ml.curves_plotly",
            "ml.kaplan_meier",
            "ml.performance_monitor",
            "ml.shap_explainer",
            "ml.umap_viz",
            "ml.vintage_analysis",
        }
        self.assertEqual(set(self.consumers), expected)
        self.assertTrue(all(Path(ROOT / item["path"]).is_file() for item in self.consumers.values()))

    def test_controls_have_real_supported_consumers(self):
        covered = set()
        for item in self.consumers.values():
            if item["classification"] in {"supported_v07", "already_supported_v04"}:
                covered.update(item["tokens"])
        self.assertEqual(set(self.registry["controls_v07"]), covered)

    def test_exceptions_are_explicit_and_actionable(self):
        exceptions = [item for item in self.consumers.values() if item["classification"] == "exception_deferred"]
        self.assertEqual({item["id"] for item in exceptions}, {"ml.kaplan_meier", "ml.shap_explainer"})
        for item in exceptions:
            self.assertFalse(item["routes"])
            self.assertTrue(item["reason"])
            self.assertTrue(item["owner"])
            self.assertTrue(item["user_effect"])

    def test_output_format_boundary_is_closed(self):
        policy = self.registry["format_policy"]
        self.assertEqual(set(policy["supported"]), {"plotly_figure_memory", "plotly_html_file"})
        for forbidden in {"pdf", "pptx", "plotly_static_png"}:
            self.assertNotIn(forbidden, policy["supported"])
            self.assertIn(forbidden, policy["not_homologated"])


class TokenAccessTests(unittest.TestCase):
    def test_tokens_are_revalidated_and_copied(self):
        theme = load_reference_theme("notebook")
        tokens = get_tokens_plotly(theme)
        original = theme.tokens["palette.categorical"][0]
        tokens["palette.categorical"][0] = "#FFFFFF"
        self.assertEqual(theme.tokens["palette.categorical"][0], original)

    def test_raw_dictionary_is_rejected(self):
        with self.assertRaises(ThemeError) as ctx:
            get_tokens_plotly(load_reference_theme("notebook").to_dict())
        self.assertEqual(ctx.exception.code, "RESULT_TYPE")


class ApiCompatibilityTests(unittest.TestCase):
    def test_legacy_signatures_remain_unchanged(self):
        self.assertEqual(list(inspect.signature(plot_roc_curve).parameters), ["y_true", "y_prob", "title", "show_auc", "n"])
        self.assertEqual(list(inspect.signature(plot_pr_curve).parameters), ["y_true", "y_prob", "title", "n"])
        self.assertEqual(list(inspect.signature(plot_lift_curve).parameters), ["y_true", "y_prob", "title", "n_bins", "n"])
        self.assertEqual(list(inspect.signature(plot_ks_curve).parameters), ["y_true", "y_prob", "title", "n"])
        self.assertEqual(list(inspect.signature(PerformanceMonitor.plot_timeline).parameters), ["self", "metric"])
        self.assertEqual(list(inspect.signature(plot_umap_clusters).parameters), ["X_scaled", "labels", "title", "cluster_names", "point_size", "n"])
        self.assertEqual(list(inspect.signature(plot_vintage_curves).parameters), ["vintage_df", "title", "max_mob", "top_n_safras"])
        self.assertEqual(list(inspect.signature(plot_vintage_heatmap).parameters), ["vintage_df", "title", "max_mob", "metric"])
        self.assertEqual(list(inspect.signature(plot_shap_global).parameters), ["shap_values", "X", "feature_names", "plot_type", "max_display", "save_path"])

    def test_pyspark_consumers_expose_resolved_routes_in_source(self):
        paths = {
            "display/correlation_matrix/correlation_matrix.py": {"plot_correlation_resolvido", "plot_correlation_matrix_resolvido"},
            "display/distribution_grid/distribution_grid.py": {"plot_distributions_resolvido", "plot_distribution_grid_resolvido"},
        }
        for relative, expected in paths.items():
            path = ASSISTANT_ROOT / "hub_snippets" / relative
            tree = ast.parse(path.read_text(encoding="utf-8"))
            names = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
            assigned = {
                target.id
                for node in tree.body if isinstance(node, ast.Assign)
                for target in node.targets if isinstance(target, ast.Name)
            }
            self.assertTrue(expected <= (names | assigned), relative)


class CurvesTests(unittest.TestCase):
    def setUp(self):
        self.y_true = np.array([0, 1] * 10)
        self.y_prob = np.linspace(0.05, 0.95, 20)
        self.reference = load_reference_theme("notebook")

    def test_reference_theme_preserves_curve_data(self):
        cases = [
            (plot_roc_curve(self.y_true, self.y_prob), plot_roc_curve_resolvido(self.y_true, self.y_prob, self.reference)),
            (plot_pr_curve(self.y_true, self.y_prob), plot_pr_curve_resolvido(self.y_true, self.y_prob, self.reference)),
            (plot_lift_curve(self.y_true, self.y_prob), plot_lift_curve_resolvido(self.y_true, self.y_prob, self.reference)),
            (plot_ks_curve(self.y_true, self.y_prob), plot_ks_curve_resolvido(self.y_true, self.y_prob, self.reference)),
        ]
        for legacy, resolved in cases:
            legacy_data = plotly_data(legacy)
            resolved_data = plotly_data(resolved)
            self.assertEqual(len(legacy_data), len(resolved_data))
            for left, right in zip(legacy_data, resolved_data):
                self.assertEqual(left.get("x"), right.get("x"))
                self.assertEqual(left.get("y"), right.get("y"))
                self.assertEqual(left.get("name"), right.get("name"))

    def test_curves_use_dedicated_palette(self):
        theme = proposta(**{
            "palette.curves_legacy": ["#112233", "#445566", "#778899"],
            "palette.categorical": ["#ABCDEF", "#FEDCBA"],
            "surface.card": "#F0F0F0",
        })
        fig = plot_roc_curve_resolvido(self.y_true, self.y_prob, theme)
        self.assertEqual(fig.data[0].line.color, "#112233")
        self.assertEqual(fig.data[1].line.color, theme.tokens["text.plot"])
        self.assertEqual(list(fig.layout.colorway), ["#112233", "#445566", "#778899"])
        self.assertEqual(fig.layout.annotations[0].bgcolor, "#F0F0F0")

    def test_resolved_curve_exports_to_self_contained_html(self):
        theme = proposta(**{"palette.curves_legacy": ["#112233", "#445566"]})
        fig = plot_roc_curve_resolvido(self.y_true, self.y_prob, theme)
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "roc.html"
            fig.write_html(path, include_plotlyjs=True, full_html=True)
            text = path.read_text(encoding="utf-8")
            self.assertIn("#112233", text)
            self.assertGreater(path.stat().st_size, 1000)


class PerformanceMonitorTests(unittest.TestCase):
    def test_resolved_timeline_preserves_values_and_thresholds(self):
        policy = {"auc": {"warning": 0.03, "critical": 0.05, "direction": "higher", "delta": "absolute"}}
        monitor = PerformanceMonitor({"auc": 0.80}, policy=policy)
        monitor.add_period("2026-07", {"auc": 0.78}, 100)
        monitor.add_period("2026-08", {"auc": 0.74}, 120)
        legacy = monitor.plot_timeline("auc")
        theme = proposta(**{
            "brand.primary": "#112233",
            "text.secondary": "#334455",
            "semantic.warning": "#AABBCC",
            "semantic.negative": "#DDEEFF",
        })
        resolved = monitor.plot_timeline_resolvido("auc", theme)
        self.assertEqual(plotly_data(legacy)[0]["x"], plotly_data(resolved)[0]["x"])
        self.assertEqual(plotly_data(legacy)[0]["y"], plotly_data(resolved)[0]["y"])
        self.assertEqual([s.y0 for s in legacy.layout.shapes], [s.y0 for s in resolved.layout.shapes])
        self.assertEqual(resolved.data[0].line.color, "#112233")
        self.assertEqual(resolved.layout.shapes[1].line.color, "#AABBCC")
        self.assertEqual(resolved.layout.shapes[2].line.color, "#DDEEFF")


class UmapTests(unittest.TestCase):
    def test_resolved_umap_reuses_same_embedding(self):
        X = np.array([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]])
        labels = np.array([0, 1, 0])
        embedding = np.array([[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]])
        theme = proposta(**{"palette.categorical": ["#112233", "#445566"]})
        with patch("hub_snippets.ml.umap_viz.umap_viz.compute_umap", return_value=embedding):
            legacy = plot_umap_clusters(X, labels)
            resolved = plot_umap_clusters_resolvido(X, labels, theme)
        for left, right in zip(plotly_data(legacy), plotly_data(resolved)):
            self.assertEqual(left["x"], right["x"])
            self.assertEqual(left["y"], right["y"])
            self.assertEqual(left["name"], right["name"])
        self.assertEqual(resolved.data[0].marker.color, "#112233")
        self.assertEqual(resolved.data[1].marker.color, "#445566")


class VintageTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "safra": ["2026-01", "2026-01", "2026-02", "2026-02"],
            "mob": [0, 1, 0, 1],
            "taxa_acumulada": [0.01, 0.02, 0.015, 0.03],
            "taxa": [0.01, 0.02, 0.015, 0.03],
        })

    def test_resolved_curves_preserve_points(self):
        theme = proposta(**{"palette.categorical": ["#112233", "#445566"]})
        legacy = plot_vintage_curves(self.df)
        resolved = plot_vintage_curves_resolvido(self.df, theme)
        for left, right in zip(plotly_data(legacy), plotly_data(resolved)):
            self.assertEqual(left["x"], right["x"])
            self.assertEqual(left["y"], right["y"])
            self.assertEqual(left["name"], right["name"])

    def test_resolved_heatmap_preserves_matrix(self):
        theme = proposta(**{"palette.sequential": ["#111111", "#555555", "#999999"]})
        legacy = plot_vintage_heatmap(self.df)
        resolved = plot_vintage_heatmap_resolvido(self.df, theme)
        self.assertEqual(plotly_data(legacy)[0]["z"], plotly_data(resolved)[0]["z"])
        self.assertEqual(plotly_data(legacy)[0]["x"], plotly_data(resolved)[0]["x"])
        self.assertEqual(plotly_data(legacy)[0]["y"], plotly_data(resolved)[0]["y"])
        colors = [pair[1] for pair in resolved.data[0].colorscale]
        self.assertEqual(colors, ["#111111", "#555555", "#999999"])


class OptionalDependencyAndLiteralTests(unittest.TestCase):
    def test_optional_visual_dependencies_remain_lazy(self):
        files_and_forbidden = {
            ASSISTANT_ROOT / "hub_snippets/ml/kaplan_meier/kaplan_meier.py": {"lifelines"},
            ASSISTANT_ROOT / "hub_snippets/ml/shap_explainer/shap_explainer.py": {"shap", "matplotlib"},
            ASSISTANT_ROOT / "hub_snippets/ml/umap_viz/umap_viz.py": {"umap"},
        }
        for path, forbidden in files_and_forbidden.items():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            top_level = set()
            for node in tree.body:
                if isinstance(node, ast.Import):
                    top_level.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    top_level.add(node.module.split(".")[0])
            self.assertTrue(forbidden.isdisjoint(top_level), f"{path}: {forbidden & top_level}")

    def test_resolved_routes_do_not_embed_hex_literals(self):
        callables = [
            plot_roc_curve_resolvido,
            plot_pr_curve_resolvido,
            plot_lift_curve_resolvido,
            plot_ks_curve_resolvido,
            PerformanceMonitor.plot_timeline_resolvido,
            plot_umap_clusters_resolvido,
            plot_vintage_curves_resolvido,
            plot_vintage_heatmap_resolvido,
        ]
        for func in callables:
            self.assertIsNone(HEX.search(inspect.getsource(func)), func.__qualname__)


if __name__ == "__main__":
    unittest.main(verbosity=2)
