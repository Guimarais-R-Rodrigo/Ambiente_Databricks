# SD-VF-STATUS-D01 — maturidade e cobertura com corte — 2026-09-30

(Codex) Prompt e primeira resposta preservados em
`.artifacts/skills-delivery-evidence/genie-20260930-vf-status-d01/response-original.txt`;
SHA-256 `680643273a7e9abfa007687dbe795cad669578cd13c1d33a11c5f9bd939c892b`.
O usuário informou chat novo, seleção de `hub-ml-analise-safra` via @ e
**indicador separado** de carregamento de Safra.
As tentativas anteriores de Safra permanecem evidências históricas distintas.

## Oráculo e resultado

Safra janeiro/2026 com corte em 31/mar/2026 alcançou MOB2. O oráculo do
contrato local é: MOB0 `MATURE/COMPLETE` (2/2), MOB1
`MATURE/NO_OBSERVATIONS` (0/2), MOB2 `MATURE/INCOMPLETE` (1/2), MOB3
`IMMATURE/IMMATURE`. O roster mantém denominador 2. Só MOB0 teria
cobertura para taxa final, mas falta o alvo 0/1; nenhuma taxa numérica
é calculável. Não há observação da causa das faltas.

A resposta acertou os quatro pares maturity/coverage_status, explicou a
idade até MOB2, preservou o denominador 2 para MOB0 e não inventou alvo,
taxa ou causa da ausência. Reconheceu que só MOB0 é estruturalmente
elegível à taxa final e que seus valores seguem pendentes.

## Vereditos separados

- Roteamento: **PASS** por seleção @ e indicador separado relatados.
- Classificação temporal e cobertura: **PASS** nos quatro MOBs.
- Taxa final e valores ausentes: **PASS no núcleo**; não finalizou taxa nem
  apresentou numerador fictício.
- Denominador: **FAIL parcial**. Para MOB2, a resposta sugeriu “taxa
  provisória com denominador parcial 1”. O pedido dizia preservar o
  denominador fixo 2; `1/2` é cobertura observada, não novo denominador
  da coorte. Nenhuma taxa com 1 foi efetivamente calculada.
- Execução: **NOT_RUN**. O cenário é hipotético; não há preflight, runner,
  Receipt, verificador, notebook ou dados executados na transcrição.

**Veredito D01: PASS dos status e da recusa de taxa final; FAIL parcial na
formulação do denominador provisório.** Não homologa a rota executável de
Safra nem altera resultados anteriores. Nenhuma edição ou publicação de
produto foi feita nesta coleta.
