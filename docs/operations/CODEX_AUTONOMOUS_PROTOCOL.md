# Codex Autonomous Controller Protocol

Versão: 1.0  
Decisão dona: ADR-0024

## 1. Objetivo

Permitir que uma sessão Codex conduza uma frente técnica por múltiplas rodadas de investigação, autoria, teste, auditoria e reparo causal sem devolver cada microdecisão ao usuário.

O controller não substitui o launcher, verifiers, manifests ou human gates. Ele coordena esses mecanismos.

## 2. Fontes e precedência

Ao iniciar uma frente:

1. obedecer instruções de sistema, plataforma e usuário;
2. ler `AGENTS.md` e `CLAUDE.md`;
3. localizar o envelope ativo da frente em `docs/operations/autonomy/`;
4. ler o arquivo de estado vivo indicado pelo envelope;
5. carregar somente os documentos donos do gate corrente;
6. tratar relatórios de executor como evidência a auditar, não como verdade canônica.

Prompt de partida não é fonte de SHA mutável. Sempre reconsultar Git/repositório.

Um `AUTHORIZATION_REQUEST` nunca é `AUTHORIZED`. Um envelope A2 só está ativo com referência humana explícita conforme schema.

## 3. State machine do controller

```text
DISCOVERING
→ PLANNING
→ IMPLEMENTING
→ LOCAL_VERIFYING
→ AUDITING
→ REPAIRING
→ EXTERNAL_RECONCILING
→ EXTERNAL_EXECUTING
→ POST_EFFECT_VERIFYING
→ GATE_ADVANCING
→ WAITING_HUMAN
→ COMPLETE
```

Saídas adicionais:

```text
BLOCKED_DESIGN
BLOCKED_ENVIRONMENT
BLOCKED_AUTHORITY
UNKNOWN_EFFECT
BUDGET_EXHAUSTED
SECURITY_STOP
EVIDENCE_INCOMPLETE
```

O estado é conclusão observável, não descrição livre.

## 4. Loop principal

### 4.1 Discover

- confirmar branch, HEAD, tree, worktree e base relevante;
- identificar gate corrente pelo estado vivo;
- identificar histórico de tentativas do mesmo gate;
- validar envelope e classe de autoridade necessária;
- identificar evidência RAW disponível e claims que só foram reportadas.

### 4.2 Plan

Construir um DAG curto da próxima rodada. Paralelizar apenas tarefas independentes. Identificar antes:

- escritor único;
- auditores necessários;
- comandos materialmente single-shot;
- precondições;
- efeito esperado;
- stop rules;
- evidence roots;
- budget causal restante.

### 4.3 Delegate

O root pode usar:

- `explorer` para investigação e histórico;
- `executor` para a única linha de escrita repo-side;
- `domain-auditor` para semântica/oráculos;
- `evidence-auditor` para autoridade/evidência/efeitos;
- `architecture-auditor` para regressão/duplicação/impacto.

Filhos não criam subagentes. O root não delega a dois writers.

### 4.4 Implement

Somente o executor escreve. Cada patch deve:

- resolver uma causa identificada;
- preservar tentativas históricas;
- evitar alterar produto fora do escopo;
- atualizar testes e documentação quando a mudança exigir;
- produzir commit identificável antes de nova certificação quando o protocolo da campanha exigir SHA imutável.

### 4.5 Verify

Executar gates determinísticos do candidato. Não usar teste como reparador. Não modificar código durante uma certificação single-shot.

Resultado parcial não vira PASS agregado.

### 4.6 Audit

Antes de avançar gate material, auditores independentes verificam o escopo aplicável. Auditor recebe artefatos primários quando disponíveis; não deve receber “confirme que passou” como tarefa.

### 4.7 Repair

Só abrir uma nova rodada se existir `causal_delta` explícito. Exemplos válidos:

- patch funcional;
- correção de fixture/teste que era defeituoso;
- ambiente alterado e autorizado;
- transporte diferente previamente qualificado;
- nova reconciliação que muda a precondição.

Não são causal delta:

- “pareceu transitório”;
- timeout maior sem diagnóstico;
- repetir o mesmo comando;
- trocar seed para obter verde;
- ignorar teste que falhou.

### 4.8 Advance

Avançar automaticamente apenas se:

- gate anterior satisfaz seus critérios;
- auditorias exigidas não têm finding material aberto;
- ação seguinte está dentro da classe ativa do envelope;
- budgets não foram excedidos;
- estado de efeito é conhecido.

Caso contrário, ir para `WAITING_HUMAN` ou blocker específico.

## 5. Classes de autoridade

### A0 — READ_ONLY

Pode incluir:

- Git/file inspection;
- parse/schema/lint;
- testes que não produzem efeito externo material;
- read-only remote status/list/export;
- auditoria e recomputação de hashes;
- investigação documental.

A0 não autoriza login/remediação de credencial, criação, compute que crie histórico, chat remoto ou escrita.

### A1 — REPO_LOCAL

Pode incluir, quando o envelope estiver ativo:

- criar/editar código e documentação na branch da frente;
- executar renderer e validadores;
- criar commits causais;
- push normal para a branch autorizada;
- atualizar draft PR e registros da frente.

A1 não autoriza:

- alterar `current_level` ou rollout;
- Ready;
- merge;
- escrita em workspace externo.

### A2 — PERSONAL_REMOTE_REVERSIBLE

Somente se explicitamente ativada no envelope. Pode incluir subconjunto declarado de:

- objetos temporários SHA-bound no Databricks Free pessoal;
- compute/probes com dados sintéticos;
- conversas Genie congeladas;
- cleanup apenas de objetos criados pelo próprio envelope;
- publicação de pacote apenas se expressamente listada.

Cada efeito precisa de host, namespace, precondição, limite de tentativas e verificação pós-efeito no envelope. A2 não cruza para destino corporativo.

### A3 — HUMAN_ONLY

Sempre parar para:

- `current_level` / `target_level` material ou `rollout_mode` quando representar promoção;
- promoção de policy;
- Ready;
- merge;
- workspace corporativo;
- dados reais/corporativos;
- expansão material de escopo/estimando;
- nova classe de efeito não listada;
- relaxamento de cobertura/guardrail;
- `UNKNOWN_EFFECT` não resolvido;
- alteração destrutiva fora de cleanup explicitamente delegado.

## 6. Single-writer e concorrência

O máximo de subagentes vem do envelope/config, mas:

```text
MAX_WRITE_CAPABLE_AGENTS = 1
```

Enquanto o executor escreve:

- root não edita os mesmos arquivos;
- auditores e explorer permanecem read-only;
- nenhum segundo executor é criado;
- filhos não criam netos.

Investigações e auditorias independentes podem rodar em paralelo.

## 7. Causal repair budget

O envelope define pelo menos:

- `max_causal_repair_rounds_per_gate`;
- `max_hypotheses_per_root_cause`;
- `same_state_same_command_retries` — deve ser 0;
- `max_unknown_effects_before_human`;
- `max_concurrent_subagents`;
- `max_write_capable_agents` — deve ser 1.

Ao consumir budget, registrar tentativa e causal delta. Budget esgotado => `BUDGET_EXHAUSTED`, não reduzir testes.

## 8. Efeitos remotos e UNKNOWN

Antes de efeito A2:

1. validar envelope ativo;
2. validar destino;
3. validar precondições;
4. congelar conteúdo/digest;
5. reservar evidência;
6. executar no máximo a tentativa permitida.

Depois:

1. readback;
2. classificar `CREATED/UPDATED/ALREADY_CORRECT/NONE/UNKNOWN`;
3. preservar saída literal;
4. executar verificação pós-efeito prevista.

Se processo falhar depois de `write_started`, não inferir ausência. Marcar `UNKNOWN` até reconciliação.

Uma reconciliação read-only pode ocorrer se já autorizada pelo envelope. Nova mutação só após estado suficiente e causal delta.

## 9. Evidência

Hierarquia de força:

1. bytes RAW / resposta literal / estado remoto observado;
2. hashes rederiváveis;
3. verifier independente;
4. summary estruturado;
5. narrativa do executor.

Narrativa nunca substitui RAW quando o claim exige RAW.

Evidence bundle compartilhável deve aplicar secret/path hygiene. Não persistir tokens.

## 10. Human Gates

O controller para com um pacote de decisão curto contendo:

- estado observado;
- evidência suficiente e lacunas;
- decisão pedida;
- delta exato que a decisão autoriza;
- riscos/rollback;
- o que continuará proibido.

Não pedir autorização para A0/A1 já ativas.

## 11. Comunicação

Atualizações durante execução devem ser event-driven:

- finding material;
- mudança causal;
- passagem de gate;
- Human Gate;
- blocker.

Não narrar cada comando.

## 12. Encerramento

Uma frente autônoma termina somente em:

- Human Gate explícito;
- COMPLETE;
- blocker que não pode ser resolvido no envelope;
- budget esgotado;
- segurança/evidência insuficiente.

Ao encerrar, atualizar estado/changelog conforme A1 e deixar worktree limpo quando aplicável.
