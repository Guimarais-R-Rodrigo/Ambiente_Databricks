# Manual Técnico

## Entender o Hub e o Databricks sem precisar ser desenvolvedor

Este manual explica o que acontece entre abrir o ambiente, pedir ajuda à Genie Code, importar uma função e obter um resultado. Foi escrito para quem utiliza ou acompanha o projeto, mas ainda não domina Python, Spark, APIs ou infraestrutura. Os termos aparecem primeiro com uma explicação concreta; depois, quando necessário, com o nome técnico e um exemplo.

**A ideia central:** o Hub não é uma API remota que o Databricks “puxa” automaticamente. Ele reúne arquivos de orientação para a IA e bibliotecas Python reutilizáveis. A conversa recebe contexto; o interpretador importa código; o mecanismo de execução processa os dados. São operações relacionadas, mas diferentes.

Este documento incorpora as funções de consulta antes separadas no catálogo de helpers e no glossário. Os READMEs continuam sendo a porta de entrada visual e operacional. Os componentes visuais já escolhidos não são substituídos por este manual.

**Base examinada:** código do commit `c5fdc61181c14124d653cf9e6222d9a402745949`, após a limpeza das pastas de rascunhos. As explicações sobre plataforma foram confrontadas com documentação oficial consultada em **11/09/2026**. Exemplos com dados são sintéticos. Uma saída esperada não é prova de execução em seu workspace; diferenças de versão, dependência e permissão precisam ser verificadas no destino.

**Manutenção de uma única redação:** a versão de autoria fica em `ambiente_fonte/.assistant/MANUAL_TECNICO.md`. O arquivo homônimo da raiz do repositório é uma cópia de leitura do mesmo conteúdo; o simulado recebe a cópia produzida pelo renderer. Não mantenha redações divergentes. As referências de implementação ao final apontam para o snapshot examinado, para não transformar uma alteração futura em evidência retroativa.

<a id="como-ler"></a>
## Como ler e encontrar uma resposta

Na primeira leitura, acompanhe os capítulos 1 a 8. Eles constroem o vocabulário necessário para entender as outras partes. Para operar um notebook, avance para os capítulos 9 a 15. Para compreender análises, modelos e controles, use os capítulos 16 a 24. O inventário de helpers e o índice de termos, no final, servem para consulta.

| Sua dúvida | Onde procurar |
|---|---|
| O que é este ambiente e onde cada coisa fica? | [1. Visão geral](#visao-geral) e [2. Pastas e caminhos](#pastas) |
| O que significa API? O Databricks busca uma API do projeto? | [3. Quatro sentidos de API](#apis) |
| O que são função, argumento, retorno e contrato? | [4. Como ler código](#codigo) e [5. Contratos](#contratos) |
| O que fazem `sys.path`, `import`, `__init__.py` e `__all__`? | [6. Importação](#importacao) e [7. Exemplo linha a linha](#bootstrap) |
| Por que mudei o arquivo e o notebook continua usando a versão anterior? | [8. Estado e reinicialização](#estado) |
| Qual a diferença entre pandas, Spark, tabela e view? | [9. Dados](#dados), [10. Spark](#spark) e [11. SQL e Unity Catalog](#unity-catalog) |
| Por que instalar uma biblioteca não resolveu? | [12. Dependências](#dependencias) |
| Como a Genie Code descobre skills e usa helpers? | [13. Contexto e execução](#genie) |
| O que são os widgets, cards e imagens? | [14. Apresentação](#visuais) |
| Como ler um diagnóstico de qualidade? | [15. Exemplo completo](#qualidade) |
| O que são leakage, point-in-time, RFV, PSI, CSI e WOE? | [16. Tempo e junções](#tempo), [17. RFV](#rfv) e [18. Estatística](#estatistica) |
| Como se escolhem modelos e se interpretam métricas? | [19. Modelos](#modelos) e [20. Métricas](#metricas) |
| O que o MLflow registra? | [21. Experimentos](#mlflow) |
| Como APIs remotas, CLI e autenticação se relacionam? | [22. Integrações](#integracoes) |
| O que são render, deploy, manifesto, CI e smoke test? | [23. Publicação](#publicacao) e [24. Validação](#validacao) |
| Apareceu um erro. Por onde começo? | [25. Segurança](#seguranca) e [26. Diagnóstico de erros](#erros) |
| Qual helper, skill ou prompt atende à minha demanda? | [27. Inventário de helpers](#catalogo-helpers) e [28. Métodos e briefings](#metodos) |
| Não lembro o significado de um termo | [29. Índice de termos](#indice-termos) |
| De onde veio a informação? | [30. Fontes e alcance](#fontes) |

<a id="visao-geral"></a>
## 1. O projeto visto como uma oficina de trabalho

Imagine uma equipe que precisa investigar uma campanha, preparar dados e avaliar um modelo. Ela precisa de orientações de trabalho, de um pedido bem formulado, de instrumentos confiáveis e de uma forma de conferir o resultado. O Hub organiza essas necessidades.

Uma **skill** funciona como um procedimento especializado: indica o método, as perguntas e os cuidados. Um **prompt** é o briefing da tarefa concreta: objetivo, dados, período, restrições e entrega. Um **helper** é uma implementação reutilizável: uma função que realmente calcula, transforma ou apresenta algo. Um **padrão** orienta a construção de novos componentes. O **README** ajuda a escolher por onde começar.

A analogia tem um limite importante. A skill é texto que orienta um modelo de linguagem; não é uma pessoa responsável pela decisão. O helper é software; pode ter defeitos e não conhece automaticamente a intenção de negócio. Uma rotina pode executar sem erro e ainda responder à pergunta errada, por exemplo quando recebe a chave de cliente como se fosse a chave de evento.

Há cinco componentes funcionais principais. `skills/` contém métodos para a Genie Code. `hub_prompts/` contém briefings. `hub_snippets/` contém funções, classes e constantes reutilizáveis. `hub_scripts/` contém utilitários para inspeção, transformação e documentação. `hub_padroes/` contém moldes de novos objetos. `hub_readmes_visual_assets/` sustenta a apresentação; não é um sexto mecanismo de análise nem uma extensão nativa de execução.

**Nativo** significa que a plataforma reconhece o mecanismo, como Agent Skills. **Customizado** significa que o conteúdo ou a implementação foi criado neste projeto, como `hub-ml-eda-profissional` ou `data_quality_check`. Assim, uma skill do Hub combina um mecanismo nativo com um método escrito localmente. O prefixo `hub_` não concede suporte especial da Databricks ao algoritmo.

O projeto também não substitui o banco de dados, não cria um modelo treinado apenas ao ser copiado e não instala todas as dependências apenas porque inclui um arquivo `requirements-optional.txt`. Cada uma dessas ações exige um mecanismo próprio, explicado adiante.

<a id="pastas"></a>
## 2. Quatro lugares que não devem ser confundidos

### 2.1. Repositório, produto, simulado e workspace

O **repositório Git** é o conjunto versionado de arquivos: produto, documentação, ferramentas e histórico. Um **commit** identifica uma versão desse conjunto. A raiz do Git é o primeiro nível do repositório, não necessariamente o local de onde um notebook importa suas bibliotecas.

`ambiente_fonte/` guarda o produto que será distribuído. Dentro dela, `.assistant_instructions.md` é irmão da pasta `.assistant/`: ele não fica dentro de `skills/`. A pasta `.assistant/` contém os componentes usados pelo Hub.

`Novo_Ambiente_Simulado/` é uma árvore de arquivos que reproduz a organização de destino. **“Simulado” aqui não significa um Databricks rodando localmente.** O diretório não fornece compute, tabelas ou uma Genie Code local. Ele facilita conferir e copiar os arquivos certos para os lugares certos.

O **workspace Databricks** é o ambiente operacional: interface, arquivos, notebooks, recursos de dados, configurações e permissões. O conteúdo publicado lá é uma cópia operacional. Uma alteração feita somente no workspace não atualiza o Git; uma mudança no Git tampouco se publica sozinha por existir um commit.

```text
Repositório Git
  ambiente_fonte/                       fonte editável do produto
    .assistant_instructions.md          instruções pessoais
    .assistant/
      README.md                         entrada do Hub
      MANUAL_TECNICO.md                  explicação técnica e consulta
      skills/                           métodos
      hub_prompts/                      briefings
      hub_snippets/                     biblioteca reutilizável
      hub_scripts/                      utilitários
      hub_padroes/                       moldes
      hub_readmes_visual_assets/        recursos visuais

  Novo_Ambiente_Simulado/                árvore gerada, não um servidor
    Users/usuario-free/
      .assistant_instructions.md
      .assistant/...
```

A organização de manutenção do Git também inclui `tools/`, `docs/` e os arquivos de instruções dos agentes. Esses arquivos de controle não são widgets nem componentes a copiar indiscriminadamente para o workspace. A consolidação deste manual não significa que o projeto inteiro deva ser reduzido a dois arquivos.

### 2.2. Caminho de arquivo, caminho de importação e nome de tabela

Um **caminho de arquivo** indica onde um objeto é encontrado no sistema de arquivos: `hub_snippets/constants/format_br/format_br.py`. As barras separam diretórios. Um **caminho Python de importação** identifica pacotes e módulos: `hub_snippets.constants.format_br`. Os pontos fazem parte do sistema de nomes do Python. Um **nome de tabela** como `catalogo.analytics.eventos` identifica catálogo, schema e tabela. Também contém pontos, mas não é um import Python.

Por isso, colocar `catalogo.analytics.eventos` em `sys.path` não dá acesso à tabela. Da mesma forma, `spark.table("hub_snippets.constants.format_br")` não importa um formatador: tenta resolver um recurso de dados com esse nome.

Um caminho **absoluto** parte de uma raiz conhecida; um caminho **relativo** depende do lugar de onde é interpretado. Em um link Markdown, `../` sobe um diretório em relação ao documento. Em um comando Python, a resolução de arquivos relativos normalmente depende do diretório de trabalho. Em um import relativo, o ponto é relativo ao pacote Python. São três contextos diferentes.

### 2.3. `/Users`, `/Workspace/Users` e a pasta local

A API de objetos do workspace usa caminhos como `/Users/<username>/.assistant`. O acesso de arquivos pelo Python em contextos de workspace files costuma usar `/Workspace/Users/<username>/.assistant`. O primeiro é um endereço de objeto na plataforma; o segundo é a representação de arquivos acessível ao código. Não acrescente ou remova o prefixo mecanicamente sem saber qual ferramenta recebe o caminho. [S04](#fonte-s04); [S17](#fonte-s17)

`<username>` é um **placeholder**, um campo a substituir pelo nome de usuário autorizado. Ele não é um identificador real a procurar. No seu computador, o checkout pode estar em `C:\Projetos\Ambiente_Databricks`; esse endereço não passa a existir no servidor porque foi escrito em um notebook.

Uma pasta com ponto inicial, como `.assistant` ou `.claude`, pode aparecer oculta em algumas interfaces. Isso é uma convenção de apresentação; não é uma proteção de acesso. E o nome `.assistant` sozinho não faz o Python descobrir todas as suas funções.

<a id="apis"></a>
## 3. API: quatro sentidos que aparecem na mesma conversa

**API** é a sigla de *Application Programming Interface*, ou interface de programação de aplicações. É a forma prevista de um software ser utilizado por outro código. Uma API não precisa ser um site, um servidor ou um serviço pago. Pode ser simplesmente o conjunto de funções que uma biblioteca oferece.

Pense no painel de um equipamento: os botões disponíveis e o que cada um faz são a interface. A fiação interna corresponde à implementação. O usuário do equipamento precisa saber qual botão apertar e quais condições respeitar; não precisa refazer a fiação para cada uso.

### 3.1. A API pública dos helpers: nomes disponíveis para o Python

Quando o projeto escreve “API: `fmt_pct`”, está dizendo que essa função é um ponto de uso da biblioteca. O código chama `fmt_pct(0.154)` e recebe a string `"15,4%"`. Nesse exemplo, **não há requisição HTTP, chave de API ou download de uma função da internet**. O código da função já precisa estar acessível ao interpretador.

“Pública” significa disponível como contrato de uso do pacote, não disponível para qualquer pessoa na internet. O arquivo pode estar em um repositório privado e continuar tendo uma API pública para os consumidores autorizados desse pacote.

A API inclui nomes, parâmetros e resultados. Se uma função muda de `checks` para `metrics` no retorno, consumidores podem quebrar mesmo que o nome da função permaneça igual. Se uma função devolve três DataFrames, tratá-la como um único número também viola seu contrato.

### 3.2. A API do Spark: instruções para trabalhar com dados

Em `df.filter(...)` ou `spark.table(...)`, o código usa a interface oferecida pelo Spark. `filter` descreve uma seleção de linhas; `table` resolve uma tabela ou view. Essas operações podem construir um plano que será executado depois. Em Spark Connect, o cliente envia planos a um serviço Spark remoto. Isso é distinto tanto de importar um helper quanto de chamar a API administrativa do workspace. [S10](#fonte-s10); [S11](#fonte-s11)

Um helper pode usar a API do Spark internamente. A sequência é: importar a função do Hub, chamar a função, e essa função construir ou executar operações Spark. O fato de haver processamento remoto nessa última etapa não transforma o arquivo Python do helper em uma API REST.

### 3.3. A API REST do Databricks: pedidos a serviços da plataforma

REST é um estilo de interação entre sistemas; no uso aqui, são requisições HTTP a endereços da Databricks. Um **endpoint** é o endereço de uma operação, por exemplo consultar o status de um objeto do workspace. A requisição inclui destino, parâmetros e autenticação; a resposta contém dados ou uma indicação de erro. [S05](#fonte-s05); [S18](#fonte-s18)

Ferramentas de administração podem usar essa API para listar arquivos, importar um notebook, consultar jobs ou acompanhar uma execução. Cada operação tem permissões e efeitos próprios. Listar um arquivo não executa suas células. Importar uma biblioteca não a treina. Consultar o estado de um job não equivale a criar outro job.

### 3.4. API de inferência de modelo: uma possibilidade, não algo criado pelo Hub

Um modelo treinado pode, em outra etapa de engenharia, ser disponibilizado por um serviço que recebe dados e devolve previsões. Esse é um uso possível de uma API de inferência. **Copiar os helpers deste repositório não cria um endpoint de serving, um contrato de disponibilidade nem uma cobrança independente de API do Hub.** É necessário configurar o serviço, o modelo, autenticação, monitoramento e governança.

### 3.5. Então, como o Databricks “puxa” a API do projeto?

Para os helpers, a pergunta mais precisa é: **como o Python do notebook encontra e carrega a biblioteca?** Ele precisa de arquivos acessíveis e de um caminho de importação resolvível. O comando `import` utiliza o sistema de importação do Python. A função importada é então chamada pelo código consumidor.

Para a Genie Code, a pergunta é outra: **como ela recebe instruções e reconhece uma skill relevante?** Isso depende dos mecanismos de contexto da plataforma. A coluna “API” do catálogo não registra endpoints na Genie Code e não faz todas as funções entrarem em sua conversa.

| Expressão no projeto | O que significa | O que não significa |
|---|---|---|
| API do helper | Funções, classes e constantes oferecidas | Serviço HTTP automaticamente publicado |
| `import` | Carregamento de módulo no Python | Download, instalação ou autorização de acesso a dados |
| API Spark | Operações sobre dados e execução distribuída | Cadastro de uma skill |
| API REST Databricks | Operações remotas da plataforma | A biblioteca do Hub sendo descoberta pelo chat |
| `@nome-da-skill` | Seleção explícita de método/contexto | Chamada Python com os parâmetros do helper |

<a id="codigo"></a>
## 4. Ler código sem precisar escrever um sistema inteiro

### 4.1. Valor, variável, tipo e estrutura

Um **valor** é um dado: `20`, `0.05` ou `"email"`. Uma **variável** é um nome associado a um objeto, como `total = 20`. O sinal `=` atribui um valor; `==` compara dois valores. Aspas indicam texto: `"20"` não é o mesmo tipo de objeto que `20`.

Um `int` representa um inteiro; `float`, um número em ponto flutuante; `str`, texto; `bool`, verdadeiro ou falso. `None` indica ausência de valor naquela referência. Uma **lista**, como `["event_id", "dt_evento"]`, reúne itens em uma sequência. Um **dicionário**, como `{"status": "warn", "score": 95}`, relaciona chaves e valores. Uma **tupla**, como `(treino, validacao, teste)`, agrupa valores cuja posição importa.

O ponto em `resultado.items()` acessa um atributo ou método do objeto. Os colchetes em `resultado["status"]` acessam um item do dicionário. Os parênteses em `fmt_pct(0.154)` efetuam uma chamada. Entender esses três sinais já permite ler grande parte dos exemplos do Hub.

### 4.2. Função, parâmetro, argumento e retorno

Uma **função** agrupa uma operação sob um nome. **Parâmetros** são os campos previstos em sua definição; **argumentos** são os valores fornecidos na chamada. Em `fmt_pct(0.154, casas=1)`, `casas` é o nome do parâmetro, e `1` é o argumento escolhido.

O **retorno** é o objeto entregue pela função ao código que a chamou. `print(...)` mostra uma representação na saída; não substitui o retorno. Um helper que devolve HTML entrega texto com marcação. Outro componente ainda precisa exibi-lo como HTML para que ele vire um card.

Exemplo conceitual, não um novo helper do projeto:

```python
# EXEMPLO: funcao_didatica

def calcular_proporcao(sucessos: int, total: int) -> float:
    if total <= 0:
        raise ValueError("O total precisa ser positivo.")
    return sucessos / total

proporcao = calcular_proporcao(sucessos=2, total=10)
assert proporcao == 0.2
```

`def` inicia a definição. A indentação mostra quais instruções pertencem à função. `if` verifica uma condição. `raise` interrompe o fluxo com uma exceção explicativa. `return` entrega o resultado. O exemplo ilustra sintaxe; não substitui o exemplar real `taxa_resposta_campanha`, que retorna uma tabela por segmento e inclui medidas de incerteza.

### 4.3. Classes, instâncias e métodos

Uma **classe** descreve um tipo de objeto com dados e comportamentos. Uma **instância** é um objeto concreto dessa classe. Um **método** é uma função vinculada ao objeto. Um monitor de performance pode armazenar uma referência e oferecer operações para comparar novas métricas.

No código de uma classe, `self` representa a instância sobre a qual o método trabalha. `__init__` é o método de inicialização da instância. Ele não é o mesmo que o arquivo `__init__.py`, que organiza um pacote. Os nomes são parecidos, mas seus papéis são distintos.

### 4.4. Loops, condições e exceções

`for` repete uma operação sobre uma sequência. `if` e `else` escolhem caminhos. `try` e `except` tratam falhas previstas. Uma exceção não deve ser simplesmente escondida para produzir um relatório verde: o tratamento precisa dizer o que falhou e o que ficou sem ser verificado.

`assert` é útil para conferir uma expectativa em testes e exemplos. Não é uma fronteira de segurança: execuções Python com otimização podem remover assertions. Para uma regra operacional indispensável, o código deve fazer uma verificação explícita e levantar a exceção adequada. [S01](#fonte-s01); [S02](#fonte-s02)

<a id="contratos"></a>
## 5. A assinatura e o contrato de uma função

A **assinatura** apresenta o nome da função e seus parâmetros. O **contrato** é mais amplo: descreve entradas válidas, significado das colunas, resultados, efeitos, erros possíveis e limitações. Um tipo `DataFrame` não informa sozinho se o objeto é pandas ou Spark, qual é o grão ou se as datas já foram validadas.

Considere a interface real do formatador:

```text
fmt_pct(v: float, casas: int = 1, input_scale = "ratio") -> str
```

`v` é o número recebido. `casas=1` define o padrão quando o usuário não informa outro valor. `input_scale="ratio"` diz que o padrão espera uma razão: `0.154`, e não `15.4`. `-> str` indica o tipo de retorno documentado. As anotações de tipo ajudam a leitura e ferramentas, mas não impõem automaticamente toda a validação em runtime. [S02](#fonte-s02); [S03](#fonte-s03)

**Escalas são parte do contrato.** A razão `0.05` corresponde a `5%`. O número `5.0` também pode representar 5%, mas somente se a interface declarar que recebe percentuais. Enviar `5.0` a uma função que espera razão pode produzir `500%`. O mesmo cuidado vale para moeda, pontos percentuais, basis points, dias e meses.

Um asterisco isolado na assinatura, como `*, atraso_publicacao_dias`, exige que os parâmetros seguintes sejam informados pelo nome. Isso torna uma escolha importante visível na chamada. No `pit_join`, o atraso é obrigatório e não tem padrão: o projeto não presume que toda informação está disponível imediatamente.

`Optional[str]` ou `str | None` significa que o valor pode ser texto ou `None`. Isso não torna o argumento dispensável: para poder omiti-lo na chamada, precisa haver um padrão apropriado na assinatura. `Sequence[str]` indica uma sequência de textos. `Dict[str, Any]` admite valores de diferentes tipos e, portanto, exige consultar também a estrutura real do retorno.

**Efeito colateral** é algo que acontece além de produzir um retorno: escrever um arquivo, registrar métricas no MLflow, alterar uma view temporária ou iniciar processamento. Um nome como `train_*` sugere treinamento; a documentação deve esclarecer se também ocorre tracking remoto. Uma importação pode executar código de inicialização, mesmo quando a função principal não foi chamada.

É possível inspecionar uma interface já importada sem adivinhar seus parâmetros:

```python
# EXEMPLO: introspeccao
import inspect
from hub_snippets.constants.format_br import fmt_pct

print(inspect.signature(fmt_pct))
print(inspect.getfile(fmt_pct))
print(inspect.getdoc(fmt_pct))
```

O primeiro comando mostra a assinatura do objeto carregado. O segundo informa o arquivo do qual a função veio. O terceiro apresenta sua documentação embutida, a **docstring**. Isso ajuda a descobrir se o notebook está usando uma cópia diferente da que você abriu no editor. Os comandos não comprovam a correção estatística da implementação. [S03](#fonte-s03)

<a id="importacao"></a>
## 6. Como `import`, `sys.path`, `__init__.py` e `__all__` se encaixam

### 6.1. Módulo, pacote, biblioteca, snippet e helper

Um **módulo** é uma unidade de código importável; neste projeto, geralmente um arquivo `.py`. Um **pacote** agrupa módulos e outros pacotes. Uma **biblioteca** é um conjunto reutilizável de funcionalidades. **Snippet** é a categoria organizacional escolhida pelo projeto; não é uma categoria especial do interpretador. **Helper** descreve o papel de ajudar uma tarefa por meio de código reutilizável.

A forma de pasta por objeto do Hub coloca implementação, API de entrada e exemplo lado a lado:

```text
hub_snippets/
  constants/
    format_br/
      __init__.py            entrada pública do objeto
      format_br.py           implementação dos formatadores
      exemplo_format_br.py   notebook que demonstra o uso
```

O notebook de exemplo não deve ser a origem do `__init__.py`. Caso contrário, importar o objeto pode executar a demonstração inteira, em vez de apenas disponibilizar a implementação.

### 6.2. `sys.path` é uma lista de lugares para procurar módulos

`sys` é um módulo do próprio Python. `sys.path` é uma lista de diretórios que participa da busca por módulos. Ele não é uma URL de API, um catálogo de dados, uma autorização ou um instalador. [S01](#fonte-s01); [S06](#fonte-s06)

Para importar `hub_snippets`, a lista precisa permitir encontrar a **pasta que contém** `hub_snippets`. No layout distribuído, essa pasta é `.assistant`. Inserir apenas `.assistant/hub_snippets` pode falhar porque o import passa a procurar outro `hub_snippets` dentro dela.

`sys.path.insert(0, caminho)` coloca o diretório no início da lista; `append(caminho)` o coloca no final. O início dá prioridade à cópia escolhida, mas cria risco de **sombreamento**: um arquivo local chamado `json.py`, por exemplo, pode esconder o módulo esperado. Adicione somente diretórios confiáveis e confirme a origem do objeto importado quando houver dúvida.

Alguns contextos Databricks acrescentam automaticamente diretórios de notebook ou de Git folder à busca, e a distribuição de módulos aos executores depende do runtime. Isso não torna uma pasta arbitrária `.assistant` universalmente importável nem autoriza supor comportamento idêntico em classic e serverless. [S04](#fonte-s04)

### 6.3. O que o `__init__.py` real faz

A entrada de `format_br` reexporta nomes da implementação:

```python
from .format_br import Number, fmt_int, fmt_pct, fmt_brl, fmt_dec, fmt_delta, fmt_n
```

O ponto inicial em `.format_br` indica o módulo vizinho dentro daquele pacote. A reexportação permite escrever `from hub_snippets.constants.format_br import fmt_pct`, sem obrigar o consumidor a repetir o nome do arquivo interno.

O arquivo também define `__all__` com os nomes públicos. Essa lista disciplina especialmente `from pacote import *`; não cria uma restrição de segurança e não impede qualquer acesso técnico a outro atributo. O Hub prefere importações explícitas, porque deixam claro qual função está sendo usada. [S01](#fonte-s01); [S07](#fonte-s07)

Nem toda pasta possível em Python exige `__init__.py`, pois existem namespace packages. **O projeto, porém, adotou pacotes regulares e entradas explícitas por objeto.** Não remova o arquivo porque encontrou um exemplo diferente na internet.

### 6.4. API pública não é descoberta automática pela IA

A ferramenta de manutenção `tools/api_publica.py` lê a árvore sintática do módulo, sem importá-lo, e identifica funções, classes e nomes definidos no topo que não começam por `_`. Ela ajuda a conferir reexportações. Não registra funções no Databricks e não chama uma API remota para instalar a biblioteca.

Há uma regra local importante: o inventário da API pública não inclui apenas funções “mais interessantes”. Constantes e outros nomes públicos também podem ser usados por outro módulo. O leitor iniciante pode começar pelos pontos de entrada recomendados; o mantenedor precisa preservar o contrato completo.

<a id="bootstrap"></a>
## 7. Um carregamento real explicado linha a linha

O bloco abaixo prepara a importação em um notebook Databricks quando o Hub está no diretório do usuário. Substitua `<username>` pelo identificador do diretório autorizado. Não execute esse caminho literalmente em um computador local.

```python
# EXEMPLO: bootstrap_workspace
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if not (assistant_root / "hub_snippets").is_dir():
    raise FileNotFoundError("Confira o caminho e a presença do Hub no workspace.")

caminho = str(assistant_root)
if caminho not in sys.path:
    sys.path.insert(0, caminho)

from hub_snippets.constants.format_br import fmt_brl, fmt_pct

print(fmt_brl(1250000.50))
print(fmt_pct(0.154))
```

`from pathlib import Path` disponibiliza uma classe para representar caminhos. `import sys` dá acesso ao módulo de configuração do interpretador. Nenhuma das duas linhas instala pacote externo.

`assistant_root = Path(...)` cria uma representação do endereço. **Criar o objeto `Path` não cria a pasta e não baixa seus arquivos.** A verificação seguinte procura `hub_snippets` naquele endereço. O operador `/`, quando usado com `Path`, compõe caminhos; não está fazendo uma divisão numérica.

Se a pasta não for encontrada, `FileNotFoundError` impede continuar com uma configuração inválida. `str(assistant_root)` converte o caminho para o texto esperado na lista de busca. A condição `if caminho not in sys.path` evita repetir a mesma entrada a cada execução da célula.

O import de `fmt_brl` e `fmt_pct` carrega a entrada do pacote e disponibiliza as duas funções. As duas chamadas finais executam os formatadores e imprimem seus retornos.

Saída esperada para esses argumentos:

```text
R$ 1.250.000,50
15,4%
```

Essa execução demonstra importação e formatação. Não testa leitura de tabela, permissão de catálogo, disponibilidade de Spark ou execução de uma skill. A separação é útil: se esse exemplo funciona e a leitura de dados falha, a investigação deve avançar da biblioteca para a camada de dados.

No checkout local, use o endereço da pasta `ambiente_fonte/.assistant` dentro da sua cópia. Evite criar um “bootstrap universal” que tente vários diretórios silenciosamente: ele pode encontrar uma cópia antiga e produzir sucesso aparente.

<a id="estado"></a>
## 8. Estado do notebook: por que a ordem e a reinicialização importam

O **interpretador** executa Python. O **kernel** ou processo da sessão mantém objetos como variáveis, funções importadas e referências a DataFrames. Fechar uma aba, executar uma célula fora de ordem e reiniciar o processo não são a mesma ação.

Um notebook pode exibir uma saída salva de ontem sem que o código tenha sido executado hoje. Também pode apresentar uma célula que usa `df` embora a célula que cria `df` ainda não tenha rodado na sessão atual. **Código visível, saída visível e estado atual são três coisas diferentes.**

O Python normalmente reutiliza módulos já carregados, registrados em `sys.modules`. Alterar o `.py` em disco não substitui automaticamente todos os objetos existentes na memória. `importlib.reload` pode ajudar no desenvolvimento, mas reexportações e referências antigas podem continuar apontando para objetos anteriores. Reiniciar o Python e executar o preparo novamente costuma ser o teste mais claro de uma instalação limpa. [S07](#fonte-s07)

Isso não deve ser confundido com abrir um chat novo da Genie Code. Um chat novo renova o contexto de conversa; não é uma garantia de reinicialização do Python. Reiniciar o Python não é garantia de atualização dos metadados de uma skill no chat.

`%run` é um mecanismo de execução de outro notebook no contexto apropriado do Databricks; não equivale a importar uma função de uma biblioteca. O projeto favorece módulos importáveis para reutilização, mantendo os notebooks como demonstrações. `%pip` trata de dependências, e `%md` indica uma célula de documentação. São comandos especiais da experiência de notebook, não funções ordinárias de um arquivo Python.

`if __name__ == "__main__":` separa o comportamento de um arquivo executado diretamente daquele importado como módulo. `__pycache__` guarda cache de código compilado para o Python; não é cache de dados Spark. `PATH` ajuda o sistema operacional a localizar executáveis como `python` e `databricks`; `PYTHONPATH` pode influenciar a busca de módulos; `sys.path` é a lista usada pelo interpretador em execução. Misturar esses três nomes dificulta o diagnóstico.


<a id="dados"></a>
## 9. O que é dado e o que é apenas uma referência a dado

### 9.1. Linha, coluna, grão e chave

Uma tabela organiza linhas e colunas. O **grão** descreve o que uma linha representa: um cliente, um envio, uma compra ou a posição de um contrato em determinada data. A **entidade** é o objeto de negócio acompanhado. Uma **chave** identifica a linha ou a combinação de atributos usada para relacioná-la a outra base.

Em uma campanha, o mesmo cliente pode receber diversos contatos. `id_cliente` identifica a entidade, mas pode não identificar cada evento. `event_id` pode ser uma chave candidata de evento. Chamar uma coluna de chave não comprova unicidade: é necessário verificar duplicações e nulos.

Uma **chave composta** usa várias colunas, como cliente e data de referência. Se uma delas estiver ausente, a combinação pode deixar de ter o significado esperado. Contar linhas não é automaticamente contar clientes, contratos ou campanhas.

### 9.2. Schema e tipos

O **schema** descreve nomes, tipos e outras propriedades das colunas. Um campo numérico pode conter inteiro, decimal ou ponto flutuante. Uma coluna de data pode conter datas, timestamps ou apenas textos que parecem datas. `nullable` indica se o schema admite nulos, não quantos nulos foram observados.

Inferir tipos a partir de uma pequena amostra é conveniente, mas pode produzir surpresas. Uma coluna com números em alguns registros e texto em outros precisa de regra explícita de conversão. Para demonstrações controladas, declarar o schema evita ambiguidades. Para valores monetários que exigem exatidão decimal, a escolha de tipo deve ser deliberada; `float` não representa exatamente todos os decimais.

`NULL`/`None`, `NaN`, texto vazio e a palavra `"NÃO INFORMADO"` não são automaticamente a mesma coisa. O `data_quality_check` desta versão usa `isNull()` para nulidade Spark. Isso não transforma todos os sentinelas de negócio em ausências; a padronização precisa ocorrer antes ou ser diagnosticada separadamente.

### 9.3. pandas DataFrame, Spark DataFrame e tabela persistida

Um **pandas DataFrame** mantém dados tabulares no processo Python. É adequado para dados que cabem na memória disponível e para diversas bibliotecas de modelagem local.

Um **Spark DataFrame** representa uma estrutura tabular e um plano de operações. Os dados podem estar distribuídos, e parte do processamento só acontece quando uma ação exige o resultado. Por isso, dizer apenas “DataFrame é uma tabela na memória” não descreve adequadamente todos os usos de Spark. [S10](#fonte-s10)

Uma **tabela persistida** existe como recurso de dados além de uma variável de notebook. O objeto Python `df` pode se referir a essa tabela, mas sua existência não cria outra tabela persistente. `df = spark.table(...)` não equivale a gravar `df` no catálogo.

`toPandas()` transfere o resultado de um Spark DataFrame para uma estrutura pandas no lado do cliente/coordenador da execução. Se o resultado for grande, a memória pode se esgotar. `collect()` também reúne resultados localmente. Ambos precisam de justificativa de volume, não de uma proibição absoluta: coletar uma linha de agregados é muito diferente de coletar a base inteira.

### 9.4. Retornos possíveis no Hub

Um helper pode retornar um número, texto, um dicionário, uma lista de alertas, uma figura Plotly, um DataFrame ou uma tupla. Alguns retornam um objeto de modelo e métricas. Outros oferecem um contexto de execução, usado com `with`.

Antes de consumir o resultado, confira o contrato. `resultado["status"]` faz sentido em um dicionário com essa chave. `resultado.count()` em Spark pode disparar uma contagem distribuída; em outra classe, um método com o mesmo nome pode ter significado diferente.

**Serializar** é converter uma estrutura para um formato de transporte ou armazenamento, como JSON ou YAML. Um dicionário Python não é automaticamente um arquivo JSON. Uma string YAML não é automaticamente uma configuração aplicada à plataforma. É preciso distinguir representação, gravação e aplicação.

<a id="spark"></a>
## 10. Spark: planejamento e execução em vez de “rodar tudo no notebook”

### 10.1. Sessão, cliente, coordenador e executores

Uma **SparkSession** é a entrada para operações de dados e SQL no Spark. Em notebooks Databricks, costuma existir uma variável `spark` disponibilizada pelo ambiente. Uma função dentro de um módulo importado não herda automaticamente todas as variáveis globais do notebook.

Por isso, vários scripts deste projeto resolvem a sessão dentro do próprio módulo:

```python
from pyspark.sql import SparkSession
spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
```

Esse código procura uma sessão ativa e, conforme o ambiente, obtém ou cria uma sessão. Em seu computador, ele não autentica sozinho no Databricks nem escolhe um workspace remoto. Um Spark local precisa de instalação/configuração local; uma conexão remota precisa do mecanismo apropriado.

Na execução Spark clássica, o **driver** coordena o trabalho, e os **executores** processam tarefas sobre partições dos dados. Em **Spark Connect**, há uma separação explícita entre cliente e servidor: planos de operação são enviados ao serviço Spark. Não é correto presumir acesso direto à JVM do driver a partir de qualquer cliente. **JVM** é a máquina virtual Java, parte da base técnica do Spark. [S11](#fonte-s11)

### 10.2. Transformações e ações

Uma **transformação** descreve um novo conjunto de dados: selecionar colunas, filtrar linhas, agregar por grupo ou fazer uma junção. Uma **ação** exige trabalho para produzir um resultado, como contar, coletar ou gravar dados. Essa separação é chamada de avaliação preguiçosa, ou *lazy evaluation*.

```python
# Exemplo de leitura; pressupõe um Spark DataFrame df já preparado.
from pyspark.sql import functions as F

selecionados = df.filter(F.col("respondeu") == 1)
quantidade = selecionados.count()
```

`functions as F` é apenas um apelido local para o módulo de funções Spark. `F.col("respondeu")` representa uma expressão de coluna. `== 1` constrói a condição. `filter` descreve as linhas selecionadas. `count()` solicita sua contagem.

Isso explica por que um erro de coluna ou tipo pode aparecer na ação, e não exatamente na linha em que o plano foi criado, especialmente quando a resolução é adiada. Também explica por que repetir ações sobre um plano pode repetir trabalho, salvo otimizações e mecanismos de reutilização aplicáveis.

### 10.3. Partição, shuffle, broadcast e custo

Uma **partição** é uma unidade de divisão dos dados para processamento. Um **shuffle** redistribui dados entre unidades de execução, por exemplo para reunir linhas da mesma chave em uma agregação ou junção. Pode custar rede, disco e tempo.

**Broadcast** é uma estratégia de disponibilizar um lado pequeno de uma operação aos executores. Não significa que qualquer tabela se torna barata: o lado considerado pequeno precisa realmente caber nos recursos previstos. Escolher uma estratégia exige evidência de volume e plano de execução.

Um filtro que devolve poucas linhas ainda pode ler muitos arquivos se a organização dos dados não permitir descartar grandes partes da entrada. Um `limit` limita linhas devolvidas; não oferece, por si só, um teto universal de bytes lidos, tempo ou custo. “Amostrado” e “barato” não são sinônimos.

### 10.4. Funções Spark e UDFs

Uma função Spark nativa, como uma expressão de data ou agregação, é reconhecida pelo mecanismo de execução. Uma **UDF** é uma função definida pelo usuário para operar em um contexto distribuído. Um helper Python não vira UDF automaticamente: ele pode apenas construir expressões Spark a partir de funções nativas.

Isso importa porque código executado no cliente e código executado nos trabalhadores não têm necessariamente os mesmos arquivos, rede, memória ou dependências. A existência de uma biblioteca no processo do notebook não comprova disponibilidade em toda forma de execução distribuída.

### 10.5. Classic, serverless e Free não são o mesmo eixo

**Classic** e **serverless** descrevem modalidades de compute e suas interfaces. **Free Edition** descreve uma edição/oferta da plataforma. O laboratório Free deste projeto usa serverless, mas não se deve tratar “Free” como sinônimo de toda implementação serverless.

Na documentação consultada, serverless para notebooks e jobs usa interfaces Spark Connect, não suporta RDDs e possui restrições nas APIs de cache e em diversas configurações clássicas. **RDD** é uma abstração de dados distribuídos do Spark; nem todo exemplo antigo com `.rdd`, `_jvm` ou configurações de cluster será válido nesse ambiente. [S12](#fonte-s12)

Um erro `NOT_SUPPORTED_WITH_SERVERLESS` aponta para uma incompatibilidade de operação naquele compute. Não é resolvido automaticamente aumentando RAM nem usando um nome diferente para a variável. A solução pode ser escolher uma operação suportada ou outro compute autorizado.

O histórico do projeto contém resultados de laboratório datados. Um sucesso ou bloqueio antigo de MLflow, cache ou biblioteca opcional não deve virar uma afirmação universal sobre todos os workspaces atuais.

<a id="unity-catalog"></a>
## 11. SQL, Unity Catalog, tabelas e views temporárias

**SQL** é uma linguagem para consultar e transformar dados. **Unity Catalog** organiza e governa recursos como catálogos, schemas e tabelas, incluindo permissões e linhagem. A estrutura usual de nome é `catalog.schema.table`. [S13](#fonte-s13)

Uma analogia útil é edifício, andar e sala: o nome completo reduz a chance de entrar na sala homônima de outro andar. Ainda assim, saber o endereço não dá permissão para entrar. Permissões de uso do catálogo/schema e de acesso ao objeto são verificadas pela plataforma. [S19](#fonte-s19)

Uma **view** expõe uma consulta ou representação de dados. A chamada `createOrReplaceTempView` cria uma view temporária local à sessão Spark correspondente. Ela não equivale a criar uma tabela persistente no Unity Catalog. Outra sessão ou outro usuário não deve ser presumido capaz de encontrá-la. [S14](#fonte-s14)

No tutorial deste manual, a view temporária permite usar helpers que recebem `table_name` sem gravar dados persistentes. A alteração de sessão é intencional e limitada. Após reiniciar a sessão, execute novamente a célula que cria a view.

Para a Genie Code analisar essa demonstração, forneça a célula de preparação, o schema e, quando apropriado, a saída no contexto oferecido pela interface. **Escrever o nome da view na conversa não comprova que ela foi anexada como recurso persistente selecionável.** Se o assistente não recebeu o conteúdo, deve pedir contexto em vez de inventar colunas.

`SELECT` lê dados; comandos de escrita como `INSERT`, `UPDATE`, `DELETE` e determinadas operações `CREATE` alteram recursos. O significado de um comando não muda porque foi sugerido por IA. Uma tarefa “somente leitura” precisa ser traduzida em ações compatíveis com esse escopo.

**Linhagem** registra relações entre origem e produtos de dados. **Delta** acrescenta mecanismos transacionais e de versionamento ao armazenamento de tabelas. Mesmo quando há histórico disponível, reprodutibilidade exige identificar a versão ou o recorte usado; o nome de uma tabela que muda diariamente não reconstrói sozinho uma análise passada.

### Histórico, retenção e camadas de dados

Uma versão de tabela e uma versão de código são coisas diferentes. Time travel permite consultar versões históricas enquanto os dados e logs necessários continuarem disponíveis e a política aplicável permitir a consulta. Não é backup permanente: remoção de arquivos e retenção podem impedir reconstruir uma versão antiga. Registre a referência dos dados e a política de preservação, não apenas o commit do notebook. [S33](#fonte-s33)

Bronze, silver e gold são convenções de organização de dados — por exemplo, captura, tratamento e produtos analíticos —, não níveis de permissão concedidos por nome de pasta. Lakeflow Spark Declarative Pipelines organiza transformações declaradas e dependências. Expectations expressam condições de qualidade dentro do pipeline, com tratamento definido; não devem ser confundidas com um dicionário `status` de diagnóstico ad hoc. Este manual explica os conceitos citados nas skills, sem afirmar que já exista um pipeline desse tipo implantado pelo Hub. [S34](#fonte-s34); [S35](#fonte-s35)

<a id="dependencias"></a>
## 12. Dependências: estar no repositório não é estar instalado

Uma **dependência** é outro software necessário ao funcionamento de um componente. O código do Hub pode depender de pandas, Plotly, PySpark, MLflow ou bibliotecas especializadas. O Python que executa o notebook precisa conseguir importá-las no ambiente correto.

Um arquivo `requirements.txt` ou `requirements-optional.txt` é uma declaração de pacotes; ele não os instala por existir. Um **pin** fixa uma versão. Uma faixa de versões aceita alternativas. Uma **dependência transitiva** é exigida por outro pacote, mesmo que o usuário não a tenha solicitado diretamente.

O arquivo `hub_snippets/requirements-optional.txt` reúne dependências especializadas e observações de testes. Ele não deve ser interpretado como garantia de que instalar tudo junto funciona hoje. Combinações de NumPy, bibliotecas compiladas e runtimes gerenciados podem ser incompatíveis.

### 12.1. Falha ao importar e falha ao chamar

Há três situações distintas. Um módulo pode importar uma dependência no topo, falhando imediatamente se ela faltar. Pode importar a dependência dentro de uma função, falhando somente quando essa função for chamada. Ou pode tentar importar e tratar a ausência para preservar parte da funcionalidade.

No `prophet_wrapper`, a importação de Prophet ocorre dentro de `train_prophet`. Isso não significa que o wrapper não tenha outras dependências na importação. No `mlflow_run`, a ausência de MLflow é tratada no carregamento do módulo, mas usar a operação que efetivamente precisa do tracking continua exigindo o ambiente apropriado.

Portanto, **“importou” não equivale a “todas as funções estão operacionais”**. Um teste representativo precisa chamar o recurso relevante com dados pequenos e conferir o resultado, não apenas executar `import`.

### 12.2. Ambiente correto e reinicialização

Instalar uma biblioteca no PowerShell do computador não a instala no Python do notebook remoto. Instalar em um notebook também não garante disponibilidade em todos os jobs ou futuras sessões. Um ambiente virtual local, uma configuração de serverless e uma biblioteca de compute têm ciclos de vida diferentes.

A documentação atual de serverless descreve configuração de ambiente e dependências. O mecanismo aplicável depende do tipo de tarefa e da configuração do notebook. Não instale uma distribuição arbitrária de `pyspark` dentro de um notebook Databricks para reproduzir um teste local: você pode substituir componentes gerenciados e criar outro problema. [S15](#fonte-s15)

Reiniciar o Python após mudar dependências pode ser necessário e descarta estado do processo. Isso exige recriar variáveis, imports e, conforme a sessão, recursos temporários. Uma mensagem de sucesso do instalador não substitui um teste de importação e uma chamada mínima.

### 12.3. Wheel, pacote de implantação e Git folder

Uma **wheel**, arquivo `.whl`, é um formato de distribuição de pacotes Python. Um ZIP de implantação do Hub é um pacote de arquivos e manifesto para transferência; não deve ser presumido uma wheel instalável por `pip`.

Uma **Git folder** organiza uma cópia versionada no workspace. Ela não garante, sozinha, que skills estejam no escopo de descoberta escolhido nem que todo job use aquele checkout. Distribuição de código, descoberta de skills e instalação de dependências são decisões separadas.

<a id="genie"></a>
## 13. Como a Genie Code recebe contexto e usa o Hub

### 13.1. Conversa não é memória ilimitada nem treinamento do modelo

A Genie Code utiliza contexto disponível para responder e executar tarefas conforme suas ferramentas e permissões. Esse contexto pode incluir a conversa, código, recursos selecionados, instruções e skills. Disponibilizar um arquivo como contexto não significa treinar permanentemente o modelo com ele.

Um **token** é uma unidade usada pelo modelo para processar texto e outros conteúdos. A **janela de contexto** limita o que pode ser considerado em uma interação. Anexar todos os arquivos indiscriminadamente pode aumentar ruído em vez de resolver a ambiguidade.

Para uma tarefa específica, o melhor contexto costuma ser o objetivo, a origem autorizada, o schema, o grão, as regras de tempo, o método relevante e as interfaces que serão usadas. O manual completo é referência; não precisa ser colado inteiro em todo pedido.

### 13.2. Instruções persistentes e skills especializadas

Instruções pessoais usam `.assistant_instructions.md`; instruções de workspace têm escopo administrado. A plataforma também documenta descoberta hierárquica de `AGENTS.md` e `CLAUDE.md` a partir do arquivo aberto. As instruções têm exceções de aplicação, incluindo Quick Fix e Autocomplete, segundo a documentação consultada. [S08](#fonte-s08)

Uma **Agent Skill** contém `SKILL.md` em pasta própria, com **frontmatter**: metadados YAML delimitados por `---` no início. `name` identifica a skill; `description` ajuda a indicar quando usá-la. O corpo descreve o procedimento e pode referenciar templates e scripts. O padrão aberto e a implementação da plataforma devem ser distinguidos das escolhas específicas deste Hub. [S09](#fonte-s09); [S20](#fonte-s20)

As skills podem ter escopo de usuário, em `/Users/<username>/.assistant/skills/`, ou de workspace, no local administrado documentado pela plataforma. A Genie Code pode carregá-las por relevância ou por seleção explícita com `@`. **Selecionar `@hub-ml-eda-profissional` escolhe um método; não equivale a passar os argumentos de uma função Python.**

### 13.3. Descobrir, propor, executar e aceitar

**Descobrir** significa identificar um recurso relevante. **Propor** significa formular passos ou código. **Executar** significa usar uma ferramenta ou rodar código. **Aceitar** significa avaliar o que ocorreu contra o objetivo e os critérios combinados.

A presença de uma skill não executa automaticamente seus helpers. Entretanto, também seria incorreto dizer que “a Genie Code nunca executa código”: a plataforma oferece ferramentas de execução e políticas de aprovação. Uma skill pode orientar o agente a usar scripts disponíveis. As permissões e aprovações continuam determinando o que pode ser feito. [S09](#fonte-s09); [S21](#fonte-s21)

Um pedido inicial adequado seria: “Use a skill de EDA para propor um diagnóstico, sem executar código nem gravar tabelas. Considere somente a célula sintética anexada. Se faltar schema ou chave, pergunte”. A frase define modo e escopo, mas não substitui controles técnicos de acesso.

### 13.4. Como saber se a skill foi realmente carregada

Uma resposta que se parece com o método não prova, sozinha, o carregamento de determinado arquivo. Para testar o **roteamento**, use pedidos positivos, negativos e seleção explícita e examine a evidência de recurso carregado disponibilizada pela interface. Para testar a **qualidade**, avalie o conteúdo da resposta e, quando houver código, sua execução.

Depois de editar e publicar uma skill, use conversa nova conforme a orientação da plataforma; atualize a interface quando necessário. Isso não publica uma versão ainda presa no Git. Antes de investigar cache, confirme qual conteúdo existe efetivamente no workspace.

### 13.5. O que não deve ser presumido

Os diretórios `hub_prompts`, `hub_snippets` e `hub_padroes` não se tornam mecanismos nativos de descoberta apenas pelo nome. Um briefing precisa ser fornecido; um helper precisa estar importável e ser chamado; um molde precisa ser consultado.

Aliases de texto como `/eda` não devem ser apresentados como comandos customizados registrados sem um mecanismo comprovado. O projeto também não implementa uma memória própria de todas as sessões nem um hook pós-resposta apenas por organizar arquivos.

**MCP**, explicado no capítulo de integrações, é outro mecanismo: conecta ferramentas e fontes. Uma skill não é um servidor MCP. Termos de outras experiências Genie voltadas a perguntas de negócio não devem ser usados como sinônimos automáticos de Genie Code. O destinatário deste pacote é a experiência de código, e a disponibilidade de cada produto precisa ser conferida no workspace.

### Outras experiências com o nome Genie

Genie Code é o destinatário deste Hub. Genie One é uma interface de consumo de dados para públicos de negócio; Genie Agents são ambientes de domínio preparados com dados e semântica. Uma Agent Skill da Genie Code não é, por isso, um Genie Agent. O nome compartilhado não torna suas configurações e APIs intercambiáveis. [S36](#fonte-s36)

<a id="visuais"></a>
## 14. Widgets, cards, gráficos e imagens: o que cada um realmente faz

### 14.1. “Widget” pode descrever coisas diferentes

No uso cotidiano, widget pode significar qualquer componente visual da página. No Databricks, `dbutils.widgets` é uma interface específica para parâmetros de notebook, como caixas de texto e listas de opções. Esses widgets recebem valores, normalmente como strings; o código precisa converter e validar quando espera números ou datas. [S16](#fonte-s16)

Um card HTML do Hub, uma imagem PNG no README e um parâmetro `dbutils.widgets` não têm o mesmo mecanismo. Um componente visual existente não deve ser presumido conectado em tempo real a uma tabela ou a um job.

Exemplo conceitual de widget nativo, **não necessário para usar o manual e não aplicado aos widgets já escolhidos**:

```python
# Código para notebook Databricks; cria um parâmetro na interface.
dbutils.widgets.text("limite_linhas", "100", "Limite de linhas")
limite = int(dbutils.widgets.get("limite_linhas"))
if not 1 <= limite <= 1000:
    raise ValueError("Escolha um limite entre 1 e 1000.")
```

O texto `"100"` precisa virar inteiro. A validação restringe o parâmetro, mas não prova que qualquer consulta com `limit(100)` será barata nem concede permissão de leitura.

### 14.2. HTML, CSS, Markdown e Plotly

**Markdown** é a marcação leve de títulos, links, tabelas e blocos de código. **HTML** descreve elementos de página. **CSS** define apresentação, como cor e espaçamento. Helpers de `visual/` podem produzir HTML ou Markdown; eles não necessariamente exibem a saída por conta própria.

**Plotly** representa gráficos que podem ter interatividade quando exibidos por uma superfície compatível. Uma figura pode existir como objeto Python antes de aparecer na tela. Exportá-la como imagem elimina comportamentos interativos e congela aquele estado.

Um badge de `pass`, `warn` ou `fail` apenas apresenta um valor calculado ou fornecido. Ele não implementa automaticamente a regra de parada de um pipeline. Cores e ícones são auxiliares: texto, unidade, denominador e origem precisam continuar legíveis.

### 14.3. PNGs e fontes visuais do projeto

Os recursos compartilhados ficam em `hub_readmes_visual_assets/`. Um PNG é uma imagem raster, formada por pixels; SVG descreve elementos vetoriais. Fontes de composição, metadados e manifestos permitem rastrear a geração de imagens aprovadas. Um hash identifica bytes; não avalia beleza ou clareza.

Uma imagem em um README usa um caminho em relação àquele documento. Copiar o Markdown para outra pasta pode quebrar a referência mesmo que o PNG continue existindo. A documentação Databricks admite imagens de workspace em células Markdown, mas a resolução do arquivo e a aparência precisam ser conferidas na superfície de uso. [S22](#fonte-s22)

O cabeçalho CRM e o cabeçalho Squad têm papéis definidos pelo projeto. Este manual não muda essas escolhas, não substitui figuras existentes e não transforma recursos visuais em execução. A página pode permanecer visualmente idêntica enquanto a documentação técnica é consolidada.

<a id="qualidade"></a>
## 15. Exemplo completo: da base sintética ao diagnóstico de qualidade

### 15.1. Pergunta e preparação

A pergunta será: “Esta base sintética tem chave de evento utilizável e nulos que precisam de atenção?”. O objetivo não é avaliar uma campanha real nem concluir se um modelo deve entrar em produção.

Prepare primeiro a importação do Hub conforme o capítulo 7. Execute os blocos abaixo em um notebook com sessão Spark disponível. Eles criam dados sintéticos e uma view temporária da sessão, sem gravar uma tabela permanente.

```python
# EXEMPLO: qualidade_preparo
from datetime import date, timedelta
from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
linhas = [
    (f"e{i:02d}", f"c{i % 5:02d}", date(2026, 6, 1) + timedelta(days=i),
     None if i == 0 else "email", i % 2, float(i))
    for i in range(20)
]
schema = (
    "event_id STRING, id_cliente STRING, dt_evento DATE, "
    "canal STRING, respondeu INT, valor_gasto DOUBLE"
)
df = spark.createDataFrame(linhas, schema=schema)
df.createOrReplaceTempView("vw_manual_campanha_sintetica")
```

`range(20)` gera os índices de zero a dezenove. `event_id` fica único porque incorpora o índice. `i % 5` repete cinco clientes; isso ajuda a distinguir entidade de evento. `timedelta(days=i)` avança a data. Há exatamente um `None` em `canal`, no primeiro evento. `i % 2` alterna o indicador entre zero e um.

O schema declara os tipos para que o exemplo não dependa de inferência. A última chamada dá um nome temporário à base para que o script possa encontrá-la na mesma sessão. O nome é exclusivo do tutorial, mas `createOrReplaceTempView` substitui uma view temporária de mesmo nome caso você já a tenha criado.

### 15.2. Chamada da API real

```python
# EXEMPLO: qualidade_chamada
from hub_scripts.data_quality_check import data_quality_check

resultado = data_quality_check(
    table_name="vw_manual_campanha_sintetica",
    pk_columns=["event_id"],
    date_column=None,
    thresholds={"null_warn": 5.0, "null_fail": 20.0},
)
```

`table_name` é o recurso lido pelo Spark; não é o caminho de uma pasta. `pk_columns` recebe uma lista, permitindo chave simples ou composta. `date_column=None` desliga somente a verificação opcional de freshness: não remove `dt_evento` da base. `thresholds` informa percentuais, não razões.

A função agrega contagem e nulos e verifica a chave candidata. Isso exige processamento sobre os dados. **Não é uma inspeção sem custo apenas porque retorna um dicionário pequeno.**

### 15.3. Retorno, significado e conferência

A implementação devolve `status`, `score`, `thresholds`, `checks` e `alerts`. Ela não oferece uma chave superior `metrics`. Para a base construída, as expectativas verificáveis são:

```python
# EXEMPLO: qualidade_conferencia
assert resultado["status"] == "warn"
assert resultado["score"] == 95
assert resultado["checks"]["row_count"] == 20
assert resultado["checks"]["pk_uniqueness"]["duplicate_rows"] == 0
assert resultado["checks"]["pk_uniqueness"]["null_key_rows"] == 0
assert resultado["checks"]["nulls"]["canal"]["count"] == 1
assert resultado["checks"]["nulls"]["canal"]["pct"] == 5.0
assert "freshness" not in resultado["checks"]

for alerta in resultado["alerts"]:
    print(alerta["check"], alerta.get("column"),
          alerta["severity"], alerta["message"])
```

A proporção é `1 / 20 × 100 = 5%`. Como a comparação usa `>=`, alcançar 5% já gera aviso. Não há duplicatas nem nulos na chave. O score parte de 100, subtrai 5 por alerta de aviso e 25 por alerta de falha, com piso zero. Um único aviso produz 95.

**95 não significa 95% de probabilidade de a base estar correta.** É um índice local, derivado dos alertas implementados. Também não significa que todas as regras de negócio foram testadas. Uma base vazia ou uma coluna cheia de textos vazios exige atenção além dessa interpretação: o helper não contém toda regra possível de qualidade e não substitui um teste explícito de população mínima.

O campo `column` do alerta identifica a coluna quando a verificação é específica por coluna. `alerta.get("column")` evita presumir que todos os tipos de alerta tenham esse campo. A mensagem não precisa repetir o nome da coluna.

### 15.4. Diagnóstico não é bloqueio automático

O helper relata o problema. O código consumidor decide como reagir:

```python
# EXEMPLO: politica_consumidor
if resultado["checks"]["row_count"] == 0:
    raise ValueError("Base vazia: a análise não deve continuar.")
if resultado["status"] == "fail":
    raise RuntimeError("Qualidade reprovada: examine os alertas antes de continuar.")
```

Essa política é um exemplo explícito do consumidor. Um retorno `"fail"` não necessariamente lança exceção sozinho. E um `"warn"` não autoriza automaticamente ignorar a coluna: a decisão depende do uso pretendido.

### 15.5. Freshness em um cenário separado

**Freshness** mede atualidade. Neste helper, a verificação opcional usa a data corrente do processo Python e o maior valor observado na coluna indicada. O limite é excedido quando a idade é maior que `freshness_days`. Uma coluna sem data válida também pode reprovar a verificação.

O teste de nulidade acima foi isolado do calendário para não mudar de resultado apenas porque o leitor executou o manual em outro mês. Ao adicionar freshness, registre a data da execução, a data máxima observada e o limiar usado. Não crie no exemplo um parâmetro `reference_date` que a função não recebe.

Uma data futura pode exigir uma regra de plausibilidade adicional: “não está velha” não equivale a “é uma data válida para o negócio”. Esse é um bom exemplo de por que conhecer a implementação melhora a interpretação de um sinal verde.

<a id="tempo"></a>
## 16. Tempo, junções e vazamento de informação

### 16.1. O problema de usar o futuro sem perceber

**Leakage**, ou vazamento de informação, ocorre quando a análise utiliza algo que não estaria disponível no instante da decisão que pretende simular. Pode ser uma variável produzida depois do evento, uma transformação ajustada com dados de teste ou uma versão de cadastro publicada posteriormente.

Imagine uma decisão tomada em 10 de junho. Um atributo se refere a 8 de junho, mas só foi publicado em 12 de junho. A data de referência parece anterior; a disponibilidade é posterior. Usá-lo como informação conhecida em 10 de junho produz uma simulação irreal.

Evitar leakage não se resume a ordenar datas. É necessário definir o instante da decisão, a disponibilidade das fontes, a janela de features e o horizonte do target. O período de maturação do rótulo também importa: um evento que precisa de noventa dias para ser observado não está completo no dia seguinte.

### 16.2. Join, cardinalidade e multiplicação de linhas

Um **join** combina bases a partir de chaves e condições. A **cardinalidade da relação** descreve se cada linha encontra uma, várias ou nenhuma correspondência. Em um relacionamento muitos-para-muitos, o número de linhas pode crescer muito.

Se uma linha de cliente encontra três linhas no cadastro utilizado à direita, valores associados à esquerda podem aparecer três vezes. Uma soma posterior pode triplicar sem que o código apresente erro. `dropDuplicates()` ao final não é uma correção universal: pode esconder um grão mal definido e eliminar fatos legítimos.

`diagnosticar_join` ajuda a examinar essa relação antes da junção final. O **fator de expansão** compara as linhas esperadas/obtidas após a relação com a base de referência. Um valor maior que um requer interpretação; não é automaticamente um defeito se o grão pretendido realmente mudou.

### 16.3. Point-in-time e `pit_join`

Uma junção **point-in-time**, também chamada *as-of* nesse contexto, escolhe a versão de uma feature elegível no instante de cada decisão. O `pit_join` do projeto exige `atraso_publicacao_dias`, permite limitar a idade da referência e trata empates de forma explícita.

Ele retorna uma tupla `(df, diagnostico)`. O DataFrame preserva as linhas de fatos e acrescenta as features elegíveis; se não houver versão válida, os atributos correspondentes ficam nulos. O diagnóstico diferencia motivos, como chave nula, entidade sem histórico e histórico indisponível na data. Não trate todos esses casos como uma única falta de cadastro.

A política padrão de empate é erro. As alternativas precisam ser escolhidas conscientemente; resolver por maior ou menor valor não transforma uma duplicação de origem em informação correta. E a janela máxima é medida segundo o contrato da implementação, não segundo uma interpretação livre da palavra “janela”.

### 16.4. Split temporal, gap e walk-forward

**Treino** ajusta o modelo. **Validação** orienta escolhas e hiperparâmetros. **Teste** avalia uma configuração que não deveria continuar sendo ajustada com base naquele resultado. Em problemas temporais, essas populações precisam reproduzir a relação passado/futuro pretendida.

`temporal_split` trabalha com pandas e separa períodos de calendário. `gap_periods` reserva intervalos entre partes. `period_unit="M"` usa períodos mensais; não significa trinta dias fixos. Os percentuais se aplicam à seleção de períodos, e o número de linhas em cada parte pode ter proporções diferentes.

```python
# EXEMPLO: split_temporal
import pandas as pd
from hub_snippets.ml.split_temporal import temporal_split

base = pd.DataFrame({
    "dt_evento": pd.date_range("2025-01-01", periods=12, freq="MS"),
    "valor": range(12),
})
treino, validacao, teste = temporal_split(
    base, date_col="dt_evento", train_pct=0.5, val_pct=0.25,
    gap_periods=1, period_unit="M",
)
assert (len(treino), len(validacao), len(teste)) == (6, 3, 1)
assert treino["dt_evento"].max().month == 6
assert validacao["dt_evento"].min().month == 8
assert teste["dt_evento"].min().month == 12
```

Os seis primeiros meses ficam no treino. Julho é gap. Agosto a outubro ficam na validação. Novembro é outro gap, e dezembro fica no teste. As duas linhas dos gaps não aparecem nos três retornos.

`group_col` ativa uma política conservadora para separar entidades entre partições, removendo linhas conforme o contrato. Isso pode esvaziar validação ou teste e não deve ser aplicado indiscriminadamente a séries em painel nas quais acompanhar a mesma entidade no futuro é parte legítima da tarefa.

**Walk-forward** repete avaliações que avançam no tempo. O `walk_forward_cv` recebe uma função de treinamento e avaliação — um **callback**, isto é, código fornecido para ser chamado em cada janela. Ele não sabe, por si só, como treinar todo modelo possível.

Dividir por índices de linhas não produz leakage inevitavelmente: há métodos temporais legítimos que trabalham com índices ordenados. O benefício dos helpers do Hub é explicitar períodos, gaps e critérios; não provar que qualquer alternativa seria incorreta. [S23](#fonte-s23)

<a id="rfv"></a>
## 17. RFV: uma transformação de dados, não um veredito de qualidade

**RFV**, ou RFM em inglês, reúne recência, frequência e valor. Recência mede há quanto tempo ocorreu o último evento considerado. Frequência conta eventos elegíveis. Valor agrega a medida monetária ou outra medida definida no contrato de entrada.

O `rfv_calculator` recebe um nome de tabela, colunas de cliente/data/valor, uma data de referência e períodos em dias. Ele remove datas nulas após conversão, considera eventos até a data de referência inclusive e produz features por cliente. Não atribui automaticamente quintis, notas de um a cinco ou segmentos como “VIP”.

Para uma janela de trinta dias, o intervalo inclui a referência e os vinte e nove dias anteriores. Isso evita a ambiguidade de chamar de “trinta dias” um intervalo com trinta e uma datas. Eventos futuros são excluídos da construção; clientes com apenas eventos futuros não são necessariamente recuperados como linhas vazias. Caso o objetivo exija incluir clientes sem transações, será necessária uma base-mestra e uma junção explicitamente planejada.

Um exemplo simples: na referência de 30 de junho, um cliente comprou em 25 de junho e em 29 de junho, por 40 e 60 unidades monetárias. A recência será um dia; a frequência total considerada, dois; e o valor total, cem. Uma compra em 2 de julho não entra nessa avaliação. Esse cálculo ilustra a regra; o schema de saída completo deve ser conferido no helper e no notebook de exemplo.

Escolher “evento” também é decisão de negócio. Uma linha pode representar uma compra, um item de compra ou uma tentativa de contato. Sem acertar o grão, a frequência pode contar itens ou tentativas em vez de transações.

<a id="estatistica"></a>
## 18. Estatística para interpretar o que os helpers calculam

### 18.1. EDA, distribuição e amostra

**EDA** é análise exploratória de dados: conhecer variáveis, cobertura, distribuições, relações e problemas antes de concluir ou modelar. Uma **distribuição** descreve como os valores se espalham. A média resume uma dimensão; não substitui quantis, caudas, proporções de nulos ou mudanças de composição.

Uma **amostra** é um subconjunto da população. Uma estimativa na amostra não deve ser rotulada como contagem exata da população. **Seed** é uma semente para mecanismos aleatórios; ajuda a reproduzir escolhas sob condições comparáveis, mas não oferece identidade bit a bit entre todos os runtimes, versões e planos distribuídos.

O `quick_profile` calcula contagens e nulos na tabela completa e usa amostra para outras estatísticas, como cardinalidade e valores frequentes. O retorno identifica essa procedência. `sample_fraction=0.1` é uma fração esperada, não um teto universal de linhas. Não troque uma métrica amostral por uma afirmação sobre todos os clientes.

### 18.2. Correlação, associação e causalidade

Uma correlação mede associação sob uma definição específica. Ela não demonstra que alterar uma variável provocará uma mudança em outra. Um canal de campanha pode ter maior resposta porque recebeu clientes mais propensos, não porque o canal causou todo o ganho observado.

O heatmap é uma apresentação das relações calculadas. Ele não corrige seleção de amostra, variáveis omitidas, desenho de experimento ou definição do target. Uma descoberta exploratória pode orientar investigação; não deve ser apresentada como efeito causal sem um desenho que sustente essa interpretação.

### 18.3. Drift, PSI e CSI

**Drift** é mudança. Pode ocorrer na distribuição das entradas, das previsões ou na relação entre entradas e resultado. Uma mudança de distribuição não prova automaticamente perda de performance; ela é um sinal a investigar.

O **PSI** compara proporções em grupos/faixas comuns. Em sua forma usual, soma `(p_i - q_i) × ln(p_i / q_i)`, com convenções de suavização quando há proporções zero. A escolha das faixas deve permitir comparar a mesma definição entre referência e população nova. Recriar faixas independentes em cada período pode ocultar a mudança.

No projeto, há implementações para entradas locais e Spark. **CSI** aplica a ideia de estabilidade a características/variáveis. Não confunda CSI com `sys.path` nem com CI de integração contínua. A base matemática e o tratamento de categorias/faixas precisam ser lidos no helper escolhido; o nome semelhante não torna todos os contratos intercambiáveis.

Um PSI igual a zero ocorre quando as proporções comparadas são iguais sob aquela discretização. Isso não demonstra que todas as propriedades das populações sejam idênticas. Limiar de alerta é política de monitoramento, não lei estatística universal nem regra obrigatória da Databricks.

`drift_detector` desta versão aceita o método `"psi"`; não presuma que uma string `"ks"` fará o script trocar de algoritmo. Helpers específicos oferecem outros cálculos, com interfaces próprias.

### 18.4. KS em dois contextos

O **KS** pode aparecer como distância entre distribuições, com uso em diagnóstico de mudança, ou como métrica de separação de scores entre classes. É necessário identificar as populações comparadas e o tipo de resultado retornado.

Um p-valor de teste não é a probabilidade de a hipótese ser verdadeira nem mede sozinho a relevância operacional. Com muitas observações, diferenças pequenas podem ser estatisticamente detectáveis. Com poucas observações, uma diferença relevante pode ser estimada com grande incerteza.

### 18.5. WOE, IV e scorecard

**WOE**, peso de evidência, transforma grupos de uma variável segundo sua relação com classes do target. **IV**, Information Value, resume separação sob a construção utilizada. Essas estatísticas dependem da definição da classe positiva, dos grupos e do tratamento de zeros.

Calcular WOE com todo o conjunto, incluindo dados reservados para teste, pode transmitir informação do target para o treinamento. O ajuste das regras deve respeitar a separação de populações. Um IV alto também pode indicar uma variável produzida depois do evento, e não uma excelente feature disponível em produção.

Um **scorecard** converte contribuições em uma escala de pontos segundo uma convenção. Não é a mesma coisa que o score de qualidade do `data_quality_check`, nem uma pontuação regulatória reconhecida apenas por ter esse nome.

### 18.6. Intervalo de confiança, Wilson e `decidivel`

Uma taxa observada em amostra pequena tem incerteza. O exemplar `taxa_resposta_campanha` retorna taxa percentual por segmento e um intervalo de Wilson, além de uma indicação local `decidivel` baseada no mínimo configurado de contatos.

Com duas respostas em dez contatos, a taxa é 20%. Com `z=1.96`, os limites de Wilson ficam aproximadamente em 5,67% e 50,98%. A amplitude calculada antes do arredondamento é aproximadamente 45,32 pontos percentuais. A distância entre os limites já arredondados pode diferir no centésimo por causa do arredondamento.

O mínimo padrão de cem contatos faz `decidivel` ser falso nesse caso. **Ter `decidivel=True` não certifica um experimento, uma decisão causal ou uma aprovação de negócio.** É uma regra local de tamanho de amostra, e as demais condições continuam necessárias.

**Odds** são uma razão entre probabilidades complementares, com orientação que precisa ser declarada (evento/não evento ou a inversa). **PDO**, points to double the odds, define quantos pontos correspondem a dobrar essa razão na escala do scorecard. Base de pontos e odds de referência são escolhas de calibração da escala; não são coeficientes estimados pelo helper.

### 18.7. Safra, vintage e MOB

Uma **safra** agrupa originações de um mesmo período. **Vintage** é o termo frequente em inglês. **MOB**, *months on book*, alinha o tempo decorrido desde a originação. Comparar uma safra com doze meses de observação a outra com apenas dois meses sem ajustar maturidade pode criar uma conclusão enganosa.

Os helpers de vintage organizam curvas e comparações; a definição de evento, denominador, unidade temporal e safras incompletas permanece parte do briefing. Um gráfico bonito não resolve uma comparação entre populações que ainda não amadureceram de forma comparável.


### 18.8. Pressupostos, magnitude e vários testes

Uma **hipótese nula** expressa a referência examinada por um teste. **Nível de significância** define uma regra de decisão sob o desenho; **poder** diz respeito à chance de detectar uma alternativa especificada sob certas condições. **Tamanho de efeito** descreve a magnitude, que precisa ser interpretada na unidade do problema. Significância e importância econômica não são sinônimos.

Normalidade se refere a uma distribuição específica, frequentemente a dos erros em um modelo, não a uma exigência de que todas as colunas sejam normais. Homocedasticidade descreve variância de erros constante sob o modelo; heterocedasticidade exige tratamento adequado à inferência pretendida. VIF é um diagnóstico de associação linear entre regressores, não uma ordem automática de excluir variáveis. Em séries, ADF e KPSS examinam hipóteses diferentes sobre raiz unitária/estacionariedade; um nome de teste no briefing não dispensa compreender sua hipótese.

Quando muitos testes são feitos, uma coleção de p-valores pequenos pode conter descobertas ocasionais. O plano deve explicitar multiplicidade, dependência entre observações, tamanho amostral e forma de seleção. Essas definições esclarecem os termos presentes em `hub-ml-validacao-estatistica`; o Hub não possui um wrapper universal que valide todos esses pressupostos para qualquer modelo.

<a id="modelos"></a>
## 19. O que significa treinar um modelo neste projeto

### 19.1. Feature, target, treino e inferência

Uma **feature** é uma informação usada como entrada: quantidade de contatos anteriores, recência da última compra ou canal utilizado. O **target**, também chamado de variável-alvo ou rótulo, é o resultado que o modelo tenta aprender, como uma resposta à campanha. `X` costuma representar as entradas; `y`, os resultados conhecidos. Essas letras não são comandos especiais: são convenções de nomes.

**Treinar**, normalmente por `fit`, ajusta parâmetros a exemplos observados. **Inferir**, por métodos como `predict` ou `predict_proba`, aplica um modelo já ajustado a novas entradas. Uma função que calcula a proporção de respostas não precisa treinar modelo. Uma função chamada `train_lightgbm_baseline`, por outro lado, efetivamente ajusta um estimador quando executada; importá-la apenas disponibiliza sua definição.

Classificação prevê categorias; regressão prevê uma quantidade; ranking ordena candidatos dentro de grupos de comparação. Séries temporais exigem atenção à ordem e ao horizonte. Sobrevivência estuda o tempo até um evento, incluindo observações cujo evento ainda não ocorreu. Agrupamento e detecção de anomalias podem operar sem uma resposta-alvo supervisionada. O inventário do capítulo 27 indica as implementações disponíveis; não é necessário usar todas em uma análise.

### 19.2. O que é um baseline

Baseline é uma referência inicial de desempenho e complexidade. Pode ser uma regra simples, uma previsão constante ou um modelo já conhecido. Seu papel é responder: o acréscimo de complexidade melhorou algo relevante sob a mesma avaliação?

O nome `baseline` em um helper não significa que seu resultado esteja aprovado para produção. Nos wrappers do Hub, significa uma forma padronizada de iniciar o ajuste. Antes de comparar resultados, mantenha população, target, data de corte e separação de treino/validação/teste compatíveis. Dois números calculados em universos diferentes não formam uma comparação controlada.

### 19.3. Parâmetro e hiperparâmetro

Em Python, parâmetro é um nome na assinatura de uma função. Em modelagem, a mesma palavra também descreve valores aprendidos, como coeficientes. **Hiperparâmetro** é uma escolha de configuração, como profundidade da árvore, taxa de aprendizagem ou número de épocas. `params_override` nos wrappers permite substituir configurações; não torna qualquer combinação automaticamente adequada.

**Regularização** restringe a flexibilidade para reduzir ajuste excessivo. **Overfitting** é aprender particularidades que não se sustentam fora do treino. **Early stopping** interrompe o ajuste quando uma avaliação de validação deixa de melhorar segundo a regra configurada. Não deve acompanhar repetidamente o teste final: usá-lo para escolher o treinamento consome sua independência.

**Seed** controla fontes de aleatoriedade conhecidas. Não é garantia universal de igualdade bit a bit entre hardware, versões, distribuição dos dados e algoritmos paralelos.

### 19.4. Famílias que aparecem nos nomes dos helpers

`train_lgbm`, `train_xgboost` e `train_catboost` encapsulam bibliotecas de árvores com boosting: modelos construídos sequencialmente para melhorar uma função objetivo. Seus parâmetros e formatos não são intercambiáveis. Um wrapper simplifica a chamada de uma biblioteca; não elimina a necessidade de compreender o algoritmo, o tipo de target e o contrato de entrada.

`mlp_embeddings` combina entradas numéricas e representações aprendidas para categorias. Um embedding é um vetor que representa uma categoria; não é, por definição, uma chamada a uma API de LLM. `autoencoder_anomaly` aprende reconstruções a partir do conjunto apresentado como normal. Erro de reconstrução elevado pode sinalizar diferença, mas não prova fraude. `tabnet_wrapper` oferece outra família de rede para dados tabulares. Mais camadas ou mais parâmetros não significam maior valor para o problema.

`isolation_forest` identifica observações que se isolam de maneira diferente no espaço de atributos. `clustering_suite` agrupa observações e pode apoiar a escolha do número de grupos. `cluster_profiling` ajuda a descrever esses grupos. Nomear um cluster como “alto potencial” é interpretação de negócio posterior; não é um fato produzido automaticamente pelo algoritmo.

`arima_wrapper` e `prophet_wrapper` atendem previsão temporal. Frequência mensal, horizonte de doze períodos e sazonalidade anual são escolhas distintas. Um mês sem observação não deve ser tratado inadvertidamente como se nunca tivesse existido.

`kaplan_meier` e `survival_cox` trabalham com duração e evento. **Censura** significa, por exemplo, que até o fechamento da observação não se conhece a data do cancelamento. Não é equivalente a afirmar que aquele cliente nunca cancelará. Cox também requer análise dos pressupostos; o projeto oferece uma função de verificação, mas a decisão não se resume à presença da função.

`lgbm_ranker` requer grupos de comparação. Os tamanhos dos grupos e a ordem das linhas devem corresponder. Não confunda o grupo de ranking com uma coluna de segmento arbitrária.

`optuna_lgbm` procura hiperparâmetros mediante múltiplas tentativas, chamadas **trials**. `n_trials=50` significa orçamento de tentativas, não cinquenta modelos obrigatoriamente distintos e concluídos. Timeout, erros e critérios de poda podem afetar a busca. O custo computacional deve ser aprovado antes de dispará-la.

### 19.5. Preparação de dados também aprende

Imputar pela média, padronizar, criar um vocabulário de categorias ou estimar WOE envolve parâmetros derivados dos dados. Esses ajustes devem ser aprendidos no conjunto permitido, normalmente o treino, e aplicados aos demais sem reestimá-los indevidamente.

Uma **pipeline de ML** pode encadear essas transformações e o estimador. Já uma **pipeline de dados** organiza ingestão e transformação; um **job** coordena tarefas. A palavra pipeline é usada para mais de um nível. A skill `hub-ml-pipeline-builder` ajuda a planejar; sua existência não significa que já haja um job agendado no workspace.

### 19.6. O retorno não é sempre apenas o modelo

Os treinadores LightGBM, XGBoost e CatBoost deste snapshot retornam uma tupla com modelo e métricas. Outros objetos retornam dicionários, projeções, importâncias ou limiares. Uma chamada como `modelo = train_...(...)` pode deixar uma tupla na variável `modelo`; tentar `modelo.predict(...)` falhará se não houver desempacotamento adequado.

Leia a assinatura e o exemplo específico. Não suponha que todo wrapper entregue `{"model": ...}` ou que todos aceitem Spark DataFrame. Vários treinadores deste Hub recebem arrays NumPy ou pandas; estar no Databricks não transforma esses algoritmos em treinamento distribuído.

<a id="metricas"></a>
## 20. Métricas: como não dar ao número um significado que ele não tem

### 20.1. Quatro contagens antes das siglas

Em um classificador binário, “positivo” precisa representar um evento definido, como responder à campanha. Verdadeiro positivo é o caso positivo corretamente sinalizado. Falso positivo é sinalizar quem não apresentou o evento. Falso negativo é deixar de sinalizar quem o apresentou. Verdadeiro negativo é o negativo corretamente reconhecido.

Imagine, apenas para ensino, cem contatos: vinte responderam; o modelo sinalizou vinte e cinco, dos quais quinze responderam. Temos 15 verdadeiros positivos, 10 falsos positivos, 5 falsos negativos e 70 verdadeiros negativos. Precisão é `15/25 = 60%`; recall é `15/20 = 75%`; acurácia é `(15+70)/100 = 85%`. Os denominadores explicam por que são medidas diferentes.

O **threshold**, ou limiar, converte um score em decisão. Alterá-lo muda aquelas contagens. A escolha depende de custo, capacidade de atendimento e restrições; `0.5` é um valor padrão comum, não uma regra econômica universal. O helper `calculate_binary_metrics` recebe esse parâmetro. Sua escala de saída deve ser conferida no contrato, não deduzida da presença do símbolo `%` no relatório.

### 20.2. Discriminação, calibração e decisão

ROC AUC resume capacidade de ordenação entre classes ao variar limiares. Não mede diretamente lucro, não define o melhor corte e não prova que uma previsão de 20% corresponda a uma frequência de 20%. Essa última correspondência é uma questão de **calibração**.

KS, no contexto de discriminação binária, compara as distribuições acumuladas de scores dos dois grupos. No retorno de `calculate_binary_metrics`, a chave é `ks_pct` e sua escala é de zero a cem; `auc_roc` usa zero a um. A chave `auc_pr` guarda average precision, não uma promessa de integração trapezoidal da curva PR. O mesmo nome KS aparece em testes de distribuição no monitoramento; não são a mesma pergunta operacional. Gini de discriminação costuma ser derivado de AUC pela relação `2 × AUC − 1`, como no helper de métricas; não é o Gini de desigualdade de renda de uma população.

Curvas Precision–Recall e medidas de lift ajudam a examinar seleção e concentração de eventos. Lift de dois em um recorte significa uma taxa de evento duas vezes a referência escolhida; não significa que a ação comercial causou o dobro de respostas. Para efeito causal, seriam necessários desenho e hipóteses adicionais. O módulo `curves_plotly` devolve figuras a partir de vetores já disponíveis; não treina nem valida a origem desses vetores. [S26](#fonte-s26)

### 20.3. Métricas com código real e dados pequenos

Depois de configurar o caminho do Hub, este exemplo utiliza apenas quatro observações sintéticas. Serve para entender interfaces, não para avaliar um modelo de negócio.

```python
# EXEMPLO: metricas_binarias
import numpy as np
from hub_snippets.ml.metrics_report import calculate_binary_metrics

y_real = np.array([0, 0, 1, 1])
y_score = np.array([0.1, 0.4, 0.35, 0.8])
metricas = calculate_binary_metrics(y_real, y_score, threshold=0.5)
print(metricas)
assert abs(metricas["auc_roc"] - 0.75) < 1e-12
```

`y_real` contém os eventos observados; `y_score` contém scores, não decisões prontas. O terceiro caso é positivo, mas está abaixo do corte. A AUC esperada é 0,75: de quatro pares possíveis entre um positivo e um negativo, três estão ordenados corretamente. Essa interpretação não exige afirmar que o score é uma probabilidade calibrada. Antes de procurar chaves adicionais, confira as efetivamente retornadas na sua versão.

Uma base com apenas uma classe pode tornar determinadas métricas indefinidas. Não converter silenciosamente um valor ausente ou não calculável em zero: “não mensurável” e “desempenho zero” são conclusões diferentes.

### 20.4. Regressão, ranking e monitoramento

MAE resume erros absolutos na unidade da variável. RMSE dá maior peso a erros grandes. R² depende da comparação com uma referência de variação e pode ser negativo fora da amostra. Para valores monetários, contextualize a unidade e o custo econômico dos erros, não apenas a posição na tabela.

MAPE é erro percentual absoluto médio: no helper de regressão, observações com valor real zero são excluídas desse cálculo; se todas forem zero, a medida fica não calculável. Isso deve ser informado junto ao denominador. No ranking, métricas como NDCG dependem de relevância, grupos e posição de corte. Um indicador calculado para os dez primeiros não descreve automaticamente a lista inteira. O módulo `lgbm_ranker` possui sua própria interface de avaliação.

`PerformanceMonitor` compara métricas observadas com uma referência e políticas fornecidas. O significado de melhora depende da métrica: AUC maior pode ser desejável; erro maior, não. A função `selecionar_metricas_do_relatorio` extrai indicadores numéricos segundo o contrato, sem transformar números arbitrários de um relatório em metas de negócio. Monitoração não é um gatilho autorizado de retreino por si só.

### 20.5. SHAP, importância e causalidade

SHAP atribui contribuições a entradas em relação à referência e à saída explicada. `compute_shap` no Hub normaliza resultados e exige atenção à tarefa e ao índice de saída quando há múltiplas saídas. `get_feature_importance_shap` resume magnitudes; as funções de plotagem ajudam a inspecionar padrões e casos individuais.

Importância alta não implica causalidade nem direção uniforme. Uma média de valores absolutos não informa se aumentar uma variável aumenta ou reduz o score. O relatório executivo deve separar interpretação do modelo, associação nos dados e efeito de uma intervenção. Não se deve recomendar alterar um atributo do cliente apenas porque sua contribuição explicativa é alta. O código de `explainability_report` auxilia a redação, mas não substitui essa revisão.

<a id="mlflow"></a>
## 21. MLflow: a memória dos experimentos não é a memória do chat

### 21.1. Experimento, run e artefato

Um **experimento** agrupa execuções relacionadas. Um **run** registra uma tentativa concreta. Parâmetros descrevem configurações; métricas registram resultados numéricos; tags acrescentam metadados; artefatos são arquivos, como modelos e relatórios. **Tracking URI** identifica o serviço ou destino de registro, não a pasta onde o Python procura helpers. O destino deve ser conferido antes de registrar. [S24](#fonte-s24)

Não confunda esse registro com a conversa da Genie Code. Uma resposta no chat não vira um run automaticamente. Tampouco um run garante que o código-fonte, a versão dos dados e todos os documentos necessários foram preservados: isso depende do que foi efetivamente registrado.

### 21.2. Assinatura de modelo não é assinatura de função

A assinatura de uma função descreve como chamá-la em Python. A **assinatura do modelo** descreve entradas e saídas aceitas pelo artefato de ML, incluindo formatos e tipos. Um exemplo de entrada ajuda a documentar e inferir esse contrato. Não é uma chave de API, assinatura digital ou prova criptográfica de aprovação. [S25](#fonte-s25)

O nome e a ordem das features também importam. Um vetor com as dimensões corretas e as colunas trocadas pode produzir uma previsão matematicamente calculável e semanticamente errada. Modelos em produção precisam conservar a mesma preparação compatível com aquela utilizada no treinamento.

### 21.3. O que `run_governado` realmente exige

O helper recebe nome, descrição do dataset, descrição do split e limitações. Recusa esses campos obrigatórios vazios. Ao entrar em `with run_governado(...) as run`, abre um run MLflow e registra tags; o objeto `run` oferece métodos para parâmetros, métricas, modelo e artefato.

O comando `with` organiza a entrada e a saída de um contexto. Neste caso, o encerramento normal verifica pendências. `run.parametros(...)` e `run.metricas(...)` precisam receber dicionários não vazios; `run.modelo(..., exemplo_entrada=...)` marca a presença do exemplo associado à assinatura. Com `exigir_completo=True`, pendências detectadas geram erro ao fechar. Se já ocorreu uma exceção dentro do bloco, não presuma que a checagem final de completude também tenha sido executada. [S30](#fonte-s30)

Há limites que precisam ficar explícitos: a checagem local usa indicadores de chamadas realizadas; não audita se o texto do dataset identifica de fato uma versão recuperável, se as métricas foram calculadas corretamente ou se a assinatura persistida é semanticamente suficiente. `artefato(...)` não está entre os três indicadores de completude cobrados no fechamento. A implementação usa o flavor `mlflow.sklearn`; não é um registrador genérico garantido para qualquer arquitetura de rede.

O helper não desfaz registros anteriores ao detectar uma pendência. Um run incompleto pode deixar artefatos e metadados que precisam ser examinados. Portanto, “deu erro” não significa “nenhuma escrita ocorreu”.

### 21.4. Registro e disponibilização são ações diferentes

Salvar um modelo como artefato, registrá-lo em um catálogo de modelos e colocá-lo em um endpoint de inferência são operações distintas. Um modelo pode estar documentado sem estar atendendo requisições. Também pode existir um endpoint cuja versão já difere do experimento que alguém consultou.

Alguns wrappers do projeto expõem `log_mlflow=True`. Esse argumento pode produzir registros, mas desativá-lo não remove uma dependência importada no topo do módulo nem garante ausência de outras formas de autologging já configuradas na sessão. Confira código, ambiente e permissões. Uma falha observada em uma conta Free e data específicas não é prova de proibição universal de MLflow na edição.

<a id="integracoes"></a>
## 22. APIs remotas, SDK, CLI, autenticação e MCP

### 22.1. O percurso de uma requisição

Considere um programa que quer saber se um arquivo do workspace existe. O programa é o **cliente**; a plataforma oferece um **serviço**; o endereço de uma operação é um **endpoint**. O cliente envia uma requisição com operação, identificação do recurso e credencial adequada. O serviço verifica identidade e autorização e devolve uma resposta, frequentemente estruturada em JSON.

JSON é um formato textual de pares nome–valor e listas. Um dicionário Python não é a API REST; ele pode ser convertido em JSON para transportar dados por uma API. Do mesmo modo, receber JSON não significa que se recebeu um DataFrame Spark.

**HTTP** é o protocolo de requisição e resposta. **HTTPS** adiciona proteção do transporte por TLS. `GET` costuma consultar; `POST` costuma submeter ações ou criações; `PATCH` costuma atualizar parcialmente; `DELETE` costuma excluir. O contrato de cada endpoint determina o efeito concreto. Não se deve adivinhar uma rota alterando palavras em uma URL antiga. [S05](#fonte-s05)

Uma falha HTTP pode indicar autenticação ausente, permissão insuficiente, recurso inexistente, limite de requisições ou problema temporário do serviço. Essa classificação é diferente de `ModuleNotFoundError`, que é uma falha de importação Python. O capítulo 26 reúne os sintomas.

### 22.2. SDK e CLI são duas formas de consumir serviços

Um **SDK** reúne código que facilita chamadas à plataforma. O SDK Python da Databricks oferece objetos como `WorkspaceClient`; métodos traduzem chamadas Python em operações remotas. A **CLI**, interface de linha de comando, oferece comandos de terminal, como operações de workspace. A interface gráfica é uma terceira superfície. Elas podem acessar recursos relacionados, mas uma ação disponível em uma não deve ser presumida idêntica em todas. [S27](#fonte-s27); [S17](#fonte-s17)

Veja uma chamada de consulta ilustrativa. Ela exige o SDK disponível e autenticação autorizada previamente configurada. Não cria conta, não autentica por mágica e não deve ser executada para sondar um ambiente sem autorização.

```python
# Consulta remota ilustrativa; exige autenticação e recurso autorizado.
from databricks.sdk import WorkspaceClient

cliente = WorkspaceClient()
objeto = cliente.workspace.get_status(path="/Users/<username>/.assistant/README.md")
print(objeto.object_type)
```

`WorkspaceClient` é uma classe; `cliente` é a instância configurada; `workspace` organiza operações dessa área; `get_status` consulta metadados; `path` identifica o recurso. A resposta informa o tipo, mas não demonstra que o conteúdo renderiza corretamente nem executa um notebook. A documentação do SDK e da operação deve ser consultada para a versão e o host de destino. [S18](#fonte-s18); [S27](#fonte-s27)

**Este exemplo é inteiramente diferente de** `from hub_snippets.constants.format_br import fmt_pct`. O primeiro usa um cliente de serviço remoto; o segundo carrega código acessível ao interpretador. Se o helper carregado fizer chamadas remotas internamente, esse será outro efeito, a ser verificado em sua implementação.

### 22.3. Identidade, perfil e segredo

**Autenticação** responde “quem está fazendo a chamada?”. **Autorização** responde “essa identidade pode realizar esta ação neste recurso?”. Um token válido não concede acesso a todas as tabelas. Um perfil da CLI seleciona configuração; não é a própria conta nem uma permissão.

OAuth e tokens de acesso são mecanismos de autenticação. Um **service principal** é uma identidade de aplicação usada em automações, não um usuário humano oculto dentro do script. Host, método de autenticação e ambiente precisam corresponder. A plataforma oferece autenticação unificada para ferramentas compatíveis; a escolha concreta deve seguir a política do workspace. [S28](#fonte-s28)

Não cole tokens em `SKILL.md`, no manual, em prompts, células salvas, prints ou comandos que fiquem em histórico. Use os mecanismos de credenciais aprovados. Um placeholder como `<username>` instrui substituição local; não é uma credencial válida. O manual não lista hosts, usuários ou catálogos reais do trabalho.

### 22.4. Por que `expected-host` é importante

O publicador do projeto pode escrever centenas de objetos. A proteção `--expected-host` exige que o destino resolvido corresponda ao host pretendido. Isso reduz a chance de confundir laboratório e trabalho. Ela não transforma a operação em transação atômica, não aprova o conteúdo e não substitui um backup.

O modo de plano do publicador integral não escreve arquivos no remoto, mas resolve a identidade e o destino por ferramentas autenticadas. Não deve ser descrito como comando inteiramente offline. Já o renderer local não precisa de credencial Databricks. Essa diferença explica por que um plano de publicação pode falhar por autenticação mesmo sem `--execute`.

### 22.5. MCP não é um pacote Python escondido

**Model Context Protocol (MCP)** é um protocolo para expor ferramentas e recursos a aplicações de IA. Um servidor MCP pode disponibilizar uma operação que um agente autorizado decide utilizar. Isso não torna todo arquivo Python do Hub uma ferramenta MCP. Também não significa que uma skill crie um servidor ao citar seu nome. [S29](#fonte-s29)

O projeto não deve ser entendido como dependente de um arquivo JSON manual para ativar MCP. A configuração segue a interface e os mecanismos oficialmente suportados no workspace. Arquivos produzidos pela própria configuração podem ser estado operacional; não os apague por não constarem do pacote do Hub. Credenciais de conectores não pertencem ao Git.

### 22.6. Não existe “uma API” única para todo o fluxo

Quando alguém diz “a API não funcionou”, peça que identifique a camada. Foi o contrato de argumentos de `data_quality_check`? A sessão Spark não estava acessível? A API de workspace recusou a credencial? Um endpoint de inferência não respondeu? A ação correta depende dessa localização. Reinstalar um helper não corrige uma ACL; renovar um token não cria uma função ausente no `__init__.py`.

<a id="publicacao"></a>
## 23. Da alteração no Git ao arquivo que aparece no Databricks

### 23.1. Commit, branch e sincronização

**Git** registra versões de arquivos. Um **commit** identifica um conjunto de alterações no histórico; seu SHA funciona como identificador. **Branch** é uma referência móvel para uma linha de trabalho. **Push** envia mudanças ao repositório remoto. **Pull request** propõe integrar uma linha de trabalho em outra. Fazer commit não publica automaticamente os arquivos no Databricks.

Um ambiente pode consumir uma pasta Git sincronizada ou receber arquivos por outra ferramenta. Este projeto possui seu próprio fluxo de renderização e publicação. Portanto, não presuma que “está na `main`” significa “está no workspace” ou que “rodei no workspace” significa “a alteração está no Git”.

### 23.2. O renderer local

O comando abaixo apenas mostra o plano:

```powershell
python tools/render_simulado.py
```

O seguinte **apaga e recria a árvore derivada local** `Novo_Ambiente_Simulado/` a partir de `ambiente_fonte/`:

```powershell
python tools/render_simulado.py --write
```

O renderer copia `.assistant_instructions.md` e a pasta `.assistant/`, excluindo caches locais conhecidos. Gera a estrutura de usuário sanitizada e o aviso `README_GERADO.md`. Não cria workspace, não envia API remota, não inicia Spark e não altera permissões. Qualquer edição manual no derivado pode ser perdida; a autoria deve permanecer na fonte.

O README de `ambiente_fonte/` e o README da raiz Git são documentos de manutenção: não entram nesse plano de cópia. O Manual Técnico de `.assistant/` entra por estar dentro da subárvore publicada. A cópia de leitura da raiz Git não é enviada separadamente.

### 23.3. FILE e NOTEBOOK: a extensão não basta

No workspace, um módulo Python deve permanecer importável como arquivo. Um notebook tem células e metadados de notebook. Ambos podem ser exportados com extensão `.py`, mas um notebook SOURCE possui marcadores, como `# Databricks notebook source`, `# COMMAND ----------` e `# MAGIC`.

As ferramentas do projeto usam esse marcador para classificar. Na publicação, notebooks são importados com formato SOURCE; arquivos de biblioteca precisam continuar FILE. Importar indiscriminadamente todo `.py` como notebook quebra a expectativa de importação. Renomear uma extensão não é uma conversão fiel de objeto. Os formatos de importação/exportação são contratos das operações de workspace. [S17](#fonte-s17)

Também não se deve confundir `RAW` de importação com uma opção universal de exportação. O fluxo escolhido pelas ferramentas diferencia formato solicitado, tipo de objeto e bytes exportados. Leia a implementação antes de substituir comandos de publicação.

### 23.4. Planejar, executar e verificar

Estes comandos são documentação operacional, **não foram executados para publicar este manual**. Substituições de perfil e host só devem ocorrer no ambiente autorizado, sem salvar credenciais no Git.

```powershell
# Resolve o destino e mostra o plano, sem publicar.
python tools/publicar_free.py --profile PERFIL --expected-host https://HOST

# Escreve no laboratório explicitamente conferido.
python tools/publicar_free.py --profile PERFIL --expected-host https://HOST --execute

# Consulta/exporta e compara conteúdo; não publica uma nova versão.
python tools/publicar_free.py --profile PERFIL --expected-host https://HOST --verify --conteudo --relatorio .artifacts/verificacao.json
```

O publicador é específico do fluxo do laboratório. O modo de execução exige destino explícito e confere fonte/espelho antes de enviar. `--verify` e `--execute` não se combinam; `--rapido` é uma conferência reduzida de contagem e não pode representar comparação integral de conteúdo. O JSON de relatório registra a verificação, não a execução de cada análise.

**Exclusão no Git não implica exclusão no workspace.** Se uma publicação anterior enviou o catálogo e o glossário, removê-los da fonte e regenerar o simulado não prova que as cópias remotas desapareceram. O publicador não deve ser tratado como um sincronizador que apaga indiscriminadamente tudo o que sobrou. Qualquer retirada remota exige conferência de escopo, autorização e tratamento explícito. Este trabalho não executa essa retirada no seu workspace.

### 23.5. Manifesto, hash e pacote de implantação

Um **manifesto** relaciona o que pertence ao pacote. Um **hash SHA-256** resume bytes para comparação de integridade: mudar um byte altera o resultado esperado. Igualdade de hashes não prova que a regra de negócio esteja correta, apenas que se está comparando o mesmo conteúdo sob aquele mecanismo.

`tools/bundle_implantacao.py` produz um ZIP do produto derivado com `MANIFEST.json`. O manifesto registra caminhos, tamanhos, hashes, commit e condição do worktree. Um worktree **dirty** possui alterações ainda não commitadas; `--allow-dirty` existe para revisão, não para fingir uma versão imutável de produção.

```powershell
python tools/bundle_implantacao.py --output .artifacts/pacote-revisado.zip
```

Esse ZIP não é uma wheel Python. **Wheel**, geralmente `.whl`, é um formato de distribuição de pacote Python; o ZIP de implantação organiza arquivos do workspace. Descompactar um pacote de workspace não equivale a instalar todas as dependências de sua biblioteca.

### 23.6. Jobs, DAGs e Bundles

Um **job** coordena uma ou mais tarefas. Dependências entre tarefas formam um grafo; quando não há ciclos, chama-se DAG. Uma tarefa pode depender do sucesso de outra, mas retries, agendamento, identidade e políticas precisam ser configurados. Lakeflow Jobs é um recurso da plataforma; não é ativado pela criação de uma pasta `hub_scripts/`. [S31](#fonte-s31)

**Declarative Automation Bundles** é a denominação atual do recurso anteriormente conhecido como Databricks Asset Bundles. Ele descreve recursos como código e apoia implantação organizada. Não confunda esse produto com o `bundle_implantacao.py` local: o nome parecido não significa que o script implemente o recurso nativo. [S32](#fonte-s32)

### 23.7. Mudança segura e rollback

Antes de publicar, delimite objetos, ambiente, identidade e critérios de aceite. Mantenha evidência da versão anterior e da nova. **Rollback** é voltar deliberadamente a uma versão adequada; não é simplesmente executar outra vez um comando que falhou pela metade.

Uma operação pode gravar alguns arquivos e falhar depois. Na dúvida, inspecione o estado e o recibo antes de repetir. **Idempotência** significa que repetir uma operação sob as mesmas condições não acrescenta efeitos indesejados. Não se deve assumir essa propriedade para um job inteiro apenas porque uma das funções é determinística.

<a id="validacao"></a>
## 24. Validação: cada teste responde a uma pergunta diferente

### 24.1. CI não é CSI e não é `sys.path`

**CI**, integração contínua, executa verificações de código e estrutura associadas a mudanças no repositório. **CSI**, discutido no capítulo 18, é uma medida de mudança de distribuição utilizada em monitoramento. **`sys.path`** é a lista de caminhos da importação Python. Nenhum é sinônimo dos outros.

**CD** pode significar entrega ou implantação contínua, conforme o processo. Um repositório ter GitHub Actions não prova que exista implantação automática. Neste snapshot, o gate local é deliberadamente separado de publicação e testes que exigem credenciais.

### 24.2. O que o gate atual executa

```powershell
python tools/ci_local.py --verbose
```

O comando usa o Python local e executa três etapas: validação de `ambiente_fonte/` com conferência das contagens do README; testes de regressão da biblioteca; e testes das ferramentas. Continua pelas etapas para apresentar mais de uma falha, em vez de esconder problemas posteriores.

As dependências desse gate estão em `tools/requirements-dev.txt`. A instalação desse arquivo é uma ação separada. Ele não prepara automaticamente o workspace Databricks nem testa todos os treinadores opcionais.

```powershell
python -m pip install -r tools/requirements-dev.txt
python tools/validate_assistant.py --conferir-readme
```

`python -m pip` vincula o instalador ao interpretador Python escolhido. Evita parte da confusão de ter vários `pip` no computador. Ainda é necessário conferir qual `python` foi resolvido pelo terminal.

### 24.3. AST: ler a estrutura do código sem executá-lo

**AST**, árvore de sintaxe abstrata, representa a estrutura de um programa: funções, argumentos, chamadas e expressões. `ast.parse` pode detectar sintaxe inválida e apoiar verificações de contratos sem iniciar Spark ou importar dependências pesadas.

A ferramenta `tools/api_publica.py` usa estrutura de código para inventariar nomes públicos e apoiar `__init__.py`. Ela não cria endpoints REST. O validador usa AST para examinar módulos e exemplos, mas uma análise estática não prova tipos em execução, acessibilidade de tabelas, correção estatística ou compatibilidade de um serviço remoto.

### 24.4. Teste unitário, regressão, integração e smoke

Um **teste unitário** exercita uma unidade pequena com entradas controladas. Um **teste de regressão** procura impedir que um comportamento corrigido volte a quebrar. **Integração** verifica componentes atuando juntos. **Smoke test** testa operações básicas para revelar falhas amplas de ambiente ou integração; não é validação exaustiva de todos os casos.

O projeto possui ferramentas de smoke Spark/ML e roteiros de teste conversacional. Elas não são equivalentes ao gate offline. Uma simulação ou mock de MLflow testa o código que usa a interface, não a conexão real, a autorização ou a persistência no serviço.

**Skip** indica caso não executado. “A suíte terminou sem falhas, com casos ignorados” não deve ser relatado como se todos tivessem passado em runtime. Registre o que foi executado, a versão, o ambiente e o motivo dos casos ausentes.

### 24.5. Contrato de documentação e limite da evidência

Um link válido demonstra que o destino referenciado existe na verificação; não garante que seu conteúdo esteja correto. Um PNG com hash esperado demonstra integridade; não garante legibilidade. Um bloco de saída presente em Markdown demonstra que foi escrito; não prova sozinho sua execução. Um teste de importação não exercita a função, e uma resposta bem redigida não prova carregamento da skill.

Neste projeto, resultados de validação exibidos no README são confrontados por `--conferir-readme`. Quando um documento é acrescentado ou removido, as contagens podem mudar sem que haja regressão de algoritmo. Devem ser atualizadas a partir da execução, não ajustadas por tentativa até desaparecer o erro.

### 24.6. Como registrar uma evidência útil

Uma evidência deve permitir entender versão, contexto e limite. Registre commit ou versão dos arquivos; ambiente/runtime; comando ou célula; entrada ou recorte; saída observada; critério esperado; resultado da comparação; e o que não foi coberto. Preserve o erro real quando a verificação falhar, removendo apenas informações sensíveis de modo declarado.

Separe quatro estados: **explicação hipotética**, **resultado esperado por cálculo**, **execução observada** e **execução revisada segundo critérios**. Não converta uma simulação em execução real mediante alteração da legenda.

<a id="seguranca"></a>
## 25. Segurança, governança e limites de confiança

### 25.1. Contexto também pode ser dado sensível

Um nome de tabela, schema, trecho de código, resultado exibido ou print pode revelar informações do ambiente. Antes de anexar conteúdo à IA, considere a política de dados, o tipo de recurso e quem poderá consultar aquele material. Retirar o nome de uma pessoa não garante anonimização de um conjunto com combinações identificáveis.

Use dados sintéticos nos exemplos. **Sintético** significa construído para demonstrar um comportamento; não é uma amostra representativa certificada da operação real. Não use um conjunto sintético pequeno para homologar desempenho de negócio.

### 25.2. Privilégio mínimo e aprovação

A identidade deve ter apenas os acessos necessários à tarefa. Um prompt com “somente leitura” é orientação ao agente; o controle efetivo depende também das permissões, ferramentas e aprovações. Autoaprovação reduz interrupções, não constitui uma fronteira de segurança independente. [S19](#fonte-s19); [S21](#fonte-s21)

Uma função de diagnóstico pode fazer ações custosas de leitura, como contagem e agregação. **Não gravar dados não significa não consumir recursos.** Da mesma forma, “só visualizar” pode coletar dados ao driver ou expô-los em uma saída persistida do notebook.

### 25.3. Injeção de prompt e cadeia de dependências

Arquivos, comentários, páginas e resultados de consulta podem conter instruções maliciosas ou inadequadas. O fato de um texto estar no contexto não lhe concede autoridade para alterar objetivo, revelar segredos ou contornar revisão. Conteúdo de terceiros deve ser tratado como dado, não como autorização.

Instalar uma dependência ou importar um módulo pode executar código. Verifique procedência, versão e mecanismo de instalação. O `sys.path.insert(0, ...)` prioriza a pasta indicada; um arquivo malicioso com nome de biblioteca conhecida pode sombrear o pacote legítimo. Não adicione diretórios arbitrários recebidos em uma resposta de IA.

### 25.4. “Fail-closed” não é uma propriedade de todos os arquivos

**Fail-closed** significa impedir a ação quando não se conseguem provar as condições necessárias. Algumas ferramentas de publicação recusam destinos inesperados ou divergências entre fonte e espelho. Isso não torna toda função do Hub automaticamente fail-closed: `data_quality_check`, por exemplo, devolve diagnóstico; cabe ao consumidor definir a interrupção.

Também não confunda status de CI, score de qualidade de dados, aprovação humana e autorização de implantação. São decisões diferentes, com responsáveis e evidências diferentes.

<a id="erros"></a>
## 26. Diagnóstico: ler o erro antes de tentar uma solução

### 26.1. Como ler um traceback

O **traceback** mostra a sequência de chamadas que levou à falha. Comece pelo tipo de exceção e pela mensagem final, depois localize o arquivo e a linha do seu código que iniciou o problema. A última biblioteca citada pode ser apenas onde a inconsistência apareceu; a origem pode estar em um argumento incorreto várias chamadas antes.

Registre a mensagem exata, sem tokens ou dados sensíveis. “Não funcionou” não informa se falhou a importação, a leitura, o cálculo, a renderização ou a publicação. Evite instalar várias bibliotecas ao acaso: isso muda o ambiente e dificulta identificar a causa.

| Sintoma | Significado provável | Primeira conferência |
|---|---|---|
| `ModuleNotFoundError: hub_snippets` | Raiz do pacote não foi encontrada | Localização de `.assistant`, existência da pasta e `sys.path` da sessão |
| `ModuleNotFoundError` com outra biblioteca | Dependência do módulo está ausente | Nome importável, pacote correspondente e etapa `imp`/`exec` |
| `ImportError: cannot import name` | Nome não exportado, versão diferente ou importação circular | `__init__.py`, API real e `__file__` do módulo carregado |
| `NameError: spark` ou `df` | Variável não definida nessa sessão | Preparação executada e ordem das células |
| `TypeError: unexpected keyword argument` | Argumento não pertence à assinatura | `inspect.signature` da função da versão carregada |
| `TypeError` por argumento ausente | Faltou parâmetro obrigatório | Assinatura; `Optional` não implica valor padrão |
| `KeyError: metrics` ao ler DQ | Chave presumida não existe no retorno | Use `checks`; examine `resultado.keys()` |
| `AttributeError` ao chamar método | O objeto é de outro tipo ou API | `type(objeto)`; tuple versus modelo, pandas versus Spark |
| Erro de tabela/view não encontrada | Nome, contexto SQL ou sessão incorretos | Nome qualificado; criação e duração da view temporária |
| Erro de coluna não resolvida | Coluna ausente/ambígua ou schema diferente | `df.printSchema()` e aliases da junção |
| HTTP 401 | Autenticação rejeitada/ausente | Perfil, método e validade da credencial, sem imprimi-la |
| HTTP 403 | Ação não permitida | Identidade efetiva, ACL e política do serviço |
| HTTP 404 | Recurso ou rota não resolvidos, eventualmente acesso ocultado | Host, caminho e contrato da operação |
| HTTP 429 | Limite de requisições atingido | Ritmo de chamadas e política de espera do serviço |
| Timeout ou falha transitória de rede | Resposta não chegou no prazo | Estado remoto antes de repetir operações com efeitos |
| Memória insuficiente | Dados/objetos excederam capacidade do processo | `collect`, `toPandas`, cardinalidade, número de colunas e plano |
| Método não suportado no serverless | API incompatível com compute/Connect | Documentação atual e alternativa suportada |
| Imagem quebrada | Caminho, permissão, tipo ou publicação incorretos | Local do Markdown e local real do PNG; não o `sys.path` |
| Função continua “antiga” | Módulo/cache/arquivo de outra localização | `__file__`, estado da sessão e reinicialização controlada |
| CI reprova contagens do README | Evidência documental ficou desatualizada | Reexecutar gate e conferir alteração de inventário |

### 26.2. Uma sequência que preserva a capacidade de diagnosticar

Primeiro, identifique a camada. Depois, reproduza com o menor caso sintético que preserva a falha. Confira versão e origem do módulo, parâmetros, schema e permissões. Mude uma hipótese por vez e registre o resultado. Somente após resolver a causa, retorne ao caso maior.

Para uma falha de visualização, não publique novamente todos os helpers. Para uma falha de importação, não altere permissões de tabela sem necessidade. Para uma divergência de métrica, não trate toda diferença como problema de conexão. Separar as camadas evita intervenções de alto impacto que não atacam o erro.


<a id="catalogo-helpers"></a>
## 27. Inventário técnico dos helpers realmente existentes

Este inventário cobre as 51 pastas de snippets e os sete scripts do snapshot examinado. A unidade contada é a pasta de objeto, não o número de funções: um objeto pode exportar várias funções, classes ou constantes. Os dois exemplares de padrões são apresentados separadamente. Nomes e assinaturas abaixo foram extraídos das definições Python, sem executar treinadores nem importar dependências opcionais.

**Como usar:** procure a finalidade, leia o tipo de entrada e de retorno, abra o exemplo específico e só então adapte a chamada. A assinatura é uma referência de consulta; os capítulos 4 a 7 explicam sua notação. Ela não substitui a docstring, os testes ou a revisão de efeitos. As dependências citadas nas fichas destacam pontos de atenção, não constituem um lockfile completo. Nenhuma ficha significa “homologado hoje no seu workspace”.

As referências de código são permalinks do snapshot, iguais nas cópias Git e workspace deste manual. Abrir esses links depende de acesso ao repositório privado. Dentro do workspace, o caminho local equivalente começa em `.assistant/` e conserva a subpasta exibida na ficha.

### 27.1. Constantes e formatação

#### `hub_snippets.constants.colors`

Reúne cores e paletas usadas na apresentação. São valores de configuração visual, não variáveis aprendidas pelo modelo nem regras de aprovação. Consumir uma constante não desenha uma figura sozinho.

Constantes exportadas: `AZUL_CAIXA`, `LARANJA`, `AZUL_CLARO`, `CINZA_ESCURO`, `VERDE`, `VERMELHO`, `ROXO`, `TEAL`, `LARANJA_ESCURO`, `CINZA_MEDIO`, `PALETA_CATEGORICA`, `PALETA_SEQUENCIAL`, `PALETA_DIVERGENTE`, `COR_POSITIVO`, `COR_NEGATIVO`, `COR_NEUTRO`, `COR_ALERTA`, `BG_SECTION`, `BG_HEADER`, `TEXTO_PRINCIPAL`, `TEXTO_SECUNDARIO`, `BORDA_CAIXA`.

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/colors/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py)

#### `hub_snippets.constants.emojis`

Relaciona símbolos e seções da apresentação. Um emoji de alerta é um recurso de comunicação; não executa um teste e não comprova gravidade estatística.

Constantes exportadas: `SECOES_EDA`, `SEMANTICA`.

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/emojis/emojis.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/emojis/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/emojis/exemplo_emojis.py)

#### `hub_snippets.constants.format_br`

Transforma números em texto brasileiro para apresentação: inteiro, percentual, moeda, decimal, diferença e número abreviado. Retorna strings, não números prontos para continuar o cálculo. Declare a escala de percentuais; `fmt_int` trunca entradas fracionárias.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
fmt_int(n: Number) -> str
fmt_pct(v: float, casas: int=1, input_scale: Literal['ratio', 'percent']='ratio') -> str
fmt_brl(v: float) -> str
fmt_dec(v: float, casas: int=4) -> str
fmt_delta(v: float, unidade: str='pp') -> str
fmt_n(n: Number, sufixo: bool=True) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/format_br/format_br.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/format_br/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py)

#### `hub_snippets.constants.styles`

Reúne estilos visuais reutilizáveis e depende das constantes de cores do Hub. CSS controla aparência; não calcula indicadores nem altera permissões do notebook.

Constantes exportadas: `FONT_FAMILY`, `STYLE_SECTION_HEADER`, `STYLE_KPI_CARD`, `STYLE_DIVIDER_LIGHT`, `STYLE_DIVIDER_HEAVY`, `STYLE_BADGE_OK`, `STYLE_BADGE_WARN`, `STYLE_BADGE_FAIL`, `STYLE_INDEX_ITEM`.

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/styles/styles.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/styles/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py)

### 27.2. Tabelas e distribuições

#### `hub_snippets.display.correlation_matrix`

Recebe um DataFrame Spark e colunas numéricas. Calcula correlações e devolve a figura Plotly e os pares fortes, não apenas uma figura isolada. Depende de APIs de `pyspark.ml`; confira suporte no compute e tratamento de nulos. Correlação não é causalidade.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
plot_correlation(df: DataFrame, cols: Optional[Iterable[str]]=None, method: str='pearson', threshold_highlight: float=0.8)
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/correlation_matrix.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/exemplo_correlation_matrix.py)

#### `hub_snippets.display.dataframe_styled`

Recebe uma tabela pandas e devolve HTML estilizado. O consumidor escolhe onde mostrar esse texto. A operação de estilo delegada ao pandas pode exigir Jinja2 na chamada; o módulo carregar não prova essa dependência.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
display_styled(df_pandas, highlight_cols: Optional[Iterable[str]]=None, format_dict: Optional[Dict[str, str]]=None) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/dataframe_styled.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/exemplo_dataframe_styled.py)

#### `hub_snippets.display.distribution_grid`

Recebe DataFrame Spark, seleciona/amostra dados numéricos e devolve uma figura Plotly com distribuições. Confirme tamanho da amostra e leitura das escalas; os histogramas não representam uma contagem integral se vieram de amostra.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
plot_distributions(df: DataFrame, cols: Optional[Iterable[str]]=None, ncols: int=3, sample_n: int=10000)
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/distribution_grid.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/exemplo_distribution_grid.py)

### 27.3. Operações Spark

#### `hub_snippets.spark.date_features`

Recebe Spark DataFrame e coluna de data; devolve atributos de calendário. Feriados nacionais fixos não abrangem automaticamente o calendário bancário, feriados móveis ou locais. Forneça `holiday_dates` quando houver um calendário de projeto autorizado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
extrair_features_data(df: DataFrame, col_data: str, prefixo: Optional[str]=None, *, holiday_dates: Optional[Sequence[str]]=None) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/date_features/date_features.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/date_features/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/date_features/exemplo_date_features.py)

#### `hub_snippets.spark.join_diagnostics`

Recebe dois Spark DataFrames e uma chave, possivelmente composta; devolve dicionário de cardinalidade, correspondência e estimativa de expansão. Não materializa o join completo, mas executa agregações de diagnóstico. Conferir um relacionamento não cria correspondências ausentes.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
diagnosticar_join(esquerda: DataFrame, direita: DataFrame, chave: str | Sequence[str], *, amostra_orfas: int=5) -> Dict[str, Any]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/join_diagnostics.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/exemplo_join_diagnostics.py)

#### `hub_snippets.spark.null_summary`

Recebe Spark DataFrame e devolve uma tabela por coluna com contagens, percentuais e status de nulos. As expressões de nulidade não substituem regras de domínio para strings vazias, sentinelas ou NaN. O semáforo comunica os limiares implementados, não uma lei da plataforma.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
null_summary(df: DataFrame, threshold_warn: float=5, threshold_fail: float=20) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/null_summary/null_summary.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/null_summary/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/null_summary/exemplo_null_summary.py)

#### `hub_snippets.spark.pit_join`

Recebe fatos e histórico de features Spark, chave e tempos, incluindo atraso obrigatório de publicação. Devolve `(dados, diagnostico)`. Impede usar versões indisponíveis sob o modelo temporal informado; atraso fixo não comprova a disponibilidade real se a fonte publica de forma irregular.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
pit_join(fatos: DataFrame, features: DataFrame, chave: str | Sequence[str], ts_decisao: str, ts_feature: str, *, atraso_publicacao_dias: int, janela_maxima_dias: Optional[int]=None, colunas_feature: Optional[Sequence[str]]=None, sufixo: str='', politica_empate: str='erro', devolver_disponibilidade: bool=False) -> Tuple[DataFrame, Dict[str, Any]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/pit_join/pit_join.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/pit_join/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py)

#### `hub_snippets.spark.psi_calculator`

Recebe Spark DataFrames e calcula PSI/CSI. `calcular_psi` devolve um float; `calcular_csi`, um dicionário por coluna; `interpretar_psi`, texto segundo limiares do consumidor. A guarda de cardinalidade categórica protege coleta no driver, mas não elimina todo custo distribuído.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
calcular_psi(df_base: DataFrame, df_atual: DataFrame, col: str, n_bins: int=20) -> float
calcular_csi(df_base: DataFrame, df_atual: DataFrame, feature_cols: List[str], n_bins: int=20, max_categorias: int=LIMITE_CATEGORIAS_CSI) -> Dict[str, float]
interpretar_psi(psi_value: float, *, warning_threshold: Optional[float]=None, critical_threshold: Optional[float]=None) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/psi_calculator.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py)

#### `hub_snippets.spark.safe_display`

Mostra uma quantidade limitada de linhas sem solicitar contagem integral apenas para exibir. Retorna `None`; não é uma função de amostragem que devolve dados para treino. Passe `display_fn=display` quando o renderer estiver disponível no notebook: o módulo não herda suas variáveis globais. Em execução local simples, forneça um renderer compatível ou espere a exceção documentada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
safe_display(df: DataFrame, limit: int=1000, msg: bool=True, *, display_fn: Optional[Callable[[DataFrame], None]]=None) -> None
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/safe_display/safe_display.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/safe_display/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/safe_display/exemplo_safe_display.py)

#### `hub_snippets.spark.smart_sample`

Recebe Spark DataFrame e devolve amostra limitada por `n`, com opção estratificada. No modo estratificado, representar todos os estratos exige capacidade suficiente; mais estratos que linhas permitidas gera erro. Uma amostra para exibição não é automaticamente apropriada para estimação.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
smart_sample(df: DataFrame, n: int=10000, stratify_col: Optional[str]=None, seed: int=42) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/smart_sample/smart_sample.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/smart_sample/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/spark/smart_sample/exemplo_smart_sample.py)

### 27.4. Modelagem, tempo, métricas e monitoramento

#### `hub_snippets.ml.arima_wrapper`

Recebe série NumPy ordenada, ajusta auto-ARIMA e devolve modelo, previsões e métricas. Requer frequência e período sazonal coerentes; lacunas temporais não são inferidas pela posição do array. Pmdarima é exigido na chamada e MLflow é importado no módulo.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_arima(series: np.ndarray, m: int=12, forecast_periods: int=6, seasonal: bool=True, log_mlflow: bool=True) -> Tuple
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/arima_wrapper.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/arima_wrapper/exemplo_arima_wrapper.py)

#### `hub_snippets.ml.autoencoder_anomaly`

Recebe arrays de treino apresentados como normais e dados a avaliar. Devolve rede treinada, limiar e erros de reconstrução. PyTorch é exigido ao importar. O limiar não é uma probabilidade de fraude; o treino pode ser custoso e depende da preparação dos atributos.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
class Autoencoder
    __init__(self, input_dim: int, encoding_dim: int=16, hidden_dims: list=None) -> None
    forward(self, x: torch.Tensor) -> torch.Tensor
train_autoencoder_anomaly(X_train_normal: np.ndarray, X_test: np.ndarray, encoding_dim: int=16, epochs: int=100, batch_size: int=256, lr: float=0.001, patience: int=10, threshold_percentile: float=95.0, log_mlflow: bool=True) -> Tuple[Autoencoder, float, np.ndarray]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/autoencoder_anomaly.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/exemplo_autoencoder_anomaly.py)

#### `hub_snippets.ml.cluster_profiling`

Recebe pandas com atributos e grupos já definidos. Devolve perfis tabulares e diferenças de um grupo em relação ao conjunto. Não cria os clusters; interpreta a segmentação previamente fornecida e exige cuidado com grupos pequenos.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
profile_clusters(df: pd.DataFrame, feature_cols: List[str], cluster_col: str='cluster_id') -> pd.DataFrame
top_differentiators(profiles_df: pd.DataFrame, cluster_id: int, top_n: int=5) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/cluster_profiling.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/exemplo_cluster_profiling.py)

#### `hub_snippets.ml.clustering_suite`

Avalia quantidades de grupos ou executa agrupamento sobre dados pandas/NumPy. Devolve dicionário com resultados, incluindo modelo e informações de agrupamento conforme a operação. Escala dos atributos muda as distâncias; métricas internas não certificam utilidade comercial. Pode registrar MLflow.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
select_k(X_scaled: np.ndarray, k_range: range=range(2, 11), method: str='both') -> Dict[str, object]
run_clustering_pipeline(df: pd.DataFrame, feature_cols: List[str], k: Optional[int]=None, k_range: range=range(2, 11), algorithm: str='kmeans', scaler: str='standard', log_mlflow: bool=True) -> Dict[str, object]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/clustering_suite.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/exemplo_clustering_suite.py)

#### `hub_snippets.ml.curves_plotly`

Recebe rótulos e scores já calculados e devolve figuras ROC, Precision–Recall, lift e KS. Uma curva é um objeto Plotly, não uma implantação ou um teste causal. Preserve classe positiva, população, amostra e tratamento de empates.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
plot_roc_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str='Curva ROC', show_auc: bool=True, n: Optional[int]=None) -> go.Figure
plot_pr_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str='Curva Precision-Recall', n: Optional[int]=None) -> go.Figure
plot_lift_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str='Curva de Lift', n_bins: int=10, n: Optional[int]=None) -> go.Figure
plot_ks_curve(y_true: np.ndarray, y_prob: np.ndarray, title: str='Curva KS', n: Optional[int]=None) -> go.Figure
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/curves_plotly.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/exemplo_curves_plotly.py)

#### `hub_snippets.ml.drift_detection`

Calcula PSI numérico, KS e estabilidade categórica sobre NumPy/pandas; também organiza relatório por feature. As referências definem bins/categorias e os limiares de classificação são política do consumidor. Não confundir o CSI escalar desta interface com o dicionário por feature da versão Spark.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
calculate_psi(reference: np.ndarray, current: np.ndarray, n_bins: int=10, eps: float=1e-06) -> float
calculate_ks(reference: np.ndarray, current: np.ndarray) -> Tuple[float, float]
calculate_csi(reference: pd.Series, current: pd.Series, eps: float=1e-06) -> float
detect_drift_all_features(df_reference: pd.DataFrame, df_current: pd.DataFrame, feature_cols: List[str], numeric_cols: Optional[List[str]]=None, categorical_cols: Optional[List[str]]=None, psi_threshold: Optional[float]=None, ks_threshold: Optional[float]=None, *, severe_psi_threshold: Optional[float]=None, severe_ks_threshold: Optional[float]=None, min_non_null: int=10) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/drift_detection.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/drift_detection/exemplo_drift_detection.py)

#### `hub_snippets.ml.explainability_report`

Recebe evidências de importância e, quando fornecidos, valores SHAP e dados correspondentes. Devolve texto Markdown executivo ou técnico. Não calcula sozinho SHAP nem descobre significado de negócio das colunas. A geração de tabelas Markdown pode exigir `tabulate` na chamada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
generate_executive_report(shap_importance: pd.DataFrame, feature_business_names: Dict[str, str], target_description: str, model_metric: float, metric_name: str='AUC', shap_values: Optional[np.ndarray]=None, X: Optional[np.ndarray]=None, feature_names: Optional[List[str]]=None) -> str
generate_technical_summary(shap_importance: pd.DataFrame, native_importance: Optional[pd.DataFrame]=None) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/explainability_report.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/exemplo_explainability_report.py)

#### `hub_snippets.ml.isolation_forest`

Ajusta detector sobre pandas e devolve dicionário de modelo, scores, rótulos e estatísticas. `profile_anomalies` organiza os casos sinalizados. Requer scikit-learn e importa MLflow no módulo; contaminação é configuração, não taxa de fraude comprovada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_isolation_forest(df: pd.DataFrame, feature_cols: List[str], contamination: float=0.01, n_estimators: int=200, max_samples: str='auto', scaler: str='standard', log_mlflow: bool=True) -> Dict[str, object]
profile_anomalies(df: pd.DataFrame, feature_cols: List[str], scores: np.ndarray, labels: np.ndarray, top_n: int=50) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/isolation_forest.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/isolation_forest/exemplo_isolation_forest.py)

#### `hub_snippets.ml.kaplan_meier`

Recebe pandas com duração e indicador de evento; devolve curvas Plotly ou resultado do teste log-rank. Lifelines é utilizado nas funções. Censura, duração e grupos precisam estar corretamente definidos antes da comparação.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
plot_kaplan_meier(df: pd.DataFrame, duration_col: str, event_col: str, group_col: Optional[str]=None, title: str='Curva de Sobrevivência (Kaplan-Meier)', ci: bool=True) -> go.Figure
log_rank_test(df: pd.DataFrame, duration_col: str, event_col: str, group_col: str) -> Dict[str, Any]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/kaplan_meier.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/kaplan_meier/exemplo_kaplan_meier.py)

#### `hub_snippets.ml.lgbm_ranker`

Recebe arrays e tamanhos dos grupos para ajustar e avaliar um ranking LightGBM. Retorna modelo e métricas no treino e dicionário na avaliação. LightGBM e MLflow integram as dependências de importação. Não trate o score de ranking como probabilidade calibrada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_lgbm_ranker(X_train: np.ndarray, y_train: np.ndarray, groups_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, groups_val: np.ndarray, params: Optional[Dict]=None, num_boost_round: int=500, early_stopping_rounds: int=50, log_mlflow: bool=True) -> Tuple[lgb.Booster, Dict[str, float]]
evaluate_ranking(model: lgb.Booster, X: np.ndarray, y: np.ndarray, groups: np.ndarray, ks: Optional[List[int]]=None) -> Dict[str, float]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/lgbm_ranker.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_ranker/exemplo_lgbm_ranker.py)

#### `hub_snippets.ml.lgbm_temporal`

Apesar do nome, cria atributos temporais em pandas; não treina LightGBM. Produz lags, janelas e atributos de calendário. Respeite entidade, formato de data e política de datas duplicadas. As primeiras linhas podem sair por falta de histórico para os atributos criados.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
create_temporal_features(df: pd.DataFrame, target_col: str, date_col: str, lags: Optional[List[int]]=None, rolling_windows: Optional[List[int]]=None, calendar_features: bool=True, entity_cols: Optional[Sequence[str]]=None, *, date_format: Optional[str]=None, on_duplicate_dates: str='raise') -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/lgbm_temporal.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/lgbm_temporal/exemplo_lgbm_temporal.py)

#### `hub_snippets.ml.metrics_report`

Recebe arrays de valores observados e previstos. Devolve dicionários de métricas. Na classificação, as chaves incluem `auc_roc`, `ks_pct`, `gini`, `auc_pr`, `brier_score`, `f1`, `precision`, `recall`, `lift_10pct` e `prevalence`. KS está em escala percentual; a maioria das demais medidas não. Na regressão, `mape` é percentual e exclui observações cujo valor real é zero.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
calculate_binary_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float=0.5) -> Dict[str, float]
calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/metrics_report.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/exemplo_metrics_report.py)

#### `hub_snippets.ml.mlflow_run`

Abre contexto de registro MLflow e entrega coletor com métodos de parâmetros, métricas, modelo e artefato. MLflow ausente é detectado ao iniciar a operação. Requer destino de tracking autorizado; há escrita e possíveis resíduos de run incompleto. O capítulo 21 explica os limites do controle de completude.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
run_governado(nome: str, *, dataset: str, split: str, limitacoes: Iterable[str], experimento: Optional[str]=None, exigir_completo: bool=True) -> Iterator[_RunGovernado]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/mlflow_run.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/exemplo_mlflow_run.py)

#### `hub_snippets.ml.mlp_embeddings`

Oferece classe de rede e treinador para entradas numéricas e categóricas separadas. Devolve rede e métricas. Índices de categoria e dimensões dos vocabulários precisam corresponder; categorias novas exigem política. PyTorch é uma dependência de importação, e o treino pode registrar MLflow.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
class EmbeddingMLP
    __init__(self, n_numeric: int, cat_dims: List[int], emb_dims: Optional[List[int]]=None, hidden_layers: Optional[List[int]]=None, dropout: float=0.3, task: str='binary')
    forward(self, x_num: torch.Tensor, x_cat: List[torch.Tensor]) -> torch.Tensor
train_embedding_mlp(X_num_train: np.ndarray, X_cat_train: List[np.ndarray], y_train: np.ndarray, X_num_val: np.ndarray, X_cat_val: List[np.ndarray], y_val: np.ndarray, cat_dims: List[int], epochs: int=50, batch_size: int=512, lr: float=0.001, patience: int=10, log_mlflow: bool=True) -> Tuple[EmbeddingMLP, Dict[str, float]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/mlp_embeddings.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/mlp_embeddings/exemplo_mlp_embeddings.py)

#### `hub_snippets.ml.optuna_lgbm`

Recebe arrays de treino/validação e orçamento de busca. Devolve os parâmetros selecionados e o objeto Study do Optuna. Não retorna automaticamente um modelo final já aprovado. A função objetivo e a população de validação determinam o que foi otimizado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
optimize_lgbm(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', n_trials: int=50, metric: str='auc', timeout: Optional[int]=None) -> Tuple[Dict, optuna.Study]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/optuna_lgbm.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/optuna_lgbm/exemplo_optuna_lgbm.py)

#### `hub_snippets.ml.performance_monitor`

Oferece extração de métricas de um relatório e uma classe para comparar desempenho com uma referência. Devolve estruturas de acompanhamento conforme o método chamado. Exige política de métricas e direção de piora; não configura por si só alerta externo, job ou retreino.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
selecionar_metricas_do_relatorio(relatorio: Dict[str, Any], politica: Optional[Dict[str, Any]]=None, *, metricas_obrigatorias: Optional[List[str]]=None) -> Dict[str, float]
class PerformanceMonitor
    __init__(self, baseline_metrics: Dict[str, float], model_name: str='model', *, policy: Optional[Dict[str, Dict[str, Any]]]=None, consecutive_alert_periods: int=3, require_complete_metrics: bool=True) -> None
    add_period(self, period: str, metrics: Dict[str, float], n_predictions: int=0) -> None
    get_current_status(self) -> str
    should_retrain(self) -> Dict[str, object]
    generate_report(self) -> str
    plot_timeline(self, metric: str) -> Any
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/performance_monitor.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/exemplo_performance_monitor.py)

#### `hub_snippets.ml.prophet_wrapper`

Recebe pandas com data e valor, ajusta Prophet e devolve modelo, DataFrame de previsão e métricas de ajuste na própria amostra. Essas métricas in-sample não substituem teste temporal fora do treino; MAPE também exige atenção a valores reais zero. A biblioteca Prophet é importada dentro da função; MLflow e outras dependências do topo continuam necessárias para carregar o módulo. Horizonte, frequência e feriados precisam representar o caso real.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_prophet(df: pd.DataFrame, ds_col: str='ds', y_col: str='y', periods: int=12, freq: str='MS', yearly: bool=True, weekly: bool=False, country_holidays: str='BR', changepoint_prior: float=0.05, log_mlflow: bool=True) -> Tuple
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/prophet_wrapper.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/prophet_wrapper/exemplo_prophet_wrapper.py)

#### `hub_snippets.ml.score_bands`

Recebe scores e eventos observados e devolve pandas por faixa. Empates podem afetar grupos. `higher_score_is_better` exige uma interpretação coerente da direção do score. Decis e labels não são segmentos comerciais aprovados automaticamente.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
generate_score_bands(scores: np.ndarray, y_true: np.ndarray, n_bands: int=10, labels: Optional[Sequence[str]]=None, *, higher_score_is_better: bool=True) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/score_bands/score_bands.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/score_bands/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/score_bands/exemplo_score_bands.py)

#### `hub_snippets.ml.scorecard_builder`

Recebe coeficientes, intercepto e tabelas WOE já estimadas; devolve tabela de pontos. PDO, base de score, odds e definição de evento governam a escala. Não ajusta sozinho uma regressão nem transforma pontos em limite de crédito aprovado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
build_scorecard(coefs: np.ndarray, intercept: float, feature_names: List[str], woe_tables: Dict[str, pd.DataFrame], pdo: int=20, base_score: int=600, base_odds: int=50, event_is_bad: bool=True) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/scorecard_builder.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/scorecard_builder/exemplo_scorecard_builder.py)

#### `hub_snippets.ml.shap_explainer`

Recebe modelo e dados compatíveis, calcula atribuições, resume importância e cria visualizações. Confira tarefa, classe/saída escolhida, ordem das features e amostragem. SHAP e suas dependências são exigidos conforme a implementação; salvar gráficos pode escrever no caminho indicado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
compute_shap(model, X: np.ndarray, feature_names: List[str], model_type: str='tree', max_samples: int=5000, *, task: str='classification', output_index: Optional[int]=None) -> Tuple[np.ndarray, float]
get_feature_importance_shap(shap_values: np.ndarray, feature_names: List[str], top_n: int=20) -> pd.DataFrame
plot_shap_global(shap_values: np.ndarray, X: np.ndarray, feature_names: List[str], plot_type: str='beeswarm', max_display: int=20, save_path: Optional[str]=None)
plot_shap_local(shap_values: np.ndarray, base_value: float, X: np.ndarray, feature_names: List[str], idx: int, save_path: Optional[str]=None)
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/shap_explainer.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/exemplo_shap_explainer.py)

#### `hub_snippets.ml.split_temporal`

Recebe pandas com data e devolve três DataFrames: treino, validação e teste. Opera por períodos e gaps; pode impor restrição adicional por grupo. Não aceita automaticamente um Spark DataFrame. O exemplo do capítulo 16 mostra por que percentuais não são sempre proporções finais de linhas.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
temporal_split(df: pd.DataFrame, date_col: str, train_pct: float=0.7, val_pct: float=0.15, gap_periods: int=1, period_unit: str='M', *, group_col: Optional[str]=None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/split_temporal.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/split_temporal/exemplo_split_temporal.py)

#### `hub_snippets.ml.survival_cox`

Recebe pandas com duração, evento e atributos; devolve modelo Cox e métricas. A função de proporcionalidade devolve tabela de diagnóstico. Lifelines é requerido na execução; o contrato pressupõe codificação coerente de evento e censura. Há registro opcional em MLflow.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_cox_ph(df: pd.DataFrame, duration_col: str, event_col: str, feature_cols: List[str], penalizer: float=0.01, l1_ratio: float=0.0, log_mlflow: bool=True) -> Tuple[object, Dict[str, float]]
validate_proportionality(model, df, duration_col, event_col) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/survival_cox.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/survival_cox/exemplo_survival_cox.py)

#### `hub_snippets.ml.tabnet_wrapper`

Recebe arrays e configuração de categorias, ajusta TabNet e devolve modelo, métricas e importâncias. Pytorch-tabnet é exigido na chamada; dependências de topo precisam estar presentes. Número de épocas e tamanho do lote influenciam custo e memória.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_tabnet(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', cat_idxs: Optional[List[int]]=None, cat_dims: Optional[List[int]]=None, n_d: int=32, n_a: int=32, n_steps: int=5, max_epochs: int=100, patience: int=15, batch_size: int=1024, log_mlflow: bool=True) -> Tuple[object, Dict[str, float], np.ndarray]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/tabnet_wrapper.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/tabnet_wrapper/exemplo_tabnet_wrapper.py)

#### `hub_snippets.ml.train_catboost`

Recebe arrays de treino/validação e devolve modelo CatBoost e métricas. Categorias devem ser identificadas conforme o parâmetro da interface; não presuma que uma string desconhecida será sempre aceita. O módulo exige a biblioteca e pode registrar tracking.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_catboost_baseline(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', cat_features: Optional[List[int]]=None, params_override: Optional[Dict[str, Any]]=None, log_mlflow: bool=True) -> Tuple[Any, Dict[str, float]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/train_catboost.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_catboost/exemplo_train_catboost.py)

#### `hub_snippets.ml.train_lgbm`

Recebe arrays de treino/validação e devolve modelo LightGBM e métricas. Permite configurações e early stopping. LightGBM/MLflow são dependências do módulo; desativar logging não remove imports. Contrato supervisionado não equivale a processamento distribuído Spark.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_lightgbm_baseline(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', params_override: Optional[Dict[str, Any]]=None, early_stopping_rounds: int=50, log_mlflow: bool=True) -> Tuple[lgb.LGBMModel, Dict[str, float]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/train_lgbm.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_lgbm/exemplo_train_lgbm.py)

#### `hub_snippets.ml.train_xgboost`

Recebe arrays de treino/validação e devolve modelo XGBoost e métricas. Exige biblioteca compatível com o ambiente. Preserve dtype, tratamento de ausentes e ordem dos atributos, sobretudo entre ajuste e inferência.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
train_xgboost_baseline(X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, task: str='binary', params_override: Optional[Dict[str, Any]]=None, early_stopping_rounds: int=50, log_mlflow: bool=True) -> Tuple[xgb.XGBModel, Dict[str, float]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/train_xgboost.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/train_xgboost/exemplo_train_xgboost.py)

#### `hub_snippets.ml.umap_viz`

Projeta um array em menor dimensão ou constrói figura Plotly por grupos. UMAP é exigido na chamada. Uma separação visual em duas dimensões é uma representação reduzida, não prova de grupos reais nem de efeito causal.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
compute_umap(X: np.ndarray, n_components: int=2, n_neighbors: int=15, min_dist: float=0.1) -> np.ndarray
plot_umap_clusters(X_scaled: np.ndarray, labels: np.ndarray, title: str='Clusters (UMAP 2D)', cluster_names: Optional[List[str]]=None, point_size: int=3, n: Optional[int]=None) -> go.Figure
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/umap_viz.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/exemplo_umap_viz.py)

#### `hub_snippets.ml.vintage_analysis`

Recebe painel pandas com contrato, originação, referência e target; devolve tabela de maturação. Outras funções geram curvas, heatmap ou comparação entre safras. Diferencie target de evento e target cumulativo; compare apenas maturidades observáveis e denominadores coerentes.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
build_vintage_table(df: pd.DataFrame, contract_id: str, dt_originacao: str, dt_referencia: str, target: str, safra_grain: str='month', mob_col: Optional[str]=None, target_is_cumulative: bool=False) -> pd.DataFrame
plot_vintage_curves(vintage_df: pd.DataFrame, title: str='Curvas de Maturação por Safra', max_mob: int=24, top_n_safras: Optional[int]=None) -> Any
plot_vintage_heatmap(vintage_df: pd.DataFrame, title: str='Heatmap de Safras', max_mob: int=24, metric: str='taxa_acumulada') -> Any
compare_safras(vintage_df: pd.DataFrame, mob_checkpoints: Optional[List[int]]=None) -> pd.DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/vintage_analysis.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/exemplo_vintage_analysis.py)

#### `hub_snippets.ml.walk_forward`

Recebe pandas temporal e uma função de avaliação passada em `model_fn`; devolve lista de resultados por janela. O callback recebe conjuntos de treino e teste de cada rodada. A função não escolhe sozinha o algoritmo; calendário, gap e critério de avaliação são parte do experimento.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
walk_forward_cv(df: pd.DataFrame, date_col: str, target_col: str, model_fn: Callable[[pd.DataFrame, pd.DataFrame], Dict[str, Any]], min_train_periods: int=12, test_periods: int=1, step: int=1, gap: int=0, *, period_unit: str='M') -> List[Dict[str, Any]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/walk_forward.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/walk_forward/exemplo_walk_forward.py)

#### `hub_snippets.ml.woe_iv_calculator`

Recebe Spark DataFrame com feature já discretizada e alvo binário. Devolve tabela WOE e IV total; `classify_iv` fornece uma interpretação por faixas do helper. Essas faixas não constituem regra universal de aprovação. Ajuste bins e WOE no conjunto permitido, não em todo o histórico.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
calculate_woe_iv(df: DataFrame, feature_col: str, target_col: str, smoothing: float=0.5) -> Tuple[DataFrame, float]
classify_iv(iv: float) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/woe_iv_calculator.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/ml/woe_iv_calculator/exemplo_woe_iv_calculator.py)

### 27.5. Dados para exercícios e testes

#### `hub_snippets.testing.fixtures`

Cria Spark DataFrames sintéticos para exercícios tabulares, séries, fatos/features e safras. Alguns testes exigem uma sessão Spark ativa. As características são controladas pelo gerador; não representam estatísticas observadas de clientes reais.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
base_tabular(n: int=500, *, seed: int=42, pct_nulos_renda: float=0.04, prevalencia_alvo: float=0.25, n_entidades: Optional[int]=None) -> DataFrame
serie_temporal(n_entidades: int=20, n_periodos: int=24, *, seed: int=42, tendencia: float=0.5) -> DataFrame
fatos_e_features(n_decisoes: int=300, *, seed: int=42, atraso_real_dias: int=3, pct_feature_futura: float=0.2) -> Tuple[DataFrame, DataFrame]
safras(n_contratos: int=400, *, seed: int=42, safras_yyyymm: Sequence[str]=('202501', '202502', '202503'), mob_maximo: int=12) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/testing/fixtures/fixtures.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/testing/fixtures/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/testing/fixtures/exemplo_fixtures.py)

### 27.6. Componentes visuais

#### `hub_snippets.visual.badge`

Devolve pequenas marcações HTML de status, score ou texto. Cor e rótulo precisam ser alimentados por uma interpretação justificada; a função visual não certifica o dado.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
badge_status(texto: str, tipo: str='ok') -> str
badge_score(valor: float, max: float=100) -> str
badge_inline(texto: str) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/badge/badge.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/badge/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/badge/exemplo_badge.py)

#### `hub_snippets.visual.divider`

Devolve separadores HTML. Controla apresentação, sem cálculo ou escrita de dados. O consumidor precisa renderizar a string na superfície adequada.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
divider_light() -> str
divider_medium() -> str
divider_heavy() -> str
divider_section() -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/divider/divider.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/divider/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/divider/exemplo_divider.py)

#### `hub_snippets.visual.index_generator`

Devolve um índice de etapas de EDA em HTML ou Markdown. O parâmetro `markdown` define o formato. Um link de etapa só será útil se a âncora correspondente existir no documento final.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
gerar_indice_eda(etapas_ativas: Optional[Iterable[int]]=None, markdown: bool=False) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/index_generator.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/index_generator/exemplo_index_generator.py)

#### `hub_snippets.visual.kpi_card`

Devolve cards HTML ou texto Markdown de indicadores. Recebe valores já apurados; não consulta tabela nem calcula KPI de negócio. Um card com número correto e denominador omitido ainda pode induzir erro.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
kpi_card_html(metricas: Dict[str, Any]) -> str
kpi_card_markdown(metricas: Dict[str, Any]) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/kpi_card.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/kpi_card/exemplo_kpi_card.py)

#### `hub_snippets.visual.section_header`

Devolve HTML de cabeçalho para uma seção, com opções preenchidas por etapa ou fornecidas diretamente. Não é o PNG do cabeçalho institucional e não registra um widget nativo.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
section_header_html(etapa: Optional[int]=None, emoji: Optional[str]=None, titulo: Optional[str]=None, descricao: Optional[str]=None) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/section_header/section_header.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/section_header/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/section_header/exemplo_section_header.py)

#### `hub_snippets.visual.theme_plotly`

Obtém configuração, aplica tema a uma figura ou registra um template na sessão. `registrar_template_plotly` tem efeito no estado de apresentação da sessão. A figura formatada continua exigindo exibição; tema não altera a lógica estatística dos dados plotados.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
get_tema_eda() -> Dict[str, Any]
aplicar_tema(fig: go.Figure, subtitulo: Optional[str]=None, fonte: Optional[str]=None, n: Optional[int]=None) -> go.Figure
registrar_template_plotly() -> None
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/theme_plotly.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/visual/theme_plotly/exemplo_theme_plotly.py)

### 27.7. Scripts de inspeção, transformação e documentação

#### `hub_scripts.data_quality_check`

Lê tabela ou view acessível à sessão e devolve dicionário de checks, alertas, score e thresholds. O capítulo 15 demonstra o contrato. Não retorna `metrics`, não impõe enforcement e não valida toda regra de negócio possível.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
data_quality_check(table_name: str, pk_columns: List[str], date_column: Optional[str]=None, thresholds: Optional[Dict[str, float]]=None) -> Dict[str, Any]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/data_quality_check/data_quality_check.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/data_quality_check/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/data_quality_check/exemplo_data_quality_check.py)

#### `hub_scripts.doc_coverage`

Lê arquivo de notebook local/exportado e devolve contagens, cobertura por adjacência e índices de células descobertas. Não busca notebook por URL e não mede a qualidade didática da explicação.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
doc_coverage(notebook_path: str) -> Dict[str, Any]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/doc_coverage/doc_coverage.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/doc_coverage/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/doc_coverage/exemplo_doc_coverage.py)

#### `hub_scripts.drift_detector`

Lê uma tabela, separa duas coortes por data e devolve diagnóstico PSI. O parâmetro `method` existe, mas apenas `psi` está implementado neste snapshot. Valores de data, colunas e critérios de alerta precisam ser fornecidos; o helper não determina o calendário do negócio.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
drift_detector(table_name: str, date_col: str, date_ref: str, date_comp: str, cols: Optional[Iterable[str]]=None, method: str='psi', *, num_bins: int=10, relative_error: float=0.001, epsilon: float=1e-06, warning_threshold: Optional[float]=None, critical_threshold: Optional[float]=None) -> Dict[str, Any]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/drift_detector/drift_detector.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/drift_detector/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/drift_detector/exemplo_drift_detector.py)

#### `hub_scripts.naming_checker`

Lê o schema do recurso e devolve lista de violações da convenção de nomes configurada. `enforce_prefix` e prefixos são política local, não exigência geral do Unity Catalog. Uma advertência sobre qualificação não equivale a falha de acesso.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
naming_checker(table_name: str, *, enforce_prefix: bool=False, allowed_table_prefixes: Sequence[str]=(), max_col_length: int=255) -> List[Dict[str, str]]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/naming_checker/naming_checker.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/naming_checker/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/naming_checker/exemplo_naming_checker.py)

#### `hub_scripts.quick_profile`

Lê tabela/view e devolve perfil em dicionário. `total_rows` e `null_summary_full_table` referem-se à base completa; cardinalidade, valores frequentes, resumos e faixas temporais identificados como sample referem-se à amostra. Metadados de seed e tamanho ajudam a interpretar.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
quick_profile(table_name: str, sample_fraction: float=0.1, max_categories: int=20, *, seed: int=42) -> Dict[str, Any]
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/quick_profile/quick_profile.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/quick_profile/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py)

#### `hub_scripts.rfv_calculator`

Lê eventos e devolve Spark DataFrame com features brutas por cliente até a data de referência inclusiva. Exclui eventos posteriores. Não inventa quintis, segmentos ou clientes que não existam nos eventos elegíveis; o capítulo 17 explica essas consequências.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
rfv_calculator(table_name: str, col_cliente: str, col_data: str, col_valor: str, dt_referencia: str, periodos: Sequence[int]=(30, 60, 90)) -> DataFrame
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/rfv_calculator/rfv_calculator.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/rfv_calculator/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/rfv_calculator/exemplo_rfv_calculator.py)

#### `hub_scripts.schema_to_yaml`

Lê schema e devolve dicionário ou string YAML/JSON serializada, conforme a função. Comentários e estatísticas são opções; estatísticas podem ler dados. O fallback JSON quando PyYAML está ausente é deliberado e não significa arquivo corrompido. Não salva automaticamente em disco.

<details>
<summary>Consultar a API deste objeto: nomes e assinaturas</summary>

```text
schema_to_dict(table_name: str, *, include_comments: bool=True, include_stats: bool=False) -> Dict[str, Any]
schema_to_yaml(table_name: str, include_comments: bool=True, include_stats: bool=False) -> str
```

</details>

[Implementação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/schema_to_yaml.py) · [API exportada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/__init__.py) · [Notebook de exemplo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/exemplo_schema_to_yaml.py)

### 27.8. Exemplares de padrões: aprender a criar sem confundir com produção

`hub_padroes.snippet.taxa_resposta_campanha` recebe contatos e devolve estatísticas por segmento com intervalo de Wilson. O capítulo 18 explica a taxa e a incerteza. `hub_padroes.script.checar_base_campanha` demonstra um diagnóstico delimitado para base de campanha. São exemplares didáticos de estrutura e contrato; não autorizações para aplicar suas regras a qualquer campanha real.

[Exemplar de snippet](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/taxa_resposta_campanha.py) · [Exemplar de script](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/checar_base_campanha.py).

### 27.9. Limites do inventário e escolha entre alternativas

Não existe um único helper correto sem conhecer a demanda. Para nulos de um DataFrame já disponível, considere `null_summary`; para um diagnóstico de chave e nulidade de uma tabela nomeada, considere `data_quality_check`. Para PSI em arrays pequenos, há a versão NumPy; para bases Spark, há funções distribuídas. Para entender distribuição, não comece treinando um modelo. Para melhorar a apresentação, não altere o algoritmo.

Uma assinatura com anotação `DataFrame` pode referir-se a Spark ou pandas conforme o import no módulo; as fichas explicitam o caso. Anotações ausentes não significam retorno livre: confira implementação e exemplo. Classes podem expor métodos públicos adicionais e a importação pode reexportar aliases de tipos; o inventário enfatiza as definições próprias e não promete que todo nome público seja uma função analítica.

Quando surgir um novo objeto, atualize esta seção a partir do código e confira seu exemplo. Ao remover ou renomear um helper, revise também as skills e os prompts que o recomendam. Alterar apenas o texto do manual não cria a implementação faltante.


<a id="metodos"></a>
## 28. Skills, prompts e padrões: como escolher sem decorar o repositório

### 28.1. As treze skills: o método não é o dado

Cada linha abaixo descreve o escopo do método, não uma promessa de execução automática. Na pasta `skills/<nome>/`, `SKILL.md` define o contrato e `templates/` reúne entregáveis de apoio quando presentes. A interface deve receber contexto suficiente para a tarefa; uma menção explícita não supre dados ausentes.

| Skill | Pergunta atendida e contexto necessário | O que revisar na entrega |
|---|---|---|
| `hub-ml-eda-profissional` | Como é uma fonte ou base consolidada? Forneça recurso, grão, chaves candidatas e período. | Perfil, qualidade, distribuições, origem integral/amostral dos números e limites. |
| `hub-ml-cross-eda-ml` | É viável combinar várias fontes? Forneça os EDAs, chaves, tempos e cobertura. | Relações, expansão dos joins, disponibilidade temporal e lacunas antes de modelar. |
| `hub-ml-feature-engineering` | Como construir atributos disponíveis no momento correto? Defina decisão, target, fontes e horizontes. | Contratos, point-in-time, preparação, testes e coerência treino/inferência. |
| `hub-ml-baseline-ml` | Qual referência de modelagem atende ao problema? Informe tarefa, base preparada, split e orçamento. | Comparabilidade, métricas pertinentes, custo, tracking e limitações. |
| `hub-ml-validacao-estatistica` | O que uma evidência sustenta sob incerteza? Defina hipótese, população e desenho. | Pressupostos, magnitude, intervalos, multiplicidade e conclusão proporcional. |
| `hub-ml-analise-safra` | Como os grupos de originação amadurecem? Informe contrato, evento, referência e MOB. | Denominador, maturidade comparável, censura/incompletude e não duplicação de eventos. |
| `hub-ml-explainability` | Como o modelo usa as entradas? Forneça modelo, preparação, dados e saída a explicar. | Coerência de features, referência explicativa, limites e distinção de causalidade. |
| `hub-ml-monitoramento-modelo` | O que observar no funcionamento do modelo? Defina referência, produção, rótulos disponíveis e políticas. | Qualidade, drift, performance, custo e critérios explícitos para investigar/agir. |
| `hub-ml-pipeline-builder` | Como organizar execução recorrente? Informe fontes, destino, frequência, dependências e permissões. | Idempotência, qualidade, retries, observabilidade e aprovação de escritas. |
| `hub-ml-comentar-notebook` | Como explicar um notebook existente? Forneça o código e suas saídas. | Explicação antes/depois, interpretação dos números reais e ausência de mudanças ocultas na lógica. |
| `hub-ml-tutor-databricks` | Como entender um conceito, erro ou bloco? Forneça a dúvida e o contexto mínimo. | Progressão didática, linha a linha quando útil e exemplo compatível com a versão. |
| `hub-ml-auditoria-skills` | O método ou a entrega seguem o contrato? Forneça ambos e o critério de avaliação. | Descoberta, segurança, referências, execução observada e conclusão sustentada. |
| `hub-ml-criar-objeto` | Como criar um componente no padrão do Hub? Defina o tipo, a necessidade e os consumidores. | Molde pertinente, ausência de duplicação, API, exemplo, testes e documentação. |

**Uma skill pode orientar além dos helpers existentes.** Por exemplo, um método de validação estatística pode demandar um teste que não possui wrapper próprio no Hub. Isso não autoriza inventar um módulo com nome convincente. A entrega deve identificar o helper existente, a API nativa ou de biblioteca externa utilizada, ou declarar a implementação adicional necessária.

A sigla `ml` no nome de uma skill é identidade do projeto. Não garante que toda solicitação deva terminar em um modelo treinado. Uma EDA pode concluir que a base ainda não está pronta, e uma auditoria pode concluir que a evidência não é suficiente.

### 28.2. Os dezesseis briefings: dar os detalhes do caso

Os arquivos ficam em `hub_prompts/<nome>/<nome>.md`, acompanhados de notebook `exemplo_<nome>.py`. Abra o briefing real para preencher todos os seus campos; esta tabela explica o ponto de entrada, não cria um formulário alternativo concorrente.

| Briefing | Use para | Informação que não deve faltar |
|---|---|---|
| `novo_projeto` | Delimitar uma iniciativa | Decisão atendida, público, escopo, fontes, riscos e critérios de sucesso. |
| `eda_rapida` | Primeiro diagnóstico limitado | Recurso, período, grão, leitura permitida e profundidade desejada. |
| `eda_completa` | Exploração desenvolvida de uma base | Regras de negócio, variáveis, população, limites de custo e entregáveis. |
| `comparar_tabelas` | Contrastar dois recursos | Qual é a referência, chaves, schemas, períodos e significado da diferença. |
| `cross_eda` | Consolidar fontes e estudos | EDAs existentes, âncora, relações de entidade, disponibilidade e cobertura. |
| `data_quality` | Diagnosticar qualidade | Chaves, campos obrigatórios, referência temporal e limiares aprovados. |
| `feature_engineering` | Planejar/construir atributos | Instante de decisão, target, fontes, transformações e janela histórica. |
| `baseline_orchestration` | Organizar um baseline | Tarefa, split, métrica, comparação e orçamento computacional. |
| `stat_check` | Planejar diagnóstico estatístico | Hipótese, unidade de observação, desenho e relevância prática. |
| `safra` | Analisar maturação de grupos | Originação, observação, evento, denominador e MOB comparável. |
| `explainability` | Explicar um modelo | Modelo/versão, features ordenadas, população e classe/saída escolhida. |
| `monitoramento_modelo` | Definir acompanhamento | Modelo em uso, referência, período corrente, rótulos e política de alerta. |
| `pipeline` | Especificar execução recorrente | Dependências, frequência, destino, qualidade, retries e escritas autorizadas. |
| `comentar_notebook` | Melhorar a explicação de um artefato | Notebook e saídas reais, público e grau de detalhe. |
| `tutor_explicar` | Aprender um ponto específico | Dúvida, bloco/erro e conhecimento prévio. |
| `auditoria_skills` | Conferir método ou resultado | Contrato, evidências e critérios; não apenas a autoavaliação do autor. |

`NÃO INFORMADO` identifica uma lacuna a resolver. `NÃO APLICÁVEL` registra algo examinado e considerado fora do caso. Nenhum dos dois significa “a IA pode escolher um valor sem avisar”. Um placeholder não preenchido também não deve virar um nome literal de tabela consultada.

### 28.3. Um pedido completo, explicado

Depois de preparar a view sintética do capítulo 15 e selecionar o contexto da célula correspondente, este pedido pode orientar uma conversa. Trata-se de um **exemplo de briefing**, não de uma transcrição certificada de resposta.

```text
@hub-ml-eda-profissional

Quero entender se a view temporária vw_manual_campanha_sintetica é adequada
para um exercício de qualidade. Ela foi criada na sessão Spark do notebook.
Selecionei no contexto a célula que a constrói e o schema resultante.

Grão: um evento de campanha por linha.
Chave candidata: event_id. id_cliente se repete legitimamente.
Campos: event_id, id_cliente, dt_evento, canal, respondeu, valor_gasto.
Dados sintéticos: não representam clientes reais.

Modo: explicar e planejar. Não execute código nem altere arquivos ou tabelas.
Confira primeiro se recebeu o preparo e o schema; se faltarem, peça-os.
Quero separar nulidade, duplicidade e freshness. A análise de freshness
não deve mudar o resultado do exercício básico de nulidade.

Entregue: plano, helper existente adequado, parâmetros a fornecer,
campos de retorno que eu devo ler e limitações do diagnóstico.
Não trate score de qualidade como probabilidade nem invente regras de negócio.
```

A primeira linha escolhe o método. O primeiro parágrafo localiza o dado e sua sessão; não o apresenta como tabela persistente de catálogo. Grão e chave impedem contar a repetição de um cliente como duplicação de evento. O modo explicita o limite da ação desejada. O contrato de entrega permite revisar se a resposta explicou algo verificável em vez de apenas produzir uma conclusão.

Uma boa revisão perguntará se a resposta respeitou o modo, utilizou nomes existentes, explicou `checks` e `alerts`, distinguiu políticas e reconheceu informações ausentes. A qualidade da resposta e a evidência de carregamento da skill continuam sendo verificações separadas.

### 28.4. Como os padrões evitam um novo formato a cada tarefa

Um padrão não é uma função especial do Databricks. É uma convenção de organização. A pasta de objeto aproxima implementação, API pública e notebook de exemplo. O checklist acrescenta verificações sobre contrato, documentação, testes e integração com quem já usa o objeto.

**Docstring** é documentação dentro do código; **README**, a entrada da coleção; **template**, um molde; **notebook de exemplo**, uma demonstração; **teste**, uma comparação automatizada com critérios. Nenhum substitui todos os outros. Uma docstring que promete uma chave inexistente deve ser corrigida; não se deve preservar o erro apenas porque está no próprio código.

<a id="indice-termos"></a>
## 29. Índice de termos técnicos e de nomes parecidos

Este índice integra o antigo papel do glossário. As explicações desenvolvidas estão nos capítulos indicados; não é necessário manter outro arquivo de definições.

| Termo | Significado de consulta | Explicação |
|---|---|---|
| API | Interface de uso; pode ser local ou remota | [3](#apis) |
| API pública do helper | Nomes e contratos oferecidos a consumidores Python | [5–6](#contratos) |
| REST, endpoint, HTTP, HTTPS | Contrato e transporte de operações de serviço | [22](#integracoes) |
| SDK / CLI | Biblioteca cliente / interface de comandos | [22](#integracoes) |
| Payload / JSON | Conteúdo transportado / formato de serialização | [22](#integracoes) |
| OAuth, token, service principal | Mecanismos/identidade de autenticação | [22](#integracoes) |
| ACL / autorização | Controle do que uma identidade pode fazer | [25](#seguranca) |
| `sys.path` | Diretórios de busca de módulos no processo Python | [6–7](#importacao) |
| `sys.modules` | Cache de módulos carregados no processo | [8](#estado) |
| PATH / PYTHONPATH | Busca de executáveis / configuração de caminhos Python | [8](#estado) |
| `__init__.py` / `__all__` | Inicialização e declaração de exportações do pacote | [6](#importacao) |
| Módulo / pacote / biblioteca | Organização e distribuição de código reutilizável | [6](#importacao) |
| Função / método / classe / instância | Operações e objetos de programação | [4](#codigo) |
| Parâmetro / argumento | Nome na definição / valor fornecido na chamada | [4–5](#codigo) |
| `return` / `print` | Devolução ao programa / apresentação de texto | [4](#codigo) |
| Assinatura / type hint | Interface de chamada / anotação de tipo | [5](#contratos) |
| Contrato | Entradas, saídas, efeitos e condições de uma operação | [5](#contratos) |
| `None` / `Optional` | Ausência de valor / possibilidade de aceitar ausência | [5](#contratos) |
| Kernel / sessão / runtime | Processo e contexto de execução / ambiente de software | [8](#estado) |
| Magic `%md`, `%pip`, `%run` | Comandos especiais do notebook, não Python puro | [8](#estado) |
| DataFrame / Series / array | Estruturas tabulares, coluna e vetores numéricos | [9](#dados) |
| Schema / dtype | Estrutura declarada / tipo de dado | [9](#dados) |
| Grão / entidade / chave | Unidade da linha / objeto acompanhado / identificação | [9](#dados) |
| Nulo / NaN / vazio / sentinela | Formas diferentes de ausência ou representação | [9](#dados) |
| Spark / PySpark / Spark SQL | Motor distribuído e suas interfaces | [10](#spark) |
| SparkSession / Spark Connect | Contexto SQL / arquitetura cliente-servidor | [10](#spark) |
| Driver / executor / partição | Coordenação / execução / divisão do trabalho | [10](#spark) |
| Lazy / ação / transformação | Plano adiado / solicitação de resultado / alteração de plano | [10](#spark) |
| `collect` / `toPandas` | Trazer resultados ao processo consumidor | [9–10](#dados) |
| Shuffle / broadcast / UDF | Redistribuição / replicação controlada / função de usuário | [10](#spark) |
| Serverless / compute / warehouse | Execução gerenciada / recurso de execução / compute SQL | [10–11](#spark) |
| Unity Catalog / tabela / view | Governança / dados organizados / consulta nomeada | [11](#unity-catalog) |
| Delta / time travel / retenção | Tabela com histórico / consulta de versão / prazo de disponibilidade | [11](#unity-catalog) |
| Dependência / pin / lockfile | Pacote requerido / versão fixada / resolução registrada | [12](#dependencias) |
| `imp` / `exec` | Dependência exigida no import / na chamada | [12](#dependencias) |
| Wheel / ZIP de implantação | Distribuição Python / pacote de arquivos do workspace | [23](#publicacao) |
| Genie Code / Agent Skill | Assistente técnico / procedimento textual carregável | [13](#genie) |
| Frontmatter / description | Metadados do arquivo / campo de relevância | [13](#genie) |
| Prompt / contexto / token | Pedido / informação disponível / unidade de processamento textual | [13](#genie) |
| MCP / conector | Protocolo de ferramentas / integração configurada | [22](#integracoes) |
| Widget / card / PNG | Parâmetro interativo / apresentação de indicador / imagem | [14](#visuais) |
| HTML / CSS / Markdown / Plotly | Estrutura visual / estilo / texto marcado / figuras programáticas | [14](#visuais) |
| Threshold / score / enforcement | Limiar / medida com definição própria / imposição de política | [15](#qualidade) |
| Freshness | Idade da informação segundo referência escolhida | [15](#qualidade) |
| Join / cardinalidade / expansão | Combinação / relação entre chaves / multiplicação de linhas | [16](#tempo) |
| Leakage / point-in-time / as-of | Informação indevida / respeito à disponibilidade temporal | [16](#tempo) |
| Split / gap / walk-forward | Separação / intervalo / avaliação que avança no tempo | [16](#tempo) |
| Callback | Função entregue a outra função para execução controlada | [16](#tempo) |
| RFV / RFM | Recência, frequência e valor | [17](#rfv) |
| EDA / amostra / distribuição | Exploração / subconjunto / organização dos valores | [18](#estatistica) |
| PSI / CSI / KS | Medidas de distribuição; contratos e escalas variam | [18](#estatistica) |
| CI / CD | Integração contínua / entrega ou implantação contínua | [24](#validacao) |
| WOE / IV / scorecard / odds / PDO | Evidência, separação e convenção de escala de pontos | [18–20](#estatistica) |
| Wilson / intervalo / p-valor | Quantificação de incerteza sob hipóteses | [18](#estatistica) |
| Safra / vintage / MOB | Grupo de originação e maturidade | [18](#estatistica) |
| Feature / target / fit / predict | Entrada / resultado-alvo / ajustar / inferir | [19](#modelos) |
| Baseline / overfitting / regularização | Referência / ajuste excessivo / controle de flexibilidade | [19](#modelos) |
| Hiperparâmetro / trial / early stopping | Configuração / tentativa / parada por critério | [19](#modelos) |
| Embedding / MLP / autoencoder | Representação vetorial / rede / reconstrução | [19](#modelos) |
| Clustering / anomalia / censura | Agrupamento / caso diferente / evento ainda não observado | [19](#modelos) |
| AUC / precisão / recall / lift | Métricas de ordenação, seleção e concentração | [20](#metricas) |
| MAE / RMSE / MAPE / R² | Medidas de erro e comparação de regressão | [20](#metricas) |
| SHAP / importância / calibração | Atribuição / relevância no modelo / coerência probabilística | [20](#metricas) |
| MLflow / run / experimento / artefato | Registro e organização de tentativas | [21](#mlflow) |
| Tracking URI / flavor / assinatura de modelo | Destino / formato de integração / contrato de artefato | [21](#mlflow) |
| Commit / branch / push / PR | Unidades e fluxo de versionamento | [23](#publicacao) |
| Fonte / render / derivado / deploy | Autoria / geração / cópia / implantação | [2](#pastas), [23](#publicacao) |
| FILE / NOTEBOOK / SOURCE / RAW | Tipos de objeto e formatos de transporte | [23](#publicacao) |
| Manifesto / hash / SHA-256 | Inventário e comparação de integridade | [23](#publicacao) |
| Job / DAG / pipeline / Bundle | Orquestração e descrição de recursos | [23](#publicacao) |
| Retry / rollback / idempotência | Repetição / reversão / repetição sem efeito adicional indevido | [23](#publicacao) |
| AST / teste / mock / skip / smoke | Formas e limites de validação | [24](#validacao) |
| Gate / evidência / aceite | Condição de avanço / registro observado / decisão revisada | [24](#validacao) |
| Fail-closed / privilégio mínimo | Recusa sem condições comprovadas / acesso necessário | [25](#seguranca) |
| Traceback / exceção / timeout | Caminho da falha / sinalização de erro / prazo excedido | [26](#erros) |
| ADR / handoff / runbook | Decisão arquitetural / passagem de estado / procedimento operacional | [30](#fontes) |

<a id="fontes"></a>
## 30. Fontes, manutenção e alcance das afirmações

### 30.1. Como conferir a procedência

Há três níveis de informação neste manual. **Conceitos** explicam uma ideia geral, como função ou intervalo de confiança. **Comportamento do Hub** descreve implementações do snapshot examinado e pode ser conferido em seus módulos. **Capacidade da plataforma** segue a documentação oficial, mas sua disponibilidade e configuração ainda precisam ser verificadas no workspace.

Os exemplos sintéticos e interpretações pedagógicas foram preparados para este manual. Números esperados são explicitamente identificados. Não se presume que a execução no computador local, o import de uma biblioteca, um registro histórico ou a existência de um README homologuem hoje o ambiente de trabalho.

Um **ADR** registra uma decisão arquitetural. Um **handoff** transmite estado, resultados e pendências para outra sessão ou pessoa. Um **runbook** organiza um procedimento operacional com pré-condições e verificação. Esses registros ficam na documentação de manutenção; não são mecanismos nativos que o Databricks executa ao abrir o Hub.

### 30.2. Referências oficiais por identificador

As referências `[Sxx]` no texto identificam as páginas abaixo. Foram consultadas em 11/09/2026. As páginas `latest` e as páginas de serviço gerenciado podem evoluir; compare-as com a versão em uso antes de implementar uma mudança de plataforma.

| ID | Fonte primária |
|---|---|
| <a id="fonte-s01"></a>S01 | [Python — módulos e pacotes](https://docs.python.org/3/tutorial/modules.html) |
| <a id="fonte-s02"></a>S02 | [Python — funções e controle de fluxo](https://docs.python.org/3/tutorial/controlflow.html) |
| <a id="fonte-s03"></a>S03 | [Python — introspecção com inspect](https://docs.python.org/3/library/inspect.html) |
| <a id="fonte-s04"></a>S04 | [Databricks — módulos e bibliotecas em workspace files](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-modules) |
| <a id="fonte-s05"></a>S05 | [Databricks — referência de APIs de workspace](https://docs.databricks.com/api/workspace/) |
| <a id="fonte-s06"></a>S06 | [Python — sys, path e modules](https://docs.python.org/3/library/sys.html) |
| <a id="fonte-s07"></a>S07 | [Python — sistema de importação](https://docs.python.org/3/reference/import.html) |
| <a id="fonte-s08"></a>S08 | [Databricks — instruções da Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions) |
| <a id="fonte-s09"></a>S09 | [Databricks — Agent Skills da Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills) |
| <a id="fonte-s10"></a>S10 | [Apache Spark — SQL e DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html) |
| <a id="fonte-s11"></a>S11 | [Apache Spark — Spark Connect](https://spark.apache.org/docs/latest/spark-connect-overview.html) |
| <a id="fonte-s12"></a>S12 | [Databricks — limitações de compute serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations) |
| <a id="fonte-s13"></a>S13 | [Databricks — Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/) |
| <a id="fonte-s14"></a>S14 | [Apache Spark — createOrReplaceTempView](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.createOrReplaceTempView.html) |
| <a id="fonte-s15"></a>S15 | [Databricks — dependências em notebooks serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies) |
| <a id="fonte-s16"></a>S16 | [Databricks — widgets de notebook](https://learn.microsoft.com/en-us/azure/databricks/notebooks/widgets) |
| <a id="fonte-s17"></a>S17 | [Databricks — comandos CLI de workspace](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/cli/reference/workspace-commands) |
| <a id="fonte-s18"></a>S18 | [Databricks — metadados e tipo de objeto no workspace](https://docs.databricks.com/api/workspace-objects/v1/get-status) |
| <a id="fonte-s19"></a>S19 | [Databricks — privilégios do Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/access-control/privileges-reference) |
| <a id="fonte-s20"></a>S20 | [Agent Skills — especificação aberta](https://agentskills.io/specification) |
| <a id="fonte-s21"></a>S21 | [Databricks — modo agente e aprovações](https://learn.microsoft.com/en-us/azure/databricks/genie-code/agent-mode) |
| <a id="fonte-s22"></a>S22 | [Databricks — imagens e mídia em notebooks](https://learn.microsoft.com/en-us/azure/databricks/notebooks/notebook-media) |
| <a id="fonte-s23"></a>S23 | [scikit-learn — TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html) |
| <a id="fonte-s24"></a>S24 | [MLflow — tracking de experimentos](https://mlflow.org/docs/latest/ml/tracking/) |
| <a id="fonte-s25"></a>S25 | [MLflow — assinaturas e exemplos de entrada](https://mlflow.org/docs/latest/ml/model/signatures/) |
| <a id="fonte-s26"></a>S26 | [scikit-learn — avaliação de modelos e métricas](https://scikit-learn.org/stable/modules/model_evaluation.html) |
| <a id="fonte-s27"></a>S27 | [Databricks — SDK Python](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/sdk-python) |
| <a id="fonte-s28"></a>S28 | [Databricks — autenticação para ferramentas](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/) |
| <a id="fonte-s29"></a>S29 | [Databricks — MCP na Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/mcp) |
| <a id="fonte-s30"></a>S30 | [Python — gerenciadores de contexto](https://docs.python.org/3/library/contextlib.html) |
| <a id="fonte-s31"></a>S31 | [Databricks — Lakeflow Jobs](https://learn.microsoft.com/en-us/azure/databricks/jobs/) |
| <a id="fonte-s32"></a>S32 | [Databricks — Declarative Automation Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/) |
| <a id="fonte-s33"></a>S33 | [Databricks — histórico, versões e retenção de tabelas](https://docs.databricks.com/aws/en/tables/history) |
| <a id="fonte-s34"></a>S34 | [Databricks — Spark Declarative Pipelines](https://learn.microsoft.com/en-us/azure/databricks/ldp/) |
| <a id="fonte-s35"></a>S35 | [Databricks — expectations de qualidade](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations) |
| <a id="fonte-s36"></a>S36 | [Databricks — família Genie, Genie One e Genie Agents](https://learn.microsoft.com/en-us/azure/databricks/genie/) |

### 30.3. Fontes de implementação e de manutenção

O inventário do capítulo 27 aponta para cada implementação, sua API exportada e seu notebook. As referências abaixo sustentam a organização, os mecanismos de validação e o fluxo de entrega. Referenciar uma ferramenta não executa o comando nem autoriza publicação.

- [`README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/README.md)
- [`CLAUDE.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/CLAUDE.md)
- [`.claude/rules/docs-e-readmes.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/.claude/rules/docs-e-readmes.md)
- [`.claude/rules/genie-code-oficial.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/.claude/rules/genie-code-oficial.md)
- [`docs/decisions/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/docs/decisions/README.md)
- [`ambiente_fonte/.assistant_instructions.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant_instructions.md)
- [`ambiente_fonte/.assistant/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/README.md)
- [`ambiente_fonte/.assistant/skills/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/skills/README.md)
- [`ambiente_fonte/.assistant/hub_prompts/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_prompts/README.md)
- [`ambiente_fonte/.assistant/hub_padroes/README.md`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_padroes/README.md)
- [`ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt)
- [`tools/api_publica.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/api_publica.py)
- [`tools/notebook_marker.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/notebook_marker.py)
- [`tools/render_simulado.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/render_simulado.py)
- [`tools/publicar_free.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/publicar_free.py)
- [`tools/bundle_implantacao.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/bundle_implantacao.py)
- [`tools/validate_assistant.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/validate_assistant.py)
- [`tools/ci_local.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/ci_local.py)
- [`tools/project_policy.py`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/c5fdc61181c14124d653cf9e6222d9a402745949/tools/project_policy.py)

### 30.4. Como atualizar este manual sem criar duas redações

Edite o arquivo de autoria `ambiente_fonte/.assistant/MANUAL_TECNICO.md`. Confira os contratos no código quando acrescentar uma API ou modificar exemplos. Sincronize a cópia de leitura da raiz Git a partir desse mesmo arquivo e regenere o simulado pelo renderer, nunca por edição manual do derivado. A igualdade das cópias é parte da conferência documental.

A seguir está uma operação **local de manutenção**, a executar a partir da raiz do repositório após revisar a nova redação. Ela não publica no Databricks:

```powershell
python -c "from pathlib import Path; Path('MANUAL_TECNICO.md').write_bytes(Path('ambiente_fonte/.assistant/MANUAL_TECNICO.md').read_bytes())"
python tools/render_simulado.py --write
python tools/validate_assistant.py --conferir-readme
python tools/ci_local.py
```

Atualizar uma referência oficial exige rever a afirmação que ela sustenta; não basta trocar a data. Atualizar uma contagem exige executar sua verificação. Atualizar um teste requer preservar a distinção entre verificações locais, runtime Databricks, serviços remotos e conversa da Genie Code.

**Síntese final:** o arquivo orienta; o import disponibiliza código; a chamada realiza trabalho; o runtime determina como esse trabalho pode ocorrer; a autorização delimita recursos e efeitos; a evidência permite conferir o resultado. Entender essas seis etapas elimina grande parte da impressão de que o Databricks “puxa uma API” ou de que a IA executa tudo o que encontra em uma pasta.
