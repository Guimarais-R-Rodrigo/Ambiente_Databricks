# PSEF00 — achados

Os achados abaixo são de baseline. PSEF00 não implementa correções em prompts produtivos.

| ID | Severidade | Superfície | Achado | Tratamento proposto |
|---|---|---|---|---|
| PSEF00-F01 | HIGH | `eda_rapida`, `eda_completa`, `data_quality` | Os três briefings selecionam `hub-ml-eda-profissional` e pedem/admitem código ou execução, mas não explicitam que a etapa protegida L4 deve seguir a rota canônica `run_enforced` → postflight; a skill, em contraste, proíbe rota PySpark/helper/manual paralela quando selecionada. | PSEF02 |
| PSEF00-F02 | HIGH | `auditoria_skills` | O briefing seleciona `hub-ml-auditoria-skills`, current L3, mas não menciona a sequência obrigatória preflight L2 → runner L3/Receipt antes da auditoria substantiva. | PSEF03 |
| PSEF00-F03 | MEDIUM | `hub_prompts/README.md` | A “Sinergia Triangular” atual é Prompt → Skill → Helpers. Ela não inclui a resolução de `policy.json`, `current_level` e rota vigente entre skill e helper. | PSEF01 |
| PSEF00-F04 | MEDIUM | `comparar_tabelas` | O briefing é corretamente multirrota, mas depois de escolher a skill não manda resolver a policy vigente. Isso é especialmente material quando a rota escolhida é EDA L4/enforce. | PSEF01/PSEF02 |
| PSEF00-F05 | MEDIUM | vários briefings | A frase “boa parte do que este formulário pede já tem implementação verificada” pode ser lida como implementação da skill/enforcement, embora em várias famílias a skill esteja em L0 e apenas helpers estejam implementados. | PSEF04; esclarecer “implementação de helpers” sem hardcode de nível |
| PSEF00-F06 | MEDIUM | `novo_projeto/README.md` + exemplo | `exemplo_novo_projeto.py` faz overwrite de `workspace.default.hub_exemplo_clientes`, mas o README local não alerta sobre a escrita; os outros 12 exemplos com overwrite possuem aviso explícito. | PSEF05 |
| PSEF00-F07 | LOW | notebooks de exemplo | 13/16 exemplos fazem escrita persistente de preparação. Todos separam o preparo da interação e 12/13 possuem aviso local, mas a superfície merece regra uniforme para não confundir “prompt read-only” com “notebook preparatório read-only”. | PSEF05 |
| PSEF00-F08 | INFO / NO_ACTION | `/findTables` | O achado candidato de referência legada foi refutado: `/findTables` continua capacidade oficial documentada do Genie Code em setembro de 2026. | manter; revalidar apenas se a Databricks mudar a interface |
| PSEF00-F09 | POSITIVE / PRESERVE | briefings ligados a skills L0 | Não foi observado overclaim explícito de preflight, runner, Receipt ou Postflight nos briefings L0. | preservar em PSEF04 |
| PSEF00-F10 | POSITIVE / PRESERVE | `novo_projeto` | Não há skill artificialmente forçada; o catálogo trata o briefing como transversal e posterga a skill especialista até a natureza da entrega ficar clara. | preservar |
| PSEF00-F11 | OPERATIONAL | PRs #5/#6 | PRs antigas ainda abertas tocam `hub_prompts`/`.assistant_instructions`; não fazem parte da baseline `main` e podem gerar conflito se forem retomadas/mergeadas durante a PSEF. | manter freeze em `main@17640a6a…`; rebase/reconciliação explícita se a concorrência mudar |

## Detalhamento F01 — EDA L4

A skill `hub-ml-eda-profissional` implementa hoje:
- `execution_contract.json`;
- preflight;
- core L3 com `ExecutionReceiptV1`;
- `run_enforced.py`;
- postflight/finalizer fail-closed;
- `completion.authorized=true` apenas após finalização válida.

Seu `SKILL.md` proíbe substituir a rota L4 por Python/PySpark manual, helper direto ou Receipt montado manualmente. Os briefings EDA atuais, por outro lado, ainda têm instruções como “priorize PySpark/Spark SQL” e “código executável”, sem declarar a precedência da rota canônica. Isso não prova bypass ocorrido; constitui ambiguidade de briefing suficiente para correção dirigida.

## Detalhamento F02 — auditoria L3

`hub-ml-auditoria-skills` exige preflight antes de auditoria substantiva e runner L3 após PASS. O briefing atual está metodologicamente próximo da skill, mas não referencia esses mecanismos. A correção deve apontar para a skill, não duplicar toda a lógica do contrato.

## `/findTables`: decisão de baseline

Não remover. A documentação oficial atual da Databricks lista `/findTables` como slash command do Genie Code ([Get coding help from Genie Code](https://docs.databricks.com/gcp/en/notebooks/code-assistant)) e as orientações de uso continuam recomendando contexto explícito e recursos com `@` ([Tips to improve Genie Code responses](https://docs.databricks.com/gcp/en/genie-code/tips)). O finding original foi mantido apenas como evidência de revalidação, não como débito.
