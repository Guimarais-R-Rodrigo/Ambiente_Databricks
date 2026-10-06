# Template: Test Plan (Plano de Testes)

> Estrutura proposta sob demanda pela skill `hub-ml-validacao-estatistica`.
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

### Core de qualidade (menu de diagnósticos; selecionar por relevância)

| # | Código | Teste | Justificativa | Prioridade | N amostra |
|---|---|---|---|---|---|
| 1 | C1 | Duplicidade PK | Sanidade — unidade de análise | 🔴 Bloqueante | N total |
| 2 | C2 | Missingness Pattern | Quantificar ausência por grupo/tempo; mecanismo causal não inferido de contagem | [conforme risco] | [N e estratégia] |
| 3 | C3 | Cardinalidade Extrema | Categóricas problemáticas | 🟡 Média | N total |
| 4 | C4 | Near-Zero Variance | Features sem informação | 🟡 Média | N total |
| 5 | C5 | Correlação/Redundância | Pares redundantes (Spearman) | 🟡 Média | {{N_SAMPLE}} |
| 6 | C6 | Class Imbalance | Balanceamento do target | 🟠 Alta | N total |
| 7 | C7 | Power Analysis (se suportado) | Planejar precisão/potência com alternativa, desenho e alfa | [conforme decisão] | [dados do planejamento] |

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

1. **Core**: selecionar somente testes pertinentes ao objetivo, desenho, estimando e pressupostos; inaplicáveis ficam identificados com motivo.
2. **Suite específica**: planejar conforme a demanda; executar somente rota/perfil disponível. Os rótulos da tabela não comprovam suporte pelo runner.
3. **N amostra** declara o tamanho usado para cada teste (ou "N total" se sem amostragem).
4. **Prioridade** segue a hierarquia: Bloqueante > Alta > Média > Info.
5. **Observações** incluem limitações conhecidas, decisões de escopo ou ressalvas.
6. Se múltiplas suites forem aplicáveis, listar ambas como plano e registrar quais são suportadas.
7. Definir H0/H1, alfa pré-especificado, efeito mínimo relevante, família de testes e multiplicidade antes de analisar resultados. Sem dados/execução, manter NÃO EXECUTADO; não inventar amostra ou tempo estimado.
8. MCAR/MAR/MNAR são hipóteses sobre o mecanismo de ausência. Taxa de nulos ou contraste descritivo não os identifica por si só.
9. No perfil TWO_SAMPLE_KS_PILOT_V1, somente comparação KS sintética única pré-registrada; multiplicidade N/A justificada e IC UNSUPPORTED_IN_PROFILE. Não usar a tabela como autorização para outras suites.
