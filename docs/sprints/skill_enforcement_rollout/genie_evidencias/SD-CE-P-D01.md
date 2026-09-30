# SD-CE-P-D01 — Cross-EDA espontânea após ajuste de roteamento — 2026-09-30

(Codex) Prompt e resposta preservados em
`.artifacts/skills-delivery-evidence/genie-20260930-ce-d01/response-original.txt`;
SHA-256 `71d4f539e6950400d8cfd531b4a3166a7a712d02fc5a368c763c9aaa3a01c7b4`.
O usuário confirmou chat novo, sem @ e com indicador separado de
`hub-ml-cross-eda-ml`. Confirmou também que, além do indicador, viu
**apenas o texto da resposta**, sem chamadas ou outputs separados.
O texto do prompt coincide com o reteste preparado.
O [SD-CE-P/T01](SD-CE-P_T01.md) permanece FAIL histórico; D01 não o
substitui nem é uma nova primeira tentativa SD.

## Versão e efeitos

O pacote B1 anteriormente verificado tinha hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
A versão remota efetiva desta coleta não foi conferida após a publicação
paralela de micromodelos. A transcrição contém declarações de preflight,
runner Spark, Receipt `er1:733eb8d8…` e verify `valid=true`, mas **não
inclui** chamadas de ferramenta, payload de contexto/datasets, hashes
integrais, trace, Receipt completo, oráculo independente nem retorno do
verificador. Esses efeitos mecânicos são **NOT_OBSERVABLE na transcrição**;
o relato textual não autoriza marcar a rota canônica como executada.

## Vereditos separados

- Roteamento espontâneo: **PASS** pelo indicador confirmado sem @. Esta
  mudança de comportamento em relação a T01 foi observada.
- Conta da fixture: **PASS como cálculo a partir do enunciado**. Dois dos
  três IDs da âncora aparecem nos atributos (`2/3 = 66,67%`), `c` não tem
  match e as linhas declaradas únicas não geram fan-out neste snapshot.
  Isso não equivale a cobertura **medida canonicamente** por Spark.
- Proveniência de entrada: **FAIL material**. O prompt não forneceu
  `decision_at`, target/horizonte, IDs de snapshots nem valor de atributo.
  O Genie declarou ter criado `attr_value` e “usado um synthetic
  decision_at” para completar o contexto. O schema SER05 exige
  `decision_at`, `snapshot_id` e hash de conteúdo; a skill exige confirmar
  contexto e registrar pendências, não preencher metadados ausentes para
  obter PASS. O pedido permitia explicitamente reportar o que faltava.
- Execução/verificação: **NOT_OBSERVABLE** na evidência fornecida. Mesmo
  uma chamada real precisaria de `status=PASS`, Receipt, recurso
  `join_diagnostics` concluído e `verify(valid=true)` vinculado aos
  inputs/oráculo independentes. A transcrição só afirma esses estados.
- Escopo: **PASS parcial**. A resposta distinguiu `join_executed=false`,
  `pit_executed=false` e `ml_readiness=NOT_EVALUATED` e não trouxe escrita
  persistente observável. “Risco nulo” e causa “ausência estrutural” são
  categóricos demais: o snapshot não tem fan-out e `c` não tem match;
  causas e snapshots futuros não foram comprovados.

**Veredito D01: PASS do roteamento espontâneo e da aritmética do cenário;
FAIL da fronteira de contexto; execução canônica NOT_OBSERVABLE.**
Não homologa SER05 no Genie nem comprova criação/ausência de tabela remota.
Nenhuma edição de produto ou publicação foi feita nesta coleta.
