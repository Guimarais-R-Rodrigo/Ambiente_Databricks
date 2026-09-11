# `ambiente_fonte/` — produto editável

Esta é a única cópia editável do conteúdo que será implantado no Databricks.
Use este README para **manter o pacote**. Para usar o ambiente já publicado,
abra o [guia do `.assistant`](.assistant/README.md).

> **Regra de ouro:** edite aqui; gere o simulado; publique; confira o remoto.
> Uma correção feita diretamente no workspace será substituída na próxima
> publicação.

> **Rascunho de sprint 7 — não publicado.** Destino previsto: `ambiente_fonte/README.md`.

---

## Como as cópias do projeto se relacionam

O título anterior “Em 30 segundos” prometia tempo de leitura. Esta seção explica
as três cópias, sem relógio.

**Canônico** é o que se edita: `ambiente_fonte/`. **Derivado** é o espelho gerado
em `Novo_Ambiente_Simulado/` — não se edita à mão. **Publicado** é o workspace
(laboratório Free ou destino controlado).

Exemplo: você corrige uma frase neste README. Sem regenerar o derivado, o
simulado e o workspace continuam com o texto velho. Sem publicar, só a máquina
local vê a correção.

| Camada | Finalidade | Pode editar? |
|---|---|---:|
| `ambiente_fonte/` | produto neutro e versionado | **sim** |
| `Novo_Ambiente_Simulado/` | espelho da árvore de workspace | **não** |
| workspace Free | teste operacional | não; recebe publicação |
| workspace do trabalho | consumo governado | não; recebe pacote aprovado |

Separar as camadas evita identidade pessoal no Git e impede duas fontes
concorrentes. Detalhes de transporte corporativo não cabem neste guia de
manutenção local.

---

## O que existe aqui

```text
ambiente_fonte/
├── .assistant_instructions.md    # NATIVO: instruções pessoais
└── .assistant/
    ├── README.md                 # guia de uso no Databricks
    ├── GLOSSARIO.md
    ├── CATALOGO_HELPERS.md
    ├── skills/                   # NATIVO: Agent Skills
    ├── hub_prompts/              # HUB: briefings manuais
    ├── hub_snippets/             # HUB: biblioteca, import manual
    ├── hub_scripts/              # HUB: diagnósticos, execução manual
    ├── hub_padroes/              # HUB: moldes
    └── hub_readmes_visual_assets/# HUB: figuras e cabeçalhos dos READMEs
```

`NATIVO` = estrutura reconhecida pela Genie Code. `HUB` = conteúdo deste
projeto. Skills `hub-ml-*` usam o mecanismo nativo com conteúdo nosso.
`hub_readmes_visual_assets` não é descoberta automática nem sexto componente
analítico.

| Pasta | Quem consome | Ação de uso | Quem mantém |
|---|---|---|---|
| `skills/` | Genie Code | relevância ou `@` | edição de `SKILL.md` aqui |
| `hub_snippets/` | notebook | import | módulo + exemplo + teste |
| `hub_scripts/` | notebook | import | idem |
| `hub_prompts/` | pessoa no chat | copiar briefing | `.md` + exemplo |
| `hub_padroes/` | autor de objeto | consultar/anexar | templates |
| assets visuais | leitores dos READMEs | ver PNG | compositor no repositório |

---

## Alterar do começo ao fim

### Antes de editar

Identifique o arquivo **nesta** árvore. Não abra o simulado para “corrigir
rápido”. Se a mudança altera comportamento Python, planeje teste; se só prosa,
ainda rode o validador de links.

### Fluxo

Na **raiz do repositório** (não dentro de `ambiente_fonte/`):

```powershell
python tools/validate_assistant.py
python tools/render_simulado.py --write
python tools/publicar_free.py --execute --profile <free> --expected-host <url-free>
python tools/publicar_free.py --verify  --profile <free> --expected-host <url-free>
```

| Comando | O que modifica | Quando parar |
|---|---|---|
| `validate_assistant.py` | nada (lê) | qualquer FAIL |
| `render_simulado.py --write` | pasta do simulado | diff inesperado |
| `--execute` | workspace Free | destino ≠ laboratório |
| `--verify` | nada | ausente, obsoleto, tipo ou conteúdo |

`--write` é obrigatório para atualizar o derivado. Sem ele, o comando só mostra
o plano. `--verify` é obrigatório porque overwrite não apaga obsoleto.

Depois, conforme o impacto: smoke (Python/Spark/ML), forward tests (`name` /
`description` / fronteira de skill), changelog, commit. Validação estática **não**
substitui Spark nem chat.

Exemplo guiado — só prosa: localizar a frase, alterar, validar links, regenerar,
olhar o diff do simulado. Exemplo contrastante — algoritmo: além disso, testes
da biblioteca e, se tocado, smoke. Não execute publicação só porque leu este
parágrafo.

### Como decidir quais testes repetir

| Mudança | Gate |
|---|---|
| helper / Spark / ML | smoke no runtime |
| skill name/description | forward P, N, `@` |
| contrato de prompt | resposta real + registro no exemplo |
| só governança fora do produto | validador local |

---

## Limites

Editar o derivado é perda na próxima regeneração: use a fonte. Credenciais no
Git vazam para qualquer clone: use placeholders. Tratar `hub_` como nativo faz
a equipe esperar descoberta que não existe. Resultado do Free não homologa o
trabalho: runtime, UC e ACL são outros. Skill nova segue
[template](.assistant/hub_padroes/skill/template.md) e precisa de roteamento.

---

## Onde continuar

| Objetivo | Documento |
|---|---|
| usar o Hub | [Guia do `.assistant`](.assistant/README.md) |
| helper | [Catálogo](.assistant/CATALOGO_HELPERS.md) |
| criar objeto | [Padrões](.assistant/hub_padroes/README.md) |
| publicar / replicar | [Playbooks](../docs/playbooks/README.md) |
