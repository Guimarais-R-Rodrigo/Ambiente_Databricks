# Hub README Visual Assets

> **CONTEÚDO CUSTOMIZADO PELO HUB** — esta pasta não é uma estrutura nativa da
> Databricks e não é descoberta automaticamente pela Genie Code.

Este diretório reúne exclusivamente os recursos visuais editoriais usados pelos
READMEs do ecossistema. Ele existe para conciliar precisão informativa,
manutenção reproduzível e acabamento visual adequado a apresentações.

## Organização

```text
hub_readmes_visual_assets/
├── README.md
├── manifest.yaml
├── visual_system/
└── readmes/
    ├── raiz/
    ├── assistant/
    ├── snippets/
    ├── scripts/
    ├── skills/
    └── prompts/
```

Dentro de cada conjunto:

- `sources/` contém SVGs editáveis;
- `png/` contém os arquivos publicados e referenciados nos READMEs.

Não edite o PNG para alterar conteúdo. Modifique a definição correspondente em
`tools/render_readme_visuals.mjs`, regenere o conjunto e revise o resultado.

## Qualidade editorial

Um recurso visual só deve permanecer se tornar uma relação, sequência,
hierarquia ou decisão mais clara. Ao mesmo tempo, precisa ter acabamento bonito,
coeso e estiloso: estes READMEs também serão usados para apresentar o trabalho a
outras pessoas. Impacto visual não significa decoração; significa hierarquia,
contraste, ritmo e síntese trabalhando a favor da informação.

O texto ao redor da figura continua sendo o contrato semântico. Assim, leitores
com tecnologias assistivas e a própria Genie Code não dependem da interpretação
do PNG para encontrar a informação essencial.
