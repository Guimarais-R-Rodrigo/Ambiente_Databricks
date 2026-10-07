<a id="parte-mu-i"></a>
# MU parte i

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MU-indice.md#sumario-mu) · [Livro completo](../../MANUAL_DO_USUARIO.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu01"></a>
<a id="mu01"></a>
### MU01 — Conhecer o Hub e escolher sua trilha

**Pergunta deste capítulo:** qual recurso do Hub ajuda na sua tarefa de hoje e por onde começar sem precisar conhecer todo o projeto? Você pode usar este capítulo para escolher uma rota e formular seu primeiro pedido. Ainda não é necessário programar nem executar uma análise.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](MU-indice.md#sumario-mu) · [Primeiro uso](#mu02) · [Catálogo e Concierge](#mu03) · [Por que o Hub existe](MT-parte-i.md#mt01)
<!-- editorial:exclude:end -->

<a id="mu01-1"></a>
#### 1. Começar pela decisão que você precisa tomar

Imagine que alguém lhe entregou uma tabela de contatos de campanha e pediu uma recomendação para o próximo mês. Antes de pensar em modelo ou gráfico, você precisa saber o que há em cada linha, se o mesmo contato aparece mais de uma vez, que período está coberto e qual pergunta a análise deve responder. O Hub reúne orientações e recursos para transformar esse começo vago em trabalho conferível. Ele oferece métodos para conversar com o assistente, formulários para declarar contexto, código reutilizável e exemplos que ensinam a ler a saída. O [guia do ecossistema](../../README.md) apresenta essas peças e suas rotas de uso.

O ganho mais simples é parar de reconstruir uma checagem conhecida a cada notebook. Outro ganho é lembrar decisões que um pedido curto costuma omitir: unidade de cada linha, momento em que uma informação estava disponível, custo de consultar uma tabela e limite do resultado. A presença do Hub, porém, não verifica automaticamente a sua base nem torna correta qualquer resposta da IA. Você continua responsável por reconhecer o dado, conferir a execução, interpretar o resultado e decidir o próximo passo. Se ainda não sabe qual tabela ou qual decisão está em jogo, a primeira ação pode ser esclarecer isso, sem rodar código.

Neste manual, **Genie Code** é o assistente com o qual você pode conversar no Databricks. O Hub usa mecanismos de instrução e Agent Skills oferecidos pela plataforma e acrescenta conteúdo próprio: skills `hub-ml-*`, prompts, snippets, scripts e padrões. As duas coisas convivem, mas têm efeitos diferentes. Abrir um chat pode disponibilizar certas instruções e sugerir uma skill pertinente; não faz toda a pasta `.assistant` ser lida nem executa cada função nela. Quando um notebook precisa de uma função auxiliar, seu código ainda tem de importá-la e chamá-la. A distinção protege você de concluir “o Hub fez a verificação” apenas porque um recurso apareceu na conversa.

Uma boa frase de partida contém **objetivo e evidência desejada**: “quero saber se esta tabela pode sustentar uma análise de resposta; preciso de contagens de nulos, duplicatas e período, sem alterar a fonte”. Essa frase permite escolher um diagnóstico curto. “Quero entender a população, distribuições, lacunas e riscos antes de recomendar uma ação” pede um percurso de exploração mais amplo. Ambas são tarefas legítimas; a segunda precisa de mais contexto e interpretação. Ao terminar este capítulo, você poderá explicar essa diferença sem memorizar nomes de pastas.

<a id="mu01-2"></a>
#### 2. Reconhecer as peças pelo que você fará com elas

Uma **skill** organiza um método de trabalho para o assistente: que perguntas fazer, que passos seguir, quais recursos considerar e que limites declarar. **Análise exploratória de dados (EDA)** é o percurso para conhecer estrutura, distribuições, lacunas e relações de uma fonte. Se você está recebendo uma base nova e quer essa exploração orientada, `@hub-ml-eda-profissional` é uma rota possível. Você pode selecionar uma skill explicitamente com `@`; a plataforma também pode considerar sua descrição para escolhê-la quando pertinente. Essa seleção não prova que todas as etapas foram cumpridas. Leia o plano proposto e, depois, a evidência do que foi de fato executado. Para uma dúvida pequena, como “o que significa esta coluna?”, não é preciso abrir uma análise completa.

Um **prompt** é um briefing que você abre, preenche e fornece ao chat. Ele ajuda a informar tabela, período, grão, restrições e entrega esperada quando seria fácil omitir algum campo. O prompt não é descoberto automaticamente só porque está em `hub_prompts/`. Se um campo não é conhecido, declare `NÃO INFORMADO` e peça inspeção ou esclarecimento; `NÃO APLICÁVEL` só cabe quando você avaliou a pergunta e ela realmente não se aplica. Preencher um formulário não concede acesso à tabela nem garante que o assistente executou o código solicitado.

Um **snippet** é uma função ou classe Python que você usa no seu próprio notebook. Por exemplo, `format_br` oferece uma função para mostrar uma taxa já calculada como texto brasileiro. Ela não precisa de skill: você localiza a cópia acessível do Hub, importa a função, chama com a escala correta e confere o texto. Um **script** também é chamado explicitamente, mas costuma ser um utilitário delimitado de inspeção, transformação ou governança. `data_quality_check` pode devolver um diagnóstico de uma tabela. Outros scripts têm retornos diferentes, inclusive tabela de features ou texto de schema; leia o README e a assinatura do candidato antes de compor seu fluxo. MU06 e MU07 ensinam as duas rotas diretas.

Um **padrão** é um molde para quem vai criar ou documentar uma peça do Hub. Consultá-lo ajuda a não inventar um formato novo para README, exemplo ou API; ele não é uma análise pronta. Um **notebook de exemplo** mostra uma situação com código e interpretação, mas precisa ser lido antes de executar, porque o exemplo pode preparar dados sintéticos ou escrever algo que o helper principal não escreve. O **README local** da pasta é a porta de entrada: explica quando usar, requisitos, efeitos e limites. Depois confira a implementação ou o briefing, que definem os nomes e comportamentos reais. O [README do produto](../../README.md#-o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho) liga essas peças às cinco famílias gerais de recursos do ecossistema. O [Hub Micromodelos](../../hub_micromodelos/README.md) combina essas famílias para especificar uma característica de domínio, estudar suas evidências e registrar incertezas. Sua skill está em `L1/audit`; a biblioteca exige chamada explícita, e o exemplo sintético não publica nem homologa um modelo.

Pense em uma taxa de resposta já pronta. Se só precisa exibi-la, escolha o snippet de formatação; pedir à skill de EDA para formatar uma string acrescentaria trabalho sem melhorar a pergunta. Se a taxa ainda depende de conferir duplicatas, nulos e denominador, a formatação é a última etapa, não a primeira. Esse contraexemplo ajuda a reconhecer que uma saída bonita não substitui uma medição adequada. Do mesmo modo, um prompt pode orientar o pedido de análise, mas não substitui o cálculo ou a revisão do notebook.

<a id="mu01-3"></a>
#### 3. Seguir uma trilha curta e testar sua escolha

Use a **intenção de hoje** para entrar no manual. Se quer apenas localizar algo, comece pelo [catálogo e Concierge](#mu03); o Concierge ajuda a recomendar recursos existentes e não executa a análise durante essa descoberta. Se quer trabalhar com um método assistido, vá a [skills](MU-parte-ii.md#mu04) e depois ao capítulo da tarefa. Se já sabe qual função ou utilitário usar, prepare o ambiente em [MU02](#mu02) e siga a chamada isolada de [snippet](MU-parte-ii.md#mu06) ou [script](MU-parte-ii.md#mu07). Para criar uma peça nova, use o capítulo de documentação e autoria. Para uma entrega visual, inicie pelo planejamento visual e avance até os exemplos de notebook e assets conforme a necessidade. A trilha é uma sequência de consulta, não uma exigência de percorrer o manual inteiro antes de trabalhar.

| Sua necessidade imediata | Primeira rota | O que esperar dessa rota |
|---|---|---|
| Ainda não sei qual recurso serve | MU03 ou Concierge | recomendação para conferir, sem execução analítica |
| Quero conhecer uma fonte inteira | skill de EDA e MU08 | plano e análise assistida com revisão das premissas |
| Quero uma checagem delimitada | script e MU07 | retorno definido pelo utilitário escolhido |
| Já tenho um cálculo, preciso reaproveitar função | snippet e MU06 | valor produzido por uma chamada no notebook |
| Quero padronizar uma peça ou visual | padrões, MU18 ou MU14 | molde e roteiro de construção, sujeitos a revisão |

Pratique com dois pedidos sobre uma tabela **fictícia** `catalogo.analytics.contatos`. Pedido A: “Antes de calcular a taxa, quero saber se a chave de contato se repete, quantas respostas estão nulas e se a tabela está atualizada.” Há perguntas delimitadas de qualidade, então um script como `data_quality_check` é candidato. Abra o [README do script](../../hub_scripts/data_quality_check/README.md), confira campos e limites e execute apenas se tiver acesso e autorização. A saída esperada é um diagnóstico para orientar a decisão de prosseguir, não uma base corrigida nem uma garantia de que o desenho da campanha foi adequado.

Pedido B: “Recebi a fonte e preciso entender a população, as distribuições, as lacunas e que análises valem a pena antes de recomendar o próximo contato.” Aqui o objetivo é mais amplo que uma lista de checagens. Uma EDA assistida pode combinar perguntas, recursos e interpretação; `@hub-ml-eda-profissional` é uma rota para orientar esse percurso. Informe que cada linha deveria representar um contato, o período conhecido e o que ainda está em aberto. Peça um plano primeiro se ainda não quer executar consultas. Uma resposta que apenas mostra `status: pass` não satisfaz B, porque não examina distribuições nem limitações; uma EDA longa para responder só A pode consumir tempo e desviar do pedido.

O exercício tem uma segunda etapa: confira o que cada rota **não** sabe. A não valida, por si, se o denominador da taxa é o certo para a decisão. B não recebe permissão de leitura apenas por ser uma skill e não demonstra execução ao ser mencionada. Se o diagnóstico indicar `fail`, entenda o alerta e decida como investigar; não filtre automaticamente os registros para produzir uma aparência de aprovação. Se a EDA encontrar um campo de tempo ambíguo, esclareça qual data representa o contato antes de aceitar conclusões. A escolha de recurso é boa quando deixa a próxima pergunta mais precisa.

<a id="mu01-4"></a>
#### 4. Pedir ajuda com contexto suficiente e reconhecer o próximo passo

Você não precisa conhecer Spark, imports ou JSON para começar. Precisa conseguir dizer **qual decisão** depende do trabalho e qual material está disponível. Um pedido útil informa a tabela ou arquivo autorizado, o período, o significado de uma linha quando conhecido, restrições como “somente leitura” e o formato esperado: explicação, plano, código para revisar ou execução. Se um item essencial não for conhecido, diga isso. Não invente nomes de colunas, regras de negócio ou permissões para fazer o pedido parecer completo. O assistente pode ajudar a transformar a lacuna em pergunta ou inspeção permitida.

Por exemplo: “Quero decidir se posso comparar a resposta por segmento em `catalogo.analytics.contatos`. Cada linha deveria ser um contato; não sei ainda se há repetições. Considere janeiro a março. Primeiro proponha checagens somente leitura e diga que informação falta; não execute nem escreva.” O texto delimita propósito, fonte, unidade provável, incerteza, período e modo de trabalho. Se você quiser uma skill específica, acrescente `@hub-ml-eda-profissional` apenas quando o percurso de EDA for o pretendido. O nome na sua **resposta** a outra pessoa não ativa uma skill; a seleção precisa ocorrer na interação e ser conferida no contexto disponível.

Depois de receber ajuda, separe três perguntas: o recurso certo foi escolhido? O código ou a consulta realmente rodou no ambiente autorizado? O resultado responde à decisão com limitações compreensíveis? A primeira não prova as outras. Se um arquivo ou tabela não estiver acessível, pare naquele passo e obtenha a localização ou permissão pelo caminho de trabalho apropriado. Se a resposta do assistente disser “feito” sem mostrar execução ou evidência, trate-a como proposta a conferir. O [guia de política de enforcement](../../hub_padroes/skill_enforcement/README.md) aprofunda essas diferenças para quem cria ou audita skills; para seu primeiro uso, basta manter proposta, execução e validação separadas.

Se a próxima dificuldade for localizar a cópia do Hub e fazer uma primeira chamada, siga [MU02](#mu02). Se a dificuldade for escolher entre recursos parecidos, siga [MU03](#mu03). O detalhe de por que as pastas e instruções foram organizadas assim está em [MT01](MT-parte-i.md#mt01) e [MT02](MT-parte-i.md#mt02). Você pode voltar a esses capítulos quando a operação pedir mais fundamento; a escolha inicial continua ancorada na tarefa e no resultado que você consegue conferir.

<!-- editorial:exclude:start -->
**Fontes principais:** [guia do produto](../../README.md), [instruções operacionais](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/ambiente_fonte/.assistant_instructions.md), [manual técnico vigente](../../MANUAL_TECNICO.md), [README raiz](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/README.md), [ADR de arquitetura](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0001-arquitetura-multi-ia.md), [policy de enforcement](../../hub_padroes/skill_enforcement/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Próximo: MU02](#mu02) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT01](MT-parte-i.md#mt01) · [MT02](MT-parte-i.md#mt02)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu02"></a>
<a id="mu02"></a>
### MU02 — Primeiro uso, ambiente e acesso aos recursos

**Pergunta deste capítulo:** como confirmar que você está vendo a cópia certa do Hub e fazer uma primeira chamada pequena? O percurso começa pela localização dos arquivos, testa uma função de formatação sem consultar tabelas e mostra onde investigar quando algo falha. Os caminhos e a saída servem como exemplo; confirme o endereço e o ambiente autorizados para a sua sessão.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](MU-indice.md#sumario-mu) · [Escolher uma trilha](#mu01) · [Usar snippet diretamente](MU-parte-ii.md#mu06) · [Fundamentos de importação](MT-parte-i.md#mt03)
<!-- editorial:exclude:end -->

<a id="mu02-1"></a>
#### 1. Localizar a cópia de uso e distinguir os objetos

Comece pelo lugar onde seu trabalho acontece. O repositório mantém o produto editável em `ambiente_fonte/`, mas isso não demonstra que ele foi instalado no seu workspace do Databricks. O [README de manutenção](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/ambiente_fonte/README.md) separa fonte editável, espelho gerado, laboratório e destino de trabalho; cada um tem finalidade e permissão próprias. Para **consumir** um recurso, encontre a cópia `.assistant` que sua equipe disponibilizou e que sua conta pode ler. Se ela não aparecer, peça a localização publicada ao responsável pelo ambiente. Não tente consertar uma ausência no workspace executando ferramentas de publicação do repositório.

Três nomes parecidos podem gerar erros diferentes. Um **arquivo** é conteúdo guardado no workspace, como `hub_snippets/constants/format_br/format_br.py`; um **notebook** organiza células executáveis e explicações, como `exemplo_format_br.py`; uma **tabela** é dado consultado pelo Spark por identificador como `catalogo.schema.tabela`. Alguns notebooks e arquivos Python terminam em `.py`, então a extensão sozinha não distingue os dois. No Hub, o marcador `# Databricks notebook source` identifica o formato de notebook de exemplo; as ferramentas de publicação conferem o tipo `NOTEBOOK` para esse exemplo e `FILE` para o módulo importável. O [detector de marcador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/notebook_marker.py) e o [publicador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/publicar_free.py) documentam essa diferença técnica. Você não precisa rodar essas ferramentas para usar `fmt_pct`; precisa saber qual peça abrir e qual peça importar.

Há também dois tipos de caminho. `/Users/<username>/.assistant` pode identificar a pasta como objeto na navegação do workspace. Para código Python acessar arquivos da mesma cópia, o caminho costuma aparecer como `/Workspace/Users/<username>/.assistant`. `<username>` é um marcador a substituir, não um usuário válido. A raiz pode ser diferente quando a entrega estiver em uma Git folder ou área compartilhada. Confira o endereço efetivo no seu ambiente antes de colocá-lo num notebook; não transforme automaticamente um caminho de interface no outro. A [documentação oficial de arquivos de workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace) distingue arquivos e source notebooks e ressalta que o suporte depende do runtime e do modo de uso.

Um endereço de tabela usa pontos por outra razão: catálogo, schema e nome do dado. Ele não entra em `sys.path`, a lista de lugares onde o Python procura módulos. Se você tentar `spark.table("hub_snippets.constants.format_br")`, pedirá ao Spark uma tabela com esse nome, não uma função; se puser `catalogo.schema.tabela` em `sys.path`, não ganhará acesso aos dados. Quando localizar `.assistant`, confirme visualmente que ela contém `hub_snippets/`, `hub_scripts/`, `hub_prompts/` e `skills/` conforme a entrega disponível. A existência das pastas no Git e a permissão para abrir uma tabela continuam sendo verificações separadas.

<a id="mu02-2"></a>
#### 2. Abrir o exemplo, preparar o import e conferir dependências

Escolha uma primeira chamada que não exija Spark nem dados da empresa. A pasta [`format_br`](../../hub_snippets/constants/format_br/README.md) contém um README para decidir quando usar, a implementação `format_br.py`, a fachada `__init__.py` que expõe os nomes públicos e o notebook `exemplo_format_br.py`. **Fachada** é o arquivo que oferece um caminho curto de importação para as funções do objeto. Leia o README antes do exemplo: `fmt_pct` devolve texto para apresentação, não recalcula a taxa. O notebook demonstra mais funções e interpreta casos de escala; não é a biblioteca a importar. Para a primeira prova, use um valor fictício conhecido, `0.12`, representando 12% como fração.

O bloco a seguir é **ilustrativo**, para uma sessão em que `.assistant` esteja acessível como arquivos de workspace. Substitua a raiz pelo local confirmado da sua entrega. A verificação com `is_dir()` procura a pasta esperada antes de tentar importar; isso evita interpretar um erro de localização como defeito da função. A inserção condicional coloca a raiz uma única vez na lista de busca do Python. A documentação oficial sobre [módulos em arquivos de workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-modules) explica por que o diretório que contém um módulo precisa estar no caminho de importação e por que a pasta atual varia conforme runtime e contexto. O caminho absoluto torna esta receita mais explícita, especialmente quando o diretório de trabalho não é garantido.

```python
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if not (assistant_root / "hub_snippets").is_dir():
    raise FileNotFoundError(f"Cópia do Hub não encontrada em {assistant_root}")

if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from hub_snippets.constants.format_br import fmt_pct

taxa_fracao = 0.12
taxa_texto = fmt_pct(taxa_fracao)
print(taxa_texto)  # esperado: 12,0%
```

Observe o nível de pasta inserido: é `.assistant`, **a pasta que contém** `hub_snippets/`. Inserir `.../.assistant/hub_snippets` faria o Python procurar outro `hub_snippets` dentro dela. `from ... import fmt_pct` pede uma função pela fachada pública; ele não executa o notebook de exemplo nem lê uma tabela. A chamada ocorre na linha `fmt_pct(taxa_fracao)`. `print` apenas mostra o texto retornado. Se você estiver numa Git folder, a plataforma pode acrescentar diretórios ao caminho automaticamente em certas condições; ainda assim, confira qual módulo foi importado, porque outra cópia com o mesmo nome pode estar na frente. Não dependa de uma raiz presumida quando a entrega real é conhecida.

Leia o bloco em quatro movimentos. Primeiro, `Path` representa um endereço de arquivo; não cria a pasta. Segundo, `is_dir()` testa se a subpasta esperada está visível para aquela sessão. Terceiro, `sys.path.insert(0, ...)` informa ao Python onde procurar o pacote; o zero põe essa raiz antes de outras candidatas e por isso merece conferência quando houver cópias duplicadas. Quarto, o `import` carrega a interface do objeto, e só a chamada passa o número à função. Se a verificação inicial falhar, não avance para o import: o erro antecipado já diz que é preciso descobrir a localização certa ou solicitar acesso. Se ela passar, mas o import falhar, investigue o tipo do arquivo e a fachada antes de discutir a taxa.

O exemplo não pede que você execute o notebook de demonstração inteiro. Para **aprender** o que cada função entrega, leia primeiro seu texto e as saídas documentadas; para **testar** no seu ambiente, rode apenas a célula pequena que entende e cuja consequência conhece. Isso é especialmente útil quando outro objeto exige sessão Spark ou dados sintéticos persistidos pelo notebook. A demonstração de `format_br` separa apresentação numérica de cálculo; preservar o número original permite refazer uma média depois, enquanto a string com `%` serve para legenda ou resumo. Uma saída com vírgula brasileira é útil para leitura, mas não deve substituir a coluna numérica de origem.

Depois dessa prova leve, abra o [notebook de exemplo](../../hub_snippets/constants/format_br/exemplo_format_br.py) para entender outras funções e erros de escala. Antes de executar **qualquer** notebook de exemplo do Hub, leia seu README local: alguns exemplos preparam ou apagam tabelas sintéticas mesmo quando o helper principal é somente leitura. `format_br` não exige uma dependência opcional de ML para sua chamada; um snippet Spark, como `null_summary`, já exige PySpark e um DataFrame Spark. **Dependência** é uma biblioteca ou capacidade necessária para importar ou executar uma função. A lista de pacotes opcionais do Hub orienta investigação, mas não prova o que está instalado na sua sessão; confirme somente as dependências do objeto escolhido.

<a id="mu02-3"></a>
#### 3. Conferir compute, permissões e estado da entrega

**Compute** é o recurso de processamento ligado ao notebook. Uma chamada simples de formatação usa Python; uma função que opera sobre um **DataFrame Spark**, isto é, uma tabela manipulada por operações distribuídas, precisa de um ambiente com APIs Spark compatíveis. Antes de trocar o exemplo leve por uma consulta real, confirme qual compute está ativo, se a biblioteca exigida está disponível e se você tem permissão para ler o recurso. O fato de o notebook abrir não prova que um módulo Python pode ser importado; conseguir importar o módulo não prova que a tabela existe ou pode ser lida. Essas são etapas distintas e seus erros ajudam a localizar a falha.

**Serverless** é um modo em que a plataforma administra o compute sem você escolher e manter um cluster clássico para cada notebook. Em notebooks serverless padrão, a configuração de bibliotecas passa pelo painel **Environment**. Na experiência Git Folder Serverless descrita pela Databricks, as dependências são geridas por `pyproject.toml` na raiz da pasta Git; jobs têm configuração própria. A [documentação oficial de dependências serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies), reconferida em 7/10/2026, distingue essas rotas e alerta para não instalar PySpark sobre o ambiente serverless gerenciado. Isso não significa que você deva alterar o ambiente para testar `fmt_pct`: a primeira chamada foi escolhida justamente para não precisar de uma instalação adicional. Quando outro recurso exigir pacote opcional, consulte o README, a versão e o mecanismo adotado pela sua equipe antes de pedir ou fazer a mudança.

Serverless também tem limites de API que importam para módulos Spark: a [documentação de limitações](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations) informa suporte a Spark Connect e ausência de APIs RDD nesse modo. Um helper que usa uma API incompatível pode importar e falhar só quando for chamado. Em outro compute, a situação pode ser diferente. Não conclua “o Hub não funciona” por uma falha específica nem instale uma biblioteca aleatória para fazê-la desaparecer. Registre o nome da função, o compute, o erro e em que etapa ocorreu; esse conjunto permite decidir se o problema é caminho, pacote, API, dado ou permissão.

Para dados, faça a mesma separação. `catalogo.schema.tabela` é um exemplo de identificador completo no Unity Catalog, não uma tabela real deste manual. Uma **view temporária** pode existir só na sessão em que foi criada, enquanto uma tabela persistente tem escopo e permissões próprios. Se a chamada seguinte usar `spark.table(...)`, confirme catálogo, schema, nome, população e autorização de leitura. Uma mensagem de acesso negado não autoriza contornar a permissão com outra conta ou cópia do dado. Para operação que grava, além da leitura, é preciso conhecer destino, modo de escrita e impacto antes de executar; a receita deste capítulo não grava nada.

Por fim, compare o que foi **publicado** com o que você vê no Git. O mantenedor valida a fonte, gera o espelho e verifica o workspace por procedimentos próprios; o [playbook do projeto](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/README.md) lembra que o laboratório Free e o destino de trabalho exigem conferências separadas. Você, como usuário, pode verificar a pasta, abrir o README, importar um objeto e pedir ao responsável a versão distribuída. Não precisa rodar `render_simulado.py`, `publicar_free.py` ou o kit de transição para resolver um `ModuleNotFoundError` no notebook. Uma versão antiga da entrega pode explicar por que o nome mostrado no Git ainda não aparece na sua sessão. Quem mantém a instalação encontra o percurso completo em [MT28](MT-parte-vii.md#mt28).

Antes de uma chamada que envolva dados, faça uma conferência em linguagem comum: “consigo abrir o arquivo de código, meu compute aceita suas bibliotecas, tenho leitura da tabela completa, e sei o que a função retornará?”. Se uma resposta for desconhecida, localize o README do objeto ou peça ao responsável a informação específica. Essa pausa é mais eficaz que testar indiscriminadamente comandos de instalação ou consultas em tabelas semelhantes. Ela também evita confundir acesso de leitura ao arquivo com autorização para copiar, transformar ou persistir os dados.

<a id="mu02-4"></a>
#### 4. Interpretar a primeira saída e recuperar uma falha

Para o valor fictício escolhido, `fmt_pct(0.12)` deve mostrar `12,0%`. A verificação Python registrada na redação original desta edição produziu esse texto; a saída no seu workspace ainda depende de importar a mesma versão do módulo. A variável `taxa_fracao` continua numérica (`0.12`), e `taxa_texto` é uma **string**, ou texto para apresentação. Confira a unidade antes de aceitar o resultado: `fmt_pct(12)` com escala padrão trataria 12 como fração e mostraria `1200,0%`, sem necessariamente lançar erro. Uma célula que termina sem exceção não certifica que a taxa de origem tinha o denominador correto. Para um teste pequeno, compare com a aritmética 12 respostas em 100 contatos, mas não use esse exemplo como estimativa de sua tabela real.

Se a célula parar, identifique **onde** parou. `FileNotFoundError` lançado pelo bloco significa que a raiz indicada não contém `hub_snippets/`; confira endereço e materialização antes de mudar código. `ModuleNotFoundError` cujo nome ausente é `hub_snippets` sugere caminho, cópia incompleta ou arquivo importável publicado como notebook. Se o nome ausente for uma biblioteca opcional exigida por outro objeto, o caminho do Hub pode estar correto e o problema ser a dependência naquele compute. `ImportError` sobre `fmt_pct` pede conferir o `__init__.py` público e a versão do objeto. Um `ValueError` durante a chamada aponta para argumento recusado, como uma escala não aceita, e exige reler o contrato da função, não reinstalar a biblioteca.

Um diagnóstico simples ajuda a diferenciar cópias depois que o import funciona: em outra célula, `import inspect` carrega a biblioteca padrão de inspeção do Python; então `inspect.getfile(fmt_pct)` mostra o arquivo Python de onde veio a função. Use-o apenas para verificar a origem, sem expor caminhos pessoais em relatório compartilhado. Se apontar para uma cópia diferente, corrija o `sys.path` e reinicie ou recarregue a sessão conforme o ambiente antes de repetir a conferência; imports já carregados podem manter estado anterior. Se a origem estiver certa e o número estiver errado, investigue unidade, argumento e fórmula que produziu a taxa. MU06 amplia esse tipo de conferência para snippets; MU07 faz o mesmo para scripts com retornos próprios.

Ao pedir ajuda, copie o **tipo de falha e a etapa**, sem colar credenciais ou dados sensíveis: “o diretório existe, importei `format_br`, mas a saída foi `1200,0%` para uma taxa que esperava 12%” é uma pergunta melhor que “não funciona”. Diga também se está em serverless ou outro compute e se usou cópia de workspace ou Git folder. Essa informação permite escolher a próxima ação mínima: corrigir o caminho, pedir a publicação que falta, revisar a dependência, ou ajustar a escala. Mantenha o primeiro teste pequeno; ele existe para localizar a fronteira que falhou antes de você envolver uma tabela ou workflow inteiro.

<!-- editorial:exclude:start -->
**Fontes do produto:** [guia `.assistant`](../../README.md), [README de `format_br`](../../hub_snippets/constants/format_br/README.md), [implementação e API](../../hub_snippets/constants/format_br/format_br.py), [exemplo](../../hub_snippets/constants/format_br/exemplo_format_br.py), [marcador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/notebook_marker.py), [publicador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/publicar_free.py) e [manual técnico vigente](../../MANUAL_TECNICO.md#importacao). **Plataforma:** [workspace files](https://learn.microsoft.com/en-us/azure/databricks/files/workspace), [módulos](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-modules), [dependências serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies) e [limitações](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations), reconferidos em 7/10/2026.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU01](#mu01) · [Próximo: MU03](#mu03) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT03](MT-parte-i.md#mt03)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu03"></a>
<a id="mu03"></a>
### MU03 — Encontrar o recurso certo para a tarefa

**Pergunta deste capítulo:** o que o Hub oferece para aquilo que você precisa fazer? Use a busca manual quando já consegue reconhecer uma família de recursos; peça ajuda ao Concierge quando a intenção ainda precisa ser traduzida em uma rota. Em ambos os casos, a escolha só fica pronta depois que você confere a entrada, o resultado e o limite do objeto encontrado.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](MU-indice.md#sumario-mu) · [Escolher uma trilha](#mu01) · [Usar skills](MU-parte-ii.md#mu04) · [Arquitetura de contexto](MT-parte-i.md#mt04) · [Catálogo técnico de skills](MT-parte-iii.md#mt14)
<!-- editorial:exclude:end -->

<a id="mu03-1"></a>
#### 1. Traduzir uma necessidade em objetivo e entregável

Antes de procurar um nome no catálogo, escreva em uma frase a **decisão** que quer apoiar. “Ver nulos” é uma operação; “saber se a coluna de identificação serve como chave para juntar duas bases” já aponta o motivo da operação. Em seguida, nomeie o recurso disponível: tabela, notebook, modelo, relatório ou apenas uma descrição. Se houver tabela, diga o que uma linha representa, isto é, o **grão**. “Uma linha por cliente” e “uma linha por compra” mudam o significado de duplicidade, taxa e junção. Acrescente período, limites de acesso e a forma esperada da entrega: número, tabela de diagnóstico, notebook, plano ou explicação.

Esse pequeno contrato evita três escolhas precipitadas. Um **snippet** é uma função reutilizável que você importa para um cálculo ou apresentação pontual. Um **script** é uma unidade de operação maior, que pode checar, transformar ou produzir um artefato. Um **prompt** do Hub é um formulário que você preenche e entrega manualmente ao assistente; por si só, não acessa dados nem executa código. Uma **skill** é o roteiro de trabalho que pode orientar o Genie Code por seleção relevante ou menção explícita. Nenhum desses nomes indica sozinho que o recurso foi executado no seu ambiente. O [índice do produto](../../README.md) e o [catálogo de skills](../../skills/README.md) situam essas famílias.

Faça uma primeira triagem por tamanho da pergunta. Se você já tem um DataFrame e só precisa da contagem de nulos por coluna, procure uma função; se precisa investigar causas, recortes, gravidade e ação, uma **análise exploratória de dados (EDA)** ou um briefing de qualidade responde à pergunta mais ampla. A EDA examina estrutura, distribuições e possíveis problemas antes de uma decisão; o [briefing de EDA rápida](../../hub_prompts/eda_rapida/README.md) mostra quando começar por um perfil limitado. **DataFrame** é a tabela manipulada pelo código Spark ou Python, não o nome de uma tabela do catálogo. O fato de uma função ser rápida de chamar não a torna suficiente para decidir se a base pode entrar em produção.

Use um pedido curto e reproduzível como rascunho: “Quero avaliar nulos por coluna no DataFrame de clientes do mês de setembro, sem escrever tabela; espero um resumo para decidir quais campos investigar”. Se você não sabe o grão ou o período, escreva “não informado” e procure primeiro como obtê-los. Se nem a fonte pode ser identificada, peça uma orientação de descoberta, não uma taxa inventada. Essa formulação será a mesma ao seguir a busca manual ou ao consultar o Concierge, facilitando comparar as recomendações com a necessidade original.

<a id="mu03-2"></a>
#### 2. Percorrer o catálogo manualmente e ler o README local

Abra o [README de entrada da `.assistant`](../../README.md). Ele organiza snippets, scripts, prompts, skills, padrões, materiais visuais e a área de domínio [Micromodelos](../../hub_micromodelos/README.md). Para especificar uma característica ou descobrir oportunidades por metadados, consulte essa área e sua skill `hub-ml-micromodelos`; uma recomendação não autoriza leitura de registros nem publicação. Escolha a família pela tarefa, não pela palavra mais parecida com a sua pergunta. O [índice de snippets](../../hub_snippets/README.md) aponta funções curtas; o [índice de scripts](../../hub_scripts/README.md) reúne operações; o [índice de prompts](../../hub_prompts/README.md) explica quando um pedido estruturado ajuda; o catálogo de skills mostra roteiros de análise. O [manual técnico vigente](../../MANUAL_TECNICO.md) conecta fundamentos e nomes de helpers. Um item listado é candidato; o README da pasta do objeto é a próxima leitura obrigatória.

Para a checagem de nulos, encontre [`null_summary`](../../hub_snippets/spark/null_summary/README.md). Leia “para que serve”, pré-requisitos, assinatura e retorno antes de copiar um import. A função recebe um DataFrame Spark e devolve um DataFrame resumido; você ainda precisa decidir quais colunas são críticas e conferir o denominador de cada percentual. Se a tarefa for apenas exibir um diagnóstico numa sessão já autorizada, a rota pode ser o snippet isolado, descrita em [MU06](MU-parte-ii.md#mu06). A skill de EDA não é requisito para uma chamada direta e independente dessa função no notebook. Se a tarefa já selecionou uma EDA protegida, porém, o snippet não substitui seu runner nem permite contornar um bloqueio; confirme a rota antes de executar. Se a pergunta for “por que os nulos aumentaram e a base ainda serve para o modelo?”, a função pode fornecer evidência, mas a rota metodológica precisa de período, segmentos, comparação e conclusão.

O segundo exemplo começa com “a variável ficou instável?”. **Estabilidade** aqui significa comparar a distribuição de um atributo entre uma população de referência e outra atual. O **Population Stability Index (PSI)** resume a diferença entre essas distribuições em um indicador; seu valor exige conhecer população, faixas e período de comparação, e não mede sozinho a qualidade do modelo. O [README do calculador de PSI em Spark](../../hub_snippets/spark/psi_calculator/README.md) explica entradas, cálculo e limites; o [script de drift](../../hub_scripts/drift_detector/README.md) faz uma checagem operacional com suas próprias entradas e saídas. “Drift” nomeia a mudança observada; não indica automaticamente que o modelo piorou. Antes de escolher, defina a variável, as duas janelas, a população, o volume e se você quer um indicador pontual ou uma investigação de monitoramento. Para um plano amplo de acompanhamento, leia a skill [`hub-ml-monitoramento-modelo`](../../skills/hub-ml-monitoramento-modelo/SKILL.md). Seu estado atual na policy deve ser conferido; a descrição da skill não prova que já existe um monitor implantado.

No README local, responda a quatro perguntas práticas. Que objeto a chamada recebe? O que retorna ou escreve? Quais dependências e permissões existem? Como o exemplo deve ser executado? Um arquivo de exemplo pode preparar uma tabela sintética com `mode("overwrite")`, ação que substitui o destino se você rodar aquela parte. Ler o exemplo é seguro; executá-lo exige conferir destino e efeito. O [guia de primeiro uso](#mu02) distingue arquivo Python, notebook e tabela e explica por que importação não equivale a publicação. Se o README não resolver o seu caso, abra a implementação e o exemplo para confirmar assinatura e resultado, ou registre a dúvida para a rota assistida.

Ao terminar a busca manual, anote o caminho do objeto, a versão ou cópia consultada, a razão da escolha e uma condição de recusa. Por exemplo: “`null_summary` serve para medir nulos no DataFrame; não conclui se a coluna é aceitável para negócio”. Esse registro evita que um nome lembrado de conversa anterior seja tomado por evidência de disponibilidade na cópia atual. Também facilita pedir ao Concierge que compare alternativas sem repetir toda a investigação.

<a id="mu03-3"></a>
#### 3. Pedir uma rota ao Concierge e interpretar a resposta

O [Concierge](../../skills/hub-ml-concierge/SKILL.md) é uma skill de descoberta e composição. Você pode mencioná-la explicitamente com `@hub-ml-concierge` quando esse recurso estiver disponível no seu ambiente, ou pedir ao assistente para localizar opções; a presença da pasta no repositório não confirma instalação nem seleção nativa na sua sessão. **Seleção por relevância** é a possibilidade de o Genie Code escolher uma skill a partir da descrição do pedido; não há uma tabela rígida de palavras que garanta a escolha. Se você já escolheu o especialista correto, pode ir a ele diretamente. O Concierge não é um portão obrigatório nem executa o especialista ao recomendá-lo.

Um pedido útil contém objetivo, entrada, saída, restrições e o escopo que pode ser inspecionado. Por exemplo: “Com `@hub-ml-concierge`, encontre no Hub uma forma de medir nulos por coluna no DataFrame de clientes. Preciso somente de um resumo em memória, sem escrever tabela. Diga o caminho do recurso, os argumentos, o retorno, o que você conseguiu verificar e o próximo passo”. O caminho, e não apenas o nome, permite abrir o README indicado. Se você não anexou a cópia do Hub ou o assistente não pode ler os arquivos, a resposta deve declarar essa limitação; uma busca sem acesso não demonstra que o recurso está ausente.

A [descoberta progressiva](../../skills/hub-ml-concierge/references/descoberta.md) compara adequação, incompatibilidade e cobertura. O [modelo de recomendação](../../skills/hub-ml-concierge/templates/recomendacao.md) separa objetivo entendido, rota, recursos indicados, evidências, alternativas recusadas, confiança e próximo passo. A rota `HELPER_ROUTE` sugere que uma **interface de programação de aplicações (API)** reutilizável basta: neste contexto, é a função pública que o código chama, com entradas e retorno definidos, como `null_summary` para uma medição pontual. O [README da função](../../hub_snippets/spark/null_summary/README.md) permite conferir essa interface concreta. `DIRECT_ROUTE` aponta um componente principal que atende ao método ou briefing. `COMPOSITE_ROUTE` combina peças com papéis complementares; `BRIEFING_FIRST` pede definições faltantes antes de escolher. `GAP` significa que a busca não achou cobertura adequada **no escopo pesquisado**, e `ACCESS_BLOCKED` que o acesso impediu verificar candidatos. Essas etiquetas pertencem à saída da skill, não são comandos do Databricks.

Leia também a cobertura, que é independente da rota: `TOTAL_PARA_ESCOPO`, `PARCIAL` ou `NAO_DETERMINADA`. Uma rota direta pode cobrir apenas parte da pergunta. Se o Concierge recomendar “skill de monitoramento” para a palavra “estabilidade”, verifique se o pedido era comparar duas distribuições com PSI, investigar drift por vários segmentos ou desenhar operação contínua. A recomendação precisa indicar referência, período e volume ainda desconhecidos. Sem eles, aceite no máximo uma rota condicionada ou um briefing inicial, não um resultado de estabilidade. A [policy integrada](../../hub_padroes/skill_enforcement/policy.json) registra níveis atuais de enforcement; nível alvo não é capacidade presente.

Um exemplo de resposta **ilustrativa**, não gerada por uma execução do Concierge nesta obra, seria: “Rota `HELPER_ROUTE`, cobertura `PARCIAL`: `null_summary` mede nulos por coluna no DataFrame, mas a decisão de aceitar a fonte requer regra de negócio e período. Caminho verificado no README e no código; tabela do workspace não inspecionada. Próximo passo: conferir o DataFrame e chamar a função com amostra controlada”. Leia a frase como uma lista de verificações. Caminho verificado é evidência documental; número calculado exigiria execução real. “Confiança alta na adequação” expressa julgamento fundamentado, não probabilidade estatística de acerto. O [registro de busca](../../skills/hub-ml-concierge/templates/registro_busca.md) deve mostrar onde e quanto o agente procurou; busca top-k ou amostra não vira “varredura completa”.

<a id="uso-hub-ml-concierge"></a>
##### Ficha de uso — hub-ml-concierge

<!-- usage-card:start hub-ml-concierge -->
Escolha o Concierge quando conhece a necessidade, mas ainda não sabe se precisa de função, script, briefing ou skill especialista. Ele procura e recomenda caminhos; não executa a análise indicada. Informe objetivo, formato da entrada, saída pretendida, restrições e quais arquivos podem ser inspecionados. Se o acesso ao Hub não estiver disponível, a resposta deve manter essa limitação visível.

O pedido abaixo busca uma função pontual de nulos, com saída em memória. Antes de enviá-lo, substitua a descrição do DataFrame pelo recorte real e informe o pacote acessível. A entrega esperada é recomendação com caminhos, adequação, cobertura, alternativas e próxima ação; não é uma tabela de percentuais já calculados. Confira se o recurso indicado recebe sua entrada, se seu retorno responde à pergunta e se o agente declarou o escopo pesquisado. Abra a fonte recomendada para confirmar assinatura e requisitos. Uma cobertura parcial pode ser suficiente para a medição curta, mas não para decidir a qualidade de toda a base. Se faltar informação, aceite um briefing condicionado e resolva a lacuna antes de executar o especialista.

```text
@hub-ml-concierge
Tenho um DataFrame Spark autorizado, uma linha por evento no mês informado.
Quero medir nulos por coluna e receber somente um resumo em memória.
Busque na cópia acessível do Hub; não execute nem persista nesta etapa.
Indique caminho, entrada, retorno, cobertura, limites e próxima ação.
Se não puder ler o pacote, declare o acesso não verificado.
```
<!-- usage-card:end hub-ml-concierge -->

<a id="mu03-4"></a>
#### 4. Aceitar cobertura parcial e escolher a próxima ação

Uma boa recomendação pode terminar com lacuna. Suponha que o Concierge encontrou o PSI para comparar distribuições, mas não recebeu o mês de referência nem sabe se a variável está disponível nos dois períodos. A resposta deve apontar o helper e pedir as duas populações antes do cálculo. Ela pode registrar cobertura `PARCIAL` porque só parte da necessidade tem solução verificada e, independentemente, rota `BRIEFING_FIRST` porque faltam definições para escolher ou executar o próximo passo. Não complete silenciosamente a data com “mês anterior”: sazonalidade e mudança de público poderiam tornar a comparação enganosa. Se o assistente disser apenas “use o monitoramento”, peça o caminho exato, a pergunta que cada peça responde e o dado que falta.

Quando houver mais de um componente, solicite uma **composição mínima**: apenas peças necessárias, na ordem em que cada resultado alimenta a etapa seguinte. Para estabilidade, uma medição pontual de PSI pode vir antes da interpretação por segmento e do desenho de alertas; se não há operação contínua, não existe motivo para pressupor job, dashboard ou deploy. O [guia de composição do Concierge](../../skills/hub-ml-concierge/references/composicao.md) exige papéis e limites por objeto. O [template de handoff](../../skills/hub-ml-concierge/templates/handoff.md) ajuda a passar ao especialista apenas objetivo, entradas, restrições, evidências e pendências, sem converter sugestão em ação já realizada.

Antes de prosseguir, confira três coisas na sua cópia: o arquivo indicado existe e pode ser lido; seu README e sua assinatura correspondem à tarefa; a recomendação distingue o que foi lido, executado e ainda precisa de confirmação. Se o recurso não estiver acessível, registre o caminho tentado e peça ao responsável a cópia ou permissão correta. Se não houver cobertura comprovada, formule uma alternativa delimitada ou um pedido de diagnóstico, sem anunciar que “o Hub não tem” a capacidade em todas as versões. O [catálogo de skills](../../skills/README.md) orienta a próxima família, e [MU04](MU-parte-ii.md#mu04) explica como acompanhar uma skill depois de escolhê-la.

Por fim, trate simulação e ambiente real separadamente. Anexar `SKILL.md` ao chat pode ajudar o assistente a ler o método e produzir um plano; isso não prova que a skill foi descoberta automaticamente, instalada no workspace ou que algum gate de execução passou. A mesma disciplina vale na busca manual: um exemplo visto no repositório é uma referência para preparar sua ação, e uma conclusão só deve citar o dado, a execução e a validação que de fato ocorreram.

<!-- editorial:exclude:start -->
Fontes de referência: [entrada do produto](../../README.md), [Concierge](../../skills/hub-ml-concierge/SKILL.md), [descoberta](../../skills/hub-ml-concierge/references/descoberta.md), [recomendação](../../skills/hub-ml-concierge/templates/recomendacao.md), [registro de busca](../../skills/hub-ml-concierge/templates/registro_busca.md) e [policy atual](../../hub_padroes/skill_enforcement/policy.json).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU02](#mu02) · [Próximo: MU04](MU-parte-ii.md#mu04) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT14](MT-parte-iii.md#mt14)
<!-- editorial:exclude:end -->
