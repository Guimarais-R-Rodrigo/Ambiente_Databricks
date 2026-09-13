# Recuperação da R09 — 2026-09-13 (ChatGPT)

## Resultado e alcance

Recuperação baseada no commit integrado `d5945e04328609878f63857cc15cf5e5039b3e75`. A construção anterior `bfa7b848517ce4b3087ec4cf6b9260cd9a2bfe6c` continha reescritas fora do escopo documental. Os sete arquivos abaixo foram restaurados byte a byte; os cinco novos READMEs foram preservados sem reescrita.

| Arquivo restaurado | Linhas antes | Linhas recuperadas |
|---|---:|---:|
| `ambiente_fonte/.assistant/hub_snippets/README.md` | 42 | 514 |
| `docs/sprints/readmes_objetos/README.md` | 34 | 59 |
| `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/exemplo_curves_plotly.py` | 94 | 132 |
| `ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/exemplo_drift_detection.py` | 94 | 191 |
| `ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/exemplo_metrics_report.py` | 70 | 114 |
| `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/exemplo_mlflow_run.py` | 89 | 158 |
| `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/exemplo_performance_monitor.py` | 74 | 115 |

## Correção do relato anterior

A descrição anterior de alterações exclusivamente editoriais estava incorreta. Além de remover conteúdo e saídas históricas, a edição de `exemplo_mlflow_run.py` modificou os literais de `limitacoes`, alterando dados efetivamente enviados ao MLflow. Houve também mudanças de formatação e comentários executáveis em outros exemplos. A recuperação repõe os arquivos completos, sem alegar que equivalência de AST seria suficiente para preservar magics ou saídas.

Notebooks cuja AST Python havia mudado: `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/exemplo_mlflow_run.py`.

## Documentações alteradas além dos novos READMEs

Foram restaurados o catálogo `hub_snippets/README.md`, o índice `docs/sprints/readmes_objetos/README.md` e os cinco notebooks listados. Foram acrescentados este registro, uma nota no relatório R09, uma nota na matriz R09 e uma entrada no `CHANGELOG.md`. O Manual, os agregadores restantes e o simulado não são modificados nesta recuperação.

## Evidência

Run de recuperação: `34764123678`. Conferências: sete arquivos iguais aos bytes da base; cinco READMEs iguais à construção anterior; dez implementações/fachadas iguais à base; metadados das quinze pendências restantes preservados. As provas incluem hashes SHA-256 e comparação de AST antes da restauração. Não houve execução de notebooks ou modelos.

## Pendências e próxima ação

R09 continua EM ELABORAÇÃO, sem PR final, freeze aprovado ou merge. As menções a R08 candidata no índice restaurado são históricas e deverão ser atualizadas cirurgicamente na integração R09; a R08 já foi integrada pelo PR #27. A retirada das cinco dispensas existe apenas na branch em construção e não certifica conclusão.

Reaplicar backlinks e erratas por alterações pontuais que preservem código, magics, comentários executáveis, saídas históricas, imagens e navegação. Reintegrar catálogo, Manual, índices e simulado. Reforçar o verificador que atualmente ignora indiscriminadamente linhas `# MAGIC`. Corrigir a asserção incorreta de unicidade de FPR na suíte core: curvas ROC podem ter segmentos verticais. Depois executar gate completo e runtimes isolados, com evidências por árvore e versões.

Sem publicação/homologação Databricks, aprovação de modelo, auditoria independente ou início da R10.
