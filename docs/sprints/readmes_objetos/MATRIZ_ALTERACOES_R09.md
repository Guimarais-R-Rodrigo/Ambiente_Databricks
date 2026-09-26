# Matriz de alterações R09

## Novos READMEs canônicos

- `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/README.md`

## Documentação não-README da candidata final

- cinco notebooks `exemplo_<objeto>.py`: somente backlinks/erratas Markdown declaradas em `evidencias_r09/aplicar_r09.py`; a guarda reverte essas substituições e exige equivalência byte a byte com a base;
- `ambiente_fonte/.assistant/hub_snippets/README.md`: bloco R09 inserido sem substituir o catálogo histórico;
- `README.md`: checkpoint R09 e snapshot de contagens gerado a partir do validador;
- `docs/sprints/README.md` e `docs/sprints/readmes_objetos/README.md`: navegação/checkpoint da iniciativa;
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`: retirada de exatamente cinco pendências R09/A;
- `CHANGELOG.md`: o registro de recuperação da própria R09 permanece como entrada histórica da leva;
- `ACHADOS_R09.md`, `MATRIZ_ALTERACOES_R09.md`, `RELATORIO_R09.md`, `RUBRICA_R09.json`, `RECUPERACAO_R09.md` e `evidencias_r09/*`: evidência auditável;
- `Novo_Ambiente_Simulado/**`: apenas as cópias derivadas dos arquivos-fonte efetivamente alterados, geradas pelo renderer.

## Documentos deliberadamente não alterados após a recuperação

`MANUAL_TECNICO.md`, `CLAUDE.md` e `PLANO_HUB.md` permanecem iguais à base integrada. O Manual já contém capítulos de métricas, MLflow e monitoramento; adicionar checkpoint redundante nesta leva aumentaria superfície de mudança sem ampliar o contrato operacional dos cinco objetos.

## Fora de escopo

As cinco implementações e cinco fachadas públicas permanecem byte a byte iguais à base integrada. Não há publicação/homologação Databricks, alteração de política de modelo, retreino automático ou mudança funcional nesta sprint documental.

## Recuperação de preservação — 2026-09-13

A construção anterior foi interrompida por reescritas excessivas de catálogo/índice e notebooks. Os sete arquivos foram restaurados integralmente da base integrada antes desta integração mínima. Consulte [RECUPERACAO_R09.md](RECUPERACAO_R09.md). A recuperação e o freeze técnico são evidências distintas.
