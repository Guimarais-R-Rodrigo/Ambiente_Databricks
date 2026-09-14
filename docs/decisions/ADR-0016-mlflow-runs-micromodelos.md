# ADR-0016 — MLflow registra runs; YAML registra definição

Data: 2026-09-14
Status: Proposto
Autor: ChatGPT

## Contexto

Micromodelos precisam preservar histórico de experimentos, validações e scorings: população, contagens de classificação, estatísticas de score, parâmetros e identidade da especificação. Colocar esse histórico no YAML faria a especificação crescer a cada execução e misturaria definição com operação.

O Hub já possui `hub_snippets.ml.mlflow_run` para registro governado de runs.

## Decisão

Usar MLflow como backend preferencial de histórico das execuções relevantes e manter `micromodelo.yaml` como definição/política.

Tipos planejados de run: `DEVELOPMENT`, `VALIDATION` e `SCORING`.

Tracking registra agregados, parâmetros, tags e artifacts. Resultados individuais por entidade permanecem na camada de dados governada e não são armazenados como artifacts de tracking.

## Alternativas consideradas

- Histórico dentro do YAML — rejeitada por misturar especificação e operação.
- Nova tabela de tracking própria no MVP — rejeitada porque MLflow já cobre a necessidade central.
- Run por entidade — rejeitada por escala, privacidade e semântica incorreta da unidade de execução.

## Consequências

- MM06 deve avaliar uma extensão aditiva do `mlflow_run` para micromodelos sem artefato sklearn.
- O contrato atual de modelos tradicionais deve permanecer retrocompatível.
- A política de métricas da run poderá ser declarada no YAML.

## Referências

- `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/`
- `docs/sprints/micromodelos/PLANO_MESTRE.md`
