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

## Diferenças de runtime já observadas

Registradas a partir da execução no laboratório (Spark 4.1 serverless, 2026-08-13):

| Comportamento | Free (serverless) | Trabalho (compute conforme política) |
|---|---|---|
| `cache()` / `persist()` | **bloqueado** (`NOT_SUPPORTED_WITH_SERVERLESS`) | disponível em compute clássico |
| `spark.conf.get` de config de cluster | bloqueado | normalmente disponível |
| Bibliotecas ML opcionais (LightGBM, XGBoost, CatBoost, Optuna, PyTorch) | ausentes | confirmar disponibilidade e fixar versão |
| Variável global `spark` dentro de módulo importado | inexistente (vale nos dois) | inexistente |

Os helpers foram ajustados para funcionar nos dois casos: degradam sem cache no
serverless e mantêm o cache onde ele existe.

## Guardrails

- Nenhum dado real, tabela real, path corporativo ou identificador do banco entra
  no Free nem neste repositório. Fixtures sintéticas sempre.
- Publicação no Free é dry-run por padrão; `--execute` é gate consciente.
- Toda diferença de comportamento encontrada entre Free e trabalho vira nota na
  matriz acima (atualize esta regra) e entrada no CHANGELOG.
- No trabalho, o username muda (placeholder `<username-trabalho>`): a replicação
  usa o runbook, nunca busca/substituição improvisada.
