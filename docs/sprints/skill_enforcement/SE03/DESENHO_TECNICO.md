# SE03 — desenho técnico inicial

## Status

**BOOTSTRAP — desenho a congelar antes da implementação funcional.**

Este documento traduz a revisão local-first/structural-first para decisões técnicas específicas da SE03. Nenhuma decisão abaixo autoriza antecipar SE04/SE05.

## 1. Problema a resolver

A SE02 provou que o preflight L2 funciona quando é acionado, mas também mostrou duas superfícies de bypass:

1. o agente pode aceitar pular o preflight sob pressão por rapidez;
2. o preflight pode confiar em contexto declarado incompatível com fatos mecanicamente deriváveis.

A SE03 deve retirar do agente a decisão sobre usar ou não o caminho protegido: o core homologável precisa nascer do runner.

## 2. Forma do runner

Requisitos do entrypoint:

- um único entrypoint público para o core protegido da skill;
- interface serializável e testável sem notebook interativo;
- resolução da raiz `.assistant` sem hardcode de usuário;
- reutilização direta de `hub_scripts.skill_execution.run_preflight`;
- nenhuma cópia da lógica de helpers;
- emissão de `ExecutionTraceV0` pelo próprio runner;
- códigos/estados de saída determinísticos;
- comportamento fail-closed quando integridade/preflight/primitive required falhar.

O nome/path final do arquivo só será congelado junto com os testes de API pública. Até lá, não deve haver mais de um candidato executável concorrente.

## 3. Fases internas obrigatórias

Fluxo conceitual:

```text
DISCOVER
  → DERIVE_CONTEXT
  → VERIFY_RELEASE
  → PREFLIGHT
  → EXECUTE_PROTECTED_STEPS
  → EMIT_TRACE
```

### DISCOVER

Resolve skill, contrato, raiz `.assistant` e artefatos canônicos. Não executa análise.

### DERIVE_CONTEXT

Deriva fatos objetivos de runtime quando possível e registra provenance. Não deve sobrescrever silenciosamente intenção do usuário.

### VERIFY_RELEASE

Valida fingerprints dos artefatos protegidos. Qualquer divergência relevante resulta em abort antes do core.

### PREFLIGHT

Chama a implementação SE02 existente. `BLOCKED` encerra o runner; não há fallback manual.

### EXECUTE_PROTECTED_STEPS

Executa somente primitives canônicas declaradas para as etapas protegidas. Etapas ainda interpretativas podem permanecer fora do runner, desde que isso seja explícito.

### EMIT_TRACE

Produz `ExecutionTraceV0` derivado do caminho real percorrido.

## 4. Primitive set mínimo

Antes de implementar, a sprint deve congelar quais recursos da EDA pertencem ao core protegido. A seleção deve favorecer recursos:

- estáveis;
- já públicos no Hub;
- determinísticos o suficiente para teste;
- diretamente ligados ao failure mode original;
- sem exigir persistência de dados reais.

Candidatos herdados do contrato SE02 incluem `quick_profile`, `data_quality_check`, `null_summary`, `smart_sample`, `safe_display`, `correlation_matrix` e `distribution_grid`. A inclusão no runner não é automática: cada primitive precisa de justificativa de acoplamento e teste próprio.

Helpers opcionais/editoriais não devem ser promovidos a required apenas para aumentar enforcement.

## 5. ContextEnvelopeV0

O runner deve trabalhar com uma representação interna que separe valor e origem. Estrutura conceitual:

```json
{
  "numeric_columns": {
    "value": 4,
    "source": "runtime_derived",
    "evidence": "schema"
  },
  "numeric_distributions_requested": {
    "value": true,
    "source": "user_intent"
  }
}
```

Fontes mínimas:

- `runtime_derived`;
- `user_intent`;
- `agent_declared`.

### Política de conflito a decidir

Para valores `runtime_derived`, duas opções são aceitáveis para avaliação inicial:

A. valor derivado prevalece e a divergência é registrada; ou
B. divergência bloqueia o runner com issue explícita.

A opção escolhida deve ser única, testada e documentada; o agente não escolhe caso a caso.

## 6. ReleaseManifestV0

O manifest deve ser determinístico e pequeno. Estrutura candidata:

```json
{
  "manifest_version": "0.1",
  "skill": "hub-ml-eda-profissional",
  "artifacts": [
    {"path": "...", "sha256": "...", "role": "contract"},
    {"path": "...", "sha256": "...", "role": "runner"},
    {"path": "...", "sha256": "...", "role": "primitive"}
  ]
}
```

Regras:

- paths relativos à raiz canônica;
- ordem determinística;
- SHA-256 de bytes normalizados apenas quando a normalização já for definida;
- sem incluir arquivos irrelevantes só para aumentar cobertura aparente;
- manifest não pode ser regenerado automaticamente durante execução para “aceitar” adulteração.

## 7. ExecutionTraceV0

Estrutura mínima candidata:

```json
{
  "trace_version": "0.1",
  "run_id": "...",
  "skill": "hub-ml-eda-profissional",
  "entrypoint": "...",
  "contract_digest": "...",
  "runner_digest": "...",
  "manifest_digest": "...",
  "preflight_status": "PASS",
  "decisions": [],
  "resources_resolved": [],
  "resources_called": [],
  "fallback_used": false,
  "status": "PASS"
}
```

Regras:

- trace derivado do runner, nunca preenchido manualmente pelo agente;
- `resources_called` deve vir de instrumentação do caminho real;
- trace não prova sozinho correção científica;
- trace não deve carregar conteúdo sensível;
- trace stale/reutilizado precisa ser distinguível no alcance dos evals da SE03.

## 8. Canonical compliance

O evaluator da SE03 deve separar:

- `task_correctness`: o resultado de negócio/técnico está correto no cenário sintético;
- `canonical_compliance`: o runner e primitives exigidos foram usados com trace válido.

Exemplo obrigatório:

```text
output manual correto
→ task_correctness = PASS
→ canonical_compliance = FAIL
```

## 9. Failure taxonomy

Códigos candidatos, a congelar antes do core:

- `RELEASE_INTEGRITY_MISMATCH`;
- `CONTEXT_PROVENANCE_CONFLICT`;
- `PREFLIGHT_BLOCKED`;
- `REQUIRED_PRIMITIVE_UNAVAILABLE`;
- `REQUIRED_PRIMITIVE_FAILED`;
- `CANONICAL_ENTRYPOINT_BYPASSED`;
- `TRACE_INVALID`;
- `TRACE_STALE`;
- `OUTPUT_DIVERGED_AFTER_RUNNER`.

A taxonomia deve evitar códigos redundantes que expressem a mesma causa.

## 10. Persistência e privacidade

Por padrão, testes locais devem manter trace em memória ou diretório temporário fora do produto. Persistência versionada de receipts/traces não pertence à SE03. O Databricks Free só deve usar dados sintéticos.

## 11. Critérios para sair do desenho e entrar em implementação

Antes do primeiro commit funcional, devem estar congelados:

1. path/API pública única do runner;
2. primitive set protegido mínimo;
3. política de conflito de provenance;
4. schema mínimo do manifest;
5. schema mínimo do trace;
6. failure taxonomy mínima;
7. evaluator correctness/compliance;
8. casos E01–E12 com fixtures reproduzíveis;
9. política de não persistência/sanitização;
10. compatibilidade com renderer, validator e publicador Free.

O próximo commit funcional deve implementar apenas o menor vertical slice capaz de satisfazer E01, E04 e E07, antes de ampliar o runner.