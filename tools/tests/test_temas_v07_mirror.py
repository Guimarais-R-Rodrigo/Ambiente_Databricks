"""V07 — fonte e .artifacts/simulado devem permanecer byte a byte iguais."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "ambiente_databricks/.assistant"
MIRROR = ROOT / ".artifacts/simulado/Users/usuario-free/.assistant"

RELATIVE_PATHS = [
    "hub_snippets/visual/theme_plotly/theme_plotly.py",
    "hub_snippets/visual/theme_plotly/__init__.py",
    "hub_snippets/visual/theme_plotly/README.md",
    "hub_snippets/display/correlation_matrix/correlation_matrix.py",
    "hub_snippets/display/correlation_matrix/__init__.py",
    "hub_snippets/display/correlation_matrix/README.md",
    "hub_snippets/display/distribution_grid/distribution_grid.py",
    "hub_snippets/display/distribution_grid/__init__.py",
    "hub_snippets/display/distribution_grid/README.md",
    "hub_snippets/ml/curves_plotly/curves_plotly.py",
    "hub_snippets/ml/curves_plotly/__init__.py",
    "hub_snippets/ml/curves_plotly/README.md",
    "hub_snippets/ml/performance_monitor/performance_monitor.py",
    "hub_snippets/ml/performance_monitor/README.md",
    "hub_snippets/ml/umap_viz/umap_viz.py",
    "hub_snippets/ml/umap_viz/__init__.py",
    "hub_snippets/ml/umap_viz/README.md",
    "hub_snippets/ml/vintage_analysis/vintage_analysis.py",
    "hub_snippets/ml/vintage_analysis/__init__.py",
    "hub_snippets/ml/vintage_analysis/README.md",
]


class MirrorTests(unittest.TestCase):
    def test_changed_consumers_match_byte_for_byte(self):
        for relative in RELATIVE_PATHS:
            source = SOURCE / relative
            mirror = MIRROR / relative
            self.assertTrue(source.is_file(), relative)
            self.assertTrue(mirror.is_file(), relative)
            self.assertEqual(source.read_bytes(), mirror.read_bytes(), relative)


class SemanticPaletteTests(unittest.TestCase):
    def test_correlation_uses_diverging_palette(self):
        text = (SOURCE / "hub_snippets/display/correlation_matrix/correlation_matrix.py").read_text(encoding="utf-8")
        self.assertIn('tokens["palette.diverging"]', text)
        self.assertNotIn('tokens["palette.sequential"]', text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
