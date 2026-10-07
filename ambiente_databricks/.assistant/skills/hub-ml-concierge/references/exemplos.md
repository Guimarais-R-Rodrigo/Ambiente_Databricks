# Exemplos ilustrativos de atendimento

Os nomes abaixo foram identificados na base de referência registrada em `docs/fontes.md`. Não são um catálogo novo, transcrições de uso, prova de execução ou garantia de publicação. A cada atendimento, confirme os arquivos e a API na instalação consultada. Os exemplos omitem linhas/commits de evidência porque não representam uma busca realizada naquele atendimento.

## 1. Checagem pontual de nulos e duplicidades

Pedido: “O que o Hub tem para verificar a qualidade desta tabela antes de modelar?”

Resposta-modelo: “Para uma checagem pontual de tabela nomeada, o candidato principal é `hub_scripts.data_quality_check`. Vou conferir suas verificações e os parâmetros de chave. Se o objetivo incluir entender distribuições e relações, `hub-ml-eda-profissional` oferece o método mais amplo. Não é necessário iniciar treinamento.”

Classificação esperada: `HELPER_ROUTE`, se a demanda for somente checagem; `COMPOSITE_ROUTE`, se diagnóstico e EDA forem explicitamente necessários. Confirmar grão e chave antes de interpretar repetição como erro.

## 2. Informação do futuro em junções

Pedido: “Quais peças posso combinar para cruzar o histórico sem usar informação que ainda não existia?”

Resposta-modelo: método `hub-ml-feature-engineering`; candidatos `hub_snippets.spark.pit_join` e `hub_snippets.spark.join_diagnostics`; briefing de feature engineering. Explicar disponibilidade do dado, instante de decisão e cardinalidade. Não assumir que a data do evento é a data de publicação.

Classificação esperada: `COMPOSITE_ROUTE`. Compatibilidade precisa ser verificada; não há código executado.

## 3. Formatação brasileira

Pedido: “O Hub tem algo para mostrar reais e porcentagens?”

Resposta-modelo: verificar `hub_snippets.constants.format_br` e seus símbolos públicos `fmt_brl` e `fmt_pct`; indicar o exemplo do objeto. Não acionar pipeline, baseline ou EDA.

Classificação esperada: `HELPER_ROUTE`. Em caso de uso apenas de uma função, recomendar esse símbolo, não copiar o módulo inteiro.

## 4. Drift versus performance

Pedido: “Qual recurso uso para descobrir se meu modelo piorou? Ainda não tenho os rótulos do mês.”

Resposta-modelo: esclarecer que a pesquisa deve separar drift de performance. `hub-ml-monitoramento-modelo` pode orientar o plano; `hub_scripts.drift_detector` e `hub_snippets.spark.psi_calculator` são candidatos dependentes do formato da entrada. Sem rótulos, não prometer mensurar performance supervisionada realizada.

Classificação esperada: `DIRECT_ROUTE` ou `COMPOSITE_ROUTE`, com cobertura parcial do objetivo original. Não concluir que o modelo piorou.

## 5. Não há acesso ao Hub

Pedido: “Encontre o melhor helper no meu Hub”, sem arquivos ou ferramenta de leitura.

Resposta-modelo: “Não consigo verificar os componentes com o contexto disponível. Forneça a raiz acessível ou as seções de inventário do Manual. Posso então comparar os candidatos; neste momento a cobertura é não determinada.”

Classificação esperada: `ACCESS_BLOCKED`, não `GAP`.

## 6. Algo ainda não implementado

Pedido: “O Hub tem um helper para esta capacidade específica?”, e a inspeção autorizada não encontra uma implementação adequada.

Resposta-modelo: delimitar as fontes pesquisadas, citar cobertura parcial encontrada e registrar a lacuna. Distinguir orientação de uma skill, API externa e novo objeto. Indicar `hub-ml-criar-objeto` somente para uma eventual criação autorizada.

Classificação esperada: `GAP` no escopo pesquisado. Não inventar o nome de um helper plausível.

## 7. Especialista explícito

Pedido: “@hub-ml-eda-profissional, analise esta tabela.”

Comportamento esperado: não interceptar. Se Concierge foi selecionado acidentalmente, fazer handoff imediato sem refazer a triagem ou afirmar que ativou outra skill por imprimir seu nome.
