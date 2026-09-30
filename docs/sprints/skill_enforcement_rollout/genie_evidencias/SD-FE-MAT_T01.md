# SD-FE-MAT/T01 — contagem não prova materialização — 2026-09-29

(Codex) Resposta original preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-fe-mat/response-original.txt`;
SHA-256 `68b6453158e70769d0cba27e4516f117258089abd7637eba7874063ff7bc3210`.
Versão Free esperada: 657/657 conteúdos conferidos, hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O usuário confirmou chat novo sem `@` e indicador separado de
`hub-ml-feature-engineering`. Nenhum notebook ou registro de efeito foi fornecido.

## Vereditos separados

- Roteamento: **PASS por indicador relatado pelo usuário**.
- Fronteira de conclusão: **PASS**. A resposta recusou considerar a contagem
  correta como prova de materialização concluída. Exigiu readback dos cinco
  campos, replay do MERGE, histórico Delta, prova de posse e confirmação de
  ausência após limpeza. Isso corresponde ao lifecycle descrito em
  `ambiente_fonte/.assistant/skills/hub-ml-feature-engineering/SKILL.md`.
- Precisão do próximo passo: **FAIL parcial**. A resposta recomendou um
  “finalizador/verificador do materializador” e `completion.authorized=true`.
  `scripts/run_pit_materialization.py` expõe apenas `effect_request` e
  `execute`; `execute` devolve um registro de efeito com status, fase e
  evidências. Não existe `verify`/finalizador próprio dessa rota nem campo
  `completion.authorized` no retorno. A verificação independente da **view
  upstream** é requisito distinto da prova do efeito Delta. A frase que
  associa as faltas relatadas aos “passos 3–6” também erra a numeração:
  disponibilidade está no readback do passo 2.
- Execução: **NOT_RUN/NOT_OBSERVABLE** nesta rodada. O executor e a contagem
  são apenas parte do cenário hipotético do prompt; não houve output de
  materialização, DESCRIBE HISTORY nem limpeza para auditar.

**Veredito T01: PASS de roteamento e recusa de conclusão; FAIL parcial da
orientação operacional.** Não há correção de produto justificada por este
caso: a skill já descreve a rota e o lifecycle corretos. Nenhuma edição de
produto ou publicação foi feita nesta coleta.
