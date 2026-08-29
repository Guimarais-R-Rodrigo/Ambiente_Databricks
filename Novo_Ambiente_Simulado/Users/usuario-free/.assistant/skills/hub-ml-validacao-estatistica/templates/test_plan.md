# Template: Test Plan (Plano de Testes)

> Gerado automaticamente pela skill `hub-ml-validacao-estatistica`.
> Apresentado no início do notebook antes da execução dos testes.

---

## Estrutura

```markdown
# 📋 Test Plan — StatCheck

## Contexto

| Campo | Valor |
|---|---|
| **Dataset** | `{{TABELA_OU_DATAFRAME}}` |
| **Objetivo** | {{OBJETIVO}} |
| **Método pretendido** | {{METODO}} |
| **Modo** | {{MODO}} (Diagnóstico / Inferência) |
| **Suite(s)** | {{SUITES}} |
| **N total** | {{N_TOTAL}} |
| **N features** | {{N_FEATURES}} ({{N_NUM}} numéricas, {{N_CAT}} categóricas) |
| **Target** | {{TARGET}} ({{TARGET_TYPE}}) |
| **Data de execução** | {{DATA}} |

---

## Testes selecionados

### Core Suite (obrigatória)

| # | Código | Teste | Justificativa | Prioridade | N amostra |
|---|---|---|---|---|---|
| 1 | C1 | Duplicidade PK | Sanidade — unidade de análise | 🔴 Bloqueante | N total |
| 2 | C2 | Missingness Pattern | Tipo de nulo (MCAR/MAR/MNAR) | 🟠 Alta | N total + amostra |
| 3 | C3 | Cardinalidade Extrema | Categóricas problemáticas | 🟡 Média | N total |
| 4 | C4 | Near-Zero Variance | Features sem informação | 🟡 Média | N total |
| 5 | C5 | Correlação/Redundância | Pares redundantes (Spearman) | 🟡 Média | {{N_SAMPLE}} |
| 6 | C6 | Class Imbalance | Balanceamento do target | 🟠 Alta | N total |
| 7 | C7 | Power Analysis | Suficiência amostral | ℹ️ Info | — |

### Suite Específica: {{SUITE_NOME}}

| # | Código | Teste | Justificativa | Prioridade | N amostra |
|---|---|---|---|---|---|
| 8 | {{COD}} | {{TESTE}} | {{JUSTIFICATIVA}} | {{PRIORIDADE}} | {{N_SAMPLE}} |
| ... | ... | ... | ... | ... | ... |

---

## Legenda de prioridade

| Nível | Significado | Se falhar... |
|---|---|---|
| 🔴 Bloqueante | Invalida análise | PARAR — resolver antes |
| 🟠 Alta | Pressuposto fundamental | Documentar + mitigar obrigatoriamente |
| 🟡 Média | Diagnóstico importante | Documentar + decidir mitigação |
| ℹ️ Info | Contexto adicional | Interpretar, sem ação obrigatória |

---

## Estimativa de execução

| Métrica | Valor |
|---|---|
| Total de testes | {{N_TESTES}} |
| Testes em PySpark nativo | {{N_SPARK}} |
| Testes com .toPandas() | {{N_PANDAS}} |
| Amostra máxima (scipy) | {{N_SAMPLE_MAX}} |
| Tempo estimado | {{TEMPO_ESTIMADO}} |

---

## Observações

- {{OBS_1}}
- {{OBS_2}}
```

---

## Regras de preenchimento

1. **Core Suite** é sempre incluída integralmente.
2. **Suite Específica** é preenchida conforme a classificação da demanda no fluxo atual da skill.
3. **N amostra** declara o tamanho usado para cada teste (ou "N total" se sem amostragem).
4. **Prioridade** segue a hierarquia: Bloqueante > Alta > Média > Info.
5. **Observações** incluem limitações conhecidas, decisões de escopo ou ressalvas.
6. Se múltiplas suites forem aplicáveis, listar ambas em seções separadas.
