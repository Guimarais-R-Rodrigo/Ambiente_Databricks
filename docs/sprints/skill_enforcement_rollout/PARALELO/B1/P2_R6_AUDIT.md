# P2 R6 — auditoria independente do AUDIT_BUNDLE

## Artefato recebido

```text
filename = SER_B1_P2_R6_996ebaccb593_AUDIT_BUNDLE.zip
sha256 = 3622a1212f81a40198409321392233d1aeafd295a78e5803eb4f964691b898b7
size_bytes = 16685
entries = 21
uncompressed_bytes = 51963
max_observed_archive_ratio = benign
path_traversal = none
symlink_entries = none
```

## Integridade pública

- MANIFEST externo: válido;
- MANIFEST do SHARE: válido;
- hashes de stdout/stderr conferem com os command records;
- RAW_SHARE_BINDING aponta para o mesmo SHARE manifest;
- ENVELOPE_VERIFICATION: `valid=true`, sem issues;
- secret scan: `SER-PARALLEL-SECRET-SCAN-2 / PASS`, zero findings;
- nenhum path `C:\Users\...` não sanitizado observado no ZIP;
- campanha: `FAIL`;
- verifier da campanha: `valid=true`, zero issues.

O RAW não está incluído, por desenho. Portanto o auditor público consegue verificar integralmente o SHARE e a integridade do envelope registrado, mas não rederivar o RAW/share binding sem o RAW privado.

## Execução observada

Wave 0 iniciou em paralelo:

- `b1.ser03.preflight`;
- `b1.ser05.preflight`.

Ambas usaram `WINDOWS_JOB_OBJECT`, sem timeout, descendente residual ou cleanup incompleto.

SER03 terminou exit 1 com:

`request:MISSING:absence_policy,cohort_roster,cutoff,denominator,duplicate_policy,estimand,max_mob,periodicity,population_id,profile,requested_effect,rows,schema_version,semantic_mode,synthetic`

SER05 terminou exit 1 com:

`context:MISSING:anchor,anchor_grain,cardinality,decision_at,entity_keys,null_key_policy,pit,profile,requested_effect,schema_version,sources,synthetic,temporal`

As cadeias dependentes foram corretamente `BLOCKED_DEPENDENCY`. Não houve global stop ou mutação protegida.

## Causa independente

Os fixtures P1 são wrappers:

- `vf_cumulative.json["request"]`;
- `vf_events.json["request"]`;
- `ce_l2_temporal.json["context"]`;
- `ce_l2_static.json["context"]`.

Os testes P1 exercitam explicitamente esses objetos internos.

O command registry R6, porém, passava os arquivos wrapper completos diretamente a:

- `preflight.py --request <wrapper>`;
- `preflight.py --context <wrapper>`.

As CLIs fazem `loads_strict(file_text)` e entregam o objeto inteiro a `validate_request`/`validate_context`. O contrato fechado então vê as chaves do wrapper, não as chaves do payload interno, produzindo exatamente os MISSING observados.

## Classificação

```text
P2_R6_LOCAL_QUALIFICATION = FAIL
AUDIT_BUNDLE_INTEGRITY = PASS
CAMPAIGN_VERIFIER = PASS_VALID_FAILURE
CANDIDATE_DOMAIN_DEFECT = false
B0_SHARED_MECHANISM_DEFECT = false
PYTHON_IDENTITY_DEFECT = false
ENVIRONMENT_DEFECT = false
P2_COMMAND_FIXTURE_WRAPPER_BINDING_DEFECT = true
SER03_L3 = NOT_PROMOTED
SER05_L2 = NOT_PROMOTED
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```

R6 permanece FAIL. A correção exige novo SHA e nova rodada.

## R7

R7 preserva os fixtures P1 e os scripts funcionais. Cria projeções CLI exatas em `tools/skill_enforcement/real_campaigns/b1/fixtures/`, atualiza apenas os quatro argv de preflight e adiciona metatestes que:
1. provam igualdade exata entre projeção e objeto interno do wrapper P1;
2. executam os quatro comandos CLI reais e exigem exit 0 / status PASS.
