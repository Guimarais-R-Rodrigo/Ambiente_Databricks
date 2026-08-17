# Checklist de Validação — Feature Engineering

> Verificar TODOS os itens antes de considerar o plano de FE completo.
> Itens marcados `[ ]` devem ser resolvidos ou justificados.

## Checklist obrigatório

### 📋 Contexto e escopo
- [ ] Unidade de decisão definida (ou `PENDENTE/DECISAO` com justificativa)
- [ ] Target/evento definido (ou `PENDENTE/DECISAO` — modo exploratório declarado)
- [ ] Horizonte de predição definido (ou `PENDENTE/DECISAO`)
- [ ] Coluna de tempo de referência identificada

### ⚠️ Anti-leakage
- [ ] Todas as features usam APENAS dados anteriores ao evento
- [ ] Nenhuma variável criada após o evento está incluída (status final, data encerramento, etc.)
- [ ] Aggregações respeitam janela retroativa (< data_referência, nunca ≤)
- [ ] Missingness não correlaciona artificialmente com target
- [ ] WoE/Target Encoding calculados apenas no conjunto de treino

### 🔗 Granularidade e joins
- [ ] Base final tem 1 linha por unidade de decisão (sem duplicidades)
- [ ] Contagens antes/depois de cada join conferem
- [ ] Cardinalidade das chaves de join validada (sem explosão)
- [ ] Agregações feitas ANTES de joins (não depois)

### 📊 Categóricas e dimensionalidade
- [ ] Cardinalidade controlada: top N + "outros" quando > 20 categorias
- [ ] Estratégia de codificação definida por feature (WoE/OHE/Freq/Target)
- [ ] One-hot limitado a ≤ 10 dummies por feature
- [ ] WoE monotônico verificado (se aplicável)

### 🔢 Nulos, outliers e sanidade
- [ ] Estratégia de nulos definida por feature (imputação / flag / drop)
- [ ] Outliers tratados (cap em percentil, winsorize, ou flag)
- [ ] Distribuições plausíveis (sem valores impossíveis: idade negativa, % > 100, etc.)
- [ ] Sem constantes (variância > 0 para todas as features)

### 📈 Seleção e estabilidade
- [ ] IV, quando pertinente, interpretado com estabilidade, incerteza e valor incremental; sem corte universal
- [ ] Correlação entre features: pares com |r| > 0.95 resolvidos (manter mais interpretável)
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
