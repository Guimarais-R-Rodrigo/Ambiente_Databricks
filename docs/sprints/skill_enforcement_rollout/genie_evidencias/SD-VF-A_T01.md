# SD-VF-A/T01 — MOB2 parcial com @ — 2026-09-29

(Codex) Resposta colada diretamente pelo usuário nesta conversa, sem arquivo
anexo. O usuário confirmou chat novo, seleção de `@hub-ml-analise-safra` no
menu e indicador separado de carregamento. Nenhum notebook ou execução foi
fornecido. Versão Free esperada: 657/657 conteúdos conferidos, hash
normalizado `7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.

## Vereditos separados

- Roteamento: **PASS** por seleção @ e indicador confirmados pelo usuário.
- Decisão da taxa: **PASS**. A resposta recusou taxa final de janeiro/MOB2
  com apenas um dos dois contratos observado e preservou denominador 2.
  Não inventou ID, target, valor da observação ou causa da ausência.
- Maturidade e cobertura: **FAIL parcial**. A resposta condicionou
  `INCOMPLETE` à maturidade e depois reconheceu que falta a data de corte;
  isso preserva a ressalva principal. Porém concluiu que uma ausência
  formalizada poderia levar a `NO_OBSERVATIONS`, incompatível com o único
  contrato já observado. Sem corte, a formulação contratual é “cobertura
  parcial relatada; maturidade e status formal pendentes da data de corte”.
  `NO_OBSERVATIONS` exige zero observações em célula temporalmente madura.
- Execução: **NOT_RUN**. Nenhum request, Receipt, coverage_grid ou taxa
  calculada foi apresentado.

**Veredito T01: PASS de roteamento e decisão principal; FAIL pontual de
status alternativo.** A skill já traz explicitamente a regra correta.
Nenhuma edição de produto/publicação foi feita por esta coleta.
