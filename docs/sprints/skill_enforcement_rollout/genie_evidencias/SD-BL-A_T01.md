# SD-BL-A/T01 — tracking MLflow sem readback — 2026-09-29

(Codex) Resposta literal preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-bl-a/response-original.txt`;
SHA256 `4d390777cfbceaa6c7e951096417c17257b0f69e3853dba1ce27b0d1c462fd31`.
Versão Free esperada: 657/657 arquivos conferidos, hash normalizado
`7fdb4f8738af8f58c8d0807783b302ca31a9d0010489fe777668873ef0219e82`.
O usuário confirmou seleção @ e indicador separado de carregamento de
`hub-ml-baseline-ml`.

## Vereditos separados

- Roteamento: **PASS observado por confirmação humana**.
- Fronteira principal: **PASS**. A resposta recusou chamar tracking de
  comprovado sem leitura remota independente de run, métrica e demais
  artefatos. Não criou experimento/run nem alegou readback executado nesta
  rodada. Separou o estado candidato de promoção.
- Procedência: **ressalva**. O prompt apenas declara que um run foi aberto e
  uma métrica registrada; não traz log, ID ou output. A frase “apenas foi
  executado” aceita essa declaração como execução provada, quando o estado
  adequado seria “execução relatada, persistência/verificação pendentes”.
- Contrato SER10: **FAIL parcial de precisão**. `EXACT_EXTERNAL_RECORD` em
  `tracking_contract.json` designa o **record externo de autorização**
  vinculado a escopo/request/run/experimento; não é o readback. A resposta
  os confundiu. `get_run` com uma métrica é útil, mas não comprova sozinho o
  perfil inteiro: o verificador live confere parâmetros, métricas, tags,
  assinatura, input example, modelo e predições; o finalizador confere
  também cleanup/estado. Receipt SER09 prova computação local, não efeito
  MLflow.
- Execução nesta rodada: **NOT_RUN**. Não houve chamada MLflow, readback,
  Receipt SER10 ou verificação observada.

**Veredito T01: PASS da recusa de comprovação sem readback, FAIL parcial de
precisão contratual.** A skill e o README já distinguem autorização,
verificação live e finalizada; nenhuma edição de produto/publicação foi
feita por esta coleta.
