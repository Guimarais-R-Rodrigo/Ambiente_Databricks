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

