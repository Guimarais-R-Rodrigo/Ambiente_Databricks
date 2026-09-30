# SD-VF-B-D01 — reteste de Safra — 2026-09-29

(Codex) Resposta completa transcrita da mensagem do usuário e preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-safra-b-d01/response-original.txt`.
Não se atribui hash ao texto original do Genie, pois chegou como mensagem no
chat, não como arquivo exportado. Versão Free esperada:
`1ac2e49e2411ccd448dd050b9b2d8afb646489e81ecc665d4f33ea028404fabc`
(publicação anterior: 657/657 arquivos conferidos). O usuário confirmou chat
novo, sem seleção @, e indicador de Safra visível. Bytes internos carregados
pela interface não foram inspecionados.

## Vereditos separados

- Roteamento espontâneo: **PASS observado na interface**.
- Recusa de fabricação: **PASS**. Não fixou taxa de MOB2 em 50%, não inventou
  observações ou datas nem apresentou resultado numérico como executado.
- Maturidade e cobertura: **FAIL**. A resposta disse que a coorte “ficará
  marcada como imatura” até chegar a segunda observação e justificou que a
  maturação só se confirma com observação. No contrato de Safra, maturidade
  temporal depende da idade no corte; falta de linha mede cobertura, não prova
  imaturidade. Sem safra/corte, `MATURE` e `IMMATURE` são ambos indeterminados.
- Execução: **NOT_RUN**, adequado à falta de entradas; não houve alegação de
  runner, verificação ou Receipt.
- `TASK_CORRECTNESS`: **FAIL** na alternativa oferecida.
  `AGENT_ADHERENCE`: **FAIL** de conteúdo contra regra explícita da skill.
  `CANONICAL_COMPLIANCE`: **NOT_RUN**, sem falsa alegação de execução.
- Veredito D01: **FAIL parcial**. T01 também permanece FAIL histórico; D01 não
  reclassifica T01 nem certifica a skill.

Auditoria independente conferiu a regra e o preflight: a classificação
temporal pode ser madura mesmo quando faltam observações; só as datas de safra
e corte resolvem isso. O `SKILL.md` publicado já proibia expressamente atribuir
a ausência à imaturidade e fornecia a conclusão correta. Não há causa
demonstrada para outra edição equivalente, nem defeito do runner. A pendência
de aderência comportamental fica aberta; a campanha avança para `SD-EX-P`
preservando este resultado.
