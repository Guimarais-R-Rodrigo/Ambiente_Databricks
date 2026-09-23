# SER00 — matriz completa de 24 superfícies

Policy observada em `11851e137dd7793b351ac08fc211c0be90005dee`. A coluna de nível é objetivo da superfície; não comprova que ela já exista no current global. Rótulos `REG` indicam somente preservação/regressão.

| Skill | Protected surface | Desired level na policy | Evidence na policy | Sprint | Evidência adicional/limite exigido |
|---|---|---|---|---|---|
| hub-ml-analise-safra | vintage_core | L3 | receipt | SER03 | Tabela safra×MOB, denominadores, incidência e maturidade vinculados ao input; target binário coberto, outros estimandos não presumidos. |
| hub-ml-analise-safra | calendar_derivation | L2 | preflight | SER03 | Originação, referência, periodicidade, MOB e regra para safras incompletas explícitos. |
| hub-ml-auditoria-skills | state_ladder | L2 | preflight | REG | Preservar citado/localizado/lido/importado/chamado/concluído; desconhecido não vira verdadeiro. |
| hub-ml-auditoria-skills | independent_verification | L3 | receipt | REG/SER15 | Receipt da auditoria não é o Receipt da produtora; adapter ausente mantém NOT_REVERIFIED. |
| hub-ml-baseline-ml | split_without_leakage | L3 | receipt | SER09/SER10 | Separações temporal/grupo, gap, holdout e preprocessing train-only vinculados ao run. |
| hub-ml-baseline-ml | training_and_tracking | L4 | postflight | SER09/SER10 | Treino e registro com dados/split/parâmetros/artefatos observados; sem promoção implícita. |
| hub-ml-comentar-notebook | preserve_code_cells | L1 | static | REG | Contrato editorial e comparação do código; não alegar execução a partir de saída ausente. |
| hub-ml-concierge | routing_and_handoff | L1 | static | REG | Descoberta read-only, origem e cobertura limitadas ao contexto realmente acessado. |
| hub-ml-criar-objeto | object_shape | L2 | preflight | SER01 | Tipo/operação/destino/conversão e confirmação validados antes de escrita. |
| hub-ml-criar-objeto | object_validation | L3 | receipt | SER01 | Validação por tipo e bytes produzidos; piloto de README não cobre todo objeto/operação/host. |
| hub-ml-cross-eda-ml | join_diagnostics | L3 | receipt | SER05/SER06 | Cobertura, multiplicidade, perdas, chaves e grão pelo símbolo público diagnosticar_join. |
| hub-ml-cross-eda-ml | point_in_time_join | L4 | postflight | SER05/SER06 | Disponibilidade <= decisão; atraso, fuso, janela, empate e não aplicabilidade explicitados. |
| hub-ml-eda-profissional | eda_core | L4 | postflight | REG | Preservar run_enforced, Receipt e finalize_or_raise; PASS como único autorizador de conclusão. |
| hub-ml-explainability | model_and_dataset_binding | L2 | preflight | SER02 | Modelo/run/versão, população, features, output_index, tarefa e método compatíveis. |
| hub-ml-explainability | explanation_computation | L3 | receipt | SER02 | Cálculo canônico e linhas efetivamente explicadas; subamostra KernelSHAP exige binding explícito. |
| hub-ml-feature-engineering | point_in_time_features | L4 | postflight | SER07/SER08 | Cutoff, disponibilidade, janela, entidade, horizonte e proveniência; criatividade fora do gate. |
| hub-ml-feature-engineering | materialization | L4 | authorization | SER07/SER08 | Plano/autorização/destino/mode/idempotência, execução, output binding e Postflight. |
| hub-ml-monitoramento-modelo | monitoring_metrics | L3 | receipt | SER11/SER12 | Referência, bins, população, janela, maturidade do target e thresholds versionados. |
| hub-ml-monitoramento-modelo | retrain_or_promotion | L4 | authorization | SER11/SER12 | Recomendação e ação distintas; autorização específica, Receipt/Postflight e efeitos verificáveis. |
| hub-ml-pipeline-builder | pipeline_spec | L2 | preflight | SER13 | Contrato/preflight read-only com ambiente, origem/destino, incremental, jobs, rollback e intent. |
| hub-ml-pipeline-builder | deploy_or_write | L4 | authorization | SER13/SER14 | Spec validada não prova deploy: execução isolada autorizada, Receipt, Postflight e cleanup. |
| hub-ml-tutor-databricks | explanation | L0 | static | REG | Resposta didática sem execução, escrita ou deployment implícitos. |
| hub-ml-validacao-estatistica | test_plan | L2 | preflight | SER04 | Hipótese, estimando, unidade, desenho, pressupostos, multiplicidade e método antes do teste. |
| hub-ml-validacao-estatistica | deterministic_statistics | L3 | receipt | SER04 | Métodos com API efetivamente suportada; efeitos/incerteza e correção múltipla quando aplicáveis. |

## Aplicabilidade e granularidade

Para cada execução, resolver aplicabilidade como verdadeiro, falso ou não determinado. Não determinado bloqueia a etapa material; não pode virar falso para obter PASS. PIT simples não aplicável dispensa a operação PIT, mas exige decisão rastreável. Maturidade, autorização e tracking não são booleanos inferidos da vontade de concluir.

As superfícies cujo `evidence` atual é `authorization` também precisam de execução verificável e Postflight para uma promoção L4. Autorização é condição necessária, não prova suficiente de execução ou integridade. Não alterar a policy para esconder esta diferença.

Cada Receipt deve vincular entradas efetivas, saída, etapa, método, versão, contexto aplicável e release. Cada Postflight deve verificar conclusão dos recursos exigidos e consistência do claim. SHA do arquivo sozinho não autentica uma operação remota nem substitui evidência de autorização humana.
