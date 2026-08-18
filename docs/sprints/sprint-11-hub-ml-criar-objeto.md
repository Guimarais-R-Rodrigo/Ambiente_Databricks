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
