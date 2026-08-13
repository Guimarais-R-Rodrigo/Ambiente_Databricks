# Roteiro de forward tests — 12 skills (36 testes)

Gerado a partir das `description` de `ambiente_fonte/.assistant/skills/` em
2026-08-13. Método e vereditos: `.claude/skills/forward-test-skills/SKILL.md`.
Registre os resultados em `resultados/<data>_rodada<N>.md` (copie o
`template_resultados.md`).

**Regras de ouro:** um chat novo por teste · colar o prompt sozinho, sem anexos ·
observar a skill carregada, não a qualidade da resposta · tabelas citadas são
fictícias de propósito (o teste é de roteamento, não de execução).

Os casos negativos foram desenhados sobre as **zonas de colisão** entre
descrições: drift (monitoramento × validação × safra), WoE/IV (features ×
baseline), explicar × documentar (tutor × comentar), revisar (auditoria × tutor)
e materialização (pipeline × features). No caso negativo, anote qual skill foi
carregada — essa informação calibra as descriptions.

---

## 1. rodrigo-eda-profissional

**P (positivo):**
```text
Faça uma EDA completa da tabela catalogo.crm.clientes_pf: granularidade, chaves, qualidade de dados, distribuições e um relatório executivo ao final.
```
**N (negativo — esperado: rodrigo-cross-eda-ml):**
```text
Já tenho os EDAs prontos de clientes, transações e produtos. Consolide os três, avalie se os joins são viáveis e diga se estou pronto para modelar.
```
**@ (menção):**
```text
@rodrigo-eda-profissional faça o perfil inicial da tabela catalogo.crm.contas.
```

## 2. rodrigo-cross-eda-ml

**P:**
```text
Cruze os resultados dos EDAs das tabelas clientes e cartões, avalie a viabilidade do join por CPF, o alinhamento temporal e a prontidão para ML.
```
**N (esperado: rodrigo-eda-profissional):**
```text
Explore a tabela catalogo.crm.cartoes e me diga como está a qualidade e a distribuição das variáveis.
```
**@:**
```text
@rodrigo-cross-eda-ml avalie a complementaridade de sinal entre as fontes A e B.
```

## 3. rodrigo-feature-engineering

**P:**
```text
Monte o plano de features para prever churn de previdência, com joins point-in-time, prevenção de leakage e materialização em feature table no Unity Catalog.
```
**N (esperado: rodrigo-baseline-ml):**
```text
Treine um primeiro modelo LightGBM para churn com split temporal e registre tudo no MLflow.
```
**@:**
```text
@rodrigo-feature-engineering especifique features de recência e frequência para o target churn_90d.
```

## 4. rodrigo-validacao-estatistica

**P:**
```text
Antes da regressão, verifique normalidade dos resíduos, homocedasticidade e VIF, com amostragem reprodutível e effect size.
```
**N (esperado: rodrigo-monitoramento-modelo) — colisão "drift":**
```text
O PSI das features do modelo em produção subiu nos últimos dois meses. Configure alertas e me diga se é hora de retreinar.
```
**@:**
```text
@rodrigo-validacao-estatistica compare as duas amostras e diga se a diferença é significativa.
```

## 5. rodrigo-baseline-ml

**P:**
```text
Treine baselines de classificação comparando LightGBM e XGBoost com split temporal anti-leakage, MLflow e scorecard final.
```
**N (esperado: rodrigo-explainability):**
```text
Quais features mais pesam no score do meu modelo de propensão? Quero a visão global e dois exemplos locais para o comitê.
```
**@:**
```text
@rodrigo-baseline-ml rode a suite de baseline para o target inadimplencia_90d.
```

## 6. rodrigo-explainability

**P:**
```text
Gere a análise SHAP global e local do modelo de propensão a consórcio e um model card com limitações para público executivo.
```
**N (esperado: rodrigo-monitoramento-modelo):**
```text
Implemente o acompanhamento mensal de performance do modelo com alertas de degradação e painel.
```
**@:**
```text
@rodrigo-explainability explique os drivers do score do cliente 12345 (dados sintéticos).
```

## 7. rodrigo-monitoramento-modelo

**P:**
```text
Implemente monitoramento do modelo de churn: qualidade de dados, drift com PSI, performance mensal, calibração e regra de decisão de retreino.
```
**N (esperado: rodrigo-validacao-estatistica) — colisão "KS/drift":**
```text
Num estudo pontual, rode um teste KS para comparar a distribuição de renda entre dois grupos de clientes e me dê intervalo de confiança.
```
**@:**
```text
@rodrigo-monitoramento-modelo desenhe os thresholds de alerta para o modelo em produção.
```

## 8. rodrigo-pipeline-builder

**P:**
```text
Desenhe um pipeline bronze/silver/gold com Lakeflow Spark Declarative Pipelines, expectations de qualidade e um bundle com targets dev e prod.
```
**N (esperado: rodrigo-feature-engineering) — colisão "materialização":**
```text
Materialize as features do modelo de churn numa feature table do Unity Catalog garantindo reuso idêntico entre treino e inferência.
```
**@:**
```text
@rodrigo-pipeline-builder estruture a orquestração dos notebooks de scoring com Lakeflow Jobs.
```

## 9. rodrigo-analise-safra

**P:**
```text
Monte a análise de safras de originação de crédito com MOB, curvas de maturação, triângulo safra-calendário e alertas de deterioração.
```
**N (esperado: rodrigo-monitoramento-modelo) — colisão "deterioração":**
```text
A inadimplência do portfólio subiu neste trimestre. O modelo de crédito degradou? Monte o acompanhamento contínuo com alertas.
```
**@:**
```text
@rodrigo-analise-safra compare as safras de 2024 e 2025 em MOB equivalente.
```

## 10. rodrigo-comentar-notebook

**P:**
```text
Adicione células %md antes e depois de cada bloco deste notebook de EDA, explicando objetivo, entradas, resultado e próximo passo, sem poluir o fluxo.
```
**N (esperado: rodrigo-tutor-databricks) — colisão "explicar":**
```text
Me explique linha a linha o que este notebook PySpark faz, como se fosse uma aula para quem está aprendendo Spark.
```
**@:**
```text
@rodrigo-comentar-notebook documente este notebook para revisão do time.
```

## 11. rodrigo-tutor-databricks

**P:**
```text
Me dê uma aula sobre este stack trace do Spark: o que causou o erro, como corrigir e uma analogia para eu nunca mais esquecer.
```
**N (esperado: rodrigo-comentar-notebook):**
```text
Adicione markdown profissional de documentação neste notebook para o time entender cada etapa.
```
**@:**
```text
@rodrigo-tutor-databricks explique a diferença entre cache() e persist() com exemplos.
```

## 12. rodrigo-auditoria-skills

**P:**
```text
Audite este relatório de EDA contra o contrato da skill rodrigo-eda-profissional: completude, reprodutibilidade e score final com prioridades.
```
**N (esperado: rodrigo-eda-profissional):**
```text
Faça a análise exploratória da tabela catalogo.crm.propostas com foco em qualidade.
```
**@:**
```text
@rodrigo-auditoria-skills avalie se a pasta da skill rodrigo-analise-safra segue o padrão Agent Skills.
```

---

## Depois da rodada

1. Preencher o arquivo de resultados (template ao lado) e commitá-lo.
2. Toda falha de positivo/negativo → ajustar `description` no `ambiente_fonte/`,
   validar, renderizar, republicar e repetir apenas os casos afetados.
3. Registrar a rodada no `CHANGELOG.md`.
