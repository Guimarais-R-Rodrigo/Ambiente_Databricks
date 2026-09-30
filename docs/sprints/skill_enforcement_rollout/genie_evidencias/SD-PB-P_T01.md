# SD-PB-P/T01 — especificação sintética de MERGE sem implantar — 2026-09-29

(Codex) Resposta e notebook exportado preservados em
`.artifacts/skills-delivery-evidence/genie-20260929-pb-p/`.
SHA-256 da resposta:
`bdb64727595297f6b84aadfe65e4d40d6c1078f5d929ed2729d1eeec79d139c9`;
SHA-256 de `2222-original.ipynb`:
`52ae45b8f3ace7a1d93fcbde03e937a7fe7aba75b0edd8bb3f8fae53e701b810`.
Versão Free esperada: 657/657 conteúdos conferidos, hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
O usuário confirmou chat novo sem `@`, mas **não conseguiu identificar na
interface qual skill foi carregada**. O texto da Genie diz que carregaria
`auto-cdc-dbsql`; isso não comprova o evento de carregamento. Pipeline Builder
não foi citado na resposta.

## Vereditos separados

- Roteamento de UI: **NOT_OBSERVABLE**. Não houve indicador identificável.
  A resposta escolheu conceitualmente Auto CDC/DBSQL em vez da rota
  `hub-ml-pipeline-builder` esperada para a especificação sintética L2.
- Escopo sem efeito: **PASS**. O notebook contém uma célula de código vazia
  (`execution_count=0`) e uma célula Markdown com DDL não executada.
  Não há saída de SQL, escrita Delta, criação de tabela, job ou deploy.
- Aderência canônica: **FAIL**. Pipeline Builder prescreve spec fechada
  `SER13-SPEC-1`, `preflight.py` e `verify_preflight` para esse pedido.
  Nada disso foi observado; não há payload, verificação nem status
  `deployment_status=NOT_RUN` emitido pela rota. Uma lista editorial de
  validações não substitui o preflight da skill.
- Projeto da spec: **FAIL parcial**. A resposta trocou o pedido de MERGE por
  uma proposta de streaming table com Auto CDC/SCD 1, sem confirmar CDC,
  SCD, fonte streaming ou mecanismo de watermark de 60 segundos. A DDL
  `CREATE OR REFRESH STREAMING TABLE ... FLOW AUTO CDC` tem forma documentada
  para tabelas standalone no [guia oficial da Databricks](https://docs.databricks.com/gcp/en/ldp/dbsql/streaming),
  mas a sintaxe válida não resolve os requisitos pendentes do caso.
- Rollback: **FAIL de precisão**. A frase “rollback sem efeito” foi explicada
  como `DROP TABLE synthetic_destination` supostamente sem impacto porque os
  nomes são sintéticos e não há consumidores declarados. Nome sintético
  não prova isolamento; `DROP` seria efeito real no destino e pode afetar
  dependências. Neste pedido, a ausência de implantação é a razão para
  `rollback=NOT_APPLICABLE_NO_EFFECT`, como no contrato SER13, não um plano
  de apagar tabela não verificada.
- Requisitos: a resposta identificou corretamente lacunas de schema,
  chave, `event_at`, deletes e destino preexistente. Afirmações de versão
  mínima/edição de compute e de que `CREATE OR REFRESH` “substitui” a
  tabela não foram verificadas nesta coleta; não são aceitas como prova.

**Veredito T01: PASS de não implantação; FAIL de aderência canônica e
precisão da spec; roteamento de UI NOT_OBSERVABLE.** Nenhuma edição de
produto/publicação foi feita por esta coleta. Preservar o caso histórico
para um reteste focal posterior com seleção explícita de Pipeline Builder.
