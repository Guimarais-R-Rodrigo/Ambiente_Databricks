# SD-FE-A/T01 — feature view composta de PIT — 2026-09-29

(Codex) Prompt e resposta completos foram enviados diretamente nesta
conversa. O usuário informou que a skill `hub-ml-feature-engineering`
apareceu no menu @, que a selecionou e que houve indicador separado de
carregamento. Versão Free esperada: 657/657 arquivos
conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.

## Vereditos separados

- Seleção/roteamento: **PASS por confirmação humana** da seleção @ e do
  indicador separado de carregamento. A frase da resposta citando o contrato
  não é usada como prova desse evento.
- Semântica do contrato: **PASS**. Para
  `COMPOSED_PIT_FEATURE_VIEW_V1`, a resposta exigiu prova PIT upstream
  válida, Receipt/finalizador/verificação do Cross-EDA, projeção FE verificada
  com inputs externos e linhagem de fontes/cutoff/janela/release/IDs.
  `pit_view_contract.json` marca `CANDIDATE_NOT_PROMOTED`,
  `COMPOSED_LOCAL_VIEW`, `fit=false`, `materialization=false` e
  `promotion_authorized=false`. `run_pit_features.py` não emite Receipt FE
  novo, conforme SKILL.md e scripts/README.md. A resposta não atribuiu
  prontidão ML ou registro em Unity Catalog ao perfil.
- Execução: **NOT_RUN**. O prompt diz “view PIT já verificada”, mas não
  fornece payload upstream, contexto, datasets, IDs ou outputs. A resposta
  formula condições para chamar a view de candidata; não mostra chamada
  `compose`/`verify` nem demonstra uma view efetivamente validada nesta
  rodada. Nenhuma materialização foi alegada como efeito observado.

**Veredito T01: PASS conceitual do contrato e do carregamento observado**,
sem execução canônica. Sem edição de produto/publicação.
