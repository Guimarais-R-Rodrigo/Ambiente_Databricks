# Fechamento da R02 — revisão dos pilotos e diagnóstico de integração

Data: 12/09/2026. Autor e revisor: ChatGPT (`A0_light`, autorrevisão).
Base de revisão: `0c76bce9f3fa0f52b4312b60c3059e0fd27a2733`.
Escopo: seis READMEs existentes, ajustes documentais pertinentes e diagnóstico.
**Sem merge, R03, publicação Databricks ou aceite humano presumido.**

## Parecer sobre o padrão

As quinze seções do contrato `0.1.0-candidata` atendem aos seis casos do piloto.
Não foi necessário mudar o template, o checklist ou os três exemplares da R01.
A rubrica de oito dimensões foi aplicada a cada piloto e está em
[RUBRICA_FECHAMENTO_R02.json](RUBRICA_FECHAMENTO_R02.json): conceito, escolha,
fidelidade, interpretação, uso seguro, validação, procedência e clareza.

Após os ajustes abaixo, considero o padrão e os pilotos adequados para serem
submetidos ao aceite editorial. Isso é meu parecer, não um teste de compreensão
com usuários e não uma auditoria independente. Manter a versão candidata evita
converter autorização para executar em aprovação dos textos ainda não avaliados.
A limitação funcional identificada no XGBoost continua explícita; o texto não
certifica correção de código só porque a descreve.

A definição deve vir antes da primeira interpretação que depende dela, sem
converter cada seção em um glossário. No piloto simples de formatação, bastou
uma explicação curta da unidade. Nos modelos, foi necessário explicar métricas
e diferenciar verificações implementadas de requisitos exigidos do chamador.
Não houve quota de palavras, alteração de títulos ou duplicação do notebook.

## Achados e ajustes desta rodada

| ID | Achado | Tratamento e estado |
|---|---|---|
| F02-01 | README XGBoost afirmava que o helper exigia duas classes, mas a guarda só testa menos de duas. | Corrigida a afirmação; três classes passaram pela guarda e falharam em `roc_auc_score` no teste real. Lacuna funcional permanece, sem mudança de API. |
| F02-02 | Codificação multiclasse e interpretação das métricas eram pouco explícitas para iniciantes. | Descritos rótulos 0…k−1 no estimador testado; AUC/ROC, Gini, log loss, accuracy e unidade do RMSE esclarecidos. |
| F02-03 | Score/ranking, desvio padronizado, fato/feature/timestamp, view/cache e dimensões de qualidade exigiam repertório não introduzido. | Explicações contextualizadas inseridas, preservando exemplos e profundidade proporcional. |
| F02-04 | Textos de Isolation Forest, PIT e Quick Profile ainda tratavam testes Spark/MLflow como futuros ou não realizados. | Identificado o run suplementar anterior e separado da reexecução local desta revisão. Tracking e Databricks continuam não homologados. |
| F02-05 | Notebook PIT associava genericamente alvo com informação futura a vazamento. | Corrigido somente Markdown: resposta futura pode definir o alvo; vazamento ocorre ao usá-la indevidamente nas características ou avaliação. |
| F02-06 | Título do notebook Quick Profile dizia que com fração 1 os dois valores coincidiam. | Título agora distingue base completa e cardinalidade ainda aproximada, alinhado à explicação que já existia abaixo. |
| F02-07 | Exemplo de formatação sugeria indiferença irrestrita entre compute serverless/clássico. | Separado Python padrão do helper e sessão Spark necessária no preparo; homologação do destino não presumida. |
| F02-08 | Em formatação, pronome ambíguo e pp antes de definir a unidade. | Corrigida a frase sobre leitura de números textuais e introduzidos pontos percentuais no cenário. |
| F02-09 | Main e branches divergem em arquivos compartilhados e usam dois ADRs 0011. | Diagnóstico reproduzido e plano de reconciliação documentado; não houve integração nem renumeração unilateral. |

Os [achados da entrega original](ACHADOS_R02.md) permanecem históricos. Perda de
precisão em inteiros grandes, cortes com empates e escrita persistente no preparo
de EDA continuam documentados; não foram convertidos em comportamentos corrigidos.

## Fontes e leitura do contrato

Foram confrontados os seis READMEs com implementação, fachada quando existente,
notebook e testes pertinentes. O formulário de EDA foi lido sem alterar seus
campos ou bloco colável. As fichas correspondentes do Manual foram conferidas;
não exigiram mudança nesta rodada. Os três exemplares e o checklist foram lidos
para verificar a compatibilidade do padrão, não para homologar sua execução.

Fontes primárias consultadas em 12/09/2026: [interface XGBoost](https://xgboost.readthedocs.io/en/stable/python/sklearn_estimator.html),
[AUC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html),
[log loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html),
[Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html),
[autologging Databricks](https://docs.databricks.com/aws/en/mlflow/databricks-autologging),
[point-in-time](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series),
[cardinalidade Spark 4.0.1](https://spark.apache.org/docs/4.0.1/api/python/reference/pyspark.sql/api/pyspark.sql.functions.approx_count_distinct.html),
[formatação Python 3.13](https://docs.python.org/3.13/library/string.html#format-specification-mini-language),
[contexto Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code)
e [modo agente](https://docs.databricks.com/aws/en/genie-code/agent-mode).
Cada fonte sustenta seu conceito/API, não homologa o wrapper nem o workspace.
As páginas `stable` podem estar à frente dos pacotes testados: a verificação
específica de rótulos desta rodada usa XGBoost 3.1.3, conforme o log, sem atualização
das dependências do projeto.

## Evidência efetivamente executada

| Verificação | Resultado e alcance |
|---|---|
| Gate de baseline, R02 original | Cinco etapas aprovadas; 159 testes aprovados e sete pulados. [Log](evidencias_fechamento_r02/gate_baseline.txt). |
| Suite suplementar R02 reexecutada localmente | 13 casos coletados: sete aprovados e seis pulados por ausência real de PySpark/MLflow. Nenhum módulo falso foi usado. [Log](evidencias_fechamento_r02/pilotos_reexecutados_local.txt). |
| Caracterização adicional de rótulos XGBoost | Três testes aprovados: falha posterior binária com três classes; rejeição de classes iniciadas em 1; sucesso multiclasse com mapeamento 0,1,2. [Script](evidencias_fechamento_r02/verificar_fechamento.py) e [log](evidencias_fechamento_r02/rotulos_xgboost.txt). |
| Preservação | 124 arquivos Python de helpers/testes intactos; seis ASTs/magics/saídas de notebooks iguais; 17 blocos coláveis iguais; 266 arquivos em prefixos protegidos intactos. [Resultado](evidencias_fechamento_r02/preservacao.json). |
| Gate final desta revisão | Cinco etapas aprovadas, 159 testes aprovados e sete pulados. [Log final](evidencias_fechamento_r02/gate_final.txt), capturado após ajustes e renderização; a CI remota posterior será registrada no PR com seu commit. |
| Integração com a main | Somente simulação: quatro conflitos textuais e uma colisão de ADR diagnosticados, sem adotar árvore combinada. [Diagnóstico](DIAGNOSTICO_INTEGRACAO_R02.md). |

As contagens de preservação são grupos com possível sobreposição, não um total
a somar. Os 17 blocos não representam 17 prompts recém-executados. Os três testes
novos caracterizam o contrato atual; passar no caso que espera falha não aprova
a fragilidade como desenho desejável. O aviso preexistente de parsing de datas
na suite da biblioteca permanece distinto dos avisos do validador.

Para reproduzir a caracterização, com dependências equivalentes e a partir da
raiz, use `python docs/sprints/readmes_objetos/evidencias_fechamento_r02/verificar_fechamento.py .`.
Para a preservação: `python docs/sprints/readmes_objetos/evidencias_fechamento_r02/verificar_preservacao.py .`.
Esses scripts pertencem ao registro da revisão, não foram incluídos nos gates
permanentes nem no pacote operacional do Hub.

A execução real anterior com 13/13 testes, PySpark e MLflow instalados, foi
conferida nos logs do pacote R02 e no [run 34696720982](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/actions/runs/34696720982).
Ela não foi recontada como nova execução desta revisão. Não foram executados
notebooks completos, escrita persistente da EDA, tracking remoto, Databricks,
Spark Connect, Unity Catalog ou teste conversacional da Genie Code.

## Matriz nominal das alterações

<!-- MATRIZ_INICIO -->

34 caminhos líquidos: seis READMEs revisados, nenhum novo README operacional.

| Caminho | Categoria | Mudança e motivo |
|---|---|---|
| `CHANGELOG.md` | Documentação atualizada | Entrada aditiva do fechamento; histórico anterior intacto. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_prompts/eda_rapida/README.md` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_scripts/quick_profile/README.md` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/constants/format_br/README.md` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/isolation_forest/README.md` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/train_xgboost/README.md` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/spark/pit_join/README.md` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py` | Derivado | Cópia do arquivo da fonte, gerada exclusivamente por render_simulado.py --write. |
| `README.md` | Documentação atualizada | Somente contagens reais do gate local; publicação remota histórica preservada. |
| `ambiente_fonte/.assistant/hub_prompts/eda_rapida/README.md` | README piloto revisado | Seções 3 e 6: dimensões de qualidade e unicidade explicadas. |
| `ambiente_fonte/.assistant/hub_scripts/quick_profile/README.md` | README piloto revisado | Seções 5, 7, 9 e 15: cache, view e procedência da execução Spark. |
| `ambiente_fonte/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py` | Notebook: somente Markdown | Esclarecimento conceitual/ambiente; AST, magics executáveis e transcrições preservados. |
| `ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md` | README piloto revisado | Seções 4 e 6: pronome, entrada textual e definição de pontos percentuais. |
| `ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py` | Notebook: somente Markdown | Esclarecimento conceitual/ambiente; AST, magics executáveis e transcrições preservados. |
| `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/README.md` | README piloto revisado | Abertura e seções 1, 8, 11, 14–15: termos, perfil e procedência. |
| `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/README.md` | README piloto revisado | Seções 6–8 e 15: métricas, classes e limite da guarda; evidências. |
| `ambiente_fonte/.assistant/hub_snippets/spark/pit_join/README.md` | README piloto revisado | Seções 1, 11 e 15: papéis das tabelas, alvo versus atributo futuro e evidência Spark. |
| `ambiente_fonte/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py` | Notebook: somente Markdown | Esclarecimento conceitual/ambiente; AST, magics executáveis e transcrições preservados. |
| `docs/sprints/readmes_objetos/CHECKPOINT_R02.md` | Documentação atualizada | Adendo datado: revisão, diagnóstico e aceites ainda pendentes. |
| `docs/sprints/readmes_objetos/DIAGNOSTICO_INTEGRACAO_R02.md` | Documento novo | Quatro conflitos, ADR duplicado, gates a preservar e plano sem executar merge. |
| `docs/sprints/readmes_objetos/README.md` | Documentação atualizada | Índice da iniciativa aponta à revisão e ao diagnóstico. |
| `docs/sprints/readmes_objetos/REVISAO_FECHAMENTO_R02.md` | Documento novo | Parecer, achados, matriz nominal e critérios de continuidade. |
| `docs/sprints/readmes_objetos/RUBRICA_FECHAMENTO_R02.json` | Registro novo | 48 avaliações editoriais próprias com evidência, sem nota compensatória. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/diagnostico_merge_r01.txt` | Evidência nova | Log literal ou resultado estruturado de teste/diagnóstico; não equivale a homologação. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/diagnostico_merge_r02.txt` | Evidência nova | Log literal ou resultado estruturado de teste/diagnóstico; não equivale a homologação. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/gate_baseline.txt` | Evidência nova | Log literal ou resultado estruturado de teste/diagnóstico; não equivale a homologação. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/gate_final.txt` | Evidência nova | Log literal ou resultado estruturado de teste/diagnóstico; não equivale a homologação. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/pilotos_reexecutados_local.txt` | Evidência nova | Log literal ou resultado estruturado de teste/diagnóstico; não equivale a homologação. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/preservacao.json` | Evidência nova | Log literal ou resultado estruturado de teste/diagnóstico; não equivale a homologação. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/rotulos_xgboost.txt` | Evidência nova | Log literal ou resultado estruturado de teste/diagnóstico; não equivale a homologação. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/verificar_fechamento.py` | Script de evidência novo | Reprodução de caracterização ou preservação; fora dos gates permanentes. |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/verificar_preservacao.py` | Script de evidência novo | Reprodução de caracterização ou preservação; fora dos gates permanentes. |

<!-- MATRIZ_FIM -->

A matriz é relativa à R02 original, não à main. Cada cópia gerada corresponde
à fonte revisada e não conta como um novo texto de autoria. O workflow temporário
`readmes-r02-revisao-base.yml`, usado para recuperar as bases com credenciais de
checkout desabilitadas, não compõe a árvore final. Commits preparatórios permanecem
no histórico; nenhum force-push foi usado. O histórico anterior do changelog foi
preservado após uma inserção aditiva.

## Documentos inspecionados e preservados

Template, checklist, exemplares da R01, regras editoriais, skills/instruções,
Manual e suas três cópias, implementação/fachadas dos helpers, formulário de EDA,
controle de migração, imagens e ferramentas/gates permanentes não receberam
mudanças nesta revisão. A main, a branch R01 e o Concierge integrado não foram
substituídos. Registros anteriores das R01/R02 conservaram as evidências originais;
o checkpoint recebeu uma atualização datada, não um aceite retroativo.

## Decisão de continuidade

Recomendo submeter os seis textos e o padrão existente ao aceite editorial.
Permanece `0.1.0-candidata`, sem renumerar ADR nesta branch isolada ou registrar
aprovação humana inexistente. A cobertura continua 6/74, com 68 pendências e os
três exemplares anteriores. A R03 não começou.

A integração exige outra decisão explícita e a reconciliação descrita no
diagnóstico, preservando as três etapas do Concierge e a etapa dos READMEs.
Uma CI verde deste PR contra R01 não remove esse bloqueio com a main.
Antes de distribuição à squad, cumprir a auditoria independente aplicável;
esta autorrevisão não substitui esse requisito.
