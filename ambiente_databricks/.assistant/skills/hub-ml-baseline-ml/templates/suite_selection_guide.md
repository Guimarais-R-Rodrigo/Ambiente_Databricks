# Template: Guia de Seleção de Suite

## Uso
Referência rápida para escolher a suite adequada ao problema.

## Tabela de decisão

| Seu problema é... | Suite | Trigger |
|---|---|---|
| Prever se algo vai acontecer (sim/não) | B1 (classif. binária) | `@hub-ml-baseline-ml: use B1 classificação binária` |
| Prever entre 3+ categorias | B1 (multiclasse) | `@hub-ml-baseline-ml: use B1 multiclasse` |
| Prever um valor numérico | B1 (regressão) | `@hub-ml-baseline-ml: use B1 regressão` |
| Desenvolver scorecard de crédito | B1 (scorecard) | `@hub-ml-baseline-ml: use B1 scorecard` |
| Prever valores futuros de uma série | B2 (temporal) | `@hub-ml-baseline-ml: use B2 temporal` |
| Classificar com features de alta cardinalidade | B3 (DL) | `@hub-ml-baseline-ml: avalie B3 e compare com B1` |
| Agrupar clientes por perfil | B4 (clustering) | `@hub-ml-baseline-ml: use B4 clustering` |
| Ordenar itens por relevância/prioridade | B5 (ranking) | `@hub-ml-baseline-ml: use B5 ranking` |
| Modelar quando algo vai acontecer | B6 (survival) | `@hub-ml-baseline-ml: use B6 survival` |
| Detectar comportamentos fora do padrão | B7 (anomaly) | `@hub-ml-baseline-ml: use B7 anomalia` |

## Perguntas de confirmação

Se o usuário não sabe qual suite usar, pergunte:
1. "Você tem um target definido (variável que quer prever)?"
2. "O problema envolve tempo (prever o futuro / quando algo acontece)?"
3. "O objetivo é classificar, prever um valor, agrupar ou ranquear?"
4. "Há labels confiáveis ou é detecção sem supervisão?"

---

#### 📌 Decisão de suite

| Condição detectada | Suite | Confiança |
|---|---|---|
| [condição] | [B1/B2/...] | 🟢 Alta / 🟡 Média |

#### ➡️ Próximo passo
Planejar a suite escolhida. Executar somente a rota e o perfil disponíveis na skill após confirmar entradas, dependências e autorização. B1–B7 são categorias de método; sua presença nesta tabela não comprova suporte executável de todas as suites.
