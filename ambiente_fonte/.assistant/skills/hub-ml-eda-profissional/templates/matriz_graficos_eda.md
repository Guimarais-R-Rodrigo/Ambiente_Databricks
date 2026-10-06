<!-- Template: matriz de visualizações para EDA (skill hub-ml-eda-profissional) -->

# Matriz de gráficos para EDA no Databricks

Use esta matriz para escolher a visualização adequada ao tipo de variável,
ao objetivo e ao volume de dados.

## Por tipo de variável

### Numérica isolada

| Visualização | Quando usar | Ferramenta sugerida |
|--------------|-------------|---------------------|
| Histograma | Distribuição geral, identificar assimetria | Plotly, native, matplotlib |
| Boxplot | Dispersão, mediana, outliers | Plotly, matplotlib |
| Tabela de percentis | Estatísticas descritivas precisas | `df.summary` + display |
| Density plot | Forma fina da distribuição | Plotly, seaborn¹ |

### Categórica isolada

| Visualização | Quando usar | Ferramenta sugerida |
|--------------|-------------|---------------------|
| Barras horizontais (top N) | Cardinalidade alta, top categorias | native (com agregação), Plotly |
| Tabela de frequência | Distribuição precisa | `groupBy + count + display` |
| Pareto | Concentração (regra 80/20) | Plotly |

### Data / temporal

| Visualização | Quando usar | Ferramenta sugerida |
|--------------|-------------|---------------------|
| Série temporal (linha) | Volume por dia/mês | native (com agregação), Plotly |
| Heatmap mês × ano | Sazonalidade | Plotly |
| Distribuição por dia da semana | Padrão semanal | native |
| Cobertura (gantt) | Lacunas temporais | Plotly |

### Numérica × numérica

| Visualização | Quando usar | Ferramenta sugerida |
|--------------|-------------|---------------------|
| Scatter plot | Relação direta entre duas variáveis | Plotly (sobre amostra) |
| Hexbin / 2D density | Volume grande, scatter ilegível | Plotly, matplotlib |
| Matriz de correlação | Visão geral de várias variáveis | Plotly heatmap, seaborn¹ |
| Pair plot | Múltiplas relações simultâneas | seaborn¹ (sobre amostra) |

### Categórica × numérica

| Visualização | Quando usar | Ferramenta sugerida |
|--------------|-------------|---------------------|
| Boxplot por categoria | Comparar distribuições | Plotly, native |
| Barras de média/mediana | Comparar tendência central | native (com agregação) |
| Violin plot | Comparar distribuições com forma | Plotly, seaborn¹ |
| Ranking de segmentos | Top N categorias por métrica | native |

### Categórica × categórica

| Visualização | Quando usar | Ferramenta sugerida |
|--------------|-------------|---------------------|
| Tabela cruzada | Frequências exatas | `groupBy + pivot + display` |
| Heatmap | Padrão visual de frequência | Plotly, seaborn¹ |
| Mosaico / treemap | Hierarquia e proporção | Plotly |
| Stacked bar (proporção) | Composição relativa | Plotly, native |

### Variável × target binário

| Visualização | Quando usar | Ferramenta sugerida |
|--------------|-------------|---------------------|
| Taxa do target por categoria | Detectar segmentos discriminantes | native (com agregação) |
| Distribuição da variável por classe | Diferença entre classes | Plotly |
| Lift por faixa | Capacidade preditiva da variável | Plotly |
| Missing rate por classe | Possível leakage de missing | native |

## Por contexto banking / CRM

### Análise de clientes

- **Métrica por segmento**: barras horizontais com média/mediana por
  cluster/perfil.
- **Métrica por faixa de renda/saldo/score**: heatmap ou barras com
  agrupamento ordenado.
- **Distribuição por canal de aquisição**: pizza ou barras verticais.

### Análise de campanhas

- **Conversão por canal**: barras com taxa de conversão.
- **Conversão ao longo do tempo**: linha temporal.
- **Funil de campanha**: gráfico de funil (Plotly).

### Análise de safras

- **Cohort retention**: heatmap de retenção por safra × período.
- **Métrica por safra**: linhas múltiplas no tempo.
- **Box plot por safra**: distribuição de variável-chave por mês de coorte.

### Análise de jornada

- **Sankey de transições**: fluxo entre status (Plotly).
- **Tempo médio em cada etapa**: barras com duração média.
- **Distribuição de status atual**: pizza ou barras.

## Princípios gerais

1. **Agregar antes de plotar**, sempre que possível.
2. **Para grandes volumes**, amostrar com seed fixa para reprodutibilidade.
3. **Gráficos do relatório executivo**: usar Plotly quando a interatividade ajudar e a rota estiver disponível.
4. **Gráficos de inspeção rápida**: visualizações nativas + display são
   suficientes.
5. **Acessibilidade**: títulos, legendas e eixos claros; paleta com
   contraste adequado.
6. **Truncar** categorias/séries quando houver muitas (top N + "outros").
7. **Não usar** gráfico de pizza com mais de 5–6 categorias; preferir
   barras horizontais.
8. **Documentar** no Markdown PÓS o que cada gráfico revela.

## Notas sobre disponibilidade de bibliotecas

- **Seaborn, Matplotlib e Plotly**: confirmar presença e versão no Environment,
  runtime e compute aprovados. Nenhuma biblioteca é presumida disponível em
  todos os ambientes; import estático no exemplo não comprova instalação.
- Se faltar dependência, registrar a lacuna e usar somente o mecanismo de
  instalação permitido, com autorização e pins exigidos pelo projeto. Não
  instalar automaticamente por copiar esta matriz.
- Preferir Plotly quando a interatividade ajudar e a biblioteca estiver
  disponível; escolher tabela ou outra visualização suportada quando bastar.
- SHAP/Matplotlib e Kaplan–Meier mantêm as limitações temáticas documentadas
  no [guia visual](estilo_visual_eda.md).
