# B1 — Pipeline Builder: esclarecimento de recuperação no Free

(Codex) Em 2026-09-30, após [RQ-PB-RECOVERY/T02](genie_evidencias/RQ-PB-RECOVERY_T02.md),
foi publicado **somente**
`.assistant/skills/hub-ml-pipeline-builder/SKILL.md` na pasta pessoal do
Databricks Free. O commit fonte foi `2d8e5f68`. O preflight confirmou objeto
remoto `FILE` e hash normalizado antigo
`9982cca1a25687d7dfa39cd94e74baef85486413bcc6dcadac13455921cde7f6`,
igual à versão anterior `e27a79d4`.

Três tentativas iniciais de import retornaram `rc=1` com readback ainda na
versão antiga; a terceira registrou erro de transporte `PROTOCOL_ERROR` na
chamada de import. Nenhuma delas foi tratada como publicada. Com
`GODEBUG=http2client=0`, configuração já usada pelos probes Free deste
repositório, uma nova tentativa guardada teve ACK `rc=0` e readback do hash
novo `5cff01d7919f9a0774c843db276bcbd59d8d297b609b707c598e02c48bb1617b`.
Uma segunda chamada independente encontrou `ALREADY_MATCH` e
`write_attempted=false`.

Relatórios finais locais e ignorados pelo Git:

| Arquivo em `.artifacts/skills-delivery-evidence/` | Estado | SHA-256 |
|---|---|---|
| `pb-recovery-skill-free-publish-20260930-success.json` | ACK e readback do novo conteúdo | `377107d602320e76840179c4e5ea3ca3f0eaba98e4159564d4ba645cbf24a0ac` |
| `pb-recovery-skill-free-publish-20260930.json` | segunda leitura, sem escrita | `ab723414a82636c86e4bc958959725d32adc8748338edb6dc72758be29860da3` |

As tentativas falhas anteriores tiveram relatórios sobrescritos pelo script;
os respectivos status e readbacks ficaram no output desta sessão. A
publicação não executou `run_delta.py`, MERGE, DROP ou probe remoto de efeito.
Readback do `SKILL.md` não prova quais bytes a Genie consumirá em outro chat.
Nenhum arquivo de micromodelos, policy, controller ou workspace corporativo
foi alterado. O PR #117 segue Draft; T02 permanece PASS focal de no-retry
com ressalva material de autoridade/primeiro passo.
