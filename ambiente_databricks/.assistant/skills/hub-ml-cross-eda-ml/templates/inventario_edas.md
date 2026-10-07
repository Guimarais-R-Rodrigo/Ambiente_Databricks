<!-- Template: inventário padronizado dos EDAs de entrada (skill hub-ml-cross-eda-ml) -->

# 📋 Etapa 1 — Inventário dos EDAs

Preencher com fonte/versão e evidência de cada EDA consultada. Sem observação,
registrar NÃO INFORMADO; sem execução, NÃO EXECUTADO. Semáforo exige critério
aprovado, não mera presença do relatório. Este inventário não executa joins.

| Campo | Fonte A | Fonte B | Fonte C |
|---|---|---|---|
| **Tabela** | `[catalog.schema.tabela_a]` | `[catalog.schema.tabela_b]` | `[catalog.schema.tabela_c]` |
| **Notebook EDA** | `[caminho_notebook_a]` | `[caminho_notebook_b]` | `[caminho_notebook_c]` |
| **Granularidade** | [1 linha = ?] | [1 linha = ?] | [1 linha = ?] |
| **Volume** | [N linhas] | [N linhas] | [N linhas] |
| **Período** | [data_min — data_max] | [data_min — data_max] | [data_min — data_max] |
| **Chave candidata (PK)** | [coluna] | [coluna] | [coluna] |
| **Qualidade geral** | [✅/🟡/🔴] | [✅/🟡/🔴] | [✅/🟡/🔴] |

## Principais achados por fonte

### Fonte A — `[nome descritivo]`

1. [Achado 1 da EDA]
2. [Achado 2 da EDA]
3. [Achado 3 da EDA]

**Limitações identificadas**: [listar]
**Relevância para ML**: [1-2 linhas: por que esta fonte é útil para o modelo]

### Fonte B — `[nome descritivo]`

1. [Achado 1 da EDA]
2. [Achado 2 da EDA]
3. [Achado 3 da EDA]

**Limitações identificadas**: [listar]
**Relevância para ML**: [1-2 linhas]

### Fonte C — `[nome descritivo]`

1. [Achado 1 da EDA]
2. [Achado 2 da EDA]
3. [Achado 3 da EDA]

**Limitações identificadas**: [listar]
**Relevância para ML**: [1-2 linhas]

## Resumo comparativo

| Dimensão | Melhor fonte | Observação |
|---|---|---|
| Volume | [X] | [justificativa] |
| Qualidade | [X] | [justificativa] |
| Cobertura temporal | [X] | [justificativa] |
| Diversidade de variáveis | [X] | [justificativa] |
| Proximidade com target | [X] | [justificativa] |

---

> **Nota**: Adicionar ou remover colunas conforme o número de fontes.
> Para 4+ fontes, considerar formato vertical (1 seção por fonte)
> em vez de tabela horizontal.
