# Matriz nominal — integração candidata R02-I

Data: 12/09/2026. Base main: `8744157`; base R02 revisada: `5996574`.
Comparação por bytes/árvores, sem recontar cópias como novos READMEs.
`A` = acrescentado; `M` = modificado; `D` = ausente/renumerado; `=` = idêntico.
Os nomes históricos continuam nos registros datados. A comparação usa caminhos,
não a heurística de rename do Git: a renumeração pode aparecer como D + A.

Contra a main: **135 caminhos**. Contra a R02 revisada: **76 caminhos**.
A união abaixo inclui também conteúdo do Concierge já existente na main,
para tornar sua preservação visível; essas linhas com `=` na primeira coluna
não são alterações do novo PR. Uma linha herdada não é uma edição produzida
nesta micro-sprint. A entrada da própria matriz é ajuste R02-I.

| Caminho | Main | R02 | Categoria | Procedência |
|---|---|---|---|---|
| `.claude/CLAUDE.md` | M | = | Outra documentação | R01/R02 preservado |
| `.claude/rules/docs-e-readmes.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `.github/workflows/ci.yml` | M | = | CI | R01/R02 preservado |
| `.github/workflows/kit-transicao-trabalho.yml` | M | = | CI | R01/R02 preservado |
| `CHANGELOG.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `CLAUDE.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `MANUAL_TECNICO.md` | M | M | Cópia sincronizada do Manual | Sincronização da autoria canônica |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md` | M | M | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/README.md` | M | M | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/README.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/notebook/template.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/prompt/analisar_campanha/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/prompt/analisar_campanha/analisar_campanha.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/prompt/analisar_campanha/exemplo_analisar_campanha.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/prompt/template.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/readme/checklist_objeto.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/readme/template.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/readme/template_objeto.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/script/checar_base_campanha/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/script/checar_base_campanha/exemplo_checar_base_campanha.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/script/template.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/snippet/taxa_resposta_campanha/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/snippet/template.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_prompts/README.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_prompts/eda_rapida/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_prompts/eda_rapida/eda_rapida.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_prompts/eda_rapida/exemplo_eda_rapida.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_scripts/README.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_scripts/quick_profile/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/README.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/constants/format_br/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/isolation_forest/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/isolation_forest/exemplo_isolation_forest.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/train_xgboost/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/ml/train_xgboost/exemplo_train_xgboost.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/spark/pit_join/README.md` | A | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/README.md` | = | M | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/README.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/SKILL.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/docs/arquitetura_e_decisao.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/docs/fontes.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/docs/instalacao_testes_promocao.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/references/composicao.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/references/descoberta.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/references/exemplos.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/templates/handoff.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/templates/recomendacao.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/templates/registro_busca.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/tests/README.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/tests/RESULTADOS.md` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/tests/casos_aceite.json` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/tests/test_validador.py` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-concierge/tests/validar_pacote.py` | = | A | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-criar-objeto/SKILL.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md` | M | = | Derivado — renderer | Regenerado; não é nova autoria |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant_instructions.md` | M | M | Derivado — renderer | Regenerado; não é nova autoria |
| `PLANO_HUB.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `README.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `ambiente_fonte/.assistant/MANUAL_TECNICO.md` | M | M | Outra documentação | Composição automática revisada |
| `ambiente_fonte/.assistant/README.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `ambiente_fonte/.assistant/hub_padroes/README.md` | M | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/notebook/template.py` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/analisar_campanha.md` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/exemplo_analisar_campanha.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/prompt/template.md` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md` | A | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/readme/template.md` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md` | A | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/exemplo_checar_base_campanha.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/script/template.md` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_padroes/snippet/template.md` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_prompts/README.md` | M | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_prompts/eda_rapida/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_prompts/eda_rapida/eda_rapida.md` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_prompts/eda_rapida/exemplo_eda_rapida.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_scripts/README.md` | M | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_scripts/quick_profile/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/README.md` | M | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/constants/format_br/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/exemplo_isolation_forest.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/exemplo_train_xgboost.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/spark/pit_join/README.md` | A | = | README (existente na frente de origem) | R01/R02 preservado |
| `ambiente_fonte/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py` | M | = | Notebook (documentação herdada da R02) | R01/R02 preservado |
| `ambiente_fonte/.assistant/skills/README.md` | = | M | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/SKILL.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/arquitetura_e_decisao.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/fontes.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/instalacao_testes_promocao.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/references/composicao.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/references/descoberta.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/references/exemplos.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/templates/handoff.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/templates/recomendacao.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/templates/registro_busca.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/README.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/RESULTADOS.md` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/casos_aceite.json` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/test_validador.py` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/validar_pacote.py` | = | A | Outra documentação | Main/Concierge preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md` | M | = | Outra documentação | R01/R02 preservado |
| `ambiente_fonte/.assistant_instructions.md` | M | M | Outra documentação | Composição automática revisada |
| `ambiente_fonte/README.md` | M | = | Outra documentação | R01/R02 preservado |
| `docs/README.md` | M | = | Outra documentação | R01/R02 preservado |
| `docs/decisions/ADR-0004-declaracao-explicita-de-helpers.md` | = | M | Outra documentação | Main/Concierge preservado |
| `docs/decisions/ADR-0011-concierge-hub.md` | = | A | Outra documentação | Main/Concierge preservado |
| `docs/decisions/ADR-0011-readmes-de-objeto.md` | = | D | Outra documentação | Main/Concierge preservado |
| `docs/decisions/ADR-0012-readmes-de-objeto.md` | A | A | Outra documentação | Ajuste/registro da R02-I |
| `docs/decisions/README.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `docs/playbooks/testes-genie-trabalho.md` | = | M | Outra documentação | Main/Concierge preservado |
| `docs/sprints/README.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/ACHADOS_R01.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/ACHADOS_R02.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/CHECKPOINT_INTEGRACAO_R02.md` | A | A | Outra documentação | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/CHECKPOINT_R01.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/CHECKPOINT_R02.md` | A | M | Outra documentação | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/DIAGNOSTICO_INTEGRACAO_R02.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/EVIDENCIAS_R01.json` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/EVIDENCIAS_R02.json` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/INTEGRACAO_R02.md` | A | A | Outra documentação | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R01.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R02.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/MATRIZ_INTEGRACAO_R02.md` | A | A | Outra documentação | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/PLANO_R00.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/README.md` | A | M | Outra documentação | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/RELATORIO_R01.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/RELATORIO_R02.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/REVISAO_FECHAMENTO_R02.md` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/RUBRICA_FECHAMENTO_R02.json` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias/baseline.txt` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias/gate-final.txt` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias/testes-readmes.txt` | A | = | Outra documentação | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/diagnostico_merge_r01.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/diagnostico_merge_r02.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/gate_baseline.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/gate_final.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/pilotos_reexecutados_local.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/preservacao.json` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/rotulos_xgboost.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/verificar_fechamento.py` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_fechamento_r02/verificar_preservacao.py` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_integracao_r02/gate_candidata.txt` | A | A | Controle/evidência | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/evidencias_integracao_r02/gate_main_base.txt` | A | A | Controle/evidência | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/evidencias_integracao_r02/preservacao.json` | A | A | Controle/evidência | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/evidencias_integracao_r02/render.txt` | A | A | Controle/evidência | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/evidencias_integracao_r02/validacao.txt` | A | A | Controle/evidência | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/evidencias_integracao_r02/verificar_preservacao.py` | A | A | Controle/evidência | Ajuste/registro da R02-I |
| `docs/sprints/readmes_objetos/evidencias_r02/baseline_ci.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_r02/gate_local.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_r02/pilotos_local.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_r02/render.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_r02/validacao.txt` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/sprints/readmes_objetos/evidencias_r02/verificar_pilotos.py` | A | = | Controle/evidência | R01/R02 preservado |
| `docs/testes/2026-09-12_concierge-integracao.md` | = | A | Outra documentação | Main/Concierge preservado |
| `docs/testes/README.md` | = | M | Outra documentação | Main/Concierge preservado |
| `docs/testes/forward/README.md` | = | M | Outra documentação | Main/Concierge preservado |
| `docs/testes/forward/roteiro.md` | = | M | Outra documentação | Main/Concierge preservado |
| `docs/testes/forward/template_resultados.md` | = | M | Outra documentação | Main/Concierge preservado |
| `novas_funcionalidades/CHANGELOG.md` | = | M | Outra documentação | Main/Concierge preservado |
| `novas_funcionalidades/skills/README.md` | = | M | Outra documentação | Main/Concierge preservado |
| `tools/README.md` | M | M | Outra documentação | Ajuste/registro da R02-I |
| `tools/ci_local.py` | M | M | Ferramenta/teste | Ajuste/registro da R02-I |
| `tools/project_policy.py` | = | M | Ferramenta/teste | Main/Concierge preservado |
| `tools/readme_objeto_contract.py` | A | = | Ferramenta/teste | R01/R02 preservado |
| `tools/tests/test_concierge_integracao.py` | = | A | Ferramenta/teste | Main/Concierge preservado |
| `tools/tests/test_readme_integracao.py` | A | A | Ferramenta/teste | Ajuste/registro da R02-I |
| `tools/tests/test_readme_objeto_contract.py` | A | = | Ferramenta/teste | R01/R02 preservado |
| `tools/validate_assistant.py` | M | = | Ferramenta/teste | R01/R02 preservado |

## Limites da contagem

Zero READMEs operacionais novos na R02-I. Seis pilotos e três exemplares são
carregados da R01/R02. Novos textos desta etapa são os registros de integração,
a nota administrativa e os ajustes de governança. Imagens, implementação do
Concierge e código dos helpers não foram reescritos. O verificador de
preservação usa grupos que podem se sobrepor; não some suas contagens.
