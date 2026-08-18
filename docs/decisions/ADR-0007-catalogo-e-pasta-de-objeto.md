# ADR-0007 — O catálogo depois da pasta de objeto

- **Status:** Aceito
- **Data:** 2026-08-17
- **Supersede:** o ADR-0004 nos pontos de **localização e forma** — a decisão de
  fundo dele continua valendo, e é reafirmada abaixo.

## Contexto

O ADR-0004 decidiu, em 2026-08-14, que os helpers seriam **declarados
explicitamente** em cada `SKILL.md`, com um catálogo central de demanda → helper.
A decisão está certa e não muda: o Genie Code não descobre `hub_snippets`
sozinho, e uma skill que não declara o helper transfere para a pessoa a tarefa de
adivinhar que ele existe.

O que envelheceu foi tudo em volta dela. O ADR-0004 é imutável, e por isso não
pode ser corrigido — descreve corretamente o repositório de 14/08, e continua
sendo o registro de por que a declaração explícita existe.

Três afirmações dele deixaram de descrever o repositório:

| ADR-0004 dizia | Hoje |
|---|---|
| "54 helpers curados (47 módulos em `x_snippets/`, 7 em `x_scripts/`)" | **58**: 51 em `hub_snippets/`, 7 em `hub_scripts/` |
| catálogo em `ambiente_fonte/.assistant/x_docs/catalogo_helpers.md` | `.assistant/CATALOGO_HELPERS.md` — a pasta `x_docs/` foi removida na Sprint 2 |
| helper é um **módulo** | helper é uma **pasta de objeto**: `__init__.py`, o módulo e o notebook que o ensina |

A terceira é a que muda a natureza da coisa, não só o caminho.

## Decisão

**1. A declaração explícita de helpers em cada `SKILL.md` permanece**, por
caminho de import pontilhado — `hub_snippets.spark.pit_join`. A forma pontilhada
foi escolhida por ser imune à conversão para pasta de objeto, e sobreviveu a ela:
as 13 skills atravessaram cinco sprints de conversão sem uma edição.

**2. O catálogo é `.assistant/CATALOGO_HELPERS.md`**, publicado com o produto, e
tem uma coluna de dependência com três estados:

| Marca | Significa |
|---|---|
| — | sem dependência além do runtime; funciona no Free e no trabalho |
| `opt` | dependência opcional exigida no import; o módulo não importa sem ela |
| `exec` | dependência exigida **na chamada**: o import passa e o erro só aparece no uso |

O terceiro estado existe porque a biblioteca tem dois casos dele —
`explainability_report` com `tabulate` e `dataframe_styled` com `jinja2` —, e
nenhuma análise de import de topo os encontra.

**3. O catálogo cobre os 58, sem exceção.** Objeto ausente do catálogo é
indescobrível pela rota que o README recomenda, e isso já aconteceu: dois objetos
ficaram fora dele por uma sprint inteira.

**4. Helper é pasta, não arquivo.** Todo helper tem `__init__.py` gerado por
`tools/api_publica.py`, o módulo com o nome da pasta, e um `exemplo_<nome>.py`
que o ensina. O `__init__.py` reexporta **todos** os nomes públicos, sem
curadoria.

## Consequências

**Positivas.** O catálogo passou a ser conferível por script: comparar as pastas
de objeto com as linhas do catálogo é uma varredura de segundos, e foi assim que
os dois ausentes apareceram. A coluna `exec` dá nome a uma classe de defeito que
antes não tinha.

**Negativas.** Manter o catálogo em dia é trabalho manual, e nenhum portão o
cobra — o `check_pastas_de_objeto` confere a forma da pasta, não a presença no
catálogo. É a lacuna conhecida mais provável de reincidir, e está declarada no
checklist canônico e na skill `hub-ml-criar-objeto`.

**Neutra.** A numeração dos helpers vai continuar mudando. Este ADR evita citar
o total no corpo das decisões justamente por isso: quem quiser o número roda
`python tools/validate_assistant.py`.

## Alternativas descartadas

**Editar o ADR-0004.** ADR aceito é imutável; corrigi-lo apagaria o registro de
que a decisão foi tomada quando o repositório era outro, e essa é metade da
informação.

**Gerar o catálogo automaticamente a partir dos docstrings.** Produziria um
índice de API, não um mapa de demanda. A coluna que importa — "preciso fazer X,
qual módulo uso?" — não está no código, está na cabeça de quem escreveu.

## Referências

- ADR-0004, superseded nos pontos de localização e forma
- ADR-0006, que renomeou `x_*` para `hub_*`
- `PLANO_HUB.md` §12.1 e §12.2, dívidas declaradas
- `.assistant/skills/hub-ml-criar-objeto/`, que faz cumprir esta forma
