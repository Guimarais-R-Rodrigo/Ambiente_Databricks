# `eda_rapida` — pedir um primeiro diagnóstico de dados com contexto e evidência

<!-- readme-objeto: 1.0.0 -->

Este recurso é um briefing: um formulário de texto que ajuda você a explicar a uma IA qual fonte quer examinar, para qual decisão e com quais limites. Ele organiza o primeiro olhar sobre os dados sem pressupor que você já saiba todas as respostas. Não é um programa de perfil de dados nem uma resposta pronta.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um prompt preenchível para orientar uma investigação inicial. |
| Para que serve? | Pedir um perfil com achados priorizados, evidências e limitações. |
| Use quando... | Precisar conhecer ou reavaliar uma fonte antes de aprofundar a análise. |
| Evite quando... | A pergunta exigir validação completa, conclusão causal ou correção automática. |
| Precisa de... | Recurso acessível, objetivo, foco e decisões de contexto declaradas. |
| Entrega... | Uma solicitação estruturada; a resposta depende da interação e deve ser verificada. |

Comece pelo [formulário original](eda_rapida.md), que contém o guia de preenchimento e o bloco colável. O [notebook de exemplo](exemplo_eda_rapida.py) mostra um cenário, mas seu preparo **sobrescreve uma tabela persistente**: leia o aviso da seção 9 antes de executar qualquer célula.

## 1. O que é?

EDA é a sigla de análise exploratória de dados. É a investigação inicial de estrutura, distribuições, qualidade e relações pertinentes a uma pergunta. O adjetivo “rápida” delimita o escopo: aqui se pede um perfil inicial, não toda a investigação necessária para aprovar um modelo ou uma decisão.

Um prompt é a instrução fornecida ao assistente. Neste Hub, `eda_rapida.md` combina contexto a preencher, modo de trabalho, contrato esperado de resposta e cuidados de revisão. Essa organização reduz omissões no pedido, mas não garante uma resposta correta nem transforma a IA em uma ferramenta determinística.

## 2. Que problema este recurso resolve?

A pergunta que motiva o formulário é: “Que problemas desta fonte preciso conhecer antes de usá-la para este objetivo?”. Um pedido como “analise a tabela” deixa em aberto população, período, chave, prioridades e custo aceitável.

O briefing torna essas escolhas visíveis. A decisão apoiada é quais verificações ou investigações devem vir a seguir. A decisão final sobre uso em campanha, treinamento ou produção continua dependendo das evidências e das pessoas responsáveis.

## 3. Quando faz sentido usar?

Use ao receber uma fonte nova, iniciar uma análise ou verificar se uma mudança tornou inadequadas premissas anteriores. Uma tabela conhecida também pode merecer novo perfil quando sua população, estrutura ou período mudar.

O recurso é especialmente útil quando você conhece a necessidade de negócio, mas ainda não sabe quais colunas podem ser problemáticas. Declare um objetivo concreto e poucas prioridades, como **completude** (quanto dos campos esperados está preenchido), **duplicidade** (repetição segundo a chave e a unidade definidas) e **recência** (quão atuais são os registros para o uso pretendido). Isso permite uma análise inicial focada, em vez de um inventário extenso sem relação com a decisão.

## 4. Quando não usar?

Não use um perfil rápido como comprovação de que uma base é adequada para conceder crédito ou implantar um modelo. Pode haver vazamento temporal, viés de seleção e regras de negócio não examinados pelo primeiro olhar. É necessário aprofundamento proporcional ao risco.

Um contraexemplo é solicitar “confirme que posso treinar” sem definir resposta, horizonte ou momento de disponibilidade das características. O briefing pode ajudar a levantar essas lacunas, mas não deve encerrá-las com uma aprovação genérica. Quando a pergunta já é específica, como conferir uma regra de duplicidade, prefira formular e verificar esse check diretamente.

## 5. Como funciona, intuitivamente?

Você informa qual recurso será observado e por que ele interessa. O formulário pede ao assistente que confirme o contexto, apresente um plano, examine dimensões de qualidade e devolva achados com evidência, impacto e ações propostas.

Os campos desconhecidos devem permanecer explicitamente desconhecidos. Uma chave candidata não vira chave comprovada porque foi escrita no prompt. A IA precisa distinguir informação fornecida, hipótese e observação de dados.

O arquivo Markdown, sozinho, não executa nada. A interação com o assistente pode gerar ou executar código conforme o modo, as ferramentas, as permissões e a autorização. A [documentação do modo agente](https://docs.databricks.com/aws/en/genie-code/agent-mode) descreve execução de código nesse contexto; não confunda uma instrução textual de limite com um bloqueio técnico de permissão.

## 6. Exemplo de situação

Imagine uma base fictícia de clientes que uma equipe pretende usar em uma campanha. Você conhece o objetivo, mas não confirmou se existe uma linha por cliente, qual é a data de referência ou como tratar renda ausente.

Ao preencher o formulário, declare essas dúvidas, indique completude e unicidade — verificar se a chave identifica uma única linha no recorte — como foco e restrinja a análise ao período relevante. Uma resposta útil apontará o que foi realmente verificado e o que depende de decisão de negócio. O resultado esperado é um diagnóstico inicial orientado a próximos passos, não uma nota de aprovação nem números que ainda não foram medidos.

## 7. O que você precisa antes de usar?

O formulário original explica os sete campos: recurso, objetivo, foco, chave candidata, coluna temporal, filtros/período e limite de execução. Consulte a seção “Como preencher cada campo” nele; ela é a referência de preenchimento, não uma tabela duplicada aqui.

Informe o recurso efetivamente selecionado ou acessível. No Genie Code, use os mecanismos de seleção de contexto disponíveis na interface e confira o item anexado; escrever um nome plausível não comprova que a tabela ou a skill foi carregada. A [documentação de navegação](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code) explica o uso de contexto na interface.

É necessário ter autorização para consultar a fonte. O prompt não concede permissões. Conheça também o que pode aparecer em chat, logs ou relatórios: peça agregação ou mascaramento e evite fornecer valores identificáveis desnecessários. Um limite de tempo escrito deve ser tratado como requisito a verificar, não como quota automaticamente imposta à infraestrutura.

## 8. O que este recurso entrega?

O artefato da pasta entrega um pedido, não dados calculados. Seu contrato solicita resumo executivo de até oito achados, quadro de dimensão, evidência, severidade, impacto e ação, além de limitações e próximos passos. Código é pedido somente quando solicitado ou autorizado.

Ao ler a resposta, diferencie o que foi observado na fonte, o que foi inferido e o que foi apenas proposto. “Há duplicidade” exige uma definição de chave, filtros e resultado de uma verificação. “Sugiro verificar duplicidade” é uma recomendação, não uma constatação.

Não interprete texto bem organizado como prova de execução. Confirme comandos executados, recursos usados e resultados apresentados. Quando algo não pôde ser acessado, a resposta correta é delimitar a lacuna, não preenchê-la com um número plausível.

## 9. Como usar este recurso no Hub?

Abra [eda_rapida.md](eda_rapida.md), leia o guia e preencha o bloco original. Selecione o contexto real na interface e indique a skill recomendada pelo formulário, `hub-ml-eda-profissional`, pelo mecanismo disponível. Antes de permitir ações, confirme o plano e o alcance de execução que você autorizou.

O [notebook](exemplo_eda_rapida.py) tem preparo sintético, um pedido preenchido e um espaço para registrar a interação real. O preparo chama `write.mode("overwrite").saveAsTable("workspace.default.hub_exemplo_clientes")`: pode substituir uma tabela existente. **Não execute esse preparo em recurso compartilhado sem autorização específica e conferência do destino.** Um ambiente de teste não torna qualquer nome seguro por definição.

O limite de não escrever, presente no prompt, não protege contra a escrita das células preparatórias do notebook. Você pode estudar o formulário e o cenário sem executar essas células. A resposta real de Genie Code permanece marcada como não executada no exemplo; esta sprint não simula essa interação nem preenche a lacuna com uma resposta inventada.

## 10. Decisões e configurações que mais importam

O objetivo determina quais achados são materiais. O foco delimita a profundidade inicial; filtros e período definem a população. A chave e a coluna temporal afetam o significado de duplicidade, cobertura e recência.

Declare o que é conhecido e o que ainda precisa ser confirmado. Não substitua “não informado” por um valor escolhido apenas para completar o formulário. Também distinga permissão de gerar código, executar leitura e escrever dados: são alcances diferentes, não consequências automáticas de pedir ajuda.

O formulário sugere limites de tempo, custo ou volume. Para um bloqueio obrigatório, dependa das políticas e permissões efetivas do ambiente, não somente de uma frase enviada ao assistente.

## 11. Limitações, riscos e armadilhas

A qualidade depende do contexto e da capacidade de inspecionar evidências. Uma resposta pode omitir uma regra de negócio importante ou confundir uma amostra com a tabela inteira. Uma instrução de privacidade pode ser descumprida; confira a saída antes de compartilhá-la.

O roteiro de até oito achados é uma prioridade de apresentação, não a garantia de que todos os problemas foram encontrados. O prompt não valida por si só custo, permissões, schema, causalidade ou segurança do código proposto.

O cenário do notebook usa dados sintéticos e contém uma escrita persistente separada da interação. Sua existência não comprova execução recente nem comportamento de uma skill no workspace. Respostas e interfaces também podem variar; registre o contexto efetivamente usado ao produzir evidência durável.

## 12. Quais são as alternativas?

Para executar diretamente um perfil com saída estruturada, examine o [script quick_profile](../../hub_scripts/quick_profile/README.md). Ele tem uma implementação definida, mas seu escopo não é equivalente à investigação conduzida pelo assistente.

Para explorar relações e aprofundar hipóteses, consulte o [prompt eda_completa](../eda_completa/eda_completa.md). Para regras de qualidade já conhecidas, considere [data_quality](../data_quality/data_quality.md) ou checks diretos. Escolha pelo tipo de pergunta e pelo que falta comprovar, não apenas pelo tamanho do prompt.

## 13. Como saber se o resultado faz sentido?

Releia “O que conferir na resposta” no formulário original. Confira que recurso, população, grão e período são os que você forneceu. Peça a evidência dos achados materiais: consulta, contagem, denominador, amostragem e limitações.

Procure uma conclusão que a resposta tenha tratado como fato e verifique sua sustentação. Se ela disser que a chave é única, há uma checagem correspondente sobre a população relevante? Se propuser correção, está distinguindo sugestão de alteração já executada?

Uma evidência ausente pede investigação adicional ou uma conclusão mais estreita. Não aprove o resultado por sua fluência, nem exija uma certeza que os dados e o contexto disponíveis não podem oferecer.

## 14. Arquivos relacionados e próximos passos

O [formulário principal](eda_rapida.md) é o ponto de uso, com seus limites e controles preservados. O [notebook](exemplo_eda_rapida.py) ilustra o cenário e os cuidados de preparo. O [Hub Prompts](../README.md) reúne outras solicitações e o [Manual Técnico](../../MANUAL_TECNICO.md#catalogo-helpers) mantém a visão integrada dos recursos.

Depois do primeiro perfil, transforme os achados em checagens concretas, mantendo a separação entre leitura, proposta e escrita. Não há importação Python do prompt nem execução automática por abrir este README.

## 15. Referências

O formulário e o notebook vinculados sustentam o contrato local, revisado na base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`, em 12/09/2026. Os blocos coláveis foram preservados; não foi executada a interação Genie Code nem a escrita persistente da demonstração.

As páginas oficiais de [navegação do Genie Code](https://docs.databricks.com/aws/en/genie-code/navigate-genie-code) e [modo agente](https://docs.databricks.com/aws/en/genie-code/agent-mode), consultadas em 12/09/2026, fundamentam as distinções de contexto e execução. Elas descrevem a plataforma, não homologam este prompt customizado.
