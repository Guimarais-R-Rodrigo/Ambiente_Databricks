# SD-EX-N-D01 — reteste do limite sintético de Validação Estatística — 2026-09-29

(Codex) Resposta completa fornecida pelo usuário nesta conversa, sem arquivo
externo anexado. Versão Free publicada e conferida antes da coleta:
`60f9b7023c0ea65feae2f39c162504a7181292311718d4e0e5d43b5b90d6bba6`
(657/657 arquivos, zero problemas). O usuário confirmou chat novo, sem seleção
por `@`, e indicador separado de **Validação Estatística**. A resposta textual
não prova quais arquivos foram efetivamente lidos nem chamada de runner.

## Vereditos separados

- Roteamento: **PASS observado por confirmação humana**. Validação Estatística
  apareceu espontaneamente no indicador; não houve seleção por `@`.
- Orientação que motivou o reteste: **PASS**. A resposta pediu os dois vetores,
  o `alpha` pré-especificado e confirmação de que os dados são realmente
  sintéticos. Deixou explícito que dados reais de tabela ou arquivo ficam fora
  do perfil piloto, sem sugerir reclassificá-los como `synthetic: true` ou
  executar manualmente como substituto da rota protegida.
- Limites do contrato: **PASS textual**. Mencionou 4–10.000 itens por vetor,
  pré-condições declaradas pelo usuário e rejeição de empates após `float64`.
  Não inventou D, p-valor, decisão, Receipt nem execução.
- Execução canônica: **NOT_RUN** por ausência de vetores, alfa e origem
  confirmada; não certifica o perfil SER04 nem uma conclusão estatística.
- Veredito D01: **PASS diagnóstico de orientação e roteamento**. O T01 conserva
  FAIL parcial histórico. D01 é diagnóstico fora dos 37 casos SD.

A primeira resposta final pediu exatamente os três pontos materiais: arrays
`reference`/`comparison`, alfa pré-especificado e origem sintética ou real.
Houve erro tipográfico em “confirhe”, sem efeito no contrato. Nenhuma nova
edição de produto ou publicação decorre deste reteste. Próximo caso guiado:
`SD-EX-B`.
