# Prompt: documentar e comentar notebook

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe o notebook com **Add context** ou
> `@`. Para uma célula específica, use `@cell`. Skill: `@rodrigo-comentar-notebook`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Escolha o modo

- `REVISÃO`: diagnostica e propõe alterações, sem editar.
- `EDIÇÃO`: aplica comentários e Markdown preservando o comportamento.
- `DOCUMENTAÇÃO`: cria narrativa e runbook sem refatorar código.

## Prompt pronto para colar

```text
Use @rodrigo-comentar-notebook para documentar o notebook anexado.

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
- Notebook organizado com sumário visual proporcional ao tamanho.
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

## Follow-ups úteis

- “Aplique somente as mudanças P0 e P1 que não alteram comportamento.”
- “Crie um resumo executivo de uma página a partir do notebook.”
- “Explique @cell linha a linha e adicione apenas comentários indispensáveis.”
