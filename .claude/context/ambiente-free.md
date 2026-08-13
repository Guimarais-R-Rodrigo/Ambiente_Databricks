# Contexto — Ambiente Free Edition (laboratório)

- Databricks Free Edition, conta pessoal (username = e-mail Gmail do Rodrigo).
- Databricks CLI instalada e autenticada nesta máquina (`databricks current-user me`).
- Somente compute serverless, Python/SQL; sem jobs permanentes, sem serving.
- Publicação via engine `databricks-genie` do Verg_Alchemy_Hub (ADR-0002):
  render (dry-run) → publish (`--execute`) → verify. O Hub já publica uma
  camada global própria (`global-*`); a camada deste projeto não deve
  sobrescrevê-la — coordenar targets no manifesto.
- Papel: executar os gates pendentes da auditoria do Codex — testes Spark
  serverless dos helpers, forward tests das 12 skills (caso positivo, negativo,
  `@menção`, sempre em chat novo), calibração das descriptions.
- Somente dados sintéticos; nada do banco.
