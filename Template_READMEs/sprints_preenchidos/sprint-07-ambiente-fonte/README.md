<a id="ambiente_fonte-produto-editável"></a>

# `ambiente_fonte/` — produto editável

Esta é a única cópia editável do conteúdo que será implantado no Databricks.
Use este README para **manter o pacote**. Para usar o ambiente já publicado,
abra o [guia do `.assistant`](../sprint-02-assistant/README.md).

> **Regra de ouro:** edite aqui; gere o simulado; publique; confira o remoto.
> Uma correção feita diretamente no workspace será substituída na próxima
> publicação.

> **Rascunho de sprint 7 — não publicado.** Destino previsto: `ambiente_fonte/README.md`.

---

<a id="como-as-cópias-do-projeto-se-relacionam"></a>

## Como as cópias do projeto se relacionam

**Canônico** é o que se edita: `ambiente_fonte/`. **Derivado** é o espelho gerado
em `Novo_Ambiente_Simulado/` — não se edita à mão. **Publicado** é o workspace
(laboratório Free ou destino controlado).

Exemplo: você corrige uma frase em `.assistant/README.md`. O renderer copia esse guia e a árvore `.assistant/`, além de `.assistant_instructions.md`. Sem regenerar e publicar, o workspace não recebe a correção. Já **este arquivo**, `ambiente_fonte/README.md`, e o README da raiz são documentação do repositório: não integram o pacote publicado. Commit e push podem compartilhar essa documentação sem uma publicação Databricks.

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

<a id="o-que-existe-aqui"></a>

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

<a id="alterar-do-começo-ao-fim"></a>

## Alterar do começo ao fim

<a id="antes-de-editar"></a>

### Antes de editar

Identifique o arquivo **nesta** árvore. Não abra o simulado para “corrigir
rápido”. Se a mudança altera comportamento Python, planeje teste; se só prosa,
ainda rode o validador de links.

<a id="fluxo"></a>

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

Antes de autorizar publicação, confira a autenticação com a CLI e o destino declarado; estes comandos não devem ser colados com `<free>` ou `<url-free>` literais. O bloco é um roteiro, não uma autorização para publicar. `--verify` lê o remoto e exige autenticação, mesmo sem alterá-lo.

Depois, conforme o impacto: smoke (Python/Spark/ML), forward tests (`name` /
`description` / fronteira de skill), changelog, commit. Validação estática **não**
substitui Spark nem chat.

Exemplo guiado — só prosa: localizar a frase, alterar, validar links, regenerar,
olhar o diff do simulado. Exemplo contrastante — algoritmo: além disso, testes
da biblioteca e, se tocado, smoke. Não execute publicação só porque leu este
parágrafo.

<a id="como-decidir-quais-testes-repetir"></a>

### Como decidir quais testes repetir

| Mudança | Gate |
|---|---|
| helper / Spark / ML | smoke no runtime |
| skill name/description | forward P, N, `@` |
| contrato de prompt | resposta real + registro no exemplo |
| só governança fora do produto | validador local |

---

<a id="limites"></a>

## Limites

Editar o derivado é perda na próxima regeneração: use a fonte. Credenciais no
Git vazam para qualquer clone: use placeholders. Tratar `hub_` como nativo faz
a equipe esperar descoberta que não existe. Resultado do Free não homologa o
trabalho: runtime, UC e ACL são outros. Skill nova segue
[template](../../../ambiente_fonte/.assistant/hub_padroes/skill/template.md) e precisa de roteamento.

---

<a id="onde-continuar"></a>

## Onde continuar

| Objetivo | Documento |
|---|---|
| usar o Hub | [Guia do `.assistant`](../sprint-02-assistant/README.md) |
| helper | [Catálogo](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md) |
| criar objeto | [Padrões](../sprint-08-padroes/README.md) |
| publicar / replicar | [Playbooks](../../../docs/playbooks/README.md) |

<a id="correção-textual-acompanhada"></a>

### Correção textual acompanhada

Na raiz do checkout, abra `ambiente_fonte/.assistant/README.md` e modifique somente a frase acordada. `git diff -- ambiente_fonte/.assistant/README.md` deve exibir apenas essa edição. Rode o gate local; gere o derivado apenas na etapa autorizada e confira `git diff -- Novo_Ambiente_Simulado`. Uma mudança de fonte sem diferença no arquivo derivado correspondente pede investigação do caminho, não edição manual do simulado.

Para esta rodada de rascunhos, o procedimento é diferente: `python tools/review_readmes.py` confere os caminhos de staging e os destinos virtuais. A opção `--export` gera um pacote de revisão fora dos caminhos oficiais. Ela não promove, não renderiza o simulado e não chama Databricks.
