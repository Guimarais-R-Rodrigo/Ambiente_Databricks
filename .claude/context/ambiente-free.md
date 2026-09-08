# Contexto — Ambiente Free Edition (laboratório)

- Databricks Free Edition, conta pessoal; username resolvido pela CLI em runtime
  e nunca persistido no repositório.
- Databricks CLI instalada e autenticada nesta máquina (`databricks current-user me`).
- Somente compute serverless, Python/SQL; sem jobs permanentes, sem serving.
- Publicação via `tools/publicar_free.py` (ADR-0005), com critério de
  conferência no ADR-0008: render → plano → `--execute` → `--verify`.
- Estado do workspace desde 2026-08-13: réplica deste projeto (a pedido do
  Rodrigo, a camada global `global-*` do Hub foi removida junto com o ambiente
  anterior; backup no scratchpad da sessão e fonte canônica no repo do Hub, que
  pode republicá-la com `databricks-genie publish-global --execute`). Se a
  camada global voltar, coordenar targets para não sobrescrever.
- Papel: executar os gates pendentes da auditoria do Codex — testes Spark
  serverless dos helpers, forward tests das skills (caso positivo, negativo,
  `@menção`, sempre em chat novo), calibração das descriptions.
- Estado em 2026-08-29: commit `02a5ad3` publicado e conferido (315 arquivos,
  0 ausente/obsoleto); smoke pós-correção aprovado no Spark 4.2.0. O chat segue
  bloqueado por cota até 01/09, impedindo prompts e os 3 forward tests pendentes.
- Somente dados sintéticos; nada do banco.
