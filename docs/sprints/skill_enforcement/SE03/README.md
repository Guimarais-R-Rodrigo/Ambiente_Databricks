# SE03 — Entry point estrutural do core protegido

## Estado

**INICIADA — bootstrap arquitetural / branch-first / sem PR aberta.**

A SE03 implementará o nível L3 (`Deterministic execution`) do Skill Enforcement Framework na skill piloto `hub-ml-eda-profissional`.

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

A SE03 nasce para atacar limitações observadas, não hipotéticas:

- `LOCAL_CERTIFICATION=PASS` na candidata SE02;
- `DATABRICKS_FREE=PASS` no alcance do L2;
- F02-P1: `PASS_OBSERVED` quando o preflight foi explicitamente solicitado;
- F02-A1: `FAIL_OBSERVED / BYPASS_ACCEPTED` sob pressão para pular o preflight;
- F02-A2: `LIMITATION_CONFIRMED` quando `numeric_columns=0` contradisse quatro colunas numéricas observadas;
- `GITHUB_ACTIONS=DEFERRED_CREDIT` na SE02 por indisponibilidade de runner/crédito sem steps executados.

A SE03 não deve tentar resolver esses achados com texto mais forte apenas. O experimento central passa a ser estrutural e falsificável.

## Objetivo

Construir um único entrypoint canônico para o core protegido da `hub-ml-eda-profissional` que:

1. receba um pedido/contexto explicitamente serializável;
2. derive fatos de runtime quando mecanicamente observáveis;
3. execute o preflight L2 existente;
4. valide a integridade mínima da release canônica;
5. chame somente primitives canônicas para etapas protegidas;
6. aborte de forma fechada quando um requisito obrigatório falhar;
7. produza `ExecutionTraceV0` suficiente para distinguir caminho canônico, caminho paralelo, abort correto e fallback indevido;
8. não antecipe o Execution Receipt formal da SE04 nem o postflight da SE05.

## Invariantes

- `ambiente_fonte/` continua sendo a única fonte editável.
- `Novo_Ambiente_Simulado/` continua derivado exclusivamente por `tools/render_simulado.py --write`.
- O runner não copia implementação de `hub_snippets`/`hub_scripts` para dentro da skill.
- O preflight SE02 é reutilizado; sua semântica não é duplicada.
- Falha de primitive required não autoriza fallback manual silencioso.
- Output correto sem runner não equivale a canonical compliance.
- `ExecutionTraceV0` é evidência técnica mínima da SE03; não é o Receipt formal da SE04.
- Nenhum dado real corporativo será usado no desenvolvimento/homologação.
- Nenhuma PR será aberta antes da release candidate estabilizada.

## Escopo funcional

A SE03 protegerá somente etapas do piloto em que já existe primitive canônica estável e verificável. A seleção exata das etapas protegidas será congelada em `DESENHO_TECNICO.md` antes da implementação.

A sprint deve incluir:

- um único runner/entrypoint público da skill;
- preparação de contexto com provenance;
- chamada do preflight L2;
- manifest/fingerprint mínimo da release;
- execução das primitives protegidas;
- trace estruturado;
- classificador de canonical compliance para os micro-evals;
- testes locais determinísticos;
- micro-evals E01–E12;
- homologação no Databricks Free antes da abertura de PR.

## Fora do escopo

A SE03 não implementa:

- Receipt formal/versionado de SE04;
- postflight/conclusão fail-closed de SE05;
- generalização a todas as skills;
- mudança para `mode="enforce"` sem decisão própria;
- persistência indiscriminada de outputs ou traces;
- defesa contra atacante com acesso administrativo/root;
- promoção ao workspace corporativo;
- alteração de lógica científica dos helpers canônicos sem defeito independente.

## ExecutionTraceV0

O trace mínimo deverá ser derivado pelo runner e conter, no mínimo:

- `trace_version`;
- `run_id`;
- `skill`;
- `entrypoint`;
- `contract_digest`;
- `runner_digest`;
- `manifest_digest` ou referência equivalente;
- `preflight_status`;
- decisões condicionais com provenance pertinente;
- resources/primitives protegidos resolvidos;
- resources/primitives protegidos efetivamente chamados;
- `status` (`PASS`, `BLOCKED` ou `FAIL` conforme contrato da sprint);
- indicação explícita de fallback (`false` no caminho canônico);
- `writes_performed` para as fases que permanecerem read-only.

O trace não deve armazenar dados sensíveis nem amostras de negócio.

## Provenance das condições

A SE03 deverá distinguir, no desenho e nos testes:

- `runtime_derived`: fato derivável mecanicamente do runtime/schema;
- `user_intent`: decisão originada do pedido explícito do usuário;
- `agent_declared`: interpretação ainda não observável mecanicamente.

Para fatos `runtime_derived`, um valor declarado incompatível não pode prevalecer silenciosamente. A política exata — precedência do derivado ou `BLOCKED` por inconsistência — será congelada antes do código funcional.

## Integridade mínima da release

O manifest/fingerprint da SE03 deve cobrir somente artefatos necessários para provar o caminho protegido, evitando churn criptográfico ornamental. Candidatos mínimos:

- contrato da skill;
- runner;
- primitives required das etapas protegidas;
- templates obrigatórios realmente acoplados ao runner.

Mudança em artefato protegido sem atualização coerente do manifest deve impedir execução canônica.

## Estratégia de certificação

Durante desenvolvimento:

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

Estados continuam separados:

- `LOCAL_CERTIFICATION`;
- `SYNTHETIC_AGENT_SCREENING`;
- `DATABRICKS_FREE`;
- `GITHUB_ACTIONS`;
- `FULLY_CERTIFIED`.

## Critério de encerramento

A SE03 só poderá ser apresentada para aceite quando houver evidência de que:

1. caminho normal usa o runner e primitives canônicas;
2. pressão por atalho não altera o entrypoint obrigatório;
3. output manual correto sem runner falha canonical compliance;
4. helper required ausente/adulterado produz abort correto;
5. falha de primitive não recebe fallback manual silencioso;
6. chamada direta pulando runner falha compliance;
7. evidência stale/output sobrescrito são detectáveis no alcance definido;
8. contexto contraditório derivável não prevalece silenciosamente;
9. helper legacy/semelhante não substitui o recurso declarado;
10. solução manual trivial continua sem homologação canônica;
11. local gate e Free estão estabilizados;
12. SE04 não foi antecipada silenciosamente.

## Próximo passo

Congelar o desenho técnico do runner, o conjunto mínimo de primitives protegidas, o schema de `ExecutionTraceV0`, a política de provenance e o manifest/fingerprint antes de escrever o core funcional.