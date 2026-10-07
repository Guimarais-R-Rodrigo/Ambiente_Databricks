# Template: Estrutura do Notebook de Saída

> Define a estrutura completa do notebook `StatCheck_<contexto>` gerado pela skill.
> Cada seção corresponde a um bloco de células no notebook, selecionado pelo
> objetivo, estimando e pressupostos. Este molde é um plano, não garantia de
> execução de todas as suites. Marcar NÃO EXECUTADO, NÃO SUPORTADO ou N/A com motivo.
> O perfil `TWO_SAMPLE_KS_PILOT_V1` aceita somente dados realmente sintéticos,
> alfa pré-especificado e entradas confirmadas. Usar preflight → runner → verifier
> com request, run_id e oráculo independentes; IC é `UNSUPPORTED_IN_PROFILE`.
> Nenhuma seção deste molde amplia esse perfil nem autoriza bypass.

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

### Bloco 2 — Configuração e dependências (plano)

Registrar perfil, versões, seed quando houver amostragem, alfa confirmado,
limite de coleta e orçamento. Não aplicar ALPHA=0.05 silenciosamente nem fixar
amostra universal. Confirmar bibliotecas suportadas antes de gerar uma célula.

Usar helpers/imports canônicos da rota. Se um import obrigatório falhar,
registrar bloqueio e corrigir a dependência pela via autorizada; não redefinir
`safe_display`, badge, tema ou qualquer helper para contornar falha. Visuais
opcionais indisponíveis podem ser omitidos com motivo, sem registrar template
global ou criar paleta/função local. Consultar o
[contrato visual](../../../hub_padroes/identidade_visual/README.md).

Pseudocódigo de preparação (não é implementação):
```text
confirmar perfil, origem dos dados, pergunta, estimando e parâmetros
verificar dependências e usar os entrypoints canônicos aplicáveis
preservar estados de bloqueio e registrar o que não foi executado
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

### Bloco 5 — Diagnósticos Core aplicáveis

> Para cada teste selecionado de C1-C7, com justificativa:
> - 1 célula Markdown PRÉ (explicação — template `test_result_card.md`)
> - 1 célula código (execução)
> - 1 célula Markdown PÓS (resultado — template `test_result_card.md`)

```markdown
## 🧪 Core — Testes selecionados

> Listar somente diagnósticos pertinentes ao desenho e suportados pela rota.
> Separar plano, execução e resultados; não executar todos por ritual.
```

### Bloco 6 — Suite Específica

> Para cada teste aplicável e suportado da suite selecionada:
> - Mesmo padrão PRÉ/código/PÓS da Core Suite

```markdown
## 🎯 Suite Específica: {{SUITE_NOME}}

> Testes de pressupostos específicos para {{METODO}}.
> Execução somente se houver rota suportada e autorização; scipy/statsmodels não são fallback do perfil fechado.
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

1. **Plano e código executável são distintos**: pseudocódigo identificado; quando execução for autorizada, usar rota suportada, parâmetros confirmados e evidência real.
2. **Código segue PySpark-first** — scipy/statsmodels apenas quando necessário (com amostragem).
3. **Nenhum `display()` irrestrito** — usar `safe_display()` com limite.
4. **Identidade visual** — usar snippets compartilhados (badges, sections, tema Plotly).
5. **Formatação BR** — números grandes no padrão brasileiro (3.456.789 / 92,8%).
6. **Se diagnóstico aplicável detectar bloqueante** — parar a etapa dependente. Em qualquer falha de preflight/runner/verifier, preservar bloqueio; não continuar por código paralelo.
