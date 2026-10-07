# Prompt: Cross-EDA para viabilidade de modelagem

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe todos os EDAs, tabelas e definições
> via **Add context**/`@`. Skill: `@hub-ml-cross-eda-ml`.

Antes de executar, siga a [skill selecionada](../../skills/hub-ml-cross-eda-ml/SKILL.md),
a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) e o contrato
da rota suportada. Helpers são componentes dessa rota, não um bypass. O
[Manual Técnico](../../MANUAL_TECNICO_V2.md#catalogo-helpers) é o catálogo integrado.

## Quando usar

Use depois de EDAs individuais para avaliar compatibilidade, joins, cobertura e
disponibilidade temporal de múltiplas fontes. Não use como substituto de EDA de uma
fonte ainda desconhecida.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{RECURSOS}}` | Anexe e nomeie cada EDA, notebook ou tabela. | Permite rastrear evidência por fonte. | `@eda_clientes`, `@eda_eventos` |
| `{{ENTIDADE_E_GRANULARIDADE}}` | Defina entidade âncora e uma linha por fonte. | Evita joins muitos-para-muitos ocultos. | cliente; evento por transação |
| `{{TARGET_E_DEFINICAO}}` | Defina evento, classe positiva e janela. | Alinha sinal e avaliação. | adesão em 60 dias |
| `{{PONTO_NO_TEMPO}}` | Informe quando a decisão é tomada. | Bloqueia informação futura. | fechamento do mês |
| `{{HORIZONTE}}` | Defina distância até o target. | Separa observação de resultado. | 60 dias |
| `{{CHAVES}}` | Mapeie chave de cada fonte até a âncora. | Torna o join executável e auditável. | conta→cliente por `id_cliente` |
| `{{PERIODOS}}` | Declare cobertura temporal por fonte. | Expõe lacunas e sobreposição. | CRM 2024–2026; eventos 2025–2026 |
| `{{FONTES_AUTORITATIVAS_OU_NAO_INFORMADO}}` | Indique a fonte de verdade por conceito. | Resolve conflitos entre tabelas. | cadastro mestre para segmento |
| `{{JOINS_SINAL_READINESS_OU_COMPLETO}}` | Escolha o foco ou peça avaliação completa. | Controla escopo da costura. | joins + readiness |
| `{{RESTRICOES}}` | Liste PII, permissões, custo e exclusões. | Evita acesso e combinação indevidos. | sem exportar CPF; somente leitura |

## Prompt pronto para colar

```text
Use @hub-ml-cross-eda-ml para comparar os recursos anexados e avaliar se formam uma
base de modelagem coerente, sem executar escrita ou treino.

CONTEXTO
- EDAs/notebooks/tabelas anexados: {{RECURSOS}}
- Entidade âncora e granularidade: {{ENTIDADE_E_GRANULARIDADE}}
- Target/evento: {{TARGET_E_DEFINICAO}}
- Cutoff/ponto de predição: {{PONTO_NO_TEMPO}}
- Horizonte: {{HORIZONTE}}
- Chaves de ligação por fonte: {{CHAVES}}
- Período esperado por fonte: {{PERIODOS}}
- Fonte de verdade por conceito: {{FONTES_AUTORITATIVAS_OU_NAO_INFORMADO}}
- Foco: {{JOINS_SINAL_READINESS_OU_COMPLETO}}
- Restrições e dados sensíveis: {{RESTRICOES}}

FLUXO
1. Faça inventário dos recursos realmente anexados; não invente resultados dos EDAs.
2. Compare granularidade, chaves, cobertura temporal, atualidade, completude, target,
   população e filtros. Marque incompatibilidades sem normalizá-las silenciosamente.
3. Proponha um grafo de joins e classifique cardinalidade esperada/observada. Calcule
   cobertura dos matches e risco de multiplicação, órfãos e viés de seleção.
4. Faça análise ponto-no-tempo: quando cada atributo passou a estar disponível e se
   pode vazar evento, tratamento ou resultado posterior ao cutoff.
5. Avalie complementaridade apenas com evidência; não confunda correlação com ganho
   incremental nem qualidade da fonte com poder preditivo.
6. Em alto volume, use agregações e amostras controladas. Não colete nem exiba PII.

CONTRATO DE SAÍDA
- Mapa de fontes e joins propostos.
- Matriz de compatibilidade por fonte e dimensão.
- Scorecard de readiness com critérios, evidências e ressalvas.
- Lista de riscos P0/P1/P2 e ações necessárias antes de feature engineering.
- Recomendação: prosseguir, prosseguir com condicionantes ou bloquear, com evidência.
- Código de validação de joins somente se solicitado, sem gravar resultados.

VALIDAÇÃO FINAL
- Confirme contagens antes/depois dos joins e cobertura por fonte/período.
- Separe fatos observados, inferências e itens não verificáveis.
- Declare explicitamente toda fonte não anexada ou EDA incompleta.
```

## Exemplo mínimo

Recursos = `@eda_clientes` e `@eda_transacoes`; entidade = cliente mensal; target =
churn em 90 dias; chaves = `id_cliente + data_snapshot`.

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

- “Gere somente os testes para validar cardinalidade e cobertura dos joins.”
- “Transforme os riscos P0 em critérios de bloqueio para feature engineering.”
- “Prepare um handoff factual para @hub-ml-feature-engineering.”
