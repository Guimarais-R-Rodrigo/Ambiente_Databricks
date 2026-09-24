# B0 — mecanismo comum da execução paralela SER

Estado de autoria: **AUDIT_CORRECTIVE_V3 / FULL_CHECKOUT_VALIDATION_PENDING / LOCAL_QUALIFICATION_PENDING**.

B0 implementa apenas a infraestrutura local comum. Não promove skill, não altera `policy.json`, não publica no Databricks e não autoriza SER02–SER14. O executor B0 opera o repositório em `READ_ONLY`; preparação mecânica de renderer/snapshot permanece serial e fora dos workers.

A auditoria independente da candidata `f803b50f898ac93eb0e5541ba428a3656dc4f732` encontrou AUD-01–AUD-12. A linha V3 implementa as correções repo-side materiais: contratos fechados de command record/result/task/campaign; resultado nulo e NA obrigatório fail-closed; causalidade/intervalos verificados; scan SHARE recalculado sobre bytes e nomes finais; paths reservados e symlinks recusados; coleta unittest real; identidade única de rodada por SHA/tree/base/release-spec; verificação final externa; lease host-wide conservador; supervisão POSIX por process group e Windows por Job Object com launcher bloqueado até a atribuição ao job; preflight barato de JSON/Python/schemas/templates.

A suíte versionada contém **72 métodos**. Essa contagem é estática do arquivo e ainda não é PASS de checkout. O histórico de 39/39 e a antiga contagem de 52 pertencem a candidatas anteriores e não são transportados.

Permanecem necessariamente pendentes de host: prova Windows/Job Object, NTFS, sandbox/permissões negativas e headroom de CPU/RAM/IO. Também permanecem deliberadamente P2 até o piloto medido: despacho ao liberar slot, cache de inventory por digest e tuning 2/1 versus 3/2.

Antes do freeze, o checkout real deve passar, nesta ordem:

```bash
python -B -m tools.skill_enforcement.parallel.preflight
python -B -m unittest tools.tests.test_ser_parallel_b0 -v
python -B -m tools.skill_enforcement.parallel.coverage
```

O roteiro operacional fechado está em [`HANDOFF_LOCAL.md`](HANDOFF_LOCAL.md). Ele é a fonte do executor para stop rules, comandos, evidências de retorno e ações proibidas.\n\nSomente se os três gates forem verdes, a preparação mecânica executa `python -B -m tools.skill_enforcement.parallel.freeze_prepare --apply`, altera exclusivamente o snapshot medido de `README.md`, e o operador cria o commit de freeze após inspecionar o diff. A qualificação então roda uma única vez com `python -B -m tools.skill_enforcement.parallel.b0_release --output-dir <DIR_EXTERNO_NOVO>`.

O `b0_release` V3 fixa `ROUND_START` e `RELEASE_SPEC`, reconfirma identidade entre gates, reabre campanha/summary/logs persistidos para verificação independente e emite um `RELEASE_VERDICT` externo ligado aos hashes do mecanismo, RAW, SHARE, binding e envelope. Um PASS funcional com host/sandbox não provados não autoriza campanha real nem promoção.
