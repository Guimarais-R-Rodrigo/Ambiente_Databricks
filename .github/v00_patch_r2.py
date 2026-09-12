"""Preparação restrita da segunda rodada V00; removida da árvore final."""
from pathlib import Path
import re, subprocess, sys

p=Path('tools/executar_baseline_visual.py')
s=p.read_text(encoding='utf-8')
old="    skips = [int(x) for x in re.findall(r'skipped=(\\d+)', text)]"
new="    # O gate imprime novamente o resumo; contar somente a linha unittest original.\n    skips = [int(x) for x in re.findall(r'^OK \\(skipped=(\\d+)\\)\\s*$', text, re.MULTILINE)]"
assert old in s
s=s.replace(old,new,1)
s=s.replace("result, _ = executar(['node', 'tools/readme_visuals/validate_production.mjs'], sandbox", "result, visual_text = executar(['node', 'tools/readme_visuals/validate_production.mjs'], sandbox",1)
old="                    qa[label] = {'status': 'nao_confirmado', 'failures': ['Execução não produziu relatório de QA novo verificável.']}"
new="""                    missing = re.search(r\"Error: (ENOENT)[^\\n]*open '([^']+)'\", visual_text)
                    reason = 'Execução não produziu relatório de QA novo verificável.'
                    if missing:
                        path = missing.group(2)
                        path = 'ambiente_fonte/' + path.split('/ambiente_fonte/', 1)[1] if '/ambiente_fonte/' in path else Path(path).name
                        reason = missing.group(1) + ': arquivo esperado pelo validador global ausente: ' + path
                    qa[label] = {'status': 'nao_confirmado', 'failures': [reason]}"""
assert old in s
s=s.replace(old,new,1)
needle="            finally:\n                subprocess.run(['git', 'worktree', 'remove', '--force', str(sandbox)]"
insert="""                # Validar as famílias não contorna nem aprova o gate global falho.
                # Cada resultado é guardado com alcance próprio, sem renderização.
                for family in ('top', 'snippets', 'scripts', 'skills', 'prompts'):
                    family_result, _ = executar(['node', 'tools/readme_visuals/validate_production.mjs', '--family', family], sandbox, out, 'figuras_' + label + '_' + family, root, base)
                    resultados.append(family_result)
                    family_path = sandbox / ('ambiente_fonte/.assistant/hub_readmes_visual_assets/qa/sprint_' + family + '.json')
                    if family_result['codigo'] == 0 and family_path.is_file():
                        family_report = json.loads(family_path.read_text(encoding='utf-8'))
                        family_result['verificacoes_visuais'] = family_report.get('checks')
                        (out / ('qa_' + label + '_' + family + '.json')).write_text(json.dumps(family_report, ensure_ascii=False, indent=2) + '\\n', encoding='utf-8')
            finally:
                subprocess.run(['git', 'worktree', 'remove', '--force', str(sandbox)]"""
assert needle in s
s=s.replace(needle,insert,1)
needle="    after_base = inventariar(base)"
insert="""    result, _ = executar([sys.executable, '-B', str(root / 'tools/tests/test_baseline_visual_runner.py')], root, out, 'guardas_runner', root, base)
    resultados.append(result)
    after_base = inventariar(base)"""
assert needle in s
s=s.replace(needle,insert,1)
p.write_text(s,encoding='utf-8')

Path('tools/tests/test_baseline_visual_runner.py').write_text('''"""Regressões do relatório: não duplicar skips nem esconder erros de execução."""
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
        d,_=self.run_text('Ran 43 tests in 0.1s\\nOK (skipped=7)\\n   OK (0.1s) OK (skipped=7)')
        self.assertEqual(d['skips_reportados'],7)
    def test_total_casos_varias_suites(self):
        d,_=self.run_text('Ran 45 tests in 0.1s\\nOK\\nRan 43 tests in 0.1s\\nOK (skipped=7)')
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
''',encoding='utf-8')

p=Path('docs/sprints/sistema_temas/ACHADOS_V00.md')
s=p.read_text(encoding='utf-8')
s+='''
## A08 — Falha global observada e anterior à V00

Na rodada 34703259496, o validador global falhou tanto na base quanto na candidata
com ENOENT ao tentar ler `ambiente_fonte/.assistant/CATALOGO_HELPERS.md`, arquivo
retirado pela consolidação do Manual. O QA versionado anterior não é resultado
desta execução. V00 não recria um catálogo concorrente nem altera o validador
histórico para esconder essa falha. A segunda rodada executa também cada família,
com alcance explícito; PASS de famílias não equivale a aprovação global.

## A09 — Contagens locais do README afetadas pela nova documentação

O gate da base passou. Na primeira candidata, a inclusão dos instrumentos e
documentos aumentou as contagens locais de arquivos e links. A correção limita-se
às duas linhas da saída local do README raiz, obtidas de nova execução real.
Não altera bloco remoto, resultado analítico, instrução de produto ou gate.

## A10 — Contagem de skips na primeira instrumentação

A primeira versão do agregador contou duas vezes sete skips, porque o gate imprime
novamente o resumo unittest. A rodada inicial registrou 14; o número real era 7.
A correção usa somente a linha original de unittest e acrescenta teste para a
repetição. Evidência inicial é histórica, não uma segunda execução dos skips.
'''
p.write_text(s,encoding='utf-8')

Path('docs/sprints/sistema_temas/RASTREABILIDADE_V00.md').write_text('''# Rastreabilidade V00 ao planejamento aprovado

Esta matriz se refere aos identificadores do catálogo de 198 cenários entregue
na conversa em 12/09/2026, base f748c144. Não declara todos esses cenários
executados: a V00 só implementa sua instrumentação inicial. Estado definitivo de
cada comando está no resumo da rodada. PARCIAL não equivale a PASS do requisito.

| Cenário | Evidência implementada | Limite de aceite |
|---|---|---|
| BASE-01 | Inventário nominal automático com caminho e linha | PARCIAL: falta classificação semântica completa e dono |
| BASE-02 | Consulta live de main e PR #5, refs e ADRs registrados | Documentado; reconferir antes da integração |
| BASE-03 | Mutantes de worktree suja e guardas antigas de empacotamento | Conferir logs; não houve promoção real |
| BASE-04 | Mutantes de Git/lista/produto sem ocorrências | Testes do inventariador |
| BASE-05 | AST, assinaturas, constantes, fachadas e imports | PARCIAL: relações dinâmicas/relativas e revisão nominal |
| BASE-06 | Fixtures fixas, arrays, Plotly e HTML antes/depois | PARCIAL: ampliar exemplos dos demais consumidores |
| BASE-07 | Hashes de arquivos, posição/seção de imagens e mutantes | PARCIAL: não é leitura de navegador |
| BASE-08 | Marcador oficial reutilizado e caso FILE/NOTEBOOK | Execução local; nenhum objeto importado no remoto |
| BASE-09 | Gates na base e candidata, logs e causa de falha separados | Falha global histórica registrada, não apagada |
| BASE-10 | Divergência do guia geral contra v2 registrada | PENDENTE de reconciliação documental |
| LEG-01 | Suíte antiga e chamadas legadas de Plotly/cabeçalho | PARCIAL: todos os imports afetados exigem revisão do inventário |
| ART-01 | Suíte existente do publicador e proteção por hashes | Revisor deve conferir aderência nominal dos mutantes |
| PUB-01 | Suíte de publicação com mocks, sem credenciais | Não é observação em destino remoto |
| DOC-01 | Guias distinguem vigente/candidata/histórico/derivado | PENDENTE de teste de leitura com pessoa nova |

V01, configuração de temas, widgets e integração App/AI-BI não foram antecipados.
Auditoria independente e aceite humano permanecem pendentes.
''',encoding='utf-8')
p=Path('docs/sprints/sistema_temas/README.md');s=p.read_text(encoding='utf-8');s+='\nConsulte também a [rastreabilidade ao plano](RASTREABILIDADE_V00.md).\n';p.write_text(s,encoding='utf-8')
p=Path('CHANGELOG.md');s=p.read_text(encoding='utf-8');needle='### Adicionado\n\n- (Codex) Inventário visual';assert needle in s
s=s.replace(needle,'### Corrigido nesta candidata\n\n- (Codex) Agregação dos skips, testada contra resumo duplicado; contagens locais do README reconciliadas com execução.\n- (Codex) Falha global editorial anterior registrada com causa concreta; famílias validadas com alcance separado.\n\n### Adicionado\n\n- (Codex) Inventário visual',1);p.write_text(s,encoding='utf-8')
# Reconciliar somente as duas linhas locais; o bloco remoto não é tocado.
subprocess.run(['git','add','tools/executar_baseline_visual.py','tools/tests/test_baseline_visual_runner.py','docs/sprints/sistema_temas','CHANGELOG.md'],check=True)
proc=subprocess.run([sys.executable,'-B','tools/validate_assistant.py'],capture_output=True,text=True,check=True)
p=Path('README.md');s=p.read_text(encoding='utf-8')
for name in ('identidade','links'):
    pattern=r'^repo \('+name+r'\)\s*:.*$'
    rows=re.findall(pattern,proc.stdout,re.MULTILINE)
    assert len(rows)==1, (name,rows)
    assert len(re.findall(pattern,s,re.MULTILINE))==1,name
    s=re.sub(pattern,lambda _:rows[0],s,count=1,flags=re.MULTILINE)
p.write_text(s,encoding='utf-8')
