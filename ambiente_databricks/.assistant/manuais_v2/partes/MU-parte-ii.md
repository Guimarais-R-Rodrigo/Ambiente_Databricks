<a id="parte-mu-ii"></a>
# MU parte ii

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MU-indice.md#sumario-mu) · [Livro completo](../../MANUAL_DO_USUARIO.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu04"></a>
<a id="mu04"></a>
### MU04 — Usar skills do pedido à entrega revisada

**Pergunta deste capítulo:** o que informar, acompanhar e conferir quando uma skill orienta seu trabalho no Genie Code? Comece por uma tarefa pequena e uma fonte identificada. A escolha da skill é só a primeira etapa: leia o plano, acompanhe as ações e confira o que a evidência permite dizer sobre o resultado.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](MU-indice.md#sumario-mu) · [Primeiro uso](MU-parte-i.md#mu02) · [Encontrar recursos](MU-parte-i.md#mu03) · [Preencher briefings](#mu05) · [Arquitetura técnica](MT-parte-iii.md#mt14) · [Execução verificável](MT-parte-iv.md#mt19)
<!-- editorial:exclude:end -->

<a id="mu04-1"></a>
#### 1. Escolher a skill e observar a seleção

Uma **Agent Skill** é uma pasta de instruções para o assistente, centrada em `SKILL.md`. Ela descreve quando se aplica, como conduzir a tarefa e que recursos adicionais consultar. O mecanismo de Agent Skills pertence ao Genie Code; os nomes `hub-ml-*` e seus métodos são conteúdo deste Hub. O [catálogo de skills](../../skills/README.md) apresenta as 15 opções desta versão. Uma skill não é uma biblioteca Python: ler suas instruções não instala nem chama os helpers recomendados. [MU03](MU-parte-i.md#mu03) ajuda a localizar a família antes de escolher.

Há duas formas de chegar a uma skill. Se você sabe qual método deseja, selecione `@hub-ml-...` na interface e descreva a tarefa. A menção explícita reduz ambiguidade e permite conferir o nome escolhido. Quando o pedido coincide com a `description` do cabeçalho de uma skill, o Genie Code **pode** selecioná-la por relevância; a redação do pedido e a disponibilidade no ambiente influenciam essa escolha. A [documentação oficial de Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills), reconferida em 2026-10-07, descreve seleção por relevância e menção `@`. Observe o indicador de seleção e a resposta em sua sessão. A simples ocorrência do nome na resposta não prova que a skill foi carregada. A [referência atual de plataforma](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/ai/references/databricks-genie-code.md) distingue `@` para skill de um atalho como `/eda`, que o Hub não registra como comando.

Escolha pela decisão a produzir. Para examinar uma fonte, `hub-ml-eda-profissional`; para cruzar fontes antes de modelar, `hub-ml-cross-eda-ml`; para definir atributos disponíveis no ponto de decisão, `hub-ml-feature-engineering`. `hub-ml-baseline-ml` orienta o primeiro modelo, `hub-ml-explainability` a explicação de um modelo identificado e `hub-ml-monitoramento-modelo` o acompanhamento de um modelo em operação. `hub-ml-analise-safra` trata coortes e maturação; `hub-ml-validacao-estatistica` trata pergunta, pressupostos, efeito e incerteza. Para fluxo de dados, escolha `hub-ml-pipeline-builder`; para criar um objeto do próprio Hub, `hub-ml-criar-objeto`. `hub-ml-comentar-notebook` documenta células, `hub-ml-tutor-databricks` ensina um objeto ou erro real, e `hub-ml-auditoria-skills` revisa implementação ou saída de skill. `hub-ml-micromodelos` orienta especificação de uma característica de domínio ou descoberta de oportunidades por metadados; sua biblioteca exige execução separada. `hub-ml-concierge` é a rota de descoberta quando ainda falta decidir qual componente usar; sua recomendação termina em um repasse, sem executar o especialista. Consulte o `SKILL.md` e o [catálogo de skills](../../skills/README.md); leia também o README local quando a pasta da skill o tiver, antes de assumir que a descrição curta cobre seu caso.

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

Quando você autorizar executar, confirme **qual operação** e **em qual ambiente**. A skill pode indicar templates e helpers, mas o notebook ainda precisa tornar a biblioteca acessível ao Python, importar a função correta e chamá-la. Um trecho de código gerado é proposta; um import é disponibilidade; uma chamada observada é execução; um resultado checado é uma etapa adicional. Por exemplo, a [análise exploratória de dados (EDA)](../../skills/hub-ml-eda-profissional/SKILL.md), que examina a fonte antes de uma decisão, pode recomendar `hub_scripts.quick_profile`, mas a recomendação textual não calcula um perfil. A [explicação do mecanismo](../../skills/README.md#relacao-entre-skills-hub-snippets-e-hub-scripts) ajuda a distinguir método e runtime.

Também pergunte o que fazer se o contexto necessário não estiver disponível. Para um cruzamento temporal, um timestamp de evento sem a data de disponibilidade da fonte não prova que um atributo existia no instante da decisão. Um plano pode mostrar o teste necessário e parar; código que presume a disponibilidade inventaria uma condição de validade. Se a etapa depende de dado ausente, o assistente deve declarar a lacuna, o possível impacto e a menor próxima ação para resolvê-la. Um bom bloqueio preserva o trabalho já verificado sem transformar incerteza em conclusão.

Se o plano propuser amostragem, peça o critério e verifique a quem os resultados se aplicam. Uma amostra dos primeiros registros pode perder meses, segmentos ou eventos raros; uma amostra aleatória sem semente e tamanho documentados dificulta a reprodução. Se propuser um gráfico, confira se a agregação ocorreu antes de levar dados ao driver e se categorias omitidas aparecem no limite declarado. Para uma ação persistente, compare nome completo do destino, modo de escrita e consequência de uma segunda execução. Guarde o plano aprovado junto da resposta e anote alterações posteriores: “execute o plano” só é uma autorização inteligível quando a versão do plano e seus efeitos estão claros.

<a id="mu04-3"></a>
#### 3. Ler níveis, gates e evidência da entrega

O **Skill Enforcement Framework (SEF)** é a convenção deste Hub para dizer quanto do procedimento de cada skill pode ser conferido mecanicamente. No [arquivo de policy](../../hub_padroes/skill_enforcement/policy.json), `current_level` descreve o nível operacional admitido pela policy; `target_level` indica a direção planejada. Verifique também `rollout_mode`: `guidance` orienta, `audit` mede sem bloquear, `warn` avisa e `enforce` pode impedir uma conclusão homologada. O nível alvo nunca substitui evidência de uso da versão atual. A [introdução à policy](../../hub_padroes/skill_enforcement/README.md) desenvolve essa leitura.

Leia a escala como perguntas sucessivas. **L0**: há orientação textual no `SKILL.md`? **L1**: existe contrato estruturado conferível sem executar a análise? **L2**: o **preflight** resolveu requisitos antes da lógica protegida? **L3**: o **runner** executou o caminho canônico e produziu um *Receipt*, comprovante ligado àquela execução? **L4**: o **postflight** conferiu a evidência final e autorizou a conclusão? O hash de um arquivo ajuda a detectar alteração dos bytes comparados, mas não prova, sozinho, que o resultado de negócio está correto. O [Manual Técnico](MT-parte-iv.md#mt19) explica contratos, Receipt e verificadores em mais detalhe.

O estado atual varia por skill. Na policy consultada para este capítulo, `hub-ml-concierge` está L1/audit e encerra na recomendação; `hub-ml-comentar-notebook` e `hub-ml-micromodelos` também estão L1/audit. `hub-ml-auditoria-skills` e `hub-ml-criar-objeto` estão L3/audit. `hub-ml-eda-profissional` está L4/enforce. Várias skills analíticas, como baseline, safra, cross-EDA, features, explicabilidade, monitoramento, pipeline e validação estatística, ainda têm `current_level=L0` mesmo quando o alvo é L3 ou L4; `hub-ml-tutor-databricks` é L0/guidance. O escopo técnico B1 já integrou perfis executáveis delimitados para essas oito skills, com contratos e verificadores próprios; isso não promoveu seus níveis L0/audit nem demonstrou orquestração universal pela Genie Code. Um runner disponível pode produzir evidência de seu perfil sintético, mas não certifica outros dados ou operações. Leia o `scripts/README.md` da skill e confira o perfil, os inputs e os efeitos autorizados. Um script encontrado na pasta não eleva essa policy. Para cada tarefa, consulte o valor vigente antes de exigir ou alegar uma prova que só pertence a outro nível.

Na EDA profissional selecionada, a rota completa usa `scripts/run_enforced.py`, que reúne a execução canônica e evidência para L4. Depois, `scripts/postflight.py::finalize_or_raise` confronta resultado, recursos, templates e resumo de entrega. Só `postflight.status="PASS"` com `completion.authorized=true` permite dizer que a skill terminou conforme seu contrato. `PENDING_POSTFLIGHT` significa que falta a verificação final; um Receipt `VALID` isolado comprova a etapa L3, não o fechamento L4. Se o preflight bloquear por recurso ou entrada faltante, peça o dado objetivo, corrija e inicie uma nova execução canônica, ou relate “não concluída”. O [SKILL de EDA](../../skills/hub-ml-eda-profissional/SKILL.md) define esse comportamento.

Essa exigência fica clara em uma entrega bloqueada. Imagine que você selecionou `@hub-ml-eda-profissional`, mas proibiu `run_enforced` e postflight no mesmo pedido. O contrato da skill trata as instruções como conflitantes; uma análise manual na mesma tarefa não recebe selo de conclusão L4 por ganhar um aviso de ressalva. A resposta útil explica o conflito, identifica os entrypoints exigidos e solicita uma nova decisão sobre a rota; enquanto isso, a EDA fica **não concluída**. A mesma cautela vale se o runner retornar bloqueio ou o postflight não passar. Não atribua a uma skill L0 essa regra específica de EDA L4; confira sua policy e o próprio `SKILL.md`.

Ao revisar uma resposta, percorra uma escada curta de evidência: recurso **citado**, **localizado**, **lido**, helper **importado**, **chamado** e **concluído**. Uma etapa não prova a seguinte. Para cada afirmação importante, peça caminho e versão consultados, entrada, operação, saída e evidência de conferência. Se a interface ou o runtime não mostrar uma dessas etapas, registre “não observável”, em vez de inventar um PASS ou concluir que não ocorreu. Separe também a qualidade da análise da aderência ao contrato: uma tabela aparentemente plausível pode ter sido produzida por outro caminho, e um Receipt íntegro não valida automaticamente interpretação, população ou decisão.

Leia um Receipt como vínculo técnico entre uma execução, seus insumos e a saída registrada, não como uma assinatura de que a decisão de negócio é boa. Quando houver verificador aplicável, confira se foi realmente executado na mesma base e release; copiar um status antigo não revalida a execução atual. No resumo final, procure também perguntas abertas, recursos pulados com justificativa e origem de cada número. Se o resultado disser que uma coluna é inadequada, peça a regra ou limiar usado, o denominador e o período. Esses detalhes permitem a uma pessoa refazer a conclusão e discordar dela com fundamento.

<a id="mu04-4"></a>
#### 4. Compor recursos e recuperar uma resposta fora do fluxo

Quando a tarefa atravessa várias etapas, passe adiante somente premissas verificadas. Uma sequência plausível é EDA da fonte, diagnóstico de junção, plano de features e, depois, baseline. A EDA responde se a fonte é compreendida; a análise cruzada pergunta se fontes se ligam sem multiplicação ou vazamento temporal; a skill de features define o que existia no ponto de decisão; o baseline testa uma referência de modelo. Essas etapas não viram uma execução única porque o pedido mencionou quatro skills. Faça um **handoff** curto: objetivo, fontes e versões, grão, chaves, tempo, resultados observados, lacunas, restrições, estado das aprovações e pergunta da próxima etapa. O Concierge pode sugerir essa composição, mas sua rota termina na recomendação; [MU03](MU-parte-i.md#mu03) ensina a ler cobertura e confiança da busca.

Considere uma resposta que afirma “a EDA está concluída” e cita `quick_profile`, mas não mostra chamada, resultado nem postflight. Primeiro peça o registro da rota executada e o estado de conclusão. Se o helper só apareceu no texto, classifique-o como citado; se foi importado, não presuma que foi chamado. Se não existe evidência de execução, aproveite as perguntas e o plano como rascunho, mas não use os números como resultado validado. Na EDA L4, peça a finalização canônica ou a declaração explícita de que ela não terminou. Em uma skill L0, confira as fontes, o código e os resultados pelos meios disponíveis, sem fabricar um Receipt obrigatório que a policy ainda não implementa.

Quando uma resposta usa uma skill diferente da pretendida, verifique primeiro o pedido e o objeto anexado. “Explique este erro” sem a mensagem de erro pode não oferecer contexto suficiente; acrescente o trecho real e selecione `@hub-ml-tutor-databricks` se essa é a tarefa. Se a seleção ocorreu e a resposta ignorou o escopo, aponte a seção pertinente do `SKILL.md`, diga o que faltou e peça uma correção delimitada. Se houve escrita ou execução fora do plano, registre o efeito e revise o artefato produzido antes de continuar. A [skill de auditoria](../../skills/hub-ml-auditoria-skills/SKILL.md) separa revisão da implementação de revisão do output e pode ajudar quando o desvio for material.

Uma última conferência de aprendizado cabe antes do próximo capítulo: você consegue dizer **qual skill foi selecionada**, **qual versão ou arquivo foi lido**, **o que executou**, **que gate passou** e **o que ainda depende de revisão**? Se uma resposta é desconhecida, escreva a lacuna no handoff. Para transformar a próxima tarefa em um pedido preenchível, siga [MU05](#mu05); para entender como policy e evidência são construídas, continue no [capítulo técnico de execução verificável](MT-parte-iv.md#mt19).

<!-- editorial:exclude:start -->
Fontes principais: [catálogo de skills](../../skills/README.md), [policy vigente](../../hub_padroes/skill_enforcement/policy.json), [guia de policy](../../hub_padroes/skill_enforcement/README.md), [SKILL de EDA](../../skills/hub-ml-eda-profissional/SKILL.md), [SKILL do Concierge](../../skills/hub-ml-concierge/SKILL.md), [ADR-0021](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0021-execucao-verificavel-de-skills.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU03](MU-parte-i.md#mu03) · [Próximo: MU05](#mu05) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT19](MT-parte-iv.md#mt19)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu05"></a>
<a id="mu05"></a>
### MU05 — Escolher e preencher os 18 briefings

**Pergunta deste capítulo:** qual formulário usar e como preencher o que falta sem inventar dados? Um briefing transforma uma intenção em pedido verificável. Comece pela decisão que precisa tomar; escolha o formulário e confira o que a resposta realmente fez.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](MU-indice.md#sumario-mu) · [Usar skills](#mu04) · [Prompts no Manual Técnico](MT-parte-iii.md#mt12) · [Próxima tarefa](#mu06)
<!-- editorial:exclude:end -->

<a id="mu05-1"></a>
#### 1. Registrar objetivo, fonte, grão, chaves, tempo e desconhecidos

Antes de copiar um texto, escreva qual decisão você espera apoiar. “Fazer análise exploratória de dados (EDA)” é uma atividade: examinar estrutura, qualidade e distribuições de uma fonte antes de decidir o próximo estudo. O [briefing de EDA rápida](../../hub_prompts/eda_rapida/README.md) mostra um primeiro recorte; já a formulação “decidir se a tabela de clientes pode sustentar um estudo de churn” delimita o resultado. Diga quem usará a resposta e qual artefato ajudará: diagnóstico, reconciliação, plano, código ou relatório. O [índice dos prompts](../../hub_prompts/README.md) ajuda a escolher entre os 18 briefings manuais desta versão. Cada pasta contém um README que explica adequação e limites, um `.md` com campos para preencher e um `exemplo_*.py` que apresenta um cenário. O briefing não é uma skill descoberta automaticamente; depois de preenchê-lo, você o envia ao Genie Code e, se quiser, seleciona uma skill pertinente com `@`.

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

Use [auditoria_skills](../../hub_prompts/auditoria_skills/README.md) quando quiser saber se uma skill foi construída conforme seu contrato ou se um output produzido com ela merece confiança. Escolha o objeto **IMPLEMENTAÇÃO** ou **OUTPUT** e, separadamente, a ação **AUDITORIA**, **PLANO DE CORREÇÃO** ou **CORRIGIR AUTORIZADO** no [briefing](../../hub_prompts/auditoria_skills/auditoria_skills.md); identifique a skill alvo e anexe `SKILL.md`, contrato, código, pedido e resposta conforme o modo. Peça requisito, evidência, lacuna e gravidade por achado. Um relatório de auditoria sem artefato lido deve dizer o que ficou não observável. A recomendação de `@hub-ml-auditoria-skills` não executa o auditor automaticamente; confira seleção e trilha de evidência. Não transforme um checklist preenchido em aprovação de comportamento no Databricks.

<a id="mu05-route-comentar-notebook"></a>
##### `comentar_notebook` — documentar código existente

Escolha [comentar_notebook](../../hub_prompts/comentar_notebook/README.md) quando um notebook precisa ficar compreensível para outra pessoa. No [formulário](../../hub_prompts/comentar_notebook/comentar_notebook.md), indique notebook ou células, público, profundidade e modo **REVISÃO**, **EDIÇÃO** ou **DOCUMENTAÇÃO**. Diga quais células e resultados devem permanecer intocados e se há dados sensíveis nos outputs. Peça explicações antes do código e interpretação depois dele, sem inferir que um comentário prova reexecução. Se você só quer sugestões, mantenha o modo de revisão; se autoriza edição documental, confira o diff e a preservação do código e da ordem das células. A rota de skill recomendada é `@hub-ml-comentar-notebook`. Uma entrega clara identifica também as células que não foram examinadas.

<a id="mu05-route-cross-eda"></a>
##### `cross_eda` — avaliar fontes em conjunto

Use [cross_eda](../../hub_prompts/cross_eda/README.md) para decidir se duas ou mais fontes podem alimentar uma análise ou modelo. No [pedido](../../hub_prompts/cross_eda/cross_eda.md), informe entidade, grão de cada tabela, chaves, período, target, horizonte e ponto de decisão; anexe EDAs anteriores quando existirem. Peça cardinalidade e cobertura de junção, perdas, multiplicação de linhas e disponibilidade histórica das colunas. Timestamp de evento não garante que o valor estava disponível antes do cutoff. Sem prova temporal, a resposta deve propor teste e declarar prontidão pendente, mesmo que a cobertura de join seja alta. A skill sugerida é `@hub-ml-cross-eda-ml`. Registre a população que ficou sem correspondência após a junção.

<a id="mu05-route-data-quality"></a>
##### `data_quality` — transformar suspeitas em regras

Escolha [data_quality](../../hub_prompts/data_quality/README.md) se a decisão depende de completude, unicidade, validade, consistência, integridade, atualidade ou volume. O [briefing](../../hub_prompts/data_quality/data_quality.md) pede fonte, grão, chaves, colunas temporais, período, consumidor downstream e regras conhecidas. Para cada regra, peça numerador, denominador, origem do limiar e população afetada. Uma taxa de nulos não determina sozinha se a tabela serve ao negócio. Solicite scorecard e plano de investigação; não trate o pedido como deploy de expectations ou correção automática dos dados. A rota recomendada usa `@hub-ml-eda-profissional` e seus gates vigentes quando selecionada. Peça prioridade de investigação conforme o impacto no uso declarado.

<a id="mu05-route-eda-completa"></a>
##### `eda_completa` — aprofundar uma fonte

Use [eda_completa](../../hub_prompts/eda_completa/README.md) quando o perfil inicial já mostrou perguntas que exigem distribuições, recortes, relações e gráficos. No [formulário](../../hub_prompts/eda_completa/eda_completa.md), declare fonte, pergunta de negócio, grão, chave, coluna temporal, período, volume, foco, restrições e target somente quando existir. Peça achados separados de hipóteses, gráficos que respeitem o tamanho da base e um backlog de verificações. Correlação ou diferença por segmento não estabelece causa; ausência de problema na amostra não certifica a população. A skill sugerida é `@hub-ml-eda-profissional`; se for selecionada para execução completa, confira a rota L4 descrita em [MU04](#mu04). Solicite a origem e a população de cada gráfico apresentado.

<a id="mu05-route-explainability"></a>
##### `explainability` — explicar um modelo identificado

Escolha [explainability](../../hub_prompts/explainability/README.md) para compreender o comportamento de uma versão específica de modelo. Preencha no [pedido](../../hub_prompts/explainability/explainability.md) o modelo/run, dataset e split, período, target e classe, público, método pretendido ou critério de escolha e tamanho de amostra. Diferencie explicação global da explicação de um caso. Peça limites, estabilidade e possível vazamento antes de comunicar drivers. [SHAP](https://shap.readthedocs.io/en/latest/index.html) (*SHapley Additive exPlanations*) é um método que atribui contribuições das variáveis à saída do modelo. Nem importância de variável nem valor SHAP demonstram causa do desfecho; uma explicação de outra versão não responde à pergunta. `@hub-ml-explainability` é a skill sugerida, sem implicar cálculo já executado ou registro no MLflow. Confira se a população explicada corresponde à pergunta inicial.

<a id="mu05-route-feature-engineering"></a>
##### `feature_engineering` — desenhar atributos no tempo

Use [feature_engineering](../../hub_prompts/feature_engineering/README.md) quando já sabe entidade, target e momento da decisão. O [briefing](../../hub_prompts/feature_engineering/feature_engineering.md) pede chave, janela de observação, cutoff, horizonte, fontes, junções, frequência e restrições de materialização. Peça especificação por feature, teste de disponibilidade e risco de vazamento entre treino e inferência. Se a data em que o fato ocorreu difere da data em que chegou ao sistema, ambas importam. Sem janela ou cutoff definidos, receba um plano de descoberta, não código que presume causalidade temporal. A skill sugerida é `@hub-ml-feature-engineering`; o formulário não cria tabela de features. Registre quais fontes ainda exigem validação de acesso.

<a id="mu05-route-monitoramento-modelo"></a>
##### `monitoramento_modelo` — investigar mudança operacional

Escolha [monitoramento_modelo](../../hub_prompts/monitoramento_modelo/README.md) para distinguir falha de serviço, mudança de população, drift e queda de performance. Identifique no [pedido](../../hub_prompts/monitoramento_modelo/monitoramento_modelo.md) modelo/run, endpoint ou job, referência, janela atual, atraso de maturação do rótulo, métricas, direção desejada, segmentos e responsáveis. Peça limites de comparação e ações condicionais. O [Population Stability Index (PSI)](../../hub_snippets/spark/psi_calculator/README.md) resume quanto a distribuição de uma variável mudou entre referência e população atual. Um alerta de PSI não demonstra deterioração de performance; sem rótulo maduro, uma taxa de acerto aparente pode ser enganosa. A skill sugerida é `@hub-ml-monitoramento-modelo`. O briefing não instala monitor, agenda job ou autoriza retreino. Peça as proporções por faixa e confira população de referência, volume e limiares definidos no contexto antes de propor uma ação.

<a id="mu05-route-micromodelo-novo"></a>
##### `micromodelo_novo` — especificar um objetivo conhecido

Use [micromodelo_novo](../../hub_prompts/micromodelo_novo/README.md) com `@hub-ml-micromodelos` no modo `OBJETIVO_CONHECIDO`. Informe decisão, característica, entidade/grão, população, horizonte, fontes, dono e restrições. O [formulário](../../hub_prompts/micromodelo_novo/micromodelo_novo.md) pede proveniência e um plano de estudo. Só peça `micromodelo.yaml` quando template e schema MM01 estiverem acessíveis; sem eles, aceite checklist textual, `YAML_NAO_CRIADO` e `MM01_NAO_VALIDADO`. Informação fornecida no pedido não vira observação de catálogo. Ausência de evidência continua indeterminada, e um score heurístico não é probabilidade calibrada.

<a id="mu05-route-descobrir-micromodelos"></a>
##### `descobrir_micromodelos` — explorar oportunidades delimitadas

Escolha [descobrir_micromodelos](../../hub_prompts/descobrir_micromodelos/README.md) quando a decisão está clara, mas a característica ainda não foi escolhida. No [briefing](../../hub_prompts/descobrir_micromodelos/descobrir_micromodelos.md), delimite área, população, catálogo autorizado ou fixture textual, restrições e critérios qualitativos. A skill produz candidatas para revisão, com cobertura e incerteza; não consulta registros por associação. Metadados fornecidos recebem `FORNECIDA`; nomes e tipos não comprovam viabilidade ou ausência de vazamento. Escolha humana precede o início do YAML. A skill permanece L1/audit, e o prompt não possui nível ou autorização próprios.

<a id="mu05-3"></a>
#### 3. Preencher, enviar e acompanhar os exemplos

As oito rotas seguintes incluem três pedidos copiáveis. Os nomes de tabela, modelo e notebook são fictícios; cada bloco pede plano ou orientação e não relata execução.

<a id="mu05-route-eda-rapida"></a>
##### `eda_rapida` — primeiro perfil de uma tabela

Use [eda_rapida](../../hub_prompts/eda_rapida/README.md) quando recebeu uma fonte nova e precisa decidir o que investigar primeiro. O [briefing](../../hub_prompts/eda_rapida/eda_rapida.md) pede tabela, objetivo, foco, chave e coluna temporal candidatas, filtros, período e limite de custo. No exemplo abaixo, `id_cliente` é apenas candidata: solicite teste de unicidade antes de chamá-la de chave. O período evita misturar fotografias diferentes; o modo “plano” impede tratar sugestão de consulta como resultado. Peça até oito achados priorizados com evidência e limite de amostragem. A skill recomendada é `@hub-ml-eda-profissional`, cujo fechamento de execução segue [MU04](#mu04). Confirme quais colunas ficaram fora do perfil inicial.

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

Use [comparar_tabelas](../../hub_prompts/comparar_tabelas/README.md) para investigar diferença entre versões de uma tabela, implementações ou populações. No [formulário](../../hub_prompts/comparar_tabelas/comparar_tabelas.md), identifique A/B, grão e chaves de cada lado, período, fuso, filtros, tolerâncias e foco: schema, contagem, chaves ou valores. O exemplo declara a tolerância desconhecida para não inventar um veredito. Peça matriz de schema, scorecard e amostras de divergências com denominadores, além de cardinalidade do join. Mesmo schema não prova semântica ou população iguais. Defina antes se é reconciliação determinística independente ou execução de EDA, cross-EDA ou monitoramento. SQL/PySpark direto não substitui o runner de uma EDA protegida já selecionada; “somente leitura” requer conferência dos efeitos reais. Registre divergências que exigem decisão humana antes do veredito.

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

Use [baseline_orchestration](../../hub_prompts/baseline_orchestration/README.md) para desenhar o primeiro modelo comparável antes de otimizar. O [briefing](../../hub_prompts/baseline_orchestration/baseline_orchestration.md) precisa de entidade, grão, target/evento positivo, momento de observação, maturação do rótulo, cutoff, horizonte, split, métrica, custo e modo. No exemplo, a maturação desconhecida impede treinar com segurança; peça primeiro a regra e uma divisão sem vazamento. Um baseline ingênuo ajuda a interpretar ganho, mas não prova valor de negócio. `@hub-ml-baseline-ml` orienta a rota atual da policy; o pedido não treina nem registra run automaticamente. Compare desempenho por período e segmento antes de escolher alternativa para investigação.

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

Use [novo_projeto](../../hub_prompts/novo_projeto/README.md) quando ainda precisa transformar uma demanda ampla em charter e backlog. No [briefing](../../hub_prompts/novo_projeto/novo_projeto.md), preencha nome estável, problema, decisão, donos, critérios de aceite, métricas, fontes, ambientes, repositório, entregáveis e modo de trabalho. Peça riscos e dependências antes de gerar recursos. Uma fonte mencionada ainda precisa de permissão e validação; não coloque tokens ou caminhos corporativos no pedido compartilhável. O Genie Code pode organizar perguntas sem uma skill específica. Separar desenho de criação efetiva evita que um charter seja relatado como projeto implantado. Confirme quem aprovará a próxima fase do projeto.

<a id="mu05-route-pipeline"></a>
##### `pipeline` — planejar fluxo de dados

Escolha [pipeline](../../hub_prompts/pipeline/README.md) quando a decisão é como transformar e entregar dados repetidamente. O [formulário](../../hub_prompts/pipeline/pipeline.md) pede fontes, destinos, consumidores, batch ou streaming, cadência, chaves, schema, qualidade, objetivo de serviço, ambientes, reprocessamento e idempotência. Peça um plano por etapa e testes para repetição sem duplicar ou perder registros. Uma meta de latência não é prova de que o job a cumprirá. `@hub-ml-pipeline-builder` pode orientar o método; texto YAML ou código sugerido não publica Lakeflow, não cria job e não confirma permissão de escrita no destino. Defina responsável por falhas, alertas e reprocessamento.

<a id="mu05-route-safra"></a>
##### `safra` — comparar coortes com maturidade igual

Use [safra](../../hub_prompts/safra/README.md) para comparar grupos formados em meses ou eventos diferentes. O [briefing](../../hub_prompts/safra/safra.md) exige entidade, chave, data de coorte, idade da coorte, evento, numerador, denominador, métrica, censura e período observado. Peça uma curva por idade comparável, marque células que ainda não amadureceram e separe efeito de calendário de diferença entre coortes. Uma célula imatura não é zero; taxas cumulativas não devem ser somadas. `@hub-ml-analise-safra` é a skill sugerida. O prompt não calcula uma safra sozinho nem valida regra regulatória sem fonte própria. Compare somente idades de coorte efetivamente observadas em ambos os grupos.

<a id="mu05-route-stat-check"></a>
##### `stat_check` — testar uma hipótese delimitada

Escolha [stat_check](../../hub_prompts/stat_check/README.md) quando uma diferença observada precisa ser avaliada com pressupostos, efeito e incerteza. O [pedido](../../hub_prompts/stat_check/stat_check.md) deve dizer pergunta/estimando, dataset, grão, grupos, target, amostra ou população, tempo, método pretendido ou critério de escolha, hipóteses e nível de decisão. Solicite diagnóstico de dependência temporal e multiplicidade antes de interpretar um p-valor. Significância estatística não equivale a tamanho de efeito útil nem a causalidade. `@hub-ml-validacao-estatistica` é a rota sugerida; sem dados examinados, a resposta só pode oferecer plano de teste. Peça também intervalo de incerteza e alternativa metodológica se os pressupostos falharem.

<a id="mu05-route-tutor-explicar"></a>
##### `tutor_explicar` — aprender com objeto real

Use [tutor_explicar](../../hub_prompts/tutor_explicar/README.md) quando quer entender código, erro ou conceito aplicado à sua tarefa. Anexe no [briefing](../../hub_prompts/tutor_explicar/tutor_explicar.md) o objeto ou a pergunta concreta; informe nível iniciante, intermediário ou avançado, profundidade, objetivo, ambiente e restrições. Peça que o assistente separe o que leu no arquivo do que inferiu sobre runtime. Uma analogia ajuda a aprender, mas deve declarar onde deixa de descrever o mecanismo. `@hub-ml-tutor-databricks` é a skill sugerida. A explicação não comprova execução ou correção do código não examinado. Uma pergunta de retorno aplicada ao mesmo objeto pode testar sua compreensão.

Depois de escolher o briefing, abra seu `exemplo_*.py` como **documento de ensino**. A Parte 1 pode preparar dados e executar células; confira destino antes de rodar, pois 13 dos 18 exemplos atuais usam `mode("overwrite")` em tabelas sintéticas. A Parte 2 mostra um pedido preenchido para copiar e adaptar manualmente ao chat. A Parte 3 reserva espaço para a resposta obtida e revisada: nos 16 exemplos anteriores, ela ainda diz `NÃO EXECUTADO`. Os dois novos exemplos de Micromodelos têm preparo textual local E0, sem tabela, e registros de conversa E1 no Free de 29/09/2026. Essas conversas não demonstram runtime E1, consulta de catálogo ou validação MM01. No objetivo conhecido, a resposta chamou dados fornecidos de observados; na descoberta, usou “viáveis” para hipóteses ainda indeterminadas e criou células apesar do pedido de resposta no chat. Preserve essas ressalvas ao estudar o caso. A marca pendente não é falha a ocultar; evita apresentar uma conversa que nunca ocorreu como evidência de Genie Code. A conversa datada, por sua vez, não transfere aprovação aos demais exemplos. Anote data, fonte, modo, seleção da skill e efeito observado se um dia registrar uma resposta real.

<a id="mu05-4"></a>
#### 4. Conferir a resposta e corrigir lacunas

Depois de enviar o briefing, compare a resposta com o **pedido que você realmente enviou**, não com a intenção que ficou na sua cabeça. Ela identificou fonte, grão, período e modo? Separou dado observado de hipótese? Explicou denominadores, filtros e unidades antes de apresentar taxas? Indicou quais arquivos, tabelas e versões foram lidos? Se prometeu código, existe entrada, dependências, saída esperada e aviso de efeitos? Uma resposta elegante pode falhar nesses pontos. No [índice dos prompts](../../hub_prompts/README.md), cada formulário traz o que conferir; use esse checklist como começo, adaptado à sua decisão.

No exemplo de EDA rápida, a entrega correta para o pedido **em modo plano** descreve verificações de grão, chave, data desconhecida, custo e prioridades. Não deve apresentar porcentagem de nulos calculada nem dizer que a tabela está aprovada sem leitura e execução. Se aparecer “nenhuma duplicata” sem consulta observada, marque o número como não verificado e peça a consulta ou evidência correspondente. Se a skill de EDA foi selecionada e uma execução completa ocorreu, confira também os gates atuais explicados em [MU04](#mu04); mencionar a skill não prova postflight aprovado.

Na comparação A/B, uma diferença de contagem só é interpretável quando as duas populações usam período, fuso e filtros compatíveis. Peça as contagens antes e depois da junção, número de chaves sem par e multiplicação por cardinalidade. Se a tolerância estava `NÃO INFORMADO`, o assistente pode mostrar diferenças, mas não inventar um limite para declarar equivalência. Corrija o briefing com a regra decidida pelo responsável e peça nova avaliação apenas do veredito afetado. Essa sequência mantém a primeira resposta como diagnóstico, não a apaga nem a chama de reconciliação aceita.

No baseline, leia o plano na ordem temporal: momento de observação, chegada de cada atributo, maturação do rótulo, corte entre treino e teste e métrica. Se a maturação continuou desconhecida, um split sugerido é hipótese de desenho, não treino autorizado. Peça primeiro a origem da regra do rótulo; depois revise o split e só então decida sobre execução e tracking. Uma métrica sem população e janela não basta para escolher modelo. O [briefing de baseline](../../hub_prompts/baseline_orchestration/baseline_orchestration.md) ajuda a localizar os campos que ficaram sem resposta.

Quando faltar informação, faça um **follow-up delimitado**. Cite o campo, a frase problemática e o efeito: “Você assumiu `id_cliente` como chave; no pedido ela era candidata. Mostre como testar unicidade sem escrever tabela e revise apenas o diagnóstico de duplicidade”. Para corrigir modo: “Pedi plano; identifique quais comandos foram apenas sugeridos e se algo foi executado”. Para corrigir acesso: “Marque como não observável o que não pôde ler e dê o caminho tentado”. Essas perguntas produzem uma revisão verificável; “refaça tudo” perde o rastro das premissas.

Registre no notebook de exemplo a resposta real somente após obtê-la, revisar efeitos e indicar ambiente e data. Preserve `NÃO EXECUTADO` na Parte 3 enquanto não houve conversa ou execução correspondente. A Parte 1 que prepara dados sintéticos pode ter escrito uma tabela mesmo que a Parte 3 continue vazia; relate esses eventos separadamente. Os 13 exemplos com `overwrite` exigem conferir destino antes de rodar, inclusive em um ambiente de testes. Se a resposta não seguiu o modo ou a skill escolhida, corrija o pedido e o estado da evidência antes de avançar. Para a próxima ação com uma função isolada, siga [MU06](#mu06); para o contrato técnico dos briefings, consulte [MT12](MT-parte-iii.md#mt12).


<!-- editorial:exclude:start -->
[Anterior: MU04](#mu04) · [Próximo: MU06](#mu06) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT12](MT-parte-iii.md#mt12)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu06"></a>
<a id="mu06"></a>
### MU06 — Usar um snippet isoladamente

**Pergunta deste capítulo:** como chamar uma função do Hub diretamente e saber se ela responde à pergunta certa? Você precisa localizar a cópia autorizada de `.assistant`, conseguir executar Python e conhecer a unidade do dado de entrada. Para a receita Spark, também precisa de uma sessão e de um DataFrame PySpark. Pode seguir a primeira receita diretamente no notebook. Se a tarefa já estiver sob uma skill com rota protegida, uma chamada isolada não substitui seus gates.

<!-- editorial:exclude:start -->
[Sumário do Manual do Usuário](MU-indice.md#sumario-mu) · [Primeiro uso](MU-parte-i.md#mu02) · [Scripts isolados](#mu07) · [Fundamentos técnicos dos snippets](MT-parte-ii.md#mt05)
<!-- editorial:exclude:end -->

<a id="mu06-1"></a>
#### 1. Escolher a função e ler seus requisitos

Imagine que você já calculou uma taxa de resposta e só quer mostrá-la em português no relatório. Abrir uma skill inteira para essa apresentação seria uma etapa adicional desnecessária: um snippet é uma função ou classe reutilizável que você chama no seu próprio código. A escolha começa pela **pergunta**, não pela semelhança do nome. Para exibir uma taxa já calculada, procure `format_br`; para descobrir quantos valores `NULL` existem em cada coluna de um DataFrame Spark, procure `null_summary`. Uma função que produz um texto não resolve uma dúvida de qualidade dos dados, e um resumo de nulos não calcula uma taxa de resposta.

Comece pelo [catálogo de snippets](../../hub_snippets/README.md), escolha a categoria e abra o README da pasta do objeto. Cada pasta operacional aproxima quatro peças com usos distintos: o README ajuda a decidir; `__init__.py` mostra os nomes que podem ser importados pela interface pública; o arquivo da implementação define a assinatura e o comportamento; `exemplo_*.py` demonstra uma situação com dados sintéticos. Leia a seção “quando usar” junto com “quando não usar”. Isso impede que uma saída atraente seja tratada como resposta a uma pergunta que a função nunca recebeu.

No [README de `format_br`](../../hub_snippets/constants/format_br/README.md), o quadro inicial diz que as seis funções recebem valores escalares e entregam **strings**, isto é, textos. Ele alerta que o cálculo deve estar pronto e que o texto não deve substituir o número quando ainda haverá soma ou comparação. A palavra “percentual” exige uma decisão prévia: `0.12` pode significar uma taxa de 12% escrita como fração; `12` pode significar os mesmos 12% já expressos na escala percentual. O formatador não adivinha qual convenção a sua base usa. Anote a escala ao lado do nome da variável antes de escolher `fmt_pct`.

No [README de `null_summary`](../../hub_snippets/spark/null_summary/README.md), os requisitos são diferentes: um **DataFrame PySpark** já disponível e limiares percentuais coerentes. DataFrame é uma tabela manipulada pelo código; PySpark é a interface Python para operações Spark distribuídas. Aqui, “nulo” quer dizer o `NULL` reconhecido por `isNull()`. String vazia, `"N/A"` e códigos sentinela não são contados automaticamente como ausência. A função devolve uma tabela de contagens e um semáforo escolhido pelos limiares, não um parecer geral sobre a qualidade da base. Se você precisa verificar duplicidade, recência e regras de domínio, escolha uma checagem mais ampla e consulte o capítulo de scripts.

Antes de continuar, formule uma frase verificável: “vou mostrar a taxa como texto, preservando o número original” ou “vou contar `NULL` na população completa e comparar com limiares que registrei”. Se você não consegue dizer qual população, unidade ou saída espera, a chamada pode executar corretamente e ainda assim responder à pergunta errada. O README local permite parar cedo e corrigir a escolha.

<a id="mu06-2"></a>
#### 2. Preparar o import e fazer uma chamada pequena

O caminho de arquivo e o caminho de importação têm papéis diferentes. A implementação de `fmt_pct` está em `hub_snippets/constants/format_br/format_br.py`; o import público é `hub_snippets.constants.format_br`. Os pontos são partes do nome de pacotes Python. A pasta que o Python precisa enxergar é **a que contém** `hub_snippets`, normalmente a `.assistant` da entrega. Uma tabela chamada `catalogo.esquema.tabela` usa pontos por outro motivo e não entra em `sys.path`. O [manual técnico vigente](../../MANUAL_TECNICO_V2.md#importacao) desenvolve essa distinção, caso você queira entender a busca de módulos.

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

Substitua `<username>` pela localização autorizada do seu Hub; a pasta pode estar em um Git folder ou outro endereço, conforme sua distribuição. `Path(...)` representa o endereço, não cria a pasta. `sys.path.insert` só altera a busca do interpretador da sessão: não instala pacotes e não concede acesso. A linha `from ... import fmt_pct` chega à [fachada pública](../../hub_snippets/constants/format_br/__init__.py), que reexporta a função implementada em `format_br.py`. Como o helper de formatação usa bibliotecas padrão do Python, o exemplo simples não requer Spark. O **notebook de exemplo** da pasta usa Spark para descobrir o usuário da sessão; essa necessidade pertence ao preparo daquele notebook, não à função `fmt_pct`.

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

O [código de `null_summary`](../../hub_snippets/spark/null_summary/null_summary.py) retorna um DataFrame Spark com `coluna`, `count_null`, `pct_null` e `status`, ordenado pela porcentagem decrescente. A interpretação exige ler as quatro colunas juntas. Se uma coluna tiver 13 `NULL` em 500 linhas, `100 × 13 / 500 = 2,6%`. Com aviso a 5% e falha a 20%, o status é verde; com aviso a 1% e falha a 10%, o mesmo dado é amarelo. O [notebook sintético do objeto](../../hub_snippets/spark/null_summary/exemplo_null_summary.py) registra exatamente essa comparação como resultado histórico de laboratório. Os números aqui ilustram o contrato e não afirmam que o notebook foi reexecutado no seu destino.

Para verificar uma base pequena sob seu controle, crie algumas linhas fictícias com uma coluna contendo `None`, chame a função e compare a contagem com o que você enxerga. Se preferir a fixture do Hub, leia antes sua [implementação](../../hub_snippets/testing/fixtures/fixtures.py): porcentagem configurada para geração aleatória é probabilidade por linha, não garantia de número exato de nulos. Registre tamanho da população e limiares junto ao resumo, porque o DataFrame retornado não contém esses dois thresholds como campos. Se você filtrar a base antes da função, estará medindo o recorte; isso pode ser desejado, mas deve aparecer no título da análise.

O semáforo responde apenas “qual percentual de `NULL` está acima dos limiares informados?”. Ele não sabe se a coluna deve ser obrigatória. Em uma coluna `data_cancelamento`, `NULL` pode representar uma pessoa ainda ativa, e verde ou vermelho não decide o tratamento correto. Da mesma forma, 30% de strings `"N/A"` podem conviver com zero `NULL` e aparecer verdes. Se o problema é ausência semântica, defina antes quais representações contam como ausentes e prepare uma checagem específica. Ao filtrar o resultado, compare `status` com os emojis reais; um filtro por texto `"ok"` não corresponde à saída e pode selecionar linhas inesperadas.

Um terceiro exemplo mostra por que nem todo snippet cabe numa chamada tão curta. O [helper temporal `pit_join`](../../hub_snippets/spark/pit_join/README.md) relaciona decisões com versões históricas que já estavam disponíveis em cada instante. Ele recebe fatos, histórico, chaves, colunas de tempo e um atraso de publicação obrigatório; devolve **um DataFrame e um dicionário de diagnóstico**. Se uma decisão fictícia ocorreu em 12/01/2026, uma versão de 08/01 com atraso de três dias já estava disponível em 11/01; uma versão de 11/01 só ficaria disponível em 14/01. Essa comparação pode ser refeita à mão antes de examinar uma saída Spark. Abra o README e o notebook específicos antes de usá-lo e siga o percurso de cruzamento temporal do manual. Uma tabela que só guarda o valor atual não reconstrói magicamente as versões passadas.

O teste pequeno deve reproduzir o **risco principal** de cada função: escala para formatação, denominador e representação de ausentes para nulidade, versão futura para junção temporal. Só depois passe a uma amostra representativa e confira schema, unidade, linhas e custos. Uma saída com formato correto e sem exceção ainda pode responder a uma população errada, uma data errada ou uma definição errada de ausência.

<a id="mu06-4"></a>
#### 4. Resolver falhas e escolher uma alternativa proporcional

Quando surgir `ModuleNotFoundError: No module named 'hub_snippets'`, examine primeiro a raiz inserida no `sys.path`: ela deve conter a pasta `hub_snippets`. Confirme que a cópia do Hub foi disponibilizada como arquivos acessíveis à sessão, que o nome da pasta está correto e que o caminho não aponta apenas para o notebook de exemplo. Um `PermissionError` pede verificação de acesso, não uma troca arbitrária de import. Se o erro nomeia uma dependência como `pyspark`, verifique o ambiente e a política de instalação aplicável; editar `sys.path` não instala essa dependência. Retome a chamada pequena depois de corrigir uma causa por vez.

Erros de argumento e erros silenciosos requerem tratamento diferente. Em `fmt_pct`, um `input_scale` fora de `"ratio"` e `"percent"` levanta `ValueError`; uma escala válida mas errada para o dado produz texto enganoso sem falhar. Em `null_summary`, os thresholds são aceitos sem conferir a faixa ou a ordem. Antes de automatizar, valide `0 <= threshold_warn <= threshold_fail <= 100`, trate uma base vazia separadamente e registre o que fazer quando a política não estiver definida. A implementação pode falhar ao converter agregados nulos em inteiros numa base sem linhas. Não transforme ausência em zero só para manter o fluxo em movimento.

Custo também faz parte da escolha. `fmt_pct` opera sobre um escalar no processo Python; não é uma instrução para formatar milhões de linhas Spark uma a uma no driver. `null_summary` dispara uma contagem da tabela e uma agregação que coleta uma **linha de resultados agregados** no processo Python; em tabela larga, o número de expressões acompanha o número de colunas. `pit_join` pode exigir uma junção por intervalo com muitos candidatos e contagens diagnósticas. No notebook, veja o plano de execução e teste volume adequado ao ambiente antes de inserir qualquer uma dessas chamadas num job recorrente.

Escolha uma alternativa quando a pergunta mudou. Para apenas exibir um valor isolado, a formatação nativa do Python pode bastar; para uma pequena tabela pandas apresentada ao leitor, veja `display.dataframe_styled`. Para conhecer uma tabela por várias dimensões, [quick_profile](../../hub_scripts/quick_profile/README.md) ou [data_quality_check](../../hub_scripts/data_quality_check/README.md) oferecem contratos mais amplos que `null_summary`, mas exigem outros preparos. Para dados sem versões temporais, uma junção comum pode bastar; com versões, especifique disponibilidade histórica antes de escolher `pit_join` ou outra solução. A semelhança de nomes não torna os retornos equivalentes.

Antes de encerrar, responda sem olhar o código: qual pergunta sua chamada respondeu, em qual população, com qual unidade e qual saída você verificou? Se a resposta envolver uma política de limiar, anote-a com o resultado. Se envolver tempo, anote instante de decisão, referência, atraso e fuso. Essa pequena conferência permite repetir a análise e ajuda outra pessoa a decidir se a função isolada bastou ou se precisa de um fluxo maior. O próximo capítulo mostra como usar um script direto quando a tarefa pede um diagnóstico ou transformação mais abrangente.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu06-h-fontes-e-estado-dos-exemplos"></a>
##### Fontes e estado dos exemplos

- Fontes de comportamento do Hub: [coleção](../../hub_snippets/README.md), [implementação de `format_br`](../../hub_snippets/constants/format_br/format_br.py), [README de `format_br`](../../hub_snippets/constants/format_br/README.md), [implementação de `null_summary`](../../hub_snippets/spark/null_summary/null_summary.py), [README de `null_summary`](../../hub_snippets/spark/null_summary/README.md), [README de `pit_join`](../../hub_snippets/spark/pit_join/README.md).
- Fontes oficiais de plataforma reconferidas em 7/10/2026: [arquivos do workspace](https://learn.microsoft.com/en-us/azure/databricks/files/workspace) e [dependências do notebook serverless no Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies). O comportamento das funções customizadas vem do código do Hub.
- Os blocos copiáveis e os resultados calculados em prosa são **ILUSTRATIVOS** nesta edição. Não houve execução no workspace do leitor; o resultado histórico do notebook de `null_summary` é identificado como tal.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU05](#mu05) · [Próximo: MU07](#mu07) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT05](MT-parte-ii.md#mt05) · [MT07](MT-parte-ii.md#mt07)
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

A escolha também depende da **entrada que você realmente tem**. Os seis primeiros nomes que consultam tabela (`quick_profile`, `data_quality_check`, `drift_detector`, `rfv_calculator`, `schema_to_yaml`, `naming_checker`) precisam de nome legível por Spark e acesso à fonte. `doc_coverage` precisa de caminho de arquivo local, não de URL de notebook no workspace. `skill_execution` precisa de contrato JSON, raiz `.assistant` e contexto objetivo completo. Se falta uma dessas entradas, busque-a antes da chamada; não preencha com um valor conveniente só para obter resposta. O [capítulo técnico dos scripts](MT-parte-ii.md#mt11) explica mecanismos; aqui seguimos a ação do leitor.

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

Esse primeiro comando é curto, mas faz uma contagem e nulos da tabela inteira, além das estatísticas amostrais. Portanto espere custo de leitura mesmo com `sample_fraction=0.10`. Antes de aumentar a fração para “melhorar” a média, veja se `sample_rows` e as colunas cobertas respondem à pergunta. Se você precisa só de uma prévia visual limitada, o snippet `safe_display` (veja o [README do objeto](../../hub_snippets/spark/safe_display/README.md)) resolve outra tarefa; se precisa de contagem integral de uma coluna específica, deixe clara a regra em vez de tomar uma média amostral como resposta completa.

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
[Anterior: MU06](#mu06) · [Próximo: MU08](MU-parte-iii.md#mu08) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT11](MT-parte-ii.md#mt11)
<!-- editorial:exclude:end -->
