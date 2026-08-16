# Plano de reestruturação — de ambiente pessoal a Hub de equipe

Documento de trabalho. Cada sprint é executada isoladamente, revisada e só então
a seguinte começa. A divisão existe para que nenhuma sprint dependa de decisão
ainda não tomada, e para que cada uma possa ser delegada como pacote fechado.

- **Status:** plano calibrado, aguardando início da Sprint 0
- **Sprint atual:** nenhuma iniciada
- **Última atualização:** 2026-08-16

---

## 1. O que muda, em uma página

| Dimensão | Hoje | Depois |
|---|---|---|
| Marca do que é customizado | prefixo `x_` | prefixo **`hub_`** / **`hub-`** |
| Identidade do projeto | ambiente pessoal | **Hub de ML** da equipe |
| Nome das skills | `rodrigo-<tema>` | **`hub-ml-<tema>`** |
| Organização de um snippet | um `.py` solto numa pasta temática | **uma pasta por snippet**, com o `.py`, o `__init__.py` e um notebook que o demonstra |
| Organização de script e prompt | idem | idem |
| Contexto de projeto | `x_projects/` | **removida** |
| Documentação avulsa | `x_docs/`, `x_config/` | **removidas**, conteúdo realocado com explicação |
| Glossário | arquivo separado em `x_docs/` | **seção do `.assistant/README.md`** |
| Padrão de README | cada um com uma cara | **template único**, com exemplo de referência |
| Criação de novos objetos | manual, sem padrão | **`hub-ml-criar-objeto`**, uma skill que aplica os templates |

O princípio que organiza tudo: **quem bate o olho na árvore de pastas deve
entender o que é da plataforma e o que é nosso, sem ler README nenhum.** O `x_`
exigia uma legenda; o `hub_` carrega o significado no próprio nome.

---

## 2. Nomenclatura — a regra e a exceção que a linguagem impõe

> **Underscore onde o Python importa. Hífen onde a plataforma nomeia.**

| Objeto | Forma | Exemplo | Razão |
|---|---|---|---|
| Pasta de biblioteca importável | `hub_` | `hub_snippets`, `hub_scripts` | nome de pacote Python não aceita hífen |
| Pasta irmã não importável | `hub_` | `hub_prompts` | consistência visual com as duas acima |
| Skill | `hub-ml-` | `hub-ml-eda-profissional` | objeto nomeado pela plataforma; hífen é a convenção do padrão Agent Skills |
| Pasta de snippet/script/prompt | minúsculas com `_` | `pit_join/`, `taxa_resposta_campanha/` | precisa ser identificador Python válido |

`hub-snippets` com hífen é **impossível**: `from hub-snippets.spark.pit_join
import pit_join` é erro de sintaxe. A alternativa seria obrigar cada notebook a
usar `importlib.import_module("hub-snippets.spark.pit_join")`, o que inviabiliza
o uso por uma equipe. Por isso a regra tem duas metades em vez de uma.

O ganho colateral é que a regra é informativa: ao ver `hub_` você sabe que aquilo
se importa no Python; ao ver `hub-` você sabe que é a plataforma que carrega.

---

## 3. Arquitetura alvo

```text
.assistant/
├── README.md                        # porta de entrada do Hub + glossário
│
├── skills/                          # NATIVO — o Genie Code descobre sozinho
│   ├── README.md
│   ├── hub-ml-eda-profissional/
│   │   └── SKILL.md
│   ├── … (11 outras)
│   └── hub-ml-criar-objeto/         # NOVA: aplica os templates do Hub
│
├── hub_snippets/                    # biblioteca Python importável
│   ├── README.md
│   ├── requirements-optional.txt
│   ├── spark/
│   │   ├── README.md
│   │   ├── pit_join/
│   │   │   ├── __init__.py          # expõe a API pública da pasta
│   │   │   ├── pit_join.py          # implementação
│   │   │   └── exemplo_pit_join.py  # notebook executável
│   │   └── … (6 outros)
│   ├── ml/  constants/  visual/  display/  testing/
│   └── tests/                       # suíte de regressão, sem notebook
│
├── hub_scripts/                     # utilitários de diagnóstico
│   ├── README.md
│   └── quick_profile/
│       ├── __init__.py
│       ├── quick_profile.py
│       └── exemplo_quick_profile.py
│
└── hub_prompts/                     # briefings prontos para colar
    ├── README.md
    └── eda_completa/
        ├── eda_completa.md
        └── exemplo_eda_completa.py
```

### 3.1 O caminho de import, desenhado do zero

Você confirmou que ainda não há trabalho apoiado no Hub e que ele ainda não foi
apresentado ao time. Isso remove a obrigação de preservar os caminhos atuais — a
escolha passa a ser puramente **qual forma lê melhor para quem chega**.

Sem nenhum tratamento, uma pasta por snippet produziria a repetição feia:

```python
from hub_snippets.spark.pit_join.pit_join import pit_join   # ruim
```

Um `__init__.py` por pasta de snippet, expondo a API pública, resolve:

```python
# hub_snippets/spark/pit_join/__init__.py
from .pit_join import pit_join

__all__ = ["pit_join"]
```

```python
from hub_snippets.spark.pit_join import pit_join            # bom
```

Esse `__init__.py` não é remendo de compatibilidade — é o que define **qual é a
API pública da pasta**. O que estiver listado em `__all__` é contrato com quem
usa; o que ficar de fora é interno e pode mudar sem aviso. Cada pasta de snippet
passa a declarar isso explicitamente, o que hoje só existe por convenção de
nomes com `_`.

O notebook de exemplo mora na mesma pasta, nunca é importado, e é publicado como
notebook e não como arquivo.

### 3.2 Destino do conteúdo que sai

Nada é descartado sem decisão, e nada é movido sem explicação. **Cada realocação
carrega junto o texto que diz por que aquilo existe** — a informação não pode
chegar ao novo lugar como um bloco solto que ninguém entende.

| Origem | Conteúdo | Destino e tratamento |
|---|---|---|
| `x_docs/` | `glossario.md` | **seção "Vocabulário" do `.assistant/README.md`**, mantendo a divisão por procedência — plataforma, modelagem, convenção do Hub e o que não existe |
| `x_docs/` | `catalogo_helpers.md` | **dissolvido** nos READMEs de seção. Com uma pasta por objeto, cada README lista o que há embaixo dele; o mapa demanda → módulo vira a coluna "quando usar" dessas tabelas |
| `x_docs/` | 4 notebooks didáticos | viram o notebook de exemplo dos snippets que ensinam: `pit_join`, `psi_calculator`, `join_diagnostics`, `vintage_analysis` — o conteúdo é reaproveitado, não recomeçado |
| `x_docs/` | `SKILL_TEMPLATE.md` | `padroes/skill/template.md`, revisado no formato novo |
| `x_docs/` | `ROADMAP_SKILLS.md`, `LEGACY_CONTEXT.md`, `skills_manifest.md`, manifesto de exportação | `docs/historico/` na raiz do repositório, com um README explicando o que cada um registrou e por que não vai para o workspace |
| `x_config/` | `mcp_servers.legacy.json` | **removido**: contém lista vazia e o projeto não usa MCP |
| `x_config/` | aviso sobre o `.mcp_servers.json` que a plataforma cria sozinha | vira FAQ do `.assistant/README.md` — é informação que salva alguém de apagar um arquivo da plataforma |
| `x_projects/` | `AGENTS_TEMPLATE.md` | `docs/historico/`. **Não vira template do Hub**: `padroes/` padroniza o que criamos aqui, e um `AGENTS.md` de projeto externo não é objeto do Hub. Fica recuperável, sem ocupar espaço na estrutura |
| `x_projects/` | explicação da descoberta hierárquica de `AGENTS.md` | vira FAQ do `README.md` da raiz: o mecanismo é nativo e vale saber que existe, mesmo sem a pasta |
| `x_projects/` | ficha de projeto, exemplo de churn, README | **removidos** |

### 3.3 Free Edition não é o ambiente de destino

O laboratório é Free; o trabalho não é. Todo notebook de exemplo declara, num
bloco no topo, o que ele assume do ambiente:

- se roda em serverless sem instalar nada;
- se exige biblioteca opcional com versão fixada, e qual;
- se depende de comportamento que difere entre Free e compute clássico —
  `cache()` é o caso conhecido.

Notebook que não puder ser executado no laboratório sai com a saída ausente e o
motivo escrito, nunca com resultado inventado. A matriz de diferenças continua em
`.claude/rules/free-vs-trabalho.md` e é atualizada a cada diferença nova.

---

## 4. Os padrões

`padroes/` na raiz do repositório, **uma subpasta por tipo de objeto** (seis). Cada
subpasta tem o template, o exemplo preenchido e um README curto dizendo quando
usar aquele template.

```text
padroes/
├── README.md                    # índice: qual template para qual objeto
├── readme/
│   ├── template.md
│   ├── exemplo.md
│   └── README.md
├── snippet/
│   ├── template.md              # a pasta: __init__.py, módulo, notebook
│   ├── exemplo/                 # pasta de snippet completa e funcional
│   │   ├── __init__.py
│   │   ├── taxa_resposta_campanha.py
│   │   └── exemplo_taxa_resposta_campanha.py
│   └── README.md
├── script/
│   ├── template.md
│   ├── exemplo/
│   └── README.md
├── prompt/
│   ├── template.md
│   ├── exemplo/
│   └── README.md
├── skill/
│   ├── template.md
│   ├── exemplo/
│   └── README.md
└── notebook/
    ├── template.py              # esqueleto do notebook de exemplo
    ├── exemplo.py
    └── README.md
```

São **seis tipos de objeto**, e a lista é fechada: se algo não é README,
snippet, script, prompt, skill ou notebook, não é objeto do Hub e não ganha
template aqui.

### 4.1 Estrutura do template de README

Nove seções em ordem fixa, hierarquia navegável (`##` seção, `###` subtópico) e
pelo menos um bloco visual por documento — tabela, mermaid ou saída real.

| # | Seção | Responde | Obrigatória? |
|---|---|---|---|
| 1 | Título + frase de identidade | "o que é isto, em uma linha" | sim |
| 2 | Aviso de natureza | é nativo da plataforma ou é do Hub? | sim |
| 3 | Para que serve / quando usar | "isto resolve o meu problema?" | sim |
| 4 | Visão estrutural | diagrama ou árvore do que existe aqui | sim |
| 5 | Como usar — exemplo copiável | "me dá o comando" | sim |
| 6 | O que existe aqui | tabela do conteúdo, uma linha por item | se houver filhos |
| 7 | Limites e armadilhas | "o que dá errado e não é óbvio" | sim |
| 8 | Perguntas frequentes | dúvidas reais de quem chega | quando houver ≥ 3 |
| 9 | Onde continuar | links para o próximo passo | sim |

Regras que o template carrega: um bloco visual por documento; termo técnico
definido no primeiro uso ou remetido ao vocabulário; nenhum número codificado em
prosa que envelheça sozinho; exemplo sempre copiável e testado; distinção nativo
× Hub visível em cada página.

### 4.2 Estrutura do template de notebook

Quatro movimentos por bloco de código, na ordem que você descreveu:

1. **Célula de contexto** — o que este trecho vai fazer e por que alguém
   precisaria disso, em linguagem de negócio antes da técnica.
2. **Código comentado** — a implementação com comentário nas linhas onde a
   decisão não é óbvia.
3. **Execução real** — a chamada, com dados sintéticos, e a saída de verdade.
4. **Leitura do resultado** — o que aquele número significa, e o erro de
   interpretação mais provável ali.

Abre com o bloco de assunções de ambiente (seção 3.3) e fecha com "quando **não**
usar este helper" — a seção que mais economiza retrabalho.

### 4.3 Tema do exemplo

**`taxa_resposta_campanha`** — a taxa de resposta de uma campanha de CRM por
segmento de cliente.

Escolhido por três razões. É do domínio real da equipe, então ninguém precisa
traduzir de outro contexto. É trivial de entender no enunciado — respondentes
sobre contatados — e portanto a atenção do leitor sobra para a *estrutura* do
documento, que é o que o exemplo existe para ensinar. E carrega uma armadilha
estatística legítima: comparar taxas entre segmentos de tamanhos muito
diferentes, onde um segmento de 30 contatos produz uma taxa instável que parece
comparável à de um de 30.000. O notebook mostra o erro acontecendo antes de
mostrar o intervalo de confiança que o desarma.

Não é um módulo real da biblioteca e não vai virar um — é material de referência
dos padrões. O mesmo tema atravessa os cinco tipos de template, para que dê para
comparar lado a lado o snippet, seu notebook, seu prompt, seu script e o README
da pasta.

---

## 5. Como uma sprint é executada

Você pretende delegar boa parte deste trabalho a subagentes em paralelo. Isso
muda o que o plano precisa entregar: não basta dizer *o que* fazer, é preciso
que dois agentes distintos, trabalhando sem se falar, produzam material
indistinguível. Cada sprint de conteúdo entrega, portanto, um **pacote de
trabalho** com quatro partes:

| Parte | Conteúdo |
|---|---|
| Inventário | a lista fechada de objetos daquela sprint, com caminho de origem e destino |
| Contrato | qual template aplicar, e o que é obrigatório em cada arquivo produzido |
| Fixture | de onde vêm os dados sintéticos do notebook — `hub_snippets.testing.fixtures`, nunca dados inventados na hora |
| Critério de aceite | o que precisa passar para a sprint fechar |

O critério de aceite é o mesmo em todas as sprints de conteúdo:

1. `python tools/validate_assistant.py` aprovado;
2. render e `--verify` aprovados, sem obsoleto nem ausente;
3. todo notebook da sprint executado no laboratório, com a saída real colada —
   ou, quando impossível, com o motivo escrito;
4. o README da pasta lista todos os objetos dela, sem sobrar nem faltar;
5. nenhuma referência órfã ao nome antigo.

O item 3 é o que impede o modo de falha mais provável de uma execução paralela:
notebook plausível que nunca rodou.

---

## 6. As sprints

| # | Sprint | Entrega | Objetos | Depende de |
|---|---|---|---:|---|
| 0 | Fundação e verificações | relatório curto, zero mudança estrutural | — | — |
| 1 | Padrões e exemplo | `padroes/` completa, 6 subpastas | — | 0 |
| 2 | Renomeação e limpeza | `hub_*`, 3 pastas removidas, conteúdo realocado | — | 1 |
| 3 | Skills renomeadas | 12 pastas `hub-ml-*` + README da seção | 12 | 0, 2 |
| 4 | `hub_scripts` | pastas + notebooks + README | 7 | 1, 2 |
| 5 | `hub_prompts` | pastas + notebooks + README | 16 | 1, 2 |
| 6 | `hub_snippets`: spark e testing | pastas + notebooks + README | 8 | 1, 2 |
| 7 | `hub_snippets`: ml núcleo | pastas + notebooks | 16 | 6 |
| 8 | `hub_snippets`: ml com dependência opcional | pastas + notebooks | 14 | 6 |
| 9 | `hub_snippets`: constants, visual, display | pastas + notebooks + READMEs | 13 | 6 |
| 10 | READMEs de topo | raiz e `.assistant`, com o vocabulário | 2 | 2–9 |
| 11 | `hub-ml-criar-objeto` | skill + forward tests | 1 | 1, 10 |
| 12 | Auditoria e fechamento | rodada A1 externa, correções, ADR | — | tudo |

**Total de notebooks a escrever: 74** — 51 em snippets, 7 em scripts, 16 em
prompts. Um por objeto, inclusive nos triviais, como você decidiu: a
padronização vale mais do que a economia, e um leitor que encontra notebook em
doze pastas e não na décima terceira desconfia da décima terceira.

### Sprint 0 — Fundação e verificações

Nada é renomeado. Responde ao que pode inviabilizar o resto.

1. **O `__init__.py` por pasta entrega a ergonomia prometida?** Provar com um
   snippet real, incluindo import a partir de notebook no workspace.
2. **Notebook dentro da pasta do módulo atrapalha o import?** Confirmar que
   importar o pacote não executa o notebook vizinho.
3. **`publicar_free.py` publica estrutura aninhada corretamente?** O `.py` do
   módulo como arquivo e o notebook como notebook, três níveis abaixo.
4. **O nome com hífen é aceito na skill?** Baixo risco — hífen é a convenção do
   padrão —, mas se verifica junto com o resto.
5. Guarda permanente contra `__pycache__` reaparecer no fonte.

**Como você verifica:** lê o relatório. Sem aprovação, a Sprint 1 não começa.

### Sprint 1 — Padrões e exemplo

Cria `padroes/` com as seis subpastas da seção 4, incluindo o exemplo completo e
executável do `taxa_resposta_campanha` em cada formato aplicável. Nenhum arquivo do
produto é tocado.

**Como você verifica:** lê `padroes/readme/exemplo.md` e roda
`padroes/snippet/exemplo/exemplo_taxa_resposta_campanha.py` no laboratório. Se o
nível de didática estiver certo, tudo depois disso segue esse padrão — é aqui
que a correção sai mais barata.

### Sprint 2 — Renomeação e limpeza estrutural

Alto volume e mecânica: 682 referências em 121 arquivos, feitas por script com
verificação. Inclui `tools/` (lista de diretórios esperados na conferência), as
regras de `.claude/` e o simulado.

Saem `x_projects/`, `x_docs/` e `x_config/`, com o conteúdo realocado conforme a
tabela 3.2 — cada peça acompanhada do texto que a explica no destino novo.

**Como você verifica:** navega no Databricks e vê `hub_snippets`, `hub_scripts` e
`hub_prompts` no lugar dos `x_`, e as três pastas ausentes. Validação, render e
conferência aprovados, com zero referência órfã.

### Sprint 3 — Skills renomeadas

12 pastas para `hub-ml-*`, `name` do frontmatter acompanhando, 254 referências
atualizadas, e o README da pasta `skills/` no template novo.

**Ponto de atenção:** renomear não altera nenhuma `description`, então o
roteamento automático segue certificado. A `@menção` muda — os 12 testes de
menção precisam ser refeitos; os 24 positivos e negativos, não.

**Como você verifica:** abre um chat novo e chama `@hub-ml-eda-profissional`.

### Sprints 4 e 5 — `hub_scripts` e `hub_prompts`

As menores, e por isso primeiras: 7 e 16 objetos. Validam o formato de pasta e de
notebook num volume revisável antes de aplicá-lo a 51 snippets.

**Como você verifica:** abre duas ou três pastas no Databricks, roda o notebook e
diz se a explicação está no nível certo. Aprovado aqui, as sprints 6 a 9
replicam o formato sem nova discussão — e é este o ponto em que a delegação a
subagentes passa a ser segura.

### Sprints 6 a 9 — `hub_snippets`

Divididas por natureza do conteúdo, não por volume:

- **6 — `spark` (7) e `testing` (1).** Onde o erro custa mais caro e onde estão
  os módulos mais novos e menos rodados: `pit_join`, `join_diagnostics`. Herdam
  três dos quatro notebooks didáticos existentes.
- **7 — `ml` sem dependência opcional (16).** Split temporal, walk-forward,
  métricas, PSI, WOE/IV, scorecard, safra. Executam no Free sem instalar nada.
- **8 — `ml` com dependência opcional (14).** Exigem versões fixadas na sessão.
  `prophet_wrapper` fica sem execução e o notebook dirá exatamente por quê.
- **9 — `constants` (4), `visual` (6), `display` (3).** Os curtos, com notebook
  próprio cada um.

### Sprint 10 — READMEs de topo

`README.md` da raiz reescrito no template, com o que hoje falta: o que é o
projeto de forma didática; o que é cada pasta; o que são skills, snippets,
scripts e prompts explicados para quem nunca viu; exemplos concretos; FAQ real; e
a arquitetura em diagrama. Mesmo tratamento para `.assistant/README.md`, que
absorve o vocabulário.

Fica no fim de propósito: um README que descreve a estrutura precisa ser escrito
depois que a estrutura existe, ou é reescrito duas vezes.

### Sprint 11 — `hub-ml-criar-objeto`

Uma skill só, como você decidiu. O gatilho é o mesmo ("preciso criar X no Hub") e
cinco skills disputando o mesmo vocabulário seria a colisão de roteamento que os
forward tests existem para pegar. O tipo do objeto é parâmetro do pedido, não
skill diferente.

Ela lê os templates de `padroes/`, pergunta o que falta, gera a estrutura de
pastas completa e roda a checagem final. Precisa de forward tests próprios: um
positivo, um negativo e a menção.

### Sprint 12 — Auditoria e fechamento

Rodada A1 em sessão sem contexto sobre o resultado inteiro, no formato que já
funcionou três vezes: acesso ao disco e à CLI, instrução para executar em vez de
ler. Correção dos achados, CHANGELOG, ADR sobre a mudança de identidade do
projeto, e o gate de replicação no trabalho.

---

## 7. O que não está neste plano, e por quê

| Item | Situação |
|---|---|
| Auditoria de segunda origem da biblioteca | segue como gate aberto antes de usar `pit_join` em decisão que importe no trabalho; independe desta reestruturação |
| `prophet_wrapper` | sem combinação de versões funcional; a Sprint 8 documenta, não resolve |
| Camada squad (`Workspace/.assistant/`) | fase seguinte; o Hub precisa estar pronto antes |
| Replicação no trabalho | o runbook existe e continua válido; roda depois da Sprint 12 |

---

## 8. Registro de execução

Preenchido ao fim de cada sprint, para retomar de outra sessão sem reconstruir
contexto.

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
