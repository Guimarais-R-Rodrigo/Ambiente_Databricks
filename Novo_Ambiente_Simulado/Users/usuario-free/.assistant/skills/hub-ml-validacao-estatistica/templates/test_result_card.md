# Template: Test Result Card

> Formato canônico para apresentação de cada teste no notebook de saída.
> Cada teste gera **2 células**: 1 Markdown (explicação) + 1 código (execução),
> seguidas de 1 Markdown (resultado/interpretação).
>
> Preencher somente o que o perfil suporta e a evidência sustenta. Sem execução,
> manter o resultado pendente; contas didáticas devem ser identificadas como
> ilustrativas. Campo ausente não recebe valor padrão por conveniência. No
> piloto KS, IC permanece `UNSUPPORTED_IN_PROFILE`; desenho declarado não é
> pressuposto comprovado. Campos não aplicáveis exigem motivo, não número fictício.

---

## Card PRÉ-execução (célula Markdown antes do código)

```markdown
---

### 📊 [C#/R#/T#/M#/D#/I#] [Nome do Teste] 

**O que é**: [Explicação em 2-3 linhas. Linguagem acessível. Sem jargão
desnecessário. Usar analogias quando útil.]

**O que verifica**:
- **H₀** (hipótese nula): [descrição]
- **H₁** (hipótese alternativa): [descrição]
- *(ou, se não é teste de hipótese formal)*: [o que está sendo medido/checado]

**Por que importa para {{CONTEXTO}}**: [Consequência prática de ignorar este
teste, conectada diretamente ao objetivo declarado pelo usuário. Não genérico.]

**Pré-condições**: [Se aplicável — ex.: "Requer resíduos do modelo ajustado"
ou "Requer normalidade verificada em teste anterior". Se nenhuma: "Nenhuma".]

**Configuração**:
- N da amostra: {{N_SAMPLE}}
- Seed: {{SEED_DECLARADA_OU_NAO_APLICAVEL_COM_MOTIVO}}
- Nível de significância: α = {{ALPHA_DECLARADO_OU_PENDENTE}}
- [Outros parâmetros relevantes]
```

---

## Card PÓS-execução (célula Markdown após o código)

### Variante A — Teste de hipótese (com p-valor)

```markdown
#### Resultado

| Estatística | Valor | p-valor | Decisão |
|---|---|---|---|
| {{STAT_NAME}} | {{STAT_VALUE}} | {{P_VALUE}} | {{BADGE}} {{DECISAO}} |

**Faixa de referência**:
- ✅ OK: {{CONDICAO_OK}}
- 🟡 Atenção: {{CONDICAO_ATENCAO}}
- 🔴 Crítico: {{CONDICAO_CRITICO}}

**Interpretação**: {{INTERPRETACAO_CONTEXTUAL}}
[Conectar o resultado ao objetivo do usuário. Explicar o que ESTE valor
significa para ESTE dataset e ESTE método. Não repetir definição genérica.]

**Severidade**: {{BADGE}} — {{JUSTIFICATIVA_1_LINHA}}

**Próximos passos**:
1. {{ACAO_1}} — [técnica + impacto esperado]
2. {{ACAO_2}} — [alternativa]
3. {{ACAO_3}} — [se anteriores não resolverem]
```

### Variante B — Métrica sem p-valor (ex.: VIF, PSI, CV)

```markdown
#### Resultado

| Métrica | Valor | Referência | Decisão |
|---|---|---|---|
| {{METRIC_NAME}} | {{VALUE}} | {{THRESHOLD}} | {{BADGE}} {{DECISAO}} |

**Faixa de referência**:
- ✅ OK: {{CONDICAO_OK}}
- 🟡 Atenção: {{CONDICAO_ATENCAO}}
- 🔴 Crítico: {{CONDICAO_CRITICO}}

**Interpretação**: {{INTERPRETACAO_CONTEXTUAL}}

**Severidade**: {{BADGE}} — {{JUSTIFICATIVA_1_LINHA}}

**Próximos passos**:
1. {{ACAO_1}}
2. {{ACAO_2}}
```

### Variante C — Teste com múltiplas variáveis (ex.: VIF por feature, KS por split)

```markdown
#### Resultado

| Feature | Estatística | Valor | Referência | Decisão |
|---|---|---|---|---|
| {{FEAT_1}} | {{STAT}} | {{VALUE}} | {{THRESHOLD}} | {{BADGE}} |
| {{FEAT_2}} | {{STAT}} | {{VALUE}} | {{THRESHOLD}} | {{BADGE}} |
| ... | ... | ... | ... | ... |

**Resumo**: {{N_OK}} ✅ | {{N_ATENCAO}} 🟡 | {{N_CRITICO}} 🔴

**Features problemáticas**: {{LISTA_FEATURES_PROBLEMATICAS}}

**Interpretação**: {{INTERPRETACAO_CONTEXTUAL}}

**Severidade geral**: {{BADGE}} — {{JUSTIFICATIVA}}

**Próximos passos**:
1. {{ACAO_1}}
2. {{ACAO_2}}
```

### Extensão para Modo Inferência (adicionar ao final de qualquer variante)

```markdown
---
**Report formal (modo Inferência)**:
- H₀: {{H0_FORMAL}}
- H₁: {{H1_FORMAL}}
- α = {{ALPHA}}
- Estatística: {{STAT_NAME}} = {{STAT_VALUE}}
- Graus de liberdade: df = {{DF}}
- p-valor: {{P_EXACT}}
- Tamanho de efeito: {{EFFECT_MEASURE}} = {{EFFECT_VALUE}} ({{EFFECT_CLASS}})
- IC: {{NIVEL_E_LIMITES_CALCULADOS_OU_STATUS_COM_MOTIVO}}
- Conclusão: {{REJEITA_NAO_REJEITA}} H₀ ao nível α = {{ALPHA}}.
- Power: {{POWER}} (risco tipo II: β ≈ {{BETA}})
```

---

## Regras de preenchimento

1. **Toda interpretação deve ser contextual**: não repetir definição genérica do teste.
   Conectar ao dataset, ao método e ao objetivo do usuário.
2. **Badges**: usar snippet `badge()` quando disponível, ou emoji direto (✅/🟡/🔴/ℹ️).
3. **Valores numéricos**: 4 casas decimais para estatísticas e p-valores;
   formatar grandes números no padrão BR (1.234.567).
4. **Próximos passos**: máximo 3, ordenados por viabilidade (mais simples primeiro).
5. **Modo Inferência**: incluir report formal quando modo = Inferência, respeitando o suporte do perfil. Graus de liberdade, IC, power e severidade sem suporte/evidência ficam não aplicáveis, não suportados ou pendentes, com motivo; não fabricar números ou política para preencher o molde.
6. **Se teste não se aplica** (pré-condição não atendida): usar card especial:

```markdown
### ⏭️ [Nome do Teste] — SKIPPED

**Motivo**: {{MOTIVO}} (ex.: "Pré-condição não atendida: normalidade rejeitada")
**Alternativa proposta**: {{ALTERNATIVA_OU_PENDENTE}}. Registrar como aplicada somente com evidência de execução na rota pertinente.
```
