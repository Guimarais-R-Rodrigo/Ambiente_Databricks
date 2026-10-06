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
│   └── png/                  # CRM e Squad, prontos para uso
├── specs/                    # contratos semânticos, microcopy e geração por tema
├── visual_system/
├── licenses/                 # Inter e Lucide
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
não edição casual do arquivo. Os insumos dos cabeçalhos ficam em
`tools/readme_visuals/assets/headers/src/` no repositório de manutenção: o fundo
original é raster, `copy.json` contém o texto editável e os SVGs tipográficos
são uma camada da composição. QA e metadados de composição ficam em
`tools/readme_visuals/qa/`; nenhum desses diretórios integra a instalação.

## Cabeçalhos reutilizáveis

| Uso | Arquivo canônico |
|---|---|
| README ou notebook geral | [CRM](headers/png/cabecalho_crm.png) |
| Notebook específico da Squad | [Squad Modelos Analíticos e Preditivos](headers/png/cabecalho_squad.png) |

Use um único cabeçalho por documento, preservando o título e as instruções em
Markdown. Não copie esses PNGs para cada notebook: referencie a localização
compartilhada. O [guia de cabeçalhos](headers/README.md) contém exemplos e os
cuidados com caminhos relativos e acessibilidade.

## Consumo e solicitação de mudança

Use os PNGs canônicos compartilhados; não crie cópias por notebook. Para mudar aparência, encaminhe a proposta ao mantenedor. Variante gerada continua candidata até revisão; não substitui automaticamente um asset aprovado. Assets congelados mantêm seus hashes e o [contrato de variantes](specs/theme_generation.yaml).

A geração e suas dependências pertencem ao [guia externo de manutenção do compositor](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/docs/ai-architecture-20261006/tools/readme_visuals/README.md), executado no checkout autorizado: revisar diff → validar → gerar o derivado. Gerar não publica por inferência.

## Ler as figuras por finalidade

O [equivalente textual das figuras](CONTEUDO_FIGURAS.md) preserva o que está nos pixels. Mapas, arquitetura de uso, catálogo e percursos de objetos ajudam o usuário. A seção [raiz.03_ciclo_de_vida](CONTEUDO_FIGURAS.md#raiz03_ciclo_de_vida) descreve o fluxo histórico de manutenção da figura; não é instrução para publicar depois de toda análise. O procedimento atual de autoria fica no repositório, separado do consumo. Não altere a transcrição para esconder que uma figura histórica descreve outro momento.

## Qualidade editorial

Um recurso visual só deve permanecer se tornar uma relação, sequência,
hierarquia ou decisão mais clara. Ao mesmo tempo, precisa ter acabamento bonito,
coeso e estiloso: estes READMEs também serão usados para apresentar o trabalho a
outras pessoas. Impacto visual não significa decoração; significa hierarquia,
contraste, ritmo e síntese trabalhando a favor da informação.

O texto ao redor da figura continua sendo o contrato semântico. Assim, leitores
com tecnologias assistivas e a própria Genie Code não dependem da interpretação
do PNG para encontrar a informação essencial.