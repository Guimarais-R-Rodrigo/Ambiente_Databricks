"""Correção de falso negativo e de contagem observados na revisão própria V00."""
from pathlib import Path
import subprocess,sys,re
p=Path('tools/inventario_visual.py');s=p.read_text(encoding='utf-8')
needle='PADROES = {\n';assert needle in s
s=s.replace(needle,"PADROES = {\n    'biblioteca_visual': re.compile(r'\\b(?:plotly|matplotlib|seaborn|altair|bokeh|ipywidgets|streamlit)\\b', re.I),\n    'helper_visual': re.compile(r'\\b(?:aplicar_tema|registrar_template_plotly|theme_plotly|section_header_html|kpi_card_html)\\b'),\n",1)
p.write_text(s,encoding='utf-8')
p=Path('tools/tests/test_inventario_visual.py');s=p.read_text(encoding='utf-8');needle="\n\nif __name__ == '__main__':";assert needle in s
new='''
    def test_consumidor_sem_literal_de_cor_e_inventariado(self):
        self.module.write_text('import plotly.graph_objects as go\\ndef desenhar():\\n    return go.Histogram(x=[1, 2])\\n', encoding='utf-8')
        self.commit()
        doc=v.inventariar(self.root)
        self.assertTrue(any(o['tipo']=='biblioteca_visual' for o in doc['ocorrencias']))
        row=next(r for r in doc['arquivos'] if r['path']==self.module.relative_to(self.root).as_posix())
        self.assertGreater(row['ocorrencias'],0)

    def test_helper_com_underscore_nao_some_da_matriz(self):
        self.module.write_text('from hub_snippets.visual.theme_plotly import aplicar_tema\\ndef desenhar(fig):\\n    return aplicar_tema(fig)\\n', encoding='utf-8')
        self.commit()
        doc=v.inventariar(self.root)
        self.assertTrue(any(o['tipo']=='helper_visual' for o in doc['ocorrencias']))
'''
s=s.replace(needle,'\n'+new+needle,1);p.write_text(s,encoding='utf-8')
p=Path('tools/executar_baseline_visual.py');s=p.read_text(encoding='utf-8');old="re.findall(r'Ran (\\d+) tests?\\b', text)";new="re.findall(r'^Ran (\\d+) tests?\\b', text, re.MULTILINE)";assert old in s;s=s.replace(old,new,1);p.write_text(s,encoding='utf-8')
p=Path('tools/tests/test_baseline_visual_runner.py');s=p.read_text(encoding='utf-8');needle="\nif __name__=='__main__':";assert needle in s
s=s.replace(needle,'''
    def test_texto_citado_nao_vira_suite_executada(self):
        d,_=self.run_text('{"exemplo": "Ran 99 tests"}\\nRan 2 tests in 0.1s\\nOK')
        self.assertEqual(d['testes_unittest_reportados'],2)
'''+needle,1);p.write_text(s,encoding='utf-8')
p=Path('docs/sprints/sistema_temas/ACHADOS_V00.md');s=p.read_text(encoding='utf-8');s+='''
## A11 — Consumidor sem cor literal não pode sumir da matriz

A revisão própria encontrou `display/distribution_grid` nos imports/AST, mas sem
ocorrência na primeira matriz de padrões: `aplicar_tema` contém underscore e não
casa com a palavra isolada `tema`. Foram adicionados padrões de bibliotecas e
helpers, com dois mutantes que criam figuras sem cor literal. A matriz foi
regenerada; revisão semântica independente continua necessária.

A agregação de casos também passou a aceitar somente linhas unittest `Ran ...`
no início da linha. Uma mensagem JSON que cita exemplo de execução não deve
inflar o total observado; há teste específico para esse cenário.
''';p.write_text(s,encoding='utf-8')
p=Path('CHANGELOG.md');s=p.read_text(encoding='utf-8');needle='### Corrigido nesta candidata\n\n';assert needle in s
s=s.replace(needle,needle+'- (Codex) Descoberta de consumidores sem cor literal e agregação que distingue casos executados de texto citado, com testes adversariais.\n',1);p.write_text(s,encoding='utf-8')
subprocess.run(['git','add','tools/inventario_visual.py','tools/executar_baseline_visual.py','tools/tests/test_inventario_visual.py','tools/tests/test_baseline_visual_runner.py','docs/sprints/sistema_temas/ACHADOS_V00.md','CHANGELOG.md'],check=True)
proc=subprocess.run([sys.executable,'-B','tools/validate_assistant.py'],capture_output=True,text=True,check=True)
p=Path('README.md');s=p.read_text(encoding='utf-8')
for name in ('identidade','links'):
    pattern=r'^repo \('+name+r'\)\s*:.*$';rows=re.findall(pattern,proc.stdout,re.MULTILINE)
    assert len(rows)==1 and len(re.findall(pattern,s,re.MULTILINE))==1
    s=re.sub(pattern,lambda _:rows[0],s,count=1,flags=re.MULTILINE)
p.write_text(s,encoding='utf-8')
