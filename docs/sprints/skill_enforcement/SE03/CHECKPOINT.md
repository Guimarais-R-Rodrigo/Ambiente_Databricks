# SE03 — checkpoint corrente

## Estado

**SE03 EM DESENVOLVIMENTO — FATIAS 01/02 CERTIFICADAS LOCALMENTE; PREPARAÇÃO FREE EM REVALIDAÇÃO LOCAL.**

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

## Fatia 02 — evidência observada

HEAD certificado: `c0f4176749dc1a48de07f0bb3c8242fdc7bee410`.

```text
22/22 testes SE03 = PASS
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE03_LOCAL
DERIVED_STALE       = false
failures            = 0
```

Também passaram contrato, SE01 14/14, SE02 22/22, estrutura, renderer, render diff e snapshot. O snapshot observado foi `python(AST)=226`, `repo identidade=1532`, `repo links=1994`, extras=0. Evidence bundle: `~/.ambiente_databricks/sef_certifications/20260917T175558Z_c0f4176749dc`.

A matriz local cobriu E01–E12. Isso não substitui E02/E12 comportamentais no Genie Code real.

## Decisões estruturais congeladas

1. Entrypoint único: `skills/hub-ml-eda-profissional/scripts/run.py::run`.
2. Primitive protegida atual: somente `hub_scripts.quick_profile.quick_profile`.
3. Manifest: `release_manifest.json`, com identidade Git blob dos artefatos acoplados.
4. Falha de integridade/preflight/provenance/primitive é fail-closed; sem fallback manual.
5. Output manual correto sem runner não satisfaz canonical compliance.
6. `numeric_columns` é `runtime_derived`; conflito declarado bloqueia com `CONTEXT_PROVENANCE_CONFLICT`.
7. Trace mínimo vincula input/output por digest e pode receber `expected_run_id` em micro-eval local.
8. Receipt formal continua SE04; postflight continua SE05.
9. PR permanece proibida até local + Free + documentação estabilizados.

## Preparação Free — alterações posteriores ao HEAD certificado

Depois do PASS em `c0f4176...`, a branch recebeu:

- `tools/skill_enforcement/se03_free_probe.py` para E01/E04/E06/E10 no runtime Free;
- `SE03/RUNBOOK_FREE.md`;
- `SKILL.md` explicitando `scripts/run.py` como único entrypoint canônico da etapa L3 protegida;
- `SKILL.md` incluído no `release_manifest.json` como `skill_guidance` protegida;
- snapshot raiz reconciliado para o estado pós-renderer esperado.

Essas mudanças tornam o HEAD corrente diferente do HEAD certificado e exigem nova rodada do perfil `se03` antes de qualquer publicação Free.

A alteração do `SKILL.md` precisa ser materializada no `Novo_Ambiente_Simulado/` somente pelo renderer canônico. Não editar o derivado manualmente.

## Estado dos gates agora

```text
FATIA_01_LOCAL_CERTIFICATION = PASS
FATIA_02_LOCAL_CERTIFICATION = PASS
FREE_PREP_LOCAL_REVALIDATION = NOT_RUN
SYNTHETIC_AGENT_SCREENING    = NOT_RUN_SE03
DATABRICKS_FREE              = NOT_RUN_SE03
GITHUB_ACTIONS               = NOT_RUN_SE03
FULLY_CERTIFIED              = false
PR                           = NOT_OPEN
```

## Próximo gate

1. sincronizar o HEAD corrente da branch;
2. executar `python -B tools/tests/test_skill_enforcement_se03.py -v`;
3. executar `python -B tools/skill_enforcement/certify_local.py --profile se03 --verbose`;
4. se o único drift for renderer em `SKILL.md`/`release_manifest.json`, versionar somente a saída do renderer e repetir até worktree limpa + PASS;
5. só então seguir `SE03/RUNBOOK_FREE.md` para publicação/verify/probe e E02/E12 no Genie Code.
