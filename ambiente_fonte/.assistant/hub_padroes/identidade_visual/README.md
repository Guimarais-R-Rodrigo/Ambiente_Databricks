# Identidade visual — contrato central do Sistema de Temas

> **PADRÃO TRANSVERSAL DO HUB · V02–V09 INTEGRADAS NO GIT; V10 EM CANDIDATA.** Não é um novo tipo de objeto,
> configuração ativa de todos os notebooks nem autorização para implantar um App. Consumo e autoria continuam opt-in; nada muda silenciosamente na rotina legada.

Para começar, abra o [guia operacional](GUIA_OPERACIONAL.md). Para corrigir uma
mensagem, consulte [Erros e recuperação](ERROS.md). Para implementar um consumidor,
leia o [objeto `visual.tema`](../../hub_snippets/visual/tema/README.md). Para a superfície de App V10 ainda candidata, use o [guia do Databricks App](databricks_app/README.md).

**Estado vigente no Git:** V02 integrou o núcleo de carga/validação/resolução; V03 o adaptador Plotly; V04 componentes HTML/tabela; V05 o Visual Lab de autoria; V06 a geração editorial orientada por tema; V07 consumidores runtime e formatos exercitados; V08 alinhou as superfícies transversais; V09 integrou o contrato mínimo de temas ao kit de transição. `ResolvedTheme` permanece a fonte efetiva para consumo configurável e as APIs legadas continuam o default. A V10 está sendo desenvolvida separadamente como interface Databricks App para autoria/persistência, sem aceite, merge ou deploy. Integração Git não equivale a publicação no workspace, homologação visual/runtime, acessibilidade ou aprovação de uma identidade.

## Fonte única e promoção

`theme.schema.json` é a fonte ativa dos campos e limites. Seus bytes foram
movidos da candidata V01 sem alterar o contrato 0.1.0; o título histórico dentro
do JSON foi preservado deliberadamente. O arquivo anterior foi removido da V01,
e o verificador de manutenção aponta a esta fonte, em vez de manter dois schemas.
A [referência de tokens](TOKENS.md) é gerada, nunca editada manualmente.

Os quatro arquivos em `exemplos/` são cópias derivadas das fixtures históricas
V01, verificadas por testes. Não devem ser editados independentemente nem usados
como sinal de aprovação de uma marca. Preservam o legado e exemplos contratuais;
para uma proposta, use uma cópia em memória ou em sua pasta autorizada.

`assets.json` é o manifesto empacotado derivado do registro V01: conserva os hashes
e converte caminhos para relativos à pasta `.assistant`. O núcleo confere os
recursos referenciados, não altera imagens. A governança de aprovação continua
fora do JSON do tema, conforme ADR-0013. Contrato válido não é permissão.

## Representação e limites

Aceita somente UTF-8 sem BOM, até 131.072 bytes e 12 níveis. Campos desconhecidos,
chaves repetidas, números não finitos, ciclos, herança e referências externas são
recusados. Cada contexto tem configuração completa: notebook, readme ou presentation.
Não há contexto temático App ou AI/BI implementado nesta versão. A existência da interface V10 não muda essa fronteira: o App candidato gerencia propostas `notebook`; ele não torna `context="app"` válido.

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

## Manutenção e efeitos

O import do núcleo não carrega Spark, Plotly, MLflow ou Streamlit. `jsonschema` e `referencing`
são dependências declaradas para validar, importadas na chamada. Não há instalação
automática, acesso à rede, escrita ou cache. A pasta do pacote é resolvida pelo
arquivo do módulo, não pelo diretório de trabalho nem pela proposta recebida.

A V10 candidata possui dependências próprias de interface em `databricks_app/requirements.txt`; isso não altera as dependências do núcleo nem faz Streamlit virar requisito de quem apenas importa `hub_snippets.visual.tema`.

Leia o [guia operacional](GUIA_OPERACIONAL.md) antes de executar o exemplo.
A [coleção de padrões](../README.md) e o [Manual Técnico](../../MANUAL_TECNICO.md#catalogo-helpers)
continuam sendo as entradas gerais. A publicação e sua homologação são gates
separados; V00–V09 integradas no Git e a existência de uma candidata V10 não oferecem, por si só, comando ou autorização para publicar ou implantar um tema/App.

## Versões que não devem ser confundidas

O contrato visual JSON está em **0.1.0**; ele define campos e limites. O contrato
editorial dos READMEs está em **1.0.0**; ele organiza como explicar cada objeto.
A compatibilidade da API do resolvedor usa **1.0.0**. São identificadores de
contratos distintos, não indicação de que a instalação foi aprovada ou publicada.
