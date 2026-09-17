# SE03 — fatia funcional 01

## Estado

**CERTIFICADA LOCALMENTE.**

Esta fatia é o menor vertical slice estrutural da SE03. Ela não fecha a sprint e não autoriza abrir PR.

A certificação final da fatia 01 foi observada no HEAD `107a0c1575ec68133df6e0d702a3d4fe74e50897` em Windows 11 / Python 3.12.10:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE03_LOCAL
DERIVED_STALE       = false
failures            = 0
```

A suíte focada terminou em 13/13 PASS; regressões SE01/SE02, validação estrutural, renderer, verificação de drift e snapshot também passaram. Evidência externa ao repositório: `~/.ambiente_databricks/sef_certifications/20260917T174041Z_107a0c1575ec`.

Uma rodada anterior no HEAD `115a318a1a7c6776fa1c39f4617649c1d08698ec` permaneceu corretamente `FAIL` por snapshot defasado e revelou que o antigo `git diff --exit-code` não detectava novos arquivos derivados não rastreados. O certifier foi corrigido para usar `git status --porcelain --untracked-files=all` no escopo derivado, e uma regressão específica passou a proteger esse caso.

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

### ExecutionTraceV0 inicial

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

## Evals certificados nesta fatia

- E01 — caminho normal;
- E04 — primitive required ausente;
- E05 — primitive adulterada;
- E06 — primitive canônica falha;
- E07 — chamada/output sem runner não satisfaz canonical compliance.

Também passaram testes de input inválido, determinismo estrutural do trace, separação entre trace e resultado de negócio, ausência de hook público para injeção de primitive e detecção de arquivo derivado novo não rastreado.

## Evals transferidos para a fatia 02

- E02 pressão por atalho;
- E03 output manual correto com evaluator completo;
- E08 output sobrescrito após runner;
- E09 trace stale/replay no alcance local;
- E10 conflito de provenance;
- E11 helper legacy concorrente;
- E12 solução manual trivial.

A política `runtime_derived` x `agent_declared` não foi implementada na fatia 01; ela é objeto da fatia 02.

## Estado dos gates da fatia 01

```text
LOCAL_CERTIFICATION        = PASS
SYNTHETIC_AGENT_SCREENING = NOT_RUN_SE03
DATABRICKS_FREE            = NOT_RUN_SE03
GITHUB_ACTIONS             = NOT_RUN_SE03
FULLY_CERTIFIED            = false
PR                         = NOT_OPEN
```

## Continuidade

A fatia 02 endurece provenance, binding do output e canonical compliance sem ampliar ainda o conjunto de primitives protegidas.
