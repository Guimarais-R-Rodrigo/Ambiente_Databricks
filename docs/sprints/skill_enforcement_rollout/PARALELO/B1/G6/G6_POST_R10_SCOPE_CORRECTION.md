# G6 — correção de escopo após o full-content verify

## Classificação

```text
G6_POST_R10_FULL_CONTENT_VERIFY = PASS (preservado)
G6_EXTERNAL = IN_PROGRESS
CORRECTION_KIND = AGGREGATE_SCOPE_CLASSIFICATION
FUNCTIONAL_BYTES_CHANGED = false
POLICY_CHANGED = false
```

O commit documental `4459876f458cc1295661720a304e34f0c08d37cb` elevou prematuramente o estado agregado `G6_EXTERNAL` para PASS após o full-content verify.

Essa elevação não corresponde ao contrato congelado de G6. O full verify é obrigatório, mas o pacote G6 também contém superfícies externas obrigatórias ainda não executadas.

A correção não reclassifica nem invalida o PASS do full verify. Ela apenas separa corretamente:

- subgate de publicação/readback/conteúdo = PASS;
- evidência Free dos dois probes = NOT_RUN;
- evidência Genie = NOT_RUN;
- verifier agregado Free + Genie = NOT_RUN;
- G6 agregado = IN_PROGRESS.

## Fonte normativa congelada

O `external_manifest.json` e os artefatos relacionados permanecem byte-idênticos entre o freeze G6 original `c11c2dff07f0f7595ed545f32990e5d54f1fd583` e o estado atual.

Blobs Git:

- external manifest: `fce914858ccf431ccd19e6c4a08ef0eea7c82d3c`
- Genie manifest: `38b0f0d24c5a8d922d1fb7c9b6f6fa81516f46e0`
- SER03 Free probe: `6d7e51116f2c4ccd0319925077ae347a8be8722c`
- SER05 L2 Free probe: `758339212a246fcacf431195d816a2f6d210f5b5`
- external verifier: `6c5959b62290097555239b2f80eb9439463852d5`
- Genie results template: `c85183300580263566aa417920c3aed963abf015`

## Remanescente obrigatório

`verify_external_results.py` exige três conjuntos de evidência:

1. output Free SER03;
2. output Free SER05 L2;
3. resultados das 20 variantes Genie.

Somente com os três canais válidos e Genie agregado PASS o verifier pode retornar G6 externo PASS.

Nenhum G7 é aberto por esta correção.
