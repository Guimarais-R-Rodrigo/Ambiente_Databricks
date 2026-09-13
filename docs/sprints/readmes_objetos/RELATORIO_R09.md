# Relatório R09 — avaliação, drift e MLOps

## Escopo

Documentar cinco objetos R09/A: `curves_plotly`, `drift_detection`, `metrics_report`, `mlflow_run` e `performance_monitor`, preservando implementação/fachada e limitando mudanças nos notebooks a backlinks/erratas Markdown explicitamente autorizadas.

## Cobertura candidata

Base integrada R08: 55/75 objetos operacionais e 20 pendências. A candidata R09 alcança **60/75 operacionais, 3/3 exemplares e 15 pendências**. O validador é a fonte de verdade estrutural; a cobertura não significa aceite editorial nem publicação no workspace.

## Alterações além dos cinco READMEs

A entrega inclui: cinco notebooks com substituições editoriais reversíveis; `README.md` raiz com checkpoint e snapshot verificável; `docs/sprints/readmes_objetos/README.md` com navegação/checkpoint; `CONTROLE_MIGRACAO.json` com retirada de exatamente cinco pendências; o registro de recuperação já presente no `CHANGELOG.md`; achados, matriz, relatório, rubrica, registro de recuperação e verificadores; e dez cópias derivadas dos cinco READMEs/notebooks no `Novo_Ambiente_Simulado`, usando o mesmo conteúdo canônico.

`MANUAL_TECNICO.md`, `CLAUDE.md`, `PLANO_HUB.md`, `docs/sprints/README.md` e o catálogo geral `hub_snippets/README.md` permanecem iguais à base integrada. Esses documentos já descrevem os objetos/categorias e não precisam de checkpoint redundante nesta leva.

## Preservação

As cinco implementações e cinco fachadas permanecem byte a byte iguais à base `d5945e04328609878f63857cc15cf5e5039b3e75`. A guarda dos notebooks reverte somente as substituições declaradas em `evidencias_r09/aplicar_r09.py` e exige que cada arquivo volte byte a byte à base; portanto código Python, magics executáveis, comentários executáveis e saídas históricas fora dessas substituições não podem derivar silenciosamente.

## Validação técnica

O preflight final **`34772841948`** passou integralmente:

- contrato README 1.0.0 e cobertura 60/75 + 3/3, 15 pendências;
- gate permanente, incluindo sistema de temas V00–V04, biblioteca, ferramentas, transição, READMEs e Concierge;
- preservação estrita: 10 implementação/fachada, 5 notebooks reversíveis, 47 READMEs anteriores e espelho publicado;
- runtime core para curvas, métricas, drift e monitor;
- runtime MLflow em backend SQLite local, sem depender do workspace Databricks;
- reconferência da `main` na mesma base.

Ambiente core observado: NumPy 2.4.6, pandas 3.0.5, scikit-learn 1.9.1, SciPy 1.17.1 e Plotly 7.0.0. Ambiente MLflow: MLflow 3.16.0, NumPy 2.4.6, pandas 3.0.5, scikit-learn 1.9.1 e SQLite local. O uso de SQLite caracteriza o wrapper; **não homologa MLflow no Databricks**.

## Recuperação de preservação

Uma construção anterior desta mesma sprint reescreveu documentação em excesso e chegou a modificar literais executáveis no exemplo MLflow. O run `34764123678` restaurou catálogo, índice e cinco notebooks a partir da base integrada antes da reaplicação pontual. Consulte `RECUPERACAO_R09.md`. Esse incidente faz parte da evidência da R09 e não deve ser apagado do histórico.

## Estado

**TECNICAMENTE APROVADA PRÉ-PR.** O preflight `34772841948` e seu artefato `10322173358` sustentam os runtimes e a preservação. A árvore final ainda precisa passar pelas CIs permanentes do PR e pelo aceite editorial do usuário antes de qualquer merge.

Não houve publicação/homologação Databricks, auditoria independente, aprovação de modelo ou início da R10.
