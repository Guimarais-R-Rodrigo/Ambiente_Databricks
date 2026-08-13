# Regra — Free Edition vs. workspace do trabalho

Dois ambientes com papéis distintos. Nunca trate "passou no Free" como "validado
para o trabalho" sem conferir esta matriz.

| Dimensão | Databricks Free (laboratório) | Trabalho (Azure Databricks) |
|---|---|---|
| Acesso | CLI configurada nesta máquina | **sem CLI**; outro computador; cópia manual |
| Compute | somente serverless, Python/SQL | conforme políticas do workspace |
| Dados | **somente sintéticos** — nunca dados reais do banco | dados reais, governados |
| Publicação | engine `databricks-genie` do Hub (gated `--execute`) | runbook de cópia manual |
| Valida | estrutura das skills, descoberta/`@menção`, código Spark serverless, forward tests | runtime real, permissões, Unity Catalog, dados reais |
| Não valida | jobs permanentes, serving, políticas corporativas, ACLs | — |

## Guardrails

- Nenhum dado real, tabela real, path corporativo ou identificador do banco entra
  no Free nem neste repositório. Fixtures sintéticas sempre.
- Publicação no Free é dry-run por padrão; `--execute` é gate consciente.
- Toda diferença de comportamento encontrada entre Free e trabalho vira nota na
  matriz acima (atualize esta regra) e entrada no CHANGELOG.
- No trabalho, o username muda (placeholder `<username-trabalho>`): a replicação
  usa o runbook, nunca busca/substituição improvisada.
