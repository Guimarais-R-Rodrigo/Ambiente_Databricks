"""Checks R02 sobre dados sintéticos; --require-all recusa dependências ausentes.

Não executa notebooks de instalação, escrita persistente ou interação Genie Code.
Ausências locais geram skips explícitos; não são usadas bibliotecas simuladas.
"""
from __future__ import annotations
import importlib.util, importlib.metadata, json, platform, re, sys, unittest
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'ambiente_fonte/.assistant'))
AVAILABLE={n:importlib.util.find_spec(n) is not None for n in ('numpy','pandas','sklearn','xgboost','mlflow','pyspark')}
if '--require-all' in sys.argv and not all(AVAILABLE.values()):
    raise SystemExit('Dependências ausentes: '+str(AVAILABLE))
versions={}
for n,present in AVAILABLE.items():
    if present:
        module=__import__(n)
        versions[n]=getattr(module,'__version__','presente')
    else:versions[n]=None
print('AMBIENTE',json.dumps({'python':platform.python_version(),'pacotes':versions},ensure_ascii=False),flush=True)

class Formato(unittest.TestCase):
    def test_bloco_readme_real(self):
        p=ROOT/'ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md'
        blocks=re.findall(r'```python\n(.*?)```',p.read_text(encoding='utf-8'),re.S)
        self.assertEqual(len(blocks),1)
        exec(compile(blocks[0],str(p),'exec'),{})
    def test_escalas_e_bordas(self):
        from hub_snippets.constants.format_br import fmt_pct,fmt_int,fmt_brl,fmt_delta,fmt_n
        self.assertEqual(fmt_int(-12.9),'-12');self.assertEqual(fmt_brl(-1.995),'-R$ 2,00')
        self.assertEqual(fmt_pct(92.8),'9280,0%')
        with self.assertRaises(ValueError):fmt_pct(1,input_scale='incorreta')
        self.assertEqual(fmt_delta(.0005,'bps'),'+5 bps')
        self.assertEqual(fmt_delta(.032,'erro_de_digitacao'),'+3,2 pp')
        self.assertEqual(fmt_n(999999),'1000,0k')
    def test_limite_inteiro_grande(self):
        """Caracteriza limitação conhecida; não aprova o comportamento como ideal."""
        from hub_snippets.constants.format_br import fmt_int,fmt_n
        for fn in (fmt_int,lambda v:fmt_n(v,False)):
            r=fn(9007199254740993)
            self.assertEqual(r,'9.007.199.254.740.992')
            self.assertNotEqual(r.replace('.',''),'9007199254740993')
        print('LIMITE: 9007199254740993 perde uma unidade em fmt_int e fmt_n.')

@unittest.skipUnless(all(AVAILABLE[x] for x in ('numpy','sklearn','xgboost')),'Dependências XGBoost ausentes')
class XGBoost(unittest.TestCase):
    def data(self,task):
        import numpy as np
        X=np.random.default_rng(27).normal(size=(90,4))
        y=np.arange(90)%(3 if task=='multiclass' else 2)
        if task=='regression':y=2*X[:,0]-.7*X[:,1]
        return X[:60],y[:60],X[60:],y[60:]
    def train(self,task):
        from hub_snippets.ml.train_xgboost import train_xgboost_baseline
        return train_xgboost_baseline(*self.data(task),task=task,params_override={'n_estimators':8,'max_depth':2,'n_jobs':1},early_stopping_rounds=3,log_mlflow=False)
    def test_binary(self):
        from sklearn.metrics import roc_auc_score
        m,d=self.train('binary');_,_,X,y=self.data('binary')
        self.assertEqual(set(d),{'auc_val','gini_val'})
        self.assertAlmostEqual(d['auc_val'],roc_auc_score(y,m.predict_proba(X)[:,1]))
        self.assertAlmostEqual(d['gini_val'],2*d['auc_val']-1)
    def test_multiclass(self):
        import numpy as np
        m,d=self.train('multiclass')
        self.assertEqual(set(d),{'log_loss_val','accuracy_val'})
        self.assertTrue(all(np.isfinite(v) for v in d.values()))
        self.assertEqual(m.predict_proba(self.data('multiclass')[2]).shape,(30,3))
    def test_regression(self):
        import numpy as np
        m,d=self.train('regression');_,_,X,y=self.data('regression')
        self.assertEqual(set(d),{'rmse_val'})
        self.assertAlmostEqual(d['rmse_val'],float(np.sqrt(np.mean((y-m.predict(X))**2))))
    def test_recusas(self):
        import numpy as np
        from hub_snippets.ml.train_xgboost import train_xgboost_baseline
        X,y,Xv,yv=self.data('binary')
        with self.assertRaises(ValueError):train_xgboost_baseline(X,y,Xv,yv,task='ranking',log_mlflow=False)
        with self.assertRaises(ValueError):train_xgboost_baseline(X,y,Xv,np.zeros(len(yv)),log_mlflow=False)
        with self.assertRaises(ValueError):train_xgboost_baseline(X,y,Xv,yv,early_stopping_rounds=-1,log_mlflow=False)

@unittest.skipUnless(all(AVAILABLE[x] for x in ('numpy','pandas','sklearn','mlflow')),'MLflow real ou dependências Isolation Forest ausentes; nenhum mock')
class Isolamento(unittest.TestCase):
    def test_contrato_e_perfil(self):
        import numpy as np,pandas as pd
        from hub_snippets.ml.isolation_forest import train_isolation_forest,profile_anomalies
        df=pd.DataFrame(np.random.default_rng(4).normal(size=(80,2)),columns=['a','b'])
        r=train_isolation_forest(df,['a','b'],contamination=.1,n_estimators=12,log_mlflow=False)
        self.assertEqual(set(r),{'scores','labels','model','stats','scaler'})
        self.assertTrue(np.array_equal(r['labels']==-1,r['scores']<0))
        self.assertAlmostEqual(r['stats']['score_threshold'],round(float(np.percentile(r['scores'],10)),4))
        prof=profile_anomalies(df,['a','b'],r['scores'],r['labels'],top_n=3)
        self.assertEqual(list(prof.columns),['index','anomaly_score','most_anomalous_feature','max_z_score'])
        self.assertTrue(prof['anomaly_score'].is_monotonic_increasing)
    def test_empates_nao_garantem_fracao(self):
        import numpy as np,pandas as pd
        from hub_snippets.ml.isolation_forest import train_isolation_forest
        df=pd.DataFrame(np.zeros((40,2)),columns=['a','b'])
        r=train_isolation_forest(df,['a','b'],contamination=.1,n_estimators=10,log_mlflow=False)
        self.assertEqual(int((r['labels']==-1).sum()),0)
        print('EMPATES: 40 pontos idênticos com contamination=.1 -> zero rótulos -1.')
    def test_auto_nao_suportado(self):
        import numpy as np,pandas as pd
        from hub_snippets.ml.isolation_forest import train_isolation_forest
        with self.assertRaises((TypeError,ValueError)):
            train_isolation_forest(pd.DataFrame({'a':np.arange(20.)}),['a'],contamination='auto',n_estimators=5,log_mlflow=False)

@unittest.skipUnless(AVAILABLE['pyspark'],'PySpark ausente; sem teste de sessão local')
class SparkSintetico(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from pyspark.sql import SparkSession
        cls.spark=(SparkSession.builder.master('local[2]').appName('r02-sintetico').config('spark.sql.shuffle.partitions','2').config('spark.sql.session.timeZone','UTC').config('spark.ui.enabled','false').getOrCreate())
        cls.spark.sparkContext.setLogLevel('ERROR')
    @classmethod
    def tearDownClass(cls):cls.spark.stop()
    def test_pit_cobertura_e_duplicata(self):
        from hub_snippets.spark.pit_join import pit_join
        s=self.spark
        f=s.createDataFrame([('a',date(2026,1,10),1),('a',date(2026,1,10),2),('b',date(2026,1,10),3),('c',date(2026,1,10),4),(None,date(2026,1,10),5)],'id string, decisao date, seq int')
        h=s.createDataFrame([('a',date(2026,1,5),10.),('a',date(2026,1,9),90.),('c',date(2026,1,20),20.)],'id string, referencia date, score double')
        o,d=pit_join(f,h,'id','decisao','referencia',atraso_publicacao_dias=2,colunas_feature=['score'],devolver_disponibilidade=True)
        rows={r.seq:r.asDict() for r in o.collect()}
        self.assertEqual(len(rows),5);self.assertEqual(rows[1]['score'],10.);self.assertEqual(rows[2]['score'],10.)
        self.assertEqual((d['com_feature'],d['sem_chave_ou_data'],d['entidade_sem_historico'],d['sem_feature_disponivel_na_data']),(2,1,1,1))
        self.assertEqual(d['cobertura_pct_linhas_validas'],50.)
    def test_pit_empate_e_janela(self):
        from hub_snippets.spark.pit_join import pit_join
        s=self.spark
        f=s.createDataFrame([('a',date(2026,1,10))],'id string, decisao date')
        h=s.createDataFrame([('a',date(2026,1,5),10.),('a',date(2026,1,5),20.)],'id string, referencia date, score double')
        with self.assertRaises(ValueError):pit_join(f,h,'id','decisao','referencia',atraso_publicacao_dias=2)
        o,d=pit_join(f,h,'id','decisao','referencia',atraso_publicacao_dias=2,politica_empate='menor')
        self.assertEqual(o.first().score,10.)
        _,d=pit_join(f,h,'id','decisao','referencia',atraso_publicacao_dias=2,janela_maxima_dias=4)
        self.assertEqual(d['com_feature'],0)
    def test_quick_profile_contrato_e_vazio(self):
        from hub_scripts.quick_profile import quick_profile
        s=self.spark
        df=s.createDataFrame([('a',1.,date(2026,1,1)),('a',None,date(2026,1,2)),('b',3.,date(2026,1,3)),(None,4.,None)],'grupo string, valor double, dia date')
        name='vw_r02_perfil_sintetico';df.createOrReplaceTempView(name)
        try:
            r=quick_profile(name,sample_fraction=1,max_categories=20,seed=42)
            self.assertEqual((r['total_rows'],r['sample_rows'],r['total_columns']),(4,4,3))
            self.assertEqual({i['column']:i['null_count'] for i in r['null_summary_full_table']},{'grupo':1,'valor':1,'dia':1})
            self.assertAlmostEqual(r['numeric_summary_sample']['valor']['mean'],8/3)
            self.assertEqual(r['date_range_sample']['dia']['max'],date(2026,1,3))
            self.assertEqual(sum(i['count'] for i in r['top_values_sample']['grupo']),4)
            with self.assertRaises(ValueError):quick_profile(name,sample_fraction=0)
            df.limit(0).createOrReplaceTempView(name)
            r=quick_profile(name,sample_fraction=1)
            self.assertEqual(r['total_rows'],0);self.assertTrue(all(i['null_pct']==0 for i in r['null_summary_full_table']))
        finally:s.catalog.dropTempView(name)

if __name__=='__main__':
    r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    print('RESUMO_R02',json.dumps({'casos':r.testsRun,'falhas':len(r.failures),'erros':len(r.errors),'pulados':len(r.skipped),'sucesso':r.wasSuccessful()},ensure_ascii=False))
    sys.exit(0 if r.wasSuccessful() else 1)
