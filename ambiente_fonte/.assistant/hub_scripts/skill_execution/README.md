# `skill_execution` — preflight e evidência verificável de execução

<!-- readme-objeto: 1.0.0 -->

`hub_scripts.skill_execution` é a camada determinística do Skill Enforcement Framework usada pela skill piloto `hub-ml-eda-profissional`. Ela reúne o preflight L2 preservado da SE02 e, na SE04, o subpacote `receipt` usado pelo runner canônico para produzir e verificar evidência estrutural da execução.

## Visão rápida

| Item | Resumo |
|---|---|
| O que é | infraestrutura determinística de preflight + Receipt da skill piloto |
| Serve para | resolver pré-condições e verificar evidência formal de uma execução canônica |
| Usa | filesystem local da `.assistant`, JSON/AST, serialização canônica e SHA-256 |
| Não faz | análise Spark por conta própria, postflight SE05, publicação ou enforcement universal |
| Entrada principal | contrato/contexto no preflight; trace/result/release no Receipt |
| Saída | `PreflightResult` e `ReceiptVerification` estruturados |

Implementações: [skill_execution.py](skill_execution.py) e [receipt/__init__.py](receipt/__init__.py). Exemplo do objeto: [exemplo_skill_execution.py](exemplo_skill_execution.py).

## 1. O que é?

A camada possui duas responsabilidades distintas:

1. `run_preflight`: resolve o contrato v0.1 antes do core analítico;
2. o subpacote `receipt`: constrói e verifica o comprovante formal da execução depois que o runner protegido conclui com sucesso.

O runner em si continua adjacente à skill em `skills/hub-ml-eda-profissional/scripts/run.py`.

## 2. Que problema este recurso resolve?

O preflight responde se os requisitos aplicáveis estão disponíveis antes do core. O Receipt responde se um resultado apresentado está formalmente vinculado ao trace, input, output e release da execução canônica específica.

Essas respostas são diferentes. `PASS` no preflight não prova que a primitive foi chamada; um Receipt `VALID` exige evidência posterior da execução.

## 3. Quando faz sentido usar?

Use `run_preflight` antes da lógica protegida. O `ExecutionReceiptV1` é emitido pelo runner canônico da EDA piloto depois de release íntegra, provenance válida, preflight PASS e conclusão da primitive protegida.

Para auditoria da SE04, use o verifier do Receipt ou o wrapper `run.py::verify_receipt()` quando a comparação também precisa considerar a release publicada/corrente.

## 4. Quando não usar?

Não use o Receipt para fabricar legitimidade de uma rota manual, chamada direta ao helper ou resultado apenas semanticamente semelhante. Não use o verifier como substituto do postflight da SE05: a SE04 classifica a evidência, mas ainda não bloqueia automaticamente a conclusão final.

## 5. Como funciona, intuitivamente?

O fluxo da skill piloto é:

```text
execution_contract
  → run_preflight
  → runner canônico
  → quick_profile chamada/concluída
  → ExecutionTraceV0
  → ExecutionReceiptV1
  → verifier
```

O Receipt não copia o resultado de negócio. Ele faz bindings por digest e registra apenas metadados probatórios necessários.

## 6. Exemplo de situação

Uma EDA executada por `scripts/run.py` termina com trace `PASS`, `quick_profile` em `resources_called` e `resources_completed`, output digest coerente e release íntegra. O runner emite um Receipt. Ao verificar o payload original, o estado esperado é `VALID`.

Se o resultado for alterado depois da emissão, o Receipt deixa de corresponder ao output atual e a classificação esperada é `INCOMPATIBLE`.

## 7. O que você precisa antes de usar?

Para o preflight: contrato v0.1 válido, raiz `.assistant`, skill e contexto objetivo das condições.

Para o Receipt: trace V0.1 coerente, result atual, skill/entrypoint esperados, primitive protegida concluída, digests válidos, provenance runtime sem conflito, ausência de blocking issues e release íntegra.

## 8. O que este recurso entrega?

### Preflight

`PreflightResult` contém `PASS`/`BLOCKED`, decisões de recursos/templates, issues e `writes_performed=false`.

### Receipt

`ExecutionReceiptV1` contém versão, identidade do run, release, bindings, recursos observáveis, decisões, provenance resumida e flags de fallback/writes. O verifier retorna:

```text
VALID
ABSENT
MALFORMED
INVALID
INCOMPATIBLE
STALE_REPLAYED
UNSUPPORTED_VERSION
```

Somente `VALID` produz canonical compliance formal da SE04.

## 9. Como usar este recurso no Hub?

Preflight pela fachada pública existente:

```python
from hub_scripts.skill_execution import run_preflight
```

Receipt/verifier pelo subpacote explícito:

```python
from hub_scripts.skill_execution.receipt import (
    build_execution_receipt,
    verify_execution_receipt,
)
```

Na operação normal da skill piloto, não é necessário montar Receipt manualmente: `scripts/run.py` emite o comprovante quando as pré-condições canônicas são satisfeitas.

## 10. Decisões e configurações que mais importam

- contrato continua `mode="audit"`;
- primitive protegida na SE04 continua somente `quick_profile`;
- `numeric_columns` deve ser `runtime_derived` e sem conflito;
- `resources_called` registra tentativa; `resources_completed` registra retorno bem-sucedido;
- import e consumo de template não são inferidos: permanecem `NOT_OBSERVABLE` sem instrumentação mecânica;
- serialização canônica evita dependência da ordem de chaves JSON;
- SHA-256 fornece tamper evidence/binding, não autenticação contra comprometimento completo do código e da release.

## 11. Limitações, riscos e armadilhas

O Receipt não é assinatura digital, HMAC ou attestation. Um atacante com capacidade de substituir código/verifier/release e recalcular todas as evidências está fora do threat model desta sprint.

A proteção de replay é contextual: `run_id`, binding ao trace e `expected_run_id` permitem rejeitar Receipt de outro run quando o consumidor conhece o run atual. Anti-replay universal exigiria estado/nonce confiável externo.

## 12. Quais são as alternativas?

`tools/skill_enforcement/validate_contracts.py` continua sendo o gate estático de contrato no repositório. `scripts/preflight.py` continua útil para diagnóstico isolado L2. Nenhum deles substitui o Receipt da SE04.

O postflight final não é alternativa presente: ele pertence à SE05 e não foi iniciado.

## 13. Como saber se o resultado faz sentido?

No preflight, teste happy path, recurso/template ausente, condições e contexto incompleto.

No Receipt, teste pelo menos: válido, ausente, tampered receipt, tampered output/trace, stale run, wrong skill/release, provenance conflict, primitive failure/fallback, schema parcial e versão desconhecida. Output manual tecnicamente correto deve continuar sem Receipt canônico.

## 14. Arquivos relacionados e próximos passos

- [skill_execution.py](skill_execution.py): preflight L2.
- [receipt/__init__.py](receipt/__init__.py): schema lógico, builder e verifier SE04.
- [__init__.py](__init__.py): fachada pública histórica do preflight.
- [exemplo_skill_execution.py](exemplo_skill_execution.py): exemplo operacional do objeto `skill_execution`.
- `skills/hub-ml-eda-profissional/scripts/run.py`: runner/emissor e wrapper de verificação contra release corrente.
- `skills/hub-ml-eda-profissional/release_manifest.json`: fingerprints protegidos.
- `docs/sprints/skill_enforcement/SE04/`: desenho, threat model, testes e runbooks.

Próximo estágio arquitetural: SE05 consumirá a verificação para postflight fail-closed. Isso não faz parte desta implementação.

## 15. Referências

- `docs/decisions/ADR-0021-execucao-verificavel-de-skills.md`;
- `docs/sprints/skill_enforcement/PLANO_MESTRE.md`;
- `docs/sprints/skill_enforcement/REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`;
- `docs/sprints/skill_enforcement/SE04/DESENHO_TECNICO.md`;
- testes `tools/tests/test_skill_enforcement_se02.py`, `test_skill_enforcement_se03.py`, `test_skill_enforcement_se04.py` e `test_skill_enforcement_se04_runner.py`.

Estado desta revisão: implementação SE04 presente na branch de desenvolvimento; certificação oficial local/Free permanece gate separado antes de release candidate.
