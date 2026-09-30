# SD-MO-P/T01 — PSI/KS sintético sem labels — 2026-09-29

(Codex) Resposta original e notebook exportado preservados em
`.artifacts/skills-delivery-evidence/genie-20260929-mo-p/`.
SHA-256 da resposta: `07b865ff6c3636b6929548f76d851f19b43632757a65b690620d23c068bfb695`;
SHA-256 de `111-original.ipynb`:
`a24ede27fbfe555ca4f4c744b11863934443470b4f6f5a431448d5f1f4d72423`.
Versão Free esperada: 657/657 conteúdos conferidos, hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O usuário confirmou chat novo, sem `@`, com indicador separado de
`hub-ml-monitoramento-modelo` carregada.

## Vereditos separados

- Roteamento: **PASS por relato humano**. Monitoramento foi selecionada
  espontaneamente para drift de score sem labels.
- Escopo/entrada: **PASS com fixture demonstrativa**. O notebook registra os
  cinco valores finitos de cada lista e acrescenta um `None` por janela,
  interpretação coerente do pedido. IDs, datas, modelo, população, `n_bins=4`
  e `eps=1e-6` foram criados pela Genie e rotulados como demonstração, não
  como metadados fornecidos pelo usuário. A execução diz respeito somente
  a esse request sintético, não a monitoramento real.
- Execução: **OBSERVED no notebook**. A célula exportada contém a chamada de
  `preflight`, `run` e `verify`; stdout registra preflight/run `PASS` e
  `verify` `VALID`, com run ID e request SHA. O Receipt existe no payload em
  memória segundo a rota, mas o objeto completo não foi impresso/exportado;
  o registro aqui não substitui inspeção independente desse Receipt.
- Métricas: **PASS**. Recálculo local independente obteve quantis internos
  `[0,1; 0,3; 0,6]`, contagens com missing `[0,2,1,2,1]` versus
  `[0,1,1,3,1]`, PSI `0,1831020481113516`, KS `0,4` e p-valor SciPy
  `0,873015873015873`. As contribuições PSI não nulas são `0,115524530093`
  e `0,067577518018` nos bins de massa alterada.
- Interpretação: **PASS da fronteira sem labels**, **FAIL parcial de precisão**.
  A resposta não inferiu performance, severidade aprovada, alerta nem retreino.
  Porém, o texto atribuiu forte influência ao smoothing por “bins que recebem
  zero observações em um lado”; nesta fixture há somente um bin vazio em
  **ambas** as janelas, cuja contribuição é zero. Os bins com contribuição
  positiva têm massa dos dois lados. Também falou em “sensibilidade limitada”
  do KS apenas por `n=5`, sem estudo de potência.
- Inferência KS: o valor numérico do p-valor reproduz SciPy, mas há empates
  (`0,1` na referência e `0,7` na atual). A documentação oficial de
  [`ks_2samp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html)
  pressupõe amostras de distribuições contínuas; sem justificar o mecanismo
  dos empates, a leitura inferencial formal desse p-valor é limitada.

**Veredito T01: PASS de roteamento, execução local sintética e contas;
FAIL parcial de interpretação.** A skill publicada já exige identificar o
bin responsável antes de atribuir efeito ao smoothing e veda conclusão de
potência sem alternativa/alfa/cálculo. Preservar a falha histórica e avaliar
reteste focal; nenhuma edição de produto ou nova publicação foi feita por
esta coleta.
