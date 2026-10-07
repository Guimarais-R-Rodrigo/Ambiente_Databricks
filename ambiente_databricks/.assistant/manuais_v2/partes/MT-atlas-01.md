<a id="atlas-documental"></a>
# MT atlas 01

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0001"></a>
<a id="doc-0001"></a>
### D0001 — Manual técnico vigente do produto

Este manual existe para que uma pessoa consiga entender o Hub sem depender do autor de cada pasta. Ele reúne conceitos que se repetem em vários recursos: o que é uma função, como um import encontra um módulo, por que uma tabela não é um arquivo Python e onde procurar um helper. Conceitualmente, transforma a coleção em um ambiente explicável; tecnicamente, conserva uma referência humana única para fundamentos, catálogo e índice de termos. A redação editável está em `ambiente_databricks/.assistant/`, e o próprio livro no produto e suas partes de leitura oferecem consulta antes da implantação.

O documento desenvolve uma progressão: pastas e caminhos, API e contratos, Python, dados e Spark, contexto da Genie Code, apresentação, métodos analíticos, micromodelos, integridade da instalação e diagnóstico de falhas. READMEs locais explicam a escolha de um objeto; o manual conecta os conceitos entre objetos. O renderer leva a cópia do produto ao simulado, e mantenedores preservam a redação única para evitar respostas divergentes.

Seu estado é importante: este é o manual **vigente** antes da consolidação da edição V2. A existência dos novos capítulos em construção não autoriza substituir links de produto nem assumir que o usuário já recebeu a nova obra. Assinatura, efeito e limite de um helper ainda precisam ser conferidos no código e no README do objeto correspondente.

<!-- editorial:exclude:start -->
Fonte: [MANUAL_TECNICO_V2.md](../../MANUAL_TECNICO_V2.md). Contexto: [MT02](MT-parte-i.md#mt02).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Próximo: D0002](#doc-0002) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0002"></a>
<a id="doc-0002"></a>
### D0002 — Entrada do ecossistema `.assistant`

O README da raiz do produto responde à primeira pergunta de quem encontrou
a pasta: para que serve este conjunto e por onde começar? Ele existe porque
uma árvore de arquivos não explica sozinha a diferença entre conversar com
uma skill, preencher um briefing e executar Python. Conceitualmente, apresenta
o trabalho analítico como uma sequência de objetivo, método, implementação e
revisão. Tecnicamente, é uma entrada Markdown transportável junto do produto,
com links relativos que conservam a proximidade entre a explicação e seus
recursos quando a pasta muda de ambiente.

Seus blocos organizam o mapa de uso, as cinco famílias e a área de Micromodelos, o fluxo de contexto,
a preparação da biblioteca e as responsabilidades de compute e segurança. Os
exemplos mostram chamadas explícitas e distinguem mecanismos nativos do Genie
Code de componentes criados pelo Hub. O Visual Lab aparece como caminho para
experimentar aparência; o Concierge, para descobrir recursos. Nenhuma dessas
entradas torna execução ou publicação automática.

O leitor consome esse documento diretamente; imagens e índices enriquecem a
consulta. O renderer e o empacotamento transportam sua versão de produto.
Ao manter o README, conferir destinos dos links, procedência dos assets e
estados citados. Sua visão geral não substitui as assinaturas dos módulos,
os contratos de execução ou a evidência datada de homologação.

<!-- editorial:exclude:start -->
Fonte: [README do produto](../../README.md).
Detalhamento: [MT01](MT-parte-i.md#mt01),
[MT02](MT-parte-i.md#mt02), [MU01](MU-parte-i.md#mu01).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0001](#doc-0001) · [Próximo: D0003](#doc-0003) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0003"></a>
<a id="doc-0003"></a>
### D0003 — Índice dos padrões de autoria

O README de `hub_padroes/` ajuda quem precisa transformar uma solução pontual em peça compreensível do Hub. Sem essa entrada, seria fácil copiar a pasta mais próxima e herdar uma forma inadequada. Ele apresenta seis tipos de artefato de autoria — README, snippet, script, prompt, skill e notebook — e liga cada tipo a seu molde e exemplar. Essa classificação responde “que arquivo estou criando?”; não altera os cinco componentes funcionais descritos na entrada geral do produto.

O documento também organiza um fluxo de necessidade, escolha de tipo, preenchimento, validação de forma e revisão de conteúdo. Quem cria o objeto o consulta; a skill de criação pode orientar a aplicação dos templates, mas a coleção não entra automaticamente no contexto da Genie Code. `auditoria/`, `output/`, identidade visual e Skill Enforcement Framework aparecem como padrões transversais, não tipos adicionais. O README explicita que os exemplos de campanha ensinam formato e não são biblioteca operacional.

Tecnicamente, este índice é o ponto de ligação entre moldes específicos e regras de procedência. Mantê-lo significa verificar se links e estados de cada padrão ainda correspondem aos arquivos reais, inclusive quando surge um novo recurso transversal. Seguir o template melhora consistência estrutural; não prova que uma função está correta, que seu notebook foi executado no destino ou que a decisão de negócio foi aprovada.

<!-- editorial:exclude:start -->
Fonte: [hub_padroes/README.md](../../hub_padroes/README.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0002](#doc-0002) · [Próximo: D0004](#doc-0004) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0004"></a>
<a id="doc-0004"></a>
### D0004 — Molde de auditoria de resultado analítico

Este template existe para confrontar uma entrega analítica com o pedido, o contrato e a evidência disponível. A ideia central é simples: um texto coerente ou um PASS salvo não comprova que o resultado foi reverificado. O arquivo organiza escopo, fontes, execução observada, conferência independente e conclusão. Ele não é relatório de uma auditoria já concluída.

O molde pede destinatário, artefato e versão, recursos autorizados e critérios do caso. Em seguida, distingue implementação consultada, ambiente e resultado observado, oráculo independente e efeitos de persistência. Quando essas informações faltam, exige registrar NÃO ACESSÍVEL, NÃO EXECUTADO, NÃO REVERIFICADO ou NÃO INFORMADO, em vez de preencher a lacuna com uma conclusão. Cada achado deve trazer localização, afirmação, evidência, contracaso, impacto e correção proposta; fato, hipótese e ausência de prova permanecem separados.

A equipe revisora consome o template, e o responsável pela entrega confronta os achados antes de corrigir. Em skill protegida, a revisão preserva runner, Receipt, verificador e autoridade de conclusão. O aceite se limita ao escopo comprovado: não promove policy, autoriza publicação nem substitui decisão de negócio. Na manutenção, adapte critérios ao caso e registre o que foi realmente reexecutado, sem chamar revisão apenas textual de auditoria operacional.

<!-- editorial:exclude:start -->
Fonte: [auditoria/template.md](../../hub_padroes/auditoria/template.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0003](#doc-0003) · [Próximo: D0005](#doc-0005) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0005"></a>
<a id="doc-0005"></a>
### D0005 — Como recuperar uma proposta de tema recusada?

`ERROS.md` traduz a recusa do resolvedor de temas em uma próxima ação segura. Conceitualmente, separa configuração inválida, pacote defeituoso e falta de dependência; tecnicamente, organiza códigos de `ThemeError` pelas três informações que a interface pode mostrar: `code`, `field` e `action`. Quem recebe uma falha no exemplo, no Visual Lab ou em um consumidor pode procurar o código sem revelar o valor recebido, pois a mensagem usa nomes conhecidos do contrato.

A tabela distingue entrada JSON, schema, contexto, cor, caminho, hash, recurso e integridade do resultado. Uma chave repetida pede correção da cópia, não escolha arbitrária; `PATH_SYMLINK` pede arquivo regular dentro da raiz autorizada; `HASH_MISMATCH` pede comparação com o recibo correto. Erros do próprio schema são destinados ao mantenedor. O guia operacional remete a essa tabela quando a demonstração falha, e `TOKENS.md` fornece limites para corrigir campos.

Na manutenção, sincronize códigos e ações com o núcleo e seus testes, mantendo a recusa fechada e sem eco de dados desconhecidos. A tabela não certifica uma paleta, não instala bibliotecas e não transforma um erro de runtime em aprovação visual.

<!-- editorial:exclude:start -->
Fonte: [ERROS.md](../../hub_padroes/identidade_visual/ERROS.md). Detalhe: [MT23](MT-parte-vi.md#mt23).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0004](#doc-0004) · [Próximo: D0006](#doc-0006) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0006"></a>
<a id="doc-0006"></a>
### D0006 — Como experimentar um tema sem mudar o padrão?

`GUIA_OPERACIONAL.md` transforma o contrato visual em uma sequência para quem abre o primeiro exemplo. Ele começa pelas dependências e pela localização da pasta `.assistant`, depois manda executar a preparação antes da referência, da cópia e do erro esperado. Na referência, o leitor confere contexto `notebook`, 48 tokens e `#005CA9`; na cópia, observa `#112233` sem mutar o original; retirar `brand.primary` demonstra `SCHEMA_REQUIRED`. Essas saídas mostram validação e imutabilidade em memória, não instalação no workspace.

O documento também encaminha usos opcionais: componentes HTML V04, Visual Lab V05, consumidores V07, App V10 e ponte AI/BI V11. Cada rota recebe um `ResolvedTheme` íntegro ou uma derivação controlada e preserva o comportamento legado quando não escolhida. `load_theme` exige raiz confiável e pode fixar SHA-256; `export_theme` devolve bytes, sem salvar.

O guia atual organiza as rotas por tarefa; o estado vivo registra V00–V13 e V14 S0/S1 integradas no Git, sem converter integração em homologação do destino. Ao mantê-lo, confira comandos, exemplo e links com o código, e separe demonstração, persistência de sessão, aprovação e publicação.

<!-- editorial:exclude:start -->
Fonte: [GUIA_OPERACIONAL.md](../../hub_padroes/identidade_visual/GUIA_OPERACIONAL.md). Estado: [V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). Detalhe: [MT23](MT-parte-vi.md#mt23).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0005](#doc-0005) · [Próximo: D0007](#doc-0007) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0007"></a>
<a id="doc-0007"></a>
### D0007 — Onde começa e termina o contrato de identidade visual?

O README de `identidade_visual` é a entrada para quem precisa consumir ou manter o Sistema de Temas. Ele aponta ao guia de primeiro uso, aos erros, ao objeto `visual.tema` e à ponte AI/BI, enquanto separa três fontes: `theme.schema.json` governa campos e limites, `TOKENS.md` é dicionário gerado, e a política de aprovação fica fora do JSON. Isso impede tratar um arquivo validado como identidade autorizada.

As seções explicam contextos completos `notebook`, `readme` e `presentation`, cores `#RRGGBB`, formato `hub-json-v1` e três identificadores com alcances diferentes: `raw_sha256` para bytes originais, `content_sha256` para exportação canônica e `fingerprint` para configuração mais dependências. O import do núcleo não carrega Spark ou Streamlit; dependências de validação são importadas na chamada. Exemplos e `assets.json` são derivados, com recursos verificados por hash.

O texto atual descreve capacidades e limites por consumidor. O estado vivo registra V00–V13 e V14 S0/S1 integradas no Git; integração não comprova publicação, acessibilidade ou aprovação. Na manutenção, reconcilie esse estado temporal sem duplicar schema nem criar contexto `app` ou `aibi`.

<!-- editorial:exclude:start -->
Fonte: [README de identidade visual](../../hub_padroes/identidade_visual/README.md). Estado: [V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). Detalhe: [MT23](MT-parte-vi.md#mt23).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0006](#doc-0006) · [Próximo: D0008](#doc-0008) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0008"></a>
<a id="doc-0008"></a>
### D0008 — O que a referência de tokens permite consultar?

`TOKENS.md` é a vista humana gerada de `theme.schema.json`, útil quando um proponente precisa reconhecer um campo antes de editar uma configuração. As entradas `notebook` começam por marca, texto e superfícies, avançam para estados, paletas, fonte e dimensões de gráfico, seção, cartão e badge. A parte editorial cobre cores, tipografia, geometria e canvas de README e apresentação. Cada verbete expõe unidade, tipo, amostra de referência, limites, papel de edição, controle declarado, contexto, consumo atual e cobertura de prévia e AI/BI.

A forma repetitiva do documento serve à consulta por caminho completo. Por exemplo, `palette.diverging` exige quantidade ímpar para existir cor central, mas não escolhe o zero dos dados; `semantic.positive` define cor favorável, mas não tem leitura visual direta nas APIs notebook atuais. `font.family` usa identificadores permitidos, sem CSS livre. O README central ensina o alcance do sistema; esta tabela ajuda a interpretar `SCHEMA_*` em `ERROS.md`.

O mantenedor regenera a referência a partir do schema e da cobertura, sem alterar verbetes à mão. Seus defaults são amostras declarativas, nunca valores injetados. Campo válido não garante aplicação: tokens editoriais podem ser preservados sem leitura pelos renderers, e o canvas não redimensiona figuras.

<!-- editorial:exclude:start -->
Fonte: [TOKENS.md](../../hub_padroes/identidade_visual/TOKENS.md). Estado: [V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). Detalhe: [MT23](MT-parte-vi.md#mt23).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0007](#doc-0007) · [Próximo: D0009](#doc-0009) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0009"></a>
<a id="doc-0009"></a>
### D0009 — Como levar uma proposta ao tema de um dashboard?

O guia AI/BI organiza uma tarefa que atravessa dois contratos diferentes. Primeiro distingue tema do workspace, administrado como padrão, de tema local de dashboard em rascunho; aplicar o primeiro a um dashboard existente cria um snapshot, sem propagação automática de alterações futuras. Depois apresenta `project_theme()`: um `ResolvedTheme` de contexto `notebook` produz classificação auditável dos tokens como `translated`, `approximated` ou `unsupported`. Essa projeção do Hub não é o JSON aceito por `Import theme`.

Para preparar candidato nativo, o roteiro exige export real de um dashboard autorizado, conservação do original e SHA-256 fixado. Um mantenedor revisa JSON Pointers já presentes; `bind_native_template()` só substitui os três campos de correspondência direta quando template e hash combinam. O fixture sintético serve ao raciocínio sobre KPI, série, barras, tabela e filtros, não é formato Databricks. A revisão compara visual claro/escuro e preserva datasets, filtros e agregações.

Na manutenção, confira o guia contra a matriz V11 e documentação oficial vigente antes de orientar operação real. V11 está integrada no Git, mas `A11-01` permanece FAIL e o gate operacional `V12-AIBI-02` bloqueado; importar tema e publicar dashboard continuam ações separadas.

<!-- editorial:exclude:start -->
Fonte: [guia AI/BI](../../hub_padroes/identidade_visual/aibi/GUIA_PRIMEIRO_USO.md). Estado: [V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0008](#doc-0008) · [Próximo: D0010](#doc-0010) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0010"></a>
<a id="doc-0010"></a>
### D0010 — Por que a ponte AI/BI conserva lacunas explícitas?

O README da pasta `aibi` explica a arquitetura da ponte V11 a quem implementa ou revisa sua projeção. `ResolvedTheme` `notebook` continua a fonte configurável: não há segundo tema canônico nem novo `context="aibi"`. A matriz `aibi_mapping.json` classifica os 48 tokens segundo capacidades documentadas de dashboard. O módulo `aibi_theme.py` produz projeção do Hub e binder local; `dashboard_sintetico.json` dá um cenário de teste sem fingir ser arquivo nativo importável.

A distinção técnica central é entre tradução direta, aproximação e falta de equivalência. Só três correspondências `translated` com `binding_strategy="direct"` admitem troca automática em campos existentes de um export nativo fixado por hash. As 23 aproximações exigem julgamento humano; 22 itens não suportados permanecem visíveis. A ausência de schema oficial completo do export impede gerar JSON nativo a partir de palpites. Tema de workspace e tema de dashboard têm autoridade e persistência diferentes.

O guia de primeiro uso conduz a operação; este README justifica os limites da implementação. Na manutenção, alinhe contagens, arquivo de mapping e código sem prometer SDK, publicação ou homologação geral. V11 está integrada no Git; o estado V14 mantém `A11-01` FAIL e a operação AI/BI posterior condicionada à autorização.

<!-- editorial:exclude:start -->
Fonte: [README AI/BI](../../hub_padroes/identidade_visual/aibi/README.md). Estado: [V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0009](#doc-0009) · [Próximo: D0011](#doc-0011) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0011"></a>
<a id="doc-0011"></a>
### D0011 — O que é necessário para implantar e reverter o App visual?

`DEPLOY_ROLLBACK.md` encaminha o mantenedor ao runbook administrativo em `docs/guias/temas/DEPLOY_ROLLBACK_APP.md`. Nesse runbook, a primeira etapa gera, em checkout limpo, um bundle V10 local e confere seu `V10_APP_MANIFEST.json`; gerar não executa CLI nem faz upload. No destino, a pessoa com permissão associa um Unity Catalog Volume pela chave `theme_storage`, concede leitura e gravação ao service principal e restringe `CAN USE` aos grupos definidos pelo proprietário. `app.yaml` recebe o caminho pelo recurso, sem gravar identificadores corporativos no Git.

O smoke posterior testa abertura, validação, comparação, salvar/reabrir sessão, histórico e isolamento entre duas identidades. Ele também verifica a ausência de ações de aprovar ou publicar. Se a aplicação falhar, o procedimento manda inspecionar logs e recurso de armazenamento, sem recorrer a `/tmp`, modo local ou PAT para contornar produção.

Rollback retorna o código a um commit aprovado e repete o smoke, mantendo o mesmo Volume e as sessões. Não desfaz tema compartilhado, pois a V10 não publica temas. Na manutenção, sincronize comando, manifesto e permissões com o bundle real; o estado V14 mantém `V12-APP-01` bloqueado por autorização, sem deploy comprovado por esta documentação.

<!-- editorial:exclude:start -->
Fonte: [DEPLOY_ROLLBACK.md](../../hub_padroes/identidade_visual/databricks_app/DEPLOY_ROLLBACK.md). Procedimento: [runbook administrativo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/guias/temas/DEPLOY_ROLLBACK_APP.md). Estado: [V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0010](#doc-0010) · [Próximo: D0012](#doc-0012) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0012"></a>
<a id="doc-0012"></a>
### D0012 — O que a pessoa faz no primeiro uso do App?

O guia do App descreve a experiência de autoria visual sem exigir Python. Antes de abrir, a pessoa confirma acesso ao App, ambiente correto e armazenamento de sessões no Unity Catalog Volume. Na tela inicial escolhe uma base de demonstração; um novo rascunho abandona ajustes não salvos na memória, mas preserva sessões já gravadas. Em seguida, aplica e valida a proposta inteira: erro mantém a última versão válida, enquanto desfazer e restaurar base oferecem retornos distintos.

A comparação Base × Proposta usa os mesmos dados sintéticos em cabeçalho, KPI, barras, série, heatmap e tabela. Salvar exige nome novo e confirmação com revisão, profundidade de histórico e prefixo do hash do manifesto. Reabrir verifica hashes antes de reconstruir estado; sessão incompleta ou adulterada é recusada. Códigos `APP_` indicam identidade ou armazenamento; `LAB_` pertencem ao laboratório reutilizado.

O documento é consumido por autores autorizados depois de um deploy que o Git, por si só, não comprova. Não há botão de aprovar, publicar, promover ou apagar histórico; fechar a página tampouco publica. Na manutenção, conferir nomes de telas e mensagens com App e Visual Lab, preservando os limites de autorização e retenção do destino.

<!-- editorial:exclude:start -->
Fonte: [guia do App](../../hub_padroes/identidade_visual/databricks_app/GUIA_PRIMEIRO_USO.md). Estado: [V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0011](#doc-0011) · [Próximo: D0013](#doc-0013) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0013"></a>
<a id="doc-0013"></a>
### D0013 — Qual é o contrato técnico do App de gestão visual?

O README V10 explica a superfície Streamlit de autoria `authoring_only`. `app.py` apresenta a interface; `app_service.py` concentra identidade e persistência e reaproveita o núcleo de temas e o Visual Lab. Assim, a UI não vira segunda fonte de schema ou validação. O App gerencia propostas de contexto `notebook`; sua existência não implementa um contexto temático `app`.

O fluxo exige `HUB_THEME_VOLUME` sob `/Volumes/` em produção, usa `X-Forwarded-User` encaminhado pelo proxy e transforma a identidade em namespace SHA-256 para listar as sessões próprias; esse namespace não cifra conteúdo nem substitui permissões do Volume. O recurso `theme_storage` em `app.yaml` fornece o caminho. Cada sessão guarda base, proposta, histórico e `session.json` escrito por último; a reabertura recusa hashes divergentes. O modo `HUB_THEME_LOCAL_DEV` com usuário sintético serve apenas ao desenvolvimento.

O README relaciona configuração, papéis, custos, guardas e smoke; o guia de primeiro uso ensina a interação, e o procedimento de deploy trata autorização e rollback. A indicação antiga “V10 candidata” foi retirada: V10 está integrada no Git, mas V14 mantém `V12-APP-01` bloqueado. Ao manter esta entrada, conferir código, recurso e política sem atribuir à interface aprovação, publicação ou ACL comprovada no destino.

<!-- editorial:exclude:start -->
Fonte: [README do App](../../hub_padroes/identidade_visual/databricks_app/README.md). Estado: [V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). Detalhe: [MT24](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0012](#doc-0012) · [Próximo: D0014](#doc-0014) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0014"></a>
<a id="doc-0014"></a>
### D0014 — Bloco de proveniência de output durável

Um relatório que sobrevive ao chat precisa deixar claro de onde veio. O padrão `output/proveniencia.md` oferece um bloco YAML para registrar esse rastro: momento, skill produtora, contrato e versão, pedido original, recursos e período, ambiente, estado de execução, validações, escritas e limitações. Conceitualmente, ele separa uma proposta de uma execução e impede que uma conclusão circule sem suas condições. Tecnicamente, é um formato textual a preencher, não um registro automático criado pela Genie Code.

Autores de relatórios, notebooks ou especificações duráveis consomem o modelo quando precisam que outra pessoa reconstrua a origem da entrega. Um campo como `execucao: proposto` é diferente de `executado`; `validacoes_executadas: []` não pode ser preenchido com testes que apenas foram planejados. O arquivo manda usar `NÃO INFORMADO` onde a versão ou snapshot não é conhecido, em vez de inventá-los. Também separa recurso citado no pedido de recurso efetivamente lido. O produtor escreve o bloco; o revisor compara cada campo com evidências da tarefa.

Na manutenção, atualize o padrão quando a equipe mudar o que precisa rastrear, avaliando os consumidores dos campos existentes. Copiar o YAML completo para toda resposta curta criaria ruído e falsa aparência de auditoria: o próprio padrão se destina a outputs duráveis. Mesmo preenchido, ele não substitui logs, resultados ou aprovação externa quando essas provas forem necessárias.

<!-- editorial:exclude:start -->
Fonte: [output/proveniencia.md](../../hub_padroes/output/proveniencia.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0013](#doc-0013) · [Próximo: D0015](#doc-0015) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0015"></a>
<a id="doc-0015"></a>
### D0015 — Guia local do prompt de campanha

Este README explica **quando** usar o briefing exemplar de campanha antes que alguém copie seu texto para uma conversa. Seu problema é evitar a conclusão apressada “o segmento com maior taxa recebe todo o orçamento”: tamanho dos grupos, período e limite de contatos também importam. A abertura resume finalidade, requisitos, saída e situações em que o formulário não serve. As quinze seções do contrato de README de objeto desenvolvem conceito, escolha, preenchimento, interpretação e alternativas.

O autor mantém esta explicação ao lado do briefing e do notebook demonstrativo; quem quer criar um prompt semelhante consulta os três. O orçamento deve estar em **número de contatos**, e a resposta pedida à IA continua sujeita a revisão. O README separa o formulário do preparo do notebook, que escreve tabela persistente e é dispensável para preencher o briefing. Uma recomendação de skill no texto não comprova que ela foi carregada na interação real.

O limite do objeto é explícito: campanha encerrada e recorte conhecido ajudam a formular uma priorização, mas o resultado histórico não demonstra que oferta ou canal causou a resposta. A pasta é exemplar dos padrões, não prompt operacional homologado. Ao manter o README, confira campos e links do briefing; não apresente saída inventada como captura da Genie Code nem transforme o exercício em autorização de acesso à tabela.

<!-- editorial:exclude:start -->
Fonte: [README de analisar_campanha](../../hub_padroes/prompt/analisar_campanha/README.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0014](#doc-0014) · [Próximo: D0016](#doc-0016) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0016"></a>
<a id="doc-0016"></a>
### D0016 — Briefing preenchível de campanha

O arquivo `analisar_campanha.md` é a peça que uma pessoa pode preencher e fornecer ao chat. Ele existe porque “mostre a taxa por segmento” omite informação necessária à decisão de alocação: qual campanha, qual período, quantos contatos cabem na próxima e o que os dados não permitem concluir. O texto oferece os campos `{{TABELA}}`, `{{PERIODO}}` e `{{ORCAMENTO_CONTATOS}}`, explica a unidade deste último e apresenta um bloco pronto para colar depois da substituição.

O briefing pede taxas por segmento e canal, uma priorização justificada, código PySpark reproduzível e uma síntese para quem decide orçamento. Também orienta conferir base de cada grupo, capacidade de contato e repetição de pessoas. O autor do prompt mantém os campos e verificações; o usuário fornece valores e contexto; o assistente pode propor uma resposta que precisará de execução e revisão. O cabeçalho recomenda `@hub-ml-eda-profissional`, mas a presença desse nome no arquivo não seleciona a skill sozinha.

Esta é uma referência de forma em `hub_padroes/`, não um briefing auto-descoberto ou garantia de análise executada. Mesmo preenchido corretamente, descreve resultado observado e não identifica causalidade da campanha. Na manutenção, preserve a ligação entre cada campo e a decisão que ele altera; um placeholder sem propósito vira formulário de aparência completa e conteúdo insuficiente.

<!-- editorial:exclude:start -->
Fonte: [analisar_campanha.md](../../hub_padroes/prompt/analisar_campanha/analisar_campanha.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0015](#doc-0015) · [Próximo: D0017](#doc-0017) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0017"></a>
<a id="doc-0017"></a>
### D0017 — Molde para um prompt novo

Este template ajuda a transformar um pedido repetido em briefing do Hub sem fingir que texto no repositório é ferramenta automaticamente carregada. Ele define a pasta de prompt com README, arquivo `.md` do pedido e notebook de exemplo, sem `__init__.py`, porque não existe função Python para importar. Conceitualmente, o formulário obriga o autor a explicitar condições que mudam a resposta; tecnicamente, preserva uma estrutura reconhecível para o leitor localizar o texto colável e a demonstração.

O briefing proposto declara uma skill recomendada ou opções quando não há rota única. Cada placeholder explica por que a informação é necessária. Depois do bloco para colar, uma seção lista lacunas previsíveis a conferir. O notebook tem preparo executável, prompt preenchido e captura de uma resposta real comentada; esta última depende de uma pessoa e não deve ser inventada. O autor usa o molde, e revisores confrontam sua aplicação com o problema concreto.

O template é critério para **novo prompt**, não descrição automática de todos os briefings antigos do produto. Seu exemplo de campanha continua fora da biblioteca operacional. Na manutenção, ajuste regras quando o fluxo de criação mudar e confira se exemplos e checklist continuam coerentes; preencher todos os títulos sem dados, limites e revisão honesta não torna o pedido seguro.

<!-- editorial:exclude:start -->
Fonte: [prompt/template.md](../../hub_padroes/prompt/template.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0016](#doc-0016) · [Próximo: D0018](#doc-0018) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0018"></a>
<a id="doc-0018"></a>
### D0018 — Checklist editorial do README de objeto

Este checklist ajuda um revisor a perguntar se o README de um snippet, script ou prompt realmente ensina o uso do objeto. Ele existe porque um validador pode encontrar quinze títulos e links corretos sem perceber uma assinatura inventada, um efeito omitido ou uma interpretação errada. Conceitualmente, separa forma de fidelidade e didática; tecnicamente, subordina a revisão ao contrato de README de objeto 1.0.0 e exige fonte identificada para cada avaliação.

As etapas incluem registrar arquivo, hashes, autor e revisor; conferir marcador, seções e links; comparar README com implementação, fachada e notebook; e avaliar conceito, escolha, retorno, uso seguro, interpretação, procedência e clareza. Classifica dimensões como satisfatória, ajuste necessário ou bloqueadora sem esconder defeito material numa média. A equipe de revisão usa o checklist; o autor corrige achados; o validador automático fornece apenas evidência de estrutura. Uma revisão pelo próprio autor não deve ser chamada de independente.

O arquivo também distingue rascunho, estrutura conferida, revisão técnica, revisão didática e aceite humano. Nenhum desses estados significa teste Databricks ou publicação. Na manutenção, alinhe a rubrica ao contrato e aos gates atuais sem reaproveitar automaticamente o aceite de um lote anterior. Seu limite é deliberado: perguntar e registrar evidência não substitui executar um helper, observar custo ou conferir permissão no workspace.

<!-- editorial:exclude:start -->
Fonte: [readme/checklist_objeto.md](../../hub_padroes/readme/checklist_objeto.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0017](#doc-0017) · [Próximo: D0019](#doc-0019) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0019"></a>
<a id="doc-0019"></a>
### D0019 — Exemplo de README agregador

O `readme/exemplo.md` mostra como um README de seção pode conduzir alguém da pergunta de negócio até os objetos daquela seção. Ele foi criado para que o template geral não fique abstrato: o texto preenche identidade, finalidade, visão estrutural, chamada ilustrativa, inventário de objetos, limites e continuação. Conceitualmente, ensina o que um índice de coleção deve explicar; tecnicamente, serve como exemplo de **escala padrão**, diferente do README de objeto com quinze seções.

O tema é uma campanha de relacionamento. Árvore, tabela e diagrama associam taxa, cobertura e validação dos dados à decisão. Uma saída histórica ilustra precisão diferente entre grupos. Um autor de README agregador consulta o exemplo; um revisor compara os itens listados com as pastas reais. Não copie nomes e contagens de uma demonstração para outra coleção.

O limite mais importante está declarado na abertura: **`hub_snippets/campanha/` não existe** no produto. O caminho de import e os objetos dessa seção são parte do exemplo preenchido, não uma rota atual para produção. A saída capturada pertence ao contexto histórico indicado ali; não é evidência de reexecução nesta edição. Ao manter o exemplar, preserve esses avisos para que sua didática não vire uma instrução operacional falsa.

<!-- editorial:exclude:start -->
Fonte: [readme/exemplo.md](../../hub_padroes/readme/exemplo.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0018](#doc-0018) · [Próximo: D0020](#doc-0020) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0020"></a>
<a id="doc-0020"></a>
### D0020 — Template geral de README

Este arquivo padroniza READMEs que explicam **coleções** do Hub, como uma categoria de snippets ou a raiz do produto. Sua razão de existir é de navegação: quem chega a uma pasta quer saber para que serve, o que ela contém, como usar e onde continuar. O template define escalas curta, padrão e longa conforme a complexidade da decisão e a quantidade de objetos a explicar. A escala de objeto tem molde próprio, com quinze seções; não se deve aplicar as nove posições agregadoras ao README de um helper isolado.

O arquivo descreve título, aviso de natureza quando necessário, finalidade, visão estrutural, uso copiável, inventário dos filhos, limites, perguntas reais e próximos links. Também recomenda bloco visual e termos definidos cedo. Autores de READMEs o consultam para organizar a página; revisores verificam que a tabela de filhos reflete a árvore real e que comandos foram testados. Poucos arquivos não tornam a explicação automaticamente curta: avalie decisões, grupos de objetos e critérios de escolha.

Exemplos orientam a organização, sem fixar contagens mutáveis de categorias. Na manutenção, confira a árvore e a necessidade do leitor antes de escolher a escala. O molde oferece ordem e perguntas, não certifica a exatidão de uma API ou de uma saída; o objeto e sua implementação continuam sendo fontes para comportamento técnico.

<!-- editorial:exclude:start -->
Fonte: [readme/template.md](../../hub_padroes/readme/template.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0019](#doc-0019) · [Próximo: D0021](#doc-0021) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0021"></a>
<a id="doc-0021"></a>
### D0021 — Contrato de README local de objeto

O `template_objeto.md` é o dono do contrato de README para pastas operacionais de snippet, script e prompt. A versão 1.0.0 pede abertura rápida e quinze seções numeradas: o que é, problema, quando escolher ou evitar, funcionamento, exemplo, requisitos, entrega, uso, decisões, riscos, alternativas, conferência, arquivos e referências. Essa ordem coloca conceito e escolha antes do código, para que alguém não execute um helper apenas porque encontrou seu nome.

Tecnicamente, o contrato distingue documentação de comportamento. O README explica a função e aponta para a implementação ou briefing que define os identificadores reais. O notebook de exemplo pode criar ou sobrescrever uma tabela sintética mesmo quando o helper só lê; por isso seus efeitos são descritos separadamente. O autor do objeto preenche o molde, revisores confrontam texto e código, e o validador confere marcador, títulos e links. Um guia agregador usa outro template; `SKILL.md` e `__init__.py` também não recebem essas quinze seções.

Na manutenção, preserve nomes de parâmetros e colunas existentes, mesmo quando a prosa é traduzida. Divergência entre docstring, exemplo e implementação deve ser apontada, não escondida com uma explicação conveniente. Passar no gate de estrutura mostra que a forma foi mantida; não demonstra adequação estatística, execução no Databricks, ausência de efeitos ou aceite humano da nova redação.

<!-- editorial:exclude:start -->
Fonte: [readme/template_objeto.md](../../hub_padroes/readme/template_objeto.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0020](#doc-0020) · [Próximo: D0022](#doc-0022) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0022"></a>
<a id="doc-0022"></a>
### D0022 — Guia do script exemplar de campanha

Este README apresenta `checar_base_campanha` como exemplo de diagnóstico antes de calcular taxa de resposta. Seu propósito é ensinar a diferença entre encontrar uma condição que precisa de decisão e alterar dados para fazê-la desaparecer. O script lê uma tabela nomeada, compara linhas e chaves, examina resposta nula ou fora de 0/1 e identifica segmentos pequenos; devolve status, contagens, limites e alertas. Um `fail` pede investigação humana, não prova que todo dado é inutilizável nem cancela automaticamente um job.

O arquivo atende ao contrato de quinze seções. Para criar um diagnóstico semelhante, consulte este README junto ao módulo e ao molde de script. Para **usar** um utilitário do produto, procure o README do objeto operacional: este exemplar em `hub_padroes/` não é homologado para produção. A implementação não altera a tabela; seu notebook de demonstração **sobrescreve e depois remove uma tabela persistente**. Leia esse aviso antes de executar o exemplo.

Na manutenção, confronte cada limiar e coluna descritos com a implementação e declare quando o diagnóstico não cobre regras de negócio ou tempo. Um status `pass` nas checagens disponíveis não certifica qualidade geral da campanha. O README ensina a ler o resultado delimitado, não substitui acesso autorizado nem teste do runtime de destino.

<!-- editorial:exclude:start -->
Fonte: [README de checar_base_campanha](../../hub_padroes/script/checar_base_campanha/README.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0021](#doc-0021) · [Próximo: D0023](#doc-0023) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0023"></a>
<a id="doc-0023"></a>
### D0023 — Molde de script e exemplo diagnóstico

O template de script orienta tarefas de inspeção, transformação ou governança, com entradas e efeitos próprios. Ele propõe pasta com README, fachada `__init__.py`, módulo de implementação e notebook de exemplo. No exemplar diagnóstico, a entrada é o nome da tabela e o retorno é um dicionário com `status`, `limites`, `checagens` e `alertas`. Conceitualmente, a saída revela tanto a política aplicada quanto os números observados, permitindo decidir se a análise prossegue. Nenhuma escrita é autorizada pelo molde.

O autor usa o molde para especificar assinatura, mensagens, custo e efeitos. A fachada expõe a API pública, e o README local explica o comportamento real. O status `fail` pede decisão humana; não sentencia toda a base. O exemplar de campanha ensina o formato, mas seu notebook pode escrever dados de demonstração, diferentemente do script que só lê.

O limite editorial é crucial: **os scripts operacionais do Hub não têm todos esse retorno**. `rfv_calculator` recebe nome de tabela e devolve DataFrame; `schema_to_yaml` recebe nome e devolve texto. Não documente a categoria inteira como pass/warn/fail. A docstring do exemplar fala em três varreduras; o corpo mostra duas ações `collect()` depois de agregações distintas, e não fixa o plano físico do Spark. Ao manter o template, confira afirmações de custo contra o código.

<!-- editorial:exclude:start -->
Fonte: [script/template.md](../../hub_padroes/script/template.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0022](#doc-0022) · [Próximo: D0024](#doc-0024) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0024"></a>
<a id="doc-0024"></a>
### D0024 — Exemplo de `SKILL.md` para campanha

Este arquivo mostra uma skill preenchida com o tema de análise de campanha, para que o autor veja como um método pode ser expresso sem confundi-lo com uma função Python. O cabeçalho declara `name` e `description`, com situação de uso e limites; o corpo explica caso típico, contraexemplos, fluxo, helpers a usar e formato de entrega. A razão técnica de listar caminhos dos helpers é que a presença de uma skill no contexto do agente não importa módulos automaticamente no notebook.

O roteiro pede confirmar a unidade de análise, declarar orçamento em contatos, medir taxa com precisão, distinguir relevância prática e dizer o que a recomendação não sustenta. A tabela liga checagem, medição, comparação temporal e formatação a caminhos fictícios; não tente importá-los. Um criador de skill consulta essa forma; um revisor examina se a descrição disputa o mesmo vocabulário de skills publicadas e se os helpers citados existem no destino pretendido.

Este é um **exemplar não publicado** em `hub_padroes/skill/exemplo/`, fora da pasta ativa `.assistant/skills/`. Copiá-lo para o catálogo criaria uma nova candidata ao roteamento, não apenas mais documentação. As rotas de campanha no exemplo são didáticas e precisam de verificação antes de uso operacional. Na manutenção, preserve esse estado explícito e nunca apresente a leitura do arquivo como prova de seleção ou execução de skill.

<!-- editorial:exclude:start -->
Fonte: [skill/exemplo/SKILL.md](../../hub_padroes/skill/exemplo/SKILL.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0023](#doc-0023) · [Próximo: D0025](#doc-0025) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0025"></a>
<a id="doc-0025"></a>
### D0025 — Molde para construir uma Agent Skill

Este template orienta quem vai criar uma skill em `.assistant/skills/` para um tipo de trabalho recorrente. Uma skill não é uma função importável; ela ajuda o agente a reconhecer quando um método se aplica, quais perguntas fazer, que recursos consultar e como entregar um resultado revisável. Tecnicamente, o molde define pasta com nome em hífens, `SKILL.md`, `name` igual ao nome da pasta e `description` que descreve **quando usar**, inclusive o que fica fora do escopo. Recursos relativos, como templates e referências, são opcionais e consultados conforme a tarefa.

O corpo proposto contém caso típico e contraexemplos, fluxo ordenado, caminhos explícitos dos helpers, armadilhas e formato de saída. O autor usa o arquivo ao escrever ou revisar a skill; testes de roteamento examinam se a descrição a torna selecionável sem disputar indevidamente outra skill. Para tarefas com controle mais forte, o molde aponta à policy de Skill Enforcement Framework e distingue `current_level`, sustentado por artefatos, de `target_level`, direção de migração. Escrever uma intenção em `SKILL.md` não implementa runner, Receipt ou postflight.

O template não é uma skill publicada. Sua descrição de roteamento não promete seleção determinística em toda conversa, e a lista de helpers não executa código sozinha. Na manutenção, refaça testes quando mudar nome, descrição ou escopo material; confira também que o nível declarado corresponde às evidências existentes.

<!-- editorial:exclude:start -->
Fonte: [skill/template.md](../../hub_padroes/skill/template.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0024](#doc-0024) · [Próximo: D0026](#doc-0026) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0026"></a>
<a id="doc-0026"></a>
### D0026 — O que a política de enforcement permite afirmar?

O README de `skill_enforcement` apresenta a policy, registro que distingue o nível **vigente** (`current_level`) da meta (`target_level`) de cada skill. SEF significa *Skill Enforcement Framework*, a estrutura de verificações por nível. L0 é orientação; L1, contrato; L2, preflight antes do trabalho protegido; L3, runner com primitive e Receipt, o comprovante da execução; L4, Postflight que pode autorizar conclusão. Uma menção a helper no texto não sobe a skill de nível.

O exemplo do README usa `get_skill_enforcement_policy("hub-ml-feature-engineering")`: a API (interface de programação) retorna nível corrente, alvo e modo de rollout para leitura, sem chamar helper ou alterar a policy. Na instância atual, essa skill está L0 com alvo L4 e modo `audit`; a EDA (análise exploratória de dados) profissional está L4/`enforce`. Esses valores exigem conferir o `policy.json` da mesma revisão antes de repetir o exemplo. `guidance`, `audit`, `warn` e `enforce` têm efeitos diferentes; `target_level` não autoriza bloqueio ou publicação por si.

Na manutenção, leia o [consumidor da policy](../../hub_scripts/skill_execution/skill_execution.py) e o validador SE07 junto ao registro. Um gate local verde, uma dívida histórica aceita ou um PASS guardado no notebook não comprovam reverificação da run nem promoção ao workspace corporativo. O README é orientação operacional; a evidência de execução pertence ao runner, Receipt e Postflight correspondentes.

<!-- editorial:exclude:start -->
Fonte: [README de skill_enforcement](../../hub_padroes/skill_enforcement/README.md). SHA-256: `8fc79351a7be74bae0702870fb84a69c92fb5a90b712a7158ec73e7ed536be3d`. Ponte: [MT16](MT-parte-iv.md#mt16), [MU04](MU-parte-ii.md#mu04).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0025](#doc-0025) · [Próximo: D0027](#doc-0027) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0027"></a>
<a id="doc-0027"></a>
### D0027 — Guia do snippet exemplar de taxa de resposta

Este README explica por que uma taxa de campanha precisa ser lida junto do tamanho do grupo e de sua incerteza. O exemplar `taxa_resposta_campanha` recebe DataFrame PySpark com uma linha por contato, segmento e resposta 0/1; devolve tabela agregada com taxa, intervalo de Wilson e marca local de base mínima. A pergunta didática é se duas taxas parecidas têm precisão igualmente sustentada. O texto não transforma a maior porcentagem em decisão automática de orçamento.

O arquivo segue o contrato README de objeto 1.0.0: apresenta escolha, pré-requisitos, funcionamento, saída, interpretação, alternativas e riscos. Quem constrói snippets pode comparar essa forma com o módulo, a fachada e o notebook; quem trabalha numa campanha real deve procurar um recurso operacional adequado e validar unidade de análise, independência e período. A marca `decidivel` compara apenas a quantidade de contatos com o mínimo configurado; não mede viés, significância entre segmentos nem causalidade. O limiar do exemplar não é política global do Hub.

Há uma diferença de efeitos que o leitor precisa ver antes da demonstração: **o helper não grava tabelas, mas o notebook sobrescreve uma tabela sintética persistente**. A pasta é material de padrões, não helper homologado para produção. Na manutenção, preserve esse aviso e confronte as colunas descritas com o código, sem apresentar um exemplo aritmético como execução PySpark desta edição.

<!-- editorial:exclude:start -->
Fonte: [README de taxa_resposta_campanha](../../hub_padroes/snippet/taxa_resposta_campanha/README.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0026](#doc-0026) · [Próximo: D0028](#doc-0028) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0028"></a>
<a id="doc-0028"></a>
### D0028 — Molde de pasta e API de snippet

O template de snippet existe para evitar que funções reutilizáveis ganhem formatos de pasta e import diferentes a cada autor. Ele pede uma pasta por objeto com README humano, implementação Python, fachada `__init__.py` e notebook de exemplo. O nome em `snake_case` integra o caminho de importação; o módulo define a lógica; o README explica escolha e limites; o notebook demonstra a chamada e sua interpretação. A fachada reexporta os nomes públicos previstos pela implementação, inclusive constantes; geração e conferência pertencem à manutenção autorizada.

O autor consulta o molde ao criar ou converter um snippet. Suas exigências incluem docstrings com entradas, retorno, erros e armadilhas; validação explícita; decisão de domínio nomeada; dependências e sessão Spark onde necessárias. O `__init__.py` da categoria não reexporta todos os filhos, evitando que dependências opcionais de um objeto impeçam importar irmãos. O exemplar de campanha mostra a forma, mas fica fora da biblioteca operacional.

Na manutenção de código já usado, o template exige preservar assinatura, colunas e comportamento de borda; mudanças de algoritmo, API ou aparência exigem decisão e testes próprios. Isso impede uma mudança semântica escondida numa reorganização de arquivos. O molde não garante que o comportamento herdado seja ideal nem que um notebook rode no destino; manutenção exige comparar consumidores, código e exemplos reais.

<!-- editorial:exclude:start -->
Fonte: [snippet/template.md](../../hub_padroes/snippet/template.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0027](#doc-0027) · [Próximo: D0029](#doc-0029) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0029"></a>
<a id="doc-0029"></a>
### D0029 — Entrada da coleção de briefings

O README de `hub_prompts` existe para quem tem uma tarefa, mas ainda não sabe qual formulário usar. É o índice da coleção e explica que um prompt estruturado é um **briefing manual**: nele a pessoa declara objetivo, fonte, parâmetros, modo de trabalho e saída esperada antes de conversar com Genie Code. Sua matriz agrupa os 18 briefings por exploração, modelagem, qualidade, documentação e Micromodelos. O leitor usa essa orientação para escolher uma pasta; o mantenedor a atualiza quando entra um novo briefing ou muda a rota indicada.

A anatomia mostrada no README separa o arquivo `.md` preenchível do `exemplo_*.py`, que prepara um cenário e reserva espaço para registrar a resposta real. `NÃO INFORMADO` indica lacuna a investigar; `NÃO APLICÁVEL` indica campo avaliado como irrelevante. Por exemplo, uma dúvida sobre nulidade inicial leva a `eda_rapida`, enquanto uma reconciliação entre versões leva a `comparar_tabelas`. O README situa skill como método e helper como código; a rota vigente e a policy governam a execução.

Esse índice não seleciona skill, não envia prompt ao chat e não executa notebook. A recomendação de um arquivo é ponto de partida: verificar README local, efeito da Parte 1 e contrato do `.md` antes de agir.

<!-- editorial:exclude:start -->
Fonte: [índice de prompts](../../hub_prompts/README.md). Uso: [MU05](MU-parte-ii.md#mu05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0028](#doc-0028) · [Próximo: D0030](#doc-0030) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0030"></a>
<a id="doc-0030"></a>
### D0030 — Guia da auditoria de skills

O README de `auditoria_skills` ajuda a decidir **o que** será auditado antes de preencher o pedido. Ele distingue a implementação de uma skill — arquivos, contrato, recursos e segurança — do output produzido por ela, como notebook ou relatório. Essa escolha muda a evidência necessária. Separadamente, a ação pode ser auditoria, plano de correção ou correção autorizada; escolher OUTPUT não autoriza editar. O arquivo pertence à pasta do prompt, é lido pela pessoa que prepara a auditoria e pelo mantenedor que revisa o formulário associado.

Seu fluxo pede alvo, versão, pedido original, resposta e evidências aplicáveis. Orienta construir uma matriz requisito→evidência, classificar gravidade e separar observado de não executado. Por exemplo, para avaliar um notebook alegadamente feito por uma skill, anexe o output e o `SKILL.md` correspondente; sem o notebook, a conformidade da saída fica não observável. O README explica como conferir se o laudo citou trechos específicos e se recomendações respeitam escopo e autorização.

O notebook demonstrativo da pasta apenas lê um `SKILL.md` local; isso não executa uma auditoria conversacional nem prova aderência do output. O pedido manual pode recomendar `@hub-ml-auditoria-skills`, mas seleção e análise precisam ser verificadas separadamente. PASS salvo não prova reverificação: confira o artefato atual pelo verificador canônico.

<!-- editorial:exclude:start -->
Fonte: [README auditoria_skills](../../hub_prompts/auditoria_skills/README.md). Formulário: [D0031](#doc-0031).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0029](#doc-0029) · [Próximo: D0031](#doc-0031) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0031"></a>
<a id="doc-0031"></a>
### D0031 — Formulário de auditoria de skill ou output

O arquivo `auditoria_skills.md` é a interface preenchível para solicitar uma revisão, não o laudo em si. Ele força a escolha entre modo **IMPLEMENTAÇÃO** e modo **OUTPUT**. No primeiro, a pessoa identifica pasta da skill, `SKILL.md`, contratos e recursos que a compõem; no segundo, liga uma entrega ao pedido, à skill alegada e à evidência de execução. O consumidor é quem cola o briefing no chat; o mantenedor preserva seus campos quando muda o contrato de auditoria.

O formulário explica cada placeholder, fornece pedido pronto, exemplo mínimo, checklist da resposta e follow-ups. Num caso de output, pode-se escrever: “revise este notebook contra a skill informada, destaque requisito, evidência e lacuna; execução remota `NÃO INFORMADO`”. Isso pede uma matriz verificável e impede que uma lacuna seja preenchida por suposição. Se o alvo ou a versão não puderem ser lidos, a resposta deve delimitar o que ficou fora da análise. Correção do artefato é uma ação distinta e requer escopo próprio.

Preencher o texto não aciona um gate de enforcement nem garante acesso aos arquivos. Execução segue a skill selecionada, sua policy e o perfil suportado; helpers diretos não substituem essa rota. O exemplo é ilustrativo até haver resposta real registrada; uma auditoria de formato não substitui teste de comportamento ou verificação independente da execução.

<!-- editorial:exclude:start -->
Fonte: [auditoria_skills.md](../../hub_prompts/auditoria_skills/auditoria_skills.md). Contexto: [D0030](#doc-0030).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0030](#doc-0030) · [Próximo: D0032](#doc-0032) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0032"></a>
<a id="doc-0032"></a>
### D0032 — Guia para uma linha de base de modelo

O README de `baseline_orchestration` situa o briefing antes de qualquer treino: uma linha de base é uma referência simples, reproduzível, para comparar alternativas posteriores. O guia existe porque “treine o melhor modelo” omite população, target, momento de observação e critério de sucesso. É usado por quem planeja modelagem e pelo mantenedor que precisa manter o formulário coerente com a skill de baseline e o exemplo da pasta.

O README orienta a escolha da unidade prevista, evento positivo, cutoff, horizonte, split, métrica e custo. Alerta contra leakage entre splits, pré-processamento fora do treino e reutilização do holdout. O formulário `baseline_orchestration.md` manda avaliar o holdout uma única vez na decisão final. Por exemplo, prever cancelamento em 30 dias por cliente-mês requer saber quando o rótulo amadurece; sem isso, a recomendação segura é um plano condicional. O formulário pede comparação com baseline ingênuo, resultados por split, tempo e segmento e registro de reprodutibilidade; indica MLflow para parâmetros, métricas e artefatos quando disponível. O perfil `BINARY_TEMPORAL_LOCAL_V1` é sintético; tracking exige autorização própria, sem homologar todo briefing.

O notebook didático prepara uma tabela sintética com `mode("overwrite")`; sua execução pode substituir o destino indicado, independentemente de o briefing estar em modo plano. Conferir nome da tabela e efeito antes de rodar. Nenhuma comparação de modelos ou validação no Databricks é demonstrada pela leitura deste README.

<!-- editorial:exclude:start -->
Fonte: [README baseline_orchestration](../../hub_prompts/baseline_orchestration/README.md). Formulário: [D0033](#doc-0033).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0031](#doc-0031) · [Próximo: D0033](#doc-0033) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0033"></a>
<a id="doc-0033"></a>
### D0033 — Pedido preenchível de baseline

`baseline_orchestration.md` traduz a ideia de “primeiro modelo” em um contrato que o assistente possa discutir e o leitor possa revisar. Seus campos pedem dataset, grão, chave, target, evento positivo, momento de observação, maturação do rótulo, cutoff, horizonte, estratégia de split, métricas, restrições e modo de trabalho. O arquivo é Markdown copiável: a pessoa o preenche, anexa a fonte e o envia ao chat; ele não é um script de treino.

O guia de campos explica por que cada decisão altera o experimento. Um pedido honesto poderia declarar “grão cliente-mês, cancelamento nos 30 dias seguintes, disponibilidade do rótulo `NÃO INFORMADO`; apresente plano e riscos antes de treinar”. A resposta deve identificar a lacuna temporal, propor baseline ingênuo e justificar split/métrica quando a informação estiver disponível. O checklist final permite conferir população, vazamento, comparabilidade e o que foi realmente executado ou registrado.

Um texto que solicita MLflow ou scorecard não prova que run, artefato ou métrica foram produzidos. Sem autorização e dados suficientes, o resultado legítimo é plano ou pergunta de esclarecimento. Execução segue a skill selecionada, sua policy e o perfil suportado; helpers diretos não substituem essa rota. O exemplo mínimo ilustra preenchimento, não certifica desempenho de modelo.

<!-- editorial:exclude:start -->
Fonte: [baseline_orchestration.md](../../hub_prompts/baseline_orchestration/baseline_orchestration.md). Contexto: [D0032](#doc-0032).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0032](#doc-0032) · [Próximo: D0034](#doc-0034) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0034"></a>
<a id="doc-0034"></a>
### D0034 — Guia para documentar um notebook

O README de `comentar_notebook` existe para melhorar a leitura de um notebook sem confundir documentação com alteração da lógica. Ele ajuda a escolher entre revisão, edição e documentação, a definir público e profundidade e a declarar células ou resultados que precisam ser preservados. É a explicação de uso da pasta; o `.md` ao lado é o pedido que será preenchido. Quem mantém o recurso deve conservar essa separação para que uma instrução de comentário não vire autorização implícita de refatoração.

O fluxo recomendado começa lendo o notebook real, localizando etapas e efeitos, e só então propondo células Markdown antes e depois do código. Por exemplo, para um notebook de junção temporal, a descrição prévia explica a chave e o cutoff; a posterior interpreta contagens e riscos, sem afirmar que os números foram reexecutados. O guia lembra de tratar dados sensíveis em outputs e de conferir diffs quando uma edição for autorizada.

O exemplo local lê um arquivo de código para demonstrar o pedido; não prova que uma célula Databricks foi executada, que a lógica continua equivalente ou que a skill foi selecionada. A revisão final pertence ao dono do notebook e ao contexto de uso.

<!-- editorial:exclude:start -->
Fonte: [README comentar_notebook](../../hub_prompts/comentar_notebook/README.md). Formulário: [D0035](#doc-0035).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0033](#doc-0033) · [Próximo: D0035](#doc-0035) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0035"></a>
<a id="doc-0035"></a>
### D0035 — Pedido para comentar células escolhidas

O formulário `comentar_notebook.md` pede que a pessoa escolha o notebook ou as células e declare o modo **REVISÃO**, **EDIÇÃO** ou **DOCUMENTAÇÃO**. Também solicita público, profundidade, objetivo, restrições e partes imutáveis. Sua função é fazer o assistente responder à tarefa editorial concreta; o documento é copiado manualmente para o chat e pode receber contexto de célula quando essa superfície estiver disponível.

Os campos evitam que “deixe didático” seja interpretado como licença para alterar cálculos. Num pedido de revisão, escreva “explique este bloco para analistas iniciantes e sugira textos antes/depois, mantendo as células de código intactas”. Em edição documental autorizada, peça diff e conferência de código, ordem, entradas, saídas e efeitos preservados. Mudança funcional exige pedido separado. O checklist do formulário ajuda a verificar se a resposta ensinou o motivo de cada etapa, interpretou a saída e indicou limites sem copiar comentários genéricos.

O briefing não insere células sozinho. Mencionar `@cell` ou uma skill recomendada não prova que o objeto foi carregado; confirme qual notebook foi lido. Mesmo uma boa explicação de código não demonstra que ele foi reexecutado nem que o resultado continuou válido.

<!-- editorial:exclude:start -->
Fonte: [comentar_notebook.md](../../hub_prompts/comentar_notebook/comentar_notebook.md). Contexto: [D0034](#doc-0034).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0034](#doc-0034) · [Próximo: D0036](#doc-0036) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0036"></a>
<a id="doc-0036"></a>
### D0036 — Guia para reconciliar duas tabelas

O README de `comparar_tabelas` ajuda a escolher uma comparação controlada quando duas versões, fontes ou implementações parecem divergir. Ele existe porque uma contagem isolada ou a igualdade de schema pode esconder mudança de população, filtro, grão ou valor. É a orientação humana da pasta: explica adequação, pré-requisitos, contrato de resposta e riscos; o `.md` associado recebe os parâmetros do caso. Mantenedores devem conservar exemplos sem identificadores reais e revisar efeitos do notebook demonstrativo.

O procedimento pede A e B, unidade de cada linha, chaves, período, fuso, filtros, tipo de comparação e tolerâncias. A resposta solicitada inclui matriz de schema, scorecard, reconciliação de chaves/valores e veredito condicionado às regras. Por exemplo, duas tabelas com a mesma coluna `id_cliente` podem conter uma linha por cliente em A e várias por cliente-mês em B; um join direto multiplicaria registros. Antes do veredito, confira cardinalidade, denominadores e amostras de divergências explicadas.

“Somente leitura” no pedido descreve a intenção, não impõe bloqueio técnico automático. O notebook sobrescreve duas tabelas sintéticas durante o preparo. Confira os destinos e a rota selecionada: SQL direto não substitui EDA protegida. O README não prova que a reconciliação foi realizada nem que as populações são equivalentes.

<!-- editorial:exclude:start -->
Fonte: [README comparar_tabelas](../../hub_prompts/comparar_tabelas/README.md). Formulário: [D0037](#doc-0037).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0035](#doc-0035) · [Próximo: D0037](#doc-0037) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0037"></a>
<a id="doc-0037"></a>
### D0037 — Formulário de comparação A/B

`comparar_tabelas.md` transforma “essas tabelas batem?” em um pedido com critérios explícitos. O usuário preenche os identificadores A/B, objetivo, grão, chaves, período, filtros, fuso, tolerâncias e foco da divergência, depois cola o texto no chat. O arquivo orienta uma resposta em etapas; não executa consulta ou comparação por si. Seu produtor é o mantenedor do Hub, e o consumidor é quem precisa explicar a diferença a um responsável de dados.

O bloco de preenchimento mostra por que chaves e tolerâncias precisam de origem. Exemplo: “A contém clientes de setembro; B é a nova saída mensal; `id_cliente` é chave candidata; tolerância `NÃO INFORMADO`; primeiro compare schema, cardinalidade e contagens”. Uma resposta pode listar diferenças observadas, mas não declarar equivalência aceitável sem regra de tolerância aprovada. Se a pergunta for sobre relacionamento entre fontes para modelagem, a rota cross-EDA pode ser mais adequada; se for reconciliação de valores de duas versões, mantenha o foco A/B.

O checklist pede matriz, scorecard, casos divergentes e limites. Após selecionar uma skill, siga sua policy e rota protegida; comparação manual não autoriza contorná-la. Mesmo schema idêntico não garante o mesmo universo nem significado de cada coluna. O pedido pode solicitar leitura, porém permissões e operações realmente executadas devem ser conferidas à parte.

<!-- editorial:exclude:start -->
Fonte: [comparar_tabelas.md](../../hub_prompts/comparar_tabelas/comparar_tabelas.md). Contexto: [D0036](#doc-0036).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0036](#doc-0036) · [Próximo: D0038](#doc-0038) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0038"></a>
<a id="doc-0038"></a>
### D0038 — Guia de exploração cruzada para modelagem

O README de `cross_eda` orienta a passagem de perfis separados para uma pergunta conjunta: as fontes podem ser ligadas de forma útil e temporalmente válida para um modelo? Sua razão de existir é evitar que alta cobertura de join seja confundida com prontidão para machine learning. Ele explica quando usar a rota, que dados de contexto reunir e como interpretar perdas, multiplicação de linhas, complementaridade e risco de vazamento. O briefing `.md` ao lado recolhe o caso específico.

O guia exige fonte âncora, entidade e grão de cada tabela, chaves, target, cutoff, horizonte, períodos e disponibilidade histórica. Por exemplo, uma tabela de cadastro e uma de transações podem se juntar por cliente; ainda é preciso saber se a transação chegou antes da decisão. A resposta esperada deve medir cardinalidade e cobertura, declarar população sem correspondência e separar fato observado de hipótese sobre sinal preditivo. Timestamp do evento, sozinho, não prova disponibilidade no ponto no tempo.

O notebook de demonstração prepara duas tabelas com `mode("overwrite")`; confira os destinos antes de executá-lo. O README encaminha a `@hub-ml-cross-eda-ml`; perfis sintéticos de contexto e PIT têm escopos próprios, sem promover policy ou realizar todo Cross-EDA. Sem evidência temporal, a conclusão correta é viabilidade pendente, não ausência certificada de leakage.

<!-- editorial:exclude:start -->
Fonte: [README cross_eda](../../hub_prompts/cross_eda/README.md). Formulário: [D0039](#doc-0039).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0037](#doc-0037) · [Próximo: D0039](#doc-0039) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0039"></a>
<a id="doc-0039"></a>
### D0039 — Pedido preenchível de cross-EDA

`cross_eda.md` é o formulário manual para examinar várias fontes antes de feature engineering ou baseline. Ele pede recursos e contexto já conhecido, entidade, grão, target, ponto de decisão, horizonte, chaves e janelas de cada fonte. O leitor substitui placeholders e envia o pedido ao Genie Code; o arquivo não é um programa que verifica joins. Seu valor está em tornar visíveis premissas que uma resposta confiante poderia ocultar.

Um pedido válido pode dizer: “cadastro mensal e transações diárias; uma linha por cliente-mês na âncora; disponibilidade da transação `NÃO INFORMADO`; avalie cardinalidade, cobertura e teste temporal necessário”. A resposta deve separar o que uma consulta realmente mediu do que falta medir, mostrar perdas e multiplicação por chave e declarar risco de leakage quando a data de disponibilidade não foi comprovada. O formulário propõe skill especializada, mas a seleção precisa ser observada na sessão. Execução segue a skill selecionada, sua policy e o perfil suportado; helpers diretos não substituem essa rota.

O checklist de saída ajuda a conferir joins, população e limitações antes do handoff para features. Mesmo 100% de chaves encontradas não confirma que as linhas representam o mesmo instante ou que a variável era utilizável na decisão. Sem fontes acessíveis, receba um plano, não um diagnóstico executado.

<!-- editorial:exclude:start -->
Fonte: [cross_eda.md](../../hub_prompts/cross_eda/cross_eda.md). Contexto: [D0038](#doc-0038).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0038](#doc-0038) · [Próximo: D0040](#doc-0040) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0040"></a>
<a id="doc-0040"></a>
### D0040 — Guia para diagnóstico de qualidade

O README de `data_quality` ajuda a transformar “a base parece suja” em dimensões testáveis: completude, unicidade, validade, consistência, integridade, atualidade e volume. Ele situa o briefing como pedido de **diagnóstico**, não de correção silenciosa. O leitor usa o guia para decidir quais regras e períodos importam; o mantenedor confere se formulário, exemplo e recomendações de skill continuam coerentes com o contrato do Hub.

Cada regra precisa de origem, população, numerador, denominador e limiar. Por exemplo, “nulos em `id_cliente`” só vira achado útil após dizer quantas linhas foram examinadas, se a chave é obrigatória no grão declarado e qual período foi coberto. O README pede scorecard, severidade, evidências e plano de investigação, distinguindo falha de dado de hipótese sobre causa. Também lembra de tempos de evento, ingestão e atualização quando atualidade é parte do uso downstream.

O notebook demonstrativo cria clientes sintéticos com duplicatas e usa `mode("overwrite")` para preparar a tabela; essa escrita pertence ao exemplo, não ao pedido de diagnóstico. Quando a EDA protegida for selecionada, exige runner, Receipt e postflight autorizado; o briefing não a executa nem faz deploy de expectations. Uma porcentagem sem regra e denominador não é prova de qualidade aceitável.

<!-- editorial:exclude:start -->
Fonte: [README data_quality](../../hub_prompts/data_quality/README.md). Formulário: [D0041](#doc-0041).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0039](#doc-0039) · [Próximo: D0041](#doc-0041) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0041"></a>
<a id="doc-0041"></a>
### D0041 — Formulário de regras de qualidade

`data_quality.md` coleta o contrato de uma checagem de qualidade antes que o assistente proponha SQL ou Python. Seus campos cobrem fonte, grão, chaves, período, tempos de evento/ingestão/atualização, uso downstream, regras conhecidas, limites e modo. O documento é um briefing manual da pasta `hub_prompts`, preenchido pela pessoa responsável pela análise; o mantenedor preserva nomes de campos e orientações quando a metodologia evolui.

Um exemplo honesto seria: “verifique duplicidade de `id_cliente` no cadastro mensal; grão esperado cliente-mês; chave composta ainda `NÃO INFORMADO`; apresente plano para descobrir a chave e conte linhas afetadas antes de sugerir correção”. A resposta solicitada deve exibir scorecard por regra, numerador, denominador, período e origem do limiar. Se um limite ainda não foi aprovado, indique a medição sem chamar automaticamente o resultado de PASS ou FAIL de negócio. O formulário também pede priorização e próximos testes.

Preencher o pedido não dá acesso à tabela nem instala monitor de qualidade. A sugestão de `@hub-ml-eda-profissional` não prova seleção. A execução protegida exige `run_enforced`, `finalize_or_raise`, Postflight `PASS` e `completion.authorized=true`; helper ou SQL direto não contorna esses gates. Valores de exemplo não são medições reais.

<!-- editorial:exclude:start -->
Fonte: [data_quality.md](../../hub_prompts/data_quality/data_quality.md). Contexto: [D0040](#doc-0040).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0040](#doc-0040) · [Próximo: D0042](#doc-0042) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0042"></a>
<a id="doc-0042"></a>
### D0042 — Guia da exploração aprofundada

O README de `eda_completa` explica quando um perfil inicial precisa virar investigação ampla de uma fonte. Em vez de listar comandos, ele liga pergunta de negócio a grão, chave, período, qualidade, distribuições, relações com target quando houver, segmentos e gráficos. É a explicação de adequação e manutenção da pasta; o formulário `.md` recolhe o caso e o notebook `exemplo_*.py` demonstra um cenário. O leitor decide se a profundidade compensa o custo antes de pedir execução.

O guia orienta especificar recurso, população, volume, foco e restrições. Por exemplo, após um perfil rápido apontar nulos em variável importante, a EDA completa pode comparar períodos e segmentos e investigar associações, apresentando achados, hipóteses e backlog de verificações. O plano deve limitar coleta ao driver e escolher visualizações agregadas. A skill recomendada é `@hub-ml-eda-profissional`; quando ela for selecionada para execução completa, sua rota atual exige evidência canônica e postflight antes da linguagem de conclusão.

O notebook sintético da pasta usa `mode("overwrite")` no preparo, ação separada do briefing. Gráfico convincente não prova causalidade, e amostra sem problema não certifica ausência de leakage ou qualidade de toda a população. O README não relata análise realizada no ambiente do leitor.

<!-- editorial:exclude:start -->
Fonte: [README eda_completa](../../hub_prompts/eda_completa/README.md). Uso: [MU05](MU-parte-ii.md#mu05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0041](#doc-0041) · [Próximo: D0043](#doc-0043) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0043"></a>
<a id="doc-0043"></a>
### D0043 — Formulário para EDA completa

O formulário de EDA, análise exploratória de dados, completa serve a quem precisa transformar uma fonte conhecida em investigação reproduzível para uma decisão. Ele pede tabela ou DataFrame anexado, contexto de negócio, unidade de análise, chave candidata, coluna temporal, target quando aplicável, período, volume, foco e restrições. A escolha de um entregável — notebook, relatório ou código — evita que o assistente confunda diagnóstico solicitado com execução já feita.

O fluxo orienta verificar schema, permissões e ambiguidades antes de varrer a fonte. Pede estrutura, qualidade, distribuições, relações, riscos de modelagem e gráficos com base e período declarados. Num conjunto de pedidos, por exemplo, a chave `id_pedido` deve ser testada no recorte definido antes de afirmar unicidade; um join que multiplica linhas muda denominadores. O contrato espera achados ligados a evidências, limitações e backlog, não uma aprovação automática da base.

O próprio texto proíbe coleta irrestrita ao driver e escrita sem impacto mostrado e autorização. Correlação não prova causa; campo desconhecido permanece `NÃO INFORMADO`. O arquivo é um pedido manual: sua leitura não acessa dados, não produz gráfico nem valida o workspace. A EDA protegida exige `run_enforced`, finalização por `finalize_or_raise`, Postflight `PASS` e `completion.authorized=true`, sem bypass manual.

<!-- editorial:exclude:start -->
Fonte: [eda_completa/eda_completa.md](../../hub_prompts/eda_completa/eda_completa.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0042](#doc-0042) · [Próximo: D0044](#doc-0044) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0044"></a>
<a id="doc-0044"></a>
### D0044 — Guia de perfil rápido de dados

O README de `eda_rapida` apresenta um primeiro perfil para decidir quais verificações aprofundar. EDA significa análise exploratória de dados. O recurso é útil ao receber fonte nova ou perceber mudança de população, estrutura ou período; é insuficiente para aprovar modelo, crédito ou correção automática. Quem escolhe o briefing deve informar objetivo e foco para que completude, duplicidade e recência sejam examinadas no universo certo.

O guia remete ao formulário de sete campos e ensina a distinguir chave candidata de unicidade demonstrada. Uma resposta útil lista até oito achados priorizados, com evidência, severidade, impacto e próximo passo. Por exemplo, “a chave é única” exige teste sobre filtros e período indicados; sem teste, é apenas hipótese. Amostra não representa automaticamente a população, e limite de custo escrito no pedido não é quota técnica do ambiente.

O notebook associado tem preparo sintético que chama `write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes")`; executar a Parte 1 pode substituir essa tabela. O briefing não executa nada sozinho. A EDA protegida selecionada exige `run_enforced`, Receipt e `finalize_or_raise`, com Postflight PASS e `completion.authorized=true`. Confira fonte, permissão e destino antes de qualquer célula, e trate a resposta de exemplo como `NÃO EXECUTADO` até haver evidência real.

<!-- editorial:exclude:start -->
Fonte: [eda_rapida/README.md](../../hub_prompts/eda_rapida/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0043](#doc-0043) · [Próximo: D0045](#doc-0045) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0045"></a>
<a id="doc-0045"></a>
### D0045 — Formulário de EDA rápida

Este formulário organiza o pedido manual de um perfil inicial: recurso, objetivo, foco, chave candidata, coluna temporal, filtros/período e limite de execução. A pessoa usuária anexa a tabela ou notebook com contexto real e mantém `NÃO INFORMADO` onde não sabe. A skill recomendada é `@hub-ml-eda-profissional`, mas mencioná-la não prova que ela foi carregada nem autoriza consulta.

O fluxo pede confirmação do contexto e plano antes de calcular volume, schema, nulos, duplicidade, cardinalidade e distribuições simples. A resposta deve priorizar até oito achados, informando dimensão, evidência, severidade, impacto, ação e limitações. Imagine que uma coluna `id_cliente` pareça chave: o assistente deve testar repetição no período filtrado antes de concluir, e mostrar denominador da taxa de duplicatas. Fatos observados ficam separados de hipóteses e sugestões.

O modo restringe código a pedido ou autorização; plano e texto não são execução. Rapidez não dispensa `run_enforced`, `finalize_or_raise`, Postflight `PASS` e `completion.authorized=true` na EDA protegida. Não se deve coletar a tabela inteira ao driver, revelar PII (informações pessoais identificáveis) ou alterar dados. Um resultado convincente ainda requer conferir recurso, período e comandos realmente executados. O [guia de escolha](#doc-0044) explica quando esse primeiro olhar precisa virar análise mais profunda.

<!-- editorial:exclude:start -->
Fonte: [eda_rapida/eda_rapida.md](../../hub_prompts/eda_rapida/eda_rapida.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0044](#doc-0044) · [Próximo: D0046](#doc-0046) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0046"></a>
<a id="doc-0046"></a>
### D0046 — Guia de explicabilidade de modelo

O README de `explainability` orienta escolher explicação global ou local para um modelo identificado, no split e público corretos. Antes do pedido, separe performance de explicação: uma importância de variável descreve contribuição segundo um método, não demonstra efeito causal. O guia exige modelo ou run, dataset e split, target, objetivo, audiência, método e amostra para evitar explicar uma versão diferente daquela usada na decisão.

Imagine um modelo de propensão versão 7 avaliado num holdout temporal. O pedido precisa fixar essa versão, população, classe positiva e espaço da saída antes de interpretar sinais ou gráficos. SHAP, método de atribuição de contribuições do modelo, requer conferir explainer, background e estabilidade; coeficientes ou PDP (gráfico de dependência parcial da saída prevista em relação a uma variável) podem ser mais adequados conforme o caso. O README aponta risco de expor registros individuais ou PII (informações pessoais identificáveis) e remete ao formulário para o contrato detalhado.

O notebook de exemplo sobrescreve `workspace.default.hub_exemplo_clientes` no preparo e usa SHAP como dependência opcional. O perfil `LINEAR_REGRESSION_SYNTHETIC_V1` cobre SHAP linear escalar sintético; não comprova o LightGBM pretendido no exemplo. Abrir este guia não calcula explicações. A existência do notebook não prova run executado nem autoriza publicar artefatos ou alterar modelo.

<!-- editorial:exclude:start -->
Fonte: [explainability/README.md](../../hub_prompts/explainability/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0045](#doc-0045) · [Próximo: D0047](#doc-0047) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0047"></a>
<a id="doc-0047"></a>
### D0047 — Formulário de explicabilidade

O formulário de explicabilidade transforma “explique o modelo” num pedido verificável. Informe URI (identificador ou endereço do artefato de modelo) ou run exato, dados e split, target e classe positiva, pergunta, público, método, amostra, período e restrições. Se modelo ou população não puderem ser identificados, a saída adequada é apenas um plano. O modo distingue plano, código e execução autorizada, sem pressupor que uma explicação já foi calculada.

O fluxo começa por versão, transformações e ordem das features. Para SHAP, atribuição relativa ao resultado de referência do modelo, pede explainer, background e espaço da saída: log-odds, score ou probabilidade quando suportado. Num holdout temporal, um gráfico global mostra padrão do modelo naquela população; um caso local mostra contribuições para uma previsão. Nem um nem outro isola causalidade. Correlação entre features e mudança de background podem alterar a leitura; por isso o formulário exige verificações de estabilidade e sinal.

O contrato separa achados globais e locais, evidência, incerteza e limitações. Não exponha atributos sensíveis nem conclua fairness ou conformidade de uma importância isolada. Código reprodutível só é solicitado quando útil; o arquivo não executa o método nem publica artefatos. Execução segue skill, policy e rota suportada; helper direto não substitui o caminho protegido.

<!-- editorial:exclude:start -->
Fonte: [explainability/explainability.md](../../hub_prompts/explainability/explainability.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0046](#doc-0046) · [Próximo: D0048](#doc-0048) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0048"></a>
<a id="doc-0048"></a>
### D0048 — Guia de engenharia de atributos

O README de `feature_engineering` apresenta um briefing para especificar atributos quando entidade, target e instante de predição já estão definidos. Seu papel é orientar quem desenha features antes de treinar ou publicar tabela, deixando visíveis fonte, janela, cutoff, fórmula, nulos e testes. Se a pergunta ainda é exploratória ou falta o instante da decisão, o guia recomenda voltar ao diagnóstico.

Uma média de transações nos últimos 90 dias parece simples. Se a fonte só publica eventos com um dia de atraso, a data do evento não prova disponibilidade no cutoff: a especificação precisa usar o dado que existia no momento da previsão. O README destaca joins que multiplicam linhas, proxies sensíveis e paridade entre treino e inferência. Ganho de modelo é hipótese até medição adequada, não consequência do texto.

O notebook associado prepara duas tabelas sintéticas com `mode("overwrite")`, `workspace.default.hub_exemplo_fatos` e `workspace.default.hub_exemplo_features`; a Parte 1 pode substituí-las. Abrir o README ou preencher o briefing não materializa nem publica features. O perfil `FREE_SYNTHETIC_PIT_FEATURE_MATERIALIZATION_V1` exige composição PIT verificada, destino e autorização explícitos. O [formulário](#doc-0049) separa plano, código e implementação autorizada.

<!-- editorial:exclude:start -->
Fonte: [feature_engineering/README.md](../../hub_prompts/feature_engineering/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0047](#doc-0047) · [Próximo: D0049](#doc-0049) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0049"></a>
<a id="doc-0049"></a>
### D0049 — Formulário de engenharia de atributos

O formulário exige três marcos antes de propor features finais: janela observada, instante de predição e horizonte do target. Acrescente entidade e chave, evento positivo, fontes e joins com timestamps e atraso, frequência, features existentes, restrições e modo. Sem cutoff conhecido, peça somente plano. Essa estrutura serve para revisar se uma variável estará disponível na inferência e se a mesma definição vale no treino.

Considere previsão mensal de resgate em 90 dias com transações atualizadas semanalmente. Uma feature de 12 meses não pode usar transações publicadas depois do fechamento do mês, ainda que o evento tenha ocorrido antes. O fluxo pede especificação por atributo com fonte, fórmula, janela, owner e testes; depois verifica cardinalidade dos joins, cobertura, estabilidade, cutoff e paridade treino/inferência. Features sensíveis ou proxies exigem avaliação própria.

No modo PLANO não há escrita; no modo CÓDIGO há proposta sem execução. Execução segue a skill selecionada, sua policy e o perfil suportado; helpers diretos não substituem essa rota. Publicação em Feature Engineering in Unity Catalog depende de configuração real e autorização separada. O arquivo não garante ausência de leakage por si só: essa conclusão requer dados, timestamps e testes observados. O [guia](#doc-0048) ajuda a decidir quando iniciar.

<!-- editorial:exclude:start -->
Fonte: [feature_engineering/feature_engineering.md](../../hub_prompts/feature_engineering/feature_engineering.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0048](#doc-0048) · [Próximo: D0050](#doc-0050) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0050"></a>
<a id="doc-0050"></a>
### D0050 — Guia de monitoramento de modelo

O README de `monitoramento_modelo` orienta escolher um briefing quando já se conhecem modelo, caminho de inferência, referência e janelas. O guia separa saúde do serviço, qualidade de dados, drift, performance preditiva e efeito de negócio. Misturar essas dimensões produz alertas sem ação: latência alta não é queda de acurácia, e mudança de distribuição não demonstra a causa de um resultado.

Para monitorar um modelo mensal, indique baseline, período atual, atraso de maturação do rótulo, unidade e direção das métricas, segmentos e donos. Se o evento só amadurece após 90 dias, a janela de julho ainda não permite avaliar performance em agosto. Um limite copiado de outro caso também não vira política válida. O guia chama atenção para melhora erroneamente tratada como alerta quando se usa `abs(delta)` e para amostras pequenas ou nulos ocultos na média.

O notebook de exemplo sobrescreve `hub_exemplo_monitor_ref` e `hub_exemplo_monitor_atual` durante o preparo. Os perfis `DRIFT_NUMERIC_LOCAL_V1` e `BINARY_MATURE_PERFORMANCE_V1` têm escopos distintos; performance exige rótulos maduros, finalização e verificação próprias. Ler o README não cria monitor, mede drift nem agenda retreino. A decisão de retreinar requer investigação e responsável, não reação automática a um ponto.

<!-- editorial:exclude:start -->
Fonte: [monitoramento_modelo/README.md](../../hub_prompts/monitoramento_modelo/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0049](#doc-0049) · [Próximo: D0051](MT-atlas-02.md#doc-0051) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
