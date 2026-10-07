"""V05 — Visual Lab notebook com rascunho isolado e UI opcional.

Sem Databricks, rede ou dados reais. A suíte geral tolera ausência de ipywidgets
como SKIP explícito; o workflow V05 usa --require-ipywidgets e não admite esse SKIP.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / "ambiente_databricks/.assistant"
sys.path.insert(0, str(PRODUCT))

from hub_snippets.visual.tema import ThemeError, load_reference_theme, resolve_theme
from hub_snippets.visual.theme_lab import (
    ThemeLabDraft,
    ThemeLabError,
    apply_dbutils_fallback,
    build_ipywidgets_lab,
    build_preview,
    compare_preview,
    create_theme_lab,
    get_control_specs,
    install_dbutils_fallback,
)

REQUIRE_IPYWIDGETS = "--require-ipywidgets" in sys.argv
if REQUIRE_IPYWIDGETS:
    sys.argv.remove("--require-ipywidgets")
IPYWIDGETS_AVAILABLE = importlib.util.find_spec("ipywidgets") is not None and importlib.util.find_spec("IPython") is not None


def tema_proposta(*, mode: str = "light", **tokens):
    data = load_reference_theme("notebook").to_dict()
    data["theme_id"] = "hub-v05-proposta"
    data["display_name"] = "V05 proposta sintética"
    data["description"] = "Configuração sintética para testar o Visual Lab V05."
    data["mode"] = mode
    data["tokens"].update(tokens)
    return resolve_theme(data, expected_context="notebook")


class DraftTests(unittest.TestCase):
    def test_criacao_revalida_e_nao_altera_base_recebida(self):
        base = load_reference_theme("notebook")
        original = base.content_sha256
        draft = create_theme_lab(base)
        self.assertIsInstance(draft, ThemeLabDraft)
        self.assertEqual(draft.current.content_sha256, original)
        self.assertEqual(base.content_sha256, original)
        self.assertFalse(draft.dirty)
        self.assertEqual(draft.history_depth, 0)

    def test_tipo_incorreto_e_rejeitado(self):
        with self.assertRaises(ThemeLabError) as cm:
            create_theme_lab({})
        self.assertEqual(cm.exception.code, "LAB_THEME_TYPE")

    def test_contexto_nao_notebook_e_rejeitado(self):
        with self.assertRaises(ThemeError):
            create_theme_lab(load_reference_theme("readme"))

    def test_hex_minusculo_e_normalizado_explicitamente(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        draft.set_token("brand.primary", "#0066cc")
        self.assertEqual(draft.current.tokens["brand.primary"], "#0066CC")
        self.assertTrue(draft.dirty)
        self.assertEqual(draft.history_depth, 1)

    def test_atualizacao_multipla_e_atomica(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        antes = draft.current.content_sha256
        with self.assertRaises((ThemeLabError, ThemeError)):
            draft.apply_updates({"section.title_px": 20, "brand.primary": "invalida"})
        self.assertEqual(draft.current.content_sha256, antes)
        self.assertEqual(draft.history_depth, 0)
        self.assertEqual(draft.revision, 0)

    def test_limite_do_schema_falha_sem_commit_parcial(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        antes = draft.current.content_sha256
        with self.assertRaises(ThemeError):
            draft.apply_updates({"chart.width_px": 999999})
        self.assertEqual(draft.current.content_sha256, antes)
        self.assertFalse(draft.dirty)

    def test_token_desconhecido_falha_sem_mudar_estado(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        antes = draft.current.content_sha256
        with self.assertRaises(ThemeLabError) as cm:
            draft.set_token("css.livre", "body{}")
        self.assertEqual(cm.exception.code, "LAB_TOKEN_UNKNOWN")
        self.assertEqual(draft.current.content_sha256, antes)

    def test_booleano_nao_vira_inteiro(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        with self.assertRaises(ThemeLabError) as cm:
            draft.set_token("chart.title_px", True)
        self.assertEqual(cm.exception.code, "LAB_VALUE_TYPE")

    def test_paleta_string_e_normalizada(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        atual = list(draft.current.tokens["palette.categorical"])
        atual[0] = "#0066cc"
        draft.set_token("palette.categorical", ",".join(atual))
        self.assertEqual(draft.current.tokens["palette.categorical"][0], "#0066CC")

    def test_paleta_divergente_par_e_rejeitada(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        antes = draft.current.content_sha256
        with self.assertRaises(ThemeError):
            draft.set_token("palette.diverging", ["#000000", "#FFFFFF"])
        self.assertEqual(draft.current.content_sha256, antes)

    def test_noop_nao_cria_historico(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        draft.set_token("brand.primary", draft.current.tokens["brand.primary"])
        self.assertEqual(draft.revision, 0)
        self.assertEqual(draft.history_depth, 0)

    def test_undo_e_restore(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        base = draft.base.content_sha256
        draft.set_token("brand.primary", "#0066CC")
        primeiro = draft.current.content_sha256
        draft.set_token("section.title_px", 20)
        self.assertNotEqual(draft.current.content_sha256, primeiro)
        draft.undo()
        self.assertEqual(draft.current.content_sha256, primeiro)
        draft.restore()
        self.assertEqual(draft.current.content_sha256, base)
        self.assertFalse(draft.dirty)

    def test_undo_vazio_falha(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        with self.assertRaises(ThemeLabError) as cm:
            draft.undo()
        self.assertEqual(cm.exception.code, "LAB_UNDO_EMPTY")

    def test_duas_instancias_nao_compartilham_estado(self):
        base = load_reference_theme("notebook")
        a = create_theme_lab(base)
        b = create_theme_lab(base)
        a.set_token("brand.primary", "#0066CC")
        self.assertNotEqual(a.current.content_sha256, b.current.content_sha256)
        self.assertEqual(b.current.content_sha256, base.content_sha256)

    def test_exportacao_em_memoria_nao_escreve(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        with tempfile.TemporaryDirectory() as tmp:
            antes = list(Path(tmp).iterdir())
            raw = draft.export_bytes()
            depois = list(Path(tmp).iterdir())
        self.assertEqual(antes, depois)
        self.assertEqual(json.loads(raw)["context"], "notebook")


class SaveTests(unittest.TestCase):
    def test_salvar_proposta_cria_novo_json_e_recibo(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        draft.set_token("brand.primary", "#0066CC")
        with tempfile.TemporaryDirectory() as tmp:
            receipt = draft.save_proposal(tmp, "proposta-v05.json")
            path = Path(tmp) / receipt.filename
            self.assertTrue(path.is_file())
            self.assertEqual(path.read_bytes(), draft.export_bytes())
            self.assertEqual(receipt.bytes_written, len(path.read_bytes()))
            self.assertEqual(receipt.sha256, __import__("hashlib").sha256(path.read_bytes()).hexdigest())

    def test_salvar_nao_sobrescreve(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "proposta.json").write_text("existente", encoding="utf-8")
            with self.assertRaises(ThemeLabError) as cm:
                draft.save_proposal(tmp, "proposta.json")
            self.assertEqual(cm.exception.code, "LAB_SAVE_EXISTS")
            self.assertEqual((Path(tmp) / "proposta.json").read_text(encoding="utf-8"), "existente")

    def test_nome_com_path_e_rejeitado(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("../x.json", "pasta/x.json", "/tmp/x.json", "Com Espaco.json", "x.txt"):
                with self.subTest(name=name), self.assertRaises(ThemeLabError):
                    draft.save_proposal(tmp, name)

    def test_raiz_inexistente_e_rejeitada(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ThemeLabError) as cm:
                draft.save_proposal(Path(tmp) / "nao-existe", "proposta.json")
            self.assertEqual(cm.exception.code, "LAB_SAVE_ROOT")


class MetadataTests(unittest.TestCase):
    def test_specs_derivados_do_schema_e_com_nomes_legiveis(self):
        theme = load_reference_theme("notebook")
        specs = get_control_specs(theme)
        by_token = {s.token: s for s in specs}
        self.assertIn("brand.primary", by_token)
        self.assertEqual(by_token["brand.primary"].label, "Cor principal")
        self.assertEqual(by_token["brand.primary"].unit, "hex")
        self.assertTrue(by_token["brand.primary"].primary)
        self.assertTrue(by_token["chart.title_px"].primary)
        self.assertTrue(all(s.description for s in specs))

    def test_metadado_nao_muta_tema(self):
        theme = load_reference_theme("notebook")
        before = theme.content_sha256
        get_control_specs(theme)
        self.assertEqual(theme.content_sha256, before)


class PreviewTests(unittest.TestCase):
    def test_preview_reusa_dados_sinteticos_e_nao_muda_default_plotly(self):
        import plotly.io as pio
        default = pio.templates.default
        preview = build_preview(load_reference_theme("notebook"))
        self.assertEqual(pio.templates.default, default)
        self.assertEqual(list(preview.bar_figure.data[0].y), [12, 7, 15, 9])
        self.assertEqual(list(preview.series_figure.data[0].y), [100, 112, None, 109, 121])
        self.assertIn("Dados sintéticos", str(preview.bar_figure.layout.annotations[0].text))
        self.assertIn("Nulo", preview.table_html)

    def test_comparacao_preserva_data_dos_graficos(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        draft.set_token("brand.primary", "#0066CC")
        pair = compare_preview(draft)
        for name in ("bar_figure", "series_figure", "heatmap_figure"):
            atual = getattr(pair.current, name).to_plotly_json()["data"]
            proposta = getattr(pair.proposal, name).to_plotly_json()["data"]
            self.assertEqual(atual, proposta, name)

    def test_dark_e_high_contrast_nao_fingem_preview_plotly(self):
        for mode in ("dark", "high_contrast"):
            with self.subTest(mode=mode), self.assertRaises(ThemeLabError) as cm:
                build_preview(tema_proposta(mode=mode))
            self.assertEqual(cm.exception.code, "LAB_PREVIEW_MODE")

    def test_comparacao_exige_draft(self):
        with self.assertRaises(ThemeLabError):
            compare_preview(load_reference_theme("notebook"))


class FakeWidgets:
    def __init__(self):
        self.values = {}
        self.labels = {}

    def text(self, name, default, label):
        self.values[name] = default
        self.labels[name] = label

    def get(self, name):
        return self.values[name]


class FakeDbutils:
    def __init__(self):
        self.widgets = FakeWidgets()


class FallbackTests(unittest.TestCase):
    def test_fallback_cria_apenas_controles_primarios_e_aplica_strings(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        dbutils = FakeDbutils()
        names = install_dbutils_fallback(draft, dbutils)
        self.assertEqual(set(names), {
            "brand.primary", "text.primary", "text.secondary", "surface.section",
            "surface.card", "chart.title_px", "section.title_px",
        })
        dbutils.widgets.values[names["brand.primary"]] = "#0066cc"
        dbutils.widgets.values[names["chart.title_px"]] = "18"
        apply_dbutils_fallback(draft, dbutils)
        self.assertEqual(draft.current.tokens["brand.primary"], "#0066CC")
        self.assertEqual(draft.current.tokens["chart.title_px"], 18)

    def test_fallback_sem_dbutils_falha(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        with self.assertRaises(ThemeLabError) as cm:
            install_dbutils_fallback(draft, object())
        self.assertEqual(cm.exception.code, "LAB_DBUTILS")


class DependencyTests(unittest.TestCase):
    def test_import_do_modulo_nao_importa_ipywidgets(self):
        code = (
            "import sys; "
            f"sys.path.insert(0, {str(PRODUCT)!r}); "
            "import hub_snippets.visual.theme_lab; "
            "assert 'ipywidgets' not in sys.modules"
        )
        completed = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=20)
        self.assertEqual(completed.returncode, 0, completed.stderr)

    @unittest.skipUnless(IPYWIDGETS_AVAILABLE, "ipywidgets/IPython ausentes; workflow V05 usa --require-ipywidgets")
    def test_ui_real_constroi_sem_exibir_e_sem_mudar_tema(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        before = draft.current.content_sha256
        ui = build_ipywidgets_lab(draft, render_initial=False)
        self.assertIs(ui.draft, draft)
        self.assertEqual(type(ui.root).__name__, "Tab")
        self.assertGreater(len(ui.controls), 20)
        self.assertEqual(draft.current.content_sha256, before)
        self.assertFalse(draft.dirty)


class DocumentationTests(unittest.TestCase):
    def test_objeto_tem_contrato_readme_exemplo_e_fachada(self):
        folder = PRODUCT / "hub_snippets/visual/theme_lab"
        for name in ("theme_lab.py", "__init__.py", "README.md", "exemplo_theme_lab.py"):
            self.assertTrue((folder / name).is_file(), name)
        readme = (folder / "README.md").read_text(encoding="utf-8")
        self.assertIn("<!-- readme-objeto: 1.0.0 -->", readme)
        self.assertIn("não publica", readme.lower())

    def test_codigo_nao_contem_rede_spark_ou_publicacao(self):
        text = (PRODUCT / "hub_snippets/visual/theme_lab/theme_lab.py").read_text(encoding="utf-8")
        forbidden = ("requests.", "urllib.request", "spark.sql", "mlflow", "force_publish", "pio.templates.default =")
        for fragment in forbidden:
            self.assertNotIn(fragment, text, fragment)


if __name__ == "__main__":
    if REQUIRE_IPYWIDGETS and not IPYWIDGETS_AVAILABLE:
        raise SystemExit("V05 exige ipywidgets/IPython neste workflow; não converter ausência em PASS.")
    unittest.main()
