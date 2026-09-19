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
