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

## Usar recursos

Carregar somente os necessários:

- [templates/feature_spec_core.md](templates/feature_spec_core.md) para a spec central;
- [templates/feature_spec_risco_validacao.md](templates/feature_spec_risco_validacao.md) para risco e testes;
- [templates/feature_backlog_tiers.md](templates/feature_backlog_tiers.md) para priorização;
- [templates/feature_taxonomy_cross_source.md](templates/feature_taxonomy_cross_source.md) para múltiplas fontes;
- [templates/checklist_validacao_features.md](templates/checklist_validacao_features.md) para aceite;
- [templates/mapa_notebooks_alvo.md](templates/mapa_notebooks_alvo.md) e [templates/notebook_output_structure.md](templates/notebook_output_structure.md) para documentar o corpus.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [CATALOGO_HELPERS.md](../../CATALOGO_HELPERS.md).

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
