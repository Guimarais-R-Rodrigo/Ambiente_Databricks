# Matriz de alterações R09

## Novos READMEs canônicos

- `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/README.md`

## Documentação não-README prevista

- cinco notebooks `exemplo_<objeto>.py`: backlink e correções exclusivamente editoriais;
- `ambiente_fonte/.assistant/hub_snippets/README.md`: catálogo e links R09;
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md` e cópias derivadas: catálogo/continuidade;
- `README.md`, `CLAUDE.md`, `PLANO_HUB.md`: checkpoint da iniciativa;
- `docs/sprints/README.md` e `docs/sprints/readmes_objetos/README.md`: índices e cobertura;
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`: retirada de exatamente cinco pendências R09/A;
- `CHANGELOG.md`: registro da leva;
- `ACHADOS_R09.md`, `MATRIZ_ALTERACOES_R09.md`, `RELATORIO_R09.md`, `RUBRICA_R09.json` e `evidencias_r09/*`: evidência auditável;
- `Novo_Ambiente_Simulado/**`: somente derivados produzidos pelo renderer.

## Fora de escopo

As cinco implementações e cinco fachadas públicas devem permanecer byte a byte iguais à base integrada. Não há publicação/homologação Databricks, alteração de política de modelo ou mudança funcional nesta sprint documental.


## Recuperação de preservação — 2026-09-13

A construção anterior foi interrompida por reescritas excessivas de catálogo/índice e notebooks. Os sete arquivos foram restaurados integralmente da base integrada; os cinco novos READMEs permanecem na branch. Consulte [RECUPERACAO_R09.md](RECUPERACAO_R09.md) para arquivos, evidências e pendências. Backlinks, erratas e integração transversal precisam ser reaplicados pontualmente. Esta recuperação não aprova o freeze nem os runtimes da R09.
