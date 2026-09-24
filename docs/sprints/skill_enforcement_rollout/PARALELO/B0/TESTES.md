# B0 — testes e gates

## Metatestes

`python -B -m unittest tools.tests.test_ser_parallel_b0 -v` cobre contratos fechados, registry sem shell/inline code, DAG/locks, first-failure determinístico, stop global, integridade de bundle, expansão de `unittest discover` e verificadores dos dois pilotos.

## Cobertura herdada

`python -B -m tools.skill_enforcement.parallel.coverage` deve retornar `status=PASS`, 21 steps SE08, nove etapas CI não-SEF e cinco grupos SER01. Métodos de arquivos de teste são enumerados por AST; `unittest discover` é expandido por arquivo. Assertions temporais conhecidas têm override explícito e não são convertidas em invariantes atuais.

## Pilotos

- selective: falha deliberada bloqueia apenas dependentes; frente independente continua; publicação sintética fica bloqueada.
- global: uma tarefa `GLOBAL_CAMPAIGN` falha; nenhuma nova tarefa de onda posterior pode iniciar.

A campanha normal permanece FAIL quando contém falha deliberada; apenas `pilot_verify.py` interpreta o cenário esperado como PASS do mecanismo.

## Preparação mecânica do freeze

`freeze_prepare.py` exige worktree limpa, roda o validador sem conferir snapshot, extrai `repo (identidade)`/`repo (links)`, reescreve exclusivamente as duas linhas correspondentes de `README.md` e então roda `validate_assistant.py --conferir-readme`. Qualquer outro path alterado bloqueia a preparação. O script não faz commit nem altera policy.
