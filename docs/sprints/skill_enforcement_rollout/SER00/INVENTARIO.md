# SER00 — inventário e reconciliação

## Identidade da baseline

```text
REPOSITORY = Guimarais-R-Rodrigo/Ambiente_Databricks
MAIN = 11851e137dd7793b351ac08fc211c0be90005dee
ROOT_TREE = 76d5a7eec8293fd070eb518d4c48f72bbae32f2f
POLICY_BLOB = 01cabb4dc45e7a2349e4b1630e3a322c4da75d6c
SKILLS_TREE = d4ff7acde0d8402f31bc15180b23f104d1a490e3
```

A main foi reconfirmada durante a leitura, sem commits posteriores ao SHA esperado nessa observação. A PR #98 está integrada. Cabeçalhos documentais PSEF00 que ainda dizem candidata não substituem o estado Git. A criação da branch SER partiu dessa main, sem incorporar #99, #51 ou #91.

## Reconstrução SEF

| Bloco | Contrato construído | Estado histórico preservado |
|---|---|---|
| SE01 | contratos L1, AST/fachada pública, required/conditional/optional | infraestrutura; não execução |
| SE02 | preflight read-only | resolver recursos não prova chamada |
| SE03 | core EDA canônico e Trace | execução/proveniência; falhas comportamentais antigas preservadas |
| SE04 | ExecutionReceiptV1 | Receipt válido não equivale a conclusão L4 |
| SE05 | run_enforced e Postflight | somente PASS autoriza completion |
| SE06 | campanha de comportamento e bypass | 24/25; S06-A1-R4 NOT_RUN; DoD INCOMPLETE |
| SE07 | policy 14/14, auditor L3, piloto criar-objeto | aceite com ressalva de storage; FULL não apaga falha específica; SE07_FULLY_CERTIFIED=false |
| SE08 | operação permanente e certificação | RC certificada, integrada e pós-merge Actions PASS; não reaberta |

SE08: RC `ee1cf04b031497bb5b7ddfa47ce28b8015d15668`; integração técnica PR #90; corretiva PR #92; fechamento documental PR #93. Os registros preservam LOCAL_CERTIFICATION=PASS, FULL_SE08_LOCAL=PASS, DATABRICKS_FREE=PASS e GENIE_BEHAVIORAL_SCREENING=NOT_APPLICABLE. A ausência de WinError32 na R5 não foi convertida em prova de causa-raiz corrigida. A PR #91 aberta é uma candidata alternativa antiga, não o novo estado canônico da SE08. Nenhum desses PASS foi herdado pela SER.

## Estrutura real 14/14

As subárvores das 14 skills foram enumeradas pela API Git Trees no SHA fixado; 104 arquivos no total, incluindo 61 templates Markdown. Diretórios não entram na contagem. A contagem não inclui o README do catálogo.

| Skill | Arquivos / templates | Contrato | Preflight | Runner | Receipt | Postflight |
|---|---|---|---|---|---|---|
| hub-ml-analise-safra | 2 / 1 | NAO | NAO | NAO | ABSENT | NAO |
| hub-ml-auditoria-skills | 8 / 3 | SIM | SIM | SIM | SUPPORTED_NOT_RERUN | NAO |
| hub-ml-baseline-ml | 18 / 17 | NAO | NAO | NAO | ABSENT | NAO |
| hub-ml-comentar-notebook | 7 / 5 | SIM | NAO | NAO | ABSENT | NAO |
| hub-ml-concierge | 17 / 3 | SIM | NAO | NAO | ABSENT | NAO |
| hub-ml-criar-objeto | 7 / 1 | SIM | SIM | PILOTO | PILOT_ONLY | NAO |
| hub-ml-cross-eda-ml | 7 / 6 | NAO | NAO | NAO | ABSENT | NAO |
| hub-ml-eda-profissional | 11 / 4 | SIM | SIM | SIM | SUPPORTED_NOT_RERUN | SIM |
| hub-ml-explainability | 3 / 2 | NAO | NAO | NAO | ABSENT | NAO |
| hub-ml-feature-engineering | 8 / 7 | NAO | NAO | NAO | ABSENT | NAO |
| hub-ml-monitoramento-modelo | 3 / 2 | NAO | NAO | NAO | ABSENT | NAO |
| hub-ml-pipeline-builder | 2 / 1 | NAO | NAO | NAO | ABSENT | NAO |
| hub-ml-tutor-databricks | 4 / 3 | NAO | NAO | NAO | ABSENT | NAO |
| hub-ml-validacao-estatistica | 7 / 6 | NAO | NAO | NAO | ABSENT | NAO |

`SUPPORTED_NOT_RERUN` significa suporte descrito no artefato/contrato vigente, não emissão de Receipt nesta auditoria. A auditoria tem Receipt próprio SE07-AUDIT-RECEIPT-1; não presumir que seja idêntico ao Receipt da EDA. Preflight/runner presentes não dispensam verificar comportamento.

## Templates existentes por skill

Todos os nomes abaixo são relativos à pasta da skill e foram encontrados nas respectivas árvores. A existência foi conferida; a leitura integral de cada template não é declarada.

### hub-ml-analise-safra

`templates/relatorio_safra.md`.

### hub-ml-auditoria-skills

`templates/checkpoints_por_skill.md`, `templates/relatorio_auditoria.md`, `templates/rubrica_universal.md`.

### hub-ml-baseline-ml

`templates/anomaly_profiling.md`, `templates/cluster_profiling.md`, `templates/dl_vs_lgbm_justificativa.md`, `templates/metricas_classificacao.md`, `templates/metricas_ranking.md`, `templates/metricas_regressao.md`, `templates/metricas_report.md`, `templates/metricas_series_temporais.md`, `templates/mlflow_checklist.md`, `templates/notebook_output_baseline.md`, `templates/relatorio_executivo_baseline.md`, `templates/score_bands_table.md`, `templates/scorecard_report.md`, `templates/split_strategy.md`, `templates/suite_selection_guide.md`, `templates/survival_interpretation.md`, `templates/walk_forward_guide.md`.

### hub-ml-comentar-notebook

`templates/bloco_markdown_pos_codigo.md`, `templates/bloco_markdown_pos_compacto.md`, `templates/bloco_markdown_pre_codigo.md`, `templates/bloco_markdown_pre_compacto.md`, `templates/cabecalho_notebook.md`.

### hub-ml-concierge

`templates/handoff.md`, `templates/recomendacao.md`, `templates/registro_busca.md`.

### hub-ml-criar-objeto

`templates/checklist-objeto-novo.md`.

### hub-ml-cross-eda-ml

`templates/coverage_matrix.md`, `templates/inventario_edas.md`, `templates/join_feasibility.md`, `templates/notebook_output_cross_eda.md`, `templates/readiness_scorecard.md`, `templates/relatorio_executivo_cross_eda.md`.

### hub-ml-eda-profissional

`templates/estilo_visual_eda.md`, `templates/matriz_graficos_eda.md`, `templates/relatorio_executivo_eda.md`, `templates/roteiro_eda.md`.

### hub-ml-explainability

`templates/relatorio_executivo_explainability.md`, `templates/shap_analysis_technical.md`.

### hub-ml-feature-engineering

`templates/checklist_validacao_features.md`, `templates/feature_backlog_tiers.md`, `templates/feature_spec_core.md`, `templates/feature_spec_risco_validacao.md`, `templates/feature_taxonomy_cross_source.md`, `templates/mapa_notebooks_alvo.md`, `templates/notebook_output_structure.md`.

### hub-ml-monitoramento-modelo

`templates/drift_report.md`, `templates/retreino_decision.md`.

### hub-ml-pipeline-builder

`templates/pipeline_spec.md`.

### hub-ml-tutor-databricks

`templates/analogias_banking_crm.md`, `templates/explicacao_bloco_codigo.md`, `templates/explicacao_notebook.md`.

### hub-ml-validacao-estatistica

`templates/decisao_pressupostos.md`, `templates/notebook_output_stat.md`, `templates/relatorio_diagnostico.md`, `templates/severity_rubric.md`, `templates/test_plan.md`, `templates/test_result_card.md`.

## Scripts e manifestos

EDA: `scripts/preflight.py`, `scripts/run.py`, `scripts/run_enforced.py`, `scripts/postflight.py`, `release_manifest.json`. Auditoria: `scripts/preflight.py`, `scripts/run.py`, `release_manifest.json`. Criar-objeto: `scripts/preflight.py`, `scripts/run.py`, `scripts/_windows_writer.py`, `release_manifest.json` (runner limitado ao piloto). As demais onze skills não possuem esses entrypoints de enforcement. Os testes locais do pacote concierge não são um runner L2/L3.

## Proveniência das leituras

Foram consultados o índice, Plano Mestre, revisão local-first e README de SE01–SE08; checkpoints SE07/SE08, resultados SE08, ADR-0021, README técnico SEF, schema, trechos do certifier/validator e o validator da policy. Foram lidos os 14 SKILL.md, a policy, instruções globais, seções de skills/README e do Manual, PSEF00/Plano Mestre e estado das PRs. A profundidade foi maior nas superfícies de promoção, não em toda implementação analítica do Hub.

Fontes de controle: `docs/sprints/skill_enforcement/`, `docs/decisions/ADR-0021-execucao-verificavel-de-skills.md`, `tools/skill_enforcement/`, `ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json` e os caminhos de produto. Usar sempre a baseline deste documento para reproduzir achados; referências antigas do Manual são evidência documental datada, não confirmação automática de código atual.

## Preservação de autoria e história

SER00 adiciona somente documentação própria. Produto, policy, skills, engine, prompts, Manual, instruções, ferramentas, workflows e derivado devem conservar os mesmos blobs/trees da baseline. Não corrigir documentos antigos para fazê-los parecer escritos durante a SER. README individual de skill continua excepcional; SKILL.md permanece canônico.
