# Auditoria de leitura, contexto longo (2026-08-19)

- **Nível:** `A1`, **segunda origem** — primeira rodada deste projeto com um
  modelo de outra família. As catorze anteriores foram todas com o modelo do
  autor.
- **Método:** leitura, sem execução. O corpus versionado inteiro numa janela só
  — 402 arquivos, cerca de 478 mil tokens, empacotados por
  `tools/bundle_para_auditoria.py`.
- **Base:** commit `ab04f31`.
- **Resultado:** 3 achados reportados, **1 procedente**, 1 parcial, 1 improcedente.
  Mais **1 achado forte fora da lista de achados**, escondido na seção de
  conflitos — e é o que justifica a rodada inteira.

## Por que esta rodada existiu, e por que o método foi outro

O `PLANO_HUB.md` §10 declara desde o início um gate aberto: auditoria de segunda
origem **da biblioteca**. Esta rodada **não o fecha** — ela é de segunda origem,
mas de leitura: auditou consistência documental sem executar uma linha de código.
O gate continua aberto e exige execução. As catorze rodadas anteriores tiveram acesso a shell, CLI e execução, e
usaram bem — mas nenhuma teve o corpus completo em contexto, e todas
compartilhavam os pontos cegos de um mesmo modelo.

A rodada foi desenhada para a força oposta: **nada de executar, tudo de ler**. O
prompt proibiu explicitamente rodar comando, e pediu oito análises que só são
possíveis com todos os arquivos abertos ao mesmo tempo.

## O achado que justificou a rodada

E ele não veio na tabela de achados: veio na seção de **conflito de instrução**,
que foi a única análise pedida que nenhuma rodada anterior tinha feito.

**Três documentos vivos mandavam "inglês em identificadores". A biblioteca media
outra coisa.**

| Onde a regra estava | Texto |
|---|---|
| `.claude/rules/docs-e-readmes.md` | *"PT-BR na prosa; inglês em código, nomes técnicos e identificadores"* |
| `ambiente_fonte/.assistant_instructions.md` | *"use inglês em código, nomes de funções, variáveis e objetos técnicos"* |
| `hub_padroes/readme/template.md` | *"PT-BR na prosa, inglês em código e identificador"* |

Medição feita na verificação do achado:

| Categoria | Inglês | Português |
|---|---|---|
| Funções e classes públicas | **85** | **5** |
| Constantes públicas | 35 | **37** |

O que torna isto grave não é a contagem: é **onde a regra vive**. O
`.assistant_instructions.md` é publicado e injetado em **toda** conversa do Genie
Code. O assistente era instruído a usar identificadores em inglês e, na mesma
sessão, mandado importar `AZUL_CAIXA`, `PALETA_CATEGORICA` e `SECOES_EDA`. A
instrução e a biblioteca discordavam dentro da mesma janela de contexto.

**A correção foi na regra, não na biblioteca.** Constante de domínio em português
é decisão certa: `AZUL_CAIXA` nomeia a paleta institucional e `SECOES_EDA` nomeia
as seções desta EDA — traduzir apaga o referente. As 37 saem da dívida, e a regra
passou a dizer o que o projeto de fato pratica: *inglês em função, classe,
parâmetro e coluna devolvida; constante de domínio pode ser português*.

Ficaram as **cinco funções** — `aplicar_tema`, `gerar_indice_eda`, `get_tema_eda`,
`calcular_psi`, `calcular_csi` —, que são deriva contra uma convenção que 85 irmãs
cumprem. Viraram `PLANO_HUB.md` §12.3, com a razão de não terem sido renomeadas
agora: renomear função pública quebra quem chama, em silêncio.

## Os três achados da tabela

| # | Reportado | Veredito | O que foi feito |
|---|---|---|---|
| 1 | `PLANO_HUB.md` diz "7 cores da paleta" para `curves_plotly`; o código tem 6 | **parcial** | o módulo tinha **7 hexadecimais oficiais** distintos — 6 da paleta e o `TEXTO_SECUNDARIO`. O número estava certo; a palavra "cores da paleta" é que estava imprecisa. A correção proposta (trocar 7 por 6) teria **introduzido** um erro. Texto reescrito para "7 hexadecimais, 6 deles da paleta" |
| 2 | O glossário do produto remete a `docs/` e `tools/`, que não são publicados | **improcedente** | é o achado A14 da rodada de 18/08, corrigido no mesmo dia. O aviso está **quatro linhas abaixo do título** do glossário, no arquivo que o auditor recebeu |
| 3 | A skill do tutor escreve "Asset Bundles"; o nome legado oficial é "Databricks Asset Bundles" | **procedente** | corrigido |

O achado 3 veio com uma justificativa **errada**: *"um usuário buscando suporte
pelo termo completo pode não ativar o gatilho da skill"*. O corpo da skill não
participa do roteamento — quem roteia é a `description`, e o prompt da rodada
declarava esse fato explicitamente. O achado é válido por precisão de vocabulário,
não por gatilho.

## O que não se confirmou, e por quê

**O conflito do exemplar de skill.** Foi reportado que
`hub_padroes/skill/template.md` proíbe copiar `exemplo/` enquanto
`hub-ml-criar-objeto` manda "aplicar o template", e que a IA copiaria a árvore
inteira. A leitura não se sustenta: o aviso está no **cabeçalho do próprio
molde**, e a skill manda **ler** o exemplar, não copiá-lo.

Mas o risco por trás dele é real e passou a estar escrito: qualquer pasta dentro
de `.assistant/skills/` é **auto-descoberta**, então uma cópia acidental do
exemplar viraria skill fantasma no chat. A skill ganhou a frase.

**A "nova classe de defeito"** reportada — normas em prosa que o validador não
mede — é a classe nomeada na rodada anterior, `norma publicada sem instrumento`,
que o prompt listava entre as já conhecidas. Veio acompanhada de uma afirmação
falsa: *"o `validate_assistant.py` varre zero da forma intelectual"*. O arquivo
recebido tinha `check_docstring_em_portugues` e `check_normas_do_molde`, escritos
justamente para isso, e ambos citam as normas que cobram.

**As previsões dos três forward tests foram inventadas.** O prompt indicava o
arquivo e a seção com os enunciados literais. Vieram três enunciados diferentes,
escritos pelo auditor. As previsões não servem para conferir os testes de
setembro, que era o objetivo do item.

## O que aprender sobre o método, e não sobre o repositório

A rodada valeu, e vale registrar por que **apesar** do índice de acerto baixo.

**Segunda origem funciona mesmo com desempenho menor.** O achado de idioma estava
disponível para as catorze rodadas anteriores e nenhuma o viu, porque nenhuma leu
uma regra de estilo contra a biblioteca inteira. Um achado procedente que só a
troca de origem produz paga uma rodada com dois improcedentes.

**A análise que rendeu foi a que ninguém tinha pedido antes.** Das oito
solicitadas, a única inédita — ler as 13 skills e as instruções pessoais como um
corpo único de instruções — foi a que produziu o achado real. As sete que
repetiam ângulos já auditados devolveram matrizes corretas e vazias.

**Auditor sem execução precisa de âncoras mais rígidas.** Três dos problemas do
relatório — a fabricação dos enunciados de teste, a afirmação falsa sobre o
validador, e o achado já corrigido — têm a mesma raiz: sem poder rodar nada, o
auditor preenche a lacuna com plausibilidade. O prompt exigia citação literal dos
dois lados; a exigência precisa vir com um pedido explícito de **transcrever
antes de julgar**, e não só de citar ao julgar.

## Ações

| Ação | Estado |
|---|---|
| Regra de idioma corrigida nos três documentos vivos | ✅ |
| `PLANO_HUB.md` §12.3 — cinco funções públicas em português | ✅ declarada |
| `PLANO_HUB.md` §12.2 — "7 hexadecimais, 6 deles da paleta" | ✅ |
| Nome legado completo na skill do tutor | ✅ |
| Aviso de que o exemplar de skill não se copia | ✅ |
| Renomear as cinco funções | **decisão de produto** — quebra contrato público |
| Instrumentar a regra de idioma de identificador | **descartado, com razão registrada** em §12.3 |
