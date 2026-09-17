# SE05 — checkpoint técnico

## Natureza deste checkpoint

Este arquivo registra o estado tecnicamente auditável da SE05 durante desenvolvimento branch-first. Ele **não** declara a sprint certificada, não abre PR e não autoriza merge.

## Git de partida

```text
branch      = sef/SE05-postflight-fail-closed
base_main   = d74b2fcbf9accdf3878aa3aef9c0ec629a811028
merge_base  = d74b2fcbf9accdf3878aa3aef9c0ec629a811028
PR          = NOT_OPENED
```

A branch nasceu diretamente da `main` após o merge aceito da SE04 pela PR #77.

## Estado funcional

```text
PostflightV1                     = IMPLEMENTED
postflight policy                = fail_closed
run_enforced L4                  = IMPLEMENTED
finalizer                        = IMPLEMENTED
completion authorization         = IMPLEMENTED
required resource validation     = IMPLEMENTED
conditional applicability        = IMPLEMENTED
conditional skip justification   = IMPLEMENTED
template load + digest evidence  = IMPLEMENTED
artifact binding                 = IMPLEMENTED
handoff validation               = IMPLEMENTED
completion claim reverification  = IMPLEMENTED
release binding SE05             = IMPLEMENTED
Free deterministic probe         = PREPARED
```

## Invariante central

```text
postflight.status != PASS
    → completion.authorized = false
    → completion.status = NOT_COMPLETED
```

Não existe caminho legítimo de homologação L4 por simples autodeclaração.

## Relação SE04 × SE05

A SE05 não substitui o core da SE04.

```text
SE04 / L3:
run.py → trace → Receipt

SE05 / L4:
run.py
  → run_enforced.py
  → Receipt enriquecido
  → postflight.py
  → PostflightV1
  → completion
```

Essa separação preserva regressões históricas e permite demonstrar que Receipt válido, sozinho, não equivale a completion L4.

## Evidências observadas

Primeiro gate:

```text
execution_contract = PASS
postflight tests    = 15/15 PASS
sintaxe             = PASS
```

Gate integrado:

```text
L4 runner tests = 7/7 PASS
```

Certifier parcial no HEAD `2a1d8afd2d072e29bfe16bf2a8e549688e4742f3`:

```text
SE01 regression      = PASS
SE02 regression      = PASS
SE03 regression      = PASS
SE04 Receipt         = PASS
SE04 runner          = PASS
SE05 postflight      = PASS
SE05 L4 integration  = PASS
assistant_structure  = PASS (aviso local __pycache__)
readme_snapshot      = FAIL por contagens stale
```

O snapshot foi atualizado depois dessa execução; guards temporais SE03/SE04 também foram reconciliados para reconhecer a implementação legítima da SE05.

## Certificação atual

Enquanto o renderer final, certifier completo e Free não forem executados:

```text
LOCAL_CERTIFICATION        = NOT_FINAL
DATABRICKS_FREE            = NOT_RUN
GENIE_BEHAVIORAL_SCREENING = MIXED   # histórico SE03; não reclassificado
GITHUB_ACTIONS             = NOT_RUN
FULLY_CERTIFIED            = false
DERIVED_STALE              = NOT_YET_MATERIALIZED_FOR_SE05
PR                         = NOT_OPENED
```

## Próximos gates permitidos

1. remover resíduos locais `__pycache__`;
2. materializar `Novo_Ambiente_Simulado/` exclusivamente por `tools/render_simulado.py --write`;
3. versionar somente o derivado gerado;
4. obter contagens finais e reconciliar snapshot README se necessário;
5. executar `certify_local.py --profile se05 --verbose` até `FULL_SE05_LOCAL=PASS`;
6. publicar/verificar por conteúdo no Databricks Free;
7. executar `SE05_FREE_PROBE_V1`;
8. reconciliar evidências/checkpoint no HEAD final;
9. congelar release candidate;
10. somente então abrir PR e observar Actions uma vez.

## O que continua proibido nesta fase

- editar `Novo_Ambiente_Simulado/` manualmente;
- abrir PR antes da RC;
- converter `DEFERRED_CREDIT` em PASS;
- promover ao workspace corporativo;
- generalizar para as demais skills antecipando SE07;
- iniciar benchmark amplo SE06 antes do encerramento/aceite da SE05.
