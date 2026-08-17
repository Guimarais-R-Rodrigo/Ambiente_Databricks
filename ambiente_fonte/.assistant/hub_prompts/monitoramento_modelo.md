# Prompt: monitoramento de modelo

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe modelo, baseline, dados atuais,
> endpoint/job e métricas com **Add context**/`@`. Skill: `@hub-ml-monitoramento-modelo`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Antes de usar

Defina evento positivo, direção das métricas, janela de referência e atraso do rótulo.
Thresholds devem ser calibrados ao caso; os exemplos não são normas universais.

## Prompt pronto para colar

```text
Use @hub-ml-monitoramento-modelo para desenhar ou avaliar monitoramento técnico e de
negócio do modelo anexado, sem alterar produção.

CONTEXTO
- Modelo/run/version: {{MODELO}}
- Serving endpoint, job ou pipeline: {{CAMINHO_INFERENCIA}}
- Baseline de referência: {{BASELINE_E_PERIODO}}
- Dados atuais e janela: {{DADOS_ATUAIS_E_JANELA}}
- Target/evento e atraso do rótulo: {{TARGET_E_LABEL_DELAY}}
- Métricas e direção de melhora: {{METRICAS_DIRECAO}}
- Segmentos críticos: {{SEGMENTOS}}
- SLOs/thresholds existentes: {{LIMITES_OU_PROPOR}}
- Frequência e owners: {{FREQUENCIA_OWNERS}}
- Modo: {{DESENHO_DIAGNOSTICO_CODIGO_OU_EXECUCAO_AUTORIZADA}}

FLUXO
1. Confirme lineage entre modelo, features, inferências, predições e rótulos.
2. Separe saúde operacional (erro, latência, throughput), qualidade dos dados,
   drift, qualidade preditiva, calibração e métricas de negócio.
3. Compare sempre com baseline e direção corretos; melhoria não deve gerar alerta por
   causa de `abs(delta)`. Inclua amostra, volume, incerteza e sazonalidade.
4. Trate ausência/nulos como categoria observável quando relevante e monitore
   cobertura/latência de rótulos antes de calcular performance.
5. Proponha níveis de alerta, owner, janela, deduplicação, runbook e critério de
   resolução. Retreino deve ser decisão governada, não reação automática a um ponto.
6. Não altere endpoint, registre webhooks, reinicie job ou promova modelo sem pedido
   separado e autorização explícita.

CONTRATO DE SAÍDA
- Mapa de monitoramento e lacunas de observabilidade.
- Catálogo de métricas com fórmula, fonte, janela, direção, limite e owner.
- Diagnóstico com evidência e severidade, distinguindo incidente de variação esperada.
- Código/queries idempotentes, se solicitado.
- Runbook e critérios de investigação, rollback e eventual retreino.

VALIDAÇÃO FINAL
- Confirme alinhamento temporal predição-rótulo e denominadores.
- Teste cenários de melhora, piora, sem rótulo, nulos e baixo volume.
- Não atribua causa ao drift sem investigação adicional.
```

## Exemplo mínimo

Modelo = churn versão 7; baseline = jan–mar; janela atual = julho; label delay = 90
dias; métricas = PR-AUC (maior melhor), Brier (menor melhor), erro e latência p95.

## Follow-ups úteis

- “Crie testes unitários para direção e severidade dos alertas.”
- “Investigue o drift por segmento sem acionar retreino.”
- “Proponha um runbook P0/P1/P2 com owners.”
