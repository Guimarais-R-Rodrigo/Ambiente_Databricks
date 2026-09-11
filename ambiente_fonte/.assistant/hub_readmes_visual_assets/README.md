# Hub README Visual Assets

> **CONTEÚDO CUSTOMIZADO PELO HUB** — esta pasta não é uma estrutura nativa da
> Databricks e não é descoberta automaticamente pela Genie Code.

Este diretório reúne os recursos visuais editoriais dos READMEs e seus
cabeçalhos reutilizáveis em notebooks. O nome `hub_readmes_visual_assets` é
preservado como localização canônica. Ele concilia precisão informativa,
manutenção reproduzível e acabamento visual adequado a apresentações.

## Organização

```text
hub_readmes_visual_assets/
├── README.md
├── manifest.yaml
├── CONTEUDO_FIGURAS.md
├── headers/                  # identidade compartilhada por README e notebook
│   ├── README.md
│   ├── src/                  # arte-base raster + texto e camada tipográfica
│   └── png/                  # CRM e Squad, prontos para uso
├── specs/                    # contratos semânticos e microcopy das assinaturas
├── visual_system/
├── licenses/                 # Inter e Lucide
├── qa/                       # verificações e metadados de composição
└── readmes/
    ├── raiz/
    ├── assistant/
    ├── snippets/
    ├── scripts/
    ├── skills/
    └── prompts/
```

Dentro de cada conjunto:

- `sources/` contém SVGs gerados, com tipografia convertida em paths;
- `png/` contém os arquivos publicados e referenciados nos READMEs.

O código de composição é a fonte editável dos novos diagramas. As cinco
assinaturas aprovadas têm SVGs congelados, usados como entrada com hashes de
preservação. Alterações nesses casos exigem revisão explícita da assinatura,
não edição casual do arquivo. Em `headers/src/`, o fundo
original é raster, não vetor; `copy.json` contém o texto editável e os SVGs
tipográficos são apenas uma camada da composição.

## Cabeçalhos reutilizáveis

| Uso | Arquivo canônico |
|---|---|
| README ou notebook geral | [CRM](headers/png/cabecalho_crm.png) |
| Notebook específico da Squad | [Squad Modelos Analíticos e Preditivos](headers/png/cabecalho_squad.png) |

Use um único cabeçalho por documento, preservando o título e as instruções em
Markdown. Não copie esses PNGs para cada notebook: referencie a localização
compartilhada. O [guia de cabeçalhos](headers/README.md) contém exemplos e os
cuidados com caminhos relativos e acessibilidade.

## Como manter

A partir da raiz do repositório de autoria, com as dependências fixadas instaladas:

```powershell
node tools/readme_visuals/headers.mjs
node tools/readme_visuals/production.mjs --family all
node tools/readme_visuals/validate_production.mjs
python tools/validate_assistant.py
python tools/render_simulado.py --write
```

Os layouts ficam em `tools/readme_visuals/archetypes/`, apoiados por
`tools/readme_visuals/lib.mjs`. Os cinco PNGs de assinatura e os dois cabeçalhos
aprovados são preservados por hashes. Os contratos delimitam finalidade,
limites, legenda e consumidor; o [índice textual das figuras](CONTEUDO_FIGURAS.md)
permite conferir o conteúdo renderizado sem depender de OCR.

O manifesto lista os ativos vigentes, não os históricos. As versões anteriores
permanecem no histórico Git e no baseline de avaliação, fora deste pacote ativo.
No workspace, consuma os PNGs; a autoria e os gates pertencem ao repositório.

`tools/render_readme_visuals.mjs` e o renderer da Sprint 0 são ferramentas da
rodada anterior; não use esses comandos para regenerar o pacote v2.

## Qualidade editorial

Um recurso visual só deve permanecer se tornar uma relação, sequência,
hierarquia ou decisão mais clara. Ao mesmo tempo, precisa ter acabamento bonito,
coeso e estiloso: estes READMEs também serão usados para apresentar o trabalho a
outras pessoas. Impacto visual não significa decoração; significa hierarquia,
contraste, ritmo e síntese trabalhando a favor da informação.

O texto ao redor da figura continua sendo o contrato semântico. Assim, leitores
com tecnologias assistivas e a própria Genie Code não dependem da interpretação
do PNG para encontrar a informação essencial.
