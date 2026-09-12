"""Caracteriza os rótulos do wrapper existente; não corrige nem homologa o modelo.

Uso: python verificar_fechamento.py /caminho/do/repositorio
Dados sintéticos locais, logging desligado, nenhuma escrita no projeto.
"""
from pathlib import Path
import sys, traceback, unittest, json, platform
ROOT=Path(sys.argv.pop(1)).resolve()
sys.path.insert(0,str(ROOT/'ambiente_fonte/.assistant'))
import numpy as np
import xgboost
from hub_snippets.ml.train_xgboost import train_xgboost_baseline
print(json.dumps({'python':platform.python_version(),'xgboost':xgboost.__version__,'tipo':'caracterizacao_do_comportamento_atual','tracking':False}),flush=True)
class DominioRotulos(unittest.TestCase):
    def data(self):
        X=np.random.default_rng(12).normal(size=(45,3)); y=np.arange(45)%3
        return X[:30],y[:30],X[30:],y[30:]
    def executar(self,data,task):
        return train_xgboost_baseline(*data,task=task,params_override={'n_estimators':2,'max_depth':2,'n_jobs':1},early_stopping_rounds=0,log_mlflow=False)
    def test_tres_classes_passam_guarda_binary_e_falham_na_metrica(self):
        try:
            self.executar(self.data(),'binary')
        except ValueError as exc:
            frames=traceback.extract_tb(exc.__traceback__)
            self.assertIn('roc_auc_score',[f.name for f in frames])
            print('BINARY_3_CLASSES:',str(exc),'; etapa=roc_auc_score',flush=True)
        else:
            self.fail('O caminho esperado não produziu ValueError; rever documentação.')
    def test_multiclasse_rotulos_um_dois_tres_rejeitados(self):
        X,y,Xv,yv=self.data()
        with self.assertRaises(ValueError) as context:
            self.executar((X,y+1,Xv,yv+1),'multiclass')
        self.assertIn('Invalid classes inferred',str(context.exception))
        print('MULTICLASS_1_2_3:',str(context.exception),flush=True)
    def test_multiclasse_mapeamento_zero_um_dois_funciona(self):
        m,metrics=self.executar(self.data(),'multiclass')
        self.assertEqual(m.classes_.tolist(),[0,1,2])
        self.assertEqual(set(metrics),{'log_loss_val','accuracy_val'})
        self.assertTrue(all(np.isfinite(v) for v in metrics.values()))
        print('MULTICLASS_0_1_2:',json.dumps(metrics),flush=True)
if __name__=='__main__':
    unittest.main(verbosity=2)
