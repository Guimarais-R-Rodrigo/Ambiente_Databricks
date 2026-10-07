# Identidade visual — contrato central do Sistema de Temas

O Sistema de Temas valida configurações e permite aplicação explícita por consumidor. É um padrão transversal customizado do Hub: não muda automaticamente notebooks, não altera temas do workspace e não concede aprovação ou publicação. As APIs legadas permanecem o padrão.

- [Conferir e aplicar uma proposta](GUIA_OPERACIONAL.md)
- [Corrigir uma mensagem de erro](ERROS.md)
- [Integrar o núcleo `visual.tema`](../../hub_snippets/visual/tema/README.md)
- [Experimentar no laboratório](../../hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md)
- [Usar o App de autoria](databricks_app/GUIA_PRIMEIRO_USO.md)
- [Preparar um candidato AI/BI](aibi/GUIA_PRIMEIRO_USO.md)

## Fonte única e promoção

[`theme.schema.json`](theme.schema.json) define os campos e limites do contrato 0.1.0. A [referência de tokens](TOKENS.md) é uma projeção documental gerada. Os arquivos em `exemplos/` são referências de demonstração, não identidades aprovadas. Prepare uma cópia em memória ou em pasta autorizada; não edite os recursos empacotados.

[`assets.json`](assets.json) contém caminhos relativos à raiz `.assistant` e hashes de integridade. O núcleo confere os recursos, sem recolorir imagens. Aprovação permanece externa ao JSON: contrato válido não é permissão.

## Representação e limites

Aceita somente UTF-8 sem BOM, até 131.072 bytes e 12 níveis. Campos desconhecidos,
chaves repetidas, números não finitos, ciclos, herança e referências externas são
recusados. Cada contexto tem configuração completa: notebook, readme ou presentation.
O App gerencia propostas `notebook`; `context="app"` não é válido. A ponte AI/BI também recebe `ResolvedTheme` `notebook`; `context="aibi"` continua reservado. Sua matriz distingue correspondências traduzidas, aproximadas e não suportadas, sem criar outro contexto no schema.

Cores no contrato são `#RRGGBB` em maiúsculas, sem transparência ou espaços.
`normalize_color` pode converter minúsculas explicitamente durante a autoria;
nenhuma proposta é corrigida automaticamente na importação.

O formato `hub-json-v1` ordena chaves, mantém listas na ordem original, usa UTF-8,
separadores compactos, uma quebra de linha final e converte números fracionários
exatamente inteiros em inteiros. Não remove acentos nem normaliza textos.
Não é uma declaração de conformidade com RFC 8785. Dois JSONs com diferente
indentação podem ter conteúdo canônico igual, mas hashes de bytes diferentes.

`raw_sha256` identifica bytes originais; `content_sha256` identifica a exportação
canônica; `fingerprint` também incorpora schema, manifesto, API 1.0.0 e serialização.
Hashes são identificação/integridade, não autenticação, assinatura ou aprovação.
A origem de cada token é o documento completo; não existem defaults injetados.

## Dependências e efeitos

O import do núcleo não carrega Spark, Plotly, MLflow ou Streamlit. `jsonschema` e `referencing`
são dependências declaradas para validar, importadas na chamada. Não há instalação
automática, acesso à rede, escrita ou cache. A pasta do pacote é resolvida pelo
arquivo do módulo, não pelo diretório de trabalho nem pela proposta recebida.

O App possui [dependências próprias de interface](databricks_app/requirements.txt); isso não altera as dependências do núcleo nem faz Streamlit virar requisito de quem apenas importa `hub_snippets.visual.tema`. A ponte AI/BI não usa Databricks SDK/REST/CLI: a projeção e o binder trabalham somente com objetos/bytes locais e recusam inventar o schema nativo de `Import theme`.

Leia o [guia operacional](GUIA_OPERACIONAL.md) antes de executar o exemplo.
A [coleção de padrões](../README.md) e o [Manual Técnico](../../MANUAL_TECNICO_V2.md#catalogo-helpers)
continuam sendo as entradas gerais. A publicação e sua homologação são gates
separados; a existência do pacote não oferece, por si só, autorização para alterar tema de workspace, importar tema ou publicar dashboard.

## Versões que não devem ser confundidas

O contrato visual JSON está em **0.1.0**; ele define campos e limites. O contrato
editorial dos READMEs está em **1.0.0**; ele organiza como explicar cada objeto.
A compatibilidade da API do resolvedor usa **1.0.0**. São identificadores de
contratos distintos, não indicação de que a instalação foi aprovada ou publicada.
