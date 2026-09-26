"""Testes suplementares R03-A. Não publica, não grava tabelas; Spark isolado.

python docs/sprints/readmes_objetos/evidencias_r03a/verificar_r03a.py
python docs/sprints/readmes_objetos/evidencias_r03a/verificar_r03a.py --require-spark

Os testes de limitações caracterizam a implementação, não a aprovam como ideal.
"""
from __future__ import annotations
import ast
import contextlib
import copy
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import random
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[4]
HUB = ROOT / 'ambiente_fonte/.assistant'
sys.path.insert(0, str(HUB))
from hub_snippets.constants import colors, emojis, styles
from hub_snippets.visual.badge import badge_status, badge_score, badge_inline
from hub_snippets.visual.divider import divider_light, divider_medium, divider_heavy, divider_section
from hub_snippets.visual.kpi_card import kpi_card_html, kpi_card_markdown
OBJECTS = ['constants/colors', 'constants/emojis', 'constants/styles', 'testing/fixtures',
           'visual/badge', 'visual/divider', 'visual/kpi_card']

def contrast(fg: str, bg: str) -> float:
    def luminance(h: str) -> float:
        c = [int(h[i:i+2], 16)/255 for i in (1, 3, 5)]
        linear = [x/12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in c]
        return sum(a*b for a,b in zip(linear, (.2126,.7152,.0722)))
    a,b = sorted((luminance(fg),luminance(bg)))
    return (b+.05)/(a+.05)

class Portable(unittest.TestCase):
    def test_palettes_and_aliases(self):
        self.assertEqual([len(colors.PALETA_CATEGORICA),len(colors.PALETA_SEQUENCIAL),len(colors.PALETA_DIVERGENTE)],[10,5,5])
        self.assertEqual(colors.COR_POSITIVO,colors.VERDE)
        self.assertEqual(colors.COR_NEGATIVO,colors.VERMELHO)
        for x in colors.PALETA_CATEGORICA:
            self.assertRegex(x,r'^#[0-9A-F]{6}$')
    def test_palette_copy_preserves_original(self):
        before=colors.PALETA_CATEGORICA.copy(); local=colors.PALETA_CATEGORICA.copy();local.append('#000000')
        self.assertEqual(colors.PALETA_CATEGORICA,before)
    def test_emojis_keys_and_absent_key(self):
        self.assertEqual(list(emojis.SECOES_EDA),list(range(9)))
        self.assertEqual(len(emojis.SEMANTICA),11)
        with self.assertRaises(KeyError): _=emojis.SEMANTICA['inexistente']
    def test_emojis_nested_copy(self):
        before=copy.deepcopy(emojis.SECOES_EDA);local=copy.deepcopy(before);local[0]['titulo']='Outro'
        self.assertEqual(emojis.SECOES_EDA,before)
    def test_styles_real_values(self):
        self.assertEqual(styles.FONT_FAMILY,'Segoe UI, Roboto, sans-serif')
        self.assertIn(colors.AZUL_CAIXA, styles.STYLE_SECTION_HEADER)
        self.assertIn(colors.BG_SECTION, styles.STYLE_SECTION_HEADER)
        self.assertIn('font-size:11px', styles.STYLE_BADGE_WARN)
    def test_no_styles_import_in_three_components(self):
        for obj in ('badge','divider','kpi_card'):
            p=HUB/f'hub_snippets/visual/{obj}/{obj}.py'
            for n in ast.walk(ast.parse(p.read_text())):
                if isinstance(n,ast.ImportFrom):
                    self.assertNotEqual(n.module,'hub_snippets.constants.styles')
                    if n.module=='hub_snippets.constants': self.assertNotIn('styles',[a.name for a in n.names])
                elif isinstance(n,ast.Import): self.assertNotIn('hub_snippets.constants.styles',[a.name for a in n.names])
    def test_badge_escape(self):
        h=badge_status('<script>"x" & y</script>','warn')
        self.assertNotIn('<script>',h);self.assertIn('&lt;script&gt;',h);self.assertIn('&quot;',h);self.assertIn('&amp;',h)
    def test_badge_fallback_and_inline(self):
        self.assertEqual(badge_status('x','inexistente'),badge_status('x','info'))
        self.assertEqual(badge_inline('x'),badge_status('x','info'))
    def test_badge_boundaries(self):
        for v,color in [(49,'#B71C1C'),(50,'#B26A00'),(79,'#B26A00'),(80,'#2E7D32')]:
            self.assertIn(color,badge_score(v))
    def test_badge_rounding_is_not_threshold(self):
        h=badge_score(79.6);self.assertIn('80/100',h);self.assertIn('#B26A00',h)
        h=badge_score(49.6);self.assertIn('50/100',h);self.assertIn('#B71C1C',h)
    def test_badge_unvalidated_zero_and_range(self):
        self.assertIn('1/0',badge_score(1,0));self.assertIn('#B71C1C',badge_score(1,0))
        self.assertIn('150/100',badge_score(150));self.assertIn('-1/100',badge_score(-1))
    def test_warning_contrast_characterization(self):
        self.assertAlmostEqual(contrast('#B26A00','#FFF8E1'),3.9894588487750156,places=9)
        self.assertLess(contrast('#B26A00','#FFF8E1'),4.5)
        self.assertLess(contrast('#FFFFFF',colors.COR_ALERTA),4.5)
        self.assertLess(contrast('#FFFFFF',colors.COR_POSITIVO),4.5)
    def test_dividers_and_no_parameters(self):
        for f,n in [(divider_light,1),(divider_medium,1),(divider_heavy,1),(divider_section,2)]:
            self.assertEqual(f(),f());self.assertEqual(f().count('<hr '),n)
            with self.assertRaises(TypeError): f('titulo')
    def test_kpi_html_escape_order_and_no_mutation(self):
        d={'A <': '"x" & y','B':.928};before=copy.deepcopy(d);h=kpi_card_html(d)
        self.assertIn('A &lt;',h);self.assertIn('&quot;x&quot; &amp; y',h)
        self.assertLess(h.index('A &lt;'),h.index(' B'))
        self.assertIn('0.928',h);self.assertNotIn('92,8%',h);self.assertEqual(d,before)
    def test_kpi_markdown_only_pipe_escaped(self):
        self.assertEqual(kpi_card_markdown({'a|b':'*x*|y'}),'> ***x*\\|y** a\\|b')
        self.assertEqual(kpi_card_html({}),'');self.assertEqual(kpi_card_markdown({}),'> ')
    def test_kpi_key_collision_characterization(self):
        self.assertEqual(kpi_card_markdown({1:'a','1':'b'}),'> **b** 1')
    def test_six_portable_readme_blocks(self):
        count=0
        for obj in OBJECTS:
            if obj=='testing/fixtures': continue
            text=(HUB/f'hub_snippets/{obj}/README.md').read_text()
            blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
            self.assertEqual(len(blocks),1,obj)
            with contextlib.redirect_stdout(io.StringIO()) as out:
                exec(compile(blocks[0],obj+'/README.md','exec'),{'__name__':'__readme_check__'})
            self.assertTrue(out.getvalue().strip(),obj)
            print('README_PORTATIL',obj,json.dumps(out.getvalue().strip(),ensure_ascii=False))
            count+=1
        self.assertEqual(count,6)

HAS_SPARK=importlib.util.find_spec('pyspark') is not None
@unittest.skipUnless(HAS_SPARK,'PySpark ausente neste ambiente; não usar simulação como execução real')
class SparkFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyspark.sql import SparkSession
        cls.temp=tempfile.TemporaryDirectory(prefix='r03a_spark_')
        cls.spark=(SparkSession.builder.master('local[2]').appName('r03a-fixtures-sinteticas')
            .config('spark.ui.enabled','false').config('spark.sql.shuffle.partitions','2')
            .config('spark.sql.warehouse.dir',cls.temp.name).getOrCreate())
        cls.spark.sparkContext.setLogLevel('ERROR')
        from hub_snippets.testing import fixtures
        cls.f=fixtures
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop();cls.temp.cleanup()
    def test_tabular_count_keys_schema(self):
        df=self.f.base_tabular(n=20,n_entidades=5,seed=42)
        self.assertEqual(df.count(),20);self.assertEqual(df.select('id_cliente').distinct().count(),5)
        self.assertEqual(df.dtypes,[('id_cliente','string'),('uf','string'),('renda','double'),('dt_referencia','date'),('alvo','int')])
    def test_repeatable_sorted_and_isolated_random(self):
        state=random.getstate()
        a=self.f.base_tabular(20,seed=42).orderBy('id_cliente').collect()
        b=self.f.base_tabular(20,seed=42).orderBy('id_cliente').collect()
        self.assertEqual(a,b);self.assertEqual(random.getstate(),state)
        c=self.f.base_tabular(20,seed=43).orderBy('id_cliente').collect();self.assertNotEqual(a,c)
    def test_tabular_zero_entities_falls_back(self):
        self.assertEqual(self.f.base_tabular(7,n_entidades=0).select('id_cliente').distinct().count(),7)
    def test_invalid_parameters(self):
        for kwargs in ({'n':0},{'pct_nulos_renda':1},{'prevalencia_alvo':0},{'n_entidades':-1}):
            with self.assertRaises(ValueError): self.f.base_tabular(**kwargs)
        with self.assertRaises(ValueError): self.f.serie_temporal(n_entidades=0)
        with self.assertRaises(ValueError): self.f.safras(safras_yyyymm=())
        with self.assertRaises(ValueError): self.f.fatos_e_features(pct_feature_futura=1)
    def test_temporal_panel(self):
        rows=self.f.serie_temporal(2,3,seed=42).orderBy('id_entidade','dt_referencia').collect()
        self.assertEqual(len(rows),6)
        self.assertEqual([r.dt_referencia.month for r in rows[:3]],[1,2,3])
        self.assertTrue(all(r.dt_referencia.year==2025 for r in rows))
    def test_temporal_versions_and_probability_denominator(self):
        facts,features=self.f.fatos_e_features(12,seed=42,pct_feature_futura=.99)
        decisions={r.id_cliente:r.dt_decisao for r in facts.collect()};rows=features.collect()
        self.assertEqual(len(decisions),12)
        self.assertEqual(sum(not r.eh_futura for r in rows),24)
        self.assertLessEqual(len(rows),36);self.assertGreaterEqual(len(rows),24)
        for r in rows:
            self.assertEqual(r.dt_referencia>decisions[r.id_cliente],r.eh_futura)
        self.assertNotIn('dt_publicacao',features.columns)
    def test_zero_decisions_returns_empty_typed_frames(self):
        f,a=self.f.fatos_e_features(0);self.assertEqual(f.count(),0);self.assertEqual(a.count(),0)
        self.assertEqual(f.columns,['id_cliente','dt_decisao','alvo'])
    def test_safra_accumulates_and_does_not_validate_dates(self):
        rows=self.f.safras(n_contratos=3,mob_maximo=6,safras_yyyymm=('nao-e-data',)).orderBy('id_contrato','mob').collect()
        self.assertEqual(len(rows),18)
        for c in range(3):
            group=rows[c*6:(c+1)*6];values=[r.inadimplente for r in group]
            self.assertEqual(values,sorted(values));self.assertEqual(group[0].safra,'nao-e-data')
    def test_fixture_readme_block(self):
        text=(HUB/'hub_snippets/testing/fixtures/README.md').read_text()
        block=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)[0]
        with contextlib.redirect_stdout(io.StringIO()) as out: exec(compile(block,'fixtures/README.md','exec'),{})
        self.assertEqual(out.getvalue().strip(),'20 5')
        print('README_SPARK',out.getvalue().strip())

if __name__=='__main__':
    require='--require-spark' in sys.argv
    if require: sys.argv.remove('--require-spark')
    if require and not HAS_SPARK: raise SystemExit('BLOQUEADO: --require-spark exige PySpark real.')
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print('R03A_RESULT',json.dumps({'python':sys.version.split()[0], 'tests':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'skips':len(result.skipped),
        'require_spark':require,'passed':result.testsRun-len(result.skipped)-len(result.errors)-len(result.failures)}))
    raise SystemExit(0 if result.wasSuccessful() and (not require or not result.skipped) else 1)
