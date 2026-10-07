# Prompt: feature engineering temporal e governado

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe notebooks, tabelas e definição do
> target com **Add context**/`@`. Skill: `@hub-ml-feature-engineering`.

Antes de executar, siga a [skill selecionada](../../skills/hub-ml-feature-engineering/SKILL.md),
a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) e o contrato
da rota suportada. Helpers são componentes dessa rota, não um bypass. O
[Manual Técnico](../../MANUAL_TECNICO_V2.md#catalogo-helpers) é o catálogo integrado.

## Pré-requisito crítico

Defina o tempo de observação, o instante de predição e o horizonte do evento. Sem
esses três marcos, peça apenas um plano; não gere features finais.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{ENTIDADE_E_GRANULARIDADE}}` | Defina entidade e o que cada linha representa. | Evita features em grão incompatível. | cliente no mês |
| `{{CHAVE_ENTIDADE}}` | Informe chave estável simples/composta. | Permite janelas e joins corretos. | `id_cliente` |
| `{{TARGET_E_DEFINICAO}}` | Defina evento positivo, regra e exclusões. | Evita leakage semântico. | contrata em 90 dias |
| `{{JANELA_OBSERVACAO}}` | Defina quanto passado pode ser usado. | Controla disponibilidade histórica. | 180 dias anteriores |
| `{{PONTO_NO_TEMPO}}` | Informe o instante de scoring. | Impede usar dados publicados depois. | último dia útil do mês |
| `{{HORIZONTE}}` | Defina a janela futura do target. | Separa feature e rótulo. | 90 dias |
| `{{FONTES_E_JOINS}}` | Liste fontes, chaves, timestamps e atraso. | Permite junção point-in-time. | transações por conta; atraso 1 dia |
| `{{FREQUENCIA}}` | Informe periodicidade de geração/scoring. | Orienta janelas e materialização. | mensal |
| `{{FEATURES_EXISTENTES_OU_NENHUMA}}` | Anexe catálogo atual ou declare nenhuma. | Evita duplicar feature existente. | `@feature_spec_v2` |
| `{{RESTRICOES}}` | Liste PII, features proibidas e compute. | Impõe governança e viabilidade. | sem atributo sensível; serverless |
| `{{PLANO_CODIGO_OU_IMPLEMENTACAO_AUTORIZADA}}` | Escolha plano, código ou implementação autorizada. | Separa desenho de mutação. | código sem executar |

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

- “Audite a especificação exclusivamente para leakage temporal.”
- “Implemente apenas as cinco features P0 em PySpark, sem executar escrita.”
- “Proponha a estrutura de feature table e os testes de parity.”
