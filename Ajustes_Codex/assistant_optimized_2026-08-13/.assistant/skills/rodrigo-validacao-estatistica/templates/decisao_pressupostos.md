# Template: Decisão de Pressupostos

> Tabela de decisão rápida: "Pressuposto violado → O que fazer?"
> Organizada por suite, com mitigação primária, secundária e última opção.
> Usar como referência no diagnóstico consolidado e calibrar ao desenho real.

---

## Suite: Regressão & Econometria

| Pressuposto | Teste | Violação detectada | Mitigação primária | Mitigação secundária | Última opção | Muda o método? |
|---|---|---|---|---|---|---|
| Normalidade (resíduos) | R1/R2 | p ≤ 0,05 | Transformação Box-Cox/log na resposta | Bootstrapped standard errors | Modelo não-paramétrico | Não (se predição) / Sim (se inferência) |
| Multicolinearidade | R3 | VIF ≥ 10 | Remover feature menos importante do par | Ridge/Lasso regularização | PCA parcial nas colineares | Não |
| Autocorrelação | R4 | DW < 1,0 ou > 3,0 | Adicionar lags/AR terms | Erros robustos Newey-West (HAC) | Reespecificar modelo | Sim (se persistir) |
| Homocedasticidade | R5/R6 | BP p ≤ 0,01 | Erros robustos HC3 (White) | WLS (Weighted Least Squares) | Transformação da resposta | Não |
| Especificação funcional | R7 | RESET p ≤ 0,01 | Termos quadráticos/interações | Modelo GAM/splines | Abandonar OLS → tree-based | Sim |
| Estabilidade numérica | R8 | CN ≥ 100 | Standardizar features (z-score) | Remover quase-colineares | Ridge regularização | Não |

### Árvore de decisão Regressão

```text
Normalidade falha?
├── Objetivo = predição → 🟡 registrar, prosseguir
└── Objetivo = inferência →
    ├── Box-Cox resolve? → ✅ re-testar
    └── Não resolve →
        ├── Bootstrap → ✅ IC via resampling
        └── Mudar para método não-paramétrico
```

---

## Suite: Séries Temporais

| Pressuposto | Teste | Violação detectada | Mitigação primária | Mitigação secundária | Última opção | Muda o método? |
|---|---|---|---|---|---|---|
| Estacionariedade | T1/T2 | ADF p ≥ 0,10 + KPSS p ≤ 0,01 | Diferenciação (d=1 ou d=2) | Remoção de tendência (detrend) | Cointegração se múltiplas séries | Pode (ARIMA vs ARIMAX) |
| Ruído branco (resíduos) | T3 | LB p ≤ 0,05 em múltiplos lags | Aumentar ordem AR/MA | Incluir termos sazonais (SARIMA) | Modelo mais complexo (VAR/GARCH) | Sim |
| Autocorrelação 1ª ordem | T4 | DW < 1,0 ou > 3,0 | Adicionar AR(1) | Reespecificar com mais lags | Modelo autoregressivo completo | Sim |
| Sazonalidade | T5 | Strength ≥ 0,40 não modelada | SARIMA (P,D,Q,s) | Dummies sazonais | Decomposição STL + modelo resíduos | Sim |
| Normalidade (resíduos) | T6 | Shapiro p ≤ 0,05 | Bootstrap nos intervalos de previsão | Transformação (log-returns) | Reportar IC com ressalva | Não (para pontuais) |
| ARCH effects | T7 | ARCH-LM p ≤ 0,05 | Modelo GARCH | Bootstrap para intervalos | Log-returns + volatilidade separada | Sim |

### Árvore de decisão Séries Temporais

```text
Série é estacionária? (ADF + KPSS)
├── Sim → prosseguir com ARMA/VAR
└── Não →
    ├── Diferenciar (d=1) → re-testar
    │   ├── Agora estacionária? → ✅ ARIMA(p,1,q)
    │   └── Ainda não? → d=2 ou detrend
    └── Múltiplas séries? → testar cointegração (Johansen)
```

---

## Suite: ML Tabular

| Pressuposto | Teste | Violação detectada | Mitigação primária | Mitigação secundária | Última opção | Muda o método? |
|---|---|---|---|---|---|---|
| Sem leakage | M7 | Correlação feature-target > 0,95 | Remover feature | Refazer split temporal | Voltar para FE | Não (muda dados) |
| Estabilidade (drift) | M4/M5 | PSI acima do limite aprovado | Investigar dados/população | Treinar challenger e validar | Redefinir referência/janela com justificativa | Pode |
| Sinal genuíno | M1/M2/M6 | Nenhuma feature significativa | Revisar feature engineering | Buscar fontes adicionais | Repensar problema | Sim (escopo) |
| Balanceamento | C6 | Métrica/volume insuficiente para a decisão | Class weights / threshold tuning | Reamostragem ajustada só no treino | Reformular o problema se justificável | Pode |
| Suficiência amostral | M9 | Power < 0,60 | Mais dados | Menos features (reduzir dimensão) | Aceitar limitação + declarar | Não |

---

## Suite: Deep Learning

| Pressuposto | Teste | Violação detectada | Mitigação primária | Mitigação secundária | Última opção | Muda o método? |
|---|---|---|---|---|---|---|
| Sem leakage (entidade) | D3 | Entidades duplicadas cross-split | Re-split por entidade | GroupKFold | Redefinir splits | Não (muda dados) |
| Label quality | D2 | Noise > 10% | Limpeza manual/heurística | Confident learning (CleanLab) | Label smoothing | Não |
| Scale consistency | D5 | Escalas divergentes > 10x | StandardScaler / MinMax | BatchNormalization | Feature-wise normalization | Não |
| Distribuição entre splits | D8 | KS p ≤ 0,05 em muitas features | Stratified split | Re-amostragem | Aceitar com documentação | Não |

---

## Suite: Inferência Estatística

| Pressuposto | Teste | Violação detectada | Mitigação primária | Mitigação secundária | Última opção | Muda o método? |
|---|---|---|---|---|---|---|
| Normalidade (dados) | I1 | Shapiro p ≤ 0,05 | Transformação | Teste não-paramétrico equivalente | Bootstrap | Sim (muda teste) |
| Homocedasticidade | I2 | Levene p ≤ 0,05 | Welch's t-test (não assume igualdade) | Transformação | Teste não-paramétrico | Sim |
| Independência | — | Amostras pareadas detectadas | Usar teste pareado (paired t) | Wilcoxon signed-rank | Modelo misto | Sim |
| N por célula (χ²) | I7 | N esperado < 5 | Fisher's Exact Test | Combinar categorias | Simulação Monte Carlo | Sim |
| Múltiplos testes | I9 | > 3 testes simultâneos | Bonferroni | FDR (Benjamini-Hochberg) | Ajuste de α por família | Não (ajusta α) |

---

## Regras gerais de decisão

1. **Se mitigação resolve (re-teste passa)** → prosseguir com documentação
2. **Se mitigação não resolve e há alternativa de método** → mudar método
3. **Se não há alternativa e violação é 🔴** → NO-GO documentado
4. **Nunca ignorar 🔴 sem justificativa** — toda decisão de "seguir mesmo assim" deve ser explícita, documentada e com risco declarado

---

*Aplicar em conjunto com o fluxo atual do SKILL.md.*
