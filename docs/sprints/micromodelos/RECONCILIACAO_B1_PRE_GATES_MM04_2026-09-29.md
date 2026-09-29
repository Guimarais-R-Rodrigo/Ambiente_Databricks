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
  P2c passou nas guardas centrais após carregar a revisão, com ressalvas de
  redação/formato; os exemplos agora contêm o prompt exato e a referência à
  resposta real. O checkout B1 ainda tem o hash anterior
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

## Diagnóstico pré-smoke posterior

Em 2026-09-29, antes de congelar a candidata, a branch da PR #116 estava em
`7642fb0f56a2e4b68aa412b14b228fade96e11ec`, com `origin/main` e merge-base
em `4ba7f551767d847381df1556ed937116258fa77d`, `behind_by=0`,
`ahead_by=13` e repositório não shallow. A árvore estava **suja** pelas
correções editoriais desta rodada, portanto esse SHA não foi congelado.

O validador do produto passou com 0 falhas e 1 aviso local de `__pycache__`.
Testes focais `test_micromodelo_mm04_flow` + `test_skill_enforcement_policy_io`
passaram 29/29; `test_micromodelo_free_kit` passou 3/3. O preparo textual dos
dois exemplos foi executado localmente em E0, sem tabela. O bloco copiável de
cada notebook permaneceu idêntico ao prompt P1/P2b, respectivamente.

Os checks do GitHub para esse SHA falharam antes de executar qualquer step:
o job `validar` da run `36628810564` tem `steps=[]` e `runner_id=0`. A
anotação do GitHub diz: “The job was not started because recent account
payments have failed or your spending limit needs to be increased.” Os demais
checks listados na PR falharam em segundos. Classificação:
`BLOCKED_EXTERNAL_CI`, **não** falha dos testes de produto nem PASS de CI. Não
houve rerun automático. PSEF01/PR #99 permanece `OPEN` e `Draft`.

**Resultado do diagnóstico:** revisão editorial local preparada; smoke formal
e `CANDIDATE_FREEZE` ainda `NOT_RUN`. É necessário resolver a indisponibilidade
dos runners/limite da conta e definir a campanha proporcional MM04 antes de
congelar uma candidata. A árvore B1 segue compartilhada e suja, com hash
anterior da skill, sem reconciliação segura nesta janela.

## Gates próprios da MM04

| Gate | Situação agora | Ação necessária |
|---|---|---|
| `MM04_SEF_READINESS` | **Preparado para revisão**, sem homologação formal. Policy L1/audit e superfícies protegidas estão declaradas; target L3 é apenas direção. | Revisar policy integrada e evidência de cada superfície no snapshot congelado; não inferir L2/L3 dos testes de conversa. |
| `MM04_PSEF_PROMPT_READINESS` e `MM05_PROMPT_CONTRACT_READY` | **Preparado para revisão editorial, sem aceite formal**. PSEF01 segue aberta; esta candidata usa o contrato integrado em `hub_padroes/prompt/template.md`, sem incorporar o draft. P1 passou nas guardas centrais com ressalvas de proveniência/policy; P2 e P2b preservam FAILs históricos; P2c passou nas guardas centrais com ressalvas de redação/formato. Os dois notebooks agora trazem o prompt preenchido exato e resposta real sanitizada na parte 3. | Revisar a qualidade editorial dos exemplos, seus hashes e limites; não transportar esse PASS conversacional à certificação MM04. Ver [roteiro](TESTE_BRIEFINGS_MM04_E1.md). |
| `PRE_CERTIFICATION_SMOKE` / `CANDIDATE_FREEZE` | **Não executados para MM04**. A PR #116 é candidata de laboratório; o B1 possui muitas alterações locais não commitadas, incluindo a skill importada. | Definir branch/escopo de sprint, atualizar refs, exigir `behind_by=0`, árvore limpa, snapshot/validator e gates focais verdes antes de congelar SHA/tree. |
| FULL proporcional, bundle lint, auditoria independente, contraditório, fechamento e revalidação final | **NOT_RUN** para MM04. | Executar somente após smoke e freeze, preservando FAILs históricos. Os testes B1 e a publicação Free não substituem estes gates. |
| Aceite humano, merge, promoção | **PENDENTE**. | Solicitar aceite sobre candidata certificada e auditada. Não promover `current_level` nem acessar E2 por inferência. |

O checkout B1 é compartilhado e continua com alterações simultâneas de outras
frentes. Em nova conferência, o `SKILL.md` da fonte B1 ainda tinha o hash
`cccdfb314452c44575f13a49232671acf8da16b3f3a5307049c18b37edbbfab5`;
a revisão da PR #116 não foi copiada para evitar renderizar sobre trabalho em
andamento. Nenhuma alteração alheia foi descartada; não houve commit, push ou
merge do B1 nesta reconciliação. Seu registro local está em
`docs/sprints/skill_enforcement_rollout/RECONCILIACAO_MM04_2026-09-29.md`.

## Conferência posterior da interface B1 (somente leitura)

Na retomada da revisão paralela, a fonte e o derivado B1 de `SKILL.md`,
`execution_contract.json` e `policy.json` coincidiram byte a byte com a
fonte da PR #116. O `SKILL.md` passou a SHA-256
`93e51ac4ca25f2c3bd88c6cb6a40e7e494fd9bf1852824cd4575628cf24351f2`;
o registro anterior acima documenta o estado observado **antes** dessa mudança
feita no checkout compartilhado. A linha de roteamento Micromodelos em
`.assistant_instructions.md` também coincide, embora o arquivo completo tenha
hash diferente por trabalho B1 de outras frentes. A árvore B1 segue com muitas
alterações locais; nenhuma cópia, renderização, staging ou commit B1 foi feita
por esta conferência. Revalidar hashes e estado antes de qualquer integração.
