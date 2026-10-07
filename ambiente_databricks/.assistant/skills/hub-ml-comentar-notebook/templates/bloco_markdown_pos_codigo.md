# Template: PÓS-código Completo

Usar para blocos **críticos** que exigem interpretação técnica e de
negócio (etapas de qualidade, granularidade, univariada, bivariada,
visualizações).

**Critério**: resultado exige interpretação material. A extensão segue o risco e a utilidade, sem quota de linhas. Sem execução, registrar NÃO EXECUTADO; com execução parcial, preservar falha, resultados efetivos e limites.

---

## Estrutura padrão

```markdown
### Resultado — Etapa N: [Nome] | `STATUS: NÃO EXECUTADO` | `RISCO: NÃO INFORMADO`

> **KPI1** valor | **KPI2** valor | **KPI3** valor | **KPI4** valor

---

#### 📊 Resultado observado

| Métrica | Valor | Status |
| --- | ---: | :---: |
| [métrica e unidade] | [valor observado ou NÃO CALCULADO] | [critério, evidência ou NÃO CLASSIFICADO] |

---

#### 🔍 Interpretação técnica

- 🟢 **Achado positivo**: explicação.
- 🟡 **Ponto de atenção**: explicação.
- 🔴 **Risco identificado**: explicação e impacto.

---

#### 💼 Interpretação de negócio

> 📌 **Insight-chave**: frase de impacto traduzindo o resultado
> para linguagem executiva.

---

#### Checks de qualidade

- [ ] [Check aplicável, resultado e fonte; marcar só após verificação]
- [ ] [Check pendente, falhou ou não suportado; motivo e próximo passo]

---

#### Riscos remanescentes

- Risco 1 e mitigação sugerida.
- Risco 2 e mitigação sugerida.

---

#### ➡️ Próximo passo

[1 linha indicando a etapa seguinte]
```

---

## Regras de formatação

### KPI Card (quando houver métricas relevantes observadas)

- Se usado, colocar após o título em blockquote (`>`); não preencher valores ausentes.
- 4-5 KPIs máximo, separados por ` | `.
- Valores em **negrito**, unidades abreviadas (M, k, bi, %).
- Selecionar os KPIs mais relevantes (não repetir todos os números).

### Separadores (`---`)

- Usar entre **todas** as seções `####` para criar hierarquia visual.
- Não usar dentro de uma mesma seção.

### Tabelas de resultado

- Máximo 6 colunas.
- Incluir coluna de Status (🟢/🟡/🔴) quando houver critério de aceitação.
- Alinhar números à direita (`---:`).
- Números no padrão BR (ponto como separador de milhar).

### Callouts (máximo 2 por célula)

- `> 🟢 **ACHADO POSITIVO**: texto`
- `> 🔴 **RISCO IDENTIFICADO**: texto`
- `> 📌 **INSIGHT-CHAVE**: texto`
- `> 💼 **VISÃO EXECUTIVA**: texto`

### Badges de status (opcional, apenas etapas 2 e 3)

- `| \`STATUS: [observado ou NÃO EXECUTADO]\` | \`RISCO: [critério ou NÃO INFORMADO]\``
- Colocar no final do título `###`.

---

## Seções opcionais

Nem toda célula PÓS completa precisa ter **todas** as seções.
Incluir apenas as que agregam valor:

| Seção | Quando incluir |
| --- | --- |
| 📊 Resultado observado | Quando executado; caso contrário, motivo de NÃO EXECUTADO |
| 🔍 Interpretação técnica | Sempre que houver achado não-óbvio |
| 💼 Interpretação de negócio | Quando o resultado tiver implicação executiva |
| Checks de qualidade | Etapas 2 e 3 (validações) |
| Riscos remanescentes | Quando houver risco acionável |
| ➡️ Próximo passo | **Sempre** (1 linha) |

---

## Quando quebrar em 2 células

Se o PÓS ficar com >40 linhas, dividir:

1. **Célula 1 — PÓS-factual**: título + KPI card + tabela de resultado.
2. **Célula 2 — PÓS-interpretativo**: interpretação técnica + negócio +
   riscos + próximo passo.
