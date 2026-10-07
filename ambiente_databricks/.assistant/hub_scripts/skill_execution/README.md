# `skill_execution` — preflight, Receipt e postflight fail-closed

<!-- readme-objeto: 1.0.0 -->

`hub_scripts.skill_execution` reúne preflight, `ExecutionReceiptV1`, `PostflightV1` e consulta da policy para rotas canônicas de skills. A camada verifica pré-condições, vínculos de evidência e autorização de conclusão no escopo instrumentado; não homologa automaticamente o mérito da análise ou o ambiente.

## Visão rápida

| Item | Resumo |
|---|---|
| O que é | infraestrutura determinística de preflight + Receipt + postflight |
| Serve para | resolver pré-condições, provar execução canônica e autorizar/recusar conclusão canônica |
| Usa | filesystem local da `.assistant`, JSON/AST, serialização canônica, SHA-256 e evidência do runner |
| Não faz | análise de negócio por conta própria, publicação ou enforcement universal para todas as skills |
| Entradas | contrato/contexto; trace/result/release; artifacts/handoff |
| Saídas | `PreflightResult`, `ReceiptVerification`, `PostflightV1` e `PostflightVerification` |

Implementações: [skill_execution.py](skill_execution.py), [receipt/__init__.py](receipt/__init__.py) e [postflight/__init__.py](postflight/__init__.py). Exemplo do objeto: [exemplo_skill_execution.py](exemplo_skill_execution.py).

## 1. O que é?

A fachada também consulta a policy transversal por `load_enforcement_policy_registry`, `get_skill_enforcement_policy` e `list_skill_enforcement_policies`. O componente interno [domain_context](domain_context/README.md) valida metadados temporais de consumidores específicos, sem executar joins.

A camada possui três responsabilidades distintas:

1. `run_preflight`: resolve o contrato antes do core analítico;
2. `receipt`: constrói e verifica o comprovante formal da execução canônica;
3. `postflight`: confronta Receipt, contrato, evidência de recursos/templates e handoff antes de autorizar conclusão L4.

O core L3 continua adjacente à skill em `skills/hub-ml-eda-profissional/scripts/run.py`. A rota L4 está em `scripts/run_enforced.py`; a finalização está em `scripts/postflight.py`.

## 2. Que problema este recurso resolve?

O preflight responde se os requisitos aplicáveis estão disponíveis antes do core. O Receipt responde se o resultado apresentado está vinculado à execução canônica correspondente. O postflight responde uma terceira pergunta: há evidência suficiente de que os requisitos materiais aplicáveis foram realmente satisfeitos para permitir o estado “skill concluída com aderência ao contrato”?

Essas respostas não são intercambiáveis. `PASS` no preflight não prova chamada de helper. Receipt `VALID` não prova, sozinho, que todos os requisitos L4 foram satisfeitos. `completion.authorized=true` só é permitido após Postflight `PASS`.

## 3. Quando faz sentido usar?

Use `run_preflight` antes da lógica protegida. O `ExecutionReceiptV1` é emitido pelo runner canônico após execução coerente. Para uma conclusão canônica da EDA piloto, use a rota L4 `run_enforced.py` e depois o finalizador `postflight.py` com handoff estruturado.

## 4. Quando não usar?

Não monte Receipt ou Postflight manualmente para legitimar rota paralela. Não trate `resolved` como sinônimo de `called`. Não transforme recurso importado em recurso concluído. Não use output tecnicamente correto como substituto de evidência canônica.

## 5. Como funciona, intuitivamente?

Fluxo L4 da skill piloto:

```text
execution_contract
  → run_preflight
  → run.py::run                # core L3
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

Uma EDA sintética deve fornecer entradas objetivas e seguir o perfil canônico. Na rota atual da skill, distribuições e diagnóstico visual são ligados por padrão; preview/amostra são opt-in. Sem PK estabelecida, `data_quality_check` é `not_applicable`, não se inventa chave para passar. Se um recurso material **aplicável** não terminar ou o handoff ficar incompleto, a finalização não autoriza conclusão.

O [notebook deste objeto](exemplo_skill_execution.py) demonstra somente preflight L2 com contexto sintético. Seu PASS não demonstra Receipt, L4, análise dos dados ou outro perfil executável.

## 7. O que você precisa antes de usar?

Para o preflight: contrato válido, raiz `.assistant` e contexto das condições.

Para o Receipt: trace coerente, resultado atual, release íntegra, provenance runtime sem conflito e primitive protegida concluída.

Para o Postflight: Receipt `VALID`, trace L4, artifacts vinculados por digest, decisões completas, evidência dos requisitos required/conditional aplicáveis, templates carregados e handoff final conforme o contrato.

## 8. O que este recurso entrega?

Na EDA, `PENDING_POSTFLIGHT` significa evidência coletada com finalização pendente: `completion.claim_allowed=false`. Não é sucesso. Após o handoff, `finalize_or_raise` deve retornar Postflight `PASS`, `completion.authorized=true` e `completion.status="COMPLETED"` antes do claim de conclusão.

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

**Operador da skill:** comece pela [EDA profissional](../../skills/hub-ml-eda-profissional/SKILL.md) ou pela [skill escolhida](../../skills/README.md). Use seus entrypoints e verificadores; não construa Receipt/Postflight para legitimar uma rota paralela.

**Integrador do framework:** confira [fachada](__init__.py), [preflight/policy](skill_execution.py), [Receipt](receipt/__init__.py), [Postflight](postflight/__init__.py) e [domínio temporal](domain_context/README.md). Assinaturas públicas:

| API | Entradas e retorno |
|---|---|
| `run_preflight(contract_path, *, assistant_root, context)` | path/string, raiz e Mapping → `PreflightResult` |
| `load_enforcement_policy_registry(*, assistant_root=None, policy_path=None)` | paths opcionais → dict por nome de skill |
| `get_skill_enforcement_policy(skill, *, assistant_root=None, policy_path=None)` | nome registrado → `SkillEnforcementPolicy` |
| `list_skill_enforcement_policies(*, assistant_root=None, policy_path=None)` | paths opcionais → tuple ordenada por nome |

Consulta mínima somente leitura:

```python
from hub_scripts.skill_execution import get_skill_enforcement_policy
policy = get_skill_enforcement_policy("hub-ml-auditoria-skills")
```

A [policy publicada](../../hub_padroes/skill_enforcement/policy.json) é a fonte do conjunto atual de registros; use a listagem em vez de congelar a contagem. Falha de leitura/forma ou skill desconhecida gera `EnforcementPolicyError`. Consulta não chama análise, emite Receipt ou promove nível.

## 10. Decisões e configurações que mais importam

- `execution_contract.mode="audit"` e `policy.rollout_mode` são campos distintos; não os iguale nem promova níveis por editar documentação.
- `current_level` é vigente; `target_level` é roadmap.
- `run.py` é core L3; `run_enforced.py` e finalização completam a rota L4 da EDA.
- `resources_called` registra tentativa; `resources_completed` exige retorno bem-sucedido.
- Templates aplicáveis só contam quando lidos e vinculados por digest.
- Contexto faltante não produz evidência fabricada; aplicabilidade segue contrato e entrada objetiva.
- Handoff incompleto não é completion; Postflight vincula trace, artifacts e handoff.
- Claim persistido exige reverificação canônica, não autodeclaração.

## 11. Limitações, riscos e armadilhas

SHA-256 fornece binding e detecção de adulteração, não assinatura digital ou attestation externa. O Postflight não comprova fatos não instrumentados: deve falhar fechado ou exigir revisão. Perfis sintéticos implementados em outras skills possuem inputs, autorizações, oráculos e verificadores próprios; sua existência ou aceite técnico delimitado não promove `current_level` nem generaliza a rota L4 da EDA.

## 12. Quais são as alternativas?

O [preflight da EDA](../../skills/hub-ml-eda-profissional/scripts/preflight.py) diagnostica pré-condições; o [core](../../skills/hub-ml-eda-profissional/scripts/run.py) emite Receipt. Nenhum isoladamente substitui o [finalizador](../../skills/hub-ml-eda-profissional/scripts/postflight.py). A [skill Auditoria](../../skills/hub-ml-auditoria-skills/SKILL.md) avalia aderência e consome verificadores existentes; não sobrepõe score editorial ao gate mecânico.

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

- [Preflight e policy](skill_execution.py) e [fachada pública](__init__.py).
- [Receipt](receipt/__init__.py) e [Postflight](postflight/__init__.py).
- [Exemplo L2](exemplo_skill_execution.py): apenas pré-condições, sem análise.
- [EDA: core](../../skills/hub-ml-eda-profissional/scripts/run.py), [executor](../../skills/hub-ml-eda-profissional/scripts/run_enforced.py), [finalizador](../../skills/hub-ml-eda-profissional/scripts/postflight.py) e [manifesto](../../skills/hub-ml-eda-profissional/release_manifest.json).
- [domain_context](domain_context/README.md): validação temporal interna, com consumidores delimitados.

Desenvolvimento, fora do pacote: [ADR-0021](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/main/docs/decisions/ADR-0021-execucao-verificavel-de-skills.md) e [gates dos perfis sintéticos](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/main/docs/sprints/skill_enforcement_rollout/B1_GATES_POS_MERGE_2026-10-01.md). Não são dependências da operação cotidiana.

## 15. Referências

O comportamento é definido pelas implementações, contratos e schemas vinculados. Para uso, siga a skill e a policy; para manutenção, use os registros externos indicados. Imports e exemplos de preflight não comprovam o ciclo completo nem homologação Databricks.
