# Sprint 12 — fechamento: os ADRs, os playbooks e as guardas

Data: 2026-08-17 · Executor: Claude · Escopo: os dois ADRs que o plano apontou
como necessários, os três playbooks de replicação, e as guardas que as auditorias
das Sprints 10 e 11 propuseram.

É a última sprint de execução do `PLANO_HUB.md`.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 11 aviso(s)
                        skills: 13 · 2/13 com as 5 seções do template
                        helpers citados: 72 caminhos, todos resolvem
--conferir-readme       APROVADO — 11 linhas conferidas contra execução real
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
