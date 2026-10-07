# Template — Agent Skill do Hub

> Um dos **seis** tipos de objeto do Hub, e a lista é fechada. Skill é o único
> que a plataforma descobre sozinha, e o único com hífen no nome. O exemplo em
> `exemplo/` **não deve ser copiado para `.assistant/skills/`**.

Use quando for criar uma skill nova em `.assistant/skills/`. Uma skill é uma
**pasta** cujo nome é idêntico ao campo `name` do frontmatter, contendo um
`SKILL.md` e, opcionalmente, recursos relativos como templates, referências e
scripts.

```text
.assistant/skills/hub-ml-<tema>/
├── SKILL.md
├── templates/          # opcional: saídas modelo
├── references/         # opcional: documentação consultada sob demanda
└── scripts/            # opcional: automação executável da própria skill
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

Este pacote padroniza somente os dois campos obrigatórios. A superfície mínima
reduz metadado sem gate e mantém compatibilidade com a estrutura documentada pela
Databricks; recursos adicionais pertencem ao corpo e aos caminhos relativos da
skill.

## A `description` participa do roteamento

O Genie Code avalia o pedido contra a `description` para carregar skills
relevantes. O corpo e os recursos orientam a tarefa depois do carregamento.
Isso tem três consequências práticas:

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
descobre `hub_snippets` sozinho. A skill declara o módulo; a execução exige importação e chamada explícita no runtime. Quando houver runner canônico para a etapa protegida, use essa rota e seus verificadores, preservando a obrigação de declaração de helpers (ADR-0004).

## Declarar a política SEF proporcional ao risco

Toda skill publicada no catálogo deve possuir uma entrada na policy canônica do
Skill Enforcement Framework. A policy separa duas coisas que não podem ser
confundidas:

- `current_level`: nível realmente sustentado pelos artefatos existentes;
- `target_level`: direção de migração aprovada, sem alegar implementação.

Criar ou editar um `SKILL.md` não promove automaticamente o nível. Para declarar
L1 é necessário contrato estruturado; L2 exige preflight; L3 exige rota
determinística e Receipt; L4 exige Postflight fail-closed antes de conclusão
homologada. Skills editoriais podem permanecer em L0/L1 quando isso for
proporcional ao risco.

O `rollout_mode` também não deve ser elevado por intenção. `audit` mede sem
transformar o target em gate já existente; `warn` exige revisão explícita do
desvio; `enforce` só é coerente quando a superfície implementada realmente
pode bloquear homologação.

Antes de considerar a mudança pronta, o validador geral e a certificação SEF
pertinente devem confirmar policy, contratos e artefatos. Teste conversacional no
Genie Code continua separado porque estrutura válida não prova aderência do
agente.

## Antes de dar por pronto

O checklist é **um só para os seis tipos**, e mora em
[`skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md`](../../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).
Ele separa o que um terceiro consegue conferir do que é juízo de quem escreveu, e
tem um bloco específico para skill.

Verifique também os requisitos específicos deste tipo:

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
