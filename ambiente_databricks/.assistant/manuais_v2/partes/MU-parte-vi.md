<a id="parte-mu-vi"></a>
# MU parte vi

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MU-indice.md#sumario-mu) · [Livro completo](../../MANUAL_DO_USUARIO.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu18"></a>
<a id="mu18"></a>
### MU18 — Documentar, criar e auditar objetos do Hub

Um objeto do Hub precisa ser compreensível antes de ser copiado para outro notebook ou entregue a outra pessoa. Aqui, **objeto** é um dos seis formatos mantidos em `.assistant`: README, snippet, script, prompt, notebook ou skill. Os templates são moldes de autoria; não calculam, homologam ou publicam por si. Escolha a tarefa primeiro: explicar um notebook, transformá-lo em conteúdo reutilizável, documentar sua [interface de programação de aplicações (API)](MT-parte-vii.md#mt27-1) ou auditar a evidência de uso. O catálogo técnico em [MT05](MT-parte-ii.md#mt-mod-mt05) ajuda a localizar recursos existentes; [MT27](MT-parte-vii.md#mt-mod-mt27) explica o alcance das verificações locais.

<a id="mu18-1"></a>
#### MU18.1 — Comentar notebook ou ensinar seu contexto

Há duas saídas diferentes para um notebook difícil de ler. Quando alguém precisa que a próxima pessoa encontre objetivo, entradas, transformação e interpretação **dentro do próprio arquivo**, use comentário em células `%md`. Quando a tarefa é aprender o funcionamento de um trecho ou diagnosticar uma dúvida, peça uma explicação no chat. Em ambos os casos, apresente o notebook ou trecho com `@`/Add Context, diga o público e se há saídas de execução observadas. Uma frase como “esta consulta encontrou 35 mil linhas” só cabe no texto final se houver resultado correspondente; sem execução, marque a observação pendente.

<a id="uso-hub-ml-comentar-notebook"></a>
<!-- usage-card:start hub-ml-comentar-notebook -->
##### Ficha de uso — comentar notebook

Escolha [`hub-ml-comentar-notebook`](../../skills/hub-ml-comentar-notebook/SKILL.md) quando o entregável deve ser o mesmo notebook, agora legível para revisão e manutenção. Forneça o arquivo, objetivo da análise, público, tabelas ou DataFrames de entrada, parâmetros, saídas existentes e células cujo comportamento deve permanecer intacto. A skill mapeia dependências entre células e insere Markdown prévio em transformações importantes, validações e decisões; o texto posterior interpreta somente resultados observados. Imports triviais e displays isolados não precisam de um comentário por célula. O cabeçalho identifica escopo, entradas, saída, pré-requisitos e limitações sem inventar proprietário ou ambiente.

O entregável é o notebook com `%md` antes ou depois dos blocos materiais e uma lista separada de inconsistências encontradas. Confira o diff das células de código: ordem, linguagem, parâmetros, lógica e resultados existentes devem permanecer como estavam, salvo pedido explícito em contrário. Verifique se cada nome de tabela e métrica no Markdown existe no arquivo ou na evidência fornecida. Se a célula não rodou, escreva `PENDENTE`, não uma contagem imaginada. Para aprofundar a lógica sem mudar o arquivo, use a rota do tutor abaixo.

Pedido copiável:

```text
@hub-ml-comentar-notebook Documente @<notebook> para <público>. Objetivo: <objetivo>. Preserve código, ordem e parâmetros; adicione contexto antes e interpretação após blocos materiais. Use apenas saídas observadas; marque o resto PENDENTE.
```
<!-- usage-card:end hub-ml-comentar-notebook -->

<a id="uso-hub-ml-tutor-databricks"></a>
<!-- usage-card:start hub-ml-tutor-databricks -->
##### Ficha de uso — tutor Databricks

Escolha [`hub-ml-tutor-databricks`](../../skills/hub-ml-tutor-databricks/SKILL.md) quando você precisa entender um bloco, um erro ou um fluxo inteiro antes de modificá-lo. Dê o trecho ou notebook, o objetivo do exercício, sua familiaridade com Spark, entradas, unidade de cada linha e stack trace se houver erro. Informe versão e ambiente quando disponíveis; o tutor deve declarar incerteza quando uma capacidade depende deles. A explicação começa pelo que o bloco produz, agrupa operações por finalidade e distingue transformação lazy de ação que executa Spark, shuffle e coleta no driver.

O entregável fica no chat: uma leitura progressiva de entradas, lógica, saída, custo e uma pequena forma de conferir schema, chaves e contagens. Em erro, procure a exceção raiz e proponha o menor diagnóstico seguro, sem transformar hipótese em causa comprovada. Confira nomes de APIs e colunas contra o trecho original; peça um exemplo sintético se a explicação estiver abstrata. A presença de uma célula não prova que ela executou. Uma analogia de [relacionamento com clientes (CRM)](../../skills/hub-ml-tutor-databricks/SKILL.md) pode ajudar depois da explicação técnica, identificada como analogia. Para gravar a narrativa no notebook, a skill de comentar tem outro entregável.

Pedido copiável:

```text
@hub-ml-tutor-databricks Explique @<trecho> para iniciante: objetivo, grão da entrada, transformação, ação Spark, saída e custo. Mostre um teste pequeno e separe intenção de resultado observado.
```
<!-- usage-card:end hub-ml-tutor-databricks -->

Os templates de comentário incluem cabeçalho, pré e pós em formas completas ou compactas. Eles orientam densidade, não obrigam um bloco de texto para cada célula. `doc_coverage` pode medir cobertura e componentes visuais podem melhorar navegação, mas citar um helper na resposta não significa que ele foi importado ou chamado. Para o tutor, `safe_display`, `smart_sample` e `format_br` são referências úteis quando o trecho lida com volume, amostragem ou apresentação; o contrato do helper precisa ser lido antes de explicar seu comportamento.

<a id="mu18-2"></a>
#### MU18.2 — Escolher template e criar um dos seis tipos

Antes de criar, pergunte **qual problema será reutilizado**. Uma função importável pertence a snippet; uma tarefa explícita de inspeção, transformação ou governança, com efeitos declarados, a script; um briefing para conversa, a prompt; a entrada de uma coleção, a README agregador; uma demonstração executável, a notebook; um método de trabalho para o agente, a skill. `auditoria/`, `output/` e identidade visual são padrões transversais, não tipos adicionais. O [índice de templates](../../hub_padroes/README.md) fornece o molde e um exemplo preenchido para cada tipo. Pesquise objeto equivalente antes de inventar nome ou seção. Se houver sobreposição, a decisão de criar recorte novo precisa ser explícita; ampliar objeto existente é outra tarefa.

<a id="uso-hub-ml-criar-objeto"></a>
<!-- usage-card:start hub-ml-criar-objeto -->
##### Ficha de uso — criar objeto

Escolha [`hub-ml-criar-objeto`](../../skills/hub-ml-criar-objeto/SKILL.md) quando uma solução já concebida precisa entrar no Hub com tipo, pasta, documentação e exemplo coerentes. Forneça objetivo, consumidor, nome, entrada, saída, limites, exemplo sintético e a busca de capacidade existente. A escolha entre os seis tipos deve ser confirmada antes da criação; para snippet, informe a seção. Uma pergunta apenas sobre formato pode receber orientação, sem iniciar [checagem prévia de contexto (preflight)](../../skills/hub-ml-criar-objeto/scripts/preflight.py) de escrita. Na conversão, declare origem e destino, preservando comportamento até decisão específica.

O entregável proposto pode reunir README local, fachada `__init__.py`, módulo e notebook de exemplo, conforme o template do tipo. Confira primeiro o resultado desse preflight, que resolve nome, template e caminho sem escrever. Para cinco tipos de `create` — snippet, script, prompt, notebook e README agregador — a [policy L3/audit](../../hub_padroes/skill_enforcement/policy.json) governa a skill; a validação do pacote no Git pode bloquear inconsistências e, quando válida, emitir um recibo verificável (Receipt). `skill` e `convert` ficam fora dessa rota. Mesmo com Receipt válido, autorizar e aplicar são passos separados. O piloto de escrita local só cobre **um README agregador novo** em pasta existente. Verifique no resultado quais arquivos realmente foram gerados, validados ou escritos; não aceite “criei os seis tipos” como conclusão genérica.

Pedido copiável:

```text
@hub-ml-criar-objeto Tenho <função/diagnóstico> repetido em <contextos>. Procure equivalente, proponha um dos seis tipos, nome e seção; confirme comigo antes de criar. Use @<template>, entrada/saída e exemplo sintético. Diga quais gates foram observados.
```
<!-- usage-card:end hub-ml-criar-objeto -->

<a id="uso-hub-ml-pipeline-builder"></a>
<!-- usage-card:start hub-ml-pipeline-builder -->
##### Ficha de uso — planejar pipeline

Escolha [`hub-ml-pipeline-builder`](../../skills/hub-ml-pipeline-builder/SKILL.md) quando o pedido é uma infraestrutura recorrente de ingestão, transformação ou scoring, com orquestração e operação. Informe origem, grão, volume, frequência, latência, [acordo de nível de serviço (SLA)](../../skills/hub-ml-pipeline-builder/SKILL.md), cloud, workspace, Unity Catalog, ambientes, política de reprocessamento e responsáveis. Uma camada bronze/silver/gold só ajuda se cada fronteira tiver contrato; não peça três camadas vazias. A skill pode propor Lakeflow pipelines, que estende o framework Apache Spark Declarative Pipelines, para fluxo declarativo, Lakeflow Jobs para orquestração e Declarative Automation Bundles para recursos por ambiente, conforme capacidades verificadas.

O entregável é uma especificação implementável: [grafo acíclico dirigido (DAG)](../../skills/hub-ml-pipeline-builder/templates/pipeline_spec.md), contratos de datasets, chaves e tempo de evento, regras de qualidade, estratégia incremental e reprocessamento histórico (backfill), observabilidade, matriz de ambientes e checklist de implantação. Confira se as expectativas declaram observar, descartar ou falhar com justificativa; se o checkpoint de progresso e a pasta de evolução de schema ficam em armazenamento governado, nunca efêmero; e se dados tardios têm reprocessamento e o retorno à versão anterior (rollback) tem responsável e critério. Helpers de qualidade podem informar protótipo, mas não substituem expectation monitorada no pipeline. Um plano não é deploy: `validate`, `deploy` e `run` exigem ambiente, credenciais, permissão e autorização próprios. Se a pergunta era apenas explicar um notebook, escolha o tutor, não uma arquitetura nova.

Pedido copiável:

```text
@hub-ml-pipeline-builder Planeje pipeline para <objetivo> com dados sintéticos. Origem <...>, grão <...>, SLA <...>, volume <...>, ambientes <...>. Entregue DAG, contratos, qualidade, backfill, testes e rollback. Não implante sem autorização.
```
<!-- usage-card:end hub-ml-pipeline-builder -->

A skill de pipeline também possui [perfis sintéticos delimitados](../../skills/hub-ml-pipeline-builder/scripts/README.md): preflight de especificação, execução Spark local e probe Delta autorizado no Free. A existência desses runners não transforma o pedido de planejamento em permissão de execução. A [reconciliação B1](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/skill_enforcement_rollout/B1_GATES_POS_MERGE_2026-10-01.md) registra aceite parcial do escopo A sintético; a policy mantém Pipeline Builder em `L0`, alvo `L4`. Orquestração Genie, promoção de nível e ambiente corporativo continuam gates separados.

O fluxo de criação tem camadas distintas. A policy vigente coloca `hub-ml-criar-objeto` em **L3/audit**; o `SKILL.md` preserva a descrição do preflight L2 e o rótulo de candidata na superfície de validação estrutural, enquanto seu piloto de escrita já remete ao nível L3/audit vigente. A policy determina o nível atual, enquanto o escopo de cada ferramenta delimita o que foi demonstrado. `preflight.py` reconhece os seis tipos e bloqueia falta de `type_confirmed` ou de busca de equivalente. `ser01_object_validation.py`, no Git, valida cinco tipos de pacote em clone/overlay e vincula base, candidato e run num Receipt. Para snippet e script, também confere cobertura de `api_publica.py`, que extrai nomes públicos do módulo por [árvore sintática de Python (AST)](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/api_publica.py) sem importá-lo e recusa notebook como módulo. A verificação do Receipt confere integridade e coerência, não identidade humana. `run.py` só escreve no piloto estreito de README agregador com autorização específica; a validação não promove essa capacidade aos outros tipos.

Essa separação evita um pedido comum que parece simples: “transforme meu notebook em snippet e atualize o catálogo”. A pessoa precisa decidir se quer **criar** um objeto novo ou **converter** um existente, apontar a origem, aceitar a pasta e revisar se o comportamento será preservado. O preflight de conversão verifica origem e destino, mas não autoriza mover, apagar ou sobrescrever. Para snippet novo, uma seção já existente pode ser indicada; abrir uma sétima seção requer autorização própria. Se o objeto for skill, o template de `SKILL.md` governa forma e recursos, mas a rota específica de validação L3 de cinco tipos não se aplica a ela. O resultado deve declarar `NOT_AVAILABLE` ou bloqueio nesse ponto, não trocar por uma checagem improvisada. Quem recebe o material consegue assim ver exatamente o que foi planejado e o que falta decidir.

<a id="mu18-3"></a>
#### MU18.3 — README, exemplo e critérios de aceite

Depois de criar um objeto, outra pessoa precisa decidir **quando usá-lo** e interpretar sua saída. O README local de snippet, script ou prompt segue [template de objeto](../../hub_padroes/readme/template_objeto.md) 1.0.0 com quinze seções: definição, problema, adequação, contraexemplo, mecanismo, situação, preparação, retorno, uso, decisões, riscos, alternativas, conferência, arquivos e referências. Um README agregador tem outro molde: apresenta uma coleção e conduz aos guias individuais. O nome “README” não torna os dois contratos intercambiáveis. Comece pela pergunta do leitor e pelo consumidor, depois confira módulo e fachada antes de escrever promessas de entrada e saída.

Para uma função importável, identifique o arquivo de implementação, a API de `__init__.py` e o notebook de demonstração. O utilitário `api_publica.py` extrai por AST definições públicas no topo do módulo e imprime conteúdo de fachada; não executa o módulo, não reexporta imports alheios e recusa um notebook marcado. Não deduza que o `__init__.py` da categoria exponha cada objeto irmão. Um exemplo mínimo deve importar da pasta de objeto, passar dados sintéticos pequenos e mostrar um retorno interpretado com unidade e grão. Para script, indique efeitos ou leitura de recursos; para prompt, mostre briefing preenchível e exemplo de pedido sem publicar uma resposta de [modelo de linguagem (LLM)](../../hub_padroes/prompt/template.md) como observação de execução.

O notebook de exemplo de snippet ou script é `.py` com a primeira linha `# Databricks notebook source`. Ele ensina a chamar a fachada e a interpretar o resultado. Antes de copiá-lo para um destino, leia dependências e células preparatórias: a demonstração pode consultar `current_user()` via Spark para montar caminho, mesmo quando o helper em si funciona em Python local. Uma linha “saída real” só pode relatar a execução documentada; se não houve execução, rotule o exemplo como ilustrativo e marque o bloqueio. O leitor precisa saber o que foi calculado, em qual base, com que parâmetros e em qual ambiente. Uma string visualmente plausível não é evidência de runtime.

Use um objeto real para preencher a receita: [`constants.format_br`](../../hub_snippets/constants/format_br/README.md) tem README local completo, [módulo](../../hub_snippets/constants/format_br/format_br.py), [fachada](../../hub_snippets/constants/format_br/__init__.py) e [notebook de exemplo](../../hub_snippets/constants/format_br/exemplo_format_br.py). Confirme na assinatura que `fmt_pct(v, casas=1, input_scale="ratio")` recebe por padrão uma **fração**, devolve `str` e não altera locale. Escolha a entrada sintética `0.928` e documente no README tanto a chamada quanto o resultado esperado que o módulo e o exemplo registram:

```python
from hub_snippets.constants.format_br import fmt_pct
taxa = 0.928  # fração sintética
texto = fmt_pct(taxa)
assert texto == "92,8%"
```

Interprete: `92,8%` é **texto de apresentação** da fração fornecida, não taxa calculada de uma tabela. `fmt_pct(92.8)` com a escala padrão mostraria valor cem vezes maior; para entrada já percentual, `input_scale="percent"` precisa ser explícito. O README exemplar explica adequação, assinatura, retorno, armadilha de escala, alternativa e conferência; use essa estrutura para outro objeto sem copiar seus fatos. A implementação e a fachada confirmam API, enquanto a saída citada aqui é a registrada no exemplo sintético da fonte, não uma execução nova neste manual. O [contrato editorial](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_objeto_contract.py) verifica forma e links; ele não calcula uma taxa real nem decide se o denominador de negócio está correto.

Os checks de manutenção formam uma sequência. Primeiro, confira marcador, quinze seções e cobertura do objeto, sem criar dispensa automática; depois, links relativos à implementação, exemplo e fachada. Compare parâmetros citados com assinatura e nomes de retorno consumidos no notebook. Execute a validação estrutural aplicável e registre comando, revisão e resultado, lendo em [MT27](MT-parte-vii.md#mt-mod-mt27) o que ela sustenta. Só depois, se houver ambiente autorizado, execute o caso sintético e guarde saída real com data e runtime. Um PASS de `validate_assistant.py` não comprova que a função roda no Databricks; uma execução Spark não revisa automaticamente acessibilidade, segurança ou adequação da explicação.

Uma mudança de API exige atualizar módulo, fachada, README, exemplo e consumidores que importam o nome antigo. A seção “quando não usar” deve acompanhar esse movimento: custo de coleta no driver, dependência opcional, tabela necessária, escala percentual e efeito de escrita são limites específicos que evitam uso incorreto. Não preencha as quinze seções com fórmulas genéricas. Se o objeto devolve [HTML, linguagem de marcação exibida no notebook](MT-parte-vi.md#mt-mod-mt24), diga quem o renderiza e como trata texto externo; se devolve DataFrame Spark, diga grão e ação que materializa o resultado. O critério de aceite editorial é o leitor conseguir reproduzir a chamada com entrada conhecida, entender a saída, reconhecer o bloqueio quando faltar dependência e saber qual validação ainda resta.

Na entrega, mantenha uma pequena trilha de conferência ao lado do README: versão do objeto, entrada sintética usada, valor esperado conhecido, saída efetivamente observada ou motivo de bloqueio, links para teste e dependências opcionais. Se a demonstração mostra uma tabela com cinco linhas, informe se cinco é contagem da amostra, de entidades distintas ou de resultados válidos após filtros. Se exibir porcentagem, declare se a função recebe fração ou número já escalado. Essa informação permite que outro mantenedor perceba um erro sem adivinhar intenção a partir de formatação. A revisão deve também abrir o documento no destino de leitura, pois Markdown renderizado e HTML de um notebook podem apresentar links ou símbolos de maneira diferente do texto fonte.

Quando um exemplo falha, corrija a causa documentada antes de “arrumar” apenas a saída. Um parâmetro inexistente pede alinhamento com a assinatura; uma coluna ausente pede entrada de teste adequada ou correção da função; um resultado sem execução pede rótulo de ilustração. Substituir uma saída real por número esperado sem rodar código apaga a distinção entre objetivo e evidência. O objeto só fica pronto para ser recomendado quando a documentação descreve o comportamento que seus testes e execução realmente sustentam, e quando os limites de uso estão visíveis para o público pretendido.

<a id="mu18-4"></a>
#### MU18.4 — Auditar evidência e corrigir desvios

Auditoria de skill começa por definir a pergunta: o **modo IMPLEMENTAÇÃO** examina a pasta da própria skill, suas referências e possibilidade de executar o fluxo; o **modo OUTPUT** confronta artefato produzido, pedido original e `SKILL.md` da produtora. Misturar modos leva a achados imprecisos: um notebook pode seguir um pedido, embora a pasta da skill tenha links quebrados; uma pasta pode estar íntegra, embora um resultado específico não tenha chamado o helper obrigatório. O preflight exige entradas observáveis antes de avaliar mérito. Um bloqueio por artefato ausente significa “não foi possível auditar”, não uma falha inventada da execução.

<a id="uso-hub-ml-auditoria-skills"></a>
<!-- usage-card:start hub-ml-auditoria-skills -->
##### Ficha de uso — auditar skill ou output

Escolha [`hub-ml-auditoria-skills`](../../skills/hub-ml-auditoria-skills/SKILL.md) quando precisar verificar se uma implementação de skill é executável ou se um resultado seguiu o contrato de sua produtora. Informe o modo. Para OUTPUT, forneça artefato, pedido original e nome do `SKILL.md` produtor; para IMPLEMENTAÇÃO, indique as pastas de skills a examinar. A [policy vigente](../../hub_padroes/skill_enforcement/policy.json) define L3, execução determinística em modo audit; a checagem prévia L2 ainda decide se há entrada suficiente para começar. A auditoria deve separar recurso apenas citado de recurso localizado, lido, importado, chamado e concluído, registrando `NOT_OBSERVABLE` onde falta prova.

O entregável é relatório com achado, fonte, efeito, correção mínima e critério de nova conferência. Confira se o Receipt `SE07-AUDIT-RECEIPT-1` se refere ao runner **da auditoria**, não à conclusão da skill produtora. Um PASS persistido pela produtora não vira `PASS_REVERIFIED` sem verifier canônico sobre o artefato atual; o adaptador explícito de [análise exploratória de dados (EDA)](MU-parte-ii.md#mu-mod-mu04) é um caso particular. Se um notebook diz “saída real” sem execução identificável, peça a evidência ou reclassifique como exemplo, sem fabricar métrica. Para qualidade estatística do resultado, use revisão de domínio além desta auditoria contratual.

Pedido copiável:

```text
@hub-ml-auditoria-skills Modo OUTPUT: confira @<artefato> contra @<SKILL.md produtora> e este pedido: <...>. Distinga citado, lido, chamado e concluído; registre evidência ausente e correção mínima sem inferir execução.
```
<!-- usage-card:end hub-ml-auditoria-skills -->

O runner L3 recebe uma escada explícita por recurso e emite Receipt de auditoria vinculado ao que observou. Esse Receipt protege a coerência do relato do runner, mas não substitui o postflight da skill produtora. No caso de EDA com payload final compatível, o adapter chama seu verifier canônico e só então pode classificar a conclusão como `PASS_REVERIFIED`. Sem adapter aplicável, use `NOT_REVERIFIED`; não prometa que todo output terá a mesma taxonomia. Para uma lacuna, peça a menor evidência que resolveria a dúvida: registro de chamada, output bruto, hash do artefato ou trecho da execução. Repetir um score geral sem apontar qual degrau faltou não ajuda a corrigir o fluxo.

Na prática, a correção pode ser documental ou funcional. Uma referência inexistente em `SKILL.md` pede reparar o link e revisar o pacote; um helper declarado mas nunca chamado pede executar a rota canônica ou ajustar o contrato, não marcar conclusão por semelhança da resposta. Se o preflight bloqueou antes da lógica, reporte o bloqueio e não culpe um algoritmo que nem rodou. O relatório deve citar revisão e artefato atual para que uma pessoa possa reproduzir a inspeção. Como em [MT27](MT-parte-vii.md#mt-mod-mt27), conformidade local não homologa Databricks, não aprova dados e não concede autorização de publicação.

Quando houver vários achados, ordene-os pelo efeito no usuário: primeiro a afirmação de conclusão sem evidência, depois contrato ou referência que impede reprodução, por fim legibilidade. A prioridade precisa apontar ação verificável, não apenas uma nota numérica. Reaudite o artefato corrigido, pois a correção muda a base da conclusão anterior.


<!-- editorial:exclude:start -->
[Anterior: MU17](MU-parte-v.md#mu17) · [Próximo: MU19](#mu19) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT27](MT-parte-vii.md#mt27)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu19"></a>
<a id="mu19"></a>
### MU19 — Instalar, atualizar e compartilhar uma entrega

Este percurso é para o mantenedor autorizado da instalação pessoal. Quem usa o Hub no dia a dia pode participar do aceite, mas não precisa operar Git, gerar ZIPs ou administrar o workspace. As decisões e comandos abaixo descrevem uma entrega planejada; sua execução depende do escopo, da autorização e do ambiente efetivo. O detalhamento técnico das ferramentas está em [MT28](MT-parte-vii.md#mt-mod-mt28), e o alcance dos testes locais em [MT27](MT-parte-vii.md#mt-mod-mt27).

<a id="mu19-1"></a>
#### MU19.1 — Defina pessoas, escopo e destino

Comece escrevendo em registro controlado qual commit será entregue, quais partes do Hub pertencem à revisão e qual pasta pessoal poderá recebê-las. Um exemplo de nomenclatura é `/Users/<username-trabalho>/hub_staging_<commit-curto>/`; os sinais angulares são espaços a preencher somente no destino autorizado. Não coloque host, usuário real, token, nome de tabela ou backup corporativo nesta documentação versionada. A pasta de staging é área de conferência, separada da instalação ativa em `/Users/<username-trabalho>/.assistant/` e do arquivo `.assistant_instructions.md` na raiz pessoal. Importar em staging não ativa skills nem atualiza instruções da Genie.

Há papéis diferentes mesmo quando uma pessoa acumula mais de um. O autor corrige a fonte no Git. O mantenedor escolhe o commit e monta o kit. O administrador do workspace define permissões e políticas. O revisor técnico confere o pacote e os testes permitidos. O usuário de aceite observa exemplos, imagens e comportamento da Genie na instalação final. Ter acesso de leitura a um ZIP, ou conseguir abrir um notebook, não concede por si só permissão para sobrescrever a pasta ativa, executar compute ou consultar dados. Confirme a autorização para cada etapa com a governança do ambiente; o [playbook de replicação](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/playbooks/replicacao-trabalho.md) é o roteiro operacional do projeto.

Antes do pacote, delimite o que é Hub e o que pertence a terceiros. Dentro de `.assistant`, não apague indiscriminadamente `skills/`: a instalação pode conter skills alheias, `.mcp_servers.json`, segredos ou outras configurações mantidas pela organização. Preserve também a lista de controle de acesso, ou ACL, ao planejar backup e promoção. O [project_policy.py](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/project_policy.py) define nomes e limites de caminhos do produto; [AGENTS.md](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/AGENTS.md) e os [ADRs](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/README.md), registros de decisões arquiteturais, documentam fronteiras de autoria e publicação. O [índice de manutenção por tarefa](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/ai/README.md) ajuda a localizar os procedimentos vigentes, sem substituir a política de acesso do workspace.

Registre a base instalada antes de escolher a atualização: commit anterior se conhecido, árvore atual, arquivos que serão substituídos, dependências esperadas e possibilidade de retorno. Se encontrar material sem dono claro, interrompa a substituição desse item e peça identificação ao mantenedor responsável. Staging permite comparar revisões sem alterar a instalação de trabalho. O objetivo da etapa é sair com um destino concreto e uma lista verificável, e não com uma autorização inferida de acesso à interface. Conteúdo customizado `.assistant` e o serviço nativo Databricks têm ciclos de vida diferentes; esta entrega atualiza somente os arquivos do Hub sob o escopo autorizado.

O plano deve nomear também quem fará cada conferência: pacote, instalação, teste técnico e observação humana. Isso evita que uma mesma marca “aprovado” esconda lacunas entre etapas. Uma pasta pessoal de testes pode ser autorizada enquanto a instalação ativa ainda está bloqueada; registre os dois estados separadamente.

<a id="mu19-2"></a>
#### MU19.2 — Valide a fonte, regenere o espelho e monte o kit

No checkout da revisão escolhida, comece pelos gates locais pertinentes, descritos em [MT27](MT-parte-vii.md#mt-mod-mt27). `validate_assistant.py` examina o contrato do produto; `ci_local.py` agrega verificações locais declaradas pelo projeto. Um PASS aqui significa que aquele teste rodou contra aquela árvore: não é prova de instalação no destino, de permissão ou de execução Spark corporativa. Registre o commit e o resultado, e resolva divergências na fonte antes de empacotar. Dependências de Python e Node precisam estar disponíveis conforme a documentação do projeto; uma falha de pré-requisito não é sucesso do produto.

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
[Anterior: MU18](#mu18) · [Próximo: MU20](#mu20) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT28](MT-parte-vii.md#mt28)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu20"></a>
<a id="mu20"></a>
### MU20 — Resolver problemas e concluir um percurso com evidência

<!-- editorial:exclude:start -->
**Pergunta:** como uma pessoa iniciante distingue erro de ambiente, contrato e resultado, e percorre uma análise até um relatório revisado? **Rota:** a parte A ensina o diagnóstico; a parte B junta os passos em uma tarefa copiável. Código e tabela deste capítulo são ilustrativos e não foram executados nesta redação. [Índice do manual](MU-indice.md#sumario-mu).
<!-- editorial:exclude:end -->

<a id="mu20-1"></a>
#### 1. Em que fase ocorreu o erro?

Comece anotando o que você tentou fazer: ler uma tabela, importar um helper, executar a skill, desenhar uma figura ou concluir o relatório. Essas ações têm dependências e efeitos diferentes. Uma **EDA** (análise exploratória de dados) examina estrutura, qualidade e distribuição de uma fonte para orientar uma decisão. Se você ainda não consegue localizar a fonte, não existe resultado de EDA a interpretar. Se uma biblioteca Python não importa, não conclua que a tabela está inacessível. Se o gráfico falha, um perfil tabular pode continuar útil, mas a obrigação visual da skill selecionada talvez permaneça aberta.

Para praticar sem dados de trabalho, a [fixture `base_tabular`](../../hub_snippets/testing/fixtures/fixtures.py) cria um **DataFrame Spark** sintético com `id_cliente`, `uf`, `renda`, `dt_referencia` e `alvo`. Spark é o motor que processa o DataFrame; a função pede uma sessão ativa ou cria uma sessão conforme o ambiente. Ela não grava tabela. `n`, `seed`, fração de nulos e número de entidades controlam a população artificial; a semente torna a geração repetível no mesmo contrato, sem garantir identidade de números em todos os runtimes. O [README de fixtures](../../hub_snippets/testing/fixtures/README.md) explica a finalidade de ensaio. A **view temporária** que criaremos na parte B recebe nome na sessão atual; não é uma tabela publicada. Mesmo esse efeito em sessão deve ocorrer só em compute autorizado.

Use a fase para localizar a primeira causa plausível. Se `from hub_snippets.testing import fixtures` falha, confira se `.assistant` existe no caminho esperado, se essa raiz está em `sys.path` e se as dependências do pacote estão disponíveis. Se `spark.table("mu20_clientes_sinteticos")` falha depois de criar a view, confira sessão, nome e se a célula de criação realmente terminou; se o nome aponta a tabela persistente de outra pessoa, também confira catálogo e permissão. Não trate `ModuleNotFoundError` como problema da lista de controle de acesso (ACL) da tabela, nem `TABLE_OR_VIEW_NOT_FOUND` como prova de que o código do helper está errado. O [README da .assistant](../../README.md) mostra a organização de imports.

Tema visual tem outra superfície. `ThemeError` com código `DEPENDENCY_MISSING` indica que a validação do tema não encontrou uma dependência; a [matriz de erros](../../hub_padroes/identidade_visual/ERROS.md) aponta para [requirements-temas.txt](../../hub_snippets/requirements-temas.txt). Ela não instala nada sozinha e não autoriza instalação num cluster. `RESULT_TYPE` ou `RESULT_INTEGRITY` apontam objeto `ResolvedTheme` inadequado ou adulterado, não falha de acesso Spark. Primeiro identifique a biblioteca e o ambiente permitidos, depois refaça `resolve_theme` ou `load_theme` na rota correta. O [MU17](MU-parte-v.md#mu17-1) detalha o tema e suas mensagens.

Estado de policy, o registro de regras e níveis da skill, também não é diagnóstico de import. A [policy](../../hub_padroes/skill_enforcement/policy.json) separa `current_level`, nível sustentado hoje, de `target_level`, direção de migração. A skill piloto EDA tem L4 e modo `enforce`; outra skill pode ainda ter nível menor e alvo L4. **L4** quer dizer que a conclusão depende de verificação posterior, chamada Postflight. Não leia “alvo L4” como “Ready” (pronto para promoção) nem como autorização para executar em qualquer dado. O [MU08](MU-parte-iii.md#mu08-1) explica como escolher recurso e confirmar sua rota; o [MU12](MU-parte-iii.md#mu12-1) ensina a interpretar saída de ML sem promover métrica a decisão.

Quando pedir ajuda, leve quatro dados pequenos: fase, comando ou nome do recurso, mensagem/código e o que foi observado antes da falha. Inclua versão e ambiente quando relevantes. Substitua tabela e identidade reais por exemplo sintético reproduzível; não cole token, dado pessoal ou cinco linhas brutas de uma base de trabalho. Se a operação tinha escrita, informe **o destino e o modo** em canal autorizado antes de repetir. Essa informação evita que alguém recomende “rodar de novo” uma célula que sobrescreve tabela. O [MU05](MU-parte-ii.md#mu05-1) ajuda a declarar objetivo, grão, fonte e desconhecidos antes de escolher um briefing.

<a id="mu20-2"></a>
#### 2. O que fazer quando o contrato bloqueia ou o resultado parece pronto?

Escolher `@hub-ml-eda-profissional` vincula a tarefa à rota da [skill](../../skills/hub-ml-eda-profissional/SKILL.md). O **preflight** confere contrato, condições, recursos e templates antes da execução; sua saída isolada é diagnóstico L2, não EDA concluída. O runner chama `quick_profile` e emite um **Receipt**, comprovante estruturado de vínculo entre entrada, trace, saída e release. O executor L4 observa imports, chamadas, conclusão de recursos e leitura de templates aplicáveis. O **Postflight** confere a evidência e o handoff final. Um número plausível de linhas, um Receipt `VALID` e uma figura bonita ainda podem coexistir com `completion.status="PENDING_POSTFLIGHT"`. O [MT30](MT-parte-vii.md#mt30-2) desenha o mecanismo completo.

O percurso principal da parte B usa `run_enforced(table_name, context=None, *, assistant_root=None, sample_fraction=0.1, max_categories=20, seed=42, display_fn=None, resolved_theme=None, strict=True)`. A tabela/view precisa existir e ser legível pela sessão autorizada. O contexto padrão solicita distribuições e diagnósticos visuais; preview tabular, amostra local adicional e tema começam desligados. Só declare `pk_columns` quando a chave candidata estiver estabelecida como lista não vazia de strings. Ausência de chave deixa `data_quality_check` não aplicável com decisão justificada; `pk_columns=[]` é entrada inválida, não uma maneira de pedir “descubra a chave”. O [contrato EDA](../../skills/hub-ml-eda-profissional/execution_contract.json) dá os IDs e as condições que serão conferidos.

Leia o retorno em ordem. `trace.status` mostra se o core passou; `trace.enforcement_status` resume gaps L4; `trace.evidence_gaps` e `blocking_issues` dizem o que investigar. `resources_resolved` informa que o nome foi encontrado, `resources_called` que a função começou, `resources_completed` que retornou; o mesmo ID não migra automaticamente entre listas. `templates_loaded` exige leitura real, não citação nominal do arquivo. `receipt` e `artifacts` permitem verificar vínculo, mas não avaliam a qualidade da inferência. Se core e enforcement passaram, `completion.status="PENDING_POSTFLIGHT"`, `authorized=false` e `claim_allowed=false` significam **etapa obrigatória pendente**, mesmo que o comando tenha terminado com código `0`. O próximo passo é o finalizador com handoff verdadeiro, não uma frase de conclusão.

Há uma nuance útil para diagnóstico. Com `strict=True`, falha de core ou enforcement levanta `CanonicalExecutionBlocked` e carrega payload; guarde o diagnóstico e corrija a causa. Com `strict=False`, falha do **core** devolve `NOT_COMPLETED`. Se o core passou, mas há gaps de enforcement, a implementação atual conserva `enforcement_status="INCOMPLETE"` e marca `completion.status="PENDING_POSTFLIGHT"`, ainda com `authorized=false` e `claim_allowed=false`. Portanto, **não leia apenas a palavra PENDING**: leia também trace e gaps. A função Python devolve um `dict`; `strict=False` é argumento dessa função, sem flag equivalente na CLI. O `main()` da CLI retorna código de saída `2` quando o payload obtido não demonstra core e enforcement PASS; esse inteiro é estado do processo, não retorno de `run_enforced`. `strict=False` serve para inspecionar, não para completar a mesma EDA por células manuais. O [MU04](MU-parte-ii.md#mu04-4) reforça como reconhecer evidência ausente e separar uma resposta segura de tarefa concluída.

O handoff da EDA tem seis campos: `sources_snapshot` (fonte e fotografia), `unit_keys_target` (unidade, chave e alvo ou ausência), `quality_risks` (riscos observados e limites), `feature_candidates_leakage` (variáveis e disponibilidade temporal), `filters_sample` (filtros, fração, semente e denominadores) e `open_questions` (pendências). Só o último aceita `[]` vazio pelo contrato atual. A [função de Postflight](../../hub_scripts/skill_execution/postflight/__init__.py) distingue campo ausente (`HANDOFF_FIELD_MISSING`) de campo nulo/vazio/branco (`HANDOFF_FIELD_EMPTY`) e pode devolver `REVIEW`. Essa validação é **estrutural**: texto genérico não vazio pode passar, mas não demonstra que o risco foi analisado. Confira cada frase com o que o payload e o dado realmente sustentam; perguntas abertas honestas são preferíveis a certeza inventada.

Imagine que `id_cliente` se repita na fixture. Um handoff útil registra que o identificador não foi aceito como chave única, informa o grão que ainda precisa de decisão e separa essa observação da hipótese de que haja duplicidade indevida no negócio. A fixture foi construída para ensinar o problema; a mesma frase não pode ser transportada para uma tabela real sem medir e conhecer seu grão. Em `filters_sample`, descreva a fração solicitada e confira a quantidade efetivamente usada; a porcentagem configurada não prova que todas as análises posteriores receberam exatamente o mesmo denominador. Em `feature_candidates_leakage`, escreva quando uma variável estaria disponível em relação ao instante de decisão. Se esse instante é desconhecido, declare a pergunta em `open_questions`, sem marcar a variável como segura.

Depois de produzir o handoff, `finalize_or_raise(payload, handoff, assistant_root=...)` reverifica Receipt, contrato e rota L4, constrói Postflight e valida a consistência final. Só um retorno com `postflight.status="PASS"`, `completion.authorized=true` e `completion.status="COMPLETED"` suporta a frase “a skill concluiu segundo o contrato”. Se falhar, `CompletionNotAuthorized` conserva diagnóstico. O [MU04](MU-parte-ii.md#mu04-3) mostra como essa exigência entra no uso da skill; o [MT19](MT-parte-iv.md#mt19-1) separa aderência de correção analítica. Uma chamada isolada de `quick_profile` pode responder a uma pergunta delimitada e produzir um dict útil; se a skill EDA foi selecionada, ela **não substitui** L4 nem autoriza o mesmo claim de conclusão.

Para recuperar, classifique o código. `RESOURCE_RUNTIME_UNAVAILABLE` em preview pede `display_fn` realmente disponível ou revisão objetiva do pedido opcional. `RESOURCE_INPUT_MISSING` em tema exige objeto resolvido ou figura representativa; não invente um. `ARTIFACTS_DIGEST_MISMATCH` exige localizar alteração de artifacts, não recalcular hash para “passar”. `HANDOFF_FIELD_MISSING` pede campo ausente; um valor real e verificável ainda precisa ser escrito por uma pessoa. Após corrigir entrada ou dependência autorizada, inicie um **novo percurso canônico**. Não remonte Receipt, não reclassifique a skill como manual e não use um disclaimer para contornar o bloqueio.

Um erro reproduzível inclui a etapa e o estado anterior: “a view foi criada nesta sessão; o preflight resolveu o recurso; a chamada falhou antes de `resources_completed`; o código foi `RESOURCE_RUNTIME_UNAVAILABLE`”. Compare essa sequência com o caso em que `resources_completed` contém o recurso, mas o relatório ainda não explica o denominador. O primeiro pede recuperação de execução; o segundo pede interpretação humana. Se a leitura do template falha, informe o nome do template e o gap, pois um arquivo apenas listado no contrato não satisfaz `templates_loaded`. Preserve o payload original para comparação com a próxima tentativa, sem editar seus campos de evidência.

<a id="mu20-3"></a>
#### 3. Como resolver uma falha visual e pedir ajuda que permita reproduzi-la?

Primeiro separe **cálculo**, **figura**, **tema** e **exibição**. Um cálculo tabular pode terminar e a figura falhar na conversão ao driver; uma `Figure` pode existir sem ser mostrada no notebook; um tema pode falhar antes de alterar a figura. Pergunte: qual função foi chamada, quais colunas recebeu, houve retorno e qual foi a primeira exceção? A [matriz de gráficos EDA](../../skills/hub-ml-eda-profissional/templates/matriz_graficos_eda.md) ajuda a escolher forma adequada à pergunta, enquanto o [estilo visual](../../skills/hub-ml-eda-profissional/templates/estilo_visual_eda.md) orienta apresentação. Ler esses templates não prova que o relatório os aplicou corretamente.

Para duas colunas numéricas da fixture, `plot_correlation(df, cols=["renda", "alvo"], method="spearman", threshold_highlight=0.8)` devolve `(Figure, strong_pairs)`. A lista marca pares cujo **valor absoluto** da correlação é maior ou igual ao limiar; associação negativa forte também aparece. A função remove linhas com nulos nas colunas selecionadas para o cálculo. Não use o total de linhas da base como denominador da correlação sem verificar esse recorte. `alvo` é um indicador sintético: uma associação não mostra causa nem valida uma variável preditora antes de definir tempo de decisão. O [código da matriz](../../hub_snippets/display/correlation_matrix/correlation_matrix.py) mostra retorno e filtros reais.

Se houver apenas uma coluna numérica útil, correlação entre duas colunas não se aplica; uma distribuição é pergunta mais adequada. [plot_distributions](../../hub_snippets/display/distribution_grid/distribution_grid.py) seleciona números, usa `smart_sample` antes de `toPandas()` e retorna `Figure`; `sample_n=10000` é default, não garantia de amostra de dez mil linhas. Confirme quantas linhas ficaram na amostra e se os extremos raros poderiam ter ficado fora. Se a figura não aparece, verifique se o retorno foi uma `Figure` e se o notebook recebeu uma chamada explícita de exibição; o helper não publica relatório nem workspace. Uma rota que devolve figura não diz onde ela foi salva. O [MU17](MU-parte-v.md#mu17-2) aprofunda escolha de tema e consumidores.

Tema validado é objeto `ResolvedTheme` obtido por [resolve_theme/load_theme](../../hub_snippets/visual/tema/tema.py), com contexto compatível com notebook. A [camada Plotly](../../hub_snippets/visual/theme_plotly/theme_plotly.py) recebe esse objeto, aplica aparência e pode devolver a mesma figura; não muda os dados, os filtros ou o significado da métrica. Dentro de L4, a seleção de tema também participa do trace e do Receipt reemitido: não diga que toda evidência permanece idêntica só porque os números são iguais. Se `resolved_theme_selected=True` sem objeto validado, há `RESOURCE_INPUT_MISSING`; se não houver figura representativa, o mesmo código pode indicar ausência de entrada visual. A solução é corrigir entrada/condição e refazer a rota, não pintar manualmente uma imagem e chamá-la de evidência L4.

Erros de tema costumam trazer um `ThemeError.code`. A [tabela ERROS](../../hub_padroes/identidade_visual/ERROS.md) distingue dependência ausente, schema inválido, caminho inseguro e resultado adulterado. Com `DEPENDENCY_MISSING`, confirme requirements e ambiente autorizado; não peça que alguém instale biblioteca em cluster compartilhado sem permissão. Um erro de contrato de tema não prova que Spark falhou; uma falha Spark não prova que a paleta está errada. O [guia operacional](../../hub_padroes/identidade_visual/GUIA_OPERACIONAL.md) separa tema de dados e descreve os contextos suportados. Compare rota legada e `_resolvido` apenas no que cada uma aceita e altera na aparência.

Um pedido de ajuda reproduzível pode caber em cinco linhas: “Queria histograma de `renda` da fixture sintética; `plot_distributions` recebeu `sample_n=200`; retornou `Figure` ou lançou [classe/código]; a sessão usa [runtime e versão] com tema [ausente ou `ResolvedTheme` notebook]; executei apenas [passos observados]”. Acrescente traceback mínimo e número de linhas/colunas, sem enviar tabela de trabalho, token nem caminho pessoal. Informe se a skill EDA estava selecionada e qual era `trace.enforcement_status`; uma figura isolada sem trace é caso diferente de recurso L4 aplicável que falhou. Se um helper funcionou, mas o relatório ficou confuso, peça revisão da legenda, do denominador e das limitações, não reexecução cega da tabela.

Antes de trocar um parâmetro, formule uma pergunta verificável. Para `renda`, “qual a distribuição dos valores não nulos na amostra exibida?” pede histograma e contagem de ausentes separada. Para `uf`, a pergunta sobre frequência por categoria pede barras com total e tratamento de categorias raras; forçar correlação numérica de códigos de estado criaria uma ordem artificial. Para `renda` e `alvo`, correlação exige explicitar método, linhas completas e se o alvo binário é apenas marcador sintético. Se o eixo parece truncado, compare dados enviados ao helper, limites do eixo e resumo tabular antes de mudar escala. Esses passos separam um defeito visual de uma propriedade da amostra.

Se a função devolveu `Figure`, use a exibição apropriada ao notebook autorizado e registre se o objeto foi efetivamente mostrado; retorno e tela são evidências diferentes. Se quiser salvar a figura, defina destino, formato e autorização como decisão adicional, pois a função de plot não fornece publicação automática. Para comparar duas versões, conserve colunas, método, amostragem e denominador, depois descreva separadamente a alteração de tema. Um tema diferente pode mudar contraste e legibilidade; não justifica afirmar que o dado mudou. Na rota L4, essa escolha pode alterar trace e novo Receipt, então reúna a evidência do percurso correspondente à versão revisada.

Evite três conclusões precipitadas. “Figura não apareceu” não significa “métrica foi zero”; “métrica correta” não significa “skill concluída”; “tema bonito” não significa “gráfico aprovado para publicação”. Cada afirmação pede sua evidência. Para uma entrega, anote colunas, método, amostra, filtros, fonte e instante da coleta. Mostre também o que permaneceu não observado. Isso permite que outra pessoa corrija a primeira falha real, em vez de alterar várias camadas e perder a causa.

<a id="mu20-4"></a>
#### 4. Como ir do objetivo a um relatório revisado sem esconder efeitos?

O objetivo deste exercício é decidir **que perguntas de qualidade ainda faltam** antes de usar uma base de clientes num estudo. A fixture é sintética, pequena e não representa clientes reais. Escolha um compute Spark autorizado, confirme que a pasta `.assistant` está instalada no local usado e execute a sequência somente nesse ambiente. O código abaixo é um roteiro copiável **condicional**: ele cria um DataFrame e uma view temporária de sessão, importa os scripts da skill por seus arquivos e chama o executor. Não houve execução nesta redação. O [MT30](MT-parte-vii.md#mt30-1) explica cada vínculo técnico.

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

Confirme na tela título, eixo, valores não nulos e legibilidade. A função amostra antes de coletar ao driver; `sample_n=120` é limite solicitado, não prova do denominador exibido. O histograma não quantifica ausentes: confronte-os com o perfil observado. Falha do renderer deve ser registrada como falha desta inspeção, sem fabricar figura ou modificar Receipt. Para outra pergunta, a correlação da seção anterior continua exigindo duas colunas e recorte de linhas completas. Registre separadamente retorno da `Figure`, exibição observada e avaliação humana. O [roteiro EDA](../../skills/hub-ml-eda-profissional/templates/roteiro_eda.md) orienta ordem da investigação, e o [modelo de relatório](../../skills/hub-ml-eda-profissional/templates/relatorio_executivo_eda.md) exige objetivo, período, volume, granularidade, padrões, anomalias e limitações. Preencha somente com observações e revisão humana; template carregado não é relatório preenchido.

> **Efeito separado: notebook de briefing `data_quality`.** A [Parte 1 do exemplo](../../hub_prompts/data_quality/exemplo_data_quality.py) faz `base.write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes_dup")`. Rodá-la pode **sobrescrever uma tabela persistente** nesse destino; confira nome, permissão e impacto antes de escolher essa rota. Ela não faz parte da view temporária do percurso principal. A Parte 2 é um prompt preenchido para copiar manualmente ao chat; texto não executa skill. A Parte 3 diz `NÃO EXECUTADO` até uma resposta real ser obtida, datada e revisada. O [MU05](MU-parte-ii.md#mu05-3) mostra como separar essas três evidências.

Por fim, revise figura e relatório com outra pessoa, retire dados ou caminhos sensíveis e identifique as dúvidas que ainda mudam a decisão. Salvar notebook, publicar em workspace ou compartilhar relatório são ações posteriores, cada uma com destino e autoridade próprios. [render_simulado.py](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/render_simulado.py) monta o espelho do produto no repositório e [validate_assistant.py](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/validate_assistant.py) verifica esse produto; nenhum deles executa esta EDA ou publica o resultado da turma. Um percurso falho termina com diagnóstico e recuperação causal, não com uma frase de sucesso. Um percurso contratualmente concluído termina com evidência preservada e interpretação revisável, sem prometer aprovação de negócio ou publicação automática.


<!-- editorial:exclude:start -->
[Anterior: MU19](#mu19) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT30](MT-parte-vii.md#mt30)
<!-- editorial:exclude:end -->
