# SD-VF-N-D03 — reteste de Monitoramento — 2026-09-29

(Codex) [Resposta literal](SD-VF-N_D03.txt); notebook original preservado em
`.artifacts/skills-delivery-evidence/genie-20260929-monitor-d03/` e não
executado localmente. SHA256 notebook
`d25419b646649e9c9fc59414263c7a47214a732bcb0cda7847e01f5383ccd90e`;
resposta `07a8e240c7f3ffc5931461194a80c58a73ae1af176432d5171a15f540d7c1ccc`.
Versão Free desta coleta: `2965556ecdb3a8a543d93610430da35dba752d2c35fda124e5b389146f847ba8`.
O usuário confirmou seleção real de `@hub-ml-monitoramento-modelo` no menu e
indicador de carregamento. Os bytes internos carregados pelo Genie não foram
inspecionados.

## Vereditos separados

- Roteamento: **PASS observado na interface** para Monitoramento.
- Enquadramento: PASS. Não presumiu o perfil SER11, Receipt nem metadados de
  operação real para o pedido exploratório.
- Execução local no Genie: OBSERVED pelas saídas salvas. O código corrigiu
  `searchsorted` de `side='right'` para `side='left'` antes da exportação final.
  Duas saídas `text/html` de Plotly estão no notebook; renderização visual no
  navegador não foi observada independentemente.
- Aritmética: PASS **para a política manual escolhida no notebook**. Contagens
  `[1,1,1,1,0]` e `[0,1,1,1,1]`; com pseudocontagem `eps=1e-6` normalizada,
  PSI `6,9077471443`, contribuições extremas `3,4538735721` cada, KS `0,25`
  e p `1`. Auditoria independente recalculou sem executar o anexo.
- Semântica/aderência: **FAIL**. O último limite dos bins usa
  `max(referência, atual)`, embora a resposta diga que os bins são quantis
  congelados na referência; trata-se de política manual e não da do helper.
  A reimplementação deliberada também contraria a instrução de importar o
  helper. O helper canônico com quatro bins produz PSI `3,2805784151`; os
  números diferem pela política de bins e smoothing. A conclusão “o teste não
  tem poder ... daí p=1” atribui ao p-valor uma potência não calculada.
  “Cada score subiu 0,1” sugere pareamento não fornecido; as distribuições são
  translações de 0,1, sem identificação de pares.
- Veredito D03: **FAIL de interpretação/aderência**, apesar de roteamento e
  cálculo manual observados. É diagnóstico fora dos 37 SD e 42 FG; T01, D01 e
  D02 conservam seus vereditos e versões históricas.

A correção local restringiu-se à instrução da skill: caudas definidas pela
referência, origem dos bins manuais declarada, helper nos exemplos executados
e interpretação do KS sem afirmação de potência. O algoritmo canônico não foi
alterado. 15 regressões PASS; validador antes/depois do renderer PASS. A
pré-checagem remota exportou 657 arquivos e encontrou somente a diferença
prevista no SKILL.md; plano → publicação → readback integral PASS em 657/657,
zero erros, hash normalizado
`05f952adfa3c5765f37c3df9e812e3ca430ceb06d91940e575880023e45c68d6`.
Evidência `.artifacts/skills-delivery-evidence/genie-20260929-monitor-d03/publish-verify.json`.
D04 usará essa nova versão; D03 permanece FAIL histórico.
