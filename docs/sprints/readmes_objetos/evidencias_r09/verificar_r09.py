"""Casos R09: portáveis e MLflow, com dados sintéticos e sem skips silenciosos.

SQLite e artefatos são temporários; nenhum backend Databricks é consultado.
Dois testes MLflow simulam log_model explicitamente para flags/fallback.
"""
from __future__ import annotations
import argparse
import importlib
import math
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
OBJECTS = ('curves_plotly','drift_detection','metrics_report','mlflow_run','performance_monitor')


def code_example(obj):
    text=(ROOT/f'ambiente_fonte/.assistant/hub_snippets/ml/{obj}/README.md').read_text(encoding='utf-8')
    blocks=re.findall(r'```python\n(.*?)\n```',text,flags=re.S)
    if len(blocks)!=1:raise AssertionError(f'{obj}: exige exatamente um exemplo Python nesta suíte')
    return blocks[0]


class Portable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import numpy as np
        import pandas as pd
        cls.np,cls.pd=np,pd
        cls.m=importlib.import_module('hub_snippets.ml.metrics_report')
        cls.c=importlib.import_module('hub_snippets.ml.curves_plotly')
        cls.d=importlib.import_module('hub_snippets.ml.drift_detection')
        cls.p=importlib.import_module('hub_snippets.ml.performance_monitor')

    def test_01_perfect_and_reversed_metrics(self):
        good=self.m.calculate_binary_metrics([0,0,1,1],[.1,.2,.8,.9])
        bad=self.m.calculate_binary_metrics([0,0,1,1],[.9,.8,.2,.1])
        self.assertEqual(len(good),10)
        self.assertEqual((good['auc_roc'],good['ks_pct'],good['gini']),(1.,100.,1.))
        self.assertEqual((bad['auc_roc'],bad['ks_pct'],bad['gini']),(0.,100.,-1.))
        self.assertFalse(hasattr(self.m,'format_metrics_table'))

    def test_02_ap_brier_and_threshold_oracles(self):
        from sklearn.metrics import average_precision_score,brier_score_loss
        y=[0,1,0,1];p=[.1,.5,.6,.8]
        a=self.m.calculate_binary_metrics(y,p,threshold=.5)
        b=self.m.calculate_binary_metrics(y,p,threshold=.7)
        self.assertEqual(a['auc_pr'],round(average_precision_score(y,p),4))
        self.assertEqual(a['brier_score'],round(brier_score_loss(y,p),4))
        self.assertEqual(a['recall'],1.)
        self.assertEqual(b['recall'],.5)
        self.assertEqual(a['auc_roc'],b['auc_roc'])

    def test_03_invalid_binary_inputs(self):
        cases=[([],[]),([0,0],[.1,.2]),([0,1],[.1,float('nan')]),([0,1],[.1,2.]),([[0,1]],[[.1,.9]]),([0,1],[.1])]
        for y,p in cases:
            with self.subTest(y=y),self.assertRaises(ValueError):self.m.calculate_binary_metrics(y,p)
        with self.assertRaises(ValueError):self.m.calculate_binary_metrics([0,1],[.1,.9],threshold=2.)

    def test_04_regression_zero_target_policy(self):
        r=self.m.calculate_regression_metrics([0,2,4],[99,1,5])
        self.assertEqual(r['mape'],37.5)
        self.assertTrue(math.isnan(self.m.calculate_regression_metrics([0,0],[1,2])['mape']))
        with self.assertRaises(ValueError):self.m.calculate_regression_metrics([1,2],[1,float('inf')])

    def test_05_small_population_lift_ceil(self):
        y=[1]+[0]*10;p=[.99]+list(self.np.linspace(.1,.8,10))
        self.assertEqual(self.m.calculate_binary_metrics(y,p)['lift_10pct'],5.5)
        f=self.c.plot_lift_curve(y,p,n_bins=10)
        self.assertAlmostEqual(float(f.data[0].y[0]),5.5)
        self.assertAlmostEqual(float(f.data[0].y[-1]),1.)

    def test_06_four_figures_and_lift_grid(self):
        import plotly.graph_objects as go
        y=[0,1]*10;p=self.np.linspace(.05,.95,20)
        for fun in (self.c.plot_roc_curve,self.c.plot_pr_curve,self.c.plot_ks_curve,self.c.plot_lift_curve):
            self.assertIsInstance(fun(y,p),go.Figure)
        f=self.c.plot_lift_curve(y,p,n_bins=4)
        self.np.testing.assert_array_equal(f.data[0].x,[25,50,75,100])
        self.assertTrue(any('top-25%' in a.text for a in f.layout.annotations))
        with self.assertRaises(ValueError):self.c.plot_lift_curve(y,p,n_bins=21)

    def test_07_ks_is_directional_not_bilateral(self):
        y=[0,0,1,1];p=[.9,.8,.2,.1]
        f=self.c.plot_ks_curve(y,p)
        self.assertTrue(any('KS = 0.0000' in a.text for a in f.layout.annotations))
        self.assertEqual(self.m.calculate_binary_metrics(y,p)['ks_pct'],100.)

    def test_08_n_is_text_and_auc_flag_partial(self):
        y=[0,1,0,1];p=[.1,.8,.3,.6]
        a=self.c.plot_roc_curve(y,p,n=4);b=self.c.plot_roc_curve(y,p,n=999,show_auc=False)
        self.np.testing.assert_array_equal(a.data[0].x,b.data[0].x)
        self.np.testing.assert_array_equal(a.data[0].y,b.data[0].y)
        self.assertIn('AUC',b.data[0].name)
        self.assertTrue(any('999' in x.text and 'AUC' in x.text for x in b.layout.annotations))
        self.assertEqual(len(a.layout.annotations),len(b.layout.annotations)+1)

    def test_09_drift_identity_and_out_of_range(self):
        x=self.np.arange(20,dtype=float)
        self.assertEqual(self.d.calculate_psi(x,x),0.)
        self.assertEqual(self.d.calculate_ks(x,x),(0.,1.))
        self.assertGreater(self.d.calculate_psi(x,x+100),0.)

    def test_10_psi_missing_and_infinity(self):
        a=self.np.array([0.,1.,2.,3.,self.np.nan]);b=self.np.array([0.,1.,2.,3.,self.np.nan,self.np.nan])
        self.assertGreater(self.d.calculate_psi(a,b),0.)
        with self.assertRaises(ValueError):self.d.calculate_psi([0.,1.],[self.np.nan])
        with self.assertRaises(ValueError):self.d.calculate_psi([0.,1.],[1.,self.np.inf])
        self.assertEqual(self.d.calculate_ks([0,1,self.np.inf],[0,1]),(0.,1.))

    def test_11_csi_missing_sentinel_collision(self):
        a=self.pd.Series(['A',None]);b=self.pd.Series(['A','__MISSING__'])
        self.assertEqual(self.d.calculate_csi(a,b),0.)
        self.assertGreater(self.d.calculate_csi(a,self.pd.Series(['B','B'])),0.)

    def test_12_drift_policy_and_insufficient(self):
        a=self.pd.DataFrame({'x':range(20),'g':['A']*20});b=self.pd.DataFrame({'x':range(100,120),'g':['B']*20})
        r=self.d.detect_drift_all_features(a,b,['x','g'])
        self.assertEqual(set(r.status),{'NOT_CLASSIFIED'})
        r=self.d.detect_drift_all_features(a,b,['x','g'],psi_threshold=.1,ks_threshold=.2,severe_psi_threshold=.5)
        self.assertEqual(set(r.status),{'SEVERE'})
        with self.assertRaises(ValueError):self.d.detect_drift_all_features(a,b,['x'],psi_threshold=.1)
        r=self.d.detect_drift_all_features(a.head(2),b.head(2),['x','g'])
        self.assertEqual(set(r.status),{'INSUFFICIENT_DATA'})

    def test_13_categorical_minimum_is_row_count(self):
        a=self.pd.DataFrame({'g':[None]*10})
        r=self.d.detect_drift_all_features(a,a,['g'])
        self.assertEqual(r.status.iloc[0],'NOT_CLASSIFIED')
        self.assertTrue(self.pd.isna(r.reference_n.iloc[0]))
        self.assertEqual(float(r.psi.iloc[0]),0.)

    def test_14_coercion_missing_and_explicit_list_limits(self):
        a=self.pd.DataFrame({'x':[str(i) for i in range(10)]+['bad'],'outside':range(11)})
        r=self.d.detect_drift_all_features(a,a,['x'],numeric_cols=['x'])
        self.assertEqual(int(r.reference_n.iloc[0]),10)
        self.assertEqual(float(r.reference_missing_pct.iloc[0]),0.)
        r=self.d.detect_drift_all_features(a,a,['x'],numeric_cols=['outside'],categorical_cols=['x'])
        self.assertIn('outside',set(r.feature))

    def test_15_threshold_validation_not_complete(self):
        a=self.pd.DataFrame({'x':range(12)})
        r=self.d.detect_drift_all_features(a,a,['x'],psi_threshold=-1,ks_threshold=-1)
        self.assertEqual(r.status.iloc[0],'ALERT')

    def test_16_metric_alias_selection_and_conflict(self):
        f=self.p.selecionar_metricas_do_relatorio
        r=f({'auc_roc':.78,'ks_pct':40.,'auc_pr':.2},metricas_obrigatorias=['auc','ks_pct'])
        self.assertEqual(r,{'auc':.78,'ks_pct':40.})
        for report in ({'auc_roc':.7,'auc':.8},{'auc_roc':True},{'auc_pr':.2}):
            with self.assertRaises(ValueError):f(report)
        with self.assertRaises(ValueError):f({'ks_pct':40.},metricas_obrigatorias=['auc'])

    def test_17_monitor_absolute_relative_and_improvement(self):
        policy={'auc':{'warning':.03,'critical':.05,'direction':'higher','delta':'absolute'},'rmse':{'warning':.1,'critical':.2,'direction':'lower','delta':'relative'}}
        m=self.p.PerformanceMonitor({'auc':.78,'rmse':100.},policy=policy)
        m.add_period('A',{'auc':.7,'rmse':115.},n_predictions=1)
        self.assertAlmostEqual(m.history[-1]['auc_delta'],.08)
        self.assertAlmostEqual(m.history[-1]['rmse_delta'],.15)
        self.assertEqual(m.get_current_status(),'🔴 Crítico')
        self.assertFalse(m.should_retrain()['automatic_retrain_authorized'])
        m.add_period('B',{'auc':.8,'rmse':90.})
        self.assertEqual(m.get_current_status(),'🟢 Saudável')
        f=m.plot_timeline('rmse')
        self.np.testing.assert_allclose([s.y0 for s in f.layout.shapes],[100.,110.,120.])

    def test_18_monitor_complete_and_invalid(self):
        with self.assertRaises(ValueError):self.p.PerformanceMonitor({'rmse':0.})
        with self.assertRaises(ValueError):self.p.PerformanceMonitor({'auc':True})
        m=self.p.PerformanceMonitor({'auc':.78,'ks_pct':40.})
        with self.assertRaises(ValueError):m.add_period('A',{'auc':.7})
        with self.assertRaises(ValueError):m.add_period('A',{'auc':.7,'ks_pct':35.},n_predictions=True)
        m=self.p.PerformanceMonitor({'auc':.78,'ks_pct':40.},require_complete_metrics=False)
        m.add_period('A',{'auc':.7})
        self.assertEqual(m.get_current_status(),'⚪ Incompleto')
        self.assertEqual(m.should_retrain()['decision'],'INVESTIGATE_RETRAINING_CANDIDATE')

    def test_19_monitor_counts_insertions_not_dates(self):
        policy={'auc':{'warning':.05,'critical':.2,'direction':'higher','delta':'absolute'}}
        m=self.p.PerformanceMonitor({'auc':.8},policy=policy,consecutive_alert_periods=3)
        for _ in range(3):m.add_period('same-period',{'auc':.7})
        self.assertEqual(len(m.history),3)
        self.assertEqual(m.should_retrain()['consecutive_alert_periods'],3)
        self.assertEqual(m.should_retrain()['decision'],'INVESTIGATE_RETRAINING_CANDIDATE')

    def test_20_example_policy_source_not_approval(self):
        m=self.p.PerformanceMonitor({'auc':.78},policy=self.p.EXAMPLE_THRESHOLDS)
        m.add_period('A',{'auc':.78})
        self.assertEqual(m.should_retrain()['policy_source'],'caller-provided')
        self.assertEqual(self.p.PerformanceMonitor({'auc':.78}).get_current_status(),'⚪ Sem dados')
        self.assertIn('NO_EVIDENCE',self.p.PerformanceMonitor({'auc':.78}).generate_report())

    def test_21_readme_examples_portable(self):
        for obj in OBJECTS:
            if obj=='mlflow_run':continue
            with self.subTest(obj=obj):exec(compile(code_example(obj),f'{obj}/README.md','exec'),{})


class MlflowReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import mlflow
        import mlflow.sklearn
        import pandas as pd
        from sklearn.linear_model import LogisticRegression
        from mlflow.tracking import MlflowClient
        cls.ml=mlflow;cls.client_class=MlflowClient
        cls.api=importlib.import_module('hub_snippets.ml.mlflow_run.mlflow_run')
        cls.tmp=tempfile.TemporaryDirectory(prefix='r09-mlflow-')
        cls.old_tracking=mlflow.get_tracking_uri();cls.old_registry=mlflow.get_registry_uri()
        uri='sqlite:///'+str(Path(cls.tmp.name)/'tracking.db')
        mlflow.set_tracking_uri(uri);mlflow.set_registry_uri(uri)
        cls.experiment=mlflow.create_experiment('r09-synthetic',artifact_location=(Path(cls.tmp.name)/'artifacts').as_uri())
        mlflow.set_experiment(experiment_id=cls.experiment)
        cls.X=pd.DataFrame({'x':[-3.,-2.,-1.,1.,2.,3.]})
        cls.model=LogisticRegression().fit(cls.X,[0,0,0,1,1,1])
        cls.kw={'dataset':'synthetic fixture','split':'demonstration, no evaluation','limitacoes':['synthetic only']}

    def tearDown(self):
        if self.ml.active_run():self.ml.end_run(status='FAILED')

    @classmethod
    def tearDownClass(cls):
        cls.ml.set_tracking_uri(cls.old_tracking);cls.ml.set_registry_uri(cls.old_registry)
        cls.tmp.cleanup()

    def test_01_complete_run_readme_and_signature(self):
        ns={};exec(compile(code_example('mlflow_run'),'mlflow_run/README.md','exec'),ns)
        run=self.ml.get_run(ns['run_id'])
        self.assertEqual(run.info.status,'FINISHED')
        self.assertEqual(run.data.params['algoritmo'],'logistic_regression')
        models=self.ml.search_logged_models(experiment_ids=[self.experiment],output_format='list')
        model=[x for x in models if x.source_run_id==ns['run_id']][0]
        info=self.ml.models.get_model_info(model.model_uri)
        self.assertIsNotNone(info.signature)
        loaded=self.ml.sklearn.load_model(model.model_uri)
        self.assertEqual(list(loaded.predict(ns['X'])),list(ns['modelo'].predict(ns['X'])))
        self.assertEqual(ns['registro'].pendencias(),[])

    def test_02_incomplete_keeps_partial_logs(self):
        with self.assertRaisesRegex(ValueError,'run incompleto'):
            with self.api.run_governado('incomplete',**self.kw) as r:
                rid=self.ml.active_run().info.run_id;r.parametros({'stage':'partial'})
        run=self.ml.get_run(rid)
        self.assertEqual(run.info.status,'FAILED')
        self.assertEqual(run.data.params['stage'],'partial')

    def test_03_body_exception_propagates_and_keeps_logs(self):
        with self.assertRaisesRegex(RuntimeError,'synthetic failure'):
            with self.api.run_governado('raises',**self.kw) as r:
                rid=self.ml.active_run().info.run_id;r.parametros({'stage':'before-exception'})
                raise RuntimeError('synthetic failure')
        self.assertEqual(self.ml.get_run(rid).info.status,'FAILED')
        self.assertEqual(self.ml.get_run(rid).data.params['stage'],'before-exception')

    def test_04_active_outer_run_is_not_closed(self):
        with self.ml.start_run(run_name='outer') as outer:
            with self.assertRaisesRegex(Exception,'already active'):
                with self.api.run_governado('inner',**self.kw):pass
            self.assertEqual(self.ml.active_run().info.run_id,outer.info.run_id)

    def test_05_exigir_false_is_not_completeness(self):
        with self.api.run_governado('relaxed',exigir_completo=False,**self.kw) as r:
            rid=self.ml.active_run().info.run_id
            self.assertEqual(len(r.pendencias()),3)
        self.assertEqual(self.ml.get_run(rid).info.status,'FINISHED')
        with self.assertRaises(ValueError):
            with self.api.run_governado('empty',dataset=' ',split='x',limitacoes=['x']):pass

    def test_06_local_signature_flag_is_not_artifact_inspection(self):
        # Deliberate mock: local flag, not a successfully logged real model.
        with self.api.run_governado('flag-only',**self.kw) as r:
            r.parametros({'x':1});r.metricas({'m':1.})
            with patch.object(self.ml.sklearn,'log_model',return_value=None) as mocked:
                r.modelo(self.model,exemplo_entrada=self.X.iloc[:2])
            self.assertEqual(r.pendencias(),[])
            self.assertEqual(mocked.call_count,1)

    def test_07_fallback_for_typeerror_is_broad(self):
        # Deliberate mock: dispatch, not universal MLflow-version compatibility.
        with self.api.run_governado('fallback',**self.kw) as r:
            r.parametros({'x':1});r.metricas({'m':1.})
            with patch.object(self.ml.sklearn,'log_model',side_effect=[TypeError('fixture'),None]) as mocked:
                r.modelo(self.model,exemplo_entrada=self.X.iloc[:2])
            self.assertIn('artifact_path',mocked.call_args_list[0].kwargs)
            self.assertIn('name',mocked.call_args_list[1].kwargs)

    def test_08_extra_artifact_and_no_snapshot(self):
        p=Path(self.tmp.name)/'synthetic.txt';p.write_text('synthetic only',encoding='utf-8')
        with self.api.run_governado('artifact',exigir_completo=False,**self.kw) as r:
            rid=self.ml.active_run().info.run_id;r.artefato(str(p))
            self.assertEqual(len(r.pendencias()),3)
        self.assertTrue(any(a.path=='synthetic.txt' for a in self.client_class().list_artifacts(rid)))
        self.assertEqual(self.ml.get_run(rid).data.tags['dataset'],'synthetic fixture')


def main():
    global ROOT
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--group',choices=['portable','mlflow','all'],default='portable')
    args=ap.parse_args();ROOT=args.root.resolve()
    sys.path.insert(0,str(ROOT/'ambiente_fonte/.assistant'))
    suite=unittest.TestSuite();loader=unittest.TestLoader()
    selected=[Portable] if args.group=='portable' else [MlflowReal] if args.group=='mlflow' else [Portable,MlflowReal]
    for cls in selected:suite.addTests(loader.loadTestsFromTestCase(cls))
    result=unittest.TextTestRunner(verbosity=2,stream=sys.stdout).run(suite)
    expected=21 if args.group=='portable' else 8 if args.group=='mlflow' else 29
    if result.testsRun!=expected or result.skipped or not result.wasSuccessful():raise SystemExit(1)
    print(f'R09_GROUP_PASS: {args.group}; cases={result.testsRun}; skips=0')


if __name__=='__main__':main()
