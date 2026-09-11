"""Executa o código efetivamente documentado, não uma cópia dos exemplos.

Sem argumentos: exemplos portáveis, sem Spark, rede, tracking ou publicação.
--spark: inclui exemplos com Spark LOCAL previamente instalado. Isto não é smoke
Databricks, teste de ACL, descoberta de skills ou treino das bibliotecas opcionais.
"""
from __future__ import annotations
import contextlib,io,re,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from markdown_contract import python_blocks

ROOT=Path(__file__).resolve().parents[2]
STAGE=ROOT/'Template_READMEs/sprints_preenchidos'
LIB=ROOT/'ambiente_fonte/.assistant'
sys.path.insert(0,str(LIB))
SPARK='--spark' in sys.argv
if SPARK:sys.argv.remove('--spark')


def code_of(sprint):return (STAGE/sprint/'README.md').read_text(encoding='utf-8')


def run(code, ns):
    code=code.replace('/Workspace/Users/<username>/.assistant',LIB.as_posix())
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code,'<codigo-do-README>','exec'),ns)


def snippet_parts():
    text=code_of('sprint-03-snippets');preps=[];cards={}
    for line,code in python_blocks(text):
        before='\n'.join(text.splitlines()[:line-2])
        headings=re.findall(r'(?m)^#{4,5} `([^`]+)`\s*$',before)
        if headings:cards.setdefault(headings[-1],[]).append(code)
        elif 'assistant_root' in code or 'numpy' in code or 'mensal =' in code or 'rng =' in code or 'from datetime' in code:
            preps.append(code)
    return preps,cards

PREPS,CARDS=snippet_parts()
PURE=['split_temporal','lgbm_temporal','walk_forward','vintage_analysis','scorecard_builder',
'score_bands','metrics_report','curves_plotly','explainability_report','performance_monitor',
'drift_detection','cluster_profiling','dataframe_styled','theme_plotly','section_header',
'badge','divider','index_generator','kpi_card','colors','styles','emojis','format_br']
SPARK_CARDS=['woe_iv_calculator','null_summary','smart_sample','date_features','join_diagnostics',
'pit_join','psi_calculator','safe_display','distribution_grid','correlation_matrix','fixtures']

class DocumentedExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import plotly.graph_objects as go
        cls.plot_patch=patch.object(go.Figure,'show',lambda *a,**kw:None)
        cls.plot_patch.start()
        if SPARK:
            from pyspark.sql import SparkSession
            cls.spark=SparkSession.builder.master('local[2]').appName('readme-review-local-only').config('spark.ui.enabled','false').config('spark.sql.shuffle.partitions','2').getOrCreate()
            cls.spark.sparkContext.setLogLevel('ERROR')
    @classmethod
    def tearDownClass(cls):
        cls.plot_patch.stop()
        if SPARK:cls.spark.stop()

    def test_doc_coverage_as_documented(self):
        text=code_of('sprint-04-scripts')
        code=next(c for _,c in python_blocks(text) if 'TemporaryDirectory(' in c)
        run(code,{})

    @unittest.skipUnless(SPARK,'Requer --spark e Spark local previamente instalado')
    def test_all_script_steps_as_documented(self):
        ns={}
        for _,code in python_blocks(code_of('sprint-04-scripts')):run(code,ns)
        self.assertEqual(ns['resultado']['score'],95)
        self.assertEqual(ns['igual']['valor_gasto']['classification'],'not_classified')

    @unittest.skipUnless(SPARK,'Requer --spark e Spark local previamente instalado')
    def test_assistant_as_documented(self):
        ns={}
        for _,code in python_blocks(code_of('sprint-02-assistant')):run(code,ns)

    @unittest.skipUnless(SPARK,'Requer --spark e Spark local previamente instalado')
    def test_pattern_wilson_as_documented(self):
        from pyspark.sql import SparkSession
        ns={'spark':SparkSession.getActiveSession()}
        for _,code in python_blocks(code_of('sprint-08-padroes')):run(code,ns)


def make_case(name, spark=False):
    def case(self):
        ns={}
        for prep in PREPS:
            if 'from pyspark' in prep and not spark:continue
            run(prep,ns)
        self.assertIn(name,CARDS)
        for code in CARDS[name]:run(code,ns)
    case.__name__='test_snippet_'+name
    if spark:case=unittest.skipUnless(SPARK,'Requer --spark e Spark local previamente instalado')(case)
    return case

for name in PURE:setattr(DocumentedExamples,'test_snippet_'+name,make_case(name))
for name in SPARK_CARDS:setattr(DocumentedExamples,'test_snippet_'+name,make_case(name,True))

if __name__=='__main__':unittest.main(verbosity=2)
