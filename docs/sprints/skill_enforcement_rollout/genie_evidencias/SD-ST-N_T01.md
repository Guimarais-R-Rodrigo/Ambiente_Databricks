# SD-ST-N/T01 — fronteira Estatística/Explainability/Tutor — 2026-09-29

(Codex) Prompt e resposta completos foram enviados diretamente nesta conversa.
O usuário informou que o indicador mostrou **Tutor**. Versão Free esperada:
657/657 arquivos conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O roteiro previa chat novo sem @; não há confirmação independente da ausência
de seleção @ nesta coleta. O texto do Genie disse que carregaria Tutor.

## Vereditos separados

- Roteamento: **FAIL em relação ao oráculo congelado**, que esperava
  Explainability. O indicador relatado foi Tutor, não Validação Estatística.
  O estímulo “quero entender” é também compatível com a rota de ensinar
  conceitos da instrução geral; portanto, isto não demonstra sozinho defeito
  da skill Explainability nem justifica mudança de produto. A ambiguidade do
  teste fica registrada sem reescrever o prompt T01.
- Conteúdo central: **PASS** para a conta solicitada, `2 × 2 = 4`, com
  decomposição linear em relação ao fundo. A resposta corretamente não alegou
  Receipt ou execução canônica.
- Precisão: a substituição `2 × (2−0)` escolhe `x1=2` e fundo `0`, embora o
  prompt forneça somente a diferença `x1−fundo=2`. É um exemplo compatível,
  não um dado observado. A formulação de que SHAP linear tem contribuição
  sempre igual ao produto simplifica o caso e depende da definição do valor
  base/perturbação, especialmente com atribuição condicional e correlações.
- Execução: **NOT_RUN**. Não há notebook, chamada de modelo, payload ou
  Receipt nesta evidência; trata-se de resposta conceitual.

**Veredito T01: FAIL de roteamento pelo oráculo do caso, com conteúdo central
correto.** Sem edição de produto/publicação por esta coleta. Próximo caso:
`SD-ST-B`.
