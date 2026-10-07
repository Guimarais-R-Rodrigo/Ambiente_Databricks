"""Contratos observados no baseline V00. Fixtures sintéticas, sem Spark/rede.

A captura JSON não é screenshot nem homologação no Databricks.
"""
from __future__ import annotations
import argparse
import inspect
import json
import sys
import unittest
from pathlib import Path

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
parser.add_argument('--capturar', action='store_true')
args, remaining = parser.parse_known_args()
sys.path.insert(0, str(args.root / 'ambiente_databricks/.assistant'))

import plotly.graph_objects as go
import plotly.io as pio
from hub_snippets.constants.colors import AZUL_CAIXA, PALETA_CATEGORICA
from hub_snippets.visual.theme_plotly import aplicar_tema, get_tema_eda, registrar_template_plotly
from hub_snippets.visual.section_header import section_header_html


def captura():
    f = go.Figure(go.Bar(x=['A', 'B', 'C'], y=[10, 20, 5], name='Observado', marker_color='#123456'))
    f.update_xaxes(title='Categoria')
    f.update_yaxes(title='Quantidade', range=[0, 25])
    antes = json.loads(f.to_json())
    aplicar_tema(f, 'Fixture sintética', 'fixture_local', 35)
    return {'fixture': {'categorias': ['A', 'B', 'C'], 'valores': [10, 20, 5], 'soma': 35,
                        'seed': None, 'tolerancia': 0, 'motivo': 'inteiros fixos; nenhuma aleatoriedade'},
            'antes': antes, 'depois': json.loads(f.to_json()),
            'header': section_header_html(None, 'X', 'Resumo sintético', 'Sem dados reais')}


class ContratosLegadosTests(unittest.TestCase):
    def test_assinatura_publica(self):
        self.assertEqual(list(inspect.signature(aplicar_tema).parameters), ['fig', 'subtitulo', 'fonte', 'n'])

    def test_mesmo_objeto_retornado(self):
        f = go.Figure(go.Bar(x=['A'], y=[10]))
        self.assertIs(aplicar_tema(f), f)

    def test_dados_nao_mudam(self):
        d = captura()
        self.assertEqual(d['antes']['data'], d['depois']['data'])
        self.assertEqual(d['depois']['data'][0]['y'], [10, 20, 5])

    def test_eixos_unidades_e_limites_nao_mudam(self):
        d = captura()
        for axis in ('xaxis', 'yaxis'):
            self.assertEqual(d['antes']['layout'][axis], d['depois']['layout'][axis])

    def test_cor_explicita_preservada(self):
        self.assertEqual(captura()['depois']['data'][0]['marker']['color'], '#123456')

    def test_configuracao_default_legada(self):
        config = get_tema_eda()
        self.assertEqual(config['height'], 450)
        self.assertEqual(config['width'], 900)
        self.assertEqual(list(config['colorway']), list(PALETA_CATEGORICA))
        self.assertEqual(config['title']['font']['color'], AZUL_CAIXA)

    def test_rodape_formato_brasileiro(self):
        f = go.Figure()
        aplicar_tema(f, 'Sintético', 'fixture_local', 12000)
        self.assertEqual(f.layout.annotations[-1].text, 'N = 12.000 | Fonte: fixture_local | Sintético')

    def test_reaplicacao_preserva_comportamento_de_adicionar_rodape(self):
        f = go.Figure()
        aplicar_tema(f, n=1)
        aplicar_tema(f, n=2)
        self.assertEqual(len(f.layout.annotations), 2)

    def test_registro_global_e_restauracao(self):
        default = pio.templates.default
        existia = 'caixa' in pio.templates
        antigo = pio.templates['caixa'] if existia else None
        try:
            self.assertIsNone(registrar_template_plotly())
            self.assertEqual(pio.templates.default, 'caixa')
        finally:
            pio.templates.default = default
            if existia:
                pio.templates['caixa'] = antigo
            else:
                del pio.templates['caixa']
        self.assertEqual(pio.templates.default, default)

    def test_escape_html(self):
        html = section_header_html(None, '<x>', '<script>teste</script>', '" & <')
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('&quot; &amp; &lt;', html)

    def test_header_deterministico(self):
        self.assertEqual(captura()['header'], captura()['header'])

    def test_captura_deterministica(self):
        self.assertEqual(captura(), captura())


if __name__ == '__main__':
    if args.capturar:
        print(json.dumps(captura(), ensure_ascii=False, sort_keys=True))
    else:
        unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
