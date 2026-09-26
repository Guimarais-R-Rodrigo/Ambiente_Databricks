# Template: Estratégia de Split

> **[N train]** treino | **[N val]** validação | **[N test]** teste | **[Strategy]** estratégia


## Uso
Guia de decisão para escolher o tipo de split adequado.

## Árvore de decisão

```text
1. O problema envolve previsão FUTURA?
   ├── SIM → Split TEMPORAL (por data)
   │         Gap de 1 período entre treino e validação
   │         Treino: passado | Val: intermediário | Teste: mais recente
   │
   └── NÃO → 2. Mesma entidade pode aparecer em múltiplas linhas?
              ├── SIM → Split por GRUPO (GroupKFold)
              │         Ex.: id_cliente não repete entre splits
              │
              └── NÃO → 3. Há desbalanceamento de classes?
                         ├── SIM → Split ESTRATIFICADO
                         │         Mantém proporção de classes em cada split
                         │
                         └── NÃO → Split ALEATÓRIO (random)
```

## Proporções padrão

| Split | Treino | Validação | Teste |
|---|---|---|---|
| Padrão | 70% | 15% | 15% |
| Dados escassos (N < 10k) | 60% | 20% | 20% |
| Walk-forward (séries) | Expanding window | 1 período | 1 período |

## Anti-leakage checklist

- [ ] Nenhuma informação futura ao evento está no treino
- [ ] Split temporal tem gap entre treino e validação
- [ ] Mesma entidade NÃO aparece em treino E teste
- [ ] Features foram calculadas ANTES da data de split
- [ ] Target leakage ausente (nenhuma feature é proxy do target)

## Código de referência

```python
# Split temporal
df_sorted = df.sort_values('dt_referencia')
n = len(df_sorted)
train = df_sorted.iloc[:int(0.70*n)]
val = df_sorted.iloc[int(0.70*n):int(0.85*n)]
test = df_sorted.iloc[int(0.85*n):]

# Split estratificado
from sklearn.model_selection import train_test_split
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42)
```

---

#### ✅ Validação do split

| Check | Status |
|---|---|
| Sem leakage temporal | ✅ / ❌ |
| Distribuição do target preservada | ✅ / ❌ |
| Sem overlap entre conjuntos | ✅ / ❌ |
| Proporção adequada (60/20/20 ou similar) | ✅ / ❌ |
