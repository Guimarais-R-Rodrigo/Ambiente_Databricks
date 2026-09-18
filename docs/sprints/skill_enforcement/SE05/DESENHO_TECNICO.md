# SE05 — desenho técnico

## 1. Objetivo de engenharia

A SE05 implementa o nível L4 do Skill Enforcement Framework para a skill piloto `hub-ml-eda-profissional`.

O problema não é mais “há evidência de execução canônica?”; isso pertence à SE04. O problema agora é:

> a evidência canônica disponível é suficiente para autorizar o estado de conclusão homologada da skill?

A resposta deve ser mecânica e fail-closed.

## 2. Separação entre L3 e L4

A SE05 preserva `scripts/run.py::run` como core L3 histórico. Essa decisão mantém regressões SE03/SE04 estáveis e evita transformar uma evolução de homologação em refatoração ampla do core.

A rota L4 é:

```text
scripts/run_enforced.py::run_enforced
```

Ela chama o core L3, depois coleta as evidências adicionais necessárias para o postflight.

O trace mantém o entrypoint L3 original para compatibilidade do Receipt e acrescenta:

```text
enforcement_entrypoint
resources_imported
templates_loaded
template_digests
evidence_gaps
enforcement_status
artifacts_digest
```

O Postflight exige `enforcement_entrypoint` igual à rota L4 esperada; portanto um payload L3 enriquecido manualmente não deve ser homologado como L4.

## 3. Evidência de recursos

O contrato continua declarando `evidence` por recurso.

Para `call`, o Postflight exige:

1. decisão `applicable=true`;
2. recurso resolvido;
3. presença em `resources_called`;
4. presença em `resources_completed`.

`called` e `completed` não são sinônimos. Se um helper lança exceção, ele pode constar como chamado, mas não como concluído.

Recursos opcionais não bloqueiam.

## 4. Evidência de templates

Templates `required` ou `conditional` aplicáveis só contam quando:

- o preflight os resolveu;
- `run_enforced.py` leu o arquivo real;
- o trace contém o ID em `templates_loaded`;
- existe SHA-256 correspondente em `template_digests`.

Menção textual ao template não é evidência de leitura.

## 5. Artifacts

`run_enforced.py` registra artifacts resumidos por recurso sem copiar payloads de negócio volumosos para o postflight.

O trace contém `artifacts_digest = sha256(canonical_json(artifacts))`.

Se `payload.artifacts` for modificado depois da execução, o Postflight classifica `ARTIFACTS_DIGEST_MISMATCH` e bloqueia homologação.

## 6. Evidence gaps

Quando o executor não consegue executar um requisito aplicável com evidência mecânica suficiente, ele registra `evidence_gaps`.

Exemplos:

- `pk_columns` ausente para `data_quality_check`;
- renderer indisponível para `safe_display`;
- `resolved_theme` ausente quando tema foi declarado selecionado;
- exceção durante import ou chamada de recurso.

O gap não é convertido em evidência positiva. O Postflight avalia o contrato e falha/revisa conforme o requisito correspondente.

## 7. Handoff

O contrato define:

```json
{
  "metadata": {
    "postflight": {
      "schema_version": "1.0",
      "policy": "fail_closed",
      "handoff": {
        "required": [
          "sources_snapshot",
          "unit_keys_target",
          "quality_risks",
          "feature_candidates_leakage",
          "filters_sample",
          "open_questions"
        ],
        "allow_empty": ["open_questions"]
      }
    }
  }
}
```

Campo obrigatório ausente/vazio resulta em `REVIEW`, exceto os explicitamente permitidos vazios.

`REVIEW` não autoriza completion.

## 8. PostflightV1

Campos centrais:

```text
postflight_version = 1.0
postflight_id       = pf1:sha256(body)
status              = PASS|FAIL|BLOCKED|REVIEW
completion_authorized
skill
run_id
receipt_status
receipt_id
policy
contract_schema_version
bindings.trace_sha256
bindings.artifacts_sha256
bindings.handoff_sha256
coverage
issues
writes_performed=false
```

O `postflight_id` é binding determinístico, não assinatura digital.

## 9. Finalizador

`scripts/postflight.py::finalize`:

1. localiza a release publicada;
2. carrega contrato;
3. verifica o Receipt contra a release corrente;
4. exige `enforcement_entrypoint` L4;
5. constrói PostflightV1;
6. autoriza completion somente se `status=PASS`.

Saída:

```json
{
  "completion": {
    "authorized": true,
    "status": "COMPLETED",
    "reason": "postflight PASS"
  }
}
```

Qualquer outro estado produz `authorized=false` e `NOT_COMPLETED`.

## 10. Reverificação

`verify_finalized` não confia no campo `completion` autodeclarado.

Ele:

- reverifica Receipt;
- reconstrói Postflight;
- compara com o objeto observado;
- confronta o claim de completion com a autorização real.

Divergência produz `INVALID` / `COMPLETION_CLAIM_MISMATCH`.

## 11. Estados e severidade

Prioridade de estado:

```text
BLOCKED > FAIL > REVIEW > PASS
```

- `BLOCKED`: evidência/configuração estruturalmente não confiável;
- `FAIL`: requisito material aplicável descumprido;
- `REVIEW`: requisito de handoff/revisão impede homologação automática;
- `PASS`: nenhum issue bloqueante/material/review permanece.

## 12. Integração com `hub-ml-auditoria-skills`

A SE05 não cria um auditor editorial paralelo. O Postflight é um gate mecânico sobre evidências estruturadas.

`hub-ml-auditoria-skills` continua responsável por auditoria de implementação/output, achados explicativos, severidade editorial e revisão humana proporcional ao risco.

## 13. Release manifest

A release da skill piloto protege, entre outros:

- contrato;
- `SKILL.md`;
- core runner L3;
- executor L4;
- finalizador;
- preflight engine;
- Receipt engine;
- Postflight engine;
- primitive protegida histórica.

Isso detecta alteração material da rota homologada antes da execução.

## 14. Threat model e limites

A SE05 protege contra:

- output manual apresentado como execução homologada;
- core L3 apresentado como conclusão L4;
- required/conditional aplicável omitido;
- helper chamado e falho apresentado como concluído;
- template aplicável não carregado;
- handoff incompleto;
- artifacts adulterados;
- Receipt stale/inválido;
- Postflight adulterado;
- claim de completion adulterado.

Fora do threat model:

- atacante com capacidade de substituir toda a release, verifier e evidências e recalcular hashes;
- qualidade semântica/estatística do resultado de negócio;
- enforcement das demais skills;
- garantia de que um LLM sempre escolherá espontaneamente a rota L4 — isso será medido em evals ampliados da SE06.
