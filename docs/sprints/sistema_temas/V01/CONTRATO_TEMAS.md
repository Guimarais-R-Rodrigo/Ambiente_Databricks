# Contrato candidato de temas — V01

Status: especificação verificável 0.1.0, não instalada. O [ADR-0013](../../../decisions/ADR-0013-sistema-de-temas.md)
registra a decisão proposta; o [schema](../../../../ambiente_fonte/.assistant/hub_padroes/identidade_visual/theme.schema.json) é a fonte dos campos.
A [referência derivada](TOKENS.md) detalha cada token. Não existe configuração
concorrente em Python, YAML ou TOML nesta sprint.

## 1. Fronteira do sistema

Tema descreve aparência. Não descreve dados, permissões, consultas, caminhos
corporativos, limites de score, algoritmos, métricas, amostragem ou critérios
para dizer que um resultado é bom. O mesmo valor pode ser favorável em um
indicador e desfavorável em outro; a regra analítica determina o estado e o
tema apenas determina sua representação.

Centralização é uma fonte de escolhas por contexto, não a obrigação de todos
os gráficos e diagramas terem o mesmo título, margem ou fundo. São dimensões
separadas: identidade (`hub` nesta candidata), modo (`light`, `dark` ou
`high_contrast`) e contexto (`notebook`, `readme` ou `presentation`). Modo é uma
intenção: escrever `high_contrast` não certifica acessibilidade. Os contextos
`app` e `aibi` estão reservados e são recusados por esta versão; suas traduções
serão especificadas com as extensões, sem simular suporte com um rótulo.

Os três contextos usam dois grupos: notebook e editorial. Um documento corresponde
a uma combinação completa. Não há mistura de tokens de notebook em README,
nem alteração de idioma, unidade de negócio ou significado de categoria.

## 2. Documento completo, sem herança implícita

A candidata adota documentos completos: todos os campos do contexto são
obrigatórios. O usuário final partirá de um preset pela interface futura;
não terá que digitar 48 parâmetros. O editor construirá o documento completo
antes de validá-lo. `default` no schema documenta a referência e não preenche
um campo ausente.

Não se aceita `extends`, `parent`, `$ref` ou herança em um tema. A proposta
anterior de compor identidade, modo e contexto continua atendida pela seleção
e exportação **explícita** de uma configuração completa. Optamos por não
introduzir um resolvedor recursivo em uma primeira versão: elimina ciclos,
valores ocultos e dependências que mudam retroativamente. Templates futuros
poderão gerar documentos completos, mas não serão herança de runtime sem
mudança revisada deste contrato.

No schema, `$ref` interno é apenas reuso de definição técnica. Referências de
schema externas ou dinâmicas são recusadas pelo verificador de manutenção;
nenhum serviço remoto é necessário para validar os exemplos.

## 3. Campos do envelope

| Campo | Semântica e regra |
|---|---|
| `schema_version` | `0.1.0` nesta candidata; futuras versões exigem compatibilidade deliberada. |
| `theme_id` | Identificador estável, 3 a 64 caracteres em minúsculas e hífens; não é caminho. |
| `theme_version` | Três números sem zeros à esquerda, como `0.1.0`; distingue revisões do conteúdo. |
| `display_name` | Nome de 1 a 80 caracteres, sem HTML ou controles. |
| `description` | Explica a intenção em até 320 caracteres; não deve conter dados de negócio. |
| `identity_id` | `hub`; outra identidade dependerá de ampliação revisada. |
| `mode` | Claro, escuro ou intenção de alto contraste, nos identificadores técnicos do schema. |
| `context` | Notebook, README ou apresentação, sem prometer renderização nesta sprint. |
| `engine_compatibility` | Protocolo-alvo major 1, mínimo compatível com 1.0.0 e teto exclusivo major 2. |
| `asset_set_id` | ID do conjunto permitido, nunca caminho ou URL fornecido pelo usuário. |
| `tokens` | Todos os parâmetros do grupo aplicável; propriedades desconhecidas são erro. |

Escopo, estado de aprovação, autor autenticado, permissões, destino e hashes
aprovados pertencem ao registro confiável do processo, **fora do tema**.
`approved=true`, `role=publicador` e `scope=compartilhado` são recusados no JSON.
Uma cópia renomeada não adquire autorização. Mesmo uma configuração válida não
é publicada por este verificador.

## 4. Formato de entrada e limites

A entrada é UTF-8 sem BOM, até 131.072 bytes (128 KiB), com até 12 níveis de
objetos/listas. Chaves duplicadas são erro, inclusive aninhadas. `NaN`, infinito,
exponentes não finitos e sequências Unicode isoladas são recusados. O parser
limita bytes e profundidade antes de interpretar a árvore. Os limites são
escolhas defensivas do contrato candidato, não medidas de desempenho no Hub.

Cores são exatamente `#RRGGBB`, letras A–F maiúsculas. Não são aceitos atalhos,
canal alpha, nomes CSS ou comandos. A interface futura poderá converter espaços
e letras minúsculas de maneira visível antes de criar uma proposta; o
validador não faz coerção silenciosa. Dimensões são números da unidade declarada:
`900`, não `"900px"`. Booleanos não são dimensões. O dicionário informa mínimos,
máximos, escolhas e comprimentos.

Paletas precisam ter número de cores dentro dos limites e sem repetição exata.
A divergente tem quantidade ímpar para indicar centro. Essas verificações não
provam ordenação perceptual, distância entre categorias, adequação a daltonismo
ou que a escala estatística tem centro apropriado. Tais propriedades exigem
adaptação e revisão visual. Mapeamentos categoria→cor devem ser estáveis no
consumidor, independentemente de filtros e ordenação.

Fontes são IDs de uma lista permitida, associados a famílias/fallbacks. Não se
aceita arquivo, URL, CSS ou fonte embutida fornecida pela proposta. Não há
redistribuição de fontes neste pacote. O fallback e a disponibilidade real
serão testados por superfície antes de prometer equivalência visual.

## 5. Compatibilidade e significado dos defaults

`legado_notebook.json` registra valores de referência da fonte V00. Preserva
separadamente a paleta geral de dez cores e a paleta de seis cores de
`ml/curves_plotly`. Unificá-las agora mudaria a saída antiga sem decisão explícita.
O token de cor institucional não substitui automaticamente as paletas:
uma mudança em série/categoria deve ser mostrada na lista de impactos.

`legado_editorial.json` reflete os tokens declarados do YAML e dimensões de
referência. Isso **não prova** que todo render atual usa cada default. Há
valores locais na implementação: por exemplo, o título editorial declarado
em 52 px convive com 48 px em `heading`, e a opacidade de glow declarada em
0,16 convive com uso de 0,12. A V06 deverá decidir se conserva o resultado
renderizado ou promove nova variante. Não basta conectar o YAML e afirmar
que o visual legado foi preservado.

O contrato identifica `default_origin`, `consumers`, `delivery`, `control`,
`contexts`, `editable_by`, `unit` e efeito de cada token. **Ponto de integração
planejado não é cobertura já entregue.** Valores ainda visíveis apenas em
amostras aparecem como avançados, sem promessa de propagação. Nenhum dos
80 campos está ligado ao produto por esta sprint.

As APIs atuais, retornos, escape de HTML, formato brasileiro de tabela e o
registro global `caixa` continuam inalterados. Adaptadores posteriores
acrescentarão tema opcional sem deslocar argumentos posicionais. Ausência
voluntária de tema mantém a rota legada. Tema explicitamente solicitado e
inválido deve falhar com orientação; não deve escolher outro silenciosamente.

## 6. Assets, versões e reprodutibilidade

Notebook usa `sem-assets`; contextos editoriais usam o conjunto
`editorial-v2-congelado` de referência. O [registro](referencias_assets.json)
reproduz os hashes de 12 recursos da V00, com base identificada. É uma prova
de integridade do baseline, não uma aprovação nova nem um catálogo rival.
O registro será integrado ao manifesto oficial quando houver runtime.

Os caminhos são internos, relativos e verificados no checkout. Diretórios
simbólicos, traversal, caminho absoluto ou recurso ausente são erro. PNG
publicado não lê tema dinamicamente. Fundos raster e assinaturas aprovadas
necessitam variante/revisão, nunca troca indiscriminada de cor ou do hash esperado.

Após aprovação, ID/versão e bytes não podem ser sobrescritos. Uma alteração
produz nova revisão. O hash SHA-256 dos bytes exatos, schema, manifesto de assets,
versão do renderizador e destino vinculam a evidência de aprovação. Reformatar
o JSON também altera esses bytes: uma ferramenta não deve reutilizar a aprovação
anterior como se o conteúdo fosse idêntico. Canonicalização, se desejada, será
feita antes da submissão, nunca depois sem nova revisão.

Versionamento de conteúdo: correção de metadado exige nova revisão; mudança
visual compatível usa versão distinta; mudança de significado/estrutura exige
revisão do contrato. Sem `latest` automático em produção. Acesso à rede para
buscar o tema corrente não será pré-requisito de cada renderização: a promoção
publicará configurações e dependências fixadas junto do produto.

## 7. Escopo, persistência e falhas

Prévia pessoal não tem efeito compartilhado. Um projeto pode fixar uma versão
aprovada. O padrão compartilhado é alterado somente por publicação explícita.
Uma preferência pessoal nunca vence uma política obrigatória do destino.
A política e a identidade são fontes confiáveis externas; não podem ser
sobrescritas pelo arquivo recebido. Não há fallback que amplie privilégios.

Na V01 não existe persistência operacional. Os fixtures são arquivos de teste.
No laboratório futuro, o rascunho da sessão será volátil até salvar/exportar;
a interface informará destino e duração de forma explícita. Antes do App,
Git continuará sendo o registro canônico dos temas aprovados e a proposta
será armazenada por fluxo autorizado, sem acrescentar banco de dados desnecessário.

Erros usam código e orientação curta, sem imprimir dados recebidos. `JSON_*`
indica formato/limite; `SCHEMA_*`, campo ou tipo; `ENGINE_VERSION`, versão-alvo;
`PALETTE_CENTER`, centro; `ASSET_*`, conjunto ou hash; `PATH_*`, referência;
`POLICY_*`, especificação de governança; `MODEL_DENY`, recusa do oráculo de teste.
O guia do mantenedor descreve correção e proíbe contornar a guarda removendo-a.

## 8. O que é propositadamente adiado

Aplicação em figura, registro global de sessão, escolha em notebook e seleção
por usuário não estão implementados. Também não há geração de PNG, exportador
novo de PDF/PPTX, recoloração de fundos raster, modificador da interface inteira
do Databricks, catálogo de adoção vivo, App ou tradutor AI/BI. Layout estrutural
novo exige template próprio, não dezenas de coordenadas expostas como cores.

Estas fronteiras reduzem o risco de a V01 parecer um sistema funcional só porque
seu JSON passa. Para avançar, revise [testes e aceite](TESTES_E_ACEITE.md).
