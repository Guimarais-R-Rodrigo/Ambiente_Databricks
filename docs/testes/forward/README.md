# Forward tests das Agent Skills

Quando você escreve um pedido no Genie Code, ele decide sozinho qual skill
carregar — lendo apenas o campo `description` de cada uma, nunca o corpo. Esse
mecanismo é o **roteamento**, e é onde mora a falha mais silenciosa do
ecossistema: descrições parecidas fazem o assistente carregar a skill errada, e
a resposta vem plausível o bastante para ninguém desconfiar.

Um forward test mede exatamente isso e nada mais. Não avalia a qualidade da
resposta nem executa código: verifica se, diante de um pedido típico, a skill
correta é carregada — e, diante de um pedido parecido de outro domínio, se ela
fica de fora. É o gate que a auditoria do Codex deixou pendente antes da
replicação no trabalho.

- Método e vereditos: `.claude/skills/forward-test-skills/SKILL.md`
- Prompts prontos para colar: [roteiro.md](roteiro.md) (36 testes, 2 mensagens cada)
- Registro de rodadas: copie [template_resultados.md](template_resultados.md)
  para `resultados/<YYYY-MM-DD>_rodada<N>.md`

| Rodada | Data | PASS | FAIL | Resultado |
|---|---|---|---|---|
| 1 | 2026-08-14 | 33 | 2 | [detalhes](resultados/2026-08-14_rodada1.md) — 12/12 negativos corretos; falhas isoladas em `10P`/`11P`; `07M` sem registro |
| 2 | 2026-08-14 | 5 | 0 | [detalhes](resultados/2026-08-14_rodada2.md) — hipótese confirmada: `10P` e `11P` passaram apenas com o prompt corrigido |

**GATE FECHADO ✅ — 36/36 PASS** (positivos 12/12 · negativos 12/12 · menções
12/12). Nenhuma `description` foi alterada em nenhuma rodada: o pacote auditado
pelo Codex passou como estava. As falhas da rodada 1 eram do instrumento de
teste, não do ambiente.

## O que a rodada 1 mostrou

As descriptions do pacote auditado pelo Codex estão **bem calibradas**: nenhuma
das colisões previstas (drift, materialização, deterioração, auditoria×execução)
se materializou, e em 11 dos 12 negativos o Genie ainda escolheu a skill *ideal*
do desvio. As duas falhas se concentraram nas skills que dependem de um artefato
no chat (`comentar-notebook`, `tutor-databricks`): os prompts citavam "este
notebook"/"este stack trace" sem que existissem — defeito do instrumento de
teste, corrigido com prompts v2 autocontidos. **Nenhuma `description` foi
alterada até aqui.**
