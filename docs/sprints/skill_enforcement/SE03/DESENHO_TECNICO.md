# SE03 — desenho técnico

## Status

**DESENHO CONGELADO PARA AS FATIAS 01–02 / IMPLEMENTAÇÃO EM EVOLUÇÃO.**

Este documento traduz a revisão local-first/structural-first para decisões técnicas específicas da SE03. Nenhuma decisão abaixo antecipa SE04/SE05.

## 1. Problema a resolver

A SE02 provou que o preflight L2 funciona quando é acionado, mas mostrou duas superfícies de bypass:

1. o agente pode aceitar pular o preflight sob pressão por rapidez;
2. o preflight pode confiar em contexto declarado incompatível com fatos mecanicamente deriváveis.

A SE03 retira do agente a decisão sobre como executar o core homologável: canonical compliance exige o runner estrutural.

## 2. Forma do runner

Entrypoint congelado:

`skills/hub-ml-eda-profissional/scripts/run.py::run`

Requisitos:

- um único entrypoint público para o core protegido da skill;
- interface serializável e testável;
- resolução da raiz `.assistant` sem hardcode de usuário;
- reutilização direta de `hub_scripts.skill_execution.run_preflight`;
- nenhuma cópia da lógica de helpers;
- emissão de `ExecutionTraceV0` pelo próprio runner;
- comportamento fail-closed quando integridade, contexto runtime, preflight ou primitive required falhar;
- nenhuma API pública para injetar/substituir primitive canônica.

## 3. Fases internas

Fluxo vigente:

```text
DISCOVER
  → VERIFY_RELEASE
  → DERIVE_CONTEXT
  → PREFLIGHT
  → EXECUTE_PROTECTED_STEPS
  → EMIT_TRACE
```

A verificação de release ocorre antes de consultar runtime para evitar executar observadores sobre uma release já divergente.

### DISCOVER

Resolve skill, contrato, raiz `.assistant` e artefatos canônicos.

### VERIFY_RELEASE

Valida fingerprints dos artefatos protegidos. Divergência relevante resulta em abort antes do core.

### DERIVE_CONTEXT

Deriva fatos objetivos de runtime. Na fatia 02, `numeric_columns` é contado a partir de `spark.table(...).dtypes`.

### PREFLIGHT

Chama a implementação SE02 existente com o contexto efetivo. `BLOCKED` encerra o runner.

### EXECUTE_PROTECTED_STEPS

Executa somente primitives canônicas declaradas para as etapas protegidas.

### EMIT_TRACE

Produz `ExecutionTraceV0` derivado do caminho real percorrido.

## 4. Primitive set protegido atual

Somente:

`hub_scripts.quick_profile.quick_profile`

A seleção é deliberadamente mínima. Antes de ampliar para `data_quality_check`, `null_summary`, amostragem ou visualização, a arquitetura atual precisa passar E01–E12 e Free.

Helpers opcionais/editoriais não são promovidos a required apenas para aumentar enforcement.

## 5. ContextEnvelopeV0 — alcance atual

O trace registra provenance por campo observado. Fontes conceituais do framework:

- `runtime_derived`;
- `user_intent`;
- `agent_declared`.

Na fatia 02, somente `numeric_columns` tem provenance mecanicamente garantida como `runtime_derived`; os demais valores recebidos continuam classificados como `agent_declared` até haver observador/contrato específico.

### Política congelada para conflito E10

**BLOCKED por inconsistência.**

Para `numeric_columns`:

- valor omitido → usa derivação runtime;
- valor declarado igual ao runtime → segue;
- valor declarado diferente → `CONTEXT_PROVENANCE_CONFLICT` e abort antes do preflight/core;
- valor declarado com tipo inválido → `CONTEXT_PROVENANCE_CONFLICT`.

O runner não sobrescreve silenciosamente uma contradição.

## 6. ReleaseManifestV0

Arquivo: `skills/hub-ml-eda-profissional/release_manifest.json`.

Algoritmo atual: `git_blob_sha1` para identidade reproduzível de bytes no Git/runtime. Isso é fingerprint operacional, não fronteira criptográfica de segurança.

Artefatos protegidos atuais:

1. `execution_contract.json`;
2. `scripts/run.py`;
3. `hub_scripts/skill_execution/skill_execution.py`;
4. `hub_scripts/quick_profile/quick_profile.py`.

Regras:

- paths relativos à raiz `.assistant`;
- nenhuma regeneração automática durante execução;
- primitive ausente/adulterada bloqueia;
- helper legacy semelhante não substitui artefato declarado.

## 7. ExecutionTraceV0

Campos vigentes:

- `trace_version`;
- `run_id`;
- `skill`;
- `entrypoint`;
- `manifest_digest`;
- `contract_digest`;
- `runner_digest`;
- `input_digest`;
- `output_digest`;
- `preflight_status`;
- `context_provenance`;
- `decisions`;
- `resources_resolved`;
- `resources_called`;
- `fallback_used`;
- `writes_performed`;
- `blocking_issues`;
- `status`.

O trace não carrega o payload de negócio. `output_digest` vincula a evidência ao resultado atual no alcance da SE03.

## 8. Canonical compliance

`is_canonically_compliant` separa resultado de negócio de aderência canônica.

Requisitos atuais incluem:

- trace válido;
- entrypoint canônico;
- status/preflight PASS;
- digests de release/input/output presentes e coerentes;
- `numeric_columns` com provenance `runtime_derived`;
- `quick_profile` registrada como chamada;
- `fallback_used=false`.

Output manual correto sem trace do runner permanece compliance FAIL.

### Stale trace — alcance local

O evaluator aceita opcionalmente `expected_run_id`. O harness pode rejeitar um trace antigo quando espera o id de uma execução atual.

Essa regra é deliberadamente limitada: não constitui proteção universal de replay. Receipt/anti-replay formal pertence à SE04.

## 9. Failure taxonomy vigente

- `RUN_INPUT_INVALID`;
- `RELEASE_MANIFEST_INVALID`;
- `RELEASE_INTEGRITY_MISMATCH`;
- `RUNTIME_CONTEXT_UNAVAILABLE`;
- `CONTEXT_PROVENANCE_CONFLICT`;
- issues estruturadas herdadas do preflight SE02;
- `REQUIRED_PRIMITIVE_FAILED`.

Códigos de Receipt/postflight continuam fora da SE03.

## 10. Persistência e privacidade

- trace permanece em memória/saída controlada;
- nenhum payload sintético de negócio é copiado para o trace;
- apenas digests e metadados estruturais entram na evidência;
- nenhuma persistência versionada de receipts/traces;
- Free usa somente dados sintéticos.

## 11. Matriz estrutural

Fatia 01: E01/E04/E05/E06/E07.

Fatia 02: E02/E03/E08/E09/E10/E11/E12 no alcance local determinístico.

E02 e E12 ainda exigem validação conversacional no Genie Code/Databricks Free antes de encerramento da sprint.

## 12. Regra de expansão

Não ampliar primitives protegidas enquanto:

1. a fatia 02 não tiver `LOCAL_CERTIFICATION=PASS`;
2. E01–E12 locais não estiverem verdes no alcance definido;
3. não houver entendimento explícito dos limites de E02/E09/E12;
4. não houver plano de Free para o runner atual.
