# Relatório R05 — READMEs de modelos tabulares

**Data:** 2026-09-12
**Base de partida:** `d9da056c95bf5c4209b2f208de1c9a987580efe7`
**Branch de autoria:** `codex/readmes-r05`
**Contrato:** README de objeto `1.0.0`
**Autoria/revisão:** ChatGPT, autorrevisão A0_light; sem auditor independente.

## 1. Objetivo

Documentar os seis objetos tabulares previstos para a R05 sem alterar suas implementações ou fachadas:

1. `lgbm_ranker`
2. `mlp_embeddings`
3. `optuna_lgbm`
4. `tabnet_wrapper`
5. `train_catboost`
6. `train_lgbm`

A sprint deve explicar conceito, contrato real, dependências, escolha, métricas, custo e limitações para um usuário que nunca entrou no Hub. A cobertura estrutural esperada por aritmética é 38/75 operacionais e 37 pendências, mas **somente a saída do validador da árvore final é fonte de verdade**.

## 2. Método de revisão

Cada objeto foi lido em quatro camadas: implementação, fachada pública, notebook de exemplo e fontes primárias da biblioteca/método quando necessárias. Divergências não foram resolvidas mudando algoritmo: foram registradas em `ACHADOS_R05.md` e refletidas na documentação.

O exemplar editorial usado como referência de profundidade é o README já aceito de `train_xgboost`; o template canônico 1.0.0 continua dono das quinze seções.

## 3. READMEs novos

| Objeto | Foco do guia |
|---|---|
| `lgbm_ranker` | ranking por grupos, NDCG, ausência de MAP no retorno real e import obrigatório de MLflow. |
| `mlp_embeddings` | embeddings, indexação categórica, treinador binário e limites da classe pública. |
| `optuna_lgbm` | TPE, função objetivo real, orçamento de trials, `best_params` incompleto e subsampling. |
| `tabnet_wrapper` | classificação/regressão, máscaras/importância, custo e limites de interpretação. |
| `train_catboost` | categóricas, ordered statistics, efeitos de `params_override` e escrita de arquivos. |
| `train_lgbm` | baseline, métricas, early stopping, overrides e `subsample_freq`. |

## 4. Documentação alterada além dos seis READMEs

A matriz nominal `MATRIZ_ALTERACOES_R05.md` é a lista de controle. A integração final deve alterar também:

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
- os documentos/evidências desta própria R05;
- cópias derivadas em `Novo_Ambiente_Simulado/`, somente pelo renderer.

## 5. Achados que mudam a interpretação

Os detalhes estão em `ACHADOS_R05.md`. Os pontos de maior risco são:

- MAP anunciado no ranker mas não implementado;
- dependência MLflow obrigatória já no import de `lgbm_ranker`;
- treinador MLP binário apesar de a classe expor regressão;
- `metric` do Optuna não redefinir a função objetivo em todas as tarefas;
- `best_params` do Optuna não ser configuração completa;
- `subsample` de LightGBM sem `subsample_freq` positivo;
- importância TabNet ser global/model-derived, não causal;
- ordered categorical statistics do CatBoost não equivalerem a point-in-time temporal;
- overrides de CatBoost/LightGBM poderem divergir do contrato de avaliação;
- notebooks instalarem dependências sem pin e conterem generalizações históricas que exigem correção de prosa.

## 6. Estratégia de testes

O fechamento deve executar, na **mesma árvore**:

1. gate permanente vigente do repositório;
2. V00, V01, V02 e V03;
3. `verificar_preservacao.py` contra `d9da056...`;
4. `verificar_r05.py` com dependências de ML reais, incluindo LightGBM, CatBoost, Optuna, PyTorch e pytorch-tabnet;
5. validador final com zero falhas/avisos e contagem derivada;
6. conferência de árvore antes/depois dos testes.

A suíte R05 deve diferenciar caracterização de garantia: provar que um comportamento existe não significa aprová-lo como design desejável.

## 7. Estado dos testes

**PENDENTE.** Esta seção será substituída pelo workflow de fechamento somente depois de todos os gates, preservação e testes específicos concluírem. A árvore não deve ser materializada como candidata final em caso de falha.

## 8. Critérios de aceite técnico

- seis READMEs passam pelo contrato 1.0.0;
- exatamente seis dispensas R05 saem do controle;
- implementações e fachadas dos seis objetos permanecem byte a byte iguais;
- notebooks preservam AST, magics executáveis e outputs históricos;
- todas as correções de notebook são documentais e registradas na matriz;
- READMEs anteriores permanecem intactos;
- V03 e demais trabalhos paralelos permanecem preservados;
- Manual canônico, raiz e simulado permanecem sincronizados;
- nenhuma dependência permanente é adicionada ao produto para viabilizar o teste;
- nenhuma publicação Databricks ou auditoria independente é alegada.

## 9. Parada

A sprint pausa para revisão editorial humana antes de qualquer merge ou início da R06. Aprovação estrutural ou runtime não substitui aceite do texto.
