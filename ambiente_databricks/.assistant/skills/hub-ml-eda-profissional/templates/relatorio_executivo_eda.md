<!-- Template: relatório executivo de EDA (skill hub-ml-eda-profissional) -->

Preencher a partir dos outputs observados da rota canônica. Planejamento fica
NÃO EXECUTADO; métrica ausente fica NÃO CALCULADO. Sem critérios de qualidade,
manter NÃO CLASSIFICADO. O relatório não substitui Receipt, Postflight nem
`completion.authorized=true` reverificado exigido para conclusão da EDA.

```md
# Relatório Executivo — Análise Exploratória de Dados

| Campo | Valor |
|-------|-------|
| **Tabela analisada** | `[CATALOGO].[SCHEMA].[TABELA]` |
| **Período de referência** | [YYYY-MM-DD a YYYY-MM-DD] |
| **Volume total** | [N de linhas] |
| **Granularidade** | [uma linha = ?] |
| **Data da análise** | [YYYY-MM-DD] |
| **Notebook fonte** | `[caminho_do_notebook]` |

## 1. Resumo executivo

[3 a 6 linhas em linguagem de negócio com os principais achados. Deve ser
legível por um executivo que não lerá o resto do relatório.]

## 2. Escopo da análise

- **Tabela**: `[CATALOGO].[SCHEMA].[TABELA]`
- **Volume**: [N] linhas e [M] colunas.
- **Período**: [data inicial] a [data final].
- **Filtros aplicados**: [descrever filtros relevantes].
- **Amostragem**: [se houve, declarar fração e tamanho efetivo].
- **Premissas**: [listar].

## 3. Qualidade geral dos dados

- **Completude**: [% global de preenchimento, colunas com >X% nulos].
- **Unicidade**: [chave de negócio identificada e duplicidades].
- **Consistência**: [tipos coerentes, datas válidas, domínios coerentes].
- **Confiabilidade global**: [NÃO CLASSIFICADA ou nível justificado por critérios, população, evidência e limitações].

| Indicador | Valor | Status |
|-----------|-------|--------|
| % nulos médio | [X%] | [✅/🟡/🔴] |
| Duplicidades por chave | [N] | [✅/🟡/🔴] |
| Datas inválidas | [N] | [✅/🟡/🔴] |
| Outliers significativos | [N variáveis] | [✅/🟡/🔴] |

## 4. Estrutura e granularidade

[Explicar o que representa uma linha, qual é a chave, quais são as
dimensões principais e quais cuidados o leitor deve ter.]

## 5. Principais padrões encontrados

[Distribuições, tendências, concentrações, sazonalidades, segmentos
relevantes. Pode incluir 3 a 6 gráficos centrais.]

### 5.1 [Padrão 1]

[Descrição + interpretação.]

### 5.2 [Padrão 2]

[Descrição + interpretação.]

## 6. Anomalias e pontos de atenção

- ⚠️ [Anomalia 1]: descrição, possível causa, impacto.
- ⚠️ [Anomalia 2]: ...
- ⚠️ [Anomalia 3]: ...

## 7. Implicações para negócio

[Como os achados afetam CRM, segmentação, modelagem, campanhas, operação,
decisão. Ligar achados técnicos a impacto operacional/comercial.]

## 8. Implicações para modelagem

- **Variáveis candidatas a feature**: [listar].
- **Variáveis problemáticas** (alta cardinalidade, muitos nulos, leakage):
  [listar com motivo].
- **Risco de desbalanceamento de classes**: [se aplicável].
- **Risco de leakage**: [se aplicável].
- **Necessidades de pré-processamento**: [imputação, encoding, scaling].

## 9. Recomendações

| # | Recomendação | Tipo | Prioridade |
|---|--------------|------|------------|
| 1 | ... | [tratamento / governança / modelagem / pipeline] | [alta/média/baixa] |
| 2 | ... | ... | ... |
| 3 | ... | ... | ... |

## 10. Próximos passos

1. [Ação 1].
2. [Ação 2].
3. [Ação 3].

---

**Anexos efetivamente produzidos** (em notebook fonte; marcar não produzido/N/A com motivo):
- Estatísticas descritivas completas.
- Matriz de correlação.
- Gráficos detalhados por variável.
- Código de validação reutilizável.
```
