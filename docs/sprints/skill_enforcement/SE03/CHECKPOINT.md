# SE03 — checkpoint corrente

## Estado

**SE03 EM DESENVOLVIMENTO — FATIA 01 CERTIFICADA / FATIA 02 IMPLEMENTADA, NÃO CERTIFICADA.**

- baseline: `main@0f1a8b18e8e7380aad75be096b0ce167e14f9662`;
- origem: PR #74 / SE02 integrada por squash;
- branch: `sef/SE03-entrypoint-estrutural`;
- estratégia: branch-first, sem PR durante desenvolvimento;
- publicação Databricks da SE03: não executada;
- GitHub Actions: não usados como motor iterativo.

## Fechamento herdado da SE02

A SE02 encerrou com:

```text
LOCAL_CERTIFICATION        = PASS
SYNTHETIC_AGENT_SCREENING = MIXED
DATABRICKS_FREE            = PASS
GITHUB_ACTIONS             = DEFERRED_CREDIT
FULLY_CERTIFIED            = false
HUMAN_ACCEPTANCE           = PASS
```

Limitações transferidas:

- F02-A1: bypass aceito quando o agente foi pressionado a pular o preflight;
- F02-A2: contexto declarado contraditório prevaleceu sobre fato derivável;
- L2 correto quando acionado, mas não obrigatório estruturalmente;
- ausência de trace/receipt para provar universalmente o caminho real.

## Fatia 01 — evidência observada

HEAD certificado: `107a0c1575ec68133df6e0d702a3d4fe74e50897`.

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE03_LOCAL
DERIVED_STALE       = false
failures            = 0
```

Resultados observados:

- suíte focada SE03: 13/13 PASS;
- contrato v0.1: PASS;
- SE01: 14/14 PASS;
- SE02: 22/22 PASS;
- estrutura do Hub: PASS;
- renderer: 557 arquivos;
- derivado: sem drift rastreado ou não rastreado;
- snapshot: PASS com `python(AST)=226`, `repo identidade=1531`, `repo links=1994`, extras=0;
- evidence bundle: `~/.ambiente_databricks/sef_certifications/20260917T174041Z_107a0c1575ec`.

A primeira rodada no HEAD `115a318a1a7c6776fa1c39f4617649c1d08698ec` permaneceu `FAIL` por `readme_snapshot`, e revelou uma lacuna do certifier: `git diff --exit-code` não detectava novos arquivos derivados untracked. O gate foi corrigido e a regressão correspondente passou na rodada verde.

## Decisões estruturais congeladas

1. Entrypoint único: `skills/hub-ml-eda-profissional/scripts/run.py::run`.
2. Primitive protegida atual: somente `hub_scripts.quick_profile.quick_profile`.
3. Manifest: `release_manifest.json`, com identidade Git blob dos artefatos acoplados.
4. Falha de integridade/preflight/primitive é fail-closed; sem fallback manual.
5. Output manual correto sem runner não satisfaz canonical compliance.
6. Receipt formal continua SE04; postflight continua SE05.
7. PR permanece proibida até local + Free + documentação estabilizados.

## Fatia 02 — implementação corrente

Objetivo: endurecer o mesmo caminho antes de ampliar primitives.

Implementado:

- `numeric_columns` derivado mecanicamente de `spark.table(...).dtypes`;
- conflito entre `numeric_columns` declarado e runtime observado → `BLOCKED` com `CONTEXT_PROVENANCE_CONFLICT`;
- `context_provenance` no trace;
- `input_digest` e `output_digest` mínimos;
- evaluator rejeita output alterado após runner;
- evaluator aceita `expected_run_id` apenas para micro-eval local de stale trace;
- helper legacy não substitui primitive canônica ausente;
- flags de atalho no contexto não criam rota alternativa no runner;
- E02/E03/E08/E09/E10/E11/E12 adicionados à suíte local.

Limites explícitos:

- E02/E12 ainda precisam do comportamento real do Genie Code no Free;
- `expected_run_id` não é defesa universal de replay;
- digest mínimo não é Receipt formal;
- apenas `quick_profile` está protegida estruturalmente;
- demais condições ainda não possuem provenance completa `user_intent` vs `agent_declared`.

## Estado dos gates agora

```text
FATIA_01_LOCAL_CERTIFICATION = PASS
FATIA_02_IMPLEMENTATION      = IMPLEMENTED_NOT_YET_RUN
SYNTHETIC_AGENT_SCREENING    = NOT_RUN_SE03
DATABRICKS_FREE               = NOT_RUN_SE03
GITHUB_ACTIONS                = NOT_RUN_SE03
FULLY_CERTIFIED               = false
PR                            = NOT_OPEN
```

## Próximo gate

Sincronizar a branch atual no clone local e executar:

1. `python -B tools/tests/test_skill_enforcement_se03.py -v`;
2. `python -B tools/skill_enforcement/certify_local.py --profile se03 --verbose`.

Somente depois dessa rodada os E02–E12 implementados podem receber classificação observada.
