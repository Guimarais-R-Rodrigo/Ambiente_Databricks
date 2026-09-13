# Matriz nominal de alterações — R05

**Base fixa:** `d9da056c95bf5c4209b2f208de1c9a987580efe7`  
**Escopo funcional:** seis objetos `hub_snippets/ml` previstos no controle de migração.  
**Regra:** implementação e fachada permanecem byte a byte iguais; notebooks podem receber apenas Markdown/backlinks/correções editoriais, preservando AST, magics executáveis e outputs históricos.

## Novos READMEs canônicos

| Caminho | Papel |
|---|---|
| `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/README.md` | Ranking LambdaRank/NDCG, grupos e dependência MLflow de import. |
| `ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/README.md` | Embeddings categóricas + MLP e escopo binário do treinador. |
| `ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/README.md` | TPE/LightGBM, função objetivo e limites de `best_params`. |
| `ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/README.md` | TabNet, tarefas, importância global e custo. |
| `ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/README.md` | Baseline CatBoost, categóricas e efeitos de overrides. |
| `ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/README.md` | Baseline LightGBM, métricas, early stopping e defaults. |

## Notebooks de exemplo — somente documentação

| Caminho | Mudança permitida |
|---|---|
| `.../lgbm_ranker/exemplo_lgbm_ranker.py` | backlink; retirar promessa de MAP. |
| `.../mlp_embeddings/exemplo_mlp_embeddings.py` | backlink; substituir afirmações universais sobre one-hot/árvores por comparação condicional. |
| `.../optuna_lgbm/exemplo_optuna_lgbm.py` | backlink; retirar limiar universal de trials e hipérbole sobre tuning. |
| `.../tabnet_wrapper/exemplo_tabnet_wrapper.py` | backlink; qualificar feature importance e retirar afirmações universais sobre zero/ordem de escolha. |
| `.../train_catboost/exemplo_train_catboost.py` | backlink; corrigir explicação de ordered categorical statistics versus tempo real. |
| `.../train_lgbm/exemplo_train_lgbm.py` | backlink; qualificar gap, early stopping, bloco abreviado de defaults e `subsample_freq=0`. |

Nenhum bloco `# MAGIC ```text ... ````, linha Python executável ou magic executável deve mudar.

## Documentação transversal prevista

| Caminho | Alteração R05 |
|---|---|
| `ambiente_fonte/.assistant/hub_snippets/README.md` | adicionar rotas para os seis guias na categoria ML. |
| `ambiente_fonte/.assistant/MANUAL_TECNICO.md` | inserir rota operacional dos seis modelos e limites de escolha. |
| `MANUAL_TECNICO.md` | cópia de leitura idêntica à canônica. |
| `README.md` | continuidade R05 e contagens reais do validador. |
| `CLAUDE.md` | checkpoint aditivo R05. |
| `PLANO_HUB.md` | checkpoint aditivo R05. |
| `docs/sprints/README.md` | rota e estado R05. |
| `docs/sprints/readmes_objetos/README.md` | estado, cobertura e próxima parada. |
| `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json` | retirar exatamente seis pendências R05. |
| `CHANGELOG.md` | entrada aditiva, sem reescrever histórico. |

## Documentos de fechamento novos

- `RELATORIO_R05.md`
- `MATRIZ_ALTERACOES_R05.md`
- `ACHADOS_R05.md`
- `RUBRICA_R05.json`
- `evidencias_r05/verificar_r05.py`
- `evidencias_r05/verificar_preservacao.py`

## Derivados

As cópias correspondentes em `Novo_Ambiente_Simulado/Users/usuario-free/` são geradas exclusivamente por `tools/render_simulado.py --write`. Elas não representam autoria duplicada nem devem ser editadas manualmente.

## Fora de escopo

- alterar algoritmo, assinatura, defaults ou fachada dos seis objetos;
- corrigir funcionalmente `subsample_freq`, import obrigatório de MLflow ou discrepâncias de API;
- instalar dependências permanentes no produto;
- publicar no Databricks ou registrar modelos;
- iniciar R06 antes do aceite da R05;
- declarar revisão independente.
