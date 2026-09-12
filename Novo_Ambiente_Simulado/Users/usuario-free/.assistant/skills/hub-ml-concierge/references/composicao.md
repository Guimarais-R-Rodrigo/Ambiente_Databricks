# Composição mínima e fronteiras

## Escolher o nível certo

Um helper atende uma operação pontual; uma skill orienta um método; um briefing estrutura as informações do caso; um padrão orienta criação. O Concierge conecta esses níveis sem reescrever suas responsabilidades.

`DIRECT_ROUTE` significa que há um componente principal suficiente para o método/briefing. `HELPER_ROUTE` identifica uso pontual de API. `COMPOSITE_ROUTE` exige contribuição complementar real. `BRIEFING_FIRST` resolve uma ambiguidade que muda a escolha; não deve virar um bloqueio burocrático para toda pergunta incompleta.

## Contrato de cada ligação

Para propor A -> B, confira o que A entrega e o que B recebe. Registre tipo de dado, grão, nomes relevantes, referência temporal, escala das métricas, dependências, estado de sessão e efeitos persistentes. Se faltar essa verificação, apresente um plano conceitual, não um pipeline executável.

Não conecte automaticamente um DataFrame Spark a uma função pandas. Não recomende `toPandas()` sem estratégia e limite apropriados. Não misture métricas em razão e percentual. Não elimine guardrails de uma skill ao reutilizar parte de seu fluxo.

## Padrões de composição, não receitas obrigatórias

**Base nova:** briefing de qualidade ou EDA -> diagnóstico adequado -> interpretação. Modelagem só entra se fizer parte do pedido e após os pré-requisitos.

**Join temporal:** esclarecer instante de decisão -> método de feature engineering -> diagnóstico de chaves/cardinalidade -> helper point-in-time -> validação do resultado. Essa sequência é conceitual; cada contrato deve ser verificado.

**Mudança na base:** distinguir qualidade, drift e performance -> escolher helper conforme a entrada -> interpretar limites. Mudança de distribuição não prova degradação; sem rótulos, não prometa medir a performance supervisionada realizada.

**Apresentação:** um formatador ou helper visual pode bastar. Não carregue uma EDA inteira para formatar reais.

**Criar um objeto:** verificar reuso primeiro -> explicar a lacuna -> apontar `hub-ml-criar-objeto` e o padrão pertinente, se existirem na base consultada. O Concierge não cria o objeto durante descoberta.

## Partes reutilizáveis

Prioridade: API pública existente; método público de classe; template/seção metodológica com origem; adaptação explícita. Funções privadas, variáveis globais e células dependentes do estado não são peças intercambiáveis sem revisão.

Diga o que já existe e o que precisará ser desenvolvido. Uma composição de componentes existentes pode exigir glue code; não a apresente como pronta para execução se esse código ainda não foi produzido e validado.

## Handoff sem ciclo

Transfira objetivo, decisões confirmadas, evidências, candidatos selecionados, restrições, lacunas e critérios de aceite. Não envie todo o conteúdo recuperado. A continuação não precisa repetir a descoberta resolvida.

Uma menção a outra skill é uma recomendação de seleção, não uma RPC nem um subagente. Não crie um ciclo Concierge -> especialista -> Concierge sem fato novo. Se o usuário autorizou apenas planejar, mantenha essa restrição no repasse.
