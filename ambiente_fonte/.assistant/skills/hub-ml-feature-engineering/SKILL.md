---
name: hub-ml-feature-engineering
description: Projeta, implementa e valida features no Databricks com foco em joins point-in-time, prevenção de leakage, contratos, Feature Engineering in Unity Catalog, tabelas Delta e reuso entre treino e inferência. Usar quando pedirem feature engineering, plano/backlog de features, transformação de variáveis, feature table, encoding, WoE/IV, seleção, linhagem, materialização ou prevenção de training-serving skew.
---

# Projetar features no Databricks

## Quando esta skill se aplica

- Pedem **feature engineering, backlog de features, transformação de variáveis,
  feature table, encoding, WoE/IV, seleção, linhagem** ou materialização.
- Há risco de **leakage** ou de training-serving skew a prevenir, e o join
  point-in-time é parte do problema.

**Não cobre:** decidir se as fontes se cruzam (`hub-ml-cross-eda-ml`) nem treinar
o modelo que consome as features (`hub-ml-baseline-ml`).

## Definir o contexto de modelagem

Registrar antes de propor features:

- entidade e chave primária;
- target e horizonte;
- instante de decisão;
- data de corte e janela de observação;
- frequência de scoring;
- fontes disponíveis naquele instante;
- modo batch ou online e requisitos de latência.

Sem esses campos, trabalhar em modo exploratório e não afirmar ausência de leakage.

## Inventariar e especificar

1. Mapear fontes, granularidade, chaves e periodicidade.
2. Classificar features: identidade, perfil, comportamento, transação, relacionamento, tempo, agregação, texto ou externa.
3. Criar uma spec por feature com nome, definição, fórmula, fontes, chave, janela, event time, disponibilidade, tratamento de missing, tipo, owner e testes.
4. Marcar PII, sensibilidade, restrição de uso e justificativa de negócio.
5. Priorizar por valor, risco, custo, disponibilidade e reuso; não por complexidade estética.

## Prevenir leakage

- Exigir `feature_timestamp <= prediction_timestamp` respeitando atraso de publicação.
- Particionar lags e janelas por entidade antes de ordenar pelo tempo.
- Ajustar imputação, encoding, binning, seleção e scaling somente no conjunto de treino.
- Não usar agregação que contenha o período do target.
- Não usar status operacional criado depois da decisão.
- Testar overlap de entidades entre splits quando o caso exigir independência.
- Comparar pipeline offline e de inferência para evitar training-serving skew.

## Implementar de forma escalável

Preferir Spark SQL/PySpark e tabelas Delta governadas por Unity Catalog. Tornar transformações determinísticas, idempotentes e parametrizadas. Evitar UDF Python quando houver função Spark equivalente.

Quando houver reuso e governança, avaliar **Feature Engineering in Unity Catalog** e `FeatureEngineeringClient`. Confirmar a API na documentação oficial do cloud/runtime antes de gerar código. Não misturar exemplos legados de Workspace Feature Store com APIs de Unity Catalog sem explicar a diferença.

## Tratar técnicas condicionais

- Encoding: escolher conforme cardinalidade, algoritmo e risco de leakage.
- Target/mean encoding: calcular out-of-fold e aplicar smoothing.
- WoE/IV: usar somente quando fizer sentido para scorecard/interpretação; validar target binário, bins, estabilidade e convenção de “good/bad”. Não apresentar como exigência regulatória universal.
- PSI: usar referência fixa, missing explícito e interpretação baseada em contexto.
- VIF/correlação: usar como diagnóstico de redundância, não regra automática de exclusão.
- Embeddings/PCA: justificar custo, interpretabilidade e caminho de inferência.

## Validar

Executar testes de:

- schema, tipos, nulos e domínio;
- unicidade da chave e multiplicidade após joins;
- consistência temporal e ausência de registros futuros;
- determinismo/reprocessamento;
- paridade treino-inferência;
- distribuição por split/período;
- custo e volume;
- valor incremental out-of-time quando houver target.

## O que nunca fazer

- **Agregar sem recorte temporal.** Média histórica calculada sobre a base
  inteira inclui o período depois da decisão — é o leakage mais comum e o mais
  difícil de ver depois.
- **Reaproveitar código de treino na inferência sem conferir a janela.** É assim
  que nasce training-serving skew.
- **Renomear coluna devolvida** de uma feature já consumida: quebra sem erro de
  import, e o sintoma aparece longe da causa.
- **Encodar categoria com estatística do alvo** sem separar as dobras.
- **Materializar antes de fixar o contrato** — chave, granularidade, instante de
  validade e dono.


## Executar o perfil temporal sintético

Para o perfil `FIXED_LAG_L1_V1`, exija um request JSON sintético com `decision_at`
UTC, `window_days`, relógios `event_at`/`available_at`, atraso constante de um
dia, fronteira `LE`, entidade, IDs e grão único. Execute
`python scripts/run.py --request <arquivo.json> --run-id <id-unico>` a partir
da raiz da skill e retenha o JSON literal. O runner chama
`hub_snippets.ml.lgbm_temporal.create_temporal_features` após resolver o
preflight; o Receipt e `scripts/verify.py::verify` vinculam release, entrada,
execução e um oráculo independente. Bloqueio do preflight encerra a rota.

O resultado deste perfil contém somente lag de uma observação anterior dentro da janela elegível por
entidade, IDs elegíveis e contagem de eventos futuros, indisponíveis ou fora
da janela. `lag_1` mede observações, não dias. Uma linha elegível sem história
anterior é removida no warm-up do helper; a lista `eligible_ids` preserva o
denominador de entrada. O perfil não faz fit, PIT join nem materialização.
Disponibilidade variável, outros atrasos, Spark, treino/inferência e destino
persistente exigem contrato e prova próprios. Receipt válido não é homologação
Genie nem autorização de publicação.


## Consumir PIT verificado como feature de decisão

Para o perfil sintético COMPOSED_PIT_FEATURE_VIEW_V1, use
scripts/run_pit_features.py::compose com contexto e datasets do Cross-EDA,
Spark UTC, window_days, upstream_run_id e view_run_id distintos. O adapter
executa a rota PIT local sintética, exige Receipt, finalizador e verificação independente
do PIT, então projeta feature_value/available_at por decision_id. Retenha o
upstream_evidence completo. Confira com scripts/run_pit_features.py::verify,
fornecendo contexto, datasets, janela e IDs originais externos ao payload.
A vista só é válida se a prova PIT upstream e a projeção forem válidas.

Este perfil é uma composição da rota PIT local, com linhagem por hashes de
fontes, cutoff, janela, release upstream e IDs de Receipt/Postflight. Não
executa create_temporal_features, fit ou materialização, nem emite Receipt
próprio da skill FE. O perfil FIXED_LAG_L1_V1 acima permanece uma rota
separada de lags por entidade e observação; as duas saídas não são
intercambiáveis. Readiness ML e promoção permanecem pendentes.

## Provar materialização Delta sintética da view PIT

No perfil FREE_SYNTHETIC_PIT_FEATURE_MATERIALIZATION_V1, componha e verifique
primeiro a view PIT acima. `scripts/run_pit_materialization.py::effect_request`
revalida o Postflight Cross, os inputs externos e a projeção FE, e retorna o
request exato para `authorization.request_digest`. Uma autorização externa
fechada exige `authorized=true`, `effect=SYNTHETIC_FEATURE_MATERIALIZATION_PROBE`,
`target_table=workspace.default.skills_delivery_<32 hex>`, `run_id`, `nonce`
de 32 hex, principal esperado, catálogo `workspace`, schema `default` e
`cleanup=DROP_OWNED`. Passe a mesma evidência, inputs, autoridade e sessão Spark
UTC a `scripts/run_pit_materialization.py::execute`.

O executor compartilha o lifecycle Delta do Pipeline Builder. Cria somente
tabela nova sob propriedades de posse e proveniência, lê de volta as cinco
colunas da view (`decision_id`, `entity_id`, `decision_at`, `feature_value`,
`available_at`), repete o MERGE e observa versões via DESCRIBE HISTORY. Depois
confere posse antes de DROP e confirma ausência. O efeito fica em registro
separado do Receipt Cross; `UNKNOWN` exige inspeção humana, sem retry automático.
`BIGINT` é o tipo físico; o contrato PIT upstream limita atualmente os valores
de feature ao intervalo inteiro [-1.000.000, 1.000.000].
O perfil é uma prova sintética descartável, sem fit, publicação, materialização
de negócio, readiness ou promoção de policy. Mantenha a view read-only original
como evidência upstream e use apenas dados sintéticos.

## Usar recursos

Carregar somente os necessários:

- [templates/feature_spec_core.md](templates/feature_spec_core.md) para a spec central;
- [templates/feature_spec_risco_validacao.md](templates/feature_spec_risco_validacao.md) para risco e testes;
- [templates/feature_backlog_tiers.md](templates/feature_backlog_tiers.md) para priorização;
- [templates/feature_taxonomy_cross_source.md](templates/feature_taxonomy_cross_source.md) para múltiplas fontes;
- [templates/checklist_validacao_features.md](templates/checklist_validacao_features.md) para aceite;
- [templates/mapa_notebooks_alvo.md](templates/mapa_notebooks_alvo.md) e [templates/notebook_output_structure.md](templates/notebook_output_structure.md) para documentar o corpus.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Junção point-in-time com atraso de publicação | `hub_snippets.spark.pit_join` |
| Features de calendário | `hub_snippets.spark.date_features` |
| Lags e janelas móveis por entidade | `hub_snippets.ml.lgbm_temporal` (`create_temporal_features`) |
| WOE e Information Value | `hub_snippets.ml.woe_iv_calculator` |
| Recência, frequência e valor até data de corte | `hub_scripts.rfv_calculator` |
| Split por período de calendário para checar leakage | `hub_snippets.ml.split_temporal` |

`rfv_calculator` já exclui eventos posteriores à data de referência — não duplicar nem remover esse filtro. `extrair_features_data` cobre apenas feriados nacionais de data fixa; os demais entram por `holiday_dates`.

## Entregar

Fornecer specs, DAG lógico, código ou pseudocódigo implementável, plano de materialização, testes, riscos e backlog. Separar feature aprovada, experimental e bloqueada. Indicar como registrar linhagem e como reproduzir a feature no momento da inferência.
