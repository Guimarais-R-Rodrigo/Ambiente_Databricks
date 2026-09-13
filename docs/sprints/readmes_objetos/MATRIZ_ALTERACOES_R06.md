# Matriz nominal de alterações — R06

**Base fixa:** `cae94988cda66a8c61ecebbe6ceed487120a76f2`
**Escopo funcional:** cinco objetos `hub_snippets/ml` marcados como R06/lote A no controle de migração.
**Regra:** implementação e fachada permanecem byte a byte iguais; notebooks podem receber somente Markdown, backlinks e correções editoriais, preservando AST Python, magics executáveis e outputs históricos.

## Novos READMEs canônicos

| Caminho | Papel |
|---|---|
| `ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/README.md` | auto-ARIMA, seleção de ordem, métricas in-sample, dependências e intervalos não retornados. |
| `ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/README.md` | features temporais pandas, entidade, ordenação, warm-up e semântica por observação. |
| `ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/README.md` | Prophet, tendência/sazonalidade/feriados, métricas in-sample e grão agregado. |
| `ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/README.md` | corte temporal por períodos observados, gaps e entidade inédita. |
| `ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/README.md` | folds expansivos, callback de modelagem, gaps e estabilidade temporal. |

## Notebooks de exemplo — somente documentação

| Caminho | Mudança permitida R06 |
|---|---|
| `.../arima_wrapper/exemplo_arima_wrapper.py` | backlink; qualificar seleção automática, estacionariedade, ordem escolhida e horizonte. |
| `.../lgbm_temporal/exemplo_lgbm_temporal.py` | backlink; corrigir “exige entidade”, pré-ordenação e alertar que o bloco “sem entidade” diverge da política atual de duplicatas. |
| `.../prophet_wrapper/exemplo_prophet_wrapper.py` | backlink; qualificar métrica in-sample, feriados em mensal, componentes e heurística de ciclos. |
| `.../split_temporal/exemplo_split_temporal.py` | backlink; esclarecer três partições, percentuais por período observado, gaps e entidade inédita. |
| `.../walk_forward/exemplo_walk_forward.py` | backlink; deixar explícito que o callback treina, que gap usa períodos observados e que quantidade de folds deve ser validada. |

Nenhum bloco de output histórico `# MAGIC ```text ... ````, linha Python executável ou magic executável deve mudar.

## Documentação transversal prevista — além dos READMEs de objeto

| Caminho | Alteração R06 |
|---|---|
| `ambiente_fonte/.assistant/hub_snippets/README.md` | adicionar rotas R06 e corrigir papel de `lgbm_temporal` para geração de features, sem alegar treino LightGBM. |
| `ambiente_fonte/.assistant/MANUAL_TECNICO.md` | rota operacional para escolha entre feature engineering, split, walk-forward, ARIMA e Prophet. |
| `MANUAL_TECNICO.md` | sincronizar cópia de leitura com o Manual canônico. |
| `README.md` | registrar continuidade R06 e contagem derivada do validador. |
| `CLAUDE.md` | checkpoint aditivo R06. |
| `PLANO_HUB.md` | checkpoint aditivo R06. |
| `docs/sprints/README.md` | rota/estado R06. |
| `docs/sprints/readmes_objetos/README.md` | estado, cobertura, evidências e próxima parada. |
| `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json` | retirar exatamente cinco pendências R06; esperado 32 restantes. |
| `CHANGELOG.md` | entrada aditiva R06, preservando histórico. |
| `docs/sprints/readmes_objetos/ACHADOS_R06.md` | registrar limitações e divergências encontradas. |
| `docs/sprints/readmes_objetos/RELATORIO_R06.md` | consolidar método, testes, documentação não-README e gate editorial. |
| `docs/sprints/readmes_objetos/RUBRICA_R06.json` | critérios de autorrevisão técnica. |
| `docs/sprints/readmes_objetos/evidencias_r06/verificar_r06.py` | caracterização estática/runtime dos cinco objetos. |
| `docs/sprints/readmes_objetos/evidencias_r06/verificar_preservacao.py` | prova de não alteração funcional e monotonicidade da migração. |

## Derivados

As cópias correspondentes em `Novo_Ambiente_Simulado/Users/usuario-free/` devem ser geradas exclusivamente por `tools/render_simulado.py --write`. Não são autoria paralela e não podem ser editadas manualmente.

## Fora de escopo

- alterar algoritmo, assinatura, defaults, import ou fachada dos cinco objetos;
- fazer `lgbm_temporal` treinar LightGBM nesta sprint;
- corrigir o bloco executável histórico do notebook `lgbm_temporal`; a divergência será documentada e preservada;
- adicionar regressoras ao Prophet ou devolver `conf_int` no ARIMA;
- transformar os helpers pandas em Spark;
- mudar a semântica de períodos observados para calendário contínuo;
- instalar dependências permanentes no produto;
- publicar/homologar no Databricks;
- declarar auditoria independente;
- iniciar R07 antes do aceite editorial da R06.
