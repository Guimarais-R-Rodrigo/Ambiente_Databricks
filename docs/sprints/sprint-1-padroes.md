# Sprint 1 — Padrões e exemplos

Data: 2026-08-16 · Executor: Claude · Escopo: `.assistant/hub_padroes/`.
**Nenhum objeto existente do produto foi tocado.**

## O que a sprint entregou

Sete subpastas em `.assistant/hub_padroes/`, com os templates dos seis tipos de
objeto do Hub, um exemplo preenchido e executável de cada um, e o molde do prompt
de auditoria de sprint.

```text
hub_padroes/
├── README.md
├── readme/     template.md · exemplo.md
├── snippet/    template.md · exemplo/ (3 arquivos)
├── script/     template.md · exemplo/ (3 arquivos)
├── prompt/     template.md · exemplo/ (2 arquivos)
├── skill/      template.md · exemplo/SKILL.md
├── notebook/   template.py
└── auditoria/  template.md
```

Publicado no workspace, conforme a decisão §2.1 do plano: na raiz do repositório
os templates ficariam invisíveis para a equipe e para a skill que vai aplicá-los.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 0 aviso(s)
render_simulado.py      OK: 199 arquivos
publicar_free.py        APROVADO: 0 problema(s)

exemplo_taxa_resposta_campanha   SUCCESS
exemplo_checar_base_campanha     SUCCESS
exemplo_analisar_campanha        SUCCESS
```

Os três notebooks foram executados como job serverless no laboratório, não
apenas validados sintaticamente.

## O que ficou decidido, e por quê

### O template de notebook ganhou o que faltava

A v1 do plano descrevia quatro movimentos. Escrever o exemplo mostrou que faltava
o que faz o arquivo funcionar, e isso entrou no template:

- **preâmbulo de `sys.path`** — três linhas sem as quais nenhum dos 74 notebooks
  importa a biblioteca;
- **formato-fonte** — marcador, separador, `# MAGIC %md` e, principalmente, que
  `%pip install` escrito do jeito natural faz `ast.parse` estourar e reprova o
  repositório inteiro;
- **bloco canônico de não executado**, com exemplo preenchido, para que os 14
  módulos da Sprint 8 não saiam com 14 convenções;
- **variante para objeto sem dados e sem número**, para os 13 objetos de
  `constants`, `visual` e `display`, onde os movimentos 3 e 4 não existem como
  descritos e o contrato de fixture não se aplica.

### O template de README tem três escalas

Nove seções servem a uma pasta de seção e não servem aos extremos. Curta (5
seções) para pasta de até 5 objetos; padrão (9) para seção; longa (9 + extras
posicionadas) para os dois READMEs de topo, que hoje têm 15 seções e 374 linhas.

A seção "aviso de natureza" passou a ser obrigatória **só onde há ambiguidade
real** — `skills/` e os dois topos. Depois da reestruturação quase tudo é do Hub,
e repetir o aviso em vinte pastas é ruído.

### O exemplo cobre quatro situações que o tema principal não cobre

`taxa_resposta_campanha` exporta função **e** constante, exercitando o caso de
`__all__` com mais de um nome — que vale para 39 dos 51 módulos. O bloco de não
executado está demonstrado dentro do próprio notebook. A variante sem dados está
descrita no template. E a resposta real do Genie Code foi capturada e comentada.

### Não há README em cada subpasta

Decisão contra a letra do plano, com motivo: cada `template.md` já abre dizendo
quando se aplica, e um README ao lado repetiria isso — que é exatamente a
duplicação que a regra do template de README proíbe. A navegação fica no índice
`hub_padroes/README.md`, que é dono da tabela "qual template para qual objeto".

**Este é o ponto mais frágil da sprint e deve ser desafiado na auditoria.**

## A premissa do exemplo estava errada, e foi corrigida

O plano afirmava que o intervalo de confiança "desarma" a comparação entre
segmentos de tamanhos muito diferentes. Rodado sobre a base real, **não desarma**:
o segmento de 28 contatos tem IC de Wilson `[26,5% ; 60,9%]`, que não se sobrepõe
a nenhum outro. A diferença é estatisticamente real.

A lição correta é melhor: **significância não é relevância**. O efeito existe, é
mensurável, e é irrelevante — há 28 clientes, e mesmo a 61% de resposta são 17
respostas numa campanha de 15.000 contatos. O que o intervalo mostra é a
precisão, cuja largura vai de 0,4 pp no maior segmento a 34,4 pp no menor.

Um exemplo ensinando "o IC derruba a diferença" seria falso, e teria sido
publicado se ninguém rodasse.

## O que a interação com o Genie Code revelou

A resposta real está registrada em `prompt/exemplo/exemplo_analisar_campanha.py`.
Dois pontos que viraram conteúdo dos templates:

**Roteamento.** O assistente considerou carregar as skills de EDA e de validação
estatística, **decidiu não fazê-lo** — "o usuário quer uma análise direta, não
pediu EDA completo" — e carregou a skill nativa `data-sampling` da Databricks. A
decisão é defensável. É a razão de o template de prompt exigir que a skill
recomendada seja declarada no cabeçalho: depender do roteamento para pedido
ambíguo é apostar.

**Lacunas previsíveis.** Ele acertou o essencial: validou grão e domínio antes de
medir, marcou o segmento de 28 contatos como amostra mínima e o excluiu da
recomendação pelo argumento operacional correto. Deixou passar três coisas:
nunca quantificou a precisão; assumiu que recontatar as mesmas pessoas reproduz
a taxa; e errou dois números ("~955" onde são 947, "50% inferior" onde são
39,4%).

Isso virou a seção "o que conferir na resposta" do template de prompt — que
existe não por desconfiança, mas porque as lacunas de um assistente competente
são sistemáticas e portanto verificáveis.

## Itens de vigilância acrescentados

`data-sampling` é skill nativa da Databricks, já registrada na rodada 1 dos
forward tests, onde foi carregada **junto** com a nossa. Aqui foi carregada **no
lugar**. Não é falha de roteamento — o pedido não era de EDA completa —, mas
mostra que `eda-profissional` está calibrada para "EDA completa" e uma pergunta
analítica direta rota para outro lugar. Fica como terceiro item de vigilância,
sem alteração de `description` por um caso isolado.

## O que fica para a auditoria

Pontos onde uma sessão sem contexto deve olhar primeiro:

- a decisão de não ter README por subpasta;
- se o template de README aguenta mesmo os dois extremos, testado contra o
  `.assistant/README.md` real de 319 linhas;
- se o template de notebook cobre um objeto de `constants`, que é o caso mais
  distante do exemplo escolhido;
- se a `description` da skill de exemplo colidiria com alguma das 12 reais, caso
  alguém a publique por engano;
- se `hub_padroes` ser um pacote Python importável (tem `__init__.py`) cria algum
  efeito indesejado.
