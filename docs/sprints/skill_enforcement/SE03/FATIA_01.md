# SE03 — fatia funcional 01

## Estado

**IMPLEMENTADA NA BRANCH / AINDA NÃO CERTIFICADA LOCALMENTE.**

Esta fatia é o menor vertical slice estrutural da SE03. Ela não fecha a sprint e não autoriza abrir PR.

## Decisões congeladas para a fatia

### Entrypoint canônico

`skills/hub-ml-eda-profissional/scripts/run.py::run`

Não existe segundo runner concorrente nesta fatia.

### Primitive protegida

Somente:

`hub_scripts.quick_profile.quick_profile`

A escolha é intencionalmente mínima: `quick_profile` já é `required` no contrato v0.1, tem API pública estável e representa uma etapa real do core da EDA. As demais primitives continuam apenas sob preflight L2 até slices posteriores.

### Manifest de release

Arquivo:

`skills/hub-ml-eda-profissional/release_manifest.json`

Protege quatro artefatos:

1. `execution_contract.json`;
2. `scripts/run.py`;
3. `hub_scripts/skill_execution/skill_execution.py`;
4. `hub_scripts/quick_profile/quick_profile.py`.

A fatia usa `git_blob_sha1` como fingerprint de identidade de bytes porque esse valor é reproduzível tanto no Git quanto no runtime sem depender de metadados externos. Isso é um mecanismo de integridade acidental/operacional, não uma fronteira criptográfica contra atacante administrativo. A evolução para hashes/receipts formais continua pertencendo às sprints seguintes.

### ExecutionTraceV0

O runner emite trace estruturado com:

- `trace_version`;
- `run_id`;
- `skill`;
- `entrypoint`;
- `manifest_digest`;
- `contract_digest`;
- `runner_digest`;
- `preflight_status`;
- decisões do preflight;
- resources resolvidos;
- resources chamados;
- `fallback_used=false`;
- `writes_performed=false`;
- issues estruturadas;
- `status`.

O resultado de negócio fica fora do trace para reduzir risco de copiar dados no artefato de evidência.

### Fail-closed

A ordem desta fatia é:

```text
VERIFY_RELEASE
  → PREFLIGHT
  → CALL quick_profile
  → TRACE
```

Falha de integridade ou preflight `BLOCKED` impede chamada do core. Exceção da primitive produz `FAIL`, sem fallback manual.

## Evals cobertos nesta fatia

- E01 — caminho normal;
- E04 — primitive required ausente;
- E05 — primitive adulterada;
- E06 — primitive canônica falha;
- E07 — chamada/output sem runner não satisfaz canonical compliance.

Também há testes de input inválido, determinismo estrutural do trace e separação entre trace e resultado de negócio.

## Evals ainda não implementados

- E02 pressão por atalho no agente;
- E03 output manual correto com evaluator completo;
- E08 output sobrescrito após runner;
- E09 trace stale/replay;
- E10 conflito de provenance;
- E11 helper legacy concorrente;
- E12 solução manual trivial no Genie Code.

Esses casos não devem ser classificados como PASS enquanto não houver implementação/evidência observável.

## Provenance

A política `runtime_derived` x `agent_declared` ainda não foi implementada nesta fatia. O runner consome o mesmo contexto L2 explícito da SE02. Portanto F02-A2 continua uma limitação aberta até o slice que implemente E10.

## Arquivos introduzidos

- `ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/scripts/run.py`;
- `ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/release_manifest.json`;
- `tools/tests/test_skill_enforcement_se03.py`.

O derivado `Novo_Ambiente_Simulado/` não é editado manualmente. Ele deve ser materializado pelo renderer canônico durante a certificação local.

## Estado dos gates

```text
LOCAL_CERTIFICATION        = NOT_RUN
SYNTHETIC_AGENT_SCREENING = NOT_RUN
DATABRICKS_FREE            = NOT_RUN
GITHUB_ACTIONS             = NOT_RUN
FULLY_CERTIFIED            = false
PR                         = NOT_OPEN
```

## Próximo passo

Sincronizar a branch no clone local, executar a nova suíte SE03 e o certifier. Corrigir qualquer falha observada antes de ampliar o runner para provenance/E10 ou novas primitives.