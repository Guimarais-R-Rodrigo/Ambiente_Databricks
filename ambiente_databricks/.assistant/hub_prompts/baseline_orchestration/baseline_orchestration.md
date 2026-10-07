# Prompt: baseline de machine learning

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe dataset/notebook e target com
> **Add context** ou `@`. Skill: `@hub-ml-baseline-ml`.

Antes de executar, siga a [skill selecionada](../../skills/hub-ml-baseline-ml/SKILL.md),
a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) e o contrato
da rota suportada. Helpers são componentes dessa rota, não um bypass. O
[Manual Técnico](../../MANUAL_TECNICO_V2.md#catalogo-helpers) é o catálogo integrado.

## Por que este formulário é detalhado

Um baseline útil depende da unidade de análise, disponibilidade temporal, definição
do evento e estratégia de validação. Se esses campos faltarem, peça diagnóstico e
plano — não aceite um treino baseado em suposições ocultas.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{DATASET}}` | Anexe features/dataset ou nomeie em três níveis. | Evita treinar sobre origem presumida. | `@main.ml.features_clientes` |
| `{{GRANULARIDADE_E_CHAVE}}` | Defina unidade e chave do exemplo. | Evita split e métrica duplicados. | cliente no cutoff; `id_cliente` |
| `{{TARGET_E_EVENTO}}` | Defina target, classe positiva e maturação. | Alinha treino e decisão. | inadimplência em 90 dias; 1=evento |
| `{{CLASSIFICACAO_REGRESSAO_SERIE_RANKING_CLUSTER_SURVIVAL_ANOMALIA}}` | Escolha a família do problema. | Determina modelos e métricas válidos. | classificação binária |
| `{{PONTO_NO_TEMPO}}` | Informe quando a predição ocorre. | Impede leakage temporal. | fechamento mensal |
| `{{HORIZONTE_OU_NAO_APLICAVEL}}` | Defina janela futura ou `NÃO APLICÁVEL`. | Separa observação e target. | 90 dias |
| `{{PERIODO}}` | Declare cobertura e maturidade. | Permite split temporal realista. | 2023-01 a 2026-03 |
| `{{SPLIT_E_JUSTIFICATIVA}}` | Escolha split por tempo/grupo e explique. | Evita validação otimista. | out-of-time por trimestre |
| `{{COLUNAS_PROIBIDAS}}` | Liste PII, pós-evento e proxies vetados. | Bloqueia leakage e uso indevido. | status_cobranca_pos_evento |
| `{{METRICA_E_CUSTO}}` | Defina métrica, direção e custo do erro. | Orienta seleção do baseline. | KS em p.p.; falso negativo custa mais |
| `{{RESTRICOES}}` | Declare compute, prazo e bibliotecas. | Mantém experimento executável. | serverless; 30 min; LightGBM disponível |
| `{{PLANO_CODIGO_OU_EXECUCAO_AUTORIZADA}}` | Escolha artefato e autorização. | Não confunde código com treino realizado. | plano + código; sem executar |

## Prompt pronto para colar

```text
Use @hub-ml-baseline-ml para construir um baseline simples, auditável e apropriado
ao problema. Priorize uma referência honesta antes de otimização complexa.

DEFINIÇÃO
- Dataset/features: {{DATASET}}
- Unidade e chave: {{GRANULARIDADE_E_CHAVE}}
- Target e semântica do evento: {{TARGET_E_EVENTO}}
- Tipo: {{CLASSIFICACAO_REGRESSAO_SERIE_RANKING_CLUSTER_SURVIVAL_ANOMALIA}}
- Ponto de predição/cutoff: {{PONTO_NO_TEMPO}}
- Horizonte: {{HORIZONTE_OU_NAO_APLICAVEL}}
- Período disponível: {{PERIODO}}
- Split e justificativa: {{SPLIT_E_JUSTIFICATIVA}}
- Colunas proibidas/PII: {{COLUNAS_PROIBIDAS}}
- Métrica primária e custo de erro: {{METRICA_E_CUSTO}}
- Restrições de compute/prazo/bibliotecas: {{RESTRICOES}}
- Modo: {{PLANO_CODIGO_OU_EXECUCAO_AUTORIZADA}}

DIAGNÓSTICO ANTES DO TREINO
1. Confirme schema, volume, target, prevalência/faixa, duplicidade e granularidade.
2. Verifique leakage, disponibilidade temporal, censura, grupos relacionados e
   desbalanceamento. Não use variável cuja informação surge depois do cutoff.
3. Escolha split coerente: temporal quando há produção no futuro, por grupo quando
   entidades se repetem, estratificado somente quando isso não causa leakage.
4. Defina baseline ingênuo e baseline de modelo. Deep learning, tuning amplo ou
   modelos complexos só entram depois de uma referência mais simples.
5. Apresente plano, custo provável e dependências antes de executar.

EXECUÇÃO SEGURA
- Use seed e registre versões, parâmetros, schema das features e split.
- Use MLflow para registrar parâmetros, métricas e artefatos quando disponível;
  informe claramente se logging ou tracking não puder ser validado.
- Avalie no holdout uma única vez para decisão final; ajuste no conjunto de validação.
- Para classificação, inclua métricas adequadas à prevalência e à decisão; não trate
  AUC como percentual de acertos. Para regressão, declare unidade e sensibilidade a
  outliers. Para survival/ranking/time series, use métricas próprias do problema.
- Não registre PII ou amostras brutas como artefatos.
- Não promova modelo, não grave tabela, não publique endpoint e não altere produção
  sem pedido separado e confirmação explícita.

CONTRATO DE SAÍDA
- Problem framing e pressupostos.
- Tabela de candidatos e justificativa do baseline escolhido.
- Código modular e parametrizado, se solicitado.
- Resultados por split/tempo/segmento com incerteza ou variabilidade quando viável.
- Comparação com baseline ingênuo, erros relevantes e riscos.
- Registro de reprodutibilidade e próximos experimentos priorizados.

VALIDAÇÃO FINAL
- Confirme ausência de sobreposição/leakage entre splits.
- Confirme que preprocessing foi ajustado somente no treino.
- Verifique consistência entre direção da métrica, evento positivo e threshold.
- Diferencie resultados medidos, inferências e expectativas.
```

## Exemplo mínimo

Dataset = `@main.ml.churn_features`; target = `churn_90d` (1 = evento); ponto no
tempo = `data_snapshot`; split = treino até 2025-09, validação 2025-10/11, teste
2025-12; métricas = PR-AUC e recall no top decil.

## O que conferir na resposta

- O recurso, o período e o grão usados coincidem com o que foi anexado e preenchido.
- Evidência observada está separada de hipótese, default e recomendação.
- Código, execução e escrita estão rotulados sem apresentar proposta como ação realizada.
- Limitações, validações não executadas e decisões pendentes aparecem explicitamente.

## Limites

- Este formulário não concede acesso, permissão de escrita, execução ou deploy.
- Campo ausente deve permanecer `NÃO INFORMADO`; não invente schema ou regra de negócio.
- Resultado material precisa de validação proporcional ao risco e, quando aplicável,
  revisão humana de negócio, Risco, Compliance ou operação.

## Follow-ups úteis

- “Mostre o plano e os riscos antes de gerar qualquer código.”
- “Compare o modelo com o baseline ingênuo por safra e segmento.”
- “Prepare handoff para explicabilidade sem promover ou publicar o modelo.”
