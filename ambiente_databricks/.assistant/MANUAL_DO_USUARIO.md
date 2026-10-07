# Manual do Usuário

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026.

<a id="apresentacao-mu"></a>
## Apresentação, público, escopo e base

Público: pessoas que precisam encontrar e usar os recursos do Hub em tarefas de trabalho.
Esta edição reúne integralmente capítulos, atlas e referências de consulta. A conferência documental não comprova execução dos exemplos, leitura humana iniciante, homologação visual ou operacional no Databricks. Cada evidência conserva o alcance e a data declarados no texto.
Base de referência: main 983c9936f139402a0130f290653ae713d65a3ac7; árvore 58c768a30dd62fb754aec2a3f1f5818f19ece21c; edição documental de 07/10/2026.
Arquivo desta edição: ambiente_databricks/.assistant/MANUAL_DO_USUARIO.md. O Manual Técnico V2 é a única edição técnica vigente, conforme ADR-0028.
[Leitura em partes](manuais_v2/partes/README.md) · [Outro manual](MANUAL_TECNICO_V2.md#sumario-mt) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [Glossário](MANUAL_TECNICO_V2.md#mt-mod-glossario)

<a id="sumario-mu"></a>
## Sumário por partes, capítulos e seções

- [Parte I — Primeiros passos](#parte-mu-i)
  - [MU01 — Conhecer o Hub e escolher sua trilha](#mu01)
    - [1. Começar pela decisão que você precisa tomar](#mu01-1)
    - [2. Reconhecer as peças pelo que você fará com elas](#mu01-2)
    - [3. Seguir uma trilha curta e testar sua escolha](#mu01-3)
    - [4. Pedir ajuda com contexto suficiente e reconhecer o próximo passo](#mu01-4)
  - [MU02 — Primeiro uso, ambiente e acesso aos recursos](#mu02)
    - [1. Localizar a cópia de uso e distinguir os objetos](#mu02-1)
    - [2. Abrir o exemplo, preparar o import e conferir dependências](#mu02-2)
    - [3. Conferir compute, permissões e estado da entrega](#mu02-3)
    - [4. Interpretar a primeira saída e recuperar uma falha](#mu02-4)
  - [MU03 — Encontrar o recurso certo para a tarefa](#mu03)
    - [1. Traduzir uma necessidade em objetivo e entregável](#mu03-1)
    - [2. Percorrer o catálogo manualmente e ler o README local](#mu03-2)
    - [3. Pedir uma rota ao Concierge e interpretar a resposta](#mu03-3)
      - [Ficha de uso — hub-ml-concierge](#uso-hub-ml-concierge)
    - [4. Aceitar cobertura parcial e escolher a próxima ação](#mu03-4)
- [Parte II — Escolher e usar recursos](#parte-mu-ii)
  - [MU04 — Usar skills do pedido à entrega revisada](#mu04)
    - [1. Escolher a skill e observar a seleção](#mu04-1)
    - [2. Dar contexto, pedir plano e delimitar a execução](#mu04-2)
    - [3. Ler níveis, gates e evidência da entrega](#mu04-3)
    - [4. Compor recursos e recuperar uma resposta fora do fluxo](#mu04-4)
  - [MU05 — Escolher e preencher os 18 briefings](#mu05)
    - [1. Registrar objetivo, fonte, grão, chaves, tempo e desconhecidos](#mu05-1)
    - [2. Escolher entre as rotas de briefing](#mu05-2)
      - [`auditoria_skills` — conferir implementação ou resultado](#mu05-route-auditoria-skills)
      - [`comentar_notebook` — documentar código existente](#mu05-route-comentar-notebook)
      - [`cross_eda` — avaliar fontes em conjunto](#mu05-route-cross-eda)
      - [`data_quality` — transformar suspeitas em regras](#mu05-route-data-quality)
      - [`eda_completa` — aprofundar uma fonte](#mu05-route-eda-completa)
      - [`explainability` — explicar um modelo identificado](#mu05-route-explainability)
      - [`feature_engineering` — desenhar atributos no tempo](#mu05-route-feature-engineering)
      - [`monitoramento_modelo` — investigar mudança operacional](#mu05-route-monitoramento-modelo)
      - [`micromodelo_novo` — especificar um objetivo conhecido](#mu05-route-micromodelo-novo)
      - [`descobrir_micromodelos` — explorar oportunidades delimitadas](#mu05-route-descobrir-micromodelos)
    - [3. Preencher, enviar e acompanhar os exemplos](#mu05-3)
      - [`eda_rapida` — primeiro perfil de uma tabela](#mu05-route-eda-rapida)
      - [`comparar_tabelas` — reconciliar A e B](#mu05-route-comparar-tabelas)
      - [`baseline_orchestration` — definir uma linha de base](#mu05-route-baseline-orchestration)
      - [`novo_projeto` — estruturar o início](#mu05-route-novo-projeto)
      - [`pipeline` — planejar fluxo de dados](#mu05-route-pipeline)
      - [`safra` — comparar coortes com maturidade igual](#mu05-route-safra)
      - [`stat_check` — testar uma hipótese delimitada](#mu05-route-stat-check)
      - [`tutor_explicar` — aprender com objeto real](#mu05-route-tutor-explicar)
    - [4. Conferir a resposta e corrigir lacunas](#mu05-4)
  - [MU06 — Usar um snippet isoladamente](#mu06)
    - [1. Escolher a função e ler seus requisitos](#mu06-1)
    - [2. Preparar o import e fazer uma chamada pequena](#mu06-2)
    - [3. Interpretar o retorno e conferir com poucos dados](#mu06-3)
    - [4. Resolver falhas e escolher uma alternativa proporcional](#mu06-4)
      - [Fontes e estado dos exemplos](#mu-mod-mu06-h-fontes-e-estado-dos-exemplos)
  - [MU07 — Usar um script isoladamente](#mu07)
    - [1. Qual dos oito scripts escolher?](#mu07-1)
    - [2. Como preparar e executar uma chamada pontual](#mu07-2)
    - [3. O que conferir no retorno de cada tipo?](#mu07-3)
    - [4. O que fazer diante de alerta, erro ou resultado estranho?](#mu07-4)
      - [Fontes e continuação](#mu-mod-mu07-h-fontes-e-continuação)
- [Parte III — Tarefas de análise](#parte-mu-iii)
  - [MU08 — Conhecer uma base: EDA, perfil e qualidade](#mu08)
    - [1. Que pergunta e população vão orientar a exploração?](#mu08-1)
    - [2. Quando pedir EDA completa e quando fazer uma verificação curta?](#mu08-2)
      - [Ficha de uso — hub-ml-eda-profissional](#uso-hub-ml-eda-profissional)
    - [3. Como fazer uma exploração direta com perfil, qualidade e prévia?](#mu08-3)
      - [Fontes desta parte](#mu-mod-mu08-h-fontes-desta-parte)
    - [4. Como transformar a exploração em decisão e passar o trabalho adiante?](#mu08-4)
      - [Fontes desta parte](#mu-mod-mu08-h-fontes-desta-parte-1)
  - [MU09 — Comparar e cruzar fontes com cuidado temporal](#mu09)
    - [1. Que chaves, grão e período cada fonte realmente possui?](#mu09-1)
    - [2. Como comparar as tabelas e usar a orientação de cross-EDA?](#mu09-2)
      - [Ficha de uso — hub-ml-cross-eda-ml](#uso-hub-ml-cross-eda-ml)
    - [3. Como diagnosticar expansão e escolher a versão disponível no tempo?](#mu09-3)
      - [Fontes desta parte](#mu-mod-mu09-h-fontes-desta-parte)
    - [4. Como interpretar multiplicação, perda, empate e bloqueio?](#mu09-4)
      - [Fontes desta parte](#mu-mod-mu09-h-fontes-desta-parte-1)
  - [MU10 — Preparar features, RFV, safra e estudos estatísticos](#mu10)
    - [1. Preciso desenhar uma feature, calcular RFV, comparar safras ou testar uma hipótese?](#mu10-1)
      - [Ficha de uso — hub-ml-feature-engineering](#uso-hub-ml-feature-engineering)
    - [2. Que data de referência e denominador tornam o estudo válido?](#mu10-2)
      - [Ficha de uso — hub-ml-analise-safra](#uso-hub-ml-analise-safra)
    - [3. Como executar cada rota sem pedir ao helper mais do que ele entrega?](#mu10-3)
      - [Fontes desta parte](#mu-mod-mu10-h-fontes-desta-parte)
      - [Ficha de uso — hub-ml-validacao-estatistica](#uso-hub-ml-validacao-estatistica)
    - [4. Como interpretar denominadores, efeito e incerteza para decidir o próximo passo?](#mu10-4)
      - [Fontes desta parte](#mu-mod-mu10-h-fontes-desta-parte-1)
  - [MU11 — Construir e revisar um baseline de ML](#mu11)
    - [1. Que decisão o primeiro modelo deve ajudar a comparar?](#mu11-1)
    - [2. Como preparar a base e escolher uma família compatível?](#mu11-2)
      - [Ficha de uso — hub-ml-baseline-ml](#uso-hub-ml-baseline-ml)
    - [3. Como pedir a skill e chamar um helper sem perder o controle do treino?](#mu11-3)
    - [4. Como ler métricas, registrar o run e decidir o próximo passo?](#mu11-4)
  - [MU12 — Explicar resultados e acompanhar modelos](#mu12)
    - [1. Preciso explicar uma predição ou acompanhar uma mudança?](#mu12-1)
      - [Ficha de uso — hub-ml-explainability](#uso-hub-ml-explainability)
    - [2. Que modelo, população, período e referência devo informar?](#mu12-2)
      - [Ficha de uso — hub-ml-monitoramento-modelo](#uso-hub-ml-monitoramento-modelo)
    - [3. Que helper uso para SHAP, relatórios, curvas, drift e desempenho?](#mu12-3)
    - [4. Como reagir a alertas sem transformar sinal em ordem automática?](#mu12-4)
- [Parte IV — Micromodelos](#parte-mu-iv)
  - [MU13 — Elaborar e revisar um micromodelo no estágio disponível](#mu13)
    - [1. Que pergunta uma linha do micromodelo responde?](#mu13-1)
    - [2. Como preencher o YAML sem completar lacunas com ficção?](#mu13-2)
    - [3. O que cada verificação demonstra?](#mu13-3)
    - [4. Como corrigir um diagnóstico sem falsificar a evidência?](#mu13-4)
- [Parte V — Entregas visuais](#parte-mu-v)
  - [MU14 — Planejar uma entrega visual e aplicar temas](#mu14)
    - [MU14.1 — Comece pela pergunta, pelo público e pela forma](#mu14-1)
    - [MU14.2 — Escolha referência, proposta e contexto](#mu14-2)
    - [MU14.3 — Aplique a uma figura e compare](#mu14-3)
    - [MU14.4 — Revise unidade, consistência e leitura real](#mu14-4)
  - [MU15 — Montar um notebook visual completo](#mu15)
    - [MU15.1 — Abertura, seções e índice honesto](#mu15-1)
    - [MU15.2 — Orientação visual, badges e indicadores já calculados](#mu15-2)
    - [MU15.3 — Tabela pequena, distribuições, correlação e curvas quando couberem](#mu15-3)
    - [MU15.4 — Revisar, compartilhar e exportar com o alcance correto](#mu15-4)
  - [MU16 — Usar cabeçalhos e figuras dos Visual Assets](#mu16)
    - [MU16.1 — Escolher CRM ou Squad e uma figura pela finalidade](#mu16-1)
    - [MU16.2 — Inserir o PNG a partir do documento que o usa](#mu16-2)
    - [MU16.3 — Texto alternativo, legenda e conferência de leitura](#mu16-3)
    - [MU16.4 — Recuperar imagem ausente e encaminhar alterações](#mu16-4)
  - [MU17 — Experimentar e entregar uma proposta visual](#mu17)
    - [MU17.1 — Decidir entre consumo, Lab, App, AI/BI e manutenção editorial](#mu17-1)
    - [MU17.2 — Abrir o Visual Lab, ajustar, comparar e exportar JSON](#mu17-2)
    - [MU17.3 — App de autoria e ponte AI/BI: o que cada uma entrega](#mu17-3)
    - [MU17.4 — Variante editorial, revisão, evidência e encaminhamento](#mu17-4)
- [Parte VI — Criação, distribuição e diagnóstico](#parte-mu-vi)
  - [MU18 — Documentar, criar e auditar objetos do Hub](#mu18)
    - [MU18.1 — Comentar notebook ou ensinar seu contexto](#mu18-1)
      - [Ficha de uso — comentar notebook](#uso-hub-ml-comentar-notebook)
      - [Ficha de uso — tutor Databricks](#uso-hub-ml-tutor-databricks)
    - [MU18.2 — Escolher template e criar um dos seis tipos](#mu18-2)
      - [Ficha de uso — criar objeto](#uso-hub-ml-criar-objeto)
      - [Ficha de uso — planejar pipeline](#uso-hub-ml-pipeline-builder)
    - [MU18.3 — README, exemplo e critérios de aceite](#mu18-3)
    - [MU18.4 — Auditar evidência e corrigir desvios](#mu18-4)
      - [Ficha de uso — auditar skill ou output](#uso-hub-ml-auditoria-skills)
  - [MU19 — Instalar, atualizar e compartilhar uma entrega](#mu19)
    - [MU19.1 — Defina pessoas, escopo e destino](#mu19-1)
    - [MU19.2 — Valide a fonte, regenere o espelho e monte o kit](#mu19-2)
    - [MU19.3 — Planeje, importe em staging e confira por camadas](#mu19-3)
    - [MU19.4 — Atualize com ponto de retorno e relate o resultado](#mu19-4)
  - [MU20 — Resolver problemas e concluir um percurso com evidência](#mu20)
    - [1. Em que fase ocorreu o erro?](#mu20-1)
    - [2. O que fazer quando o contrato bloqueia ou o resultado parece pronto?](#mu20-2)
    - [3. Como resolver uma falha visual e pedir ajuda que permita reproduzi-la?](#mu20-3)
    - [4. Como ir do objetivo a um relatório revisado sem esconder efeitos?](#mu20-4)

### Guias, atlas e referências

- [Guia de leitura do Manual do Usuário](#mu-mod-guia-leitura-usuario)
  - [Comece pela decisão que precisa tomar](#mu-mod-guia-leitura-usuario-h-comece-pela-decisão-que-precisa-tomar)
  - [Escolha quanto do procedimento precisa usar](#mu-mod-guia-leitura-usuario-h-escolha-quanto-do-procedimento-precisa-usar)
  - [Leia exemplos como exercícios verificáveis](#mu-mod-guia-leitura-usuario-h-leia-exemplos-como-exercícios-verificáveis)
  - [Volte à etapa em que apareceu a dificuldade](#mu-mod-guia-leitura-usuario-h-volte-à-etapa-em-que-apareceu-a-dificuldade)
  - [Prepare uma entrega que outra pessoa consiga continuar](#mu-mod-guia-leitura-usuario-h-prepare-uma-entrega-que-outra-pessoa-consiga-continuar)
  - [Rotas de consulta](#mu-mod-guia-leitura-usuario-h-rotas-de-consulta)

<a id="perguntas-mu"></a>
## Encontre uma seção pela pergunta

- qual caminho serve para minha necessidade e meu nível de experiência? [1. Começar pela decisão que você precisa tomar](#mu01-1)
- como sei que estou no ambiente certo e tenho acesso ao que vou usar? [1. Localizar a cópia de uso e distinguir os objetos](#mu02-1)
- o que o Hub oferece para aquilo que preciso fazer? [1. Traduzir uma necessidade em objetivo e entregável](#mu03-1)
- o que devo informar, acompanhar e conferir ao usar uma skill? [1. Escolher a skill e observar a seleção](#mu04-1)
- qual formulário usar e como completar campos sem inventar informação? [1. Registrar objetivo, fonte, grão, chaves, tempo e desconhecidos](#mu05-1)
- como usar uma função diretamente e saber se ela responde à pergunta certa? [1. Escolher a função e ler seus requisitos](#mu06-1)
- como fazer uma checagem ou transformação sem pedir uma análise completa à IA? [1. Qual dos oito scripts escolher?](#mu07-1)
- como conhecer dados e registrar se estão prontos para o próximo estudo? [1. Que pergunta e população vão orientar a exploração?](#mu08-1)
- o cruzamento preserva entidades, linhas e informação disponível naquele momento? [1. Que chaves, grão e período cada fonte realmente possui?](#mu09-1)
- como transformar a pergunta de negócio em estudo com tempo e pressupostos claros? [1. Preciso desenhar uma feature, calcular RFV, comparar safras ou testar uma hipótese?](#mu10-1)
- como preparar, treinar e revisar uma primeira referência de modelo? [1. Que decisão o primeiro modelo deve ajudar a comparar?](#mu11-1)
- como comunicar desempenho, estabilidade e explicações de forma útil? [1. Preciso explicar uma predição ou acompanhar uma mudança?](#mu12-1)
- o que já posso especificar e revisar sem depender da esteira futura? [1. Que pergunta uma linha do micromodelo responde?](#mu13-1)
- qual aparência ajuda esta entrega e como aplicar uma configuração válida? [MU14.1 — Comece pela pergunta, pelo público e pela forma](#mu14-1)
- como compor uma análise visual legível do título à conclusão? [MU15.1 — Abertura, seções e índice honesto](#mu15-1)
- como usar o material visual pronto sem copiar ou quebrar suas referências? [MU16.1 — Escolher CRM ou Squad e uma figura pela finalidade](#mu16-1)
- como experimentar e entregar uma proposta visual sem confundir exportação com aprovação? [MU17.1 — Decidir entre consumo, Lab, App, AI/BI e manutenção editorial](#mu17-1)
- como transformar uma solução local em objeto compreensível e revisável? [MU18.1 — Comentar notebook ou ensinar seu contexto](#mu18-1)
- para quem mantém o ambiente, qual sequência prepara e confere uma instalação? [MU19.1 — Defina pessoas, escopo e destino](#mu19-1)
- como sair de um sintoma para uma correção sem perder o que foi observado? [1. Em que fase ocorreu o erro?](#mu20-1)

<a id="trilhas-mu"></a>
## Trilhas de leitura

- Iniciante: [MU01](#mu01) → [MU02](#mu02) → [MU03](#mu03) → [MU06](#mu06) → [MU07](#mu07) → [MU08](#mu08)
- Usuário recorrente: [MU03](#mu03) → [MU04](#mu04) → [MU05](#mu05) → [MU08](#mu08) → [MU09](#mu09) → [MU10](#mu10) → [MU11](#mu11) → [MU12](#mu12) → [MU20](#mu20)
- Mantenedor: [MU18](#mu18) → [MU19](#mu19) → [MU20](#mu20)

### Ponte para o glossário técnico

[Consulte as definições desenvolvidas no glossário do Manual Técnico V2](MANUAL_TECNICO_V2.md#mt-mod-glossario).

<!-- editorial:exclude:end -->


<a id="mu-mod-guia-leitura-usuario"></a>
<a id="mu-mod-guia-leitura-usuario-h-guia-de-leitura-do-manual-do-usuário"></a>
## Guia de leitura do Manual do Usuário


<a id="mu-mod-guia-leitura-usuario-h-comece-pela-decisão-que-precisa-tomar"></a>
### Comece pela decisão que precisa tomar

Este manual pode acompanhar uma primeira experiência completa ou uma consulta
durante o trabalho. Para escolher um ponto de entrada, transforme sua necessidade
numa frase que termine com uma decisão: conhecer uma base para decidir se ela
serve ao estudo; comparar fontes para decidir se o cruzamento é confiável; montar
um visual para comunicar uma conclusão. Essa pequena preparação ajuda a escolher
o capítulo e a reconhecer quando a tarefa terminou. “Quero usar Python” descreve
uma ferramenta; “quero descobrir quais campos têm ausência e como isso afeta a
análise” descreve uma pergunta que o livro consegue encaminhar.

Se ainda não conhece o ambiente, percorra os capítulos iniciais na ordem. Eles
ensinam a localizar recursos, separar arquivos de dados e preparar o primeiro
uso. Nas consultas seguintes, entre pela pergunta do sumário. Você pode ler uma
receita específica sem repetir o livro inteiro, desde que confira os seus
pré-requisitos. Uma indicação de leitura anterior significa que aquela decisão
ou preparação será usada no procedimento; não significa executar novamente
todas as análises anteriores numa mesma sessão.

Ao abrir um capítulo, procure primeiro a pergunta, a rota indicada e o resultado
esperado. Depois leia a explicação dos termos necessários e a receita completa.
Reserve os detalhes de exceção para a etapa em que eles se aplicam, mas leia os
efeitos antes de executar código: um exemplo pode criar dados de demonstração,
instalar uma dependência ou iniciar um registro de execução. A explicação desses
efeitos faz parte da receita. O fato de um comando aparecer num manual não
define, sozinho, o destino adequado para o seu ambiente.

<a id="mu-mod-guia-leitura-usuario-h-escolha-quanto-do-procedimento-precisa-usar"></a>
### Escolha quanto do procedimento precisa usar

Algumas perguntas cabem numa função auxiliar isolada. Outras exigem um roteiro
com escolhas de população, tempo, qualidade e forma de entrega. Os capítulos
mostram essas duas possibilidades. Quando você já conhece a pergunta, os dados e
a interface de um recurso, siga a receita de uso isolado. Quando precisa de
ajuda para organizar decisões e produzir uma análise revisável, siga a receita
da skill pertinente. Uma skill é um conjunto de orientações e recursos para um
tipo de trabalho; sua seleção não demonstra que os dados já foram analisados.

Descreva também o tipo de ajuda desejado. Pedir uma explicação, um plano, código
para revisar ou execução produz expectativas diferentes. Se quer aprender sem
acionar cálculo, diga isso no pedido. Se quer executar, informe os recursos
autorizados e os limites conhecidos. Ao conferir a resposta, veja se ela ficou
no modo solicitado e se apresenta as evidências correspondentes. Um plano pode
ser uma boa entrega de planejamento; uma célula escrita pode ser uma boa entrega
de código. Para reconhecer uma análise executada, você precisa dos resultados e
das verificações que pertencem àquela rota.

Um briefing pronto ajuda a organizar o pedido, mas ainda precisa dos seus
valores. Leia cada campo antes de substituir um marcador. Uma tabela identificada
por catálogo, schema e nome é diferente de uma view temporária da sessão; uma
data de ocorrência é diferente da data em que o dado ficou disponível. Se não
souber uma informação necessária, registre a pendência e explique quem pode
resolvê-la. Preencher um campo com um valor inventado cria um pedido aparentemente
completo e uma análise que responde a outra pergunta.

<a id="mu-mod-guia-leitura-usuario-h-leia-exemplos-como-exercícios-verificáveis"></a>
### Leia exemplos como exercícios verificáveis

Os exemplos pequenos permitem acompanhar o raciocínio antes de usar uma base
grande. Observe os valores de entrada, a chamada e a interpretação da saída.
Faça a conta simples quando houver números: qual é o denominador de uma taxa,
quantas entidades foram incluídas, qual data limita o histórico e em qual escala
está o percentual? Essa leitura transforma o exemplo numa ferramenta de
aprendizado. Copiar apenas a chamada elimina justamente as decisões que tornam
o resultado compreensível.

Considere uma tabela de três decisões que você pretende cruzar com outra fonte.
Uma decisão encontra duas versões, outra não encontra correspondência e a
terceira não tem chave. O total depois de um cruzamento pode parecer próximo do
total original, mas ainda existe multiplicação e perda de fatos. O exemplo de
joins ensina a examinar essas causas separadamente. Ao transportar a receita
para o trabalho, preserve a pergunta sobre a unidade de cada linha. Uma tabela
que ficou maior não demonstra, por si, que você obteve mais informação válida.

O mesmo cuidado vale para gráficos. Veja primeiro o que foi calculado e depois
como foi apresentado. Alterar cor, título ou tema não deve mudar amostra, unidade
ou denominador. Se uma figura parece comunicar outra conclusão após uma mudança
visual, confira escala, seleção de dados, legenda e destaque. Os capítulos
visuais apresentam uma sequência de planejamento, construção, comparação e
revisão; você pode usar essa sequência mesmo quando escolhe manter a aparência
existente.

Resultados ilustrativos explicam o comportamento esperado sob condições
declaradas. Resultados observados registram uma execução identificável. Mantenha
essa diferença ao escrever suas próprias notas. Se executou apenas o exemplo
local, descreva esse alcance. Se adaptou o código e ainda não rodou, registre a
adaptação como proposta. Outra pessoa precisa conseguir reconhecer o que pode
reutilizar como evidência e o que ainda depende de verificação.

<a id="mu-mod-guia-leitura-usuario-h-volte-à-etapa-em-que-apareceu-a-dificuldade"></a>
### Volte à etapa em que apareceu a dificuldade

Quando o procedimento falhar, localize a etapa antes de trocar de recurso.
Arquivo não encontrado pede conferir caminho e cópia instalada. Importação que
falha pede conferir a raiz da biblioteca e a dependência pertinente. Argumento
recusado pede conferir a assinatura e o valor fornecido. Uma saída inesperada
pede revisar população, filtros, unidades e hipóteses. Essas situações têm
recuperações diferentes; o quadro de erros de cada capítulo ajuda a escolher a
próxima ação sem repetir trabalho desnecessário.

Se estiver usando uma skill com mecanismo obrigatório de verificação, leia o
estado retornado e a recuperação indicada. Um bloqueio identifica uma condição
que precisa ser resolvida na mesma rota. A ausência de finalização significa que
o trabalho ainda não recebeu autorização de conclusão por aquele mecanismo.
Uma mensagem bem escrita ou um gráfico plausível não substitui essa etapa. Em
contrapartida, uma função de diagnóstico pode apenas devolver alertas para você
interpretar. O manual identifica o alcance de cada recurso para evitar tratar
todo aviso como bloqueio ou todo resultado como aprovação.

Você também pode encontrar um recurso descrito como candidato ou uma superfície
que depende de instalação e autorização. Leia a condição antes de tentar o
procedimento. Use as alternativas documentadas que atendam à sua tarefa e
registre o limite encontrado. Se uma funcionalidade ainda não está disponível,
o livro pode ensinar a preparar uma proposta ou interpretar seus arquivos; isso
não torna aquela funcionalidade operacional no seu workspace.

<a id="mu-mod-guia-leitura-usuario-h-prepare-uma-entrega-que-outra-pessoa-consiga-continuar"></a>
### Prepare uma entrega que outra pessoa consiga continuar

Ao terminar, faça uma leitura breve como se estivesse recebendo seu próprio
trabalho. A pergunta foi respondida? As entradas e os recortes estão claros? Os
números têm unidade e denominador? A pessoa consegue distinguir dados completos,
amostra, ausência e resultado negativo? Os limites que podem mudar a decisão
ficaram próximos da conclusão? Essa revisão é útil para uma tabela pequena,
um notebook longo e uma entrega visual.

Registre também a próxima ação. Ela pode ser usar o resultado, corrigir uma
entrada, resolver uma decisão de domínio ou pedir revisão especializada. Quando
houver escrita ou compartilhamento, confira destino, modo e alcance antes da
ação. Para consultas futuras, guarde a identificação dos recursos e a versão da
entrega. O objetivo é permitir que alguém continue o trabalho sem reconstruir
intenções a partir de células soltas ou de uma conversa esquecida.

O Manual Técnico V2 serve como complemento quando você precisar entender a
construção de um recurso, seu contrato e suas limitações internas. Continue pelo
Manual do Usuário enquanto a pergunta principal for como realizar a tarefa. As
pontes entre os livros permitem aprofundar um ponto específico sem transformar
toda consulta prática numa investigação da arquitetura.

<!-- editorial:exclude:start -->
<a id="mu-mod-guia-leitura-usuario-h-rotas-de-consulta"></a>
### Rotas de consulta

| Necessidade | Capítulos |
|---|---|
| Conhecer, preparar acesso e escolher recursos | [MU01](#mu01), [MU02](#mu02), [MU03](#mu03) |
| Usar uma skill ou preencher briefing | [MU04](#mu04), [MU05](#mu05) |
| Usar uma função ou um script isoladamente | [MU06](#mu06), [MU07](#mu07) |
| Conhecer dados e cruzar fontes | [MU08](#mu08), [MU09](#mu09) |
| Preparar features, estudos e modelos | [MU10](#mu10), [MU11](#mu11), [MU12](#mu12) |
| Trabalhar com micromodelos | [MU13](#mu13) |
| Planejar e construir uma entrega visual | [MU14](#mu14), [MU15](#mu15), [MU16](#mu16), [MU17](#mu17) |
| Criar, documentar e compartilhar | [MU18](#mu18), [MU19](#mu19) |
| Resolver problemas e percorrer o fluxo completo | [MU20](#mu20) |

[Índice completo](#sumario-mu) · [Referência técnica](MANUAL_TECNICO_V2.md#sumario-mt).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [Outro manual](MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<!-- editorial:exclude:start -->
<a id="parte-mu-i"></a>
## Parte I — Primeiros passos
<!-- editorial:exclude:end -->


<a id="mu-mod-mu01"></a>
<a id="mu01"></a>
### MU01 — Conhecer o Hub e escolher sua trilha

**Pergunta deste capítulo:** qual recurso do Hub ajuda na sua tarefa de hoje e por onde começar sem precisar conhecer todo o projeto? Você pode usar este capítulo para escolher uma rota e formular seu primeiro pedido. Ainda não é necessário programar nem executar uma análise.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](#sumario-mu) · [Primeiro uso](#mu02) · [Catálogo e Concierge](#mu03) · [Por que o Hub existe](MANUAL_TECNICO_V2.md#mt01)
<!-- editorial:exclude:end -->

<a id="mu01-1"></a>
#### 1. Começar pela decisão que você precisa tomar

Imagine que alguém lhe entregou uma tabela de contatos de campanha e pediu uma recomendação para o próximo mês. Antes de pensar em modelo ou gráfico, você precisa saber o que há em cada linha, se o mesmo contato aparece mais de uma vez, que período está coberto e qual pergunta a análise deve responder. O Hub reúne orientações e recursos para transformar esse começo vago em trabalho conferível. Ele oferece métodos para conversar com o assistente, formulários para declarar contexto, código reutilizável e exemplos que ensinam a ler a saída. O [guia do ecossistema](README.md) apresenta essas peças e suas rotas de uso.

O ganho mais simples é parar de reconstruir uma checagem conhecida a cada notebook. Outro ganho é lembrar decisões que um pedido curto costuma omitir: unidade de cada linha, momento em que uma informação estava disponível, custo de consultar uma tabela e limite do resultado. A presença do Hub, porém, não verifica automaticamente a sua base nem torna correta qualquer resposta da IA. Você continua responsável por reconhecer o dado, conferir a execução, interpretar o resultado e decidir o próximo passo. Se ainda não sabe qual tabela ou qual decisão está em jogo, a primeira ação pode ser esclarecer isso, sem rodar código.

Neste manual, **Genie Code** é o assistente com o qual você pode conversar no Databricks. O Hub usa mecanismos de instrução e Agent Skills oferecidos pela plataforma e acrescenta conteúdo próprio: skills `hub-ml-*`, prompts, snippets, scripts e padrões. As duas coisas convivem, mas têm efeitos diferentes. Abrir um chat pode disponibilizar certas instruções e sugerir uma skill pertinente; não faz toda a pasta `.assistant` ser lida nem executa cada função nela. Quando um notebook precisa de uma função auxiliar, seu código ainda tem de importá-la e chamá-la. A distinção protege você de concluir “o Hub fez a verificação” apenas porque um recurso apareceu na conversa.

Uma boa frase de partida contém **objetivo e evidência desejada**: “quero saber se esta tabela pode sustentar uma análise de resposta; preciso de contagens de nulos, duplicatas e período, sem alterar a fonte”. Essa frase permite escolher um diagnóstico curto. “Quero entender a população, distribuições, lacunas e riscos antes de recomendar uma ação” pede um percurso de exploração mais amplo. Ambas são tarefas legítimas; a segunda precisa de mais contexto e interpretação. Ao terminar este capítulo, você poderá explicar essa diferença sem memorizar nomes de pastas.

<a id="mu01-2"></a>
#### 2. Reconhecer as peças pelo que você fará com elas

Uma **skill** organiza um método de trabalho para o assistente: que perguntas fazer, que passos seguir, quais recursos considerar e que limites declarar. **Análise exploratória de dados (EDA)** é o percurso para conhecer estrutura, distribuições, lacunas e relações de uma fonte. Se você está recebendo uma base nova e quer essa exploração orientada, `@hub-ml-eda-profissional` é uma rota possível. Você pode selecionar uma skill explicitamente com `@`; a plataforma também pode considerar sua descrição para escolhê-la quando pertinente. Essa seleção não prova que todas as etapas foram cumpridas. Leia o plano proposto e, depois, a evidência do que foi de fato executado. Para uma dúvida pequena, como “o que significa esta coluna?”, não é preciso abrir uma análise completa.

Um **prompt** é um briefing que você abre, preenche e fornece ao chat. Ele ajuda a informar tabela, período, grão, restrições e entrega esperada quando seria fácil omitir algum campo. O prompt não é descoberto automaticamente só porque está em `hub_prompts/`. Se um campo não é conhecido, declare `NÃO INFORMADO` e peça inspeção ou esclarecimento; `NÃO APLICÁVEL` só cabe quando você avaliou a pergunta e ela realmente não se aplica. Preencher um formulário não concede acesso à tabela nem garante que o assistente executou o código solicitado.

Um **snippet** é uma função ou classe Python que você usa no seu próprio notebook. Por exemplo, `format_br` oferece uma função para mostrar uma taxa já calculada como texto brasileiro. Ela não precisa de skill: você localiza a cópia acessível do Hub, importa a função, chama com a escala correta e confere o texto. Um **script** também é chamado explicitamente, mas costuma ser um utilitário delimitado de inspeção, transformação ou governança. `data_quality_check` pode devolver um diagnóstico de uma tabela. Outros scripts têm retornos diferentes, inclusive tabela de features ou texto de schema; leia o README e a assinatura do candidato antes de compor seu fluxo. MU06 e MU07 ensinam as duas rotas diretas.

Um **padrão** é um molde para quem vai criar ou documentar uma peça do Hub. Consultá-lo ajuda a não inventar um formato novo para README, exemplo ou API; ele não é uma análise pronta. Um **notebook de exemplo** mostra uma situação com código e interpretação, mas precisa ser lido antes de executar, porque o exemplo pode preparar dados sintéticos ou escrever algo que o helper principal não escreve. O **README local** da pasta é a porta de entrada: explica quando usar, requisitos, efeitos e limites. Depois confira a implementação ou o briefing, que definem os nomes e comportamentos reais. O [README do produto](README.md#-o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho) liga essas peças às cinco famílias gerais de recursos do ecossistema. O [Hub Micromodelos](hub_micromodelos/README.md) combina essas famílias para especificar uma característica de domínio, estudar suas evidências e registrar incertezas. Sua skill está em `L1/audit`; a biblioteca exige chamada explícita, e o exemplo sintético não publica nem homologa um modelo.

Pense em uma taxa de resposta já pronta. Se só precisa exibi-la, escolha o snippet de formatação; pedir à skill de EDA para formatar uma string acrescentaria trabalho sem melhorar a pergunta. Se a taxa ainda depende de conferir duplicatas, nulos e denominador, a formatação é a última etapa, não a primeira. Esse contraexemplo ajuda a reconhecer que uma saída bonita não substitui uma medição adequada. Do mesmo modo, um prompt pode orientar o pedido de análise, mas não substitui o cálculo ou a revisão do notebook.

<a id="mu01-3"></a>
#### 3. Seguir uma trilha curta e testar sua escolha

Use a **intenção de hoje** para entrar no manual. Se quer apenas localizar algo, comece pelo [catálogo e Concierge](#mu03); o Concierge ajuda a recomendar recursos existentes e não executa a análise durante essa descoberta. Se quer trabalhar com um método assistido, vá a [skills](#mu04) e depois ao capítulo da tarefa. Se já sabe qual função ou utilitário usar, prepare o ambiente em [MU02](#mu02) e siga a chamada isolada de [snippet](#mu06) ou [script](#mu07). Para criar uma peça nova, use o capítulo de documentação e autoria. Para uma entrega visual, inicie pelo planejamento visual e avance até os exemplos de notebook e assets conforme a necessidade. A trilha é uma sequência de consulta, não uma exigência de percorrer o manual inteiro antes de trabalhar.

| Sua necessidade imediata | Primeira rota | O que esperar dessa rota |
|---|---|---|
| Ainda não sei qual recurso serve | MU03 ou Concierge | recomendação para conferir, sem execução analítica |
| Quero conhecer uma fonte inteira | skill de EDA e MU08 | plano e análise assistida com revisão das premissas |
| Quero uma checagem delimitada | script e MU07 | retorno definido pelo utilitário escolhido |
| Já tenho um cálculo, preciso reaproveitar função | snippet e MU06 | valor produzido por uma chamada no notebook |
| Quero padronizar uma peça ou visual | padrões, MU18 ou MU14 | molde e roteiro de construção, sujeitos a revisão |

Pratique com dois pedidos sobre uma tabela **fictícia** `catalogo.analytics.contatos`. Pedido A: “Antes de calcular a taxa, quero saber se a chave de contato se repete, quantas respostas estão nulas e se a tabela está atualizada.” Há perguntas delimitadas de qualidade, então um script como `data_quality_check` é candidato. Abra o [README do script](hub_scripts/data_quality_check/README.md), confira campos e limites e execute apenas se tiver acesso e autorização. A saída esperada é um diagnóstico para orientar a decisão de prosseguir, não uma base corrigida nem uma garantia de que o desenho da campanha foi adequado.

Pedido B: “Recebi a fonte e preciso entender a população, as distribuições, as lacunas e que análises valem a pena antes de recomendar o próximo contato.” Aqui o objetivo é mais amplo que uma lista de checagens. Uma EDA assistida pode combinar perguntas, recursos e interpretação; `@hub-ml-eda-profissional` é uma rota para orientar esse percurso. Informe que cada linha deveria representar um contato, o período conhecido e o que ainda está em aberto. Peça um plano primeiro se ainda não quer executar consultas. Uma resposta que apenas mostra `status: pass` não satisfaz B, porque não examina distribuições nem limitações; uma EDA longa para responder só A pode consumir tempo e desviar do pedido.

O exercício tem uma segunda etapa: confira o que cada rota **não** sabe. A não valida, por si, se o denominador da taxa é o certo para a decisão. B não recebe permissão de leitura apenas por ser uma skill e não demonstra execução ao ser mencionada. Se o diagnóstico indicar `fail`, entenda o alerta e decida como investigar; não filtre automaticamente os registros para produzir uma aparência de aprovação. Se a EDA encontrar um campo de tempo ambíguo, esclareça qual data representa o contato antes de aceitar conclusões. A escolha de recurso é boa quando deixa a próxima pergunta mais precisa.

<a id="mu01-4"></a>
#### 4. Pedir ajuda com contexto suficiente e reconhecer o próximo passo

Você não precisa conhecer Spark, imports ou JSON para começar. Precisa conseguir dizer **qual decisão** depende do trabalho e qual material está disponível. Um pedido útil informa a tabela ou arquivo autorizado, o período, o significado de uma linha quando conhecido, restrições como “somente leitura” e o formato esperado: explicação, plano, código para revisar ou execução. Se um item essencial não for conhecido, diga isso. Não invente nomes de colunas, regras de negócio ou permissões para fazer o pedido parecer completo. O assistente pode ajudar a transformar a lacuna em pergunta ou inspeção permitida.

Por exemplo: “Quero decidir se posso comparar a resposta por segmento em `catalogo.analytics.contatos`. Cada linha deveria ser um contato; não sei ainda se há repetições. Considere janeiro a março. Primeiro proponha checagens somente leitura e diga que informação falta; não execute nem escreva.” O texto delimita propósito, fonte, unidade provável, incerteza, período e modo de trabalho. Se você quiser uma skill específica, acrescente `@hub-ml-eda-profissional` apenas quando o percurso de EDA for o pretendido. O nome na sua **resposta** a outra pessoa não ativa uma skill; a seleção precisa ocorrer na interação e ser conferida no contexto disponível.

Depois de receber ajuda, separe três perguntas: o recurso certo foi escolhido? O código ou a consulta realmente rodou no ambiente autorizado? O resultado responde à decisão com limitações compreensíveis? A primeira não prova as outras. Se um arquivo ou tabela não estiver acessível, pare naquele passo e obtenha a localização ou permissão pelo caminho de trabalho apropriado. Se a resposta do assistente disser “feito” sem mostrar execução ou evidência, trate-a como proposta a conferir. O [guia de política de enforcement](hub_padroes/skill_enforcement/README.md) aprofunda essas diferenças para quem cria ou audita skills; para seu primeiro uso, basta manter proposta, execução e validação separadas.

Se a próxima dificuldade for localizar a cópia do Hub e fazer uma primeira chamada, siga [MU02](#mu02). Se a dificuldade for escolher entre recursos parecidos, siga [MU03](#mu03). O detalhe de por que as pastas e instruções foram organizadas assim está em [MT01](MANUAL_TECNICO_V2.md#mt01) e [MT02](MANUAL_TECNICO_V2.md#mt02). Você pode voltar a esses capítulos quando a operação pedir mais fundamento; a escolha inicial continua ancorada na tarefa e no resultado que você consegue conferir.

<!-- editorial:exclude:start -->
**Fontes principais:** [guia do produto](README.md), [instruções operacionais](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/ambiente_databricks/.assistant_instructions.md), [manual técnico vigente](MANUAL_TECNICO_V2.md), [README raiz](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/README.md), [ADR de arquitetura](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0001-arquitetura-multi-ia.md), [policy de enforcement](hub_padroes/skill_enforcement/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Próximo: MU02](#mu02) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT01](MANUAL_TECNICO_V2.md#mt01) · [MT02](MANUAL_TECNICO_V2.md#mt02)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu02"></a>
<a id="mu02"></a>
### MU02 — Primeiro uso, ambiente e acesso aos recursos

**Pergunta deste capítulo:** como confirmar que você está vendo a cópia certa do Hub e fazer uma primeira chamada pequena? O percurso começa pela localização dos arquivos, testa uma função de formatação sem consultar tabelas e mostra onde investigar quando algo falha. Os caminhos e a saída servem como exemplo; confirme o endereço e o ambiente autorizados para a sua sessão.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](#sumario-mu) · [Escolher uma trilha](#mu01) · [Usar snippet diretamente](#mu06) · [Fundamentos de importação](MANUAL_TECNICO_V2.md#mt03)
<!-- editorial:exclude:end -->

<a id="mu02-1"></a>
#### 1. Localizar a cópia de uso e distinguir os objetos

Comece pelo lugar onde seu trabalho acontece. O repositório mantém o produto editável em `ambiente_databricks/`, mas isso não demonstra que ele foi instalado no seu workspace do Databricks. O [README de manutenção](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/ambiente_databricks/README.md) separa fonte editável, espelho gerado, laboratório e destino de trabalho; cada um tem finalidade e permissão próprias. Para **consumir** um recurso, encontre a cópia `.assistant` que sua equipe disponibilizou e que sua conta pode ler. Se ela não aparecer, peça a localização publicada ao responsável pelo ambiente. Não tente consertar uma ausência no workspace executando ferramentas de publicação do repositório.

Três nomes parecidos podem gerar erros diferentes. Um **arquivo** é conteúdo guardado no workspace, como `hub_snippets/constants/format_br/format_br.py`; um **notebook** organiza células executáveis e explicações, como `exemplo_format_br.py`; uma **tabela** é dado consultado pelo Spark por identificador como `catalogo.schema.tabela`. Alguns notebooks e arquivos Python terminam em `.py`, então a extensão sozinha não distingue os dois. No Hub, o marcador `# Databricks notebook source` identifica o formato de notebook de exemplo; as ferramentas de publicação conferem o tipo `NOTEBOOK` para esse exemplo e `FILE` para o módulo importável. O [detector de marcador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/notebook_marker.py) e o [publicador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/publicar_free.py) documentam essa diferença técnica. Você não precisa rodar essas ferramentas para usar `fmt_pct`; precisa saber qual peça abrir e qual peça importar.

Há também dois tipos de caminho. `/Users/<username>/.assistant` pode identificar a pasta como objeto na navegação do workspace. Para código Python acessar arquivos da mesma cópia, o caminho costuma aparecer como `/Workspace/Users/<username>/.assistant`. `<username>` é um marcador a substituir, não um usuário válido. A raiz pode ser diferente quando a entrega estiver em uma Git folder ou área compartilhada. Confira o endereço efetivo no seu ambiente antes de colocá-lo num notebook; não transforme automaticamente um caminho de interface no outro. A [documentação oficial de arquivos de workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace) distingue arquivos e source notebooks e ressalta que o suporte depende do runtime e do modo de uso.

Um endereço de tabela usa pontos por outra razão: catálogo, schema e nome do dado. Ele não entra em `sys.path`, a lista de lugares onde o Python procura módulos. Se você tentar `spark.table("hub_snippets.constants.format_br")`, pedirá ao Spark uma tabela com esse nome, não uma função; se puser `catalogo.schema.tabela` em `sys.path`, não ganhará acesso aos dados. Quando localizar `.assistant`, confirme visualmente que ela contém `hub_snippets/`, `hub_scripts/`, `hub_prompts/` e `skills/` conforme a entrega disponível. A existência das pastas no Git e a permissão para abrir uma tabela continuam sendo verificações separadas.

<a id="mu02-2"></a>
#### 2. Abrir o exemplo, preparar o import e conferir dependências

Escolha uma primeira chamada que não exija Spark nem dados da empresa. A pasta [`format_br`](hub_snippets/constants/format_br/README.md) contém um README para decidir quando usar, a implementação `format_br.py`, a fachada `__init__.py` que expõe os nomes públicos e o notebook `exemplo_format_br.py`. **Fachada** é o arquivo que oferece um caminho curto de importação para as funções do objeto. Leia o README antes do exemplo: `fmt_pct` devolve texto para apresentação, não recalcula a taxa. O notebook demonstra mais funções e interpreta casos de escala; não é a biblioteca a importar. Para a primeira prova, use um valor fictício conhecido, `0.12`, representando 12% como fração.

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

Depois dessa prova leve, abra o [notebook de exemplo](hub_snippets/constants/format_br/exemplo_format_br.py) para entender outras funções e erros de escala. Antes de executar **qualquer** notebook de exemplo do Hub, leia seu README local: alguns exemplos preparam ou apagam tabelas sintéticas mesmo quando o helper principal é somente leitura. `format_br` não exige uma dependência opcional de ML para sua chamada; um snippet Spark, como `null_summary`, já exige PySpark e um DataFrame Spark. **Dependência** é uma biblioteca ou capacidade necessária para importar ou executar uma função. A lista de pacotes opcionais do Hub orienta investigação, mas não prova o que está instalado na sua sessão; confirme somente as dependências do objeto escolhido.

<a id="mu02-3"></a>
#### 3. Conferir compute, permissões e estado da entrega

**Compute** é o recurso de processamento ligado ao notebook. Uma chamada simples de formatação usa Python; uma função que opera sobre um **DataFrame Spark**, isto é, uma tabela manipulada por operações distribuídas, precisa de um ambiente com APIs Spark compatíveis. Antes de trocar o exemplo leve por uma consulta real, confirme qual compute está ativo, se a biblioteca exigida está disponível e se você tem permissão para ler o recurso. O fato de o notebook abrir não prova que um módulo Python pode ser importado; conseguir importar o módulo não prova que a tabela existe ou pode ser lida. Essas são etapas distintas e seus erros ajudam a localizar a falha.

**Serverless** é um modo em que a plataforma administra o compute sem você escolher e manter um cluster clássico para cada notebook. Em notebooks serverless padrão, a configuração de bibliotecas passa pelo painel **Environment**. Na experiência Git Folder Serverless descrita pela Databricks, as dependências são geridas por `pyproject.toml` na raiz da pasta Git; jobs têm configuração própria. A [documentação oficial de dependências serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies), reconferida em 7/10/2026, distingue essas rotas e alerta para não instalar PySpark sobre o ambiente serverless gerenciado. Isso não significa que você deva alterar o ambiente para testar `fmt_pct`: a primeira chamada foi escolhida justamente para não precisar de uma instalação adicional. Quando outro recurso exigir pacote opcional, consulte o README, a versão e o mecanismo adotado pela sua equipe antes de pedir ou fazer a mudança.

Serverless também tem limites de API que importam para módulos Spark: a [documentação de limitações](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations) informa suporte a Spark Connect e ausência de APIs RDD nesse modo. Um helper que usa uma API incompatível pode importar e falhar só quando for chamado. Em outro compute, a situação pode ser diferente. Não conclua “o Hub não funciona” por uma falha específica nem instale uma biblioteca aleatória para fazê-la desaparecer. Registre o nome da função, o compute, o erro e em que etapa ocorreu; esse conjunto permite decidir se o problema é caminho, pacote, API, dado ou permissão.

Para dados, faça a mesma separação. `catalogo.schema.tabela` é um exemplo de identificador completo no Unity Catalog, não uma tabela real deste manual. Uma **view temporária** pode existir só na sessão em que foi criada, enquanto uma tabela persistente tem escopo e permissões próprios. Se a chamada seguinte usar `spark.table(...)`, confirme catálogo, schema, nome, população e autorização de leitura. Uma mensagem de acesso negado não autoriza contornar a permissão com outra conta ou cópia do dado. Para operação que grava, além da leitura, é preciso conhecer destino, modo de escrita e impacto antes de executar; a receita deste capítulo não grava nada.

Por fim, compare o que foi **publicado** com o que você vê no Git. O mantenedor valida a fonte, gera o espelho e verifica o workspace por procedimentos próprios; o [playbook do projeto](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/README.md) lembra que o laboratório Free e o destino de trabalho exigem conferências separadas. Você, como usuário, pode verificar a pasta, abrir o README, importar um objeto e pedir ao responsável a versão distribuída. Não precisa rodar `render_simulado.py`, `publicar_free.py` ou o kit de transição para resolver um `ModuleNotFoundError` no notebook. Uma versão antiga da entrega pode explicar por que o nome mostrado no Git ainda não aparece na sua sessão. Quem mantém a instalação encontra o percurso completo em [MT28](MANUAL_TECNICO_V2.md#mt28).

Antes de uma chamada que envolva dados, faça uma conferência em linguagem comum: “consigo abrir o arquivo de código, meu compute aceita suas bibliotecas, tenho leitura da tabela completa, e sei o que a função retornará?”. Se uma resposta for desconhecida, localize o README do objeto ou peça ao responsável a informação específica. Essa pausa é mais eficaz que testar indiscriminadamente comandos de instalação ou consultas em tabelas semelhantes. Ela também evita confundir acesso de leitura ao arquivo com autorização para copiar, transformar ou persistir os dados.

<a id="mu02-4"></a>
#### 4. Interpretar a primeira saída e recuperar uma falha

Para o valor fictício escolhido, `fmt_pct(0.12)` deve mostrar `12,0%`. A verificação Python registrada na redação original desta edição produziu esse texto; a saída no seu workspace ainda depende de importar a mesma versão do módulo. A variável `taxa_fracao` continua numérica (`0.12`), e `taxa_texto` é uma **string**, ou texto para apresentação. Confira a unidade antes de aceitar o resultado: `fmt_pct(12)` com escala padrão trataria 12 como fração e mostraria `1200,0%`, sem necessariamente lançar erro. Uma célula que termina sem exceção não certifica que a taxa de origem tinha o denominador correto. Para um teste pequeno, compare com a aritmética 12 respostas em 100 contatos, mas não use esse exemplo como estimativa de sua tabela real.

Se a célula parar, identifique **onde** parou. `FileNotFoundError` lançado pelo bloco significa que a raiz indicada não contém `hub_snippets/`; confira endereço e materialização antes de mudar código. `ModuleNotFoundError` cujo nome ausente é `hub_snippets` sugere caminho, cópia incompleta ou arquivo importável publicado como notebook. Se o nome ausente for uma biblioteca opcional exigida por outro objeto, o caminho do Hub pode estar correto e o problema ser a dependência naquele compute. `ImportError` sobre `fmt_pct` pede conferir o `__init__.py` público e a versão do objeto. Um `ValueError` durante a chamada aponta para argumento recusado, como uma escala não aceita, e exige reler o contrato da função, não reinstalar a biblioteca.

Um diagnóstico simples ajuda a diferenciar cópias depois que o import funciona: em outra célula, `import inspect` carrega a biblioteca padrão de inspeção do Python; então `inspect.getfile(fmt_pct)` mostra o arquivo Python de onde veio a função. Use-o apenas para verificar a origem, sem expor caminhos pessoais em relatório compartilhado. Se apontar para uma cópia diferente, corrija o `sys.path` e reinicie ou recarregue a sessão conforme o ambiente antes de repetir a conferência; imports já carregados podem manter estado anterior. Se a origem estiver certa e o número estiver errado, investigue unidade, argumento e fórmula que produziu a taxa. MU06 amplia esse tipo de conferência para snippets; MU07 faz o mesmo para scripts com retornos próprios.

Ao pedir ajuda, copie o **tipo de falha e a etapa**, sem colar credenciais ou dados sensíveis: “o diretório existe, importei `format_br`, mas a saída foi `1200,0%` para uma taxa que esperava 12%” é uma pergunta melhor que “não funciona”. Diga também se está em serverless ou outro compute e se usou cópia de workspace ou Git folder. Essa informação permite escolher a próxima ação mínima: corrigir o caminho, pedir a publicação que falta, revisar a dependência, ou ajustar a escala. Mantenha o primeiro teste pequeno; ele existe para localizar a fronteira que falhou antes de você envolver uma tabela ou workflow inteiro.

<!-- editorial:exclude:start -->
**Fontes do produto:** [guia `.assistant`](README.md), [README de `format_br`](hub_snippets/constants/format_br/README.md), [implementação e API](hub_snippets/constants/format_br/format_br.py), [exemplo](hub_snippets/constants/format_br/exemplo_format_br.py), [marcador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/notebook_marker.py), [publicador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/publicar_free.py) e [manual técnico vigente](MANUAL_TECNICO_V2.md#importacao). **Plataforma:** [workspace files](https://learn.microsoft.com/en-us/azure/databricks/files/workspace), [módulos](https://learn.microsoft.com/en-us/azure/databricks/files/workspace-modules), [dependências serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies) e [limitações](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/limitations), reconferidos em 7/10/2026.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU01](#mu01) · [Próximo: MU03](#mu03) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT03](MANUAL_TECNICO_V2.md#mt03)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu03"></a>
<a id="mu03"></a>
### MU03 — Encontrar o recurso certo para a tarefa

**Pergunta deste capítulo:** o que o Hub oferece para aquilo que você precisa fazer? Use a busca manual quando já consegue reconhecer uma família de recursos; peça ajuda ao Concierge quando a intenção ainda precisa ser traduzida em uma rota. Em ambos os casos, a escolha só fica pronta depois que você confere a entrada, o resultado e o limite do objeto encontrado.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](#sumario-mu) · [Escolher uma trilha](#mu01) · [Usar skills](#mu04) · [Arquitetura de contexto](MANUAL_TECNICO_V2.md#mt04) · [Catálogo técnico de skills](MANUAL_TECNICO_V2.md#mt14)
<!-- editorial:exclude:end -->

<a id="mu03-1"></a>
#### 1. Traduzir uma necessidade em objetivo e entregável

Antes de procurar um nome no catálogo, escreva em uma frase a **decisão** que quer apoiar. “Ver nulos” é uma operação; “saber se a coluna de identificação serve como chave para juntar duas bases” já aponta o motivo da operação. Em seguida, nomeie o recurso disponível: tabela, notebook, modelo, relatório ou apenas uma descrição. Se houver tabela, diga o que uma linha representa, isto é, o **grão**. “Uma linha por cliente” e “uma linha por compra” mudam o significado de duplicidade, taxa e junção. Acrescente período, limites de acesso e a forma esperada da entrega: número, tabela de diagnóstico, notebook, plano ou explicação.

Esse pequeno contrato evita três escolhas precipitadas. Um **snippet** é uma função reutilizável que você importa para um cálculo ou apresentação pontual. Um **script** é uma unidade de operação maior, que pode checar, transformar ou produzir um artefato. Um **prompt** do Hub é um formulário que você preenche e entrega manualmente ao assistente; por si só, não acessa dados nem executa código. Uma **skill** é o roteiro de trabalho que pode orientar o Genie Code por seleção relevante ou menção explícita. Nenhum desses nomes indica sozinho que o recurso foi executado no seu ambiente. O [índice do produto](README.md) e o [catálogo de skills](skills/README.md) situam essas famílias.

Faça uma primeira triagem por tamanho da pergunta. Se você já tem um DataFrame e só precisa da contagem de nulos por coluna, procure uma função; se precisa investigar causas, recortes, gravidade e ação, uma **análise exploratória de dados (EDA)** ou um briefing de qualidade responde à pergunta mais ampla. A EDA examina estrutura, distribuições e possíveis problemas antes de uma decisão; o [briefing de EDA rápida](hub_prompts/eda_rapida/README.md) mostra quando começar por um perfil limitado. **DataFrame** é a tabela manipulada pelo código Spark ou Python, não o nome de uma tabela do catálogo. O fato de uma função ser rápida de chamar não a torna suficiente para decidir se a base pode entrar em produção.

Use um pedido curto e reproduzível como rascunho: “Quero avaliar nulos por coluna no DataFrame de clientes do mês de setembro, sem escrever tabela; espero um resumo para decidir quais campos investigar”. Se você não sabe o grão ou o período, escreva “não informado” e procure primeiro como obtê-los. Se nem a fonte pode ser identificada, peça uma orientação de descoberta, não uma taxa inventada. Essa formulação será a mesma ao seguir a busca manual ou ao consultar o Concierge, facilitando comparar as recomendações com a necessidade original.

<a id="mu03-2"></a>
#### 2. Percorrer o catálogo manualmente e ler o README local

Abra o [README de entrada da `.assistant`](README.md). Ele organiza snippets, scripts, prompts, skills, padrões, materiais visuais e a área de domínio [Micromodelos](hub_micromodelos/README.md). Para especificar uma característica ou descobrir oportunidades por metadados, consulte essa área e sua skill `hub-ml-micromodelos`; uma recomendação não autoriza leitura de registros nem publicação. Escolha a família pela tarefa, não pela palavra mais parecida com a sua pergunta. O [índice de snippets](hub_snippets/README.md) aponta funções curtas; o [índice de scripts](hub_scripts/README.md) reúne operações; o [índice de prompts](hub_prompts/README.md) explica quando um pedido estruturado ajuda; o catálogo de skills mostra roteiros de análise. O [manual técnico vigente](MANUAL_TECNICO_V2.md) conecta fundamentos e nomes de helpers. Um item listado é candidato; o README da pasta do objeto é a próxima leitura obrigatória.

Para a checagem de nulos, encontre [`null_summary`](hub_snippets/spark/null_summary/README.md). Leia “para que serve”, pré-requisitos, assinatura e retorno antes de copiar um import. A função recebe um DataFrame Spark e devolve um DataFrame resumido; você ainda precisa decidir quais colunas são críticas e conferir o denominador de cada percentual. Se a tarefa for apenas exibir um diagnóstico numa sessão já autorizada, a rota pode ser o snippet isolado, descrita em [MU06](#mu06). A skill de EDA não é requisito para uma chamada direta e independente dessa função no notebook. Se a tarefa já selecionou uma EDA protegida, porém, o snippet não substitui seu runner nem permite contornar um bloqueio; confirme a rota antes de executar. Se a pergunta for “por que os nulos aumentaram e a base ainda serve para o modelo?”, a função pode fornecer evidência, mas a rota metodológica precisa de período, segmentos, comparação e conclusão.

O segundo exemplo começa com “a variável ficou instável?”. **Estabilidade** aqui significa comparar a distribuição de um atributo entre uma população de referência e outra atual. O **Population Stability Index (PSI)** resume a diferença entre essas distribuições em um indicador; seu valor exige conhecer população, faixas e período de comparação, e não mede sozinho a qualidade do modelo. O [README do calculador de PSI em Spark](hub_snippets/spark/psi_calculator/README.md) explica entradas, cálculo e limites; o [script de drift](hub_scripts/drift_detector/README.md) faz uma checagem operacional com suas próprias entradas e saídas. “Drift” nomeia a mudança observada; não indica automaticamente que o modelo piorou. Antes de escolher, defina a variável, as duas janelas, a população, o volume e se você quer um indicador pontual ou uma investigação de monitoramento. Para um plano amplo de acompanhamento, leia a skill [`hub-ml-monitoramento-modelo`](skills/hub-ml-monitoramento-modelo/SKILL.md). Seu estado atual na policy deve ser conferido; a descrição da skill não prova que já existe um monitor implantado.

No README local, responda a quatro perguntas práticas. Que objeto a chamada recebe? O que retorna ou escreve? Quais dependências e permissões existem? Como o exemplo deve ser executado? Um arquivo de exemplo pode preparar uma tabela sintética com `mode("overwrite")`, ação que substitui o destino se você rodar aquela parte. Ler o exemplo é seguro; executá-lo exige conferir destino e efeito. O [guia de primeiro uso](#mu02) distingue arquivo Python, notebook e tabela e explica por que importação não equivale a publicação. Se o README não resolver o seu caso, abra a implementação e o exemplo para confirmar assinatura e resultado, ou registre a dúvida para a rota assistida.

Ao terminar a busca manual, anote o caminho do objeto, a versão ou cópia consultada, a razão da escolha e uma condição de recusa. Por exemplo: “`null_summary` serve para medir nulos no DataFrame; não conclui se a coluna é aceitável para negócio”. Esse registro evita que um nome lembrado de conversa anterior seja tomado por evidência de disponibilidade na cópia atual. Também facilita pedir ao Concierge que compare alternativas sem repetir toda a investigação.

<a id="mu03-3"></a>
#### 3. Pedir uma rota ao Concierge e interpretar a resposta

O [Concierge](skills/hub-ml-concierge/SKILL.md) é uma skill de descoberta e composição. Você pode mencioná-la explicitamente com `@hub-ml-concierge` quando esse recurso estiver disponível no seu ambiente, ou pedir ao assistente para localizar opções; a presença da pasta no repositório não confirma instalação nem seleção nativa na sua sessão. **Seleção por relevância** é a possibilidade de o Genie Code escolher uma skill a partir da descrição do pedido; não há uma tabela rígida de palavras que garanta a escolha. Se você já escolheu o especialista correto, pode ir a ele diretamente. O Concierge não é um portão obrigatório nem executa o especialista ao recomendá-lo.

Um pedido útil contém objetivo, entrada, saída, restrições e o escopo que pode ser inspecionado. Por exemplo: “Com `@hub-ml-concierge`, encontre no Hub uma forma de medir nulos por coluna no DataFrame de clientes. Preciso somente de um resumo em memória, sem escrever tabela. Diga o caminho do recurso, os argumentos, o retorno, o que você conseguiu verificar e o próximo passo”. O caminho, e não apenas o nome, permite abrir o README indicado. Se você não anexou a cópia do Hub ou o assistente não pode ler os arquivos, a resposta deve declarar essa limitação; uma busca sem acesso não demonstra que o recurso está ausente.

A [descoberta progressiva](skills/hub-ml-concierge/references/descoberta.md) compara adequação, incompatibilidade e cobertura. O [modelo de recomendação](skills/hub-ml-concierge/templates/recomendacao.md) separa objetivo entendido, rota, recursos indicados, evidências, alternativas recusadas, confiança e próximo passo. A rota `HELPER_ROUTE` sugere que uma **interface de programação de aplicações (API)** reutilizável basta: neste contexto, é a função pública que o código chama, com entradas e retorno definidos, como `null_summary` para uma medição pontual. O [README da função](hub_snippets/spark/null_summary/README.md) permite conferir essa interface concreta. `DIRECT_ROUTE` aponta um componente principal que atende ao método ou briefing. `COMPOSITE_ROUTE` combina peças com papéis complementares; `BRIEFING_FIRST` pede definições faltantes antes de escolher. `GAP` significa que a busca não achou cobertura adequada **no escopo pesquisado**, e `ACCESS_BLOCKED` que o acesso impediu verificar candidatos. Essas etiquetas pertencem à saída da skill, não são comandos do Databricks.

Leia também a cobertura, que é independente da rota: `TOTAL_PARA_ESCOPO`, `PARCIAL` ou `NAO_DETERMINADA`. Uma rota direta pode cobrir apenas parte da pergunta. Se o Concierge recomendar “skill de monitoramento” para a palavra “estabilidade”, verifique se o pedido era comparar duas distribuições com PSI, investigar drift por vários segmentos ou desenhar operação contínua. A recomendação precisa indicar referência, período e volume ainda desconhecidos. Sem eles, aceite no máximo uma rota condicionada ou um briefing inicial, não um resultado de estabilidade. A [policy integrada](hub_padroes/skill_enforcement/policy.json) registra níveis atuais de enforcement; nível alvo não é capacidade presente.

Um exemplo de resposta **ilustrativa**, não gerada por uma execução do Concierge nesta obra, seria: “Rota `HELPER_ROUTE`, cobertura `PARCIAL`: `null_summary` mede nulos por coluna no DataFrame, mas a decisão de aceitar a fonte requer regra de negócio e período. Caminho verificado no README e no código; tabela do workspace não inspecionada. Próximo passo: conferir o DataFrame e chamar a função com amostra controlada”. Leia a frase como uma lista de verificações. Caminho verificado é evidência documental; número calculado exigiria execução real. “Confiança alta na adequação” expressa julgamento fundamentado, não probabilidade estatística de acerto. O [registro de busca](skills/hub-ml-concierge/templates/registro_busca.md) deve mostrar onde e quanto o agente procurou; busca top-k ou amostra não vira “varredura completa”.

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

Quando houver mais de um componente, solicite uma **composição mínima**: apenas peças necessárias, na ordem em que cada resultado alimenta a etapa seguinte. Para estabilidade, uma medição pontual de PSI pode vir antes da interpretação por segmento e do desenho de alertas; se não há operação contínua, não existe motivo para pressupor job, dashboard ou deploy. O [guia de composição do Concierge](skills/hub-ml-concierge/references/composicao.md) exige papéis e limites por objeto. O [template de handoff](skills/hub-ml-concierge/templates/handoff.md) ajuda a passar ao especialista apenas objetivo, entradas, restrições, evidências e pendências, sem converter sugestão em ação já realizada.

Antes de prosseguir, confira três coisas na sua cópia: o arquivo indicado existe e pode ser lido; seu README e sua assinatura correspondem à tarefa; a recomendação distingue o que foi lido, executado e ainda precisa de confirmação. Se o recurso não estiver acessível, registre o caminho tentado e peça ao responsável a cópia ou permissão correta. Se não houver cobertura comprovada, formule uma alternativa delimitada ou um pedido de diagnóstico, sem anunciar que “o Hub não tem” a capacidade em todas as versões. O [catálogo de skills](skills/README.md) orienta a próxima família, e [MU04](#mu04) explica como acompanhar uma skill depois de escolhê-la.

Por fim, trate simulação e ambiente real separadamente. Anexar `SKILL.md` ao chat pode ajudar o assistente a ler o método e produzir um plano; isso não prova que a skill foi descoberta automaticamente, instalada no workspace ou que algum gate de execução passou. A mesma disciplina vale na busca manual: um exemplo visto no repositório é uma referência para preparar sua ação, e uma conclusão só deve citar o dado, a execução e a validação que de fato ocorreram.

<!-- editorial:exclude:start -->
Fontes de referência: [entrada do produto](README.md), [Concierge](skills/hub-ml-concierge/SKILL.md), [descoberta](skills/hub-ml-concierge/references/descoberta.md), [recomendação](skills/hub-ml-concierge/templates/recomendacao.md), [registro de busca](skills/hub-ml-concierge/templates/registro_busca.md) e [policy atual](hub_padroes/skill_enforcement/policy.json).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU02](#mu02) · [Próximo: MU04](#mu04) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT14](MANUAL_TECNICO_V2.md#mt14)
<!-- editorial:exclude:end -->

<!-- editorial:exclude:start -->
<a id="parte-mu-ii"></a>
## Parte II — Escolher e usar recursos
<!-- editorial:exclude:end -->


<a id="mu-mod-mu04"></a>
<a id="mu04"></a>
### MU04 — Usar skills do pedido à entrega revisada

**Pergunta deste capítulo:** o que informar, acompanhar e conferir quando uma skill orienta seu trabalho no Genie Code? Comece por uma tarefa pequena e uma fonte identificada. A escolha da skill é só a primeira etapa: leia o plano, acompanhe as ações e confira o que a evidência permite dizer sobre o resultado.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](#sumario-mu) · [Primeiro uso](#mu02) · [Encontrar recursos](#mu03) · [Preencher briefings](#mu05) · [Arquitetura técnica](MANUAL_TECNICO_V2.md#mt14) · [Execução verificável](MANUAL_TECNICO_V2.md#mt19)
<!-- editorial:exclude:end -->

<a id="mu04-1"></a>
#### 1. Escolher a skill e observar a seleção

Uma **Agent Skill** é uma pasta de instruções para o assistente, centrada em `SKILL.md`. Ela descreve quando se aplica, como conduzir a tarefa e que recursos adicionais consultar. O mecanismo de Agent Skills pertence ao Genie Code; os nomes `hub-ml-*` e seus métodos são conteúdo deste Hub. O [catálogo de skills](skills/README.md) apresenta as 15 opções desta versão. Uma skill não é uma biblioteca Python: ler suas instruções não instala nem chama os helpers recomendados. [MU03](#mu03) ajuda a localizar a família antes de escolher.

Há duas formas de chegar a uma skill. Se você sabe qual método deseja, selecione `@hub-ml-...` na interface e descreva a tarefa. A menção explícita reduz ambiguidade e permite conferir o nome escolhido. Quando o pedido coincide com a `description` do cabeçalho de uma skill, o Genie Code **pode** selecioná-la por relevância; a redação do pedido e a disponibilidade no ambiente influenciam essa escolha. A [documentação oficial de Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills), reconferida em 2026-10-07, descreve seleção por relevância e menção `@`. Observe o indicador de seleção e a resposta em sua sessão. A simples ocorrência do nome na resposta não prova que a skill foi carregada. A [referência atual de plataforma](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/ai/references/databricks-genie-code.md) distingue `@` para skill de um atalho como `/eda`, que o Hub não registra como comando.

Escolha pela decisão a produzir. Para examinar uma fonte, `hub-ml-eda-profissional`; para cruzar fontes antes de modelar, `hub-ml-cross-eda-ml`; para definir atributos disponíveis no ponto de decisão, `hub-ml-feature-engineering`. `hub-ml-baseline-ml` orienta o primeiro modelo, `hub-ml-explainability` a explicação de um modelo identificado e `hub-ml-monitoramento-modelo` o acompanhamento de um modelo em operação. `hub-ml-analise-safra` trata coortes e maturação; `hub-ml-validacao-estatistica` trata pergunta, pressupostos, efeito e incerteza. Para fluxo de dados, escolha `hub-ml-pipeline-builder`; para criar um objeto do próprio Hub, `hub-ml-criar-objeto`. `hub-ml-comentar-notebook` documenta células, `hub-ml-tutor-databricks` ensina um objeto ou erro real, e `hub-ml-auditoria-skills` revisa implementação ou saída de skill. `hub-ml-micromodelos` orienta especificação de uma característica de domínio ou descoberta de oportunidades por metadados; sua biblioteca exige execução separada. `hub-ml-concierge` é a rota de descoberta quando ainda falta decidir qual componente usar; sua recomendação termina em um repasse, sem executar o especialista. Consulte o `SKILL.md` e o [catálogo de skills](skills/README.md); leia também o README local quando a pasta da skill o tiver, antes de assumir que a descrição curta cobre seu caso.

Se você anexou um `SKILL.md` como arquivo comum para o assistente ler, registre isso como **leitura por anexo**. É útil para discutir o método, mas não demonstra descoberta nativa, instalação ou seleção no workspace. Se uma skill foi editada após a abertura do chat, confira a cópia disponível em uma conversa nova; uma resposta antiga pode refletir outra versão. Se a descrição continuar antiga, faça hard refresh da aba. Pastas adicionais de skills são cadastradas na interface pela pasta que contém suas subpastas; manter arquivos no Git não prova descoberta. No caso de dúvida, peça ao assistente que diga qual recurso viu e qual trecho do procedimento está usando, e compare com sua cópia. Assim você sabe se está seguindo uma skill identificada ou apenas recebendo uma sugestão de rota.

<a id="mu04-2"></a>
#### 2. Dar contexto, pedir plano e delimitar a execução

Uma solicitação útil começa pelo **resultado pretendido**, não por “rode a skill”. Informe a fonte concreta, como tabela, notebook ou modelo; diga o que uma linha representa (**grão**) e quais chaves ligam registros. Acrescente período, coluna de evento e momento em que a informação estava disponível. Se houver modelo, descreva o **target**, isto é, o resultado que se quer prever ou avaliar, e seu horizonte. Declare o público da entrega, os recursos que o assistente pode ler, o limite de tempo/custo e se deseja explicação, plano, código ou execução. Use `NÃO INFORMADO` para um dado material desconhecido e peça diagnóstico antes de qualquer suposição. A [memória entre sessões da Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/memory), documentada e reconferida em 7/10/2026, pode recuperar contexto relevante; ela é distinta das instruções e não garante lembrança integral. Reconfirme premissas materiais, versão, fonte e autorização em cada tarefa. [MU05](#mu05) oferece formulários por tarefa.

Um pedido completo para começar uma análise poderia ser:

```text
@hub-ml-eda-profissional
Quero decidir se a tabela sintética catalogo_exemplo.dados.clientes serve
para um diagnóstico inicial. Uma linha representa um cliente; a chave
candidata é id_cliente. Examine setembro de 2026. O momento de disponibilidade
das colunas é NÃO INFORMADO: destaque o que precisa ser verificado.
Primeiro apresente um plano, colunas e custos aproximados; não execute nem
persista nada nesta etapa. Se eu autorizar execução depois, mostre a rota
canônica, evidências obtidas e limitações antes de concluir.
```

O nome de tabela e a data são **ilustrativos**; não foram consultados neste manual. O pedido separa planejamento de execução e torna verificável se o assistente respeitou a etapa solicitada. Antes de aceitar o plano, confira se ele usou o grão informado, delimitou a população, identificou colunas e períodos, tratou nulos e duplicidade no denominador correto e estimou operações caras, como varredura integral ou coleta ao driver. Se houver escrita, treino, job ou mudança de configuração, peça destino, efeito, modo de reprocessamento e ponto de aprovação. Um texto no prompt não amplia suas permissões nem substitui a política de aprovação do ambiente.

Um pedido insuficiente seria: “Use a skill de baseline e diga o melhor modelo”. Faltam tabela, unidade da previsão, evento positivo, data de corte, horizonte, maturação do rótulo, divisão de treino e avaliação e métrica. A resposta apropriada é perguntar pelos elementos decisivos ou propor um plano condicional, sem declarar modelo treinado. Na skill de safra, faltas equivalentes são coorte, idade da coorte, evento, numerador, denominador e tratamento de períodos imaturos. Na de monitoramento, seriam modelo/run, referência, janela atual, atraso do rótulo e responsável pela ação. Cada `SKILL.md` delimita seu contrato; esses exemplos mostram por que uma mesma lista genérica de campos não serve a todas as tarefas.

Quando você autorizar executar, confirme **qual operação** e **em qual ambiente**. A skill pode indicar templates e helpers, mas o notebook ainda precisa tornar a biblioteca acessível ao Python, importar a função correta e chamá-la. Um trecho de código gerado é proposta; um import é disponibilidade; uma chamada observada é execução; um resultado checado é uma etapa adicional. Por exemplo, a [análise exploratória de dados (EDA)](skills/hub-ml-eda-profissional/SKILL.md), que examina a fonte antes de uma decisão, pode recomendar `hub_scripts.quick_profile`, mas a recomendação textual não calcula um perfil. A [explicação do mecanismo](skills/README.md#relacao-entre-skills-hub-snippets-e-hub-scripts) ajuda a distinguir método e runtime.

Também pergunte o que fazer se o contexto necessário não estiver disponível. Para um cruzamento temporal, um timestamp de evento sem a data de disponibilidade da fonte não prova que um atributo existia no instante da decisão. Um plano pode mostrar o teste necessário e parar; código que presume a disponibilidade inventaria uma condição de validade. Se a etapa depende de dado ausente, o assistente deve declarar a lacuna, o possível impacto e a menor próxima ação para resolvê-la. Um bom bloqueio preserva o trabalho já verificado sem transformar incerteza em conclusão.

Se o plano propuser amostragem, peça o critério e verifique a quem os resultados se aplicam. Uma amostra dos primeiros registros pode perder meses, segmentos ou eventos raros; uma amostra aleatória sem semente e tamanho documentados dificulta a reprodução. Se propuser um gráfico, confira se a agregação ocorreu antes de levar dados ao driver e se categorias omitidas aparecem no limite declarado. Para uma ação persistente, compare nome completo do destino, modo de escrita e consequência de uma segunda execução. Guarde o plano aprovado junto da resposta e anote alterações posteriores: “execute o plano” só é uma autorização inteligível quando a versão do plano e seus efeitos estão claros.

<a id="mu04-3"></a>
#### 3. Ler níveis, gates e evidência da entrega

O **Skill Enforcement Framework (SEF)** é a convenção deste Hub para dizer quanto do procedimento de cada skill pode ser conferido mecanicamente. No [arquivo de policy](hub_padroes/skill_enforcement/policy.json), `current_level` descreve o nível operacional admitido pela policy; `target_level` indica a direção planejada. Verifique também `rollout_mode`: `guidance` orienta, `audit` mede sem bloquear, `warn` avisa e `enforce` pode impedir uma conclusão homologada. O nível alvo nunca substitui evidência de uso da versão atual. A [introdução à policy](hub_padroes/skill_enforcement/README.md) desenvolve essa leitura.

Leia a escala como perguntas sucessivas. **L0**: há orientação textual no `SKILL.md`? **L1**: existe contrato estruturado conferível sem executar a análise? **L2**: o **preflight** resolveu requisitos antes da lógica protegida? **L3**: o **runner** executou o caminho canônico e produziu um *Receipt*, comprovante ligado àquela execução? **L4**: o **postflight** conferiu a evidência final e autorizou a conclusão? O hash de um arquivo ajuda a detectar alteração dos bytes comparados, mas não prova, sozinho, que o resultado de negócio está correto. O [Manual Técnico](MANUAL_TECNICO_V2.md#mt19) explica contratos, Receipt e verificadores em mais detalhe.

O estado atual varia por skill. Na policy consultada para este capítulo, `hub-ml-concierge` está L1/audit e encerra na recomendação; `hub-ml-comentar-notebook` e `hub-ml-micromodelos` também estão L1/audit. `hub-ml-auditoria-skills` e `hub-ml-criar-objeto` estão L3/audit. `hub-ml-eda-profissional` está L4/enforce. Várias skills analíticas, como baseline, safra, cross-EDA, features, explicabilidade, monitoramento, pipeline e validação estatística, ainda têm `current_level=L0` mesmo quando o alvo é L3 ou L4; `hub-ml-tutor-databricks` é L0/guidance. O escopo técnico B1 já integrou perfis executáveis delimitados para essas oito skills, com contratos e verificadores próprios; isso não promoveu seus níveis L0/audit nem demonstrou orquestração universal pela Genie Code. Um runner disponível pode produzir evidência de seu perfil sintético, mas não certifica outros dados ou operações. Leia o `scripts/README.md` da skill e confira o perfil, os inputs e os efeitos autorizados. Um script encontrado na pasta não eleva essa policy. Para cada tarefa, consulte o valor vigente antes de exigir ou alegar uma prova que só pertence a outro nível.

Na EDA profissional selecionada, a rota completa usa `scripts/run_enforced.py`, que reúne a execução canônica e evidência para L4. Depois, `scripts/postflight.py::finalize_or_raise` confronta resultado, recursos, templates e resumo de entrega. Só `postflight.status="PASS"` com `completion.authorized=true` permite dizer que a skill terminou conforme seu contrato. `PENDING_POSTFLIGHT` significa que falta a verificação final; um Receipt `VALID` isolado comprova a etapa L3, não o fechamento L4. Se o preflight bloquear por recurso ou entrada faltante, peça o dado objetivo, corrija e inicie uma nova execução canônica, ou relate “não concluída”. O [SKILL de EDA](skills/hub-ml-eda-profissional/SKILL.md) define esse comportamento.

Essa exigência fica clara em uma entrega bloqueada. Imagine que você selecionou `@hub-ml-eda-profissional`, mas proibiu `run_enforced` e postflight no mesmo pedido. O contrato da skill trata as instruções como conflitantes; uma análise manual na mesma tarefa não recebe selo de conclusão L4 por ganhar um aviso de ressalva. A resposta útil explica o conflito, identifica os entrypoints exigidos e solicita uma nova decisão sobre a rota; enquanto isso, a EDA fica **não concluída**. A mesma cautela vale se o runner retornar bloqueio ou o postflight não passar. Não atribua a uma skill L0 essa regra específica de EDA L4; confira sua policy e o próprio `SKILL.md`.

Ao revisar uma resposta, percorra uma escada curta de evidência: recurso **citado**, **localizado**, **lido**, helper **importado**, **chamado** e **concluído**. Uma etapa não prova a seguinte. Para cada afirmação importante, peça caminho e versão consultados, entrada, operação, saída e evidência de conferência. Se a interface ou o runtime não mostrar uma dessas etapas, registre “não observável”, em vez de inventar um PASS ou concluir que não ocorreu. Separe também a qualidade da análise da aderência ao contrato: uma tabela aparentemente plausível pode ter sido produzida por outro caminho, e um Receipt íntegro não valida automaticamente interpretação, população ou decisão.

Leia um Receipt como vínculo técnico entre uma execução, seus insumos e a saída registrada, não como uma assinatura de que a decisão de negócio é boa. Quando houver verificador aplicável, confira se foi realmente executado na mesma base e release; copiar um status antigo não revalida a execução atual. No resumo final, procure também perguntas abertas, recursos pulados com justificativa e origem de cada número. Se o resultado disser que uma coluna é inadequada, peça a regra ou limiar usado, o denominador e o período. Esses detalhes permitem a uma pessoa refazer a conclusão e discordar dela com fundamento.

<a id="mu04-4"></a>
#### 4. Compor recursos e recuperar uma resposta fora do fluxo

Quando a tarefa atravessa várias etapas, passe adiante somente premissas verificadas. Uma sequência plausível é EDA da fonte, diagnóstico de junção, plano de features e, depois, baseline. A EDA responde se a fonte é compreendida; a análise cruzada pergunta se fontes se ligam sem multiplicação ou vazamento temporal; a skill de features define o que existia no ponto de decisão; o baseline testa uma referência de modelo. Essas etapas não viram uma execução única porque o pedido mencionou quatro skills. Faça um **handoff** curto: objetivo, fontes e versões, grão, chaves, tempo, resultados observados, lacunas, restrições, estado das aprovações e pergunta da próxima etapa. O Concierge pode sugerir essa composição, mas sua rota termina na recomendação; [MU03](#mu03) ensina a ler cobertura e confiança da busca.

Considere uma resposta que afirma “a EDA está concluída” e cita `quick_profile`, mas não mostra chamada, resultado nem postflight. Primeiro peça o registro da rota executada e o estado de conclusão. Se o helper só apareceu no texto, classifique-o como citado; se foi importado, não presuma que foi chamado. Se não existe evidência de execução, aproveite as perguntas e o plano como rascunho, mas não use os números como resultado validado. Na EDA L4, peça a finalização canônica ou a declaração explícita de que ela não terminou. Em uma skill L0, confira as fontes, o código e os resultados pelos meios disponíveis, sem fabricar um Receipt obrigatório que a policy ainda não implementa.

Quando uma resposta usa uma skill diferente da pretendida, verifique primeiro o pedido e o objeto anexado. “Explique este erro” sem a mensagem de erro pode não oferecer contexto suficiente; acrescente o trecho real e selecione `@hub-ml-tutor-databricks` se essa é a tarefa. Se a seleção ocorreu e a resposta ignorou o escopo, aponte a seção pertinente do `SKILL.md`, diga o que faltou e peça uma correção delimitada. Se houve escrita ou execução fora do plano, registre o efeito e revise o artefato produzido antes de continuar. A [skill de auditoria](skills/hub-ml-auditoria-skills/SKILL.md) separa revisão da implementação de revisão do output e pode ajudar quando o desvio for material.

Uma última conferência de aprendizado cabe antes do próximo capítulo: você consegue dizer **qual skill foi selecionada**, **qual versão ou arquivo foi lido**, **o que executou**, **que gate passou** e **o que ainda depende de revisão**? Se uma resposta é desconhecida, escreva a lacuna no handoff. Para transformar a próxima tarefa em um pedido preenchível, siga [MU05](#mu05); para entender como policy e evidência são construídas, continue no [capítulo técnico de execução verificável](MANUAL_TECNICO_V2.md#mt19).

<!-- editorial:exclude:start -->
Fontes principais: [catálogo de skills](skills/README.md), [policy vigente](hub_padroes/skill_enforcement/policy.json), [guia de policy](hub_padroes/skill_enforcement/README.md), [SKILL de EDA](skills/hub-ml-eda-profissional/SKILL.md), [SKILL do Concierge](skills/hub-ml-concierge/SKILL.md), [ADR-0021](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0021-execucao-verificavel-de-skills.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU03](#mu03) · [Próximo: MU05](#mu05) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT19](MANUAL_TECNICO_V2.md#mt19)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu05"></a>
<a id="mu05"></a>
### MU05 — Escolher e preencher os 18 briefings

**Pergunta deste capítulo:** qual formulário usar e como preencher o que falta sem inventar dados? Um briefing transforma uma intenção em pedido verificável. Comece pela decisão que precisa tomar; escolha o formulário e confira o que a resposta realmente fez.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](#sumario-mu) · [Usar skills](#mu04) · [Prompts no Manual Técnico](MANUAL_TECNICO_V2.md#mt12) · [Próxima tarefa](#mu06)
<!-- editorial:exclude:end -->

<a id="mu05-1"></a>
#### 1. Registrar objetivo, fonte, grão, chaves, tempo e desconhecidos

Antes de copiar um texto, escreva qual decisão você espera apoiar. “Fazer análise exploratória de dados (EDA)” é uma atividade: examinar estrutura, qualidade e distribuições de uma fonte antes de decidir o próximo estudo. O [briefing de EDA rápida](hub_prompts/eda_rapida/README.md) mostra um primeiro recorte; já a formulação “decidir se a tabela de clientes pode sustentar um estudo de churn” delimita o resultado. Diga quem usará a resposta e qual artefato ajudará: diagnóstico, reconciliação, plano, código ou relatório. O [índice dos prompts](hub_prompts/README.md) ajuda a escolher entre os 18 briefings manuais desta versão. Cada pasta contém um README que explica adequação e limites, um `.md` com campos para preencher e um `exemplo_*.py` que apresenta um cenário. O briefing não é uma skill descoberta automaticamente; depois de preenchê-lo, você o envia ao Genie Code e, se quiser, seleciona uma skill pertinente com `@`.

Nomeie a **fonte** de modo que ela possa ser localizada: tabela `catalog.schema.table`, DataFrame já criado, notebook, modelo/run ou documento. Diga o que uma linha representa, isto é, o **grão**: uma linha por cliente, transação, contrato ou mês não são unidades intercambiáveis. Declare a chave candidata e o que torna duas linhas comparáveis. Para duas tabelas, informe o grão e as chaves de cada uma; uma coluna de mesmo nome pode ter significado ou cardinalidade diferente. Quando houver target, defina o evento positivo e o horizonte da previsão. Não envie credenciais, dados pessoais desnecessários ou uma amostra sensível apenas para preencher o formulário.

O **tempo** pede mais que uma data no schema. Informe período analisado, fuso quando relevante, data de ocorrência, data de ingestão ou disponibilidade e momento em que a decisão seria tomada. Um valor registrado depois da decisão não pode entrar silenciosamente como preditor anterior. Para safra, indique coorte, idade da coorte e quando o evento amadurece; para monitoramento, separe janela de referência da atual e diga quando o rótulo fica conhecido. Se você ainda não tem essas informações, escreva `NÃO INFORMADO`. Esse marcador obriga a resposta a apontar a investigação necessária, sem fabricar uma coluna ou assumir “mês anterior”.

Complete também o **modo de trabalho**: explicação, plano, código ou execução. Um plano pode sugerir consultas e testes; não autoriza por si só criar tabela, sobrescrever destino, treinar modelo ou agendar job. Declare limite de custo/tempo, permissões conhecidas, operações proibidas e o formato do resultado. Para execução, peça primeiro a lista de efeitos: leituras, escritas, nomes completos dos destinos, amostragem, coleta ao driver e condição de repetição. [MU04](#mu04) mostra como conferir a skill selecionada e os gates que ela realmente implementa. Um prompt que recomenda uma skill não prova sua seleção nem satisfaz o contrato da skill.

Leia os placeholders como perguntas. `{{TABELA}}` pede uma fonte concreta; `{{CHAVE}}` pode receber `NÃO INFORMADO` e uma instrução para descobrir candidatos; `{{PERIODO}}` precisa distinguir recorte de análise e janela disponível. Não substitua lacunas por nomes plausíveis. Se faltam fonte e objetivo, o próximo resultado útil é uma pergunta de esclarecimento; se a fonte existe mas não há chave confiável, pode ser um plano para testar unicidade e junções. O pedido bem preenchido reduz ambiguidade, mas a resposta ainda precisa ser conferida contra o contrato do briefing e o dado real. A sequência é briefing, skill selecionada, policy, contrato da rota e helpers. Perfis sintéticos integrados têm entradas e limites próprios; não tornam todo pedido executável nem promovem a policy por associação.

Guarde a versão enviada do texto. Se você mudar chave, período ou modo depois da primeira resposta, anote a mudança para não atribuir conclusões novas ao pedido antigo. Essa trilha ajuda outra pessoa a reproduzir a decisão e a separar hipótese inicial de evidência obtida.

<a id="mu05-2"></a>
#### 2. Escolher entre as rotas de briefing

Escolha pelo produto que deseja receber. As rotas abaixo são pedidos manuais, não comandos executáveis. Cada par README/`.md` mostra campos e revisão esperada; os três casos com pedido copiável aparecem na seção seguinte. Ao comparar opções próximas, leia o limite de cada README e prefira o briefing que produz a decisão principal; análises secundárias podem vir depois.

<a id="mu05-route-auditoria-skills"></a>
##### `auditoria_skills` — conferir implementação ou resultado

Use [auditoria_skills](hub_prompts/auditoria_skills/README.md) quando quiser saber se uma skill foi construída conforme seu contrato ou se um output produzido com ela merece confiança. Escolha o objeto **IMPLEMENTAÇÃO** ou **OUTPUT** e, separadamente, a ação **AUDITORIA**, **PLANO DE CORREÇÃO** ou **CORRIGIR AUTORIZADO** no [briefing](hub_prompts/auditoria_skills/auditoria_skills.md); identifique a skill alvo e anexe `SKILL.md`, contrato, código, pedido e resposta conforme o modo. Peça requisito, evidência, lacuna e gravidade por achado. Um relatório de auditoria sem artefato lido deve dizer o que ficou não observável. A recomendação de `@hub-ml-auditoria-skills` não executa o auditor automaticamente; confira seleção e trilha de evidência. Não transforme um checklist preenchido em aprovação de comportamento no Databricks.

<a id="mu05-route-comentar-notebook"></a>
##### `comentar_notebook` — documentar código existente

Escolha [comentar_notebook](hub_prompts/comentar_notebook/README.md) quando um notebook precisa ficar compreensível para outra pessoa. No [formulário](hub_prompts/comentar_notebook/comentar_notebook.md), indique notebook ou células, público, profundidade e modo **REVISÃO**, **EDIÇÃO** ou **DOCUMENTAÇÃO**. Diga quais células e resultados devem permanecer intocados e se há dados sensíveis nos outputs. Peça explicações antes do código e interpretação depois dele, sem inferir que um comentário prova reexecução. Se você só quer sugestões, mantenha o modo de revisão; se autoriza edição documental, confira o diff e a preservação do código e da ordem das células. A rota de skill recomendada é `@hub-ml-comentar-notebook`. Uma entrega clara identifica também as células que não foram examinadas.

<a id="mu05-route-cross-eda"></a>
##### `cross_eda` — avaliar fontes em conjunto

Use [cross_eda](hub_prompts/cross_eda/README.md) para decidir se duas ou mais fontes podem alimentar uma análise ou modelo. No [pedido](hub_prompts/cross_eda/cross_eda.md), informe entidade, grão de cada tabela, chaves, período, target, horizonte e ponto de decisão; anexe EDAs anteriores quando existirem. Peça cardinalidade e cobertura de junção, perdas, multiplicação de linhas e disponibilidade histórica das colunas. Timestamp de evento não garante que o valor estava disponível antes do cutoff. Sem prova temporal, a resposta deve propor teste e declarar prontidão pendente, mesmo que a cobertura de join seja alta. A skill sugerida é `@hub-ml-cross-eda-ml`. Registre a população que ficou sem correspondência após a junção.

<a id="mu05-route-data-quality"></a>
##### `data_quality` — transformar suspeitas em regras

Escolha [data_quality](hub_prompts/data_quality/README.md) se a decisão depende de completude, unicidade, validade, consistência, integridade, atualidade ou volume. O [briefing](hub_prompts/data_quality/data_quality.md) pede fonte, grão, chaves, colunas temporais, período, consumidor downstream e regras conhecidas. Para cada regra, peça numerador, denominador, origem do limiar e população afetada. Uma taxa de nulos não determina sozinha se a tabela serve ao negócio. Solicite scorecard e plano de investigação; não trate o pedido como deploy de expectations ou correção automática dos dados. A rota recomendada usa `@hub-ml-eda-profissional` e seus gates vigentes quando selecionada. Peça prioridade de investigação conforme o impacto no uso declarado.

<a id="mu05-route-eda-completa"></a>
##### `eda_completa` — aprofundar uma fonte

Use [eda_completa](hub_prompts/eda_completa/README.md) quando o perfil inicial já mostrou perguntas que exigem distribuições, recortes, relações e gráficos. No [formulário](hub_prompts/eda_completa/eda_completa.md), declare fonte, pergunta de negócio, grão, chave, coluna temporal, período, volume, foco, restrições e target somente quando existir. Peça achados separados de hipóteses, gráficos que respeitem o tamanho da base e um backlog de verificações. Correlação ou diferença por segmento não estabelece causa; ausência de problema na amostra não certifica a população. A skill sugerida é `@hub-ml-eda-profissional`; se for selecionada para execução completa, confira a rota L4 descrita em [MU04](#mu04). Solicite a origem e a população de cada gráfico apresentado.

<a id="mu05-route-explainability"></a>
##### `explainability` — explicar um modelo identificado

Escolha [explainability](hub_prompts/explainability/README.md) para compreender o comportamento de uma versão específica de modelo. Preencha no [pedido](hub_prompts/explainability/explainability.md) o modelo/run, dataset e split, período, target e classe, público, método pretendido ou critério de escolha e tamanho de amostra. Diferencie explicação global da explicação de um caso. Peça limites, estabilidade e possível vazamento antes de comunicar drivers. [SHAP](https://shap.readthedocs.io/en/latest/index.html) (*SHapley Additive exPlanations*) é um método que atribui contribuições das variáveis à saída do modelo. Nem importância de variável nem valor SHAP demonstram causa do desfecho; uma explicação de outra versão não responde à pergunta. `@hub-ml-explainability` é a skill sugerida, sem implicar cálculo já executado ou registro no MLflow. Confira se a população explicada corresponde à pergunta inicial.

<a id="mu05-route-feature-engineering"></a>
##### `feature_engineering` — desenhar atributos no tempo

Use [feature_engineering](hub_prompts/feature_engineering/README.md) quando já sabe entidade, target e momento da decisão. O [briefing](hub_prompts/feature_engineering/feature_engineering.md) pede chave, janela de observação, cutoff, horizonte, fontes, junções, frequência e restrições de materialização. Peça especificação por feature, teste de disponibilidade e risco de vazamento entre treino e inferência. Se a data em que o fato ocorreu difere da data em que chegou ao sistema, ambas importam. Sem janela ou cutoff definidos, receba um plano de descoberta, não código que presume causalidade temporal. A skill sugerida é `@hub-ml-feature-engineering`; o formulário não cria tabela de features. Registre quais fontes ainda exigem validação de acesso.

<a id="mu05-route-monitoramento-modelo"></a>
##### `monitoramento_modelo` — investigar mudança operacional

Escolha [monitoramento_modelo](hub_prompts/monitoramento_modelo/README.md) para distinguir falha de serviço, mudança de população, drift e queda de performance. Identifique no [pedido](hub_prompts/monitoramento_modelo/monitoramento_modelo.md) modelo/run, endpoint ou job, referência, janela atual, atraso de maturação do rótulo, métricas, direção desejada, segmentos e responsáveis. Peça limites de comparação e ações condicionais. O [Population Stability Index (PSI)](hub_snippets/spark/psi_calculator/README.md) resume quanto a distribuição de uma variável mudou entre referência e população atual. Um alerta de PSI não demonstra deterioração de performance; sem rótulo maduro, uma taxa de acerto aparente pode ser enganosa. A skill sugerida é `@hub-ml-monitoramento-modelo`. O briefing não instala monitor, agenda job ou autoriza retreino. Peça as proporções por faixa e confira população de referência, volume e limiares definidos no contexto antes de propor uma ação.

<a id="mu05-route-micromodelo-novo"></a>
##### `micromodelo_novo` — especificar um objetivo conhecido

Use [micromodelo_novo](hub_prompts/micromodelo_novo/README.md) com `@hub-ml-micromodelos` no modo `OBJETIVO_CONHECIDO`. Informe decisão, característica, entidade/grão, população, horizonte, fontes, dono e restrições. O [formulário](hub_prompts/micromodelo_novo/micromodelo_novo.md) pede proveniência e um plano de estudo. Só peça `micromodelo.yaml` quando template e schema MM01 estiverem acessíveis; sem eles, aceite checklist textual, `YAML_NAO_CRIADO` e `MM01_NAO_VALIDADO`. Informação fornecida no pedido não vira observação de catálogo. Ausência de evidência continua indeterminada, e um score heurístico não é probabilidade calibrada.

<a id="mu05-route-descobrir-micromodelos"></a>
##### `descobrir_micromodelos` — explorar oportunidades delimitadas

Escolha [descobrir_micromodelos](hub_prompts/descobrir_micromodelos/README.md) quando a decisão está clara, mas a característica ainda não foi escolhida. No [briefing](hub_prompts/descobrir_micromodelos/descobrir_micromodelos.md), delimite área, população, catálogo autorizado ou fixture textual, restrições e critérios qualitativos. A skill produz candidatas para revisão, com cobertura e incerteza; não consulta registros por associação. Metadados fornecidos recebem `FORNECIDA`; nomes e tipos não comprovam viabilidade ou ausência de vazamento. Escolha humana precede o início do YAML. A skill permanece L1/audit, e o prompt não possui nível ou autorização próprios.

<a id="mu05-3"></a>
#### 3. Preencher, enviar e acompanhar os exemplos

As oito rotas seguintes incluem três pedidos copiáveis. Os nomes de tabela, modelo e notebook são fictícios; cada bloco pede plano ou orientação e não relata execução.

<a id="mu05-route-eda-rapida"></a>
##### `eda_rapida` — primeiro perfil de uma tabela

Use [eda_rapida](hub_prompts/eda_rapida/README.md) quando recebeu uma fonte nova e precisa decidir o que investigar primeiro. O [briefing](hub_prompts/eda_rapida/eda_rapida.md) pede tabela, objetivo, foco, chave e coluna temporal candidatas, filtros, período e limite de custo. No exemplo abaixo, `id_cliente` é apenas candidata: solicite teste de unicidade antes de chamá-la de chave. O período evita misturar fotografias diferentes; o modo “plano” impede tratar sugestão de consulta como resultado. Peça até oito achados priorizados com evidência e limite de amostragem. A skill recomendada é `@hub-ml-eda-profissional`, cujo fechamento de execução segue [MU04](#mu04). Confirme quais colunas ficaram fora do perfil inicial.

```text
@hub-ml-eda-profissional
Use o briefing eda_rapida para planejar um perfil inicial de
catalogo_exemplo.dados.clientes. Objetivo: avaliar se a base permite um
diagnóstico de clientes ativos. Grão informado: uma linha por cliente;
chave candidata: id_cliente, ainda não verificada. Data: NÃO INFORMADO.
Recorte: setembro de 2026. Limite: proponha consultas de custo moderado.
Primeiro entregue plano, verificações e dúvidas; não execute nem escreva.
```

<a id="mu05-route-comparar-tabelas"></a>
##### `comparar_tabelas` — reconciliar A e B

Use [comparar_tabelas](hub_prompts/comparar_tabelas/README.md) para investigar diferença entre versões de uma tabela, implementações ou populações. No [formulário](hub_prompts/comparar_tabelas/comparar_tabelas.md), identifique A/B, grão e chaves de cada lado, período, fuso, filtros, tolerâncias e foco: schema, contagem, chaves ou valores. O exemplo declara a tolerância desconhecida para não inventar um veredito. Peça matriz de schema, scorecard e amostras de divergências com denominadores, além de cardinalidade do join. Mesmo schema não prova semântica ou população iguais. Defina antes se é reconciliação determinística independente ou execução de EDA, cross-EDA ou monitoramento. SQL/PySpark direto não substitui o runner de uma EDA protegida já selecionada; “somente leitura” requer conferência dos efeitos reais. Registre divergências que exigem decisão humana antes do veredito.

```text
Compare catalogo_exemplo.dados.clientes_v1 (A) e
catalogo_exemplo.dados.clientes_v2 (B), sem executar nesta etapa.
Grão esperado em ambas: uma linha por cliente; chave candidata: id_cliente.
Período: setembro de 2026; fuso: NÃO INFORMADO.
Filtros e tolerância de valores: NÃO INFORMADO.
Primeiro mostre como conferir população, cardinalidade e diferenças;
marque decisões que dependem de regra de negócio ainda ausente.
```

<a id="mu05-route-baseline-orchestration"></a>
##### `baseline_orchestration` — definir uma linha de base

Use [baseline_orchestration](hub_prompts/baseline_orchestration/README.md) para desenhar o primeiro modelo comparável antes de otimizar. O [briefing](hub_prompts/baseline_orchestration/baseline_orchestration.md) precisa de entidade, grão, target/evento positivo, momento de observação, maturação do rótulo, cutoff, horizonte, split, métrica, custo e modo. No exemplo, a maturação desconhecida impede treinar com segurança; peça primeiro a regra e uma divisão sem vazamento. Um baseline ingênuo ajuda a interpretar ganho, mas não prova valor de negócio. `@hub-ml-baseline-ml` orienta a rota atual da policy; o pedido não treina nem registra run automaticamente. Compare desempenho por período e segmento antes de escolher alternativa para investigação.

```text
@hub-ml-baseline-ml
Planeje um baseline para prever cancelamento em 30 dias por cliente.
Fonte: catalogo_exemplo.dados.clientes_mensal; grão: cliente-mês;
chave: id_cliente + mes_referencia. Evento positivo: cancelou=1.
Maturação do rótulo e data real de disponibilidade: NÃO INFORMADO.
Proponha cutoff, split temporal, baseline ingênuo e métricas justificadas.
Não treine, registre run ou persista artefatos antes de esclarecer as lacunas.
```

<a id="mu05-route-novo-projeto"></a>
##### `novo_projeto` — estruturar o início

Use [novo_projeto](hub_prompts/novo_projeto/README.md) quando ainda precisa transformar uma demanda ampla em charter e backlog. No [briefing](hub_prompts/novo_projeto/novo_projeto.md), preencha nome estável, problema, decisão, donos, critérios de aceite, métricas, fontes, ambientes, repositório, entregáveis e modo de trabalho. Peça riscos e dependências antes de gerar recursos. Uma fonte mencionada ainda precisa de permissão e validação; não coloque tokens ou caminhos corporativos no pedido compartilhável. O Genie Code pode organizar perguntas sem uma skill específica. Separar desenho de criação efetiva evita que um charter seja relatado como projeto implantado. Confirme quem aprovará a próxima fase do projeto.

<a id="mu05-route-pipeline"></a>
##### `pipeline` — planejar fluxo de dados

Escolha [pipeline](hub_prompts/pipeline/README.md) quando a decisão é como transformar e entregar dados repetidamente. O [formulário](hub_prompts/pipeline/pipeline.md) pede fontes, destinos, consumidores, batch ou streaming, cadência, chaves, schema, qualidade, objetivo de serviço, ambientes, reprocessamento e idempotência. Peça um plano por etapa e testes para repetição sem duplicar ou perder registros. Uma meta de latência não é prova de que o job a cumprirá. `@hub-ml-pipeline-builder` pode orientar o método; texto YAML ou código sugerido não publica Lakeflow, não cria job e não confirma permissão de escrita no destino. Defina responsável por falhas, alertas e reprocessamento.

<a id="mu05-route-safra"></a>
##### `safra` — comparar coortes com maturidade igual

Use [safra](hub_prompts/safra/README.md) para comparar grupos formados em meses ou eventos diferentes. O [briefing](hub_prompts/safra/safra.md) exige entidade, chave, data de coorte, idade da coorte, evento, numerador, denominador, métrica, censura e período observado. Peça uma curva por idade comparável, marque células que ainda não amadureceram e separe efeito de calendário de diferença entre coortes. Uma célula imatura não é zero; taxas cumulativas não devem ser somadas. `@hub-ml-analise-safra` é a skill sugerida. O prompt não calcula uma safra sozinho nem valida regra regulatória sem fonte própria. Compare somente idades de coorte efetivamente observadas em ambos os grupos.

<a id="mu05-route-stat-check"></a>
##### `stat_check` — testar uma hipótese delimitada

Escolha [stat_check](hub_prompts/stat_check/README.md) quando uma diferença observada precisa ser avaliada com pressupostos, efeito e incerteza. O [pedido](hub_prompts/stat_check/stat_check.md) deve dizer pergunta/estimando, dataset, grão, grupos, target, amostra ou população, tempo, método pretendido ou critério de escolha, hipóteses e nível de decisão. Solicite diagnóstico de dependência temporal e multiplicidade antes de interpretar um p-valor. Significância estatística não equivale a tamanho de efeito útil nem a causalidade. `@hub-ml-validacao-estatistica` é a rota sugerida; sem dados examinados, a resposta só pode oferecer plano de teste. Peça também intervalo de incerteza e alternativa metodológica se os pressupostos falharem.

<a id="mu05-route-tutor-explicar"></a>
##### `tutor_explicar` — aprender com objeto real

Use [tutor_explicar](hub_prompts/tutor_explicar/README.md) quando quer entender código, erro ou conceito aplicado à sua tarefa. Anexe no [briefing](hub_prompts/tutor_explicar/tutor_explicar.md) o objeto ou a pergunta concreta; informe nível iniciante, intermediário ou avançado, profundidade, objetivo, ambiente e restrições. Peça que o assistente separe o que leu no arquivo do que inferiu sobre runtime. Uma analogia ajuda a aprender, mas deve declarar onde deixa de descrever o mecanismo. `@hub-ml-tutor-databricks` é a skill sugerida. A explicação não comprova execução ou correção do código não examinado. Uma pergunta de retorno aplicada ao mesmo objeto pode testar sua compreensão.

Depois de escolher o briefing, abra seu `exemplo_*.py` como **documento de ensino**. A Parte 1 pode preparar dados e executar células; confira destino antes de rodar, pois 13 dos 18 exemplos atuais usam `mode("overwrite")` em tabelas sintéticas. A Parte 2 mostra um pedido preenchido para copiar e adaptar manualmente ao chat. A Parte 3 reserva espaço para a resposta obtida e revisada: nos 16 exemplos anteriores, ela ainda diz `NÃO EXECUTADO`. Os dois novos exemplos de Micromodelos têm preparo textual local E0, sem tabela, e registros de conversa E1 no Free de 29/09/2026. Essas conversas não demonstram runtime E1, consulta de catálogo ou validação MM01. No objetivo conhecido, a resposta chamou dados fornecidos de observados; na descoberta, usou “viáveis” para hipóteses ainda indeterminadas e criou células apesar do pedido de resposta no chat. Preserve essas ressalvas ao estudar o caso. A marca pendente não é falha a ocultar; evita apresentar uma conversa que nunca ocorreu como evidência de Genie Code. A conversa datada, por sua vez, não transfere aprovação aos demais exemplos. Anote data, fonte, modo, seleção da skill e efeito observado se um dia registrar uma resposta real.

<a id="mu05-4"></a>
#### 4. Conferir a resposta e corrigir lacunas

Depois de enviar o briefing, compare a resposta com o **pedido que você realmente enviou**, não com a intenção que ficou na sua cabeça. Ela identificou fonte, grão, período e modo? Separou dado observado de hipótese? Explicou denominadores, filtros e unidades antes de apresentar taxas? Indicou quais arquivos, tabelas e versões foram lidos? Se prometeu código, existe entrada, dependências, saída esperada e aviso de efeitos? Uma resposta elegante pode falhar nesses pontos. No [índice dos prompts](hub_prompts/README.md), cada formulário traz o que conferir; use esse checklist como começo, adaptado à sua decisão.

No exemplo de EDA rápida, a entrega correta para o pedido **em modo plano** descreve verificações de grão, chave, data desconhecida, custo e prioridades. Não deve apresentar porcentagem de nulos calculada nem dizer que a tabela está aprovada sem leitura e execução. Se aparecer “nenhuma duplicata” sem consulta observada, marque o número como não verificado e peça a consulta ou evidência correspondente. Se a skill de EDA foi selecionada e uma execução completa ocorreu, confira também os gates atuais explicados em [MU04](#mu04); mencionar a skill não prova postflight aprovado.

Na comparação A/B, uma diferença de contagem só é interpretável quando as duas populações usam período, fuso e filtros compatíveis. Peça as contagens antes e depois da junção, número de chaves sem par e multiplicação por cardinalidade. Se a tolerância estava `NÃO INFORMADO`, o assistente pode mostrar diferenças, mas não inventar um limite para declarar equivalência. Corrija o briefing com a regra decidida pelo responsável e peça nova avaliação apenas do veredito afetado. Essa sequência mantém a primeira resposta como diagnóstico, não a apaga nem a chama de reconciliação aceita.

No baseline, leia o plano na ordem temporal: momento de observação, chegada de cada atributo, maturação do rótulo, corte entre treino e teste e métrica. Se a maturação continuou desconhecida, um split sugerido é hipótese de desenho, não treino autorizado. Peça primeiro a origem da regra do rótulo; depois revise o split e só então decida sobre execução e tracking. Uma métrica sem população e janela não basta para escolher modelo. O [briefing de baseline](hub_prompts/baseline_orchestration/baseline_orchestration.md) ajuda a localizar os campos que ficaram sem resposta.

Quando faltar informação, faça um **follow-up delimitado**. Cite o campo, a frase problemática e o efeito: “Você assumiu `id_cliente` como chave; no pedido ela era candidata. Mostre como testar unicidade sem escrever tabela e revise apenas o diagnóstico de duplicidade”. Para corrigir modo: “Pedi plano; identifique quais comandos foram apenas sugeridos e se algo foi executado”. Para corrigir acesso: “Marque como não observável o que não pôde ler e dê o caminho tentado”. Essas perguntas produzem uma revisão verificável; “refaça tudo” perde o rastro das premissas.

Registre no notebook de exemplo a resposta real somente após obtê-la, revisar efeitos e indicar ambiente e data. Preserve `NÃO EXECUTADO` na Parte 3 enquanto não houve conversa ou execução correspondente. A Parte 1 que prepara dados sintéticos pode ter escrito uma tabela mesmo que a Parte 3 continue vazia; relate esses eventos separadamente. Os 13 exemplos com `overwrite` exigem conferir destino antes de rodar, inclusive em um ambiente de testes. Se a resposta não seguiu o modo ou a skill escolhida, corrija o pedido e o estado da evidência antes de avançar. Para a próxima ação com uma função isolada, siga [MU06](#mu06); para o contrato técnico dos briefings, consulte [MT12](MANUAL_TECNICO_V2.md#mt12).


<!-- editorial:exclude:start -->
[Anterior: MU04](#mu04) · [Próximo: MU06](#mu06) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT12](MANUAL_TECNICO_V2.md#mt12)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu06"></a>
<a id="mu06"></a>
### MU06 — Usar um snippet isoladamente

**Pergunta deste capítulo:** como chamar uma função do Hub diretamente e saber se ela responde à pergunta certa? Você precisa localizar a cópia autorizada de `.assistant`, conseguir executar Python e conhecer a unidade do dado de entrada. Para a receita Spark, também precisa de uma sessão e de um DataFrame PySpark. Pode seguir a primeira receita diretamente no notebook. Se a tarefa já estiver sob uma skill com rota protegida, uma chamada isolada não substitui seus gates.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](#sumario-mu) · [Primeiro uso](#mu02) · [Scripts isolados](#mu07) · [Fundamentos técnicos dos snippets](MANUAL_TECNICO_V2.md#mt05)
<!-- editorial:exclude:end -->

<a id="mu06-1"></a>
#### 1. Escolher a função e ler seus requisitos

Imagine que você já calculou uma taxa de resposta e só quer mostrá-la em português no relatório. Abrir uma skill inteira para essa apresentação seria uma etapa adicional desnecessária: um snippet é uma função ou classe reutilizável que você chama no seu próprio código. A escolha começa pela **pergunta**, não pela semelhança do nome. Para exibir uma taxa já calculada, procure `format_br`; para descobrir quantos valores `NULL` existem em cada coluna de um DataFrame Spark, procure `null_summary`. Uma função que produz um texto não resolve uma dúvida de qualidade dos dados, e um resumo de nulos não calcula uma taxa de resposta.

Comece pelo [catálogo de snippets](hub_snippets/README.md), escolha a categoria e abra o README da pasta do objeto. Cada pasta operacional aproxima quatro peças com usos distintos: o README ajuda a decidir; `__init__.py` mostra os nomes que podem ser importados pela interface pública; o arquivo da implementação define a assinatura e o comportamento; `exemplo_*.py` demonstra uma situação com dados sintéticos. Leia a seção “quando usar” junto com “quando não usar”. Isso impede que uma saída atraente seja tratada como resposta a uma pergunta que a função nunca recebeu.

No [README de `format_br`](hub_snippets/constants/format_br/README.md), o quadro inicial diz que as seis funções recebem valores escalares e entregam **strings**, isto é, textos. Ele alerta que o cálculo deve estar pronto e que o texto não deve substituir o número quando ainda haverá soma ou comparação. A palavra “percentual” exige uma decisão prévia: `0.12` pode significar uma taxa de 12% escrita como fração; `12` pode significar os mesmos 12% já expressos na escala percentual. O formatador não adivinha qual convenção a sua base usa. Anote a escala ao lado do nome da variável antes de escolher `fmt_pct`.

No [README de `null_summary`](hub_snippets/spark/null_summary/README.md), os requisitos são diferentes: um **DataFrame PySpark** já disponível e limiares percentuais coerentes. DataFrame é uma tabela manipulada pelo código; PySpark é a interface Python para operações Spark distribuídas. Aqui, “nulo” quer dizer o `NULL` reconhecido por `isNull()`. String vazia, `"N/A"` e códigos sentinela não são contados automaticamente como ausência. A função devolve uma tabela de contagens e um semáforo escolhido pelos limiares, não um parecer geral sobre a qualidade da base. Se você precisa verificar duplicidade, recência e regras de domínio, escolha uma checagem mais ampla e consulte o capítulo de scripts.

Antes de continuar, formule uma frase verificável: “vou mostrar a taxa como texto, preservando o número original” ou “vou contar `NULL` na população completa e comparar com limiares que registrei”. Se você não consegue dizer qual população, unidade ou saída espera, a chamada pode executar corretamente e ainda assim responder à pergunta errada. O README local permite parar cedo e corrigir a escolha.

<a id="mu06-2"></a>
#### 2. Preparar o import e fazer uma chamada pequena

O caminho de arquivo e o caminho de importação têm papéis diferentes. A implementação de `fmt_pct` está em `hub_snippets/constants/format_br/format_br.py`; o import público é `hub_snippets.constants.format_br`. Os pontos são partes do nome de pacotes Python. A pasta que o Python precisa enxergar é **a que contém** `hub_snippets`, normalmente a `.assistant` da entrega. Uma tabela chamada `catalogo.esquema.tabela` usa pontos por outro motivo e não entra em `sys.path`. O [manual técnico vigente](MANUAL_TECNICO_V2.md#importacao) desenvolve essa distinção, caso você queira entender a busca de módulos.

Em um notebook onde a cópia autorizada do Hub esteja como arquivos do workspace, adapte somente a raiz do exemplo a seguir. O código verifica se a pasta esperada existe, evita inserir o mesmo caminho duas vezes e depois chama uma API pública. O bloco é **ilustrativo, não foi executado no seu workspace**; confirme o caminho real e a permissão de leitura antes de rodá-lo. A documentação oficial do [Azure Databricks sobre arquivos de workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace) ajuda a conferir o endereço usado pelo Python. A disponibilidade efetiva depende do ambiente em que o notebook roda.

```python
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if not (assistant_root / "hub_snippets").is_dir():
    raise FileNotFoundError(f"Hub não encontrado em {assistant_root}")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from hub_snippets.constants.format_br import fmt_pct

taxa_resposta_fracao = 0.12
taxa_resposta_texto = fmt_pct(taxa_resposta_fracao)
print(taxa_resposta_texto)  # saída esperada para este valor: 12,0%
```

Substitua `<username>` pela localização autorizada do seu Hub; a pasta pode estar em um Git folder ou outro endereço, conforme sua distribuição. `Path(...)` representa o endereço, não cria a pasta. `sys.path.insert` só altera a busca do interpretador da sessão: não instala pacotes e não concede acesso. A linha `from ... import fmt_pct` chega à [fachada pública](hub_snippets/constants/format_br/__init__.py), que reexporta a função implementada em `format_br.py`. Como o helper de formatação usa bibliotecas padrão do Python, o exemplo simples não requer Spark. O **notebook de exemplo** da pasta usa Spark para descobrir o usuário da sessão; essa necessidade pertence ao preparo daquele notebook, não à função `fmt_pct`.

Se você abriu `exemplo_format_br.py` no repositório, observe o marcador `# Databricks notebook source` na primeira linha e as divisões de células. Ele documenta um notebook de demonstração. A implementação `format_br.py` é o arquivo de biblioteca importado pela fachada; copiar o notebook inteiro para dentro de um módulo mudaria o papel dos arquivos. Na distribuição do Hub, esses dois tipos de `.py` precisam conservar seus formatos de workspace apropriados. Se houver dúvida sobre qual cópia foi importada, use `import inspect` e `print(inspect.getfile(fmt_pct))` para ver o caminho do arquivo carregado. Isso ajuda a detectar outro pacote na frente da sua lista de busca sem modificar dados ou permissões.

A assinatura real é `fmt_pct(v, casas=1, input_scale="ratio") -> str`. `v` é a taxa recebida; `casas` controla quantas casas decimais serão exibidas; `input_scale` diz se `v` está como fração (`"ratio"`) ou já como percentual (`"percent"`). O valor retornado é texto. Para uma entrada já na escala percentual, faça a escolha explícita: `fmt_pct(12, input_scale="percent")`. Não mude o número para obter uma aparência convincente sem verificar o significado na origem. Uma métrica pode ter sido multiplicada por cem antes de chegar ao notebook.

Uma segunda chamada usa outro tipo de entrada e outro compute. Se `base` é um **DataFrame Spark já preparado**, o bloco ilustrativo abaixo mede `NULL` em cada coluna. Escolha os limiares em percentuais de zero a cem conforme a política do seu caso; `5.0` e `20.0` são os padrões da API e servem aqui apenas para demonstrar a chamada, não para estabelecer uma regra de aceitação universal.

```python
from hub_snippets.spark.null_summary import null_summary

resumo = null_summary(base, threshold_warn=5.0, threshold_fail=20.0)
display(resumo)
```

Se o import de formatação funcionar e o de nulos falhar, isso não significa necessariamente que a biblioteca inteira esteja ausente. O segundo módulo importa `pyspark.sql`; confira se o ambiente disponibiliza PySpark e se `base` é mesmo um DataFrame Spark. Se `base` for pandas, procure um recurso apropriado para pandas em vez de tratar os objetos como intercambiáveis. Para notebooks serverless padrão, a documentação oficial de [configuração de dependências](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies), reconferida em 7/10/2026, orienta o painel **Environment**; a experiência Git Folder Serverless usa `pyproject.toml` na raiz da pasta. Siga a política do workspace e não instale PySpark por conta própria no serverless.

<a id="mu06-3"></a>
#### 3. Interpretar o retorno e conferir com poucos dados

Depois de executar, comece pelo **tipo** da saída. `fmt_pct(0.12)` deve produzir a string `"12,0%"`, enquanto `taxa_resposta_fracao` permanece numérica e disponível para cálculos. O formato apresentado só é útil se a escala estava certa. Veja o contraexemplo: `fmt_pct(12)` com o padrão `"ratio"` produz `"1200,0%"`. Não há exceção, porque 12 é um número válido para a função; quem conhece a origem da métrica é você. Na outra direção, `fmt_pct(0.12, input_scale="percent")` produziria `"0,1%"` com uma casa, aparentemente plausível em muitos relatórios e ainda assim errado para uma taxa originalmente de 12%.

Faça uma conferência mínima em uma célula pequena e mantenha os dois valores à vista. Para o cenário fictício de campanha, 12 respostas em 100 contatos dão fração `12 / 100 = 0.12`; o texto esperado é 12,0%. Uma comparação independente por aritmética simples é mais informativa do que olhar apenas se a célula terminou sem erro. `assert fmt_pct(0.12) == "12,0%"` verifica o caso conhecido quando o código está disponível. Esse `assert` não prova que a taxa da tabela real foi calculada com o denominador correto, mas detecta uma mudança inesperada no formato do exemplo. Guarde a taxa numérica na base e use a string na camada de apresentação.

O [código de `null_summary`](hub_snippets/spark/null_summary/null_summary.py) retorna um DataFrame Spark com `coluna`, `count_null`, `pct_null` e `status`, ordenado pela porcentagem decrescente. A interpretação exige ler as quatro colunas juntas. Se uma coluna tiver 13 `NULL` em 500 linhas, `100 × 13 / 500 = 2,6%`. Com aviso a 5% e falha a 20%, o status é verde; com aviso a 1% e falha a 10%, o mesmo dado é amarelo. O [notebook sintético do objeto](hub_snippets/spark/null_summary/exemplo_null_summary.py) registra exatamente essa comparação como resultado histórico de laboratório. Os números aqui ilustram o contrato e não afirmam que o notebook foi reexecutado no seu destino.

Para verificar uma base pequena sob seu controle, crie algumas linhas fictícias com uma coluna contendo `None`, chame a função e compare a contagem com o que você enxerga. Se preferir a fixture do Hub, leia antes sua [implementação](hub_snippets/testing/fixtures/fixtures.py): porcentagem configurada para geração aleatória é probabilidade por linha, não garantia de número exato de nulos. Registre tamanho da população e limiares junto ao resumo, porque o DataFrame retornado não contém esses dois thresholds como campos. Se você filtrar a base antes da função, estará medindo o recorte; isso pode ser desejado, mas deve aparecer no título da análise.

O semáforo responde apenas “qual percentual de `NULL` está acima dos limiares informados?”. Ele não sabe se a coluna deve ser obrigatória. Em uma coluna `data_cancelamento`, `NULL` pode representar uma pessoa ainda ativa, e verde ou vermelho não decide o tratamento correto. Da mesma forma, 30% de strings `"N/A"` podem conviver com zero `NULL` e aparecer verdes. Se o problema é ausência semântica, defina antes quais representações contam como ausentes e prepare uma checagem específica. Ao filtrar o resultado, compare `status` com os emojis reais; um filtro por texto `"ok"` não corresponde à saída e pode selecionar linhas inesperadas.

Um terceiro exemplo mostra por que nem todo snippet cabe numa chamada tão curta. O [helper temporal `pit_join`](hub_snippets/spark/pit_join/README.md) relaciona decisões com versões históricas que já estavam disponíveis em cada instante. Ele recebe fatos, histórico, chaves, colunas de tempo e um atraso de publicação obrigatório; devolve **um DataFrame e um dicionário de diagnóstico**. Se uma decisão fictícia ocorreu em 12/01/2026, uma versão de 08/01 com atraso de três dias já estava disponível em 11/01; uma versão de 11/01 só ficaria disponível em 14/01. Essa comparação pode ser refeita à mão antes de examinar uma saída Spark. Abra o README e o notebook específicos antes de usá-lo e siga o percurso de cruzamento temporal do manual. Uma tabela que só guarda o valor atual não reconstrói magicamente as versões passadas.

O teste pequeno deve reproduzir o **risco principal** de cada função: escala para formatação, denominador e representação de ausentes para nulidade, versão futura para junção temporal. Só depois passe a uma amostra representativa e confira schema, unidade, linhas e custos. Uma saída com formato correto e sem exceção ainda pode responder a uma população errada, uma data errada ou uma definição errada de ausência.

<a id="mu06-4"></a>
#### 4. Resolver falhas e escolher uma alternativa proporcional

Quando surgir `ModuleNotFoundError: No module named 'hub_snippets'`, examine primeiro a raiz inserida no `sys.path`: ela deve conter a pasta `hub_snippets`. Confirme que a cópia do Hub foi disponibilizada como arquivos acessíveis à sessão, que o nome da pasta está correto e que o caminho não aponta apenas para o notebook de exemplo. Um `PermissionError` pede verificação de acesso, não uma troca arbitrária de import. Se o erro nomeia uma dependência como `pyspark`, verifique o ambiente e a política de instalação aplicável; editar `sys.path` não instala essa dependência. Retome a chamada pequena depois de corrigir uma causa por vez.

Erros de argumento e erros silenciosos requerem tratamento diferente. Em `fmt_pct`, um `input_scale` fora de `"ratio"` e `"percent"` levanta `ValueError`; uma escala válida mas errada para o dado produz texto enganoso sem falhar. Em `null_summary`, os thresholds são aceitos sem conferir a faixa ou a ordem. Antes de automatizar, valide `0 <= threshold_warn <= threshold_fail <= 100`, trate uma base vazia separadamente e registre o que fazer quando a política não estiver definida. A implementação pode falhar ao converter agregados nulos em inteiros numa base sem linhas. Não transforme ausência em zero só para manter o fluxo em movimento.

Custo também faz parte da escolha. `fmt_pct` opera sobre um escalar no processo Python; não é uma instrução para formatar milhões de linhas Spark uma a uma no driver. `null_summary` dispara uma contagem da tabela e uma agregação que coleta uma **linha de resultados agregados** no processo Python; em tabela larga, o número de expressões acompanha o número de colunas. `pit_join` pode exigir uma junção por intervalo com muitos candidatos e contagens diagnósticas. No notebook, veja o plano de execução e teste volume adequado ao ambiente antes de inserir qualquer uma dessas chamadas num job recorrente.

Escolha uma alternativa quando a pergunta mudou. Para apenas exibir um valor isolado, a formatação nativa do Python pode bastar; para uma pequena tabela pandas apresentada ao leitor, veja `display.dataframe_styled`. Para conhecer uma tabela por várias dimensões, [quick_profile](hub_scripts/quick_profile/README.md) ou [data_quality_check](hub_scripts/data_quality_check/README.md) oferecem contratos mais amplos que `null_summary`, mas exigem outros preparos. Para dados sem versões temporais, uma junção comum pode bastar; com versões, especifique disponibilidade histórica antes de escolher `pit_join` ou outra solução. A semelhança de nomes não torna os retornos equivalentes.

Antes de encerrar, responda sem olhar o código: qual pergunta sua chamada respondeu, em qual população, com qual unidade e qual saída você verificou? Se a resposta envolver uma política de limiar, anote-a com o resultado. Se envolver tempo, anote instante de decisão, referência, atraso e fuso. Essa pequena conferência permite repetir a análise e ajuda outra pessoa a decidir se a função isolada bastou ou se precisa de um fluxo maior. O próximo capítulo mostra como usar um script direto quando a tarefa pede um diagnóstico ou transformação mais abrangente.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu06-h-fontes-e-estado-dos-exemplos"></a>
##### Fontes e estado dos exemplos

- Fontes de comportamento do Hub: [coleção](hub_snippets/README.md), [implementação de `format_br`](hub_snippets/constants/format_br/format_br.py), [README de `format_br`](hub_snippets/constants/format_br/README.md), [implementação de `null_summary`](hub_snippets/spark/null_summary/null_summary.py), [README de `null_summary`](hub_snippets/spark/null_summary/README.md), [README de `pit_join`](hub_snippets/spark/pit_join/README.md).
- Fontes oficiais de plataforma reconferidas em 7/10/2026: [arquivos do workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace) e [dependências do notebook serverless no Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies). O comportamento das funções customizadas vem do código do Hub.
- Os blocos copiáveis e os resultados calculados em prosa são **ILUSTRATIVOS** nesta edição. Não houve execução no workspace do leitor; o resultado histórico do notebook de `null_summary` é identificado como tal.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU05](#mu05) · [Próximo: MU07](#mu07) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT05](MANUAL_TECNICO_V2.md#mt05) · [MT07](MANUAL_TECNICO_V2.md#mt07)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu07"></a>
<a id="mu07"></a>
### MU07 — Usar um script isoladamente

<!-- editorial:exclude:start -->
**Você quer:** fazer uma checagem ou transformação pontual sem pedir à IA uma análise completa. **Antes:** encontre a tabela ou arquivo autorizado, confirme a sessão de execução e identifique a unidade de cada linha. **Depois:** leia o retorno específico, confira sua população e decida a próxima ação. Este capítulo usa nomes de tabela e resultados sintéticos; substitua placeholders pelo seu ambiente.
<!-- editorial:exclude:end -->

<a id="mu07-1"></a>
#### 1. Qual dos oito scripts escolher?

Comece pela pergunta que deseja responder, não pelo nome que parece mais amplo. Se quer um retrato inicial de colunas, volume, nulos e alguns valores, escolha `quick_profile`. Se já possui uma chave candidata e uma política de qualidade para nulos e atualidade, escolha `data_quality_check`. Se quer comparar duas janelas de uma mesma tabela numérica, escolha `drift_detector`. Esses três devolvem dicionários, mas seus campos e critérios são diferentes: um perfil descreve, a checagem aplica limiares locais e o detector mostra deslocamento de distribuição.

Se quer preparar recência, frequência e valor por entidade até uma data de corte, escolha `rfv_calculator`. Seu retorno é um DataFrame Spark de features brutas, útil como entrada de estudo. Se quer registrar a estrutura observada de uma tabela num texto revisável, escolha `schema_to_yaml` ou sua parceira `schema_to_dict`. O primeiro devolve string YAML, ou JSON compatível quando PyYAML não está disponível; o segundo, dicionário. Se quer revisar a convenção de nomes, `naming_checker` devolve uma lista de avisos. Se quer achar células de código sem Markdown ao lado em um notebook **exportado como arquivo local**, `doc_coverage` devolve um dicionário de cobertura estrutural.

A coleção reúne sete utilitários e um oitavo objeto transversal, `skill_execution`, que atende um público mais específico: quem executa ou mantém uma skill com contrato verificável. Sua função `run_preflight` confere pré-condições de um contrato antes do trabalho analítico; ela não faz perfil de tabela. Se você pediu a skill `hub-ml-eda-profissional`, a rota completa da própria skill usa runner e finalização protegidos. Uma chamada isolada a `quick_profile` ou `run_preflight` não substitui essa execução selecionada. Para uma necessidade independente, como só conferir o schema de uma tabela, você pode usar o script correspondente sem pedir uma EDA inteira.

A escolha também depende da **entrada que você realmente tem**. Os seis primeiros nomes que consultam tabela (`quick_profile`, `data_quality_check`, `drift_detector`, `rfv_calculator`, `schema_to_yaml`, `naming_checker`) precisam de nome legível por Spark e acesso à fonte. `doc_coverage` precisa de caminho de arquivo local, não de URL de notebook no workspace. `skill_execution` precisa de contrato JSON, raiz `.assistant` e contexto objetivo completo. Se falta uma dessas entradas, busque-a antes da chamada; não preencha com um valor conveniente só para obter resposta. O [capítulo técnico dos scripts](MANUAL_TECNICO_V2.md#mt11) explica mecanismos; aqui seguimos a ação do leitor.

Como decisão rápida, pergunte: “Quero observar, transformar ou verificar um contrato?”. Observar leva a perfil, qualidade, deriva, nomes ou cobertura documental; transformar eventos em features leva a RFV; verificar pré-condições de skill leva a `skill_execution`. Se o trabalho envolve várias fontes, modelagem ou visual completo, um script sozinho provavelmente entrega apenas uma peça. Encadeie peças somente depois de conferir tipo de retorno e grão. Uma lista vazia de `naming_checker` tem sentido distinto de `status='pass'` em `data_quality_check`; nenhum dos dois diz que todas as perguntas do estudo foram resolvidas.

| Rota | Quando escolher | Entrada essencial | Retorno e ponte protegida |
|---|---|---|---|
| `quick_profile` | Retrato inicial de uma tabela | Nome da tabela, fração e semente da amostra | Dicionário de contagens integrais e estatísticas amostrais; na skill EDA, use seu runner. |
| `data_quality_check` | Chave candidata, nulos e frescor opcional | Tabela, `pk_columns` estabelecida, limiares locais | Dicionário de checks/alertas; a skill EDA decide aplicabilidade pelo contexto objetivo. |
| `drift_detector` | Comparar variável numérica em duas coortes | Tabela, coluna de período, dois valores, colunas numéricas | Dicionário de PSI por coluna; não conclui uma skill nem mede performance de modelo. |
| `rfv_calculator` | Recência, frequência e valor até um corte | Tabela, entidade, data, valor e `dt_referencia` | DataFrame Spark de medidas brutas; não atribui segmentos nem completa uma skill. |
| `schema_to_yaml` | Fotografar schema para revisão | Nome da tabela e opção de estatísticas | Texto YAML ou fallback JSON compatível; não valida contrato de publicação. |
| `naming_checker` | Conferir convenções de nome | Nome da tabela e política de nomes opcional | Lista de avisos; se `enforce_prefix=True`, forneça também prefixos permitidos. |
| `doc_coverage` | Localizar código sem explicação adjacente | Caminho de notebook exportado localmente | Dicionário de cobertura e índices; não avalia a qualidade da explicação. |
| `skill_execution` | Diagnosticar pré-condições contratuais | Contrato JSON, raiz `.assistant` e contexto completo | `PreflightResult`; `PASS` não substitui runner, Receipt, postflight e conclusão da skill. |

<a id="mu07-2"></a>
#### 2. Como preparar e executar uma chamada pontual

Antes de importar, confirme que o pacote `.assistant` está disponível no caminho Python do notebook, que a sessão Spark consegue ler a fonte e que você conhece tabela, período e unidade de linha. A instalação e os caminhos são tratados em MU02; neste roteiro, `catalogo.esquema.eventos_exemplo` é **placeholder**, não uma tabela fornecida pelo Hub. Para tabela real, substitua pelo nome autorizado, de preferência qualificado, e confira permissões com uma leitura pequena apropriada. Anote a data de referência antes de gerar números que serão comparados mais tarde. Evite chamar todos os scripts por rotina: cada um pode fazer leituras ou agregações próprias.

Uma preparação útil cabe em três conferências. Primeiro, olhe o schema e confirme que os nomes usados nos argumentos existem com tipos coerentes: `dt_evento` precisa representar data, `valor` precisa permitir soma e a chave precisa ter o grão esperado. Segundo, fixe o recorte de população e período: estes scripts leem a tabela indicada e não compartilham automaticamente um filtro escondido do seu notebook. Terceiro, escolha um local seguro para registrar resultados sintéticos ou agregados, sem despejar linhas sensíveis no output. Assim, uma falha de nome ou de conceito aparece antes de uma varredura custosa.

Para um primeiro retrato, use a fachada do objeto. A fração da amostra vale apenas para parte das medidas, então mantenha o valor no registro:

```python
from hub_scripts.quick_profile import quick_profile

table_name = "catalogo.esquema.eventos_exemplo"  # substitua pela tabela autorizada
perfil = quick_profile(table_name, sample_fraction=0.10, seed=42)
print(perfil["total_rows"], perfil["sample_rows"])
```

Esse primeiro comando é curto, mas faz uma contagem e nulos da tabela inteira, além das estatísticas amostrais. Portanto espere custo de leitura mesmo com `sample_fraction=0.10`. Antes de aumentar a fração para “melhorar” a média, veja se `sample_rows` e as colunas cobertas respondem à pergunta. Se você precisa só de uma prévia visual limitada, o snippet `safe_display` (veja o [README do objeto](hub_snippets/spark/safe_display/README.md)) resolve outra tarefa; se precisa de contagem integral de uma coluna específica, deixe clara a regra em vez de tomar uma média amostral como resposta completa.

Se a próxima pergunta for qualidade, declare uma **chave candidata real**. `pk_columns` é uma lista de colunas da tabela; não escolha `id_cliente` por hábito quando cada linha é um evento e esse cliente pode se repetir. O exemplo abaixo só faria sentido se `id_evento` fosse a chave do grão de evento e `dt_evento` a data de frescor desejada:

```python
from hub_scripts.data_quality_check import data_quality_check

qualidade = data_quality_check(
    table_name, pk_columns=["id_evento"], date_column="dt_evento",
    thresholds={"null_warn": 5, "null_fail": 20, "freshness_days": 2},
)
print(qualidade["status"], qualidade["checks"]["pk_uniqueness"])
```

Este exemplo supõe que a tabela tem `id_evento` e `dt_evento`; substitua ambos conforme o schema e a definição da equipe. Confirme que o maior valor temporal chega como `date` ou `datetime`: uma string não é convertida e pode falhar; data futura pode passar por produzir idade negativa. O script usa a data atual do ambiente para frescor, então uma tabela histórica correta para um estudo antigo poderia receber alerta se você usar essa verificação sem adaptar a intenção. `thresholds` sobrescreve os defaults locais, não uma regra universal da plataforma. Se sua análise só precisa conferir chaves e nulos, omita `date_column` e explique por que não avaliou atualidade, em vez de escolher uma coluna temporal irrelevante.

Para duas coortes numéricas na **mesma** tabela, informe a coluna que identifica o período e seus dois valores observados. PSI significa **Índice de Estabilidade da População**: ele compara proporções entre faixas de valores definidas com a distribuição de referência. Essas faixas também aparecem como *bins* ou *buckets* no retorno; `missing` representa valores ausentes tratados à parte no cálculo, não uma faixa numérica comum. `drift_detector` aceita somente o método PSI atual; sem limiares calibrados, a classificação ficará informativa, sem selo de estável/alerta. `date_ref` e `date_comp` abaixo são valores da coluna `safra`, não nomes de tabelas:

```python
from hub_scripts.drift_detector import drift_detector

drift = drift_detector(
    table_name, date_col="safra", date_ref="2026-01", date_comp="2026-02",
    cols=["valor"], method="psi",
)
print(drift["valor"]["psi"], drift["valor"]["classification"])
```

Antes de chamar, confira que `safra` contém exatamente as duas etiquetas escolhidas e que `valor` é numérica em ambos os períodos. Coorte vazia gera erro, e quantis aproximados da referência mais agregações dos buckets pedem trabalho Spark. Para comparação justa, registre mudanças de filtro, unidade ou definição da variável entre as coortes. Se você precisa comparar tabelas diferentes ou categorias, este exemplo já não representa a pergunta; escolha outro recurso ou uma etapa anterior de harmonização, sem forçar `method` para um nome que o código não implementa.

Para RFV, escolha a coluna de entidade, de evento e de valor, e fixe um corte **inclusivo**. Se houver um instante de decisão distinto para cada linha, este helper com um único `dt_referencia` não basta para reconstruir todas as decisões:

```python
from hub_scripts.rfv_calculator import rfv_calculator

rfv = rfv_calculator(
    table_name, col_cliente="id_cliente", col_data="dt_evento",
    col_valor="valor", dt_referencia="2026-01-31", periodos=(30, 60, 90),
)
rfv.limit(5).show()
```

Para metadados e documentação, a chamada também é direta. Use `include_stats=False` se só quer a estrutura, pois estatísticas exigem leitura dos dados. `naming_checker` não renomeia nada; prefixos personalizados só entram se você declarar uma política. `doc_coverage` trabalha com arquivo local exportado:

```python
from hub_scripts.schema_to_yaml import schema_to_yaml
from hub_scripts.naming_checker import naming_checker
from hub_scripts.doc_coverage import doc_coverage

schema_texto = schema_to_yaml(table_name, include_comments=True, include_stats=False)
avisos_nome = naming_checker(table_name)
cobertura = doc_coverage("notebook_exportado.py")  # arquivo no diretório local de execução
```

Escolha só as linhas pertinentes. Os exemplos de objeto mostram como criar dados sintéticos ou views temporárias para uma demonstração, mas não são requisito para consultar sua tabela. O `skill_execution` pede um contexto de contrato inteiro e pertence à rota da skill selecionada ou ao diagnóstico do mantenedor; sua preparação atual é explicada em MU04. Não copie um notebook antigo de preflight sem conferir `execution_contract.json`: o exemplo histórico desta coleção omite uma chave hoje obrigatória. Quando o pacote ou uma importação faltar, volte à instalação em MU02 antes de mexer em parâmetros de análise.

Repare também no momento em que o resultado é materializado. A chamada `rfv_calculator` devolve um DataFrame; `rfv.limit(5).show()` é a ação de prévia que calcula o necessário para exibir linhas. Já `quick_profile`, `data_quality_check` e `drift_detector` fazem ações durante a própria chamada para montar seus dicionários. `schema_to_yaml` com estatísticas desligadas lê o schema; com estatísticas ligadas, aciona agregações. Para evitar trabalho duplicado, execute a função escolhida uma vez, guarde o retorno e só então navegue por seus campos ou exiba uma parte pequena.

<a id="mu07-3"></a>
#### 3. O que conferir no retorno de cada tipo?

Comece pelo objeto que recebeu de volta. Em `quick_profile`, leia `total_rows` e `null_summary_full_table` como medidas da tabela inteira; `cardinality_sample`, `top_values_sample`, `numeric_summary_sample` e `date_range_sample` usam a amostra. `sample_fraction`, `sample_seed` e `sample_rows` documentam quanto entrou nessa segunda parte. Se a tabela tem 100 linhas e o perfil seleciona aproximadamente dez, dez nulos apurados no total não tornam a média dessas dez linhas uma média de todas as cem. Uma amostra pequena pode deixar uma categoria rara invisível. Registre essa incerteza em vez de completar o perfil com suposição.

Em `data_quality_check`, `checks` separa chave, nulos e frescor opcional; `alerts` traz ocorrências com severidade, e `thresholds` mostra a política efetivamente aplicada. O `score` é uma pontuação interna que perde 25 por alerta de falha e 5 por aviso, não uma nota universal. Se `status='warn'`, abra os alertas para descobrir qual coluna atingiu ou ultrapassou qual limiar; se `pk_uniqueness.status='fail'`, inspecione duplicatas e componentes nulos antes de usar a chave para join. Se `status='pass'`, ainda revise volume e regras não cobertas, como domínio de valores e sentido da data. Uma tabela vazia pode receber `pass` com limiares positivos e freshness desligada; isso não demonstra aptidão. Quem consome decide se um alerta bloqueia uma etapa; o script sozinho não instala esse bloqueio.

Em `drift_detector`, o primeiro nível do dicionário é a coluna medida. Para `valor`, confira `reference_size`, `comparison_size`, `boundaries` e cada item de `buckets`, além de `psi`. Os bins são definidos pela referência; comparar duas execuções com referências diferentes muda a régua. `classification='not_classified'` é esperado sem os dois limiares fornecidos, e não significa “estável”. Um PSI elevado pede investigar mudança de população, extração, missing ou processo. Não conclua degradação de modelo sem medir o alvo e a performance pertinente. Quando precisar acompanhar uma categoria textual, este script de PSI numérico não atende; escolha outra ferramenta com contrato categórico.

Em `rfv_calculator`, o retorno é **DataFrame Spark**, não um dicionário de status. Confira as colunas `ultima_data`, `recencia`, `frequencia_total`, `valor_total` e pares `frequencia_30d`/`valor_30d` para cada período escolhido. Imagine `E001` com eventos de 100 em 10/01 e 50 em 20/01 e corte em 31/01: a linha ilustrativa teria frequência total 2, valor total 150 e recência 11 dias, com ambos os eventos dentro dos últimos 30 dias. Antes de chamar isso de segmento, defina a regra de segmentação; o script só entrega medidas brutas. Entidades sem evento válido até o corte não ganham linha de zeros automaticamente. Prepare chaves não nulas: o agregado de entidade nula não encontra suas janelas pelos joins atuais e pode receber zeros enganosos. Forneça períodos inteiros positivos, pois a conversão por `int` pode truncar valores fracionários.

`schema_to_yaml` devolve **texto**. Abra-o e confira `table`, a lista `columns` e, se foram pedidas, estatísticas. Se PyYAML não estiver instalado, o texto pode aparecer em formato JSON válido como YAML 1.2; isso é fallback esperado quando falta PyYAML, não erro de schema. Só `ImportError` dessa importação ativa o fallback; falhas de Spark ou serialização continuam falhas. Valide o parser consumidor, pois a compatibilidade exige suporte adequado a YAML 1.2. Para manipular campos em Python, `schema_to_dict` devolve o dicionário correspondente. Versões devem ser comparadas com data e fonte, pois o texto é uma fotografia. `naming_checker` devolve **lista**: cada item indica objeto, severidade, mensagem e política. Lista vazia significa que aquelas convenções não acharam desvio; não comprova semântica correta, compatibilidade de mudança ou permissão de publicação.

`doc_coverage` devolve um **dicionário** com `total_code_cells`, `total_markdown_cells`, `coverage_pct` e `uncovered_cell_indexes`. Os índices começam em zero. Em um arquivo com células Markdown, código, código, a primeira célula de código tem uma explicação adjacente e a segunda não: duas células de código, 50% de cobertura e índice 2 descoberto. Abra esse ponto no arquivo e escreva uma explicação que ajude a entender o propósito; adicionar qualquer Markdown só para elevar o percentual satisfaz a heurística, mas não o leitor. Arquivo sem célula de código recebe 100% por convenção e exige a mesma leitura crítica.

Se estiver conferindo preflight de uma skill, `PreflightResult` separa `status`, `blocking_issues`, decisões de recurso e template e `writes_performed`. `PASS` mostra que pré-condições aplicáveis foram resolvidas naquele contexto, não que helpers tenham sido chamados. `BLOCKED` pede ler o item e o código do problema, corrigir a entrada ou recurso real e repetir o preflight. O notebook histórico `exemplo_skill_execution.py` não contém `pk_columns_available`, hoje obrigatório no contrato da EDA; copiá-lo pode produzir `CONDITION_CONTEXT_INVALID`. Consulte o contrato atual e a rota da skill antes de tentar concluir o trabalho. Receipt e postflight respondem às etapas seguintes.

<a id="mu07-4"></a>
#### 4. O que fazer diante de alerta, erro ou resultado estranho?

Uma falha de importação pede conferir instalação e caminho do pacote, não inventar uma função de substituição com mesmo nome. Uma falha em `spark.table(table_name)` pede verificar nome, acesso e sessão no ambiente autorizado. Se a coluna informada não existe, abra o schema atual; alterar `pk_columns` ou `date_col` às cegas apenas troca o significado da pergunta. Em `doc_coverage`, um `FileNotFoundError` significa que o caminho local não aponta a um arquivo disponível; URL do workspace não é aceita por essa API. Para qualquer erro, registre chamada, parâmetros sem dados sensíveis, versão da fonte e mensagem antes de tentar outra rota.

Alguns resultados exigem decisão em vez de correção de sintaxe. Duplicidade de chave pode revelar grão incorreto ou dado duplicado; a ação é investigar a fonte e decidir qual unidade deveria ser única. `drift_detector` com coorte vazia lança erro; ajuste o período somente se o período correto foi informado errado, não para fabricar população. RFV com poucos clientes pode decorrer de corte anterior aos eventos ou datas inválidas removidas; confira quantos eventos restaram até `dt_referencia`. `schema_to_yaml` com colunas inesperadas pede comparar schema observado com contrato do produtor. Um aviso de `naming_checker` sobre prefixo pertence à política local declarada, não é prova de que a plataforma recusará o objeto.

Ao interpretar `data_quality_check`, leia severidade e motivo. Um `warn` de nulos pode permitir continuar uma exploração com ressalva; um `fail` de chave pode impedir um join que depende de unicidade. Essa reação deve ser explícita no notebook ou processo, com limiar e dono, porque o script só devolve a evidência. Para `drift_detector`, não passe limiares genéricos apenas para trocar `not_classified` por uma cor. Calibre com referência, tamanho das populações, risco e política aplicável. Se o objetivo mudou de exploração para acompanhamento recorrente, documente quem recebe o alerta, com que frequência e o que será feito.

Quando a chamada isolada já respondeu à pergunta, anote o resultado e seu limite em poucas frases: “nulos completos da tabela”, “média em amostra”, “RFV até 31/01”, “cobertura documental por adjacência”. Inclua tabela ou arquivo de origem, período, filtros, grão, parâmetros e quem revisará a próxima decisão. Se outra análise for necessária, o guia por intenção aponta à skill adequada; uma skill selecionada pode ter contratos de runner, evidência e finalização próprios. Preservar esse contexto permite que o próximo passo use a saída correta sem converter um diagnóstico pontual em certificado geral.

Para uma alternativa simples, ajuste o instrumento à pergunta. Se só quer cinco registros legíveis, use uma prévia limitada; se quer uma amostra, escolha uma estratégia de amostragem; se quer discutir risco de um join, execute o diagnóstico de junção antes de criar features. Se nenhuma ferramenta cobre a pergunta, registre a lacuna e construa uma análise própria com sua regra declarada. O catálogo ajuda a começar, mas a responsabilidade por autorização, custo e interpretação continua com a pessoa ou processo que faz a chamada.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu07-h-fontes-e-continuação"></a>
##### Fontes e continuação

Implementações e READMEs em `ambiente_databricks/.assistant/hub_scripts/`; contrato atual da EDA em `ambiente_databricks/.assistant/skills/hub-ml-eda-profissional/execution_contract.json` e teste `tools/tests/test_skill_enforcement_se02.py`. Exemplos de valores são ILLUSTRATIVE. Continue em MU08 para uma base, MU09 para cruzamento de fontes e MU10 para features/safra. Nenhuma tabela real ou runtime foi executado nesta redação.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU06](#mu06) · [Próximo: MU08](#mu08) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT11](MANUAL_TECNICO_V2.md#mt11)
<!-- editorial:exclude:end -->

<!-- editorial:exclude:start -->
<a id="parte-mu-iii"></a>
## Parte III — Tarefas de análise
<!-- editorial:exclude:end -->


<a id="mu-mod-mu08"></a>
<a id="mu08"></a>
### MU08 — Conhecer uma base: EDA, perfil e qualidade

<!-- editorial:exclude:start -->
**Você quer:** entender uma fonte antes de estudá-la, cruzá-la ou modelá-la. **Rota:** defina a pergunta e o grão na seção 1; escolha EDA completa ou pergunta pontual na seção 2; execute e confira a rota direta na seção 3; conclua com um handoff rastreável na seção 4. Exemplos usam tabela fictícia; nenhuma autorização ou execução é presumida.
<!-- editorial:exclude:end -->

<a id="mu08-1"></a>
#### 1. Que pergunta e população vão orientar a exploração?

Antes de pedir um gráfico, formule uma frase que indique o que quer decidir: “Esta tabela de eventos permite estudar respostas a campanhas por entidade e mês?”. Essa frase determina quais colunas importam, qual período deve ser lido e que erro seria grave. Se você pedir apenas “faça EDA”, o planejamento ainda pode começar, declarando hipóteses e perguntas abertas; entradas críticas ausentes não autorizam executar a análise por suposição. Uma EDA — **análise exploratória de dados** — descreve estrutura, qualidade, distribuição e relações de uma população. Ela ajuda a descobrir problemas e possibilidades; não certifica por si que a base está pronta para produção ou que uma relação é causal.

Escreva o **grão** em linguagem comum: uma linha é um evento, uma entidade ou um contrato em um mês? Na tabela fictícia `catalogo.esquema.eventos_exemplo`, `E001` pode aparecer três vezes porque teve três ocorrências. Nesse caso, `id_cliente` não é chave única da tabela, embora possa ser a entidade que será agregada. Se a pergunta é sobre clientes únicos, conte entidades; se é sobre eventos, conte linhas. Anote também chave candidata no grão real, como `id_evento` se cada ocorrência tiver identificador próprio. Essa distinção evita chamar duplicidade um comportamento esperado ou esconder uma duplicidade verdadeira.

Delimite a fonte e o período: nome autorizado da tabela, filtros, snapshot ou data de extração, coluna de data e janela estudada. Se houver alvo, descreva quando ele é observado e qual data representa a decisão. Uma resposta futura pode ser analisada como alvo, mas não pode ser colocada entre características conhecidas antes da decisão. Se o alvo ainda não amadureceu para as linhas recentes, separe essas linhas em vez de tratá-las como ausência do evento. Para o retrato inicial, você pode deixar o alvo fora e registrar que a relação com ele virá em outra etapa.

Confirme acesso e sensibilidade antes de exibir dados. A EDA profissional recomenda agregações Spark e visualizações sobre resultados limitados; linhas pessoais, identificadores ou texto livre podem exigir mascaramento ou exclusão conforme a política do ambiente. Não transforme um notebook de amostra em cópia da tabela inteira no processo Python. Se uma coluna parece categórica mas contém milhões de identificadores diferentes, um gráfico de todas as categorias não ajuda o leitor e pode custar caro. Registre o limite aplicado à amostra e a semente usada para que outra pessoa saiba o que viu.

Ao final desta preparação, você deve conseguir preencher uma ficha curta: objetivo, fonte, população, unidade de linha, chave candidata, período, filtros, data de decisão, alvo se houver e o que permanece desconhecido. Um exemplo ilustrativo seria: “eventos de janeiro a março de 2026; uma linha por ocorrência; `id_evento` candidato a chave; `id_cliente` pode repetir; sem alvo confirmado”. Essa ficha acompanha tanto a skill quanto uma chamada isolada de helper. Se não há fonte ou período estabelecido, descubra-os primeiro; um número sem população definida não responde à pergunta inicial.

Verifique ainda se o período da pergunta coincide com o conteúdo inteiro da tabela. `quick_profile` e `data_quality_check` recebem um nome de tabela e leem essa tabela; eles não aceitam diretamente um filtro de datas. Se a tabela contém vários anos, o resultado desses helpers descreve todos eles. Para medir somente janeiro a março, use um DataFrame filtrado nos snippets que recebem DataFrame, ou providencie uma fonte autorizada cujo conteúdo já corresponda ao recorte e registre como ela foi formada. Escrever “janeiro a março” no briefing sem aplicar o filtro no dado não modifica o denominador das porcentagens.

<a id="mu08-2"></a>
#### 2. Quando pedir EDA completa e quando fazer uma verificação curta?

Use a skill `hub-ml-eda-profissional` quando precisa de um diagnóstico integrado de **uma** fonte: granularidade, chaves, qualidade, distribuições, relações, visualizações agregadas e recomendações. Ela traz um roteiro, templates e uma rota protegida de execução. Distribuições e diagnóstico visual entram por padrão nessa rota; prévia e amostra são opt-in. Escolha os itens pertinentes e reaproveite evidência do mesmo snapshot/run, sem repetir varreduras por ritual. Para solicitar, informe a ficha construída acima e o formato de entrega: notebook, relatório ou ambos. Um briefing útil é: “Analise a tabela autorizada X, uma linha por evento, de janeiro a março; avalie a chave candidata Y, nulos e cobertura, distribuições e possíveis sinais para o alvo Z, que ainda precisa ser confirmado; entregue achados, limites e próximos testes”. Substitua X/Y/Z pelo contexto real e indique restrições de visualização.

A skill atual tem uma rota L4 de execução e finalização. O runner `run_enforced` usa o core analítico e coleta evidência dos recursos e templates aplicáveis; depois `finalize_or_raise` confronta o resultado com o handoff e o postflight. Se o runner devolve `PENDING_POSTFLIGHT`, isso significa que ainda falta a finalização, não que a EDA foi concluída. Só o payload final com `postflight.status='PASS'`, `completion.authorized=True` e `completion.status='COMPLETED'` autoriza dizer que a execução daquela skill terminou conforme o contrato. Um `PASS` isolado de preflight confere pré-condições; não prova que análises foram feitas. Para o leitor, a ação é pedir que a rota termine e observar esse estado final, não editar um dicionário de resultado manualmente.

Se a execução lançar `CanonicalExecutionBlocked`, a rota canônica daquele run parou. Leia o motivo: pode faltar recurso obrigatório, entrada objetiva ou evidência. Corrija a fonte ou contexto real e inicie outro run pela mesma rota quando possível; não declare a EDA concluída juntando chamadas manuais por fora. Se ainda não há chave primária candidata estabelecida, não invente `pk_columns` para satisfazer `data_quality_check`; a própria skill sabe marcar esse recurso como não aplicável no contexto apropriado. Uma instrução simultânea para selecionar a skill e pular runner/postflight entra em conflito com seu contrato; explicite o conflito e peça uma decisão de tarefa coerente.

Para uma pergunta menor e independente, use um objeto isolado. “Quais colunas, tipos, volume e alguns valores aparecem?” pede `quick_profile`. “Quantos nulos há por coluna?” pede `null_summary`; “a chave candidata está única e recente sob nossa política?” pede `data_quality_check`. “Quero cinco linhas legíveis” pede `safe_display`, que limita prévia; “quero um recorte limitado para inspeção” pode pedir `smart_sample`, respeitando seus limites de inclusão. São perguntas diferentes e a resposta de uma não substitui as outras. O [roteiro de script isolado](#mu07) ensina importação e leitura de dicionários; o [roteiro de snippet isolado](#mu06) explica como incorporar o DataFrame recebido no notebook.

Uma EDA rápida pode ter escopo reduzido, mas precisa manter a distinção entre achado e hipótese. Uma contagem de nulos acima de um limite mostra ausência naquela coluna; não diz se a causa foi extração, regra de negócio ou população incorreta. Uma distribuição com cauda longa sugere olhar extremos; não autoriza remover observações automaticamente. Se a pergunta evoluir para cruzar **duas ou mais fontes**, siga a rota de cross-EDA do MU09. Se evoluir para teste de hipótese com valor-p e tamanho de efeito, escolha a skill de validação estatística. Se evoluir para visualização pronta para comunicação, use os capítulos de trabalho visual. Essa escolha evita pedir à EDA de uma fonte uma conclusão para a qual falta outra base ou outro método.

Há um limite técnico importante para não prometer uma execução impossível. O Hub fornece código, templates e contratos; a análise precisa de tabela legível, ambiente compatível e dados com significado conhecido. Ter o arquivo `SKILL.md` na árvore não prova que a skill foi publicada ou homologada no workspace em que você está. Antes de pedir resultado, confira se o ambiente atual tem o pacote instalado e acesso autorizado à fonte; a rota MU02 cobre essa preparação. Se você só está lendo esta edição offline, use os exemplos como instruções e não como resultados produzidos pelo seu ambiente.

Para transformar a escolha em uma decisão concreta, imagine duas solicitações. Na primeira, a equipe quer decidir se uma base pode sustentar um estudo e precisa de relatório com limitações, hipóteses, gráficos e recomendações: entregue o briefing à skill e confira cada etapa de sua rota protegida. Na segunda, um analista recebeu uma dúvida estreita — “a coluna de evento está nula no trimestre?” — e já tem um DataFrame do trimestre: `null_summary` responde essa pergunta sem pedir uma análise completa. Se a dúvida curta revelar um problema estrutural, registre o achado e amplie o escopo de modo explícito. Esse encadeamento mantém claro o que foi verificado, em qual população e por qual ferramenta.

Se você for receber uma EDA feita por outra pessoa, confira o relatório como artefato de trabalho: a fonte e a janela correspondem ao pedido? Há contagens para acompanhar percentuais? A análise separa amostra de população? As figuras têm escala, unidade e legenda suficientes? Estão descritos itens não aplicáveis e dados insuficientes? Um arquivo de notebook que abre sem erro ou um gráfico bonito não responde sozinho a essas perguntas. Na rota protegida, leia também a evidência de finalização; na rota direta, documente suas próprias verificações, sem atribuir a elas o estado de execução da skill.

<a id="uso-hub-ml-eda-profissional"></a>
##### Ficha de uso — hub-ml-eda-profissional

<!-- usage-card:start hub-ml-eda-profissional -->
Escolha EDA profissional para compreender uma fonte de modo integrado, reunindo perfil, qualidade, distribuições, relações e recomendações. Para uma contagem independente, considere o helper isolado. Informe tabela autorizada, população, grão, chave candidata, período, disponibilidade temporal, alvo quando houver, custo permitido e formato da entrega. Use desconhecidos explícitos, sem inventar uma chave para satisfazer um requisito.

O pedido abaixo começa pelo plano. Antes de autorizar execução, confira recorte, operações, recursos, efeito e destino. A entrega esperada depois da execução autorizada é notebook ou relatório com achados sustentados, limitações e próximos testes, acompanhado da finalização canônica. Na versão L4/enforce, o runner e o postflight pertencem à rota selecionada: `PENDING_POSTFLIGHT` ainda não conclui a tarefa. Confira `postflight.status=PASS`, `completion.authorized=true` e o estado final de conclusão, além da coerência dos denominadores e da origem dos números. Um Receipt isolado não substitui essa conferência. Se a rota bloquear, leia o motivo, corrija entrada ou recurso real e inicie outra execução canônica quando possível; conserve o resultado como não concluído enquanto faltar evidência. A resposta deve separar hipótese de achado observado.

```text
@hub-ml-eda-profissional
Quero avaliar a fonte autorizada [TABELA], uma linha por [GRÃO],
no período [INÍCIO/FIM], com chave candidata [CHAVE OU NÃO INFORMADO].
Disponibilidade temporal e alvo: [DEFINIÇÕES OU NÃO INFORMADO].
Primeiro apresente plano, recursos e custos; não execute nesta etapa.
Após autorização específica, entregue [NOTEBOOK/RELATÓRIO], limites e
evidências da execução canônica e da finalização. Não invente requisitos.
```
<!-- usage-card:end hub-ml-eda-profissional -->

<a id="mu08-3"></a>
#### 3. Como fazer uma exploração direta com perfil, qualidade e prévia?

Suponha que a tarefa pontual seja reconhecer a tabela `catalogo.esquema.eventos_exemplo` e decidir se ela merece uma EDA completa. Substitua esse nome por uma tabela real autorizada. Execute primeiro um perfil, porque ele registra linhas, tipos e nulos da tabela inteira e resumos limitados por amostra. No exemplo, assuma que a tabela nomeada já contém somente os meses definidos na ficha; se contiver mais meses, as saídas de perfil e qualidade não estarão restritas ao trimestre. A fração de 10% controla a amostra das estatísticas, não a contagem total:

```python
from hub_scripts.quick_profile import quick_profile

table_name = "catalogo.esquema.eventos_exemplo"  # placeholder
perfil = quick_profile(table_name, sample_fraction=0.10, seed=42)
print(perfil["total_rows"], perfil["sample_rows"])
print(perfil["null_summary_full_table"][:5])
```

Leia `dtypes` antes de decidir gráficos; confira `sample_rows` antes de interpretar `numeric_summary_sample` ou `top_values_sample`. `quick_profile` só percorre um número limitado de colunas para algumas medidas, então ausência de estatística não é ausência da coluna. Se você observar 100 linhas e 10 nulos em `valor`, isso é um fato integral sobre nulos do perfil. Se a média vier de aproximadamente 10 linhas selecionadas, trate-a como retrato exploratório sujeito à amostra. Se a fração for pequena demais para categorias raras, ajuste o desenho da amostra conscientemente ou faça agregação específica sobre a população, anotando o custo.

Depois, confirme a unidade e uma chave **candidata**. Se cada linha é evento, `id_cliente` pode repetir legitimamente; use `id_evento` apenas se o produtor definiu um identificador por ocorrência. A chamada a seguir retorna um dicionário de checks e alertas sob limiares locais. Como o trimestre ilustrativo é histórico, ela omite `date_column`: essa opção mede frescor pela maior data em relação ao dia do ambiente e, neste caso, uma reprovação seria esperada sem dizer nada sobre a completude histórica.

```python
from hub_scripts.data_quality_check import data_quality_check

qualidade = data_quality_check(
    table_name, pk_columns=["id_evento"],
    thresholds={"null_warn": 5, "null_fail": 20},
)
print(qualidade["status"], qualidade["checks"]["pk_uniqueness"])
for alerta in qualidade["alerts"]:
    print(alerta["check"], alerta["severity"], alerta["message"])
```

Quando só precisa da distribuição de nulos por coluna, `null_summary` trabalha sobre um **DataFrame Spark** que você já selecionou, o que permite aplicar o recorte definido na ficha. Confirme que o recorte não está vazio antes da chamada; a implementação pode falhar ao converter uma soma nula em inteiro em tabela vazia. Os defaults 5/20 são limiares locais da função, não critério universal de qualidade. Se o perfil e o resumo de nulos usam recortes diferentes, seus percentuais também serão diferentes, sem que uma das funções esteja errada.

Interprete os alertas de `data_quality_check` por componente. `status='pass'` significa apenas que os checks configurados não violaram esses limiares naquela tabela: ainda falta confirmar se a chave representa o grão correto e se as colunas exigidas pelo estudo existem. `status='warn'` aponta uma taxa de nulos no patamar de aviso; planeje investigar coluna, população e impacto antes de usá-la. `status='fail'` pode vir de duplicidade ou componente nulo da chave, taxa de nulos no patamar de falha ou frescor quando essa opção foi ativada. Nesse caso, leia `alerts` e `checks` para localizar a causa em vez de interpretar `score` como uma nota geral de aptidão para modelagem. O número é uma pontuação local formada pelos alertas, não uma certificação da base. Confira `row_count`: tabela vazia pode receber `pass` com limiares positivos e sem freshness; isso não representa uma população adequada.

```python
from hub_snippets.spark.null_summary import null_summary

base = spark.table(table_name).filter("dt_evento >= '2026-01-01' AND dt_evento < '2026-04-01'")
if base.limit(1).count() == 0:
    raise ValueError("recorte sem linhas; confira período e filtros")
nulos = null_summary(base, threshold_warn=5, threshold_fail=20)
nulos.show(truncate=False)
```

Para inspecionar linhas, escolha entre **prévia** e **amostra**. `safe_display` observa no máximo `limit+1` linhas para indicar truncamento e envia até `limit` ao renderer; ele não sorteia linhas. `smart_sample` pode produzir uma amostra sem reposição limitada por `n`; no modo estratificado preserva pelo menos uma linha por categoria quando o número de estratos cabe no orçamento. Preservar categoria rara altera proporções, e o modo simples pode devolver menos de `n` e não garante inclusão probabilística uniforme. Com 110 linhas e `n=100`, a fração calculada é 1 e o limite pode selecionar um prefixo. Nenhum dos dois autoriza trazer a base inteira para pandas. A chamada abaixo é apenas para um notebook em que `display` está disponível; fora dele, passe uma função de exibição apropriada.

```python
from hub_snippets.spark.safe_display import safe_display
from hub_snippets.spark.smart_sample import smart_sample

safe_display(base, limit=5, display_fn=display)
amostra = smart_sample(base, n=100, stratify_col="canal", seed=42)
amostra.limit(5).show()
```

Antes de usar `stratify_col`, confirme que `canal` existe e que preservar cada categoria faz sentido para a pergunta. Confira também se a entrada tem `__sample_rank` ou `__stratum_target`: esses nomes auxiliares podem ser sobrescritos, removidos ou causar ambiguidade. Renomeie ou recuse a entrada antes da chamada; o helper não faz essa guarda completa. Se a fonte tem mais categorias que `n`, `smart_sample` recusa o pedido; aumentar `n` ou escolher outro agrupamento exige avaliar custo e objetivo. Registre a semente, o recorte e o número de linhas efetivo da amostra. Para uma apresentação visual, agregue no Spark e leve somente o resultado pequeno ao gráfico; a [trilha visual](#mu14) desenvolve tema, escala, legenda e acessibilidade. Aqui o resultado esperado é um diagnóstico inicial: grão e chave plausíveis, qualidade medida, distribuições que merecem aprofundamento e dúvidas documentadas.

Um pequeno resultado ilustrativo mostra como decidir. Suponha 100 eventos no recorte, 10 valores ausentes em `valor` e dois `id_evento` duplicados na tabela nomeada. O resumo de nulos sustenta a frase “10% dos eventos do recorte não têm `valor`”; o alerta da chave sustenta “a tabela nomeada viola a unicidade candidata”. Antes de combinar ambos em uma conclusão, confirme que a tabela nomeada e o recorte do DataFrame contêm a mesma população. Se não contêm, relate dois universos separados e repita a checagem de chave na população correta por uma rota apropriada. O exemplo não é uma medição real.

Também verifique o que cada retorno não revela. `safe_display` mostra primeiras linhas conforme a ordem de leitura disponível, sem sorteio nem representatividade estatística. `smart_sample` oferece inspeção amostral, mas mesmo com semente registrada pode deixar de fora anomalias raras; uma ausência na amostra não equivale a zero ocorrência na base. `quick_profile` limita cardinalidade, categorias, resumos numéricos e intervalos de datas a subconjuntos de colunas e à amostra. Ao compartilhar a exploração, deixe esses limites junto da tabela ou figura. Assim o próximo leitor não transformará uma prévia conveniente em afirmação sobre toda a população.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu08-h-fontes-desta-parte"></a>
##### Fontes desta parte

`ambiente_databricks/.assistant/skills/hub-ml-eda-profissional/SKILL.md`, contrato, runners e templates; implementações/READMEs de `quick_profile`, `data_quality_check`, `null_summary`, `safe_display` e `smart_sample` em `ambiente_databricks/.assistant/`. Todas as tabelas, valores e chamadas são ILLUSTRATIVE e dependem de substituição por fonte autorizada. Não houve execução de skill ou Spark para esta redação.
<!-- editorial:exclude:end -->

<a id="mu08-4"></a>
#### 4. Como transformar a exploração em decisão e passar o trabalho adiante?

Feche a exploração respondendo à pergunta que a abriu. Para o exemplo dos eventos, uma conclusão prudente seria: “A tabela parece ter o grão de ocorrência; a chave `id_evento` precisa de correção por causa de duas repetições; 10 dos 100 eventos do trimestre têm `valor` ausente; ainda não sabemos se esses nulos significam falha de carga ou regra de negócio”. Os números são **ilustrativos**. O valor da frase está em separar uma observação medida, uma interpretação provisória e o que falta descobrir. “A base está pronta” seria precipitado, porque nem a semântica dos nulos nem a unicidade foram resolvidas.

Monte um relatório que outra pessoa possa conferir sem adivinhar o recorte. O template de relatório executivo da skill propõe identificação da tabela, período, volume, grão, data da análise, notebook fonte, qualidade, padrões, anomalias, implicações e próximos passos. Na rota direta, você pode usar a mesma organização sem atribuir à chamada isolada o status da skill. Abra com a decisão que a EDA apoia e seus limites. Em seguida, declare nome da fonte, snapshot ou momento de leitura, filtros, contagens, unidade, chave candidata, amostra e semente. Para cada tabela ou gráfico, identifique denominador, unidade e período. Se o perfil abrange toda a tabela mas um gráfico cobre só o trimestre, diga isso junto do resultado; não misture percentuais em uma única comparação.

Para cada achado importante, escreva uma linha de raciocínio: evidência observável, população afetada, consequência possível, hipótese de causa e teste seguinte. Por exemplo, “`valor` está ausente em 10% dos eventos do recorte; qualquer média feita só sobre valores presentes pode representar outra população; verificar com o responsável pela origem se ausência significa evento sem valor ou perda de captura”. O teste não é preencher os nulos imediatamente. Em outro caso, uma categoria rara vista na amostra estratificada pode merecer uma contagem na população antes de virar recomendação operacional. Mostre também resultados negativos relevantes, como “não avaliamos consistência entre fontes”, para delimitar a conclusão.

O handoff da skill EDA possui campos explícitos: `sources_snapshot`, `unit_keys_target`, `quality_risks`, `feature_candidates_leakage`, `filters_sample` e `open_questions`. Preencha cada um com conteúdo verificável; a lista de questões pode ficar vazia quando nada material está pendente, mas não invente chave, alvo ou snapshot para obter uma aprovação. Se o postflight indicar `REVIEW`, resolva as pendências do handoff e finalize novamente pela rota apropriada; se indicar `FAIL` ou `BLOCKED`, leia a evidência e corrija a causa antes de repetir o run canônico. Na exploração direta, mantenha os mesmos campos como notas de passagem, sabendo que isso não produz Receipt nem Postflight da skill.

Defina a próxima ação conforme a pergunta que restou. Se o problema é duplicidade, peça ao produtor a regra de identificação e repita a checagem no grão correto. Se a cobertura do período está incompleta, investigue extração e partições antes de interpretar tendência. Se são duas fontes a reconciliar, vá ao MU09 com chave, janela e diferenças já registradas. Se a decisão envolve construção de variáveis, leve candidatos e suspeitas de vazamento à rota de feature engineering; se exige evidência estatística, formule hipótese e população para validação. Para apresentação, leve apenas resultados agregados e as limitações à trilha visual. O destinatário deve conseguir dizer que dado recebeu, o que foi realmente medido e qual pergunta permanece aberta.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu08-h-fontes-desta-parte-1"></a>
##### Fontes desta parte

`ambiente_databricks/.assistant/skills/hub-ml-eda-profissional/SKILL.md`, `execution_contract.json`, `templates/relatorio_executivo_eda.md` e `scripts/postflight.py`. Exemplo de 100 eventos, 10 nulos e duas repetições é ILLUSTRATIVE; não houve execução sobre dados reais para este texto.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU07](#mu07) · [Próximo: MU09](#mu09) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT19](MANUAL_TECNICO_V2.md#mt19)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu09"></a>
<a id="mu09"></a>
### MU09 — Comparar e cruzar fontes com cuidado temporal

<!-- editorial:exclude:start -->
**Você quer:** saber se duas fontes podem compor uma base sem mudar indevidamente a unidade de análise ou trazer informação futura. **Rota:** descreva as fontes e a decisão (1); compare compatibilidade e escolha a profundidade do estudo (2); faça diagnósticos de chave e tempo (3); decida com evidências (4). Tabelas e valores do exemplo são sintéticos; o código é uma receita a adaptar, não um resultado executado.
<!-- editorial:exclude:end -->

<a id="mu09-1"></a>
#### 1. Que chaves, grão e período cada fonte realmente possui?

Imagine que a equipe queira acrescentar ao evento de contato de um cliente a última informação de relacionamento disponível antes desse contato. A fonte **âncora** é a tabela de contatos: ela define quantas decisões serão estudadas e o que significa preservar uma linha. A fonte complementar é um histórico de informações do cliente. Antes de arrastar uma coluna com o mesmo nome para um `join`, escreva uma frase por fonte: “uma linha de `contatos` é uma decisão de contato de `id_cliente` em `ts_decisao`”; “uma linha de `historico` é uma versão de `saldo` referente a `ts_feature`”. A mesma chave textual pode representar unidades diferentes.

Registre o identificador de entidade e, se a linha de decisão precisar ser única, sua chave de evento. `id_cliente` pode repetir corretamente na âncora porque o cliente foi contatado mais de uma vez. Na direita, várias linhas por cliente também podem ser corretas, pois representam versões; um join apenas por `id_cliente` multiplicaria os contatos. Uma chave composta, como cliente e data de referência, só ajuda se esses componentes definem a mesma relação nos dois lados. Não invente uma chave única a partir de uma coluna conveniente. Se um lado usa contrato e o outro cliente, obtenha uma regra de mapeamento validada antes de chamar ambos de “mesma entidade”.

Monte um cartão de fonte para cada lado antes da execução. Os exemplos abaixo servem para conferir a informação que falta, não são cadastro real:

| Cartão | Âncora: contatos | Complementar: histórico |
|---|---|---|
| Grão | Uma linha por contato/decisão | Uma linha por cliente e versão de referência |
| Chave e tempo | `id_cliente`, `id_contato`, `ts_decisao` | `id_cliente`, `ts_feature` e instante de disponibilidade |
| População | Contatos do trimestre definido | Histórico que pode cobrir esse trimestre |
| Snapshot e filtro | Identificador/data de leitura e filtros | Identificador/data de leitura e filtros |
| Qualidade a confirmar | Chaves e datas nulas, duplicidade de `id_contato` | Duplicidade por versão, datas nulas, atraso de publicação |
| Restrição | Uso permitido e sensibilidade | Uso permitido e sensibilidade |

Esse cartão impede que duas porcentagens incompatíveis pareçam uma cobertura única. Meça a população da âncora em linhas de decisão e, quando necessário, em entidades únicas. Um cadastro pode cobrir 90% dos clientes únicos e apenas 70% dos contatos se os clientes sem cadastro forem mais frequentes; ambas as medidas respondem a perguntas distintas. Anote se o período é o da decisão, da referência da feature ou de sua publicação. Para uso preditivo, o alvo e seu horizonte ficam separados: uma resposta ocorrida depois do contato pode ser o resultado a prever, mas não uma característica disponível antes do contato.

Se você não conhece o grão ou o instante de disponibilidade, peça essa definição ao responsável pela fonte e faça uma exploração limitada, sem declarar prontidão para modelagem. Uma comparação de schemas ajuda a localizar colunas e tipos, mas não prova igualdade semântica. A próxima seção mostra como reunir EDAs de fontes individuais; os números de join só ganham sentido quando o cartão diz qual linha deve sobreviver.

Preveja como conferirá a preservação: conte os contatos da âncora antes da operação e exija o mesmo número de linhas depois de uma junção que promete uma versão por decisão. Separe contatos com chave nula dos que têm chave válida sem histórico. Para evitar conclusões de um snapshot mutável, anote o identificador da versão ou um corte reprodutível de cada fonte; se a origem muda entre o diagnóstico e a materialização, o número previsto pode deixar de coincidir. Quando não há snapshot fixável, indique essa limitação e repita a contagem sobre as entradas efetivamente usadas.

<a id="mu09-2"></a>
#### 2. Como comparar as tabelas e usar a orientação de cross-EDA?

Se cada fonte ainda é pouco conhecida, faça primeiro a EDA de uma fonte do MU08 para cada uma, mantendo snapshot, filtro, grão e limitações. Depois use a skill `hub-ml-cross-eda-ml` para organizar a pergunta entre fontes: inventário dos EDAs, resolução de entidade, alinhamento temporal, simulação de joins, cobertura, qualidade combinada e decisão de prontidão. Um pedido útil seria: “Avalie se contatos por cliente e horário podem receber a última versão de saldo disponível antes do contato; preserve a linha de decisão, documente duplicações e não correspondências por mês; proponha GO, CONDICIONAL ou NO-GO com evidência, responsáveis e critérios”. Inclua os dois cartões e informe target/horizonte se a intenção é modelagem.

A policy mantém `current_level=L0/audit`; o alvo L4 não foi promovido. Entretanto, o código integrado já contém três rotas sintéticas distintas, descritas no [README dos scripts](skills/hub-ml-cross-eda-ml/scripts/README.md): contexto, diagnóstico e PIT. O contexto L2 não executa Spark nem mede cobertura. `run_diagnostic.py` calcula cardinalidade/cobertura, exige verificação com entradas e diagnóstico esperado externos e não produz join de negócio. `run_pit.py` executa o perfil temporal local; `verify_pit.py` finaliza e reverifica seus inputs, janela e run. Escolha o contrato antes de autorizar ações. Um PASS do contexto não prova join, e o perfil executável não certifica todo pedido de cross-EDA nem prontidão para ML.

Há também briefings de comparação de tabelas e de cross-EDA no catálogo de prompts. Eles ajudam a formular intenção, fontes, coluna-chave, diferenças de schema, cobertura e saída desejada; não consultam dados por si. Use o briefing de comparar tabelas quando a primeira dúvida é estrutural — colunas, tipos, grão e compatibilidade — e o de cross-EDA quando a decisão exige juntar achados de múltiplas fontes e avaliar uso para ML. Informe o que é desconhecido em vez de preencher lacunas com supostos valores. Um prompt bem preenchido não transforma duas tabelas distintas em uma chave válida.

Faça uma comparação que respeite o papel de cada fonte. Verifique formatos de `id_cliente`, nulos, regras de normalização, cobertura de datas e cardinalidade por chave. Compare a data máxima do histórico com o período de decisões, mas não conclua que todas as decisões antigas tinham acesso ao dado só porque o snapshot atual o contém. Uma linha antiga pode ter sido corrigida ou publicada depois. Verifique também se colunas com o mesmo nome têm unidade e interpretação iguais: `valor` pode ser um saldo monetário em uma fonte e um código em outra. A comparação estrutural deve virar perguntas objetivas ao produtor, não um merge automático de schemas.

Use uma pequena matriz de viabilidade, com evidência em cada célula. Ela facilita perceber que “cobertura alta” e “sem futuro” são condições diferentes:

| Dimensão | Pergunta verificável | Evidência a registrar |
|---|---|---|
| Entidade | As chaves representam o mesmo cliente? | Regra de mapeamento, nulos, conflitos |
| Cardinalidade | Uma decisão vira quantas linhas? | Expansão prevista left/inner e amostra de chaves |
| Tempo | A versão existia na decisão? | Referência, atraso, fuso, janela e disponibilidade |
| Cobertura | Quem fica sem feature e por quê? | Denominador e causas separadas por mês/segmento |
| Qualidade e uso | O valor é coerente e permitido? | Domínios, sensibilidade, restrições e dono |

Se a âncora tiver três contatos para o mesmo cliente, conte três decisões ao avaliar cobertura por linha; se o problema é inclusão de clientes, conte também entidades. Não reduza as duas leituras a um único score. A classificação GO/CONDICIONAL/NO-GO da skill é um argumento com vetos possíveis: chave indefinida ou vazamento temporal material pode impedir GO apesar de boa cobertura. Se uma dimensão está desconhecida, registre responsável e teste de aceite. A próxima etapa mostra os helpers que produzem parte dessa evidência, não uma decisão automática.

Um caminho prático é comparar as fontes em duas passagens. Na primeira, sem join, verifique o contrato de cada uma: tipos de chave, percentual de chaves nulas, intervalo de datas e número de versões por entidade. Na segunda, sobre o mesmo recorte e snapshots declarados, meça cobertura e expansão e estratifique os achados por mês de decisão. Se cobertura cai em fevereiro, investigue se faltam clientes novos, se houve atraso na publicação ou se as chaves mudaram de formato. Uma média trimestral poderia ocultar que o primeiro mês está bem coberto e o último quase vazio. Só depois avalie se uma variável adicional melhora a análise ou o modelo, comparando populações equivalentes e separação temporal adequada.

Não confunda “mesma quantidade de linhas” com “cruzamento correto”. Um `left join` com direita única pode manter o total e preencher todos os atributos com nulo porque as chaves têm formatos incompatíveis. Também pode preservar a cardinalidade e usar uma versão atual para explicar uma decisão antiga, introduzindo informação futura. Exija uma checagem de conteúdo e de instante além da contagem. Quando a conclusão depende de uma tabela de correspondência entre identificadores, documente quem a mantém e desde quando cada associação é válida. Uma correspondência criada depois da decisão pode conter informação que o processo histórico não tinha.

O relatório de cross-EDA deve mostrar, para cada decisão GO/CONDICIONAL/NO-GO, o dado que a sustenta e a ação que a tornaria revisável. “CONDICIONAL: 12% dos contatos de fevereiro não têm feature elegível; responsável pela fonte verificará atraso de publicação e repetiremos o diagnóstico” é melhor que “faltam alguns dados”. “NO-GO: origem não guarda versões históricas e não permite reconstruir disponibilidade” indica um bloqueio que mais Spark não resolve. Evite transformar uma observação de correlação entre colunas em prova de sinal incremental: para isso, seria preciso comparar modelos ou análises com e sem a fonte em população e período comparáveis.

<a id="uso-hub-ml-cross-eda-ml"></a>
##### Ficha de uso — hub-ml-cross-eda-ml

<!-- usage-card:start hub-ml-cross-eda-ml -->
Escolha cross-EDA quando precisa decidir se várias fontes podem compor uma análise ou base de modelagem. Informe os cartões das fontes, unidade de decisão, chaves, snapshots, filtros, período, alvo e horizonte, disponibilidade dos atributos e restrições de uso. Se ainda não conhece uma fonte, faça sua exploração individual antes de concluir que o cruzamento é viável. Sem tempo confiável, mantenha a prontidão preditiva em aberto.

O pedido abaixo organiza a investigação antes de qualquer materialização. A entrega esperada é mapa das fontes, contrato temporal, diagnóstico de cobertura e multiplicidade, riscos e decisão GO, CONDICIONAL ou NO-GO com responsáveis e próximos testes. Confira quais medições foram realmente executadas, em quais recortes e com qual denominador. Verifique perdas e duplicações separadamente e examine exemplos de versões anteriores e posteriores à decisão. A skill está em L0/audit na policy vigente. Contexto, diagnóstico e PIT têm contratos distintos; o preflight de contexto não executa join e não substitui a finalização/verificação do perfil PIT. Se o agente oferecer apenas um plano por falta de acesso, registre a entrega como proposta. Não preencha medições faltantes com os números ilustrativos deste capítulo.

```text
@hub-ml-cross-eda-ml
Avalie a viabilidade de combinar [ÂNCORA] e [COMPLEMENTAR].
Cartões, snapshots, filtros e restrições: [CONTEXTO].
Unidade, chaves, decisão, alvo/horizonte e disponibilidade: [DEFINIÇÕES].
Primeiro apresente plano; não materialize nem execute nesta etapa.
Proponha verificações de cobertura, expansão e tempo, decisão condicionada
e próximos testes. Declare toda medição ainda não realizada.
```
<!-- usage-card:end hub-ml-cross-eda-ml -->

<a id="mu09-3"></a>
#### 3. Como diagnosticar expansão e escolher a versão disponível no tempo?

A receita direta abaixo ensina os helpers; não substitui o runner de um perfil já selecionado. O perfil `LOCAL_SYNTHETIC_PIT_V1` exige UTC, fronteira inclusiva e janela positiva, limita cada fonte a 500 linhas e bloqueia atraso variável, fronteira `LT` ou bitemporalidade. Preserve inputs e run_id externos ao payload para a verificação.

Comece por `diagnosticar_join` quando quer saber o efeito **de uma chave** antes de combinar as colunas. Ele recebe dois DataFrames Spark, chave simples ou composta e número de exemplos de chaves órfãs. A chamada pode fazer contagens, agregações e joins de diagnóstico; portanto, prepare uma população filtrada, fonte autorizada e compute compatível. Se a tabela de histórico contém várias versões por cliente, um diagnóstico por `id_cliente` revela a multiplicação de um join ingênuo, não significa que você deva materializá-lo.

```python
from hub_snippets.spark.join_diagnostics import diagnosticar_join

contatos = spark.table("catalogo.esquema.contatos_exemplo")  # placeholder
historico = spark.table("catalogo.esquema.historico_exemplo")  # placeholder
diag = diagnosticar_join(contatos, historico, "id_cliente", amostra_orfas=5)
print(diag["linhas_esquerda"], diag["linhas_apos_join_left"])
print(diag["cobertura_pct_chaves_validas"], diag["expansao_prevista_left"])
print(diag["exemplos_sem_match"])
```

Leia `cobertura_pct_chaves_validas` como porcentagem das **linhas da esquerda com chave não nula** que encontram alguma chave à direita. `chaves_nulas_esquerda` é uma causa separada. `linhas_apos_join_left` inclui órfãs e chaves nulas preservadas; `linhas_apos_join_inner` as perde. A multiplicidade da direita considera somente chaves presentes na esquerda. Se a esquerda ilustrativa tiver E001, E002 e uma chave nula, e a direita duas linhas E001, o left projetado tem quatro linhas: duas de E001, uma órfã E002 e uma sem chave. Cobertura das chaves válidas é 1/2, ou 50%; expansão left é 4/3, cerca de 1,333. Isso é aritmética ilustrativa da API, não medição Spark neste manual.

Quando a direita é um histórico, use `pit_join` para associar uma única versão elegível por decisão. Antes da chamada, confirme três relógios: instante da decisão, referência do valor e momento em que o valor ficou disponível. A API soma a `ts_feature` um `atraso_publicacao_dias` fixo e exige disponibilidade menor ou igual a `ts_decisao`. O atraso é obrigatório, inteiro não negativo; zero só quando disponibilidade imediata foi demonstrada. `janela_maxima_dias` limita a idade da **referência**. Se `ts_feature` for uma data sem horário, ela vira meia-noite no fuso da sessão; um fechamento diário tipicamente requer pelo menos um dia de atraso para não aparecer na manhã do mesmo dia.

```python
from hub_snippets.spark.pit_join import pit_join

com_saldo, pit = pit_join(
    contatos, historico, chave="id_cliente",
    ts_decisao="ts_decisao", ts_feature="ts_feature",
    atraso_publicacao_dias=1, janela_maxima_dias=30,
    colunas_feature=["saldo"], sufixo="_hist",
    politica_empate="erro", devolver_disponibilidade=True,
)
print(pit["linhas_fato"], pit["com_feature"])
print(pit["sem_feature_disponivel_na_data"], pit["fuso_da_sessao"])
com_saldo.select("id_cliente", "ts_decisao", "saldo_hist", "__feature_disponivel_em_hist").limit(5).show()
```

No cenário ilustrativo, a decisão de E001 em 12/01 às 14h pode usar uma versão referida a 11/01 às 10h com atraso de um dia: ficou disponível em 12/01 às 10h. Uma versão referida a 12/01 às 10h só chega em 13/01 às 10h e deve ficar de fora. Se E002 não tem histórico, sua linha continua no DataFrame com `saldo_hist` nulo. `pit` separa `sem_chave_ou_data`, `entidade_sem_historico` e `sem_feature_disponivel_na_data`, além de `com_feature`. Essas quatro categorias devem somar `linhas_fato`. `cobertura_pct_linhas_validas` exclui da base os fatos sem chave ou data; não leia 100% como cobertura de toda a âncora.

O `pit_join` executa ações de contagem e uma junção de candidatos potencialmente custosa. Evite também nomes auxiliares `__disponivel_em`, `__ts_feature_ref`, `__rank`, `__empatados` e prefixos `__pit_*`: o helper não confere todas as colisões. Confirme colunas e tipos antes de rodar e teste o desenho em dados pequenos ou representativos; não estime custo apenas pelo número final de linhas. O resultado tabular preserva os fatos, inclusive fatos repetidos, e acrescenta as colunas escolhidas. Confira a contagem de saída e compare manualmente algumas entidades com versões de ambos os lados da decisão. A coluna de disponibilidade devolvida ajuda a testar a regra sem presumir que `saldo` é o relógio. Se a fonte publica com atraso variável ou reescreve o passado sem histórico de revisões, um atraso fixo não reconstrói a disponibilidade real; obtenha dado melhor ou mude o desenho antes de chamar a junção de point-in-time correta.

As duas APIs respondem perguntas consecutivas, não intercambiáveis. `diagnosticar_join` revela o que um join por chave faria com a cardinalidade; seu 1:N pode ser esperado para uma tabela histórica. `pit_join` escolhe uma versão por combinação de entidade e decisão, respeitando tempo e atraso declarados. Se duas versões elegíveis empatam **no instante de disponibilidade mais recente selecionado** para uma entidade e decisão, a política padrão `politica_empate="erro"` levanta `ValueError`. Um empate antigo que não foi selecionado, ou uma versão futura inelegível, não dispara esse erro por si. Investigue duplicidade na origem e qual registro é verdadeiro. As opções `menor` e `maior` impõem um critério pelos valores trazidos; escolha-as apenas quando houver regra de negócio justificável, não para silenciar o erro.

Há dois tipos de ausência que pedem respostas diferentes. `entidade_sem_historico` sugere chave não mapeada, população fora da fonte ou fonte incompleta. `sem_feature_disponivel_na_data` significa que existe histórico para a entidade, mas nenhuma versão satisfaz disponibilidade e janela naquela decisão. Confira timestamp, fuso da sessão, atraso e idade máxima antes de mudar a população. Aumentar a janela apenas para elevar cobertura pode introduzir valores velhos; reduzir o atraso apenas para preencher nulos pode introduzir futuro. Se o diagnóstico mostrar `sem_chave_ou_data`, volte à qualidade dos fatos da âncora. Use `linhas_feature_com_ts_nulo` para inspecionar também um problema temporal na direita.

Registre as escolhas temporais ao lado do resultado: data de decisão, regra de publicação, janela, fuso e versão das entradas. Assim outra pessoa consegue reproduzir por que um valor foi aceito ou rejeitado.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu09-h-fontes-desta-parte"></a>
##### Fontes desta parte

`ambiente_databricks/.assistant/hub_snippets/spark/join_diagnostics/{join_diagnostics.py,README.md}`; `ambiente_databricks/.assistant/hub_snippets/spark/pit_join/{pit_join.py,README.md}`; `ambiente_databricks/.assistant/skills/hub-ml-cross-eda-ml/{SKILL.md,input.schema.json,scripts/README.md}`; `ambiente_databricks/.assistant/hub_scripts/skill_execution/domain_context/temporal.schema.json`; `ambiente_databricks/.assistant/hub_prompts/comparar_tabelas/comparar_tabelas.md`; `ambiente_databricks/.assistant/hub_prompts/cross_eda/cross_eda.md`. Exemplos e números são ILLUSTRATIVE, sem execução Spark, skill ou preflight nesta redação.
<!-- editorial:exclude:end -->

<a id="mu09-4"></a>
#### 4. Como interpretar multiplicação, perda, empate e bloqueio?

Confronte os diagnósticos com a unidade escolhida antes de publicar uma base combinada. Se cada linha de contato deve continuar sendo uma decisão, `expansao_prevista_left` acima de 1 indica que o join simples multiplicaria algumas linhas. No exemplo sintético da seção 3, a passagem de três para quatro linhas ocorre porque E001 tem duas versões à direita; não é um aumento de clientes nem de contatos. Evite somar resultados depois desse join como se fossem quatro decisões independentes. Uma saída legítima pode ser manter o histórico separado e usar `pit_join` para escolher uma versão disponível por decisão. Se a pergunta realmente exige uma linha por contrato e o histórico representa contratos, redefina o grão e documente a conversão, em vez de rotular toda expansão como defeito.

Perda também tem mais de uma causa. Para contar **linhas da âncora perdidas** por um inner join, some `chaves_nulas_esquerda` e `linhas_sem_match_chave_valida`. Não subtraia `linhas_apos_join_inner` de `linhas_esquerda`: duplicações de chaves casadas podem compensar perdas e até deixar os totais iguais. No exemplo anterior, E002 e a chave nula se perderiam, enquanto E001 produziria duas linhas; o inner teria duas linhas, mas perderia duas decisões originais. Um left preserva órfãs e chaves nulas, porém deixa atributos vazios; preservação de linhas não é cobertura de informação. Confira essas duas causas ao lado de `cobertura_pct_chaves_validas`, cujo denominador exclui chaves nulas. No `pit_join`, confirme que `linhas_fato` coincide com a âncora e que as quatro categorias se reconciliam. Depois olhe a cobertura por mês e segmento relevante, porque ausência concentrada pode tornar uma média global pouco útil.

Use um quadro de decisão para separar sintoma de resposta. Ele pode ficar no relatório de cross-EDA com responsável e critério de aceite:

| Sintoma | Leitura inicial | Próxima ação e aceite |
|---|---|---|
| Expansão 1:N no join simples | Mais de uma linha relevante à direita | Confirmar grão; selecionar versão temporal ou regra de agregação; recontar decisões |
| Chave nula ou órfã | Falha de identificação ou ausência na fonte | Investigar origem/mapeamento; medir cobertura no denominador declarado |
| Histórico inelegível | Dado existe, mas não estava disponível ou está velho | Conferir referência, atraso, fuso e janela com produtor; não antecipar publicação |
| Empate no instante escolhido | Versões concorrentes | Corrigir duplicidade ou justificar `menor`/`maior`; repetir checagem |
| Falta de histórico confiável | Passado não pode ser reconstruído | Bloquear afirmação temporal até obter versão e disponibilidade verificáveis |

Se `pit_join` parar por empate com a política padrão, preserve o erro como evidência de uma decisão ainda não tomada. A opção `maior` escolhe maior valor dentre colunas selecionadas em um desempate, mas isso não faz dele o valor verdadeiro; `menor` tem o mesmo limite. Investigue também colisão de nomes ao juntar múltiplas fontes: use `sufixo` com intenção clara e mantenha o nome da coluna de disponibilidade quando precisar auditá-la. Se faltar coluna ou o atraso for inválido, corrija a entrada real e execute novamente; não preencha com zero ou altere o timestamp para produzir uma linha.

Ao final, declare GO apenas se chave, grão, cobertura, temporalidade, qualidade e autorização de uso sustentam a aplicação proposta. Sem dados ou execução suficientes, registre **NÃO AVALIADO**. CONDICIONAL identifica pendências mitigáveis com responsável, prazo e teste reproduzível. NO-GO cabe quando não há chave coerente, disponibilidade histórica confiável ou cobertura suficiente para a população exigida. A skill de cross-EDA fornece o roteiro desse julgamento; seus templates de inventário, viabilidade, matriz de cobertura e scorecard ajudam a apresentar evidência, mas não promovem automaticamente o estudo a um nível de policy que ainda não foi promovido. Entregue ao próximo analista os cartões de fonte, filtros e snapshots, diagnósticos, regra de join, exemplos verificados manualmente, decisão e perguntas abertas. Assim ele sabe quais fatos pode reutilizar e quais hipóteses ainda exigem teste.

Se uma verificação falhar, registre a versão exata da entrada e repita os cálculos depois da correção. Compare a nova cobertura e a nova contagem de fatos com as anteriores: uma melhora no percentual pode vir simplesmente da exclusão de decisões difíceis, e essa perda precisa ficar visível para quem decide.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu09-h-fontes-desta-parte-1"></a>
##### Fontes desta parte

`ambiente_databricks/.assistant/hub_snippets/spark/join_diagnostics/join_diagnostics.py`, `ambiente_databricks/.assistant/hub_snippets/spark/pit_join/pit_join.py`, `ambiente_databricks/.assistant/skills/hub-ml-cross-eda-ml/SKILL.md` e templates de `coverage_matrix.md`, `join_feasibility.md` e `readiness_scorecard.md`. Quadro e números são ilustrações de leitura; nenhuma execução real foi alegada.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU08](#mu08) · [Próximo: MU10](#mu10) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT07](MANUAL_TECNICO_V2.md#mt07) · [MT17](MANUAL_TECNICO_V2.md#mt17)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu10"></a>
<a id="mu10"></a>
### MU10 — Preparar features, RFV, safra e estudos estatísticos

<!-- editorial:exclude:start -->
**Você quer:** transformar uma pergunta de negócio em variáveis ou em um estudo com tempo e evidência claros. **Rota:** escolha o instrumento (1), fixe cortes e definições (2), execute apenas a rota compatível com sua entrada (3) e interprete efeito, cobertura e incerteza (4). Os dados e resultados pequenos deste capítulo são ILLUSTRATIVE; nada foi executado em uma fonte corporativa.
<!-- editorial:exclude:end -->

<a id="mu10-1"></a>
#### 1. Preciso desenhar uma feature, calcular RFV, comparar safras ou testar uma hipótese?

Comece pela decisão que será tomada, não pela técnica que parece mais sofisticada. Se quer criar uma variável reutilizável para previsão, como “quantas compras o cliente fez nos 30 dias anteriores ao contato”, a rota é **feature engineering**: especificar fonte, grão, janela, disponibilidade, fórmula, dono e testes antes de materializar. Se só precisa calcular recência, frequência e valor em uma data comum, `rfv_calculator` já entrega medidas brutas. Se pergunta “os contratos originados em janeiro pioram mais cedo que os de março?”, a unidade é **safra**, ou coorte de entrada, comparada na mesma idade. Se precisa decidir se uma diferença observada é compatível com um efeito relevante sob incerteza, formule um estudo de **validação estatística** com hipótese e desenho.

O mesmo conjunto de dados pode originar as quatro perguntas, mas elas não têm a mesma saída. RFV soma e conta eventos até um corte; não escolhe segmento comercial. A análise de safra alinha contratos pela idade desde a origem; não prova causa da diferença. Uma feature é uma especificação que deve funcionar tanto no histórico quanto no momento de uso; uma estatística descritiva isolada não garante essa paridade. Um teste de hipótese responde a uma pergunta inferencial com pressupostos e intervalo; não transforma automaticamente uma variável em feature aceita. O quadro serve para escolher o próximo passo:

| Intenção do leitor | Entrada mínima | Rota do Hub | Saída que se deve conferir |
|---|---|---|---|
| Construir variável para decisão/modelo | Entidade, decisão, target, fontes e disponibilidade | `hub-ml-feature-engineering` e helpers adequados | Spec, código, testes e risco de vazamento |
| Resumir comportamento até corte comum | Tabela de eventos, entidade, data, valor e corte | `rfv_calculator` | DataFrame Spark com medidas brutas e janelas |
| Comparar coortes por maturação | Contrato, origem, observação, evento e corte | `hub-ml-analise-safra`; `build_vintage_table` para tabela pequena | Safra × MOB, cobertura e taxa quando completa |
| Avaliar diferença/pressuposto com incerteza | Hipótese, população, grupos, desenho e efeito relevante | `hub-ml-validacao-estatistica` | Plano, estimativa, intervalo, pressupostos e decisão condicionada |

As três skills permanecem L0/audit na policy, apesar de perfis executáveis já integrados. `target_level` não é promoção. Feature Engineering separa lag local, vista PIT em memória e materialização sintética autorizada; Safra oferece perfil mensal binário com roster fixo; Estatística oferece KS de duas amostras sintéticas. Cada rota exige contrato, inputs e verificador próprios. Use o `SKILL.md` e seu `scripts/README.md` antes do cálculo; helper avulso não substitui runner selecionado. Receipt ou PASS local não homologa dados reais, autoriza escrita nem torna toda a metodologia executável.

Um pedido pequeno e bem formulado orienta a escolha: “Em 31/01, quero medir compras por cliente nos últimos 30 dias para selecionar uma campanha” aponta RFV; “quero produzir esse atributo para cada contato histórico” exige janela por decisão e contrato de feature; “quero comparar contratos de janeiro e fevereiro no MOB 3” aponta safra; “quero saber se a diferença no MOB 3 excede o mínimo relevante” pede plano estatístico após confirmar população e maturidade. Se não sabe qual pergunta tem, descreva público, decisão e unidade de linha; o MU03 ajuda a localizar o recurso, e MU09 resolve a viabilidade de múltiplas fontes antes de juntar características.

Escolha também o nível de trabalho esperado. Um helper isolado responde a uma operação com entradas definidas; uma skill orienta a sequência de levantamento, verificação, interpretação e entrega. Um briefing preenchido pode pedir essa sequência de maneira clara, mas não executa cálculos por existir como arquivo. Se você precisa de uma decisão de negócio hoje, diga se quer apenas proposta de estudo, notebook para executar no ambiente autorizado ou resultado efetivamente calculado e revisado. Essa distinção evita que uma tabela de exemplo seja apresentada como evidência da sua carteira. Quando uma técnica não se encaixa, registre o motivo: uma carteira sem originação confiável não sustenta safra, e uma fonte sem histórico de publicação não sustenta afirmação point-in-time.

<a id="uso-hub-ml-feature-engineering"></a>
##### Ficha de uso — hub-ml-feature-engineering

<!-- usage-card:start hub-ml-feature-engineering -->
Escolha feature engineering quando deseja construir variáveis que possam ser reproduzidas no treino e no momento de uso. Informe entidade, chave, alvo, horizonte, instante de decisão, fontes, disponibilidade, janela de observação, frequência de cálculo e modo de consumo. Para uma fotografia RFV independente, o helper pode bastar; para uma variável histórica por decisão, o contrato precisa explicar como excluir informação que ainda não existia.

O pedido abaixo busca especificação antes da implementação. A entrega esperada reúne cartões de features, prioridades, transformação proposta, plano de materialização, testes, riscos e responsáveis. Confira fórmula, unidade, grão, corte temporal, ausentes e linhagem de cada variável. Exija exemplos de fronteira da janela e testes de paridade entre cálculo histórico e inferência. Parâmetros aprendidos, como mediana de imputação, devem ser ajustados somente no treino. A policy atual mantém esta skill em L0/audit: texto e templates não comprovam job executado, tabela criada ou feature aprovada. Se o tempo de publicação for desconhecido, peça investigação e mantenha a feature experimental ou bloqueada. Antes de executar, revise separadamente operações, custo e destino.

```text
@hub-ml-feature-engineering
Planeje [FEATURES] para [ENTIDADE/CHAVE], decisão [INSTANTE]
e alvo [DEFINIÇÃO/HORIZONTE]. Fontes e disponibilidade: [CONTEXTO].
Janelas, frequência, consumo e restrições: [DEFINIÇÕES].
Não execute nem materialize nesta etapa. Entregue specs, prioridades,
testes temporais e de paridade, riscos, responsáveis e lacunas.
```
<!-- usage-card:end hub-ml-feature-engineering -->

<a id="mu10-2"></a>
#### 2. Que data de referência e denominador tornam o estudo válido?

Registre quatro tempos antes de calcular: quando a entidade entrou ou o evento ocorreu, quando a decisão seria tomada, quando a informação ficou disponível e quando o resultado foi observado. Eles podem coincidir em uma tabela, mas não são sinônimos. Uma compra de segunda-feira publicada na sexta não estava disponível para decidir na terça. O `rfv_calculator` filtra pela **data do evento** até `dt_referencia`; sozinho, não modela atraso de publicação. Se a decisão é por contato, cada contato pode ter seu próprio instante e um corte global não basta. A rota `pit_join` do MU09 mostra como selecionar versões disponíveis em cada decisão, desde que a origem guarde histórico confiável.

Para RFV, fixe primeiro o grão: uma linha da tabela significa compra, item de compra ou atualização? A frequência do script é contagem de linhas. Se cada compra contém três itens, contar linhas resultará em três, não uma compra. A soma de `valor` também depende de estornos, moeda e nulos. Escreva a regra de negócio para esses casos antes de interpretar total. Escolha `dt_referencia` em formato de data, chave de entidade não nula e `periodos` inteiros positivos; a janela de 30 dias inclui o dia do corte e os 29 anteriores. Quem não tem evento válido até esse corte não aparece no retorno; isso difere de aparecer com frequência zero. Quando uma janela recente não tem eventos para um cliente que possui histórico anterior, os pares da janela são preenchidos com zero.

Um cartão de feature evita que uma coluna calculada hoje receba um significado diferente amanhã. Preencha, por exemplo, “`freq_compra_30d`: quantidade de compras distintas de `id_pedido` para `id_cliente`, nos 30 dias de calendário até o instante de decisão, usando apenas pedidos publicados até esse instante; origem X, atualização diária, tipo inteiro, nulos conforme ausência de histórico, dono Y”. O helper RFV não calcula `countDistinct(id_pedido)` nem filtra disponibilidade: se essas regras forem necessárias, a spec aponta uma adaptação ou outro processo. Não chame a saída RFV de implementação desse cartão até demonstrar equivalência.

Para safra, a origem define a coorte e **MOB** (*months on book*, meses desde a origem) define sua idade. O helper `build_vintage_table` calcula a diferença inteira entre ano/mês da observação e da originação, salvo se você fornecer `mob_col`. Uma observação de 31/01 e outra de 01/02 podem ficar em MOBs diferentes apesar de um dia de distância; declare essa convenção. Defina se o `target` 0/1 é evento naquele MOB ou indicador acumulado, pois `target_is_cumulative` muda a validação. Registre data de corte, snapshots incluídos, regra para contratos sem observação e se a métrica é fluxo ou estoque acumulado. Não some porcentagens mensais para obter incidência acumulada; conte contratos com evento acumulado e divida pelo denominador coerente.

A implementação descarta observações com MOB ausente ou negativo antes de validar as demais e forma `n_contratos_safra` a partir dos contratos que restaram. Portanto, compare esse denominador com a população de originação original para detectar exclusões; o retorno não recupera contratos que não possuem snapshot válido. Em cada célula safra × MOB, `n_contratos_observados` mede quantos aparecem naquele MOB e `cobertura_observada` divide por `n_contratos_safra`. Só quando a célula está completa o helper publica `taxa_acumulada`; caso contrário, ela é `NaN`, ou ausente, e não zero. Compare janeiro e fevereiro no mesmo MOB e com coberturas conhecidas. Uma safra recente sem MOB 6 não é uma safra com taxa zero no MOB 6. No [runner mensal](skills/hub-ml-analise-safra/scripts/README.md), o denominador vem do roster completo em MOB0 e permanece fixo; `IMMATURE`, `NO_OBSERVATIONS` e `INCOMPLETE` não autorizam taxa provisória sobre o subconjunto observado.

Para um teste estatístico, fixe a população e a **unidade independente** antes de escolher teste. Dois contatos do mesmo cliente podem compartilhar comportamento e não serem duas observações independentes. Declare H0, a hipótese nula de referência, e H1, a alternativa que quer investigar. Defina o **estimando**, isto é, a quantidade ou efeito que deseja conhecer na população, a diferença mínima que mudaria a decisão, período, grupos, desenho amostral e número de comparações planejadas. Escolha antes de olhar o resultado o **alfa**, nível de significância usado como regra de decisão estatística. O p-valor descreve quão incompatível seria uma estatística tão ou mais extrema com H0 sob o modelo e pressupostos do teste; não é a probabilidade de H0 ser verdadeira nem mede tamanho de efeito. Um p-valor alto não prova que grupos são equivalentes. Se pretende testar várias safras ou segmentos, planeje tratamento da multiplicidade. Se o teste consumir pandas/scipy, limite a coleta ao driver ou agregue no Spark primeiro, preservando pesos e estrutura de dependência quando necessários.

Antes de executar, confirme acesso à fonte, compute e pacote, tipos de colunas, data de corte e permissões de uso. O capítulo MU02 mostra como preparar imports. Não use um exemplo sintético da documentação como prova de que a sua fonte tem aqueles campos. Se falta a data de disponibilidade, o resultado pode servir a um retrato descritivo da história observada, mas não sustenta por si uma afirmação de ausência de vazamento numa previsão histórica.

Planeje a avaliação temporal da feature antes de treiná-la. Um conjunto de treino com decisões de meses posteriores misturado ao teste de meses anteriores pode fazer uma variável aparentemente útil parecer disponível quando não era. `temporal_split` trabalha em pandas com períodos completos de calendário e gaps explícitos; ele pode ainda remover entidades repetidas entre partições quando `group_col` é usado. Recuse ou renomeie a coluna auxiliar `__period`; chaves de grupo nulas não têm exclusividade garantida. Essa opção é adequada apenas se independência entre entidades for exigida pela pergunta; em séries por entidade, observar o passado da mesma entidade pode ser parte legítima do desenho. O helper não conserta uma feature calculada com dados futuros: primeiro construa a variável no instante de cada decisão, depois separe treino, validação e teste.

<a id="uso-hub-ml-analise-safra"></a>
##### Ficha de uso — hub-ml-analise-safra

<!-- usage-card:start hub-ml-analise-safra -->
Escolha análise de safra quando quer comparar grupos definidos pela entrada e acompanhar sua maturação. Informe unidade, identificador, data de origem, observação, evento, exposição, corte, snapshots e denominador. Declare se o evento é incremental ou acumulado e qual convenção de MOB será usada. MOB significa meses desde a origem; duas safras devem ser comparadas na mesma idade observada, com maturidade e cobertura conhecidas.

O pedido abaixo prepara o contrato antes de calcular curvas. A entrega esperada é notebook ou relatório com qualidade, definições, matriz safra por MOB, curvas, volumes, cobertura, limitações e ações investigativas. Confira o cadastro inicial contra os contratos que sobreviveram aos filtros; o helper não recupera contratos sem observação válida. Uma célula imatura ou incompleta deve continuar ausente quando o contrato assim exige. Não some taxas mensais nem substitua ausência por zero para completar o heatmap. Na policy vigente, a skill está em L0/audit; o perfil mensal integrado tem alcance específico e não executa toda análise de safra. Se quiser inferência sobre diferenças, encaminhe desenho e incerteza à skill estatística, preservando a pergunta original.

```text
@hub-ml-analise-safra
Planeje comparar [COORTES] na unidade [UNIDADE], com chave [CHAVE].
Origem, observação, evento, exposição e snapshots: [COLUNAS/DEFINIÇÕES].
Corte, denominador e convenção de MOB: [REGRAS OU LACUNAS].
Não execute nesta etapa. Proponha qualidade, matriz e curvas no mesmo MOB,
tratamento de maturidade/cobertura, limitações e próximos testes.
```
<!-- usage-card:end hub-ml-analise-safra -->

<a id="mu10-3"></a>
#### 3. Como executar cada rota sem pedir ao helper mais do que ele entrega?

Para uma fotografia RFV em corte comum, importe a fachada de `hub_scripts` e passe **nome de tabela**, não DataFrame. O trecho presume uma tabela autorizada em grão de compra; substitua os nomes pelo seu schema e verifique as colunas antes. A chamada devolve DataFrame Spark, cuja prévia limitada é uma ação separada:

```python
from hub_scripts.rfv_calculator import rfv_calculator

rfv = rfv_calculator(
    "catalogo.esquema.compras_exemplo",  # placeholder
    col_cliente="id_cliente", col_data="dt_compra", col_valor="valor",
    dt_referencia="2026-01-31", periodos=(30, 60, 90),
)
rfv.select("id_cliente", "ultima_data", "recencia",
           "frequencia_total", "valor_total", "frequencia_30d").limit(5).show()
```

Leia `ultima_data` e `recencia` junto de `frequencia_total` e `valor_total`. Suponha E001 com compras de 100 em 10/01 e 50 em 20/01 e corte inclusivo em 31/01: a frequência total é 2, valor total 150 e recência 11 dias; ambas entram na janela de 30 dias, que começa em 02/01. Uma compra em 01/02 não entra. Isso é uma conta ilustrativa, não a saída de um notebook executado aqui. Confira para uma entidade pequena as duas bordas da janela e compare manualmente com o retorno. Se `valor` inclui estorno de -20, ele reduz a soma; o helper não decide se estorno deve contar como compra.

Se RFV será feature de um modelo, transforme o cálculo em spec e teste sua disponibilidade por decisão. A skill `hub-ml-feature-engineering` pede definição, chave, janela, event time, momento real de disponibilidade, tratamento de missing, dono e testes de paridade treino–uso. Use o helper somente quando seu corte comum e grão correspondem a essa spec. Para datas por linha, use construção point-in-time; para janelas por entidade, confirme partição e corte em cada decisão. **Imputação** preenche valores ausentes segundo regra declarada; **binning** divide valores em faixas; **encoding** representa categorias em formato consumível pelo modelo. Quando seus parâmetros são aprendidos dos dados — por exemplo mediana de preenchimento, limites das faixas ou vocabulário de categorias — ajuste-os somente no treino e aplique a mesma regra à validação e ao teste. O fato de uma coluna ter nome `freq_30d` não prova que respeita os 30 dias disponíveis no passado de cada linha.

As [rotas atuais de features](skills/hub-ml-feature-engineering/scripts/README.md) separam `FIXED_LAG_L1_V1`, lag da observação anterior elegível por entidade, de `COMPOSED_PIT_FEATURE_VIEW_V1`, projeção em memória após verificar PIT upstream. Materialização exige request de efeito, autorização vinculada, destino pessoal, readback, replay e cleanup; `UNKNOWN` pede inspeção, sem retry automático. Nenhuma delas faz fit ou aprova a feature.

Para safra, prepare uma **tabela pandas pequena e deliberadamente limitada** com contrato, originação, observação e evento binário. `build_vintage_table` não recebe DataFrame Spark; não converta tabela inteira com `toPandas()` sem estimar volume e restringir população. O exemplo cria quatro observações sintéticas de dois contratos; cada contrato aparece em MOB 0 e 1, e apenas C1 registra evento no MOB 1:

```python
import pandas as pd
from hub_snippets.ml.vintage_analysis import build_vintage_table, compare_safras

amostra = pd.DataFrame({
    "id_contrato": ["C1", "C1", "C2", "C2"],
    "dt_orig": ["2026-01-05"] * 4,
    "dt_ref": ["2026-01-31", "2026-02-28", "2026-01-31", "2026-02-28"],
    "evento": [0, 1, 0, 0],
})
vintage = build_vintage_table(
    amostra, contract_id="id_contrato", dt_originacao="dt_orig",
    dt_referencia="dt_ref", target="evento", safra_grain="month",
)
print(vintage[["safra", "mob", "n_contratos_observados",
               "n_contratos_safra", "cobertura_observada", "taxa_acumulada"]])
```

Pelo contrato da função, janeiro tem dois contratos após filtro. MOB 0 está completo e tem taxa 0/2; MOB 1 está completo e tem 1/2, ou 50%. Se a linha de C2 em fevereiro faltar, a célula MOB 1 teria cobertura 1/2 e `taxa_acumulada=NaN`, mesmo que C1 tenha evento. Não conclua taxa de 100%. `compare_safras(vintage, mob_checkpoints=[1, 3])` pode organizar comparação por MOB quando houver mais safras; checkpoints não observados ficam ausentes. Curva ou heatmap ajudam a ver maturação, mas figuras não preenchem células imaturas. Se usar tema visual resolvido, as rotas `*_resolvido` alteram aparência sem mudar denominador ou taxa.

Quando a pergunta é inferencial, preencha um cartão antes de rodar teste: “H0: diferença de taxa no MOB 3 entre safras comparáveis é zero; H1: difere; unidade contrato; efeito mínimo relevante 3 pontos percentuais; grupos e tamanho; independência a conferir; teste e intervalo a escolher conforme desenho; família de comparações declarada”. Não escolha teste ou alfa olhando a primeira saída. A skill de validação estatística recomenda reportar estimativa, intervalo, tamanho de efeito, pressupostos e consequência operacional. Se a coorte ainda não atingiu MOB 3, não há observação para esse teste; esperar maturidade ou mudar a pergunta é mais honesto que atribuir zero.

Essas rotas podem se encadear, mas não se substituem. `rfv_calculator` retorna DataFrame Spark de medidas brutas; `build_vintage_table` retorna pandas de safra × MOB; uma skill orienta o processo e a revisão. Não trate um trecho de código exibido como execução certificada nem persista resultado sem decidir destino, contrato e permissões. Se uma fonte falha por coluna ausente, confira schema; se o MOB é inválido, investigue origem/referência; se a amostra estatística não representa a população, revise desenho antes de interpretar p-valor.

Para outras perguntas, escolha o helper pelo fenômeno. [`calculate_woe_iv`](hub_snippets/ml/woe_iv_calculator/README.md) pode avaliar separação de categorias ou faixas já definidas diante de um alvo binário, mas seu valor não aprova automaticamente uma feature, e as faixas precisam ser aprendidas somente no treino. [`kaplan_meier`](hub_snippets/ml/kaplan_meier/README.md) e [`survival_cox`](hub_snippets/ml/survival_cox/README.md) tratam tempo até evento com censura; são caminhos quando contratos têm acompanhamentos de durações diferentes e “ainda não ocorreu” não significa “nunca ocorrerá”. Eles não substituem uma safra descritiva apenas por parecerem mais estatísticos. `score_bands` e `scorecard_builder` pertencem à etapa de pontuação de um modelo, não ao cálculo inicial de RFV. Consulte [MT08](MANUAL_TECNICO_V2.md#mt08) para APIs de ML, [MT17](MANUAL_TECNICO_V2.md#mt17) para contratos de skills e [MT20](MANUAL_TECNICO_V2.md#mt20) para a fronteira com micromodelos; leia as páginas de cada objeto antes de incorporá-lo e declare qual pergunta motivou a escolha.

Se o estudo exigir comparação formal de safras, não aplique um teste de proporções diretamente às células da tabela sem conferir independência, censura, tamanho e seleção. Uma taxa de 50% obtida de dois contratos é aritmeticamente correta e extremamente incerta; uma diferença de dois pontos percentuais entre milhares de contratos pode ser precisa e ainda irrelevante para a decisão. Peça à skill estatística uma proposta de estimando e intervalo compatível com o desenho e depois confronte o efeito observado com o mínimo relevante definido antes. Relate qualquer célula `NaN` como falta de observação completa, não como dado negativo para o teste.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu10-h-fontes-desta-parte"></a>
##### Fontes desta parte

`ambiente_databricks/.assistant/hub_scripts/rfv_calculator/{rfv_calculator.py,README.md}`; `ambiente_databricks/.assistant/hub_snippets/ml/vintage_analysis/{vintage_analysis.py,README.md}`; `ambiente_databricks/.assistant/skills/hub-ml-feature-engineering/SKILL.md`; `ambiente_databricks/.assistant/skills/hub-ml-analise-safra/{SKILL.md,scripts/README.md}`; `ambiente_databricks/.assistant/skills/hub-ml-validacao-estatistica/SKILL.md`; policy de skill enforcement. Exemplos são ILLUSTRATIVE, sem execução de Spark/pandas neste capítulo.
<!-- editorial:exclude:end -->

<a id="uso-hub-ml-validacao-estatistica"></a>
##### Ficha de uso — hub-ml-validacao-estatistica

<!-- usage-card:start hub-ml-validacao-estatistica -->
Escolha validação estatística quando a decisão exige estimativa com incerteza ou avaliação de pressupostos. Informe pergunta, população, unidade independente, grupos, período, desenho amostral, variáveis, estimando, efeito mínimo relevante e comparações planejadas. Estimando é o efeito ou quantidade que deseja conhecer. Diferencie diagnóstico exploratório de inferência; várias linhas do mesmo cliente podem exigir tratamento de dependência, não um teste de grupos independentes.

O pedido abaixo solicita plano antes de observar o resultado. A entrega esperada descreve hipóteses, método, pressupostos, amostra, limites de coleta, multiplicidade, estimativas e critérios de decisão; resultados entram somente após execução real. Confira se o método responde ao estimando, se preserva pesos ou pareamento necessários e se informa tamanho de efeito, unidade e intervalo. Um p-valor pequeno não mede relevância prática; um p-valor alto não prova equivalência. A policy atual está em L0/audit. O [perfil KS](skills/hub-ml-validacao-estatistica/scripts/README.md) aceita uma comparação sintética bicaudal, contínua, independente e sem empates; independência é declarada, não inferida. Exige alfa definido e oráculo externo ao payload. Não produz equivalência nem causalidade. O intervalo retorna `confidence_interval=None` e `confidence_interval_status="UNSUPPORTED_IN_PROFILE"`, sem números inventados. Se dados ou pressupostos faltarem, peça método compatível ou coleta adicional. Registre a lacuna e a consequência antes de recomendar retirada de variável ou retreino.

```text
@hub-ml-validacao-estatistica
Planeje avaliar [PERGUNTA/DECISÃO] em [POPULAÇÃO/PERÍODO].
Unidade, grupos, desenho e variáveis: [CONTEXTO].
Estimando, efeito mínimo, hipóteses e comparações: [DEFINIÇÕES/LACUNAS].
Não execute nem ajuste a decisão a resultados nesta etapa.
Proponha método, pressupostos, limites de coleta, intervalos,
multiplicidade, critério de decisão e próximos passos.
```
<!-- usage-card:end hub-ml-validacao-estatistica -->

<a id="mu10-4"></a>
#### 4. Como interpretar denominadores, efeito e incerteza para decidir o próximo passo?

Ao receber qualquer resultado, recupere a pergunta e os limites escritos antes da execução. Para RFV, registre o nome da tabela, o grão, a data de corte, os períodos e a quantidade de entidades com ao menos um evento válido. No exemplo sintético, `frequencia_total=2` de E001 significa duas linhas de compra até 31/01; se a origem estiver em grão de item, a leitura muda. `recencia=11` significa onze dias entre 20/01 e o corte, não onze dias desde a publicação do dado. `valor_total=150` soma os valores presentes segundo a semântica Spark; não assegura moeda uniforme, valor líquido ou ausência de estorno. Se você vai chamar essas medidas de features, confirme ainda a disponibilidade real em cada decisão histórica e a paridade do cálculo no momento de uso.

Para safra, leia sempre volume e cobertura antes da taxa. Na demonstração de dois contratos, MOB 1 completo permite descrever incidência acumulada de 1/2, ou 50%, naquela coorte. A célula com só um contrato observado teria `cobertura_observada=0,5` e taxa ausente: não é 0%, 50% nem 100% para a safra inteira. O denominador `n_contratos_safra` decorre das observações que sobreviveram ao filtro de MOB válido; reconcilie-o com o cadastro de originados quando a decisão depender de cobertura integral. Uma curva pode tornar a comparação legível, mas não adiciona contratos nem maturidade. No [briefing de safra](hub_prompts/safra/exemplo_safra.py), a frase sobre 202503 ter menos MOB não corresponde ao preparo: `fixtures.safras(..., mob_maximo=12)` gera MOB1–12 para todas as safras. Confira o máximo observado por safra; sem corte adicional, essa fixture não demonstra imaturidade diferenciada. Compare coortes no mesmo MOB, com calendário, mix de entrada e tamanho da população visíveis.

O relatório de uma feature precisa ir além do valor calculado. Use um cartão de aceite com nome, fórmula, origem, chave, instante de decisão, janela, atraso de publicação, regra de ausentes, tipo, testes e dono. Marque **aprovada** apenas quando as checagens exigidas pelo projeto passarem; **experimental** se há evidência parcial; **bloqueada** se tempo, fonte ou semântica impedem uso. Uma feature com distribuição estável pode continuar vazando informação futura; uma feature com nulos pode ser válida se a ausência tem sentido de negócio e tratamento definido. Registre o teste que permitiu ou impediu a decisão, não apenas uma cor de scorecard.

Para validação estatística, apresente estimativa com unidade e intervalo de confiança, tamanho e composição dos grupos, pressupostos, correção de múltiplas comparações quando cabível e consequência prática. “Diferença estimada de três pontos percentuais” é uma magnitude; o intervalo mostra a faixa de valores compatíveis com o método e dados sob seus pressupostos. Um p-valor pequeno não é a probabilidade de a hipótese nula ser verdadeira e não mede relevância para a operação. Um p-valor não pequeno também não comprova igualdade: pode refletir amostra insuficiente, variabilidade ou desenho inadequado. Se houver várias linhas por cliente, trate a dependência no plano antes de contar cada linha como observação independente.

Reaja à falha de acordo com a causa. RFV sem clientes esperados pede conferir data de corte, conversão de datas e eventos removidos, não preencher uma população fictícia de zeros. `build_vintage_table` pode rejeitar target não binário, MOB inválido ou target cumulativo que diminui; revise a definição na fonte e só então recalcule. Uma taxa ausente por cobertura incompleta pede investigar snapshots e maturidade, não forçar zero. Se uma premissa estatística falhar, peça método compatível, análise de sensibilidade ou coleta adicional e registre o risco residual. Em todos os casos, preserve os parâmetros e a versão da fonte para comparar o antes e o depois da correção.

Entregue ao próximo responsável uma ficha única com objetivo, população, unidade, fonte/snapshot, corte, definições de variáveis e evento, resultados com denominadores, limitações e questão aberta. Para RFV que seguirá à modelagem, encaminhe a spec à feature engineering; para safra com diferença aparente, encaminhe um plano de teste apenas se a decisão exige inferência; para fontes ainda incompatíveis, volte ao diagnóstico de MU09. O destinatário deve saber exatamente o que foi medido e qual decisão ainda depende de confirmação, sem confundir código de exemplo, cálculo feito no seu ambiente e aprovação de uso.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu10-h-fontes-desta-parte-1"></a>
##### Fontes desta parte

`ambiente_databricks/.assistant/hub_scripts/rfv_calculator/{rfv_calculator.py,README.md}`; `ambiente_databricks/.assistant/hub_snippets/ml/vintage_analysis/{vintage_analysis.py,README.md}`; `ambiente_databricks/.assistant/skills/hub-ml-feature-engineering/SKILL.md`; `ambiente_databricks/.assistant/skills/hub-ml-validacao-estatistica/SKILL.md`; `ambiente_databricks/.assistant/skills/hub-ml-analise-safra/SKILL.md`. Valores são ILLUSTRATIVE; nenhuma análise real foi executada para o manual.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU09](#mu09) · [Próximo: MU11](#mu11) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT08](MANUAL_TECNICO_V2.md#mt08)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu11"></a>
<a id="mu11"></a>
### MU11 — Construir e revisar um baseline de ML

<!-- editorial:exclude:start -->
**Você quer:** construir uma primeira referência de modelo que outra pessoa consiga comparar e revisar. **Rota:** defina a pergunta e o baseline trivial (1), prepare dados e escolha a família (2), use skill e helpers com entradas verificáveis (3); a parte final interpreta medidas, run e próximos passos (4). Os exemplos são sintéticos e ilustrativos: nenhum treinamento ou acesso remoto foi realizado para este texto. [Índice do manual](#sumario-mu).
<!-- editorial:exclude:end -->

<a id="mu11-1"></a>
#### 1. Que decisão o primeiro modelo deve ajudar a comparar?

Comece com uma frase que alguém de fora do projeto consiga contestar: “na data de contato, ordenar entidades pela chance de resposta nos próximos 30 dias, para escolher quais serão revisadas”. Essa frase fixa a **unidade** da previsão (uma decisão de contato), o **alvo** (resposta dentro de 30 dias), o **instante** em que a pontuação seria usada e o **horizonte** em que a resposta amadurece. O primeiro modelo é um **baseline**, uma régua inicial de comparação. Ele não precisa ser o mais complexo; precisa revelar se adicionar modelagem supera uma alternativa simples com dados e período equivalentes.

Escreva a população antes de abrir um notebook de treino. No exemplo fictício, são decisões para entidades `E001` a `E100`, elegíveis em janeiro a junho. Liste quem ficou fora: decisões duplicadas, resposta ainda imatura, falta de chave ou ausência de atributos indispensáveis. Conte linhas e entidades separadamente, porque uma entidade pode ter mais de uma decisão. Registre também quantos `y=1` há por mês. Se todas as decisões de junho ainda estão dentro dos 30 dias de espera, elas não são negativos prontos para avaliação. O [guia de preparação](#mu08-1) ajuda a conferir grão e cobertura, e [MU09](#mu09-3) trata disponibilidade temporal em junções.

Escolha um baseline trivial coerente. Para classificação binária, pode ser uma pontuação constante igual à taxa de evento do treino ou uma regra já usada, como ordenar pela recência de interação disponível na data da decisão. A regra deve ser calculada só com informação que um operador teria naquele dia. Se a taxa do treino é 20%, prever `0.20` para todos pode servir como referência de erro probabilístico, mas não discrimina positivos de negativos. Se há uma regra de triagem antiga, compare-a na mesma população e no mesmo período, sem aproveitar um corte mais favorável para o novo modelo.

Defina antes da escolha a **métrica principal** e as restrições. AUC mede ordenação de positivos acima de negativos; precisão num volume de revisão fixo pode ser mais próxima da operação; Brier e calibração importam se o score será interpretado como probabilidade. Uma equipe que só pode investigar dez casos por semana precisa olhar os dez maiores scores e os falsos alarmes, não apenas AUC. Registre custo aproximado de perder uma resposta e de investigar um caso inútil. Nenhum threshold de template vira regra de negócio apenas por constar no Hub. Se a resposta é uma quantidade contínua, mude para MAE/RMSE; se é ordem de ofertas por entidade, NDCG dentro de grupos, e assim por diante. A família vem depois da pergunta.

Antes de treinar, abra um quadro de experimento com: identificador da base e data de corte, definição de `y`, lista de exclusões, instante de disponibilidade de cada feature, período de treino/validação/teste, baseline trivial, métrica primária e guardrails, owner da revisão e orçamento de compute. Se algum item está desconhecido, resolva ou marque como lacuna explícita. O propósito desse quadro é impedir que a função de treino produza um número aparentemente preciso para uma pergunta diferente da desejada. O [contrato técnico de treino](MANUAL_TECNICO_V2.md#mt09-1) detalha por que os wrappers não corrigem esse desenho.

Escreva também o que será feito se o baseline não melhorar a regra trivial. Pode ser sinal de que os atributos ainda não estavam disponíveis no momento certo, de que a definição do alvo não condiz com a decisão ou de que a regra antiga já captura boa parte do sinal. A resposta não é obrigatoriamente testar um modelo mais complexo. Para revisão, entregue um exemplo de linha com data de decisão, atributos permitidos e data em que o alvo ficou observável, removendo qualquer informação sensível. Esse exemplo dá ao leitor um teste concreto da definição, anterior a qualquer métrica.

<a id="mu11-2"></a>
#### 2. Como preparar a base e escolher uma família compatível?

Para uma decisão tomada em janeiro, use somente atributos disponíveis até essa data. Uma coluna `interacoes_ate_decisao` pode contar contatos anteriores; uma coluna `resposta_30d` só serve como alvo depois da maturação, nunca como feature. A tabela deve ter grão estável: se a entidade tem três ofertas no mesmo dia, decida se cada oferta é uma linha ou se haverá uma linha única da decisão. Conferir joins por chave e instante evita que uma linha de resultado posterior amplie o conjunto de features. [MU09](#mu09-2) traz a conferência de cobertura e expansão da junção; [MU10](#mu10-2) ajuda a especificar a feature e seu instante de validade.

Separe treino, validação e teste antes de transformar dados. Se o uso será no futuro, uma sequência ilustrativa é treino em janeiro–março, validação em abril e teste em maio, desde que todos os alvos estejam maduros. Se a janela de resposta atravessa a fronteira, inclua um gap temporal real ou redesenhe cortes. Se a mesma entidade aparece nos três conjuntos, decida se isso representa o uso real; quando a pergunta exige entidades inéditas, agrupe a partição para impedir cruzamento. Use `split_temporal` ou `walk_forward_cv` segundo o desenho descrito em [MU10](#mu10-2) e [MT08](MANUAL_TECNICO_V2.md#mt08-2), mas confira seus retornos e descartes. Não chame um split aleatório de validação futura.

Ajuste imputação de ausentes, padronização, binning, codificação de categorias e seleção de atributos **apenas no treino**. Imputação preenche ausentes segundo uma regra aprendida; binning transforma valores em faixas; encoding representa categorias numericamente. Depois aplique as mesmas regras congeladas à validação e ao teste. Se a média de uma coluna foi calculada com as linhas de maio antes da divisão, informação do teste entrou na preparação, mesmo sem copiar `y`. Se uma categoria nova aparece no teste, registre a política de desconhecidos; não refaça o vocabulário usando o teste. Preserve lista e ordem das colunas, além dos transformadores, para a inferência posterior.

O mapa de suites da skill `hub-ml-baseline-ml` organiza a escolha. **B1 tabular** compara regra trivial com modelo linear/árvore simples e, se fizer sentido, LightGBM, XGBoost ou CatBoost para classificação/regressão. **B1 scorecard** privilegia regressão logística e pontos transparentes; WOE pode ser diagnóstico, não aprovação. **B2 temporal** começa com previsão ingênua ou sazonal ingênua e compara ARIMA/Prophet com backtest. **B3 deep learning** testa TabNet ou MLP só com hipótese e orçamento que justifiquem seu custo diante de B1. **B4 clustering** procura grupos sem `y`, verifica estabilidade e perfil; **B5 ranking** ordena alternativas dentro de grupos com regra simples e ranker; **B6 survival** modela tempo até evento com censura; **B7 anomalia** prioriza casos sem rótulo confiável. Escolha uma suite explicitamente e anote por que as outras não respondem à pergunta atual.

Uma tabela rápida evita trocar ferramenta pela tarefa:

| Pergunta principal | Primeiro comparador | Objetos do Hub que podem entrar depois | Evidência exigida |
|---|---|---|---|
| Evento 0/1 ou quantidade | Constante, regra ou linear | `train_lgbm`, `train_xgboost`, `train_catboost`, `optuna_lgbm` | Teste separado, métrica com unidade |
| Série no tempo | Último valor ou sazonal ingênuo | `arima_wrapper`, `prophet_wrapper`, `walk_forward` | Erro fora da amostra por horizonte |
| Ofertas por entidade | Regra de ordem | `lgbm_ranker` | Grupos contíguos e NDCG@k |
| Segmentos sem rótulo | Regra de grupos simples | `clustering_suite`, `cluster_profiling`, `umap_viz` | Estabilidade, perfil e utilidade |
| Casos incomuns | Regra robusta de revisão | `isolation_forest`, `autoencoder_anomaly` | Fila investigada, sem chamar alerta de fraude |

O quadro é um roteiro de seleção, não uma afirmação de que todos os objetos executam no mesmo ambiente. Os wrappers de ML citados em [MT09](MANUAL_TECNICO_V2.md#mt09-2) usam dados locais pandas/NumPy ou PyTorch; se os dados brutos estão em Spark, faça filtros e agregações distribuídas e **estime o tamanho** antes de converter a amostra ao driver. Uma contagem enorme convertida diretamente com `toPandas()` pode esgotar memória. Registre critério da amostra e seed. Verifique no compute as bibliotecas necessárias: LightGBM/XGBoost/CatBoost, scikit-learn, MLflow quando o logging estiver ativo, ou PyTorch/Prophet conforme a suite. Ler o README não instala pacotes, mas vários notebooks de exemplo contêm células `%pip` e reinício de Python. Examine esses efeitos antes de executar; o exemplo não autoriza instalação nem destino remoto.

Uma forma prática de conferir o corte é montar uma tabela pequena por período com colunas `n_decisoes`, `n_entidades`, `n_eventos_maduros` e `n_sem_alvo_maduro`. Se abril tem 200 decisões, mas somente 120 com janela de resposta fechada, a validação não deve tratar as 80 restantes como negativos. Se maio contém metade das entidades já vistas no treino, anote se o caso de uso prevê as mesmas entidades ou entidades inéditas. Se uma regra de exclusão elimina quase todos os casos de um canal, a métrica estimará o desempenho na população restante; não extrapole silenciosamente para o canal ausente. Esses números também orientam se há eventos suficientes em cada parte para AUC ou se será necessário outro desenho.

Para features, registre uma ficha simples por coluna: nome, fonte, grão original, instante de observação, instante de publicação, janela de cálculo, tratamento de ausentes e transformação aplicada. `interacoes_ate_decisao` pode usar eventos anteriores, mas uma carga noturna publicada depois da decisão talvez só esteja disponível no dia seguinte. Valide pelo relógio de publicação, não apenas pela data do evento. Faça uma amostra de linhas na fronteira do corte e tente explicar manualmente por que cada valor era conhecido naquele instante. Se a explicação depende do resultado futuro, a coluna não entra. O mesmo controle vale para estatísticas globais, como frequência de categoria, aprendidas apenas no treino.

Quando os dados cabem no driver, `X_train` e `X_val` podem ser matrizes NumPy ou DataFrames pandas conforme o wrapper; preserve índices/IDs num objeto paralelo para auditar a correspondência com `y`. Converter não significa descartar a origem: guarde versão da consulta, filtros e semente da amostra. Para modelos de árvores, categorias e valores ausentes têm tratamentos distintos nas bibliotecas; a existência de um parâmetro `cat_features` no CatBoost não significa que a mesma matriz textual funcionará no LightGBM ou no XGBoost. Se planeja compará-los, defina uma representação consistente ou documente explicitamente as diferenças de pré-processamento para que a comparação não misture algoritmo e entrada.

<a id="uso-hub-ml-baseline-ml"></a>
##### Ficha de uso — hub-ml-baseline-ml

<!-- usage-card:start hub-ml-baseline-ml -->
Escolha baseline quando precisa de uma referência reproduzível para comparar modelos ou uma regra existente. Informe decisão, unidade, alvo, horizonte, população, exclusões, instante de disponibilidade, períodos de treino, validação e teste, métrica principal, restrições e orçamento. Escolha a suite pelo problema: classificação, série, ranking e agrupamento exigem desenhos distintos. Se os rótulos ainda não amadureceram, registre a lacuna antes de chamar o conjunto de teste válido.

O pedido abaixo solicita um plano antes do treino. A entrega esperada reúne comparador trivial, preparação, splits, dependências, treinamento proposto, critérios, tracking e handoff. Depois da execução autorizada, acrescente modelo, métricas realmente calculadas, população avaliada e limitações. Confira que transformações foram ajustadas só no treino, IDs e alvos permaneceram alinhados e o teste não participou da seleção. Exija comparação nas mesmas linhas e unidade adequada para cada métrica. A skill está em L0/audit na policy vigente; templates não treinam nem promovem modelos. Se um wrapper registrar apenas parâmetros e métricas, complete o registro conforme o contrato do projeto. Tracking não autoriza promoção nem alteração de alias.

```text
@hub-ml-baseline-ml
Planeje um baseline [SUITE] para [DECISÃO/UNIDADE/ALVO/HORIZONTE].
População, disponibilidade e splits: [DEFINIÇÕES OU LACUNAS].
Régua trivial, métrica, restrições e orçamento: [CONTEXTO].
Não treine nem registre nesta etapa. Entregue preparação, comparação,
dependências, critérios de revisão e plano de tracking.
Separe proposta, execução autorizada e promoção.
```
<!-- usage-card:end hub-ml-baseline-ml -->

<a id="mu11-3"></a>
#### 3. Como pedir a skill e chamar um helper sem perder o controle do treino?

Se você quer assistência na escolha, invoque `hub-ml-baseline-ml` com um briefing concreto: “Construa um baseline B1 binário para resposta em 30 dias, uma linha por decisão de contato, treino janeiro–março, validação abril e teste maio após maturação; compare regra de recência com modelo simples, métrica principal AUC e precisão no top dez; liste exclusões, features disponíveis, dependências, custos e limites antes de executar”. Esse texto orienta a skill, mas não substitui acesso à tabela, compute, permissão para registrar runs ou revisão humana. A skill contém `suite_selection_guide.md`, `split_strategy.md`, templates de métricas e `mlflow_checklist.md` para organizar a saída. Preencha cada campo com sua fonte real; valores exemplificativos dos templates não são thresholds institucionais.

A [rota integrada da skill](skills/hub-ml-baseline-ml/scripts/README.md) oferece `BINARY_TEMPORAL_LOCAL_V1`: fixture sintética com pelo menos 12 meses, partições 50/25/25, gap zero, feature numérica única e regressão logística ajustada no treino. `run.py` calcula em memória, sem MLflow; `verify.py::verify` refaz partições, fit e métricas a partir de request/run_id externos. O perfil não executa todas as suites B1–B7 nem promove a policy L0/audit. A receita LightGBM abaixo é outra chamada direta, não esse runner.

Para usar só um snippet, importe a função do módulo correspondente de `hub_snippets.ml` em um ambiente Python onde o pacote e as dependências estejam acessíveis. Uma chamada ilustrativa válida tem a forma `model, metrics = train_lightgbm_baseline(X_train, y_train, X_val, y_val, task='binary', log_mlflow=False)`. `X_train` e `X_val` devem ter as mesmas colunas na mesma ordem, e cada vetor `y` deve corresponder às linhas da matriz do mesmo nome. `log_mlflow=False` evita somente o registro explícito do wrapper, sem desligar autologging já configurado na sessão; não transforma o retorno em um run governado. A função devolve modelo ajustado e dicionário de métricas de treino/validação; leia as chaves efetivas para a tarefa escolhida. Ela não divide seus dados nem cria um teste final.

Para tornar a rota concreta, o exemplo sintético abaixo cria 20 decisões ordenadas `D00` a `D19`, com duas features numéricas disponíveis no instante da decisão e rótulos já maduros. As primeiras 12 linhas são treino, quatro seguintes validação e as últimas quatro ficam reservadas como teste. A taxa de evento do treino é `6/12=0,5`; uma régua trivial prevê esse mesmo valor para toda a validação. Como a validação contém dois positivos e dois negativos, o Brier da régua é `0,25`: cada uma das quatro diferenças quadráticas vale `0,25`. O candidato é treinado apenas com as primeiras 12 linhas e comparado nas mesmas quatro de validação. O código é uma receita para um ambiente preparado, não um relato de execução.

```python
import numpy as np
from hub_snippets.ml.train_lgbm import train_lightgbm_baseline
from hub_snippets.ml.metrics_report import calculate_binary_metrics

ids = [f"D{i:02d}" for i in range(20)]
X = np.column_stack([np.arange(20) + 30, np.arange(20) % 3]).astype(float)
y = np.arange(20) % 2
X_train, y_train = X[:12], y[:12]
X_val, y_val = X[12:16], y[12:16]
X_test, y_test = X[16:], y[16:]  # reservado; não entra na escolha

baseline_prob = np.full(len(y_val), y_train.mean())
baseline = calculate_binary_metrics(y_val, baseline_prob)
model, treino = train_lightgbm_baseline(
    X_train, y_train, X_val, y_val,
    task="binary", early_stopping_rounds=0, log_mlflow=False,
)
prob_val = model.predict_proba(X_val)[:, 1]
candidato = calculate_binary_metrics(y_val, prob_val)
print(ids[12:16], baseline["brier_score"], candidato["brier_score"], treino["auc_val"])
```

Ao ler a saída, confira que `ids[12:16]` nomeia exatamente as quatro linhas avaliadas. `baseline["brier_score"]` deve representar o `0,25` calculado à mão; `candidato["brier_score"]` e `treino["auc_val"]` dependem do ajuste real e não recebem valores inventados aqui. `early_stopping_rounds=0` desativa a parada antecipada nesse conjunto minúsculo, mas não torna sua estimativa estável. Para trabalho real, use volume e período adequados, guarde transformadores e só abra `X_test` depois de selecionar a configuração. Se faltar LightGBM ou os imports do Hub, resolva a dependência e o caminho do pacote antes de usar a receita.

Em um exemplo de quatro decisões de validação com rótulos `[1,0,1,0]`, qualquer AUC numérica dependerá dos scores que o modelo realmente produzir. O retorno `metrics['auc_val']`, se existir nessa tarefa, deve ser interpretado como ordenação **nessas quatro linhas**, não como acurácia nem garantia futura. Não invente um valor de AUC no relatório antes de rodar e verificar a população. Uma chamada com `X_val` contendo uma coluna futura, ou com `y_val` reordenado sem reordenar `X_val`, pode gerar número enganoso mesmo que as dimensões coincidam. Corrija as matrizes, não a métrica. Se a validação contém só uma classe, a função ou o cálculo de AUC pode falhar; a ação é rever tamanho, maturação e corte da amostra, não preencher o resultado com zero.

Treine primeiro a régua trivial e o modelo simples sobre exatamente as mesmas linhas. Só depois compare um wrapper de boosting. Use `params_override` com escolhas registradas quando houver razão, não uma busca cega. `optimize_lgbm` usa a validação repetidamente e devolve `best_params` e `study`, não um modelo final; reserve o teste para depois da seleção. Quando for série, `train_arima` e `train_prophet` devolvem forecast e métricas **in-sample**, portanto organize backtest antes de reportar “melhor previsão”. Quando for ranking, `groups_train` contém tamanhos de blocos contíguos; seis ofertas de dois clientes com três cada pedem `[3,3]`, não seis identificadores. A leitura técnica de cada retorno está em [MT09](MANUAL_TECNICO_V2.md#mt09-2).

Para clustering/anomalia, substitua a ideia de “acerto” por verificação apropriada. `run_clustering_pipeline` devolve labels, modelo, scaler e métricas internas; `profile_clusters` ajuda a ver diferenças descritivas. `train_isolation_forest` devolve scores e labels para priorização; `train_autoencoder_anomaly` usa uma referência declarada normal e devolve limiar e erros de reconstrução. Nenhum dos dois confirma fraude. Para survival, use `kaplan_meier` e `survival_cox` apenas com duração, evento e censura definidos; para deep learning, compare TabNet/MLP com B1 no mesmo split e registre o custo. Essas alternativas estão no índice da categoria [ML](hub_snippets/ml/README.md), e seus limites técnicos aparecem em [MT08](MANUAL_TECNICO_V2.md#mt08-4) e [MT09](MANUAL_TECNICO_V2.md#mt09-3).

Antes de rodar, faça uma conferência final: counts por split, classes por split, datas máximas das features, ordem das colunas, transformação ajustada só no treino, memória estimada do driver, dependências disponíveis e destino de qualquer logging. Se um item falhar, documente a correção e refaça a preparação. Uma execução que termina sem erro prova apenas que o código aceitou aquela entrada; a comparação justa depende dessas condições externas. O próximo passo é interpretar os números junto com limitação e registro.

Se você optar por `log_mlflow=True`, confira antes se existe um run ativo adequado e quais parâmetros/métricas o wrapper registra. Alguns módulos apenas chamam `mlflow.log_params` e `mlflow.log_metrics`; isso não produz automaticamente dataset, split, assinatura e limitações. O helper `run_governado` pode exigir esses elementos para modelos compatíveis com o flavor sklearn, como detalhado em [MT10](MANUAL_TECNICO_V2.md#mt10-3), mas tem efeito persistente no backend. Para um ensaio local de API, `log_mlflow=False` isola o exemplo do registro opcional; confira também autologging da sessão; para trabalho real, combine um plano de tracking com o owner do experimento e não suponha que “treino concluído” significa run completo.

Um erro de dependência também tem tratamento específico. Se `lightgbm` não está disponível, confirme a biblioteca instalada no compute e a versão prevista pelo projeto; se MLflow falta com logging habilitado, desabilitar o registro só serve para um ensaio que não precisa dele, não para uma entrega cujo contrato exige rastreabilidade. Se o modelo recebe uma categoria fora do domínio codificado ou as matrizes têm colunas em ordens diferentes, corrija a preparação e rode a conferência novamente. Não recodifique categorias com base no teste para fazê-lo “passar”: isso muda a pergunta e pode contaminar a avaliação.

O notebook deve mostrar os nomes das funções chamadas e o estado de cada etapa: dados prontos, split conferido, baseline trivial medido, candidato treinado e avaliação pendente ou concluída. Se uma etapa foi apenas planejada, escreva “não executada” em vez de apresentar o formato de retorno como resultado observado. Esse cuidado permite a quem revisa distinguir uma receita reproduzível de uma evidência de desempenho, especialmente quando o trabalho foi dividido entre conversas ou sessões diferentes.

<!-- editorial:exclude:start -->
**Fontes:** [skill de baseline](skills/hub-ml-baseline-ml/SKILL.md), [guia de suites](skills/hub-ml-baseline-ml/templates/suite_selection_guide.md), [split](skills/hub-ml-baseline-ml/templates/split_strategy.md), [LightGBM](hub_snippets/ml/train_lgbm/train_lgbm.py), [Optuna](hub_snippets/ml/optuna_lgbm/optuna_lgbm.py) e [índice ML](hub_snippets/ml/README.md).
<!-- editorial:exclude:end -->

<a id="mu11-4"></a>
#### 4. Como ler métricas, registrar o run e decidir o próximo passo?

Compare primeiro na mesma tabela o baseline trivial, o modelo simples e o candidato mais complexo. Para cada linha, informe período, população, número de decisões e eventos, métrica principal, unidade, custo de treino e limitações. Em classificação, inclua AUC de ordenação, precisão e recall no limiar ou volume que a operação suporta, e medida de calibração quando o score for chamado de probabilidade. AUC de 0,80 não significa 80% de decisões corretas. Se o objetivo era revisar dez casos, mostre quantos eventos apareceram nos dez maiores scores e quantos falsos alertas exigiram trabalho. Para regressão, MAE mede erro absoluto médio na unidade do alvo e RMSE penaliza mais os erros grandes; para série, reporte erro **fora** da amostra por horizonte; para ranking, NDCG por grupo. O [capítulo de métricas](MANUAL_TECNICO_V2.md#mt10-1) explica os denominadores.

Leia o dicionário retornado antes de copiar números. `metrics_report.calculate_binary_metrics(y_true,y_prob,threshold=0.5)` devolve `auc_roc`, `ks_pct`, `gini`, `auc_pr`, `brier_score`, `precision`, `recall` e outras chaves para vetores com as duas classes; `ks_pct` é em pontos percentuais. `calculate_regression_metrics` devolve `rmse`, `mae`, `mape` e `r2`, mas MAPE fica indefinido quando todos os valores reais são zero. O wrapper `train_lightgbm_baseline` tem seu próprio dicionário de treino/validação, como `auc_val` em binária; não misture essas chaves com métricas de um teste separado sem nomear a população. Se a figura de KS e `ks_pct` divergirem, o código usa definições distintas, não somente escalas. Confira [MT10](MANUAL_TECNICO_V2.md#mt10-2) antes de copiar um threshold de uma saída para outra.

Um exemplo de leitura ilustrativo: baseline trivial com AUC 0,50 e candidato com AUC 0,74 em validação, mas precisão igual no top dez, não sustenta afirmar que o candidato melhora a rotina de dez investigações. AUC e precisão respondem a perguntas diferentes. Esses valores são hipotéticos; não foram produzidos pelo Hub. A conclusão provisória seria investigar distribuição de scores, custo de falsos alertas e estabilidade em outro período. Se o teste reservado mostra queda importante, volte às diferenças de população e ao desenho de features antes de ajustar mais parâmetros. Não use o teste repetidamente para escolher a próxima versão, pois ele passaria a funcionar como validação.

No registro, anote parâmetros, versão de código e dependências, identidade e recorte dos dados, split, métricas, limitações e artefatos seguros. A skill traz `mlflow_checklist.md`, `notebook_output_baseline.md` e `relatorio_executivo_baseline.md` para organizar a entrega. `run_governado` abre um contexto MLflow com tags de dataset, split e limitações; criação ou retomada do run depende da configuração vigente. O helper não isola backend nem solicita run aninhado, e cobra parâmetros, métricas e exemplo de entrada do modelo sklearn após a saída normal do bloco `with`. Se você usá-lo, confirme backend, experimento e run ativo antes de executar; chamadas podem gravar artefatos persistentemente, e uma falha de completude no fechamento não desfaz registros anteriores. Uma exceção dentro do corpo pula a checagem posterior de completude. Não grave dados pessoais em exemplos ou artifacts de tracking. O [ADR-0016](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0016-mlflow-runs-micromodelos.md) separa histórico operacional de definição, e um run completo não é aprovação para publicar modelo. Veja o [contrato de runs em MT10](MANUAL_TECNICO_V2.md#mt10-3).

O adapter `run_tracking.py` é uma rota separada: exige autorização `SER10-AUTH-1`, backend/identidade conferidos e destino pessoal novo. Cria experimento/run/modelo, verifica o modelo enquanto ativo e faz soft delete dos IDs próprios. `verify_finalized` confere a evidência e o estado deletado, sem reler o modelo após exclusão. `UNKNOWN_RESIDUE` exige inspeção, não retry automático; soft delete não é apagamento físico.

Escolha o próximo passo explicitamente. Se o candidato não supera a régua trivial no critério principal ou viola guardrail, documente-o e revise alvo, janela, features e representatividade; talvez a tarefa de modelagem precise ser reformulada. Se melhora, valide em teste intocado e por períodos ou segmentos relevantes, quantifique incerteza quando ela muda a decisão e prepare [explicabilidade e acompanhamento](#mu12-1). Se uma solução de deep learning custa muito mais sem ganho material, registre a comparação e prefira a opção mais simples. Para clustering e anomalias, a decisão seguinte costuma ser revisão de casos/estabilidade, não promoção de um classificador sem rótulos.

Entregue a outra pessoa um pacote mínimo conferível: pergunta de decisão; população e exclusões; datas de treino, validação e teste; inventário de features e disponibilidade; baseline trivial; funções e parâmetros usados; métricas com unidade e denominador; erros conhecidos; run ou plano de registro; e decisão proposta com quem deve revisá-la. Essa lista vale mesmo que a execução tenha falhado: registre a falha, sua causa conhecida e a alternativa tentada. A ausência de evidência é um resultado a comunicar, não um motivo para preencher métricas. Treinar um modelo cria um candidato técnico; publicação, promoção e uso institucional exigem outras verificações e autoridade.

<!-- editorial:exclude:start -->
**Fontes:** [skill baseline](skills/hub-ml-baseline-ml/SKILL.md), [template de métricas](skills/hub-ml-baseline-ml/templates/metricas_classificacao.md), [checklist MLflow](skills/hub-ml-baseline-ml/templates/mlflow_checklist.md), [saída de notebook](skills/hub-ml-baseline-ml/templates/notebook_output_baseline.md), [métricas](hub_snippets/ml/metrics_report/metrics_report.py), [run governado](hub_snippets/ml/mlflow_run/mlflow_run.py) e [ADR-0016](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0016-mlflow-runs-micromodelos.md). [Índice](#sumario-mu).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU10](#mu10) · [Próximo: MU12](#mu12) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT09](MANUAL_TECNICO_V2.md#mt09) · [MT10](MANUAL_TECNICO_V2.md#mt10)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu12"></a>
<a id="mu12"></a>
### MU12 — Explicar resultados e acompanhar modelos

<!-- editorial:exclude:start -->
**Você quer:** entender uma predição, comunicar seus limites ou investigar mudança depois do treino. **Rota:** escolha a pergunta (1), fixe modelo, amostra e referência (2), chame apenas os helpers adequados (3); a última seção transforma sinais em uma ação revisada (4). Todos os números são ilustrativos; nenhuma execução de modelo, run ou monitor remoto foi realizada. [Índice do manual](#sumario-mu).
<!-- editorial:exclude:end -->

<a id="mu12-1"></a>
#### 1. Preciso explicar uma predição ou acompanhar uma mudança?

“Por que `E001` recebeu esse score?” e “o modelo piorou em setembro?” são perguntas diferentes. A primeira pede **explicabilidade local**: qual saída do modelo está sendo decomposta, comparada com qual referência, para uma linha específica. “Quais atributos mais influenciam a carteira?” pede explicabilidade **global** numa população definida. “A distribuição de idade da conta mudou?” pede **drift de dados**, comparação entre referência e período atual. “A AUC (área sob a curva ROC (característica de operação do receptor), medida de discriminação entre classes) caiu?” pede **performance**, que só pode ser medida quando rótulos verdadeiros já amadureceram. Um relatório pode juntar as quatro, mas deve preservar seus denominadores e tempos.

Se você tem um modelo recém-treinado e quer compreender seus resultados, comece pelo conjunto de validação/teste, pelas métricas e por exemplos representativos de acerto, erro e fronteira. Use `hub-ml-explainability` para orientar método, classe, escala e camadas de comunicação. Se o modelo está em uso ou prestes a entrar e você quer acompanhar seu comportamento, use `hub-ml-monitoramento-modelo` para desenhar referência, frequência, atraso do alvo, política, owner e resposta. As skills são instruções e templates de trabalho, não um agendador nem um monitor implantado automaticamente. Um pedido claro menciona o objetivo e a evidência disponível: “explique a classe positiva do modelo versão V em decisões de maio” ou “compare o score de setembro com referência de junho e avalie performance só nas decisões cujo alvo de 30 dias fechou”.

Há uma sequência útil de perguntas. O score mudou porque a população de entrada mudou? O dado chegou com outra cobertura ou muitos ausentes? O próprio mapeamento entre score e evento mudou? Houve degradação em todos os segmentos ou só em um canal? Sem resposta observada, você pode relatar drift e qualidade de dados, mas não concluir que a AUC caiu. Com resposta observada, ainda verifique se foi medida na mesma definição de alvo e na mesma população. PSI (índice de estabilidade populacional para variável numérica), KS (estatística de Kolmogorov–Smirnov entre distribuições) e CSI (índice de estabilidade de categorias) comparam distribuições por mecanismos diferentes; veja a [leitura técnica](MANUAL_TECNICO_V2.md#mt10-4). Um alerta desses índices é sinal de investigação, não prova de dano ou ordem de retreino.

Para comunicar a alguém não técnico, comece com a decisão que o resultado afeta: quantos casos seriam revisados, qual é o custo dos erros e qual período foi observado. Depois apresente a medida e o limite. “Atributo X liderou a importância SHAP (SHapley Additive exPlanations, atribuições aditivas da saída prevista) na amostra de maio” é uma descrição da saída do modelo; “X causou o evento” não decorre dela. “A AUC caiu quatro centésimos” pode merecer investigação, mas não define sozinha a resposta. O [capítulo técnico](MANUAL_TECNICO_V2.md#mt10-1) separa discriminação, calibração, decisão e tracking; [MU11](#mu11-4) ensina a guardar um baseline antes de monitorar.

Escolha uma pergunta por painel ou parágrafo. Se o assunto é mudança de distribuição, mostre referência, período atual, volumes, missing e índice de estabilidade. Se é desempenho, mostre apenas a coorte com resultado conhecido, sua definição e métrica com unidade. Se é explicação, diga se ela é global ou local e qual versão do modelo gerou os scores. Esse enquadramento evita que um gráfico de SHAP seja lido como prova de melhora, ou que um alerta de entrada seja apresentado como queda de AUC. Uma mesma investigação pode chegar às três análises em sequência, mas cada conclusão deve apontar para sua própria evidência.

<a id="uso-hub-ml-explainability"></a>
##### Ficha de uso — hub-ml-explainability

<!-- usage-card:start hub-ml-explainability -->
Escolha explainability para compreender a saída de um modelo treinado, globalmente ou em casos identificados. Informe modelo e versão, população, período, preparação, classe, escala da saída, amostra, IDs e orçamento. Preserve a ordem entre linhas e identificadores; para Kernel, selecione externamente os casos quando precisar rastreá-los.

O pedido abaixo solicita método antes do cálculo. A entrega esperada reúne explicação técnica, gráficos, ranking, exemplos locais, tradução executiva, limites e próximos testes. Confira conjunto, classe, escala, background quando aplicável e correspondência de cada caso com o score explicado. SHAP atribui partes da saída do modelo; não demonstra causas do evento. Uma contribuição em log-odds não é uma porcentagem. A policy vigente mantém a skill em L0/audit: o texto não comprova execução nem publica gráficos. Confirme dependências e destino antes de autorizar cálculos ou salvamento. Se a classe ou a escala faltar, resolva essa informação antes de interpretar contribuições; mantenha o resultado condicionado enquanto isso.

```text
@hub-ml-explainability
Planeje explicar [MODELO/VERSÃO], conjunto [POPULAÇÃO/PERÍODO].
Classe, escala, preparação e IDs: [DEFINIÇÕES OU LACUNAS].
Amostra e orçamento: [LIMITES]. Não calcule nem salve nesta etapa.
Proponha método, controles de correspondência, entregas técnica e executiva,
limitações e próximos testes, sem atribuir causalidade ao SHAP.
```
<!-- usage-card:end hub-ml-explainability -->

<a id="mu12-2"></a>
#### 2. Que modelo, população, período e referência devo informar?

Anote versão do modelo e do pipeline de preparação, lista ordenada de colunas, alvo, classe positiva e **escala da saída**: probabilidade, margem, log-odds ou valor previsto. Log-odds é o logaritmo da razão entre chance de evento e de não evento; não se lê diretamente como porcentagem. Um SHAP de `+0.2` nessa escala não significa “20 pontos percentuais de risco”. Para uma decisão fictícia `E001` em 15/01, identifique o score produzido naquele dia e os atributos que o modelo recebeu. Se o notebook recalcular a linha com atributos atualizados em fevereiro, já estará explicando outra entrada.

Escolha a amostra que representa a pergunta. Para explicação global do desempenho de maio, use decisões de maio avaliáveis, com o mesmo pré-processamento da inferência e IDs guardados. Para explicação local, preserve a correspondência entre `idx` do array, identificador e data; uma ordenação intermediária pode levar o gráfico à pessoa errada. A função `compute_shap` limita opcionalmente o caminho `kernel` por subamostragem quando `len(X)>max_samples`, mas não devolve os IDs selecionados. Se você precisa ligar atribuições a casos, selecione externamente um conjunto pequeno, preserve seus IDs na mesma ordem e passe-o já dentro do limite. Isso também permite registrar semente e critério de amostragem.

A [rota executável da skill](skills/hub-ml-explainability/scripts/README.md), `LINEAR_REGRESSION_SYNTHETIC_V1`, exige regressão linear escalar sintética e uma linha de background explícita. Request, modelo, arrays e run_id externos alimentam o verificador com oráculo analítico. Não cobre árvores, classificação, KernelSHAP ou plots, nem promove L0/audit. No helper geral, `background=` só é aceito para `model_type="linear"`; omiti-lo preserva `X` como referência linear.

Defina a **referência** conforme a medida. Para SHAP, há um valor base associado ao explicador e, no caminho Kernel, um conjunto de background que influencia a comparação. Para PSI/CSI, a distribuição de referência determina bins ou categorias e não deve ser recalculada silenciosamente com o período atual. Para monitoramento de AUC, a referência é uma métrica de baseline para uma população e janela declaradas. Uma referência de treino com idade de conta distinta da carteira atual pode gerar alerta legítimo de mudança, mas não diz se a diferença é ruim. Escreva por que a referência é relevante e quando precisará ser atualizada por revisão, não por conveniência diante de um alerta.

Uma ficha mínima para cada comparação inclui: modelo/versão, origem dos dados, período de referência, período atual, número de linhas e entidades, porcentagem de ausentes, alvo e data de maturação, segmento, método e parâmetros, limiar adotado e responsável. A coluna “alvo maduro?” deve ficar explícita. No exemplo, respostas de decisões em 25/09 com janela de 30 dias ainda não podem medir performance em 01/10. Drift de score ou de atributos pode ser calculado sem rótulo, desde que as populações sejam comparáveis; performance precisa esperar ou usar somente a coorte madura, informando a cobertura reduzida.

Antes de abrir o explicador, verifique se o modelo faz predições coerentes no conjunto escolhido e se as colunas têm a mesma ordem de treino. Um erro de schema pode gerar atribuições com nomes trocados. Para dados sensíveis, evite publicar gráficos locais identificáveis e não envie exemplos pessoais a artifacts de tracking. Para comparação periódica, reserve a tabela de métricas em camada governada com versão, janela, população e timestamp; o `PerformanceMonitor` em si guarda histórico apenas na memória do processo. Um run MLflow pode registrar gráficos e agregados seguros, mas não deve virar depósito de resultados individuais por entidade.

Se o briefing estiver incompleto, ainda é possível produzir uma lista de perguntas pendentes: “qual classe?”, “qual período?”, “qual atraso do alvo?”, “qual população base?”. Não force uma explicação colorida para preencher essa ausência. A skill de explainability pede explicitamente classe/escala e amostra; a de monitoramento pede baseline, frequência, owner e runbook. Essa disciplina protege o leitor contra duas narrativas convincentes mas falsas: importância de atributo trocada por causalidade e drift de entrada trocado por queda de performance.

Em um acompanhamento mensal, compare o mesmo **grão** de decisão. Se junho contém uma linha por entidade e setembro uma linha por contato, a diferença de distribuição pode refletir duplicação do grão, não comportamento novo. Preserve um contador de chaves únicas e de linhas por período. Registre também versões de tratamento de ausentes e de categorias: a passagem de “sem informação” para um código numérico novo pode alterar PSI sem alterar a realidade subjacente. Uma referência útil não é apenas a fotografia de uma tabela; inclui as regras que geraram suas colunas. Quando essas regras mudam, abra uma investigação de compatibilidade antes de atribuir o sinal ao modelo.

Para um caso local, evite escolher apenas o erro mais dramático. Selecione, com critério declarado, exemplos de acerto, erro e score próximo ao limiar, e compare-os com a população. Um caso extremo pode explicar uma falha específica, mas não representa a carteira toda. Para um relatório global, informe quantas linhas foram explicadas e se houve amostragem estratificada por período ou segmento. A estatística de importância média pode esconder um atributo dominante em um grupo pequeno; uma tabela por segmento ajuda a perceber essa diferença sem sugerir causalidade.

<a id="uso-hub-ml-monitoramento-modelo"></a>
##### Ficha de uso — hub-ml-monitoramento-modelo

<!-- usage-card:start hub-ml-monitoramento-modelo -->
Escolha monitoramento quando precisa acompanhar um modelo em uso ou preparar sua observação operacional. Informe versão, população, frequência, referência, alvo, atraso dos rótulos, métricas, limites justificados, responsáveis, destino e resposta a alertas. Separe disponibilidade do serviço, qualidade dos dados, mudança de distribuição e desempenho: uma mudança de entrada pode ser medida sem alvo, mas performance exige resultados conhecidos.

O pedido abaixo planeja acompanhamento, sem criar job ou alerta. A entrega esperada reúne arquitetura, contrato de métricas, comparações, política, runbook, limitações e o que depende de revisão. Depois da execução, confira períodos, volumes, denominadores, maturidade dos rótulos e direção de cada métrica. Não trate PSI como prova de queda de desempenho nem aplique limiar universal. O PerformanceMonitor mantém histórico em memória; persistência governada precisa de desenho separado. A skill atual está em L0/audit, e o helper nunca autoriza retreino. Um estado sem evidência pede resolver referência ou cobertura, não inventar degradação. Só proponha recalibração, challenger ou promoção após investigação e gates correspondentes. Registre quem decide, qual teste falta e quando repetir a avaliação.

```text
@hub-ml-monitoramento-modelo
Planeje acompanhar [MODELO/VERSÃO] em [POPULAÇÃO/FREQUÊNCIA].
Referência, alvo, atraso de rótulos e métricas: [CONTEXTO].
Limites, responsáveis, destinos e resposta: [REGRAS OU LACUNAS].
Não crie jobs, alertas ou retreino nesta etapa.
Entregue contrato, verificações, runbook e limites de evidência;
separe drift, desempenho e decisão de ação.
```
<!-- usage-card:end hub-ml-monitoramento-modelo -->

<a id="mu12-3"></a>
#### 3. Que helper uso para SHAP, relatórios, curvas, drift e desempenho?

Para um modelo de árvore compatível já validado, uma chamada de forma pública é `values, base = compute_shap(model, X_eval, feature_names, model_type='tree', task='classification', output_index=1)` **se** a biblioteca devolver várias saídas e a saída 1 for a classe positiva confirmada. Em saída 2D única, `output_index` pode ser desnecessário; inspecione o contrato e a forma obtida, sem adivinhar. `values` deve ter uma linha por caso avaliado e uma coluna por atributo; `base` é a referência na escala explicada. `get_feature_importance_shap(values, feature_names, top_n=20)` produz tabela de média absoluta e participação relativa. Esse percentual é fração da importância absoluta média na amostra, não “porcentagem de causalidade” ou de acertos. `plot_shap_global` e `plot_shap_local` geram gráficos SHAP/Matplotlib e podem salvar arquivo com `save_path`; o tema Plotly do Hub não recolore automaticamente esses plots.

Uma receita para um modelo de árvore **já validado** exige que o notebook tenha `modelo_validado`, `X_casos_validos`, `ids_casos_validos`, `colunas_treino`, `classe_indice_confirmado` e `escala_saida_confirmada` vindos da mesma versão e ordem. Confirme que índice 1 representa a classe positiva; a escala do `TreeExplainer` padrão é a saída *raw* do modelo, que pode ser margem/log-odds, conforme a [documentação SHAP](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html), reconferida em 7/10/2026. Configure `saida_autorizada` como diretório local aprovado antes de salvar gráficos; os helpers salvam e fecham figuras Matplotlib e não retornam `Figure`.

```python
from pathlib import Path
import numpy as np
from hub_snippets.ml.shap_explainer import (
    compute_shap, get_feature_importance_shap,
    plot_shap_global, plot_shap_local,
)

X_eval = np.asarray(X_casos_validos, dtype=float)
ids_eval = list(ids_casos_validos)
feature_names = list(colunas_treino)
assert X_eval.ndim == 2 and X_eval.shape[1] == len(feature_names)
assert len(ids_eval) == len(X_eval) and len(set(ids_eval)) == len(ids_eval)
assert classe_indice_confirmado == 1 and escala_saida_confirmada
saida = Path(saida_autorizada)
assert saida.is_dir()  # diretório aprovado antes desta receita
values, base = compute_shap(
    modelo_validado, X_eval, feature_names,
    model_type="tree", task="classification", output_index=1,
)
assert values.shape == X_eval.shape
ranking = get_feature_importance_shap(values, feature_names)
idx = ids_eval.index("E001")
plot_shap_global(values, X_eval, feature_names,
                 save_path=str(saida / "shap_global.png"))
plot_shap_local(values, base, X_eval, feature_names, idx,
                save_path=str(saida / "shap_E001.png"))
print(ranking.head(), base, ids_eval[idx])
```

O retorno contém matriz de atribuições, base e ranking; dois arquivos surgem no destino autorizado. Se o modelo não for compatível, a classe não estiver mapeada ou a escala não tiver sido confirmada, interrompa a receita e resolva esses pré-requisitos.
Um exemplo interpretado sem inventar execução: se a saída explicada tem base `0.30`, atribuições `+0.10` e `−0.05` na mesma escala, a soma é `0.35`. Essa conta só explica a regra aditiva; não garante que o modelo real use escala de probabilidade. Se for log-odds, 0.35 não representa 35%. Para explicar `E001`, selecione o índice correspondente em `X_eval`, confira o vetor de atributos e o score do modelo antes de gerar o waterfall local. Se `compute_shap` rejeitar saída multiclasse sem `output_index`, informe a classe correta; não achate o array para fazer o erro desaparecer.

`generate_executive_report(shap_importance,feature_business_names,target_description,model_metric,metric_name='AUC',...)` transforma uma tabela de importância já calculada em Markdown para leitores de negócio. `generate_technical_summary(shap_importance,native_importance=None)` cria resumo técnico e pode comparar rankings. O relatório não calcula SHAP nem demonstra causa. Comparar rankings exige `feature` e `rank` únicos em ambos os lados; confira a interseção, pois duplicatas multiplicam pares. Use [template executivo](skills/hub-ml-explainability/templates/relatorio_executivo_explainability.md) e [template técnico](skills/hub-ml-explainability/templates/shap_analysis_technical.md) para acrescentar população, classe, escala, amostra, período e limitações; substitua o texto de exemplo por evidência do seu estudo. Uma direção inferida por correlação entre feature e SHAP é descritiva e pode mudar com a amostra.

Para desempenho binário, ROC (curva de sensibilidade contra taxa de falsos positivos) ajuda a ver a discriminação ao variar o limiar; [MT10](MANUAL_TECNICO_V2.md#mt10-2) desenvolve sua interpretação. `calculate_binary_metrics(y_true,y_prob,threshold=0.5)` exige rótulos 0/1 com ambas as classes e probabilidades finitas entre 0 e 1; retorna AUC, KS em pontos percentuais, Gini, Brier, precision, recall, lift e prevalência. Use `plot_roc_curve`, `plot_pr_curve`, `plot_lift_curve` e `plot_ks_curve` para visualizar aspectos distintos; variantes `_resolvido` aplicam tema visual, sem mudar os dados. Atenção: `ks_pct` do relatório e a curva KS têm fórmulas diferentes além da unidade, conforme [MT10](MANUAL_TECNICO_V2.md#mt10-2). A figura não escolhe limiar ou capacidade de revisão. Compare curvas apenas com classe, população e maturação equivalentes. A precisão pode variar com a prevalência mesmo mantendo a revocação; ROC não escolhe capacidade operacional. Com pouco volume, registre incerteza. Em regressão, `calculate_regression_metrics` fornece RMSE (raiz do erro quadrático médio, penaliza erros grandes), MAE (erro absoluto médio), MAPE (erro percentual absoluto médio; este helper exclui alvos zero e devolve NaN se todos forem zero) e R² (coeficiente de determinação, comparação com prever a média do alvo); vetores finitos devem estar alinhados. Um R² negativo indica desempenho pior que essa referência na amostra avaliada.

Para drift driver-side, `detect_drift_all_features(df_reference,df_current,feature_cols,psi_threshold=None,ks_threshold=None,min_non_null=10)` devolve DataFrame por atributo. Sem limites fornecidos, a condição é `NOT_CLASSIFIED`; para classificação, informe **ambos** `psi_threshold` e `ks_threshold` conforme política justificada, não somente um. Numéricas têm PSI e KS; categóricas usam CSI na coluna `psi` do relatório. Recuse ou remapeie a categoria real `__MISSING__`, reservada para ausência no CSI. Valores ausentes entram em baldes/categoria próprios, e a contagem mínima numérica considera observações finitas. Um exemplo de duas coortes de 12 linhas, com categoria A em oito linhas da referência e quatro da atual, mostra uma mudança descritiva de `8/12` para `4/12`; o status depende da política e do cálculo, não é automaticamente “grave”. Se `INSUFFICIENT_DATA`, aumente a amostra ou descreva a cobertura antes de classificar.

Para repetir o detector sem dados de clientes, este exemplo pequeno cria duas tabelas pandas, incluindo ausência numérica e categoria ausente. A função calcula PSI com cortes da referência e um balde de ausentes; CSI trata ausência como categoria. KS usa somente valores numéricos finitos, portanto pode ter denominador diferente do PSI. Sem política de limiares, o status esperado é `NOT_CLASSIFIED`; os valores não devem ser lidos como prova de perda de performance.

```python
import numpy as np
import pandas as pd
from hub_snippets.ml.drift_detection import detect_drift_all_features

ref_num = np.arange(12, dtype=float)
cur_num = np.arange(12, dtype=float) + 2
ref_num[2] = np.nan
cur_num[5] = np.nan
referencia = pd.DataFrame({
    "idade_conta": ref_num,
    "canal": ["A"] * 8 + ["B"] * 3 + [None],
})
atual = pd.DataFrame({
    "idade_conta": cur_num,
    "canal": ["A"] * 4 + ["B"] * 7 + [None],
})
drift = detect_drift_all_features(
    referencia, atual, ["idade_conta", "canal"], min_non_null=10,
)
print(drift[["feature", "psi", "ks_statistic", "status"]])
```
Para acompanhar métricas já maduras, `selecionar_metricas_do_relatorio` traduz `auc_roc` para `auc` e mantém `ks_pct` na unidade correta. Crie `PerformanceMonitor(baseline_metrics,policy=politica,consecutive_alert_periods=3)` com limiares calibrados para cada métrica e direção de deterioração. `add_period('2026-09',metricas,n_predictions=volume)` adiciona um período; `get_current_status()`, `generate_report()` e `plot_timeline("auc")` apresentam leitura; a timeline recebe a chave monitorada e devolve uma figura Plotly. `should_retrain()` devolve candidato de investigação quando critérios são atingidos, nunca autorização automática. A política padrão do módulo é **exemplo**; não a use como norma sem revisão. As skills de [explicação](skills/hub-ml-explainability/SKILL.md) e [monitoramento](skills/hub-ml-monitoramento-modelo/SKILL.md) orientam os métodos e templates, mas não implantam scheduler ou job.

Esta segunda receita usa rótulos e scores **sintéticos** de duas coortes já maduras. Ela calcula relatórios separados, traduz `auc_roc` para `auc`, define uma política ilustrativa e devolve texto, decisão e figura Plotly. Em dados reais, alinhe IDs, janela do alvo e versão do modelo antes da comparação.

```python
import numpy as np
from hub_snippets.ml.metrics_report import calculate_binary_metrics
from hub_snippets.ml.performance_monitor import (
    PerformanceMonitor, selecionar_metricas_do_relatorio,
)

y_base = np.array([0, 1, 0, 1, 0, 1, 0, 1])
p_base = np.array([.10, .90, .20, .80, .30, .70, .40, .60])
y_atual = np.array([0, 1, 0, 1, 0, 1, 0, 1])
p_atual = np.array([.15, .75, .35, .65, .45, .55, .60, .40])
policy = {"auc": {"warning": .03, "critical": .05,
                  "direction": "higher", "delta": "absolute"}}
base = selecionar_metricas_do_relatorio(
    calculate_binary_metrics(y_base, p_base), policy,
    metricas_obrigatorias=["auc"],
)
mes = selecionar_metricas_do_relatorio(
    calculate_binary_metrics(y_atual, p_atual), policy,
    metricas_obrigatorias=["auc"],
)
monitor = PerformanceMonitor(base, policy=policy)
monitor.add_period("2026-09", mes, n_predictions=len(y_atual))
print(monitor.generate_report())
print(monitor.should_retrain())
fig = monitor.plot_timeline("auc")  # Figure Plotly; exiba no notebook
```
Um retorno de monitor precisa ser lido com a política. Com baseline AUC 0,80, warning absoluto 0,03 e critical 0,05, uma AUC 0,76 cai 0,04 e entra em atenção. Se a regra fosse relativa, o cálculo seria `0,04/0,80=5%`, com outro significado de limite. Para RMSE, aumento costuma ser deterioração; para AUC, queda costuma ser. O módulo rejeita política que não cobre o baseline e pode marcar período incompleto quando a configuração permite ausência de parte das métricas. Sem período algum, `should_retrain()` informa `NO_EVIDENCE`; não há `automatic_retrain_authorized` nesse retorno inicial. O mesmo nome de método não elimina a obrigação de verificar a estrutura do retorno recebido.

<!-- editorial:exclude:start -->
**Fontes:** [SHAP](hub_snippets/ml/shap_explainer/shap_explainer.py), [relatório](hub_snippets/ml/explainability_report/explainability_report.py), [métricas](hub_snippets/ml/metrics_report/metrics_report.py), [curvas](hub_snippets/ml/curves_plotly/curves_plotly.py), [drift](hub_snippets/ml/drift_detection/drift_detection.py), [monitor](hub_snippets/ml/performance_monitor/performance_monitor.py) e skills citadas.
<!-- editorial:exclude:end -->

<a id="mu12-4"></a>
#### 4. Como reagir a alertas sem transformar sinal em ordem automática?

Leia primeiro o **status e sua causa**. `NOT_CLASSIFIED` no detector de drift significa que você não forneceu a dupla de limites necessária para classificar; o número calculado ainda pode ser descrito, com referência e período, mas não recebe cor de política. `INSUFFICIENT_DATA` significa amostra insuficiente segundo a regra da função; aumente cobertura ou registre que ainda não há base para aquele cálculo. Um `ALERT` ou `SEVERE` usa os thresholds que o consumidor escolheu, e sua gravidade deve ser defendida à luz da variabilidade histórica, do tamanho da população e do custo de erro. Um `OK` não prova ausência de todo problema: outros atributos, segmentos ou qualidade de dados podem ter mudado.

As [rotas sintéticas da skill](skills/hub-ml-monitoramento-modelo/scripts/README.md) distinguem `DRIFT_NUMERIC_LOCAL_V1`, sem labels, de `BINARY_MATURE_PERFORMANCE_V1`, com labels disponíveis até `evaluation_at`. Performance exige `verify`, `finalize` e `verify_finalized` com request/run_id externos; runner isolado não conclui esse escopo. Nenhuma rota autoriza alerta, retreino ou promoção, e ambas conservam L0/audit na policy.

Depois separe o que mudou. Se PSI de um atributo subiu mas a AUC em coorte madura permaneceu estável, investigue mudança de composição, ausentes, fonte ou regras de transformação; não anuncie degradação comprovada. Se a AUC cai enquanto as entradas parecem estáveis, confira primeiro maturação do alvo, seleção de rótulos, versão do modelo e custo de erros por segmento. Se ambos mudam, compare períodos intermediários e procure a origem do desvio. O teste KS entre distribuições é sensível ao tamanho da amostra; um p-valor pequeno em base enorme não informa sozinho se a diferença é operacionalmente relevante. O [template de drift](skills/hub-ml-monitoramento-modelo/templates/drift_report.md) ajuda a registrar volume, referência, política e investigação.

Quando `PerformanceMonitor.should_retrain()` devolve `INVESTIGATE_RETRAINING_CANDIDATE`, o próprio retorno após período informa `automatic_retrain_authorized=False` e passos como validar qualidade dos dados, examinar drift/causa e fazer comparação offline entre modelo vigente e candidato. Se devolve `NO_TRIGGER`, continue acompanhando conforme a política, sem chamar isso de prova de estabilidade permanente. Se devolve `NO_EVIDENCE`, falta período de avaliação; reúna dados maduros antes de concluir. O [template de decisão](skills/hub-ml-monitoramento-modelo/templates/retreino_decision.md) organiza alternativas: manter e observar, corrigir pipeline, recalibrar limiar/probabilidade, treinar challenger ou propor promoção depois dos gates. O monitor não executa nenhuma dessas etapas. Ordene e deduplique períodos antes de adicioná-los: “consecutivo” significa ordem de inserção; a classe não detecta lacunas nem repetições de calendário.

Se a preocupação foi levantada por SHAP, confira se a explicação usa a classe e a escala corretas, se o `X` conserva a ordem de colunas e se os IDs acompanharam qualquer amostra. Um atributo que ganhou importância pode apenas estar correlacionado com outro ou refletir mudança de mistura de clientes. Compare importância por período e segmento e examine erros concretos antes de sugerir ação. `generate_executive_report` usa cortes internos de rótulos “alto/médio/moderado” sobre participação relativa; eles não são aprovação regulatória nem prioridade de remediação. Uma explicação local com informação sensível deve ficar no ambiente de acesso apropriado.

Para entregar o resultado, produza duas camadas. A técnica contém versões, queries ou snapshots, contagens, janelas, classes, fórmulas, thresholds, gráficos e logs/runs necessários para reconstrução. A executiva responde o que foi observado, a quem afeta, qual decisão está proposta e que evidência falta. MLflow pode registrar parâmetros, métricas e artifacts seguros, mas `run_governado` herda tracking/experimento do ambiente; confira destino e run ativo antes de usá-lo. Uma falha no fechamento do contexto não desfaz necessariamente registros anteriores. O histórico do `PerformanceMonitor` permanece em memória se não for persistido por outro componente. Não coloque predições individuais por entidade em artifact de tracking; registre agregados e preserve as linhas em camada governada apropriada.

Feche com um próximo passo que tenha responsável e critério de retorno. No exemplo fictício, “a taxa de ausentes na feature de contatos dobrou em setembro; equipe de dados verificará a carga até 05/10; a equipe de modelo repetirá AUC apenas nas decisões com 30 dias completos” é uma ação verificável. “Retreinar porque PSI passou de 0,2” não descreve causa nem autorização; 0,2 tampouco é limite universal. Se o modelo precisar de mudança, teste challenger fora do período de escolha e submeta promoção à governança. A documentação de um alerta deve permitir que outra pessoa veja a mesma evidência e discorde da interpretação sem precisar adivinhar população ou regra.

<!-- editorial:exclude:start -->
**Fontes:** [skill de monitoramento](skills/hub-ml-monitoramento-modelo/SKILL.md), [template de drift](skills/hub-ml-monitoramento-modelo/templates/drift_report.md), [template de decisão](skills/hub-ml-monitoramento-modelo/templates/retreino_decision.md), [detector](hub_snippets/ml/drift_detection/drift_detection.py), [monitor](hub_snippets/ml/performance_monitor/performance_monitor.py), [run governado](hub_snippets/ml/mlflow_run/mlflow_run.py) e [ADR-0016](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0016-mlflow-runs-micromodelos.md). [Índice](#sumario-mu).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU11](#mu11) · [Próximo: MU13](#mu13) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT10](MANUAL_TECNICO_V2.md#mt10)
<!-- editorial:exclude:end -->

<!-- editorial:exclude:start -->
<a id="parte-mu-iv"></a>
## Parte IV — Micromodelos
<!-- editorial:exclude:end -->


<a id="mu-mod-mu13"></a>
<a id="mu13"></a>
### MU13 — Elaborar e revisar um micromodelo no estágio disponível

<!-- editorial:exclude:start -->
**Você quer:** transformar uma pergunta delimitada em uma especificação revisável, sem inventar dados ou aprovação. **Rota:** fixe unidade e significado (1), preencha o template MM01 (2), interprete validação, fingerprint e descoberta sintética (3), depois trate pendências e gates (4). Os exemplos usam somente entidades fictícias; os comandos abaixo são roteiros de leitura local, não execuções feitas neste manual. [Índice do manual](#sumario-mu).
<!-- editorial:exclude:end -->

<a id="mu13-1"></a>
#### 1. Que pergunta uma linha do micromodelo responde?

Comece com uma frase observável, não com um nome atraente: “Para cada conta fictícia e mês de referência, houve atividade comprovável na janela definida?”. Uma linha seria **conta × mês**. Escreva qual é a chave lógica, quem entra na população elegível e qual data fixa a janela antes de olhar eventos. Se a conta pode aparecer em três meses, são três avaliações, não três evidências independentes para uma linha. Se um evento de fevereiro só chega em março, decidir fevereiro com base na data de ingestão sem registrar o atraso distorce o tempo. A [unidade técnica](MANUAL_TECNICO_V2.md#mt20-1) explica por que entidade, granularidade e referência temporal vêm antes de limiar ou algoritmo.

Agora descreva três respostas separadas. `TRUE` significa que uma regra favorável, aplicada a uma fonte completa para aquela janela, encontrou evidência suficiente. `FALSE` exige **contraevidência suficiente** sob uma regra própria: por exemplo, cobertura confirmada da janela e nenhuma atividade elegível, se essa for a decisão analítica aprovada. `INDETERMINADO` preserva falta de cobertura, atraso ou conflito que impede concluir. “Não encontrei evento” não basta para `FALSE` se a fonte esteve indisponível. A saída de estudo do [contrato MM01](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/MM01/CONTRATO_MICROMODELO.md) mantém as três classes; a passagem futura a um campo booleano de publicação exige política explícita para o indeterminado. Não escreva “sem dado = falso” em comentário esperando que o validador entenda: a política está em campos estruturados.

Separe também o que a característica **não** deve orientar. Neste exemplo, “não usar para decisão automatizada sobre pessoa” é uma restrição de uso, mesmo que uma tabela futura consiga calcular a classificação. `negocio.uso_pretendido` pode registrar estudo de cobertura ou exploração de hipótese; `nao_usar_para` contém a proibição. Não use nomes de cliente, catálogo, esquema, usuário ou caminho do trabalho num exemplo versionado. `CATALOGO_PRODUTO` é a referência simbólica permitida no YAML; o catálogo físico só se vincula no destino autorizado pelo [ADR-0020](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0020-fontes-catalogo-configurado.md). Fonte declarada ainda não é fonte observada nem acesso concedido.

Decida se há score. Uma nota 80 numa escala de 0 a 100 pode expressar força de evidência, não “80% de chance”. Para chamar de `PROBABILIDADE_CALIBRADA`, o [contrato de score](MANUAL_TECNICO_V2.md#mt21-2) exige calibração medida e experimento executado referenciado. Na fase `IDEIA`, deixar método como `PENDENTE`, ou desabilitar score de modo coerente, diz mais verdade que produzir percentagem sem ensaio. Pergunte a quem propôs o caso: qual comportamento observável faria a resposta mudar de TRUE para FALSE, qual ausência a tornaria INDETERMINADA e qual evidência refutaria a hipótese? As respostas alimentam definição operacional, evidências, contraevidências e critério de validação; elas não são resultados medidos.

Um micromodelo é a especificação de domínio que une essas decisões, e não mais um tipo de objeto da biblioteca `.assistant`. O [ADR-0014](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0014-micromodelo-artefato-de-dominio.md) o distingue tanto de skill quanto de Produto de Dados publicado. Na árvore corrente consultada em 07/10/2026, você pode escrever e conferir o contrato local sintético e consultar a [skill `hub-ml-micromodelos`](skills/hub-ml-micromodelos/SKILL.md), já integrada. Ela orienta especificação e descoberta nos modos `OBJETIVO_CONHECIDO` e `DESCOBRIR_OPORTUNIDADES`; permanece `L1/audit`, sem runner protegido ou Receipt próprios. A biblioteca instalada é chamada explicitamente. A presença da skill não executa um projeto nem concede acesso a dados reais. Leve para a próxima seção uma frase de unidade, três condições de resposta, fontes candidatas ainda não confirmadas e usos proibidos.

<a id="mu13-2"></a>
#### 2. Como preencher o YAML sem completar lacunas com ficção?

YAML é o formato de dados legível por pessoas usado no arquivo `micromodelo.yaml`. Trabalhe numa área autorizada e comece pela cópia integral do [template MM01 instalado no Hub](hub_micromodelos/contratos/micromodelo.template.yaml), que já traz 16 propriedades de topo: `schema_version: "1.0.0"` e os 15 grupos: `identidade`, `negocio`, `entidade`, `fontes`, `evidencias`, `contra_evidencias`, `classificacao`, `score`, `experimentos`, `validacao`, `saida`, `tracking`, `governanca`, `publicacao` e `proveniencia`. Schema de validação é o contrato de campos, tipos e condições aceitos pelo arquivo; aqui ele é `micromodelo.schema.json`. O [mapa técnico](MANUAL_TECNICO_V2.md#mt-mod-mt21-fullpath-map) detalha todos os 304 caminhos, obrigações por pai e condições. Não reduza o documento a um exemplo de cinco chaves: o schema é fechado e não injeta valores ausentes. `PENDENTE`, `null` e `[]` escritos no template são valores explícitos de uma proposta inicial, não defaults aplicados em silêncio.

Na cópia para uma proposta própria, substitua `identidade.nome` e `identidade.titulo` pelos identificadores sanitizados do caso, defina `identidade.micromodel_version` e preserve a fase inicial coerente. Registre em `proveniencia.criado_em_utc` o instante real de criação em UTC e em `gerado_por` a autoria ou ferramenta efetivamente usada; a data de exemplo e “template MM01” não são a proveniência da nova proposta. Vincule `pedido_original_ref` à referência autorizada do pedido; se ela ainda não existe, mantenha `PENDENTE`. Não invente pessoa, decisão ou data para completar o arquivo.

Este trecho é copiável **para substituir apenas os blocos correspondentes na cópia do template**, não um arquivo completo por si. Mantém o caso totalmente fictício e a fase `IDEIA`; adapte a pergunta e os termos sem converter hipótese em fato:

```yaml
negocio:
  caracteristica: "atividade observável na janela mensal sintética"
  objetivo: "estudar cobertura de eventos na população fictícia"
  definicao_operacional: "uma conta fictícia é avaliada por mês de referência; atividade requer evento elegível na janela definida"
  uso_pretendido:
    - "estudo analítico sintético de cobertura mensal"
  nao_usar_para:
    - "decisão automatizada sobre pessoa"
entidade:
  tipo: "conta fictícia"
  chave_logica: "id_conta"
  granularidade: "uma avaliação por conta e mês de referência"
  populacao_elegivel: "contas fictícias com mês de referência delimitado"
  referencia_temporal: "último dia do mês de estudo; janela declarada separadamente na regra"
```

O bloco `negocio` responde o que se quer estudar e para quê; `entidade` fixa quem é uma linha e quando ela existe. O trecho ainda não diz qual tabela contém eventos nem como provar completude. Por isso, manter `fontes: []`, `evidencias: []` e `contra_evidencias: []` na fase inicial é mais honesto que inventar `schema` ou `objeto`. Quando uma fonte for declarada, cada item precisa de `id`, `catalogo_ref: CATALOGO_PRODUTO`, `schema`, `objeto`, `tipo_objeto`, `campos`, `papel` e proveniência próprios. Nesse item, `fontes[].schema` nomeia o agrupamento de objetos dentro do catálogo, não o arquivo que valida o YAML. Esses valores devem vir de decisão e observação autorizadas. `fontes_ref[]` de cada regra deve apontar a um `fontes[].id` existente. No Git, use apenas fixture ou placeholder, nunca o nome físico do catálogo do trabalho. O binding de MM03 não altera o YAML nem autoriza leitura.

Para planejar uma fonte sem alegar que ela já foi descoberta, anote fora do bloco confirmado qual papel ela precisaria cumprir. Uma fonte de eventos poderia sustentar atividade, mas uma segunda peça talvez seja necessária para provar que a janela esteve completamente coberta. Regra favorável, regra contrária e hipótese de cobertura não são três nomes para a mesma observação. Quando houver informação autorizada para declarar itens em `fontes[]`, dê IDs estáveis e use esses IDs em `evidencias[].fontes_ref[]` e `contra_evidencias[].fontes_ref[]`. A descrição explica a intenção humana; `regra` enuncia o critério que seria testado; `proveniencia` diz se aquilo foi descoberto, inferido ou apenas proposto. O validador confere o vínculo entre IDs, não a existência física nem a qualidade estatística da tabela. Por isso a revisão da fonte precisa guardar, separadamente, cobertura temporal, permissões e compatibilidade da coluna com a chave lógica.

No bloco `classificacao`, mantenha `tipo: BOOLEANO_COM_INDETERMINADO`, escreva `quando_true`, `quando_false` e `quando_indeterminado` como condições materialmente diferentes, e preserve `ausencia_evidencia.tratamento: INDETERMINADO`, `resultado_sem_evidencia: INDETERMINADO`, `regra_ref: null` até haver motivo e aprovação para exceção. Se criar limiar, documente `operador`, número finito, `unidade` e proveniência; um 70 sem unidade e janela não é regra reproduzível. `PROPOSTO` é válido antes do gate formal. `APROVADO` requer responsável, instante e referência da decisão; `MEDIDO` requer execução identificável e data. Preencher esses estados para “passar no teste” fabricaria prova. O [guia de estados](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/MM01/ESTADOS_E_PROVENIENCIA.md) mostra o que muda em `EM_VALIDACAO` e `VALIDADO`.

O template habilita score como `FORCA_EVIDENCIA` com escala 0–100 e normalização `PENDENTE`. Se você ainda não definiu score, pode preservar a proposta pendente na fase `IDEIA`; se o desabilitar, alinhe `tipo_semantica`, `semantica_ref`, `escala`, `normalizacao`, `calibracao` e `saida.estudo.campo_score` com as regras do schema, em vez de mudar só `habilitado`. `experimentos: []` e `validacao.resultado: null` dizem que não houve resultado observado; `validacao.aprovacao_humana.status: PENDENTE` não carrega nome ou data de aprovação. `saida.estudo` conserva as três classes; `saida.publicacao` fica pendente antes de candidato. `tracking` reserva MLflow para fase posterior, sem guardar histórico de runs no YAML. `governanca` aceita `PENDENTE` enquanto classificação de dados, LGPD (Lei Geral de Proteção de Dados) e gestor não forem decididos; `publicacao` começa `NAO_INICIADA`, com autoridade `GOVERNANCA_EXTERNA`.

Antes de validar, faça uma revisão humana de cinco pares: grão/chave, janela/referência temporal, regra favorável/contraevidência, ausência/resultado indeterminado e uso pretendido/uso proibido. Depois confira proveniência ao lado de **cada** afirmação. Um documento pode ser formalmente válido em `IDEIA` e ainda estar longe de uma regra aprovada, justamente porque a fase permite registrar trabalho incompleto sem disfarçá-lo. A [fixture MM01 validada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/tests/fixtures/micromodelos_mm01/valido_validado.json) mostra um shape de fase posterior, mas seus aprovadores, fontes e resultados são sintéticos e não devem ser copiados como fatos de outro caso.

Ao revisar a cópia, percorra também os grupos que não mudaram no trecho. `identidade.estado.fase_atual: IDEIA` deve acompanhar `fase_anterior: null`; a condição `ATIVO` não precisa de motivo, mas uma condição bloqueada precisaria. `proveniencia.criado_em_utc` e `pedido_original_ref` identificam a origem do arquivo, não aprovam cada regra. Em `saida.estudo`, confira se os valores continuam exatamente `TRUE`, `FALSE` e `INDETERMINADO`. Em `publicacao`, mantenha a autoridade externa e referências nulas enquanto não houver handoff. Isso evita que a cópia pareça coerente apenas porque os dois blocos novos estão bem escritos, enquanto algum valor herdado do template foi interpretado como decisão específica do caso.

<a id="mu13-3"></a>
#### 3. O que cada verificação demonstra?

Os comandos abaixo são para demonstração **offline**, a partir da raiz deste repositório, sobre fixtures sintéticas. `python -B` evita gravar bytecode; não impede que uma ferramenta faça outros efeitos, então leia o contrato de cada CLI (interface de linha de comando). Nenhum comando foi executado para escrever este capítulo. Os três caminhos `tools/micromodelo_mm0*.py` continuam como entradas de compatibilidade; as implementações atuais estão em [hub_micromodelos/execucao](hub_micromodelos/execucao/README.md), nos módulos `especificacao.py`, `assinatura.py` e `metadados.py`. O primeiro carrega a fixture JSON (formato estruturado de dados), carrega pelo argumento `--schema` o arquivo de contrato `micromodelo.schema.json` da MM01 e valida forma, referências e regras de fase:

```text
python -B tools/micromodelo_mm01_contract.py tools/tests/fixtures/micromodelos_mm01/valido_validado.json --schema docs/sprints/micromodelos/MM01/micromodelo.schema.json
```

O arquivo de entrada e o schema são lidos; a ferramenta imprime diagnóstico no terminal, sem alterar o YAML. Se não houver issues, a categoria de saída é `SNAPSHOT_VALIDO` com `HISTORICO_NAO_CERTIFICADO`: ela conferiu o documento corrente, não encontrou um passado confiável sozinha. Se houver problema, imprime fullpath, código e `REPROVADO`; falha de carga aparece como `ERRO_DE_CARGA`. O comando opcional `--previous caminho/para/anterior_confiavel.yaml` só é apropriado quando você tem snapshot anterior **confiável** da mesma identidade. Ele compara versão e transição observada; não prova história por juntar dois arquivos escolhidos arbitrariamente. A [MM01 técnica](MANUAL_TECNICO_V2.md#mt21-4) explica a diferença entre shape, branch semântico e evolução.

Ao usar o mesmo comando na sua cópia autorizada do template, passe o caminho real do arquivo somente no seu ambiente; não registre esse caminho ou mensagens com identificadores corporativos neste repositório. Se `REPROVADO` citar um campo obrigatório, abra o grupo pai e confira se o trecho foi inserido no nível correto de indentação. Se citar um ID referenciado, compare a lista de fontes com a regra. Se o problema for gate de fase, não tente satisfazê-lo elevando uma proveniência para `APROVADO` ou um experimento para `MEDIDO` por edição textual. Volte a `IDEIA` ou ao estudo enquanto a decisão ou execução não existem, preservando a hipótese legível. Uma saída limpa da fixture demonstra que o validador funciona para aquele documento sintético; não valida sua proposta diferente.

Para um documento MM01 válido, a [MM02](MANUAL_TECNICO_V2.md#mt22-2) calcula fingerprint, resumo SHA-256 da parte material canonicalizada da especificação. SHA-256 é um hash de bytes; o preimage é a representação canônica entregue a esse hash. Este comando lê a **mesma fixture** e o schema, valida de novo, e imprime ID do algoritmo, versão e digest; `--show-canonical` também mostra o JSON exato do preimage:

```text
python -B tools/micromodelo_mm02_fingerprint.py tools/tests/fixtures/micromodelos_mm01/valido_validado.json --schema docs/sprints/micromodelos/MM01/micromodelo.schema.json --show-canonical
```

Não copie um digest imaginado deste manual: o valor correto depende dos bytes canônicos da fixture e da versão `mm02-spec-fingerprint-v1`. Registre algoritmo, versão, digest e documento validado juntos. Alterar um título ou uma aprovação pode manter a identidade material; alterar fonte, janela, regra, limiar, peso ou saída deve ser examinado como mudança. O fingerprint não é hash do YAML bruto, resultado de teste, recibo de execução ou aceite humano. A [matriz de materialidade](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/MM02/MATRIZ_MATERIALIDADE.md) permite conferir que campos entram; ela evita tratar qualquer alteração do arquivo como nova definição.

A [coleta MM03 integrada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/MM03/README.md) oferece outra pergunta: “quais metadados uma fonte sintética deixou observar?”. Provider é o componente que fornece páginas de metadados ao coletor; o `FixtureProvider` incluído lê um JSON local sintético e responde a essas solicitações. O produto também contém um [adapter Databricks](hub_micromodelos/execucao/databricks.py), mas ele não é usado neste roteiro offline nem autoriza consulta no destino. Use a fixture local que declara `catalogo_sintetico` e escolha uma shortlist só depois de observar o objeto:

“Shortlist” aqui é a lista curta de pares schema/objeto que você decidiu inspecionar após a descoberta. Não é a lista de todos os objetos visíveis e não nasce de um comentário da tabela. A fixture contém uma view com texto adversarial que tenta mandar consultar outro catálogo; o coletor deve manter esse texto marcado como não confiável. A etapa de detalhes solicita colunas, tags de coluna e constraints somente do candidato observado. Uma constraint é restrição declarada, como chave ou unicidade; ela sai com `enforcement=NOT_VERIFIED`, sem prova de que a base física a imponha. Mesmo uma coluna `nullable: false` em metadata não substitui inspeção autorizada de qualidade dos registros; o laboratório não a faz. Na sua anotação de descoberta, mantenha a diferença entre “nome observado”, “dado lido” e “uso aprovado”.

Primeiro, liste os objetos do schema sem antecipar a escolha humana:

```text
python -B tools/micromodelo_mm03_metadata.py --fixture tools/tests/fixtures/micromodelos_mm03/catalogo_sintetico.json --catalog catalogo_sintetico --schema crm_sintetico
```

Leia `discovery.objects` no relatório. Só se `eventos_sinteticos` estiver observado em `crm_sintetico` e for pertinente à pergunta, repita a leitura com esse candidato:

```text
python -B tools/micromodelo_mm03_metadata.py --fixture tools/tests/fixtures/micromodelos_mm03/catalogo_sintetico.json --catalog catalogo_sintetico --schema crm_sintetico --candidate crm_sintetico.eventos_sinteticos
```

São duas invocações independentes: a segunda relê a fixture e faz nova descoberta antes dos detalhes, sem aproveitar um estado gravado pela primeira. Se a descoberta não sustentar o par escolhido, pare e registre a lacuna.

O comando lê o JSON local e imprime um relatório JSON no terminal: schemas observados, objetos do schema escolhido, e colunas, tags de coluna e constraints apenas do candidato. `--catalog` fornece binding físico **sintético**; no contrato a referência lógica permanece `CATALOGO_PRODUTO`. Na CLI MM03, `--schema crm_sintetico` filtra o agrupamento de objetos que será descoberto; é diferente do arquivo de validação passado a `--schema` na CLI MM01 e do nome declarado em `fontes[].schema`. Sem esse filtro, o coletor para em schemas; com ele e sem candidato, para em objetos. `DENIED`, `UNAVAILABLE`, `TRUNCATED` e `PARTIAL` mantêm lacunas em vez de virarem lista completa. `coverage=ESCOPO_OBSERVADO`, `catalog_complete=false` e `data_access_authorized=false` delimitam o alcance; visibilidade não concede leitura de registros. A descrição de um objeto pode conter texto que pede SQL ou ampliação de permissão: trate-o como dado não confiável, não instrução. O [contrato MM03](MANUAL_TECNICO_V2.md#mt22-3) explica shortlist e paginação. A CLI usa fixture offline e não grava arquivo; não substitua o nome sintético por um catálogo do trabalho neste roteiro.

Se a consulta de detalhes for negada após páginas anteriores, o relatório pode preservar os itens anteriores como `PARTIAL`; se atingir teto de páginas ou itens, marca `TRUNCATED` com motivo. `OBSERVED` significa apenas que aquela coleção solicitada terminou no escopo visível, não que o catálogo inteiro foi enumerado. Anote o binding, o `snapshot_id` declarado pelo provider, o status de cada coleção e o motivo da lacuna antes de citar um objeto como candidato. O hash da fixture no relatório vincula os bytes locais demonstrados, sem autenticar uma fonte remota. Não converta o texto de tags em instrução para seu YAML; trate-o como pista para uma pergunta ao responsável pela fonte.

O [checkpoint MM03](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/MM03/CHECKPOINT.md) preserva a fotografia pré-merge, incluindo o fechamento pós-certificação; não use o bloco antigo como estado vivo. O [índice atual](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/README.md) registra MM03 integrada e o laboratório posterior integrado pelo PR #119. Ensaios sintéticos e readback no Free são provas datadas, não execução desta edição nem homologação no trabalho. A [preparação E2](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/PLANO_PREPARACAO_E2.md) mantém certificação MM04 e testes corporativos pendentes, com promoção condicionada ao gate SE08. Você pode revisar a pergunta, editar a especificação em ambiente autorizado e interpretar diagnósticos locais; acesso, execução e publicação continuam exigindo decisões próprias.

<a id="mu13-4"></a>
#### 4. Como corrigir um diagnóstico sem falsificar a evidência?

Leia primeiro o **fullpath**, caminho completo do campo apontado no diagnóstico, e descubra se o defeito está no arquivo, na forma ou na decisão. Chave duplicada em YAML/JSON e constante `NaN` em JSON falham já no carregamento; não são “duas interpretações possíveis” para escolher depois. Campo obrigatório ausente, enum fora da lista ou texto sem letra/número material falha no schema. `fontes_ref` que aponta para um `fontes[].id` inexistente é erro de referência. Proveniência `APROVADO` sem bloco de aprovação e `MEDIDO` sem referência de execução são erros de prova, mesmo que o texto pareça convincente. O [contrato MM01](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/MM01/CONTRATO_MICROMODELO.md) mantém essas categorias separadas para que a correção atinja a origem do valor.

Suponha que o diagnóstico cite `evidencias[0].fontes_ref[0]`. Compare o ID com os declarados em `fontes[]`; corrija a grafia ou declare a fonte por decisão autorizada. Não invente uma fonte para satisfazer a referência. Se o erro aponta `classificacao.ausencia_evidencia`, verifique `tratamento`, `resultado_sem_evidencia`, `regra_ref` e proveniência juntos. Ausência comum deve continuar `INDETERMINADO`; converter para `FALSE` pede regra explícita aprovada. Um texto como “não há eventos” não autoriza essa conversão quando a cobertura da fonte é parcial. Se aparecer um erro de limiar ou peso, confirme valor finito, unidade, hipótese de corte e status correto; mudar só `PROPOSTO` para `APROVADO` sem decisão humana real corrige a string e corrompe o processo.

Gates de fase acrescentam exigências, não resultados automáticos. Em `EM_VALIDACAO`, fontes, evidências, contraevidências e critérios precisam estar presentes, e regras, semântica, limiares e pesos existentes exigem aprovações pertinentes. `VALIDADO` exige resultado técnico `MEDIDO` e decisão humana final `APROVADO`. `CANDIDATO_PRODUTO` exige campo booleano e política estruturada para o `INDETERMINADO`, com `indeterminado_vira_false=false`; isso ainda não é Produto de Dados publicado. O [ADR-0017](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0017-governanca-externa-publicacao.md) reserva geração, validação final e publicação à governança institucional no destino. Uma referência de handoff não é autorização de publicar, e um YAML que diz `PUBLICADO` não substitui confirmação externa. A condição `BLOQUEADO` pode registrar impedimento sem fingir que a hipótese foi refutada.

Se o snapshot passa sem `--previous`, preserve `HISTORICO_NAO_CERTIFICADO`. Para certificar evolução, localize o anterior confiável, confira identidade e versão e só então compare transição; nunca fabrique um arquivo anterior para obter a mensagem `APROVADO_EVOLUCAO`. Quando a definição muda, confronte o preimage e o fingerprint MM02 com a justificativa da mudança; quando apenas a aprovação muda, conserve a trilha de decisão mesmo que o fingerprint fique igual. Da mesma forma, uma observação MM03 `OBSERVED` se refere ao recorte pedido, não ao catálogo inteiro; `DENIED` ou `TRUNCATED` não são permissão para procurar outra fonte por conta própria. Nomes e tags podem ser sensíveis ou adversariais e exigem revisão antes de qualquer transcrição fora do ambiente autorizado.

O [índice vivo de Micromodelos](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/README.md), consultado em 07/10/2026, registra MM00–MM03 integradas e o módulo de laboratório MM04–MM13 integrado ao Hub. O aceite do laboratório sintético e os ensaios Free registrados não certificam todas essas sprints, o destino corporativo ou a capacidade presente da conta do leitor. A [revisão pós-SEF](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/micromodelos/REVISAO_PLANO_POS_SEF_2026-09-23.md) é uma fotografia de arquitetura de 23/09, útil para os gates futuros, mas seu antigo `MM02=NOT_STARTED` não descreve o presente. A skill e os briefings MM04–MM05 já existem; a [policy integrada](hub_padroes/skill_enforcement/policy.json) mantém `current_level=L1`, `target_level=L3` e modo `audit` para Micromodelos. O alvo não é execução protegida disponível. Migração de legados pertence à MM12, depois de piloto novo e congelamento da versão inicial do framework. Para encerrar sua revisão atual, registre a pergunta, a versão do YAML, diagnósticos, evidência disponível, lacunas e quem precisa decidir cada uma. Uma fixture verde mostra apenas que o contrato sintético foi satisfeito; ela não preenche dados, permissão ou aceite institucional.


<!-- editorial:exclude:start -->
[Anterior: MU12](#mu12) · [Próximo: MU14](#mu14) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT22](MANUAL_TECNICO_V2.md#mt22)
<!-- editorial:exclude:end -->

<!-- editorial:exclude:start -->
<a id="parte-mu-v"></a>
## Parte V — Entregas visuais
<!-- editorial:exclude:end -->


<a id="mu-mod-mu14"></a>
<a id="mu14"></a>
### MU14 — Planejar uma entrega visual e aplicar temas

Um tema organiza escolhas de apresentação, como cor, fonte e espaço. Ele ajuda a manter uma linguagem comum, mas não decide qual pergunta responder nem verifica os números mostrados. Este capítulo guia uma entrega simples: escolher uma forma de gráfico, carregar uma referência do Hub, criar uma proposta isolada, aplicá-la apenas a uma figura e comparar o resultado. Os dados do exemplo são sintéticos. As funções descritas existem no código do Hub; sua presença no Git não confirma instalação ou homologação no seu workspace.

<a id="mu14-1"></a>
#### MU14.1 — Comece pela pergunta, pelo público e pela forma

Antes de escolher cor, escreva em uma frase a decisão que a imagem deve apoiar. “Quantos chamados cada equipe resolveu nesta semana?” pede comparar quantidades entre categorias. “Como o volume de chamados variou ao longo das semanas?” pede mostrar uma sequência no tempo. “A solução ficou melhor para quais grupos?” exige decidir qual medida representa “melhor” e se os grupos são comparáveis. Essas perguntas não são intercambiáveis: a primeira pode funcionar em barras; a segunda, em linha temporal; a terceira talvez precise de barras separadas ou tabela com contexto. A forma deve expor a relação importante, sem sugerir uma relação que os dados não sustentam.

Defina quem vai ler. Uma equipe operacional pode precisar de rótulos exatos e da unidade em cada eixo; uma apresentação executiva talvez precise começar pela conclusão e depois mostrar os detalhes. Não retire unidade, período, denominador ou definição da métrica para “limpar” o desenho. Se o eixo mostra contagem de chamados, escreva “chamados”; se mostra porcentagem, indique a base da porcentagem. Para proporções, pergunte “de quantos?”; para uma série, pergunte se os intervalos são iguais e se há lacunas. O visual deve preservar a possibilidade de conferir o número, não apenas produzir uma impressão de crescimento ou queda.

Um roteiro curto ajuda a preparar a célula antes de importar qualquer helper: pergunta, audiência, dados necessários, unidade, forma, conclusão provisória e ressalvas. Por exemplo: “Comparar chamados resolvidos por três equipes em uma semana; contagem de chamados; dados sintéticos de demonstração; barras horizontais; não interpretar a diferença como produtividade sem saber volume recebido e complexidade.” Nesse caso, três barras deixam a comparação direta. A diferença entre 12 e 8 chamados é visível, mas não prova que uma equipe trabalhou melhor. O tema pode uniformizar as barras e o título; não fornece o contexto operacional ausente.

O [guia de Plotly](hub_snippets/visual/theme_plotly/README.md) reforça essa ordem: construa uma figura com dados e rótulos corretos, depois aplique aparência. Plotly é a biblioteca Python usada aqui para construir o gráfico. Uma figura pronta ainda pede inspeção de escala, unidade, fonte declarada e espaço disponível. Ao apresentar a alguém, inclua uma frase de interpretação perto da figura; o leitor não deve adivinhar a decisão pretendida a partir da paleta. Se houver mais de uma figura no mesmo notebook, anote quais usam uma proposta visual e quais mantêm o padrão, para não transformar uma experiência local em regra tácita da equipe.

Se a comparação envolve muitos grupos, barras podem ficar espremidas; então ordene categorias de modo explicado, agrupe apenas quando houver justificativa ou divida a pergunta em gráficos menores. Para uma relação entre duas medidas contínuas, pontos podem revelar dispersão que uma única média esconderia. Para distribuição, um histograma mostra frequência por faixa, mas a escolha das faixas altera a leitura e precisa ser declarada. Essas são escolhas de comunicação, não configurações automáticas do tema. Em qualquer formato, evite um título que já prometa causalidade quando a figura mostra apenas associação. A pergunta deve ser mais específica que “fazer um gráfico bonito”.

<a id="mu14-2"></a>
#### MU14.2 — Escolha referência, proposta e contexto

O Hub conserva rotas legadas e oferece uma rota de tema **opt-in**, isto é, usada apenas quando você a chama explicitamente. O núcleo [`visual.tema`](hub_snippets/visual/tema/README.md) lê uma configuração JSON, um texto estruturado em campos e valores, e devolve um `ResolvedTheme`: um retrato completo e protegido daquelas escolhas. “Resolver” significa validar e reunir os valores para um consumidor; não significa redesenhar todos os notebooks. Os contextos do contrato são `notebook`, `readme` e `presentation`. Para o adaptador Plotly deste capítulo, escolha `notebook`; ele aceita somente o modo visual `light`. Uma configuração válida de `readme` não deve ser passada ao gráfico para tentar obter uma aparência editorial.

Há três decisões de uso. Se você quer a aparência histórica sem criar proposta, mantenha as funções legadas do componente. Se quer testar um tema no notebook, carregue a referência sintética com `load_reference_theme("notebook")` e use as funções terminadas em `_resolvido`. Se recebeu um arquivo de proposta do mantenedor, ele pode ser carregado com `load_theme(root, relative_path, expected_sha256=..., expected_context="notebook")`, usando uma raiz de arquivos autorizada e a revisão exata. O último caminho é mais exigente porque lê bytes de um arquivo escolhido; não remova o hash esperado para fazer outra revisão “passar”. Nenhuma das três decisões, por si, instala um padrão no workspace.

A referência `legado_notebook.json` é uma fixture, ou seja, um exemplo controlado para comparação e teste. Ela contém 48 tokens; **token** é um nome de escolha visual associado a um valor, como `brand.primary = #005CA9`. É útil para começar porque reproduz a linguagem histórica nos consumidores integrados, mas não significa que a proposta esteja aprovada como nova identidade. O [guia operacional](hub_padroes/identidade_visual/GUIA_OPERACIONAL.md) demonstra a referência, a cópia e um erro esperado. Seu notebook de exemplo altera apenas dados sintéticos em memória; a preparação localiza a pasta `.assistant` e pode exigir as bibliotecas declaradas em `requirements-temas.txt`. Não instale pacotes fora do procedimento autorizado do seu ambiente só porque uma importação falhou.

Para experimentar uma cor sem alterar a referência, obtenha uma cópia com `to_dict()`, ajuste um campo e valide a cópia. Um dicionário Python é uma coleção de nomes e valores; neste caso, `tokens` é outro dicionário dentro dele. O código seguinte supõe que a pasta `.assistant` já está no caminho de importação do Python, como explica o exemplo do Hub:

```python
from hub_snippets.visual.tema import load_reference_theme, resolve_theme

referencia = load_reference_theme("notebook")
proposta = referencia.to_dict()
proposta["tokens"]["brand.primary"] = "#112233"
tema_proposto = resolve_theme(proposta, expected_context="notebook")

print(referencia.tokens["brand.primary"])   # #005CA9
print(tema_proposto.tokens["brand.primary"])  # #112233
```

O `#` inicia uma cor hexadecimal de seis dígitos; o contrato exige `#RRGGBB` em maiúsculas. `resolve_theme` não corrige silenciosamente um valor inválido nem acrescenta campos ausentes. Se você apagar `brand.primary`, recebe `SCHEMA_REQUIRED`; isso indica que a proposta ficou incompleta, não que a função deva usar uma cor de fallback. `normalize_color` pode converter uma cor minúscula explicitamente durante a autoria, mas a importação não o faz por conta própria. A referência continua azul depois que a cópia muda. Se precisar guardar o trabalho, `export_theme(tema_proposto)` devolve bytes em memória; salvar arquivo, compartilhar, aprovar e publicar são ações separadas.

Um `fingerprint` permite reconhecer o conteúdo resolvido junto com o schema e o manifesto de assets que participaram da validação. Ele ajuda a comparar a mesma configuração em uma rodada compatível, mas não identifica o autor, garante contraste ou aprova a paleta. O [contrato central](hub_padroes/identidade_visual/README.md) explica que os defaults do schema são exemplos declarativos, não valores inseridos numa proposta. Assim, uma proposta precisa ser completa; “ficou parecida com o legado” não basta para concluir que todos os campos são válidos. Se um erro aparecer, consulte [ERROS.md](hub_padroes/identidade_visual/ERROS.md) pelo código, campo e ação recomendada, sem colar dados sensíveis na mensagem de ajuda.

Ao escolher uma proposta recebida, pergunte também qual parte dela será realmente lida pelo consumidor. O schema tem tokens para notebook, material editorial e apresentação, e não existe um botão universal que aplique tudo ao mesmo tempo. No caso Plotly, a cor principal, a paleta, a fonte e medidas de gráfico têm efeitos definidos no adaptador; tokens de uma tabela HTML ou de um cabeçalho não serão aplicados magicamente à mesma figura. Essa limitação ajuda a comparar com justiça: anote “o que mudou” e “o que não mudou” antes de concluir que a proposta ficou melhor. Se a organização exige uma identidade aprovada, valide com o mantenedor qual configuração é autorizada; uma referência de teste é ponto de partida pedagógico, não decisão institucional.

<a id="mu14-3"></a>
#### MU14.3 — Aplique a uma figura e compare

Construa primeiro uma figura com os dados e rótulos escolhidos. O exemplo abaixo cria três contagens sintéticas que somam 30. A contagem total é conhecida porque foi escrita no exemplo; o helper não a calcula para você. `aplicar_tema_resolvido` é uma função do Hub que muda propriedades de apresentação da figura Plotly recebida e devolve a mesma figura. A chamada não ativa um template global da sessão e não muda os valores das barras. `fig.show()` é o passo que pede ao notebook para exibir o gráfico; o retorno da função de tema, sozinho, não equivale a uma visualização vista por alguém.

```python
import plotly.graph_objects as go
from hub_snippets.visual.tema import load_reference_theme, resolve_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido

referencia = load_reference_theme("notebook")
dados = {"Equipe A": 12, "Equipe B": 10, "Equipe C": 8}

base = go.Figure(go.Bar(x=list(dados), y=list(dados.values())))
base.update_layout(
    title="Chamados resolvidos por equipe — semana sintética",
    xaxis_title="Equipe",
    yaxis_title="Chamados resolvidos",
)

fig_referencia = go.Figure(base)
aplicar_tema_resolvido(fig_referencia, referencia,
                      fonte="dados sintéticos deste exemplo", n=30)

proposta = referencia.to_dict()
proposta["tokens"]["brand.primary"] = "#112233"
tema_proposto = resolve_theme(proposta, expected_context="notebook")
fig_proposta = go.Figure(base)
aplicar_tema_resolvido(fig_proposta, tema_proposto,
                      fonte="dados sintéticos deste exemplo", n=30)

fig_referencia.show()
fig_proposta.show()
```

Compare as duas imagens mantendo o mesmo conjunto, período, tipo de barra e escala. `brand.primary` alimenta a cor do título no adaptador Plotly, então essa escolha deve mudar entre referência e proposta. Ela **não** altera automaticamente a cor de cada barra: o consumidor usa `palette.categorical` para uma sequência de cores e respeita cores já fixadas nos traces. Se você esperava mudar as barras e só o título mudou, a função não falhou; foi a expectativa que estava fora do mapeamento daquele token. O que comparar agora é legibilidade do título, contraste com o fundo, espaço de eixo e clareza do rodapé. A frase “Fonte: dados sintéticos deste exemplo” e o “N = 30” são declarações do código acima. Com dados reais, confira origem e total antes de exibi-los.

Uma função legada como `aplicar_tema` continua disponível para quem precisa do padrão anterior. Evite misturar a rota legada e a nova sem anotar qual foi aplicada a cada figura. Para a nova rota, o tema pode redefinir largura, altura, margens, fonte e legenda; por isso, se uma figura exige um tamanho específico, ajuste esse layout **depois** da chamada. A função não corrige eixos enganadores, unidade errada, agregações ou métricas. Também não recolore cores explícitas de traces nem modifica dados analíticos. Se a figura já tinha uma legenda muito abaixo do desenho, inspecione o rodapé: reaplicar a função pode duplicar anotações e criar sobreposição.

Existe uma operação separada, `registrar_template_plotly_resolvido`, para registrar um template `hub-*` na sessão. O argumento `nome` é obrigatório e passado por palavra-chave, por exemplo `nome="hub-proposta"`; o registro não troca o padrão da sessão a menos que `ativar=True`. Mesmo com esse controle, uma ativação pode afetar figuras criadas depois na mesma sessão. Para uma comparação de duas figuras, prefira a aplicação por figura do exemplo: ela deixa claro o alcance. Se alguém escolheu registrar um template, deve documentar o nome, a opção de ativação e como restaurará o default anterior. A rota HTML, como `section_header_html_resolvido`, também exige tema explícito, mas tem seus próprios modos e propriedades; o fato de Plotly aceitar o tema não demonstra que todo consumidor o aceitará.

Faça a comparação como um pequeno experimento controlado. Primeiro confira os números na variável `dados`: 12 + 10 + 8 = 30; esse total é o N declarado e não uma medição feita pela função. Depois olhe a figura com a referência e anote título, cor de barras, posição da legenda, dimensões e rodapé. Repita a observação com a proposta, sem trocar o conjunto de dados. Se a proposta só alterou `brand.primary`, não atribua à cor nova uma mudança de quantidade: ambas as figuras devem mostrar as mesmas três alturas. Se aparecer uma diferença numérica, ela veio de outro trecho do notebook e precisa ser investigada antes da entrega. A comparação lado a lado separa efeito do tema de efeito da análise.

Também compare com intenção. Um título `#112233` pode ter bom contraste em uma superfície e fraco em outra; mesmo que o schema aceite o valor, o público precisa conseguir lê-lo. Se a figura ficou larga demais, ajuste a largura explicitamente após aplicar o tema e confira o efeito no eixo e no rodapé. Se você decidir usar cores próprias para as barras, registre esse fato: a paleta categórica do tema já não será a única responsável pela aparência. O resultado desejado é uma figura cujo caminho de construção pode ser explicado: dados e rótulos primeiro, tema opt-in depois, ajustes locais por último, exibição e revisão ao final.

<a id="mu14-4"></a>
#### MU14.4 — Revise unidade, consistência e leitura real

Depois de ver a figura, volte à pergunta inicial. As barras realmente permitem comparar as equipes? O eixo vertical começa e termina em valores que não dramatizam uma diferença pequena? Os rótulos “Equipe A/B/C” correspondem aos registros? “Semana sintética” e “chamados resolvidos” continuam visíveis? A cor não deve ser a única forma de distinguir um estado importante; acrescente rótulo, legenda ou texto quando o significado exigir. Uma paleta coerente ajuda a reconhecer o Hub, mas não substitui valor, unidade, escala e explicação da conclusão. Se a comparação atravessa gráficos, mantenha as mesmas definições, período e limites de eixo quando isso for necessário para comparar diretamente.

Inspecione a figura no tamanho em que o público vai usá-la. Um notebook largo pode esconder que o título, o rodapé ou a legenda colidem numa tela menor. Conferir uma saída em Python local não prova como ela ficará no Databricks; abrir a superfície real é uma etapa própria. Verifique contraste, tamanho do texto, leitura de cores e possibilidade de entender a figura sem depender apenas da cor. Um tema validado pode ter combinações pouco legíveis; um modo chamado “alto contraste” também precisa de avaliação visual. O adaptador Plotly atual aceita apenas `notebook/light`, portanto não tente selecionar `dark` ou `high_contrast` para esse gráfico esperando uma conversão implícita.

Antes de entregar, deixe junto da figura uma frase que diga o que ela mostra e outra que diga seu limite. Para o exemplo: “A Equipe A resolveu 12 chamados na semana sintética, contra 8 da Equipe C.” Em seguida: “Essas contagens não consideram complexidade nem volume recebido; não são medida de produtividade.” Com dados de trabalho, acrescente fonte verificável, data de extração, definição da métrica e tratamento de ausentes. Não use a cor temática para esconder uma ressalva: ela deve estar em texto. Essa checagem final dá ao leitor as condições para julgar o dado e mantém a identidade visual no seu papel correto, o de apresentar com clareza uma análise já bem construída.

Uma revisão por outra pessoa deve conseguir reconstruir a leitura sem receber o notebook inteiro em explicação oral. Peça que ela responda qual é a unidade, de onde veio o N, qual período foi medido, o que cada categoria representa e qual conclusão é permitida. Se precisar explicar que uma cor “na verdade” significa outra coisa ou que um eixo omite casos especiais, a figura ainda precisa de rótulos ou texto adicional. Para compartilhar a proposta visual, envie a revisão e o contexto corretos pelos canais autorizados; exportar JSON ou fazer uma captura de tela não converte uma experiência em tema aprovado. Guarde a interpretação perto dos números para que uma alteração futura do visual não apague o significado.

<!-- editorial:exclude:start -->
[Construção do contrato de temas](MANUAL_TECNICO_V2.md#mt23) · [Consumidores e superfícies](MANUAL_TECNICO_V2.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU13](#mu13) · [Próximo: MU15](#mu15) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT23](MANUAL_TECNICO_V2.md#mt23)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu15"></a>
<a id="mu15"></a>
### MU15 — Montar um notebook visual completo

Um notebook visual útil permite descobrir o que foi analisado, de onde vieram os números e qual conclusão eles sustentam. Este roteiro monta uma versão pequena com dados sintéticos: abertura, índice, seções, indicadores, tabela, distribuição e correlação; curvas de modelo entram somente se houver avaliação binária pertinente. Os exemplos partem de uma sessão nova com o pacote `.assistant` disponível e, para a parte distribuída, Spark configurado. HTML é a linguagem que marca elementos de uma página; CSS descreve sua aparência. As funções do Hub que devolvem HTML entregam texto para um renderizador, não uma figura já vista por alguém.

<a id="mu15-1"></a>
#### MU15.1 — Abertura, seções e índice honesto

Comece com uma célula Markdown: título, pergunta, população, unidade de observação, janela temporal, origem dos dados e limite conhecido. Markdown é o texto com títulos `#` e listas que permanece legível sem executar Python. Num notebook de demonstração, escreva “dados sintéticos” perto do título, não só no rodapé de uma figura. Por exemplo, a pergunta “Como saldo e tempo de relacionamento se distribuem e se associam?” não é respondida por um cartão de indicadores sozinho. O leitor precisará ver o recorte, os valores e a ressalva de que uma associação não demonstra causa. Um pequeno parágrafo de orientação reduz a chance de alguém interpretar um gráfico fora de contexto quando abrir o notebook no meio.

Um cabeçalho visual pode vir antes do título, mas não substitui esse texto. O pacote traz os PNGs compartilhados `headers/png/cabecalho_crm.png` e `cabecalho_squad.png`; o [guia de cabeçalhos](hub_readmes_visual_assets/headers/README.md) explica qual usar e como calcular o caminho relativo a partir do documento. Em notebook geral, escolha CRM; no específico da Squad, escolha Squad, sem empilhá-los. A célula Markdown pode exibir a imagem por caminho, sem iniciar compute. Mantenha título, escopo e instruções em texto normal, com alt adequado para a imagem. Ao publicar o notebook por um procedimento autorizado, a árvore de assets precisa acompanhá-lo; uma referência para arquivo ausente renderizará mal mesmo que a célula Markdown esteja correta.

Esboce a sequência real: contexto, descrição de variáveis, qualidade e recorte, distribuição, relações e síntese. O [`index_generator`](hub_snippets/visual/index_generator/README.md) pode imprimir os nomes canônicos de etapas de análise exploratória de dados, também chamada EDA. Ele não examina as células para saber o que foi feito e não cria links clicáveis. Se seu notebook tiver apenas as etapas 0, 4, 5 e 8, peça somente essas. `markdown=True` devolve texto Markdown, que você pode revisar e colocar numa célula de texto; `markdown=False` devolve HTML visual. A versão `_resolvido` aplica um tema apenas no HTML, sem mudar o conteúdo nem criar navegação. Se precisa de navegação clicável, mantenha títulos e âncoras reais no Markdown e teste os links no destino; não atribua essa função ao índice visual.

O bloco a seguir encontra o pacote a partir da pasta atual e de seus pais, como faz o exemplo de tema do Hub. Em uma instalação de workspace cujo caminho não é encontrado, preencha `HUB_ROOT` com a pasta `.assistant` recebida do mantenedor antes de continuar. Ele não instala bibliotecas nem procura dados. As importações de apresentação são declaradas agora para que as próximas células não dependam de variáveis invisíveis:

```python
from pathlib import Path
import sys

HUB_ROOT = ""  # se necessário, informe a pasta .assistant recebida
inicio = Path.cwd()
candidatas = [Path(HUB_ROOT)] if HUB_ROOT else [
    candidato
    for base in [inicio, *inicio.parents]
    for candidato in (base, base / ".assistant", base / "ambiente_databricks/.assistant")
]
raiz_hub = next(
    (p for p in candidatas if (p / "hub_snippets/visual/tema/tema.py").is_file()),
    None,
)
if raiz_hub is None:
    raise RuntimeError("Informe HUB_ROOT com a pasta .assistant do Hub")
sys.path.insert(0, str(raiz_hub))

from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.index_generator import gerar_indice_eda

tema = load_reference_theme("notebook")
indice_textual = gerar_indice_eda(etapas_ativas=[0, 4, 5, 8], markdown=True)
print(indice_textual)
```

O retorno é um rascunho de roteiro, não prova de que as quatro seções existem. Depois de criar cada seção, confira se título e ordem correspondem ao índice; se não houver etapa 5, retire-a. `None` pediria as nove etapas do mapa, e uma lista vazia não mostraria nenhuma. Isso evita um sumário ornamental que promete análises ausentes. A referência carregada é uma configuração sintética e validada de contexto `notebook`, apropriada para os consumidores demonstrados; ela não é uma nova identidade aprovada pela organização. O capítulo [MU14](#mu-mod-mu14) mostra como propor outra cor e aplicar tema a uma figura sem alterar o padrão da sessão.

No texto da abertura, deixe uma nota de reprodução: versão ou data da extração, critérios de inclusão, campos usados e se o notebook consulta uma fonte viva ou uma amostra congelada. Em material sintético, escreva que os números foram inventados somente para ensinar o fluxo; não cite um sistema corporativo como origem. Antes do primeiro gráfico, anuncie o que significa uma linha do conjunto, pois contar linhas, clientes e eventos são operações diferentes. Se a análise tiver execução demorada, separe células de preparação das de apresentação para que o leitor possa reler as conclusões sem acreditar que um bloco HTML recalculou os dados. O índice deve descrever essa ordem real.

<a id="mu15-2"></a>
#### MU15.2 — Orientação visual, badges e indicadores já calculados

Um título Markdown anuncia uma seção para navegação e leitura; [`section_header_html_resolvido`](hub_snippets/visual/section_header/README.md) pode reforçar visualmente a etapa e sua descrição. A função recebe `tema` explicitamente e devolve uma string HTML. `displayHTML` é a função disponível no notebook Databricks para pedir que esse texto seja exibido; em outro ambiente, escolha um renderizador HTML apropriado. O cabeçalho não detecta a etapa real nem certifica que uma análise foi feita. Use `etapa=4` somente diante de conteúdo de análise univariada, e dê `titulo`/`descricao` explícitos quando estiver fora do roteiro do Hub. Um número inválido pode virar um cabeçalho genérico em vez de falhar. Preserve o título Markdown próximo, pois um bloco HTML não deve ser a única pista textual da estrutura.

Um divisor resolve outro problema: separar blocos sem anunciar uma nova análise. `divider_light_resolvido(tema)` e variantes retornam HTML curto. Um badge é uma pequena etiqueta de estado; `badge_status_resolvido("Dados sintéticos", tema, tipo="info")` comunica o texto que você declarou, sem inspecionar uma tabela. `badge_score_resolvido` calcula uma classe por cortes fixos da implementação; não use seu verde como veredicto de negócio sem revisar esses cortes. O HTML desses componentes usa CSS derivado do `ResolvedTheme`, mas só na chamada terminada em `_resolvido`. Carregar o tema não modifica HTML já exibido nem atualiza as funções legadas. Isso permite testar o visual de uma seção por vez.

KPI significa **indicador-chave de desempenho**. O [`kpi_card`](hub_snippets/visual/kpi_card/README.md) monta cartões de valores que você já calculou; não soma linhas, não busca Spark nem verifica fonte ou unidade. O argumento `metricas` é um dicionário de rótulos e textos prontos. Uma boa escolha para a primeira tela é mostrar recorte, total e ressalva curta, e depois oferecer a tabela que sustenta os valores. Formate números brasileiros antes do cartão com `fmt_int`, `fmt_pct`, `fmt_brl` ou `fmt_delta` conforme a unidade. `fmt_pct(0.928)` produz `92,8%` porque, por padrão, recebe uma razão entre 0 e 1; se o valor já vier como 92,8, use `input_scale="percent"`. Guarde a medida numérica para cálculos posteriores. Strings formatadas servem à leitura, não substituem a coluna original.

Esta célula define o único conjunto principal do roteiro: oito observações sintéticas, uma por `id_sintetico`. Cada registro traz equipe, saldo, tempo de relacionamento em meses, variação, volume e estado de resolução. Os dois indicadores são calculados desse conjunto; a tabela e os gráficos da próxima seção reutilizam `registros`. Mantenha um título Markdown “Resumo” na célula de texto anterior. `displayHTML` pode ser chamado várias vezes, mas cada retorno é uma peça visual, não um documento persistido:

```python
from hub_snippets.constants.format_br import fmt_int, fmt_pct
from hub_snippets.visual.section_header import section_header_html_resolvido
from hub_snippets.visual.divider import divider_light_resolvido
from hub_snippets.visual.badge import badge_status_resolvido
from hub_snippets.visual.kpi_card import kpi_card_html_resolvido

registros = [
    {
        "id_sintetico": i,
        "equipe": "A" if i <= 4 else "B",
        "saldo": float(i),
        "tempo_meses": float(2 * i),
        "variacao": -5 if i == 1 else i,
        "resolvido": i not in (4, 8),
        "volume": 1000 * i,
    }
    for i in range(1, 9)
]
total_sintetico = len(registros)
resolvidos = sum(int(r["resolvido"]) for r in registros)
taxa_sintetica = resolvidos / total_sintetico
metricas = {
    "Registros do exemplo": fmt_int(total_sintetico),
    "Resolvidos": fmt_int(resolvidos),
    "Taxa de resolução": fmt_pct(taxa_sintetica),
    "Escopo": "oito observações sintéticas",
}

displayHTML(section_header_html_resolvido(
    tema, titulo="Resumo do exemplo", descricao="Seis resolvidos em oito registros."
))
displayHTML(badge_status_resolvido("Demonstração, não dado real", tema, tipo="info"))
displayHTML(kpi_card_html_resolvido(metricas, tema))
displayHTML(divider_light_resolvido(tema))
```

Há oito registros e seis marcados como resolvidos: 6 ÷ 8 = 0,75, portanto `fmt_pct` mostra `75,0%`. As equipes A e B têm quatro registros cada, com três resolvidos em cada uma; isso dá ao leitor outra forma de conferir o numerador e o denominador na tabela. O formatador só apresenta a razão e o cartão só percorre o dicionário. Se o resumo mostrar uma taxa diferente da contagem detalhada, reconcilie o cálculo antes de alterar a string. O HTML do cartão escapa rótulo e valor como texto, mas isso não dispensa política de dados sensíveis nem revisão da saída. A versão Markdown do KPI existe para texto mais portátil, sem a aparência temática da função HTML. O mecanismo de precisão e localidade dos formatadores está no [manual técnico de formatação](MANUAL_TECNICO_V2.md#mt-mod-mt06).

Para representar um estado analítico, não deixe a cor falar sozinha. Um badge “amostra parcial” com `tipo="warn"` continua sendo uma declaração de quem redigiu; precisa aparecer no texto da seção que explica o recorte. O [guia do badge](hub_snippets/visual/badge/README.md) registra contraste aproximado de 3,99:1 no estilo `warn` legado, abaixo do [requisito de 4,5:1 para texto comum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), consultado em 07/10/2026; não o apresente como componente plenamente acessível. Na rota resolvida, confira a combinação realmente recebida do tema. Para percentuais, pontos percentuais e pontos-base não são a mesma coisa: uma taxa que sobe de 10% para 12% aumentou **2 pontos percentuais**. `fmt_delta(0.02)` formata `+2,0 pp`; `unidade="bps"` muda a escala para pontos-base. O [guia de formatos brasileiros](hub_snippets/constants/format_br/README.md) explica também moeda, decimais, abreviações e limites de precisão. Use o formatador somente depois de decidir qual unidade e escala seus dados realmente têm.

O `ResolvedTheme` usado aqui é uma configuração completa de contexto notebook, validada pelo núcleo. Cada consumidor escolhe apenas os tokens relevantes ao seu HTML. Por exemplo, trocar a cor do título do Plotly não significa que a borda de um cartão ou a linha do divisor mudará da mesma forma. Se uma peça parece diferente das demais, confira qual rota foi chamada antes de concluir que o tema está inconsistente: `section_header_html` sem `_resolvido` continua legado, enquanto `section_header_html_resolvido` usa o argumento `tema`. Os componentes não ficam inscritos num tema global. Isso reduz surpresas entre células, mas exige passar o tema em cada chamada e registrar no notebook qual referência ou proposta está em teste. O [contrato técnico do tema](MANUAL_TECNICO_V2.md#mt-mod-mt23) explica sua resolução; o [mapa de consumidores](MANUAL_TECNICO_V2.md#mt-mod-mt24) mostra quais campos chegam a cada componente.

Também vale distinguir estado e score. `badge_status_resolvido("Revisar unidade", tema, tipo="warn")` usa um tipo que o autor escolheu; não calcula se a unidade está errada. `badge_score_resolvido(80, tema, max=100)` calcula uma razão 0,8 e retorna o estilo `ok` pelos cortes do próprio helper. Esse `ok` é uma regra de apresentação, não autorização para implantar um modelo nem parecer de qualidade de dados. Se sua política usa outro limiar, escreva e implemente a política em lugar próprio, e use um badge de status explícito apenas para comunicar a decisão já tomada. O texto do badge deve permitir a leitura mesmo sem distinguir verde e amarelo.

Pense na composição como uma página com hierarquia: título da seção, uma frase que explique o recorte, cartões de poucos indicadores e só então a tabela ou figura que sustenta a síntese. Aqui o cartão “8 registros” significa oito observações inventadas, cada uma identificada por uma linha de `registros`; não significa oito clientes reais nem oito eventos de uma fonte externa. Numa adaptação, mude o rótulo para a unidade correta. Se uma taxa tiver muitos denominadores possíveis, mostre também o denominador no cartão ou na frase imediatamente seguinte. O resultado HTML pode ser bonito e ainda conter uma métrica mal definida; a validação principal é confrontar cada string com a análise numérica anterior.

<a id="mu15-3"></a>
#### MU15.3 — Tabela pequena, distribuições, correlação e curvas quando couberem

Depois do resumo, mostre os valores que permitem ao leitor conferir a síntese. Para poucas linhas já agregadas, [`display_styled_resolvido`](hub_snippets/display/dataframe_styled/README.md) recebe um **DataFrame pandas**, uma tabela que cabe na memória do processo Python, e devolve HTML. Um DataFrame Spark distribui trabalho e dados entre máquinas; não passe o objeto Spark diretamente ao Styler do pandas. Se a base é grande, agregue ou limite no Spark antes de trazer um resultado pequeno ao **driver**, o processo que coordena a aplicação e mantém a memória local usada pelo pandas e pelo Plotly. Converter a base inteira com `toPandas()` apenas para colorir uma tabela pode exceder essa memória e expor dados que não deveriam sair do processamento distribuído.

Esta célula usa os mesmos oito `registros` criados na seção anterior, sem converter um conjunto real. Assim, a contagem de linhas da tabela pode ser confrontada com o KPI: quatro da equipe A e quatro da B, sendo três resolvidos em cada equipe. `highlight_cols` indica explicitamente onde negativos devem ganhar ênfase; sem ela, o tema muda a aparência do cabeçalho, mas não destaca sinais. `fmt_int` produz texto brasileiro para a coluna de exibição, enquanto `variacao` permanece numérica para a regra de destaque. A string HTML é enviada ao renderizador só depois de produzida:

```python
import pandas as pd
from hub_snippets.constants.format_br import fmt_int
from hub_snippets.display.dataframe_styled import display_styled_resolvido

resumo = pd.DataFrame(registros)
resumo["Volume (texto BR)"] = resumo["volume"].map(fmt_int)
resumo = resumo[[
    "id_sintetico", "equipe", "saldo", "variacao", "resolvido",
    "Volume (texto BR)",
]]
html_tabela = display_styled_resolvido(
    resumo, tema, highlight_cols=["variacao"]
)
displayHTML(html_tabela)
```

Espera-se `1.000` até `8.000` na coluna de volume, um valor por linha, e realce apenas para `-5` na `variacao` do primeiro registro; os números em `registros` permanecem os mesmos. A coluna booleana `resolvido` permite contar seis valores verdadeiros sem confiar no cartão. Uma coluna inexistente em `highlight_cols` pode passar sem aviso, então confira os nomes após qualquer renomeação. O helper reconhece para destaque `int` e `float` negativos, não uma string `"-5"` que apenas parece numérica. Sua saída não habilita escape HTML geral de células: conteúdo textual externo não confiável requer política apropriada antes da renderização. Para uma tabela grande ou com paginação, use outra camada de apresentação; este recurso é para um resultado local pequeno.

Quando a pergunta é “como os valores se espalham?”, a [`distribution_grid`](hub_snippets/display/distribution_grid/README.md) produz histogramas. Um histograma agrupa números em faixas e mostra frequência. A rota `_resolvido` aceita DataFrame Spark, escolhe colunas numéricas, usa `smart_sample` e coleta uma amostra limitada ao driver para desenhar no Plotly. O N no rodapé é o tamanho coletado, não o volume total da população. Uma cauda rara pode não aparecer; se a decisão depende de poucos casos extremos, faça contagens direcionadas no Spark. Escolha `sample_n` e `ncols` para sua pergunta e capacidade do ambiente, mantendo unidade de cada variável e anotando o recorte.

Para a pergunta “duas medidas variam juntas?”, [`correlation_matrix`](hub_snippets/display/correlation_matrix/README.md) calcula uma matriz no Spark e devolve uma figura mais `strong_pairs`, lista de pares cuja **magnitude** da correlação atinge o corte indicado: `abs(coeficiente) >= threshold_highlight`. Assim, com corte 0,8, tanto −0,9 como +0,8 entram; o sinal ainda distingue direção da associação. A função aceita Pearson ou Spearman; no exemplo, Pearson resume associação linear. O código elimina linhas com nulos nas colunas selecionadas antes do cálculo, o que pode mudar a população. O corte seleciona pares para investigação, não elimina variáveis nem prova causalidade. A escala divergente do tema muda a apresentação de valores de −1 a +1, sem alterar os coeficientes. Não use códigos numéricos de categorias como se fossem medidas contínuas com relação substantiva.

O bloco abaixo reutiliza `registros` da primeira célula de indicadores, de modo que tabela, distribuição e correlação representem as mesmas oito observações. Ele só deve ser executado em ambiente no qual PySpark, Plotly, pandas e os requisitos do Hub já estejam disponíveis; criar a sessão ou calcular correlação pode iniciar trabalho Spark. As duas medidas foram construídas proporcionalmente (`tempo_meses = 2 × saldo`), então Pearson deve ser +1, salvo diferença de representação numérica no runtime. Essa expectativa matemática ajuda a conferir o mecanismo, mas a figura gerada em seu ambiente ainda precisa ser vista e interpretada:

```python
from pyspark.sql import SparkSession
from hub_snippets.display.distribution_grid import plot_distributions_resolvido
from hub_snippets.display.correlation_matrix import plot_correlation_resolvido

spark = SparkSession.builder.getOrCreate()
dados_spark = spark.createDataFrame(registros)

grade = plot_distributions_resolvido(
    dados_spark, tema, cols=["saldo", "tempo_meses"],
    ncols=2, sample_n=8,
)
matriz, pares = plot_correlation_resolvido(
    dados_spark, tema, cols=["saldo", "tempo_meses"],
    method="pearson", threshold_highlight=0.8,
)
print("Pares para investigar:", pares)
grade.show()
matriz.show()
```

Mesmo o coeficiente esperado de +1 aqui não deve ser narrado como descoberta: `tempo_meses` foi definido como o dobro de `saldo` no exemplo. Como `sample_n=8` e a fonte tem oito linhas, a grade usa as oito neste roteiro; em bases maiores ela continua amostral. A matriz calcula sobre as oito linhas sem nulos nas colunas selecionadas. Num trabalho real, confira unidade de observação, período, faltantes, valores constantes e possível mistura de segmentos antes de interpretar a matriz. Se uma figura surpreender, compare N, mínimo, máximo e quantis com cálculos apropriados no Spark, em vez de alterar apenas a paleta até a figura parecer convincente. Os dois helpers resolvidos preservam o cálculo das rotas legadas; o tema só entra no layout e nas cores declaradas.

Curvas de avaliação pertencem a um notebook de modelo de classificação binária, não a qualquer EDA. [`curves_plotly`](hub_snippets/ml/curves_plotly/README.md) oferece ROC, Precision–Recall, lift e KS, cada uma com uma pergunta distinta. Suas rotas `_resolvido` recebem arrays locais unidimensionais de rótulos 0/1 e probabilidades finitas em `[0,1]`; a amostra precisa conter **ambas as classes 0 e 1** para que a avaliação faça sentido. Elas não fazem cálculo Spark distribuído nem escolhem threshold de negócio. `n` muda somente o texto no rodapé. O próximo bloco é complementar e independente dos oito registros: seus quatro casos inventados servem apenas para mostrar a API de curvas, sem participar dos KPI, da tabela ou da matriz:

```python
import numpy as np
from hub_snippets.ml.curves_plotly import plot_pr_curve_resolvido

y_true = np.array([0, 1, 0, 1])
y_prob = np.array([0.10, 0.80, 0.40, 0.70])
curva_pr = plot_pr_curve_resolvido(y_true, y_prob, tema, n=4)
curva_pr.show()
```

A figura ilustra precisão e recall em quatro casos inventados, com dois rótulos de cada classe; quatro observações não sustentam um parecer sobre modelo real. A paleta temática dessa família é `palette.curves_legacy`, separada da paleta categórica geral. Um resultado de ROC, PR, lift ou KS não substitui calibração, análise de impacto, escolha do threshold e validação de negócio. Se o notebook não avalia classificação binária, omita as curvas do roteiro e do índice. O usuário não ganha clareza com uma figura tecnicamente válida, porém sem relação com sua pergunta.

Na adaptação a dados reais, preserve a fronteira entre número e texto. `fmt_int(1000)` ajuda a exibir `1.000`, mas essa string não deve voltar à coluna Spark como se ainda fosse uma contagem numérica. `fmt_pct` recebe uma razão por padrão; uma taxa já multiplicada por cem precisa declarar outra escala. A tabela pandas mostra o negativo realçado e a grade usa as medidas `saldo` e `tempo_meses` da mesma fonte, mas cada camada tem um papel: uma explica linhas específicas, outra resume a distribuição. Se o total da amostra não corresponde ao total da população, indique ambos com nomes diferentes. O [detalhe dos formatadores](MANUAL_TECNICO_V2.md#mt-mod-mt06) e o [mapa de consumidores visuais](MANUAL_TECNICO_V2.md#mt-mod-mt24) ajudam a verificar onde há transformação de dados e onde há apenas apresentação.

<a id="mu15-4"></a>
#### MU15.4 — Revisar, compartilhar e exportar com o alcance correto

Antes de compartilhar, percorra o notebook do começo ao fim como leitor novo. O título e o índice correspondem às seções presentes? A imagem de cabeçalho abre a partir daquele caminho? HTML e CSS continuam legíveis na largura real? Uma cor de badge tem texto equivalente? Aqui o cartão deve mostrar oito registros, seis resolvidos e `75,0%`; a tabela deve ter oito linhas, das quais seis com `resolvido=True`, e um único `-5` em `variacao`. N da distribuição é amostra coletada; neste exemplo coincide com oito, enquanto N de uma curva complementar, quando fornecido, é só texto declarado. A matriz mostra associação no recorte após nulos, não uma relação causal. Se uma unidade é porcentagem, diferencie fração `0,75`, percentual `75%` e diferença em pontos percentuais; uma string formatada não resolve confusão de denominador.

Inspecione também em uma largura menor. Cabeçalhos, legendas, rodapés e grades podem colidir mesmo que o Python tenha devolvido objetos válidos. Preserve títulos e explicações em Markdown comum para que o conteúdo essencial não dependa apenas de HTML ou pixels de um PNG. Para gráficos, escreva uma frase que interprete o padrão e outra que registre limite do dado; para a tabela, diga o que significa um valor negativo antes de destacá-lo. Revise rótulos, alt, contraste, ordem de leitura e cores de estados com o público de destino. Uma saída que passou por testes locais de construção não equivale a renderização homologada no Databricks ou em todos os browsers.

Exportar depende do objeto e do formato documentado. `display_styled_resolvido`, cabeçalhos, cartões e badges devolvem HTML, que pode ser mostrado numa superfície compatível; não produzem planilha ou PDF. `gerar_indice_eda(..., markdown=True)` devolve texto Markdown. Uma figura Plotly pode ser serializada localmente para HTML quando essa rota é suportada; o README de `curves_plotly` documenta essa possibilidade e explicita que PNG Plotly, PDF e PPTX não foram homologados para a V07. Não trate `export_theme`, que devolve JSON de configuração em memória, como exportação do relatório. Antes de gravar qualquer arquivo, escolha uma pasta autorizada e confirme se os dados contidos na figura podem ser compartilhados; a figura de distribuição contém os valores coletados no driver, não apenas barras anônimas.

Uma conclusão fiel a este exemplo diria: “Nos oito registros sintéticos, seis foram marcados como resolvidos (75%); o saldo varia de 1 a 8, o tempo de 2 a 16 meses, e os dois têm correlação de Pearson +1 por construção. O primeiro registro tem variação −5, realçada na tabela. Esses números ensinam a conferir a continuidade entre indicador, linha e figura; não descrevem clientes reais nem demonstram causa.” Essa frase não usa a curva PR complementar como evidência do mesmo conjunto. O notebook com texto e chamadas, a evidência dos cálculos e a evidência visual no destino são três entregáveis distintos: a receita está aqui; os dois últimos dependem de conferir o runtime e a superfície reais. Cada função `_resolvido` recebe explicitamente o mesmo `tema` de contexto notebook, cujo contrato está no [manual técnico de tema](MANUAL_TECNICO_V2.md#mt-mod-mt23).

Faça uma revisão de conteúdo em pares, quando o material justificar: peça a outra pessoa que localize a definição de uma linha, a fonte da taxa, a quantidade de registros efetivamente mostrados na distribuição e a diferença entre “fortemente associado” e “causado por”. Não sugira que o revisor aceite uma figura porque a cor parece profissional. Se não conseguir reconstruir um valor do cartão a partir da tabela ou da etapa de cálculo, acrescente o elo antes de apresentar a entrega. Mantenha os valores originais para auditoria; não use HTML gerado nem string brasileira como única cópia do resultado numérico.

Ao transportar a saída, registre o que foi de fato conferido. “HTML gerado” significa que o helper devolveu texto; “figura construída” significa que Plotly montou um objeto; “figura vista no notebook” exige renderização na sessão; “arquivo exportado” exige escrita e leitura desse arquivo. Esses estados não são equivalentes. Um HTML Plotly salvo localmente pode incluir dados usados pelos traces; revise-os e controle o destino antes de compartilhá-lo. Se o notebook for versionado, decida explicitamente se outputs e imagens devem acompanhá-lo, conforme a política do projeto, para não publicar por acidente uma amostra coletada. A presença de um cabeçalho bonito não reduz a responsabilidade por dados, acesso e interpretação.


<!-- editorial:exclude:start -->
[Anterior: MU14](#mu14) · [Próximo: MU16](#mu16) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT24](MANUAL_TECNICO_V2.md#mt24)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu16"></a>
<a id="mu16"></a>
### MU16 — Usar cabeçalhos e figuras dos Visual Assets

Os Visual Assets são imagens editoriais prontas para explicar o Hub. O usuário normalmente escolhe um PNG, aponta o documento para o arquivo compartilhado e mantém a explicação em texto. Este capítulo cobre essa tarefa em README e notebook. O [pacote visual](hub_readmes_visual_assets/README.md) é conteúdo próprio do Hub; a presença de uma imagem no repositório não a instala no workspace nem faz a Genie Code extrair regras dos seus pixels. Para entender a produção dos arquivos, consulte [MT25](MANUAL_TECNICO_V2.md#mt-mod-mt25) e [MT26](MANUAL_TECNICO_V2.md#mt-mod-mt26).

<a id="mu16-1"></a>
#### MU16.1 — Escolher CRM ou Squad e uma figura pela finalidade

Comece pela função da imagem. Um **cabeçalho** identifica o material; uma **figura** esclarece uma relação, sequência ou decisão. Os cabeçalhos aprovados são duas faixas PNG de 1920 × 480 pixels. Para um guia ou notebook geral, use `headers/png/cabecalho_crm.png`, com a identificação “CRM — Missão Modelos Analíticos CRM”. Para um notebook específico da Squad, use `headers/png/cabecalho_squad.png`, que traz “Squad Modelos Analíticos e Preditivos”. Escolha um por documento; empilhar os dois cria duas identidades concorrentes. O [guia dos cabeçalhos](hub_readmes_visual_assets/headers/README.md) mostra os arquivos e o texto exato. Eles são identidade editorial do projeto, não logotipos ou recursos nativos da Databricks. A arte de conexões não representa permissões, execução de código nem disponibilidade de serviços.

Para uma figura, escreva primeiro a pergunta que o leitor precisa responder. “Como fonte, workspace, contexto e notebook se relacionam?” aponta para `raiz/02_arquitetura_ecossistema.png`; “qual a diferença entre medir um problema e impedir uma ação?” aponta para `scripts/04_diagnostico_vs_enforcement.png`; “como descobrir uma skill apropriada?” aponta para `skills/01_descoberta_e_selecao.png`. Essas imagens não substituem o procedimento: a primeira não prova que algo foi publicado; a segunda não transforma todo diagnóstico em bloqueio; a terceira não autoriza inventar um limiar de seleção de skill. Leia a pergunta, o limite e o dono indicados no [`manifest.yaml`](hub_readmes_visual_assets/manifest.yaml) e abra o README ao qual a figura pertence antes de reutilizá-la.

O pacote ativo lista 21 figuras em seis famílias: raiz, assistant, snippets, scripts, skills e prompts. Uma família indica o assunto do README proprietário, não uma coleção decorativa para preencher páginas. Se o seu documento fala de reutilização de snippet, procure na família `snippets`; se fala de prompts, procure em `prompts`. O [índice textual das figuras](hub_readmes_visual_assets/CONTEUDO_FIGURAS.md) permite percorrer as perguntas sem abrir vinte e uma imagens. Se nenhuma figura responde à pergunta, texto simples ou um esquema novo submetido à revisão é melhor que uma imagem inadequada. Escolher pela aparência isolada pode transmitir uma relação diferente da que o texto afirma.

Antes de inserir, confira se o documento contém uma frase que apresenta a pergunta e outra que interpreta a resposta. Num guia para iniciantes, “a fonte versionada é publicada no workspace, enquanto a execução do helper depende de uma chamada no notebook” prepara a leitura da figura de arquitetura. No cabeçalho, mantenha título, público e finalidade em Markdown normal logo abaixo da imagem. Markdown é a marcação de texto com títulos e links; o PNG apenas acrescenta identidade ou síntese visual. Essa separação ajuda quando a imagem não carrega e quando alguém lê o documento por busca ou tecnologia assistiva.

<a id="mu16-2"></a>
#### MU16.2 — Inserir o PNG a partir do documento que o usa

Um caminho de imagem em Markdown tem a forma `![texto alternativo](caminho/arquivo.png)`. O caminho **relativo** é calculado a partir da pasta do documento consumidor. Os segmentos `..` sobem um nível; cada barra seguinte desce a uma pasta. Não comece a contar da pasta do pacote visual se o README que receberá a imagem está em outra pasta. O arquivo canônico permanece em `ambiente_databricks/.assistant/hub_readmes_visual_assets/`; referenciá-lo evita cópias divergentes em cada notebook. O PNG é o arquivo de leitura; `sources/*.svg`, manifesto e registros de qualidade servem à autoria e conferência. Inserir um PNG não importa um módulo Python, não inicia Spark e não executa uma skill.

Considere o `README.md` na raiz deste repositório. Da raiz, o cabeçalho CRM fica dentro de `ambiente_databricks/.assistant/`. A célula ou linha Markdown copiável é:

```markdown
![CRM — Missão Modelos Analíticos CRM](ambiente_databricks/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Guia geral do Hub
```

Já em `ambiente_databricks/.assistant/README.md`, o ponto de partida está **dentro** de `.assistant`; o prefixo `ambiente_databricks/.assistant/` desaparece. Uma figura de arquitetura nesse mesmo arquivo pode ser citada assim:

```markdown
![Corte entre fonte versionada, workspace, contexto, notebook e runtime](hub_readmes_visual_assets/readmes/raiz/png/02_arquitetura_ecossistema.png)

A fonte é publicada no workspace; o notebook só executa código reutilizável quando há uma chamada explícita.
```

Se o consumidor for `ambiente_databricks/.assistant/hub_snippets/README.md`, suba uma pasta antes de entrar nos assets. O exemplo abaixo aponta para um arquivo da família `snippets` que já existe no pacote:

```markdown
![Pasta de snippet com fachada, implementação e exemplo didático](../hub_readmes_visual_assets/readmes/snippets/png/01_anatomia_pasta.png)

O README da pasta apresenta a API; o arquivo Python implementa a função e o exemplo mostra a chamada.
```

Observe a diferença entre os três prefixos: `ambiente_databricks/.assistant/`, `hub_readmes_visual_assets/` e `../hub_readmes_visual_assets/`. Nenhum deles é “o caminho universal da figura”; cada um está correto para o documento nomeado. Se você mover o README de lugar, recalcule os `..` e teste a referência. O mesmo vale para letras maiúsculas e minúsculas, espaços e extensão `.png`: um caminho que parece funcionar num sistema tolerante pode falhar no destino. Não copie uma imagem para contornar um erro de caminho sem verificar onde o documento será lido.

Veja um erro concreto. Em `ambiente_databricks/.assistant/hub_snippets/README.md`, escrever `![Pasta de snippet](hub_readmes_visual_assets/readmes/snippets/png/01_anatomia_pasta.png)` procuraria uma pasta `hub_readmes_visual_assets` **dentro de** `hub_snippets`, onde ela não existe. O endereço correto começa com `../`, sobe à pasta `.assistant` e só então entra no pacote. Para conferir sem adivinhar, localize no explorador de arquivos o README, suba à pasta pai uma vez e percorra o restante do caminho. Se o caminho terminar num diretório, não num arquivo `.png`, faltou parte do nome. Se um link `[abrir imagem](...)` funcionar, isso ainda não significa que a imagem apareceu embutida: o prefixo `!` é o que instrui o Markdown a renderizá-la no corpo do documento.

Em um notebook com célula Markdown, a sintaxe da imagem continua sendo Markdown. Se o notebook estiver salvo na própria pasta `headers/`, o [exemplo oficial do pacote](hub_readmes_visual_assets/headers/README.md) usa `%md` e `./png/cabecalho_squad.png`:

```markdown
%md
![Squad Modelos Analíticos e Preditivos](./png/cabecalho_squad.png)

# Análise da Squad
```

Se o notebook estiver em outra pasta do workspace, ajuste o endereço desde **essa** pasta e confirme que a árvore de assets foi distribuída junto com ele. Um caminho local do repositório não vira automaticamente um caminho válido no workspace. O suporte documentado para imagens de workspace aceita caminhos relativos ou absolutos em células Markdown, mas o modo exato de distribuição do seu projeto precisa ser conferido no destino autorizado. Use o README e a célula como exemplos de localização, não como prova de que qualquer instalação já ocorreu. Também não use prefixo de link entre notebooks, `%run` ou `displayHTML` para mostrar esse arquivo: eles resolvem tarefas diferentes.

Uma forma prática de revisar é ler o caminho da esquerda para a direita. Partindo da pasta do arquivo consumidor, aplique cada `..`, entre nas pastas seguintes e confirme a existência do nome final. Em seguida, abra o documento em sua superfície real e observe se o PNG aparece na largura prevista. Esse segundo passo detecta problemas que a simples presença do arquivo na fonte não detecta, como uma publicação que deixou a pasta de imagens de fora. Se o notebook será compartilhado, peça ao responsável pela publicação que confirme a árvore entregue, mantendo uma única localização canônica para as imagens.

O caminho também não deve ser confundido com a referência editorial ao conteúdo. Uma figura pode estar bem localizada e ainda aparecer no capítulo errado. O manifesto fornece o `owner_readme` e uma âncora do trecho que dá contexto; siga essa indicação para entender o lugar original da imagem. Ao levar a figura a outro documento, acrescente uma frase própria que explique por que ela serve à nova pergunta, além de preservar o limite do contrato. Assim o leitor não precisa adivinhar se a seta representa ordem obrigatória, opção ou simples relação entre componentes.

<a id="mu16-3"></a>
#### MU16.3 — Texto alternativo, legenda e conferência de leitura

O texto entre `![` e `]` é o **alt**, ou texto alternativo. Ele comunica a função da imagem quando os pixels não são vistos, por exemplo por falha de carregamento ou por leitor de tela. Um nome de arquivo, como `02_arquitetura_ecossistema.png`, pouco informa; uma frase como “Corte entre fonte versionada, workspace, contexto, notebook e runtime” já apresenta a relação principal. O alt não precisa transcrever cada rótulo da figura. A **legenda** ou o parágrafo próximo explica a mensagem e, quando necessário, o limite: “a publicação leva arquivos ao workspace; uma chamada explícita no notebook inicia o uso do helper”. Alt e legenda têm papéis complementares. A figura pode ajudar a enxergar o fluxo, mas a regra operável precisa permanecer no texto.

Para o cabeçalho, decida se a identidade já está escrita imediatamente abaixo. Se ela for informação nova, dê alt descritivo, como `![CRM — Missão Modelos Analíticos CRM](...)`. Se o mesmo nome estiver repetido ao lado como título e o banner servir só de decoração, `![](...)` pode evitar leitura duplicada. Não aplique alt vazio a uma figura que explica uma sequência sem equivalente textual. Para uma imagem de diagnóstico e enforcement, por exemplo, escreva no parágrafo o que é apenas medido e o que de fato bloqueia, com o gatilho e o alcance indicados pelo README proprietário. Uma frase “veja a figura” deixa o leitor sem instrução quando a imagem não aparece.

O [`CONTEUDO_FIGURAS.md`](hub_readmes_visual_assets/CONTEUDO_FIGURAS.md) é uma ajuda concreta: para cada figura, traz a pergunta, o alt, os rótulos e a síntese textual. Ao preparar sua página, compare essa síntese com o seu parágrafo. Se a figura disser “contexto explícito” e o texto afirmar “prompt carregado automaticamente”, há conflito que precisa ser corrigido antes do compartilhamento. O índice textual não substitui a explicação do README; consulte o documento proprietário para critérios, sequência e exemplos copiáveis. A Genie Code pode receber contexto de texto, mas não conte com leitura de pixels para descobrir regras ou parâmetros do Hub.

Confira a leitura em quatro passagens. Primeiro, leia o documento sem olhar a imagem: pergunta, instrução e conclusão continuam compreensíveis? Segundo, confira se o alt identifica a finalidade da imagem sem repetir um parágrafo inteiro. Terceiro, abra o PNG na superfície que o usuário realmente usará e examine se títulos, legendas internas e setas continuam legíveis na largura disponível. Quarto, compare a interpretação escrita com os rótulos da figura, inclusive direção de flechas, fronteiras e cores. Cor sozinha não deve carregar “permitido”, “bloqueado” ou “revisar”; acrescente palavras. Uma imagem visualmente limpa ainda pode induzir erro se uma seta ou uma legenda for tratada como uma autorização que não existe.

Os cabeçalhos foram compostos como faixas 1920 × 480 e o guia registra uma composição avaliada com referência de 720 pixels de largura e menor texto calculado em 18 pixels; isso não garante legibilidade ou acessibilidade em toda página que o reutiliza. Uma página pode reduzir demais a imagem ou cortá-la com CSS próprio. CSS é a camada de estilo que controla aparência e dimensão; se o destino a aplica, observe o resultado em largura estreita e larga. Para diagramas, compare a visualização com o texto equivalente, especialmente se a página dimensiona a figura automaticamente. Um alt correto não compensa rótulos minúsculos para quem vê, e uma imagem nítida não compensa um texto alternativo vazio para quem não a vê.

Os registros de manutenção [`tools/readme_visuals/qa/validation.json`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_visuals/qa/validation.json) e [`tools/readme_visuals/qa/headers/validation.json`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_visuals/qa/headers/validation.json) registram verificações da respectiva rodada. Foram separados do pacote instalado; a ausência dessas pastas em `.assistant` não significa que falte um PNG de uso. Eles ajudam o mantenedor a rastrear integridade, mas não demonstram que seu README abriu no navegador, que o notebook está presente no workspace ou que uma pessoa com tecnologia assistiva conseguiu usá-lo. Ao entregar um documento, anote o que foi efetivamente conferido: caminho na fonte, arquivo incluído no destino e imagem vista no contexto de leitura. Se só verificou o primeiro, não declare os outros dois. O [manual técnico dos assets](MANUAL_TECNICO_V2.md#mt-mod-mt25) aprofunda a função dos arquivos e das verificações.

<a id="mu16-4"></a>
#### MU16.4 — Recuperar imagem ausente e encaminhar alterações

Se aparecer um ícone de imagem quebrada, comece pelo documento consumidor. Copie o caminho escrito entre parênteses, identifique a pasta desse documento e siga os segmentos até o PNG. Compare o nome completo, a extensão `.png` e a caixa das letras com o [diretório do pacote](hub_readmes_visual_assets/README.md). O erro mais comum nos exemplos deste capítulo é manter `hub_readmes_visual_assets/...` ao mover uma página de `.assistant/` para `hub_snippets/`: ali falta `../`. Corrigir o prefixo resolve a referência sem duplicar o arquivo. Faça a mesma conferência no destino, porque a fonte pode conter a imagem enquanto a distribuição deixou sua pasta de fora.

Se o caminho estiver certo, pergunte se o PNG foi entregue com o README ou notebook e se o visualizador aceita aquela referência. Em uma célula Markdown de notebook, teste o caminho relativo à localização do notebook; não copie o caminho de outro notebook sem recalculá-lo. Confira também se a imagem não foi apenas ocultada por estilo, recortada ou reduzida a um tamanho ilegível. Um problema de carregamento não pede gerar novamente o desenho de início. Diferencie “arquivo existe na fonte”, “arquivo chegou ao destino” e “arquivo foi visto na página”; cada verificação responde a uma causa diferente. Documente qual etapa falhou ao encaminhar o caso ao mantenedor.

Se a imagem carrega mas está conceitualmente errada ou desatualizada, descreva a pergunta que deveria responder, o trecho textual conflitante e a mudança proposta. Indique o README proprietário e, se houver, o identificador da figura no manifesto. Mudanças em copy, setas ou cores precisam passar pelo fluxo de autoria e revisão; cinco assinaturas e os dois cabeçalhos aprovados têm preservação por hash. Não edite o PNG final para “consertar” o desenho em um único README: isso criaria uma versão paralela sem atualizar os outros consumidores nem o texto equivalente. Uma variante temática V06 gerada localmente é candidata e não substitui o pacote ativo automaticamente.

Para escolher ou trocar uma imagem no documento do usuário, volte à pergunta: o arquivo correto existe, a explicação ao redor está presente e o caminho parte da pasta certa? Se sim, insira o PNG central, abra a página no destino e revise alt, legenda e legibilidade. Se a pergunta requer uma figura nova, entregue ao mantenedor uma proposta com finalidade e limites, sem atribuir publicação ou aprovação ao simples arquivo gerado. O [guia operacional de produção](MANUAL_TECNICO_V2.md#mt-mod-mt26) explica as etapas técnicas; este capítulo encerra no uso e na conferência da imagem que o leitor realmente receberá.


<!-- editorial:exclude:start -->
[Anterior: MU15](#mu15) · [Próximo: MU17](#mu17) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT25](MANUAL_TECNICO_V2.md#mt25)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu17"></a>
<a id="mu17"></a>
### MU17 — Experimentar e entregar uma proposta visual

Uma proposta visual começa com a pergunta “onde esta aparência será vista?”. Um notebook, um painel de comparação, um Databricks App, um dashboard AI/BI e as figuras dos READMEs não recebem as mesmas propriedades de tema nem compartilham o mesmo caminho de entrega. Este capítulo ajuda a escolher a rota, experimentar com dados sintéticos e entregar uma revisão legível. **Salvar uma proposta não a aprova; gerar um arquivo não o publica.** As ferramentas citadas estão integradas no Git no alcance registrado, mas a instalação, o browser, o armazenamento, as permissões e a homologação do destino exigem evidências próprias.

<a id="mu17-1"></a>
#### MU17.1 — Decidir entre consumo, Lab, App, AI/BI e manutenção editorial

Se você quer mudar **uma figura ou componente de um notebook**, comece pelo [MU14](#mu-mod-mu14): carregue um `ResolvedTheme` de contexto `notebook` e passe-o explicitamente a uma função terminada em `_resolvido`. `ResolvedTheme` é a configuração completa e validada que os consumidores do Hub conseguem ler; `_resolvido` identifica a rota que recebe essa configuração. Essa escolha permite comparar uma apresentação sem criar proposta persistida. O [MU15](#mu-mod-mu15) mostra como manter indicadores, tabela e gráficos coerentes na mesma análise. O contrato do tema e o mapa de consumidores estão em [MT23](MANUAL_TECNICO_V2.md#mt-mod-mt23) e [MT24](MANUAL_TECNICO_V2.md#mt-mod-mt24): um token de cor não afeta automaticamente todo objeto que aparece no notebook.

Se a tarefa é **experimentar controles e comparar uma base com uma proposta**, escolha o Visual Lab. Ele é uma interface customizada em notebook, não um menu nativo da Databricks. Usa uma galeria sintética fixa para que diferenças de dados não sejam confundidas com diferenças visuais. A rota permite desfazer, exportar somente a configuração ou salvar uma sessão rastreável em pasta fornecida pelo mantenedor. O Lab não aprova, publica, migra notebooks nem altera dashboards. A necessidade de uma pasta de rascunhos controlada é prática: sem `save_root`, a prévia continua disponível, mas salvar e reabrir não ficam habilitados.

Se o responsável entregou um **Databricks App de autoria visual** já implantado e acesso ao usuário, o App oferece esse percurso sem exigir que ele edite Python. Ele reaproveita o Lab, mas a persistência de produção depende de identidade recebida pelo **proxy**, a camada do Databricks Apps que encaminha ao aplicativo a identidade da pessoa autenticada, e do recurso `theme_storage` ligado a um Unity Catalog Volume. “Volume” aqui é um local de armazenamento governado no ambiente, não o diretório temporário do notebook. Os arquivos do App no Git não demonstram que esses recursos foram configurados. Se o App não foi entregue, use a rota de notebook que esteja disponível ou peça ao responsável a preparação; não troque uma falha de identidade por modo local para simular produção.

Se o destino é um **dashboard AI/BI**, a ponte V11 ajuda a classificar o que o Hub consegue traduzir, aproximar ou deixar sem suporte. Ela recebe um tema `notebook` íntegro e produz uma projeção do Hub. Não existe `context="aibi"` habilitado no schema de temas do núcleo. O JSON de projeção não é um arquivo nativo para o botão *Import theme*. Um candidato nativo depende de um export real de dashboard em estado **draft**, isto é, rascunho ainda editável antes da publicação, no ambiente autorizado e de um mapeamento revisado para campos já existentes. Quem só tem permissão de editar um dashboard não ganha, por isso, permissão para alterar o tema do workspace inteiro ou publicar o dashboard.

Se a mudança é em **cabeçalhos ou diagramas dos READMEs**, use os PNGs aprovados pelo [MU16](#mu-mod-mu16) para consumo comum. Uma cor nova nessa frente pertence a uma variante editorial candidata V06, gerada fora do pacote ativo e revisada por quem mantém os assets. Ela não recolore automaticamente os cinco diagramas de assinatura congelada nem os dois cabeçalhos aprovados. O [MT25](MANUAL_TECNICO_V2.md#mt-mod-mt25) explica os arquivos e o [MT26](MANUAL_TECNICO_V2.md#mt-mod-mt26) explica a produção. Escolher essa rota quando a necessidade era apenas estilizar uma figura Plotly acrescentaria trabalho sem melhorar o notebook.

Antes de avançar, escreva em uma linha: “quero propor mudança em [superfície], comparar contra [base], com [mesmos dados] e entregar [configuração/sessão/candidato] a [responsável]”. Se não consegue preencher a superfície ou o responsável, faça primeiro uma prévia local, sem atribuir a ela estado aprovado. Isso também orienta quais evidências recolher: captura de uma tela pode ajudar a discutir aparência, enquanto um hash e uma sessão permitem rastrear exatamente quais bytes foram salvos. Nenhuma evidência isolada responde a todas as perguntas.

<a id="mu17-2"></a>
#### MU17.2 — Abrir o Visual Lab, ajustar, comparar e exportar JSON

Na cópia autorizada do Hub, abra a pasta `hub_snippets/visual/theme_lab/` e leia o [guia de primeiro uso](hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md). O mantenedor deve entregar o pacote `.assistant` completo e as dependências permitidas pelo ambiente; copiar só `theme_lab.py` não basta. O exemplo `exemplo_theme_lab.py` serve de notebook de entrada. Primeiro confirme que a sessão Python consegue importar o Hub; o preparo de `HUB_ROOT` do [MU15](#mu-mod-mu15) mostra uma forma de localizar a pasta `.assistant`. Depois, se houver pasta regular de rascunhos já existente e autorizada, use o launcher. No bloco abaixo, substitua o placeholder pelo caminho entregue pelo mantenedor antes de executar:

```python
from pathlib import Path
from IPython.display import display
from hub_snippets.visual.theme_lab import build_theme_lab_launcher

PASTA_DE_RASCUNHOS = Path("/CAMINHO/AUTORIZADO/EXISTENTE")
if not PASTA_DE_RASCUNHOS.is_dir():
    raise RuntimeError("Peça ao mantenedor a pasta de rascunhos existente")

launcher = build_theme_lab_launcher(save_root=PASTA_DE_RASCUNHOS)
display(launcher.root)
```

Se a intenção é apenas comparar e nenhuma pasta foi entregue, use `build_theme_lab_launcher()` sem `save_root`; a experiência de prévia funciona, mas os botões de persistência e reabertura ficam indisponíveis. Não crie por conta própria uma pasta na fonte `.assistant` ou um destino compartilhado para “habilitar” salvamento. O caminho de sessão não concede permissão, não descobre controle de acesso e não publica um tema. No launcher, escolha **Ponto de partida** e clique **Abrir ponto de partida**. Referências empacotadas aparecem marcadas como “demonstração”; são úteis para aprender a interface, não prova de tema institucional aprovado.

Na área **Escolher e ajustar**, altere um campo habilitado, por exemplo **Cor principal**. Um valor hexadecimal tem `#` seguido de seis dígitos, como `#112233`. Clique **Aplicar na prévia**. A operação valida todos os campos habilitados em conjunto; se houver erro, a última proposta válida continua ativa. Campos desabilitados mostram por que aquela propriedade não tem consumidor na galeria, em vez de fingir que toda mudança produzirá efeito. “Restaurar este campo” muda o formulário; é preciso aplicar de novo para a proposta refletir o valor. “Desfazer” volta ao estado aplicado anterior. “Restaurar ponto de partida” volta à base original e pode pedir confirmação se descartar trabalho em memória.

Abra **Comparar** e percorra cabeçalho, cartão de indicador, barras, série temporal, mapa de calor e tabela. Base e proposta devem mostrar os mesmos dados sintéticos, nomes e ordem; diferenças permitidas nessa comparação são visuais. Um cartão mais legível não prova que a métrica real está correta. Registre onde o contraste, os rótulos, os negativos e os nulos ficaram melhores ou piores. A galeria completa usa o modo claro (*light*); não trate a prévia como homologação de modo escuro ou alto contraste. Se os controles aparecem mas as figuras não, o guia orienta o mantenedor a usar `compare_preview(draft)` para distinguir problema de frontend de problema da proposta, registrando runtime e navegador. Não instale JavaScript arbitrário para forçar a tela.

Faça uma revisão pequena antes de salvar. Suponha que a proposta troque a cor principal para `#112233`. Compare primeiro um elemento onde essa cor é consumida e anote a diferença vista; depois percorra a tabela e os gráficos que podem usar outros tokens. Se uma peça não mudou, verifique no mapa do consumidor se ela realmente lê `brand.primary`, em vez de declarar que a aplicação falhou. Se uma etiqueta perdeu contraste, registre o local, a cor de fundo e o texto afetado; corrigir só o hex sem olhar a combinação pode criar outra falha. Confirme que uma linha negativa, um valor nulo e a ordem das categorias continuam idênticos entre as duas colunas da comparação. Assim a revisão responde a uma pergunta verificável: o ajuste melhora a leitura pretendida sem alterar o conteúdo?

Para **exportar só a configuração**, use **Exportar JSON** ou `save_proposal()` no fluxo apropriado. JSON é o formato de pares de nomes e valores que preserva a proposta; ele não guarda necessariamente a base nem a sequência de mudanças. `export_theme` do núcleo também devolve bytes em memória, o que não é a mesma coisa que salvar num diretório. Se a intenção é continuar a autoria em outra sessão, escolha **Salvar sessão rastreável**. O Lab grava `base.json`, `proposal.json`, arquivos `history_000.json` e, por último, `session.json` com revisão e hashes. Um hash SHA-256 permite conferir se bytes mudaram desde o registro; não é assinatura de aprovação. O salvamento recusa nome já existente e campos editados mas ainda não aplicados. Um recibo de sucesso indica persistência local da sessão, não submissão. O guia e a implementação correntes usam o sublinhado mostrado aqui; registros anteriores com hífen devem ser interpretados como nomenclatura histórica.

Ao reabrir, escolha a sessão no campo **Reabrir** e clique **Reabrir sessão**. O Lab revalida base, proposta, histórico e hashes, preservando a base original; a proposta antiga não vira base nova por conveniência. Um `LAB_SESSION_HASH` indica divergência de bytes e exige inspeção, não alteração manual do hash. `LAB_SAVE_ROOT` aponta raiz de rascunhos inválida ou não acessível; `LAB_SESSION_MISSING` indica que a sessão escolhida não foi encontrada. `LAB_SAVE_EXISTS` ou `LAB_SESSION_EXISTS` pede outro nome. O guia anterior chama o campo de “Sessão salva” e menciona `LAB_SESSION_ROOT`, mas o código atual usa **Reabrir** e não emite esse último código. Se só `dbutils.widgets` estiver disponível, o fallback documentado cobre controles primários, mas exige reexecutar a aplicação e não oferece o catálogo de sessões com a mesma ergonomia. Um teste Python da lógica ainda não comprova o comportamento do frontend Databricks, teclado, leitor de tela ou facilidade de uso por iniciante.

Ao entregar a sessão a outra pessoa, informe qual base foi aberta, qual revisão foi salva e quais controles foram aplicados. Uma alteração digitada e não aplicada não pertence ao estado persistido. Peça ao revisor que reabra a sessão com o mesmo pacote e confira se a base permanece base e se a proposta reproduz a comparação. Se ele recebeu apenas o JSON avulso, explique que o histórico de tentativas não viaja com esse arquivo; não anuncie “sessão reaberta” sem `session.json` íntegro. O recibo e o hash rastreiam o conteúdo do arquivo, mas a aprovação estética e a instalação no destino continuam decisões separadas.

Para usar no notebook **a mesma proposta salva**, substitua `NOME_CONFIRMADO` pelo nome do recibo e recupere a sessão na pasta autorizada já definida acima. A função abaixo devolve o rascunho validado: `current` contém sua proposta, enquanto `base` conserva o ponto de partida original.

```python
from hub_snippets.visual.theme_lab import reopen_theme_lab_session

rascunho = reopen_theme_lab_session(PASTA_DE_RASCUNHOS, "NOME_CONFIRMADO")
referencia = rascunho.base
tema_proposto = rascunho.current
```

Continue com a figura e as duas chamadas de `aplicar_tema_resolvido` de [MU14.3](#mu14-3), usando essas variáveis. Nesse exemplo, substitua a linha que carrega a referência e o bloco que cria outra proposta (`to_dict`, alteração da cor e `resolve_theme`) pela recuperação acima. Conserve os mesmos dados, as cópias da figura e `fig.show()`. Assim você compara a base original com a proposta reaberta, sem recriar uma configuração diferente. A recuperação não ativa padrão global, publica ou homologa o tema; se houver erro de sessão, resolva-o antes da aplicação.

<a id="mu17-3"></a>
#### MU17.3 — App de autoria e ponte AI/BI: o que cada uma entrega

No App V10, o caminho para o usuário só começa **se** o responsável confirmou implantação, acesso, identidade pelo proxy e armazenamento `theme_storage` em Unity Catalog Volume. Abra então a interface entregue: escolha um ponto de partida na barra lateral, clique **Abrir novo rascunho**, ajuste controles e use **Aplicar e validar proposta**. A configuração inteira é validada antes de substituir a última proposta válida. Compare **Base** e **Proposta** sobre a mesma galeria sintética, inclusive negativos e nulos; o objetivo é julgar aparência, não medir desempenho analítico. O [guia do App](hub_padroes/identidade_visual/databricks_app/GUIA_PRIMEIRO_USO.md) descreve os nomes das telas e como retomar. Abrir outro rascunho descarta só mudanças ainda não salvas na sessão atual, não apaga uma sessão anterior persistida.

Para salvar no App, informe um nome simples e clique **Salvar sessão**. Confirme o recibo com nome, revisão, profundidade do histórico e prefixo do hash; sem confirmação, não presuma persistência. Uma sessão com mesmo nome não é sobrescrita. A área **Retomar** lista sessões do **namespace** da identidade atual: uma pasta de sessões separada para aquela pessoa, derivada de um hash, sem pôr seu identificador bruto no caminho. O namespace organiza as sessões oferecidas pelo App; o hash não cifra conteúdo nem substitui ACL do Volume ou impede acesso administrativo já autorizado. Ao reabrir, hashes são conferidos antes de reconstruir base, proposta e histórico; sessão parcial ou adulterada é recusada. Não há botões de aprovar, rejeitar, publicar, promover, ativar como padrão ou apagar histórico. Essa ausência é parte da fronteira `authoring_only`. `APP_IDENTITY_MISSING`, `APP_STORAGE_MISSING`, `APP_STORAGE_NOT_VOLUME` e `APP_STORAGE_UNAVAILABLE` pedem conferência do responsável; um erro `LAB_` vem da camada de sessão compartilhada com o Lab. Não envie token, não mude hash e não troque o Volume por `/tmp` para contornar uma falha.

Em AI/BI, a primeira saída do Hub é outra: uma **projeção auditável** de um `ResolvedTheme` de contexto `notebook`. A matriz V11 classifica 48 tokens em 3 `translated`, 23 `approximated` e 22 `unsupported`. “Translated” significa que há correspondência nativa suficientemente direta; “approximated” indica capacidade parecida cuja interpretação precisa ser revista; “unsupported” registra lacuna. Apenas três correspondências `translated` com estratégia `direct` podem receber **binding**, um mapeamento revisado de capacidades do Hub para campos existentes no JSON nativo. A projeção tem identificador `hub-aibi-theme-projection`, formato do Hub, e **não** é JSON nativo importável pelo Databricks. O [guia AI/BI](hub_padroes/identidade_visual/aibi/GUIA_PRIMEIRO_USO.md) separa essa preparação local da edição de um dashboard real.

As três correspondências diretas são concretas: `surface.card` para fundo de widget, `palette.categorical` para paleta categórica de visualização e `card.radius_px` para raio do canto do widget. Isso não significa que a ponte saiba onde estão esses campos em qualquer export nativo. `brand.primary` para cor de seleção é uma **aproximação**: nomes parecidos não tornam as semânticas idênticas. `brand.accent` permanece sem capacidade alvo segura na matriz. Ao ler uma projeção, procure a classe e a justificativa de cada token, não apenas um valor hexadecimal. A regra protege contra uma aparência parcialmente aplicada que seria anunciada como tema completo.

Se houver permissão para um dashboard **draft**, o percurso de candidato nativo começa no destino: abra *Settings → Theme → Export theme*, preserve o JSON original e registre seu SHA-256. Um mantenedor técnico revisa esse export e escreve um binding com JSON Pointers para campos que já existem nele. JSON Pointer é um endereço dentro de um documento JSON, como uma sequência de chaves; a ponte não adivinha o schema. `bind_native_template()` confere o hash exato do export, recusa caminho ausente e só substitui as três capacidades diretas permitidas. O arquivo produzido ainda é **candidato local** até ser testado com *Import theme* no próprio destino autorizado. Se a importação falhar, preserve o original, registre a diferença e revise binding/template; não force uma aproximação a passar como tradução.

Na revisão do dashboard, mantenha datasets, consultas, filtros, campos, agregações, unidades e ordenação idênticos. O fixture `dashboard_sintetico.json` é roteiro local para inspecionar KPI, série, barras, tabela, texto e filtros, não um arquivo Databricks importável. Compare o resultado em claro e escuro, observando paleta, texto, fundos, bordas, seleção, gradiente e mapeamentos locais de cor. Itens `approximated` exigem decisão explícita; `unsupported` continuam sem tradução. **Tema de workspace** e **tema de dashboard** são superfícies diferentes: o primeiro exige administrador, enquanto um dashboard existente recebe um snapshot quando ele é aplicado. Mudanças posteriores no tema do workspace não atualizam automaticamente esse dashboard. Importar um tema e publicar um dashboard também são ações separadas; a V11 não faz nenhuma das duas por você.

Há duas verificações que devem aparecer juntas no registro. A primeira é de **conteúdo**: confirme que uma barra ainda representa o mesmo campo, que o filtro seleciona a mesma população e que o KPI conserva numerador, denominador e unidade. A segunda é de **aparência**: observe o mesmo widget com a proposta e com o tema anterior, de preferência em dimensões e modos de visualização pertinentes ao uso. Uma cor específica por valor em *Color mappings* pertence ao dashboard, não se propaga automaticamente a todos os objetos pela paleta do Hub. Se um item da matriz era `approximated`, documente qual decisão manual foi tomada e por quem; se era `unsupported`, deixe a lacuna visível. Não atribua a um arquivo candidato o resultado de um teste que ainda depende do botão *Import theme* no workspace.

O estado importa ao descrever essas rotas. O índice vivo e a nota administrativa V14 de 06/10/2026 registram V00–V13 e V14 S0/S1 integradas no Git; S1 entrou pela PR #72 em 16/09/2026. Os rótulos de candidata no corpo histórico preservam o estágio pré-merge. S2–S8 não possuem início comprovado, e os slots operacionais seguem `BLOCKED` sem autoridade evidenciada. Há teste local e documentação para Lab, App e ponte AI/BI; isso não substitui instalação, frontend, identidade, Volume, importação nativa, acessibilidade ou aceite no ambiente corporativo. `A11-01` permanece `FAIL`: numa revisão real de um dashboard draft com dados sintéticos, dois pares de texto e fundo da formatação condicional `cellFormat` ficaram abaixo do contraste exigido de 4,5:1 para texto comum, apesar de a pessoa não ter percebido problema. O [registro da medição](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V12/TESTES.md) preserva esse achado na issue #57; `cellFormat` não é uma das três capacidades diretas da ponte V11. Os gates `V12-LAB-01`, `V12-APP-01`, `V12-AIBI-02` permanecem bloqueados por autorização na [situação V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). A palavra “integrado” descreve o estado do código no Git, não autorização de operação. Quando um README da época ainda diz “candidata”, consulte também esse registro de estado posterior para não confundir data de autoria do guia com o alcance atual.

<a id="mu17-4"></a>
#### MU17.4 — Variante editorial, revisão, evidência e encaminhamento

Quando a proposta diz respeito a um diagrama ou cabeçalho usado em README, comece identificando o PNG ativo e o texto equivalente. O [MU16](#mu-mod-mu16) ensina a escolher pela pergunta e apontar para o arquivo central. Para mudar a aparência do pacote editorial, o mantenedor pode usar a rota V06: um `theme_id` canônico é resolvido pelo núcleo de temas, e o compositor grava uma **variante candidata** em `.artifacts/visual-v2/theme-variants/`, fora de `hub_readmes_visual_assets/`. `SOURCE_DATE_EPOCH` fixa a referência temporal da geração reproduzível do manifesto. O [guia técnico da rota](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_visuals/README.md) mostra os comandos, e o [MT26](MANUAL_TECNICO_V2.md#mt-mod-mt26) explica o mecanismo. O usuário que só precisa colocar uma figura no documento continua usando o PNG ativo, sem executar gerador.

Na comparação, peça ao mantenedor três coisas concretas: o identificador e a pergunta da figura, o PNG vigente com seu hash e o PNG candidato com seu hash. Veja ambos na largura em que o README é lido; confira rótulos, setas, contraste, legenda e texto alternativo. Pergunte se alguma mudança de cor alterou a leitura de estado ou procedência. Nos assets paramétricos, bytes idênticos ao ativo podem ser classificados como `parametric_equivalent`; bytes alterados pedem `variant_review_required` e nova revisão antes de promoção. Os cinco diagramas de assinatura aprovada são entradas congeladas, copiadas sem reinterpretar o desenho; a rota não os recolore. Os dois cabeçalhos canônicos também permanecem preservados. Um manifesto candidato registra classificação e política da geração, não a aprovação de uma pessoa nem publicação no workspace.

Uma entrega útil de proposta visual reúne origem, alteração e alcance. Anote a base usada, contexto e modo do tema, versão/fingerprint, tokens alterados e componentes realmente comparados; mantenha os mesmos dados sintéticos entre Base e Proposta. Se for Lab, inclua recibo e hash da sessão ou JSON avulso, dizendo qual dos dois foi salvo. Se for App, inclua apenas recibo e códigos de erro necessários, nunca identidade bruta ou token. Se for AI/BI, inclua projeção, classificação das capacidades, export nativo original com SHA-256 e binding revisado; o candidato resultante não prova importação. Se for asset editorial, inclua ID da figura, hashes, escala de inspeção e texto equivalente atualizado. Esses registros permitem a outra pessoa reconstruir o que foi proposto sem assumir que uma captura de tela conta toda a história.

Ao encaminhar, use palavras de estado precisas: “proposta salva no Lab”, “sessão reaberta”, “candidato nativo gerado”, “PNG candidato comparado” ou “imagem vista no notebook”. Cada uma sustenta uma afirmação diferente. Não escreva “aprovado” porque a configuração passou no schema, “publicado” porque um arquivo existe em `.artifacts`, nem “homologado” porque a galeria sintética abriu localmente. O [estado V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md) mantém slots de autoridade operacional bloqueados quando falta evidência versionada; um owner técnico documentado não vira automaticamente aprovador, publicador ou autoridade de go-live. Entregue a proposta e as limitações ao responsável real pelo destino, segundo a política do ambiente.

Se a revisão apontar problema, volte à fonte da proposta, não ajuste o registro de evidência para escondê-lo. Corrija um campo no Lab e salve outra sessão; no App, crie revisão ou sessão conforme a interface; em AI/BI, reexporte o template se o formato nativo mudou e revise os JSON Pointers; em assets, encaminhe correção ao compositor e confira o novo PNG. Depois repita apenas as verificações afetadas e registre o que foi feito de fato. O ponto de chegada deste capítulo é uma proposta compreensível, rastreável e limitada ao seu escopo. Decisão de aprovação, instalação, publicação e aceite operacional pertencem aos fluxos e autoridades próprios.

<!-- editorial:exclude:start -->
**Consulta de plataforma — 07/10/2026:** [temas de workspace](https://docs.databricks.com/aws/en/ai-bi/admin/themes) e [configurações de dashboard](https://docs.databricks.com/aws/en/dashboards/manage/settings). A documentação sustenta administração, snapshot, draft e import/export; não atesta a interface ou as permissões deste leitor.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU16](#mu16) · [Próximo: MU18](#mu18) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT26](MANUAL_TECNICO_V2.md#mt26)
<!-- editorial:exclude:end -->

<!-- editorial:exclude:start -->
<a id="parte-mu-vi"></a>
## Parte VI — Criação, distribuição e diagnóstico
<!-- editorial:exclude:end -->


<a id="mu-mod-mu18"></a>
<a id="mu18"></a>
### MU18 — Documentar, criar e auditar objetos do Hub

Um objeto do Hub precisa ser compreensível antes de ser copiado para outro notebook ou entregue a outra pessoa. Aqui, **objeto** é um dos seis formatos mantidos em `.assistant`: README, snippet, script, prompt, notebook ou skill. Os templates são moldes de autoria; não calculam, homologam ou publicam por si. Escolha a tarefa primeiro: explicar um notebook, transformá-lo em conteúdo reutilizável, documentar sua [interface de programação de aplicações (API)](MANUAL_TECNICO_V2.md#mt27-1) ou auditar a evidência de uso. O catálogo técnico em [MT05](MANUAL_TECNICO_V2.md#mt-mod-mt05) ajuda a localizar recursos existentes; [MT27](MANUAL_TECNICO_V2.md#mt-mod-mt27) explica o alcance das verificações locais.

<a id="mu18-1"></a>
#### MU18.1 — Comentar notebook ou ensinar seu contexto

Há duas saídas diferentes para um notebook difícil de ler. Quando alguém precisa que a próxima pessoa encontre objetivo, entradas, transformação e interpretação **dentro do próprio arquivo**, use comentário em células `%md`. Quando a tarefa é aprender o funcionamento de um trecho ou diagnosticar uma dúvida, peça uma explicação no chat. Em ambos os casos, apresente o notebook ou trecho com `@`/Add Context, diga o público e se há saídas de execução observadas. Uma frase como “esta consulta encontrou 35 mil linhas” só cabe no texto final se houver resultado correspondente; sem execução, marque a observação pendente.

<a id="uso-hub-ml-comentar-notebook"></a>
<!-- usage-card:start hub-ml-comentar-notebook -->
##### Ficha de uso — comentar notebook

Escolha [`hub-ml-comentar-notebook`](skills/hub-ml-comentar-notebook/SKILL.md) quando o entregável deve ser o mesmo notebook, agora legível para revisão e manutenção. Forneça o arquivo, objetivo da análise, público, tabelas ou DataFrames de entrada, parâmetros, saídas existentes e células cujo comportamento deve permanecer intacto. A skill mapeia dependências entre células e insere Markdown prévio em transformações importantes, validações e decisões; o texto posterior interpreta somente resultados observados. Imports triviais e displays isolados não precisam de um comentário por célula. O cabeçalho identifica escopo, entradas, saída, pré-requisitos e limitações sem inventar proprietário ou ambiente.

O entregável é o notebook com `%md` antes ou depois dos blocos materiais e uma lista separada de inconsistências encontradas. Confira o diff das células de código: ordem, linguagem, parâmetros, lógica e resultados existentes devem permanecer como estavam, salvo pedido explícito em contrário. Verifique se cada nome de tabela e métrica no Markdown existe no arquivo ou na evidência fornecida. Se a célula não rodou, escreva `PENDENTE`, não uma contagem imaginada. Para aprofundar a lógica sem mudar o arquivo, use a rota do tutor abaixo.

Pedido copiável:

```text
@hub-ml-comentar-notebook Documente @<notebook> para <público>. Objetivo: <objetivo>. Preserve código, ordem e parâmetros; adicione contexto antes e interpretação após blocos materiais. Use apenas saídas observadas; marque o resto PENDENTE.
```
<!-- usage-card:end hub-ml-comentar-notebook -->

<a id="uso-hub-ml-tutor-databricks"></a>
<!-- usage-card:start hub-ml-tutor-databricks -->
##### Ficha de uso — tutor Databricks

Escolha [`hub-ml-tutor-databricks`](skills/hub-ml-tutor-databricks/SKILL.md) quando você precisa entender um bloco, um erro ou um fluxo inteiro antes de modificá-lo. Dê o trecho ou notebook, o objetivo do exercício, sua familiaridade com Spark, entradas, unidade de cada linha e stack trace se houver erro. Informe versão e ambiente quando disponíveis; o tutor deve declarar incerteza quando uma capacidade depende deles. A explicação começa pelo que o bloco produz, agrupa operações por finalidade e distingue transformação lazy de ação que executa Spark, shuffle e coleta no driver.

O entregável fica no chat: uma leitura progressiva de entradas, lógica, saída, custo e uma pequena forma de conferir schema, chaves e contagens. Em erro, procure a exceção raiz e proponha o menor diagnóstico seguro, sem transformar hipótese em causa comprovada. Confira nomes de APIs e colunas contra o trecho original; peça um exemplo sintético se a explicação estiver abstrata. A presença de uma célula não prova que ela executou. Uma analogia de [relacionamento com clientes (CRM)](skills/hub-ml-tutor-databricks/SKILL.md) pode ajudar depois da explicação técnica, identificada como analogia. Para gravar a narrativa no notebook, a skill de comentar tem outro entregável.

Pedido copiável:

```text
@hub-ml-tutor-databricks Explique @<trecho> para iniciante: objetivo, grão da entrada, transformação, ação Spark, saída e custo. Mostre um teste pequeno e separe intenção de resultado observado.
```
<!-- usage-card:end hub-ml-tutor-databricks -->

Os templates de comentário incluem cabeçalho, pré e pós em formas completas ou compactas. Eles orientam densidade, não obrigam um bloco de texto para cada célula. `doc_coverage` pode medir cobertura e componentes visuais podem melhorar navegação, mas citar um helper na resposta não significa que ele foi importado ou chamado. Para o tutor, `safe_display`, `smart_sample` e `format_br` são referências úteis quando o trecho lida com volume, amostragem ou apresentação; o contrato do helper precisa ser lido antes de explicar seu comportamento.

<a id="mu18-2"></a>
#### MU18.2 — Escolher template e criar um dos seis tipos

Antes de criar, pergunte **qual problema será reutilizado**. Uma função importável pertence a snippet; uma tarefa explícita de inspeção, transformação ou governança, com efeitos declarados, a script; um briefing para conversa, a prompt; a entrada de uma coleção, a README agregador; uma demonstração executável, a notebook; um método de trabalho para o agente, a skill. `auditoria/`, `output/` e identidade visual são padrões transversais, não tipos adicionais. O [índice de templates](hub_padroes/README.md) fornece o molde e um exemplo preenchido para cada tipo. Pesquise objeto equivalente antes de inventar nome ou seção. Se houver sobreposição, a decisão de criar recorte novo precisa ser explícita; ampliar objeto existente é outra tarefa.

<a id="uso-hub-ml-criar-objeto"></a>
<!-- usage-card:start hub-ml-criar-objeto -->
##### Ficha de uso — criar objeto

Escolha [`hub-ml-criar-objeto`](skills/hub-ml-criar-objeto/SKILL.md) quando uma solução já concebida precisa entrar no Hub com tipo, pasta, documentação e exemplo coerentes. Forneça objetivo, consumidor, nome, entrada, saída, limites, exemplo sintético e a busca de capacidade existente. A escolha entre os seis tipos deve ser confirmada antes da criação; para snippet, informe a seção. Uma pergunta apenas sobre formato pode receber orientação, sem iniciar [checagem prévia de contexto (preflight)](skills/hub-ml-criar-objeto/scripts/preflight.py) de escrita. Na conversão, declare origem e destino, preservando comportamento até decisão específica.

O entregável proposto pode reunir README local, fachada `__init__.py`, módulo e notebook de exemplo, conforme o template do tipo. Confira primeiro o resultado desse preflight, que resolve nome, template e caminho sem escrever. Para cinco tipos de `create` — snippet, script, prompt, notebook e README agregador — a [policy L3/audit](hub_padroes/skill_enforcement/policy.json) governa a skill; a validação do pacote no Git pode bloquear inconsistências e, quando válida, emitir um recibo verificável (Receipt). `skill` e `convert` ficam fora dessa rota. Mesmo com Receipt válido, autorizar e aplicar são passos separados. O piloto de escrita local só cobre **um README agregador novo** em pasta existente. Verifique no resultado quais arquivos realmente foram gerados, validados ou escritos; não aceite “criei os seis tipos” como conclusão genérica.

Pedido copiável:

```text
@hub-ml-criar-objeto Tenho <função/diagnóstico> repetido em <contextos>. Procure equivalente, proponha um dos seis tipos, nome e seção; confirme comigo antes de criar. Use @<template>, entrada/saída e exemplo sintético. Diga quais gates foram observados.
```
<!-- usage-card:end hub-ml-criar-objeto -->

<a id="uso-hub-ml-pipeline-builder"></a>
<!-- usage-card:start hub-ml-pipeline-builder -->
##### Ficha de uso — planejar pipeline

Escolha [`hub-ml-pipeline-builder`](skills/hub-ml-pipeline-builder/SKILL.md) quando o pedido é uma infraestrutura recorrente de ingestão, transformação ou scoring, com orquestração e operação. Informe origem, grão, volume, frequência, latência, [acordo de nível de serviço (SLA)](skills/hub-ml-pipeline-builder/SKILL.md), cloud, workspace, Unity Catalog, ambientes, política de reprocessamento e responsáveis. Uma camada bronze/silver/gold só ajuda se cada fronteira tiver contrato; não peça três camadas vazias. A skill pode propor Lakeflow pipelines, que estende o framework Apache Spark Declarative Pipelines, para fluxo declarativo, Lakeflow Jobs para orquestração e Declarative Automation Bundles para recursos por ambiente, conforme capacidades verificadas.

O entregável é uma especificação implementável: [grafo acíclico dirigido (DAG)](skills/hub-ml-pipeline-builder/templates/pipeline_spec.md), contratos de datasets, chaves e tempo de evento, regras de qualidade, estratégia incremental e reprocessamento histórico (backfill), observabilidade, matriz de ambientes e checklist de implantação. Confira se as expectativas declaram observar, descartar ou falhar com justificativa; se o checkpoint de progresso e a pasta de evolução de schema ficam em armazenamento governado, nunca efêmero; e se dados tardios têm reprocessamento e o retorno à versão anterior (rollback) tem responsável e critério. Helpers de qualidade podem informar protótipo, mas não substituem expectation monitorada no pipeline. Um plano não é deploy: `validate`, `deploy` e `run` exigem ambiente, credenciais, permissão e autorização próprios. Se a pergunta era apenas explicar um notebook, escolha o tutor, não uma arquitetura nova.

Pedido copiável:

```text
@hub-ml-pipeline-builder Planeje pipeline para <objetivo> com dados sintéticos. Origem <...>, grão <...>, SLA <...>, volume <...>, ambientes <...>. Entregue DAG, contratos, qualidade, backfill, testes e rollback. Não implante sem autorização.
```
<!-- usage-card:end hub-ml-pipeline-builder -->

A skill de pipeline também possui [perfis sintéticos delimitados](skills/hub-ml-pipeline-builder/scripts/README.md): preflight de especificação, execução Spark local e probe Delta autorizado no Free. A existência desses runners não transforma o pedido de planejamento em permissão de execução. A [reconciliação B1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/skill_enforcement_rollout/B1_GATES_POS_MERGE_2026-10-01.md) registra aceite parcial do escopo A sintético; a policy mantém Pipeline Builder em `L0`, alvo `L4`. Orquestração Genie, promoção de nível e ambiente corporativo continuam gates separados.

O fluxo de criação tem camadas distintas. A policy vigente coloca `hub-ml-criar-objeto` em **L3/audit**; o `SKILL.md` preserva a descrição do preflight L2 e o rótulo de candidata na superfície de validação estrutural, enquanto seu piloto de escrita já remete ao nível L3/audit vigente. A policy determina o nível atual, enquanto o escopo de cada ferramenta delimita o que foi demonstrado. `preflight.py` reconhece os seis tipos e bloqueia falta de `type_confirmed` ou de busca de equivalente. `ser01_object_validation.py`, no Git, valida cinco tipos de pacote em clone/overlay e vincula base, candidato e run num Receipt. Para snippet e script, também confere cobertura de `api_publica.py`, que extrai nomes públicos do módulo por [árvore sintática de Python (AST)](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/api_publica.py) sem importá-lo e recusa notebook como módulo. A verificação do Receipt confere integridade e coerência, não identidade humana. `run.py` só escreve no piloto estreito de README agregador com autorização específica; a validação não promove essa capacidade aos outros tipos.

Essa separação evita um pedido comum que parece simples: “transforme meu notebook em snippet e atualize o catálogo”. A pessoa precisa decidir se quer **criar** um objeto novo ou **converter** um existente, apontar a origem, aceitar a pasta e revisar se o comportamento será preservado. O preflight de conversão verifica origem e destino, mas não autoriza mover, apagar ou sobrescrever. Para snippet novo, uma seção já existente pode ser indicada; abrir uma sétima seção requer autorização própria. Se o objeto for skill, o template de `SKILL.md` governa forma e recursos, mas a rota específica de validação L3 de cinco tipos não se aplica a ela. O resultado deve declarar `NOT_AVAILABLE` ou bloqueio nesse ponto, não trocar por uma checagem improvisada. Quem recebe o material consegue assim ver exatamente o que foi planejado e o que falta decidir.

<a id="mu18-3"></a>
#### MU18.3 — README, exemplo e critérios de aceite

Depois de criar um objeto, outra pessoa precisa decidir **quando usá-lo** e interpretar sua saída. O README local de snippet, script ou prompt segue [template de objeto](hub_padroes/readme/template_objeto.md) 1.0.0 com quinze seções: definição, problema, adequação, contraexemplo, mecanismo, situação, preparação, retorno, uso, decisões, riscos, alternativas, conferência, arquivos e referências. Um README agregador tem outro molde: apresenta uma coleção e conduz aos guias individuais. O nome “README” não torna os dois contratos intercambiáveis. Comece pela pergunta do leitor e pelo consumidor, depois confira módulo e fachada antes de escrever promessas de entrada e saída.

Para uma função importável, identifique o arquivo de implementação, a API de `__init__.py` e o notebook de demonstração. O utilitário `api_publica.py` extrai por AST definições públicas no topo do módulo e imprime conteúdo de fachada; não executa o módulo, não reexporta imports alheios e recusa um notebook marcado. Não deduza que o `__init__.py` da categoria exponha cada objeto irmão. Um exemplo mínimo deve importar da pasta de objeto, passar dados sintéticos pequenos e mostrar um retorno interpretado com unidade e grão. Para script, indique efeitos ou leitura de recursos; para prompt, mostre briefing preenchível e exemplo de pedido sem publicar uma resposta de [modelo de linguagem (LLM)](hub_padroes/prompt/template.md) como observação de execução.

O notebook de exemplo de snippet ou script é `.py` com a primeira linha `# Databricks notebook source`. Ele ensina a chamar a fachada e a interpretar o resultado. Antes de copiá-lo para um destino, leia dependências e células preparatórias: a demonstração pode consultar `current_user()` via Spark para montar caminho, mesmo quando o helper em si funciona em Python local. Uma linha “saída real” só pode relatar a execução documentada; se não houve execução, rotule o exemplo como ilustrativo e marque o bloqueio. O leitor precisa saber o que foi calculado, em qual base, com que parâmetros e em qual ambiente. Uma string visualmente plausível não é evidência de runtime.

Use um objeto real para preencher a receita: [`constants.format_br`](hub_snippets/constants/format_br/README.md) tem README local completo, [módulo](hub_snippets/constants/format_br/format_br.py), [fachada](hub_snippets/constants/format_br/__init__.py) e [notebook de exemplo](hub_snippets/constants/format_br/exemplo_format_br.py). Confirme na assinatura que `fmt_pct(v, casas=1, input_scale="ratio")` recebe por padrão uma **fração**, devolve `str` e não altera locale. Escolha a entrada sintética `0.928` e documente no README tanto a chamada quanto o resultado esperado que o módulo e o exemplo registram:

```python
from hub_snippets.constants.format_br import fmt_pct
taxa = 0.928  # fração sintética
texto = fmt_pct(taxa)
assert texto == "92,8%"
```

Interprete: `92,8%` é **texto de apresentação** da fração fornecida, não taxa calculada de uma tabela. `fmt_pct(92.8)` com a escala padrão mostraria valor cem vezes maior; para entrada já percentual, `input_scale="percent"` precisa ser explícito. O README exemplar explica adequação, assinatura, retorno, armadilha de escala, alternativa e conferência; use essa estrutura para outro objeto sem copiar seus fatos. A implementação e a fachada confirmam API, enquanto a saída citada aqui é a registrada no exemplo sintético da fonte, não uma execução nova neste manual. O [contrato editorial](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_objeto_contract.py) verifica forma e links; ele não calcula uma taxa real nem decide se o denominador de negócio está correto.

Os checks de manutenção formam uma sequência. Primeiro, confira marcador, quinze seções e cobertura do objeto, sem criar dispensa automática; depois, links relativos à implementação, exemplo e fachada. Compare parâmetros citados com assinatura e nomes de retorno consumidos no notebook. Execute a validação estrutural aplicável e registre comando, revisão e resultado, lendo em [MT27](MANUAL_TECNICO_V2.md#mt-mod-mt27) o que ela sustenta. Só depois, se houver ambiente autorizado, execute o caso sintético e guarde saída real com data e runtime. Um PASS de `validate_assistant.py` não comprova que a função roda no Databricks; uma execução Spark não revisa automaticamente acessibilidade, segurança ou adequação da explicação.

Uma mudança de API exige atualizar módulo, fachada, README, exemplo e consumidores que importam o nome antigo. A seção “quando não usar” deve acompanhar esse movimento: custo de coleta no driver, dependência opcional, tabela necessária, escala percentual e efeito de escrita são limites específicos que evitam uso incorreto. Não preencha as quinze seções com fórmulas genéricas. Se o objeto devolve [HTML, linguagem de marcação exibida no notebook](MANUAL_TECNICO_V2.md#mt-mod-mt24), diga quem o renderiza e como trata texto externo; se devolve DataFrame Spark, diga grão e ação que materializa o resultado. O critério de aceite editorial é o leitor conseguir reproduzir a chamada com entrada conhecida, entender a saída, reconhecer o bloqueio quando faltar dependência e saber qual validação ainda resta.

Na entrega, mantenha uma pequena trilha de conferência ao lado do README: versão do objeto, entrada sintética usada, valor esperado conhecido, saída efetivamente observada ou motivo de bloqueio, links para teste e dependências opcionais. Se a demonstração mostra uma tabela com cinco linhas, informe se cinco é contagem da amostra, de entidades distintas ou de resultados válidos após filtros. Se exibir porcentagem, declare se a função recebe fração ou número já escalado. Essa informação permite que outro mantenedor perceba um erro sem adivinhar intenção a partir de formatação. A revisão deve também abrir o documento no destino de leitura, pois Markdown renderizado e HTML de um notebook podem apresentar links ou símbolos de maneira diferente do texto fonte.

Quando um exemplo falha, corrija a causa documentada antes de “arrumar” apenas a saída. Um parâmetro inexistente pede alinhamento com a assinatura; uma coluna ausente pede entrada de teste adequada ou correção da função; um resultado sem execução pede rótulo de ilustração. Substituir uma saída real por número esperado sem rodar código apaga a distinção entre objetivo e evidência. O objeto só fica pronto para ser recomendado quando a documentação descreve o comportamento que seus testes e execução realmente sustentam, e quando os limites de uso estão visíveis para o público pretendido.

<a id="mu18-4"></a>
#### MU18.4 — Auditar evidência e corrigir desvios

Auditoria de skill começa por definir a pergunta: o **modo IMPLEMENTAÇÃO** examina a pasta da própria skill, suas referências e possibilidade de executar o fluxo; o **modo OUTPUT** confronta artefato produzido, pedido original e `SKILL.md` da produtora. Misturar modos leva a achados imprecisos: um notebook pode seguir um pedido, embora a pasta da skill tenha links quebrados; uma pasta pode estar íntegra, embora um resultado específico não tenha chamado o helper obrigatório. O preflight exige entradas observáveis antes de avaliar mérito. Um bloqueio por artefato ausente significa “não foi possível auditar”, não uma falha inventada da execução.

<a id="uso-hub-ml-auditoria-skills"></a>
<!-- usage-card:start hub-ml-auditoria-skills -->
##### Ficha de uso — auditar skill ou output

Escolha [`hub-ml-auditoria-skills`](skills/hub-ml-auditoria-skills/SKILL.md) quando precisar verificar se uma implementação de skill é executável ou se um resultado seguiu o contrato de sua produtora. Informe o modo. Para OUTPUT, forneça artefato, pedido original e nome do `SKILL.md` produtor; para IMPLEMENTAÇÃO, indique as pastas de skills a examinar. A [policy vigente](hub_padroes/skill_enforcement/policy.json) define L3, execução determinística em modo audit; a checagem prévia L2 ainda decide se há entrada suficiente para começar. A auditoria deve separar recurso apenas citado de recurso localizado, lido, importado, chamado e concluído, registrando `NOT_OBSERVABLE` onde falta prova.

O entregável é relatório com achado, fonte, efeito, correção mínima e critério de nova conferência. Confira se o Receipt `SE07-AUDIT-RECEIPT-1` se refere ao runner **da auditoria**, não à conclusão da skill produtora. Um PASS persistido pela produtora não vira `PASS_REVERIFIED` sem verifier canônico sobre o artefato atual; o adaptador explícito de [análise exploratória de dados (EDA)](#mu-mod-mu04) é um caso particular. Se um notebook diz “saída real” sem execução identificável, peça a evidência ou reclassifique como exemplo, sem fabricar métrica. Para qualidade estatística do resultado, use revisão de domínio além desta auditoria contratual.

Pedido copiável:

```text
@hub-ml-auditoria-skills Modo OUTPUT: confira @<artefato> contra @<SKILL.md produtora> e este pedido: <...>. Distinga citado, lido, chamado e concluído; registre evidência ausente e correção mínima sem inferir execução.
```
<!-- usage-card:end hub-ml-auditoria-skills -->

O runner L3 recebe uma escada explícita por recurso e emite Receipt de auditoria vinculado ao que observou. Esse Receipt protege a coerência do relato do runner, mas não substitui o postflight da skill produtora. No caso de EDA com payload final compatível, o adapter chama seu verifier canônico e só então pode classificar a conclusão como `PASS_REVERIFIED`. Sem adapter aplicável, use `NOT_REVERIFIED`; não prometa que todo output terá a mesma taxonomia. Para uma lacuna, peça a menor evidência que resolveria a dúvida: registro de chamada, output bruto, hash do artefato ou trecho da execução. Repetir um score geral sem apontar qual degrau faltou não ajuda a corrigir o fluxo.

Na prática, a correção pode ser documental ou funcional. Uma referência inexistente em `SKILL.md` pede reparar o link e revisar o pacote; um helper declarado mas nunca chamado pede executar a rota canônica ou ajustar o contrato, não marcar conclusão por semelhança da resposta. Se o preflight bloqueou antes da lógica, reporte o bloqueio e não culpe um algoritmo que nem rodou. O relatório deve citar revisão e artefato atual para que uma pessoa possa reproduzir a inspeção. Como em [MT27](MANUAL_TECNICO_V2.md#mt-mod-mt27), conformidade local não homologa Databricks, não aprova dados e não concede autorização de publicação.

Quando houver vários achados, ordene-os pelo efeito no usuário: primeiro a afirmação de conclusão sem evidência, depois contrato ou referência que impede reprodução, por fim legibilidade. A prioridade precisa apontar ação verificável, não apenas uma nota numérica. Reaudite o artefato corrigido, pois a correção muda a base da conclusão anterior.


<!-- editorial:exclude:start -->
[Anterior: MU17](#mu17) · [Próximo: MU19](#mu19) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT27](MANUAL_TECNICO_V2.md#mt27)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu19"></a>
<a id="mu19"></a>
### MU19 — Instalar, atualizar e compartilhar uma entrega

Este percurso é para o mantenedor autorizado da instalação pessoal. Quem usa o Hub no dia a dia pode participar do aceite, mas não precisa operar Git, gerar ZIPs ou administrar o workspace. As decisões e comandos abaixo descrevem uma entrega planejada; sua execução depende do escopo, da autorização e do ambiente efetivo. O detalhamento técnico das ferramentas está em [MT28](MANUAL_TECNICO_V2.md#mt-mod-mt28), e o alcance dos testes locais em [MT27](MANUAL_TECNICO_V2.md#mt-mod-mt27).

<a id="mu19-1"></a>
#### MU19.1 — Defina pessoas, escopo e destino

Comece escrevendo em registro controlado qual commit será entregue, quais partes do Hub pertencem à revisão e qual pasta pessoal poderá recebê-las. Um exemplo de nomenclatura é `/Users/<username-trabalho>/hub_staging_<commit-curto>/`; os sinais angulares são espaços a preencher somente no destino autorizado. Não coloque host, usuário real, token, nome de tabela ou backup corporativo nesta documentação versionada. A pasta de staging é área de conferência, separada da instalação ativa em `/Users/<username-trabalho>/.assistant/` e do arquivo `.assistant_instructions.md` na raiz pessoal. Importar em staging não ativa skills nem atualiza instruções da Genie.

Há papéis diferentes mesmo quando uma pessoa acumula mais de um. O autor corrige a fonte no Git. O mantenedor escolhe o commit e monta o kit. O administrador do workspace define permissões e políticas. O revisor técnico confere o pacote e os testes permitidos. O usuário de aceite observa exemplos, imagens e comportamento da Genie na instalação final. Ter acesso de leitura a um ZIP, ou conseguir abrir um notebook, não concede por si só permissão para sobrescrever a pasta ativa, executar compute ou consultar dados. Confirme a autorização para cada etapa com a governança do ambiente; o [playbook de replicação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/replicacao-trabalho.md) é o roteiro operacional do projeto.

Antes do pacote, delimite o que é Hub e o que pertence a terceiros. Dentro de `.assistant`, não apague indiscriminadamente `skills/`: a instalação pode conter skills alheias, `.mcp_servers.json`, segredos ou outras configurações mantidas pela organização. Preserve também a lista de controle de acesso, ou ACL, ao planejar backup e promoção. O [project_policy.py](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/project_policy.py) define nomes e limites de caminhos do produto; [AGENTS.md](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/AGENTS.md) e os [ADRs](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/README.md), registros de decisões arquiteturais, documentam fronteiras de autoria e publicação. O [índice de manutenção por tarefa](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/ai/README.md) ajuda a localizar os procedimentos vigentes, sem substituir a política de acesso do workspace.

Registre a base instalada antes de escolher a atualização: commit anterior se conhecido, árvore atual, arquivos que serão substituídos, dependências esperadas e possibilidade de retorno. Se encontrar material sem dono claro, interrompa a substituição desse item e peça identificação ao mantenedor responsável. Staging permite comparar revisões sem alterar a instalação de trabalho. O objetivo da etapa é sair com um destino concreto e uma lista verificável, e não com uma autorização inferida de acesso à interface. Conteúdo customizado `.assistant` e o serviço nativo Databricks têm ciclos de vida diferentes; esta entrega atualiza somente os arquivos do Hub sob o escopo autorizado.

O plano deve nomear também quem fará cada conferência: pacote, instalação, teste técnico e observação humana. Isso evita que uma mesma marca “aprovado” esconda lacunas entre etapas. Uma pasta pessoal de testes pode ser autorizada enquanto a instalação ativa ainda está bloqueada; registre os dois estados separadamente.

<a id="mu19-2"></a>
#### MU19.2 — Valide a fonte, regenere o espelho e monte o kit

No checkout da revisão escolhida, comece pelos gates locais pertinentes, descritos em [MT27](MANUAL_TECNICO_V2.md#mt-mod-mt27). `validate_assistant.py` examina o contrato do produto; `ci_local.py` agrega verificações locais declaradas pelo projeto. Um PASS aqui significa que aquele teste rodou contra aquela árvore: não é prova de instalação no destino, de permissão ou de execução Spark corporativa. Registre o commit e o resultado, e resolva divergências na fonte antes de empacotar. Dependências de Python e Node precisam estar disponíveis conforme a documentação do projeto; uma falha de pré-requisito não é sucesso do produto.

```console
python tools/validate_assistant.py
python tools/ci_local.py
```

O próximo comando mostra o plano do renderer, sem alterar o derivado. Revise origem, usuário simulado e destino. Para produzir o espelho destinado ao pacote, `--write` remove e recria `.artifacts/simulado/` a partir de `ambiente_databricks/`. Antes dessa escrita autorizada, inventarie destino e extras, confirme ownership e preserve conteúdo alheio; prefira uma cópia isolada. Não edite o espelho manualmente. `--output-root` aceita somente um subdiretório gerado permitido dentro de `.artifacts/`. Depois, `--check` compara paths, bytes/hashes e tipos; o diff Git não cobre essa saída ignorada. Divergência pede diagnóstico na fonte e no inventário, sem acrescentar arquivo ao ZIP ou apagar extra desconhecido para obter PASS.

```console
python tools/render_simulado.py
python tools/render_simulado.py --write
python tools/render_simulado.py --check
```

Um `.py` no pacote pode ser módulo `FILE` ou exemplo `NOTEBOOK`. A [regra do marcador](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/notebook_marker.py) examina `# Databricks notebook source` no começo do arquivo, aceitando apenas BOM (marcador de codificação), linhas vazias e preâmbulos específicos antes dele. O [bundle](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/bundle_implantacao.py) grava o tipo de cada item, tamanho e SHA-256 em `MANIFEST.json`. Antes de distribuir, confira se os exemplos esperados aparecem como NOTEBOOK e os módulos importáveis como FILE. Um tipo errado exige corrigir o arquivo ou a importação; alterar a etiqueta do manifesto não conserta o objeto.

Há duas saídas com propósitos diferentes. Para revisão interna de trabalho ainda não commitado no produto, `bundle_implantacao.py --allow-dirty` pode emitir um ZIP marcado `worktree_dirty=true`; se o escopo estiver sujo, o nome padrão recebe `-dirty`. Isso serve para discutir uma candidata, não para identificá-la como entrega limpa. O kit de transição exige checkout inteiro limpo e chama o bundler sem essa opção. Ele recusa diretório de saída já existente, para que uma revisão não sobrescreva a anterior. Depois de congelar o commit e conferir o espelho, use um nome novo:

```console
python tools/kit_transicao_trabalho.py --output .artifacts/kit-trabalho-<commit-curto>
```

O kit gera `01_IMPORTAR_HUB_<commit>.zip` com produto e manifesto, e `02_IMPORTAR_ACEITE_<commit>.zip` com os notebooks `01_ACEITE_TECNICO.ipynb` e `02_ACEITE_MICROMODELOS.ipynb`, manifesto e guias. Fora dos ZIPs ficam `COMECE_AQUI.md`, `GUIA_TRANSICAO.md`, `CHECKLIST.md`, `TESTES_GENIE.md`, cópias dos dois notebooks, `ACEITE_MICROMODELOS.md` e `SHA256SUMS.txt`. Leia `COMECE_AQUI.md` para a camada correta: se o canal de distribuição entregar um ZIP externo contendo o kit, extraia-o no computador autorizado e importe somente os ZIPs internos nos locais indicados. Não recomprima o produto perdendo nomes ocultos como `.assistant`. No workflow do kit, artefatos de pull request recebem nome de teste com PR e versão Python; são evidência de CI, não uma release para instalar no trabalho.

Confira o commit no manifesto, o conjunto de arquivos, o contrato de temas e os hashes contra a referência que o produtor forneceu por canal confiável. SHA-256 detecta mudança de bytes nessa comparação, mas não assina autoria. O pacote não carrega Git, credenciais nem autorização de workspace. Leve os arquivos pelo canal corporativo permitido e mantenha uma cópia controlada do relatório da revisão. Ao terminar esta etapa, você possui um artefato rastreável para staging; nenhuma skill foi instalada, nenhum notebook foi executado e nenhum runtime foi homologado.

Antes do transporte, abra os ZIPs localmente sem extrair para dentro do produto. Confirme que o ZIP 01 tem `MANIFEST.json`, `.assistant_instructions.md` e a árvore `.assistant`, e que o ZIP 02 tem o notebook e os guias sob `aceite_hub_<commit-curto>`. Compare o manifesto copiado nos dois ZIPs, não apenas os nomes dos arquivos: o notebook de aceite espera o hash do manifesto usado para gerar o kit. Verifique que o campo `worktree_dirty` está falso para entrega limpa. Se encontrar `-dirty`, volte à etapa de commit e geração; renomear o arquivo não muda o estado registrado no manifesto.

O contrato de temas no manifesto serve para confirmar que os caminhos obrigatórios, inclusive schema, tokens, registro de assets, resolvedor e adaptador, foram transportados. Seu estado de ativação é manual: presença e hash corretos não publicam um tema global nem aprovam aparência no workspace. Essa distinção evita anunciar ao usuário final uma opção visual que ainda precisa de inspeção e ativação próprias. Se a lista obrigatória estiver incompleta, o gerador recusa o pacote; se o import de algum item falhar depois, o aceite no destino deverá mostrar a divergência.

Por fim, anote onde cada artefato será usado. O ZIP 01 vai apenas para staging; o ZIP 02 cria a pasta de aceite na raiz pessoal; os guias orientam o operador; `SHA256SUMS.txt` acompanha o transporte como referência de integridade. Enviar só o produto sem o roteiro de aceite elimina a capacidade de conferir a mesma revisão. Enviar um notebook preenchido com parâmetros do trabalho para fora do ambiente autorizado, por sua vez, expõe contexto que o kit original não contém. Mantenha a configuração real somente no destino.

<a id="mu19-3"></a>
#### MU19.3 — Planeje, importe em staging e confira por camadas

Existem duas rotas que não devem ser confundidas. No laboratório pessoal Free, [publicar_free.py](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/publicar_free.py) oferece um plano sem escrita remota, mas que consulta a CLI autenticada e portanto não é offline, `--execute` para publicar no destino Free explícito, `--verify` para inventário e tipos, e `--verify --conteudo` para comparar conteúdo exportado após normalização de finais de linha. `--verify --rapido` só olha diretórios até a profundidade configurada; não confere arquivos, tipos ou bytes. O plano não prova que a escrita terá êxito; `--execute` altera o workspace e depende de autorização. A rota do trabalho usa o kit e a interface, conforme o [playbook](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/replicacao-trabalho.md). Não aponte o publicador Free para o workspace corporativo.

Na rota de trabalho, prepare primeiro o backup da instalação pessoal ativa. Exporte `.assistant` no formato **Zip - Source (notebook + files only)** e exporte `.assistant_instructions.md` separadamente. Abra o backup em lugar isolado e confirme que contém módulos, Markdown, imagens e notebooks recuperáveis. Um DBC, formato de exportação de notebooks do Databricks, não cobre esse conjunto quando contém somente notebooks. Guarde backup e parâmetros reais dentro do ambiente autorizado, junto ao mapa de ACL; a pasta de staging não substitui esse ponto de retorno. Antes de importar, confirme permissão de upload, acesso a Workspace Files, compute e uso da Genie em cada fase prevista.

Crie uma pasta pessoal vazia `hub_staging_<commit-curto>` e importe ali o ZIP 01, conferindo se `.assistant` e `.assistant_instructions.md` ficaram na camada esperada. Importe o ZIP 02 na raiz pessoal para criar `aceite_hub_<commit-curto>`. Abra `01_ACEITE_TECNICO` dentro da pasta do kit, em sessão Python nova. Preencha `USER_HOME` com o caminho visto na interface e mantenha `PHASE="staging"`. O [aceite sintético de Micromodelos](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/aceite-micromodelos-trabalho.md) também confere o domínio transportado no ZIP 01, mantendo metadata e MLflow institucionais desligados. O notebook fixa commit e SHA-256 do manifesto; opções de Spark, MLflow, tabela Unity Catalog e consulta de tipos via API (interface de programação de aplicações) começam desligadas. Não execute todas as células de uma vez. Siga a sequência de identidade, manifesto e arquivos antes de habilitar qualquer extensão.

O primeiro resultado esperado é manifesto íntegro e todos os `FILE` comparados por SHA-256. Se algum divergir, reimporte do pacote correto; não edite o manifesto para obter PASS. Confirme pela interface que os `NOTEBOOK` abriram como notebooks, pois a importação pode reescrever sua representação e o teste de FILE não certifica igualdade de células. A consulta opcional à API pode verificar metadados de tipo, mas também não prova o texto das células. Depois examine dependências e imports; um pacote listado não demonstra que cada recurso funcionará no compute escolhido.

Quando houver compute aprovado, habilite o Spark sintético e recomece em sessão nova. O roteiro testa ação mínima, qualidade com aviso esperado, defeito de duplicidade injetado, RFV (recência, frequência e valor), ponto no tempo, PSI (índice de estabilidade populacional) e objeto Plotly; um teste negativo pode ser PASS justamente porque detectou o defeito. MLflow só deve ser habilitado para experimento pessoal existente e autorizado; leitura Unity Catalog só para uma tabela nomeada e autorizada, sem inferir permissão de escrita. Mantenha essas extensões como `NAO_TESTADO` ou `PENDENTE` quando não forem executadas. Guarde o resultado sanitizado, a revisão e a data dentro do ambiente permitido, sem enviar configurações preenchidas para o Git.

Staging tecnicamente aprovado continua inativo. A promoção seletiva exige seu próprio gate e aceite. O checklist vigente mantém SE08 **BLOQUEADA** enquanto a exceção G2 cobre apenas SE06 → SE07; staging aprovado não remove esse bloqueio. Depois de resolvido e autorizado o avanço, preserve skills alheias, a configuração MCP (protocolo de contexto de modelo) dos servidores, ACL e instruções administrativas; depois execute os testes novamente na instalação final, em sessão nova, e observe a Genie e a aparência das imagens. Uma exportação com bytes correspondentes, ou um notebook técnico aprovado, não certifica roteamento, marca, experiência do usuário ou autorização de uso. O [checklist](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/checklist-replicacao.md) mantém essas confirmações humanas separadas das verificações automáticas.

Registre o veredito da fase de staging literalmente, por exemplo `STAGING_TECNICO_APROVADO_NAO_ATIVADO`, somente se os testes correspondentes foram executados. Se Spark não foi habilitado, diga que os testes Spark ficaram pendentes, mesmo que o manifesto tenha PASS. Se a UI (interface gráfica do workspace) confirmou um NOTEBOOK, descreva a observação e quem a fez; a consulta de tipos via API não substitui uma abertura que revele células úteis. Esses detalhes tornam a próxima fase repetível e permitem interromper a promoção antes de atingir o ambiente ativo.

<a id="mu19-4"></a>
#### MU19.4 — Atualize com ponto de retorno e relate o resultado

Antes da primeira substituição na instalação ativa, congele qual commit e manifesto passaram em staging, quais pastas e arquivos serão promovidos e onde está o backup testado. Reserve uma janela sem edição simultânea do mesmo escopo. A promoção ocorre por partes do Hub, não por substituição da pasta `.assistant` inteira: atualize as extensões e skills declaradas, preserve skills de terceiros e `.mcp_servers.json`, e trate legados identificados em revisão. Atualize README e Manual no escopo autorizado; substitua `.assistant_instructions.md` por último e confirme no Settings da Genie. O [guia de transição](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/replicacao-trabalho.md) e o [checklist](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/checklist-replicacao.md) detalham a ordem e o aceite.

Após a promoção, reinicie a sessão Python, altere `PHASE` para `final` e repita identidade, FILEs, imports e testes técnicos autorizados. Abra READMEs, imagens, links e exemplos FILE/NOTEBOOK na interface. O aceite humano observa EDA (análise exploratória de dados) sem seleção explícita, baseline e criar objeto com seleção, contexto proporcional e proveniência. Marque cada confirmação como observada, pendente ou reprovada; uma resposta plausível da Genie isolada não prova que a instrução correta foi carregada. Um resultado no Free ou um screenshot de staging descreve outro ambiente e não homologa a revisão corporativa atual.

Se houver falha, pare a promoção ou o uso do componente afetado. Registre qual teste falhou, em qual fase, com qual commit e qual objeto; compare o inventário e, quando aplicável, a exportação com o manifesto. Restaure do backup apenas o escopo substituído, preservando mudanças alheias posteriores e a ACL. Reinicie Python e chat antes de retestar, para evitar módulos ou contexto antigos em cache. Se uma extensão opcional criou um run MLflow próprio e a limpeza falhou, trate somente esse run dentro do destino autorizado. A correção durável volta à fonte sem identificadores do trabalho e resulta em novo commit e novo kit, nunca em edição clandestina do ZIP.

Ao compartilhar o estado, separe o que foi comprovado do que ficou pendente: integridade do pacote, tipo dos objetos, comparação de FILEs, testes sintéticos, observação visual, comportamento da Genie e extensões opcionais. Informe bloqueios com causa e próximo passo. `SHA256SUMS.txt` vale como detecção de alteração contra referência confiável, não como autenticação de autor. `PRONTO_PARA_PILOTO_BASICO`, quando aplicável, tem apenas o alcance dos testes e permissões vistos; modelos, serving, dados corporativos e produção seguem gates próprios. Isso permite que o próximo mantenedor retome a instalação pelo estado real, sem transformar ausência de teste em aprovação.

O registro compartilhável deve omitir host, usuário, tabela, experimento e exceções brutas que revelem dados internos. Conserve o relato completo no ambiente corporativo permitido e ofereça ao usuário um resumo de funcionalidades verificadas, pendências e impacto prático. Uma futura atualização começa dessa linha de base, repete o processo com novo commit e mantém o backup anterior até que o novo aceite termine.


<!-- editorial:exclude:start -->
[Anterior: MU18](#mu18) · [Próximo: MU20](#mu20) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT28](MANUAL_TECNICO_V2.md#mt28)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu20"></a>
<a id="mu20"></a>
### MU20 — Resolver problemas e concluir um percurso com evidência

<!-- editorial:exclude:start -->
**Pergunta:** como uma pessoa iniciante distingue erro de ambiente, contrato e resultado, e percorre uma análise até um relatório revisado? **Rota:** a parte A ensina o diagnóstico; a parte B junta os passos em uma tarefa copiável. Código e tabela deste capítulo são ilustrativos e não foram executados nesta redação. [Índice do manual](#sumario-mu).
<!-- editorial:exclude:end -->

<a id="mu20-1"></a>
#### 1. Em que fase ocorreu o erro?

Comece anotando o que você tentou fazer: ler uma tabela, importar um helper, executar a skill, desenhar uma figura ou concluir o relatório. Essas ações têm dependências e efeitos diferentes. Uma **EDA** (análise exploratória de dados) examina estrutura, qualidade e distribuição de uma fonte para orientar uma decisão. Se você ainda não consegue localizar a fonte, não existe resultado de EDA a interpretar. Se uma biblioteca Python não importa, não conclua que a tabela está inacessível. Se o gráfico falha, um perfil tabular pode continuar útil, mas a obrigação visual da skill selecionada talvez permaneça aberta.

Para praticar sem dados de trabalho, a [fixture `base_tabular`](hub_snippets/testing/fixtures/fixtures.py) cria um **DataFrame Spark** sintético com `id_cliente`, `uf`, `renda`, `dt_referencia` e `alvo`. Spark é o motor que processa o DataFrame; a função pede uma sessão ativa ou cria uma sessão conforme o ambiente. Ela não grava tabela. `n`, `seed`, fração de nulos e número de entidades controlam a população artificial; a semente torna a geração repetível no mesmo contrato, sem garantir identidade de números em todos os runtimes. O [README de fixtures](hub_snippets/testing/fixtures/README.md) explica a finalidade de ensaio. A **view temporária** que criaremos na parte B recebe nome na sessão atual; não é uma tabela publicada. Mesmo esse efeito em sessão deve ocorrer só em compute autorizado.

Use a fase para localizar a primeira causa plausível. Se `from hub_snippets.testing import fixtures` falha, confira se `.assistant` existe no caminho esperado, se essa raiz está em `sys.path` e se as dependências do pacote estão disponíveis. Se `spark.table("mu20_clientes_sinteticos")` falha depois de criar a view, confira sessão, nome e se a célula de criação realmente terminou; se o nome aponta a tabela persistente de outra pessoa, também confira catálogo e permissão. Não trate `ModuleNotFoundError` como problema da lista de controle de acesso (ACL) da tabela, nem `TABLE_OR_VIEW_NOT_FOUND` como prova de que o código do helper está errado. O [README da .assistant](README.md) mostra a organização de imports.

Tema visual tem outra superfície. `ThemeError` com código `DEPENDENCY_MISSING` indica que a validação do tema não encontrou uma dependência; a [matriz de erros](hub_padroes/identidade_visual/ERROS.md) aponta para [requirements-temas.txt](hub_snippets/requirements-temas.txt). Ela não instala nada sozinha e não autoriza instalação num cluster. `RESULT_TYPE` ou `RESULT_INTEGRITY` apontam objeto `ResolvedTheme` inadequado ou adulterado, não falha de acesso Spark. Primeiro identifique a biblioteca e o ambiente permitidos, depois refaça `resolve_theme` ou `load_theme` na rota correta. O [MU17](#mu17-1) detalha o tema e suas mensagens.

Estado de policy, o registro de regras e níveis da skill, também não é diagnóstico de import. A [policy](hub_padroes/skill_enforcement/policy.json) separa `current_level`, nível sustentado hoje, de `target_level`, direção de migração. A skill piloto EDA tem L4 e modo `enforce`; outra skill pode ainda ter nível menor e alvo L4. **L4** quer dizer que a conclusão depende de verificação posterior, chamada Postflight. Não leia “alvo L4” como “Ready” (pronto para promoção) nem como autorização para executar em qualquer dado. O [MU08](#mu08-1) explica como escolher recurso e confirmar sua rota; o [MU12](#mu12-1) ensina a interpretar saída de ML sem promover métrica a decisão.

Quando pedir ajuda, leve quatro dados pequenos: fase, comando ou nome do recurso, mensagem/código e o que foi observado antes da falha. Inclua versão e ambiente quando relevantes. Substitua tabela e identidade reais por exemplo sintético reproduzível; não cole token, dado pessoal ou cinco linhas brutas de uma base de trabalho. Se a operação tinha escrita, informe **o destino e o modo** em canal autorizado antes de repetir. Essa informação evita que alguém recomende “rodar de novo” uma célula que sobrescreve tabela. O [MU05](#mu05-1) ajuda a declarar objetivo, grão, fonte e desconhecidos antes de escolher um briefing.

<a id="mu20-2"></a>
#### 2. O que fazer quando o contrato bloqueia ou o resultado parece pronto?

Escolher `@hub-ml-eda-profissional` vincula a tarefa à rota da [skill](skills/hub-ml-eda-profissional/SKILL.md). O **preflight** confere contrato, condições, recursos e templates antes da execução; sua saída isolada é diagnóstico L2, não EDA concluída. O runner chama `quick_profile` e emite um **Receipt**, comprovante estruturado de vínculo entre entrada, trace, saída e release. O executor L4 observa imports, chamadas, conclusão de recursos e leitura de templates aplicáveis. O **Postflight** confere a evidência e o handoff final. Um número plausível de linhas, um Receipt `VALID` e uma figura bonita ainda podem coexistir com `completion.status="PENDING_POSTFLIGHT"`. O [MT30](MANUAL_TECNICO_V2.md#mt30-2) desenha o mecanismo completo.

O percurso principal da parte B usa `run_enforced(table_name, context=None, *, assistant_root=None, sample_fraction=0.1, max_categories=20, seed=42, display_fn=None, resolved_theme=None, strict=True)`. A tabela/view precisa existir e ser legível pela sessão autorizada. O contexto padrão solicita distribuições e diagnósticos visuais; preview tabular, amostra local adicional e tema começam desligados. Só declare `pk_columns` quando a chave candidata estiver estabelecida como lista não vazia de strings. Ausência de chave deixa `data_quality_check` não aplicável com decisão justificada; `pk_columns=[]` é entrada inválida, não uma maneira de pedir “descubra a chave”. O [contrato EDA](skills/hub-ml-eda-profissional/execution_contract.json) dá os IDs e as condições que serão conferidos.

Leia o retorno em ordem. `trace.status` mostra se o core passou; `trace.enforcement_status` resume gaps L4; `trace.evidence_gaps` e `blocking_issues` dizem o que investigar. `resources_resolved` informa que o nome foi encontrado, `resources_called` que a função começou, `resources_completed` que retornou; o mesmo ID não migra automaticamente entre listas. `templates_loaded` exige leitura real, não citação nominal do arquivo. `receipt` e `artifacts` permitem verificar vínculo, mas não avaliam a qualidade da inferência. Se core e enforcement passaram, `completion.status="PENDING_POSTFLIGHT"`, `authorized=false` e `claim_allowed=false` significam **etapa obrigatória pendente**, mesmo que o comando tenha terminado com código `0`. O próximo passo é o finalizador com handoff verdadeiro, não uma frase de conclusão.

Há uma nuance útil para diagnóstico. Com `strict=True`, falha de core ou enforcement levanta `CanonicalExecutionBlocked` e carrega payload; guarde o diagnóstico e corrija a causa. Com `strict=False`, falha do **core** devolve `NOT_COMPLETED`. Se o core passou, mas há gaps de enforcement, a implementação atual conserva `enforcement_status="INCOMPLETE"` e marca `completion.status="PENDING_POSTFLIGHT"`, ainda com `authorized=false` e `claim_allowed=false`. Portanto, **não leia apenas a palavra PENDING**: leia também trace e gaps. A função Python devolve um `dict`; `strict=False` é argumento dessa função, sem flag equivalente na CLI. O `main()` da CLI retorna código de saída `2` quando o payload obtido não demonstra core e enforcement PASS; esse inteiro é estado do processo, não retorno de `run_enforced`. `strict=False` serve para inspecionar, não para completar a mesma EDA por células manuais. O [MU04](#mu04-4) reforça como reconhecer evidência ausente e separar uma resposta segura de tarefa concluída.

O handoff da EDA tem seis campos: `sources_snapshot` (fonte e fotografia), `unit_keys_target` (unidade, chave e alvo ou ausência), `quality_risks` (riscos observados e limites), `feature_candidates_leakage` (variáveis e disponibilidade temporal), `filters_sample` (filtros, fração, semente e denominadores) e `open_questions` (pendências). Só o último aceita `[]` vazio pelo contrato atual. A [função de Postflight](hub_scripts/skill_execution/postflight/__init__.py) distingue campo ausente (`HANDOFF_FIELD_MISSING`) de campo nulo/vazio/branco (`HANDOFF_FIELD_EMPTY`) e pode devolver `REVIEW`. Essa validação é **estrutural**: texto genérico não vazio pode passar, mas não demonstra que o risco foi analisado. Confira cada frase com o que o payload e o dado realmente sustentam; perguntas abertas honestas são preferíveis a certeza inventada.

Imagine que `id_cliente` se repita na fixture. Um handoff útil registra que o identificador não foi aceito como chave única, informa o grão que ainda precisa de decisão e separa essa observação da hipótese de que haja duplicidade indevida no negócio. A fixture foi construída para ensinar o problema; a mesma frase não pode ser transportada para uma tabela real sem medir e conhecer seu grão. Em `filters_sample`, descreva a fração solicitada e confira a quantidade efetivamente usada; a porcentagem configurada não prova que todas as análises posteriores receberam exatamente o mesmo denominador. Em `feature_candidates_leakage`, escreva quando uma variável estaria disponível em relação ao instante de decisão. Se esse instante é desconhecido, declare a pergunta em `open_questions`, sem marcar a variável como segura.

Depois de produzir o handoff, `finalize_or_raise(payload, handoff, assistant_root=...)` reverifica Receipt, contrato e rota L4, constrói Postflight e valida a consistência final. Só um retorno com `postflight.status="PASS"`, `completion.authorized=true` e `completion.status="COMPLETED"` suporta a frase “a skill concluiu segundo o contrato”. Se falhar, `CompletionNotAuthorized` conserva diagnóstico. O [MU04](#mu04-3) mostra como essa exigência entra no uso da skill; o [MT19](MANUAL_TECNICO_V2.md#mt19-1) separa aderência de correção analítica. Uma chamada isolada de `quick_profile` pode responder a uma pergunta delimitada e produzir um dict útil; se a skill EDA foi selecionada, ela **não substitui** L4 nem autoriza o mesmo claim de conclusão.

Para recuperar, classifique o código. `RESOURCE_RUNTIME_UNAVAILABLE` em preview pede `display_fn` realmente disponível ou revisão objetiva do pedido opcional. `RESOURCE_INPUT_MISSING` em tema exige objeto resolvido ou figura representativa; não invente um. `ARTIFACTS_DIGEST_MISMATCH` exige localizar alteração de artifacts, não recalcular hash para “passar”. `HANDOFF_FIELD_MISSING` pede campo ausente; um valor real e verificável ainda precisa ser escrito por uma pessoa. Após corrigir entrada ou dependência autorizada, inicie um **novo percurso canônico**. Não remonte Receipt, não reclassifique a skill como manual e não use um disclaimer para contornar o bloqueio.

Um erro reproduzível inclui a etapa e o estado anterior: “a view foi criada nesta sessão; o preflight resolveu o recurso; a chamada falhou antes de `resources_completed`; o código foi `RESOURCE_RUNTIME_UNAVAILABLE`”. Compare essa sequência com o caso em que `resources_completed` contém o recurso, mas o relatório ainda não explica o denominador. O primeiro pede recuperação de execução; o segundo pede interpretação humana. Se a leitura do template falha, informe o nome do template e o gap, pois um arquivo apenas listado no contrato não satisfaz `templates_loaded`. Preserve o payload original para comparação com a próxima tentativa, sem editar seus campos de evidência.

<a id="mu20-3"></a>
#### 3. Como resolver uma falha visual e pedir ajuda que permita reproduzi-la?

Primeiro separe **cálculo**, **figura**, **tema** e **exibição**. Um cálculo tabular pode terminar e a figura falhar na conversão ao driver; uma `Figure` pode existir sem ser mostrada no notebook; um tema pode falhar antes de alterar a figura. Pergunte: qual função foi chamada, quais colunas recebeu, houve retorno e qual foi a primeira exceção? A [matriz de gráficos EDA](skills/hub-ml-eda-profissional/templates/matriz_graficos_eda.md) ajuda a escolher forma adequada à pergunta, enquanto o [estilo visual](skills/hub-ml-eda-profissional/templates/estilo_visual_eda.md) orienta apresentação. Ler esses templates não prova que o relatório os aplicou corretamente.

Para duas colunas numéricas da fixture, `plot_correlation(df, cols=["renda", "alvo"], method="spearman", threshold_highlight=0.8)` devolve `(Figure, strong_pairs)`. A lista marca pares cujo **valor absoluto** da correlação é maior ou igual ao limiar; associação negativa forte também aparece. A função remove linhas com nulos nas colunas selecionadas para o cálculo. Não use o total de linhas da base como denominador da correlação sem verificar esse recorte. `alvo` é um indicador sintético: uma associação não mostra causa nem valida uma variável preditora antes de definir tempo de decisão. O [código da matriz](hub_snippets/display/correlation_matrix/correlation_matrix.py) mostra retorno e filtros reais.

Se houver apenas uma coluna numérica útil, correlação entre duas colunas não se aplica; uma distribuição é pergunta mais adequada. [plot_distributions](hub_snippets/display/distribution_grid/distribution_grid.py) seleciona números, usa `smart_sample` antes de `toPandas()` e retorna `Figure`; `sample_n=10000` é default, não garantia de amostra de dez mil linhas. Confirme quantas linhas ficaram na amostra e se os extremos raros poderiam ter ficado fora. Se a figura não aparece, verifique se o retorno foi uma `Figure` e se o notebook recebeu uma chamada explícita de exibição; o helper não publica relatório nem workspace. Uma rota que devolve figura não diz onde ela foi salva. O [MU17](#mu17-2) aprofunda escolha de tema e consumidores.

Tema validado é objeto `ResolvedTheme` obtido por [resolve_theme/load_theme](hub_snippets/visual/tema/tema.py), com contexto compatível com notebook. A [camada Plotly](hub_snippets/visual/theme_plotly/theme_plotly.py) recebe esse objeto, aplica aparência e pode devolver a mesma figura; não muda os dados, os filtros ou o significado da métrica. Dentro de L4, a seleção de tema também participa do trace e do Receipt reemitido: não diga que toda evidência permanece idêntica só porque os números são iguais. Se `resolved_theme_selected=True` sem objeto validado, há `RESOURCE_INPUT_MISSING`; se não houver figura representativa, o mesmo código pode indicar ausência de entrada visual. A solução é corrigir entrada/condição e refazer a rota, não pintar manualmente uma imagem e chamá-la de evidência L4.

Erros de tema costumam trazer um `ThemeError.code`. A [tabela ERROS](hub_padroes/identidade_visual/ERROS.md) distingue dependência ausente, schema inválido, caminho inseguro e resultado adulterado. Com `DEPENDENCY_MISSING`, confirme requirements e ambiente autorizado; não peça que alguém instale biblioteca em cluster compartilhado sem permissão. Um erro de contrato de tema não prova que Spark falhou; uma falha Spark não prova que a paleta está errada. O [guia operacional](hub_padroes/identidade_visual/GUIA_OPERACIONAL.md) separa tema de dados e descreve os contextos suportados. Compare rota legada e `_resolvido` apenas no que cada uma aceita e altera na aparência.

Um pedido de ajuda reproduzível pode caber em cinco linhas: “Queria histograma de `renda` da fixture sintética; `plot_distributions` recebeu `sample_n=200`; retornou `Figure` ou lançou [classe/código]; a sessão usa [runtime e versão] com tema [ausente ou `ResolvedTheme` notebook]; executei apenas [passos observados]”. Acrescente traceback mínimo e número de linhas/colunas, sem enviar tabela de trabalho, token nem caminho pessoal. Informe se a skill EDA estava selecionada e qual era `trace.enforcement_status`; uma figura isolada sem trace é caso diferente de recurso L4 aplicável que falhou. Se um helper funcionou, mas o relatório ficou confuso, peça revisão da legenda, do denominador e das limitações, não reexecução cega da tabela.

Antes de trocar um parâmetro, formule uma pergunta verificável. Para `renda`, “qual a distribuição dos valores não nulos na amostra exibida?” pede histograma e contagem de ausentes separada. Para `uf`, a pergunta sobre frequência por categoria pede barras com total e tratamento de categorias raras; forçar correlação numérica de códigos de estado criaria uma ordem artificial. Para `renda` e `alvo`, correlação exige explicitar método, linhas completas e se o alvo binário é apenas marcador sintético. Se o eixo parece truncado, compare dados enviados ao helper, limites do eixo e resumo tabular antes de mudar escala. Esses passos separam um defeito visual de uma propriedade da amostra.

Se a função devolveu `Figure`, use a exibição apropriada ao notebook autorizado e registre se o objeto foi efetivamente mostrado; retorno e tela são evidências diferentes. Se quiser salvar a figura, defina destino, formato e autorização como decisão adicional, pois a função de plot não fornece publicação automática. Para comparar duas versões, conserve colunas, método, amostragem e denominador, depois descreva separadamente a alteração de tema. Um tema diferente pode mudar contraste e legibilidade; não justifica afirmar que o dado mudou. Na rota L4, essa escolha pode alterar trace e novo Receipt, então reúna a evidência do percurso correspondente à versão revisada.

Evite três conclusões precipitadas. “Figura não apareceu” não significa “métrica foi zero”; “métrica correta” não significa “skill concluída”; “tema bonito” não significa “gráfico aprovado para publicação”. Cada afirmação pede sua evidência. Para uma entrega, anote colunas, método, amostra, filtros, fonte e instante da coleta. Mostre também o que permaneceu não observado. Isso permite que outra pessoa corrija a primeira falha real, em vez de alterar várias camadas e perder a causa.

<a id="mu20-4"></a>
#### 4. Como ir do objetivo a um relatório revisado sem esconder efeitos?

O objetivo deste exercício é decidir **que perguntas de qualidade ainda faltam** antes de usar uma base de clientes num estudo. A fixture é sintética, pequena e não representa clientes reais. Escolha um compute Spark autorizado, confirme que a pasta `.assistant` está instalada no local usado e execute a sequência somente nesse ambiente. O código abaixo é um roteiro copiável **condicional**: ele cria um DataFrame e uma view temporária de sessão, importa os scripts da skill por seus arquivos e chama o executor. Não houve execução nesta redação. O [MT30](MANUAL_TECNICO_V2.md#mt30-1) explica cada vínculo técnico.

```python
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

usuario = spark.sql("SELECT current_user()").first()[0]
ASSISTANT_ROOT = Path(f"/Workspace/Users/{usuario}/.assistant")
if not ASSISTANT_ROOT.is_dir():
    raise FileNotFoundError(f".assistant não encontrada: {ASSISTANT_ROOT}")
sys.path.insert(0, str(ASSISTANT_ROOT))

from hub_snippets.testing import fixtures

base = fixtures.base_tabular(n=120, seed=42, n_entidades=100)
table_name = "mu20_clientes_sinteticos"
base.createOrReplaceTempView(table_name)  # view da sessão, sem saveAsTable

skill_dir = ASSISTANT_ROOT / "skills" / "hub-ml-eda-profissional"
def carregar(nome, arquivo):
    spec = spec_from_file_location(nome, arquivo)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"módulo indisponível: {arquivo}")
    modulo = module_from_spec(spec)
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo

executor = carregar("mu20_eda_executor", skill_dir / "scripts" / "run_enforced.py")
finalizador = carregar("mu20_eda_finalizador", skill_dir / "scripts" / "postflight.py")
context = {"numeric_distributions_requested": True,
           "visual_diagnostics_requested": True}
# Não declare pk_columns antes de verificar o grão e a chave.
payload = executor.run_enforced(table_name, context,
                                assistant_root=ASSISTANT_ROOT, strict=True)
assert payload["trace"]["status"] == "PASS"
assert payload["trace"]["enforcement_status"] == "PASS"
assert payload["completion"]["status"] == "PENDING_POSTFLIGHT"
assert payload["completion"]["claim_allowed"] is False
```

`base_tabular(n=120, n_entidades=100)` constrói duplicidade proposital em `id_cliente`; isso ensina por que não se deve declará-lo chave única só pelo nome. A geração não grava tabela. `createOrReplaceTempView` substitui uma **view temporária com esse nome na sessão atual**, se ela já existir; confira o nome antes de repetir a célula. Não é `saveAsTable`, nem publica no catálogo. `current_user()` é consultado apenas para montar o caminho de import do produto nessa instalação; adapte o caminho se o seu ambiente autorizado usa outro layout. Se a fixture, view, import, preflight, helper ou gráfico falhar, preserve a exceção e o trace disponível; não execute a continuação como se os `assert` tivessem passado.

O executor devolve evidência, não um relatório pronto. Confira `payload["result"]`, que vem do perfil, e o trace para extrair somente números observados; não presuma a contagem de nulos ou a força de uma correlação. O `artifacts` do executor registra status dos recursos e integridade, mas não expõe o objeto `Figure` mantido localmente durante a execução. Revise fonte, filtros, amostra e denominadores antes de escrever o handoff. O exemplo a seguir registra fatos conhecidos **do próprio roteiro** e lacunas reais; ajuste cada frase à execução observada. Ele não finge ter medido qualidade nem provado ausência de vazamento. `open_questions` permanece não vazio porque data de decisão e disponibilidade das variáveis não foram estabelecidas.

```python
handoff = {
    "sources_snapshot": "view temporária mu20_clientes_sinteticos, fixture base_tabular(n=120, seed=42, n_entidades=100), sessão atual",
    "unit_keys_target": "linha sintética gerada; id_cliente se repete e não foi aceito como chave; alvo é marcador binário sintético",
    "quality_risks": "duplicidade intencional de id_cliente; renda pode ter nulos; conferir taxas e denominadores no payload observado",
    "feature_candidates_leakage": "uf e renda são candidatas de exploração; disponibilidade anterior à decisão não foi demonstrada",
    "filters_sample": "sem filtro adicional; sample_fraction=0.1 e seed=42 no executor; conferir sample_rows observado",
    "open_questions": ["Qual é o grão de negócio pretendido?", "Quando renda estaria disponível para a decisão?"],
}
final_payload = finalizador.finalize_or_raise(
    payload, handoff, assistant_root=ASSISTANT_ROOT
)
assert final_payload["postflight"]["status"] == "PASS"
assert final_payload["completion"]["authorized"] is True
assert final_payload["completion"]["status"] == "COMPLETED"
```

Mesmo que esse finalizador retorne, o Postflight verifica aderência e presença estrutural, não a qualidade de cada frase. Perguntas abertas devem continuar no relatório; um `PASS` contratual não transforma a fixture em base apta a treino. Se a chamada levantar `CompletionNotAuthorized`, leia `final_payload` e `verification` da exceção e corrija a causa em novo percurso canônico. Para fechar a inspeção visual, execute o bloco separado abaixo somente após o percurso canônico bem-sucedido e com a mesma fixture ainda disponível. Ele obtém e exibe uma distribuição de `renda`; não recupera a figura interna do executor, não altera o payload e não preenche gaps L4 por fora da rota:

```python
from hub_snippets.display.distribution_grid import plot_distributions

figura = plot_distributions(base, cols=["renda"], ncols=1, sample_n=120)
figura.show()  # exibição Plotly no notebook autorizado, sem salvar arquivo
```

Confirme na tela título, eixo, valores não nulos e legibilidade. A função amostra antes de coletar ao driver; `sample_n=120` é limite solicitado, não prova do denominador exibido. O histograma não quantifica ausentes: confronte-os com o perfil observado. Falha do renderer deve ser registrada como falha desta inspeção, sem fabricar figura ou modificar Receipt. Para outra pergunta, a correlação da seção anterior continua exigindo duas colunas e recorte de linhas completas. Registre separadamente retorno da `Figure`, exibição observada e avaliação humana. O [roteiro EDA](skills/hub-ml-eda-profissional/templates/roteiro_eda.md) orienta ordem da investigação, e o [modelo de relatório](skills/hub-ml-eda-profissional/templates/relatorio_executivo_eda.md) exige objetivo, período, volume, granularidade, padrões, anomalias e limitações. Preencha somente com observações e revisão humana; template carregado não é relatório preenchido.

> **Efeito separado: notebook de briefing `data_quality`.** A [Parte 1 do exemplo](hub_prompts/data_quality/exemplo_data_quality.py) faz `base.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes_dup")`. Rodá-la pode **sobrescrever uma tabela persistente** nesse destino; confira nome, permissão e impacto antes de escolher essa rota. Ela não faz parte da view temporária do percurso principal. A Parte 2 é um prompt preenchido para copiar manualmente ao chat; texto não executa skill. A Parte 3 diz `NÃO EXECUTADO` até uma resposta real ser obtida, datada e revisada. O [MU05](#mu05-3) mostra como separar essas três evidências.

Por fim, revise figura e relatório com outra pessoa, retire dados ou caminhos sensíveis e identifique as dúvidas que ainda mudam a decisão. Salvar notebook, publicar em workspace ou compartilhar relatório são ações posteriores, cada uma com destino e autoridade próprios. [render_simulado.py](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/render_simulado.py) monta o espelho do produto no repositório e [validate_assistant.py](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/validate_assistant.py) verifica esse produto; nenhum deles executa esta EDA ou publica o resultado da turma. Um percurso falho termina com diagnóstico e recuperação causal, não com uma frase de sucesso. Um percurso contratualmente concluído termina com evidência preservada e interpretação revisável, sem prometer aprovação de negócio ou publicação automática.


<!-- editorial:exclude:start -->
[Anterior: MU19](#mu19) · [Sumário](#sumario-mu) · [Guia por pergunta](#perguntas-mu) · [Trilhas](#trilhas-mu) · [MT30](MANUAL_TECNICO_V2.md#mt30)
<!-- editorial:exclude:end -->
