# Plano de sprints — READMEs preenchidos a partir dos templates

> Material de rascunho editorial. **Não publicar no Databricks.** Não substitui
> os READMEs em `ambiente_fonte/` até aprovação humana e cópia deliberada.

Fonte normativa: [`../README.md`](../README.md) (guia de tom, fichas e critérios).
Cada sprint abaixo produz **um** README, alinhado a um template e a um documento
de origem. Os arquivos prontos (sem notas ao autor) ficam nesta pasta.

## Fio condutor compartilhado

Campanha fictícia de CRM, **sintético**: eventos de envio e resposta. Serve para
ensinar; não é dado da organização.

| Artefato didático | Papel |
|---|---|
| `event_id` | chave candidata da linha |
| `id_cliente` | entidade |
| `dt_evento` | eixo temporal |
| `respondeu` | indicador 0/1 |
| `valor_gasto` | valor associado ao evento |

Cada guia responde a **uma** pergunta. Quem abre só um deles encontra o
pré-requisito necessário, sem obrigação de ler os outros.

## Ordem das sprints

| Sprint | README destino | Template | Pergunta que o guia responde | Arquivo desta pasta |
|---|---|---|---|---|
| 1 | `README.md` (raiz do repositório) | `README_raiz.md` | Quais peças existem e onde manter o produto? | `sprint-01-raiz/README.md` |
| 2 | `ambiente_fonte/.assistant/README.md` | `README_assistant.md` | Como faço a primeira tarefa no workspace? | `sprint-02-assistant/README.md` |
| 3 | `hub_snippets/README.md` | `README_snippets.md` | Como reutilizo uma implementação com contrato? | `sprint-03-snippets/README.md` |
| 4 | `hub_scripts/README.md` | `README_scripts.md` | Como diagnostico um recurso e leio o veredito? | `sprint-04-scripts/README.md` |
| 5 | `skills/README.md` | `README_skills.md` | Como aplico um método com a Genie Code? | `sprint-05-skills/README.md` |
| 6 | `hub_prompts/README.md` | `README_prompts.md` | Como formulo a demanda sem inventar dados? | `sprint-06-prompts/README.md` |
| 7 | `ambiente_fonte/README.md` | `README_ambiente_fonte.md` | Onde edito e como levo uma correção até o derivado? | `sprint-07-ambiente-fonte/README.md` |
| 8 | `hub_padroes/README.md` | `README_padroes.md` | Como crio um objeto novo sem inventar formato? | `sprint-08-padroes/README.md` |
| 9 | `hub_readmes_visual_assets/README.md` | `README_visual_assets.md` | Como uso ou mantenho uma figura sem cópia divergente? | `sprint-09-visual-assets/README.md` |
| 10 | `headers/README.md` | `README_cabecalhos.md` | Qual banner usar e como inseri-lo? | `sprint-10-cabecalhos/README.md` |

## Regras desta rodada

- Títulos e subtítulos da origem foram preservados, salvo correção pontual
  justificada no próprio arquivo (ex.: “Em 30 segundos” → título descritivo).
- Caminhos de imagem estão no formato do **destino final**, não desta pasta.
- Placeholders `{{...}}` e notas ao autor foram removidos.
- Nenhuma publicação, render de simulado, commit ou alteração dos READMEs
  canônicos foi feita nesta etapa.

## Como promover depois da aprovação

1. Revisar o rascunho da sprint.
2. Copiar para o caminho de origem correspondente.
3. Validar (`python tools/validate_assistant.py`).
4. Regenerar o simulado.
5. Só então publicar, se autorizado.

Não use `git add .`. Não apague `READMEs_refeitos/` neste passo.
