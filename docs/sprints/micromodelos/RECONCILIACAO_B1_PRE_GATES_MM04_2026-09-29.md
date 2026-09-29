# Reconciliação B1 e pré-gates da candidata MM04

**Data:** 2026-09-29. **Escopo:** candidata de laboratório da PR #116 e
checkout compartilhado B1. Este registro é uma
verificação de desenvolvimento; não é FULL, auditoria independente, aceite
humano ou autorização de merge/promoção.

## Estado e delta de produto

- PR #110/MM03: `MERGED` em `3214a131`; PR #99/PSEF01: `OPEN`;
  PR #108/SER01 e PR #113/B0: `MERGED`. A `main` observada era `4ba7f551`.
- PR #116: `OPEN`, `Draft`, base `main`, branch
  `micromodelos/autonomia-local-v2`. A policy candidata declara 15 skills;
  `hub-ml-micromodelos` é `risk_class=high`, `current_level=L1`,
  `target_level=L3`, `scope_mode=stage_specific`, `rollout_mode=audit`.
  Não há runner, Receipt ou adapter Databricks da skill.
- O B1 havia importado do Free a versão anterior de `SKILL.md`, SHA-256
  `e7964e906acca0f8a6376a44229a05c557c23afff6aad606fdea7e5ad6a00fba`.
  Somente esse arquivo foi atualizado na fonte B1 para a revisão que passou
  pelos casos Genie, SHA-256
  `cccdfb314452c44575f13a49232671acf8da16b3f3a5307049c18b37edbbfab5`.
  O derivado foi regenerado por `tools/render_simulado.py --write`; os 657
  arquivos renderizados coincidem byte a byte com a fonte. Contrato, policy e
  instruções conservam os hashes da reconciliação B1 original.
- Os dois briefings da PR #116 foram alinhados à skill corrigida. O de objetivo
  conhecido só pede YAML quando o schema MM01 está acessível; o de descoberta
  distingue fixture `FORNECIDA` de metadata `OBSERVADA`. Esses briefings
  revisados foram testados depois no Genie: P1 passou como resposta com
  ressalva de proveniência; P2 falhou por inferir detecção de fabricação a
  partir de “eventos fictícios”, expressão ambígua na fixture. O reteste P2b
  esclarecido corrigiu a semântica, mas falhou em classificar E0/E1 e em
  localizar a policy integrada. A skill da PR foi então revisada e publicada
  no Free com readback idêntico, SHA-256
`93e51ac4ca25f2c3bd88c6cb6a40e7e494fd9bf1852824cd4575628cf24351f2`.
  P2c segue `NOT_RUN`. O checkout B1 ainda tem o hash anterior
  `cccdfb314452c44575f13a49232671acf8da16b3f3a5307049c18b37edbbfab5`;
  sua nova reconciliação fica pendente antes de integração. Ver
  [resultados](TESTE_BRIEFINGS_MM04_E1.md).

## Verificações proporcionais desta reconciliação

| Verificação | Resultado | Limite |
|---|---|---|
| Genie Code Free, revisão corrigida | Casos E1 1 e 2 PASS de resposta; caso 3 PASS de contenção adversarial, com ressalvas de ambiente/proveniência. | Seleção no menu declarada pelo usuário, sem captura independente; transcrições não auditam todas as chamadas internas. Ver [resultados](RESULTADOS_GENIE_E1_2026-09-29.md). |
| B1 source → derivado | 657 arquivos byte a byte iguais; só `README.md` da raiz da fonte fica fora do renderer. | Não prova publicação da árvore B1 revisada. O `SKILL.md` novo já tinha readback idêntico no Free pela PR #116. |
| B1 `validate_assistant.py --root ambiente_fonte` | APROVADO, 0 falhas, 0 avisos. | B1 continua com mudanças locais de outras frentes. |
| B1 policy I/O | 15 testes PASS. | Bateria SE07/policy de 59 testes teve 2 FAIL e 1 skip por expectativa histórica L2 de `hub-ml-criar-objeto` frente à policy atual L3; não apresentar como PASS. |
| PR #116 validação do produto | APROVADO após o ajuste dos briefings, 0 falhas e 1 aviso local de `__pycache__`; derivado regenerado pelo renderer. | Validação estática não comprova resposta real dos briefings. |

## Gates próprios da MM04

| Gate | Situação agora | Ação necessária |
|---|---|---|
| `MM04_SEF_READINESS` | **Preparado para revisão**, sem homologação formal. Policy L1/audit e superfícies protegidas estão declaradas; target L3 é apenas direção. | Revisar policy integrada e evidência de cada superfície no snapshot congelado; não inferir L2/L3 dos testes de conversa. |
| `MM04_PSEF_PROMPT_READINESS` e `MM05_PROMPT_CONTRACT_READY` | **Pendente**. PSEF01 segue aberta; decisão desta candidata: usar o contrato integrado em `hub_padroes/prompt/template.md`, sem incorporar o draft. P1 passou como resposta; P2 falhou em interpretação semântica; P2b corrigiu essa interpretação, mas falhou em classificar ambiente e policy. Os briefings dos notebooks de exemplo ainda diferem de P1/P2b e suas partes 3 seguem `NOT_RUN`. | Executar [P2c com a skill revisada](TESTE_BRIEFINGS_MM04_E1.md) em chat novo. Alinhar o briefing de cada notebook à prova real antes de preencher a parte 3; não atribuir uma resposta a texto diferente. |
| `PRE_CERTIFICATION_SMOKE` / `CANDIDATE_FREEZE` | **Não executados para MM04**. A PR #116 é candidata de laboratório; o B1 possui muitas alterações locais não commitadas, incluindo a skill importada. | Definir branch/escopo de sprint, atualizar refs, exigir `behind_by=0`, árvore limpa, snapshot/validator e gates focais verdes antes de congelar SHA/tree. |
| FULL proporcional, bundle lint, auditoria independente, contraditório, fechamento e revalidação final | **NOT_RUN** para MM04. | Executar somente após smoke e freeze, preservando FAILs históricos. Os testes B1 e a publicação Free não substituem estes gates. |
| Aceite humano, merge, promoção | **PENDENTE**. | Solicitar aceite sobre candidata certificada e auditada. Não promover `current_level` nem acessar E2 por inferência. |

O checkout B1 é compartilhado e estava sujo antes desta atualização. Nenhuma
alteração alheia foi descartada; não houve commit, push ou merge do B1 nesta
reconciliação. Seu registro local está em
`docs/sprints/skill_enforcement_rollout/RECONCILIACAO_MM04_2026-09-29.md`.
