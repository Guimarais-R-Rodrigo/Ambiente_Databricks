# B0 — handoff local fechado

Este documento é operacional e não concede autoridade de release, promoção, Ready ou merge.

## 1. Bootstrap isolado e identidade obrigatória

Repositório:

`Guimarais-R-Rodrigo/Ambiente_Databricks`

Branch remota fonte:

`origin/ser/B0-parallel-rollout-framework`

PR:

`#113`

O checkout em que o operador/Codex foi iniciado **não precisa estar limpo nem na branch B0**. Mudanças locais preexistentes pertencem a outra frente e devem ser preservadas. Elas não são motivo para tentar `checkout`, `stash`, `reset` ou limpeza.

### 1.1 No checkout já existente

Executar apenas operações read-only/fetch:

```bash
git fetch --all --prune
git rev-parse --show-toplevel
git rev-parse refs/remotes/origin/ser/B0-parallel-rollout-framework
git rev-parse origin/main
```

O SHA de `refs/remotes/origin/ser/B0-parallel-rollout-framework` deve ser **exatamente o `CURRENT_HEAD` publicado no corpo da PR #113 no momento do handoff**.

Se divergir, PARE com:

```text
B0_LOCAL_HANDOFF = BLOCKED_ENVIRONMENT_REMOTE_HEAD_DIVERGED
```

Não tente atualizar o esperado localmente.

### 1.2 Criar worktree dedicado

Escolher um path externo, curto, novo e vazio, por exemplo:

`C:\b0_worktrees\b0_<shortsha>`

Criar o worktree **destacado no SHA exato**:

```bash
git worktree add --detach <B0_WORKTREE_NOVO> <CURRENT_HEAD_EXATO>
```

Não reutilizar worktree anterior.

Entrar em `<B0_WORKTREE_NOVO>` e executar:

```bash
git rev-parse HEAD
git rev-parse HEAD^{tree}
git merge-base HEAD origin/main
git status --porcelain=v1 --untracked-files=all
git rev-parse --is-shallow-repository
git rev-list --left-right --count origin/main...HEAD
```

Condições obrigatórias:

- HEAD = `CURRENT_HEAD` publicado na PR;
- merge-base = base/merge-base publicado na PR;
- worktree dedicado = limpo;
- shallow = `false`;
- behind = `0`.

O estado do **checkout original** é apenas registrado para rastreabilidade e não bloqueia a rodada. Ele não deve ser modificado.

Parar se qualquer condição do **worktree dedicado** divergir ou se qualquer correção funcional parecer necessária.

O executor não altera código, testes, schemas, JSONs, documentação, timeouts ou policy antes do freeze mecânico autorizado.

## 2. Gate de autoria no checkout real

Executar em ordem e sem retry:

```bash
python -B -m tools.skill_enforcement.parallel.preflight
python -B -m unittest tools.tests.test_ser_parallel_b0 -v
python -B -m tools.skill_enforcement.parallel.coverage
```

Condições para continuar:

```text
AUTHORING_PREFLIGHT = PASS
B0_METATESTS = PASS
COVERAGE_V3.status = PASS
```

A suíte contém 82 métodos definidos estaticamente na autoria atual. A coleta real do checkout é a autoridade para a execução; não ajustar o esperado localmente.

Se qualquer comando falhar:

1. não editar;
2. não repetir;
3. preservar stdout/stderr completos;
4. registrar exit code;
5. registrar HEAD/tree/merge-base/status;
6. retornar a evidência à autoria repo-side.

## 3. Preparação mecânica do freeze

Somente após os três gates anteriores passarem:

```bash
python -B -m tools.skill_enforcement.parallel.freeze_prepare --apply
git status --porcelain=v1 --untracked-files=all
git diff -- README.md
```

O único delta permitido é `README.md`, limitado ao snapshot medido.

Qualquer outro path alterado é STOP.

Reexecutar a conferência do snapshot conforme saída do próprio `freeze_prepare`.

Depois da inspeção mecânica, transformar o worktree destacado em uma branch local temporária e criar **um único commit de freeze**, sem alteração funcional adicional:

```bash
git switch -c b0-local-freeze-<shortsha>
```

Se `freeze_prepare` alterou exclusivamente `README.md`:

```bash
git add -- README.md
git commit -m "SER B0: freeze candidate after local authoring gates"
```

Se `freeze_prepare` reportou `changed=false` e o worktree continua totalmente limpo, criar um marcador de freeze vazio:

```bash
git commit --allow-empty -m "SER B0: freeze candidate after local authoring gates"
```

O commit vazio é permitido somente nesse caso e deve ter a mesma tree da autoria. Qualquer outro delta continua sendo STOP.

Antes de publicar o freeze, reconfirmar que a branch remota B0 ainda aponta para o SHA de autoria original:

```bash
git fetch origin --prune
git rev-parse refs/remotes/origin/ser/B0-parallel-rollout-framework
```

Se o remoto tiver mudado, PARE com `BLOCKED_ENVIRONMENT_REMOTE_HEAD_DIVERGED_BEFORE_FREEZE_PUSH`.

Se continuar idêntico, publicar **somente** o commit mecânico de freeze por fast-forward normal:

```bash
git push origin HEAD:ser/B0-parallel-rollout-framework
```

É proibido `--force`, `--force-with-lease`, rebase, amend ou push de qualquer outro delta.

O commit de freeze cria um novo SHA e passa a ser o HEAD da PR. A partir desse ponto, toda evidência pertence ao SHA de freeze, não ao SHA de autoria anterior.

## 4. Rodada única de qualificação B0

Escolher um diretório externo novo, curto e exclusivo da rodada.

Exemplo conceitual:

`C:\b0_evidence\<round>`

Não reutilizar diretório existente.

Executar uma única vez:

```bash
python -B -m tools.skill_enforcement.parallel.b0_release --output-dir <DIR_EXTERNO_NOVO>
```

Não rodar novamente para obter verde.

O release driver executa internamente:

1. captura `ROUND_START`;
2. preflight de autoria;
3. metatestes B0;
4. coverage V3;
5. host probe;
6. construção de `RELEASE_SPEC`;
7. piloto selective;
8. verificação independente dos artefatos persistidos;
9. piloto global;
10. verificação independente dos artefatos persistidos;
11. reconfirmação final da identidade;
12. RAW/SHARE;
13. scan SHARE independente;
14. envelope verification;
15. `RELEASE_VERDICT` externo.

## 5. Semântica esperada dos pilotos

Selective:

```text
pilot.alpha.pass = PASS
pilot.beta.fail = FAIL
pilot.beta.dependent = BLOCKED_DEPENDENCY
pilot.gamma.independent = PASS
pilot.publication.blocked = BLOCKED_DEPENDENCY
normal campaign status = FAIL
launcher exit = 1
pilot mechanism verdict = PASS
```

Global:

```text
pilot.global.arm = PASS
pilot.global.fail = FAIL
pilot.global.anchor = PASS
pilot.global.must_not_start = BLOCKED_GLOBAL_STOP
pilot.global.integrator = BLOCKED_GLOBAL_STOP
normal campaign status = FAIL
launcher exit = 1
pilot mechanism verdict = PASS
```

A falha deliberada do piloto não é falha do mecanismo quando o oráculo independente confirma exatamente a topologia esperada.

## 6. Artefatos obrigatórios de retorno

Preservar e retornar, sem editar:

- estado do checkout original (somente observação; não alterado);
- SHA/tree/base do worktree dedicado;
- SHA remoto da branch antes e depois do freeze;
- SHA/tree/base/branch local da rodada;
- `ROUND_START.json`;
- `RELEASE_SPEC.json`;
- stdout/stderr + records dos release gates;
- `coverage.json`;
- `host.json`;
- `sandbox_probe.json`;
- `HOST_QUALIFICATION.json`;
- campanhas prepared;
- evidence roots dos dois pilotos;
- summaries dos pilotos;
- independent verifications;
- pilot verifications;
- `MECHANISM_RESULT.json`;
- RAW `MANIFEST.json`;
- SHARE completo + `MANIFEST.json`;
- `RAW_SHARE_BINDING.json`;
- `ENVELOPE_VERIFICATION.json`;
- `RELEASE_VERDICT.json`.

Não reconstruir manualmente arquivo faltante.

## 7. Provas ambientais que não podem ser inferidas

A rodada atual deve produzir `HOST_QUALIFICATION.json`. Para `LOCAL_QUALIFIED`, exigir:

```text
HOST_QUALIFICATION.status = PASS
filesystem_ntfs_or_not_windows = true
sandbox_negative_probe = true
windows_job_object = true
resource_observation_complete = true
initial_parallelism_2_1_observed = true
```

O probe negativo do sandbox deve provar scratch write permitido, escrita externa bloqueada, subprocesso bloqueado, rede bloqueada e credencial sentinela ausente. O filesystem Windows deve ser observado como NTFS. CPU/memória/disco precisam ser efetivamente medidos, e os próprios pilotos devem mostrar overlap de duas tasks.

`post_pilot_candidate_3_2` deve continuar `NOT_QUALIFIED_REQUIRES_SEPARATE_HEADROOM_MEASUREMENT`. Não converter a prova do perfil inicial 2/1 em autorização para 3/2.

O sandbox qualificado aqui é o sandbox Python audit-hook das tasks Python allowlisted do B0; não alegar sandbox genérico de SO.

## 8. Paralelismo autorizado no B0

`max_parallel` é o total de tasks simultâneas, incluindo auditores.

`max_auditors` é um subconjunto desse total.

O B0 usa lease host-wide conservador: uma campanha/launcher por host.

Múltiplos launchers concorrentes no mesmo host não estão autorizados.

Não aumentar 2/1 para 3/2 durante a rodada.

Dispatch por slot liberado, cache de inventory e tuning de concorrência permanecem fora desta qualificação.

## 9. Ações proibidas

Durante o handoff não:

- editar candidata;
- editar testes;
- editar fixtures;
- editar schemas;
- editar policy;
- alterar timeouts;
- instalar dependência para fazer teste passar;
- usar shell/comando fora da allowlist para substituir gate;
- fazer retry-until-green;
- apagar evidência vermelha;
- mover membro de campanha para ocultar FAIL;
- executar Databricks;
- publicar;
- marcar PR Ready;
- fazer merge;
- stash/reset/clean no checkout original;
- force push ou force-with-lease.

## 10. Resultado do handoff

Um dos estados abaixo deve ser devolvido literalmente:

```text
B0_LOCAL_HANDOFF = PASS_EVIDENCE_RETURNED
```

ou

```text
B0_LOCAL_HANDOFF = FAIL_STOPPED_AT_<GATE>
```

ou

```text
B0_LOCAL_HANDOFF = BLOCKED_ENVIRONMENT_<REASON>
```

Mesmo `PASS_EVIDENCE_RETURNED` não autoriza merge ou campanha real. A evidência retorna para auditoria/revisão B0 e gate humano posterior.
