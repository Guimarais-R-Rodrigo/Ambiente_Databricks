# ADR-0025 — Reconciliação de papéis e precedência de estado no controller SER

Data: 2026-09-26
Status: Aceito
Autor: ChatGPT + autorização humana explícita para AC-R1

## Contexto

O ADR-0023 separou autoria repo-side de workers locais determinísticos: workers de
campanha recebem candidatas congeladas e não corrigem código durante certificação.
O ADR-0024 adicionou um controller Codex com um executor de autoria A1 capaz de
fazer reparos causais repo-side.

Sem uma reconciliação explícita, frases anteriores como “executor não aplica patch”
ou “a implementação volta à autoria” podem ser lidas como proibição global e
contradizer o novo papel A1. O mesmo problema existe para estado: snapshots de
planejamento B0 e runbooks congelados continuam versionados e podem parecer mais
atuais que o state source B1.

## Decisão

Adotar três planos de execução com nomes não intercambiáveis:

1. **Authoring Controller / A1 Authoring Executor** — pode investigar e alterar
   somente `repo_scope.write_roots` do envelope ativo, com causal delta e
   single-writer.
2. **Deterministic Campaign Coordinator/Executor** — executa candidata congelada,
   commands allowlisted e evidência; nunca corrige código/teste/critério durante
   certificação.
3. **Controlled Integrator/Publisher** — opera composição/renderer/publicação/merge
   apenas sob os gates próprios.

As proibições históricas de “worker/executor não altera produto”, “não aplica
patch” e “coordenador não inventa script” pertencem ao plano 2, salvo quando o
texto disser explicitamente outra coisa.

O controller A1 não pode modificar sua própria governança. Paths listados em
`repo_scope.shared_roots_requiring_human_gate` exigem
`CONTROLLER_MAINTENANCE`. Paths em `protected_roots` permanecem fora de A1.

### Precedência de estado

Para B1:

1. `B1/AUTHORING_STATE.json` é o state source vivo;
2. os READMEs correntes da SER/PARALELO são índices humanos;
3. manifests e contratos do gate corrente definem critérios;
4. `CONTROLE_PLANO.json`, `DAG.json`, runbooks congelados e documentos de
   tentativa são planejamento/histórico, salvo ponteiro explícito do state source.

Um arquivo histórico nunca reabre um gate já fechado apenas por conter
`NOT_RUN` ou `PLANNED_NOT_STARTED`.

### A2

A2 só pode ser ativada quando `activation.a2_reference` e `a2_contract`
estiverem completos e válidos. O contrato precisa fixar target, namespace,
effects, budgets, dados, overwrite, readback, UNKNOWN policy e cleanup.

## Alternativas consideradas

- Confiar apenas na seção 9.12 para desambiguar os papéis — rejeitada: a
  instrução contraditória continuaria em documentos normativos anteriores.
- Reescrever ADR-0023 — rejeitada: ADR aceito é histórico imutável.
- Permitir ao controller reparar sua própria governança — rejeitada por
  circularidade de autoridade.

## Consequências

- Repair A1 fica claramente permitido sem relaxar single-shot de certificação.
- O controller deixa de tratar snapshots antigos como estado vivo.
- Mudança de governança vira Human Gate separado.
- B0 continua prova do executor determinístico; ADR-0024 não o transforma em
  writer.
- O envelope passa a ser a fronteira executável de escopo repo-side/remoto.

## Referências

- ADR-0023
- ADR-0024
- `docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md`
- `docs/operations/autonomy/B1_AUTONOMY_ENVELOPE.json`
