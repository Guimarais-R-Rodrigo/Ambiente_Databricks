# Matriz de alterações R07

**Base:** `289731c79e8ed43d82b39d61cdc41ba2e69ea717`  
**Contrato:** README de objeto 1.0.0

Esta matriz é a lista nominal da R07. Qualquer caminho adicional precisa ser explicado no relatório final.

## READMEs canônicos novos

| Objeto | README |
|---|---|
| `kaplan_meier` | `ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/README.md` |
| `score_bands` | `ambiente_fonte/.assistant/hub_snippets/ml/score_bands/README.md` |
| `scorecard_builder` | `ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/README.md` |
| `survival_cox` | `ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/README.md` |
| `vintage_analysis` | `ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/README.md` |
| `woe_iv_calculator` | `ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/README.md` |

## Notebooks — somente Markdown/backlinks

| Notebook | Mudança editorial prevista |
|---|---|
| `.../kaplan_meier/exemplo_kaplan_meier.py` | backlink; corrigir afirmação de que o Plotly mostra marcas de censura; qualificar leitura do log-rank |
| `.../score_bands/exemplo_score_bands.py` | backlink; corrigir afirmação de que a direção não possui default; explicar `aprovacao_acum` como cobertura cumulativa |
| `.../scorecard_builder/exemplo_scorecard_builder.py` | backlink; trocar “chance” por odds; identificar output histórico abreviado; qualificar auditabilidade |
| `.../survival_cox/exemplo_survival_cox.py` | backlink; p≥0,05 como não rejeição; hazard ratio não causal; C-index sem corte universal |
| `.../vintage_analysis/exemplo_vintage_analysis.py` | backlink; qualificar equivalência `30 dias`/mês e células incompletas |
| `.../woe_iv_calculator/exemplo_woe_iv_calculator.py` | backlink; suavizar “IV alto = leakage”; deixar claro que o helper não faz binning |

**Guardas:** AST Python, magics executáveis, linhas não-Markdown e blocos históricos de output devem permanecer iguais à base.

## Implementações e fachadas protegidas

Os doze arquivos abaixo devem permanecer byte a byte iguais à base:

- `kaplan_meier/{kaplan_meier.py,__init__.py}`
- `score_bands/{score_bands.py,__init__.py}`
- `scorecard_builder/{scorecard_builder.py,__init__.py}`
- `survival_cox/{survival_cox.py,__init__.py}`
- `vintage_analysis/{vintage_analysis.py,__init__.py}`
- `woe_iv_calculator/{woe_iv_calculator.py,__init__.py}`

## Documentação transversal — não-README de objeto

A integração R07 deve alterar nominalmente:

- `ambiente_fonte/.assistant/hub_snippets/README.md` — rotas locais e descrição real dos seis objetos;
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md` — rota operacional R07;
- `MANUAL_TECNICO.md` — cópia idêntica do Manual canônico;
- `README.md` — continuidade R07 + contagens derivadas do validador;
- `CLAUDE.md` — checkpoint aditivo R07;
- `PLANO_HUB.md` — checkpoint aditivo R07;
- `docs/sprints/README.md` — rota/estado R07;
- `docs/sprints/readmes_objetos/README.md` — estado, cobertura e próxima parada;
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json` — retirada de exatamente seis pendências R07;
- `CHANGELOG.md` — entrada aditiva;
- `ACHADOS_R07.md`, `MATRIZ_ALTERACOES_R07.md`, `RELATORIO_R07.md`, `RUBRICA_R07.json`;
- `evidencias_r07/verificar_r07.py`, `evidencias_r07/verificar_preservacao.py` e script de integração fail-closed.

## Derivados

As cópias correspondentes em `Novo_Ambiente_Simulado/Users/usuario-free/.assistant/...` devem ser criadas/atualizadas **somente** por `tools/render_simulado.py`, nunca por edição manual.

## Fora de escopo

- alterar algoritmo, assinatura, defaults ou fachada dos seis helpers;
- corrigir outputs históricos executando/substituindo blocos colados;
- criar política de crédito/cutoff;
- publicar no Databricks;
- homologar modelo/scorecard;
- declarar auditoria independente;
- iniciar R08 antes do aceite editorial da R07.