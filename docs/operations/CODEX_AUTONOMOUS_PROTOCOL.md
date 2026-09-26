# Codex Autonomous Controller Protocol

Versão: 1.3  
Decisões donas: ADR-0024 + ADR-0025

## 1. Objetivo

Permitir que uma sessão Codex conduza investigação, autoria A1, teste, auditoria e
repair causal sem devolver microdecisões ao usuário, preservando autoridade humana
para decisões materiais.

## 2. Fontes e precedência

Ao iniciar uma frente:

1. obedecer sistema/plataforma/usuário;
2. ler `AGENTS.md` e `CLAUDE.md`;
3. localizar o envelope ativo;
4. ler o state source apontado pelo envelope;
5. aplicar: live state > índices correntes > contrato do gate > histórico;
6. carregar somente documentos donos do gate;
7. tratar reports como evidência a auditar;
8. consultar `CHANGELOG.md` apenas por busca/tail quando necessário.

Prompt não é fonte de SHA mutável. `AUTHORIZATION_REQUEST` nunca é autorização.
A2 exige referência humana explícita + contrato válido.

## 2.1 Runtime qualification e bootstrap de autoridade

Antes de B1 material, executar `CODEX_RUNTIME_QUALIFICATION.md`.

AC-R2 usa permission profiles:
- no Windows elevado, A0 e A1 declaram `:root=read` porque o backend atual
  exige leitura efetiva da raiz; esta é uma ampliação de leitura observada e
  documentada, não uma autorização de write;
- root + explorer/auditors: `ser-controller-a0`, repository read-only para
  mutações, command network disabled, com scratch externo explícito
  `~\codex-scratch\Ambiente_Databricks` para capability/write temporário no
  Windows nativo;
- executor: `ser-b1-a1`, workspace default read, somente 10 arquivos A1 concretos
  writable, sem escrita direta em `.git` e sem command network;
- `sandbox_mode` legado é incompatível com esse target.

Configuração declarada não prova configuração efetiva. Parent/live overrides,
project trust, Windows sandbox e MCP/hosted surfaces precisam ser observados.

CQ0–CQ5 pode produzir um resultado técnico verde, mas A1 não pode promover a
própria qualificação a autoridade canônica. Quando CQ passar, A1 pode registrar:

`REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE`

e deve manter `AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION` em `blocked_by`.
A remoção desse blocker e o estado canônico `PASS` exigem o Human Gate já
existente `CONTROLLER_MAINTENANCE`. Não é um novo gate.

## 3. Loop

```text
DISCOVERING -> PLANNING -> IMPLEMENTING -> LOCAL_VERIFYING -> AUDITING
-> REPAIRING -> GATE_ADVANCING -> WAITING_HUMAN | COMPLETE
```

Também são saídas válidas:
`BLOCKED_DESIGN`, `BLOCKED_ENVIRONMENT`, `BLOCKED_AUTHORITY`,
`UNKNOWN_EFFECT`, `BUDGET_EXHAUSTED`, `SECURITY_STOP`,
`EVIDENCE_INCOMPLETE`.

Retry-until-green é proibido. Nova rodada exige causal delta identificável.

## 4. Papéis

- root controller — coordena; repository read-only;
- explorer — read-only;
- executor — único writer A1;
- domain-auditor — read-only;
- evidence-auditor — read-only;
- architecture-auditor — read-only, somente quando estrutural.

Filhos não criam filhos. Cinco definições não significam cinco agentes ativos.
Normalmente usar 0–2 subagentes e escalar por causa.

## 5. Autoridade

### A0 — READ_ONLY

Inspeção, análise estática, testes sem efeito externo material, auditoria,
recomputação e reconciliação remota somente quando o contrato já permitir.

### A1 — REPO_LOCAL

Somente paths exatos de `repo_scope.write_roots`. Não inclui controller
governance, produto, policy, evidência histórica, outras frentes, `.git` direto
ou command network direto.

### A2 — PERSONAL_REMOTE_REVERSIBLE

Permanece inativa até ativação humana explícita e contrato completo.

### A3 — HUMAN_ONLY

Inclui promoção/current_level/rollout, Ready, merge, corporativo, dados reais,
mudança material de escopo/estimand, relaxamento de guardrail e UNKNOWN irresolvido.

## 6. A1 filesystem e Git

A barreira primária é o permission profile, não hooks.

O executor pode alterar apenas os arquivos concretos do envelope. O journal
`B1/AUTONOMY/JOURNAL.jsonl` e changelogs são append-only. O delta checker
reprova escrita fora de A1, origem/destino de rename indevido, delete protegido,
symlink, reescrita de histórico e transição inválida do live state.

O executor não escreve `.git` e não possui command network. Commit/push usam
exclusivamente:

```text
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File .codex\transport\a1_git_transport.ps1
```

via regra project-scoped `decision="prompt"`. Somente o executor mantém
`approval_policy.granular.rules=true` e `approvals_reviewer=auto_review`;
sandbox escalation, request_permissions, MCP elicitations e skill approval são
fail-closed. Não há override local de `[auto_review].policy`: o projeto não
substitui a política padrão do reviewer.

O transportador protegido:
- aceita zero argumentos;
- verifica Git root, branch e remote exatos;
- confronta a lista de paths com o envelope;
- valida worktree e index antes do commit;
- faz commit normal;
- revalida o commit;
- exige worktree limpo;
- faz push non-force somente para a branch B1 esperada.

MCP/apps/hosted GitHub APIs não são transporte A1 de escrita.

## 7. State integrity

`AUTHORING_STATE.json` é estado vivo, não prova de si próprio.

O scratch externo A0 não é evidence root nem autoridade do projeto. Ele existe
somente para execução determinística temporária e nunca substitui o worktree.

A proteção de least privilege material deste backend está nos efeitos:
filesystem write, network e transportes remotos permanecem restritos. O
controller pode ler mais filesystem do que o ideal no Windows elevado; qualquer
tentativa futura de voltar a uma leitura mais estreita exige nova qualificação do
backend e não pode ser inferida deste contrato.

A1 não pode:
- alterar Human Gates;
- alterar autoridade do controller;
- escrever `PASS` canônico para runtime qualification;
- remover o blocker de runtime qualification;
- tornar `launchable=true` mantendo blockers;
- reescrever tentativa/histórico append-only.

Demais remoções de blocker precisam satisfazer invariantes determinísticos
definidos no checker.

## 8. Evidência, efeitos e UNKNOWN

Força de evidência:
1. RAW/estado observado;
2. hashes rederiváveis;
3. verifier independente;
4. summary estruturado;
5. narrativa.

Após possível write remoto com resultado incerto: `UNKNOWN` até reconciliação.
Não repetir a mesma operação no mesmo estado.

## 9. Human Gates

O pacote de gate deve conter estado observado, o que foi/não foi provado,
autoridade pedida, efeitos, riscos/rollback e o que permanece proibido.

Auto-review é aprovação técnica de uma categoria permitida; nunca equivale a
A2/A3/`CONTROLLER_MAINTENANCE`.

## 10. Encerramento

A frente termina em Human Gate, COMPLETE, blocker, budget esgotado ou limite de
segurança/evidência. Nenhum PASS técnico implica promoção, Ready ou merge.
