# Relatório R09 — avaliação, drift e MLOps

## Escopo

Documentar cinco objetos R09/A: `curves_plotly`, `drift_detection`, `metrics_report`, `mlflow_run` e `performance_monitor`, preservando implementação/fachada e corrigindo somente documentação quando necessário.

## Meta de cobertura

Base integrada: 55/75 objetos operacionais, 20 pendências. Meta candidata: **60/75 operacionais, 3/3 exemplares e 15 pendências**, com o validador como fonte de verdade.

## Alterações além dos READMEs

A candidata mínima inclui: backlinks/erratas Markdown nos cinco notebooks; bloco R09 no catálogo de Hub Snippets; checkpoint e snapshot verificável no README raiz; índices de sprints/iniciativa; controle de migração; registro de recuperação no CHANGELOG; achados, matriz, rubrica, recuperação e verificadores; além das cópias correspondentes do simulado produzidas pelo renderer.

Após a recuperação de preservação, **Manual Técnico, `CLAUDE.md` e `PLANO_HUB.md` foram retirados do escopo final da R09**. O Manual já cobre métricas, MLflow e monitoramento; repetir um checkpoint não é necessário para operar os cinco objetos e ampliaria a superfície de mudança.

## Limites

Nenhuma implementação ou fachada dos cinco objetos pode mudar. Nos notebooks, somente as substituições declaradas no aplicador são autorizadas; a guarda as reverte e exige que o arquivo volte a ser byte a byte igual à base, preservando código, magics, comentários executáveis e saídas históricas.

Observações de runtime são evidência datada. Nenhum resultado desta sprint equivale a publicação/homologação Databricks, autorização de retreino ou auditoria independente.

## Validação

- contrato README 1.0.0 e cobertura 60/75;
- gate permanente, incluindo temas V00–V04 e Concierge;
- preservação byte a byte das dez peças executáveis de produto e equivalência reversível dos cinco notebooks;
- runtime core para curvas, métricas, drift e monitor;
- runtime MLflow isolado em SQLite local, sem depender do workspace Databricks;
- renderer com espelho da fonte publicada;
- CIs permanentes do PR ainda serão exigidas sobre o commit final.

## Estado

Preflight técnico **`34772019675`** aprovado integralmente: validador em 60/75 + 3/3 e 15 pendências, gate completo, preservação estrita, runtime core e runtime MLflow local com MLflow 3.16.0/SQLite. A candidata final ainda requer materialização limpa, CIs do PR e aceite editorial humano.

## Recuperação de preservação — 2026-09-13

A construção anterior foi interrompida por reescritas excessivas de catálogo/índice e notebooks. Os sete arquivos foram restaurados integralmente da base integrada; os cinco READMEs permaneceram. Consulte [RECUPERACAO_R09.md](RECUPERACAO_R09.md). A recuperação não é apresentada como auditoria independente nem como teste no Databricks.
