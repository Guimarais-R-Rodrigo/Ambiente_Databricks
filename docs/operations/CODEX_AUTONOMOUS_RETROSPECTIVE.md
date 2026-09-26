# Retrospectiva operacional para o Codex Autonomous Controller

Data: 2026-09-26  
Escopo principal: SER B1 / G6

Este documento não reinterpreta resultados históricos. Ele extrai padrões operacionais para reduzir repetição de falhas e handoffs.

## 1. O que gerou morosidade

### 1.1 Micro-handoffs

A cadeia de G6 foi repartida em preparação, autorização, execução, auditoria, corretiva e novo handoff em quase toda mudança causal. Isso preservou autoridade, mas fez o usuário operar como scheduler de tarefas técnicas.

**Lição:** o usuário deve aprovar envelope/gate material; o controller deve gerar internamente tarefas fechadas.

### 1.2 Retry proibido confundido com repair proibido

A regra correta “não retry-until-green” levou a várias paradas mesmo quando já havia causa e uma correção causal diferente.

**Lição:** mesmo estado + mesmo comando continua proibido; novo SHA/transporte/precondição permite nova rodada causal dentro do budget autorizado.

### 1.3 Transporte individual com `PROTOCOL_ERROR`

G6 registrou falhas repetidas do transporte CLI para Workspace Import. A R10 moveu somente a escrita material para Python HTTP/1.1 e concluiu o pacote com readback.

O primeiro attempt dos probes voltou a usar import individual e repetiu a mesma classe de erro: SER03 apareceu criado apesar do erro; SER05 permaneceu ausente.

**Lição:** erro de transporte não prova efeito. Reconciliar primeiro. Quando uma classe de transporte já tem histórico negativo, não repetir por conveniência se existe transporte alternativo qualificado e autorizado.

### 1.4 PASS de subgate confundido com PASS agregado

O full-content verify pós-R10 passou 590/590, mas o G6 agregado ainda exigia probes Free + Genie. A classificação documental foi corrigida sem apagar o PASS do subgate.

**Lição:** o controller deve consultar o documento dono do agregado antes de transicionar o gate.

### 1.5 Request não é autorização

Um registro `AUTHORIZATION_REQUEST_NOT_AUTHORIZATION` foi corretamente separado do aceite humano, mas a proveniência de uma tentativa posterior chegou no bundle como narrativa sem uma referência de autorização independentemente verificável.

**Lição:** autoridade precisa de referência concreta; summary não cria autorização.

### 1.6 Summary sem RAW

Alguns bundles permitiram verificar coerência interna, mas não recomputar observações remotas por ausência de get-status/export/list brutos.

**Lição:** evidence-auditor deve classificar explicitamente `REPORTED` versus `RECOMPUTED`.

### 1.7 Ambiente Windows

ENV01–ENV04 mostrou que descoberta de Python/venv e aliases do Windows pode consumir rodadas antes dos gates.

**Lição:** o controller deve fazer diagnóstico ambiental barato antes de congelar uma rodada dependente daquele runtime; mudança de ambiente gera nova causal identity.

## 2. Guardrails que funcionaram e devem permanecer

- tentativas históricas imutáveis;
- freeze SHA/tree e digests;
- worktree clean;
- no force/rebase destrutivo;
- single-use authorization;
- token memory-only;
- readback por tipo/conteúdo/hash;
- `UNKNOWN` após write_started sem prova;
- reconciliação read-only antes de nova mutação;
- promoção/policy/Ready/merge separados;
- auditoria independente;
- produto e derived mirror separados;
- nenhuma promoção por inferência.

## 3. Heurísticas para o controller

1. Antes de inventar mecanismo, procurar precedente no repositório.
2. Antes de repetir transporte, consultar histórico de falhas da mesma classe.
3. Antes de marcar gate PASS, conferir todos os subgates do documento dono.
4. Antes de escrever remoto, provar destino e precondição.
5. Depois de erro remoto, observar efeito; não interpretar exit code como estado.
6. Usar um único writer e vários leitores.
7. Pedir ao usuário decisão, não execução mecânica.
8. Fazer auditoria completa em transição de gate; durante repair loop usar auditor direcionado à causa.
9. Não transportar PASS entre SHAs quando a matriz de impacto exigir nova prova.
10. Se uma correção exigir relaxar critério, parar; isso é decisão humana.

## 4. Aplicação imediata à B1

O estado vivo permanece em:

`docs/sprints/skill_enforcement_rollout/PARALELO/B1/AUTHORING_STATE.json`.

Na ativação inicial do controller, A0/A1 estão disponíveis e A2 permanece pendente. Portanto o controller pode:

- auditar e melhorar o recovery SER05;
- executar qualificação local permitida no ambiente;
- registrar commits/push/PR draft;
- fazer reconciliação remota apenas quando o envelope/ambiente a classificar dentro de A0 autorizada.

Ele não pode transformar a aprovação desta arquitetura em autorização retroativa para criar o SER05, executar probes ou Genie.
