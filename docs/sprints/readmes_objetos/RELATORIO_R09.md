# Relatório R09 — avaliação, drift e MLOps

## Escopo

Documentar cinco objetos R09/A: `curves_plotly`, `drift_detection`, `metrics_report`, `mlflow_run` e `performance_monitor`, preservando implementação/fachada e corrigindo apenas documentação quando necessário.

## Meta de cobertura

Base integrada: 55/75 objetos operacionais, 20 pendências. Meta candidata: **60/75 operacionais, 3/3 exemplares e 15 pendências**, sujeita ao validador como fonte de verdade.

## Alterações além dos READMEs

Esta sprint não se limita aos cinco novos guias. O fechamento deve registrar nominalmente: backlinks/correções editoriais nos cinco notebooks; catálogo de Hub Snippets; Manual Técnico e cópias; README raiz; `CLAUDE.md`; `PLANO_HUB.md`; índices de sprints; controle de migração; CHANGELOG; achados, matriz, rubrica e verificadores; além das cópias do simulado regeneradas pelo renderer.

## Limites

Nenhuma implementação ou fachada dos cinco objetos pode mudar. Observações históricas de runtime são preservadas como evidência datada, não promovidas a regra atual. Nenhum resultado desta sprint equivale a publicação/homologação Databricks ou auditoria independente.

## Validação planejada

- contrato README 1.0.0 e cobertura 60/75;
- gate permanente e regressões V00–V04;
- preservação byte a byte das dez peças executáveis de produto e preservação do código/magics/outputs dos notebooks;
- runtime core para curvas, métricas, drift e monitor;
- runtime MLflow isolado com tracking local, sem depender do workspace Databricks;
- reconferência final e materialização de uma única árvore candidata.

## Estado

Em elaboração. O resultado dos testes e a árvore final só serão registrados após execução fail-closed.
