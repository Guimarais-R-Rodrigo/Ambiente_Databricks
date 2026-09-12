"""Regressões do relatório: não duplicar skips nem esconder erros de execução."""
from __future__ import annotations
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import executar_baseline_visual as r

class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.base=self.root/'base'
    def tearDown(self):
        self.tmp.cleanup()
    def run_text(self,text):
        return r.executar([sys.executable,'-c','print('+repr(text)+')'],self.root,self.root,'teste',self.root,self.base)
    def test_skip_nao_conta_resumo_repetido(self):
        d,_=self.run_text('Ran 43 tests in 0.1s\nOK (skipped=7)\n   OK (0.1s) OK (skipped=7)')
        self.assertEqual(d['skips_reportados'],7)
    def test_total_casos_varias_suites(self):
        d,_=self.run_text('Ran 45 tests in 0.1s\nOK\nRan 43 tests in 0.1s\nOK (skipped=7)')
        self.assertEqual(d['testes_unittest_reportados'],88)
        self.assertEqual(d['skips_reportados'],7)
    def test_saida_sem_unittest_nao_inventa_casos(self):
        d,_=self.run_text('Verificação estrutural executada')
        self.assertEqual(d['testes_unittest_reportados'],0)
    def test_comando_valido_estado_e_hash(self):
        d,text=self.run_text('fixture')
        self.assertEqual(d['estado'],'PASS')
        self.assertEqual(d['log_sha256'],hashlib.sha256(text.encode()).hexdigest())
    def test_falha_de_processo_nao_vira_pass(self):
        d,_=r.executar([sys.executable,'-c','raise SystemExit(3)'],self.root,self.root,'falha',self.root,self.base)
        self.assertEqual((d['estado'],d['codigo']),('FAIL',3))
    def test_comando_ausente_bloqueia(self):
        d,_=r.executar([str(self.root/'nao_existe')],self.root,self.root,'ausente',self.root,self.base)
        self.assertEqual((d['estado'],d['codigo']),('BLOQUEADO',127))
    def test_timeout_bloqueia(self):
        with patch.object(r.subprocess,'run',side_effect=subprocess.TimeoutExpired('fixture',240)):
            d,_=r.executar(['fixture'],self.root,self.root,'timeout',self.root,self.base)
        self.assertEqual((d['estado'],d['codigo']),('BLOQUEADO',124))
    def test_caminhos_reais_sanitizados_no_log(self):
        _,text=self.run_text(str(self.root))
        self.assertNotIn(str(self.root),text)
        self.assertIn('<CANDIDATA>',text)

if __name__=='__main__':
    unittest.main(verbosity=2)
