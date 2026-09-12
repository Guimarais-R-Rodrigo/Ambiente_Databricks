"""Testes suplementares R04-A: seis helpers Spark e blocos copiáveis dos READMEs."""
from __future__ import annotations
import argparse, io, re, sys, unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
ASSISTANT=ROOT/'ambiente_fonte/.assistant'
sys.path.insert(0,str(ASSISTANT))
OBJECTS=['date_features','join_diagnostics','null_summary','psi_calculator','safe_display','smart_sample']

try:
    from pyspark.sql import SparkSession, functions as F
    HAS_SPARK=True
except Exception:
    HAS_SPARK=False


def first_python_block(obj: str) -> str:
    text=(ASSISTANT/f'hub_snippets/spark/{obj}/README.md').read_text(encoding='utf-8')
    blocks=re.findall(r'```python\n(.*?)```',text,re.S)
    if not blocks:
        raise AssertionError(f'bloco Python ausente: {obj}')
    return blocks[0]


class StaticCases(unittest.TestCase):
    def test_six_readmes_have_contract_marker_and_links(self):
        for obj in OBJECTS:
            text=(ASSISTANT/f'hub_snippets/spark/{obj}/README.md').read_text()
            self.assertIn('<!-- readme-objeto: 1.0.0 -->',text)
            self.assertIn(f'[{"Implementação" if obj!="smart_sample" else "Implementação"}]({obj}.py)',text)
            self.assertIn(f'(exemplo_{obj}.py)',text)

    def test_notebooks_link_readme(self):
        for obj in OBJECTS:
            text=(ASSISTANT/f'hub_snippets/spark/{obj}/exemplo_{obj}.py').read_text()
            self.assertIn('[README.md](README.md)',text,obj)


@unittest.skipUnless(HAS_SPARK,'PySpark ausente: teste não executado')
class SparkCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark=(SparkSession.builder.master('local[2]').appName('R04A-synthetic')
                   .config('spark.ui.enabled','false')
                   .config('spark.sql.shuffle.partitions','2')
                   .getOrCreate())
        cls.spark.sparkContext.setLogLevel('ERROR')
        from hub_snippets.spark.date_features import extrair_features_data
        from hub_snippets.spark.join_diagnostics import diagnosticar_join
        from hub_snippets.spark.null_summary import null_summary
        from hub_snippets.spark.psi_calculator import calcular_psi,calcular_csi,interpretar_psi
        from hub_snippets.spark.safe_display import safe_display
        from hub_snippets.spark.smart_sample import smart_sample
        cls.date=staticmethod(extrair_features_data); cls.join=staticmethod(diagnosticar_join)
        cls.nulls=staticmethod(null_summary); cls.psi=staticmethod(calcular_psi)
        cls.csi=staticmethod(calcular_csi); cls.interpret=staticmethod(interpretar_psi)
        cls.show=staticmethod(safe_display); cls.sample=staticmethod(smart_sample)

    @classmethod
    def tearDownClass(cls): cls.spark.stop()

    def test_date_known_weekday_holiday_and_explicit_calendar(self):
        df=self.spark.createDataFrame([('2026-01-01',),('2026-02-17',),('2026-01-04',)],['dt'])
        rows={r['dt']:r.asDict() for r in self.date(df,'dt',holiday_dates=['2026-02-17']).collect()}
        self.assertTrue(rows['2026-01-01']['is_feriado_nacional_fixo'])
        self.assertFalse(rows['2026-01-01']['is_feriado_calendario'])
        self.assertTrue(rows['2026-02-17']['is_feriado_calendario'])
        self.assertEqual(rows['2026-01-04']['dia_semana_iso'],7); self.assertTrue(rows['2026-01-04']['is_fim_semana'])

    def test_date_prefix_and_malformed_input_characterized(self):
        valido=self.spark.createDataFrame([('2026-03-01',)],['dt'])
        row=self.date(valido,'dt',prefixo='x').first().asDict()
        self.assertIn('x_mes',row); self.assertEqual(row['x_mes'],3)
        invalido=self.spark.createDataFrame([('bad-date',)],['dt'])
        with self.assertRaises(Exception) as ctx:
            self.date(invalido,'dt',prefixo='x').first()
        self.assertIn('CAST_INVALID_INPUT',str(ctx.exception))

    def test_join_one_to_one_and_expansion(self):
        left=self.spark.createDataFrame([(1,),(2,)],['id'])
        right=self.spark.createDataFrame([(1,'a'),(2,'b')],['id','v'])
        d=self.join(left,right,'id'); self.assertEqual(d['expansao_prevista_left'],1.0); self.assertEqual(d['multiplicidade_max_direita'],1)
        right2=self.spark.createDataFrame([(1,'a'),(1,'b'),(2,'c'),(2,'d')],['id','v'])
        d2=self.join(left,right2,'id'); self.assertEqual(d2['linhas_apos_join_left'],4); self.assertEqual(d2['relacao'],'1:N — join duplica linhas da esquerda')

    def test_join_coverage_excludes_null_key(self):
        left=self.spark.createDataFrame([(1,),(None,)],'id long')
        right=self.spark.createDataFrame([(1,)],'id long')
        d=self.join(left,right,'id')
        self.assertEqual(d['cobertura_pct_chaves_validas'],100.0); self.assertEqual(d['chaves_nulas_esquerda'],1)
        self.assertEqual(d['linhas_apos_join_left'],2)

    def test_join_orphan_and_empty_convention(self):
        left=self.spark.createDataFrame([(1,),(2,)],['id']); right=self.spark.createDataFrame([(1,)],['id'])
        d=self.join(left,right,'id'); self.assertEqual(d['linhas_sem_match_chave_valida'],1); self.assertEqual(d['cobertura_pct_chaves_validas'],50.0)
        empty=self.spark.createDataFrame([], 'id long'); e=self.join(empty,right,'id')
        self.assertEqual(e['linhas_esquerda'],0); self.assertEqual(e['expansao_prevista_left'],1.0)

    def test_null_summary_counts_threshold_boundaries(self):
        df=self.spark.createDataFrame([(1,None),(2,2),(3,3),(4,4)],'id int,x int')
        rows={r['coluna']:r.asDict() for r in self.nulls(df,threshold_warn=25,threshold_fail=50).collect()}
        self.assertEqual(rows['x']['count_null'],1); self.assertEqual(rows['x']['pct_null'],25.0); self.assertEqual(rows['x']['status'],'🟡')
        red={r['coluna']:r.asDict() for r in self.nulls(df,threshold_warn=10,threshold_fail=25).collect()}
        self.assertEqual(red['x']['status'],'🔴')

    def test_null_summary_incoherent_thresholds_characterized(self):
        df=self.spark.createDataFrame([(1,None),(2,2)],'id int,x int')
        rows={r['coluna']:r.asDict() for r in self.nulls(df,threshold_warn=80,threshold_fail=20).collect()}
        self.assertEqual(rows['x']['status'],'🔴')  # fail é avaliado primeiro; helper não valida a política

    def test_psi_identical_zero_and_shift_positive(self):
        base=self.spark.createDataFrame([(float(i),) for i in range(1,101)],['x'])
        same=self.spark.createDataFrame([(float(i),) for i in range(1,101)],['x'])
        shift=self.spark.createDataFrame([(float(i+100),) for i in range(1,101)],['x'])
        self.assertAlmostEqual(self.psi(base,same,'x',10),0.0,places=6)
        self.assertGreater(self.psi(base,shift,'x',10),0.0)

    def test_psi_missing_shift_and_csi_categorical(self):
        base=self.spark.createDataFrame([(1.0,), (2.0,), (None,), (3.0,)],'x double')
        cur=self.spark.createDataFrame([(None,), (None,), (2.0,), (3.0,)],'x double')
        self.assertGreater(self.psi(base,cur,'x',4),0.0)
        b=self.spark.createDataFrame([('A',),('A',),('B',),(None,)],'c string')
        c=self.spark.createDataFrame([('A',),('B',),('B',),(None,)],'c string')
        self.assertGreater(self.csi(b,c,['c'])['c'],0.0)

    def test_csi_cardinality_guard_and_interpretation(self):
        b=self.spark.createDataFrame([('A',),('B',),('C',)],['c']); c=b
        with self.assertRaises(ValueError): self.csi(b,c,['c'],max_categorias=2)
        self.assertIn('política calibrada',self.interpret(0.2))
        self.assertIn('🟡',self.interpret(0.2,warning_threshold=.1,critical_threshold=.25))
        with self.assertRaises(ValueError): self.interpret(-0.1,warning_threshold=.1,critical_threshold=.25)

    def test_safe_display_limit_message_and_renderer(self):
        df=self.spark.range(5); captured=[]; out=io.StringIO()
        with redirect_stdout(out): self.show(df,limit=3,display_fn=lambda d: captured.append(d.count()))
        self.assertEqual(captured,[3]); self.assertIn('3+ rows',out.getvalue())
        with self.assertRaises(ValueError): self.show(df,limit=0,display_fn=lambda d:None)

    def test_safe_display_missing_renderer_raises(self):
        with self.assertRaises(RuntimeError): self.show(self.spark.range(2),limit=1)

    def test_smart_sample_small_returns_all_and_simple_bounded(self):
        small=self.spark.range(3); self.assertEqual(self.sample(small,n=5).count(),3)
        big=self.spark.range(1000); n=self.sample(big,n=50,seed=42).count(); self.assertLessEqual(n,50)

    def test_smart_sample_stratified_exact_and_preserves_strata(self):
        rows=[(i,'A' if i<90 else 'B') for i in range(100)]
        df=self.spark.createDataFrame(rows,['id','g']); out=self.sample(df,n=20,stratify_col='g',seed=7)
        self.assertEqual(out.count(),20); self.assertEqual(out.select('g').distinct().count(),2)

    def test_smart_sample_rejects_too_many_strata_and_bad_args(self):
        df=self.spark.createDataFrame([(i,str(i)) for i in range(10)],['id','g'])
        with self.assertRaises(ValueError): self.sample(df,n=5,stratify_col='g')
        with self.assertRaises(ValueError): self.sample(df,n=0)
        with self.assertRaises(ValueError): self.sample(df,n=5,stratify_col='missing')

    def test_readme_blocks_execute(self):
        df=self.spark.createDataFrame([('2026-01-01',1),('2026-02-17',2)],['dt_referencia','id'])
        fatos=self.spark.createDataFrame([(1,'2026-01'),(2,'2026-01')],['id_cliente','safra']); cadastro=self.spark.createDataFrame([(1,'2026-01'),(2,'2026-01')],['id_cliente','safra'])
        referencia=self.spark.createDataFrame([(1.0,),(2.0,),(3.0,)],['renda'])
        atual=self.spark.createDataFrame([(1.0,),(2.0,),(4.0,)],['renda'])
        df_smart=self.spark.createDataFrame([(1,'RJ'),(2,'SP'),(3,'RJ')],['id','uf'])
        def display(_): pass
        namespaces={
          'date_features':dict(df=df), 'join_diagnostics':dict(fatos=fatos,cadastro=cadastro),
          'null_summary':dict(df=df,display=display), 'psi_calculator':dict(referencia=referencia,atual=atual),
          'safe_display':dict(df=df,display=display), 'smart_sample':dict(df=df_smart),
        }
        for obj in OBJECTS:
            ns=namespaces[obj]
            exec(first_python_block(obj),ns,ns)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--require-spark',action='store_true'); args=parser.parse_args()
    if args.require_spark and not HAS_SPARK:
        raise SystemExit('PySpark obrigatório nesta execução')
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful(): raise SystemExit(1)
    if args.require_spark and result.skipped: raise SystemExit(f'skips inesperados: {result.skipped}')

if __name__=='__main__': main()
