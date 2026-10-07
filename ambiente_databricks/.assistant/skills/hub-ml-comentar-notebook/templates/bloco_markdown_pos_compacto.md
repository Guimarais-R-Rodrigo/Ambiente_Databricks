# Template: PÓS-código Compacto

Usar quando o resultado for **simples e direto** (etapa não-crítica,
resultado binário, ou continuação de bloco anterior já documentado).

**Critério**: resultado exige somente síntese curta, sem quota rígida de linhas. No molde vazio usar NÃO EXECUTADO; falha parcial e métricas ausentes devem permanecer visíveis.

---

## Estrutura

```markdown
### Resultado — [Nome da Etapa/Bloco] — [NÃO EXECUTADO/estado observado]

> **KPI1** valor | **KPI2** valor | **KPI3** valor

- Achado principal em 1-2 linhas.
- Impacto ou ação decorrente em 1 linha.

➡️ **Próximo**: [1 linha indicando continuidade]
```

---

## Exemplo ilustrativo fictício (não copiar como resultado observado)

```markdown
### ✅ Resultado — Validação de Constantes

> **0** colunas constantes | **0** quase-vazias

- Neste exemplo fictício, não houve coluna com variância zero nem preenchimento abaixo do corte ilustrativo de 5%.
- Essas checagens não demonstram valor preditivo, ausência de redundância ou qualidade de todas as colunas.

➡️ **Próximo**: Análise de outliers (IQR)
```

---

## Quando usar este template

- Validações que passaram sem achados (“tudo OK”).
- Blocos intermediários que são continuação de uma etapa já documentada.
- Schema, printSchema, amostra simples.
- Resumo exploratório cujo significado e limites já estejam claros no contexto.

## Quando NÃO usar (preferir template completo)

- Resultado com anomalias ou riscos.
- Resultado que exige interpretação de negócio.
- Etapas críticas (Qualidade, Granularidade, Bivariada).
- Visualizações que precisam de leitura interpretativa.
