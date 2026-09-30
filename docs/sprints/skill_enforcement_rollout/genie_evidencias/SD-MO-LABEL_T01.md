# SD-MO-LABEL/T01 — label posterior ao cutoff — 2026-09-29

(Codex) Resposta original preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-mo-label/response-original.txt`;
SHA-256 `b1af94359928254965f0878746e60934431d433553eb2f878403245a77c768c3`.
Versão Free esperada: 657/657 conteúdos conferidos, hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O usuário confirmou chat novo sem `@` e informativo de uso de
`hub-ml-validacao-estatistica`. Nenhum notebook ou execução foi fornecido.

## Vereditos separados

- Roteamento: **FAIL específico de Monitoramento**. Validação Estatística é
  temática próxima, mas o caso testa maturidade de labels no monitoramento
  de performance; a skill `hub-ml-monitoramento-modelo` não apareceu.
- Decisão de AUC: **PASS**. A resposta não fechou a AUC atual com o label
  indisponível em 10/mar e reconheceu a métrica como incompleta naquele
  corte. Não alegou AUC calculada nem execução SER12.
- Escopo e orientação: **FAIL parcial**. Não distinguiu a superfície de
  drift sem labels, esperada no caso. Tratou atraso de disponibilidade como
  censura à direita sem saber se o desfecho é de tempo até evento. Sugeriu
  excluir uma “instância equivalente” da referência sem chave/pareamento
  definido; comparabilidade exige populações, janelas e regra de maturidade
  pré-especificadas, não remoção arbitrária em ambos os grupos. Também
  chamou o impacto de um label em milhares de “desprezível” sem scores,
  classes ou análise de sensibilidade. Mover o cutoff a 11/mar só bastaria
  após verificar completude das duas janelas e política de avaliação.
- Execução: **NOT_RUN**. Nenhum request, métrica ou Receipt foi apresentado.

**Veredito T01: PASS da decisão principal; FAIL de roteamento e precisão
parcial.** A skill de Monitoramento já diz considerar atraso dos labels e
não concluir performance sem eles. Nenhuma edição de produto/publicação foi
justificada ou realizada por esta coleta.
