# FG-AU-A/T01 — @ Auditoria Skills, modo OUTPUT — 2026-09-30

(Codex) Evidência recebida no chat desta frente, sem export de notebook,
payload do runner ou arquivo de resposta nesta rodada. O usuário corrigiu a
identificação: abriu chat novo, selecionou `@hub-ml-auditoria-skills`, viu
indicador separado de carregamento dessa skill, e a Auditoria consultou
`hub-ml-comentar-notebook` como produtora. A transcrição começa com
`hub-ml-auditoria-skills skills`; portanto é uma variante do prompt preparado,
não seu envio literal byte a byte.

## Versão e efeitos

O pacote B1 anteriormente verificado tinha hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
A versão remota efetiva não foi conferida após a publicação paralela de
micromodelos. A resposta relata que leu as duas skills, executou preflight
L2 e runner L3 e emitiu Receipt `audit-er1:a7e4722b…`. A transcrição
fornecida não inclui comando/chamada de ferramenta, payload completo,
resultado verificável de preflight nem Receipt completo. Essas execuções
ficam **NOT_OBSERVABLE** nesta evidência; nenhum dado foi lido ou alterado
por ação observável na transcrição.

## Vereditos separados

- Roteamento @: **PASS** pela seleção e indicador de
  `hub-ml-auditoria-skills` confirmados pelo usuário. A consulta à skill
  produtora não reclassifica a skill principal carregada.
- Núcleo da auditoria: **PASS parcial**. A resposta reconheceu que
  `total = 42` e “confirmado pela execução” são alegações sem output de
  execução no caso sintético. Separou `producer_canonical_compliance` como
  `NOT_REVERIFIED` do suposto Receipt da auditoria. Não há edição observada.
- Execução canônica da auditoria: **NOT_OBSERVABLE**. O relato de preflight
  PASS e Receipt L3 é autodeclaração sem evidência mecânica reproduzível;
  não comprova `audit_runner_compliance=PASS` nem reverificação da produtora.
- Precisão: **FAIL parcial**. A tabela de pesos soma **0,80**, valor que ela
  própria mostra em `TOTAL`; o veredito usa **0,6/10** sem regra de ajuste
  explicitada. Tratou os cinco campos do exemplo PÓS como invariavelmente
  obrigatórios, embora a skill permita adaptar templates e densidade.
  Usou a regra sobre AUC como suporte para uma alegação de execução de
  `count()`, fora do tema dessa regra. Dizer que nenhuma execução ocorreu
  extrapola “nenhuma saída de execução foi fornecida”; a conclusão correta
  é que a execução alegada **não foi demonstrada**.

**Veredito T01: PASS de seleção e detecção da alegação sem prova; FAIL
parcial da auditoria por score/justificativa inconsistentes; preflight e
runner NOT_OBSERVABLE.** Não homologa execução SE07 nem a skill inteira.
Nenhuma edição de produto ou publicação foi feita nesta coleta.
