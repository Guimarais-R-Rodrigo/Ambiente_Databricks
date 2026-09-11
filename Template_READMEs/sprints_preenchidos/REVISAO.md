# Revisão dos READMEs candidatos — 11/09/2026

## Escopo e estado

Revisão sobre a base `b395d632055ce632daa1e0799622b10ceee1e560`.
Os dez documentos desta pasta são candidatos, ainda sujeitos ao aceite de Rodrigo.
Não houve substituição dos READMEs em `ambiente_fonte/`, mudança da lógica de
helpers, render do simulado, publicação Databricks ou teste de conversa presumido.
Na raiz, somente as linhas numéricas do gate são atualizadas mecanicamente.

## Correspondência com os achados

| Achado | Correção implementada | Verificação |
|---|---|---|
| DQ com metrics inexistente | checks, alerts, score e campo column reais | API por AST; exemplos extraídos do Markdown |
| Score confundido com certificação | fórmula e alcance local explicados | revisão de contrato e oráculo 95 |
| Taxa escalar fictícia | exemplar Spark por segmento e Wilson | conta 2/10, limites 5,67/50,98 e largura 45,32 |
| Freshness dependente do calendário | nulidade sem data; caso de freshness separado | casos com None, data atual e data antiga |
| Schema muda entre guias | fixture comum e schemas adicionais explicitados | preparo em cada percurso ou link exato |
| View temporária tratada como tabela anexada | contexto da célula/schema e sessão local | revisão documental; interface real ainda exige workspace |
| Genie nunca executaria helpers | presença, carregamento, execução e aprovação separados | documentação oficial consultada |
| Dependências generalizadas | import versus chamada e efeitos de tracking | implementação e chamadas de exemplo |
| Split por índice sempre vazaria | generalização removida; benefício de períodos/gaps | conta 6/3/1 meses e callback walk-forward |
| Guia usa README não publicável | exemplo passa a usar .assistant/README.md | renderer e itens publicáveis lidos |
| Catálogos resumidos | 51 snippets, 7 scripts, 13 skills, 16 prompts com fichas | inventário e links específicos |
| Caminhos incompatíveis com staging | links físicos + mapping + destino virtual | gate de links/âncoras nas duas posições |
| Exemplos de Markdown tratados como links | mascaramento de código antes da varredura | testes positivos/negativos dos guardas |
| Imagens e legendas | 21 diagramas + 2 banners reutilizados, sem alteração binária | hashes, dimensões, contato visual e preview |
| Placeholder de evidência | saída real do gate no candidato raiz | execução local; sem inventar execução remota |
| Seguir método confundido com carregamento | testes de roteamento separados de qualidade | procedimentos P/N/@; sem certificação de conversa |
| MLflow Free generalizado | incidente histórico localizado, sem proibição universal | referência ao exemplo específico |
| Notas ao autor e 18 px | metatexto removido; 18 px exatos a 720 px | copy.json/manifest e cálculo |
| Links históricos fora dos rascunhos | protótipos locais identificados como não versionados | sem arquivos fictícios ou supressão global do gate |

## Errata de entrega e disposição das imagens

Na primeira entrega, as correções estavam apenas na branch de revisão; os
rascunhos da `main` ainda usavam caminhos relativos aos futuros destinos e,
por isso, não exibiam as imagens. Esta entrega atualiza os próprios rascunhos,
sem promover o conteúdo para os READMEs oficiais.

A comparação seção a seção também encontrou duas diferenças que a checagem
anterior de existência/hash não detectava: o guia da raiz não mostrava o
fluxo de contexto na seção correspondente, e o panorama de retornos dos scripts
estava no catálogo, em vez do passo a passo operacional. Ambos foram corrigidos.

O gate agora compara as imagens, sua ordem e a seção imediatamente anterior
com o README atual de referência. Quatro testes adicionais cobrem ausência,
seção incorreta, ordem incorreta e caminhos relativos com exemplos em código.
O índice [README desta pasta](README.md) oferece acesso direto aos dez candidatos.
São 31 inserções reais, provenientes dos mesmos 23 PNGs aprovados; nenhum PNG
foi alterado. O preview offline desta correção carregou as 31 inserções nos
dez guias; a resolução dos caminhos foi conferida separadamente pelo gate.
A promoção oficial e a publicação no workspace continuam pendentes.

## Imagens e apresentação

As imagens são os PNGs aprovados já existentes. Foram inspecionados os 21 diagramas
por família e os dois cabeçalhos em largura reduzida de 720 px. As referências
foram inseridas nas seções conceituais correspondentes, com texto antes/depois,
alt e âncoras explícitas. Os hashes/dimensões são confrontados com os manifestos
existentes; nenhum hash foi relaxado e nenhuma nova arte foi gerada.
Na primeira revisão, o snapshot foi renderizado em HTML local: 30 ocorrências
de imagem carregaram a partir dos 23 PNGs. Esse teste não detectava omissão
em relação ao README de referência; a errata acima corrige essa lacuna. O preview usa os bytes incorporados em memória;
a navegação de URLs do navegador local é bloqueada. A resolução física e virtual
dos caminhos é verificada separadamente pelo gate. Isto não é preview Databricks.

O mapa da raiz representa componentes; não se atribui significado de descoberta
nativa a um traço cuja figura não sustenta isso. Diagramas de notebook ilustram
uma rota, sem negar ferramentas de execução do agente. O cabeçalho CRM é único
nos guias; Squad aparece no guia de escolha, não empilhado como segundo banner.

## Testes reproduzíveis e limites

```powershell
python tools/ci_local.py
python tools/review_readmes.py
python tools/tests/test_readme_review.py
python tools/tests/test_readme_examples.py
```

O teste de exemplos lê os blocos Python dos próprios READMEs. A suíte básica
executa 24 casos portáveis e informa 14 casos Spark ignorados, sem considerar
skip como execução bem-sucedida. Os guardas de revisão possuem 24 testes, incluindo os quatro de disposição de imagens.

O workflow `readme-examples.yml` instala PySpark 4.0.1 somente no runner Linux,
com Python 3.11/Java 17, e executa `test_readme_examples.py --spark`. O resultado
corrente deve ser lido no GitHub Actions do commit, não inferido da existência
do workflow. Esses testes não abrangem treinadores opcionais, MLflow real,
Databricks serverless/Connect, ACL ou conversas com Genie Code. Não instale
PySpark em notebooks serverless para reproduzir esse job de CI local.

O gate estático confere dez documentos, ambos os contextos dos links, argumentos
de chamadas diretas por AST e 23 imagens únicas. AST não comprova tipos de
DataFrame, nomes dinâmicos ou correção estatística de toda a biblioteca.

## Fontes de plataforma consultadas em 11/09/2026

[Skills e scripts referenciados](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills),
[modo agente e aprovações](https://learn.microsoft.com/en-us/azure/databricks/genie-code/agent-mode),
[instruções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions),
[contexto de células](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips),
[dependências serverless](https://learn.microsoft.com/en-us/azure/databricks/compute/serverless/dependencies)
e [imagens em notebooks](https://docs.databricks.com/aws/en/notebooks/notebook-media).
A disponibilidade concreta continua dependente da configuração do workspace.

## Próximo aceite

Revise os dez rascunhos pelo [plano de navegação](PLANO.md). A exportação descrita
ali gera somente um snapshot isolado. A promoção dos documentos à fonte oficial
é uma operação separada, posterior à aprovação, seguida de validação, render e
publicação explicitamente autorizada. Não copiar a pasta inteira do snapshot.
