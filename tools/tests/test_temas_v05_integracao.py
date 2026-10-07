"""Regressões adicionais V05: salvamento, callbacks reais e galeria.

Mocks de falha testam o tratamento da falha, não permissões Databricks reais.
Não substituem browser, homologação ou uso por iniciante.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'ambiente_databricks/.assistant'))
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_lab import (
    ThemeLabError, build_ipywidgets_lab, build_preview, create_theme_lab,
    get_control_specs, install_dbutils_fallback,
)
import hub_snippets.visual.theme_lab.theme_lab as impl


def _draft():
    return create_theme_lab(load_reference_theme('notebook'))


def _walk(widget):
    yield widget
    for child in getattr(widget, 'children', ()):
        yield from _walk(child)


def _button(ui, name):
    return next(w for w in _walk(ui.root) if type(w).__name__ == 'Button' and w.description == name)


class SaveSafetyTests(unittest.TestCase):
    def test_permission_error_does_not_delete_preexisting_empty_file(self):
        draft = _draft()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'existente.json'
            target.touch()
            original_open = os.open
            def denied(path, flags, *args, **kwargs):
                if Path(path) == target:
                    raise PermissionError('mensagem arbitrária não deve sair')
                return original_open(path, flags, *args, **kwargs)
            with patch.object(impl.os, 'open', side_effect=denied):
                with self.assertRaises(ThemeLabError) as cm:
                    draft.save_proposal(tmp, target.name)
            self.assertEqual(cm.exception.code, 'LAB_SAVE_IO')
            self.assertNotIn('mensagem arbitrária', str(cm.exception))
            self.assertTrue(target.exists())
            self.assertEqual(target.read_bytes(), b'')

    def test_invalid_root_has_operational_error_and_no_write(self):
        for root in (None, 7, ['pasta'], 'pasta\x00invalida'):
            with self.subTest(root=repr(root)), self.assertRaises(ThemeLabError) as cm:
                _draft().save_proposal(root, 'proposta.json')
            self.assertEqual(cm.exception.code, 'LAB_SAVE_ROOT')

    def test_fsync_failure_does_not_issue_receipt_or_delete_file(self):
        draft = _draft()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(impl.os, 'fsync', side_effect=OSError('disco')):
                with self.assertRaises(ThemeLabError) as cm:
                    draft.save_proposal(tmp, 'parcial.json')
            self.assertEqual(cm.exception.code, 'LAB_SAVE_IO')
            self.assertIn('parcial', str(cm.exception))
            self.assertTrue((Path(tmp) / 'parcial.json').exists())
            with self.assertRaises(ThemeLabError) as retry:
                draft.save_proposal(tmp, 'parcial.json')
            self.assertEqual(retry.exception.code, 'LAB_SAVE_EXISTS')

    def test_receipt_has_destination_and_verified_bytes(self):
        draft = _draft()
        with tempfile.TemporaryDirectory() as tmp:
            receipt = draft.save_proposal(tmp, 'proposta.json')
            self.assertEqual(receipt.destination, str(Path(tmp).absolute() / receipt.filename))
            data = Path(receipt.destination).read_bytes()
            self.assertEqual(data, draft.export_bytes())
            self.assertEqual(receipt.bytes_written, len(data))
            self.assertEqual(receipt.sha256, __import__('hashlib').sha256(data).hexdigest())

    def test_symlink_target_is_not_followed_or_removed(self):
        draft = _draft()
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / 'real.txt'; real.write_text('preservar')
            link = Path(tmp) / 'proposta.json'
            try:
                link.symlink_to(real)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f'filesystem sem symlink de arquivo: {exc}')
            with self.assertRaises(ThemeLabError) as cm:
                draft.save_proposal(tmp, link.name)
            self.assertEqual(cm.exception.code, 'LAB_SAVE_EXISTS')
            self.assertTrue(link.is_symlink())
            self.assertEqual(real.read_text(), 'preservar')

    def test_empty_palette_fields_are_not_silently_discarded(self):
        draft = _draft(); before = draft.current.content_sha256
        for value in ('#112233,,#445566', '#112233,', ',#112233', ''):
            with self.subTest(value=value), self.assertRaises(ThemeLabError):
                draft.set_token('palette.categorical', value)
        self.assertEqual(draft.current.content_sha256, before)
        self.assertEqual(draft.history_depth, 0)

    def test_short_write_is_failure_not_receipt(self):
        draft = _draft(); original_fdopen = os.fdopen
        class Partial:
            def __init__(self, stream): self.stream = stream
            def __enter__(self): return self
            def __exit__(self, *args): self.stream.close()
            def write(self, data): return self.stream.write(data[:10])
        def partial_open(fd, mode, *args, **kwargs):
            stream = original_fdopen(fd, mode, *args, **kwargs)
            return Partial(stream) if mode == 'w+b' else stream
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(impl.os, 'fdopen', side_effect=partial_open):
                with self.assertRaises(ThemeLabError) as cm:
                    draft.save_proposal(tmp, 'curto.json')
            self.assertEqual(cm.exception.code, 'LAB_SAVE_IO')
            self.assertEqual((Path(tmp) / 'curto.json').stat().st_size, 10)


class ControlCoverageTests(unittest.TestCase):
    def test_controls_without_preview_are_explicit(self):
        specs = {s.token: s for s in get_control_specs(load_reference_theme('notebook'))}
        self.assertFalse(specs['palette.sequential'].preview_supported)
        self.assertTrue(specs['palette.sequential'].unavailable_reason)
        self.assertTrue(specs['palette.diverging'].preview_supported)
        self.assertTrue(specs['brand.primary'].preview_supported)

    def test_fallback_reinstallation_preserves_typed_values(self):
        class Widgets:
            def __init__(self): self.values = {}
            def get(self, name): return self.values[name]
            def text(self, name, default, label): self.values[name] = default
        class Dbutils:
            def __init__(self): self.widgets = Widgets()
        d = _draft(); db = Dbutils()
        names = install_dbutils_fallback(d, db)
        db.widgets.values[names['brand.primary']] = '#112233'
        install_dbutils_fallback(d, db)
        self.assertEqual(db.widgets.values[names['brand.primary']], '#112233')
        before = dict(db.widgets.values)
        with self.assertRaises(ThemeLabError):
            install_dbutils_fallback(d, db, prefix='../ruim')
        self.assertEqual(db.widgets.values, before)


class GalleryCoverageTests(unittest.TestCase):
    def test_diverging_colors_reach_heatmap_without_changing_values(self):
        draft = _draft(); original = build_preview(draft.current)
        colors = ['#112233', '#667788', '#CCDDEE']
        draft.set_token('palette.diverging', colors)
        new = build_preview(draft.current)
        self.assertEqual([color for _, color in new.heatmap_figure.data[0].colorscale], colors)
        self.assertEqual(original.heatmap_figure.data[0].z, new.heatmap_figure.data[0].z)
        self.assertEqual(new.heatmap_figure.data[0].zmin, -1)
        self.assertEqual(new.heatmap_figure.data[0].zmax, 1)
        self.assertEqual(new.heatmap_figure.data[0].zmid, 0)

    def test_bar_has_four_fixed_series(self):
        p = build_preview(load_reference_theme('notebook'))
        self.assertEqual(len(p.bar_figure.data), 4)
        self.assertEqual(list(p.bar_figure.data[0].y), [12, 7, 15, 9])
        self.assertEqual(p.bar_figure.layout.barmode, 'group')


@unittest.skipUnless(importlib.util.find_spec('ipywidgets') and importlib.util.find_spec('IPython'),
                     'UI opcional ausente; workflow específico V05 a instala explicitamente')
class RealWidgetCallbackTests(unittest.TestCase):
    def make_ui(self, **kwargs):
        ui = build_ipywidgets_lab(_draft(), render_initial=False, **kwargs)
        self.addCleanup(lambda: [w.close() for w in _walk(ui.root)])
        return ui

    def test_failed_generation_preserves_draft_and_last_outputs(self):
        ui = self.make_ui(); before = ui.draft.current.content_sha256
        old = ({'output_type': 'display_data', 'data': {'text/html': '<b>prévia anterior</b>'}, 'metadata': {}},)
        ui.preview.outputs = old
        ui.controls['brand.primary'].value = '#112233'
        with patch.object(impl, 'build_preview', side_effect=ThemeLabError('SIMULADA', 'falha', action='corrigir')):
            _button(ui, 'Aplicar na prévia').click()
        self.assertEqual(ui.draft.current.content_sha256, before)
        self.assertEqual(ui.draft.history_depth, 0)
        self.assertEqual(ui.preview.outputs, old)
        self.assertIn('Não aplicado', ui.status.value)

    def test_pending_fields_block_save_and_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            ui = self.make_ui(save_root=tmp)
            ui.controls['brand.primary'].value = '#112233'
            _button(ui, 'Salvar proposta').click()
            self.assertIn('LAB_PENDING_FIELDS', ui.status.value)
            self.assertEqual(list(Path(tmp).iterdir()), [])
            _button(ui, 'Exportar JSON na saída').click()
            self.assertIn('LAB_PENDING_FIELDS', ui.status.value)

    def test_apply_emits_symmetric_gallery_without_script_or_cdn(self):
        ui = self.make_ui()
        ui.controls['brand.primary'].value = '#112233'
        _button(ui, 'Aplicar na prévia').click()
        self.assertTrue(ui.draft.dirty, ui.status.value)
        outputs = ui.preview.outputs
        self.assertEqual(len(outputs), 14)
        self.assertEqual(sum('application/vnd.plotly.v1+json' in o['data'] for o in outputs), 6)
        serialized = json.dumps(outputs)
        self.assertNotIn('<script', serialized)
        self.assertNotIn('cdn.plot.ly', serialized)

    def test_restore_requires_explicit_confirmation(self):
        ui = self.make_ui()
        ui.controls['brand.primary'].value = '#112233'
        _button(ui, 'Aplicar na prévia').click()
        self.assertTrue(ui.draft.dirty, ui.status.value)
        changed = ui.draft.current.content_sha256
        _button(ui, 'Restaurar ponto de partida').click()
        self.assertEqual(ui.draft.current.content_sha256, changed)
        confirm = next(w for w in _walk(ui.root) if type(w).__name__ == 'Checkbox')
        confirm.value = True
        _button(ui, 'Restaurar ponto de partida').click()
        self.assertFalse(ui.draft.dirty, ui.status.value)

    def test_unimplemented_fields_disabled(self):
        ui = self.make_ui()
        self.assertTrue(ui.controls['palette.sequential'].disabled)
        self.assertFalse(ui.controls['palette.diverging'].disabled)
        self.assertTrue(_button(ui, 'Publicar versão aprovada').disabled)
        self.assertTrue(_button(ui, 'Submeter para revisão').disabled)


if __name__ == '__main__':
    unittest.main()
