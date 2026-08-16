# Prompt: tutor de Databricks

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe o notebook, célula, tabela, erro ou
> pipeline com **Add context**/`@`. Skill: `@rodrigo-tutor-databricks`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Prompt pronto para colar

```text
Use @rodrigo-tutor-databricks para explicar o objeto anexado de forma progressiva,
tecnicamente precisa e conectada ao meu contexto.

CONTEXTO
- Objeto/pergunta: {{OBJETO_OU_PERGUNTA}}
- Meu nível atual: {{INICIANTE_INTERMEDIARIO_AVANCADO}}
- Profundidade: {{RESUMO_PASSO_A_PASSO_OU_LINHA_A_LINHA}}
- Objetivo prático: {{O_QUE_PRECISO_FAZER}}
- Ambiente/compute/runtime: {{AMBIENTE_OU_NAO_INFORMADO}}
- Contexto de negócio: {{CONTEXTO_NEGOCIO_OU_NAO_APLICAVEL}}
- Restrições: {{RESTRICOES}}

MÉTODO
1. Confirme o objeto anexado e destaque pré-requisitos ou versão que afetam a resposta.
2. Comece com um mapa mental curto; depois explique do conceito ao detalhe solicitado.
3. Use um exemplo mínimo e um exemplo aplicado ao contexto, sem inventar schema/dados.
4. Diferencie comportamento documentado, boa prática, escolha de arquitetura e opinião.
5. Ao explicar código, cubra entradas, saídas, execução lazy/eager, shuffle, custo,
   falhas comuns e como validar o resultado.
6. Não execute nem altere recursos. Se um experimento ajudar, proponha um teste pequeno,
   reversível e sem dados sensíveis, aguardando autorização.

CONTRATO DE SAÍDA
- Resposta direta em primeiro lugar.
- Explicação em camadas com termos definidos.
- Exemplo mínimo reproduzível.
- Armadilhas e checklist de verificação.
- Duas perguntas de autoavaliação com respostas recolhidas em seção separada.
- Referências oficiais da Databricks quando a versão ou o produto importar.

VALIDAÇÃO FINAL
- Não afirme que uma funcionalidade existe sem distingui-la de convenção personalizada.
- Declare incertezas e dependências de versão.
- Verifique que o exemplo não usa APIs obsoletas nem coleta dados em excesso.
```

## Exemplo mínimo

Objeto = `@cell`; nível = intermediário; profundidade = passo a passo; objetivo =
entender o shuffle deste join.

## Follow-ups úteis

- “Agora faça três perguntas para verificar se entendi.”
- “Compare esta abordagem com a alternativa Spark SQL.”
- “Mostre como observar o plano físico e interpretar os nós principais.”
