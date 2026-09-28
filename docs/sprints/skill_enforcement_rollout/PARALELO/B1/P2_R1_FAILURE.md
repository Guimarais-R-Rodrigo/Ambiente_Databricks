# P2 R1 — falha de bootstrap antes da execução Python

## Identidade

- candidate SHA: `3149ff684d31dbbb31c870faaeb1b50253a34520`
- candidate tree: `3f0e5c61d38d7c39c1f3b74853ffaf2520c2e156`
- main/merge-base: `4ba7f551767d847381df1556ed937116258fa77d`
- branch: `ser/B1-ser03-ser05-authoring`
- host observado pelo executor: Windows 10.0.26200 / NTFS
- worktree inicial/final: clean

## Resultado observado

O primeiro comando formal instruído para P2-01 era:

`python -B -m tools.skill_enforcement.real_campaigns.b1.preflight`

O shell não resolveu o executável literal `python`. Nenhum processo Python foi iniciado e, por fail-fast, P2-02 a P2-05 ficaram NOT_RUN.

```text
P2_LOCAL_QUALIFICATION = FAIL
FIRST_NEW_FAILURE = P2_01_PREFLIGHT / PYTHON_COMMAND_NOT_FOUND
P2_01_PROCESS_STARTED = false
P2_02 = NOT_RUN
P2_03 = NOT_RUN
P2_04 = NOT_RUN
P2_05 = NOT_RUN
```

Não houve mudança de policy, B0, SER03/SER05, Ready ou merge.

## Classificação independente

A falha não exercitou preflight, campaign adapter, B0 scheduler/verifier ou código funcional das skills.

Classificação:

```text
CANDIDATE_DOMAIN_DEFECT = false
TREE_REGRESSION = false
HISTORICAL_DEBT = false
ENVIRONMENT_ALIAS_ABSENT = true
HANDOFF_BOOTSTRAP_DEFECT = true
```

O erro do handoff foi assumir que o alias de shell `python` existia antes de o release spec poder congelar `sys.executable`.

A rodada R1 permanece FAIL e não deve ser reexecutada ou reinterpretada.

## Corretiva autorizada para uma rodada sucessora

Uma nova candidata P2 deve resolver Python 3 em uma etapa **pré-gate**, somente ambiental, antes de P2-01. O resolver deve retornar o caminho real de `sys.executable`; os gates formais subsequentes usam esse caminho exato.

Descoberta do interpretador não é P2-01 e não transforma R1 em PASS. A próxima execução é uma nova rodada sobre novo SHA.
