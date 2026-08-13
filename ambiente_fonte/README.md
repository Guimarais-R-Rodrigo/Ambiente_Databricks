# ambiente_fonte — o produto (fonte editável)

Este diretório é a **única cópia editável** do ecossistema `.assistant` do Genie
Code (regra `.claude/rules/fonte-de-verdade.md`). Origem: cópia da entrega
auditada do Codex (`Ajustes_Codex/assistant_optimized_2026-08-13/`, congelada);
toda evolução acontece aqui, com trilha no `CHANGELOG.md` da raiz.

## Conteúdo

```text
ambiente_fonte/
├── .assistant_instructions.md    # NATIVO: instruções pessoais (≤ 20.000 chars)
└── .assistant/
    ├── README.md                 # guia completo do ecossistema (instalação, uso, testes)
    ├── skills/                   # NATIVO: 12 Agent Skills rodrigo-*
    └── x_prompts | x_projects | x_snippets | x_scripts | x_docs | x_config
                                  # CUSTOM: extensões manuais (@/import/execução)
```

O guia detalhado de instalação, invocação das skills e solução de problemas está
em [.assistant/README.md](.assistant/README.md).

## Regras de edição

1. Valide antes de commitar: `python tools/validate_assistant.py`.
2. Regenere o simulado após aprovar: `python tools/render_simulado.py --write`.
3. Nunca insira identificadores corporativos, paths reais ou PII (placeholders).
4. Skills novas seguem `.assistant/x_docs/SKILL_TEMPLATE.md` e o padrão
   Agent Skills (frontmatter `name` + `description`).
