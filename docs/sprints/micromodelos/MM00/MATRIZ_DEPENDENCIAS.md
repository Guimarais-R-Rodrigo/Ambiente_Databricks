# MM00 — Dependências

## Sequência

MM00 → MM01 → MM02 → MM03 → MM04 → MM05 → MM06 → MM07 → MM08 → MM09 → MM10 → MM11 → MM12 → MM13.

## Gates principais

- MM01 depende do aceite da MM00.
- MM06 depende do contrato YAML e da skill principal.
- MM08 depende do pacote departamental aprovado.
- MM09 depende da homologação técnica.
- MM12 depende do piloto novo concluído e do freeze V1.

## Reuso obrigatório

O framework deve verificar antes de criar: padrões de skill, prompt, notebook, proveniência e auditoria; skills de EDA, cross-EDA, feature engineering, validação e documentação; helpers `schema_to_yaml`, `join_diagnostics`, `pit_join` e `mlflow_run`.

## Visual

A integração visual é tardia. MM11 reconsulta o estado vigente do Sistema de Temas e não congela API futura na MM00.
