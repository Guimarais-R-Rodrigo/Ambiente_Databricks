# Checklist de Validação — Feature Engineering

> Conferir aplicabilidade de cada item pelo contrato. Usar pendente/NÃO EXECUTADO
> ou NÃO APLICÁVEL com motivo quando necessário. Plano completo não prova execução
> nem autoriza materialização. Preservar gates e verificadores do perfil selecionado.

## Checklist obrigatório

### 📋 Contexto e escopo
- [ ] Unidade de decisão definida (ou `PENDENTE/DECISAO` com justificativa)
- [ ] Target/evento definido (ou `PENDENTE/DECISAO` — modo exploratório declarado)
- [ ] Horizonte de predição definido (ou `PENDENTE/DECISAO`)
- [ ] Coluna de tempo de referência identificada

### ⚠️ Anti-leakage
- [ ] Features usam apenas informação disponível no instante de decisão, sem incorporar o período do target
- [ ] Nenhuma variável criada após o evento está incluída (status final, data encerramento, etc.)
- [ ] Agregações respeitam `event_time`, `available_at`, cutoff e fronteira LT/LE declarados no contrato; não impor `<` universal (o perfil `FIXED_LAG_L1_V1` exige LE)
- [ ] Missingness não correlaciona artificialmente com target
- [ ] WoE/Target Encoding calculados apenas no conjunto de treino

### 🔗 Granularidade e joins
- [ ] Base final tem 1 linha por unidade de decisão (sem duplicidades)
- [ ] Contagens antes/depois de cada join conferem
- [ ] Cardinalidade das chaves de join validada (sem explosão)
- [ ] Estratégia de agregação/join preserva a semântica e o grão contratados; pré-agregar apenas quando correto para o caso

### 📊 Categóricas e dimensionalidade
- [ ] Cardinalidade e política top-N/“outros” justificadas por algoritmo, frequência, estabilidade e orçamento
- [ ] Estratégia de codificação definida por feature (WoE/OHE/Freq/Target)
- [ ] Dimensão one-hot avaliada contra capacidade/contrato do modelo, sem limite universal de dummies
- [ ] WoE monotônico verificado (se aplicável)

### 🔢 Nulos, outliers e sanidade
- [ ] Estratégia de nulos definida por feature (imputação / flag / drop)
- [ ] Extremos investigados; tratamento somente com regra justificada e ajustada no treino, sem cap automático
- [ ] Distribuições plausíveis (sem valores impossíveis: idade negativa, % > 100, etc.)
- [ ] Sem constantes (variância > 0 para todas as features)

### 📈 Seleção e estabilidade
- [ ] IV, quando pertinente, interpretado com estabilidade, incerteza e valor incremental; sem corte universal
- [ ] Redundância/correlação examinada com valor incremental, estabilidade e objetivo; sem exclusão por limiar isolado
- [ ] PSI calculado com referência/bins fixos e comparado ao limite aprovado (se houver dado temporal)

### 🏗️ Implementação
- [ ] Ordem de execução definida (base âncora → agregações → joins → codificação → seleção)
- [ ] Seeds fixas declaradas para amostragens de inspeção
- [ ] Feature Store avaliado (usar / não usar — justificado)
- [ ] Próximo passo claro (notebook de implementação identificado)

## Status final
- **Itens resolvidos**: ___ / ___
- **Pendências críticas**: ___
- **Decisão necessária**: ___
