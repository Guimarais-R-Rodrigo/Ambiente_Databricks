# Matriz de alterações — R04-B

Base autorizada: `a8f314a31106aceb52db2661544146cc2bddcc99` (`main` após R04-A). Data: 2026-09-12.

A matriz separa autoria, documentação transversal, evidência e cópia derivada. **Não some cópias do simulado como novos objetos.** A contagem líquida final contra a base é registrada no relatório/PR depois que o renderer e os testes produzirem a árvore fechada.

## 1. Novos READMEs canônicos

| Caminho | Papel |
|---|---|
| `ambiente_fonte/.assistant/hub_scripts/data_quality_check/README.md` | Guia de qualidade ad hoc, limiares, score e custo. |
| `ambiente_fonte/.assistant/hub_scripts/doc_coverage/README.md` | Guia da heurística de adjacência Markdown-código. |
| `ambiente_fonte/.assistant/hub_scripts/drift_detector/README.md` | Guia de PSI numérico entre coortes. |
| `ambiente_fonte/.assistant/hub_scripts/naming_checker/README.md` | Guia de convenções e origem das políticas. |
| `ambiente_fonte/.assistant/hub_scripts/rfv_calculator/README.md` | Guia de RFV com corte temporal. |
| `ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/README.md` | Guia de snapshot de schema e serialização. |

## 2. Notebooks de exemplo — somente documentação

| Caminho | Alteração permitida |
|---|---|
| `.../hub_scripts/data_quality_check/exemplo_data_quality_check.py` | backlink e ajuste de prosa, sem alterar código/magics/output. |
| `.../hub_scripts/doc_coverage/exemplo_doc_coverage.py` | backlink e ajuste de prosa, sem alterar código/magics/output. |
| `.../hub_scripts/drift_detector/exemplo_drift_detector.py` | backlink e ajuste de prosa, sem alterar código/magics/output. |
| `.../hub_scripts/naming_checker/exemplo_naming_checker.py` | backlink e ajuste de prosa, sem alterar código/magics/output. |
| `.../hub_scripts/rfv_calculator/exemplo_rfv_calculator.py` | backlink e correção da inconsistência textual A16, preservando output. |
| `.../hub_scripts/schema_to_yaml/exemplo_schema_to_yaml.py` | backlink e ajuste de prosa, sem alterar código/magics/output. |

A guarda `evidencias_r04b/verificar_preservacao.py` compara AST, magics executáveis, blocos de output e linhas não-Markdown com a base.

## 3. Documentação transversal e governança

| Caminho | Motivo |
|---|---|
| `ambiente_fonte/.assistant/hub_scripts/README.md` | acrescentar rotas locais dos seis guias, sem mudar contratos dos scripts. |
| `ambiente_fonte/.assistant/MANUAL_TECNICO.md` | orientar primeiro acesso aos seis READMEs e registrar limites essenciais. |
| `MANUAL_TECNICO.md` | cópia de leitura idêntica ao Manual canônico. |
| `README.md` | atualizar continuidade da iniciativa e contagens geradas pelo validador. |
| `CLAUDE.md` | atualizar estado/rota da iniciativa sem alterar regras de outras frentes. |
| `PLANO_HUB.md` | registrar fechamento R04-A e lote R04-B em revisão. |
| `docs/sprints/README.md` | atualizar checkpoint global de sprints. |
| `docs/sprints/readmes_objetos/README.md` | atualizar estado, rotas e próxima parada. |
| `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json` | retirar exatamente as seis dispensas R04-B; nenhuma nova. |
| `CHANGELOG.md` | entrada aditiva da sprint, preservando todo histórico anterior. |

## 4. Registros novos da sprint

| Caminho | Papel |
|---|---|
| `docs/sprints/readmes_objetos/RELATORIO_R04B.md` | escopo, testes, limites e fechamento. |
| `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R04B.md` | este inventário nominal. |
| `docs/sprints/readmes_objetos/ACHADOS_R04B.md` | comportamentos/limitações caracterizados. |
| `docs/sprints/readmes_objetos/RUBRICA_R04B.json` | autorrevisão editorial/técnica, sem alegar independência. |
| `docs/sprints/readmes_objetos/evidencias_r04b/verificar_r04b.py` | casos estáticos + runtime dos seis scripts. |
| `docs/sprints/readmes_objetos/evidencias_r04b/verificar_preservacao.py` | guarda de preservação contra `a8f314a`. |

## 5. Derivados

Toda mudança em `ambiente_fonte/`, exceto `ambiente_fonte/README.md`, deve ser espelhada sob `Novo_Ambiente_Simulado/Users/usuario-free/` **somente pelo renderer**. Esses caminhos são derivados e não constituem autoria independente.

O workflow de fechamento executa `python tools/render_simulado.py --write`, verifica igualdade de bytes e materializa a árvore resultante. A matriz não lista dezenas de espelhos linha a linha porque a correspondência é determinística `ambiente_fonte/<relativo> → Novo_Ambiente_Simulado/Users/usuario-free/<relativo>` e é validada automaticamente.

## 6. Arquivos explicitamente protegidos

- Implementações `hub_scripts/<obj>/<obj>.py` dos seis scripts.
- Fachadas `hub_scripts/<obj>/__init__.py`.
- 29 READMEs de objeto/exemplares anteriores à R04-B.
- `skills/`, `hub_padroes/`, assets, `tools/`, workflows permanentes, ADRs, sistema de temas e formulários de prompts.
- `ambiente_fonte/.assistant_instructions.md`.

Qualquer divergência nesses grupos reprova a guarda, salvo caminhos agregadores declarados nesta matriz.