---
name: render-simulado
description: >-
  Regenera Novo_Ambiente_Simulado/ como espelho da árvore do workspace a partir
  de ambiente_fonte/. Use após qualquer edição aprovada no ambiente_fonte/ e
  antes de publicar no Free ou replicar no trabalho.
---

# Renderizar o ambiente simulado

## Executar

```powershell
python tools/render_simulado.py            # dry-run: mostra o plano
python tools/render_simulado.py --write    # apaga e regenera o simulado
```

Username padrão do render: o do Free Edition (definido no script; sobreponha com
`--username`). Para o trabalho, o runbook de replicação faz o mapeamento — não
renderize com o username corporativo (regra `free-vs-trabalho.md`).

## O que o render produz

```text
Novo_Ambiente_Simulado/
└── Users/<username>/
    ├── .assistant_instructions.md
    └── .assistant/
        ├── skills/rodrigo-*/...
        └── x_*/...
```

Cópia fiel byte a byte (sem headers injetados), para que a replicação no
trabalho seja literalmente copiar a subárvore.

## Regras

- Rodar `validar-assistant` ANTES do render; nunca renderizar fonte inválido.
- `Novo_Ambiente_Simulado/` é derivado: nunca editar à mão (regra
  `fonte-de-verdade.md`).
- Registrar o re-render no CHANGELOG junto da mudança que o motivou.
