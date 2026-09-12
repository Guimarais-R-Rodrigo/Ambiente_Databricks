# `analisar_campanha` — formular a pergunta antes de pedir uma análise

<!-- readme-objeto: 0.1.0-candidata -->

Este exemplar ajuda a transformar “mostre a taxa por segmento” em um pedido
com dados, período e uma decisão explícita. É **material dos padrões do Hub**;
o texto orienta uma interação, não executa uma análise sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing preenchível para análise de campanha encerrada. |
| Para que serve? | Organizar a pergunta de priorização da próxima campanha. |
| Use quando... | Houver recorte conhecido e orçamento expresso em contatos. |
| Evite quando... | Precisar atribuir causalidade só com o resultado observado. |
| Precisa de... | Tabela, período, unidade de análise e restrição operacional. |
| Entrega... | Um pedido estruturado; a resposta da IA ainda precisa de revisão. |

Abra o [formulário](analisar_campanha.md) para preencher ou o
[notebook](exemplo_analisar_campanha.py) para estudar a demonstração. Não execute
preparações de dados sem conferir seus efeitos e o ambiente.

## 1. O que é?

Um briefing é uma descrição organizada do trabalho desejado. Neste objeto,
ele informa uma campanha, o período considerado e a quantidade de pessoas que
a próxima ação pode contatar. Os campos entre chaves duplas, como `{{PERIODO}}`,
são espaços a substituir antes de enviar a solicitação.

A IA recebe uma pergunta mais delimitada, mas isso não garante resposta correta.
O arquivo não concede acesso à tabela nem comprova que uma skill foi carregada.
No projeto, o formulário recomenda `hub-ml-eda-profissional`; sua utilização
efetiva depende do contexto e das ferramentas disponíveis.

## 2. Que problema este recurso resolve?

A pergunta é: “O resultado desta campanha ajuda a priorizar os contatos da
próxima, e o que ainda não sabemos?”. Pedir somente taxas pode esconder tamanho
de grupo, restrição de orçamento e incerteza.

O briefing solicita uma recomendação acompanhada de limites. Isso organiza a
conversa, mas não substitui a decisão humana nem transforma uma descrição
histórica em previsão validada.

## 3. Quando faz sentido usar?

É adequado para estudar como formular um pedido analítico quando uma campanha
já terminou e sua base foi delimitada. O orçamento em contatos dá significado
operacional à comparação: um segmento muito pequeno não consegue absorver
uma grande quantidade de contatos apenas porque sua taxa foi alta.

Também é útil como referência para construir outro prompt do Hub, mantendo
contexto, entrega e revisão humana separados do texto livre de uma conversa.

## 4. Quando não usar?

Não use o formulário sem conhecer o recurso ou o período, esperando que a IA
invente essas definições. Se a campanha ainda estiver em andamento, diferenças
no tempo de exposição podem invalidar a comparação planejada.

Também não o use como comprovação de que uma oferta causou o resultado. Essa
conclusão exige desenho de identificação e evidência próprios; pedir uma
explicação convincente não os cria.

## 5. Como funciona, intuitivamente?

Você confere o recurso e preenche os campos. O pedido declara unidade de análise,
colunas esperadas, período e orçamento. Em seguida, solicita taxas, uma
priorização e aquilo que os dados não permitem concluir.

A resposta solicitada combina código PySpark e síntese executiva. A função do
formulário é organizar essas exigências. A execução, o uso de ferramentas e a
qualidade da resposta são etapas distintas, que precisam ser observadas e
validadas na interação real.

## 6. Exemplo de situação

Uma equipe fictícia dispõe de uma campanha encerrada e planeja outra com limite
de 5.000 contatos. Ela conhece a tabela e o intervalo de datas e quer comparar
segmentos sem ignorar seu tamanho.

No formulário, ela informa a tabela confirmada, o período da campanha e `5000`
como orçamento de contatos. O resultado desejado é uma priorização justificada,
com limites explícitos. Não há aqui uma resposta simulada da IA apresentada
como captura real, nem indicação de que alguma tabela foi consultada nesta R01.

## 7. O que você precisa antes de usar?

| Campo | O que informar | Por que importa |
|---|---|---|
| `{{TABELA}}` | Recurso confirmado e acessível ao contexto autorizado. | Evita análise de uma fonte inventada ou diferente. |
| `{{PERIODO}}` | Janela de datas da campanha escolhida. | Define quais contatos são comparáveis. |
| `{{ORCAMENTO_CONTATOS}}` | Quantidade de clientes que poderão ser contatados. | Expressa a restrição usada na priorização. |

O texto pressupõe um cliente contatado por campanha e menciona `id_cliente`,
`segmento`, `canal`, `dt_contato` e `respondeu`. Verifique se a fonte real
corresponde a isso. O formulário não adapta sozinho nomes ou definições de
colunas; uma diferença material precisa ser explicitada no pedido.

## 8. O que este recurso entrega?

O arquivo entrega uma instrução reutilizável. Ela solicita taxa por segmento e
canal, recomendação de priorização, limitações, código reproduzível com saída
e síntese executiva de até oito linhas.

Esses itens são um **contrato solicitado**, não uma garantia de execução ou
qualidade. Uma resposta que mostre código sem executá-lo precisa dizer isso.
Recomendação produzida não significa campanha aprovada ou público autorizado
para contato.

## 9. Como usar este recurso no Hub?

Abra [analisar_campanha.md](analisar_campanha.md), leia “Antes de colar”, preencha
os campos e forneça o contexto autorizado. O bloco “Prompt pronto para colar”
permanece no formulário, sem duplicação neste guia. Depois, use “O que conferir
na resposta” do próprio arquivo.

O [notebook](exemplo_analisar_campanha.py) contém preparo, prompt preenchido e
registro histórico da interação. Ele depende da demonstração de campanha do
[snippet](../../snippet/taxa_resposta_campanha/README.md), cujo preparo sobrescreve
uma tabela sintética persistente. Ler o prompt não exige executar essa
preparação. Não envie dados pessoais ou segredos desnecessários à conversa.

## 10. Decisões e configurações que mais importam

O orçamento é quantidade de contatos, não dinheiro. Confundir as unidades muda
a restrição da recomendação. O período deve corresponder a uma campanha
comparável, e a definição de `respondeu` deve ser conhecida.

Defina também se os clientes da próxima campanha podem ser os mesmos da
anterior. Essa informação afeta a interpretação de reaplicar uma taxa histórica.
O formulário atual não possui campo específico para todas essas decisões;
explicite lacunas relevantes em vez de esperar inferência automática.

## 11. Limitações, riscos e armadilhas

Mesmo com o formulário preenchido, podem faltar custo por contato, capacidade
de canal, elegibilidade, saturação e objetivo financeiro. Uma taxa elevada não
implica maior retorno incremental. O texto não implementa um otimizador de
alocação nem inclui todas as políticas da instituição.

A seção de limites do exemplar histórico usa formulações fortes sobre desenho
experimental. A orientação deste guia é mais delimitada: o briefing não
estabelece identificação causal, experimental ou observacional. O conteúdo
da resposta continua exigindo análise de pressupostos e evidências.

## 12. Quais são as alternativas?

Para conhecer inicialmente a tabela, consulte o
[prompt operacional de perfil rápido](../../../hub_prompts/eda_rapida/eda_rapida.md).
Para uma investigação mais ampla, examine
[`eda_completa`](../../../hub_prompts/eda_completa/eda_completa.md).

Uma consulta definida por um analista pode ser mais adequada quando a pergunta
já está fechada e não exige interação generativa. Esses caminhos não são
intercambiáveis: perfil de dados, recomendação de priorização e avaliação de
intervenção respondem a perguntas diferentes.

## 13. Como saber se o resultado faz sentido?

Confira recurso, datas e unidade de análise. Verifique se cada taxa vem com
quantidade de contatos e respostas e se a priorização respeita o tamanho dos
grupos e o orçamento informado. Reproduza contagens relevantes em ambiente
autorizado, em vez de confiar somente na narrativa.

Veja se a resposta distingue execução de proposta, explica o que não sabe e
considera a possibilidade de contatar novamente as mesmas pessoas. A presença
de texto bem organizado não demonstra que essas verificações ocorreram.

## 14. Arquivos relacionados e próximos passos

| Arquivo | Papel |
|---|---|
| [Formulário](analisar_campanha.md) | Campos, bloco colável, QA e limites. |
| [Notebook](exemplo_analisar_campanha.py) | Demonstração e registro histórico. |
| [Molde de prompt](../template.md) | Organização de um novo briefing. |
| [Molde deste README](../../readme/template_objeto.md) | Contrato comum dos guias. |

Prompt não é pacote Python: esta pasta não precisa de `__init__.py`.

## 15. Referências

As afirmações sobre campos e entrega foram confrontadas com o
[formulário](analisar_campanha.md). O [notebook](exemplo_analisar_campanha.py)
é evidência histórica da demonstração, não de uma execução desta sprint.
O [Manual Técnico](../../../MANUAL_TECNICO.md#genie) delimita contexto e execução
no ecossistema.

R01: leitura estática e revisão pelo próprio autor. Não houve envio do prompt
à Genie Code, acesso a dados, geração de resposta observada nem teste de
roteamento. Auditoria independente e aceite humano estão pendentes.
