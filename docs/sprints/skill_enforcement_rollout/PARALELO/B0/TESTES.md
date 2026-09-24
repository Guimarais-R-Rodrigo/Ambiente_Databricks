# B0 — testes e gates

## Metatestes

`python -B -m unittest tools.tests.test_ser_parallel_b0 -v` contém **52 métodos** na candidata corretiva.

Os 39 testes originais permanecem como regressão histórica do B0. Treze regressões adicionais travam os achados RV-01–RV-07 e fragilidades adjacentes: allowlist exata, dependência/global stop reconstruídos, bindings de task/SHA/effect/command/log, limites por onda, manifesto aninhado, RAW/SHARE final, binário não examinável, bytes CRLF e composição do gate de piloto.

A autoria corretiva executou 9 reproduções adversariais isoladas sobre os módulos críticos, todas PASS após a correção. Isso não substitui a execução dos 52 métodos no checkout real.

## Cobertura herdada

`python -B -m tools.skill_enforcement.parallel.coverage` deve retornar `status=PASS`, 21 steps SE08, nove etapas CI não-SEF e cinco grupos SER01.

O inventário distingue:
- `MAPPED`: comando de teste com métodos enumerados por AST;
- `COMMAND_ONLY`: validador/probe executável que não é suíte unittest;
- `EMPTY_METHOD_MAP`: erro bloqueante quando um comando esperado como teste resolve para arquivo(s) sem métodos.

`unittest discover` é expandido por arquivo. Assertions temporais conhecidas têm override explícito e não são convertidas em invariantes atuais.

## Pilotos

- selective: falha deliberada bloqueia apenas dependentes; frente independente continua; integrador/publicação sintética fica bloqueado.
- global: uma tarefa `GLOBAL_CAMPAIGN` falha; nenhuma nova tarefa de onda posterior, inclusive integrador, pode iniciar.

A campanha normal permanece FAIL quando contém falha deliberada. `pilot_verify.py` somente classifica o mecanismo como PASS quando `summary.verification.valid=true`, o conjunto/topologia de resultados coincide exatamente e o launcher termina com exit code deliberado `1`.

## Evidência

`process.py` persiste stdout/stderr como bytes e calcula SHA-256 sobre esses mesmos bytes.

O manifesto exclui apenas o `MANIFEST.json` raiz; manifestos aninhados são conteúdo normal e ficam cobertos.

RAW e SHARE possuem manifestos finais independentes. O binding é arquivo irmão externo aos dois roots, eliminando circularidade. SHARE adiciona metadata própria para identidade distinta. Arquivo não UTF-8 é copiado byte a byte, mas torna `secret_scan=FAIL` por não ter sido examinável.

## Preparação mecânica do freeze

`freeze_prepare.py` exige worktree limpa, roda o validador sem conferir snapshot, extrai `repo (identidade)`/`repo (links)`, reescreve exclusivamente as duas linhas correspondentes de `README.md` e então roda `validate_assistant.py --conferir-readme`. Qualquer outro path alterado bloqueia a preparação. O script não faz commit nem altera policy.
