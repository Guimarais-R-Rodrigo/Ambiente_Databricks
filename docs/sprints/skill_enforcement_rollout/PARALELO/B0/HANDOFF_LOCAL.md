# B0 — handoff local fechado

Este documento é operacional e não concede autoridade de release, promoção, Ready ou merge.

## 1. Identidade obrigatória

Repositório:

`Guimarais-R-Rodrigo/Ambiente_Databricks`

Branch:

`ser/B0-parallel-rollout-framework`

PR:

`#113`

O SHA executável é **exatamente o HEAD da PR #113 indicado no corpo da própria PR no momento do handoff**. Antes de qualquer comando:

```bash
git fetch --all --prune
git checkout ser/B0-parallel-rollout-framework
git rev-parse HEAD
git rev-parse HEAD^{tree}
git merge-base HEAD origin/main
git status --porcelain=v1 --untracked-files=all
git rev-parse --is-shallow-repository
```

Parar se:

- HEAD divergir do `CURRENT_HEAD` publicado na PR;
- merge-base divergir da base publicada;
- worktree não estiver limpa;
- repositório for shallow;
- branch estiver behind de `main`;
- qualquer correção funcional parecer necessária.

O executor não altera código, testes, schemas, JSONs, documentação, timeouts ou policy.

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

A suíte contém 72 métodos definidos estaticamente na autoria atual. A coleta real do checkout é a autoridade para a execução; não ajustar o esperado localmente.

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

Depois da inspeção mecânica, criar **um único commit de freeze**, sem alteração funcional adicional.

O commit de freeze cria um novo SHA. A partir desse ponto, toda evidência pertence ao SHA de freeze, não ao SHA de autoria anterior.

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

- SHA/tree/base/branch da rodada;
- `ROUND_START.json`;
- `RELEASE_SPEC.json`;
- stdout/stderr + records dos release gates;
- `coverage.json`;
- `host.json`;
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

Mesmo com gates funcionais verdes, registrar separadamente:

```text
WINDOWS_JOB_OBJECT_PROOF
NTFS_QUALIFICATION
SANDBOX_NEGATIVE_PERMISSIONS
HOST_RESOURCE_HEADROOM
```

Se uma dessas dimensões não tiver sido efetivamente observada, usar estado pendente correspondente.

Não converter ausência de prova em PASS.

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
- fazer merge.

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
