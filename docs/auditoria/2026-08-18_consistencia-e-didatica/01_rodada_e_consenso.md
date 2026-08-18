# Auditoria — consistência residual e padrão didático (2026-08-18)

- **Nível:** `A1` — uma rodada, modelo do autor, sessão sem contexto, com acesso
  ao sistema de arquivos e à CLI do Databricks autenticada.
- **Escopo:** o conjunto, não uma sprint. A documentação inteira contra a régua de
  `.claude/rules/docs-e-readmes.md`, consistência residual entre artefatos, e o
  que mais aparecesse.
- **Base:** commit `2b56958`, 888 arquivos versionados.
- **Resultado:** 18 achados, todos procedentes. Todos corrigidos nesta sessão.

É a décima quarta rodada do projeto e a primeira a auditar a documentação como
**produto**, na ordem em que uma pessoa a lê, e não como lista de arquivos.

## Os dois achados vermelhos

### Um identificador corporativo publicado, invisível para a guarda que existe para isso

`rubrica_universal.md`, linha 89, dentro de `templates/` de uma skill: a sigla de
um órgão de governança interno da instituição, numa linha de rubrica de nota.
Estava no workspace Free e entraria no workspace do trabalho pelo runbook.

É a inversão exata do vetor que o `ADR-0003` previu. A quarentena de 15/08 isolou
a **pasta** `Ambiente_Antigo/`; não isolou o **vocabulário** que já tinha
atravessado para `ambiente_fonte/` antes de ela existir. *"Foi quarentenado"
também tem data de validade.*

O `CORPORATE_RE` não o alcançava por construção: ele cobre formatos reconhecíveis
— matrícula, domínio, e-mail —, e sigla interna não tem formato. Só lista pega. A
regex ganhou uma classe nova, com duas particularidades que valem registro:

| Decisão | Por quê |
|---|---|
| a sigla é escrita com uma letra entre colchetes | o arquivo do validador **também** é varrido pelo check; sem isso, a constante reprovaria a si mesma |
| a fronteira é escrita à mão, e não com a de expressão regular | `_` conta como caractere de palavra, e o token aparece colado em nome de arquivo (`conformidade_<sigla>.md`) |

Provada com sete casos, entre eles os três nomes reais em que o token aparece na
pasta em quarentena. E a guarda **reprovou de imediato** na camada derivada,
antes do re-render — que é a demonstração de que ela pega o caso real, e não só o
construído.

Uma varredura exaustiva cruzando todo o vocabulário em siglas da pasta em
quarentena contra o produto não encontrou nenhuma outra: 101 siglas em comum,
todas palavras portuguesas, termos técnicos ou vocabulário de cor.

### O CHANGELOG registrava uma correção que nunca foi escrita em disco

A entrada de 17/08 afirmava que `ADR-0004` e `ADR-0005` tinham ganhado aviso de
superseding. A segunda metade da frase aconteceu; a primeira, não.

A causa é conhecida e vale mais que o defeito: o script que aplicou aquelas
correções procurava a âncora `- **Status:` — o formato dos ADRs **novos**. Os
ADRs 0004 e 0005 usam `Status:` sem marcação. A âncora não casou, nada foi
inserido, e a função **imprimiu sucesso mesmo assim**, porque a mensagem estava
fora do `if`.

Custo real, e é por isso que este é o segundo vermelho: o changelog é o
instrumento que toda IA lê para saber o que já foi feito, e a regra multi-IA o
torna obrigatório justamente por isso. Uma entrada falsa é pior que entrada
ausente — a próxima sessão pula a correção por considerá-la feita. E o efeito já
estava de pé: quem abrisse o `ADR-0004`, roteado pelo `CLAUDE.md`, leria como
vigente um documento que fala de `x_snippets/` e de um catálogo em
`x_docs/catalogo_helpers.md`, caminho que não existe há dez sprints.

Os dois banners foram escritos, e o script de correção desta rodada foi feito
para **abortar** quando uma âncora não casa, em vez de reportar sucesso.

## A norma que ninguém media

`hub_padroes/snippet/template.md` não descreve: manda. *"Docstring, comentário e
notebook são prosa e vão em português"*, *"não traduza identificador"*.

Medição: **15 dos 58 módulos (26%)** tinham docstring de módulo em inglês, e a
divisão era limpa por pasta — **7 de 7** em `hub_scripts/`. A biblioteca ensinava
duas convenções ao mesmo tempo, e o molde publicado perdia autoridade sobre a
etapa que o criou.

As 15 foram traduzidas, identificadores intactos, e a norma virou o vigésimo
check. Duas notas sobre a detecção:

- **"Tem acento" não basta.** Cinco docstrings legítimas em português não têm
  nenhum — *"Wrapper Prophet com MLflow e feriados BR."* O sinal usado é a razão
  entre palavras funcionais das duas línguas, e ele separa as duas populações sem
  falso positivo.
- **A guarda nasceu como falha, não como aviso.** O padrão do repositório é
  avisar enquanto a dívida existe; aqui a dívida fechou na mesma sessão, e aviso
  sobre norma já cumprida é convite à regressão.

Provada nos dois sentidos: acusa as 15 antes da tradução, zera depois, e reprova
quando uma delas é revertida.

## A porta de degradação que sobrou

`--conferir-readme` foi corrigido em 17/08 para reprovar quando um rótulo some da
saída. Ficou aberta a outra porta: quando o comando **não lança**, o `except`
devolvia zero e a guarda aprovava em silêncio.

O auditor construiu o caso apontando o interpretador para um caminho inexistente:
0 linhas conferidas, 0 problemas, `APROVADO`. Timeout entra pela mesma porta, e o
`--verify` gasta cerca de 100 s de rede.

Corrigido para reprovar nomeando o comando e a causa provável, e provado com o
mesmo caso. É a terceira vez que este repositório corrige degradação silenciosa —
e as três foram no mesmo padrão: varredura vazia que passa.

## Os demais

| # | Achado | Correção |
|---|---|---|
| A3 | o `CLAUDE.md` canônico atribuía ao `ADR-0006` uma supersessão que é do `ADR-0005`, com a razão do 0005 colada no bullet do 0006 | dois bullets separados; o 0006 passa a declarar que não supersede nada |
| A4 | `forward/README.md` anunciava **GATE FECHADO 36/36** enquanto o `roteiro.md`, na mesma pasta, fala em 39 testes | "gate das 12 originais", com os 3 casos que faltam nomeados |
| A6 | a tabela do `PLANO_HUB.md` §1 dizia que o nome das skills era `hub-ml-` **antes** da renomeação — uma busca-e-substituição varreu a coluna histórica | `rodrigo-<tema>`, como o `ADR-0006` registra |
| A7 | dois `Status:` adjacentes no topo do plano, o primeiro vencido | o vencido saiu |
| A8 | `ciclo-de-vida.md` mandava a um runbook "a criar" que existe, e ignorava o runbook irmão na mesma pasta | aponta para os dois |
| A9 | três documentos descreviam o mesmo ciclo em ordens diferentes, e o playbook citava como resumo de si um diagrama que o contradizia | ordem única — registrar **depois** de conferir, porque o `--verify` produz o número que a entrada cita |
| A11 | o comentário do `PERSONAL_RE` dizia "jamais em conteúdo versionado"; os dois checks que o usam recebem `ambiente_fonte/`, não o repositório — 439 caminhos nunca vistos | comentário reescrito com o alcance real e a razão |
| A12 | o inventário que justifica gerar os `__all__` por AST estava errado em três números: seis imports cruzados (são 7), nove nomes (são 10), 37 de 51 (são 39) | a sétima linha entrou; os deriváveis viraram comando |
| A13 | `hub_padroes/README.md` era o único README do produto sem o aviso de não-descoberta — e é o que o guia principal indica como porta de entrada dos moldes | banner igual ao dos irmãos |
| A14 | o glossário publicado remetia oito verbetes a `docs/`, que não é publicado; e uma linha mandava ao `ADR-0004` supersedido | aviso sob o título do glossário; a remissão passou ao `ADR-0007` |
| A15.1 | o glossário publicado citava "36 testes" — o quarto documento a fazê-lo, e o único que viaja para o workspace | 39, dos quais 36 concluídos |
| A15.2 | `hub_snippets/tests/` é publicado e nenhum documento publicado o menciona | linha na tabela de pacotes, declarando que não é pasta de objeto |
| A15.3 | `docs/auditoria/README.md` dizia "as três rodadas" sobre uma tabela de quatro, e o índice cobria 4 auditorias enquanto 13 viviam em `docs/sprints/` | quatro, e um parágrafo que manda ao outro lugar |
| A15.4 | o roteiro de forward tests traz 44 vezes o caminho com o username do laboratório | aviso de substituição no topo (ver decisão abaixo) |
| A15.5 | o docstring da guarda de helpers citava "38 caminhos"; são 72 | "os caminhos existentes à época" |
| A15.6 | `tools/` e `docs/testes/` sem README, contra a regra de documentação | os dois escritos |

### Duas decisões tomadas contra a recomendação literal do auditor

**O roteiro não foi parametrizado.** O auditor propôs trocar as 44 ocorrências
por `<username>`. Os prompts do roteiro existem para ser colados sem edição, e
quem os cola hoje é quem os escreveu: parametrizar cobra 44 substituições por
rodada para proteger um reuso futuro. Ficou o aviso no topo, que resolve o caso
da squad sem onerar o caso de hoje. É decisão registrada, não omissão.

**Três dos cinco READMEs ausentes não foram escritos.** `docs/`,
`docs/playbooks/` e `docs/sprints/` continuam sem README, e o próprio auditor
classificou os três como burocracia: o `README.md` da raiz já mapeia as três, e
os arquivos de dentro se explicam. Escritos foram os dois que custam — `tools/`,
porque é a única pasta descrita como editável sem dizer o que cada script faz nem
que ela não é publicada; e `docs/testes/`, porque o README da raiz entrega o link
cru a quem vai assumir o projeto.

## A classe de defeito que as treze rodadas anteriores não viram

> **Norma publicada sem instrumento — e auditada como prosa, nunca como
> especificação.**

As treze rodadas leram os documentos perguntando *"isto é verdade?"*. A décima
terceira acrescentou *"isto concorda com aquilo?"*. Nenhuma perguntou a terceira:
*"isto é uma norma, e o repositório a cumpre?"*

O repositório publica normas vinculantes dentro de artefatos que viajam com o
produto. São especificações executáveis escritas em Markdown, com autoridade
declarada e zero cobertura: as 19 checks testavam fatos estruturais — caminhos
existem, links resolvem, contagens batem, contratos casam —, e nenhuma testava
uma frase normativa de `hub_padroes/`.

O resultado foi medível: 26% da biblioteca violando o molde que a própria
biblioteca publica, concentrado 100% numa pasta, com treze auditorias passando
por cima. Não por descuido — porque o molde foi lido como documento a verificar,
nunca como régua contra a qual medir o produto. A mesma cegueira explica o A13: o
produto estabelece que todo `hub_` avisa não ser auto-descoberto, e ninguém testou
a norma contra os cinco READMEs.

**A diferença em relação à classe da rodada anterior** — contradição entre dois
artefatos — é a hierarquia. Lá os dois lados são simétricos, e qualquer um pode
ceder. Aqui o molde está certo por construção, e o que sobra é dívida de
conformidade: mensurável, e portanto automatizável de um jeito que a outra classe
nunca será. O método que faltou tem nome: extrair de cada documento normativo do
produto a lista de asserções verificáveis, e rodar cada uma contra a biblioteca.

O check de idioma é o primeiro exercício dele. As outras normas de
`hub_padroes/` são a fila.

## Verificação final

```text
validate_assistant.py              APROVADO: 0 falha(s), 11 aviso(s)
                                   idioma da docstring: 60 módulos, 0 em inglês
validate_assistant.py --conferir   APROVADO — 13 linhas conferidas
publicar_free.py --verify          APROVADO: 0 problema(s) — obsoletos: 0
render + git status                limpo
```

## Ações pendentes

| Ação | Dono | Critério de verificação |
|---|---|---|
| 3 forward tests da `hub-ml-criar-objeto` | Rodrigo | `39/39` no `forward/README.md` |
| 16 partes 3 dos notebooks de prompt | Rodrigo | bloco canônico substituído por resposta real |
| instrumentar as demais normas de `hub_padroes/` | próxima sessão | um check por asserção, com o caso que ele pega |
| 11 notebooks sem saída colada | passe próprio | `saída colada: 77 com bloco real, 0 sem` |
