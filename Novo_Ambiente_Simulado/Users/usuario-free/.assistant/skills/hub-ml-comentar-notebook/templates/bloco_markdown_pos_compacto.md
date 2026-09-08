# Template: PÓS-código Compacto

Usar quando o resultado for **simples e direto** (etapa não-crítica,
resultado binário, ou continuação de bloco anterior já documentado).

**Critério**: resultado cabe em ≤15 linhas de Markdown.

---

## Estrutura

```markdown
### ✅ Resultado — [Nome da Etapa/Bloco]

> **KPI1** valor | **KPI2** valor | **KPI3** valor

- Achado principal em 1-2 linhas.
- Impacto ou ação decorrente em 1 linha.

➡️ **Próximo**: [1 linha indicando continuidade]
```

---

## Exemplo real

```markdown
### ✅ Resultado — Validação de Constantes

> **0** colunas constantes | **0** quase-vazias

- Nenhuma coluna com variância zero ou preenchimento < 5%.
- Base sem redundância trivial — todas as colunas têm valor analítico potencial.

➡️ **Próximo**: Análise de outliers (IQR)
```

---

## Quando usar este template

- Validações que passaram sem achados (“tudo OK”).
- Blocos intermediários que são continuação de uma etapa já documentada.
- Schema, printSchema, amostra simples.
- `dbutils.data.summarize` (o próprio output já é autoexplicativo).

## Quando NÃO usar (preferir template completo)

- Resultado com anomalias ou riscos.
- Resultado que exige interpretação de negócio.
- Etapas críticas (Qualidade, Granularidade, Bivariada).
- Visualizações que precisam de leitura interpretativa.
