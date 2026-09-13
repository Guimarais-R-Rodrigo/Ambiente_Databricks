# Relatório R07 — READMEs de score, vintage e sobrevivência

**Data:** 2026-09-12  
**Base de partida:** `289731c79e8ed43d82b39d61cdc41ba2e69ea717`  
**Branch de autoria:** `codex/readmes-r07`  
**Contrato:** README de objeto `1.0.0`  
**Autoria/revisão:** ChatGPT, autorrevisão A0_light; sem auditor independente.

## 1. Objetivo

Documentar os seis objetos previstos para a R07 sem alterar suas implementações ou fachadas:

1. `kaplan_meier`
2. `score_bands`
3. `scorecard_builder`
4. `survival_cox`
5. `vintage_analysis`
6. `woe_iv_calculator`

A sprint deve explicar conceitos de censura, hazard, score, odds, WOE/IV, safra e MOB antes da sintaxe, e delimitar claramente o que os helpers não fazem. A cobertura aritmética esperada é **49/75 operacionais e 26 pendências**, mas a saída do validador da árvore final é a fonte de verdade.

## 2. Método de revisão

Cada objeto foi lido em quatro camadas: implementação, fachada pública, notebook e documentação primária das bibliotecas quando relevante. Para `kaplan_meier`, `survival_cox` e quantis de score, foram confrontadas também as APIs atuais de `lifelines` e pandas.

Divergências não são corrigidas mudando algoritmo nesta sprint. São registradas em `ACHADOS_R07.md`, explicadas no README e, quando necessário, corrigidas apenas na prosa do notebook.

## 3. READMEs novos

| Objeto | Foco do guia |
|---|---|
| `kaplan_meier` | censura, função de sobrevivência, formato do log-rank e ausência de marcas de censura no Plotly local |
| `score_bands` | quantis, direção do score, ties, cobertura cumulativa versus aprovação real |
| `scorecard_builder` | escala log-odds/PDO, orientação do evento, ponte WOE Spark→pandas e limites da tabela de pontos |
| `survival_cox` | hazard ratio, complete-case, C-index in-sample, PH e limites de p-valores |
| `vintage_analysis` | safra/MOB, maturidade completa, snapshots ausentes e incidência acumulada |
| `woe_iv_calculator` | WOE/IV Spark, smoothing, binning externo, custos de ações e heurísticas de IV |

## 4. Documentação alterada além dos seis READMEs

Esta seção é obrigatória e faz parte do critério de aceite. A lista nominal completa está em `MATRIZ_ALTERACOES_R07.md`. A integração final deve alterar também:

- os seis notebooks `exemplo_*.py`, **somente em Markdown/backlinks e correções editoriais**;
- `ambiente_fonte/.assistant/hub_snippets/README.md`;
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md` e a cópia `MANUAL_TECNICO.md`;
- `README.md` da raiz;
- `CLAUDE.md`;
- `PLANO_HUB.md`;
- `docs/sprints/README.md`;
- `docs/sprints/readmes_objetos/README.md`;
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`;
- `CHANGELOG.md`;
- `ACHADOS_R07.md`, `MATRIZ_ALTERACOES_R07.md`, `RELATORIO_R07.md`, `RUBRICA_R07.json`;
- scripts em `docs/sprints/readmes_objetos/evidencias_r07/`;
- cópias derivadas em `Novo_Ambiente_Simulado/`, somente pelo renderer.

Nenhuma implementação/fachada dos seis objetos deve mudar.

## 5. Achados que mudam interpretação

Os detalhes estão em `ACHADOS_R07.md`. Os principais são:

- o Plotly de Kaplan–Meier não mostra marcas de censura apesar da afirmação histórica do notebook;
- log-rank para >2 grupos muda o formato de retorno e aplica Holm nos pares;
- `score_bands.higher_score_is_better` possui default `True`; direção não é exigida pela assinatura;
- `aprovacao_acum` é cobertura acumulada, não política de aprovação executada;
- scorecard constrói tabela de pontos, não pipeline completo de scoring, e arredonda pontos por faixa;
- Cox devolve C-index/AIC parcial in-sample, usa complete-case e imprime `p<0,05` sem correção múltipla;
- vintage só publica taxa em célula completamente observada e não fabrica snapshots faltantes;
- WOE/IV não faz binning e realiza ações Spark/coletas agregadas;
- faixas de IV são heurística local, não norma regulatória universal.

## 6. Estratégia de testes

O fechamento deve executar, na **mesma árvore final**:

1. gate permanente vigente do repositório;
2. V00, V01, V02 e V03;
3. `verificar_preservacao.py` contra `289731c...`;
4. `verificar_r07.py` com `lifelines` real para Kaplan–Meier/Cox e PySpark real para WOE/IV, além de pandas/NumPy/Plotly para os demais objetos;
5. validador final com zero falhas/avisos e contagem derivada;
6. conferência de árvore antes/depois dos testes;
7. materialização somente do SHA exato aprovado.

A suíte deve distinguir caracterização de aprovação de design. Um teste que comprova comportamento histórico não o transforma em recomendação.

## 7. Estado dos testes

**Pendente de freeze remoto nesta versão de autoria.** O relatório só deve ser promovido a fechamento técnico depois de registrar run, versões, contagem de testes, cobertura validada e árvore exata materializada.

## 8. Critérios de aceite técnico

- seis READMEs no contrato 1.0.0;
- exatamente seis pendências R07 retiradas do controle;
- implementações e fachadas byte a byte iguais à base;
- notebooks preservam AST, magics, linhas não-Markdown e outputs históricos;
- READMEs anteriores intactos;
- V00–V03 e trabalhos paralelos preservados;
- Manual canônico, raiz e simulado sincronizados;
- dependências de teste apenas no ambiente isolado;
- nenhuma publicação Databricks, homologação de política/modelo ou auditoria independente alegada.

## 9. Parada

Depois do fechamento técnico, a sprint deve abrir PR em **draft** e pausar para aceite editorial humano. R08 não começa e nenhum merge ocorre antes desse gate.