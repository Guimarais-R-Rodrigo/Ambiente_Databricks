# Estrutura do Notebook de Saída — Feature Engineering Plan

> Este template define a sequência de células que o agente deve criar no notebook de saída.
> Adaptar ao tamanho e ao risco do corpus: condensado, padrão ou expandido.
> A numeração organiza a leitura, não impõe quantidade de células. Um plano não
> executa features. Campos sem fonte ficam PENDENTES/NÃO INFORMADOS, e etapas
> não executadas não recebem PASS. Perfis limitados e gates da skill prevalecem.

## Organização padrão (adaptável)

### Célula 1 — Header [%md]
```markdown
# 🧬 Plano de Feature Engineering — <Contexto>

| Item | Valor |
|---|---|
| **Objetivo** | <1 linha> |
| **Data** | YYYY-MM-DD |
| **Notebooks-fonte** | <lista> |
| **Unidade de decisão** | <cliente/contrato/...> |
| **Target** | <evento> ou `PENDENTE/DECISAO` |
| **Horizonte** | <N dias> ou `PENDENTE/DECISAO` |
| **Autor/owner** | [nome ou equipe fornecida] |
```

### Célula 2 — Contexto de Modelagem [%md]
```markdown
## 🎯 Pré-requisito — Contexto de Modelagem

| Elemento | Definição | Status |
|---|---|---|
| Unidade de decisão | ... | ✅ / 🔴 PENDENTE |
| Evento (target) | ... | ✅ / 🔴 PENDENTE |
| Horizonte | ... | ✅ / 🔴 PENDENTE |
| Coluna de tempo | ... | ✅ / 🔴 PENDENTE |

> ⚠️ Anti-leakage: confirmar event_time, available_at, cutoff e fronteira LT/LE do contrato; o plano não prova disponibilidade.
```

### Célula 3 — Inventário do Corpus [%md]
```markdown
## 📋 Etapa 1 — Inventário dos Notebooks-Alvo

| Notebook | Papel no corpus | Entradas | Saídas | Granularidade | Obs |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |
```

### Célula 4 — Mapa das Etapas [%md]
```markdown
## 🗺️ Etapa 2 — Mapa das Etapas

**Notebook: <nome>**
1. Configuração e leitura de parâmetros
2. Leitura da tabela X (N linhas)
3. Filtro por ...
4. Join com tabela Y (chave: ...)
5. Agregação por ... (janela: ...)
6. Escrita em ...

**Notebook: <nome>** (repetir se >1)
1. ...
```

### Célula 5 — Fluxo de Dados [%md]
```markdown
## 🔄 Etapa 3 — Fluxo de Dados Consolidado

```
[catalog.schema.tabela_A] ──┐
                            ├──> join (chave: id_cliente)
[catalog.schema.tabela_B] ──┘          │
                                       ▼
                              filtro (ativo=True)
                                       │
                                       ▼
                              agregação (por cliente, 30d)
                                       │
                                       ▼
                              [Base de Modelagem: 1 linha/cliente]
```
```

### Célula 6 — Evidências [%md]
```markdown
## 🔍 Etapa 4 — Evidências Extraídas do Corpus

### Schema e tipos
| Coluna | Tipo | Nulos (%) | Obs |
|---|---|---|---|
| ... | ... | ... | ... |

### Qualidade
- Duplicidades: ...
- Categorias raras: ...
- Outliers: ...

### Temporalidade
- Cobertura: <data_min> a <data_max>
- Granularidade temporal: diária / mensal / snapshot

### ⚠️ Indícios de leakage
- [ ] <item identificado ou "nenhum identificado">
```

### Célula 7 — Validação de evidências [code] (opcional)
```python
# === VALIDAÇÃO: schema e qualidade das fontes ===
# Planejar a verificação pertinente; executar somente com escopo/autorização e rota canônica aplicável

# df = spark.table("catalog.schema.tabela")
# display(df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]))
```

### Célula 8 — Taxonomia de Features [%md]
```markdown
## 🧬 Etapa 5 — Taxonomia de Features (Famílias)

### 1. Estáticas (cadastro/perfil)
- `feat_uf_residencia`: UF de residência do cliente
- `feat_segmento`: segmento comercial (PF/PJ/Private)
- ...

### 2. Comportamentais (RFV + agregações)
- `feat_qtd_transacoes_30d`: quantidade de transações nos últimos 30 dias
- `feat_valor_medio_compra_90d`: ticket médio em 90 dias
- ...

### 3. Temporais / safra
- `feat_tempo_relacionamento_meses`: meses desde abertura da conta
- `feat_dias_desde_ultima_compra`: recência
- `feat_delta_saldo_30d_vs_90d`: tendência (Δ entre janelas)
- ...

### 4. Interações
- `feat_razao_saldo_renda`: saldo / renda declarada
- `feat_uso_sobre_limite`: utilização de crédito / limite
- ...

### 5. Missingness como sinal
- `feat_qtd_campos_nulos`: contagem de campos sem preenchimento
- `feat_flag_renda_ausente`: indicador binário
- ...

### 6. Categóricas (codificação)
- Estratégia: WoE somente quando justificado para target binário e com fit no treino
- `feat_woe_uf`: WoE da UF de residência
- ...

### 7. Derivadas de regras
- `feat_regra_cliente_ativo`: captura regra de negócio "ativo se >1 transação em 30d"
- ...
```

### Célula 9 — Feature Spec Core [%md]
```markdown
## 📐 Etapa 6A — Feature Spec (Core)

| feature_name | definicao | tipo | granularidade | janela | origem |
|---|---|---|---|---|---|
| feat_qtd_transacoes_30d | Nº de transações nos últimos 30 dias | int | cliente | 30d | transacoes.qtd |
| ... | ... | ... | ... | ... | ... |
```

### Célula 10 — Feature Spec Risco [%md]
```markdown
## 📐 Etapa 6B — Feature Spec (Risco & Validação)

| feature_name | risco_leakage | custo | validacao | expectativa_sinal | obs |
|---|---|---|---|---|---|
| feat_qtd_transacoes_30d | NÃO AVALIADO | A ESTIMAR | Domínio, janela e disponibilidade conforme contrato | Hipótese a testar | Exemplo ilustrativo |
| ... | ... | ... | ... | ... | ... |
```

### Célula 11 — Backlog [%md]
```markdown
## 🎯 Etapa 7 — Backlog de Features (Tier A/B/C)

| tier | feature_name | motivo | risco | dependencias | status |
|---|---|---|---|---|---|
| [tier a avaliar] | feat_qtd_transacoes_30d | Hipótese de sinal incremental | NÃO AVALIADO | fonte e disponibilidade a confirmar | [ ] |
| [tier a avaliar] | feat_razao_saldo_renda | Hipótese de informação adicional | NÃO AVALIADO | componentes/denominador/disponibilidade a confirmar | [ ] |
| B | feat_delta_saldo_30d_vs_90d | tendência, validar janela | MÉDIO | tabela saldos (histórico) | [ ] |
| C | feat_embedding_produto | experimental, alta dim | ALTO | tabela produtos | [ ] |
```

### Célula 12 — Plano de Implementação [%md]
```markdown
## 🏗️ Etapa 8 — Plano de Implementação

### Ordem de execução
1. **Base âncora**: 1 linha por `id_cliente` + `data_referencia`
2. **Estáticas**: join com cadastro (cardinalidade 1:1, validar)
3. **Agregações comportamentais**: janela, event_time, available_at, cutoff e fronteira LT/LE definidos pelo contrato; respeitar o perfil executável
4. **Temporais**: datediff, lag, tendências
5. **Interações**: razões e diferenças (após ter componentes)
6. **Codificação categóricas**: WoE fit no treino, transform no score
7. **Missingness flags**: após todos os joins
8. **Seleção final**: combinar valor incremental, estabilidade, leakage, custo e interpretabilidade; não usar corte universal de IV/correlação/PSI

### Prevenção de explosão de join
- Definir ordem de agregação/join pela semântica e pelo grão. Pré-agregar quando necessário e correto; não é regra universal
- Validar cardinalidade da chave: `df.groupBy("chave").count().where("count > 1")`
- Conferir count antes/depois do join

### Feature Store (somente planejamento; efeitos dependem de autorização)
- [ ] Registrar tabela de features com chave `id_cliente` + timestamp
- [ ] Configurar `FeatureLookup` para treino
- [ ] Definir frequência de atualização
```

### Célula 13 — Checklist [%md]
```markdown
## ✅ Checklist de Validação

- [ ] Contexto: unidade de decisão e horizonte definidos (ou `PENDENTE/DECISAO`)
- [ ] Anti-leakage: disponibilidade até a decisão e fronteiras conforme contrato; evidência ou pendência
- [ ] Granularidade: 1 linha por unidade de decisão (sem duplicidades)
- [ ] Pós-join: contagens antes/depois fazem sentido
- [ ] Categóricas: cardinalidade controlada (WoE / top N + "outros")
- [ ] Nulos/outliers: estratégia definida por feature
- [ ] Sanidade: distribuições plausíveis (sem bug de regra/join)
- [ ] IV, se pertinente, validado sem regra universal de descarte
- [ ] Estabilidade: PSI com referência/bins fixos e limite aprovado (se houver dado temporal)
```

### Célula 14 — Resumo Executivo [%md]
```markdown
## 📌 Resumo Executivo

- **Total de features propostas**: N (Tier A: X, Tier B: Y, Tier C: Z)
- **Famílias pertinentes cobertas**: [lista e escopo, sem quota obrigatória]
- **Riscos principais**: <1–2 linhas>
- **Pendências (`PENDENTE/DECISAO`)**: <lista ou "nenhuma">
- **Próximo passo**: [resolver pendência ou implementar escopo aprovado no destino confirmado]
```

---

## Organização condensada
Mesclar: Header + Contexto (1 célula), Inventário + Mapa (1 célula), pular Fluxo e Evidências detalhadas,
ir direto para Taxonomia → Spec → Backlog → Checklist → Resumo.

## Organização expandida
Adicionar somente quando pertinente ao objetivo e autorizado:
- Célula de código por família de features (skeleton de implementação)
- Diagrama Mermaid para fluxo (se suportado)
- Célula de código com cálculo de IV por feature candidata
- Célula de código com análise de correlação entre features propostas
