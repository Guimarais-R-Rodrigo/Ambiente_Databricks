# Prompt: análise de resultado de campanha

> **Exemplo dos padrões do Hub.** Objeto customizado, **não auto-descoberto**:
> nada aqui entra no contexto sozinho. Skill recomendada:
> `@hub-ml-eda-profissional`.

Este formulário produz a análise de uma campanha encerrada com o objetivo de
decidir a alocação da próxima. Ele existe porque o pedido informal — "me dá a
taxa de resposta por segmento" — devolve uma tabela correta que sustenta uma
decisão errada.

## Antes de colar

Preencha `{{TABELA}}`, `{{PERIODO}}` e `{{ORCAMENTO_CONTATOS}}`. Se não souber o
nome da tabela, peça antes `/findTables`.

Declare o orçamento em **número de contatos**, não em reais: é a restrição que
transforma "qual segmento responde mais" em "onde alocar", e é justamente ela
que impede o assistente de recomendar um segmento de 28 pessoas.

## Prompt pronto para colar

```text
Analise o resultado da campanha de relacionamento armazenada em {{TABELA}}.

CONTEXTO
- Unidade de análise: um cliente contatado por campanha.
- Colunas: id_cliente, segmento, canal, dt_contato, respondeu (1 = respondeu).
- Período: {{PERIODO}}, campanha única.
- Decisão que depende disto: para onde direcionar o orçamento da próxima
  campanha, que atende cerca de {{ORCAMENTO_CONTATOS}} clientes.

O QUE PRECISO
1. Taxa de resposta por segmento e por canal.
2. Uma recomendação de priorização: quais segmentos devem receber a maior
   parte dos {{ORCAMENTO_CONTATOS}} contatos da próxima campanha, e por quê.
3. O que nestes dados não sustenta a recomendação — o que você não conseguiu
   concluir com o que existe aqui.

FORMATO
- Código PySpark reproduzível, com a saída que você obteve.
- Uma síntese executiva de no máximo 8 linhas, em português, para quem decide
  orçamento e não lê código.
```

## O que conferir na resposta

O item 3 não é formalidade: é o que separa análise de relatório. Se a resposta
não disser o que **não** sabe, ela está afirmando mais do que os dados sustentam.

Três verificações concretas, na ordem em que valem a pena:

| Verifique | Por quê |
|---|---|
| A base de cada segmento aparece junto da taxa | taxa sem `n` não sustenta comparação |
| A recomendação respeita o tamanho do segmento | segmento minúsculo com taxa alta é irrelevante, por mais real que a diferença seja |
| A recontagem sobre as mesmas pessoas foi questionada | responder a um segundo contato não é o mesmo processo que responder ao primeiro |

A terceira é a que quase sempre falta — inclusive em resposta de assistente
competente. Ver o registro em
[`exemplo_analisar_campanha.py`](exemplo_analisar_campanha.py).

## Limites deste prompt

Ele descreve o que aconteceu; não isola o efeito da oferta, do canal ou do momento. Este briefing não estabelece identificação causal. Qualquer afirmação causal exige desenho e pressupostos próprios.

## Guia do exemplar

Para entender o contexto de aplicação, os requisitos e os limites antes de
preencher, consulte o [README deste objeto](README.md). O formulário e o bloco
colável acima foram preservados. Seu preenchimento não autoriza escrita ou
execução adicional por si só.
