# Testes Spark serverless dos helpers

Gate da fase 3 (herdado da auditoria do Codex): executar `x_snippets`/`x_scripts`
no runtime Databricks real. Executor: job serverless one-time no Free Edition,
notebook [tools/spark_smoke_test.py](../../../tools/spark_smoke_test.py)
(importado em `/Users/<username>/x_lab/`), dados 100% sintéticos.

## Resultado — 2026-08-13 (Spark 4.1.0 serverless) ✅ APROVADO

| Rodada (run_id) | Resultado | O que revelou |
|---|---|---|
| 1 (…638992) | FAIL | bug do próprio notebook de teste (`import *` em função) |
| 2 (…610980) | FAIL | `spark.conf.get` de config de cluster é bloqueado no serverless (só o sumário) |
| 3 (…004103) | 56 PASS / 8 FAIL | **3 defeitos reais do ambiente** (abaixo) |
| 4 (…266634) | 62 PASS / 2 FAIL | restavam `cache()` em `quick_profile` e `drift_detector` |
| 5 (…159902) | **64 PASS / 0 FAIL / 7 opcionais ausentes** | gate aprovado — [JSON bruto](resultados/2026-08-13_smoke_run5.json) |
| 6 (…314130) | 64 PASS / 0 FAIL | regressão após parametrizar o caminho — [JSON bruto](resultados/2026-08-14_smoke_run6_parametrizado.json) |

## Defeitos reais encontrados e corrigidos no `ambiente_fonte/`

Nenhum deles era detectável pela validação estática (AST compilava na máquina
local com Python 3.12):

1. **`spark` como global inexistente** — `null_summary` e os 5 `x_scripts`
   (`quick_profile`, `data_quality_check`, `rfv_calculator`, `drift_detector`,
   `schema_to_yaml`) referenciavam o global de notebook `spark`, que não existe
   quando o módulo é importado (`NameError`). Correção: `df.sparkSession` no
   snippet e `SparkSession.getActiveSession() or ...getOrCreate()` nos scripts.
2. **`cache()`/`unpersist()` proibidos no serverless** (`NOT_SUPPORTED_WITH_SERVERLESS`)
   — em `safe_display` (removido: o prefixo `limit+1` já limita custo) e em
   `quick_profile`/`drift_detector` (guardas `_cache_if_supported`/`_unpersist_quietly`,
   preservando o cache em compute clássico do trabalho).
3. **f-string com backslash em `kpi_card.py`** — sintaxe PEP 701, válida só em
   Python ≥ 3.12; o runtime usa versão anterior. Escapes movidos para fora da
   f-string.

## Dependências opcionais ausentes no Free (esperado)

`lightgbm`, `xgboost`, `catboost`, `optuna`, `torch` (×2 módulos) — 7 módulos de
`x_snippets/ml` só importam com as libs instaladas no ambiente do projeto
consumidor (`x_snippets/requirements-optional.txt`). Testá-los com versões
fixadas continua como gate específico por workflow.

## Como ler uma falha

O relatório classifica cada verificação em três estados, e a diferença entre eles
decide o que fazer:

| Estado | Significado | Ação |
|---|---|---|
| `PASS` | executou como esperado | nenhuma |
| `OPTIONAL_MISSING` | biblioteca opcional não instalada neste ambiente | nenhuma no laboratório; instalar com versão fixada no projeto que precisar do módulo |
| `FAIL` | defeito real no código ou incompatibilidade com o runtime | corrigir no `ambiente_fonte/` e reexecutar |

Um `FAIL` costuma cair em um de três padrões, todos vistos na primeira execução
deste projeto. `NameError` sobre `spark` indica código contando com a variável
global de notebook dentro de um módulo importado. `NOT_SUPPORTED_WITH_SERVERLESS`
aponta operação que o compute serverless recusa, tipicamente `cache()`.
`SyntaxError` significa que o runtime tem uma versão de Python anterior à que a
sintaxe exige — foi o caso de uma f-string com barra invertida, válida a partir
do Python 3.12.

Um detalhe que engana: teste que passa na máquina local não prova nada sobre o
runtime. Os três defeitos acima compilavam sem erro aqui e só apareceram lá.

## Portabilidade

O notebook resolve o caminho da biblioteca pelo usuário logado e aceita o widget
`assistant_root` para sobrepor. Com isso roda também no workspace do trabalho,
onde não há CLI: basta importá-lo e executar pela interface (passo 6.3 do
[runbook de replicação](../../playbooks/replicacao-trabalho.md)).

## Reexecutar

```powershell
databricks workspace import "/Users/<username>/x_lab/spark_smoke_test" --file tools\spark_smoke_test.py --format SOURCE --language PYTHON --overwrite
databricks jobs submit --json '{"run_name":"smoke","tasks":[{"task_key":"smoke","notebook_task":{"notebook_path":"/Users/<username>/x_lab/spark_smoke_test"}}]}'
```
