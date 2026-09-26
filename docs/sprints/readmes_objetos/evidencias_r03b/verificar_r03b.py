"""Testes suplementares R03-B: sintéticos, sem tabela persistente ou publicação.

Execute com Python preparado e --require-spark para não aceitar ausência de Spark.
Não execute os notebooks inteiros: alguns contêm instalação/reinício de sessão.
Testes de caracterização registram limites; não corrigem a implementação.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import math
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[4]
LIB = ROOT / "ambiente_fonte/.assistant"
sys.path.insert(0, str(LIB))

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from hub_snippets.constants.colors import PALETA_CATEGORICA, VERMELHO, CINZA_ESCURO
from hub_snippets.display.dataframe_styled import display_styled
from hub_snippets.visual.index_generator import gerar_indice_eda
from hub_snippets.visual.section_header import section_header_html
from hub_snippets.visual.theme_plotly import aplicar_tema, get_tema_eda, registrar_template_plotly

OBJECTS = (
    "display/correlation_matrix", "display/dataframe_styled", "display/distribution_grid",
    "visual/index_generator", "visual/section_header", "visual/theme_plotly",
)
try:
    from pyspark.sql import SparkSession
    HAS_SPARK = True
except ModuleNotFoundError as exc:
    if exc.name != "pyspark":
        raise
    HAS_SPARK = False


def run_readme(obj: str, spark=None) -> None:
    path = LIB / "hub_snippets" / obj / "README.md"
    blocks = re.findall(r"(?ms)^```python\n(.*?)^```\s*$", path.read_text())
    if len(blocks) != 1:
        raise AssertionError(f"{obj}: esperado um bloco Python, obtidos {len(blocks)}")
    scope = {"__name__": "__readme_example__"}
    if spark is not None:
        scope["spark"] = spark
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(blocks[0], str(path), "exec"), scope)


class Portable(unittest.TestCase):
    def test_table_does_not_mutate_input(self):
        df = pd.DataFrame({"saldo": [-2.0, 3.0]})
        before = df.copy(deep=True)
        html = display_styled(df, ["saldo"], {"saldo": "{:.1f}"})
        self.assertIn("-2.0", html)
        pd.testing.assert_frame_equal(df, before)

    def test_negative_only_in_selected_column(self):
        html = display_styled(pd.DataFrame({"a": [-2., 1.], "b": [-4., -5.]}), ["a"])
        rule = re.search(r"(#T_[^{}]+)\{[^{}]*font-weight:\s*bold", html)
        self.assertIsNotNone(rule)
        self.assertIn("row0_col0", rule[1])
        self.assertNotIn("col1", rule[1])
        self.assertNotIn("row1_col0", rule[1])
        self.assertIn(VERMELHO, html)

    def test_unknown_highlight_column_is_ignored(self):
        html = display_styled(pd.DataFrame({"a": [-2]}), ["inexistente"])
        self.assertNotIn("font-weight:", html)

    def test_numeric_string_is_not_highlighted(self):
        html = display_styled(pd.DataFrame({"a": ["-2"]}), ["a"])
        self.assertNotIn("font-weight:", html)

    def test_html_not_escaped_by_default(self):
        # Marcação inofensiva; não há execução de scripts nem conteúdo externo.
        with pd.option_context("styler.format.escape", None):
            html = display_styled(pd.DataFrame({"a": ["<b>externo</b>"]}))
        self.assertIn("<b>externo</b>", html)
        self.assertNotIn("&lt;b&gt;externo", html)

    def test_percentage_units_differ(self):
        df = pd.DataFrame({"x": [0.25]})
        self.assertIn("0.2%", display_styled(df, format_dict={"x": "{:.1f}%"}))
        self.assertIn("25.0%", display_styled(df, format_dict={"x": "{:.1%}"}))

    def test_index_default_nine_no_links(self):
        text = gerar_indice_eda(markdown=True)
        self.assertEqual(text.count("* "), 9)
        html = gerar_indice_eda()
        self.assertNotIn("href=", html)
        self.assertIn("Etapa 0", html)
        self.assertIn("Etapa 8", html)

    def test_index_preserves_order_duplicates(self):
        text = gerar_indice_eda([8, 1, 1], markdown=True)
        self.assertLess(text.index("Etapa 8"), text.index("Etapa 1"))
        self.assertEqual(text.count("Etapa 1"), 2)

    def test_index_empty_distinct_from_none(self):
        self.assertNotIn("Etapa", gerar_indice_eda([], markdown=True))
        self.assertIn("Etapa", gerar_indice_eda(None, markdown=True))

    def test_index_invalid_rejected(self):
        with self.assertRaises(KeyError):
            gerar_indice_eda([99])

    def test_index_generator_iterable(self):
        self.assertEqual(gerar_indice_eda(iter([1, 3])), gerar_indice_eda([1, 3]))

    def test_header_stage_defaults(self):
        text = section_header_html(etapa=3)
        self.assertIn("Etapa 3", text)
        self.assertIn("Qualidade", text)

    def test_header_override(self):
        text = section_header_html(etapa=3, titulo="Título próprio", descricao="Contexto")
        self.assertIn("Título próprio", text)
        self.assertIn("Contexto", text)
        self.assertNotIn("Etapa 3", text)

    def test_header_unknown_falls_back(self):
        text = section_header_html(etapa=99)
        self.assertIn("Seção", text)
        self.assertIn("Descrição não informada.", text)

    def test_header_empty_cannot_remove_defaults(self):
        text = section_header_html(etapa=3, titulo="", descricao="")
        self.assertIn("Etapa 3", text)
        self.assertIn("Diagnostica", text)

    def test_header_escapes_controlled_markup(self):
        text = section_header_html(emoji="<b>", titulo='A & "B"', descricao="<i>texto</i>")
        self.assertIn("&lt;b&gt;", text)
        self.assertIn("A &amp; &quot;B&quot;", text)
        self.assertIn("&lt;i&gt;texto&lt;/i&gt;", text)
        self.assertNotIn("<i>texto</i>", text)

    def test_theme_mutates_same_figure_preserves_data(self):
        fig = go.Figure(go.Bar(x=[1, 2], y=[3, 4]))
        before = fig.data[0].to_plotly_json()
        self.assertIs(aplicar_tema(fig), fig)
        self.assertEqual(fig.data[0].to_plotly_json(), before)

    def test_theme_overrides_dimensions_later_customization_wins(self):
        fig = go.Figure().update_layout(width=600)
        aplicar_tema(fig)
        self.assertEqual(fig.layout.width, 900)
        fig.update_layout(width=720)
        self.assertEqual(fig.layout.width, 720)

    def test_theme_repeat_appends_footer(self):
        fig = go.Figure()
        aplicar_tema(fig, n=10)
        aplicar_tema(fig, n=10)
        self.assertEqual(len(fig.layout.annotations), 2)
        aplicar_tema(fig)
        self.assertEqual(len(fig.layout.annotations), 2)

    def test_theme_footer_declared_without_counting_data(self):
        fig = go.Figure(go.Bar(x=[1], y=[1]))
        aplicar_tema(fig, n=12500, fonte="sintética", subtitulo="linhas declaradas")
        self.assertIn("N = 12.500", fig.layout.annotations[-1].text)
        self.assertIn("linhas declaradas", fig.layout.annotations[-1].text)

    def test_theme_explicit_trace_color_preserved(self):
        fig = go.Figure(go.Bar(x=[1], y=[1], marker_color="black"))
        aplicar_tema(fig)
        self.assertEqual(fig.data[0].marker.color, "black")

    def test_theme_palette_reference_and_imported_font(self):
        theme = get_tema_eda()
        self.assertIs(theme["colorway"], PALETA_CATEGORICA)
        self.assertEqual(theme["font"]["color"], CINZA_ESCURO)

    def test_theme_registration_restores_state(self):
        old_default = pio.templates.default
        existed = "caixa" in pio.templates
        old_template = pio.templates["caixa"] if existed else None
        try:
            self.assertIsNone(registrar_template_plotly())
            self.assertEqual(pio.templates.default, "caixa")
            self.assertEqual(pio.templates["caixa"].layout.width, 900)
        finally:
            pio.templates.default = old_default
            if existed:
                pio.templates["caixa"] = old_template
            else:
                del pio.templates["caixa"]
        self.assertEqual(pio.templates.default, old_default)

    def test_readme_dataframe(self):
        run_readme("display/dataframe_styled")

    def test_readme_index(self):
        run_readme("visual/index_generator")

    def test_readme_section(self):
        run_readme("visual/section_header")

    def test_readme_theme(self):
        run_readme("visual/theme_plotly")


@unittest.skipUnless(HAS_SPARK, "PySpark ausente: teste não executado")
class SparkCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = (SparkSession.builder.master("local[2]").appName("R03B-synthetic")
                     .config("spark.ui.enabled", "false")
                     .config("spark.sql.shuffle.partitions", "2")
                     .config("spark.sql.execution.arrow.pyspark.enabled", "false")
                     .getOrCreate())
        cls.spark.sparkContext.setLogLevel("ERROR")
        from hub_snippets.display.correlation_matrix import plot_correlation
        from hub_snippets.display.distribution_grid import plot_distributions
        cls.corr = staticmethod(plot_correlation)
        cls.dist = staticmethod(plot_distributions)

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def linear(self):
        return self.spark.createDataFrame([(float(i), float(3*i), float(-i)) for i in range(1,6)], "a double,b double,c double")

    def test_correlation_linear_signs_symmetry(self):
        fig, pairs = self.corr(self.linear())
        z = fig.data[0].z
        self.assertAlmostEqual(z[0][1], 1.)
        self.assertAlmostEqual(z[0][2], -1.)
        self.assertAlmostEqual(z[0][1], z[1][0])
        self.assertEqual(len(pairs), 3)

    def test_spearman_monotonic(self):
        df = self.spark.createDataFrame([(float(i),float(i*i)) for i in range(1,8)], "a double,b double")
        fig, _ = self.corr(df, method="spearman")
        self.assertAlmostEqual(fig.data[0].z[0][1], 1.)

    def test_threshold_only_changes_pairs(self):
        f1,p1 = self.corr(self.linear(),threshold_highlight=0.8)
        f2,p2 = self.corr(self.linear(),threshold_highlight=1.1)
        self.assertEqual(f1.data[0].to_plotly_json(), f2.data[0].to_plotly_json())
        self.assertTrue(p1)
        self.assertEqual(p2, [])

    def test_correlation_listwise_deletion(self):
        df = self.spark.createDataFrame([(1.,1.,1.),(2.,2.,2.),(3.,3.,3.),(4.,-20.,None)], "a double,b double,c double")
        two,_ = self.corr(df,cols=["a","b"])
        three,_ = self.corr(df,cols=["a","b","c"])
        self.assertLess(two.data[0].z[0][1], 0)
        self.assertAlmostEqual(three.data[0].z[0][1], 1.)

    def test_correlation_constant_nan(self):
        df = self.spark.createDataFrame([(1.,1.),(2.,1.),(3.,1.)], "a double,b double")
        fig,pairs = self.corr(df)
        self.assertTrue(math.isnan(fig.data[0].z[0][1]))
        self.assertEqual(pairs, [])

    def test_correlation_bad_method(self):
        with self.assertRaises(ValueError):
            self.corr(self.linear(),method="kendall")

    def test_correlation_missing_column(self):
        with self.assertRaises(ValueError):
            self.corr(self.linear(),cols=["a","ausente"])

    def test_correlation_single_column(self):
        with self.assertRaises(ValueError):
            self.corr(self.linear(),cols=["a"])

    def test_correlation_features_collision(self):
        df = self.linear().selectExpr("a as features", "b")
        with self.assertRaises(Exception) as caught:
            self.corr(df,cols=["features","b"])
        self.assertIn("features", str(caught.exception).lower())
        self.assertRegex(str(caught.exception).lower(), r"already exists|já existe")

    def test_distribution_raw_values_and_footer(self):
        fig = self.dist(self.linear(),cols=["a","b"],ncols=2,sample_n=10)
        self.assertEqual(len(fig.data),2)
        self.assertEqual(list(fig.data[0].x),[1.,2.,3.,4.,5.])
        self.assertEqual(fig.data[0].type,"histogram")
        self.assertIsNone(fig.data[0].histnorm)
        self.assertIsNone(fig.data[0].nbinsx)
        self.assertIn("N = 5",fig.layout.annotations[-1].text)

    def test_distribution_sample_cap_not_quota(self):
        df=self.spark.range(200).selectExpr("cast(id as double) as x")
        fig=self.dist(df,sample_n=10)
        n=len(fig.data[0].x)
        self.assertLessEqual(n,10)
        self.assertGreater(n,0)
        self.assertIn(f"N = {n}",fig.layout.annotations[-1].text)

    def test_distribution_null_count_not_valid_count(self):
        df=self.spark.createDataFrame([(1.,),(None,),(3.,)], "a double")
        fig=self.dist(df,sample_n=10)
        self.assertEqual(len(fig.data[0].x),3)
        self.assertEqual(sum(math.isnan(v) for v in fig.data[0].x),1)
        self.assertIn("N = 3",fig.layout.annotations[-1].text)

    def test_distribution_invalid_limits(self):
        with self.assertRaises(ValueError):
            self.dist(self.linear(),ncols=0)
        with self.assertRaises(ValueError):
            self.dist(self.linear(),sample_n=0)

    def test_distribution_missing_column(self):
        with self.assertRaises(ValueError):
            self.dist(self.linear(),cols=["ausente"])

    def test_distribution_no_numeric_column(self):
        df=self.spark.createDataFrame([("a",)],"categoria string")
        with self.assertRaises(ValueError):
            self.dist(df)

    def test_aliases(self):
        from hub_snippets.display.correlation_matrix import plot_correlation_matrix
        from hub_snippets.display.distribution_grid import plot_distribution_grid
        self.assertIs(plot_correlation_matrix,self.corr)
        self.assertIs(plot_distribution_grid,self.dist)

    def test_readme_correlation(self):
        run_readme("display/correlation_matrix",self.spark)

    def test_readme_distribution(self):
        run_readme("display/distribution_grid",self.spark)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-spark",action="store_true")
    args=parser.parse_args()
    if args.require_spark and not HAS_SPARK:
        parser.error("PySpark obrigatório nesta execução; não aceitar skips")
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"R03B_RESULT tests={result.testsRun} failures={len(result.failures)} errors={len(result.errors)} skipped={len(result.skipped)}")
    return 0 if result.wasSuccessful() and not (args.require_spark and result.skipped) else 1

if __name__=="__main__":
    raise SystemExit(main())
