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

---

## Auditoria da Sprint 10 — 12 achados, todos procedentes

O auditor seguiu o README ao pé da letra: publicou um notebook no Free com os
trechos copiados literalmente, rodou como job, recuperou o `GLOSSARIO.md` por
`git show` e comparou termo a termo, e varreu o repositório contra cada número
afirmado.

### O achado que fecha o círculo

**As três saídas coladas estavam erradas — e erravam exatamente pelo arquivo que
esta sprint apagou.**

Capturei os números, depois apaguei o `GLOSSARIO.md`. Quatro contagens caíram em
1 (markdown, arquivos do repo, renderizados, publicados) e uma subiu em 2
(`repo (links)`, porque os READMEs ganharam links). Seis números discordando na
primeira execução.

Esta sprint existia para corrigir saídas desatualizadas. **Ela reproduziu o
defeito um commit adiante**, e o auditor demonstrou a causa com
`git cat-file -e HEAD~1:` contra `HEAD:`.

A correção do número é trivial. A que importa é de processo, e ficou escrita no
próprio README, onde a próxima pessoa vai ler: **editar → rodar → colar →
commitar**, com a captura depois da última edição do commit.

### O README prometia o que a biblioteca não entrega

Duas afirmações erradas na seção nova, a que eu tinha chamado de "o buraco
maior":

**"O que você encontra dentro, sempre na mesma ordem"** — e a Leitura, com a
saída real colada, falta em **11 dos 58**. Pior: eu ilustrei a seção com
`pit_join` e escrevi "← abra este primeiro". `pit_join` é um dos onze. O
recém-chegado abriria justamente o contraexemplo.

Trocado por `safe_display`, que cumpre o contrato, e os onze passaram a estar
declarados com ponteiro para §12.1. A seção "quando não usar", essa sim, existe
nos 58 — o auditor conferiu um a um.

**"Três casos conhecidos" de bloco não-executado** — e os três estavam errados:

| Eu afirmava | É |
|---|---|
| MLflow não abre run no serverless | ✅ bloco real |
| API clássica de `pyspark.ml` não é exposta | ❌ **não é bloco de não-executado** — `correlation_matrix` executa e cola o `Py4JError` real |
| duas funções do pandas exigem biblioteca ausente | ⚠️ sobrou **uma**: o `jinja2` foi resolvido na própria Sprint 9 |

E havia um quarto bloco que a lista não mencionava, no template de
`hub_padroes/`, ensinando uma limitação do Prophet que deixou de existir.

### Uma promessa sobre o validador que o validador não cumpria

O README dizia: *"se qualquer uma das duas linhas vier zero, a proteção
correspondente não rodou — e isso reprova a execução"*. Só `check_repo_corporate`
tinha essa guarda. `check_repo_links` devolvia `0` e seguia em silêncio.

Aqui preferi consertar o código a enfraquecer a frase. Provado com sonda que
troca `REPO_ROOT` por diretório vazio:

```text
check_repo_links       verificados=0  -> REPROVA
check_repo_corporate   verificados=0  -> REPROVA
```

### Os demais

| # | Achado | Correção |
|---|---|---|
| 5 | "quatorze objetos de `ml/` instalam sozinhos" — são **quinze**, com `display/dataframe_styled` idêntico | contagem e escopo corrigidos |
| 6 | `docs/testes/spark/README.md` ainda declarava `prophet_wrapper` não verificado, contra três outras fontes, e usava caminhos `x_snippets/` de antes da Sprint 2 | bloco de situação reescrito para 14 de 14, com nota datada da reversão; caminhos corrigidos |
| 7 | o "Mapa do repositório" omitia o `PLANO_HUB.md` — o plano das 12 sprints, citado 20 linhas adiante | acrescentado |
| 8 | o catálogo de helpers, que o README aponta como o jeito de achar módulo, não tinha `constants.emojis` nem `constants.styles` | três linhas acrescentadas, incluindo `constants.colors` |
| 9 | duas descrições de "nasceu de" na tabela de guardas não batiam com o docstring | alinhadas |
| 10 | os dois READMEs usavam denominadores diferentes (60 e 58) sem reconciliar | nota explicando que os 60 incluem os 2 exemplares de template |
| 11 | `checklist-replicacao.md` dizia 6 diretórios na linha 13 e 4 na 86 | a contagem saiu da linha 13, que o banner de obsolescência já cobre |
| 12 | falta de linha em branco depois de `## Glossário` | corrigida |

### O que a auditoria confirmou intacto

O item mais importante: **seguir o README funciona**. O auditor publicou um
notebook com os trechos copiados literalmente e rodou como job — os caminhos de
instalação existem na caixa exata, os três imports funcionam, as três saídas de
confirmação batem caractere por caractere, e o "engano mais comum" documentado
reproduz a mensagem prometida.

O glossário migrou limpo: **65 termos antes, 65 depois**, zero alterados, zero
perdidos, hierarquia correta, e a única prosa descartada foi o cabeçalho que
descrevia o arquivo como documento avulso. Nenhum link vivo aponta para ele, e as
onze âncoras da tabela de navegação resolvem — inclusive as acentuadas.

### O que nenhum portão veria

Os doze achados. Os portões conferem estrutura, sintaxe, link e tipo de objeto;
nenhum lê uma frase em português e pergunta se ela é verdade. E há uma ironia
específica no achado 1: **o validador imprimia a resposta certa na tela enquanto
o README exibia a errada.**

O auditor propôs a guarda que fecharia esse caso — extrair os blocos de saída do
README, reexecutar os comandos e falhar na divergência. Fica registrada aqui como
candidata para a Sprint 12; não a construí agora porque ela precisa de um
contrato entre o bloco e o comando que o produz, e isso é desenho, não conserto.
