# SD-FE-PIT/T01 — referência anterior, disponibilidade posterior — 2026-09-29

(Codex) Resposta original preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-fe-pit/response-original.txt`;
SHA-256 `d4eb460a5b12fc0a93527f8fdf8547cc51076ee3c5ff7d490e809f564db4c10e`.
Versão Free esperada: 657/657 conteúdos conferidos, hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O usuário confirmou chat novo sem `@` e indicador separado de
`hub-ml-feature-engineering` carregada. Nenhum notebook foi exportado.

## Vereditos separados

- Roteamento: **PASS por indicador relatado pelo usuário**. Feature
  Engineering foi selecionada espontaneamente para elegibilidade PIT.
- Regra temporal: **PASS**. O valor do atributo com disponibilidade
  posterior à decisão não é elegível naquela decisão, ainda que sua data
  de referência seja anterior. A distinção entre tempo do fato e tempo
  conhecido pelo sistema é correta.
- Estado da view: **FAIL parcial de precisão**. O prompt não informa qual
  coluna governa o PIT nem o resultado da verificação upstream. A resposta
  presumiu que a view usa a referência como `timeseries_column` e afirmou
  que a view inteira está configurada com leakage. Uma view que já use
  disponibilidade corretamente pode continuar válida para outras decisões,
  mas deve excluir/deixar nulo esse atributo nesta. É o **valor nessa linha**
  que é inelegível; a validade geral da view requer inspecionar contrato,
  cutoff e prova PIT. A [documentação Databricks de PIT](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series)
  explica o papel da coluna temporal declarada no join, mas não prova qual
  coluna foi usada neste caso.
- Execução: **NOT_RUN**. Nenhum request, Receipt upstream, `compose`,
  `verify` ou materialização foi fornecido. A resposta é conceitual;
  não homologa a feature view sintética citada no prompt.

**Veredito T01: PASS de roteamento e regra de disponibilidade, FAIL parcial
de escopo/prova da view.** Nenhuma edição de produto/publicação foi feita
por esta coleta.
