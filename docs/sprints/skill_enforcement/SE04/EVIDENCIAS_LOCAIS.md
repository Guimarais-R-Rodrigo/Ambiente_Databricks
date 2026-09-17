# SE04 — evidências de desenvolvimento local

## Escopo desta evidência

Durante a construção da SE04, foi possível executar harnesses isolados dos novos componentes no ambiente disponível, sem um checkout completo do repositório.

Resultados observados:

```text
Receipt unit harness      = 20/20 PASS
Runner synthetic fixture  = PASS
Receipt verification      = VALID
Tampered output            = INCOMPATIBLE
```

A suíte unitária isolada cobriu o contrato V1, tampering, bindings, stale/replay contextual, wrong skill/release, provenance, failure/fallback, malformed/unknown version, determinismo e ausência de payload de negócio.

A fixture de integração confirmou:

1. runner sintético `PASS`;
2. emissão de `receipt_version=1.0`;
3. `verify_receipt(...)` classificando o payload original como `VALID`;
4. alteração posterior do resultado tornando a verificação `INCOMPATIBLE`.

## O que esta evidência NÃO prova

Ela não executou o certifier oficial sobre a árvore completa. Portanto, não prova:

- regressões integrais SE01–SE03 no checkout final;
- `validate_assistant.py` sobre a árvore inteira;
- renderer canônico;
- render-diff;
- snapshot README;
- worktree limpa;
- publicação/verify Databricks Free.

Por isso, a classificação correta neste checkpoint é:

```text
LOCAL_CERTIFICATION = NOT_RUN
DATABRICKS_FREE      = NOT_RUN
FULLY_CERTIFIED      = false
```

Os harnesses isolados são evidência de desenvolvimento, não substitutos dos gates canônicos.
