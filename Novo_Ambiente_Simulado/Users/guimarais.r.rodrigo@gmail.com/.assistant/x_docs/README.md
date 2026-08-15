# `x_docs` — documentação e governança do ecossistema

> **EXTENSÃO CUSTOMIZADA (`x_`) — não auto-descoberta pela Genie Code.**
> Nada aqui entra no contexto sozinho. Para usar um destes arquivos numa
> conversa, adicione-o com `@` ou **Add context**.

Esta pasta guarda o que explica e governa o ecossistema, em oposição ao que a
Genie Code executa. Se você procura *o que usar para uma tarefa*, comece pelo
catálogo; se procura *o que uma palavra significa*, pelo glossário.

## O que tem aqui

| Arquivo | Para que serve | Quando abrir |
|---|---|---|
| [catalogo_helpers.md](catalogo_helpers.md) | Mapa demanda → módulo de toda a biblioteca, com API e dependências | "preciso calcular PSI, o que uso?" |
| [glossario.md](glossario.md) | Termos separados por procedência: plataforma, modelagem e convenção do projeto | um termo travou a leitura |
| [notebooks/](notebooks/) | Quatro notebooks executáveis sobre os conceitos onde o erro custa caro | quer entender por que um helper existe |
| [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) | Modelo para criar uma skill nova | vai acrescentar uma skill |
| [skills_manifest.md](skills_manifest.md) | Manifesto funcional das skills existentes | quer a visão geral do que cada uma cobre |
| [ROADMAP_SKILLS.md](ROADMAP_SKILLS.md) | Backlog priorizado e gates pendentes | vai planejar o próximo passo |
| [LEGACY_CONTEXT.md](LEGACY_CONTEXT.md) | Contexto histórico do ambiente anterior | investigando por que algo é como é |
| `x_original_export_manifest.json` | Evidência da exportação original | rastreabilidade; consulta rara |

## Como acrescentar uma skill

Este é o procedimento que faltava estar escrito em algum lugar.

1. Copie [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) para
   `.assistant/skills/<nome-da-skill>/SKILL.md`.
2. No frontmatter, o campo `name` precisa ser **idêntico ao nome da pasta** — a
   validação reprova se divergirem.
3. Escreva a `description` dizendo **quando** usar, não apenas o que faz: é o
   único texto que a Genie Code lê para escolher entre as skills. Descrição vaga
   produz skill que nunca é selecionada, ou que rouba a vez de outra.
4. Declare os helpers do fluxo numa seção `## Usar helpers da biblioteca`,
   consultando o [catálogo](catalogo_helpers.md).
5. Rode o ciclo: validar, renderizar, publicar, conferir.
6. Teste o roteamento em **chat novo**: um pedido típico deve acionar a skill
   sozinha, e um pedido parecido de outro domínio não deve acioná-la.

O passo 6 não é formalidade. Descrições parecidas fazem a Genie Code carregar a
skill errada, e a resposta sai plausível o bastante para ninguém desconfiar.
