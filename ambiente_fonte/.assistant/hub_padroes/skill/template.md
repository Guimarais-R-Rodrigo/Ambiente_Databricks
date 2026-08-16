# Template — Agent Skill do Hub

Use quando for criar uma skill nova em `.assistant/skills/`. Uma skill é uma
**pasta** cujo nome é idêntico ao campo `name` do frontmatter, contendo um
`SKILL.md` e, opcionalmente, uma subpasta `templates/`.

```text
.assistant/skills/hub-ml-<tema>/
├── SKILL.md
└── templates/          # opcional: saídas modelo que a skill referencia
```

Nome com **hífen**, sempre: `hub-ml-analise-campanha`. É o único objeto do Hub
que usa hífen, porque é a plataforma que o nomeia, não o Python.

## O frontmatter

```yaml
---
name: hub-ml-analise-campanha
description: <quando usar, não o que faz>
---
```

Só dois campos. O padrão Agent Skills admite outros, e este pacote não os usa: só
a `description` entra no roteamento, então campo extra vira texto que ninguém lê
e que envelhece sem que nada acuse.

## A `description` é a skill inteira, do ponto de vista do roteamento

O Genie Code decide qual skill carregar lendo **apenas** a `description`. Nunca o
corpo. Isso tem três consequências práticas:

| Consequência | O que fazer |
|---|---|
| Descrição vaga produz skill que nunca é escolhida | escreva o vocabulário do domínio, não o nome da tarefa |
| Descrição ampla demais rouba a vez de outra | delimite o que ela **não** cobre |
| Alterar a `description` invalida a certificação de roteamento | refaça os testes daquela skill e das que competem no mesmo vocabulário |

Escreva **quando usar**, não o que faz:

```text
description: Analisa resultado de campanha de relacionamento encerrada —
  taxa de resposta por segmento e canal, precisão da estimativa e
  recomendação de alocação de orçamento. Use quando a pergunta for onde
  investir a próxima campanha. Não cobre desenho experimental nem
  atribuição de causa.
```

O último período é o que evita colisão. Uma skill que não diz o que deixa de
fora compete com todas as vizinhas.

## O corpo

| Seção | Conteúdo |
|---|---|
| Quando esta skill se aplica | o caso típico e dois contra-exemplos |
| Fluxo | os passos, na ordem, com o que decidir em cada um |
| Usar helpers da biblioteca | tabela demanda → módulo, **declarada explicitamente** |
| O que nunca fazer | as armadilhas do domínio |
| Formato de saída | o que entregar, e para quem |

A seção de helpers não é opcional e não é decorativa: o Genie Code **não**
descobre `hub_snippets` sozinho. A skill recomenda o módulo no texto que injeta,
e quem importa é a pessoa, no notebook (ADR-0004).

## Antes de dar por pronto

```text
[ ] o nome da pasta é idêntico ao campo name
[ ] a description diz quando usar e o que não cobre
[ ] os helpers estão declarados por caminho de import
[ ] o SKILL.md tem menos de 500 linhas (acima disso, use progressive disclosure)
[ ] forward test em chat novo: um caso positivo, um negativo e a @menção
[ ] python tools/validate_assistant.py aprovado
```

O forward test não é formalidade. Descrições parecidas fazem o Genie Code
carregar a skill errada, e a resposta sai plausível o bastante para ninguém
desconfiar.

O exemplo preenchido está em [`exemplo/SKILL.md`](exemplo/SKILL.md) — e **não é
publicado**, para não disputar roteamento com as skills reais.
