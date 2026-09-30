# SD-BL-MLFLOW/T01 — Receipt local versus tracking remoto — 2026-09-29

(Codex) Resposta original preservada em
`.artifacts/skills-delivery-evidence/genie-20260929-bl-mlflow/response-original.txt`;
SHA-256 `e31dc56f3dc1c91aa1b46549665fa7f2cdc24173f270dc88db685c0d15b6108f`.
Versão Free esperada: 657/657 conteúdos conferidos, hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O usuário confirmou chat novo sem `@`; indicador de skill não ficou claro.
Nenhum run, notebook ou output MLflow foi fornecido.

## Vereditos separados

- Roteamento: **NOT_OBSERVABLE**. A resposta menciona skills genéricas de
  machine learning e system tables, mas o relato não confirma indicador
  separado de `hub-ml-baseline-ml`. Texto que diz ter carregado algo não
  prova evento de carregamento.
- Fronteira de evidência: **PASS**. A resposta distinguiu Receipt local e
  nome de experimento de um run remoto comprovado; pediu run ID resolvível,
  readback de métricas e listagem do artefato. Não alegou execução presente.
- Contrato SER10: **FAIL parcial**. O perfil requer experimento pessoal novo,
  autorização vinculada a request/run/identidade, readback do modelo
  serializado com assinatura e predições, verificação live antes do cleanup,
  cleanup e `verify_finalized`. A resposta apresentou uma lista genérica de
  MLflow como se bastasse ao fluxo governado, sem vínculo com o Receipt de
  treino e sem a prova final do efeito. Também sugeriu
  `system.mlflow.tracking` como tabela/SQL de corroboração sem evidência de
  disponibilidade ou contrato dessa tabela neste workspace; não se deve
  usá-la como requisito ou prova aqui.
- Execução: **NOT_RUN**. O run remoto é hipotético; não houve readback.

**Veredito T01: PASS da distinção essencial; FAIL parcial de aderência ao
SER10; roteamento NOT_OBSERVABLE.** A skill Baseline já documenta o fluxo
governado. Nenhuma edição de produto/publicação foi feita nesta coleta.
