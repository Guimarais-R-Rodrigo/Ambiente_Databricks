# Sprint 12 — fechamento: os ADRs, os playbooks e as guardas

Data: 2026-08-17 · Executor: Claude · Escopo: os dois ADRs que o plano apontou
como necessários, os três playbooks de replicação, e as guardas que as auditorias
das Sprints 10 e 11 propuseram.

É a última sprint de execução do `PLANO_HUB.md`.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 11 aviso(s)
                        skills: 13 · 2/13 com as 5 seções do template
                        helpers citados: 72 caminhos verificados
--conferir-readme       APROVADO — 12 linhas conferidas contra execução real
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
```

## Dois ADRs que supersedem, sem apagar

O plano apontou que `ADR-0004` e `ADR-0005` ficaram para trás. Os dois são
imutáveis, e a regra do projeto é clara: mudança de ideia gera ADR novo que
supersede, preservando o raciocínio original.

**`ADR-0007` — o catálogo depois da pasta de objeto.** O ADR-0004 decidiu a
declaração explícita de helpers, e essa decisão **não muda**. O que envelheceu foi
o entorno: "54 helpers em `x_snippets`" hoje são 58 em `hub_snippets`, o catálogo
saiu de `x_docs/` para `.assistant/CATALOGO_HELPERS.md`, e helper deixou de ser
um módulo para ser uma pasta com três arquivos.

O ADR novo reafirma o que continua valendo e formaliza a coluna de dependência
com três estados — incluindo o `exec`, que nomeia a classe de defeito descoberta
nas Sprints 7 e 9: dependência exigida **na chamada**, que nenhuma análise de
import encontra.

**`ADR-0008` — o critério de conferência sai do ADR e vai para o código.** O
ADR-0005 fechava declarando que a conferência valida "12 skills, 6 diretórios de
extensão". São 13 e 4.

A decisão do ADR novo não é corrigir os números: é **tirá-los do texto**. Contagem
em ADR envelhece sem que nada acuse; contagem em constante de código reprova a
execução quando diverge. Foi o que aconteceu na Sprint 11 — subir
`EXPECTED_SKILLS` para 13 fez parte da mudança, não de uma correção posterior.

## Os três playbooks: número morto vira comando

`checklist-replicacao.md`, `replicacao-trabalho.md` e
`GUIA_REPLICACAO_TEMPORARIO.md` fixavam "174 arquivos", "12 skills", "6
diretórios" e "12 pastas `hub-ml-*`". Nenhum sobreviveu — o total publicado saiu
de 175 para 315.

Dois deles já carregavam banner de obsolescência apontando para esta sprint, o
que foi a coisa certa a fazer na época. O conserto não foi atualizar os números:
foi **substituí-los pela linha que os produz**.

O checklist agora tem um quadro em branco para quem replicar preencher com a
saída do `--verify` — commit, arquivos, skills, extensões. O registro passa a ser
do que foi de fato copiado, não do que estava certo quando o documento foi
escrito.

## As três guardas, cada uma contra um defeito que aconteceu

**`check_saida_de_comando_no_readme`**, proposta pela auditoria da Sprint 10.
Reexecuta os comandos que o README documenta e compara com a saída colada.
Provada com o defeito exato que a originou:

```text
FAIL README.md: a saída colada diverge da execução
    colado : python (AST)       : 208 arquivos
    real   : python (AST)       : 209 arquivos
```

Fica atrás da flag `--conferir-readme`, fora do caminho padrão, porque chama os
próprios scripts — recursão em validação é armadilha.

E ela **já pegou quatro divergências reais** na primeira execução, criadas pelas
edições desta própria sprint. A ironia registrada pela auditoria — *"o validador
imprimia a resposta certa na tela enquanto o README exibia a errada"* — deixou de
ser possível.

**`check_skill_helpers_resolvem`**, proposta pela auditoria da Sprint 11. Todo
caminho `hub_snippets.x.y` citado numa skill precisa existir. São **72 caminhos**
nas 13 skills, e todos resolvem hoje — mas renomear um objeto os quebraria em
silêncio, porque quem resolve o caminho é a pessoa, no notebook, e o erro aparece
longe da causa.

**A primeira versão desta guarda não funcionava**, e a auditoria final mediu o
tamanho do buraco: 59 dos 72 caminhos desprotegidos. Ver a seção de auditoria no
fim deste relatório.

**`check_skill_secoes`**, da mesma auditoria, e a que exigiu mais calibragem. A
primeira versão acusava treze skills por execução: as 12 originais são anteriores
ao template, e o casamento por palavra-chave produz falso positivo sobre título
legítimo — `hub-ml-auditoria-skills` chama a seção de recursos de "Usar recursos"
e quase não usa a biblioteca, o que é correto para uma skill que audita skills.

A versão final cobra **só a seção de helpers**, que é a que o template chama de
não opcional e cuja consequência é concreta, e reporta as outras quatro como
contagem informativa: **2 de 13** com as cinco seções. É dívida declarada, não
ruído.

## O que este projeto aprendeu, e que vale mais que o código

Doze sprints, doze auditorias, cerca de 150 achados — todos procedentes. Três
padrões se repetiram o suficiente para virar regra:

**Prosa confiante sobre coisa não verificada é a classe de defeito mais
frequente.** Não número inventado — afirmação plausível escrita de memória. A
comparação do autoencoder com o Isolation Forest estava invertida; a skill
afirmava que o validador reprovava um caso que ele pulava; o README prometia uma
guarda que não existia. Nenhuma passa em portão de sintaxe.

**"Foi testado" tem data de validade em ambiente gerenciado.** Em três dias, três
registros de teste venceram — o MLflow deixou de abrir run, o Prophet passou a
funcionar, e o pin defensivo de numpy virou conflito. Reexecute antes de
replicar.

**Cada portão pega uma classe, e nenhum pega a do vizinho.** A validação olha o
disco, o `--verify` olha o workspace, a execução olha o comportamento. Na Sprint 5
os três pegaram defeitos diferentes no mesmo commit.

## O que fica em aberto, declarado

| Item | Onde | Depende de |
|---|---|---|
| 3 forward tests da skill nova | `docs/testes/forward/roteiro.md`, Skill 13 | você |
| 16 partes 3 dos prompts | cada `hub_prompts/<nome>/exemplo_*.py` | você |
| 11 notebooks sem saída colada | `PLANO_HUB.md` §12.1 | passe próprio |
| Cor redeclarada em 12 módulos | `PLANO_HUB.md` §12.2 | decisão de produto (só 1 dos 12) |
| 11 das 13 skills sem as 5 seções | contagem no validador | decisão de produto |

Nenhum é bloqueio para apresentar o Hub à squad. Os dois primeiros são medição
que só você pode fazer; os três últimos são dívida com nome, lugar e custo
conhecido — que é a diferença entre dívida e defeito.

---

## Auditoria final — 18 achados, e a classe que doze rodadas não viram

A décima terceira rodada auditou a Sprint 12 **e o conjunto**. Dezoito achados,
todos procedentes.

### O pior: a guarda escrita nesta sprint não pegava o defeito que a originou

`check_skill_helpers_resolvem` aceitava o caminho quando a **pasta-pai** existia.
Para `hub_snippets.<secao>.<objeto>`, a pasta-pai é a seção — e seção sempre
existe. O objeto podia ser renomeado ou apagado que ela aprovava.

Raio de ação medido pelo auditor: **59 dos 72 caminhos (82%) desprotegidos**. Os
13 cobertos eram os `hub_scripts.<nome>` de um nível.

E o docstring dizia, literalmente, que ela existia "para que a próxima auditoria
não precise" conferir os 72 à mão — a única verificação que funcionava.

Reescrita com a regra certa: o destino tem de ser **pasta de objeto** (`is_dir()`
não basta — precisa ter `__init__.py`), e quando o caminho termina na função, o
último componente tem de estar na API pública que o `__init__.py` de lá exporta.
Provada contra os quatro casos que o auditor construiu:

| Caso | Antes | Depois |
|---|---|---|
| objeto removido dentro de seção válida | passou | **pega** |
| caminho até função inexistente | passou | **pega** |
| seção inexistente | pega | pega |
| script de um nível removido | pega | pega |
| `hub_snippets.spark.pit_join.pit_join` (legítimo) | passa | passa |

### O bloqueio de prontidão: duas frases retratadas no catálogo

`CATALOGO_HELPERS.md` — o documento para onde o README manda quem pergunta
"existe função pronta para isto?" — publicava duas afirmações de 14/08 que a
execução de 17/08 desmentiu, e cuja retratação estava escrita em **três outros
documentos**:

- que `prophet_wrapper` falha por não inicializar o backend;
- que instalar sem fixar versão derruba o kernel.

O analista que lesse o catálogo reimplementaria Prophet do zero — o custo exato
que a biblioteca existe para evitar, e o argumento de abertura do ADR-0004 — e
fixaria as doze versões, que é o que a regra 3 do inventário diz que gera
conflito.

Corrigido, e o parágrafo passou a **remeter ao inventário em vez de repetir o
conteúdo dele**, com a razão declarada: "foi testado" tem data de validade.

### O guia temporário descrevia o repositório de 35 commits atrás

`GUIA_REPLICACAO_TEMPORARIO.md` constava como reescrito nesta sprint; o corpo era
o repositório de `ac9a782`, com um find-replace parcial de `x_` → `hub_`.
Sobreviveram as três pastas que a Sprint 2 **apagou** em vez de renomear.

Quem o seguisse procuraria `x_config/`, `x_docs/` e `x_projects/`, deixaria
`hub_padroes/` para trás, contaria doze skills, abriria um caminho inexistente e
subestimaria o volume em 45%.

A causa é estrutural e vale registrar: o arquivo é **git-ignored**. Sem histórico,
sem guarda, sem revisor — nenhum dos portões o alcança, porque eles varrem o que
está versionado. Foi aposentado com um aviso no lugar do conteúdo; apagá-lo é
decisão do Rodrigo, já que não há como recuperá-lo do git.

### `--conferir-readme` degradava em silêncio

Quando um rótulo não aparecia na saída real, o laço seguia. Dois gatilhos: o
comando renomeou a linha, ou a CLI do Databricks não está autenticada.

O auditor mediu: numa máquina sem CLI, três contagens erradas por 685, 684 e 86
foram **aprovadas em dois segundos**, com o contador caindo de 12 para 9 sem
alarme. É o mesmo modo de falha que o repositório já corrigiu duas vezes — e o
README se orgulha disso vinte linhas acima.

A guarda passou a reprovar quando documenta uma linha que o comando não produz,
nomeando o rótulo e a causa provável.

### Os demais

| # | Achado | Correção |
|---|---|---|
| 5 | `replicacao-trabalho` estimava 165 arquivos; são 314 | o número vem do `--verify` |
| 6 | ADR-0007 define o marcador como `opt` (o catálogo usa `imp`) e diz "dois casos" de `exec` (são dez) | errata append-only no próprio ADR |
| 7 | o sumário imprimia "todos resolvem" mesmo reprovando | "caminhos verificados" |
| 8 | ADR-0004 e 0005 sem aviso de superseding, e o `CLAUDE.md` canônico roteando só para eles | aviso no topo dos dois, e as "Decisões ativas" completadas |
| 9 | §12.1 dizia "São 11" e, três linhas depois, "doze capturas" | onze |
| 10 | três documentos citavam 36/36 sem a ressalva de que a 13ª skill nunca foi testada | ressalva nos três, com a instrução de incluí-la nos testes |
| 11 | "as quatro linhas do meio" sobre uma tabela de seis | seis, e a segunda frase ancorada |
| 12 | o produto publicado manda rodar `tools/`, que não é publicado | ressalva no checklist e no README do produto |
| 13 | §12.1 e §12.2 apareciam **antes** de §12, aninhadas sob §11 | movidas |
| 14 | ADR-0008 datava o ADR-0005 em 15/08; é 14/08 | errata |
| 15 | ADR-0007: "as 13 skills atravessaram cinco sprints sem uma edição" — o corpo das 12 mudou e a 13ª nasceu na 11 | errata, com o que a afirmação tem de verdadeiro preservado |
| 16 | checklist deixou "4 diretórios `hub_`" fixo | vem do `--verify` |
| 17 | um `x_` residual no README do produto, o único em todo o `.assistant/` | corrigido |

### O veredito de prontidão

O auditor escolheu um perfil concreto — analista de CRM, SQL fluente, Spark
superficial, sem CLI, sem acesso ao repositório — e respondeu três perguntas.

**O que ele faz sozinho no primeiro dia:** bastante. A avaliação do
`.assistant/README.md` foi a mais elogiosa de todas as treze rodadas — a tabela
de navegação, a separação NATIVO × `hub_`, e uma seção de problemas que antecipa
os cinco erros que ele de fato vai cometer.

**Onde trava:** nos notebooks de `spark/`, que é onde um analista SQL-first
começa e onde estão sete dos onze sem saída colada; e quando quiser contribuir,
porque o checklist manda rodar ferramentas que não existem no workspace dele.

**O que acreditaria e não é verdade:** as duas frases do catálogo, o "36/36" sem
ressalva, e que `constants.styles` controla o estilo — quando é espelho morto.

A frase que ele deixou para repetir à squad:

> "O ecossistema está pronto para uso e o `.assistant/README.md` é um bom
> primeiro dia; antes de distribuir, corrijam duas frases do
> `CATALOGO_HELPERS.md` que contradizem a evidência do próprio repositório, e não
> usem o guia de replicação temporário — ele descreve uma versão de três dias
> atrás."

**As duas condições foram atendidas nesta rodada.**

### A classe que doze auditorias não viram

O auditor encontrou uma, e ela é sobre método, não sobre defeito:

> **Contradição entre dois artefatos publicados, quando cada um passa sozinho.**

Todas as rodadas anteriores compararam **um documento contra a realidade** — os
links resolvem? o número bate com a contagem viva? Ninguém leu **dois documentos
publicados um contra o outro**. E é aí que este repositório sangra, porque tem
muitos documentos que descrevem a mesma coisa e uma disciplina explícita de nunca
editar registro datado.

Seis dos dezoito achados só aparecem por leitura pareada — as duas frases do
catálogo contra o inventário, o marcador do ADR-0007 contra o catálogo, os 165
contra os 174 contra os 314, o "São 11" contra o "doze capturas", e o 36/36 com
ressalva num documento e sem ela em três.

Cada uma dessas frases, sozinha, passa em qualquer critério das doze rodadas.
E **nenhum portão pode pegá-las por construção**: o validador confere links,
sintaxe, forma e contagens contra o disco — nunca duas afirmações entre si.

**A variante sutil da mesma classe:** a referência de volta. Doze auditorias
verificaram exaustivamente que os links resolvem. Ninguém verificou se o que o
link aponta **sabe que foi apontado**. Foi assim que os ADR-0004 e 0005 ficaram
sem aviso de superseding, e que o `CLAUDE.md` — a entrada canônica — continuou
roteando para eles. A validação de links dizia que estava tudo certo: os quatro
links resolvem perfeitamente, para documentos que dizem coisas falsas.

### O custo dos portões, medido

| Comando | Tempo |
|---|---|
| `validate_assistant.py` (19 checks) | 1,5 s |
| `render_simulado.py --write` | < 5 s |
| `publicar_free.py --verify` | 1m36s |
| `validate_assistant.py --conferir-readme` | 1m41s |

O auditor apontou uma duplicação real no último: ele reexecuta o
`validate_assistant.py` inteiro como subprocesso para reler a própria saída como
texto, quando os números já estão em variáveis no `main()` de onde é chamado.
Metade do custo é duplicação pura. A parte que se justifica é o `--verify`, que
precisa mesmo ir à rede.

Fica registrado como candidato de melhoria, não corrigido nesta rodada: mudar o
desenho da guarda no mesmo dia em que ela foi escrita e corrigida duas vezes é
como se introduz o terceiro defeito.
