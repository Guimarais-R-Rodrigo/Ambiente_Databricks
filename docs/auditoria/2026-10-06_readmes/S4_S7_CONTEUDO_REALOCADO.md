# Conteúdo de manutenção realocado: prompts, scripts e templates

Registro de proveniência da revisão documental de 06/10/2026 (Codex).
Os trechos abaixo são transcrições históricas da baseline, não instruções de uso
vigentes nem execução realizada nesta revisão. Links dentro das transcrições
permanecem texto; a URL de origem de cada bloco preserva a navegação no contexto
original. A implementação e os exemplos atuais permanecem donos do uso.

## ambiente_fonte/.assistant/hub_prompts/auditoria_skills/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/auditoria_skills/README.md).

```text
A descrição foi confrontada com [auditoria_skills.md](auditoria_skills.md) e [exemplo_auditoria_skills.py](exemplo_auditoria_skills.py) na base R11. Para comportamento atual de Genie Code, Agent Skills e instruções, consulte a documentação oficial do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/baseline_orchestration/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/baseline_orchestration/README.md).

```text
A descrição foi confrontada com [baseline_orchestration.md](baseline_orchestration.md) e [exemplo_baseline_orchestration.py](exemplo_baseline_orchestration.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/comentar_notebook/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/comentar_notebook/README.md).

```text
A descrição foi confrontada com [comentar_notebook.md](comentar_notebook.md) e [exemplo_comentar_notebook.py](exemplo_comentar_notebook.py) na base R11. Para comportamento atual de Genie Code, Agent Skills e instruções, consulte a documentação oficial do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/comparar_tabelas/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/comparar_tabelas/README.md).

```text
O comportamento local descrito aqui foi confrontado com [comparar_tabelas.md](comparar_tabelas.md) e [exemplo_comparar_tabelas.py](exemplo_comparar_tabelas.py) na base R10 iniciada a partir do merge R09. O prompt e o notebook não foram executados no Databricks nesta revisão.

Para a seleção de contexto no Genie Code, consulte a documentação oficial [Navigate Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code), consultada em 13/09/2026. Ela documenta anexos e seleção de recursos com `@`; não homologa este prompt customizado.
```

## ambiente_fonte/.assistant/hub_prompts/cross_eda/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/cross_eda/README.md).

```text
A descrição local foi confrontada com [cross_eda.md](cross_eda.md) e [exemplo_cross_eda.py](exemplo_cross_eda.py). Esta revisão foi estática e não executou o notebook nem uma conversa real com Genie Code.

Para seleção de recursos no Genie Code, consulte [Navigate Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code). Para o conceito de point-in-time, consulte [Point-in-time feature joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series). Consultadas em 13/09/2026.
```

## ambiente_fonte/.assistant/hub_prompts/data_quality/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/data_quality/README.md).

```text
A descrição local foi confrontada com [data_quality.md](data_quality.md) e [exemplo_data_quality.py](exemplo_data_quality.py). Esta revisão foi estática.

A documentação oficial [Manage data quality with pipeline expectations](https://docs.databricks.com/aws/en/ldp/expectations), consultada em 13/09/2026, descreve expectations e suas políticas de tratamento no Lakeflow. Ela sustenta a capacidade de plataforma, não valida regras específicas deste prompt.
```

## ambiente_fonte/.assistant/hub_prompts/descobrir_micromodelos/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/descobrir_micromodelos/README.md).

```text
Progressividade, binding, `ESCOPO_OBSERVADO` e estados parciais seguem o contrato
MM03 no repositório de desenvolvimento. A especificação posterior segue schema
MM01. A seleção da skill foi confirmada pelo usuário em chat manual no Free;
transcrição e notebook de resposta foram avaliados, sem auditoria completa de
chamadas internas. Runtime Databricks e MM01 permanecem não executados neste
teste; a evidência conversacional não certifica MM04.
```

## ambiente_fonte/.assistant/hub_prompts/eda_completa/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/eda_completa/README.md).

```text
A descrição local foi confrontada com [eda_completa.md](eda_completa.md) e [exemplo_eda_completa.py](exemplo_eda_completa.py). Esta revisão foi estática e não executou o notebook nem uma interação do Genie Code.

Para seleção de recursos no Genie Code, consulte [Navigate Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code), consultada em 13/09/2026.
```

## ambiente_fonte/.assistant/hub_prompts/eda_rapida/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/eda_rapida/README.md).

```text
O formulário e o notebook vinculados sustentam o contrato local, revisado na base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`, em 12/09/2026. Os blocos coláveis foram preservados; não foi executada a interação Genie Code nem a escrita persistente da demonstração.

As páginas oficiais de [navegação do Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code) e [modo agente](https://docs.databricks.com/aws/en/genie-code/agent-mode), consultadas em 12/09/2026, fundamentam as distinções de contexto e execução. Elas descrevem a plataforma, não homologam este prompt customizado.
```

## ambiente_fonte/.assistant/hub_prompts/explainability/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/explainability/README.md).

```text
A descrição foi confrontada com [explainability.md](explainability.md) e [exemplo_explainability.py](exemplo_explainability.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/feature_engineering/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/feature_engineering/README.md).

```text
A descrição local foi confrontada com [feature_engineering.md](feature_engineering.md) e [exemplo_feature_engineering.py](exemplo_feature_engineering.py). Esta revisão foi estática.

A documentação oficial [Databricks Feature Store](https://docs.databricks.com/aws/en/machine-learning/feature-store) descreve recursos governados em Unity Catalog, e [Point-in-time feature joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series) descreve joins temporais para evitar uso de valores futuros. Consultadas em 13/09/2026.
```

## ambiente_fonte/.assistant/hub_prompts/micromodelo_novo/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/micromodelo_novo/README.md).

```text
Contrato e fases: MM01 `micromodelo.schema.json` e `ESTADOS_E_PROVENIENCIA.md`
no repositório de desenvolvimento. Progressividade e limites de metadata: contrato
MM03. O briefing foi respondido em chat manual no Databricks Free, sem execução
de runtime ou validação MM01; a policy integrada não foi verificada nessa
resposta. A evidência conversacional não certifica MM04.
```

## ambiente_fonte/.assistant/hub_prompts/monitoramento_modelo/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/monitoramento_modelo/README.md).

```text
A descrição foi confrontada com [monitoramento_modelo.md](monitoramento_modelo.md) e [exemplo_monitoramento_modelo.py](exemplo_monitoramento_modelo.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/novo_projeto/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/novo_projeto/README.md).

```text
A descrição foi confrontada com [novo_projeto.md](novo_projeto.md) e [exemplo_novo_projeto.py](exemplo_novo_projeto.py) na base R11. Para comportamento atual de Genie Code, Agent Skills e instruções, consulte a documentação oficial do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/pipeline/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/pipeline/README.md).

```text
A descrição foi confrontada com [pipeline.md](pipeline.md) e [exemplo_pipeline.py](exemplo_pipeline.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/safra/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/safra/README.md).

```text
A descrição foi confrontada com [safra.md](safra.md) e [exemplo_safra.py](exemplo_safra.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/stat_check/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/stat_check/README.md).

```text
A descrição local foi confrontada com [stat_check.md](stat_check.md) e [exemplo_stat_check.py](exemplo_stat_check.py). Esta revisão foi estática e não executou o notebook nem a interação do Genie Code.

Para seleção de recursos no Genie Code, consulte [Navigate Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code), consultada em 13/09/2026.
```

## ambiente_fonte/.assistant/hub_prompts/tutor_explicar/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/tutor_explicar/README.md).

```text
A descrição foi confrontada com [tutor_explicar.md](tutor_explicar.md) e [exemplo_tutor_explicar.py](exemplo_tutor_explicar.py) na base R11. Para comportamento atual de Genie Code, Agent Skills e instruções, consulte a documentação oficial do Databricks antes de operar em produção.
```

## ambiente_fonte/.assistant/hub_prompts/eda_rapida/exemplo_eda_rapida.py

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/eda_rapida/exemplo_eda_rapida.py).

```text
# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas históricas abaixo foram preservadas; a revisão R02 não as transforma em execução recente.
# MAGIC **Nota R02 sobre o registro acima:** a falta de execução é deste exemplo.
# MAGIC A frase histórica sobre nenhum job reproduzir a interação não descreve
# MAGIC todas as capacidades atuais: existe [tarefa Genie Code para jobs](https://docs.databricks.com/aws/en/jobs/tasks/genie-code), em Beta.
# MAGIC Esta sprint não configura nem executa essa tarefa; preserva o bloco como registro histórico.
```

## ambiente_fonte/.assistant/hub_prompts/comentar_notebook/exemplo_comentar_notebook.py

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/comentar_notebook/exemplo_comentar_notebook.py).

```text
# MAGIC **Como ler.** O alvo é um notebook real que você pode abrir ao lado. O estado atual do repositório já exige saída colada nos exemplos; o exercício aqui avalia clareza documental, não uma dívida antiga de outputs.
```

## ambiente_fonte/.assistant/hub_prompts/descobrir_micromodelos/exemplo_descobrir_micromodelos.py

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/descobrir_micromodelos/exemplo_descobrir_micromodelos.py).

```text
# MAGIC ## Parte 3 — resposta real e limites
# MAGIC
# MAGIC Capturada em 29 set 2026 no Genie Code Free, com carregamento da skill
# MAGIC confirmado pelo usuário. A transcrição tem SHA-256
# MAGIC `7ae1b9679881f7d34ecdd5466533133627989fc98151b3ea3134bb7d2d72081e`.
# MAGIC O notebook `x2.ipynb` entregue como evidência tem SHA-256
# MAGIC `c75a3bceb43c52164addc2d073a0cb072968439d5c604c5d12aba85c334757b8`.
# MAGIC Os arquivos brutos permanecem fora do Git.
# MAGIC
# MAGIC - A resposta consultou a entrada de `hub-ml-micromodelos` na policy integrada
# MAGIC   e declarou `current_level=L1`, `target_level=L3`, `rollout_mode=audit`.
# MAGIC - Classificou o chat como E1, a fixture textual como `FORNECIDA`,
# MAGIC   `ESCOPO_OBSERVADO` vazio e runtime E1 não executado.
# MAGIC - Propôs três candidatas para revisão humana, sem detecção de fraude ou
# MAGIC   fabricação; marcou viabilidade, qualidade temporal e leakage
# MAGIC   `INDETERMINADO`, sem score, YAML ou publicação alegados.
# MAGIC - Ressalvas: chamou as candidatas de “viáveis” em uma passagem apesar da
# MAGIC   viabilidade indeterminada; escreveu seis células Markdown no notebook,
# MAGIC   embora o roteiro de teste pedisse resposta no chat. O arquivo ainda contém
# MAGIC   uma célula de código vazia, com zero execuções e zero outputs.
# MAGIC - Veredito: PASS para as guardas centrais e a correção E1/policy, com
# MAGIC   ressalvas editoriais e de formato. A transcrição não audita todas as
# MAGIC   chamadas internas do Genie nem certifica MM04.
# MAGIC
# MAGIC A avaliação completa está em
# MAGIC `docs/sprints/micromodelos/TESTE_BRIEFINGS_MM04_E1.md`.

```

## ambiente_fonte/.assistant/hub_prompts/micromodelo_novo/exemplo_micromodelo_novo.py

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/micromodelo_novo/exemplo_micromodelo_novo.py).

```text
# MAGIC ## Parte 3 — resposta real e limites
# MAGIC
# MAGIC Capturada em 29 set 2026 no Genie Code Free, com seleção e carregamento da
# MAGIC skill declarados pelo usuário. A transcrição bruta tem SHA-256
# MAGIC `d9b0600aa1184ca62e3cb95393eab2c91499f9b90d221fe9482d1b8b961eaa8a`
# MAGIC e permanece fora do Git.
# MAGIC
# MAGIC - Rota observável na transcrição: carregamento de `hub-ml-micromodelos`.
# MAGIC   Não há captura independente do indicador do menu.
# MAGIC - A resposta registrou `YAML_NAO_CRIADO`, `MM01_NAO_VALIDADO` e
# MAGIC   `SCORE_INDETERMINADO`; não alegou consulta a registros ou publicação.
# MAGIC - Ressalva: alguns campos vindos do briefing foram chamados de `OBSERVADO`,
# MAGIC   quando a proveniência correta é `FORNECIDA`. A policy integrada não foi
# MAGIC   verificada de forma independente nessa resposta; a leitura do contrato
# MAGIC   estático não substitui `policy.json`.
# MAGIC - Veredito do conteúdo guardado: PASS com ressalvas. Não é validação MM01,
# MAGIC   execução do runtime E1, certificação MM04 ou aceite humano.
# MAGIC
# MAGIC A avaliação completa está em
# MAGIC `docs/sprints/micromodelos/TESTE_BRIEFINGS_MM04_E1.md`.

```

## ambiente_fonte/.assistant/hub_scripts/data_quality_check/README.md

Nota de curadoria (06/10/2026): a evidência histórica navegável é o [Relatório R04-B](../../sprints/readmes_objetos/RELATORIO_R04B.md). O trecho original abaixo conserva o estado em que foi escrito; a referência não alega reexecução nesta revisão.

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/data_quality_check/README.md).

```text
O contrato específico é sustentado pela implementação, fachada e notebook vinculados acima, revisados na R04-B em 12/09/2026. O texto foi confrontado com o comportamento do código; revisão pelo próprio autor não é auditoria independente.

A documentação Databricks de [boas práticas de governança e qualidade](https://docs.databricks.com/aws/en/lakehouse-architecture/data-governance/best-practices) e de [patterns de expectations](https://docs.databricks.com/aws/en/ldp/expectation-patterns) sustenta a distinção entre diagnóstico ad hoc e regra de pipeline. Fontes consultadas em 12/09/2026.

A validação específica da R04-B, incluindo Spark real, é registrada no relatório da sprint após a execução. Não há, nesta redação, alegação de publicação ou homologação em workspace Databricks.
```

## ambiente_fonte/.assistant/hub_scripts/doc_coverage/README.md

Nota de curadoria (06/10/2026): a evidência histórica navegável é o [Relatório R04-B](../../sprints/readmes_objetos/RELATORIO_R04B.md). O trecho original abaixo conserva o estado em que foi escrito; a referência não alega reexecução nesta revisão.

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/doc_coverage/README.md).

```text
O contrato deste recurso vem da implementação, fachada e exemplo locais, revisados na R04-B em 12/09/2026. Não há dependência de documentação externa para a fórmula local.

O formato-fonte reconhecido é o que a implementação codifica hoje; isso não deve ser generalizado como especificação eterna de exportação Databricks. A validação específica da R04-B é registrada no relatório da sprint após execução.

Revisão do próprio texto não é auditoria independente; nenhuma alegação de publicação ou homologação Databricks é feita.
```

## ambiente_fonte/.assistant/hub_scripts/drift_detector/README.md

Nota de curadoria (06/10/2026): a evidência histórica navegável é o [Relatório R04-B](../../sprints/readmes_objetos/RELATORIO_R04B.md). O trecho original abaixo conserva o estado em que foi escrito; a referência não alega reexecução nesta revisão.

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/drift_detector/README.md).

```text
O comportamento específico foi conferido na implementação e no exemplo locais durante a R04-B em 12/09/2026. O Apache Spark documenta [`DataFrame.approxQuantile`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.approxQuantile.html), incluindo o papel do erro relativo; essa API sustenta o cálculo dos limites, não os limiares de PSI.

Os thresholds de monitoramento permanecem política local. A validação da R04-B registra a execução com Spark real após o fechamento técnico. Revisão do próprio autor não é auditoria independente nem homologação Databricks.
```

## ambiente_fonte/.assistant/hub_scripts/naming_checker/README.md

Nota de curadoria (06/10/2026): a evidência histórica navegável é o [Relatório R04-B](../../sprints/readmes_objetos/RELATORIO_R04B.md). O trecho original abaixo conserva o estado em que foi escrito; a referência não alega reexecução nesta revisão.

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/naming_checker/README.md).

```text
O comportamento específico é sustentado pelos arquivos locais vinculados acima, revisados na R04-B em 12/09/2026. A documentação Databricks de [consulta a tabelas](https://docs.databricks.com/aws/en/query) descreve o namespace de três níveis do Unity Catalog e recomenda identificadores totalmente qualificados em cenários com múltiplos catálogos/schemas. Fonte consultada em 12/09/2026.

As regras de `snake_case`, comprimento e prefixos continuam sendo política deste projeto/organização, não exigência oficial. A validação de runtime da sprint é registrada separadamente; não há auditoria independente ou homologação Databricks.
```

## ambiente_fonte/.assistant/hub_scripts/quick_profile/README.md

Nota de curadoria (06/10/2026): consulte o [Relatório R02](../../sprints/readmes_objetos/RELATORIO_R02.md) e o [run suplementar histórico com Spark](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/actions/runs/34696720982). A prova pertence ao cenário e à data registrados, sem reexecução atual presumida.

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/quick_profile/README.md).

```text
A implementação e o notebook vinculados acima sustentam o contrato específico, revisado na base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`, em 12/09/2026. As evidências de revisão e execução ficam no relatório R02; nenhum resultado de um workspace foi recertificado por esta redação.

A documentação Apache Spark de [amostragem](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.sample.html) sustenta a distinção entre fração pedida e amostra obtida. A de [contagem aproximada distinta](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.approx_count_distinct.html) sustenta o caráter estimado da cardinalidade. Fontes consultadas em 12/09/2026; os limites de dez ou cinco colunas vêm do código do Hub, não dessas APIs.

Na [execução suplementar da R02 em 12/09/2026](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/actions/runs/34696720982), testes com PySpark 4.0.1 real conferiram campos de retorno, contagens, nulos e recusas sobre uma view temporária sintética. O ambiente local da revisão de fechamento não possui PySpark; a evidência anterior permanece identificada, sem alegação de reexecução local. Revisão do texto pelo próprio autor não é auditoria independente nem aceite humano.
```

## ambiente_fonte/.assistant/hub_scripts/rfv_calculator/README.md

Nota de curadoria (06/10/2026): a evidência histórica navegável é o [Relatório R04-B](../../sprints/readmes_objetos/RELATORIO_R04B.md). O trecho original abaixo conserva o estado em que foi escrito; a referência não alega reexecução nesta revisão.

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/rfv_calculator/README.md).

```text
O contrato específico é sustentado pelos arquivos locais vinculados, revisados na R04-B em 12/09/2026. A semântica de datas, `datediff`, `date_sub`, agregações e joins segue Apache Spark; os detalhes usados aqui estão explícitos na implementação.

A validação da sprint inclui casos sintéticos com Spark real para corte temporal e janelas. Revisão do texto pelo próprio autor não é auditoria independente nem homologação no Databricks.
```

## ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/README.md

Nota de curadoria (06/10/2026): a evidência histórica navegável é o [Relatório R04-B](../../sprints/readmes_objetos/RELATORIO_R04B.md). O trecho original abaixo conserva o estado em que foi escrito; a referência não alega reexecução nesta revisão.

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/README.md).

```text
O contrato local foi revisado na implementação e no notebook durante a R04-B em 12/09/2026. A documentação Apache Spark de [`approx_count_distinct`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.approx_count_distinct.html) sustenta o caráter aproximado da cardinalidade.

A especificação [YAML 1.2](https://yaml.org/spec/1.2.1/) registra JSON como subconjunto oficial, base do fallback implementado. Fontes consultadas em 12/09/2026.

A validação de runtime da R04-B é registrada após execução. Revisão do próprio autor não é auditoria independente nem publicação/homologação Databricks.
```

## ambiente_fonte/.assistant/hub_scripts/skill_execution/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/skill_execution/README.md).

````text
- [skill_execution.py](skill_execution.py): preflight L2.
- [receipt/__init__.py](receipt/__init__.py): Receipt SE04.
- [postflight/__init__.py](postflight/__init__.py): Postflight SE05.
- [__init__.py](__init__.py): fachada pública histórica do preflight.
- [exemplo_skill_execution.py](exemplo_skill_execution.py): exemplo operacional.
- `skills/hub-ml-eda-profissional/scripts/run.py`: core L3.
- `skills/hub-ml-eda-profissional/scripts/run_enforced.py`: executor L4.
- `skills/hub-ml-eda-profissional/scripts/postflight.py`: finalizador fail-closed.
- `skills/hub-ml-eda-profissional/release_manifest.json`: fingerprints da release.
- `docs/sprints/skill_enforcement/SE05/`: desenho, testes e runbook.

Próximo estágio arquitetural após a SE05: SE06 amplia evals repetidos/adversariais e calibra falsos bloqueios/escapes.

## 15. Referências

- `docs/decisions/ADR-0021-execucao-verificavel-de-skills.md`;
- `docs/sprints/skill_enforcement/PLANO_MESTRE.md`;
- `docs/sprints/skill_enforcement/REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`;
- `docs/sprints/skill_enforcement/SE04/DESENHO_TECNICO.md`;
- `docs/sprints/skill_enforcement/SE05/DESENHO_TECNICO.md`;
- testes `tools/tests/test_skill_enforcement_se03.py`, `test_skill_enforcement_se04.py`, `test_skill_enforcement_se04_runner.py`, `test_skill_enforcement_se05.py` e `test_skill_enforcement_se05_runner.py`.

Estado desta revisão: implementação SE05 presente na branch de desenvolvimento; certificação oficial local/Free permanece gate separado antes de release candidate.


## Política transversal SE07

A SE07 adiciona um registry publicado para as 14 skills:

`hub_padroes/skill_enforcement/policy.json`

Consulta:

```python
from hub_scripts.skill_execution import get_skill_enforcement_policy

policy = get_skill_enforcement_policy("hub-ml-auditoria-skills")
```

`current_level` é evidence-based. `target_level` é roadmap. A API é somente leitura e não executa helpers, não cria Receipt e não promove uma skill de nível.
````

## ambiente_fonte/.assistant/hub_scripts/skill_execution/domain_context/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/skill_execution/domain_context/README.md).

```text
Comportamento sustentado pelos arquivos locais acima e pelo plano B1 do repositório. Estado: testes de domínio em overlay Linux; integração completa com checkout, renderer e ambiente de campanha ainda pendente.
```

## ambiente_fonte/.assistant/hub_prompts/README.md: migração editorial

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_prompts/README.md).

```text
Cada objeto novo inclui um `README.md` para explicar conceito, contexto e
limites antes do exemplo. A migração dos legados é gradual. O
[contrato editorial](../hub_padroes/readme/template_objeto.md) padroniza essa
leitura; o Manual continua sendo o catálogo integrado. Leia o aviso de efeitos
do exemplo: ele pode escrever mesmo quando o helper apenas lê.

No piloto R02, o [guia de eda_rapida](eda_rapida/README.md) explica quando
usar o briefing e como avaliar sua resposta. Leia também o aviso de overwrite
do notebook: o preparo escreve uma tabela, separadamente do pedido de leitura.
```

## ambiente_fonte/.assistant/hub_scripts/README.md: migração editorial

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/README.md).

```text
Cada objeto novo inclui um `README.md` para explicar conceito, contexto e
limites antes do exemplo. A migração dos legados é gradual. O
[contrato editorial](../hub_padroes/readme/template_objeto.md) padroniza essa
leitura; o Manual continua sendo o catálogo integrado. Leia o aviso de efeitos
do exemplo: ele pode escrever mesmo quando o helper apenas lê.

No piloto R02, o [guia de quick_profile](quick_profile/README.md) explica
o que vem da tabela inteira e o que vem da amostra, além dos limites de
cardinalidade e da possível exposição de categorias sensíveis.
```

## ambiente_fonte/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py: proveniência histórica

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py).

````text
# MAGIC **Antes de usar:** veja o [README do objeto](README.md) para conceito, requisitos, efeitos e interpretação. As saídas históricas abaixo foram preservadas; a revisão R02 não as transforma em execução recente.
````

## ambiente_fonte/.assistant/hub_scripts/skill_execution/exemplo_skill_execution.py: proveniência histórica

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/skill_execution/exemplo_skill_execution.py).

````text
# MAGIC ## Invariantes já reproduzidos pela suíte SE02
# MAGIC
# MAGIC O happy path automatizado executado no GitHub Actions confirmou estes
# MAGIC invariantes. Este bloco não é uma captura do Databricks Free; a homologação
# MAGIC remota permanece um gate separado da sprint.
# MAGIC
# MAGIC ```text
# MAGIC status=PASS
# MAGIC blocking_issues=0
# MAGIC writes_performed=False
# MAGIC ```

````

