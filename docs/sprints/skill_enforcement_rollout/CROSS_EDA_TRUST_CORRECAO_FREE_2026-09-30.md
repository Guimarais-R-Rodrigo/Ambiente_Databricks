# Cross-EDA: correção de confiança publicada no Free

(Codex) Em 2026-09-30, a [rodada RQ-TRUST-COMBINED/T01](genie_evidencias/RQ-TRUST-COMBINED_T01.md)
expôs uma falha comportamental: a resposta tratou `valid=true` hipotético
como prova de execução/integridade e confundiu `stage_level` com os níveis da
policy. T01 permanece FAIL parcial; uma alteração posterior não reescreve o
resultado original.

Foi editado **somente**
`ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/SKILL.md` no produto:
agora separa diagnóstico estático L3 da rota PIT L4, nível do perfil de
`current_level`/`target_level` da policy, e texto colado de output de
verificador conferido. O derivado foi regenerado pelo renderer. Policy,
runner, Receipt, verifier, MM04 e controller não mudaram.

| Etapa | Resultado e limite |
|---|---|
| Identidade fonte antes/depois | árvore Git `.assistant` `af738a9a897abcbf0474c90bb8a87c0e46e93ad8` → `5d9024df92da0edb9f0fbc8762c63bdbccbda3ee`, commit de produto `e0780ae2bb2d6ce79751f6be5e3125d47b84b2ff` |
| Validação local | `validate_assistant.py` 0 falhas/avisos; 24 testes SE05 PASS; fonte e derivado byte a byte iguais para a skill; `git diff --check` do commit PASS |
| Preflight Free | leitura do arquivo exato em `FREE`: hash normalizado anterior `567196fcb69b02494d5d0c8a25299b4b510453d5deebd029404d5785d8038b9f`, igual ao produto anterior; nenhum objeto MM lido/escrito por este publicador |
| Escrita delimitada | `workspace import --format RAW --overwrite` só para `.assistant/skills/hub-ml-cross-eda-ml/SKILL.md` na pasta pessoal; o CLI devolveu `rc=1`, portanto o ACK é **falho/incerto** |
| Reconciliação do efeito | Readback imediato após o ACK falho e segunda leitura independente coincidiram com o novo hash normalizado `c6f24a49d2a53400e8a0e7197252729f2d9bfaf1bce4c8567c8f24fb30397c9a`. Na segunda chamada de publicação, estado `ALREADY_MATCH`, `write_attempted=false` |

Relatórios completos ficam locais e ignorados pelo Git:
`.artifacts/skills-delivery-evidence/cross-skill-trust-free-publish-20260930-attempt1.json`
(SHA-256 `3d84d6a51c708d72836e02518f655d8916dcb0533bd356090a55b1cce35d159e`)
e `.artifacts/skills-delivery-evidence/cross-skill-trust-free-publish-20260930.json`
(SHA-256 `085ea726aada493b51eb7062585c10fb1109bb1593aa05f11d7a4ac621c74a7d`).
O script local de uma única rota também está ignorado. O readback comprova
o conteúdo normalizado naquele arquivo após a tentativa; não transforma o
ACK falho em sucesso de transporte nem comprova que a Genie leu os bytes
novos em um chat.

No commit documental anterior, os 14 checks do PR #117 falharam **antes de
iniciar jobs** por bloqueio de cobrança/limite de gastos da conta GitHub,
segundo as anotações dos checks; `se02` foi `SKIPPED`. Isso não é falha de
teste do produto, mas o CI desta revisão está indisponível até mudança
externa. Os checks de commits anteriores tinham passado e os testes locais
acima foram executados nesta correção.

**Próximo passo:** abrir chat Genie novo e repetir o mesmo prompt
RQ-TRUST-COMBINED, preservando a primeira resposta e o indicador separado.
Somente essa nova resposta pode avaliar o comportamento após a correção.
Ela também não apaga os FAILs anteriores de Safra/Cross-EDA ou fecha o G6
congelado. Sem PASS dirigido e sem resolver os outros FAILs materiais,
homologação integral continua pendente.
