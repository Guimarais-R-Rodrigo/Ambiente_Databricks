# Playbook — Ciclo de vida de uma mudança no ecossistema

Procedimento completo para alterar qualquer coisa em `ambiente_fonte/` e levá-la
até os workspaces. Diagrama resumido no `README.md` da raiz.

## 1. Editar

- Edite apenas `ambiente_fonte/` (regra `fonte-de-verdade.md`).
- Skills: mantenha frontmatter `name`+`description`, imperativo, progressive
  disclosure (detalhe grande vai para `templates/` da própria skill).
- Instruções: vigie o limite de 20.000 caracteres.

## 2. Validar

```powershell
python tools/validate_assistant.py
```

Só siga adiante com exit 0. `WARN` de tamanho: avalie progressive disclosure.

## 3. Renderizar

```powershell
python tools/render_simulado.py --write
```

## 4. Registrar

- Entrada no `CHANGELOG.md` (template `.claude/templates/changelog-entry.md`).
- Decisão estrutural → ADR; sessão interrompida → handoff.

## 5. Publicar no Free (fase 3 — via engine do Hub)

```powershell
# após pip install -e ../../Verg_Projects/Verg_Alchemy_Hub --no-deps
# manifesto fino deste projeto + wrappers (a criar na fase 3)
# padrão do engine: render (dry-run) → publish --execute → verify
```

Dry-run por padrão; `--execute` é gate consciente. Não sobrescrever a camada
global `global-*` do Hub.

## 6. Testar no Free

Para cada skill alterada, em **chat novo** do Genie Code:

1. caso positivo (pedido que deveria acionar a skill por relevância);
2. caso negativo (pedido parecido que NÃO deveria acionar);
3. `@menção` explícita.

Falha de auto-seleção → melhorar `description` e repetir. Registrar resultados.

## 7. Replicar no trabalho (fase 4 — runbook)

Cópia manual da subárvore `Novo_Ambiente_Simulado/Users/<username>/` para o
workspace do trabalho, com mapeamento de username. Detalhes no runbook da fase 4
(`.claude/skills/replicar-trabalho/`, a criar).
