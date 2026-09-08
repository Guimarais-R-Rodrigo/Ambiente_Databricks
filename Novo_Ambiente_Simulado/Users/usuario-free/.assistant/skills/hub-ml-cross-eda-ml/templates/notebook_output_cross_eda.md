<!-- Template: estrutura do notebook de saída (skill hub-ml-cross-eda-ml) -->

# Estrutura do Notebook de Saída — Cross-EDA ML Readiness

> Este template define a sequência de células que o agente deve criar.
> Adaptar ao número de fontes e ao risco: compacto, padrão ou expandido.

## Modo Padrão (~18–24 células)

### Célula 1 — Header [%md]
```markdown
# 🔬 Cross-EDA — ML Readiness Assessment

| Item | Valor |
|---|---|
| **Objetivo** | Avaliar viabilidade de integração de [N] fontes para [modelo/target] |
| **Data** | YYYY-MM-DD |
| **EDAs fonte** | [lista de notebooks] |
| **Entidade âncora** | [cliente / contrato / ...] |
| **Target** | [evento] ou `PENDENTE/DECISAO` |
| **Horizonte** | [N dias] ou `PENDENTE/DECISAO` |
| **Autor/owner** | [nome ou equipe fornecida] |
```

### Célula 2 — Setup visual [code]
```python
try:
    from hub_snippets.visual.theme_plotly import registrar_template_plotly, aplicar_tema
    from hub_snippets.visual.section_header import section_header_html
    from hub_snippets.constants.colors import PALETA_CATEGORICA
    registrar_template_plotly()
except ImportError:
    # Fallback autônomo: hub_snippets é uma extensão visual opcional.
    PALETA_CATEGORICA = ["#005CA9", "#F7941D", "#6CBDE1", "#333333"]

    def aplicar_tema(fig, **kwargs):
        fig.update_layout(template="plotly_white")
        return fig

    def section_header_html(etapa=None, emoji="📌", titulo="Seção", descricao=""):
        return f"## {emoji} {titulo}\n\n{descricao}"
```

### Célula 3 — Inventário dos EDAs [%md]
```markdown
## 📋 Etapa 1 — Inventário dos EDAs

[Conteúdo conforme template inventario_edas.md]
```

### Célula 4 — Resolução de Entidade [%md]
```markdown
## 🔑 Etapa 2 — Resolução de Entidade & Granularidade

### Entidade âncora: `[nome]`

| Fonte | Granularidade | Chave de ligação | Compatível? |
|---|---|---|---|
| A | [1 linha = ?] | [coluna] | [✅/🔴] |
| B | [1 linha = ?] | [coluna] | [✅/🔴] |
| C | [1 linha = ?] | [coluna] | [✅/🔴] |

### Estratégia de alinhamento
[Agregar → Juntar / Juntar direto / ...]
```

### Célula 5 — Validação de chaves [code]
```python
# === VALIDAÇÃO: overlap de chaves entre fontes ===
# [código de Jaccard/Overlap entre pares]
```

### Célula 6 — Alinhamento Temporal [%md]
```markdown
## ⏰ Etapa 3 — Alinhamento Temporal

| Fonte | Período | N datas | Frequência | Lag |
|---|---|---|---|---|
| A | [min — max] | [N] | [diária/mensal] | [D-0/D-1] |
| B | [min — max] | [N] | [diária/mensal] | [D-0/D-1] |

**Overlap temporal**: [data_inicio — data_fim] ([N meses])
**Point-in-time**: [Viável / Parcial / Inviável]
**Risco de leakage temporal**: [Baixo / Médio / Alto — justificar]
```

### Célula 7 — Timeline visual [code]
```python
# === VISUALIZAÇÃO: timeline de cobertura temporal por fonte ===
# [código Plotly com barras horizontais]
```

### Célula 8 — Join Feasibility [%md]
```markdown
## 🔗 Etapa 4 — Join Feasibility & Cobertura

[Conteúdo conforme templates join_feasibility.md e coverage_matrix.md]
```

### Célula 9 — Validação de join [code]
```python
# === VALIDAÇÃO: coverage matrix e simulação de join ===
# [código com coverage rates e perfil dos órfãos]
```

### Célula 10 — Heatmap de Coverage [code]
```python
# === VISUALIZAÇÃO: heatmap de coverage (entidade × fonte) ===
# [código Plotly com imshow]
```

### Célula 11 — Complementaridade [%md]
```markdown
## 🧩 Etapa 5 — Complementaridade de Sinal

### Famílias de sinal por fonte

| Família | Fonte A | Fonte B | Fonte C | Exclusiva de |
|---|---|---|---|---|
| Estáticas | [✅/—] | [✅/—] | [✅/—] | [fonte ou "compartilhada"] |
| Comportamentais | ... | ... | ... | ... |
| Temporais | ... | ... | ... | ... |
| Interações | ... | ... | ... | ... |
| Missingness | ... | ... | ... | ... |
| Categóricas | ... | ... | ... | ... |
| Regras | ... | ... | ... | ... |

### Valor incremental por fonte
[ranking e justificativa]
```

### Célula 12 — Qualidade Combinada [%md]
```markdown
## 🔍 Etapa 6 — Qualidade Combinada

[PSI cross-source, nulos correlacionados, consistência]
```

### Célula 13 — Validação de qualidade [code]
```python
# === VALIDAÇÃO: PSI cross-source para variáveis compartilhadas ===
# [código de cálculo de PSI]
```

### Célula 14 — Padrões Cruzados [%md]
```markdown
## 🔀 Etapa 7 — Padrões Estatísticos Cruzados

[Correlações inter-fonte, MI, paradoxo de Simpson se relevante]
```

### Célula 15 — Correlação cross-source [code]
```python
# === VISUALIZAÇÃO: heatmap de correlação cross-source ===
# [código Plotly]
```

### Célula 16 — Readiness Scorecard [%md]
```markdown
## 🎯 Etapa 8 — ML Readiness Scorecard

[Conteúdo conforme template readiness_scorecard.md]
```

### Célula 17 — Radar de Readiness [code]
```python
# === VISUALIZAÇÃO: radar chart do scorecard (6 dimensões) ===
# [código Plotly scatterpolar]
```

### Célula 18 — Recomendações-Ponte [%md]
```markdown
## 🌉 Recomendações-Ponte para Feature Engineering

### Features cross-source possíveis
[lista de features que só existem pela combinação]

### Estratégia de join recomendada
[ordem, tipo, pré-agregação]

### Gaps a resolver antes de FE
[lista priorizada]
```

### Célula 19 — Relatório Executivo [%md]
```markdown
## 📌 Relatório Executivo

[Conteúdo conforme template relatorio_executivo_cross_eda.md]
```

---

## Modo Compacto (~10–12 células)
Mesclar: Header + Inventário (1 célula), Entidade + Temporal (1 célula),
Join + Coverage (1 célula + 1 código), pular Etapas 5-7 detalhadas,
ir direto para Scorecard → Recomendações → Relatório.

## Modo Expandido (~25–30 células)
Adicionar:
- Célula de código para CADA par de fontes (Jaccard, Overlap, PSI)
- Diagrama Mermaid para fluxo de joins
- Análise de subconjuntos (ex.: "se usar só A+B sem C, o que muda?")
- Célula com cálculo de Mutual Information entre top variáveis
- Análise de paradoxo de Simpson por segmento
