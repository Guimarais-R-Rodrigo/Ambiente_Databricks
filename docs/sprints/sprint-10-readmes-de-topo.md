# Sprint 10 — os dois READMEs de topo

Data: 2026-08-17 · Executor: Claude · Escopo: `README.md` da raiz do repositório
e `.assistant/README.md`, na variante longa, absorvendo o glossário.

Estes dois são a porta de entrada: o primeiro para quem vai **manter** o Hub, o
segundo para quem vai **usá-lo**. Nenhum dos dois tinha sido tocado desde a
Sprint 2, e a biblioteca inteira mudou de forma no meio do caminho.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 12 aviso(s)
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
README.md (raiz)        396 linhas
.assistant/README.md    494 linhas
```

## O que estava desatualizado, e por quê importa

O README da raiz documenta os três comandos do ciclo **colando a saída real de
cada um**. Essa é a escolha certa — e é também a que envelhece sozinha. As três
saídas estavam da Sprint 2:

| Linha | Dizia | É |
|---|---|---|
| `markdown / links` | 103 arquivos / 109 links | 104 / 143 |
| `python (AST)` | 70 arquivos | 193 |
| `repo (corporativo)` | 409 arquivos varridos | 674 |
| render | 176 arquivos | 298 |
| verify | 175 esperados / 176 remotos | 297 / 298 |

E o bloco do validador **não mostrava as quatro guardas criadas depois** —
`pastas de objeto`, `contrato de dados`, `contrato de entrada` e `saída colada`.
Quem lesse o README para saber o que a validação cobre veria metade.

Elas ganharam uma tabela dizendo o que cada uma confere **e de qual defeito real
nasceu**, porque é isso que faz alguém levá-las a sério.

**Uma afirmação estava errada, não só velha:** o quadro de status dizia que
`prophet_wrapper` "segue sem combinação funcional". A Sprint 8 mostrou que
instala e ajusta um modelo completo.

## O glossário virou seção

Conforme §5 do plano. As 101 linhas do `GLOSSARIO.md` entraram como última seção
do `.assistant/README.md`, os subtítulos desceram um nível, e os cinco links que
apontavam para o arquivo foram reapontados para a âncora.

O `--verify` da publicação pegou o que a validação local não vê: o arquivo
continuava no workspace depois de removido da fonte. Removido à mão, como sempre.

**A contrapartida, registrada porque é real:** o resultado tem 494 linhas, e
glossário é documento de **consulta por termo** enquanto README é leitura linear.
Mitigado com uma tabela de navegação no topo — dez perguntas, dez âncoras —, que
é o que transforma um documento longo em um documento consultável.

## O que faltava, e era o mais importante

Nenhum dos dois READMEs mencionava o que esta fase inteira produziu: **cada um
dos 58 objetos tem um notebook próprio que o ensina**.

Ganhou seção própria no `.assistant/README.md`, com a estrutura da pasta, o que
se encontra dentro de um `exemplo_*` na ordem em que aparece, e três coisas que
alguém precisa saber antes de abrir o primeiro:

- no workspace o notebook aparece **sem** a extensão, e o módulo ao lado é
  arquivo comum — a diferença é o que mantém o `import` funcionando;
- os catorze objetos com dependência opcional **instalam sozinhos**, com `%pip`
  na primeira célula;
- o bloco de "não executado" é deliberado e confiável — significa motivo
  verificado, com o erro real citado.

A seção "quando **não** usar" ganhou destaque na descrição, porque é a que mais
economiza tempo e a que ninguém procura.

## O que fica para depois

| Item | Por quê |
|---|---|
| Dívida de saída colada: 12 notebooks | §12.1 do plano |
| Duplicação de cor em 12 módulos | §12.2 do plano; onze são higiene, um é decisão de produto |
| `ADR-0006` cita `GLOSSARIO.md` | é registro datado e imutável: descrevia corretamente o destino da Sprint 2 |
