# Plano de reestruturação — de ambiente pessoal a Hub de equipe

Documento de trabalho. Cada sprint é executada isoladamente, revisada e só então
a seguinte começa. O objetivo desta divisão é que nenhuma sprint dependa de uma
decisão que ainda não foi tomada.

- **Status:** aguardando aprovação do plano
- **Sprint atual:** nenhuma iniciada
- **Última atualização:** 2026-08-16

---

## 1. O que muda, em uma página

| Dimensão | Hoje | Depois |
|---|---|---|
| Marca do que é customizado | prefixo `x_` | prefixo **`hub_`** |
| Identidade do projeto | ambiente pessoal | **Hub** de ML da equipe |
| Nome das skills | `rodrigo-<tema>` | **`hub_ml-<tema>`** |
| Organização de um snippet | um `.py` solto numa pasta temática | **uma pasta por snippet**, com o `.py` e um notebook que o demonstra |
| Organização de script e prompt | idem | idem |
| Contexto de projeto | `x_projects/` | **removida** |
| Documentação avulsa | `x_docs/`, `x_config/` | **removidas**, conteúdo útil realocado |
| Padrão de README | cada um com uma cara | **template único**, com exemplo de referência |
| Criação de novos objetos | manual, sem padrão | **skill que aplica os templates** |

O princípio que organiza tudo: **quem bate o olho na árvore de pastas deve
entender o que é da plataforma e o que é nosso, sem ler README nenhum.** O `x_`
exigia uma legenda; o `hub_` carrega o significado no próprio nome.

---

## 2. Decisões que preciso de você antes da Sprint 1

Três pontos mudam o desenho e não quero adivinhar.

### 2.1 O caractere `_` no nome da skill

`hub_ml-eda-profissional` mistura underscore e hífen. O padrão Agent Skills e o
Genie Code podem restringir o conjunto de caracteres do campo `name` — e o nome
da pasta precisa ser idêntico a ele. Se houver restrição a `[a-z0-9-]`, as 12
skills quebram de uma vez.

Isso é verificável em quinze minutos no laboratório, e é a primeira coisa da
Sprint 0. As opções, em ordem de preferência caso o underscore não passe:

| Opção | Exemplo | Observação |
|---|---|---|
| A — como você pediu | `hub_ml-eda-profissional` | preferida; sujeita à verificação |
| B — só hífens | `hub-ml-eda-profissional` | seguro em qualquer implementação |
| C — sem o `ml` | `hub-eda-profissional` | mais curto; perde a marca de domínio |

**Não faço nada aqui até a verificação responder.** Se a opção A passar, seguimos
com ela.

### 2.2 Volume de notebooks

Uma pasta por objeto, cada uma com notebook, significa:

| Seção | Objetos | Notebooks a escrever |
|---|---:|---:|
| `hub_snippets` | 51 | 51 |
| `hub_scripts` | 7 | 7 |
| `hub_prompts` | 16 | 16 |
| **Total** | **74** | **74** |

São 74 notebooks didáticos, cada um com explicação prévia, código comentado,
execução real e leitura do resultado. É o que produz a qualidade que você quer, e
é também o item mais caro do plano — a maior parte do esforço total está aqui.

Duas restrições reais, que não são opinião:

1. **Quatorze módulos de `ml` dependem de biblioteca opcional.** Sete quebram já
   no import. No Free eles só executam com as versões fixadas instaladas na
   sessão, e `prophet_wrapper` não executa de jeito nenhum hoje. Os notebooks
   desses módulos existirão, mas alguns não terão saída executada — e vão dizer
   isso explicitamente em vez de fingir.
2. **Treze módulos são triviais** (`constants/emojis`, `visual/divider`,
   `visual/badge` e afins): uma constante ou uma função de três linhas que
   devolve HTML. Um notebook inteiro para cada um produz cerimônia sem
   aprendizado.

Minha recomendação para os treze triviais: **um notebook por pasta temática**
(um para `constants`, um para `visual`, um para `display`), mostrando todos os
helpers daquela pasta em sequência. Cada snippet mantém sua pasta e seu `.py`; o
que muda é que o notebook é compartilhado e o README da pasta aponta para a
célula certa. Cai de 13 notebooks para 3, sem perder explicação.

**Preciso do seu aval nisso.** Se preferir um notebook por snippet mesmo nos
triviais, faço — só quero que a escolha seja sua e não uma economia minha.

### 2.3 Onde vive o glossário

`x_docs/` sai, e nela mora o glossário — que é, segundo a própria auditoria, o
melhor documento do conjunto, e para o qual outros documentos remetem o leitor.
Proponho `.assistant/GLOSSARIO.md`, na raiz do ecossistema, em caixa alta para
saltar aos olhos ao lado do `README.md`. Alternativa: virar uma seção do
`.assistant/README.md`, o que engorda a porta de entrada em ~150 linhas.

---

## 3. Arquitetura alvo

```text
.assistant/
├── README.md                        # porta de entrada do Hub
├── GLOSSARIO.md                     # vindo de x_docs/
│
├── skills/                          # NATIVO — o Genie Code descobre sozinho
│   ├── README.md
│   ├── hub_ml-eda-profissional/
│   │   └── SKILL.md
│   ├── … (11 outras)
│   └── hub_ml-criar-objeto/         # NOVA: aplica os templates do Hub
│
├── hub_snippets/                    # biblioteca Python importável
│   ├── README.md
│   ├── spark/
│   │   ├── README.md
│   │   ├── pit_join/
│   │   │   ├── __init__.py          # preserva o caminho de import
│   │   │   ├── pit_join.py
│   │   │   └── exemplo_pit_join.py  # notebook executável
│   │   └── … (6 outros)
│   ├── ml/  constants/  visual/  display/  testing/
│   └── requirements-optional.txt
│
├── hub_scripts/                     # utilitários de diagnóstico
│   ├── README.md
│   └── quick_profile/
│       ├── quick_profile.py
│       └── exemplo_quick_profile.py
│
└── hub_prompts/                     # briefings prontos para colar
    ├── README.md
    └── eda_completa/
        ├── eda_completa.md
        └── exemplo_eda_completa.py
```

### 3.1 Como os imports continuam funcionando

Este é o detalhe técnico que decide se a reestruturação é indolor ou um desastre.

Hoje: `from x_snippets.spark.pit_join import pit_join`

Se `pit_join.py` virar `pit_join/pit_join.py`, o caminho natural passaria a ser
`hub_snippets.spark.pit_join.pit_join` — feio, e quebraria todas as 252
referências a `x_snippets` no repositório, mais o que a equipe já tiver escrito.

A solução é um `__init__.py` em cada pasta de snippet, reexportando a API:

```python
# hub_snippets/spark/pit_join/__init__.py
from .pit_join import pit_join

__all__ = ["pit_join"]
```

Com isso o import fica **exatamente igual ao de hoje**, trocado só o prefixo:

```python
from hub_snippets.spark.pit_join import pit_join
```

O notebook de exemplo mora na mesma pasta e nunca é importado — é publicado como
notebook, não como módulo.

### 3.2 Destino do conteúdo que sai

Nada de valor é descartado sem decisão explícita.

| Origem | Conteúdo | Destino |
|---|---|---|
| `x_docs/` | `glossario.md` | `.assistant/GLOSSARIO.md` |
| `x_docs/` | `catalogo_helpers.md` | **dissolvido** nos READMEs de seção — com uma pasta por objeto, cada README lista o que tem embaixo dele, e o catálogo central perde a razão de existir |
| `x_docs/` | 4 notebooks didáticos | viram o notebook de exemplo dos snippets que eles ensinam (`pit_join`, `psi_calculator`, `join_diagnostics`, `vintage_analysis`) |
| `x_docs/` | `SKILL_TEMPLATE.md` | `padroes/template_skill.md` |
| `x_docs/` | `ROADMAP_SKILLS.md`, `LEGACY_CONTEXT.md`, `skills_manifest.md`, manifesto de exportação | `docs/` na raiz do repositório — é governança, não produto; não precisa estar no workspace |
| `x_config/` | `mcp_servers.legacy.json` | **removido**. Contém uma lista vazia e o projeto não usa MCP |
| `x_config/` | aviso sobre `.mcp_servers.json` que a plataforma cria | uma nota no `README.md` do Hub e na regra `.claude/rules/genie-code-oficial.md`, onde já está |
| `x_projects/` | `AGENTS_TEMPLATE.md` | `padroes/template_agents.md` — vale como referência mesmo sem a pasta |
| `x_projects/` | ficha, exemplo e README | **removidos** |

---

## 4. Os templates

Ficam em `padroes/`, na raiz do repositório, versionados e fora do produto.
São a fonte que a skill de criação vai aplicar.

| Arquivo | Padroniza |
|---|---|
| `padroes/README.md` | o que é a pasta e como usar cada template |
| `padroes/template_readme.md` | estrutura de qualquer README do projeto |
| `padroes/exemplo_readme.md` | o template preenchido num tema fora do domínio |
| `padroes/template_snippet.md` | pasta de snippet: `.py`, `__init__.py` e notebook |
| `padroes/template_script.md` | pasta de script |
| `padroes/template_prompt.md` | pasta de prompt |
| `padroes/template_skill.md` | `SKILL.md`, com o que faz uma `description` rotear |
| `padroes/template_notebook.py` | esqueleto do notebook de exemplo |
| `padroes/template_agents.md` | `AGENTS.md` de projeto (herdado de `x_projects`) |

### 4.1 Estrutura proposta para o template de README

Sete seções fixas, em ordem obrigatória, com hierarquia de Markdown navegável
(`##` para seção, `###` para subtópico) e um bloco visual obrigatório por
documento — tabela, mermaid ou saída real.

| # | Seção | Responde | Obrigatória? |
|---|---|---|---|
| 1 | Título + frase de identidade | "o que é isto, em uma linha" | sim |
| 2 | Aviso de natureza | é nativo da plataforma ou é do Hub? | sim |
| 3 | Para que serve / quando usar | "isto resolve o meu problema?" | sim |
| 4 | Visão estrutural | diagrama ou árvore do que existe aqui | sim |
| 5 | Como usar — exemplo copiável | "me dá o comando" | sim |
| 6 | O que existe aqui | tabela do conteúdo, uma linha por item | sim, se houver filhos |
| 7 | Limites e armadilhas | "o que dá errado e não é óbvio" | sim |
| 8 | Perguntas frequentes | dúvidas reais de quem chega | quando houver ≥ 3 |
| 9 | Onde continuar | links para o próximo passo | sim |

Regras de escrita que o template carrega: um bloco visual por documento; termo
técnico definido no primeiro uso ou remetido ao glossário; nenhum número
codificado em prosa que envelheça sozinho; exemplo sempre copiável e testado; e a
distinção nativo × Hub visível em cada página.

### 4.2 Tema do exemplo

Um **conversor de medidas de receita culinária** — "duas xícaras de farinha em
gramas". Escolhido de propósito: qualquer pessoa entende o domínio em cinco
segundos, então toda a atenção do leitor sobra para a *estrutura* do documento,
que é o que o exemplo existe para ensinar. Um exemplo de crédito ou de safra
faria o contrário — o leitor estudaria o domínio e não repararia na forma.

O mesmo tema atravessa todos os templates, para que dê para comparar lado a lado:
o snippet `converter_medida`, seu notebook, seu prompt e o README da pasta.

---

## 5. As sprints

Ordenadas para que cada uma feche sozinha. As três primeiras não tocam em
conteúdo — preparam o terreno; as do meio são mecânicas e verificáveis; as
finais são de escrita.

| # | Sprint | Entrega | Peso | Depende de |
|---|---|---|---|---|
| 0 | Verificações de risco | relatório curto, zero mudança estrutural | leve | — |
| 1 | Templates e exemplo | pasta `padroes/` completa | médio | 0 (decisão de nome) |
| 2 | Renomeação `x_` → `hub_` | prefixo trocado, 3 pastas removidas | médio | 1 |
| 3 | Renomeação das skills | 12 skills `hub_ml-*` + README da pasta | médio | 0, 2 |
| 4 | `hub_scripts` reestruturada | 7 pastas + 7 notebooks + README | médio | 1, 2 |
| 5 | `hub_prompts` reestruturada | 16 pastas + 16 notebooks + README | médio | 1, 2 |
| 6 | `hub_snippets`: spark e testing | 8 pastas + 8 notebooks + README | pesado | 1, 2 |
| 7 | `hub_snippets`: ml sem dependência opcional | 16 pastas + 16 notebooks | pesado | 6 |
| 8 | `hub_snippets`: ml com dependência opcional | 14 pastas + 14 notebooks | pesado | 6 |
| 9 | `hub_snippets`: constants, visual, display | 13 pastas + 3 ou 13 notebooks | médio | 6 |
| 10 | READMEs de topo | `README.md` da raiz e do `.assistant` | médio | 2–9 |
| 11 | Skill de criação de objetos | `hub_ml-criar-objeto` | médio | 1, 10 |
| 12 | Auditoria e fechamento | rodada A1 externa + correções | médio | tudo |

### Sprint 0 — Verificações de risco

Nada é renomeado. Só se responde ao que pode inviabilizar o resto.

1. **O Genie Code aceita `_` no nome de uma skill?** Criar uma skill descartável
   `hub_ml-teste-nome`, publicar, abrir chat novo, tentar `@hub_ml-teste-nome`.
   Resultado decide entre as opções A, B e C da seção 2.1.
2. **O padrão `__init__.py` preserva os imports?** Provar localmente com um
   snippet real, sem tocar nos outros.
3. **Notebook dentro da pasta do módulo atrapalha o import?** Verificar que
   `import hub_snippets.spark.pit_join` não executa o notebook vizinho.
4. **`publicar_free.py` publica a estrutura aninhada corretamente?** Confirmar
   que o `.py` do módulo vai como arquivo e o notebook como notebook, três
   níveis abaixo.
5. Guarda contra `__pycache__` reaparecer no fonte.

**Como você verifica:** leio o relatório e confirmo o nome escolhido. Sem
aprovação aqui, a Sprint 1 não começa.

### Sprint 1 — Templates e exemplo

Cria `padroes/` com os nove arquivos da seção 4, incluindo o exemplo completo do
conversor de medidas. Nenhum arquivo do produto é tocado.

**Como você verifica:** lê `padroes/exemplo_readme.md` e diz se é esse o nível de
didática que você quer. Tudo depois disso segue esse padrão, então é aqui que a
correção sai barata.

### Sprint 2 — Renomeação `x_` → `hub_` e remoção de três pastas

Mecânica e de alto volume: 682 referências em 121 arquivos. Feita por script com
verificação, nunca à mão. Inclui atualizar `tools/` (a lista de diretórios
esperados na conferência), a matriz de regras e o simulado.

Sai `x_projects/`, `x_docs/` e `x_config/`, com o conteúdo realocado conforme a
tabela 3.2.

**Como você verifica:** navega no Databricks e vê `hub_snippets`, `hub_scripts`,
`hub_prompts` no lugar dos `x_`, e as três pastas ausentes. Validação, render e
conferência aprovados, com zero referência órfã.

### Sprint 3 — Renomeação das skills

12 pastas renomeadas, `name` do frontmatter acompanhando, e todas as 254
referências a `rodrigo-` atualizadas. README da pasta `skills/` no template novo.

**Ponto de atenção:** renomear não altera nenhuma `description`, então o
roteamento automático continua certificado. Mas a `@menção` muda — os 12 testes
de menção precisam ser refeitos. Os 24 testes positivos e negativos não.

**Como você verifica:** abre um chat novo e chama `@hub_ml-eda-profissional`.

### Sprints 4 e 5 — `hub_scripts` e `hub_prompts`

As menores, e por isso primeiras: 7 e 16 objetos. Servem para validar o formato
de pasta e de notebook num volume revisável antes de aplicá-lo a 51 snippets.

**Como você verifica:** abre duas ou três pastas no Databricks, roda o notebook
de exemplo e diz se a explicação está no nível certo. Se estiver, as sprints 6 a
9 replicam o formato sem nova discussão.

### Sprints 6 a 9 — `hub_snippets`

O grosso do trabalho, dividido por natureza do conteúdo e não por volume:

- **6 — `spark` (7) e `testing` (1).** Onde o erro custa mais caro e onde estão
  os módulos mais recentes e menos rodados: `pit_join`, `join_diagnostics`.
  Herdam três dos quatro notebooks didáticos existentes.
- **7 — `ml` sem dependência opcional (16).** Split temporal, walk-forward,
  métricas, PSI, WOE/IV, scorecard, safra. Todos executam no Free sem instalar
  nada.
- **8 — `ml` com dependência opcional (14).** Exigem versões fixadas na sessão;
  `prophet_wrapper` fica sem execução e o notebook dirá por quê.
- **9 — `constants`, `visual`, `display` (13).** Os triviais, sujeitos à decisão
  2.2 sobre notebook agrupado.

### Sprint 10 — READMEs de topo

O `README.md` da raiz reescrito no template, com o que hoje falta: o que é o
projeto de forma didática, o que é cada pasta, o que são skills, snippets,
scripts e prompts explicados para quem nunca viu, exemplos concretos, FAQ real e
a arquitetura em diagrama. Mesmo tratamento para `.assistant/README.md`.

Fica no fim de propósito: um README que descreve a estrutura precisa ser escrito
depois que a estrutura existe, ou é reescrito duas vezes.

### Sprint 11 — Skill de criação de objetos do Hub

**Uma skill só**, `hub_ml-criar-objeto`, e não cinco. O gatilho é o mesmo
("preciso criar X no Hub") e cinco skills competindo pelo mesmo vocabulário é
exatamente a colisão de roteamento que os forward tests existem para evitar. A
distinção entre README, snippet, script, prompt e skill é um parâmetro do pedido,
não uma skill diferente — e o corpo da skill trata cada caso.

A skill lê os templates de `padroes/`, faz as perguntas que faltam, gera a
estrutura de pastas completa e roda a checagem final. Precisa de forward tests
próprios: um caso positivo, um negativo e a menção.

### Sprint 12 — Auditoria e fechamento

Rodada A1 em sessão sem contexto sobre o resultado inteiro, no formato que já
provou funcionar três vezes: acesso ao disco e à CLI, instrução para executar em
vez de ler. Correção dos achados, CHANGELOG, ADR sobre a mudança de identidade do
projeto, e o gate de replicação no trabalho.

---

## 6. O que não está neste plano, e por quê

| Item | Situação |
|---|---|
| Auditoria de segunda origem da biblioteca | segue como gate aberto antes de usar `pit_join` em decisão que importe no trabalho; independe desta reestruturação |
| `prophet_wrapper` | sem combinação de versões funcional; a Sprint 8 documenta, não resolve |
| Camada squad (`Workspace/.assistant/`) | fase seguinte; o Hub precisa estar pronto antes |
| Replicação no trabalho | o runbook existe e continua válido; roda depois da Sprint 12 |

---

## 7. Registro de execução

Preenchido ao fim de cada sprint. Serve para retomar o trabalho de outra sessão
sem reconstruir contexto.

| Sprint | Status | Data | Observação |
|---|---|---|---|
| 0 | não iniciada | — | — |
| 1 | não iniciada | — | — |
| 2 | não iniciada | — | — |
| 3 | não iniciada | — | — |
| 4 | não iniciada | — | — |
| 5 | não iniciada | — | — |
| 6 | não iniciada | — | — |
| 7 | não iniciada | — | — |
| 8 | não iniciada | — | — |
| 9 | não iniciada | — | — |
| 10 | não iniciada | — | — |
| 11 | não iniciada | — | — |
| 12 | não iniciada | — | — |
