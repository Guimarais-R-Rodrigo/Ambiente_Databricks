<!-- Template: relatório executivo de Cross-EDA (skill rodrigo-cross-eda-ml) -->

# Relatório Executivo — Análise Cruzada para ML

| Campo | Valor |
|---|---|
| **Fontes analisadas** | [N] tabelas de [N] EDAs |
| **Entidade âncora** | [cliente / contrato / ...] |
| **Target pretendido** | [evento] ou `PENDENTE/DECISAO` |
| **Horizonte** | [N dias] ou `PENDENTE/DECISAO` |
| **Data da análise** | YYYY-MM-DD |
| **Decisão** | [🟢 GO / 🟡 CONDICIONAL / 🔴 NO-GO] (Score: [X.X]) |

## 1. Resumo executivo

[4 a 8 linhas em linguagem de negócio. Deve ser legível por um executivo
que não lerá o resto. Incluir: decisão, principal risco, principal
oportunidade e próximo passo recomendado.]

## 2. Fontes integradas

| Fonte | Tabela | Papel | Coverage | Qualidade |
|---|---|---|---|---|
| [Nome A] | `[catalog.schema.a]` | [âncora / enriquecimento / ...] | [X%] | [✅/🟡/🔴] |
| [Nome B] | `[catalog.schema.b]` | [...] | [X%] | [...] |
| [Nome C] | `[catalog.schema.c]` | [...] | [X%] | [...] |

## 3. Viabilidade de integração

- **Chave de ligação**: `[coluna]` — tipo [mesmo / mapeamento necessário]
- **Overlap (Jaccard médio)**: [0.XX] — [alta/moderada/baixa]
- **Estratégia de join**: [descrever ordem e tipo]
- **Base efetiva pós-join**: [N] entidades ([X%] da âncora)
- **Fator de explosão**: [Nenhum / X.Xx — controlado por pré-agregação]

## 4. ML Readiness Score

| Dimensão | Score | Status |
|---|---|---|
| Integrabilidade | [X]/5 | [✅/🟡/🔴] |
| Cobertura | [X]/5 | [✅/🟡/🔴] |
| Qualidade combinada | [X]/5 | [✅/🟡/🔴] |
| Diversidade de sinal | [X]/5 | [✅/🟡/🔴] |
| Profundidade temporal | [X]/5 | [✅/🟡/🔴] |
| Disponibilidade de target | [X]/5 | [✅/🟡/🔴] |
| **Score final (ponderado)** | **[X.X]/5** | **[GO/CONDICIONAL/NO-GO]** |

## 5. Principais oportunidades (o que se ganha cruzando)

1. [Feature cross-source 1: descrição + fontes envolvidas]
2. [Feature cross-source 2: descrição + fontes envolvidas]
3. [Feature cross-source 3: descrição + fontes envolvidas]

## 6. Principais riscos

| Risco | Severidade | Mitigação |
|---|---|---|
| [Risco 1 — ex.: leakage temporal] | [Alta/Média/Baixa] | [Ação proposta] |
| [Risco 2 — ex.: viés de sobrevivência] | [...] | [...] |
| [Risco 3 — ex.: inconsistência cross-source] | [...] | [...] |

## 7. Recomendações

| # | Recomendação | Tipo | Prioridade |
|---|---|---|---|
| 1 | [ação] | [integração / qualidade / modelagem / governança] | [alta/média/baixa] |
| 2 | [...] | [...] | [...] |
| 3 | [...] | [...] | [...] |

## 8. Próximos passos

1. [Ação imediata — geralmente "executar FE Plan com Modo B"]
2. [Ação de mitigação — resolver gap principal]
3. [Ação de validação — confirmar premissa pendente]

---

**Notebook fonte**: `[caminho completo do notebook Cross-EDA]`
**Input para FE**: Este relatório + scorecard servem como input direto
para `rodrigo-feature-engineering` (Modo B).
