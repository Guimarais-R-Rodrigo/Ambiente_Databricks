# Skills operacionais deste repositório

Playbooks executáveis para trabalhar NO repositório (não confundir com as Agent
Skills do produto, que vivem em `ambiente_fonte/.assistant/skills/`).

| Skill | Faz o quê | Status |
|---|---|---|
| `validar-assistant` | Bateria de validação do `ambiente_fonte/` | ✅ ativa |
| `render-simulado` | Gera `Novo_Ambiente_Simulado/` a partir do fonte | ✅ ativa |
| `publicar-free` | Publica no Databricks Free via engine do Hub | ⏳ fase 3 |
| `forward-test-skills` | Roteiro de testes das 12 skills no Genie Code | ✅ ativa |
| `replicar-trabalho` | Runbook de cópia manual para o workspace do trabalho | ⏳ fase 4 |
| `revisar-docs-oficiais` | Revisão periódica da documentação oficial (vanguarda) | ⏳ fase 4 |

Convenção: cada skill tem pasta própria com `SKILL.md` (frontmatter `name` +
`description`), scripts ficam em `tools/` na raiz do repo e são referenciados
pelo caminho relativo.
