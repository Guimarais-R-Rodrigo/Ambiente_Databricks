# Testes Spark serverless dos helpers

> **Nomenclatura da época.** Os nomes `x_*` e `rodrigo-*` neste registro são
> os que existiam na data. A correspondência com os nomes atuais está no ADR
> da reestruturação do Hub; este documento não é reescrito porque descreve o
> que foi observado, não o estado atual.

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
| 7 (…965277) | **11 PASS / 0 FAIL** | módulos novos e correção do ranker — [JSON bruto](resultados/2026-08-14_modulos_novos.json) |
| 8 (…191413) | 4 PASS / 1 FAIL | xgboost, optuna, umap e shap verificados; catboost falhou por colisão de run |
| 9 (…632341) | **4 PASS / 0 FAIL** | catboost isolado e `run_governado` — [JSON bruto](resultados/2026-08-14_catboost_mlflow.json) |

Os três estados da tabela não são sinônimos, e a diferença decide o que fazer:

| Estado | Significado | Ação |
|---|---|---|
| `PASS` | executou como esperado | nenhuma |
| `OPTIONAL_MISSING` | biblioteca opcional não instalada neste ambiente | nenhuma no laboratório; instalar com versão fixada no projeto que precisar do módulo |
| `FAIL` | defeito real no código ou incompatibilidade com o runtime | corrigir no `ambiente_fonte/` e reexecutar |

Por isso a rodada 5 fecha o gate com **64 PASS / 0 FAIL / 7 opcionais ausentes**:
são 71 verificações, e as 7 restantes não são falhas. Para diagnosticar um `FAIL`
concreto, veja [Como ler uma falha](#como-ler-uma-falha).

## Módulos com dependência opcional — situação final

**13 dos 14 verificados em runtime.** O conjunto de versões que funciona está em
`x_snippets/requirements-optional.txt`.

| Situação | Módulos |
|---|---|
| **Verificados** (13) | `train_lgbm`, `train_xgboost`, `train_catboost`, `optuna_lgbm`, `lgbm_ranker`, `umap_viz`, `shap_explainer`, `survival_cox`, `kaplan_meier`, `autoencoder_anomaly`, `mlp_embeddings`, `tabnet_wrapper`, `arima_wrapper` |
| **Não verificado** (1) | `prophet_wrapper` |

`prophet_wrapper` falha com `AttributeError: 'Prophet' object has no attribute
'stan_backend'` — inclusive com autologging desligado e sem registro. O atributo
não é usado pelo nosso código: ele deixa de ser criado quando o backend de
inferência do Prophet não inicializa, o que aponta para incompatibilidade entre
`prophet 1.1.5` e o ambiente serverless, não defeito do módulo. Enquanto não
houver combinação de versões que funcione, ele permanece marcado como não
verificado, e prometer execução com ele é afirmar algo sem evidência.

Três armadilhas confirmadas, válidas para todos os wrappers de treino:

- registram no run **ativo** do MLflow, então dois deles na mesma sessão colidem
  na chave `algorithm`, que o MLflow trata como imutável — use `run_governado`
  ou `log_mlflow=False` para isolar;
- o Databricks liga **autologging por padrão**, e ele intercepta o `fit` mesmo
  quando o wrapper não registra nada; desligue com `mlflow.autolog(disable=True)`
  quando a biblioteca não for compatível;
- `shap_explainer` exige `output_index` em resultado multi-output — recusa
  correta, já que escolher a classe sozinho seria arbitrar sobre a classe
  positiva; e `mlp_embeddings` espera **uma lista de arrays**, um por feature
  categórica, não uma matriz.

## Restrição de ambiente descoberta na rodada 7

Instalar o conjunto de bibliotecas de ML sem fixar versão **derruba o kernel** em
compute serverless: pip sobe `pandas` de 1.5.3 para 2.3.3 e `numpy` de 1.26.4
para 2.2.6, e o Databricks recusa a alteração dos pacotes core
(`ERROR_CORE_PACKAGE_VERSION_CHANGE`).

A instalação funciona com as versões core fixadas junto das bibliotecas:

```text
numpy==1.26.4  pandas==1.5.3  lightgbm==4.3.0  shap==0.44.1  lifelines==0.27.8
```

Consequência prática: em job serverless, dependências vão no bloco
`environments` da submissão, não em `%pip` — `%pip` antes do primeiro comando
Spark aborta a execução com `spark should be initialized with the first notebook
command`.

Foi essa rodada que motivou fixar as versões em `requirements-optional.txt`. O
arquivo hoje traz o conjunto que funcionou; antes dela listava só nomes, e nessa
forma não era instalável neste ambiente.

## Defeitos reais encontrados e corrigidos no `ambiente_fonte/`

Nenhum deles era detectável pela validação estática (AST compilava na máquina
local com Python 3.12):

1. **`spark` como global inexistente** — `null_summary` e 5 `x_scripts`
   (`quick_profile`, `data_quality_check`, `rfv_calculator`, `drift_detector`,
   `schema_to_yaml`) referenciavam o global de notebook `spark`, que não existe
   quando o módulo é importado (`NameError`). Correção: `df.sparkSession` no
   snippet e `SparkSession.getActiveSession() or ...getOrCreate()` nos scripts.
   **`naming_checker` tinha o mesmo defeito e escapou desta rodada**: ele não
   estava coberto pelo smoke test, então nunca foi importado no runtime.
   Encontrado e corrigido em 2026-08-15 pela auditoria de documentação, que
   comparou a lista acima com o código. Hoje nenhum módulo de `x_scripts` ou
   `x_snippets` usa o global — a varredura por AST está descrita no CHANGELOG.
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

$job = '{"run_name":"smoke","tasks":[{"task_key":"smoke","notebook_task":{"notebook_path":"/Users/<username>/x_lab/spark_smoke_test"}}]}'
[System.IO.File]::WriteAllText("$env:TEMP\smoke_job.json", $job)
databricks jobs submit --json "@$env:TEMP\smoke_job.json"
```

> **Passe o JSON por arquivo, não inline.** O PowerShell remove as aspas duplas
> antes de o executável recebê-las, e a CLI recusa o payload com
> `invalid character 'r'`. A here-string (`@'` … `'@`) **também não resolve** —
> verificado em 2026-08-16, mesmo erro. O prefixo `@` no valor de `--json` é o
> que faz a CLI ler de arquivo.
>
> Use `[System.IO.File]::WriteAllText` e não `Set-Content`: este último grava em
> ANSI por padrão neste ambiente.
