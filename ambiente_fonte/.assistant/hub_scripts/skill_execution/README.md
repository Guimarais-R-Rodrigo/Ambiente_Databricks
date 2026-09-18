# `skill_execution` — preflight, Receipt e postflight fail-closed

<!-- readme-objeto: 1.0.0 -->

`hub_scripts.skill_execution` é a camada determinística do Skill Enforcement Framework usada pela skill piloto `hub-ml-eda-profissional`. Ela reúne o preflight L2, o `ExecutionReceiptV1` da SE04 e, na SE05, o `PostflightV1` que decide se uma execução pode ser homologada como concluída com aderência ao contrato.

## Visão rápida

| Item | Resumo |
|---|---|
| O que é | infraestrutura determinística de preflight + Receipt + postflight |
| Serve para | resolver pré-condições, provar execução canônica e autorizar/recusar conclusão homologada |
| Usa | filesystem local da `.assistant`, JSON/AST, serialização canônica, SHA-256 e evidência do runner |
| Não faz | análise de negócio por conta própria, publicação ou enforcement universal para todas as skills |
| Entradas | contrato/contexto; trace/result/release; artifacts/handoff |
| Saídas | `PreflightResult`, `ReceiptVerification`, `PostflightV1` e `PostflightVerification` |

Implementações: [skill_execution.py](skill_execution.py), [receipt/__init__.py](receipt/__init__.py) e [postflight/__init__.py](postflight/__init__.py). Exemplo do objeto: [exemplo_skill_execution.py](exemplo_skill_execution.py).

## 1. O que é?

A camada possui três responsabilidades distintas:

1. `run_preflight`: resolve o contrato antes do core analítico;
2. `receipt`: constrói e verifica o comprovante formal da execução canônica;
3. `postflight`: confronta Receipt, contrato, evidência de recursos/templates e handoff antes de autorizar conclusão L4.

O core L3 continua adjacente à skill em `skills/hub-ml-eda-profissional/scripts/run.py`. A rota L4 está em `scripts/run_enforced.py`; a finalização está em `scripts/postflight.py`.

## 2. Que problema este recurso resolve?

O preflight responde se os requisitos aplicáveis estão disponíveis antes do core. O Receipt responde se o resultado apresentado está vinculado à execução canônica correspondente. O postflight responde uma terceira pergunta: há evidência suficiente de que os requisitos materiais aplicáveis foram realmente satisfeitos para permitir o estado “skill concluída com aderência ao contrato”?

Essas respostas não são intercambiáveis. `PASS` no preflight não prova chamada de helper. Receipt `VALID` não prova, sozinho, que todos os requisitos L4 foram satisfeitos. `completion.authorized=true` só é permitido após Postflight `PASS`.

## 3. Quando faz sentido usar?

Use `run_preflight` antes da lógica protegida. O `ExecutionReceiptV1` é emitido pelo runner canônico após execução coerente. Para uma conclusão homologada da EDA piloto, use a rota L4 `run_enforced.py` e depois o finalizador `postflight.py` com handoff estruturado.

## 4. Quando não usar?

Não monte Receipt ou Postflight manualmente para legitimar rota paralela. Não trate `resolved` como sinônimo de `called`. Não transforme recurso importado em recurso concluído. Não use output tecnicamente correto como substituto de evidência canônica.

## 5. Como funciona, intuitivamente?

Fluxo L4 da skill piloto:

```text
execution_contract
  → run_preflight
  → run.py::run                # core L3 histórico
  → ExecutionTraceV0
  → run_enforced.py            # coleta evidência L4
      ├── imports observados
      ├── calls/completions observados
      ├── templates carregados + digests
      └── artifacts + gaps
  → ExecutionReceiptV1
  → verify_receipt
  → postflight.py
  → PostflightV1
  → PASS ? completion=COMPLETED : completion=NOT_COMPLETED
```

## 6. Exemplo de situação

Uma EDA sobre uma tabela sintética possui `pk_columns`, não pede gráficos nem amostra local. O L4 executa `quick_profile`, `data_quality_check` e `null_summary`, carrega os templates obrigatórios, gera Receipt válido e recebe um handoff completo. O Postflight pode retornar `PASS` e autorizar conclusão.

Se `pk_columns` estiver ausente, `data_quality_check` não é marcado como chamado. O executor registra o gap, o Receipt continua servindo para provar a execução L3 correspondente, mas o Postflight retorna `FAIL` e a conclusão permanece `NOT_COMPLETED`.

## 7. O que você precisa antes de usar?

Para o preflight: contrato válido, raiz `.assistant` e contexto das condições.

Para o Receipt: trace coerente, resultado atual, release íntegra, provenance runtime sem conflito e primitive protegida concluída.

Para o Postflight: Receipt `VALID`, trace L4, artifacts vinculados por digest, decisões completas, evidência dos requisitos required/conditional aplicáveis, templates carregados e handoff final conforme o contrato.

## 8. O que este recurso entrega?

### Preflight

`PreflightResult` contém `PASS`/`BLOCKED`, decisões, issues e `writes_performed=false`.

### Receipt

O verifier retorna:

```text
VALID
ABSENT
MALFORMED
INVALID
INCOMPATIBLE
STALE_REPLAYED
UNSUPPORTED_VERSION
```

### Postflight

`PostflightV1` usa os estados:

```text
PASS
FAIL
BLOCKED
REVIEW
```

- `PASS`: toda evidência material exigida para aquele contexto está presente e o handoff está completo;
- `FAIL`: requisito material aplicável não foi satisfeito;
- `BLOCKED`: a própria evidência/configuração não é confiável o bastante para decidir;
- `REVIEW`: a execução não pode ser homologada automaticamente e requer revisão explícita.

Somente `PASS` autoriza conclusão.

## 9. Como usar este recurso no Hub?

Preflight:

```python
from hub_scripts.skill_execution import run_preflight
```

Receipt:

```python
from hub_scripts.skill_execution.receipt import (
    build_execution_receipt,
    verify_execution_receipt,
)
```

Postflight:

```python
from hub_scripts.skill_execution.postflight import (
    build_postflight,
    verify_postflight,
)
```

Na operação normal da skill, prefira os scripts adjacentes à própria skill em vez de montar objetos manualmente.

## 10. Decisões e configurações que mais importam

- o contrato permanece `mode="audit"`; a política `metadata.postflight.policy="fail_closed"` governa homologação, não altera silenciosamente o schema histórico;
- `run.py` continua sendo o core L3 preservado para regressão;
- `run_enforced.py` é a rota L4 necessária para conclusão homologada;
- `resources_called` registra tentativa; `resources_completed` exige retorno bem-sucedido;
- templates aplicáveis só contam quando são realmente lidos e recebem digest;
- falta de input para um helper gera gap; não produz evidência fabricada;
- handoff incompleto não é completion;
- o Postflight é vinculado por hash ao trace, artifacts e handoff;
- qualquer claim de `completion` deve ser reverificado, não confiado por autodeclaração.

## 11. Limitações, riscos e armadilhas

SHA-256 continua sendo mecanismo de binding/tamper evidence, não assinatura digital ou attestation externa.

O postflight não consegue provar fatos que não estejam instrumentados. Nesses casos deve falhar fechado ou exigir revisão; não deve inferir consumo por menção textual.

O executor L4 da SE05 continua restrito ao piloto. Generalização para as demais skills pertence a sprint posterior.

## 12. Quais são as alternativas?

`tools/skill_enforcement/validate_contracts.py` valida estrutura estática. `scripts/preflight.py` diagnostica L2. `run.py` executa o core L3 e emite Receipt. Nenhum desses, isoladamente, substitui o Postflight L4.

A skill `hub-ml-auditoria-skills` continua sendo a ferramenta de auditoria humana/estruturada do ecossistema; a SE05 não cria um segundo auditor editorial.

## 13. Como saber se o resultado faz sentido?

Teste no mínimo:

- happy path L4 autorizado;
- output manual/core L3 sem L4;
- required resource omitido;
- conditional aplicável omitido;
- skip condicional sem justificativa;
- template obrigatório ausente;
- handoff incompleto;
- Receipt stale/inválido;
- artifacts adulterados;
- helper chamado e não concluído;
- claim de completion adulterado.

Nenhum desses desvios pode terminar com `completion_authorized=true`.

## 14. Arquivos relacionados e próximos passos

- [skill_execution.py](skill_execution.py): preflight L2.
- [receipt/__init__.py](receipt/__init__.py): Receipt SE04.
- [postflight/__init__.py](postflight/__init__.py): Postflight SE05.
- [__init__.py](__init__.py): fachada pública histórica do preflight.
- [exemplo_skill_execution.py](exemplo_skill_execution.py): exemplo operacional.
- `skills/hub-ml-eda-profissional/scripts/run.py`: core L3.
- `skills/hub-ml-eda-profissional/scripts/run_enforced.py`: executor L4.
- `skills/hub-ml-eda-profissional/scripts/postflight.py`: finalizador fail-closed.
- `skills/hub-ml-eda-profissional/release_manifest.json`: fingerprints da release.
- `docs/sprints/skill_enforcement/SE05/`: desenho, testes e runbook.

Próximo estágio arquitetural após a SE05: SE06 amplia evals repetidos/adversariais e calibra falsos bloqueios/escapes.

## 15. Referências

- `docs/decisions/ADR-0021-execucao-verificavel-de-skills.md`;
- `docs/sprints/skill_enforcement/PLANO_MESTRE.md`;
- `docs/sprints/skill_enforcement/REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`;
- `docs/sprints/skill_enforcement/SE04/DESENHO_TECNICO.md`;
- `docs/sprints/skill_enforcement/SE05/DESENHO_TECNICO.md`;
- testes `tools/tests/test_skill_enforcement_se03.py`, `test_skill_enforcement_se04.py`, `test_skill_enforcement_se04_runner.py`, `test_skill_enforcement_se05.py` e `test_skill_enforcement_se05_runner.py`.

Estado desta revisão: implementação SE05 presente na branch de desenvolvimento; certificação oficial local/Free permanece gate separado antes de release candidate.
