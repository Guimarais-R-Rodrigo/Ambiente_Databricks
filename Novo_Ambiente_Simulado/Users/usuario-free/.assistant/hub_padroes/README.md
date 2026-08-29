# `hub_padroes` — os moldes do Hub

> **EXTENSÃO DO HUB (`hub_`) — NÃO AUTO-DESCOBERTA.** Os moldes desta pasta são
> consulta humana: o Genie Code não os lê nem os aplica sozinho. Para que um
> deles chegue ao chat, anexe o arquivo com `@`/Add context — ou use
> `@hub-ml-criar-objeto`, a skill que faz cumprir esta forma.

Os templates que todo objeto do Hub segue, com um exemplo preenchido de cada um.

## Para que serve

Um Hub usado por uma equipe inteira falha por deriva antes de falhar por erro:
cada pessoa escreve um README com uma cara, um notebook com outra profundidade,
um snippet com outra convenção de nome. Seis meses depois ninguém acha nada e
todo mundo reescreve o que já existia.

Esta pasta é o antídoto. Use quando for **criar** qualquer objeto novo, ou quando
estiver em dúvida sobre a forma de um que já existe.

## Como usar

Copie o template do tipo de objeto que você vai criar, a partir da tabela
abaixo, e siga o checklist que fecha cada um.

> **Para aplicar estes moldes, use `@hub-ml-criar-objeto`.** Ela conduz a
> escolha do tipo, aponta o template certo e cobra o que a validação não
> confere. A cópia manual continua funcionando e é o caminho de quem não está no
> Genie Code.

## O que existe aqui

| Tipo | Template | Exemplo preenchido |
|---|---|---|
| README | [readme/template.md](readme/template.md) | [readme/exemplo.md](readme/exemplo.md) |
| Snippet | [snippet/template.md](snippet/template.md) | [snippet/taxa_resposta_campanha/](snippet/taxa_resposta_campanha/) |
| Script | [script/template.md](script/template.md) | [script/checar_base_campanha/](script/checar_base_campanha/) |
| Prompt | [prompt/template.md](prompt/template.md) | [prompt/analisar_campanha/](prompt/analisar_campanha/) |
| Skill | [skill/template.md](skill/template.md) | [skill/exemplo/](skill/exemplo/) |
| Notebook | [notebook/template.py](notebook/template.py) | os notebooks dos exemplos acima |
| Auditoria de sprint | [auditoria/template.md](auditoria/template.md) | — |
| Proveniência de output | [output/proveniencia.md](output/proveniencia.md) | bloco para artefato durável |

**Seis tipos, e a lista é fechada.** Se algo não é README, snippet, script,
prompt, skill ou notebook, não é objeto do Hub e não ganha template aqui. Foi
uma lista aberta que transformou a antiga pasta de documentação num depósito.
`auditoria/` e `output/` são padrões transversais de processo, não novos tipos de
objeto.

### Um tema atravessa todos os exemplos

Análise de campanha de CRM: o snippet `taxa_resposta_campanha`, o script
`checar_base_campanha`, o prompt `analisar_campanha` e a skill
`hub-ml-analise-campanha`. Dá para comparar os quatro lado a lado e ver o que
muda de forma entre eles.

O tema foi escolhido por ser do domínio da equipe e trivial no enunciado —
respondentes sobre contatados —, de modo que a atenção sobre para a **estrutura**,
que é o que os exemplos existem para ensinar.

## Limites e armadilhas

- **A skill de exemplo não entra no roteamento.** `skill/exemplo/SKILL.md` é
  publicado junto com esta pasta, como todo o resto — mas a descoberta do Genie
  Code é escopada a `.assistant/skills/`, e ele não está lá. Não o copie para
  lá: com `name` válido e uma `description` desenhada para vencer vocabulário de
  campanha, ele passaria na validação e disputaria roteamento com as skills
  reais.
- **Exemplo não é biblioteca.** `taxa_resposta_campanha` e `checar_base_campanha`
  são material de referência: não os importe em trabalho real. O que serve para
  produção está em `hub_snippets/` e `hub_scripts/`.
- **Template não substitui revisão.** Ele garante forma, não conteúdo. Um
  notebook no formato certo com explicação errada continua errado.
- **Não há README em cada subpasta**, de propósito: seria um sétimo lugar para
  atualizar a cada mudança de padrão, e cada `template.md` já abre dizendo
  quando se aplica. Em compensação, quem entra direto numa subpasta perde três
  coisas que só existem aqui — por isso cada template repete, no topo, a lista
  fechada de tipos, a distinção snippet × script e o aviso de que `exemplo/` não
  é biblioteca.

## Onde continuar

- Para criar um objeto: copie o template do tipo, na tabela acima.
- Para entender um termo: o vocabulário está no
  [README do `.assistant`](../README.md).
- Para auditar o resultado de uma sprint: [auditoria/](auditoria/).
