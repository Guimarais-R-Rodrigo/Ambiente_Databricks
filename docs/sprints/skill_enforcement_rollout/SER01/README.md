# SER01 — criar-objeto: rollout L2 → L3

Estado: **IN_PROGRESS / A3_COMPLETE / A4_PREPARED_NOT_RUN**.

A3 encerrou a prova local prospectiva da superfície `object_validation` em `fcec3e34898006081b3e9063c627b5783108687f`: `SER-CERT-1` PASS, certificado verificável, 27/27 steps únicos, route/evidence gates PASS, regressões/CI/SE08 históricos verdes e push fast-forward do mesmo SHA certificado. A policy continua em L2.

A4 não altera o produto certificado. Ela acrescenta somente instrumentos externos de prova:

- [A4-FREE](A4_RUNBOOK_FREE.md): publicação/verify por conteúdo e portabilidade do verifier no Databricks Free;
- [A4-GENIE](A4_GENIE_CASES.md): aderência comportamental quando a rota repo-side está indisponível, Receipt é ausente/inválido ou possui autoridade limitada.

## Navegação

- [Desenho e limites](DESENHO_TECNICO.md)
- [Matriz operação, tipo, host e efeito](MATRIZ_OPERACAO_TIPO_HOST_EFEITO.md)
- [Testes](TESTES.md)
- [Resultados](RESULTADOS.md)
- [Checkpoint](CHECKPOINT.md)
- [A4 Free](A4_RUNBOOK_FREE.md)
- [A4 Genie](A4_GENIE_CASES.md)

## Estado de autoridade

```text
CURRENT_LEVEL = L2_UNCHANGED
TARGET_LEVEL = L3_UNCHANGED
ROLLOUT_MODE = audit_UNCHANGED
A3_SER_CERT = PASS
A4_FREE = NOT_RUN
A4_GENIE = NOT_RUN
POLICY_PROMOTION = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
SER02 = NOT_STARTED
```

A4-FREE pode provar que o verifier publicado funciona no runtime e que o pacote remoto corresponde à fonte; não pode transformar a primitive repo-side em capacidade do workspace. A4-GENIE mede essa fronteira explicitamente.
