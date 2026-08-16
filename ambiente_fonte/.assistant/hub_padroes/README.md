# `hub_padroes` — os moldes do Hub

Os templates que todo objeto do Hub segue, com um exemplo preenchido de cada um.

## Para que serve

Um Hub usado por uma equipe inteira falha por deriva antes de falhar por erro:
cada pessoa escreve um README com uma cara, um notebook com outra profundidade,
um snippet com outra convenção de nome. Seis meses depois ninguém acha nada e
todo mundo reescreve o que já existia.

Esta pasta é o antídoto. Use quando for **criar** qualquer objeto novo, ou quando
estiver em dúvida sobre a forma de um que já existe.

## Como usar

Peça à skill, que aplica o template certo e monta a estrutura de pastas:

```text
@hub-ml-criar-objeto preciso de um snippet novo em hub_snippets/spark que
calcule a cobertura de uma feature ao longo do tempo
```

Ou copie o template à mão, a partir da tabela abaixo.

## O que existe aqui

| Tipo | Template | Exemplo preenchido |
|---|---|---|
| README | [readme/template.md](readme/template.md) | [readme/exemplo.md](readme/exemplo.md) |
| Snippet | [snippet/template.md](snippet/template.md) | [snippet/exemplo/](snippet/exemplo/) |
| Script | [script/template.md](script/template.md) | [script/exemplo/](script/exemplo/) |
| Prompt | [prompt/template.md](prompt/template.md) | [prompt/exemplo/](prompt/exemplo/) |
| Skill | [skill/template.md](skill/template.md) | [skill/exemplo/](skill/exemplo/) |
| Notebook | [notebook/template.py](notebook/template.py) | os notebooks dos exemplos acima |
| Auditoria de sprint | [auditoria/template.md](auditoria/template.md) | — |

**Seis tipos, e a lista é fechada.** Se algo não é README, snippet, script,
prompt, skill ou notebook, não é objeto do Hub e não ganha template aqui. Foi
uma lista aberta que transformou a antiga pasta de documentação num depósito.

### Um tema atravessa todos os exemplos

Análise de campanha de CRM: o snippet `taxa_resposta_campanha`, o script
`checar_base_campanha`, o prompt `analisar_campanha` e a skill
`hub-ml-analise-campanha`. Dá para comparar os quatro lado a lado e ver o que
muda de forma entre eles.

O tema foi escolhido por ser do domínio da equipe e trivial no enunciado —
respondentes sobre contatados —, de modo que a atenção sobre para a **estrutura**,
que é o que os exemplos existem para ensinar.

## Limites e armadilhas

- **A skill de exemplo não é publicada.** `skill/exemplo/SKILL.md` fica aqui e
  **não** vai para `.assistant/skills/`. Publicada, entraria no roteamento real e
  disputaria vocabulário com as skills de verdade.
- **Exemplo não é biblioteca.** `taxa_resposta_campanha` e `checar_base_campanha`
  são material de referência: não os importe em trabalho real. O que serve para
  produção está em `hub_snippets/` e `hub_scripts/`.
- **Template não substitui revisão.** Ele garante forma, não conteúdo. Um
  notebook no formato certo com explicação errada continua errado.
- **Não há README em cada subpasta**, de propósito: cada `template.md` já abre
  dizendo quando se aplica, e um README ao lado repetiria isso — que é
  exatamente o que a regra de duplicação do template de README proíbe.

## Onde continuar

- Para criar um objeto: `@hub-ml-criar-objeto`.
- Para entender um termo: o vocabulário está no
  [README do `.assistant`](../README.md).
- Para auditar o resultado de uma sprint: [auditoria/](auditoria/).
