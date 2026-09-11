![CRM — Missão Modelos Analíticos CRM](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Ecossistema/Hub `.assistant` para Databricks Genie Code voltado para Machine Learning

Uma demanda como “verifique se podemos usar os eventos da campanha para modelagem” combina contexto de negócio, qualidade dos dados, método analítico e execução de código. Este Hub organiza essas responsabilidades para que a equipe consiga escolher uma ferramenta, compreender suas entradas e revisar o resultado.

> **Versão candidata para revisão.** Ainda não substitui o README oficial. Os links desta versão funcionam na pasta de revisão; a preparação para publicação deve recalculá-los para o destino. Não publicar esta pasta no Databricks.

> **Procedência.** Instruções e Agent Skills utilizam mecanismos documentados da Genie Code. Os conteúdos `hub-ml-*` e as coleções com prefixo `hub_` são implementações deste projeto. Eles não são produtos institucionais da Databricks. Configuração de contexto, execução de código e aprovação de resultados são etapas distintas.

---

<a id="mapa-de-leitura"></a>
## 🧭 Mapa de Leitura

Este guia apresenta a finalidade, os componentes, a arquitetura e a manutenção do repositório. Você aprenderá a reconhecer qual peça atende sua necessidade e onde uma correção deve nascer. Para executar a primeira tarefa, abra o [guia candidato do `.assistant`](../sprint-02-assistant/README.md).

A primeira leitura pode seguir visão geral, componentes, arquitetura e manutenção. Para consulta, escolha pela pergunta:

| Sua pergunta | Próxima seção |
|---|---|
| Que problema o Hub resolve? | [Visão geral](#visao-geral) |
| Preciso de método, briefing, código ou molde? | [Componentes](#componentes) |
| Onde o arquivo é mantido e onde executa? | [Arquitetura](#arquitetura) |
| O que a Genie Code recebe como contexto? | [Contexto](#contexto) |
| Como encaminhar uma correção? | [Manutenção](#manutencao) |

---

<a id="visao-geral"></a>
## 🌟 O que é este Ecossistema e como ele ajuda no Databricks?

O ecossistema reúne instruções, métodos, briefings, módulos Python e padrões de autoria. Ele reduz a necessidade de reconstruir o contexto e reimplementar rotinas em cada conversa. Não substitui permissões, testes, desenho estatístico nem decisão de negócio.

Considere uma campanha fictícia. Cada linha é um evento; `event_id` é a chave candidata, `id_cliente` identifica a entidade, `dt_evento` é a data, `respondeu` é um indicador 0/1 e `valor_gasto` é um valor associado ao evento. Esses nomes são didáticos, não identificadores de uma tabela corporativa. Uma checagem posterior também usa `canal`, com um nulo introduzido de propósito.

A passagem de pedido vago para trabalho revisável tem três momentos. Primeiro, “analise a campanha” deixa dados, grão e restrições indefinidos. Depois, um briefing declara a fonte, o período e a permissão de somente planejar. Finalmente, código autorizado produz números cuja origem e interpretação podem ser verificadas. Um evento de resposta, por si só, não define retenção: a definição dessa variável de negócio ainda precisa ser fornecida.

---

<a id="componentes"></a>
## 🧰 O que tem neste ambiente e como ele ajuda na rotina de trabalho?

A figura separa componentes que orientam a conversa daqueles que oferecem código ou moldes. Observe a forma de uso indicada em cada componente, não apenas sua posição no desenho.

![Cinco componentes do Hub: skills, prompts, snippets, scripts e padrões, separados por responsabilidade.](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/01_mapa_ecossistema.png)

As ligações representam organização. Não são gatilhos que executam todo o conjunto. Na campanha, um briefing pode acompanhar uma skill de exploração; um helper só será executado quando houver uma chamada de código no ambiente que o disponibiliza.

### 🧠 1. Agent Skills (`skills/`)

Você escolhe uma skill quando precisa de um método: por onde começar uma EDA, como investigar um cruzamento ou como estruturar um baseline. Cada pacote contém `SKILL.md`, com descrição de uso, instruções e referências. A plataforma pode carregá-lo por relevância; a seleção com `@` explicita a intenção.

Na campanha, você pode selecionar `@hub-ml-eda-profissional`, fornecer as células com a fixture e pedir apenas o plano. A entrega esperada nessa fase é uma proposta de inspeção, não métricas inventadas. A skill orienta a atuação do agente; não é um módulo Python. Veja os [pedidos e critérios de revisão por skill](../sprint-05-skills/README.md).

### 📦 2. Hub Snippets (`hub_snippets/`)

Você utiliza um snippet para reaproveitar uma implementação: divisão temporal, cálculo de PSI ou formatação de números. Neste projeto, o objeto tem API pública, implementação e notebook de exemplo. A forma de entrada depende da função; não é correto presumir que todo snippet receba um DataFrame.

O código consumidor localiza o pacote, importa a função e chama a API. Para a campanha, `temporal_split` pode organizar períodos de avaliação depois que o problema temporal estiver definido. O retorno precisa ser interpretado conforme seu contrato, e não como uma aprovação automática da análise. O [guia de snippets](../sprint-03-snippets/README.md) explica essa reutilização.

### ⚡ 3. Hub Scripts (`hub_scripts/`)

Os scripts são utilitários com uma tarefa delimitada, frequentemente sobre um recurso identificado por nome ou caminho. Nem todos são diagnósticos: há perfilamento, qualidade, transformação RFV, serialização de schema e inspeção de documentação.

`data_quality_check`, por exemplo, recebe o nome de uma tabela ou view acessível na sessão Spark e devolve `status`, `score`, `thresholds`, `checks` e `alerts`. Ele não interrompe outra tarefa por retornar `fail`. A política consumidora decide o que fazer. `rfv_calculator`, por sua vez, devolve um DataFrame, não um veredito. Compare os [contratos dos sete utilitários](../sprint-04-scripts/README.md).

### 📝 4. Hub Prompts (`hub_prompts/`)

Um prompt do Hub é um briefing que você preenche para formular a demanda. Ele explicita objetivo, recursos, granularidade, período, restrições, entrega e critérios de aceite. A pasta não registra novos comandos na interface.

Na campanha, o briefing informa `event_id` como chave candidata e pede que a unicidade seja verificada. Quando um dado é desconhecido, declara `NÃO INFORMADO`, em vez de inventá-lo. O prompt define o trabalho; a skill pode orientar como realizá-lo. O [guia de prompts](../sprint-06-prompts/README.md) mostra exemplos preenchidos.

### 📐 5. Hub Padrões (`hub_padroes/`)

Um padrão ajuda quem vai criar um objeto novo a manter estrutura, contrato, exemplo e revisão consistentes. Escolha o tipo antes de copiar um molde: README, snippet, script, prompt, skill ou notebook.

O resultado é uma proposta de objeto com responsabilidades explícitas, não uma certificação de sua fórmula. O [guia de padrões](../sprint-08-padroes/README.md) acompanha o exemplar real de taxa de resposta por segmento, sem substituir sua API por uma assinatura imaginada.

A pasta `hub_readmes_visual_assets/` é infraestrutura editorial compartilhada. Não é um sexto componente analítico e não alimenta a conversa apenas por existir. Os diagramas continuam acompanhados de explicação textual.

### A mesma demanda vista por cinco componentes

| Componente | Papel no exemplo |
|---|---|
| Prompt de EDA | Delimitar dados, pergunta e ações permitidas |
| Skill de EDA | Organizar o método e as perguntas faltantes |
| Script de qualidade | Medir regras configuradas quando chamado |
| Snippet temporal | Preparar avaliação temporal, quando aplicável |
| Padrão | Orientar criação de novo objeto, somente se necessário |

---

<a id="arquitetura"></a>
## 🏛️ Arquitetura Completa do Ecossistema

O percurso de um arquivo explica por que ler, publicar e executar são ações diferentes.

![Fonte versionada, workspace, contexto aplicável e rota de execução no runtime.](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/02_arquitetura_ecossistema.png)

A fonte mantém o conteúdo editável; a publicação disponibiliza uma cópia; o runtime executa o código consumidor. A rota em notebook ilustrada é a adotada pelos tutoriais, não um limite de capacidade da Genie Code. O agente também pode executar código por ferramentas autorizadas. Em ambos os casos, o ambiente de execução precisa ter acesso ao pacote e às suas dependências.

### O que este diagrama deixa explícito

Contexto de conversa não é importação. Selecionar o arquivo de um helper permite que o modelo consulte seu conteúdo; não coloca automaticamente a biblioteca no `sys.path` de todo processo Python. Da mesma forma, importar uma função no notebook não injeta sua implementação no contexto do chat.

Para corrigir um helper publicado, altere a implementação correspondente em `ambiente_fonte/`, seu exemplo e os testes pertinentes. Uma edição feita somente na cópia operacional pode ser perdida quando o mesmo arquivo for sobrescrito na publicação seguinte.

### Ciclo de vida do projeto

A próxima figura mostra verificações complementares, não uma aprovação única.

![Etapas de edição, validação, geração do espelho, publicação e conferência, testes, registro e promoção.](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/03_ciclo_de_vida.png)

Uma mudança de explicação exige revisão de conteúdo e links. Uma mudança de algoritmo exige também regressões. Compatibilidade com Spark, permissões e comportamento conversacional precisam de evidência própria no ambiente correspondente. Aprovar uma etapa não permite atribuir sucesso às demais.

---

<a id="contexto"></a>
## 🔄 Como o Contexto chega ao Genie Code?

Contexto é a informação disponível para a tarefa: pedido, histórico, código, recursos selecionados, instruções aplicáveis e skills carregadas. Não existe uma regra geral de leitura integral de qualquer pasta denominada `.assistant`.

### Explicação Passo a Passo

1. No chat, declare a pergunta e o modo pretendido. Para a primeira revisão: “Explique o plano; não execute código nem altere arquivos”.
2. Selecione os recursos reais pelo mecanismo de contexto oferecido na interface. Em uma fixture com view temporária, forneça a célula de criação e o resultado de schema; não presuma que a view seja uma tabela persistente do Unity Catalog.
3. Selecione a skill quando desejar um método específico. Instruções pessoais, de workspace e de arquivos hierárquicos seguem os mecanismos suportados pela plataforma.
4. Revise fontes, grão, filtros, custo, coletas e possíveis efeitos antes de autorizar ferramentas. O modo de aprovação configurado pode permitir ações sem uma nova confirmação a cada chamada.
5. Confira a saída efetiva: tipo, unidade, população e limitações. Código proposto, código executado e resultado aceito são estados distintos.

A documentação oficial confirma a descoberta de `AGENTS.md` e `CLAUDE.md` na hierarquia do arquivo aberto e as exceções de Quick Fix e Autocomplete para instruções. Essas capacidades são da plataforma; os métodos e restrições particulares do Hub são conteúdo local. Consulte as referências de plataforma ao final.

---

<a id="manutencao"></a>
## 🧭 Como o Projeto é Mantido sem Criar Duas Verdades

`ambiente_fonte/` contém a fonte editável do produto. `Novo_Ambiente_Simulado/` é gerado. O workspace é uma cópia operacional. `tools/` contém automação de manutenção e `docs/` registra evidências e decisões operacionais.

### Encontrei um problema: como encaminhar uma correção

| Problema | Onde corrigir | Evidência necessária |
|---|---|---|
| Explicação ou link do produto | README correspondente em `ambiente_fonte/` | Revisão humana e validação de referências |
| Resultado de helper | Implementação, exemplo e regressão | Teste com entrada e saída conhecidas |
| Seleção inadequada de skill | `SKILL.md` e casos de fronteira | Testes positivos, negativos e seleção explícita |
| Arquivo não aparece no workspace | Inventário e publicação autorizada | Conferência remota de existência, tipo e conteúdo |

Não edite o espelho à mão. O [guia de manutenção](../sprint-07-ambiente-fonte/README.md) distingue os dois itens publicados — `.assistant_instructions.md` e `.assistant/` — dos documentos que permanecem apenas no repositório.

### Estado verificável do gate local

O estado de um gate deve ser consultado na execução correspondente ao commit, com saída, ambiente e alcance identificados. Este candidato não declara que executou testes no Databricks nem replica uma aprovação histórica como se fosse atual.

As [evidências de testes do projeto](../../../docs/testes/README.md) e o resultado do CI são as rotas de conferência. Na futura promoção deste README, o mecanismo de validação das contagens deve receber a saída real da árvore promovida. Uma contagem antiga não deve ser ajustada para aparentar aprovação, e uma execução que falhou deve permanecer identificada como falha.

---

## ❓ Perguntas Frequentes (FAQ)

### 1. O que acontece quando eu abro o chat da Genie Code com este ecossistema configurado?

As instruções aplicáveis podem orientar a resposta e uma skill pode ser carregada por relevância ou seleção explícita. As pastas customizadas não são executadas por sua mera presença. Observe a indicação de recursos ou ações oferecida pela interface; uma resposta que parece seguir o método não comprova, sozinha, que determinado `SKILL.md` foi carregado.

### 2. Preciso instalar alguma biblioteca ou configurar o Python para usar os snippets?

O processo que executa a chamada precisa localizar o pacote e ter as dependências da função. Configurar `sys.path` não instala bibliotecas. Algumas dependências são exigidas ao importar; outras, apenas na chamada. O [tutorial de snippets](../sprint-03-snippets/README.md) separa essas falhas e aponta o inventário de dependências.

### 3. Qual é a diferença prática entre Skill, Prompt, Snippet e Script?

Skill orienta o método do agente; prompt delimita o pedido; snippet oferece uma API reutilizável; script resolve uma tarefa delimitada com contrato próprio. Na campanha, você pode formular o briefing, selecionar a skill e autorizar uma chamada de qualidade. Não precisa usar todas as peças em toda tarefa.

### 4. Como o ecossistema ajuda a mitigar leakage e erros analíticos?

Ele torna instante de decisão, disponibilidade dos atributos, períodos e critérios de avaliação explícitos. Não garante ausência de vazamento. Um corte por índices cronologicamente ordenados pode ser válido; o risco está em misturar futuro, entidades ou informações ainda indisponíveis. O helper de períodos é uma implementação reutilizável dessa disciplina, não prova automática de validade de todo o desenho.

### 5. A equipe pode criar novos snippets, prompts ou skills?

Sim, mediante definição de contrato, exemplo e revisão. O molde orienta a estrutura e a skill de criação pode auxiliar. Uma nova skill precisa também de teste de seleção e de fronteira com as existentes. Comece pelo [guia de padrões](../sprint-08-padroes/README.md).

### 6. Se o código foi gerado pela Genie Code, posso executá-lo sem revisão?

Não tome a geração como aprovação. Confira recursos, filtros, escrita, instalação de pacotes, coletas e permissões. A Genie Code pode executar ferramentas conforme as aprovações configuradas; autoaprovação é uma conveniência, não uma barreira de segurança. Em recursos sensíveis, adote os controles de acesso e revisão apropriados.

### Por onde começo se só quero usar?

No [guia do `.assistant`](../sprint-02-assistant/README.md), que prepara uma fixture, formula o pedido, chama um helper e interpreta o resultado. O exemplo não depende de uma tabela corporativa supostamente existente.

### Preciso dominar todas as coleções?

Não. Identifique primeiro o resultado desejado. Use a comparação de componentes para escolher o ponto de entrada e aprofunde o contrato apenas dos objetos necessários à tarefa.

### Quem mantém o código?

Os mantenedores alteram a fonte versionada, revisam os contratos e executam os testes pertinentes. Quem usa a cópia operacional informa o defeito com entrada, erro, versão e ambiente, sem transformar uma correção isolada no workspace em nova fonte de verdade.

---

## 🔗 Próximos Passos

Para usar, siga o [tutorial de primeira tarefa](../sprint-02-assistant/README.md). Para manter o pacote, consulte o [fluxo de alteração](../sprint-07-ambiente-fonte/README.md). Para localizar APIs, abra o [Catálogo de Helpers](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md); para termos, o [Glossário](../../../ambiente_fonte/.assistant/GLOSSARIO.md).

### Referências de plataforma

Conferidas em 11/09/2026. São fontes das capacidades da plataforma, não certificação da instalação do Hub: [Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills), [instruções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions), [modo agente e aprovações](https://learn.microsoft.com/en-us/azure/databricks/genie-code/agent-mode) e [imagens em notebooks](https://docs.databricks.com/aws/en/notebooks/notebook-media).
