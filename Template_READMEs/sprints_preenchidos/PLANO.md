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
| 1 | `README.md` (raiz do repositório) | `README_raiz.md` | Quais peças existem e onde manter o produto? | [Abrir rascunho](sprint-01-raiz/README.md) |
| 2 | `ambiente_fonte/.assistant/README.md` | `README_assistant.md` | Como faço a primeira tarefa no workspace? | [Abrir rascunho](sprint-02-assistant/README.md) |
| 3 | `hub_snippets/README.md` | `README_snippets.md` | Como reutilizo uma implementação com contrato? | [Abrir rascunho](sprint-03-snippets/README.md) |
| 4 | `hub_scripts/README.md` | `README_scripts.md` | Como diagnostico um recurso e leio o veredito? | [Abrir rascunho](sprint-04-scripts/README.md) |
| 5 | `skills/README.md` | `README_skills.md` | Como aplico um método com a Genie Code? | [Abrir rascunho](sprint-05-skills/README.md) |
| 6 | `hub_prompts/README.md` | `README_prompts.md` | Como formulo a demanda sem inventar dados? | [Abrir rascunho](sprint-06-prompts/README.md) |
| 7 | `ambiente_fonte/README.md` | `README_ambiente_fonte.md` | Onde edito e como levo uma correção até o derivado? | [Abrir rascunho](sprint-07-ambiente-fonte/README.md) |
| 8 | `hub_padroes/README.md` | `README_padroes.md` | Como crio um objeto novo sem inventar formato? | [Abrir rascunho](sprint-08-padroes/README.md) |
| 9 | `hub_readmes_visual_assets/README.md` | `README_visual_assets.md` | Como uso ou mantenho uma figura sem cópia divergente? | [Abrir rascunho](sprint-09-visual-assets/README.md) |
| 10 | `headers/README.md` | `README_cabecalhos.md` | Qual banner usar e como inseri-lo? | [Abrir rascunho](sprint-10-cabecalhos/README.md) |

## Estado desta revisão

Os dez rascunhos foram corrigidos para revisão humana. Os READMEs de uso em
`ambiente_fonte/`, a lógica dos helpers e o simulado não foram substituídos.
No README da raiz, somente as linhas numéricas da evidência do gate local
são atualizadas mecanicamente quando o inventário muda; isso não promove a redação candidata.

Links e imagens dos rascunhos agora resolvem **na pasta em que você os está
lendo no GitHub**. Não é necessário copiar imagens: todos apontam para os PNGs
canônicos em `ambiente_fonte/.assistant/hub_readmes_visual_assets/`.
O [mapping de destinos](mapping.json) permite converter os caminhos sem
adivinhar quantos níveis subir. Links escritos em exemplos de código continuam
representando o local explicitamente descrito no exemplo.

O [índice de revisão](README.md) abre os dez candidatos e indica a seção de
cada imagem. O gate também compara presença, ordem e posição com os READMEs
atuais, além de conferir caminhos e integridade dos PNGs.

## Como conferir antes de promover

Na raiz do repositório, execute:

```powershell
python tools/review_readmes.py
python tools/tests/test_readme_review.py
python tools/tests/test_readme_examples.py
python tools/ci_local.py
```

O primeiro comando verifica rascunhos e destinos virtuais, links, âncoras,
assinaturas diretas e imagens. O segundo testa os guardas. O terceiro executa
os exemplos portáveis e identifica os casos Spark não executados. O gate
integra os testes locais; nenhum deles instala bibliotecas ou publica no workspace.

O workflow específico de exemplos usa PySpark **local no GitHub Actions**, com
dependência explícita e dados sintéticos. Isso não homologa Databricks,
Spark Connect, ACL, conversas da Genie ou os treinadores opcionais.

## Exportação para revisão, sem promoção

```powershell
python tools/review_readmes.py --export .artifacts/readme-review/candidato
```

Use diretório novo. A ferramenta cria um snapshot isolado com caminhos finais;
não escreve nos READMEs oficiais, no simulado nem no workspace. Ela remove
somente o aviso de rascunho da cópia exportada. O staging preserva esse aviso.

Após aprovação humana, uma mudança separada pode copiar os dez READMEs do
snapshot para seus destinos do mapping, validar, regenerar e encaminhar
publicação autorizada. Não copie os rascunhos literalmente para a fonte sem
converter os links. Não use `git add .` e não promova o snapshot inteiro.
