# Template: Guia de Walk-Forward Validation

> **[N folds]** folds | **[Win train]** janela treino | **[Win test]** janela teste | **[Métrica média]** resultado


## Uso
Referência para implementação de validação temporal correta.

## Por que walk-forward é obrigatório

Em séries temporais, **random split é proibido** porque:
1. Contamina treino com informação futura (leakage temporal)
2. Superestima performance (modelo "vê" padrões que não existiriam em produção)
3. Não simula o cenário real de previsão

## Tipos de walk-forward

### Expanding window (padrão recomendado)
```text
Fold 1: Treino=[1..12]  → Teste=[13..14]
Fold 2: Treino=[1..14]  → Teste=[15..16]
Fold 3: Treino=[1..16]  → Teste=[17..18]
...
```
- Treino cresce a cada fold (mais dados)
- Simula produção com retreino periódico

### Sliding window (dados com regime change)
```text
Fold 1: Treino=[1..12]   → Teste=[13..14]
Fold 2: Treino=[3..14]   → Teste=[15..16]
Fold 3: Treino=[5..16]   → Teste=[17..18]
...
```
- Treino tem tamanho fixo (janela deslizante)
- Útil quando dados antigos não são mais representativos

## Parâmetros de configuração

| Parâmetro | Descrição | Valor típico |
|---|---|---|
| min_train_size | Mínimo de pontos para treinar | 2× período sazonal |
| test_size | Tamanho de cada fold de teste | 1 período (ou horizonte) |
| step_size | Quanto avançar entre folds | = test_size |
| n_folds | Número de folds | 6-12 (depende do histórico) |
| gap | Períodos de gap entre treino e teste | 0-1 (anti-leakage) |

## Código de referência

```python
def walk_forward_split(df, date_col, min_train, test_size, step=None, gap=0):
    dates = sorted(df[date_col].unique())
    step = step or test_size
    splits = []
    
    for i in range(min_train, len(dates) - test_size - gap + 1, step):
        train_dates = dates[:i]
        test_dates = dates[i + gap:i + gap + test_size]
        
        train_mask = df[date_col].isin(train_dates)
        test_mask = df[date_col].isin(test_dates)
        
        splits.append((train_mask, test_mask))
    
    return splits
```

## Reporte de performance

Reportar métricas **por fold** E **agregada**:
- Média ± desvio entre folds
- Tendência (performance está melhorando ou piorando ao longo do tempo?)
- Pior fold (worst case)

---

#### 📊 Resultado por fold

| Fold | Período treino | Período teste | Métrica | Status |
|---|---|---|---|---|
| 1 | [range] | [range] | [X] | 🟢 / 🟡 / 🔴 |
| 2 | [range] | [range] | [X] | 🟢 / 🟡 / 🔴 |

#### 🔍 Interpretação
- Estabilidade: [desvio entre folds] → [estável/instável]
- Tendência: [melhorando/piorando/flat]
