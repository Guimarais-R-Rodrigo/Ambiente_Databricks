# Prompt: feature engineering temporal e governado

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe notebooks, tabelas e definição do
> target com **Add context**/`@`. Skill: `@hub-ml-feature-engineering`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Pré-requisito crítico

Defina o tempo de observação, o instante de predição e o horizonte do evento. Sem
esses três marcos, peça apenas um plano; não gere features finais.

## Prompt pronto para colar

```text
Use @hub-ml-feature-engineering para desenhar e, se autorizado, implementar features
reprodutíveis, sem leakage e compatíveis com o volume.

BRIEFING
- Entidade/granularidade: {{ENTIDADE_E_GRANULARIDADE}}
- Chave da entidade: {{CHAVE_ENTIDADE}}
- Target/evento positivo: {{TARGET_E_DEFINICAO}}
- Tempo de observação: {{JANELA_OBSERVACAO}}
- Instante de predição: {{PONTO_NO_TEMPO}}
- Horizonte do target: {{HORIZONTE}}
- Fontes anexadas e chaves: {{FONTES_E_JOINS}}
- Frequência de scoring: {{FREQUENCIA}}
- Features existentes: {{FEATURES_EXISTENTES_OU_NENHUMA}}
- Restrições/PII/compute: {{RESTRICOES}}
- Modo: {{PLANO_CODIGO_OU_IMPLEMENTACAO_AUTORIZADA}}

FLUXO
1. Confirme granularidade, disponibilidade temporal e momento real de cada fonte.
2. Crie uma especificação com nome, definição, fonte, janela, cutoff, fórmula, tipo,
   tratamento de nulos, owner e testes. Não use informação posterior à predição.
3. Proponha famílias comportamentais, temporais, RFV, estabilidade e contexto somente
   quando justificadas pelo caso; evite proxies sensíveis sem avaliação apropriada.
4. Valide cardinalidade e multiplicação de linhas antes/depois de cada join.
5. Prefira PySpark/Spark SQL, agregações incrementais e funções determinísticas. Evite
   Python UDF quando houver função nativa e não use `toPandas()` irrestrito.
6. Quando houver reuso entre treino e inferência, proponha publicação e lineage em
   Feature Engineering in Unity Catalog, sem assumir que já está configurado.
7. No modo PLANO, não gere escrita. No modo CÓDIGO, gere sem executar. Só implemente
   ou publique após autorização explícita e ambiente alvo confirmado.

CONTRATO DE SAÍDA
- Diagrama textual do ponto-no-tempo e fontes.
- Feature specification priorizada com risco de leakage e custo.
- Código parametrizado/idempotente, se solicitado.
- Testes: unicidade, cobertura, estabilidade, janela, cutoff e parity treino/inferência.
- Evidências, pressupostos, features rejeitadas e próximos passos.

VALIDAÇÃO FINAL
- Demonstre que nenhuma feature vê o futuro do target.
- Confirme contagens e granularidade após joins.
- Separe ganho hipotético de ganho medido; não faça alegação regulatória automática.
```

## Exemplo mínimo

Entidade = cliente; target = resgate em 90 dias; ponto no tempo = último dia de cada
mês; janela de observação = 12 meses anteriores.

## Follow-ups úteis

- “Audite a especificação exclusivamente para leakage temporal.”
- “Implemente apenas as cinco features P0 em PySpark, sem executar escrita.”
- “Proponha a estrutura de feature table e os testes de parity.”
