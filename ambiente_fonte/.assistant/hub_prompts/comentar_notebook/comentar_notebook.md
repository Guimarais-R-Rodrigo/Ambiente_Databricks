# Prompt: documentar e comentar notebook

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe o notebook com **Add context** ou
> `@`. Para uma célula específica, use `@cell`. Skill: `@hub-ml-comentar-notebook`.

Antes de executar, siga a [skill selecionada](../../skills/hub-ml-comentar-notebook/SKILL.md),
a [policy vigente](../../hub_padroes/skill_enforcement/policy.json) e o contrato
da rota suportada. Helpers são componentes dessa rota, não um bypass. O
[Manual Técnico](../../MANUAL_TECNICO.md#catalogo-helpers) é o catálogo integrado.

## Escolha o modo

- `REVISÃO`: diagnostica e propõe alterações, sem editar.
- `EDIÇÃO`: aplica comentários e Markdown preservando o comportamento.
- `DOCUMENTAÇÃO`: cria narrativa e runbook sem refatorar código.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{NOTEBOOK_OU_CELULAS}}` | Anexe notebook ou selecione células. | Evita revisar versão/trecho errado. | `@02_feature_engineering` |
| `{{REVISAO_EDICAO_OU_DOCUMENTACAO}}` | Escolha revisar, editar ou só documentar. | Define revisão ou edição documental; código permanece preservado. | documentação |
| `{{PUBLICO_ALVO}}` | Informe quem usará o notebook. | Calibra contexto e linguagem. | analista novo na squad |
| `{{RESUMIDA_TECNICA_OU_DIDATICA}}` | Escolha profundidade e tamanho. | Evita comentário excessivo ou insuficiente. | técnica |
| `{{OBJETIVO}}` | Explique decisão e papel do notebook. | Dá sentido à narrativa. | gerar features mensais |
| `{{CONVENCOES}}` | Liste idioma, estrutura e padrão visual. | Mantém consistência com o projeto. | PT-BR; Markdown antes/depois |
| `{{RESTRICOES}}` | Declare células, APIs e resultados imutáveis. | Impede alteração funcional acidental. | não mudar SQL nem outputs |
| `{{SIM_NAO_NAO_INFORMADO}}` | Informe presença de PII ou lacuna. | Determina mascaramento e exemplos. | SIM; CPF e renda |

## Prompt pronto para colar

```text
Use @hub-ml-comentar-notebook para documentar o notebook anexado.

BRIEFING
- Notebook/células: {{NOTEBOOK_OU_CELULAS}}
- Modo: {{REVISAO_EDICAO_OU_DOCUMENTACAO}}
- Público: {{PUBLICO_ALVO}}
- Profundidade: {{RESUMIDA_TECNICA_OU_DIDATICA}}
- Objetivo de negócio: {{OBJETIVO}}
- Convenções/idioma: {{CONVENCOES}}
- Partes que não podem mudar: {{RESTRICOES}}
- Dados sensíveis presentes: {{SIM_NAO_NAO_INFORMADO}}

INSTRUÇÕES
1. Resuma o fluxo atual e identifique células, entradas, saídas e efeitos colaterais.
2. No modo REVISÃO, não edite: entregue proposta e exemplos.
3. No modo EDIÇÃO, preserve ordem, lógica, parâmetros, nomes públicos e resultados;
   não execute, refatore ou formate além do necessário sem autorização.
4. Use células Markdown para objetivo, pré-requisitos, parâmetros, etapas, validações,
   limitações e próximos passos. Comentários inline devem explicar intenção e risco,
   não repetir literalmente o código.
5. Marque pressupostos, TODOs e decisões pendentes; não invente regra de negócio.
6. Remova de exemplos segredos, tokens, caminhos pessoais e valores de PII.

CONTRATO DE SAÍDA
- Resumo das mudanças ou recomendações.
- No modo REVISÃO, proposta de organização; nos modos autorizados, documentação
  com sumário proporcional, preservando código e ordem.
- Descrição de inputs/outputs, compute/dependências e forma segura de execução.
- Alertas de qualidade, custo, segurança e idempotência encontrados.
- Lista explícita do que foi preservado e do que não foi possível validar.

VALIDAÇÃO FINAL
- Confirme que nenhuma lógica foi alterada inadvertidamente.
- Confirme que referências entre células continuam válidas.
- Diferencie comentário factual de recomendação.
```

## Exemplo mínimo

Notebook = `@churn_training`; modo = REVISÃO; público = cientistas de dados;
profundidade = técnica.

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

- “Aplique somente as mudanças P0 e P1 que não alteram comportamento.”
- “Crie um resumo executivo de uma página a partir do notebook.”
- “Explique @cell linha a linha e adicione apenas comentários indispensáveis.”
