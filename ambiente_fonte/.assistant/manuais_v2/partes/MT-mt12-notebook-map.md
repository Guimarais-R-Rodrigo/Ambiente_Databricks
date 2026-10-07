# Leitura dos notebooks de briefing

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt12-notebook-map"></a>
<a id="mt12-notebook-map"></a>
### Leitura dos notebooks de briefing

Leia cada ficha como uma ligação entre a arquitetura ensinada no capítulo e os bytes de um arquivo concreto. A coluna de papel responde por que o arquivo existe. As entradas e saídas mostram onde os dados entram e o que o chamador recebe. A coluna de efeitos separa calcular um resultado de alterar a sessão, gravar uma tabela ou produzir uma apresentação. Essa separação evita atribuir ao helper tudo que aparece no notebook de demonstração.

Uma fachada é a camada de importação que disponibiliza nomes de outro módulo. Ela pode carregar bibliotecas necessárias no momento do import, embora ainda não chame a função de negócio. Um marcador de pacote apenas estabelece a organização do diretório. Uma implementação contém o algoritmo. Um exemplo é um roteiro de notebook: pode preparar dados, instalar bibliotecas, mostrar resultados e conservar observações históricas. Esses quatro papéis explicam a repetição de nomes entre arquivos sem sugerir quatro versões independentes do mesmo algoritmo.

As fichas complementam a leitura contínua; não substituem a assinatura e a interpretação desenvolvidas nos capítulos. Quando um resultado histórico difere do comportamento atual, a nota identifica a diferença e o cuidado necessário. Uma saída colada no exemplo descreve o ensaio registrado naquela fonte; ela não demonstra uma execução atual. Os nomes citados também não tornam automaticamente uma função interna uma interface pública. Para compor uma chamada, use a fachada indicada e confira o contrato do objeto.

Os links levam ao arquivo correspondente e ao trecho conceitual do manual. Compare sempre helper e exemplo antes de executar células: efeitos pertencem ao corpo que realmente os realiza. As limitações descritas fazem parte da interpretação do resultado, inclusive quando o código devolve números plausíveis.

Nos briefings, distinga as três partes do roteiro. A preparação pode ler arquivos ou sobrescrever tabelas, o texto orienta uma conversa e a captura registra o que foi observado. Sete exemplos compartilham o destino hub_exemplo_clientes, portanto executar um deles pode substituir a base preparada por outro.

<a id="mt12-notebook-preparacao"></a>
#### Preparação Spark dos dezesseis notebooks originais

Os dezesseis notebooks originais começam consultando `current_user()` pela sessão Spark e obtendo o primeiro resultado com `first()`. Em seguida, inserem o caminho do Hub em `sys.path`. Essa consulta de identidade e alteração do caminho de importação exigem sessão Spark, inclusive nos exemplos cujo insumo é um arquivo. São efeitos de preparação, distintos das leituras e escritas de tabelas de negócio descritas nas fichas. Os dois exemplos novos de Micromodelos têm outra preparação: imprimem somente uma fixture textual local, sem Spark, catálogo ou tabelas. Suas conversas E1 datadas não são execução de runtime.

<a id="mt12-notebook-map-file-001"></a>
#### 1. `exemplo_auditoria_skills.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/auditoria_skills/exemplo_auditoria_skills.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-4)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/auditoria_skills/exemplo_auditoria_skills.py` · SHA-256 `d8ee872968da35d2600157c766b213b984f16446dbb076e021cd43fc6df88d5e` |
| Papel e motivo técnico | Auditar uma skill real contra contrato e evidências de roteamento. |
| Parte 1: preparação e leitura | Lê hub-ml-criar-objeto/SKILL.md, mostra contagem de linhas e frontmatter; não altera a skill. |
| Parte 1: efeitos de escrita | Não grava tabela persistente nesta etapa. |
| Parte 1: arquivos ou tabelas lidos | ["/Workspace/Users/{usuario}/.assistant/skills/hub-ml-criar-objeto/SKILL.md"] |
| Parte 2: texto para o chat | Modo implementação/OUTPUT e plano de correção; não editar description. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-002"></a>
#### 2. `exemplo_baseline_orchestration.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/baseline_orchestration/exemplo_baseline_orchestration.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-3)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/baseline_orchestration/exemplo_baseline_orchestration.py` · SHA-256 `722a8b43987db597da9841d134eb7c6d9551186a3b575c142eab2231f270cc87` |
| Papel e motivo técnico | Pedir baseline binário temporal honesto com comparação e registro. |
| Parte 1: preparação e leitura | base_tabular(n=4000, seed=42, nulos renda 0,06, prevalência alvo 0,18). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | COLUNAS_PROIBIDAS e PONTO_NO_TEMPO; plano e código sem treino executado. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-003"></a>
#### 3. `exemplo_comentar_notebook.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/comentar_notebook/exemplo_comentar_notebook.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-4)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/comentar_notebook/exemplo_comentar_notebook.py` · SHA-256 `ebe739d6739e97a79c44b5abc4f284013131b9173295e09a496888d4c555e23b` |
| Papel e motivo técnico | Pedir revisão documental de notebook existente sem editar código. |
| Parte 1: preparação e leitura | Lê exemplo_pit_join.py e conta linhas/células Markdown; não edita. |
| Parte 1: efeitos de escrita | Não grava tabela persistente nesta etapa. |
| Parte 1: arquivos ou tabelas lidos | ["/Workspace/Users/{usuario}/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py"] |
| Parte 2: texto para o chat | REVISAO_EDICAO_OU_DOCUMENTACAO; exemplo escolhe revisão sem reescrever. Dados sensíveis permanecem NÃO INFORMADO, e sugestões de células Markdown não autorizam aplicá-las. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-004"></a>
#### 4. `exemplo_comparar_tabelas.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/comparar_tabelas/exemplo_comparar_tabelas.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-2)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/comparar_tabelas/exemplo_comparar_tabelas.py` · SHA-256 `d8c38d69ec30484ca8ecddbbf3341c5f81c2ed4a8c58ffa38f7042c9e08b22e5` |
| Papel e motivo técnico | Reconciliação de duas versões de base com chave, tolerâncias e diferenças. |
| Parte 1: preparação e leitura | base_tabular v1 n=4000/nulos=0,04; v2 n=4200/nulos=0,09. |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes_v1, workspace.default.hub_exemplo_clientes_v2. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | TIPO_COMPARACAO conteúdo/distribuição; tolerâncias propostas, sem skill explícita no cabeçalho. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-005"></a>
#### 5. `exemplo_cross_eda.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/cross_eda/exemplo_cross_eda.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-2)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/cross_eda/exemplo_cross_eda.py` · SHA-256 `96281155b05c03aa4cad9a31c6142ae4d68a08648a72e14a3404b1ee96a198a8` |
| Papel e motivo técnico | Avaliar viabilidade de combinar fatos e features para modelagem. |
| Parte 1: preparação e leitura | fatos_e_features(n_decisoes=1500, atraso_real_dias=3, pct_feature_futura=0,2). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_fatos, workspace.default.hub_exemplo_features. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | PONTO_NO_TEMPO, atraso de publicação, cardinalidade e cobertura antes de join. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-006"></a>
#### 6. `exemplo_data_quality.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/data_quality/exemplo_data_quality.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-2)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/data_quality/exemplo_data_quality.py` · SHA-256 `743a88a62255919bf6b13f57d3b7eefce399d476a2ddaee2e3b25788a16ffb7b` |
| Papel e motivo técnico | Pedir diagnóstico e contrato de qualidade para base de treino. |
| Parte 1: preparação e leitura | base_tabular(n=4000, n_entidades=3200, nulos renda=0,06). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes_dup. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | USO_DOWNSTREAM, chave/grão, limites justificados; leitura no chat, sem correção mutável. Se EDA for selecionada, sua rota canônica e o Postflight continuam obrigatórios. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-007"></a>
#### 7. `exemplo_eda_completa.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/eda_completa/exemplo_eda_completa.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-2)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/eda_completa/exemplo_eda_completa.py` · SHA-256 `c40437402fcc6827d57800d7830b6c75af2ab672fd9ad4e6071a6a875cb50a8d` |
| Papel e motivo técnico | Pedir EDA completa orientada a target e notebook de saída. |
| Parte 1: preparação e leitura | base_tabular(n=4000, nulos renda=0,06, prevalência alvo=0,18). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | Target e entregável declarados; qualidade, relações e risco de modelagem. A rota EDA exige `run_enforced`, Receipt, handoff e Postflight, com `completion.authorized=true`; `PENDING_POSTFLIGHT` não é conclusão. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-008"></a>
#### 8. `exemplo_eda_rapida.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/eda_rapida/exemplo_eda_rapida.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-2)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/eda_rapida/exemplo_eda_rapida.py` · SHA-256 `5a733b7ce0ed36e9e963a61bf91c87a32a192d307620da3efa5774f1c1ac7c2a` |
| Papel e motivo técnico | Pedir perfil rápido de tabela desconhecida com custo limitado. |
| Parte 1: preparação e leitura | base_tabular(n=4000, nulos renda=0,06, prevalência alvo=0,18). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | Chave suspeita, não confirmada; modo curto. A análise selecionada segue a rota EDA `run_enforced`, Receipt, handoff e `finalize_or_raise`, sem usar helper manual para contornar um bloqueio. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-009"></a>
#### 9. `exemplo_explainability.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/explainability/exemplo_explainability.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-3)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/explainability/exemplo_explainability.py` · SHA-256 `37647a68ea52dd29fbb0647f9205d76567fbb4499578d6a9294134a972a39f9b` |
| Papel e motivo técnico | Pedir plano de explicação global e local para modelo pretendido, ainda sem artefato informado. |
| Parte 1: preparação e leitura | base_tabular(n=4000, nulos renda=0,06, prevalência alvo=0,18); não treina nem registra modelo. |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | PUBLICO gestor/técnico e espaço da saída SHAP; LightGBM é explicitamente PRETENDIDO, sem modelo treinado, run ou URI informado. A instalação de SHAP depende de autorização e compatibilidade próprias. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-010"></a>
#### 10. `exemplo_feature_engineering.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/feature_engineering/exemplo_feature_engineering.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-3)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/feature_engineering/exemplo_feature_engineering.py` · SHA-256 `b072a78171500421a4a285b374b211b187ffef18e493d7930362ecec6685d687` |
| Papel e motivo técnico | Especificar features com disponibilidade temporal e teste de leakage. |
| Parte 1: preparação e leitura | fatos_e_features(n_decisoes=1500, atraso_real_dias=3, pct_feature_futura=0,2). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_fatos, workspace.default.hub_exemplo_features. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | JANELA_OBSERVACAO 90 dias e PONTO_NO_TEMPO; código proposto sem execução. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-011"></a>
#### 11. `exemplo_monitoramento_modelo.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/monitoramento_modelo/exemplo_monitoramento_modelo.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-3)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/monitoramento_modelo/exemplo_monitoramento_modelo.py` · SHA-256 `15c7fc48b5abd95f2430550f4be4123ac11e8744e36e5b9aea7bbcb0817a718e` |
| Papel e motivo técnico | Projetar monitoramento separando drift, rótulo atrasado e desempenho. |
| Parte 1: preparação e leitura | base_tabular ref/atual n=3000 cada; prevalências solicitadas 0,18/0,11 e nulos renda 0,04/0,12. |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_monitor_ref, workspace.default.hub_exemplo_monitor_atual. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | TARGET_E_LABEL_DELAY 30 dias; sem performance corrente observada ou modelo em produção criado. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-012"></a>
#### 12. `exemplo_novo_projeto.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/novo_projeto/exemplo_novo_projeto.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-2)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/novo_projeto/exemplo_novo_projeto.py` · SHA-256 `7fb6ed4749265284302663b0d8050814c2189b6754152250b8e3222c569649e1` |
| Papel e motivo técnico | Estruturar projeto analítico e rascunho de AGENTS.md em modo plano. |
| Parte 1: preparação e leitura | base_tabular(n=4000, nulos renda=0,06, prevalência alvo=0,18). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | Sem skill explícita; MODO somente plano, sem deploy ou arquivo persistido pelo notebook. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-013"></a>
#### 13. `exemplo_pipeline.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/pipeline/exemplo_pipeline.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-3)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/pipeline/exemplo_pipeline.py` · SHA-256 `88ddfb4dff61e4a681d24c9cf06d20389e3e66bc490d8a2c3f201b077c288dc6` |
| Papel e motivo técnico | Pedir arquitetura/código de pipeline para base de exemplo, sem deploy. |
| Parte 1: preparação e leitura | base_tabular(n=4000, nulos renda=0,06, prevalência alvo=0,18). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | SCHEMA_EVOLUCAO e MODO; bronze/silver/gold condicionais, sem iniciar pipeline. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-014"></a>
#### 14. `exemplo_safra.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/safra/exemplo_safra.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-3)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/safra/exemplo_safra.py` · SHA-256 `ea4b09dfc0887f3baea45860ba6ab429570ad7fd6254e2c4c3989884e3c6e385` |
| Papel e motivo técnico | Pedir análise de vintages por maturidade e denominadores comparáveis. |
| Parte 1: preparação e leitura | `safras(n_contratos=1200, safras_yyyymm=("202501", "202502", "202503"), mob_maximo=12, seed=42)` cria a base sintética; `base.count()` e `base.groupBy("safra").agg(F.countDistinct("id_contrato"), F.max("mob")).orderBy("safra").show()` exibem volume, contratos distintos e maior idade observada por safra. A agregação usa `pyspark.sql.functions` nesta Parte 1. |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_safras. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | O pedido preenchido exige alinhamento por idade/MOB, células imaturas marcadas como não observáveis, regra de censura, numerador e denominador comparáveis; solicita agregações Spark em alto volume, sem que a análise do chat tenha sido executada. A frase do briefing de que a safra `202503` tem menos MOB observado não é sustentada pelo preparo: `fixtures.safras(..., mob_maximo=12)` gera MOB de 1 a 12 para todos os contratos nas três safras. Sem corte temporal adicional, o exemplo não demonstra imaturidade diferenciada. Confira `F.max("mob")` por safra e corrija essa hipótese antes de interpretar uma comparação; não transforme o texto do prompt em resultado medido. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-015"></a>
#### 15. `exemplo_stat_check.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/stat_check/exemplo_stat_check.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-2)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/stat_check/exemplo_stat_check.py` · SHA-256 `6410675f82ce9dc0264d41006b2465c930e2790f129186025775f92d8c7a87f3` |
| Papel e motivo técnico | Pedir desenho de validação estatística antes de escolher teste. |
| Parte 1: preparação e leitura | base_tabular(n=4000, nulos renda=0,06, prevalência alvo=0,18). |
| Parte 1: efeitos de escrita | Ao executar esta etapa, usa overwrite nos destinos listados; isso substitui o conteúdo anterior. Destinos: workspace.default.hub_exemplo_clientes. |
| Parte 1: arquivos ou tabelas lidos | [] |
| Parte 2: texto para o chat | PREDICAO_INFERENCIA_EXPERIMENTO: inferência, estimando, efeito e incerteza. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |

<a id="mt12-notebook-map-file-016"></a>
#### 16. `exemplo_tutor_explicar.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/tutor_explicar/exemplo_tutor_explicar.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-4)
[Preparação da sessão para este notebook](#mt12-notebook-preparacao)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/tutor_explicar/exemplo_tutor_explicar.py` · SHA-256 `d48758a1330560bc8e1aa04e380f5c2b5a0f0b2b8ecd0af28098cd707620ffcb` |
| Papel e motivo técnico | Pedir explicação didática do módulo point-in-time por nível do aprendiz. |
| Parte 1: preparação e leitura | Lê pit_join.py e mostra as primeiras 20 linhas; não modifica. A impressão parcial não prova que o chat recebeu o módulo inteiro; o conteúdo integral autorizado deve ser fornecido quando necessário. |
| Parte 1: efeitos de escrita | Não grava tabela persistente nesta etapa. |
| Parte 1: arquivos ou tabelas lidos | ["/Workspace/Users/{usuario}/.assistant/hub_snippets/spark/pit_join/pit_join.py"] |
| Parte 2: texto para o chat | INICIANTE_INTERMEDIARIO_AVANCADO; exemplo intermediário em SQL/iniciante em Spark. |
| Parte 3: registro de resposta | {"kind": "human_capture", "state": "NÃO EXECUTADO", "requires": "novo chat no Genie Code, resposta real colada com data e skill selecionada observada"} |
| Como interpretar este arquivo | As partes são independentes: preparar uma base não executa o prompt; copiar o prompt não comprova a escolha da skill. O marcador NÃO EXECUTADO da Parte 3 descreve a captura da resposta, sem certificar o estado da Parte 1. Confira o destino de qualquer escrita antes de executar a célula e registre somente uma resposta realmente observada. |


<a id="mt12-notebook-map-file-017"></a>
#### 17. `exemplo_descobrir_micromodelos.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/descobrir_micromodelos/exemplo_descobrir_micromodelos.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-3) · [MU13: uso de Micromodelos](MU-parte-iv.md#mu13)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/descobrir_micromodelos/exemplo_descobrir_micromodelos.py` · SHA-256 `531141be882e5895638d53c2a142a73be94f2fff130dcb8c8da65373a454469c` |
| Papel e motivo técnico | Descobrir oportunidades para escolha humana, preservando limites da evidência disponível. |
| Parte 1: preparação e leitura | Cria e imprime um dicionário local com schema/objeto/tipos fictícios e estado FORNECIDA; não usa Spark ou catálogo. |
| Parte 1: efeitos de escrita | Nenhuma tabela, arquivo ou recurso remoto é escrito; o efeito executável é a impressão local da fixture textual. |
| Parte 2: texto para o chat | O briefing pede até três candidatas, deduplicação por definição e grão, viabilidade INDETERMINADO quando só há nomes/tipos, e escolha humana antes de iniciar YAML. Metadata fornecida não vira OBSERVADA. |
| Parte 3: registro de resposta | Registro da conversa E1 de 29/09/2026, caso P2c: três candidatas, sem YAML, publicação ou execução. Ressalvas: uso indevido de “viáveis” apesar da indeterminação e saída em células Markdown/código vazio. A declaração de consulta da policy não audita chamadas internas. |
| Como interpretar este arquivo | O preparo E0 e a conversa E1 são evidências históricas diferentes. A fixture permanece fornecida e sintética. Nenhum deles certifica a conta atual, autoriza acesso ou representa uma execução feita para esta edição. |

<a id="mt12-notebook-map-file-018"></a>
#### 18. `exemplo_micromodelo_novo.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_prompts/micromodelo_novo/exemplo_micromodelo_novo.py) · [MT12: explicação do mecanismo](MT-parte-iii.md#mt12-3) · [MU13: uso de Micromodelos](MU-parte-iv.md#mu13)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_prompts/micromodelo_novo/exemplo_micromodelo_novo.py` · SHA-256 `b14845477bb268b5a7767821d8cbdbc9c418737b3080f09a9600c5957f3671c2` |
| Papel e motivo técnico | Delimitar uma especificação progressiva a partir de um objetivo conhecido. |
| Parte 1: preparação e leitura | Cria e imprime um dicionário local de decisão, entidade, população fictícia, fonte lógica sem binding e horizonte PROPOSTO. Não consulta catálogo ou registros. |
| Parte 1: efeitos de escrita | Nenhuma tabela, arquivo ou recurso remoto é escrito; o efeito executável é a impressão local da fixture textual. |
| Parte 2: texto para o chat | O briefing distingue proposta de evidência, exige template/schema acessível antes de YAML e validação real pela rota autorizada. Sem isso, pede checklist com YAML_NAO_CRIADO e MM01_NAO_VALIDADO; não inventa fonte, score ou aprovação. |
| Parte 3: registro de resposta | Registro da conversa E1 de 29/09/2026, caso P1: YAML_NAO_CRIADO, MM01_NAO_VALIDADO e SCORE_INDETERMINADO. Ressalvas: alguns campos fornecidos foram chamados OBSERVADO e a policy não foi verificada independentemente. O texto não comprova runtime E1, validação MM01 ou homologação corporativa. |
| Como interpretar este arquivo | O preparo E0 e a conversa E1 são evidências históricas diferentes. A fixture permanece fornecida e sintética. Nenhum deles certifica a conta atual, autoriza acesso ou representa uma execução feita para esta edição. |


<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
