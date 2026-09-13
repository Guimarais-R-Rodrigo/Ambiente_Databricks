"""Integração editorial R09 sobre base fixa; não é instalador do workspace.

Recortes de texto usam posições Unicode da versão de notebook verificada por
blob Git. Apenas Markdown é editado; a guarda independente confere células,
magics, AST e blocos de saída antes de qualquer fechamento da candidata.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

BASE = "d5945e04328609878f63857cc15cf5e5039b3e75"
ROOT = Path(__file__).resolve().parents[4]
OBJECTS = ("curves_plotly", "drift_detection", "metrics_report", "mlflow_run", "performance_monitor")
SPRINT = "docs/sprints/readmes_objetos"
NOTEBOOK_BLOBS = {
    "curves_plotly": "072e8c5dd1a3a4f9434efa566a9c6d836765c89f",
    "metrics_report": "cc41f3c1cb6345156d88fe34267eba3c5029e17e",
    "drift_detection": "1adac3a013a0c259bcdff38d2c3474fd2266e6bb",
    "performance_monitor": "907efef5813637a3884a1378bd854489cc7ab2a6",
    "mlflow_run": "5b20976d56c74df3f9b0eb45d18328e789ce422c",
}
EDITS = {
 "curves_plotly": [
  [3791,3904,"# MAGIC - **Sem conferir memória e tamanho da entrada.** O argumento `n` só escreve o rodapé; não limita linhas, amostra nem reduz o cálculo."],
  [3580,3678,"# MAGIC - **Tratando ROC como precisão da seleção.** Em evento raro, complemente discriminação com PR, lift e custos."],
  [3080,3343,"# MAGIC **Como ler.** Lift cumulativo compara a concentração de eventos no topo\n# MAGIC com a base, não lucro nem ganho causal. Aqui KS é `max(TPR - FPR)`, na\n# MAGIC escala 0–1, destacado sobre a ROC. Já `metrics_report.ks_pct` usa máximo\n# MAGIC absoluto bilateral, em 0–100. Com scores invertidos, nem dividir por 100\n# MAGIC torna as duas medidas iguais."],
  [2682,2921,"# MAGIC 1,85%** (a fixture pede 2%; o sorteio entrega 1,85%). A referência horizontal\n# MAGIC usada pelo gráfico é **0,0185**, não 0,02. Uma curva empírica obtida de scores\n# MAGIC aleatórios não precisa ser exatamente uma reta."],
  [2271,2513,"# MAGIC **Como ler.** Precisão responde: **entre os selecionados, quantos são\n# MAGIC evento?** Recall responde quantos eventos foram alcançados. A curva ajuda a\n# MAGIC examinar esse compromisso; precisão não é monotônica em toda amostra, e a\n# MAGIC ordem dos pontos desenhados não é uma regra de decisão."],
  [1797,2151,"# MAGIC **Como ler.** ROC compara TPR (eventos encontrados) com FPR (não eventos\n# MAGIC marcados). O denominador de FPR são os não eventos: nesta fixture histórica,\n# MAGIC 7.852 linhas. Mil falsos positivos corresponderiam a cerca de 12,7% deles,\n# MAGIC não a um movimento desprezível. A curva continua útil; complemente-a com\n# MAGIC a precisão e com o custo da seleção."],
  [393,506,"# MAGIC **O que este helper faz.** Gera ROC, precisão-recall, lift cumulativo e KS direcional com tema local. Quem chama precisa limitar a população; o helper não amostra os dados."],
  [120,384,"# MAGIC **O problema.** ROC mede discriminação, mas não informa sozinha a precisão de uma seleção. Em população com evento raro, uma taxa pequena de falsos positivos pode representar muitos casos. Combine ROC, precisão-recall e lift conforme a decisão; desbalanceamento não torna ROC automaticamente inútil."]
 ],
 "metrics_report": [
  [4424,4518,"# MAGIC - **Comparando F1 sem regra operacional comum.** Declare como os cortes\n# MAGIC   foram escolhidos e avalie na mesma população."],
  [3475,3994,"# MAGIC **Como ler.** Mudar o corte muda a seleção. Nesta fixture poucos scores\n# MAGIC ultrapassam 0,5; isso não decorre apenas da prevalência nem ocorre em todo\n# MAGIC modelo desbalanceado.\n# MAGIC\n# MAGIC Comparações podem usar cortes diferentes se a regra operacional for comum\n# MAGIC e os cortes tiverem sido escolhidos na validação, sem consultar o teste.\n# MAGIC Mesmo corte numérico não garante comparabilidade se escalas/calibração,\n# MAGIC população ou horizonte forem diferentes."],
  [2826,3101,"# MAGIC Precisão e recall descrevem a seleção no corte escolhido. Ao elevar o\n# MAGIC corte, recall não aumenta; precisão não precisa aumentar em toda amostra.\n# MAGIC AUC resume ordenação sem depender desse corte. A chave `auc_pr` contém\n# MAGIC Average Precision, não integração trapezoidal; `ks_pct` é bilateral em\n# MAGIC pontos percentuais. A prevalência de 5% e os valores abaixo são apenas\n# MAGIC esta fixture, não taxas típicas garantidas para risco, churn ou fraude."],
  [1312,1379,"# MAGIC ## 1. Uma base sintética desbalanceada"],
  [124,393,"# MAGIC **O problema.** Com 5% de eventos, marcar todos como não evento acerta 95% das linhas, mas não encontra evento algum. Acurácia isolada pode esconder esse problema. O limiar `0.5` deste helper é uma convenção; escolha-o segundo a decisão e os dados, não como padrão universal de bibliotecas."]
 ],
 "drift_detection": [
  [6681,6715,"# MAGIC alarme por **0,000667**, menos de um milésimo."],
  [6452,6589,"# MAGIC responde: `ALERT` para o que passou do limiar, `OK` para o resto. A nova\n# MAGIC chamada recalcula os índices pelo mesmo algoritmo; a política acrescenta\n# MAGIC a classificação. `ks_threshold` compara estatística KS, não p-valor."],
  [4749,4861,"# MAGIC certo em cada uma. A fixture altera fortemente `score`, mas também muda\n# MAGIC a distribuição de UF; não há apenas uma variável construída para mudar."],
  [3386,3811,"# MAGIC **Como ler.** CSI aplica a aritmética de estabilidade a categorias. Isso\n# MAGIC não torna o índice automaticamente estável: categorias novas/raras e o\n# MAGIC piso `eps` influenciam o resultado. O literal `__MISSING__` representa\n# MAGIC faltantes e não deve coincidir com uma categoria legítima.\n# MAGIC\n# MAGIC Códigos de categorias podem ser convertidos em números e passar pelo PSI\n# MAGIC sem erro; o resultado ainda será inadequado se sua ordem for arbitrária."],
  [2477,2716,"# MAGIC O KS vem acompanhado do **p-valor**, que depende também da amostra e das\n# MAGIC premissas do teste. Mais observações podem tornar detectável uma diferença\n# MAGIC pequena. Não existe um limite universal de 4.000 linhas que torne o p-valor\n# MAGIC inútil; examine a estatística, a amostragem e a relevância operacional."]
 ],
 "performance_monitor": [
  [4182,4267,"# MAGIC - **Esperando comparação mês a mês.** Esta classe usa baseline fixo e uma política; outra referência exige desenho próprio."],
  [3805,4014,"# MAGIC Este monitor compara com o baseline fixo, não com o mês anterior. Variação\n# MAGIC mês a mês pode conter sinal ou ruído; a classe não faz essa distinção.\n# MAGIC `should_retrain` sugere investigação e nunca autoriza retreino automático.\n# MAGIC Persistência conta entradas na ordem das chamadas, mesmo com datas\n# MAGIC duplicadas ou alertas em métricas diferentes."],
  [2637,2833,"# MAGIC **Como ler.** São limites de **exemplo** aplicados à deterioração, não\n# MAGIC AUCs mínimos universais. Com baseline 0,78, queda absoluta de 0,05 aponta\n# MAGIC para 0,73. A política é opcional na assinatura: omiti-la usa o exemplo.\n# MAGIC Passar `EXAMPLE_THRESHOLDS` explicitamente não a torna calibrada."],
  [407,557,"# MAGIC **O que este helper faz.** Guarda métricas em memória e compara deterioração com limiares declarados. Não calibra a política nem diferencia automaticamente ruído estatístico de mudança real."]
 ],
 "mlflow_run": [
  [5715,5869,"# MAGIC não abre, segundo o relato histórico. Isso não identifica sozinho a causa\n# MAGIC da diferença: versão, configuração e condições de sessão precisam ser\n# MAGIC comparadas antes de atribuir a mudança ao runtime gerenciado."],
  [5089,5407,"# MAGIC **Como ler.** O bloco preservado descreve aquela execução. A célula captura\n# MAGIC uma exceção de qualquer etapa do `with`; sua mensagem de abertura não prova\n# MAGIC que toda falha futura ocorrerá ao abrir. Sucesso depende de backend,\n# MAGIC permissões e versões, não apenas de usar compute clássico.\n# MAGIC\n# MAGIC A documentação oficial de MLflow apresenta uso no Free Edition. Essa edição\n# MAGIC é serverless e não oferece compute clássico. A recomendação histórica no\n# MAGIC bloco acima não é uma alternativa disponível dentro do Free. Veja as\n# MAGIC referências atuais e os limites no [README](README.md)."],
  [2852,2915,"# MAGIC ## 3. O registro completo — tentativa e relato histórico"],
  [2566,2710,"# MAGIC Blocos sucessivos já encerrados separam os registros. `run_governado` não\n# MAGIC fecha um run externo ativo nem passa `nested=True`. Se houver run ativo,\n# MAGIC resolva explicitamente a situação antes de abrir outro."],
  [1025,1137,"# MAGIC | Diferença Free × trabalho | depende de versão, configuração e permissões; a seção 3 preserva uma falha histórica, não uma proibição geral |"],
  [935,1024,"# MAGIC | Escrita | runs, parâmetros, métricas, modelo e exemplo podem ser persistidos no backend ativo; confira destino e permissões |"],
  [807,856,"# MAGIC | Bibliotecas | MLflow; scikit-learn para o flavor fixo de registro; conferir versões |"],
  [477,609,"# MAGIC **O que este helper faz.** Abre um run sem aninhamento automático, grava contexto textual e verifica parâmetros, métricas e presença de exemplo do modelo ao sair normalmente. A checagem não inspeciona a assinatura persistida nem comprova a qualidade do registro."]
 ]
}
ENV_NOTE = 'Nota da revisão R09: as bibliotecas e a disponibilidade do compute precisam ser conferidas no ambiente real. Os resultados colados abaixo são históricos; esta sprint não executou o notebook completo no Databricks.'


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def write(path,text):
    (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/path).write_text(text,encoding='utf-8')


def once(path,old,new):
    text=(ROOT/path).read_text(encoding='utf-8')
    if text.count(old)!=1:raise ValueError(f'âncora não única: {path}: {old[:80]}')
    write(path,text.replace(old,new,1))


def append(path,heading,body):
    text=(ROOT/path).read_text(encoding='utf-8')
    if heading in text:raise ValueError(f'já aplicado: {path}: {heading}')
    write(path,text.rstrip()+'\n\n'+heading+'\n\n'+body.strip()+'\n')


def expected_paths():
    paths=[f'ambiente_fonte/.assistant/hub_snippets/ml/{o}/{n}' for o in OBJECTS for n in ('README.md',f'exemplo_{o}.py')]
    paths+=['ambiente_fonte/.assistant/MANUAL_TECNICO.md','ambiente_fonte/.assistant/hub_snippets/README.md','MANUAL_TECNICO.md','README.md','CLAUDE.md','PLANO_HUB.md','CHANGELOG.md','docs/sprints/README.md']
    paths += [f'{SPRINT}/{p}' for p in ('README.md','CONTROLE_MIGRACAO.json','ACHADOS_R09.md','RELATORIO_R09.md','MATRIZ_ALTERACOES_R09.md','RUBRICA_R09.json','evidencias_r09/aplicar_r09.py','evidencias_r09/verificar_r09.py','evidencias_r09/verificar_preservacao.py')]
    paths += [p.replace('ambiente_fonte/','Novo_Ambiente_Simulado/Users/usuario-free/',1) for p in paths if p.startswith('ambiente_fonte/')]
    if len(paths)!=39 or len(set(paths))!=39:raise ValueError('inventário inesperado')
    return sorted(paths)


def nominal():
    text='# Matriz nominal R09\n\nBase `'+BASE+'`; contrato 1.0.0. **39 caminhos previstos: cinco READMEs de objeto novos, doze derivados e demais documentação/instrumentos.** O verificador exige exatamente esta lista, sem alteração funcional.\n\n| Caminho | Natureza |\n|---|---|\n'
    for p in expected_paths():
        if p.startswith('Novo_Ambiente_Simulado/'):kind='Derivado pelo renderer; não editar manualmente'
        elif p.endswith('/README.md') and '/ml/' in p:kind='README de objeto novo'
        elif '/exemplo_' in p:kind='Notebook atualizado apenas na prosa/backlinks'
        elif '/evidencias_r09/' in p:kind='Instrumento novo de aplicação/verificação'
        elif any(x in p for x in ('ACHADOS_R09','RELATORIO_R09','MATRIZ_ALTERACOES_R09','RUBRICA_R09')):kind='Registro novo da sprint'
        elif p=='MANUAL_TECNICO.md':kind='Cópia sincronizada do Manual canônico'
        else:kind='Documentação ou controle atualizado'
        text+=f'| `{p}` | {kind} |\n'
    text+='\nOs guias anteriores, formulários, implementações/fachadas e sistema de temas não são reescritos. O aplicador é manutenção da sprint sobre sua base fixa, não instalador do produto nem comando para executar no workspace. O PR e o relatório registram o fechamento remoto posterior, sem presumir aceite.\n'
    write(f'{SPRINT}/MATRIZ_ALTERACOES_R09.md',text)


def write_records():
    findings=[
        ('metrics_report','O exemplo da docstring cita format_metrics_table, ausente na implementação/fachada.'),
        ('metrics_report','auc_pr contém Average Precision, não integração trapezoidal da curva PR.'),
        ('metrics_report','KS bilateral em 0–100 pode ser alto com AUC zero; interpretar orientação e unidade.'),
        ('metrics_report','MAPE exclui alvos zero e pode ser NaN; métricas são arredondadas, sem intervalo de confiança.'),
        ('metrics_report','Lift usa ceil de 10% e pode exceder essa fração; não há desempate de negócio.'),
        ('metrics_report','Não há realinhamento por índice nem sample_weight; tipos/valores válidos não comprovam população adequada.'),
        ('curves_plotly','n apenas formata o rodapé, não limita a população; show_auc=False mantém AUC na legenda/rodapé.'),
        ('curves_plotly','KS usa max(TPR-FPR), sem absoluto, em escala 0–1; não é equivalente a ks_pct com scores invertidos.'),
        ('curves_plotly','Lift é cumulativo e usa frações nominais com contagem arredondada para cima, não lift isolado do decil.'),
        ('curves_plotly','ROC continua informativa em população desbalanceada; PR aleatória empírica não precisa ser reta.'),
        ('curves_plotly','Tema e paleta local de seis cores são legados; nenhuma rota de tema resolvido foi implantada pela R09.'),
        ('drift_detection','PSI inclui bucket NaN, exige finitos dos dois lados e rejeita infinito; KS elimina não finitos.'),
        ('drift_detection','CSI aparece na coluna psi; min_non_null em categóricas conta linhas, inclusive faltantes.'),
        ('drift_detection','__MISSING__ pode colidir com categoria legítima; eps é piso sem renormalização.'),
        ('drift_detection','Listas explícitas não são validadas como partição de feature_cols; lista vazia ativa inferência.'),
        ('drift_detection','Percentuais de faltantes são anteriores à coerção numérica; não incluem toda conversão malsucedida.'),
        ('drift_detection','Limiar KS compara estatística, não p-valor; finitude/ordem de políticas não têm validação completa.'),
        ('drift_detection','Não existe limite universal de 4.000 linhas para inutilidade de p-valores; a fixture muda também UF.'),
        ('drift_detection','0,250667 supera 0,25 por 0,000667, não seis milésimos; nova chamada recalcula os índices.'),
        ('performance_monitor','auc_roc é traduzido para auc; filtrar apenas nomes iguais pode perder AUC silenciosamente.'),
        ('performance_monitor','Deltas são unilaterais, absolutos ou relativos; n_predictions não pondera nem calibra alertas.'),
        ('performance_monitor','Datas duplicadas e fora de ordem são aceitas; persistência conta inserções com algum alerta.'),
        ('performance_monitor','Período incompleto ainda pode gerar investigação; caller-provided não significa política aprovada.'),
        ('performance_monitor','Não há armazenamento durável, agenda, notificação, retreino ou implantação automáticos.'),
        ('mlflow_run','Completude verifica exemplo não None, não assinatura persistida; arquivo adicional é opcional.'),
        ('mlflow_run','Dataset/split/limitações são textos, sem reconstrução, snapshot ou linhagem automática.'),
        ('mlflow_run','Flavor sklearn é fixo; fallback TypeError é amplo; retorno não expõe ModelInfo/URI.'),
        ('mlflow_run','Falha de completude ou de corpo não reverte logs; start_run não aninha nem fecha run externo.'),
        ('mlflow_run','input_example pode gravar linhas; experimento afeta sessão; conversão textual não valida semanticamente campos.'),
        ('mlflow_run','Erro histórico do Free não prova proibição geral; Free não oferece compute clássico como alternativa interna.'),
    ]
    content='# Achados R09 — leitura de contrato e correções editoriais\n\nBase `'+BASE+'`. Estes itens **não são correções funcionais**. Implementações e fachadas permanecem preservadas.\n\n'
    for i,(obj,note) in enumerate(findings,1):content+=f'{i}. **{obj}** — {note}\n'
    content+='\nAs docstrings e comentários de células executáveis não foram alterados. Os guias e a prosa dos notebooks esclarecem divergências sem reescrever saídas históricas. Testes de caracterização registram comportamento existente, não certificam que toda limitação seja desejável.\n'
    write(f'{SPRINT}/ACHADOS_R09.md',content)
    report='''# Relatório R09 — avaliação, monitoramento e registro

## Estado e escopo

STATUS_R09: CANDIDATA — validação integral e aceite editorial pendentes.

Base: `d5945e04328609878f63857cc15cf5e5039b3e75`, R08 integrada pelo PR #27. Contrato dos READMEs 1.0.0. Cinco objetos: `curves_plotly`, `drift_detection`, `metrics_report`, `mlflow_run` e `performance_monitor`.

A meta é 60/75 objetos operacionais, três exemplares e 15 pendências. A saída do validador da composição final, não esta previsão, confirma a cobertura.

## Documentações alteradas além dos cinco guias

Cinco notebooks apenas em prosa/backlinks; Manual Técnico canônico e cópia de leitura; catálogo de snippets; README raiz; CLAUDE; PLANO_HUB; índices geral de sprints e da iniciativa; controle de migração; CHANGELOG. Foram acrescentados achados, matriz nominal, este relatório, rubrica e três scripts de integração/verificação. Os doze arquivos correspondentes no simulado são gerados exclusivamente pelo renderer.

A [matriz nominal](MATRIZ_ALTERACOES_R09.md) discrimina novos READMEs, documentos atualizados, instrumentos e derivados. Os [achados](ACHADOS_R09.md) registram 30 limitações/divergências. Nenhum algoritmo foi ajustado para fazer teste passar.

## Evidência local delimitada

Antes da integração, 21 testes portáveis passaram em Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0, SciPy 1.17.0 e Plotly 6.5.2. A cópia local era histórica, mas os cinco módulos foram confrontados com a base atual e tinham os mesmos hashes Git. Isso sustenta apenas os testes desses contratos e quatro exemplos, não o gate do repositório atual.

MLflow não estava instalado localmente; a tentativa de instalação falhou por resolução de rede. Nenhum teste MLflow foi declarado aprovado por essa tentativa. A validação integral exige um checkout completo da base atual e ambiente isolado com MLflow real.

## Testes exigidos para fechar

Gate permanente; validador sem falhas/avisos; V00–V04; contrato 1.0.0 e links; preservação da API e dos cinco notebooks; cinco exemplos dos guias; 21 casos portáveis e oito do grupo MLflow, sem skips. Dois casos do grupo MLflow simulam deliberadamente o retorno de log_model para verificar flags/fallback; seis exercitam integração real, inclusive persistência/releitura de assinatura/modelo. São 29 métodos ao todo; subtestes e reexecuções não aumentam a contagem.

O MLflow de teste usa SQLite e artefatos em diretório temporário, com dados sintéticos e URIs explicitamente isoladas. As versões completas devem acompanhar os logs do run. Isso não valida permissões, tracking corporativo, Unity Catalog ou um runtime Databricks.

## Preservação e procedência

A guarda confere o conjunto exato de caminhos, todos os arquivos pré-existentes fora da lista autorizada, implementações/fachadas byte a byte, células executáveis e magics, AST, blocos históricos de saída, pendências e seus metadados, espelho publicado e três cópias do Manual. O comentário de que o relatório fornece accuracy, presente na implementação do monitor, não foi reescrito: a API efetiva e o README explicam as dez chaves reais.

A autoria e revisão são ChatGPT, A0_light. Não houve auditor independente. Referências primárias de scikit-learn, SciPy, MLflow e Databricks foram consultadas em 13/09/2026 e ligadas nos guias.

## Parada e limites

Não integrar sem aceite editorial específico da R09. Não iniciar R10. Sem publicação no Databricks, execução integral dos notebooks no workspace, homologação de modelos/políticas/acessibilidade, alteração de CSS/paleta, dependências ou workflows permanentes. Um gate verde não equivale a certificação de produção.
'''
    write(f'{SPRINT}/RELATORIO_R09.md',report)
    rubric={'sprint':'R09','base':BASE,'template_version':'1.0.0','objects':list(OBJECTS),'review_level':'A0_light_self_review','independent_audit':False,'human_editorial_acceptance':False,'databricks_published':False,'scope':'documentation_only','coverage_expected':{'operational':60,'total':75,'exemplars':3,'pending':15},'editorial_self_review':{'concept_before_api':True,'decision_and_limits':True,'runtime_not_homologation':True,'synthetic_examples':True,'sources_checked':True,'related_documentation_identified':True},'local_evidence':{'portable_cases':21,'portable_result':'PASS','mlflow_result':'NOT_EXECUTED_NETWORK_UNAVAILABLE','full_current_repository_gate':'NOT_EXECUTED_LOCALLY'},'remote_evidence':{'state':'PENDING','portable_expected':21,'mlflow_expected':8,'mlflow_mocked_dispatch_cases':2,'run_id':None}}
    write(f'{SPRINT}/RUBRICA_R09.json',json.dumps(rubric,ensure_ascii=False,indent=2)+'\n')
    nominal()


def prepare():
    if git('merge-base','HEAD',BASE).decode().strip()!=BASE:raise ValueError('base não ancestral')
    if git('rev-parse','origin/main').decode().strip()!=BASE:raise ValueError('main mudou: reconciliar')
    for obj in OBJECTS:
        path=f'ambiente_fonte/.assistant/hub_snippets/ml/{obj}/exemplo_{obj}.py'
        if git('hash-object',path).decode().strip()!=NOTEBOOK_BLOBS[obj]:raise ValueError(f'notebook mudou: {path}')
        text=(ROOT/path).read_text(encoding='utf-8')
        previous=len(text)
        for start,end,replacement in EDITS[obj]:
            if not 0<=start<end<=previous:raise ValueError('recortes sobrepostos/fora de ordem')
            if any(line and not line.startswith('# MAGIC') for line in text[start:end].splitlines()):raise ValueError('recorte não Markdown')
            text=text[:start]+replacement+text[end:];previous=start
        if 'Guia local completo:' in text:raise ValueError('backlink já existe')
        intro='\n# MAGIC\n# MAGIC **Guia local completo:** [README deste objeto](README.md).\n# MAGIC\n# MAGIC '+ENV_NOTE+'\n'
        marker='\n# COMMAND ----------'
        if marker not in text:raise ValueError('sem células')
        write(path,text.replace(marker,intro+marker,1))
    notes={
        'curves_plotly':'`n` só altera o rodapé; o KS visual é direcional e não equivale ao KS bilateral do relatório.',
        'drift_detection':'PSI/CSI e KS descrevem distribuições; ausência de política não significa ausência de drift.',
        'metrics_report':'`auc_pr` é Average Precision; `ks_pct` é bilateral em 0–100; MAPE exclui alvos zero.',
        'mlflow_run':'O exemplo pode persistir modelo e linhas de entrada; completude local não comprova assinatura ou governança.',
        'performance_monitor':'O histórico é local; alertas orientam investigação e não autorizam retreino automático.',
    }
    manual='ambiente_fonte/.assistant/MANUAL_TECNICO.md'
    for obj in OBJECTS:
        heading=f'#### `hub_snippets.ml.{obj}`'
        route=f'Guia didático: [README de {obj}](hub_snippets/ml/{obj}/README.md). {notes[obj]}'
        once(manual,heading+'\n',heading+'\n\n'+route+'\n')
    write('MANUAL_TECNICO.md',(ROOT/manual).read_text(encoding='utf-8'))
    links='\n'.join(f'- [{o}](ml/{o}/README.md) — {notes[o]}' for o in OBJECTS)
    append('ambiente_fonte/.assistant/hub_snippets/README.md','## Guias R09 — avaliação, monitoramento e registro','Calcular métricas, desenhar curvas, diagnosticar drift, acompanhar períodos e registrar experimentos são tarefas distintas. Escolha a pergunta antes do helper.\n\n'+links)
    for path in ('CLAUDE.md','PLANO_HUB.md'):
        append(path,'### Continuidade R09 — READMEs de avaliação e monitoramento','A R08 foi aceita e integrada pelo PR #27 em `d5945e0`. A R09 documenta cinco objetos sem alterar suas implementações. Estado, outras documentações alteradas e evidências: `docs/sprints/readmes_objetos/RELATORIO_R09.md`. Não iniciar R10 nem presumir aceite editorial da R09.')
    append('docs/sprints/README.md','## R09 — avaliação, monitoramento e registro','R08 integrada pelo PR #27. Consulte o [relatório R09](readmes_objetos/RELATORIO_R09.md), a [matriz de arquivos](readmes_objetos/MATRIZ_ALTERACOES_R09.md) e os [achados](readmes_objetos/ACHADOS_R09.md). A nova leva exige aceite próprio; não publica o Hub.')
    append('README.md','### Continuidade documental — R09','R08 aceita e integrada pelo PR #27. A R09 acrescenta cinco guias de avaliação, monitoramento e registro, com implementações preservadas. Consulte [estado e evidências](docs/sprints/readmes_objetos/RELATORIO_R09.md) e [alterações além dos guias](docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R09.md). A contagem do snapshot é estrutural, não homologação do workspace.')
    index=f'{SPRINT}/README.md';text=(ROOT/index).read_text(encoding='utf-8')
    begin=text.index('O contrato vigente é **1.0.0**.');end=text.index('Os relatórios anteriores preservam',begin)
    text=text[:begin]+'O contrato vigente é **1.0.0**. A R08 foi aceita e integrada pelo PR nº 27 no commit `d5945e0`. A R09 documenta `curves_plotly`, `drift_detection`, `metrics_report`, `mlflow_run` e `performance_monitor`, preservando implementações e fachadas. A meta é **60/75 operacionais, 3/3 exemplares e 15 pendências**; a contagem efetiva é a saída do validador da candidata.\n\nConsulte o [relatório R09](RELATORIO_R09.md), a [matriz nominal](MATRIZ_ALTERACOES_R09.md) e os [achados](ACHADOS_R09.md). Parar para o aceite editorial desta leva antes de integrar ou iniciar a R10. O [relatório R08](RELATORIO_R08.md) preserva o estado pré-merge; seu aceite posterior está registrado no PR #27.\n\n'+text[end:]
    for old,new in (('[Matriz R08](MATRIZ_ALTERACOES_R08.md)','[Matriz R09](MATRIZ_ALTERACOES_R09.md)'),('[Achados R08](ACHADOS_R08.md)','[Achados R09](ACHADOS_R09.md)'),('[Relatório R08](RELATORIO_R08.md)','[Relatório R09](RELATORIO_R09.md)')):
        if text.count(old)!=1:raise ValueError(f'rota inesperada: {old}')
        text=text.replace(old,new,1)
    write(index,text)
    control=f'{SPRINT}/CONTROLE_MIGRACAO.json';data=json.loads((ROOT/control).read_text(encoding='utf-8'))
    keys={f'hub_snippets/ml/{o}' for o in OBJECTS}
    actual={k for k,v in data['pending'].items() if v['sprint']=='R09'}
    if actual!=keys:raise ValueError('escopo R09 divergiu')
    for k in keys:
        if data['pending'][k]!={'sprint':'R09','lote':'A'}:raise ValueError(k)
        del data['pending'][k]
    write(control,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    ch='''## 2026-09-13 — R09: avaliação, monitoramento e registro (ChatGPT)

### Adicionado

- (ChatGPT) Cinco READMEs 1.0.0: curves_plotly, drift_detection, metrics_report, mlflow_run e performance_monitor.
- (ChatGPT) Achados, relatório, matriz nominal, rubrica e verificadores; 29 casos previstos, com seis integrações MLflow e dois testes de despacho explicitamente simulados dentro do grupo de oito.

### Atualizado

- (ChatGPT) Cinco notebooks apenas na prosa/backlinks; Manual canônico e cópia, catálogo, README raiz, CLAUDE, PLANO_HUB e índices. Simulado gerado pelo renderer.
- (ChatGPT) Controle remove exatamente cinco pendências R09. R08 aceita e integrada pelo PR #27; R09 ainda exige aceite próprio.

### Corrigido na documentação

- (ChatGPT) Diferencia KS direcional/bilateral e unidades, AP/área PR, efeitos do rodapé, limiares exemplificativos, faltantes e persistência do monitor.
- (ChatGPT) MLflow: campos preenchidos não comprovam assinatura; registros parciais não sofrem rollback; relatos históricos não são restrições universais do Free.

### Limites

- (ChatGPT) Sem alteração de implementação, fachada, comandos executáveis, saídas históricas, temas ou dependências permanentes. Sem publicação/homologação Databricks, auditoria independente, merge R09 ou início da R10.

'''
    s=(ROOT/'CHANGELOG.md').read_text(encoding='utf-8')
    if '## 2026-09-13 — R09:' in s:raise ValueError('changelog já aplicado')
    i=s.index('\n## ');write('CHANGELOG.md',s[:i+1]+ch+s[i+1:])
    write_records();git('add','-A')
    print('R09_PREPARED: 5 guias; integração aplicada; executar renderer e gates')


def snapshot():
    out=subprocess.check_output([sys.executable,'tools/validate_assistant.py'],cwd=ROOT,text=True)
    keys=['skills','prompts','helpers citados','markdown / links','notebooks / links','readmes de objeto','pastas de objeto','forma da pasta','contrato de dados','contrato de entrada','saída colada','idioma da docstring','normas do molde','notebook exercita','python (AST)','instrucoes','repo (identidade)','repo (links)']
    actual={key:line for line in out.splitlines() for key in keys if line.startswith(key)}
    if set(actual)!=set(keys):raise ValueError('snapshot incompleto')
    if '60/75 operacionais' not in actual['readmes de objeto'] or '15 pendentes' not in actual['readmes de objeto']:raise ValueError('cobertura inesperada')
    lines=(ROOT/'README.md').read_text(encoding='utf-8').splitlines();found=set()
    for i,line in enumerate(lines):
        for key,value in actual.items():
            if line.startswith(key):lines[i]=value;found.add(key);break
    if found!=set(keys):raise ValueError('snapshot anterior não localizado')
    write('README.md','\n'.join(lines)+'\n');git('add','README.md');print(out)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--snapshot',action='store_true');args=ap.parse_args()
    snapshot() if args.snapshot else prepare()
