# Auditoria da documentação — segunda rodada

> **Nomenclatura da época.** Os nomes `x_*` e `rodrigo-*` neste registro são
> os que existiam na data. A tradução para os nomes atuais está na tabela de
> correspondência do [ADR-0006](../../decisions/ADR-0006-identidade-hub.md);
> este documento não é reescrito porque descreve o que foi observado, não o
> estado atual.

Data: 2026-08-15 · Auditor: Claude em sessão sem contexto, com acesso ao sistema
de arquivos e à CLI do Databricks · Nível: **A1**

## Desenho da rodada

A rodada anterior cobriu 8 documentos e pediu para **ler e julgar**. Esta cobriu
os **15 READMEs** do repositório e pediu para **executar**: seguir o percurso
inicial ao pé da letra, rodando os comandos, e comparar cada README com o
conteúdo real da pasta que ele documenta.

Sete documentos entraram no escopo pela primeira vez: `.claude/skills/`,
`ambiente_fonte/`, e os índices de `docs/decisions/`, `docs/auditoria/`,
`docs/handoffs/`, `docs/testes/forward/` e `docs/testes/spark/`.

O auditor foi instruído a **não** ler `CHANGELOG.md`, o conteúdo dos ADRs, as
auditorias anteriores nem o guia temporário de replicação — e a rodada anterior
não foi mencionada. Saber que algo já foi revisado é o tipo de informação que
faz um auditor procurar menos.

Continua sendo A1: mesmo modelo do autor, pontos cegos comuns permanecem.

## Resultado

25 achados, **todos procedentes**. Quatorze classificados como erro factual,
onze como oportunidade de melhoria. Nenhum foi descartado.

| Categoria | Achados | Situação |
|---|---|---|
| Proteção que não cobria o que prometia | 3 | corrigidas, todas com mudança de código |
| Procedimento documentado que não executa | 3 | corrigidos |
| Contradição entre documentos | 4 | corrigidas |
| Índice que nega o próprio conteúdo | 3 | preenchidos |
| Defeito de código encontrado por leitura de documento | 1 | corrigido |
| Didática, ordem, excesso e ausência | 11 | ajustados |

## Os quatro achados de maior impacto

**A proteção contra identificador corporativo dependia do diretório atual.** A
varredura de repositório inteiro partia de `Path(".")`. Rodada de qualquer pasta
que não a raiz — de `tools/`, por exemplo —, ela varria quatro arquivos em vez de
quatrocentos e devolvia `APROVADO: 0 falha(s), 0 aviso(s)`, sem um único aviso de
que a proteção não tinha rodado. Reproduzido e corrigido em três frentes: a raiz
passou a ser derivada de `__file__`, varredura vazia passou a **reprovar**, e o
padrão foi ampliado de três alternativas para matrícula genérica, domínio
corporativo e domínio bancário. O README passou a listar o que é bloqueado, em
vez de prometer cobertura genérica — a lista não é exaustiva, e afirmar que é
seria o mesmo defeito com outra roupa.

**O percurso inicial publicava o espelho antigo e passava na conferência.** A
"Primeira hora" mandava rodar quatro comandos "logo abaixo"; o bloco do render
aparecia sem `--write`, que é o que efetivamente escreve. Quem copiasse os blocos
na ordem publicava o espelho anterior e recebia `APROVADO` na conferência —
porque ela compara workspace contra espelho, nunca contra a fonte. Os quatro
comandos passaram a estar no próprio passo 4, com o `--write` e a explicação do
porquê.

**Um script carregava, ainda hoje, o defeito que a documentação declarava
eliminado.** `docs/testes/spark/` listava como corrigidos `null_summary` e cinco
`x_scripts`. São seis os scripts que leem tabela: `naming_checker` referenciava o
global de notebook `spark`, sem sequer importar `pyspark`. Ele nunca foi coberto
pelo smoke test, então nunca foi importado no runtime — passava na validação
estática porque é sintaticamente válido. O achado veio de comparar uma lista em
prosa com o código, não de executar. Corrigido, e uma varredura por AST confirmou
que nenhum outro módulo de `x_snippets` ou `x_scripts` usa o global.

**A CLI documentada era a errada.** O README mandava `pip install databricks-cli`,
que instala a CLI legada, parada na 0.18 e desaconselhada pela própria Databricks
— sem `auth login` nem `current-user`, e capaz de sombrear o binário correto no
PATH em Windows. Todo o resto do documento foi produzido com a v1.12.1, instalada
por winget. O README ainda antecipava o sintoma errado, mandando o leitor caçar
problema de autenticação onde a causa era outra.

## O que apareceu ao corrigir

Corrigir a cegueira do `--verify` a diretórios órfãos revelou algo que não estava
em nenhum achado: **a plataforma escreve dentro de `.assistant/`**. Abrir o
painel de MCP em Genie Code → Settings materializa
`/Users/<username>/.assistant/.mcp_servers.json` com a lista de conectores
internos. Sem tratamento, a conferência recém-corrigida classificaria um arquivo
gerenciado pela plataforma como obsoleto e mandaria apagá-lo.

O arquivo passou a ser reconhecido e reportado à parte. A observação foi
registrada em `.claude/rules/genie-code-oficial.md` com a inversão que importa:
o arquivo é **saída** da configuração, nunca entrada — criá-lo à mão não
configura integração nenhuma, o que preserva a afirmação original da regra.

## O que o auditor confirmou

Delimita o que a correção não precisou tocar. Verificados contra o disco e
aprovados: a tabela de inventário de `x_snippets` fecha nos dois sentidos (51
módulos reais, zero fora da tabela, zero citados e inexistentes); os 16 arquivos
de `x_prompts`; as 8 entradas de `x_docs`; os 5 ADRs; as assinaturas e chaves de
retorno de `quick_profile`, `data_quality_check` e `drift_detector`, incluindo a
aritmética do `score` e a mensagem de freshness; os `assert` de formatação
brasileira; os 64 PASS e 7 opcionais ausentes conferidos no JSON bruto da rodada
5; os 7 módulos que importam biblioteca opcional no topo e os 7 que a importam
dentro da função; e seis dos sete diagramas do conjunto.

`ambiente_fonte/.assistant/x_docs/glossario.md` foi apontado como o melhor
documento do conjunto, pela separação entre plataforma, modelagem e convenção
local, e pela seção que descreve o que **não** existe.

## O que ficou sem verificação

Que `description` seja o único campo lido no roteamento — cinco documentos
afirmam, todos concordam entre si, e a confirmação depende da documentação
oficial, sem acesso web na sessão. Se os registros de forward test refletem
execução real no navegador: o auditor viu os arquivos, não o comportamento. E o
comportamento de `--execute` com o espelho desatualizado, por ser escrita.

## Lição para o processo

Terceira rodada em que uma sessão sem contexto encontra defeito relevante em
material já revisado pelo autor. Treze achados na biblioteca, vinte e dois na
primeira rodada de documentação, vinte e cinco nesta.

O que mudou aqui foi o método. Mandar **executar** em vez de ler produziu os dois
achados mais caros — o percurso que publica o espelho velho e a proteção que
depende do diretório atual —, e nenhum dos dois é visível em leitura. Comparar
cada README com o conteúdo real da pasta produziu um defeito de código que dois
gates de teste não pegaram.

Vale manter as duas instruções nas próximas rodadas, e vale registrar a categoria
que se repete nas três: **promessa mais ampla que a implementação**. Apareceu na
garantia de identificador corporativo (duas vezes, em rodadas diferentes), na
verificação de links, na detecção de obsoletos e no contrato de sessão Spark.
