# Forward tests das Agent Skills

Testes de roteamento das 12 skills no Genie Code do Databricks Free — o gate
pendente da auditoria do Codex antes da replicação no trabalho.

- Método e vereditos: `.claude/skills/forward-test-skills/SKILL.md`
- Prompts prontos para colar: [roteiro.md](roteiro.md) (36 testes, 2 mensagens cada)
- Registro de rodadas: copie [template_resultados.md](template_resultados.md)
  para `resultados/<YYYY-MM-DD>_rodada<N>.md`

| Rodada | Data | PASS | FAIL | Resultado |
|---|---|---|---|---|
| 1 | 2026-08-14 | 33 | 2 | [detalhes](resultados/2026-08-14_rodada1.md) — 12/12 negativos corretos; falhas isoladas em `10P`/`11P`; `07M` sem registro |
| 2 | 2026-08-14 | 4 | 0 | [detalhes](resultados/2026-08-14_rodada2.md) — hipótese confirmada: `10P` passou só com o prompt corrigido; falta `11P-r2` (sem registro) |

**Consolidado:** 35/36 aprovados · negativos 12/12 · menções 12/12 · pendente
apenas `11P-r2` para fechar o gate. Nenhuma `description` foi alterada em
nenhuma rodada.

## O que a rodada 1 mostrou

As descriptions do pacote auditado pelo Codex estão **bem calibradas**: nenhuma
das colisões previstas (drift, materialização, deterioração, auditoria×execução)
se materializou, e em 11 dos 12 negativos o Genie ainda escolheu a skill *ideal*
do desvio. As duas falhas se concentraram nas skills que dependem de um artefato
no chat (`comentar-notebook`, `tutor-databricks`): os prompts citavam "este
notebook"/"este stack trace" sem que existissem — defeito do instrumento de
teste, corrigido com prompts v2 autocontidos. **Nenhuma `description` foi
alterada até aqui.**
