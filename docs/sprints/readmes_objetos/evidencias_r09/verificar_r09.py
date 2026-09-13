"""Caracterização R09: contratos documentais e runtime dos cinco objetos."""
from __future__ import annotations
import argparse, json, math, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
ASSISTANT = ROOT / "ambiente_fonte/.assistant"
sys.path.insert(0, str(ASSISTANT))
OBJECTS = ["curves_plotly", "drift_detection", "metrics_report", "mlflow_run", "performance_monitor"]
SECTIONS = [f"## {i}. " for i in range(1, 16)]

class StaticCases(unittest.TestCase):
    def test_readme_contract_and_coverage(self):
        for obj in OBJECTS:
            text=(ASSISTANT/f"hub_snippets/ml/{obj}/README.md").read_text(encoding="utf-8")
            self.assertIn("<!-- readme-objeto: 1.0.0 -->", text)
            pos=[]
            for prefix in SECTIONS:
                p=text.find(prefix); self.assertGreaterEqual(p,0,(obj,prefix)); pos.append(p)
            self.assertEqual(pos, sorted(pos), obj)
        data=json.loads((ROOT/"docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json").read_text(encoding="utf-8"))
        for obj in OBJECTS: self.assertNotIn(f"hub_snippets/ml/{obj}", data["pending"])
        idx=(ROOT/"docs/sprints/readmes_objetos/README.md").read_text(encoding="utf-8")
        self.assertIn("60/75 operacionais", idx); self.assertIn("15 pendências", idx)

    def test_backlinks_and_erratas(self):
        expected={
            "curves_plotly":"**não subamostra**",
            "drift_detection":"min_non_null",
            "metrics_report":"escala 0–100",
            "mlflow_run":"observação histórica deste runtime",
            "performance_monitor":"automatic_retrain_authorized",
        }
        for obj, marker in expected.items():
            text=(ASSISTANT/f"hub_snippets/ml/{obj}/exemplo_{obj}.py").read_text(encoding="utf-8")
            self.assertIn("Guia local completo:", text, obj)
            self.assertIn(marker, text, obj)

class CoreCases(unittest.TestCase):
    def test_curves_metrics_drift_and_monitor(self):
        import numpy as np, pandas as pd
        from hub_snippets.ml.curves_plotly import plot_roc_curve, plot_lift_curve
        from hub_snippets.ml.metrics_report import calculate_binary_metrics, calculate_regression_metrics
        from hub_snippets.ml.drift_detection import detect_drift_all_features
        from hub_snippets.ml.performance_monitor import PerformanceMonitor, selecionar_metricas_do_relatorio
        y=np.array([0,0,1,1,0,1]); p=np.array([.1,.2,.7,.9,.3,.8])
        roc=plot_roc_curve(y,p,n=999)
        self.assertTrue(any("999" in str(a.text) for a in roc.layout.annotations))
        fpr=np.asarray(roc.data[0].x,dtype=float)
        self.assertTrue(np.all(np.diff(fpr)>=0)); self.assertGreaterEqual(float(fpr.min()),0.0); self.assertLessEqual(float(fpr.max()),1.0)
        lift=plot_lift_curve(y,p,n_bins=3); self.assertEqual(len(lift.data[0].x),3)
        m=calculate_binary_metrics(y,p); self.assertGreater(m["ks_pct"],1); self.assertIn("auc_roc",m)
        r=calculate_regression_metrics(np.array([0.,0.]),np.array([1.,2.])); self.assertTrue(math.isnan(r["mape"]))
        ref=pd.DataFrame({"x":range(20),"cat":[None]*20}); cur=pd.DataFrame({"x":range(1,21),"cat":[None]*20})
        out=detect_drift_all_features(ref,cur,["x","cat"],numeric_cols=["x"],categorical_cols=["cat"],min_non_null=10)
        cat=out.loc[out.feature=="cat"].iloc[0]
        self.assertEqual(cat["status"],"NOT_CLASSIFIED")
        self.assertTrue(math.isfinite(float(cat["psi"])))
        selected=selecionar_metricas_do_relatorio(m, metricas_obrigatorias=["auc","ks_pct"])
        self.assertIn("auc",selected); self.assertIn("ks_pct",selected)
        policy={"auc":{"warning":.03,"critical":.05,"direction":"higher","delta":"absolute"}}
        mon=PerformanceMonitor({"auc":.8},policy=policy,consecutive_alert_periods=2)
        mon.add_period("a",{"auc":.76}); mon.add_period("b",{"auc":.75})
        decision=mon.should_retrain(); self.assertFalse(decision["automatic_retrain_authorized"]); self.assertEqual(decision["decision"],"INVESTIGATE_RETRAINING_CANDIDATE")

class MlflowCases(unittest.TestCase):
    def test_governed_run_with_local_tracking(self):
        import mlflow
        from sklearn.linear_model import LogisticRegression
        import numpy as np
        from hub_snippets.ml.mlflow_run import run_governado
        with tempfile.TemporaryDirectory() as td:
            mlflow.set_tracking_uri(f"sqlite:///{Path(td) / 'mlflow.db'}")
            X=np.array([[0.],[1.],[2.],[3.]]); y=np.array([0,0,1,1]); model=LogisticRegression().fit(X,y)
            with run_governado("r09",dataset="fixture",split="fixture",limitacoes=["fixture"]) as run:
                run.parametros({"c":1}); run.metricas({"auc":.9}); run.modelo(model,exemplo_entrada=X[:1])
            with self.assertRaises(ValueError):
                with run_governado("incompleto",dataset="fixture",split="fixture",limitacoes=["fixture"]): pass

GROUPS={"static":StaticCases,"core":CoreCases,"mlflow":MlflowCases}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--group",choices=GROUPS,default="static"); args=ap.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(GROUPS[args.group]))
    if not result.wasSuccessful() or result.skipped: raise SystemExit(1)
if __name__=="__main__": main()
