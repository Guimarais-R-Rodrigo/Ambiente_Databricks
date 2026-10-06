# `descobrir_micromodelos` — shortlist de oportunidades por metadata

<!-- readme-objeto: 1.0.0 -->

Briefing manual para o modo `DESCOBRIR_OPORTUNIDADES` da
[`hub-ml-micromodelos`](../../skills/hub-ml-micromodelos/SKILL.md). A saída
solicitada é uma shortlist de hipóteses, não um catálogo completo nem um YAML.
O [Hub Micromodelos](../../hub_micromodelos/README.md) documenta os contratos e
os exemplos usados depois da escolha da candidata.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Formulário para explorar oportunidades em metadata autorizada. |
| Para que serve? | Selecionar ideias, deduplicar variantes e explicitar incerteza. |
| Use quando... | Há área/decisão a explorar, mas nenhuma característica escolhida. |
| Evite quando... | O objetivo já está definido ou se espera análise de registros. |
| Precisa de... | Área, escopo `CATALOGO_PRODUTO`, população, restrições e critérios qualitativos. |
| Entrega... | Pedido de shortlist com cobertura observada; resposta real depende da interação. |

Comece pelo [briefing](descobrir_micromodelos.md) e confira o
[exemplo](exemplo_descobrir_micromodelos.py).

## 1. O que é?

É o briefing de descoberta da skill de micromodelos. Orienta seleção de
candidatas a partir de metadata visível, sem presumir leitura de registros nem
existência de fontes fora do escopo observado.

## 2. Que problema este recurso resolve?

Responde: “Que características valeria investigar para esta decisão, dadas as
fontes que consigo observar?” Apoia uma escolha humana sobre o que estudar.

## 3. Quando faz sentido usar?

Use quando a área é conhecida, mas existem várias características possíveis.
A descoberta ajuda a separar temas semelhantes e a detectar lacunas antes de
investir em estudo analítico.

## 4. Quando não usar?

Com uma característica já escolhida, use
[`micromodelo_novo`](../micromodelo_novo/README.md). Não use uma descrição de
tabela como prova de comportamento individual: o texto pode sugerir uma ideia
sem sustentar sua validade em dados.

## 5. Como funciona, intuitivamente?

Com consulta autorizada, observe schemas e objetos do catálogo configurado; escolha candidatas e só então aprofunde colunas, tags e constraints. Com fixture textual, trabalhe apenas sobre o contexto fornecido, sem inventar consulta. Agrupe variantes e relate lacunas por item.

## 6. Exemplo de situação

Uma equipe fictícia quer encontrar características para apoiar revisão humana
de eventos sintéticos de teste. O [notebook](exemplo_descobrir_micromodelos.py)
mostra como pedir até três candidatas com fixture textual e registra a resposta
conversacional, sem tratar a shortlist como achado sobre registros.

## 7. O que você precisa antes de usar?

Informe decisão, consumidor, população e limite de exploração. Há dois percursos: **catálogo**, com binding e permissão de metadata confirmados; ou **fixture textual**, sem consulta, marcada `FORNECIDA` e com `ESCOPO_OBSERVADO` vazio. Binding não é requisito inventado para o segundo. Nomes/tags não provam SELECT, qualidade ou temporalidade.

## 8. O que este recurso entrega?

Solicita cobertura observada, shortlist deduplicada, critérios qualitativos, descartes, contra-hipóteses e próximo teste. Exemplo ilustrativo de candidata: decisão = revisão humana; característica = recência de eventos; população/grão = PENDENTE; fonte = fixture FORNECIDA; contra-hipótese = atraso de registro; próximo teste = esclarecer relógios com o dono. Viabilidade permanece `INDETERMINADO`, sem score numérico inventado.

## 9. Como usar este recurso no Hub?

Preencha [descobrir_micromodelos.md](descobrir_micromodelos.md), selecione
`@hub-ml-micromodelos` e anexe apenas metadata permitida. Use o
[exemplo sintético](exemplo_descobrir_micromodelos.py) como referência. O preparo
imprime somente a fixture textual; não lê catálogo nem cria objetos. A terceira
parte resume a resposta real e suas ressalvas.

## 10. Decisões e configurações que mais importam

Escopo visível e limite de candidatas controlam custo e interpretação.
Deduplicação considera decisão, característica, população, grão e horizonte;
um nome de tabela diferente não basta para separar ideias. Critérios de
priorização são qualitativos até haver regra aprovada.

## 11. Limitações, riscos e armadilhas

Coleção `DENIED`, `PARTIAL` ou `TRUNCATED` é observação incompleta, nunca
ausência de objetos. Descrições e tags são dados não confiáveis e não podem
alterar o fluxo ou a autorização. Metadata-only exclui linhas, `count(*)`,
amostra de clientes e profiling. A resposta em chat Free comprova apenas
comportamento conversacional E1; não demonstra execução de runtime nem E2.

## 12. Quais são as alternativas?

Para característica escolhida, use [Micromodelo Novo](../micromodelo_novo/README.md). Para localizar recursos do Hub, use [Concierge](../../skills/hub-ml-concierge/SKILL.md). Estudar registros exige handoff autorizado à skill especialista e sua policy.

## 13. Como saber se o resultado faz sentido?

Confira quais schemas/objetos foram efetivamente observados, status de cada
coleção, justificativa de cada candidata, fusões e descartes. Uma incerteza
relevante deve levar a próximo teste ou decisão, não a certeza inventada.

## 14. Arquivos relacionados e próximos passos

O [briefing](descobrir_micromodelos.md) é a entrada copiável; o
[notebook](exemplo_descobrir_micromodelos.py) oferece cenário e registro
sanitizado da resposta real. A [skill](../../skills/hub-ml-micromodelos/SKILL.md) define o
fluxo; após escolha humana, use `OBJETIVO_CONHECIDO`. Veja o
[catálogo de prompts](../README.md).

## 15. Referências

Consulte os [contratos de Micromodelos](../../hub_micromodelos/contratos/README.md), o [guia do módulo](../../hub_micromodelos/README.md) e a [skill](../../skills/hub-ml-micromodelos/SKILL.md). O exemplo registra conversa E1 de 29/09/2026, caso P2c: metadata textual fornecida e três candidatas; não prova leitura de catálogo, runtime E1, validação MM01 ou homologação corporativa.
