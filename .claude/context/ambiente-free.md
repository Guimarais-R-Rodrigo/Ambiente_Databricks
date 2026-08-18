# Contexto — Ambiente Free Edition (laboratório)

- Databricks Free Edition, conta pessoal (username = e-mail Gmail do Rodrigo).
- Databricks CLI instalada e autenticada nesta máquina (`databricks current-user me`).
- Somente compute serverless, Python/SQL; sem jobs permanentes, sem serving.
- Publicação via engine `databricks-genie` do Verg_Alchemy_Hub (ADR-0002):
  render (dry-run) → publish (`--execute`) → verify.
- Estado do workspace desde 2026-08-13: réplica deste projeto (a pedido do
  Rodrigo, a camada global `global-*` do Hub foi removida junto com o ambiente
  anterior; backup no scratchpad da sessão e fonte canônica no repo do Hub, que
  pode republicá-la com `databricks-genie publish-global --execute`). Se a
  camada global voltar, coordenar targets para não sobrescrever.
- Papel: executar os gates pendentes da auditoria do Codex — testes Spark
  serverless dos helpers, forward tests das skills (caso positivo, negativo,
  `@menção`, sempre em chat novo), calibração das descriptions.
- Somente dados sintéticos; nada do banco.
