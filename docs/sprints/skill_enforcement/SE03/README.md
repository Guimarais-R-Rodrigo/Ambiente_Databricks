# SE03 — Entry point estrutural do core protegido

## Estado

**EM DESENVOLVIMENTO — branch-first / sem PR aberta.**

A SE03 implementa o nível L3 (`Deterministic execution`) do Skill Enforcement Framework na skill piloto `hub-ml-eda-profissional`.

Baseline de abertura:

- `main`: `0f1a8b18e8e7380aad75be096b0ce167e14f9662`;
- origem: merge por squash da PR #74 (SE02);
- branch: `sef/SE03-entrypoint-estrutural`;
- SE02: aceita e integrada;
- contrato vigente da skill: v0.1, `mode="audit"`;
- PR da SE03: **não aberta** durante desenvolvimento;
- publicação corporativa: fora do escopo.

A revisão operacional vigente é `../REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md`.

## Evidência herdada da SE02

A SE03 nasce para atacar limitações observadas:

- `LOCAL_CERTIFICATION=PASS` na candidata SE02;
- `DATABRICKS_FREE=PASS` no alcance do L2;
- F02-P1: `PASS_OBSERVED` quando o preflight foi explicitamente solicitado;
- F02-A1: `FAIL_OBSERVED / BYPASS_ACCEPTED` sob pressão para pular o preflight;
- F02-A2: `LIMITATION_CONFIRMED` quando `numeric_columns=0` contradisse quatro colunas numéricas observadas;
- `GITHUB_ACTIONS=DEFERRED_CREDIT` na SE02 por indisponibilidade de runner/crédito sem steps executados.

## Progresso observado

### Fatia 01

Certificada localmente no HEAD `107a0c1575ec68133df6e0d702a3d4fe74e50897`:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE03_LOCAL
DERIVED_STALE       = false
failures            = 0
```

A rodada verde incluiu 13/13 testes SE03, regressões SE01/SE02, estrutura, renderer, drift e snapshot.

### Fatia 02

Implementada, ainda aguardando execução local observável. Ela mantém a mesma única primitive protegida e acrescenta:

- `numeric_columns` como `runtime_derived`;
- conflito runtime x declarado → fail-closed;
- provenance estruturada no trace;
- digest de input/output;
- detecção de output pós-runner alterado;
- avaliação de stale trace por `expected_run_id` no alcance local;
- E02/E03/E08/E09/E10/E11/E12 na suíte.

## Objetivo

Construir um único entrypoint canônico para o core protegido da `hub-ml-eda-profissional` que:

1. receba pedido/contexto serializável;
2. derive fatos de runtime mecanicamente observáveis;
3. valide integridade mínima da release;
4. execute o preflight L2 existente;
5. chame somente primitives canônicas nas etapas protegidas;
6. aborte de forma fechada quando requisito obrigatório falhar;
7. produza `ExecutionTraceV0` suficiente para distinguir caminho canônico, caminho paralelo, abort correto e fallback indevido;
8. não antecipe o Execution Receipt formal da SE04 nem o postflight da SE05.

## Invariantes

- `ambiente_fonte/` é a única fonte editável.
- `Novo_Ambiente_Simulado/` é derivado exclusivamente por `tools/render_simulado.py --write`.
- O runner não copia implementação de `hub_snippets`/`hub_scripts`.
- O preflight SE02 é reutilizado; sua semântica não é duplicada.
- Falha de primitive required não autoriza fallback manual silencioso.
- Output correto sem runner não equivale a canonical compliance.
- `ExecutionTraceV0` é evidência técnica mínima da SE03; não é Receipt SE04.
- Nenhum dado real corporativo é usado no desenvolvimento/homologação.
- Nenhuma PR é aberta antes da release candidate estabilizada.

## Entrypoint e primitive protegida

Entrypoint único:

`skills/hub-ml-eda-profissional/scripts/run.py::run`

Primitive protegida atual:

`hub_scripts.quick_profile.quick_profile`

A expansão para outras primitives fica condicionada à estabilização das fatias 01–02 e aos evals no Free.

## ExecutionTraceV0

O trace atual contém:

- `trace_version`;
- `run_id`;
- `skill`;
- `entrypoint`;
- `contract_digest`;
- `runner_digest`;
- `manifest_digest`;
- `input_digest`;
- `output_digest`;
- `preflight_status`;
- `context_provenance`;
- decisões do preflight;
- resources resolvidos/chamados;
- `fallback_used`;
- `writes_performed`;
- issues estruturadas;
- `status`.

O trace não armazena payload de negócio.

## Provenance

Fontes conceituais:

- `runtime_derived`;
- `user_intent`;
- `agent_declared`.

Na fatia 02, `numeric_columns` é derivado de `spark.table(...).dtypes`. Se o valor declarado divergir do runtime, a execução fica `BLOCKED` com `CONTEXT_PROVENANCE_CONFLICT`; não existe correção silenciosa.

Os demais campos ainda não possuem provenance mecanicamente diferenciada entre `user_intent` e `agent_declared`.

## Integridade mínima da release

`release_manifest.json` protege:

- contrato da skill;
- runner;
- engine do preflight;
- `quick_profile`.

A identidade atual usa `git_blob_sha1` por reprodutibilidade de bytes Git/runtime. Isso não é alegação de segurança contra atacante administrativo.

## Canonical compliance

O evaluator exige caminho/trace coerentes, primitive protegida chamada, ausência de fallback, provenance runtime para `numeric_columns` e digest do resultado atual compatível com o trace.

Output manual, helper direto ou resultado alterado depois do runner não satisfaz compliance.

`expected_run_id` é somente um mecanismo de micro-eval para stale trace; anti-replay formal pertence à SE04.

## Fora do escopo

A SE03 não implementa:

- Receipt formal/versionado de SE04;
- postflight/conclusão fail-closed de SE05;
- generalização a todas as skills;
- mudança para `mode="enforce"` sem decisão própria;
- persistência indiscriminada de outputs ou traces;
- defesa contra atacante com acesso administrativo/root;
- promoção ao workspace corporativo;
- alteração da lógica científica de helpers sem defeito independente.

## Estratégia de certificação

```text
branch sem PR
  → testes locais
  → certifier local
  → micro-evals estruturais
  → Databricks Free
  → documentação + release candidate
  → abrir PR
  → GitHub Actions final
  → aceite humano
  → merge
```

Estados permanecem separados:

- `LOCAL_CERTIFICATION`;
- `SYNTHETIC_AGENT_SCREENING`;
- `DATABRICKS_FREE`;
- `GITHUB_ACTIONS`;
- `FULLY_CERTIFIED`.

## Critério de encerramento

A SE03 só pode ser apresentada para aceite quando houver evidência de que E01–E12 foram exercitados no alcance definido, local gate e Free estiverem estabilizados e SE04/SE05 não tiverem sido antecipadas.

## Próximo passo

Executar a suíte ampliada da fatia 02 e o `certify_local.py --profile se03`. Depois, com os E01–E12 locais observados, preparar o protocolo do Databricks Free sem abrir PR.
