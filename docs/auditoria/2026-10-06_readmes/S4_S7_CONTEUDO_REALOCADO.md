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

### Excerto adicional da baseline, linhas 54–54

````text
Abra [comentar_notebook.md](comentar_notebook.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_comentar_notebook.py) demonstra o preenchimento. O exemplo apenas lê `exemplo_pit_join.py`; o estado atual já exige saída colada nos notebooks de exemplo.
````

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

### Excerto adicional da baseline, linhas 78–80

````text
O [notebook](exemplo_eda_rapida.py) tem preparo sintético, um pedido preenchido e um espaço para registrar a interação real. O preparo chama `write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes")`: pode substituir uma tabela existente. **Não execute esse preparo em recurso compartilhado sem autorização específica e conferência do destino.** Um ambiente de teste não torna qualquer nome seguro por definição.

O limite de não escrever, presente no prompt, não protege contra a escrita das células preparatórias do notebook. Você pode estudar o formulário e o cenário sem executar essas células. A resposta real de Genie Code permanece marcada como não executada no exemplo; esta sprint não simula essa interação nem preenche a lacuna com uma resposta inventada.
````

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

### Excerto adicional da baseline, linhas 54–54

````text
Abra [monitoramento_modelo.md](monitoramento_modelo.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_monitoramento_modelo.py) demonstra o preenchimento. O código do exemplo sobrescreve `hub_exemplo_monitor_ref` e `hub_exemplo_monitor_atual`; a prosa antiga citava outro nome.
````

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

### Excerto adicional da baseline, linhas 5–5

````text
`hub_scripts.skill_execution` é a camada determinística do Skill Enforcement Framework usada pela skill piloto `hub-ml-eda-profissional`. Ela reúne o preflight L2, o `ExecutionReceiptV1` da SE04 e, na SE05, o `PostflightV1` que decide se uma execução pode ser homologada como concluída com aderência ao contrato.
````

## ambiente_fonte/.assistant/hub_scripts/skill_execution/domain_context/README.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_scripts/skill_execution/domain_context/README.md).

```text
Comportamento sustentado pelos arquivos locais acima e pelo plano B1 do repositório. Estado: testes de domínio em overlay Linux; integração completa com checkout, renderer e ambiente de campanha ainda pendente.
```

### Excerto adicional da baseline, linhas 1–3

````text
# domain_context — validação estrita de contexto para SER03/SER05

Componente interno candidato do `hub_scripts.skill_execution`; não substitui o preflight ou o Receipt canônicos.
````

### Excerto adicional da baseline, linhas 27–29

````text
## 3. Quando faz sentido usar?

Nos dois perfis candidatos B1: safra mensal binária e cross-EDA L2. O owner temporal é único; uma futura adoção por feature engineering requer integração e testes próprios.
````

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

### Excerto adicional da baseline, linhas 75–92

````text
O catálogo reúne os sete utilitários históricos de qualidade, estabilidade, transformação e governança técnica, além do objeto transversal `skill_execution`, introduzido pelo Skill Enforcement Framework para resolver pré-condições antes do core analítico. Todos são executados sob demanda e cada um preserva seu próprio contrato de retorno.

![Bancada dos Hub Scripts com sete ferramentas executadas sob demanda, agrupadas em qualidade, estabilidade, transformação analítica e governança técnica.](../hub_readmes_visual_assets/readmes/scripts/png/02_catalogo_diagnosticos.png)

*Leitura da figura: qualidade e perfil, estabilidade, transformação analítica e governança técnica respondem a necessidades diferentes.*

**Equivalente textual da figura:** `data_quality_check` e `quick_profile` inspecionam qualidade e perfil; `drift_detector` compara distribuições; `rfv_calculator` constrói features RFV; `schema_to_yaml`, `naming_checker` e `doc_coverage` apoiam governança técnica. A figura retrata esses sete objetos históricos; `skill_execution` é um oitavo objeto transversal acrescentado depois dela. Os tipos de retorno estão explícitos no catálogo abaixo.

---

### 🛡️ 0. Preflight e Governança de Execução

#### `skill_execution` — Preflight do Contrato de Skill

- **Guia local:** [skill_execution: guia local](skill_execution/README.md)
- **O que faz:** lê um `execution_contract.json`, avalia condições objetivas e resolve APIs públicas/templates aplicáveis antes do core analítico.
- **O que retorna:** `PreflightResult` estruturado com `PASS` ou `BLOCKED`, decisões por item, issues bloqueantes e `writes_performed=false`.
- **Quando usar:** antes de uma execução protegida pelo Skill Enforcement Framework. Na SE02, não executa a EDA, não chama helpers analíticos e não substitui runner, receipt ou postflight.
````

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


## Snapshots históricos realocados dos templates

As transcrições seguintes preservam a proveniência da separação entre uso e
manutenção. Instruções, limiares e estados pré-preenchidos abaixo são o conteúdo
anterior da baseline, não o contrato vigente de preenchimento. O checklist de
contribuição atual tem destino `docs/manutencao/CHECKLIST_OBJETO_NOVO.md`; os templates
operacionais continuam nos caminhos originais. Nenhum snapshot autoriza execução.

### ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).

````text
# Checklist — objeto novo do Hub

Cole numa PR, num chamado ou no fim do notebook de trabalho.

**A lista está dividida em duas naturezas**, e a distinção não é formalidade:
o primeiro grupo um terceiro consegue conferir sozinho, sem conversar com quem
escreveu; o segundo é juízo de quem escreveu, e vale como declaração, não como
prova. Um checklist que promete verificação e entrega opinião ensina a marcar
tudo — e aí as linhas boas perdem força junto.

Este é o checklist **canônico**. Os templates de `hub_padroes/` apontam para cá
em vez de repetir a lista.

---

> **Sobre os comandos deste checklist.** `tools/validate_assistant.py`,
> `tools/api_publica.py` e `tools/spark_smoke_test.py` vivem **no repositório**,
> não no workspace — eles não são publicados com o `.assistant/`. Quem estiver só
> no Genie Code marca os itens que dependem deles como "a conferir no
> repositório" e avisa quem for commitar.

## Parte 1 — verificável por terceiro

### Comum a todos os tipos

- [ ] O tipo é um dos seis: snippet, script, prompt, README, notebook, skill
      (`auditoria/` é molde de processo, não conta)
- [ ] Nenhum objeto do `MANUAL_TECNICO.md#catalogo-helpers` atende à mesma demanda
- [ ] `python tools/validate_assistant.py` aprovado
- [ ] O inventário de `MANUAL_TECNICO.md` ganhou a ficha, com API e dependências conferidas
- [ ] Entrada no `CHANGELOG.md`

### Se é snippet, script ou prompt

- [ ] Existe `README.md` com o [contrato de objeto](../../../hub_padroes/readme/template_objeto.md)
- [ ] O [checklist editorial](../../../hub_padroes/readme/checklist_objeto.md) foi aplicado e tem evidência
- [ ] README e notebook têm links recíprocos; efeitos do exemplo estão explícitos
- [ ] Em migração, a dispensa temporária foi removida; nenhuma implementação mudou

### Se é snippet ou script

- [ ] Nome em `snake_case`, identificador Python válido
- [ ] Snippet mora em `hub_snippets/<secao>/<nome>/`; script mora em
      `hub_scripts/<nome>/`, **sem** nível de seção
- [ ] O módulo se chama **como a pasta**: `pit_join/pit_join.py`
- [ ] Existe `exemplo_<nome>.py`, mesmo que o objeto seja trivial
- [ ] **`exemplo_<nome>.py` abre com `# Databricks notebook source`**
- [ ] `__init__.py` idêntico à saída de `python tools/api_publica.py`
- [ ] Docstring da função tem `Args`, `Returns` e `Raises` (e `Note`, se houver
      armadilha)
- [ ] Sem `cache()`/`persist()` desprotegido, sem `toPandas()` sem limite, e sem
      sentinela numérica para sinalizar erro
- [ ] Sessão Spark obtida por `getActiveSession() or getOrCreate()`, se usa Spark
- [ ] A tabela de módulos em `hub_snippets/README.md` (ou `hub_scripts/README.md`)
      lista o objeto
- [ ] O objeto importa: `from hub_snippets.<secao>.<nome> import <api>`
- [ ] O smoke test continua verde (`tools/spark_smoke_test.py`)
- [ ] Se é conversão: `grep` mostra que quem importava o módulo continua
      importando

### Se é script, além do acima

- [ ] Recebe o **endereço** do que diagnostica — nome de tabela ou caminho —,
      não o dado já carregado
- [ ] Devolve veredito estruturado, com contagem do que foi varrido
- [ ] Não escreve nada: sem tabela, sem arquivo, sem run de MLflow
- [ ] O notebook mostra o caso que **passa** e o caso que **falha**

### Se é notebook

- [ ] Abre com `# Databricks notebook source`
- [ ] Tem tabela "o que este notebook assume do ambiente", com a linha **Escrita**
- [ ] Tem bloco de saída com a cerca `text` — ou o bloco canônico de não executado
- [ ] Se instala biblioteca: `%pip install` e `%restart_python` na abertura, com
      o pin conferido em `requirements-optional.txt`
- [ ] Tem seção "quando **não** usar"
- [ ] Executou no ambiente alvo, e o resultado foi SUCCESS

### Se é skill

- [ ] O nome da pasta é idêntico ao campo `name` do frontmatter
- [ ] O frontmatter tem só `name` e `description`
- [ ] A `description` declara o que a skill **não** cobre
- [ ] O `SKILL.md` tem menos de 500 linhas
- [ ] O corpo tem as cinco seções do template: quando se aplica, fluxo, helpers,
      o que nunca fazer, formato de saída
- [ ] Os helpers estão declarados por caminho de import, em tabela
- [ ] Todos os caminhos de helper citados resolvem para objeto existente
- [ ] `EXPECTED_SKILLS` em `tools/publicar_free.py` acompanha a contagem
- [ ] Os dois inventários listam a skill: `skills/README.md` e a tabela de
      invocação do `.assistant/README.md`
- [ ] O roteiro de forward test ganhou os três casos, e o formulário de
      resultados ganhou a linha
- [ ] **Forward test executado**: caso positivo, caso negativo e `@menção`, cada
      um em chat novo

### Se é conversão de objeto que já existe

- [ ] Assinatura, ordem e nome dos parâmetros **inalterados**
- [ ] Nomes devolvidos — colunas, chaves — **inalterados**
- [ ] Comportamento em base vazia, nulo e caso limite **inalterado**
- [ ] Nenhum identificador traduzido
- [ ] A melhoria, se houver, está em **commit separado**

---

## Parte 2 — juízo de quem escreveu

Ninguém confere isto por você. São declarações, e valem pelo que quem assina
souber sustentar.

- [ ] O tipo foi **confirmado** com quem pediu
- [ ] O template do tipo foi lido nesta sessão, não de memória
- [ ] A docstring do módulo diz **por que ele existe**, não o que ele faz
- [ ] Toda decisão de projeto não óbvia tem comentário com o **motivo**
- [ ] A mensagem de erro diz **o que fazer**, não só o que houve
- [ ] Todo limite calibrável virou constante nomeada
- [ ] O cabeçalho do notebook abre com o **problema**, não com a função
- [ ] A saída colada é **literal**; se foi cortada, o corte está declarado
- [ ] A prosa cita o número **obtido**, não o pretendido
- [ ] A seção "quando não usar" é específica **deste** objeto, e não genérica

---

## O que este checklist não cobre

**Roteamento**, se o objeto for skill. Uma `description` nova compete com as
existentes, e isso só se mede em chat: caso positivo, caso negativo e `@menção`.
O roteiro está em `docs/testes/forward/roteiro.md`.

**Comportamento em dado real.** Tudo aqui é sobre forma e sobre o laboratório. O
que só aparece com volume, permissão e dado governado é assunto do runbook de
replicação, em `docs/playbooks/`.
````

### ambiente_fonte/.assistant/skills/hub-ml-concierge/templates/handoff.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/templates/handoff.md).

````text
# Template — repasse para a etapa especializada

> Contexto portátil para continuar no mesmo chat ou em outro assistente. Um texto contendo `@` não é uma chamada de ferramenta. Preencha apenas fatos confirmados e diferencie campos não informados.

```text
DESTINO: [skill especializada ou etapa de implementação, verificada]
OBJETIVO: [necessidade original]
DECISAO ESPERADA: [resultado útil]
MODO AUTORIZADO: [explicar / planejar / gerar código / executar, conforme pedido]
PROIBICOES PRESERVADAS: [sem consultas / sem escrita / outros limites]

BASE CONSULTADA: [raiz e versão observada]
RECURSOS SELECIONADOS: [caminhos, símbolos públicos, seções]
EVIDENCIAS: [referências realmente lidas]
PAPEL DE CADA RECURSO: [contribuição para cada subobjetivo]
ENTRADAS DISPONIVEIS: [schema, tipo, notebook, modelo, quando fornecidos]
ENTRADAS FALTANTES: [NÃO INFORMADO; nunca preencher por suposição]
ORDEM: [pré-condição -> etapa -> saída]
ADAPTACOES: [necessárias e ainda não implementadas]
LACUNAS: [não cobertas ou não verificadas]
CRITERIO DE ACEITE: [o que a próxima etapa precisa demonstrar]

NAO REPETIR A DESCOBERTA: [itens já resolvidos e fonte]
RETORNAR AO CONCIERGE SOMENTE SE: [surgir nova lacuna de recurso]
ESTADO: recomendação produzida; execução da próxima etapa não presumida.
```

Não inclua dados pessoais, credenciais, payloads de clientes ou resultados não observados. Mencione nomes de tabelas e paths reais somente no contexto autorizado de uso, nunca em evidência versionada desta área experimental.
````

### ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/templates/estilo_visual_eda.md

[Origem na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/templates/estilo_visual_eda.md).

````text
# Estilo Visual — EDA Profissional sobre o Sistema de Temas

Este template orienta **composição, hierarquia e leitura** de uma EDA. Ele não é fonte de paleta, token ou aprovação. As escolhas configuráveis pertencem ao contrato `hub_padroes/identidade_visual` e chegam ao consumidor por `ResolvedTheme`.

---

## 1. Fonte de verdade visual

- Não declare paleta, dicionário de tema ou convenção local que replique a política visual do Hub.
- Não copie valores de `TOKENS.md` para “congelar” uma aparência local.
- Não registre template global como preparação padrão do notebook; **não registre template global** apenas para aplicar uma proposta.
- Se não houver tema explicitamente selecionado, use as APIs legadas do Hub.
- Se houver tema notebook válido, use as rotas `_resolvido` do consumidor.

Fluxo mínimo para uma figura Plotly genérica:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido

tema = load_reference_theme("notebook")
fig = ...  # mesmos dados, agregações e eixos da análise
aplicar_tema_resolvido(fig, tema, subtitulo="Recorte analisado", n=n_amostra)
fig.show()
```

Para componentes especializados, prefira a própria rota resolvida, por exemplo `plot_correlation_resolvido`, `plot_distributions_resolvido`, curvas `*_resolvido`, `plot_vintage_curves_resolvido` ou `plot_timeline_resolvido`. Isso evita reconstruir semântica de cor no notebook.

---

## 2. O que o tema pode e não pode mudar

O tema pode controlar propriedades visuais cobertas pelo contrato, como tipografia, dimensões, margens, paletas e cores semânticas. Ele **não** muda:

- filtro, população ou data de corte;
- amostragem, seed ou agregação;
- bins, denominadores e unidade;
- threshold analítico ou política de monitoramento;
- métrica, modelo ou conclusão de negócio.

Aparência consistente não valida a análise.

---

## 3. Regras de gráficos

### 3.1. Escolher o visual pela pergunta

| Tipo de dado/pergunta | Visual sugerido | Cuidados |
| --- | --- | --- |
| numérica univariada | histograma, ECDF ou box plot | declarar amostra/agregação |
| categórica | barras ordenadas | mostrar denominador, top-N e cauda |
| temporal | linha em frequência regular | rotular janela e gaps |
| associação numérica | scatter/agregado ou correlação | sinal não implica causalidade |
| matriz com centro significativo | heatmap divergente | preservar centro e domínio |
| comparação de segmentos | small multiples ou barras | manter escala comparável |

Use Plotly para gráficos do relatório quando a interatividade ajudar. `createVisualization` ou visualização nativa podem ser melhores para exploração rápida ou agregações que devem ficar no backend. Matplotlib permanece válido para casos estáticos específicos, mas não herda automaticamente o Sistema de Temas Plotly.

### 3.2. Anotações do relatório final

Todo gráfico material deve deixar explícitos, quando aplicável:

- N amostral ou volume agregado;
- fonte/snapshot;
- janela, segmento ou recorte;
- unidade e denominador;
- uma anotação de destaque somente quando houver achado realmente sustentado.

Não transforme anotação em conclusão causal. Em rotas Plotly do Hub, use os argumentos de rodapé do adaptador/consumidor em vez de criar um segundo estilo.

### 3.3. Dimensão da figura

Não copie uma tabela local de alturas/larguras para simular o tema. Dimensões configuráveis pertencem aos tokens do contexto. Ajustes excepcionais por conteúdo — por exemplo, um heatmap com muitas safras — podem complementar o tema quando o próprio consumidor documentar essa regra.

---

## 4. Emojis padronizados

Uso **limitado e semântico**, nunca apenas decorativo.

| Emoji | Significado | Contexto de uso |
| --- | --- | --- |
| ✅ | validação passou / OK | checks de qualidade |
| ❌ | validação falhou / erro | checks de qualidade |
| ⚠️ | atenção / risco moderado | ponto de atenção |
| 🟢 | status positivo | indicador de qualidade |
| 🟡 | status intermediário | indicador de qualidade |
| 🔴 | status crítico | indicador de qualidade |
| 📌 | insight-chave | interpretação material |
| 📊 | resultado factual | seção de dados |
| 🔍 | interpretação/análise | seção técnica |
| 💼 | visão de negócio | seção executiva |
| ➡️ | próximo passo | transição entre etapas |

Use no máximo três emojis por célula Markdown. Evite emojis nos títulos `##`; prefira-os em subtítulos ou blocos de resultado quando acrescentarem significado.

---

## 5. Formato de números

Prefira `hub_snippets.constants.format_br` quando a entrega exigir convenção brasileira. O ponto importante é manter a **mesma unidade e convenção em todo o notebook**, não copiar formatações ad hoc em cada célula.

| Tipo | Apresentação esperada |
| --- | --- |
| inteiro grande | separador de milhar consistente |
| monetário BRL | símbolo, duas casas quando materiais e convenção BR |
| percentual | uma ou duas casas conforme precisão útil |
| razão/taxa | casas suficientes para não esconder variação relevante |
| contagem pequena | inteiro sem decimal |

Em tabelas Markdown destinadas ao público brasileiro, use a convenção de milhares/decimais prevista pelo helper. Não transforme arredondamento de apresentação em alteração do valor calculado.

---

## 6. Tabelas Markdown

- Prefira até seis colunas por bloco legível; se houver muitas dimensões, divida a apresentação.
- Alinhe números à direita quando a superfície permitir.
- Use nomes de coluna curtos, sem repetir o título inteiro.
- Use negrito apenas para destaques semânticos.
- Use backticks para nomes técnicos, como `` `valor_pago` ``.
- Trunque texto longo apenas na apresentação e deixe claro quando houver perda de conteúdo.
- Sempre declare unidade/denominador quando eles não forem óbvios pelo rótulo.

Exemplo de estrutura:

```markdown
| Métrica | Valor | Status |
| --- | ---: | :---: |
| Total de linhas | ... | 🟢 |
| PK única | ... | 🟡 |
| Nulos | ... | 🟢 |
```

---

## 7. KPI card — linha de impacto

Uma célula pós-código pode abrir com poucos KPIs materiais para leitura rápida:

```markdown
> **N linhas** | **P colunas** | **x% nulos** | **D duplicatas**
```

Regras:

- use somente valores observados na saída;
- limite-se a quatro ou cinco KPIs por linha;
- mantenha unidade explícita;
- não preencha um card com números inventados para completar layout;
- quando precisar de HTML/card institucional, use `hub_snippets.visual.kpi_card` e sua rota `_resolvido` quando houver `ResolvedTheme`.

---

## 8. Output de código e cabeçalhos de seção

Para notebook exploratório, um output textual simples é suficiente. Se quiser um cabeçalho textual, priorize função sem política de cor local:

```python
def exibir_secao(titulo, subtitulo=None):
    largura = 60
    print(f"\n┌{'─' * (largura - 2)}┐")
    print(f"│ {titulo:<{largura - 4}} │")
    if subtitulo:
        print(f"│ {subtitulo:<{largura - 4}} │")
    print(f"└{'─' * (largura - 2)}┘")
```

Para apresentação rica, não escreva `displayHTML` com CSS/cores inline para recriar o padrão. Use `hub_snippets.visual.section_header`, `kpi_card`, `badge` e `divider`; com tema selecionado, use a rota `_resolvido` documentada pelo componente.

---

## 9. Hierarquia de títulos Markdown

| Nível | Uso | Exemplo |
| --- | --- | --- |
| `#` | título único do notebook | `# EDA — Tabela X` |
| `##` | etapas principais | `## Etapa 3 — Qualidade` |
| `###` | subseções/resultados | `### Resultado — Etapa 3` |
| `####` | tópicos internos | `#### Resultado observado` |

Evite `#####` ou níveis inferiores; em geral indicam profundidade excessiva.

---

## 10. Separadores e narrativa pós-código

Para um bloco de resultado longo, mantenha uma ordem previsível:

```markdown
### Resultado — Etapa N

> **KPI1** | **KPI2** | **KPI3**

---

#### 📊 Resultado observado
(tabela ou fatos)

---

#### 🔍 Interpretação técnica
(análise suportada pela saída)

---

#### 💼 Interpretação de negócio
(implicação, sem transformar associação em causalidade)

---

#### ➡️ Próximo passo
(continuidade concreta)
```

Use `hub_snippets.visual.divider` quando precisar de um componente institucional; não replique borda/cor manualmente.

---

## 11. Índice de seções

Todo notebook EDA extenso deve oferecer uma rota de navegação no início. O helper oficial é `hub_snippets.visual.index_generator`.

- O mapeamento de emojis compartilhados vive em `hub_snippets.constants.emojis`.
- Liste etapa, título e descrição curta.
- O índice pode ser Markdown ou HTML conforme o consumidor; com `ResolvedTheme`, prefira a rota resolvida existente.
- O índice não substitui títulos reais no notebook.

---

## 12. Section headers

Cada seção principal pode abrir com `hub_snippets.visual.section_header`.

O cabeçalho deve comunicar:

- etapa/seção;
- título objetivo;
- descrição de uma frase;
- hierarquia coerente com o restante do notebook.

Cor, fonte e borda não são especificadas neste template: vêm da implementação legada ou do `ResolvedTheme` pela rota `_resolvido`.

---

## 13. Referência de componentes compartilhados

| Necessidade | Fonte/consumidor |
| --- | --- |
| contrato e primeiro uso | `hub_padroes/identidade_visual/README.md` e `GUIA_OPERACIONAL.md` |
| carregar/validar tema | `hub_snippets.visual.tema` |
| aplicar tema Plotly | `hub_snippets.visual.theme_plotly.aplicar_tema_resolvido` |
| correlação | `hub_snippets.display.correlation_matrix.plot_correlation_resolvido` |
| distribuições | `hub_snippets.display.distribution_grid.plot_distributions_resolvido` |
| índice | `hub_snippets.visual.index_generator` |
| cabeçalho de seção | `hub_snippets.visual.section_header` |
| KPI cards | `hub_snippets.visual.kpi_card` |
| divisores | `hub_snippets.visual.divider` |
| badges | `hub_snippets.visual.badge` |
| autoria/comparação | `hub_snippets.visual.theme_lab` |

Use a API legada quando não houver tema explicitamente selecionado; use a rota `_resolvido` quando houver um `ResolvedTheme` válido e o componente documentar suporte.

---

## 14. Consumidores com limite explícito

- **SHAP/Matplotlib:** o theming V07 não cobre sua aparência interna nem o PNG salvo pelo helper.
- **Kaplan–Meier:** permanece com a ordem visual legada até existir token que represente sua semântica sem remapeamento silencioso.

Não prometa consistência temática para essas superfícies apenas porque o restante do notebook usa `ResolvedTheme`.

O template EDA organiza a apresentação. A fonte de verdade do tema permanece fora desta skill.
````

