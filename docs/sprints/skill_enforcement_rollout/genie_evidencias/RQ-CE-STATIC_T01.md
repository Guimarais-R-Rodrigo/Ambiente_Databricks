# RQ-CE-STATIC/T01 — contexto Cross-EDA sem PIT

(Codex) Coleta recebida em 2026-09-30. [Texto integral colado pelo usuário](RQ-CE-STATIC_T01_resposta.txt),
com apenas três bytes de espaços/quebras finais removidos para versionamento.
SHA-256 original do anexo:
`85fa9ddc45d3e29151ba7a663ef1e61f020d8863f1e1323624e9552c9d82f774`;
SHA-256 da cópia versionada:
`b2b6b09dfc00ec44eb8b19d698fb7125fa201ccf713d2ca9188d93dae0db2cc0`.
O usuário confirmou **indicador separado de carregamento de
`hub-ml-cross-eda-ml`**; a linha inicial colada com o nome da skill não é,
isoladamente, essa prova. Não há export de eventos/ferramentas do chat.

## Veredito por dimensão

| Dimensão | Estado | Evidência e limite |
|---|---|---|
| Indicador da skill | OBSERVADO por relato humano | Cross-EDA apareceu separadamente; bytes internos carregados não foram conferidos |
| Contexto L2 estático | PASS do núcleo conceitual | Aceita `PIT=NOT_APPLICABLE` apenas sob a invariância declarada; distingue contexto verbal de objeto fechado para preflight |
| Campos faltantes | PASS com ressalva de precisão | Aponta `decision_at`, identidades/hash/snapshot/grão/colunas das fontes e campos do contexto. Chamou `entity_id` de implícito, embora esteja nomeado no prompt; o valor do array `entity_keys` ainda não foi formalizado. A contagem final de campos faltantes sobrepõe categorias e não deve ser usada como total auditado |
| Coverage/cardinalidade | PASS de fronteira | Não mede coverage nem executa join; menciona `c` sem atributo apenas como consequência dos IDs declarados, não como leitura executada |
| Execução/efeito | NOT_RUN | Não executa preflight, runner, Receipt, join, escrita ou verificador; não declara ML readiness |

O [schema SER05-CONTEXT-1](../../../../ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/input.schema.json)
e o [preflight](../../../../ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/scripts/preflight.py)
confirmam os campos citados. `not_applicable_reason` é opcional no JSON Schema,
mas exigido semanticamente pelo validador quando `pit=NOT_APPLICABLE`.

**Resultado:** PASS do risco específico de contexto estático sem PIT, com
ressalva menor de precisão; execução canônica `NOT_RUN`. O FAIL anterior de
[SD-CE-P-D01](SD-CE-P-D01.md), que inventou campos e narrou execução sem
outputs, continua aberto. Esta resposta não fecha o G6 congelado nem
homologa Cross-EDA integralmente.
