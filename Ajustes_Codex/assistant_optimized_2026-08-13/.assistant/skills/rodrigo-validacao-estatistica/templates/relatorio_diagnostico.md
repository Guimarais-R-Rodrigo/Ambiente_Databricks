# Template: Relatório Diagnóstico Consolidado

> Formato canônico do diagnóstico final emitido pela skill.
> Posicionado após execução de todos os testes (Core + Suite específica).
> Resume resultados, emite decisão e prescreve ações.

---

## Estrutura completa

```markdown
## 📊 Diagnóstico Consolidado — Validação Estatística

### Visão geral

| Métrica | Valor |
|---|---|
| **Dataset** | `{{TABELA}}` |
| **Método pretendido** | {{METODO}} |
| **Modo** | {{MODO}} |
| **Suite(s) executada(s)** | {{SUITES}} |
| **Total de testes** | {{N_TOTAL}} |
| **Data** | {{DATA}} |

---

### Resultado por teste

| # | Código | Teste | Resultado | Severidade |
|---|---|---|---|---|
| 1 | C1 | Duplicidade PK | {{RESULTADO}} | {{BADGE}} |
| 2 | C2 | Missingness Pattern | {{RESULTADO}} | {{BADGE}} |
| 3 | C3 | Cardinalidade Extrema | {{RESULTADO}} | {{BADGE}} |
| 4 | C4 | Near-Zero Variance | {{RESULTADO}} | {{BADGE}} |
| 5 | C5 | Correlação/Redundância | {{RESULTADO}} | {{BADGE}} |
| 6 | C6 | Class Imbalance | {{RESULTADO}} | {{BADGE}} |
| 7 | C7 | Power Analysis | {{RESULTADO}} | {{BADGE}} |
| 8+ | {{COD}} | {{TESTE_SUITE}} | {{RESULTADO}} | {{BADGE}} |

---

### Contagem por severidade

```text
✅ OK:       {{N_OK}} testes
🟡 Atenção:  {{N_ATENCAO}} testes
🔴 Crítico:  {{N_CRITICO}} testes
ℹ️ Info:     {{N_INFO}} testes
⏭️ Skipped:  {{N_SKIPPED}} testes
```

---

### Semáforo geral

```text
┌─────────────────────────────────────────┐
│                                         │
│   {{EMOJI}}  {{DECISAO}}                │
│                                         │
│   {{JUSTIFICATIVA_CURTA}}               │
│                                         │
└─────────────────────────────────────────┘
```

**Regras aplicadas** (registrar critérios aprovados e direção de cada métrica):

| Condição verificada | Resultado |
|---|---|
| Testes 🔴 | {{N_CRITICO}} |
| Testes 🟡 | {{N_ATENCAO}} |
| Mitigação viável para 🔴? | {{SIM_NAO}} |
| Modo | {{MODO}} |
| → Decisão | {{DECISAO}} |

---

### Prescrições

#### 🔴 Ações obrigatórias (resolver antes de prosseguir)

| # | Teste | Violação | Ação prescrita | Impacto |
|---|---|---|---|---|
| 1 | {{TESTE}} | {{VIOLACAO}} | {{ACAO}} | {{IMPACTO}} |

#### 🟡 Ações recomendadas (mitigar para robustez)

| # | Teste | Violação | Ação prescrita | Impacto |
|---|---|---|---|---|
| 1 | {{TESTE}} | {{VIOLACAO}} | {{ACAO}} | {{IMPACTO}} |

#### Sequência sugerida de resolução

> Ordenada por dependência (resolver primeiro o que desbloqueia o resto).

1. **{{PASSO_1}}** — [justificativa: por que primeiro]
2. **{{PASSO_2}}** — [justificativa]
3. **{{PASSO_3}}** — [justificativa]

---

### Decisão final

| | |
|---|---|
| **Semáforo** | {{EMOJI}} {{DECISAO}} |
| **Justificativa** | {{JUSTIFICATIVA_COMPLETA}} |
| **Condições** | {{CONDICOES}} (se CONDICIONAL) |
| **Próximo passo** | {{PROXIMO_PASSO}} |

---

### Conexão com pipeline

| Se decisão = | Próxima etapa |
|---|---|
| ✅ GO | Prosseguir para modelagem / análise |
| 🟡 CONDICIONAL | Aplicar mitigações → reexecutar `@rodrigo-validacao-estatistica` → GO |
| 🔴 NO-GO | Resolver violações críticas → usar `@rodrigo-feature-engineering` ou `@rodrigo-eda-profissional` |

---

*Gerado por `rodrigo-validacao-estatistica` v{{VERSION}} | {{DATA}}*
```

---

## Regras de preenchimento

1. **Toda decisão deve ser justificada** — nunca emitir GO/NO-GO sem explicar.
2. **Prescrições devem ser acionáveis** — técnica + referência à implementação.
3. **Sequência de resolução** respeita dependências (ex.: resolver duplicatas antes de correlação).
4. **Se modo = Inferência e há 🔴**: decisão é sempre NO-GO (sem exceção).
5. **Se modo = Diagnóstico e há 🔴 com mitigação**: decisão pode ser CONDICIONAL.
6. **Formatação BR**: números grandes no padrão brasileiro.
7. **Badges**: usar snippet `badge()` quando disponível.
8. **Conexão com pipeline**: sempre indicar qual etapa vem depois (ou qual revisitar).
