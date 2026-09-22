# SER00 — helpers, primitives e lacunas

Base: `11851e137dd7793b351ac08fc211c0be90005dee`. Legenda de profundidade: **P** = export público conferido; **I** = implementação pertinente inspecionada; **D** = declarado na skill/Manual, precisa revalidação da fachada/implementação antes de contrato. Nenhum helper foi executado nesta sessão. Não converter D em P/I nem leitura estática em teste de runtime.

## Infraestrutura compartilhada

| Recurso | Símbolo/contrato identificado | Evidência e reutilização | Lacuna relevante |
|---|---|---|---|
| hub_scripts.skill_execution | run_preflight; get_skill_enforcement_policy; load_enforcement_policy_registry; list_skill_enforcement_policies | P: fachada pública; contratos/resolução compartilhados | condições 0.1 fechadas, orientadas à EDA; domínios novos exigem desenho aditivo |
| hub_scripts.skill_execution.receipt | ExecutionReceiptV1 e verificação documentados pelo SEF | Trace, release, inputs, outputs e recursos | adaptar binding por domínio; não emitir Receipt sintético para chamada ausente |
| hub_scripts.skill_execution.postflight | Postflight e estados PASS/FAIL/BLOCKED/REVIEW documentados | composição com runner fino de domínio | regra específica, aplicabilidade e autorização não são genéricas por mágica |
| EDA scripts/run.py e run_enforced.py | run / run_enforced | referência concreta de core + coleta + Receipt | não copiar lógica analítica para um runner universal |
| EDA scripts/postflight.py | finalize_or_raise / verify_finalized | finalização e adapter de auditoria descritos | criar contratos de verificação das novas produtoras |
| tools/skill_enforcement/se07_policy.py | validação do registry pela CLI se07_policy.py | I: presença, enumerações e cardinalidade 14 | validação estrutural não demonstra semântica; enforce requer L4 |
| tools/skill_enforcement/certify_local.py | perfis cumulativos se01–se08 | I parcial + README integral: Git state, logs, renderer, evidência externa | assertions históricas sobre árvore mutável exigem separação histórica/prospectiva aceita no ADR-0022; implementação SER pendente |

## Mapa 14/14

| Skill | Recursos existentes e símbolos | Profundidade | Efeitos/compatibilidade | Artefatos ainda necessários |
|---|---|---|---|---|
| hub-ml-criar-objeto | scripts/run.py::generate/apply; preflight; tools/skill_enforcement/validate_create_readme.py; moldes hub_padroes; tools/validate_assistant.py | D + árvore; comportamento e limites no SKILL | geração separada de escrita; piloto Windows/NTFS; validator repo-side não publicado | cobertura por tipo/operação/host, validação de bytes por tipo, Receipt e autorização; não generalizar piloto |
| hub-ml-explainability | ml.shap_explainer::compute_shap, get_feature_importance_shap, plot_shap_global/local; ml.explainability_report | P/I para SHAP; D para relatório | numpy/pandas; SHAP carregado na chamada; Kernel pode subamostrar; gráficos podem salvar arquivo | contrato, preflight, runner, Receipt, método/output_index/linhas efetivas; dependência ausente bloqueia |
| hub-ml-analise-safra | ml.vintage_analysis::build_vintage_table, compare_safras, plots; spark.date_features | P/I para core vintage; D para calendário | pandas; safra month/quarter; target binário; cobertura incompleta gera NaN, não zero | contrato/preflight e Receipt de população, MOB, denominadores, maturidade; não universalizar estimando |
| hub-ml-validacao-estatistica | ml.drift_detection::calculate_psi, calculate_ks, calculate_csi, detect_drift_all_features; spark.smart_sample, psi_calculator, null_summary | P para drift; D para demais | diagnóstico amostral/distribucional não implementa todo teste descrito no SKILL | plano/contrato/preflight, catálogo aprovado de cálculos, efeitos/incerteza/correções aplicáveis, runner/Receipt |
| hub-ml-cross-eda-ml | spark.join_diagnostics::diagnosticar_join; spark.pit_join::pit_join; quick_profile/schema_to_yaml | P para diagnosticar_join; I para pit_join; D para auxiliares | PIT executa ações Spark/count/collect; atraso obrigatório, fuso e desempate; não escreve tabela | contexto L2, condição PIT, runner/Receipt e Postflight de disponibilidade/cardinalidade |
| hub-ml-feature-engineering | spark.pit_join::pit_join; ml.lgbm_temporal::create_temporal_features; spark.date_features; ml.woe_iv_calculator; hub_scripts.rfv_calculator; ml.split_temporal::temporal_split | I PIT; P split; D restantes | Spark e pandas distintos; fit somente treino; materialização não é implícita | contrato/preflight temporal; bindings de janelas/cutoff; rota de materialização autorizada; Receipt/Postflight |
| hub-ml-baseline-ml | ml.split_temporal::temporal_split; ml.mlflow_run::run_governado; ml.walk_forward; wrappers de treino e metrics_report | P split; P/I tracking; D wrappers | tracking escreve estado externo; bibliotecas opcionais; modelos/tarefas heterogêneos | contexto/split canônico, runner configurável sem algoritmo universal, Receipt/Postflight e verificação de registro real |
| hub-ml-monitoramento-modelo | ml.performance_monitor::PerformanceMonitor, selecionar_metricas_do_relatorio; ml.drift_detection; spark.psi_calculator; hub_scripts.drift_detector | P performance/drift; D demais | métricas não criam alertas/jobs/retreino automaticamente; target pode não estar maturado | L2 janela/thresholds/maturidade, L3 métricas, L4 fronteira autorizada de ação e Postflight |
| hub-ml-pipeline-builder | hub_scripts.data_quality_check, schema_to_yaml, naming_checker; spark.safe_display; templates/pipeline_spec.md | D + template encontrado | diagnóstico/spec não são executores de deploy/write/run | contrato/preflight read-only, executor canônico de efeito autorizado, verificação no destino, Receipt/Postflight/cleanup |
| hub-ml-eda-profissional | quick_profile, data_quality_check, null_summary, smart_sample, safe_display, correlation_matrix, distribution_grid; engine SEF | D + entrypoints e contrato existentes | Spark, coleta limitada, tema opt-in; rota L4 já vigente | somente regressões/interoperabilidade; dívidas analíticas históricas preservadas |
| hub-ml-auditoria-skills | preflight/run e templates de auditoria; adapter EDA verify_finalized | D + arquivos encontrados | read-only sobre evidência; own Receipt não valida produtora | adapters novos somente quando contratos de verificação forem definidos; sem falso PASS |
| hub-ml-comentar-notebook | doc_coverage, helpers visuais e format_br; contrato e cinco templates | D + contrato/templates encontrados | edição editorial, preservação do código | não há promoção; validar regressões proporcionais |
| hub-ml-concierge | índices/Manual/contrato/templates; descoberta de helpers conforme tarefa | D + pacote encontrado | read-only; exemplos/testes do pacote não são execução de especialista | não há promoção; preservar cobertura e handoff |
| hub-ml-tutor-databricks | safe_display, smart_sample, format_br opcionais; três templates | D + templates encontrados | explicar não autoriza executar | não há promoção; L0 mantido |

Prefixos abreviados ml/spark nesta tabela significam hub_snippets.ml/hub_snippets.spark. Não são assinaturas prontas para copiar.

## Achados de implementação para os próximos desenhos

**SHAP:** compute_shap retorna valores e base, não identificadores das linhas subamostradas internamente no modo Kernel. A SER02 deve vincular a população efetiva: por exemplo, controlar previamente a amostra via recurso adequado e impedir nova subamostragem silenciosa. A estratégia exata deve ser testada; não copiar o algoritmo de SHAP nem afirmar explicação de toda a base quando só uma amostra foi calculada. Tree/linear/kernel e output_index possuem validações diferentes.

**Safra:** build_vintage_table usa grão mensal/trimestral, MOB inteiro não negativo e target 0/1. Agrupa contrato×MOB, exige monotonicidade quando target já cumulativo e não calcula taxa acumulada em célula com cobertura incompleta. Isso sustenta um núcleo específico; não prova fluxos monetários ou todos os conceitos de maturidade de negócio.

**PIT:** a implementação recebe atraso_publicacao_dias obrigatório e opcionalmente devolve disponibilidade. Calcula disponibilidade por referência + atraso constante, usa fuso da sessão e possui política de empate. Fontes com latência variável/bitemporalidade não ficam certificadas automaticamente. A camada SER deve verificar a premissa e falhar quando o contrato da fonte não couber no helper.

**Tracking:** run_governado exige MLflow, texto de dataset/split/limitações e registro mínimo. Os textos não comprovam que o modelo realmente usou aquele split. A SER10 deve ligar dados/split/params ao run efetivo e conferir artefatos, sem importar a classe privada _RunGovernado como API pública. Falhas podem deixar efeito externo; cleanup não é presumido.

## Testes existentes versus cobertura necessária

Há suites SEF concretas: tools/tests/test_skill_enforcement_se01.py até se08, test_skill_enforcement_se04_runner.py, test_skill_enforcement_se05_runner.py, test_skill_enforcement_policy_io.py, test_certify_local.py, test_certify_storage_cleanup.py, test_se08_windows_corrective.py e test_se08_cleanup_diagnostics.py. O pacote concierge também contém tests/test_validador.py e tests/validar_pacote.py.

Não foi feita nesta rodada uma enumeração exaustiva dos testes analíticos de cada helper. A cobertura de cada primitive permanece **NOT_ESTABLISHED_BY_SER00**: antes de reutilizá-la como gate, localizar testes, ler assertions e executar casos sintéticos adversariais no host pertinente. Teste de helper, teste de wrapper, integração no Free e aderência do agente são quatro provas diferentes. Esta limitação é um débito explícito da conclusão da SER00, não um PASS implícito.
