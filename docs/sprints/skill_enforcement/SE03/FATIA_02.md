# SE03 — fatia funcional 02

## Estado

**CERTIFICADA LOCALMENTE NO HEAD `c0f4176749dc1a48de07f0bb3c8242fdc7bee410`.**

Esta fatia endurece o mesmo entrypoint estrutural antes de ampliar o conjunto de primitives protegidas. A fatia 01 havia sido certificada localmente no HEAD `107a0c1575ec68133df6e0d702a3d4fe74e50897`.

Evidência observada da fatia 02:

```text
22/22 testes SE03 = PASS
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE03_LOCAL
DERIVED_STALE       = false
failures            = 0
```

O evidence bundle local foi registrado em `~/.ambiente_databricks/sef_certifications/20260917T175558Z_c0f4176749dc`.

Depois desse PASS, a preparação da homologação Free adicionou `se03_free_probe.py`, `RUNBOOK_FREE.md`, tornou `scripts/run.py` explícito no `SKILL.md` e incluiu a guidance da skill no `release_manifest.json`. Essas mudanças são posteriores ao HEAD certificado e exigem uma nova certificação local antes da publicação no Free.

## Objetivo

Fechar, no alcance local determinístico, as superfícies E02/E03/E08/E09/E10/E11/E12 sem antecipar Receipt formal ou postflight.

## Decisões congeladas

### Provenance E10

`numeric_columns` passa a ser `runtime_derived` a partir de `spark.table(...).dtypes`.

Política de conflito: **fail closed**.

- se o chamador omitir `numeric_columns`, o runner usa o valor derivado;
- se o chamador declarar o mesmo valor, a execução pode seguir;
- se o valor declarado divergir do valor derivado, o runner retorna `BLOCKED` com `CONTEXT_PROVENANCE_CONFLICT` antes do preflight/core;
- o runner registra valor derivado, valor declarado, evidence e `conflict` no trace.

A escolha evita corrigir silenciosamente um contexto contraditório e cobre diretamente a limitação observada em F02-A2.

### Binding de input/output

`ExecutionTraceV0` passa a registrar:

- `input_digest`: SHA-256 de serialização JSON canônica do input efetivo;
- `output_digest`: SHA-256 do resultado de negócio serializado de forma determinística para o alcance da SE03;
- `context_provenance`.

O evaluator recusa payload cujo resultado tenha sido alterado depois do runner.

### Stale trace — alcance SE03

`is_canonically_compliant(..., expected_run_id=...)` pode comparar o `run_id` observado com o id esperado por um harness atual. Isso permite falsificar reutilização de trace nos micro-evals locais.

Isso **não é** proteção universal contra replay e não substitui o Receipt formal da SE04.

### Atalho/manual

Flags ou metadados extras no contexto não criam rota alternativa dentro do runner. Output manual correto, chamada direta da primitive ou solução trivial sem trace do runner permanecem `canonical_compliance=FAIL`.

### Helper legacy

A presença de helper semelhante/legacy não autoriza fallback. Se a primitive canônica protegida estiver ausente, a integridade da release bloqueia antes do core.

## Evals desta fatia

No HEAD certificado `c0f4176749dc1a48de07f0bb3c8242fdc7bee410`, E01–E12 passaram na suíte local determinística, incluindo:

- E02 — flag de atalho não cria rota alternativa dentro do runner;
- E03 — output manual correto sem runner falha compliance;
- E08 — output sobrescrito pós-runner falha compliance por digest;
- E09 — trace de run anterior é recusado quando confrontado com `expected_run_id` do run atual;
- E10 — conflito `numeric_columns` declarado x schema derivado bloqueia;
- E11 — helper legacy não substitui primitive canônica ausente;
- E12 — solução manual trivial com mesmo resultado continua sem compliance.

E02/E12 comportamentais ainda exigem o Genie Code real no Databricks Free.

## Limites preservados

- continua apenas uma primitive protegida: `quick_profile`;
- E02/E12 ainda exigem teste conversacional no Databricks Free;
- o digest de output é evidência mínima de SE03, não Receipt de SE04;
- `expected_run_id` não é defesa universal de replay;
- não há postflight SE05;
- não há `mode="enforce"`;
- sem PR durante desenvolvimento.
