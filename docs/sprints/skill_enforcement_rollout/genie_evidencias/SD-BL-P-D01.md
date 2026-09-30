# SD-BL-P-D01 — plano temporal sem treino — 2026-09-30

(Codex) Prompt e resposta originais preservados em
`.artifacts/skills-delivery-evidence/genie-20260930-bl-d01/response-original.txt`;
SHA-256 `a091fdce6799cc4b3f9687964a8b1379b25378fcc257abeee264e0cc714206db`.
O usuário informou chat novo, sem @, e que `hub-ml-baseline-ml` foi lida e
chamada. Depois confirmou indicador separado de Baseline ML: **OBSERVED**.
O [SD-BL-P/T01](SD-BL-P_T01.md) permanece FAIL histórico; este
diagnóstico não o substitui.

## Versão e efeitos

O pacote B1 anteriormente verificado tinha hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
A versão remota efetiva após publicação paralela de micromodelos não foi
conferida. Não há notebook, linhas sintéticas criadas, preflight, run,
Receipt, MLflow ou métrica na transcrição. O Genie apresentou apenas um
plano, conforme a restrição do prompt.

## Vereditos separados

- Roteamento: **PASS** por indicador separado de `hub-ml-baseline-ml`
  confirmado pelo usuário em chat novo sem @.
- Fit e holdout: **PASS no núcleo**. Restringiu ajuste do modelo e do
  preprocessamento ao treino; usou julho–setembro para escolher
  hiperparâmetros e manteve outubro–dezembro fora da seleção. Condicionou
  avaliação final à maturidade dos labels e à data de corte. Não criou
  dados, treino ou run MLflow.
- Precisão temporal: **FAIL parcial**. “Um mês depois” não especifica
  automaticamente “fim do mês seguinte”; o texto adotou essa convenção
  para fixar fins de julho, outubro e janeiro sem rotulá-la como hipótese.
  A disponibilidade exata depende de timestamps e da data de corte, que
  o prompt deixou ausentes. Tratou maturação dos labels como condição
  também para ajustar *scaler/imputer* não supervisionados, o que não é
  necessidade geral. Chamou o atraso de label de “gap natural” entre
  splits, embora gap e disponibilidade das features exijam definição
  própria. Essas imprecisões não fizeram o holdout selecionar parâmetros.
- Execução: **NOT_RUN na evidência recebida**. Nenhuma métrica, promoção
  ou efeito remoto foi declarado como realizado.

**Veredito D01: PASS de planejamento/holdout e respeito ao não executar,
com FAIL parcial de precisão temporal.** O roteamento espontâneo passou.
Não homologa a skill inteira; nenhuma edição de
produto ou publicação foi feita nesta coleta.
