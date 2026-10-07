<!-- Template: roteiro completo de EDA (skill hub-ml-eda-profissional) -->

# Roteiro EDA — Checklist por aplicabilidade

Selecionar itens pertinentes ao pedido e ao contrato da [skill](../SKILL.md).
Reaproveitar evidência do mesmo snapshot/run já produzida pela rota canônica;
não repetir scans/contagens por ritual. Registrar fonte, estado e motivo de
NÃO EXECUTADO ou NÃO APLICÁVEL. Itens opcionais não dispensam `run_enforced`,
Receipt, handoff, Postflight e `completion.authorized=true` reverificado.
Bloqueio canônico não autoriza continuar manualmente este checklist.

## 🎯 Etapa 0 — Contexto da Análise

> Define objetivo, escopo e premissas da exploração.

- [ ] Tabela ou DataFrame analisado: `[CATALOGO].[SCHEMA].[TABELA]`
- [ ] Objetivo da EDA declarado.
- [ ] Unidade de análise (uma linha = ?) definida.
- [ ] Período de referência declarado.
- [ ] Premissas listadas.
- [ ] Limitações listadas.
- [ ] Cuidados de segurança/governança definidos.

## 📐 Etapa 1 — Inventário Inicial

> Reconhece estrutura, volume, tipos e perfil geral dos dados.

- [ ] Volume obtido pela rota canônica, com fonte e recorte; distinguir contagem de estimativa
- [ ] Schema observado e tipos conferidos, sem repetir exibição se já registrada.
- [ ] Tipos de colunas categorizados (numéricas, categóricas, datas, booleanas).
- [ ] Comentários de tabela e colunas recuperados (Unity Catalog).
- [ ] Amostra controlada exibida (`display(df.limit(N))`).
- [ ] Resumo adicional somente se necessário, suportado e autorizado; registrar amostra/custo ou N/A.

## 🔑 Etapa 2 — Granularidade e Chaves

> Identifica o que representa uma linha e valida unicidade.

- [ ] Significado de uma linha definido.
- [ ] Candidatas a chave primária identificadas.
- [ ] Cardinalidade de cada candidata medida.
- [ ] Duplicidades por chave de negócio investigadas.
- [ ] Múltiplas linhas por entidade (cliente/contrato/etc.) investigadas.

## ✅ Etapa 3 — Qualidade de Dados

> Diagnostica nulos, duplicatas, outliers e inconsistências.

- [ ] % nulos por coluna.
- [ ] % preenchimento.
- [ ] Duplicidades por chave.
- [ ] Colunas constantes (variância zero) identificadas.
- [ ] Colunas quase vazias segundo limite definido no estudo e significado dos nulos.
- [ ] Tipos inconsistentes detectados.
- [ ] Datas inválidas/fora de domínio detectadas.
- [ ] Valores negativos inesperados detectados.
- [ ] Categorias raras identificadas.
- [ ] Outliers numéricos identificados (IQR ou desvio-padrão).
- [ ] Inconsistências temporais detectadas.

## 📊 Etapa 4 — Análise Univariada

> Distribuição individual de cada variável numérica, categórica e temporal.

**Numéricas**:
- [ ] count, mean, stddev, min, max.
- [ ] Percentis 1/5/25/50/75/95/99.
- [ ] Histogramas.
- [ ] Boxplots (quando aplicável).

**Categóricas**:
- [ ] Cardinalidade.
- [ ] Top categorias por frequência.
- [ ] Frequência absoluta e relativa.
- [ ] Concentração (Pareto/Gini).
- [ ] Categorias raras.

**Datas**:
- [ ] Mínimo e máximo.
- [ ] Cobertura temporal (volume por dia/mês).
- [ ] Lacunas temporais.
- [ ] Sazonalidade simples.

## 🔗 Etapa 5 — Análise Bivariada e Multivariada

> Correlações, relações entre variáveis e com o target.

- [ ] Numérica × numérica (correlação, scatter sobre amostra).
- [ ] Categórica × numérica (boxplot, média por categoria).
- [ ] Categórica × categórica (tabela cruzada, heatmap).
- [ ] Variável × tempo (séries temporais).
- [ ] Variável × segmento (métrica por grupo).
- [ ] Relação com target (se houver).
- [ ] Riscos de leakage (se houver modelagem).

## 🎨 Etapa 6 — Visualizações

> Visuais pertinentes ao contrato, com Plotly quando disponível e útil.

- [ ] Matriz de gráficos consultada.
- [ ] Agregação prévia em Spark feita.
- [ ] Plotly aplicado para gráficos interativos do relatório.
- [ ] Visualizações nativas usadas onde a agregação no backend é vantajosa.
- [ ] Limitações de cada gráfico declaradas.

## 🛠️ Etapa 7 — Recomendações Técnicas

> Tratamentos, features candidatas e riscos para modelagem.

- [ ] Colunas a manter / descartar.
- [ ] Tratamento de nulos.
- [ ] Tratamento de outliers.
- [ ] Ajuste de tipos.
- [ ] Padronização de categorias.
- [ ] Features candidatas.
- [ ] Necessidade de enriquecimento.
- [ ] Riscos para modelagem.
- [ ] Necessidades de governança.

## 📈 Etapa 8 — Relatório Executivo

> Síntese final com achados, impactos e próximos passos.

- [ ] Resumo executivo.
- [ ] Escopo.
- [ ] Qualidade geral.
- [ ] Estrutura e granularidade.
- [ ] Principais padrões.
- [ ] Anomalias.
- [ ] Implicações para negócio.
- [ ] Implicações para modelagem.
- [ ] Recomendações.
- [ ] Próximos passos.
