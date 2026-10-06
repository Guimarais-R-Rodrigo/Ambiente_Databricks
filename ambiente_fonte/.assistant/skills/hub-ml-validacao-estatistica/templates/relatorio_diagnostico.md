# Template: Relatório Diagnóstico Consolidado

> Formato canônico do diagnóstico final emitido pela skill.
> Resume somente testes aplicáveis, distinguindo executados, não executados e
> não suportados pela rota. Se o pedido foi só planejamento, manter NÃO EXECUTADO.
> Recomendação técnica depende do estimando, do critério e da evidência; registrar
> decisor/aprovação separadamente. Não presumir Core + Suite completos.

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

| Código/teste aplicável | Estado | Resultado e evidência | Severidade/critério |
|---|---|---|---|
| [teste selecionado] | [EXECUTADO/NÃO EXECUTADO/NÃO SUPORTADO] | [estatística, efeito e fonte; ausentes ficam pendentes] | [critério aprovado ou NÃO CLASSIFICADO] |

Inaplicáveis ficam em registro separado com motivo, fora da contagem de testes
executados. Listar também falhas e execução parcial; não herdar resultado de
um plano, de exemplo sintético ou de outro run. IC/power só quando calculados
e suportados; no piloto KS, IC é UNSUPPORTED_IN_PROFILE.

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
| **Estimando e critério** | {{ESTIMANDO_CRITERIO_E_AUTORIDADE}} |
| **Decisor/aprovação** | {{RESPONSAVEL_E_ESTADO_OU_PENDENTE}} |
| **Próximo passo** | {{PROXIMO_PASSO}} |

---

### Conexão com pipeline

| Se decisão = | Próxima etapa |
|---|---|
| ✅ GO técnico | Próxima etapa somente dentro do escopo e autorização aplicáveis |
| 🟡 CONDICIONAL | Propor mitigações e reavaliar pela rota autorizada; GO não é garantido |
| 🔴 NO-GO | Resolver violações críticas → usar `@hub-ml-feature-engineering` ou `@hub-ml-eda-profissional` |

---

*Gerado por `hub-ml-validacao-estatistica` v{{VERSION}} | {{DATA}}*
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
