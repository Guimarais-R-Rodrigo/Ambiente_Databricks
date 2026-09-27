# Codex Autonomous Controller Protocol

Versão: 1.9  
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

Antes de B1 material, executar `CODEX_RUNTIME_QUALIFICATION.md`. No aplicativo
Codex Desktop para Windows, aplicar também
`CODEX_DESKTOP_WINDOWS_CQ.md` e exigir o host preflight SHA-bound produzido por
`tools/codex_desktop_cq_host_preflight.ps1`.

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

Durante CQ3 existe uma exceção de qualificação estritamente rotulada nas
developer_instructions dos custom agents. `CQ3_NEGATIVE_PERMISSION_PROBE` permite
uma única tentativa-sentinela dos roles A0; `CQ3_EXECUTOR_PERMISSION_PROBES`
obriga o executor a testar negativos e o único positivo journal A1. Essa exceção
não muda permission profiles nem autoridade normal e não pode ser usada fora de
CONTROLLER_RUNTIME_QUALIFICATION. Metadata declarativa do role não substitui
enforcement comportamental.

No CQ3 Desktop, command-network é provado por `.codex/probes/cq3_executor_network_probe.ps1`, source-SHA-bound pelo host preflight v6. Antes de qualquer baseline/retry de CQ, o host executa `-SelfTest` no mesmo Windows PowerShell: três payloads sintéticos, JSON round-trip e zero network attempts. O script runtime reutiliza o IPv4:443 previamente validado no host, faz um único TCP raw BeginConnect/EndConnect e não usa DNS/HTTP/TLS/auth na sandbox. AccessDenied/10013 é denial; conexão bem-sucedida prova network boundary aberta; demais erros ficam NOT_PROVEN.

No Desktop, ausência da CLI Codex, de credenciais Git dentro da sandbox ou do
nome nominal do permission profile não é automaticamente equivalente a falha.
O contrato Desktop usa host preflight v6 para identidade e CQ0.5/CQ5 repo-side; Python roda somente no host. CQ3/CQ4 continuam provas comportamentais obrigatórias do sandbox. Quando o nome do profile não é observável, o PASS agregado exige CQ3/CQ4 e CQ5 host-bound verdes.
Estado de PR pode ficar `DEFERRED_TO_EXTERNAL_ADJUDICATION` e ser recomputado
fora da sessão.

`CODEX_DESKTOP_TOOL_SURFACE_POLICY.json` separa presença, trust, autoridade e invocação. `mcp__node_repl__*` é control-plane interno de code mode; Browser/CUA integrado e `mcp__codex_app__*` podem estar presentes sem virar transporte A1. Antes de CQ0, o hash atual dos hooks do projeto precisa estar revisado/confiado. O `external_surface_guard` bloqueia Browser/CUA, Codex-app, MCP externos/resources e web conforme a policy; qualquer superfície proibida que alcance o backend é `SECURITY_STOP`.

CQ0–CQ5 pode produzir um resultado técnico verde, mas A1 não pode promover a própria qualificação a autoridade canônica. Depois de CQ4 não há segunda escrita repo-side para registrar o resultado: `REPORTED_PASS_AWAITING_CONTROLLER_MAINTENANCE` fica somente no pacote externo de evidências, e `AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION` permanece em `blocked_by`.
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

### 3.1 Falha recuperável não é Human Gate

Dentro de A1 já autorizado, falha local determinística (teste, lint, parser,
validator, build ou commit ainda não publicado) entra em `REPAIRING`. O
controller identifica a causa, aplica um delta causal e pode repetir a
verificação dentro de `budgets.max_causal_repair_rounds_per_gate`. Não pedir
microautorização ao usuário para correção reversível que não amplia autoridade.

Distinguir:
- `RECOVERABLE_A1`: corrigir autonomamente;
- `PRECONDITION`: informar/obter a pré-condição já prevista no contrato;
- `UNKNOWN_EFFECT`: reconciliar somente por leitura; não repetir write;
- `AUTHORITY_BOUNDARY`: Human Gate.

O orçamento conta **rodadas causais**, não comandos de leitura/testes necessários
para verificar a mesma correção. `same_state_same_command_retries=0` continua
proibindo repetição cega.

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

### 6.1 Qualificação versus transporte operacional

`.codex/transport/a1_git_transport.ps1` permanece exclusivo da qualificação CQ
e continua single-shot/preflight-head-bound.

Depois que o runtime for adjudicado como qualificado e uma tarefa A1 estiver
ativa, commits normais usam exclusivamente
`.codex/transport/a1_operational_git_transport.ps1`, conforme
`docs/operations/autonomy/A1_OPERATIONAL_POLICY.json`.

O transporte operacional:
- inicializa checkpoint externo no HEAD de controle qualificado;
- permite sucessores causais sequenciais dentro dos mesmos write roots;
- valida cada delta com `check_codex_autonomy_delta.py`;
- faz fetch imediatamente antes de publicar;
- preserva commit local se push/readback falhar;
- reconcilia publicação parcial antes de qualquer nova mutação;
- nunca transforma journal em fonte de autoridade;
- para em divergência não reconciliável.

Um commit A1 válido **não invalida por si só** a qualificação do controller.
Mudança em config, envelope, hooks, rules, transportes, validators ou demais
governance roots exige `CONTROLLER_MAINTENANCE` e nova qualificação pertinente.

O primeiro checkpoint operacional ocorre **depois** da adjudicação canônica do
CQ. Como CQ4 e a própria adjudicação podem avançar a branch, o bootstrap aceita
um HEAD descendente do preflight somente quando:
- `runtime_validation=PASS` e `effective_config_observation=PASS`;
- `AUTONOMOUS_CONTROLLER_RUNTIME_VALIDATION` já foi removido por Human Gate;
- todos os control-source hashes continuam idênticos ao host evidence;
- local HEAD = remote HEAD e worktree está limpo;
- o caminho entre qualified HEAD e operational base altera somente
  journal/state/changelogs previstos na policy.

Depois disso, o checkpoint, e não o preflight HEAD, acompanha os commits de
trabalho.

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
