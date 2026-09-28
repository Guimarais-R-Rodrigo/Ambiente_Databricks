# ADR-0024 — Codex Autonomous Controller para execução governada

Data: 2026-09-26
Status: Aceito
Autor: ChatGPT + decisão humana explícita

## Contexto

A execução paralela governada da SER foi formalizada no ADR-0023 e provou separação útil entre autoria, certificação, auditoria, efeitos externos, promoção e integração. O piloto B1 também expôs um custo operacional: tarefas causalmente relacionadas foram repartidas em muitos handoffs ChatGPT→Codex→ChatGPT, com nova intervenção humana mesmo quando a próxima ação era puramente técnica, reversível ou read-only.

O problema não é ausência de guardrails. O repositório já possui freeze, manifests, single-shot, readback, estados de efeito, evidence bundles, auditoria independente, fail-closed e gates humanos. O problema é a granularidade da coordenação: o usuário passou a arbitrar microtransições que podem ser decididas mecanicamente dentro de um envelope previamente aprovado.

O Codex atual suporta instruções hierárquicas via `AGENTS.md`, configuração por projeto em `.codex/config.toml`, multi-agent e papéis customizados. GPT-6 Astra é apropriado para o controller e auditorias exigentes; o modelo concreto é configuração operacional, não autoridade normativa.

## Decisão

Adotar um modo opcional **Codex Autonomous Controller Mode** para frentes SER/SEF.

O modo é ativado por frente e exige três objetos separados:

1. protocolo durável: `docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md`;
2. envelope machine-readable de autoridade da frente;
3. estado factual já pertencente à campanha, por exemplo `AUTHORING_STATE.json`.

O controller pode decompor uma frente em tarefas fechadas, despachar subagentes, implementar, verificar, auditar, corrigir causalmente e avançar entre gates sem novo handoff humano enquanto todas as ações permanecerem dentro do envelope ativo.

### Autoridade por classe

- **A0 — read-only:** inspeção, testes sem efeito externo, reconciliação e auditoria. Pode ser autônoma.
- **A1 — repo-local:** autoria, testes, renderer, commits/push na branch da frente e atualização de PR draft. Pode ser autônoma quando o envelope a ativa.
- **A2 — remoto pessoal/reversível:** efeitos delimitados no Databricks Free pessoal, compute/probes, conversas Genie e cleanup de objetos próprios. Só é autônoma após ativação humana explícita no envelope.
- **A3 — autoridade humana:** mudança de `current_level`/rollout, promoção, Ready, merge, destino corporativo, dados reais, expansão material de escopo e decisão após efeito remoto irresolvido. Nunca é delegada por inferência.

### Topologia de agentes

O root thread é o **controller**. Há no máximo um agente write-capable por vez:

- explorer — read-only;
- executor — único writer de autoria repo-side;
- domain-auditor — read-only;
- evidence-auditor — read-only;
- architecture-auditor — read-only.

Subagentes não criam netos. O controller agrega resultados e decide a próxima tarefa; auditores não recebem como premissa o veredito do executor.

O “executor” Codex desta camada é diferente do executor determinístico de campanha descrito no plano SER. O primeiro pode editar autoria repo-side dentro de A1; o segundo continua executando apenas comandos congelados e não corrige a candidata durante uma certificação.

### Repair loop causal

Retry-until-green continua proibido. Uma nova rodada só pode ocorrer após mudança causal identificável: novo SHA, correção de ambiente autorizada, transporte qualificado diferente ou nova evidência que altere a precondição.

A tentativa anterior permanece imutável. Mesmo SHA + mesmo estado + mesmo comando não pode ser repetido para buscar verde.

O envelope define budgets de repair; excedê-los é Human Gate.

### Efeito remoto desconhecido

`UNKNOWN` exige reconciliação read-only antes de qualquer nova mutação. Se a reconciliação não produzir estado suficiente, parar em Human Gate. Nenhum auditor ou controller pode inferir ausência de efeito a partir de exit code ou erro de transporte.

### Um writer

Somente um agente pode modificar a árvore por vez. Explorer e auditores são read-only. O controller não edita em paralelo com o executor. Essa regra vale mesmo quando a ferramenta permitir múltiplos worktrees.

## Alternativas consideradas

- Manter micro-handoffs ChatGPT↔Codex — rejeitada pelo custo de coordenação observado no B1.
- Dar acesso irrestrito ao Codex e remover gates — rejeitada porque mistura execução técnica com autoridade de promoção/integração.
- Colocar todo o procedimento em um `AGENTS.md` grande — rejeitada porque duplicaria governança e carregaria contexto excessivo em todas as tarefas.
- Construir agora uma aplicação própria na Agents API — adiada; o Codex nativo já oferece instruções por projeto, multi-agent e sandbox suficientes para o objetivo imediato.

## Consequências

- O usuário passa a autorizar envelopes, não comandos microscópicos.
- O root controller pode consumir mais tokens, mas reduz latência humana e repetição de contexto.
- A0/A1 podem prosseguir sem novo aceite quando o envelope estiver ativo.
- A2 requer ativação explícita e limites por host/path/effect/budget.
- A3 permanece humana.
- Histórico vermelho, evidence sufficiency, freeze e single-shot continuam obrigatórios.
- `.codex/` e `.agents/` são adapters de execução; `CLAUDE.md`, ADRs e plano SER continuam fontes normativas.
- Mudança de modelo não muda autoridade.

## Referências

- `docs/decisions/ADR-0023-execucao-paralela-governada-ser.md`
- `docs/sprints/skill_enforcement_rollout/PARALELO/03_CICLO_GATES.md`
- `docs/sprints/skill_enforcement_rollout/PARALELO/09_PAPEIS_HANDOFFS.md`
- `docs/operations/CODEX_AUTONOMOUS_PROTOCOL.md`
- `docs/operations/autonomy/autonomy-envelope.schema.json`
- OpenAI Codex configuration reference: https://developers.openai.com/docs/config-file/config-reference
- OpenAI guidance for GPT-6 Astra: https://developers.openai.com/api/docs/guides/latest-model
