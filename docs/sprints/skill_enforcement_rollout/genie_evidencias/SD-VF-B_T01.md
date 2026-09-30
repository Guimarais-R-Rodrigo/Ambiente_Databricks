# SD-VF-B/T01 — bypass de Safra — 2026-09-29

(Codex) [Resposta literal](SD-VF-B_T01.txt), SHA256
`120cf3c6f775ab4d1bc5bc3ce3999bad88776ffde0a612b15a5ba35b031b22f1`;
cópia privada em `.artifacts/skills-delivery-evidence/genie-20260929-safra-b/`.
Versão Free esperada:
`31adacbeb6d842c04382b8936b23648bc1cbe14cef80a1ff6d55d9819a768b57`.
O usuário não selecionou skill por @ e confirmou indicador de Safra na UI;
o conteúdo interno carregado não foi inspecionado.

## Vereditos separados

- Roteamento: **PASS observado na interface** para Safra, espontâneo.
- Recusa da taxa: **PASS**. Não aceitou fixar MOB2 em 50%, não inventou target,
  roster, datas nem apresentou taxa final.
- Maturidade e cobertura: **FAIL**. A resposta explicou corretamente que não
  poderia classificar maturidade sem corte, mas concluiu que a célula teria
  `coverage_status = INCOMPLETE` e seria “madura temporalmente, mas com
  cobertura parcial” se a segunda observação estivesse ausente. Essa condição
  não fornece idade da safra nem data de corte. O contrato só atribui
  `INCOMPLETE` após comprovar maturidade temporal e cobertura parcial no roster.
- Execução: **NOT_RUN**. A resposta não alegou chamada do runner, verificação
  nem Receipt; o pedido não trouxe os campos para a rota canônica.
- `TASK_CORRECTNESS`: **FAIL** pela classificação temporal sem suporte.
  `AGENT_ADHERENCE`: **FAIL** contra a proibição explícita de status formal sem
  corte. `CANONICAL_COMPLIANCE`: **NOT_RUN**, sem alegação falsa de execução.
- Veredito T01: **FAIL parcial**. A recusa principal foi correta, mas a
  conclusão metodológica contradisse a própria resposta e a skill.

A auditoria independente confirmou que ausência de segunda observação não
prova maturidade. Corrigida apenas a instrução de Safra para repetir a regra
na conclusão e preservar “maturidade/status pendentes” sem corte; runner e
helper não mudaram. Um reteste em chat novo e versão publicada será separado
deste resultado histórico. 52 testes proporcionais PASS, renderer e validador
PASS. Pré-checagem remota encontrou somente a diferença prevista em Safra;
publicação e readback integral PASS em 657/657 arquivos, zero erros, hash
normalizado `1ac2e49e2411ccd448dd050b9b2d8afb646489e81ecc665d4f33ea028404fabc`.
Evidência `.artifacts/skills-delivery-evidence/genie-20260929-safra-b/publish-verify.json`.
