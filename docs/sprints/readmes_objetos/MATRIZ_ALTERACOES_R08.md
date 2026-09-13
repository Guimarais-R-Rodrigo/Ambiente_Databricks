# Matriz de alterações R08

**Base:** `b73bbb91961f9ba5f9031d648c42ec0891b63347` (main pós-R07)
**Contrato:** README de objeto 1.0.0
**Escopo funcional:** nenhum; implementação/fachadas protegidas.

## READMEs novos

- `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/README.md`

## Documentação não-README alterada

- `CHANGELOG.md`
- `CLAUDE.md`
- `MANUAL_TECNICO.md` (cópia sincronizada a partir do canônico)
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md`
- seis `exemplo_<objeto>.py` da R08 — somente Markdown/backlink/correção didática
- `PLANO_HUB.md`
- `docs/sprints/README.md`
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`
- `docs/sprints/readmes_objetos/README.md`
- `docs/sprints/readmes_objetos/RELATORIO_R08.md`
- `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R08.md`
- `docs/sprints/readmes_objetos/ACHADOS_R08.md`
- `docs/sprints/readmes_objetos/RUBRICA_R08.json`
- `docs/sprints/readmes_objetos/evidencias_r08/aplicar_r08.py`
- `docs/sprints/readmes_objetos/evidencias_r08/verificar_r08.py`
- `docs/sprints/readmes_objetos/evidencias_r08/verificar_preservacao.py`

## READMEs/derivados alterados além dos seis novos

- `README.md` raiz — checkpoint R08 + snapshot derivado do validador.
- `ambiente_fonte/.assistant/hub_snippets/README.md` — rota narrativa R08.
- `Novo_Ambiente_Simulado/**` correspondente — **somente** via `tools/render_simulado.py`.

## Proteções

As seis implementações e seis fachadas da R08 devem permanecer byte a byte iguais à base. Os notebooks preservam código/magics executáveis e blocos de output; apenas a camada Markdown é ajustada. R09 não começa nesta árvore.

- `docs/sprints/readmes_objetos/evidencias_r08/aplicar_r08_v2.py` — entrada compativel com o schema `pending` vigente.

## Inventario nominal final

44 caminhos contra a base; 14 derivados gerados pelo renderer. Workflow temporario ausente da arvore final.

- `CHANGELOG.md`
- `CLAUDE.md`
- `MANUAL_TECNICO.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/README.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/autoencoder_anomaly/README.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/autoencoder_anomaly/exemplo_autoencoder_anomaly.py`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/cluster_profiling/README.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/cluster_profiling/exemplo_cluster_profiling.py`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/clustering_suite/README.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/clustering_suite/exemplo_clustering_suite.py`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/explainability_report/README.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/explainability_report/exemplo_explainability_report.py`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/shap_explainer/README.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/shap_explainer/exemplo_shap_explainer.py`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/umap_viz/README.md`
- `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/umap_viz/exemplo_umap_viz.py`
- `PLANO_HUB.md`
- `README.md`
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md`
- `ambiente_fonte/.assistant/hub_snippets/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/exemplo_autoencoder_anomaly.py`
- `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/exemplo_cluster_profiling.py`
- `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/exemplo_clustering_suite.py`
- `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/exemplo_explainability_report.py`
- `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/exemplo_shap_explainer.py`
- `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/exemplo_umap_viz.py`
- `docs/sprints/README.md`
- `docs/sprints/readmes_objetos/ACHADOS_R08.md`
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`
- `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R08.md`
- `docs/sprints/readmes_objetos/README.md`
- `docs/sprints/readmes_objetos/RELATORIO_R08.md`
- `docs/sprints/readmes_objetos/RUBRICA_R08.json`
- `docs/sprints/readmes_objetos/evidencias_r08/aplicar_r08.py`
- `docs/sprints/readmes_objetos/evidencias_r08/aplicar_r08_v2.py`
- `docs/sprints/readmes_objetos/evidencias_r08/verificar_preservacao.py`
- `docs/sprints/readmes_objetos/evidencias_r08/verificar_r08.py`
