# SD-EX-P/T01 — Explainability linear — 2026-09-29

(Codex) Resposta completa transcrita da mensagem do usuário e preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-explainability-p/response-original.txt`.
Não se atribui hash ao texto original do Genie, pois chegou como mensagem no
chat, não como arquivo exportado. Versão Free esperada:
`1ac2e49e2411ccd448dd050b9b2d8afb646489e81ecc665d4f33ea028404fabc`
(657/657 arquivos conferidos antes desta coleta). O usuário confirmou chat
novo, sem seleção @, e indicador de Explainability visível. Os bytes internos
carregados não foram inspecionados.

## Vereditos separados

- Roteamento espontâneo: **PASS observado na interface**. O texto intermediário
  disse que dispensaria skill por ser dúvida simples, mas a UI mostrou o
  carregamento; essa fala não substitui o evento observado.
- Aritmética e explicação: **PASS**. Para `f(x)=3+2x1−x2`, fundo `(0,0)` e
  observação `(2,1)`, base `f(0,0)=3`, contribuições locais `(+4,−1)` e
  predição `3+4−1=6`. O total local `+3` coincide com a diferença entre
  predição e base. Identificou a decomposição como conceitual/“SHAP-style”.
- Execução: **NOT_RUN**. Não há notebook, chamada ao helper SHAP, modelo
  vinculado, Receipt nem saída canônica; a resposta não alegou tê-los produzido.
- Interpretação: a observação final sobre fundo com múltiplos pontos usa a
  fórmula linear interventional de modo simplificado; implementações SHAP
  dependem do explicador e das hipóteses sobre dependência entre features.
  Essa frase não muda a conta do caso de fundo único nem é prova de execução.
- Veredito T01: **PASS no escopo conceitual solicitado**, com execução NOT_RUN.
  Não certifica o perfil `LINEAR_REGRESSION_SYNTHETIC_V1` nem homologação geral
  da skill.

Nenhuma edição de produto ou publicação decorre desta resposta. O próximo
caso guiado é `SD-EX-A`, com seleção explícita pelo menu @ e chat novo.
