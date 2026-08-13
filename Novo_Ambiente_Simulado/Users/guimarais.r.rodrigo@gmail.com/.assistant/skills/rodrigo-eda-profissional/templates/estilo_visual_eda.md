# Estilo Visual — Padrão EDA Profissional

Este arquivo centraliza todas as decisões estéticas para notebooks de EDA.
Ambas as skills (`rodrigo-eda-profissional` e `rodrigo-comentar-notebook`)
devem seguir estas convenções.

---

## 1. Paleta de Cores

Paleta principal (6 cores) para gráficos Plotly e referências em Markdown:

| Índice | Nome         | Hex       | Uso principal                          |
| ------ | ------------ | --------- | -------------------------------------- |
| 1      | Azul CAIXA   | `#005CA9` | Barras primárias, linhas principais    |
| 2      | Laranja      | `#F7941D` | Destaque, alertas, segunda série       |
| 3      | Azul Claro   | `#6CBDE1` | Preenchimento, áreas, séries terciárias |
| 4      | Cinza Escuro | `#333333` | Texto, eixos, linhas de referência     |
| 5      | Verde        | `#8DC63F` | Positivo, aprovado, meta atingida      |
| 6      | Vermelho     | `#C4262E` | Negativo, risco, meta não atingida     |

Paleta estendida (para >6 categorias):
`#005CA9`, `#F7941D`, `#6CBDE1`, `#333333`, `#8DC63F`, `#C4262E`,
`#7B2D8B`, `#00A79D`, `#F15A29`, `#A7A9AC`

---

## 2. Template Plotly Reutilizável

Todo notebook de EDA deve inicializar o tema visual numa célula de
configuração (logo após os imports):

```python
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

# === CONFIGURAÇÃO VISUAL ===
PALETA_EDA = ["#005CA9", "#F7941D", "#6CBDE1", "#333333", "#8DC63F", "#C4262E"]

TEMA_EDA = dict(
    template="plotly_white",
    font=dict(family="Segoe UI, Roboto, sans-serif", size=12, color="#333333"),
    title=dict(font=dict(size=16, color="#005CA9"), x=0.01, xanchor="left"),
    colorway=PALETA_EDA,
    height=450,
    width=900,
    margin=dict(l=60, r=30, t=70, b=60),
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
)

def aplicar_tema(fig, subtitulo=None, fonte=None, n=None):
    """Aplica tema padrão + anotações opcionais."""
    fig.update_layout(**TEMA_EDA)
    
    anotacoes = []
    if subtitulo or fonte or n:
        texto_rodape = []
        if n:
            texto_rodape.append(f"N = {n:,.0f}")
        if fonte:
            texto_rodape.append(f"Fonte: {fonte}")
        if subtitulo:
            texto_rodape.append(subtitulo)
        fig.add_annotation(
            text=" | ".join(texto_rodape),
            xref="paper", yref="paper",
            x=0, y=-0.18, showarrow=False,
            font=dict(size=10, color="#666666"),
            xanchor="left"
        )
    return fig
```

### Regras de uso:

- **Sempre** chamar `aplicar_tema(fig, ...)` antes de `fig.show()`.
- **Subtítulo** vai como anotação inferior (não no título principal).
- **Título**: frase curta e objetiva (≤60 chars). Sem "Gráfico de...".
- **Formato do título**: `"Distribuição de X por Y"` ou `"Top N — Métrica"`.

---

## 3. Regras de Gráficos

### 3.1 Anotações obrigatórias

Todo gráfico do relatório final (Etapa 6) deve ter:
- **Rodapé** com N amostral e fonte (via `aplicar_tema`).
- **Pelo menos 1 anotação de destaque** no corpo do gráfico para o
  achado principal (ex.: seta apontando para pico, texto com o valor
  máximo, linha de referência para mediana).

### 3.2 Tamanhos padrão

| Tipo de gráfico   | height | width |
| ----------------- | ------ | ----- |
| Padrão (bar, line)| 450    | 900   |
| Pie chart         | 400    | 600   |
| Heatmap           | 500    | 900   |
| Boxplot           | 450    | 800   |
| Small multiples   | 300    | 400   |

### 3.3 Quando usar cada ferramenta

| Ferramenta              | Quando usar                                      |
| ----------------------- | ------------------------------------------------ |
| `createVisualization`   | Exploração rápida sobre resultados de `display()` |
| Plotly                  | Relatório final, gráficos do corpo da EDA        |
| Matplotlib              | Gráficos estáticos simples (se Plotly for overkill) |
| Visualização nativa     | Tabelas com agregação no backend (>64k linhas)   |

---

## 4. Emojis Padronizados

Uso **limitado e semântico** — nunca decorativo.

| Emoji | Significado                | Contexto de uso                    |
| ----- | -------------------------- | ---------------------------------- |
| ✅    | Validação passou / OK      | Checks de qualidade                |
| ❌    | Validação falhou / erro    | Checks de qualidade                |
| ⚠️    | Atenção / risco moderado   | Pontos de atenção                  |
| 🟢    | Status positivo            | Indicadores de qualidade           |
| 🟡    | Status intermediário       | Indicadores de qualidade           |
| 🔴    | Status crítico             | Indicadores de qualidade           |
| 📌    | Insight-chave / destaque   | Interpretação de negócio           |
| 📊    | Resultado factual          | Cabeçalho de seção de dados        |
| 🔍    | Interpretação / análise    | Cabeçalho de seção interpretativa  |
| 💼    | Visão de negócio           | Cabeçalho de seção executiva       |
| ➡️    | Próximo passo              | Transição entre etapas             |

**Máximo**: 3 emojis por célula Markdown. Nunca em títulos `##`.

---

## 5. Formato de Números

| Tipo              | Formato Python         | Exemplo          |
| ----------------- | ---------------------- | ---------------- |
| Inteiro grande    | `{:,.0f}`              | 3.375.674        |
| Monetário (BRL)   | `R$ {:,.2f}`           | R$ 29.516,15     |
| Percentual        | `{:.1f}%` ou `{:.2f}%`| 92,8% ou 12,29%  |
| Razão / taxa      | `{:.4f}`               | 0,9998           |
| Contagem pequena  | `{:,}` (sem decimal)   | 54               |

Em tabelas Markdown: usar separador de milhar com ponto (padrão BR).
Exemplo: `3.375.674` (não `3,375,674`).

---

## 6. Tabelas Markdown

### Regras de formatação:

- **Máximo 6 colunas** por tabela. Se precisar mais → quebrar em 2 tabelas.
- **Alinhar números à direita** quando possível (Databricks nem sempre
  renderiza alignment, mas manter a convenção).
- **Nomes de coluna**: curtos, sem redundância com o título da tabela.
- **Negrito** apenas para destaques semânticos (não para toda a coluna).
- **Backticks** para nomes técnicos: `` `valor_pago` ``.
- **Truncar texto longo**: máximo 40 chars por célula.

### Padrão de tabelas de resultado:

```markdown
| Métrica | Valor | Status |
| --- | ---: | :---: |
| Total de linhas | 3.375.674 | 🟢 |
| PK única | 99,998% | 🟡 |
| Nulos | 0% | 🟢 |
```

---

## 7. KPI Card — Linha de Impacto

Toda célula PÓS-código deve **abrir** com uma linha de KPIs de impacto
rápido (scan de 2 segundos):

```markdown
> **3,37M** propostas | **22** colunas | **0%** nulos | **54** duplicatas
```

Regras:
- Usar blockquote (`>`) com **negrito** nos valores.
- Máximo **4-5 KPIs** por linha.
- Separador: ` | ` (pipe com espaço).
- Números formatados conforme seção 5.
- Unidades abreviadas quando possível (M, k, bi, %).

---

## 8. Output de Código (prints)

Substituir `print("="*60)` por formato limpo com box-drawing:

```python
def exibir_secao(titulo, subtitulo=None):
    """Exibe cabeçalho de seção formatado no output."""
    largura = 60
    print(f"\n┌{'─' * (largura - 2)}┐")
    print(f"│ {titulo:<{largura - 4}} │")
    if subtitulo:
        print(f"│ {subtitulo:<{largura - 4}} │")
    print(f"└{'─' * (largura - 2)}┘")
```

Alternativa com `displayHTML` para outputs mais ricos:

```python
def exibir_html_secao(titulo, metricas=None):
    """Exibe seção como HTML estilizado."""
    html = f'''
    <div style="background:#f8f9fa; border-left:4px solid #005CA9;
                padding:12px 16px; margin:8px 0; border-radius:4px;">
        <h4 style="margin:0; color:#005CA9; font-size:14px;">{titulo}</h4>
    </div>
    '''
    if metricas:
        badges = " ".join([
            f'<span style="background:#e8f4fd; padding:4px 10px; '
            f'border-radius:12px; font-size:12px; margin-right:8px;">'
            f'<b>{v}</b> {k}</span>'
            for k, v in metricas.items()
        ])
        html += f'<div style="margin:8px 0;">{badges}</div>'
    displayHTML(html)
```

O agente deve **escolher a abordagem mais simples que atenda**:
- Se o notebook é exploratório → box-drawing com `print` é suficiente.
- Se o notebook é para apresentação → `displayHTML` para seções principais.

---

## 9. Hierarquia de Títulos Markdown

| Nível | Uso                              | Exemplo                         |
| ----- | -------------------------------- | ------------------------------- |
| `#`   | Apenas no cabeçalho do notebook  | `# EDA — Tabela X`             |
| `##`  | Etapas principais                | `## Etapa 3 — Qualidade`       |
| `###` | Subseções dentro de etapa / PÓS  | `### ✅ Resultado — Etapa 3`   |
| `####`| Tópicos dentro de PÓS           | `#### 📊 Resultado observado`  |

Nunca usar `#####` ou inferior — sinal de profundidade excessiva.

---

## 10. Separadores Visuais em PÓS

Usar `---` (horizontal rule) para separar seções semânticas dentro de
PÓS longos:

```markdown
### ✅ Resultado — Etapa N

> **KPI1** | **KPI2** | **KPI3** | **KPI4**

---

#### 📊 Resultado observado
(tabela factual)

---

#### 🔍 Interpretação técnica
(bullets com análise)

---

#### 💼 Interpretação de negócio
> (blockquote com visão executiva)

---

#### ➡️ Próximo passo
(1 linha indicando continuidade)
```

## 11. Índice de Seções (obrigatório)

Todo notebook EDA deve começar com um índice visual. O padrão oficial é usar `snippets/visual/index_generator.py`.

* Mapeamento emoji ↔ seção: definido em `snippets/constants/emojis.py`
* O índice deve listar etapa, título e descrição curta.
* O índice pode ser renderizado em HTML ou Markdown.

Exemplo de referência:

* `gerar_indice_eda()`

## 12. Section Headers (padrão por seção)

Cada seção principal da EDA deve abrir com header visual via `snippets/visual/section_header.py`.

Formato esperado:

* borda lateral azul Caixa
* emoji da seção
* título padronizado
* descrição de uma frase

A descrição padrão pode ser expandida, mas nunca omitida.

## 13. Referência de Snippets Compartilhados

| Snippet | Quando usar | Como chamar |
| --- | --- | --- |
| `theme_plotly.py` | Antes de qualquer Plotly | `registrar_template_plotly()` |
| `section_header.py` | Abertura de seção | `section_header_html(etapa=3)` |
| `kpi_card.py` | KPI cards de impacto | `kpi_card_html(metricas)` |
| `divider.py` | Separação visual | `divider_heavy()` |
| `index_generator.py` | Índice do notebook | `gerar_indice_eda()` |
| `badge.py` | Badges de score/status | `badge_score(84)` |

Nota: `estilo_visual_eda.md` documenta o padrão; a implementação opcional vive na extensão customizada `.assistant/x_snippets/` e exige import explícito.
