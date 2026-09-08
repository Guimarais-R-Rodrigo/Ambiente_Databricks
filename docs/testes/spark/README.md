# Testes Spark serverless — evidência por runtime

> **Nomenclatura da época.** Os nomes `x_*` e `rodrigo-*` neste registro são
> os que existiam na data. A tradução para os nomes atuais está na tabela de
> correspondência do [ADR-0006](../../decisions/ADR-0006-identidade-hub.md);
> este documento não é reescrito porque descreve o que foi observado, não o
> estado atual.

Este documento preserva as descobertas por rodada. Para decidir sobre o estado
atual, leia primeiro o resumo abaixo; as seções seguintes são histórico técnico
e não são reescritas para parecerem atuais.

Executor: job serverless one-time no Free Edition, notebook
[`tools/spark_smoke_test.py`](../../../tools/spark_smoke_test.py), dados 100%
sintéticos.

## Resultado vigente — 2026-08-29 (Spark 4.2.0 serverless)

| Verificação | Resultado |
|---|---:|
| total | 145 |
| `PASS` | **136** |
| `FAIL` | **0** |
| `OPTIONAL_MISSING` | 8 |
| `BLOQUEADO_ESPERADO` | 1 |

Execução: run `996607251657906`, task `657506000110053`. Resultado bruto:
[`2026-08-29_smoke_a2.json`](resultados/2026-08-29_smoke_a2.json).

As oito ausências são dependências opcionais não instaladas nessa rodada. O
bloqueio esperado é a abertura de run MLflow no serverless observado; o caso
reprova se o comportamento mudar sem revisão.

> Este resultado prova execução no runtime e na data declarados. Não prova
> permissões, bibliotecas, Spark Connect ou política do workspace do trabalho.

## Histórico inicial — 2026-08-13 (Spark 4.1.0 serverless)

### Gate aprovado após cinco rodadas

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

### Módulos com dependência opcional — situação em 2026-08-17

> **Atualizado em 2026-08-17.** O bloco abaixo foi reescrito: a situação de
> 14/08 registrava 13 de 14 e classificava `prophet_wrapper` como sem combinação
> funcional conhecida. Isso deixou de ser verdade. A tabela de rodadas acima é
> evidência datada e permanece como está.

**14 dos 14 verificados em runtime**, cada um com chamada real — ajuste de
modelo, projeção ou previsão, não apenas import. O inventário com a prova de
execução de cada biblioteca está em
`ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt`.

`prophet_wrapper` era o único pendente. Em **14/08** falhava com
`AttributeError: 'Prophet' object has no attribute 'stan_backend'` — o backend de
inferência não inicializava, e o registro concluiu, corretamente para a época,
que prometer execução com ele seria afirmar algo sem evidência.

Em **17/08**, `%pip install prophet` sem pin instalou e ajustou um modelo
completo, com previsão de 7 dias à frente. O impedimento não existe mais no
runtime atual do Free.

**A lição é de método, e vale mais que o caso:** em ambiente gerenciado, "foi
testado" tem data de validade — nos dois sentidos. No mesmo dia em que o Prophet
passou a funcionar, o `mlflow_run`, registrado aqui como aprovado em 14/08,
deixou de abrir run. Reexecute antes de replicar; ver
`.claude/rules/free-vs-trabalho.md`.

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

### Restrição de ambiente descoberta na rodada 7

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

### Defeitos reais encontrados e corrigidos no `ambiente_fonte/`

Nenhum deles era detectável pela validação estática (AST compilava na máquina
local com Python 3.12):

1. **`spark` como global inexistente** — `null_summary` e 5 `hub_scripts`
   (`quick_profile`, `data_quality_check`, `rfv_calculator`, `drift_detector`,
   `schema_to_yaml`) referenciavam o global de notebook `spark`, que não existe
   quando o módulo é importado (`NameError`). Correção: `df.sparkSession` no
   snippet e `SparkSession.getActiveSession() or ...getOrCreate()` nos scripts.
   **`naming_checker` tinha o mesmo defeito e escapou desta rodada**: ele não
   estava coberto pelo smoke test, então nunca foi importado no runtime.
   Encontrado e corrigido em 2026-08-15 pela auditoria de documentação, que
   comparou a lista acima com o código. Hoje nenhum módulo de `hub_scripts` ou
   `hub_snippets` usa o global — a varredura por AST está descrita no CHANGELOG.
2. **`cache()`/`unpersist()` proibidos no serverless** (`NOT_SUPPORTED_WITH_SERVERLESS`)
   — em `safe_display` (removido: o prefixo `limit+1` já limita custo) e em
   `quick_profile`/`drift_detector` (guardas `_cache_if_supported`/`_unpersist_quietly`,
   preservando o cache em compute clássico do trabalho).
3. **f-string com backslash em `kpi_card.py`** — sintaxe PEP 701, válida só em
   Python ≥ 3.12; o runtime usa versão anterior. Escapes movidos para fora da
   f-string.

### Dependências opcionais ausentes na rodada 5 — 2026-08-13

`lightgbm`, `xgboost`, `catboost`, `optuna`, `torch` (×2 módulos) — 7 módulos de
`hub_snippets/ml` só importam com as libs instaladas no ambiente do projeto
consumidor (`hub_snippets/requirements-optional.txt`). Testá-los com versões
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
databricks workspace import "/Users/<username>/hub_lab/spark_smoke_test" --file tools\spark_smoke_test.py --format SOURCE --language PYTHON --overwrite

$job = '{"run_name":"smoke","tasks":[{"task_key":"smoke","notebook_task":{"notebook_path":"/Users/<username>/hub_lab/spark_smoke_test"}}]}'
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
