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

Username padrão do render: o placeholder neutro `usuario-free`. Não persista
username real no simulado; o publicador e o runbook mapeiam o pacote para o
destino escolhido no momento da implantação (ADR-0009).

## O que o render produz

```text
Novo_Ambiente_Simulado/
└── Users/usuario-free/
    ├── .assistant_instructions.md
    └── .assistant/
        ├── skills/hub-ml-*/...
        └── hub_*/...
```

Cópia fiel byte a byte (sem headers injetados), para que a replicação no
trabalho seja literalmente copiar a subárvore.

## Regras

- Rodar `validar-assistant` ANTES do render; nunca renderizar fonte inválido.
- `Novo_Ambiente_Simulado/` é derivado: nunca editar à mão (regra
  `fonte-de-verdade.md`).
- Registrar o re-render no CHANGELOG junto da mudança que o motivou.
