# SD-ST-A/T01 — KS intercalado com seleção @ — 2026-09-29

(Codex) Resposta literal preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-st-a/response-original.txt`;
SHA256 `f1b9935ef150ececbd328075f58f25cc56408fa8ec5adc3e4b04c4b1cdace207`.
Versão Free esperada: 657/657 arquivos conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O usuário confirmou seleção de `hub-ml-validacao-estatistica` no menu @ e
indicador separado de carregamento.

## Vereditos separados

- Roteamento: **PASS observado** por confirmação humana.
- Estatística e decisão: **PASS no oráculo principal**. As amostras intercaladas
  têm `D=0,25`; o p-valor exato bilateral é `1`; a decisão é não rejeitar H0
  a 5%. A resposta corretamente disse que não rejeição não demonstra
  equivalência. A aproximação assintótica de limiar `~0,96` foi identificada
  como aproximação e leva à mesma decisão; não é o limiar exato.
- Procedência de execução: **FAIL parcial**. O texto anunciou “vou calcular”,
  afirmou que “os resultados confirmam” e atribuiu `p=1` a retorno do SciPy,
  mas a evidência recebida não inclui célula, comando, stdout, notebook, payload
  ou Receipt. O valor está correto por cálculo independente; a execução no
  Genie e a rota canônica permanecem **NOT_OBSERVABLE/NOT_RUN**. Uma conta
  conceitual poderia sustentar o número sem alegar chamada executada.
- Poder: **FAIL parcial de interpretação**. `n=4` limita a resolução do teste,
  mas “poder quase nulo” e “praticamente qualquer configuração” não decorrem
  de `D=0,25` e `p=1`. Poder exige alternativa/distribuições e desenho
  especificados. Para estas amostras sem empates, apenas `D=1` rejeita no
  teste exato a 5%; isso não permite quantificar poder contra toda alternativa.
- Pressupostos: o prompt não afirma origem sintética nem independência/i.i.d.
  A resposta conceitual não certificou o perfil executável, mas deveria
  manter esses pressupostos explícitos caso interpretasse o p-valor como
  inferência sobre populações.

**Veredito T01: FAIL parcial de aderência/procedência e interpretação;**
oráculo central e roteamento PASS. A skill já separa conta conceitual de
execução canônica e recomenda planejar poder a priori. Por isso, esta coleta
não motivou edição de produto/publicação; a falha comportamental permanece
registrada, sem converter a resposta em execução observada.
