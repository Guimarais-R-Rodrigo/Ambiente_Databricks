# Template: Estrutura do Notebook de Saída

> Define a estrutura completa do notebook `StatCheck_<contexto>` gerado pela skill.
> Cada seção corresponde a um bloco de células no notebook.

---

## Nomenclatura

`StatCheck_<Contexto>` — exemplos:
- `StatCheck_Churn_Previdencia`
- `StatCheck_Regressao_Captacoes`
- `StatCheck_Serie_Poupanca`
- `StatCheck_ANOVA_Segmentos`

---

## Estrutura completa

### Bloco 1 — Header e Configuração

```markdown
# 🔬 Validação Estatística — {{CONTEXTO}}

> **Skill**: `hub-ml-validacao-estatistica`
> **Modo**: {{MODO}} (Diagnóstico / Inferência)
> **Suite(s)**: {{SUITES}}
> **Dataset**: `{{TABELA}}`
> **Objetivo**: {{OBJETIVO}}
> **Data**: {{DATA_EXECUCAO}}
> **Autor/owner**: {{OWNER}}

---

## 📑 Índice

1. [Configuração e Imports](#config)
2. [Inventário do Dataset](#inventario)
3. [Test Plan](#test-plan)
4. [Core Suite](#core-suite)
5. [Suite Específica: {{SUITE}}](#suite-especifica)
6. [Diagnóstico Consolidado](#diagnostico)
7. [Prescrições e Próximos Passos](#prescricoes)
8. [Relatório Executivo](#relatorio)
```

### Bloco 2 — Configuração e Imports (código)

```python
# --- Configuração ---
# Snippets visuais são opcionais; o notebook permanece executável sem hub_snippets.
try:
    from hub_snippets.visual.theme_plotly import registrar_template_plotly, aplicar_tema
    from hub_snippets.visual.badge import badge_status
    from hub_snippets.visual.section_header import section_header_html
    from hub_snippets.visual.kpi_card import kpi_card_html
    from hub_snippets.spark.safe_display import safe_display
    registrar_template_plotly()
except ImportError:
    def aplicar_tema(fig, **kwargs):
        fig.update_layout(template="plotly_white")
        return fig

    def badge_status(texto, tipo="info"):
        return f"[{tipo.upper()}] {texto}"

    def section_header_html(etapa=None, emoji="📌", titulo="Seção", descricao=""):
        return f"## {emoji} {titulo}\n\n{descricao}"

    def kpi_card_html(metricas):
        return " | ".join(f"{label}: {value}" for label, value in metricas.items())

    def safe_display(df, limit=1000, msg=True):
        if msg:
            print(f"Exibindo no máximo {limit} linhas (fallback sem hub_snippets).")
        display(df.limit(limit))

# Bibliotecas estatísticas
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np
import pandas as pd

# PySpark
from pyspark.sql import functions as F

# Configurações globais
SEED = 42
ALPHA = 0.05
SAMPLE_SIZE_DEFAULT = 50_000
```

### Bloco 3 — Inventário do Dataset (Markdown + código)

```markdown
## 📦 Inventário do Dataset

| Campo | Valor |
|---|---|
| **Tabela** | `{{TABELA}}` |
| **Granularidade** | {{GRANULARIDADE}} |
| **Volume** | {{N_LINHAS}} linhas × {{N_COLUNAS}} colunas |
| **Target** | `{{TARGET}}` ({{TARGET_TYPE}}) |
| **Features numéricas** | {{N_NUM}} |
| **Features categóricas** | {{N_CAT}} |
| **Coluna temporal** | `{{COL_TEMPO}}` |
| **Método pretendido** | {{METODO}} |
| **Pipeline anterior** | {{PIPELINE}} (EDA / Cross-EDA / FE) |
```

### Bloco 4 — Test Plan

> Usar template `test_plan.md` para esta seção.

### Bloco 5 — Core Suite (7 testes)

> Para cada teste C1-C7:
> - 1 célula Markdown PRÉ (explicação — template `test_result_card.md`)
> - 1 célula código (execução)
> - 1 célula Markdown PÓS (resultado — template `test_result_card.md`)

```markdown
## 🧪 Core Suite — Testes Universais

> Testes que se aplicam a qualquer cenário, independente do método.
> Executados preferencialmente em PySpark nativo.
```

### Bloco 6 — Suite Específica

> Para cada teste da suite selecionada:
> - Mesmo padrão PRÉ/código/PÓS da Core Suite

```markdown
## 🎯 Suite Específica: {{SUITE_NOME}}

> Testes de pressupostos específicos para {{METODO}}.
> Executados com scipy/statsmodels sobre amostra controlada.
```

### Bloco 7 — Diagnóstico Consolidado

> Usar template `relatorio_diagnostico.md` para esta seção.

```markdown
## 📊 Diagnóstico Consolidado

### Resumo por severidade

| Severidade | Count | Testes |
|---|---|---|
| ✅ OK | {{N_OK}} | {{LISTA_OK}} |
| 🟡 Atenção | {{N_ATENCAO}} | {{LISTA_ATENCAO}} |
| 🔴 Crítico | {{N_CRITICO}} | {{LISTA_CRITICO}} |

### Decisão

| | |
|---|---|
| **Semáforo** | {{SEMAFORO}} |
| **Decisão** | {{DECISAO}} (GO / CONDICIONAL / NO-GO) |
| **Justificativa** | {{JUSTIFICATIVA}} |
```

### Bloco 8 — Prescrições

```markdown
## 💊 Prescrições e Próximos Passos

### Ações obrigatórias (🔴)

| # | Violação | Ação | Impacto esperado |
|---|---|---|---|
| 1 | {{VIOLACAO}} | {{ACAO}} | {{IMPACTO}} |

### Ações recomendadas (🟡)

| # | Violação | Ação | Impacto esperado |
|---|---|---|---|
| 1 | {{VIOLACAO}} | {{ACAO}} | {{IMPACTO}} |

### Sequência sugerida

1. {{PASSO_1}}
2. {{PASSO_2}}
3. {{PASSO_3}}
```

### Bloco 9 — Relatório Executivo

```markdown
## 📋 Relatório Executivo — Validação Estatística

**Dataset**: `{{TABELA}}` | **Método**: {{METODO}} | **Modo**: {{MODO}}

**Decisão**: {{SEMAFORO}} {{DECISAO}}

**Resumo**: [2-3 linhas com o principal achado e a recomendação]

**Riscos identificados**: [lista dos 🔴 e 🟡 mais relevantes]

**Próximo passo imediato**: {{PROXIMO_PASSO}}

---
*Gerado com `hub-ml-validacao-estatistica` | {{DATA}}*
```

---

## Regras de construção

1. **Toda célula de código deve ser executável e reproduzível** (seed fixa, imports no topo).
2. **Código segue PySpark-first** — scipy/statsmodels apenas quando necessário (com amostragem).
3. **Nenhum `display()` irrestrito** — usar `safe_display()` com limite.
4. **Identidade visual** — usar snippets compartilhados (badges, sections, tema Plotly).
5. **Formatação BR** — números grandes no padrão brasileiro (3.456.789 / 92,8%).
6. **Se Core Suite detectar bloqueante (C1)** — parar e não executar suite específica.
