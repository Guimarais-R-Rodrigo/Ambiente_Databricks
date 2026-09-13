"""Regressões V05 para escolha, linhagem e reabertura de sessões.

Exercitam filesystem local temporário e objetos ipywidgets quando disponíveis;
não homologam ACL, navegador ou runtime Databricks.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ambiente_fonte/.assistant"))

from hub_snippets.visual.tema import ThemeError, load_reference_theme
from hub_snippets.visual.theme_lab import (
    ThemeLabError,
    build_theme_lab_launcher,
    create_theme_lab,
    create_theme_lab_from_preset,
    get_demo_presets,
    list_theme_lab_sessions,
    prepare_theme_lab_presets,
    reopen_theme_lab_session,
    save_theme_lab_session,
)


def _walk(widget):
    yield widget
    for child in getattr(widget, "children", ()):
        yield from _walk(child)


def _button(root, name):
    return next(w for w in _walk(root) if type(w).__name__ == "Button" and w.description == name)


class PresetTests(unittest.TestCase):
    def test_demo_catalog_is_explicit_and_not_approval(self):
        presets = get_demo_presets()
        self.assertEqual([p.key for p in presets], ["legado_notebook", "executivo_claro"])
        self.assertTrue(all(p.demo for p in presets))
        self.assertTrue(all(p.theme.context == "notebook" for p in presets))
        self.assertTrue(all("não" in p.note.lower() and "aprov" in p.note.lower() for p in presets))

    def test_maintainer_presets_are_revalidated(self):
        theme = load_reference_theme("notebook")
        presets = prepare_theme_lab_presets({"atual": theme})
        self.assertEqual(len(presets), 1)
        self.assertFalse(presets[0].demo)
        self.assertEqual(presets[0].theme.content_sha256, theme.content_sha256)
        self.assertIn("não significa aprovação", presets[0].note)

    def test_bad_key_and_wrong_context_fail_closed(self):
        with self.assertRaises(ThemeLabError) as cm:
            prepare_theme_lab_presets({"../ruim": load_reference_theme("notebook")})
        self.assertEqual(cm.exception.code, "LAB_PRESET_KEY")
        with self.assertRaises(ThemeError) as cm2:
            prepare_theme_lab_presets({"editorial": load_reference_theme("readme")})
        self.assertEqual(cm2.exception.code, "CONTEXT_MISMATCH")

    def test_unknown_preset_does_not_fallback(self):
        presets = get_demo_presets()
        with self.assertRaises(ThemeLabError) as cm:
            create_theme_lab_from_preset(presets, "nao-existe")
        self.assertEqual(cm.exception.code, "LAB_PRESET_UNKNOWN")


class SessionPersistenceTests(unittest.TestCase):
    def _changed(self):
        draft = create_theme_lab(load_reference_theme("notebook"))
        draft.set_token("brand.primary", "#112233")
        draft.set_token("section.title_px", 22)
        return draft

    def test_roundtrip_preserves_base_proposal_history_and_revision(self):
        draft = self._changed()
        base_sha = draft.base.content_sha256
        proposal_sha = draft.current.content_sha256
        history_sha = [item.content_sha256 for item in draft._history]
        revision = draft.revision
        with tempfile.TemporaryDirectory() as tmp:
            receipt = save_theme_lab_session(draft, tmp, "sessao-a")
            self.assertEqual(receipt.base_sha256, base_sha)
            self.assertEqual(receipt.proposal_sha256, proposal_sha)
            self.assertEqual(receipt.history_depth, len(history_sha))
            reopened = reopen_theme_lab_session(tmp, "sessao-a")
            self.assertEqual(reopened.base.content_sha256, base_sha)
            self.assertEqual(reopened.current.content_sha256, proposal_sha)
            self.assertEqual([x.content_sha256 for x in reopened._history], history_sha)
            self.assertEqual(reopened.revision, revision)
            self.assertTrue(reopened.dirty)

    def test_manifest_is_commit_marker_and_contains_lineage(self):
        draft = self._changed()
        with tempfile.TemporaryDirectory() as tmp:
            receipt = save_theme_lab_session(draft, tmp, "linhagem")
            folder = Path(receipt.destination)
            data = json.loads((folder / "session.json").read_text(encoding="utf-8"))
            self.assertEqual(data["base_sha256"], draft.base.content_sha256)
            self.assertEqual(data["proposal_sha256"], draft.current.content_sha256)
            self.assertEqual(data["history_sha256"], [x.content_sha256 for x in draft._history])
            self.assertNotIn("approved", data)
            self.assertNotIn("user", data)
            self.assertEqual(receipt.manifest_sha256, __import__("hashlib").sha256((folder / "session.json").read_bytes()).hexdigest())

    def test_existing_session_is_never_overwritten(self):
        draft = self._changed()
        with tempfile.TemporaryDirectory() as tmp:
            save_theme_lab_session(draft, tmp, "existente")
            before = {p.name: p.read_bytes() for p in (Path(tmp) / "existente").iterdir() if p.is_file()}
            with self.assertRaises(ThemeLabError) as cm:
                save_theme_lab_session(draft, tmp, "existente")
            self.assertEqual(cm.exception.code, "LAB_SESSION_EXISTS")
            after = {p.name: p.read_bytes() for p in (Path(tmp) / "existente").iterdir() if p.is_file()}
            self.assertEqual(after, before)

    def test_incomplete_directory_is_hidden_and_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            partial = Path(tmp) / "parcial"
            partial.mkdir()
            (partial / "base.json").write_text("{}", encoding="utf-8")
            self.assertEqual(list_theme_lab_sessions(tmp), ())
            with self.assertRaises(ThemeLabError) as cm:
                reopen_theme_lab_session(tmp, "parcial")
            self.assertEqual(cm.exception.code, "LAB_SESSION_MANIFEST")

    def test_tampered_proposal_is_refused_without_hash_repair(self):
        draft = self._changed()
        with tempfile.TemporaryDirectory() as tmp:
            receipt = save_theme_lab_session(draft, tmp, "adulterada")
            proposal = Path(receipt.destination) / "proposal.json"
            proposal.write_bytes(proposal.read_bytes().replace(b"#112233", b"#445566"))
            with self.assertRaises(ThemeLabError) as cm:
                reopen_theme_lab_session(tmp, "adulterada")
            self.assertEqual(cm.exception.code, "LAB_SESSION_HASH")

    def test_reopened_history_can_undo_to_previous_valid_state(self):
        draft = self._changed()
        expected_previous = draft._history[-1].content_sha256
        with tempfile.TemporaryDirectory() as tmp:
            save_theme_lab_session(draft, tmp, "undo")
            reopened = reopen_theme_lab_session(tmp, "undo")
            reopened.undo()
            self.assertEqual(reopened.current.content_sha256, expected_previous)

    def test_listing_exposes_only_safe_metadata(self):
        draft = self._changed()
        with tempfile.TemporaryDirectory() as tmp:
            save_theme_lab_session(draft, tmp, "sessao-b")
            infos = list_theme_lab_sessions(tmp)
            self.assertEqual(len(infos), 1)
            self.assertEqual(infos[0].session_name, "sessao-b")
            self.assertEqual(infos[0].base_sha256, draft.base.content_sha256)
            self.assertEqual(infos[0].proposal_sha256, draft.current.content_sha256)


@unittest.skipUnless(importlib.util.find_spec("ipywidgets") and importlib.util.find_spec("IPython"),
                     "UI opcional ausente; workflow V05 instala ipywidgets")
class LauncherTests(unittest.TestCase):
    def test_launcher_marks_demo_and_opens_selected_base(self):
        ui = build_theme_lab_launcher(render_initial=False)
        self.addCleanup(lambda: [w.close() for w in _walk(ui.root)])
        labels = [label for label, _ in ui.preset_control.options]
        self.assertTrue(labels)
        self.assertTrue(all("demonstração" in label for label in labels))
        _button(ui.root, "Abrir ponto de partida").click()
        self.assertTrue(ui.workspace.children)
        self.assertIn("não submete, aprova ou publica", ui.root.children[0].value)

    def test_launcher_saves_and_reopens_session_without_user_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            ui = build_theme_lab_launcher(save_root=tmp, render_initial=False)
            self.addCleanup(lambda: [w.close() for w in _walk(ui.root)])
            _button(ui.root, "Abrir ponto de partida").click()
            session_field = next(w for w in _walk(ui.root) if type(w).__name__ == "Text" and w.description == "Sessão")
            session_field.value = "sessao-ui"
            _button(ui.root, "Salvar sessão rastreável").click()
            self.assertTrue((Path(tmp) / "sessao-ui" / "session.json").is_file(), ui.status.value)
            self.assertTrue(ui.session_control.options)
            ui.session_control.value = "sessao-ui"
            _button(ui.root, "Reabrir sessão").click()
            self.assertIn("Sessão reaberta", ui.status.value)

    def test_launcher_blocks_session_save_with_unapplied_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            ui = build_theme_lab_launcher(save_root=tmp, render_initial=False)
            self.addCleanup(lambda: [w.close() for w in _walk(ui.root)])
            _button(ui.root, "Abrir ponto de partida").click()
            color = next(w for w in _walk(ui.workspace) if type(w).__name__ == "Text" and w.description == "HEX")
            color.value = "#112233"
            session_field = next(w for w in _walk(ui.root) if type(w).__name__ == "Text" and w.description == "Sessão")
            session_field.value = "nao-salvar"
            _button(ui.root, "Salvar sessão rastreável").click()
            self.assertIn("campos ainda não aplicados", ui.status.value)
            self.assertFalse((Path(tmp) / "nao-salvar").exists())


if __name__ == "__main__":
    unittest.main()
