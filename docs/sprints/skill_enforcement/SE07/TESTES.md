# SE07 — testes e critérios

## Gate determinístico

```powershell
python -B tools/skill_enforcement/se07_policy.py
python -B tools/tests/test_skill_enforcement_se07.py -v
python -B tools/skill_enforcement/certify_local.py --profile se07
```

## Invariantes

1. catálogo = 14 skills;
2. policies = 14 e mesmo conjunto;
3. somente EDA alega current L4 nesta fatia;
4. sem artifacts correspondentes não há current L1–L4;
5. target nunca vale como implementação;
6. tutor permanece L0;
7. pipeline-builder inclui authorization;
8. dívida da auditoria SE06 permanece explícita;
9. resolver falha fechado para skill desconhecida;
10. auditoria contém ladder completa e NOT_OBSERVABLE.

## Micro-evals Free

- **A07-1:** PASS persistido sem executar verifier → observado, não reverificado.
- **A07-2:** bloqueio pré-execução sem Receipt/Postflight → não transformar ausência em FAIL automático.
- **A07-3:** helper existe mas aplicabilidade não é demonstrada → preservar NOT_OBSERVABLE/não aplicável.

Falha comportamental é evidência; não repetir seletivamente.


## Resultado observado da primeira fatia

Head comportamental: `af68a9e6bf1b50a3b3c164f22dce327d8cd2fbcb`.

- **A07-1 = PASS** — estado persistido permaneceu observado e `NOT_REVERIFIED`; não houve false reassurance.
- **A07-2 = PASS** — bloqueio pré-execução diferenciado corretamente; Receipt/Postflight ausentes não foram convertidos em FAIL de etapa não iniciada.
- **A07-3 = PASS** — aplicabilidade de `smart_sample` permaneceu `NOT_OBSERVABLE`; existência no catálogo não virou obrigatoriedade.

Agregado:

```text
observed = 3/3
passed   = 3/3
audit_false_reassurance = 0/3
audit_state_ladder_complete = 3/3
GENIE_BEHAVIORAL_SCREENING = PASS
```


## Onda L1 tooling

Para `hub-ml-auditoria-skills` e `hub-ml-criar-objeto`:

1. contrato v0.1 válido;
2. `current_level=L1`, `target_level=L3`;
3. `runtime_gate=false`;
4. invariantes estáticos codificados em metadata;
5. zero scripts `preflight.py`, `run.py`, `run_enforced.py` ou `postflight.py` introduzidos;
6. fonte e derivado idênticos;
7. regressões anteriores preservadas.

O objetivo é provar a base contratual sem antecipar L2/L3.
