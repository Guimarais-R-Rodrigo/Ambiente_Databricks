# B0 — testes e gates

## Metatestes

`python -B -m unittest tools.tests.test_ser_parallel_b0 -v` contém **69 testes** após a corretiva adversarial. A suíte cobre contratos fechados, allowlist exata do registry, DAG/locks, first-failure determinístico, stop global, integridade e binding de command records, limites por onda, bytes RAW, envelope RAW/SHARE não circular, secret scan fail-closed, expansão de `unittest discover`, cobertura command-only explícita e verificadores dos dois pilotos.

Na autoria corretiva foram executados isoladamente os 65 testes que não dependem da árvore documental completa: **65/65 PASS**. Os quatro `DocumentationContractTests` não são contabilizados como executados fora do checkout completo. O gate anterior de 39/39 pertence à candidata pré-revisão e continua apenas como evidência histórica.

## Regressões adversariais obrigatórias

A suíte deve rejeitar, no mínimo:

- dependente executado depois de predecessor falho;
- tarefa iniciada em onda posterior a `GLOBAL_CAMPAIGN` FAIL;
- `task_id`, task SHA, result SHA ou effect sem binding;
- status não terminal, `PASS` com issues, comando/argv não vinculado;
- estouro de `max_parallel`, `max_auditors`, resource limit ou `exclusivity_key`;
- executable, módulo Python, script ou shell absoluto fora da allowlist B0;
- pilot summary cuja verificação embutida falhe ou diverja da verificação independente;
- integrador declarado bloqueado mas com `command_records`;
- cenário de piloto desconhecido, topologia/wave/role/blocker divergente;
- manifesto aninhado adulterado, arquivo extra ou symlink;
- binding RAW/SHARE que não corresponda aos manifestos internos finais;
- SHARE com arquivo não examinável retornando scan PASS;
- normalização de CRLF/bytes RAW ou colisão de nomes de evidência;
- cobertura vazia marcada `MAPPED` sem exceção command-only explícita.

## Cobertura herdada

`python -B -m tools.skill_enforcement.parallel.coverage` deve retornar `status=PASS`, 21 steps SE08, nove etapas CI não-SEF e cinco grupos SER01. Métodos de arquivos de teste são enumerados por AST; `unittest discover` é expandido por arquivo. Assertions temporais conhecidas têm override explícito e não são convertidas em invariantes atuais.

Uma entrada sem métodos só recebe `mapping_status=MAPPED` se seu ID estiver no catálogo fechado `command_only_steps`, com `mapping_kind=COMMAND_INVARIANT`. Override command-only não observado na árvore é erro; portanto a exceção não pode virar uma lista stale de dispensa.

## Pilotos

- selective: duas raízes na onda 0; a falha deliberada `pilot.beta.fail` bloqueia sua cadeia, enquanto a frente independente continua; o integrador/publicação sintético fica bloqueado e não possui command record;
- global: `pilot.global.fail` falha na onda 1 com `GLOBAL_CAMPAIGN`; tarefa já iniciada na mesma onda pode terminar, mas nenhuma tarefa da onda posterior pode iniciar.

A campanha normal permanece FAIL porque os pilotos contêm falhas deliberadas. `b0_release.py` exige `exit_code=1` do launcher e depois executa o verificador do piloto, que rederiva a integridade da campanha a partir do campaign manifest, resultados e bytes persistidos. Qualquer outro exit code ou divergência bloqueia a qualificação.

## Evidência RAW/SHARE

O qualificador B0 persiste stdout/stderr RAW como bytes, fecha `RAW/MANIFEST.json`, cria SHARE sanitizado sem alterar o RAW, fecha `SHARE/MANIFEST.json`, escreve `RAW_SHARE_BINDING.json` fora de ambas as identidades e fecha o `MANIFEST.json` do envelope. O verificador recalcula os três manifestos e os hashes do binding. Binário não examinável no SHARE é finding, não PASS silencioso.

## Preparação mecânica do freeze

`freeze_prepare.py` exige worktree limpa, roda o validador sem conferir snapshot, extrai `repo (identidade)`/`repo (links)`, reescreve exclusivamente as duas linhas correspondentes de `README.md` e então roda `validate_assistant.py --conferir-readme`. Qualquer outro path alterado bloqueia a preparação. O script não faz commit nem altera policy.
