"""Guardas V00: caminhos válidos passam; mutantes falham pelo motivo previsto."""
from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import inventario_visual as v


class InventarioVisualTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.run_git('init', '-q')
        self.module = self.root / 'ambiente_fonte/.assistant/hub_snippets/visual/demo/demo.py'
        self.module.parent.mkdir(parents=True)
        self.module.write_text('COR = "#005CA9"\n\ndef desenhar(x: int = 1) -> str:\n    return str(x)\n', encoding='utf-8')
        (self.root / '.gitignore').write_text('.artifacts/\n', encoding='utf-8')
        (self.root / 'README.md').write_text('# A\n![primeira](um.png)\n## B\n![segunda](dois.svg)\n', encoding='utf-8')
        self.commit()

    def tearDown(self):
        self.tmp.cleanup()

    def run_git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, capture_output=True, check=True)

    def commit(self):
        self.run_git('add', '-A')
        self.run_git('-c', 'user.name=Fixture', '-c', 'user.email=' + 'fixture' + '@' + 'example.invalid', 'commit', '-qm', 'fixture')

    def test_inventario_valido_tem_volume_e_api(self):
        d = v.inventariar(self.root)
        self.assertEqual(d['resumo']['arquivos'], 3)
        self.assertGreater(d['resumo']['ocorrencias'], 0)
        m = d['modulos'][self.module.relative_to(self.root).as_posix()]
        self.assertEqual(m['api'], ['COR', 'desenhar'])
        self.assertEqual(m['constantes'][0]['tipo_literal'], 'str')
        self.assertEqual(m['funcoes'][0]['assinatura'], 'x: int=1')
        self.assertEqual(m['tipo_objeto'], 'FILE')

    def test_determinismo(self):
        self.assertEqual(v.inventariar(self.root), v.inventariar(self.root))

    def test_reutiliza_guarda_git_falho(self):
        with patch.object(v, 'git_paths', side_effect=ValueError('Git indisponível')):
            with self.assertRaisesRegex(ValueError, 'Git indisponível'):
                v.inventariar(self.root)

    def test_lista_vazia_nao_aprova(self):
        with patch.object(v, 'git_paths', return_value=[]):
            with self.assertRaisesRegex(ValueError, 'Varredura vazia'):
                v.inventariar(self.root)

    def test_produto_sem_ocorrencias_nao_aprova(self):
        self.module.write_text('X = 1\n', encoding='utf-8')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'Varredura vazia'):
            v.inventariar(self.root)

    def test_modificacao_nao_commitada_recusada_e_preservada(self):
        self.module.write_text('X = 2\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Worktree suja'):
            v.inventariar(self.root)
        self.assertEqual(self.module.read_text(), 'X = 2\n')

    def test_arquivo_extra_nao_ignorado_recusado(self):
        (self.root / 'extra.txt').write_text('novo', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Worktree suja'):
            v.inventariar(self.root)

    def test_artefato_ignorado_nao_e_lido(self):
        folder = self.root / '.artifacts'
        folder.mkdir()
        (folder / 'binario.py').write_bytes(b'\xff')
        self.assertEqual(v.inventariar(self.root)['resumo']['arquivos'], 3)

    def test_quarentena_versionada_recusada(self):
        folder = self.root / 'Ambiente_Antigo'
        folder.mkdir()
        (folder / 'nao_ler.txt').write_bytes(b'\xff')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'Quarentena'):
            v.inventariar(self.root)

    def test_symlink_interno_recusado(self):
        p = self.root / 'link.py'
        try:
            p.symlink_to(self.module)
        except OSError as e:
            self.skipTest('Plataforma não permite symlink de fixture: ' + type(e).__name__)
        self.commit()
        with self.assertRaisesRegex(ValueError, 'Link simbólico'):
            v.inventariar(self.root)

    def test_utf8_invalido_recusado(self):
        self.module.write_bytes(b'\xff')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'UTF-8 inválido'):
            v.inventariar(self.root)

    def test_ast_invalida_nao_vira_inventario_parcial_aprovado(self):
        self.module.write_text('def broken(\n', encoding='utf-8')
        self.commit()
        with self.assertRaises(SyntaxError):
            v.inventariar(self.root)

    def test_scanner_nao_importa_codigo(self):
        self.module.write_text('COR = "#005CA9"\nraise RuntimeError("não executar")\n', encoding='utf-8')
        self.commit()
        self.assertGreater(v.inventariar(self.root)['resumo']['ocorrencias'], 0)

    def test_notebook_sem_api_de_modulo(self):
        self.module.write_text('# Databricks notebook source\nCOR = "#005CA9"\n', encoding='utf-8')
        self.commit()
        m = v.inventariar(self.root)['modulos'][self.module.relative_to(self.root).as_posix()]
        self.assertEqual(m['tipo_objeto'], 'NOTEBOOK_SOURCE')
        self.assertEqual(m['api'], [])

    def test_imports_e_chamadas_estaticos(self):
        self.module.write_text('from hub_snippets.constants.colors import AZUL_CAIXA\nimport plotly.io as pio\nCOR="#005CA9"\ndef desenhar():\n    aplicar_tema(None)\n', encoding='utf-8')
        self.commit()
        m = v.inventariar(self.root)['modulos'][self.module.relative_to(self.root).as_posix()]
        self.assertEqual(m['imports'][0]['origem'], 'hub_snippets.constants.colors')
        self.assertEqual(m['chamadas_visuais'][0]['funcao'], 'aplicar_tema')

    def test_ordem_e_secao_das_imagens(self):
        rows = v.referencias_imagens((self.root / 'README.md').read_text())
        self.assertEqual([(r['ordem'], r['secao'], r['destino']) for r in rows], [(1, 'A', 'um.png'), (2, 'B', 'dois.svg')])

    def test_html_img_e_capturado(self):
        self.assertEqual(v.referencias_imagens('<img src="banner.png">')[0]['destino'], 'banner.png')

    def test_semantica_nao_e_aprovada_automaticamente(self):
        doc = v.inventariar(self.root)
        self.assertTrue(all(not o['revisado'] for o in doc['ocorrencias']))
        self.assertEqual(doc['estado'], 'INVENTARIO_AUTOMATICO_REQUER_REVISAO')

    def test_camadas_separadas(self):
        self.assertEqual(v.camada('Novo_Ambiente_Simulado/a.py'), 'derivado')
        self.assertEqual(v.camada('.artifacts/simulado/a.py'), 'derivado')
        self.assertEqual(v.camada('novas_funcionalidades/a.py'), 'experimental')
        self.assertEqual(v.camada('tools/a.py'), 'ferramenta')

    def test_protecao_igual(self):
        doc = v.inventariar(self.root)
        self.assertEqual(v.comparar_protegidos(doc, doc), [])

    def test_protecao_detecta_alteracao_adicao_remocao(self):
        before = v.inventariar(self.root)
        after = json.loads(json.dumps(before))
        p = self.module.relative_to(self.root).as_posix()
        next(r for r in after['arquivos'] if r['path'] == p)['sha256'] = 'alterado'
        self.assertEqual(v.comparar_protegidos(before, after), [p])
        after['arquivos'] = [r for r in after['arquivos'] if r['path'] != p]
        after['arquivos'].append({'path': 'ambiente_fonte/novo.png', 'sha256': 'novo'})
        self.assertEqual(v.comparar_protegidos(before, after), sorted([p, 'ambiente_fonte/novo.png']))

    def test_conjunto_protegido_vazio_reprova(self):
        with self.assertRaisesRegex(ValueError, 'Conjunto protegido vazio'):
            v.comparar_protegidos({'arquivos': []}, {'arquivos': []})

    def test_saida_valida_e_sem_sobrescrita(self):
        target = self.root / '.artifacts/v00.json'
        v.gravar(self.root, target, {'a': 1})
        with self.assertRaisesRegex(ValueError, 'Saída já existe'):
            v.gravar(self.root, target, {'a': 2})
        self.assertEqual(json.loads(target.read_text()), {'a': 1})

    def test_saida_no_produto_recusada(self):
        target = self.root / 'ambiente_fonte/resultado.json'
        with self.assertRaisesRegex(ValueError, 'Saída deve estar'):
            v.gravar(self.root, target, {})
        self.assertFalse(target.exists())

    def test_artefatos_symlink_recusado(self):
        folder = self.root / 'destino'
        folder.mkdir()
        try:
            (self.root / '.artifacts').symlink_to(folder, target_is_directory=True)
        except OSError as e:
            self.skipTest('Plataforma não permite symlink de fixture: ' + type(e).__name__)
        with self.assertRaisesRegex(ValueError, 'simbólico'):
            v.gravar(self.root, self.root / '.artifacts/v00.json', {})


    def test_consumidor_sem_literal_de_cor_e_inventariado(self):
        self.module.write_text('import plotly.graph_objects as go\ndef desenhar():\n    return go.Histogram(x=[1, 2])\n', encoding='utf-8')
        self.commit()
        doc=v.inventariar(self.root)
        self.assertTrue(any(o['tipo']=='biblioteca_visual' for o in doc['ocorrencias']))
        row=next(r for r in doc['arquivos'] if r['path']==self.module.relative_to(self.root).as_posix())
        self.assertGreater(row['ocorrencias'],0)

    def test_helper_com_underscore_nao_some_da_matriz(self):
        self.module.write_text('from hub_snippets.visual.theme_plotly import aplicar_tema\ndef desenhar(fig):\n    return aplicar_tema(fig)\n', encoding='utf-8')
        self.commit()
        doc=v.inventariar(self.root)
        self.assertTrue(any(o['tipo']=='helper_visual' for o in doc['ocorrencias']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
