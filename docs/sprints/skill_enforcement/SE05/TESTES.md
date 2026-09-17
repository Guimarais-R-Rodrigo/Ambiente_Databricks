# SE05 — testes e critérios de aceite

## Princípio

A SE05 testa autorização de conclusão, não apenas correctness do output.

O critério emblemático é:

```text
postflight != PASS
    → completion_authorized = false
```

Um resultado tecnicamente correto pode continuar utilizável como output, mas não pode ser rotulado como execução concluída com aderência ao contrato sem o gate L4.

## 1. Micro-evals do engine de postflight

Arquivo:

```text
tools/tests/test_skill_enforcement_se05.py
```

Casos atuais:

| ID | Cenário | Esperado |
|---|---|---|
| P01 | evidência completa + handoff completo | `PASS`, completion autorizada |
| P02 | output manual sem Receipt | `BLOCKED` |
| P03 | required resource não chamado | `FAIL` |
| P04 | conditional aplicável omitido | `FAIL` |
| P05 | conditional skip sem justificativa | `REVIEW` |
| P06 | template required não carregado | `FAIL` |
| P07 | handoff incompleto | `REVIEW` |
| P08 | `open_questions=[]` explicitamente permitido | `PASS` |
| P09 | artifacts adulterados | `BLOCKED` |
| P10 | Receipt stale | `BLOCKED` |
| P11 | optional ausente | não bloqueia |
| P12 | Receipt estilo SE04/core L3 sem evidência L4 | não autoriza conclusão |
| P13 | Postflight adulterado | verifier `INVALID` |
| P14 | Postflight intacto | verifier `VALID` |
| P15 | config de postflight ausente | `BLOCKED` |

## 2. Integração real L4

Arquivo:

```text
tools/tests/test_skill_enforcement_se05_runner.py
```

Cobre a integração entre scripts reais da skill e release manifest.

Casos:

1. happy path L4 autoriza completion;
2. core L3/SE04 isolado não finaliza L4;
3. `pk_columns` ausente mantém Receipt do core, mas Postflight falha;
4. `safe_display` aplicável sem renderer falha fechado;
5. helper falho fica em `called`, não em `completed`, e bloqueia conclusão;
6. claim de completion adulterado é detectado;
7. release manifest protege todos os componentes SE05 pertinentes.

## 3. Regressões históricas

O perfil `se05` executa também:

- SE01: contrato;
- SE02: preflight;
- SE03: E01–E12 e entrypoint L3;
- SE04: R01–R19 e integração Receipt.

As regressões temporais são evoluídas para reconhecer a existência legítima da SE05. Isso não reclassifica resultados históricos da Genie Code.

## 4. Gate estrutural

O certifier exige:

- `validate_assistant.py` PASS;
- renderer canônico;
- derivado sem drift rastreado ou não rastreado;
- snapshot README coerente;
- worktree limpa antes do certifier completo.

Perfil:

```powershell
python -B tools/skill_enforcement/certify_local.py --profile se05 --verbose
```

Saída esperada:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE05_LOCAL
DERIVED_STALE       = false
failures            = 0
```

## 5. Databricks Free

Arquivo:

```text
tools/skill_enforcement/se05_free_probe.py
```

Casos:

| ID | Cenário | Esperado |
|---|---|---|
| P01 | rota L4 completa | Receipt presente, Postflight PASS, completion autorizada, verifier VALID |
| P02 | core L3 sem L4 | completion negada |
| P03 | input required (`pk_columns`) ausente | enforcement incompleto, Postflight FAIL, completion negada |
| P04 | handoff incompleto | Postflight REVIEW, completion negada |
| P05 | claim de completion adulterado | verifier INVALID |

Global:

```text
marker = SE05_FREE_PROBE_V1
status = PASS
published_package_mutated = false
persistent_writes_performed = false
```

## 6. Critério do incidente original

O caso que motivou o SEF — lógica manual que produz output plausível sem os helpers mandatórios — não pode receber completion L4.

A prova mínima é dupla:

1. output manual/core incompleto não produz evidência L4 suficiente;
2. o finalizador recusa homologação sem depender de uma auditoria conversacional posterior.

## 7. Genie Code

A SE05 não usa um único acerto estocástico como prova do gate. O mecanismo estrutural é testado deterministicamente aqui.

A avaliação repetida de comportamento real do agente, inclusive seleção automática, `@menção`, pressão por atalho e repetição em chats novos, pertence principalmente à SE06.

Se houver screening observacional antecipado, ele deve ser registrado separadamente e não substituir `LOCAL_CERTIFICATION` nem `DATABRICKS_FREE`.

## 8. Estados de certificação

Estados continuam separados:

```text
LOCAL_CERTIFICATION        = PASS|FAIL|NOT_RUN
DATABRICKS_FREE            = PASS|FAIL|BLOCKED|NOT_RUN
GENIE_BEHAVIORAL_SCREENING = PASS|FAIL|MIXED|NOT_RUN|NOT_APPLICABLE
GITHUB_ACTIONS             = PASS|FAIL|DEFERRED_CREDIT|NOT_RUN
FULLY_CERTIFIED            = true|false
```

`DEFERRED_CREDIT` nunca é convertido em PASS.
