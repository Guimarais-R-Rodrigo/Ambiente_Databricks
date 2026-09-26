# Prompt: tutor de Databricks

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe o notebook, célula, tabela, erro ou
> pipeline com **Add context**/`@`. Skill: `@hub-ml-tutor-databricks`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{OBJETO_OU_PERGUNTA}}` | Anexe código/recurso e formule a dúvida. | Ancora a explicação no objeto real. | `@notebook` e dúvida sobre window |
| `{{INICIANTE_INTERMEDIARIO_AVANCADO}}` | Escolha seu nível atual. | Evita pular base ou repetir trivialidades. | intermediário |
| `{{RESUMO_PASSO_A_PASSO_OU_LINHA_A_LINHA}}` | Escolha granularidade. | Controla extensão e foco. | passo a passo |
| `{{O_QUE_PRECISO_FAZER}}` | Diga a tarefa que executará depois. | Transforma teoria em orientação acionável. | adaptar join temporal |
| `{{AMBIENTE_OU_NAO_INFORMADO}}` | Informe runtime, compute e linguagem. | Evita exemplo incompatível. | Databricks serverless; PySpark |
| `{{CONTEXTO_NEGOCIO_OU_NAO_APLICAVEL}}` | Explique domínio ou declare não aplicável. | Permite analogia correta sem inventar. | CRM de campanhas |
| `{{RESTRICOES}}` | Liste prazo, tópicos fora e ações proibidas. | Mantém a tutoria no escopo. | não executar; sem alterar notebook |

## Prompt pronto para colar

```text
Use @hub-ml-tutor-databricks para explicar o objeto anexado de forma progressiva,
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

- “Agora faça três perguntas para verificar se entendi.”
- “Compare esta abordagem com a alternativa Spark SQL.”
- “Mostre como observar o plano físico e interpretar os nós principais.”
