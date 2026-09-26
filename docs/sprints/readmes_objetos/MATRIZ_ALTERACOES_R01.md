# R01 — matriz efetiva de alterações

Gerada a partir do diff contra o snapshot de trabalho, não do plano de intenção.
`A`: adicionado; `M`: modificado; `D`: removido. Derivados não contam como novos
textos de autoria. A remoção do workflow temporário é limpeza do transporte da
própria sprint, que não existe na base principal. O fechamento remoto informa
separadamente os commits de transporte e de integração.

| Caminho exato | Estado | Classe | Motivo |
|---|---|---|---|
| `.claude/CLAUDE.md` | M | Outra documentação | Roteamento para o novo contrato e para o checkpoint. |
| `.claude/rules/docs-e-readmes.md` | M | Outra documentação | Camada Objeto e regras de autoria sem duplicar o Manual. |
| `.github/workflows/ci.yml` | M | Workflow | Checkout completo para a trava histórica; permissões de CI continuam somente leitura. |
| `.github/workflows/kit-transicao-trabalho.yml` | M | Workflow | Checkout completo para a trava histórica; permissões de CI continuam somente leitura. |
| `.github/workflows/readmes-r01-snapshot.yml` | D | Workflow | Remoção do transporte temporário do snapshot. |
| `CHANGELOG.md` | M | Outra documentação | Registro datado com autoria, escopo e limites. |
| `CLAUDE.md` | M | Outra documentação | Registro da decisão candidata e da iniciativa. |
| `MANUAL_TECNICO.md` | M | Cópia sincronizada | Cópia de leitura sincronizada, sem redação independente. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/MANUAL_TECNICO.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/README.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/README.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/notebook/template.py` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/prompt/analisar_campanha/README.md` | A | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/prompt/analisar_campanha/analisar_campanha.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/prompt/analisar_campanha/exemplo_analisar_campanha.py` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/prompt/template.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/readme/checklist_objeto.md` | A | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/readme/template.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/readme/template_objeto.md` | A | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/script/checar_base_campanha/README.md` | A | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/script/checar_base_campanha/exemplo_checar_base_campanha.py` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/script/template.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/snippet/taxa_resposta_campanha/README.md` | A | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha.py` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_padroes/snippet/template.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_prompts/README.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_scripts/README.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/hub_snippets/README.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-criar-objeto/SKILL.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `Novo_Ambiente_Simulado/Users/usuario-free/.assistant_instructions.md` | M | Derivado gerado | Renderer, a partir da fonte; não editado à mão. |
| `PLANO_HUB.md` | M | Outra documentação | Ponte para a migração R00–R13, preservando o histórico. |
| `README.md` | M | README de navegação | Navegação e contagens locais reconciliadas com o gate. |
| `ambiente_fonte/.assistant/MANUAL_TECNICO.md` | M | Outra documentação | Explicação da camada Objeto com âncoras internas portáveis. |
| `ambiente_fonte/.assistant/README.md` | M | README de navegação | Explicar papel e acesso à nova camada; preservar visual e demais rotas. |
| `ambiente_fonte/.assistant/hub_padroes/README.md` | M | README de navegação | Explicar papel e acesso à nova camada; preservar visual e demais rotas. |
| `ambiente_fonte/.assistant/hub_padroes/notebook/template.py` | M | Documentação em notebook | Somente comentários/Markdown e links; AST executável preservada. |
| `ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/README.md` | A | README de exemplar novo | Explicação completa do conceito, uso, contrato e limites do exemplar. |
| `ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/analisar_campanha.md` | M | Outra documentação | Link para o README fora do bloco colável, que permanece igual. |
| `ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/exemplo_analisar_campanha.py` | M | Documentação em notebook | Somente comentários/Markdown e links; AST executável preservada. |
| `ambiente_fonte/.assistant/hub_padroes/prompt/template.md` | M | Outra documentação | Integração cirúrgica ao contrato de README de objeto; preserva responsabilidades anteriores. |
| `ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md` | A | Outra documentação | Critérios técnicos/didáticos e estados de revisão distintos. |
| `ambiente_fonte/.assistant/hub_padroes/readme/template.md` | M | Outra documentação | Integração cirúrgica ao contrato de README de objeto; preserva responsabilidades anteriores. |
| `ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md` | A | Outra documentação | Contrato único candidato: quinze seções e abertura didática. |
| `ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/README.md` | A | README de exemplar novo | Explicação completa do conceito, uso, contrato e limites do exemplar. |
| `ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/exemplo_checar_base_campanha.py` | M | Documentação em notebook | Somente comentários/Markdown e links; AST executável preservada. |
| `ambiente_fonte/.assistant/hub_padroes/script/template.md` | M | Outra documentação | Integração cirúrgica ao contrato de README de objeto; preserva responsabilidades anteriores. |
| `ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/README.md` | A | README de exemplar novo | Explicação completa do conceito, uso, contrato e limites do exemplar. |
| `ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha.py` | M | Documentação em notebook | Somente comentários/Markdown e links; AST executável preservada. |
| `ambiente_fonte/.assistant/hub_padroes/snippet/template.md` | M | Outra documentação | Integração cirúrgica ao contrato de README de objeto; preserva responsabilidades anteriores. |
| `ambiente_fonte/.assistant/hub_prompts/README.md` | M | README de navegação | Explicar papel e acesso à nova camada; preservar visual e demais rotas. |
| `ambiente_fonte/.assistant/hub_scripts/README.md` | M | README de navegação | Explicar papel e acesso à nova camada; preservar visual e demais rotas. |
| `ambiente_fonte/.assistant/hub_snippets/README.md` | M | README de navegação | Explicar papel e acesso à nova camada; preservar visual e demais rotas. |
| `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md` | M | Outra documentação | Integração cirúrgica ao contrato de README de objeto; preserva responsabilidades anteriores. |
| `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md` | M | Outra documentação | Integração cirúrgica ao contrato de README de objeto; preserva responsabilidades anteriores. |
| `ambiente_fonte/.assistant_instructions.md` | M | Outra documentação | Leitura seletiva de README, sem carregamento integral ou autorização implícita. |
| `ambiente_fonte/README.md` | M | README de navegação | Explicar papel e acesso à nova camada; preservar visual e demais rotas. |
| `docs/README.md` | M | README de navegação | Entrada para a iniciativa. |
| `docs/decisions/ADR-0011-readmes-de-objeto.md` | A | Outra documentação | Decisão proposta, aguardando aceite humano. |
| `docs/decisions/README.md` | M | README de navegação | Índice do ADR proposto; sem alterar corpos aceitos. |
| `docs/sprints/README.md` | M | README de navegação | Separa as sprints R das sprints históricas. |
| `docs/sprints/readmes_objetos/ACHADOS_R01.md` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/CHECKPOINT_R01.md` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/EVIDENCIAS_R01.json` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R01.md` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/PLANO_R00.md` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/README.md` | A | README de navegação | Explicar papel e acesso à nova camada; preservar visual e demais rotas. |
| `docs/sprints/readmes_objetos/RELATORIO_R01.md` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/evidencias/baseline.txt` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/evidencias/gate-final.txt` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `docs/sprints/readmes_objetos/evidencias/testes-readmes.txt` | A | Registro/evidência | Plano, controle de dispensas, checkpoint, achados ou log identificado pelo nome. |
| `tools/README.md` | M | Documentação de ferramentas | Guarda de READMEs, integração explícita no gate ou regressões adversariais. |
| `tools/ci_local.py` | M | Ferramenta/teste | Guarda de READMEs, integração explícita no gate ou regressões adversariais. |
| `tools/readme_objeto_contract.py` | A | Ferramenta/teste | Guarda de READMEs, integração explícita no gate ou regressões adversariais. |
| `tools/tests/test_readme_objeto_contract.py` | A | Ferramenta/teste | Guarda de READMEs, integração explícita no gate ou regressões adversariais. |
| `tools/validate_assistant.py` | M | Ferramenta/teste | Guarda de READMEs, integração explícita no gate ou regressões adversariais. |

## Revisados e preservados

Implementações e fachadas públicas dos exemplares, todos os helpers analíticos,
blocos coláveis dos prompts, imagens/identidade visual, `novas_funcionalidades/`,
ADRs aceitos e scripts de publicação foram preservados. O renderer existente foi
usado sem mudar sua lógica. Skills de tutoria/auditoria/comentário de notebook
não precisaram mudar para este contrato de autoria: não foram reescritas apenas
para aumentar a lista de entregas. `__init__.py` não recebe README próprio.

Não há aprovação de execução Databricks, publicação nem auditoria independente.
