# Matriz de alterações R09

## Novos READMEs canônicos

- `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/README.md`

## Documentação não-README da candidata final

- cinco notebooks `exemplo_<objeto>.py`: somente backlinks/erratas Markdown declaradas em `evidencias_r09/aplicar_r09.py`; a guarda reverte essas substituições e exige equivalência byte a byte com a base;
- `README.md` raiz: checkpoint R09 e snapshot verificável das contagens finais;
- `docs/sprints/readmes_objetos/README.md`: estado, navegação e cobertura da iniciativa;
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`: retirada de exatamente cinco pendências R09/A;
- `CHANGELOG.md`: mantém o registro de recuperação/preservação desta sprint, incluindo que os cinco novos READMEs foram preservados;
- `ACHADOS_R09.md`, `MATRIZ_ALTERACOES_R09.md`, `RELATORIO_R09.md`, `RUBRICA_R09.json`, `RECUPERACAO_R09.md` e `evidencias_r09/*`: evidência auditável;
- `Novo_Ambiente_Simulado/**`: dez cópias derivadas correspondentes aos cinco READMEs e cinco notebooks, byte a byte iguais à fonte.

## Documentos deliberadamente não alterados

`MANUAL_TECNICO.md`, `CLAUDE.md`, `PLANO_HUB.md`, `docs/sprints/README.md` e `ambiente_fonte/.assistant/hub_snippets/README.md` permanecem iguais à base integrada. O catálogo geral já lista os cinco objetos; a navegação específica para a leva fica no índice da iniciativa e nos próprios READMEs.

## Executáveis preservados

As cinco implementações e cinco fachadas públicas permanecem byte a byte iguais à base `d5945e04328609878f63857cc15cf5e5039b3e75`. Nos notebooks, apenas as substituições editoriais registradas são permitidas; código, magics/comentários executáveis e saídas históricas fora delas permanecem preservados.

## Evidências

- recuperação de preservação: run `34764123678`;
- preflight final verde: run `34772841948`;
- artefato do preflight: `10322173358`, digest `sha256:720bc038f4b23a38f15afe8bb12e8cacc7cd1e72175c002c88995e80bf96d40f`;
- cobertura observada no preflight: 60/75 operacionais, 3/3 exemplares e 15 pendências;
- runtime core e MLflow/SQLite local aprovados; sem homologação Databricks.

## Fora de escopo

Não há publicação no Databricks, alteração de política de modelo, retreino automático, mudança funcional nos helpers, auditoria independente ou início da R10.
