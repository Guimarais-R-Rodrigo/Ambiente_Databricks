# Sprint 11 — a skill `hub-ml-criar-objeto`

Data: 2026-08-17 · Executor: Claude · Escopo: uma skill nova, que aplica os
moldes de `.assistant/hub_padroes/`. `EXPECTED_SKILLS` sobe de 12 para 13.

É a **primeira mudança em roteamento desde a Sprint 3**, e a única desta fase que
adiciona um competidor ao pool de descoberta automática.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 12 aviso(s) — skills: 13
publicar_free.py        APROVADO: 0 problema(s) — skills 13/13, obsoletos: 0
forward test            PENDENTE — depende de interação humana no Genie Code
```

## Por que uma só, e por que esta

O pedido original falava em "uma skill de Hub Documents ou Documentation". A
calibração do plano fechou em **uma**, com nome `hub-ml-criar-objeto`.

A razão de ser é concreta: os seis templates de `hub_padroes/` existem desde a
Sprint 1 e **não são auto-descobertos**. Sem uma skill que os aplique, cada
objeto novo depende de alguém lembrar de anexar o molde certo — e a experiência
das dez sprints anteriores diz que não lembra. Os defeitos recorrentes desta fase
(saída não colada, notebook escrito contra API imaginada, tipo errado escolhido)
são todos falhas de aplicação de template.

A skill existe por causa da decisão §2.1: `hub_padroes/` mora dentro de
`.assistant/` e por isso chega ao workspace. Numa pasta da raiz do repositório os
templates seriam invisíveis para ela.

## O que a skill faz de diferente de um "gerador"

Ela não gera arquivo pronto. Ela **conduz**, e a diferença está em três pontos:

**Primeiro, escolher o tipo — e recusar quando não couber.** A lista é fechada
em seis, e a distinção entre snippet e script é a que mais erra: snippet recebe
**dado**, script recebe **nome de tabela**, e isso muda a assinatura. A skill
manda confirmar o tipo com quem pediu antes de escrever qualquer linha, e dizer
"não cabe" em vez de forçar o mais próximo.

**Segundo, exigir que o template seja anexado.** Ela declara explicitamente que
`hub_padroes/` não é auto-descoberto, e que trabalhar de memória significa
aplicar uma versão antiga do formato.

**Terceiro, carregar as armadilhas que custaram caro.** Cada regra do corpo tem
um custo real por trás, e a skill diz qual:

| Regra | O que ela evita |
|---|---|
| `__init__.py` sai da ferramenta, exaustivo | curadoria plausível de `constants/colors` exportaria 5 de 22 e quebraria quem depende |
| cite o número obtido, não o pretendido | a prosa que descreve uma saída diferente da produzida |
| cole a saída literal; corte declarado, nunca completado | seis blocos editados numa sprint, um deles omitindo o que contradizia o texto |
| converter é mover, e melhorar é commit separado | a diferença só aparece quando algo que funcionava para de funcionar |
| confira o nome contra os existentes | `drift_detection` e `drift_detector` já convivem |

**E ela cobra o catálogo.** É o item mais esquecido: dois objetos ficaram fora do
`CATALOGO_HELPERS.md` por uma sprint inteira, indescobríveis pela rota que o
próprio README recomenda.

## A `description`, que é o que decide o roteamento

O Genie Code lê **apenas** a `description` para escolher qual skill carregar.
Esta declara o vocabulário do domínio — criar, adicionar, padronizar, converter,
helper, utilitário, prompt, documento, skill — e fecha com o que **não** cobre:

> Não cobre escrever a lógica de análise em si, nem alterar objeto já existente
> sem que a conversão para o padrão seja o pedido.

Esse último período é o que evita colisão. Sem ele, "criar um snippet que calcula
PSI" carregaria esta skill em vez da `hub-ml-validacao-estatistica`, e o usuário
receberia formato quando queria estatística.

**A hipótese não está testada.** É o que o forward test existe para medir, e ele
depende de interação humana no Genie Code.

## O que mudou fora da skill

Onze arquivos afirmavam "12 skills". O próprio template de README avisa contra
isso — *"as 12 skills vira mentira na décima terceira; prefira 'as skills de
`skills/`'"* — e a décima terceira chegou.

| Arquivo | Mudança |
|---|---|
| `tools/publicar_free.py` | `EXPECTED_SKILLS` 12 → 13 |
| `.assistant/README.md` | inventário de invocação, saída de exemplo (13/13), e o glossário |
| `.assistant/skills/README.md` | linha nova no inventário |
| `hub_padroes/snippet/template.md` | "as 12 `SKILL.md`" → "as `SKILL.md` de `skills/`" |
| `README.md` da raiz | o quadro de forward tests declara 36/36 nas 12 **originais**, com a décima terceira pendente |
| `.claude/` (4 arquivos) | contagens trocadas por formulação que não envelhece |

Onde dava, troquei o número por uma formulação que não envelhece. Onde o número
é o ponto — `EXPECTED_SKILLS`, a saída de exemplo — ele foi atualizado.

## O que fica pendente, e é seu

**O forward test da skill nova.** Três casos, em chat novo cada um:

| Caso | O que medir |
|---|---|
| Positivo | "quero criar um snippet novo para calcular taxa de resposta" → carrega `hub-ml-criar-objeto`? |
| Negativo | "como calculo PSI entre duas safras?" → carrega `hub-ml-validacao-estatistica` ou similar, **não** esta |
| `@menção` | `@hub-ml-criar-objeto` → carrega deterministicamente |

**O roteiro não cobria a skill nova** — os 36 casos eram das doze originais, e
os três de `13P`/`13N`/`13M` foram acrescentados agora a
`docs/testes/forward/roteiro.md`. Sem isso não haveria o que executar.

O caso negativo é o que importa mais. Uma skill de "criar objeto" tem vocabulário
que roça o de todas as outras, e o risco real é ela roubar a vez — o pedido de
análise virando conversa sobre formato de pasta.

Se ela roubar, o conserto é na `description`, e isso invalida a certificação de
roteamento das vizinhas que competem no mesmo vocabulário. O roteiro está em
`docs/testes/forward/`.

## O que fica para depois

| Item | Por quê |
|---|---|
| Forward test das 3 interações | depende de você, no Genie Code |
| Dívida de saída colada: 12 notebooks | §12.1 do plano |
| Duplicação de cor em 12 módulos | §12.2 do plano |
| Guarda que confere saída colada no README contra execução | proposta pela auditoria da Sprint 10; é desenho, entra na 12 |

---

## Auditoria da Sprint 11 — 19 achados, e uma previsão registrada

O auditor fez o que nenhum anterior tinha feito: **usou a skill** para criar um
objeto, do começo ao fim, e relatou onde travou. Foi de lá que saiu o achado
bloqueante.

### A previsão de roteamento, registrada antes do teste

Pedi que ele previsse o resultado dos três forward tests lendo apenas as treze
`description`, antes de abrir o corpo da skill. Fica aqui para ser confrontada
com o teste real:

| Caso | Previsão | Confiança |
|---|---|---|
| `13P` | `hub-ml-criar-objeto` | alta — quatro tokens que só existem nessa description |
| `13N` | `hub-ml-monitoramento-modelo`, **não** a skill nova | média-alta |
| `13M` | `hub-ml-criar-objeto` | determinístico, a menção força |

**Ele concorda que o `13N` não colide com a skill nova**, e a razão é forte: zero
sobreposição léxica — a description dela não contém PSI, drift, safra nem
qualquer verbo do pedido.

**Mas discordou do ideal declarado**, e tinha razão. Eu havia escrito
`hub-ml-validacao-estatistica`; a description dela não contém "PSI" nem "safra",
enquanto `hub-ml-monitoramento-modelo` contém **PSI/CSI/KS** e **alerta**
literalmente, e o caso `04N` do mesmo roteiro, com enunciado quase idêntico, já
declara esse ideal.

E ele apontou a colisão real, que é entre duas outras skills:
`monitoramento-modelo` × `analise-safra`. Esta última dispara em "mencionar
safra" — **o único gatilho incondicional das treze** — e a palavra está no
pedido. Essa colisão é anterior a esta sprint; o `13N` a expõe, não a cria.

### O achado bloqueante: a skill nunca menciona o marcador

O auditor seguiu o `SKILL.md` ao pé da letra para criar um snippet. As cinco
etapas do notebook, escritas exatamente como descritas, produziram duas falhas
que se contradizem sobre o mesmo arquivo — "módulo extra na pasta do objeto" e
"falta o notebook" —, por uma causa que a skill **nunca citava**: a primeira
linha precisa ser o marcador `# Databricks notebook source`.

Ele só saiu lendo `tools/notebook_marker.py` — e a skill contempla
explicitamente quem **não** tem o repositório.

É a exigência mais fácil de esquecer e a mais cara: sem ela a publicação envia o
arquivo no formato errado e quebra o import no workspace.

### O erro que a skill chamava de fatal era o que passava

A skill afirmava: *"O nome da pasta e o do módulo são iguais. O validador reprova
qualquer outra combinação."*

Ele não reprovava. `check_pastas_de_objeto` só enxerga a pasta **quando o módulo
tem o nome dela** — `if not modulo.exists(): continue`. Uma pasta
`taxa_nulos/calcula.py` com `__init__.py` era simplesmente pulada, e não entrava
nem na contagem.

Nova guarda `check_pasta_de_objeto_malformada`, com a regra invertida: toda pasta
sob `hub_snippets/<secao>/` ou `hub_scripts/` que tenha `__init__.py`
**precisa** ter `<nome>.py`. Provada com o caso que o auditor construiu — a pasta
`taxa_nulos` com `calcula.py` dentro passou a reprovar, com a mensagem dizendo o
que encontrou e por que importa.

E a skill passou a ter uma tabela dizendo, linha a linha, **o que a ferramenta
confere e o que é você** — porque ela também afirmava que "os quatro primeiros o
validador confere", quando o primeiro é "o tipo foi confirmado com quem pediu",
que nenhuma ferramenta verifica.

### A skill criada para fazer cumprir os moldes era a que menos cumpria

Faltavam **três das cinco seções** que `hub_padroes/skill/template.md` declara
obrigatórias: "quando esta skill se aplica", "usar helpers da biblioteca" e
"formato de saída". As doze anteriores têm todas.

A de helpers é a que o template chama de "não opcional e não decorativa",
ancorada no ADR-0004 — o Genie Code não descobre `hub_snippets` sozinho.

E ela fazia o inverso do que o template prevê: **duplicava o checklist**, inline
no corpo e expandido em `templates/`. As duas listas já discordavam no mesmo
commit.

### Três checklists, três conteúdos

O auditor encontrou três listas convivendo — em `snippet/template.md`, no corpo
da skill e em `templates/` — divergindo nos dois sentidos: uma pedia smoke test e
não pedia catálogo, outra o inverso, e nenhuma das duas novas cobria script ou
skill, apesar de o checklist se intitular "objeto novo do Hub".

O `checklist-objeto-novo.md` virou o **canônico**, com bloco por tipo, e os
quatro templates passaram a apontar para ele.

E ele testou a promessa de que "cada linha é verificável": cerca de oito de trinta
não eram — "docstring diz por que existe", "decisão não óbvia", "problema real".
A lista foi dividida em **verificável por terceiro** e **juízo de quem escreveu**,
porque um checklist que promete verificação e entrega opinião ensina a marcar
tudo.

### Os demais

| # | Achado | Correção |
|---|---|---|
| 4 | a árvore de pastas mostrava `hub_snippets/<secao>/` rotulada "para snippet e script"; script não tem seção | duas árvores |
| 5 | `skills/README.md` dizia "Doze skills" acima de uma tabela com treze — publicado no Free | sem número |
| 6 | `hub_padroes/README.md` anunciava a skill como "planejado, ainda não existe" | aponta para a skill |
| 8 | o formulário de resultados dos forward tests não tinha a Skill 13 | três linhas e a síntese em 39 |
| 9 | o roteiro dizia 36 e 39 no mesmo arquivo, e a **meta do gate** estava em 36/36 | 39 testes, meta 39/39, com o bloco histórico intacto |
| 13 | "o exemplo em `hub_padroes/<tipo>/<exemplo>/`" não existe para README nem notebook | remete à tabela do README de `hub_padroes` |
| 14 | "um caso de CRM real" contra a regra de fixture sintética | "sintético, do domínio da equipe" |
| 15 | "script recebe nome de tabela" não classifica `doc_coverage`, que recebe caminho | "o endereço do que vai diagnosticar" |
| 16 | o exemplar que a skill manda ler violava a regra da saída colada | as duas saídas coladas, `warn` e `fail`. **A dívida de §12.1 caiu de 12 para 11** |
| 17 | "o README da seção" não existe — não há `spark/README.md` | "a tabela de módulos em `hub_snippets/README.md`" |
| 18 | `ambiente_fonte/README.md` ainda dizia "12 Agent Skills" | sem número |
| 19 | `hub_padroes/` tem sete pastas; a skill fala em seis "fechados" | uma linha explicando que `auditoria/` é molde de processo |

### O que a auditoria confirmou

Todas as demais afirmações do corpo conferem, e ele mediu cada uma: os 22 nomes
de `constants/colors`, a coexistência de `drift_detection` e `drift_detector`, o
comando de `api_publica.py` produzindo diff vazio contra o `__init__.py`
commitado, os três pins, e — com um script sobre os 64 commits — que "dois
objetos ficaram fora do catálogo por uma sprint inteira" é **verdadeiro e
preciso**: `constants/emojis` e `constants/styles`, ausentes em três commits,
corrigidos no quarto.

Nenhum registro datado foi promovido a 13. Os 38 caminhos de helper citados nas
treze skills resolvem, zero quebrados.

### O que nenhum portão vê, numa skill

O auditor nomeou cinco classes, e a que ele priorizaria é a que produziu o achado
das seções faltantes: **conformidade do corpo ao `skill/template.md`**. Doze de
treze têm a seção de helpers; a décima terceira não tinha, e os dois portões
aprovaram.

Fica registrada como candidata da Sprint 12, junto com a que a auditoria anterior
propôs. As duas são baratas e pegam defeitos que já aconteceram.

### Onde ele travou ao usar a skill

Cinco pontos, um bloqueante (o marcador). Os outros quatro viraram correção:

- **em qual seção o objeto entra** — a skill não dizia que existem seis, nem que
  criar seção nova exige decisão; agora diz, e avisa que o `__init__.py` de seção
  não reexporta;
- **a demanda já estava coberta** — ele descobriu `spark/null_summary` seguindo a
  instrução, e a skill não tinha procedimento para isso; agora tem, com a busca
  no catálogo e a decisão trazida para quem pediu;
- **os dois contratos que a validação cruza** não eram citados; agora são;
- **o fechamento ambíguo**, resolvido pelo checklist canônico.

O que funcionou sem atrito, no relato dele: a escolha do tipo, a nomenclatura, a
geração do `__init__.py` e **a ordem das cinco etapas do notebook** — que
"produziu um notebook melhor do que eu escreveria sem ela".
