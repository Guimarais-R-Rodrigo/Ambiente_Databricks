# Plano de reestruturação — de ambiente pessoal a Hub de equipe

Documento de trabalho, versão 2. Cada sprint é executada isoladamente, auditada
em sessão sem contexto, revisada por você, e só então a seguinte começa.

- **Status: as 13 sprints executadas.** A 5 entregou as partes 1 e 2 dos 16 prompts; as partes 3 e os forward tests dependem de interação humana. 13 skills; a biblioteca convertida (**58 objetos**: 51 `hub_snippets` + 7 `hub_scripts`) e os dois READMEs de topo atualizados. O validador conta **60 pastas de objeto**, somando os 2 exemplares de `hub_padroes`, que são template e não biblioteca. Pendem de você: os 3 forward tests da skill nova e as 16 partes 3 dos prompts
- **Última atualização:** 2026-08-17

> **Histórico de revisão.** A v1 foi submetida a auditoria em sessão sem
> contexto, com instrução para executar o plano sobre um objeto real em vez de
> lê-lo. Vieram 25 achados, todos procedentes, verificados um a um contra o
> disco. Nove eram do tipo que só apareceria depois de dezenas de arquivos
> escritos. O que sobreviveu intacto está marcado em §11.

---

## 1. O que muda, em uma página

| Dimensão | Hoje | Depois |
|---|---|---|
| Marca do que é customizado | prefixo `x_` | prefixo **`hub_`** / **`hub-`** |
| Identidade do projeto | ambiente pessoal | **Hub de ML** da equipe |
| Nome das skills | `rodrigo-<tema>` | **`hub-ml-<tema>`** |
| Organização de um snippet | um `.py` solto numa pasta temática | **uma pasta por snippet**: `.py`, `__init__.py` e notebook |
| Organização de script e prompt | idem | idem |
| Contexto de projeto | `x_projects/` | **removida** |
| Documentação avulsa | `x_docs/`, `x_config/` | **removidas**, conteúdo realocado |
| Glossário | arquivo em `x_docs/` | **seção do `.assistant/README.md`** |
| Padrão de README | cada um com uma cara | **template único**, publicado com o produto |
| Criação de novos objetos | manual | **`hub-ml-criar-objeto`** |
| Garantia de qualidade | auditoria no fim | **auditoria por sprint** (§6) |

O princípio que organiza tudo: **quem bate o olho na árvore de pastas deve
entender o que é da plataforma e o que é nosso, sem ler README nenhum.**

---

## 2. Decisões tomadas

### 2.1 `hub_padroes/` é publicado com o produto

**Decidido em 2026-08-16: `.assistant/hub_padroes/`.**

A auditoria provou que uma pasta na raiz do repositório **nunca chega ao
workspace** — `render_simulado.py` copia exatamente `.assistant_instructions.md`
e `.assistant/`. Ali os templates ficariam invisíveis para a equipe e para a
skill `hub-ml-criar-objeto`, que roda dentro do Genie Code e existe para
aplicá-los. Publicados, entram no `--verify` e servem de destino aos links
órfãos da §4.3.

### 2.2 A paleta permanece como está

**Decidido em 2026-08-16: manter `AZUL_CAIXA` e a nomenclatura atual de
`constants/colors.py`.** O repositório é privado e o material circula apenas
dentro da instituição.

Registrado aqui para que uma auditoria futura não reabra o ponto: a constante é
identificador institucional, foi avaliada, e a permanência é decisão consciente.
O `CORPORATE_RE` do validador não a alcança — ele cobre domínios de e-mail, não
nomes de constante —, então nenhuma exceção de código é necessária.

---

## 3. Nomenclatura

> **Underscore onde o Python importa. Hífen onde a plataforma nomeia.**

| Objeto | Forma | Exemplo | Razão |
|---|---|---|---|
| Pasta de biblioteca importável | `hub_` | `hub_snippets`, `hub_scripts` | nome de pacote Python não aceita hífen |
| Pasta irmã não importável | `hub_` | `hub_prompts`, `hub_padroes` | consistência visual |
| Skill | `hub-ml-` | `hub-ml-eda-profissional` | hífen já é o que as 12 skills usam e funciona |
| Pasta de snippet e de script | minúsculas com `_` | `pit_join/` | é pacote Python |
| Pasta de prompt e de padrão | minúsculas com `_` | `eda_completa/` | não importada; `_` por consistência |

`hub-snippets` com hífen é **impossível**: `from hub-snippets.spark.pit_join
import pit_join` é erro de sintaxe — verificado.

**Fora do `.assistant`:** a pasta `/Users/<user>/hub_lab/`, onde o smoke test é
importado, é o último `x_` visível no workspace. Renomeada para `hub_lab/` na
Sprint 2, com as 6 referências em `docs/` acompanhando.

---

## 4. Arquitetura alvo

```text
.assistant/
├── README.md                        # porta de entrada do Hub + vocabulário
│
├── skills/                          # NATIVO — o Genie Code descobre sozinho
│   ├── README.md
│   ├── hub-ml-eda-profissional/SKILL.md
│   ├── … (11 outras)
│   └── hub-ml-criar-objeto/         # NOVA (Sprint 11)
│
├── hub_padroes/                     # os templates, publicados (§2.1)
│   ├── README.md
│   ├── readme/  snippet/  script/  prompt/  skill/  notebook/
│   └── auditoria/                   # prompts de auditoria por sprint (§6)
│
├── hub_snippets/                    # biblioteca Python importável
│   ├── __init__.py
│   ├── README.md
│   ├── requirements-optional.txt
│   ├── spark/
│   │   ├── __init__.py
│   │   ├── README.md
│   │   └── pit_join/
│   │       ├── __init__.py          # declara a API pública
│   │       ├── pit_join.py
│   │       └── exemplo_pit_join.py  # notebook
│   ├── ml/  constants/  visual/  display/  testing/   (mesma forma)
│   └── tests/                       # suíte de regressão: sem pasta-por-objeto
│
├── hub_scripts/                     # 7 utilitários, mesma forma
└── hub_prompts/                     # 16 briefings, mesma forma
```

Os `__init__.py` de nível de seção e da raiz do pacote **existem hoje e
permanecem** — estavam ausentes da árvore da v1, que é o contrato que o executor
lê.

### 4.1 O caminho de import

Sem tratamento, uma pasta por snippet produziria `from
hub_snippets.spark.pit_join.pit_join import pit_join`. O `__init__.py` resolve:

```python
# hub_snippets/spark/pit_join/__init__.py
from .pit_join import pit_join

__all__ = ["pit_join"]
```

```python
from hub_snippets.spark.pit_join import pit_join     # idêntico ao de hoje
```

Verificado na auditoria: preserva **226 referências pontilhadas em 59 arquivos**,
e só uma referência no repositório inteiro usa caminho de arquivo. A
reestruturação de 51 objetos custa uma linha de documentação.

#### `__all__` é exaustivo, não curado

**Regra:** `__all__` contém **todos** os nomes públicos de nível superior do
módulo — funções, classes e constantes em maiúscula que não começam com `_`.
Não é curadoria.

Isto não é preferência. Há **sete** imports cruzados reais entre módulos da
biblioteca, e `tests/test_core.py` importa dez nomes de oito módulos:

```text
display/correlation_matrix  -> visual.theme_plotly : aplicar_tema
display/distribution_grid   -> spark.smart_sample  : smart_sample
display/distribution_grid   -> visual.theme_plotly : aplicar_tema
visual/index_generator      -> constants.emojis    : SECOES_EDA
visual/section_header       -> constants.colors    : AZUL_CAIXA, BG_SECTION, TEXTO_SECUNDARIO
visual/section_header       -> constants.emojis    : SECOES_EDA
visual/theme_plotly         -> constants.colors    : PALETA_CATEGORICA, TEXTO_SECUNDARIO, AZUL_CAIXA
```

`constants/colors` tem **22 nomes públicos**. Um executor que interprete "API
pública" como curadoria exporta cinco e quebra `section_header` — reproduzido na
auditoria com `ImportError: cannot import name 'BG_SECTION'`. E `smart_sample` é
escrito na Sprint 6 enquanto `distribution_grid` o consome na Sprint 9: três
sprints de distância entre a causa e o sintoma.

**A maioria dos módulos tem mais de um nome público** — hoje 39 dos 51, e o
número sai de `python tools/validate_assistant.py`, não daqui. Por isso os 51 `__all__` são
gerados **mecanicamente por AST na Sprint 0b**, não por 51 julgamentos
independentes.

### 4.2 O notebook dentro do pacote quebra o smoke test

Até a Sprint 7 os notebooks viviam em `hub_snippets/_notebooks_a_migrar/`, **fora** do pacote. Movê-los para
dentro da pasta de cada snippet os torna submódulos importáveis, e
`tools/spark_smoke_test.py` importa todo submódulo que encontra:

```python
for module_info in pkgutil.walk_packages(hub_snippets.__path__, prefix="hub_snippets."):
    run_case(f"import:{module_info.name}", lambda name=module_info.name: importlib.import_module(name))
```

Confirmado experimentalmente: `hub_snippets.spark.pit_join.exemplo_pit_join` é
enumerado, e importá-lo devolve `NameError: name 'spark' is not defined`,
classificado como FAIL. Seriam **51 execuções indevidas** — 58 com a descoberta
automática de `hub_scripts`. Os 16 notebooks de prompt não são varridos.

Correção obrigatória na Sprint 0, com dois detalhes que a v1 não tinha:

- **`ispkg=True` não tem arquivo `<nome>.py`**, e sim `<dir>/__init__.py`. A regra
  é explícita: **sem caminho resolvível → importa**. A leitura oposta pularia os
  51 `__init__.py`, ou seja, exatamente a nova API pública nunca seria testada.
- **A detecção do marcador é frágil.** `eh_notebook` lê a primeira linha crua e
  falha com BOM UTF-8, linha em branco antes, ou `# -*- coding: utf-8 -*-` antes
  — convenção usada por 11 módulos do repositório. A falha é silenciosa: o
  notebook vira `FILE`, o `--verify` aprova porque o nome bate, e o smoke test
  passa a importá-lo. A Sprint 0 endurece a detecção (ignora BOM, linhas em
  branco e comentários de encoding) num único lugar usado pelas duas ferramentas.

### 4.3 Destino do conteúdo que sai — e os 43 links que ele deixa

A v1 tratava `catalogo_helpers.md` como uma linha de tabela. A auditoria contou
**43 links markdown em 33 arquivos** apontando para as pastas que serão removidas:

| Alvo que some | Links | Onde |
|---|---:|---|
| `CATALOGO_HELPERS.md` | 35 | 12 `SKILL.md`, `rubrica_universal.md`, 16 prompts, 3 READMEs |
| `GLOSSARIO.md` | 4 | `.assistant/README.md`, `hub_snippets/README.md`, README da raiz |
| `hub_padroes/README.md`, `x_docs/README.md`, `docs/historico/AGENTS_TEMPLATE.md` | 4 | `.assistant/README.md`, README da raiz |

Simulada, a Sprint 2 da v1 terminava em `REPROVADO: 40 falha(s)` — reprovando o
próprio critério de aceite. E o destino que ela declarava ("READMEs de seção")
só nasce quatro sprints depois.

**Correção: o destino tem de existir no momento em que o link é reapontado.**

| Origem | Conteúdo | Destino, e em que sprint |
|---|---|---|
| `CATALOGO_HELPERS.md` | mapa demanda → módulo | **Sprint 2:** o conteúdo é absorvido por `hub_snippets/README.md`, que já existe (é o `hub_snippets/README.md` de hoje). Os 35 links passam a apontar para lá. **Sprints 6–9:** cada seção herda a fatia que lhe cabe, e o README de `hub_snippets` vira índice |
| `GLOSSARIO.md` | vocabulário | **Sprint 2:** vira `.assistant/GLOSSARIO.md`, publicado, e os 4 links apontam para lá. **Sprint 10:** absorvido como seção do `.assistant/README.md`, com os links reapontados de novo |
| `hub_snippets/_notebooks_a_migrar/` (4 arquivos) | material didático | **Sprint 2:** movidos para `.assistant/hub_snippets/_notebooks_a_migrar/`, uma pasta de trânsito explícita. **Sprints 6 e 7:** desmembrados (§4.4) e a pasta de trânsito é removida. Sem essa ponte, a Sprint 2 apaga o insumo das Sprints 6 e 7 |
| `.assistant/hub_padroes/skill/template.md` | modelo de skill | **Sprint 1:** `hub_padroes/skill/template.md`, publicado |
| `docs/historico/ROADMAP_SKILLS.md`, `LEGACY_CONTEXT.md`, `skills_manifest.md`, manifesto | governança | **Sprint 2:** `docs/historico/` na raiz, com README explicando cada um |
| `x_config/mcp_servers.legacy.json` | lista vazia | **removido** |
| `hub_padroes/README.md` | aviso do `.mcp_servers.json` da plataforma | vira FAQ do `.assistant/README.md` |
| `docs/historico/AGENTS_TEMPLATE.md` | modelo `AGENTS.md` | `docs/historico/`. Não é objeto do Hub |
| `x_projects/` restante | ficha, exemplo, README | **removidos** |
| `.assistant_instructions.md` | arquivo **nativo**, ≤ 20.000 chars | referência a `catalogo_helpers.md` reapontada; identidade "pessoal" → "Hub" |

### 4.4 Os quatro notebooks didáticos cobrem seis módulos

| Notebook | Ensina | Destino | Sprint |
|---|---|---|---|
| `01_vazamento_temporal` | `spark.pit_join` **e** `ml.split_temporal` | **dividido em dois** | 6 e 7 |
| `02_drift_e_estabilidade` | `spark.psi_calculator` | `spark/psi_calculator/` | 6 |
| `03_qualidade_de_juncao` | `spark.join_diagnostics` | `spark/join_diagnostics/` | 6 |
| `04_armadilhas_de_credito` | `ml.vintage_analysis` **e** `ml.woe_iv_calculator` | **dividido em dois** | 7 |

Dividir custa algo: o notebook 01 ensina vazamento mostrando join e split juntos,
que é como o erro acontece. As metades precisam recuperar esse contexto, e cada
uma remete à outra **por nome em prosa**, não por link relativo — link entre
pastas de pacote não é clicável na UI do Databricks e não é verificado por
ferramenta nenhuma.

### 4.5 Free Edition não é o ambiente de destino

Todo notebook abre declarando o que assume: se roda em serverless sem instalar
nada; se exige biblioteca opcional com versão fixada, e qual; se depende de
comportamento que difere entre Free e compute clássico. O formato literal desse
bloco está no template, não descrito em prosa.

---

## 5. Os padrões

`.assistant/hub_padroes/`, uma subpasta por tipo de objeto, **publicada com o
produto**. Seis tipos, lista fechada, mais os prompts de auditoria de §6.

### 5.1 O que o template de notebook precisa conter, literalmente

A v1 descrevia quatro movimentos. A auditoria mostrou que faltava o que faz o
arquivo funcionar:

1. **Preâmbulo de bootstrap.** Os quatro notebooks atuais abrem resolvendo o
   usuário e inserindo `/Workspace/Users/<user>/.assistant` no `sys.path`. Sem
   essas três linhas, **nenhum dos 74 notebooks importa a biblioteca**.
2. **Formato-fonte.** Primeira linha `# Databricks notebook source`, separador
   `# COMMAND ----------`, markdown como `# MAGIC %md`, e magics como
   `# MAGIC %pip install ...`. Escrito do jeito natural, `%pip install x==1.0`
   faz `ast.parse` estourar e a validação reprovar.
3. **Bloco de assunções de ambiente** (§4.5), com esqueleto literal.
4. Os quatro movimentos: contexto em linguagem de negócio → código comentado →
   execução real → leitura do resultado.
5. **Bloco canônico de "não executado"**, com exemplo preenchido: usado pelos 14
   módulos da Sprint 8 e por `prophet_wrapper`. Sem forma única, a Sprint 8 sai
   com 14 convenções diferentes.
6. Fechamento: "quando **não** usar este helper".

**Nome do arquivo: `exemplo_<nome_do_objeto>.py`, sempre.** A v1 usava três
formas diferentes. `exemplo.py` criaria 51 módulos com o mesmo nome-base.

#### Variante para objeto sem dados e sem número

Treze objetos da Sprint 9 são constantes ou funções que devolvem HTML:
`constants/colors` tem 22 constantes e zero funções. Para eles os movimentos 3 e
4 não existem como descritos, e o contrato de fixture não se aplica — as fixtures
só produzem DataFrames. O template tem uma **segunda variante**: mostrar o valor,
mostrar o efeito visual renderizado, e explicar a decisão de design por trás
(por que esta paleta, por que este limite de contraste).

### 5.2 O template de README tem duas escalas

Nove seções servem a uma pasta de seção. Não servem aos dois extremos:

- **Pasta pequena** (`display/`, 3 objetos): "visão estrutural" e "o que existe
  aqui" viram o mesmo conteúdo em dois formatos, e a FAQ força inventar dúvidas.
  → Variante curta: cinco seções, sem visão estrutural separada e sem FAQ.
- **README da raiz** (hoje 374 linhas) e **`.assistant/README.md`** (319 linhas,
  15 seções): nove seções não comportam "Instalação", "Fluxo de engenharia",
  "Solução de problemas" e "Fontes oficiais".
  → Variante longa: as nove seções são o **esqueleto obrigatório**, e seções
  adicionais entram em posições declaradas.

| Escala | Quando | Seções |
|---|---|---|
| Curta | pasta com ≤ 5 objetos | 5 |
| Padrão | pasta de seção, `hub_*` | 9 |
| Longa | raiz do repositório e `.assistant/` | 9 + extras posicionadas |

A seção "Aviso de natureza" só é obrigatória onde há ambiguidade real entre
nativo e Hub — em `skills/` e nos dois READMEs de topo. Repeti-la em 19 pastas
que são todas do Hub é ruído.

### 5.3 Tema do exemplo

**`taxa_resposta_campanha`** — taxa de resposta de campanha de CRM por segmento.
Do domínio da equipe e trivial no enunciado.

**A armadilha foi medida, não suposta.** A v2 afirmava que o intervalo de
confiança "desarma" a comparação entre segmentos de tamanhos muito diferentes.
Rodado sobre a base de exemplo, **não desarma**: o segmento de 28 contatos tem
IC de Wilson `[26,5% ; 60,9%]`, que não se sobrepõe a nenhum outro. A diferença é
estatisticamente real.

O que o exemplo ensina, então, é mais fino e mais útil:

| Leitura | Conclusão |
|---|---|
| Ingênua | "42,9% contra 3,8%: mande tudo para lá" |
| Estatística | a diferença é real, mas a **precisão** é péssima — a largura do IC vai de 0,4 pp no maior segmento a 34,4 pp no menor |
| Operacional | há 28 clientes no segmento. Mesmo a 60% de resposta, são 17 respostas numa campanha de 15.000 contatos |

A lição é que **significância não é relevância**: o efeito existe, é
mensurável, e é irrelevante para a decisão. Um exemplo que só mostrasse "o IC
derruba a diferença" ensinaria algo falso — e teria sido publicado se ninguém
rodasse.

A auditoria mostrou que ele **não exercita quatro situações** que os executores
vão encontrar. O conjunto de exemplos ganha, por isso, três peças a mais:

| Situação | Exemplo que a demonstra |
|---|---|
| `__all__` com mais de um nome (a maioria dos módulos) | `taxa_resposta_campanha` exporta a função **e** a constante de limite mínimo de base |
| Notebook que não pode ser executado | um exemplo curto e explicitamente falso, com o bloco canônico preenchido |
| Objeto sem dados e sem número | uma constante de exemplo, na variante de §5.1 |
| Resposta real do Genie Code no notebook de prompt | **exige uma interação humana já na Sprint 1** — ver §5.4 |

A skill de exemplo `hub-ml-analise-campanha` **não é publicada** em
`.assistant/skills/`: entraria no roteamento real e disputaria vocabulário com as
skills de verdade.

### 5.4 O notebook de um prompt não executa

Prompt é briefing para colar num chat. O notebook tem três partes: preparo
executável que cria a tabela sintética; o prompt preenchido; e a resposta real do
Genie Code colada como markdown, com comentário.

A parte 3 **exige uma pessoa num chat**. São **17 interações**, não 16: uma na
Sprint 1, para o exemplo de referência, e 16 na Sprint 5. A da Sprint 1 está no
portão que libera todo o resto — a v1 localizava a dependência humana só na
Sprint 5.

---

## 6. Auditoria por sprint

Toda sprint fecha com uma rodada A1 em aba nova, sem o contexto da execução. O
prompt vem de `hub_padroes/auditoria/`, e a profundidade varia com o que a sprint
produz:

| Sprint | Tipo | Por quê |
|---|---|---|
| 0, 0b | completa | fundação: erro aqui contamina as doze seguintes |
| 1 | completa + leitura sua | os templates são copiados 74 vezes |
| 2, 3 | de execução | renomeação mecânica; o que importa é o que quebrou sem ninguém ver |
| 4 | completa | é o portão de formato |
| 5–9 | por amostragem | o auditor escolhe os objetos, não eu; audita a fundo 3 de cada sprint e faz varredura rasa no resto |
| 10, 11 | completa | porta de entrada e skill que entra no roteamento |
| 12 | é a auditoria final | — |

Três invariantes em todo prompt de auditoria, herdados do que funcionou quatro
vezes: **acesso ao disco e à CLI**; **instrução para executar, não ler**; e
**bloqueio de `CHANGELOG.md`, `docs/auditoria/` e histórico do git**, que
vazariam o raciocínio de quem executou.

Custo real: 13 rodadas, cada uma pedindo uma aba nova e a colagem do resultado. É
o preço de não descobrir na Sprint 9 um defeito nascido na Sprint 4.

---

## 7. Como uma sprint é executada

Cada sprint de conteúdo entrega um pacote de trabalho com quatro partes:

| Parte | Conteúdo |
|---|---|
| Inventário | **a lista nominal fechada** dos objetos, com caminho de origem e destino. Não uma contagem: os nomes |
| Contrato | qual template e variante aplicar, e o que é obrigatório em cada arquivo |
| Fixture | `hub_snippets.testing.fixtures`, nunca dados inventados na hora |
| Critério de aceite | abaixo |

A v1 prometia "lista fechada" e entregava contagens. Isso fez a auditoria
reconstruir a divisão das Sprints 7 e 8 de três formas diferentes, duas delas
erradas. **Nome, não número.**

### 7.1 Critério de aceite

1. `python tools/validate_assistant.py` aprovado;
2. `render` e `--verify` aprovados, com **`obsoletos: 0`** — que é o que prova a
   limpeza remota da §7.3;
3. **smoke test verde no laboratório** (sprints 6–9): é a única ferramenta que
   pega `__all__` incompleto e notebook publicado no formato errado;
4. todo notebook da sprint executado, com saída real colada — ou com o bloco
   canônico de não executado (§5.1);
5. o README da pasta lista todos os objetos, sem sobrar nem faltar;
6. nenhuma referência órfã ao nome antigo **nas camadas vivas** (§7.2);
7. rodada de auditoria da §6 concluída e achados tratados.

A v1 tinha cinco critérios e nenhum deles enxergava as quatro classes de defeito
mais prováveis. A auditoria rodou a validação sobre um resultado com notebook
duplicado, link quebrado e import errado: `APROVADO, 0 falhas`.

### 7.2 O que **não** é renomeado

`CHANGELOG.md` é append-only, ADRs são imutáveis, e registros de auditoria e de
teste descrevem o que foi observado na época. Renomear ali falsifica o registro.

| Camada | `x_` / `hub-ml-` | Renomeia? |
|---|---:|---|
| `ambiente_fonte/`, `tools/`, `.claude/`, canônicos, `docs/playbooks/`, `GUIA_REPLICACAO_TEMPORARIO.md` | **471 / 162** | **sim** |
| `docs/testes/`, `CHANGELOG.md`, `docs/auditoria/`, `docs/handoffs/`, `docs/decisions/` | **187 / 108** | **não**, com nota de cabeçalho |

Os números da v1 (601 e 262) foram medidos sobre um universo que **incluía as
camadas preservadas** — o plano contradizia a si mesmo, superestimando a Sprint 2
em 27% e a Sprint 3 em 62%. Os acima são o escopo real.

Exceção: `docs/testes/forward/roteiro.md` é registro **e** instrumento
reutilizável. É atualizado; os resultados das rodadas ficam intactos.

### 7.3 Toda sprint que muda a árvore apaga o remoto

`import-dir --overwrite` sobrescreve e **nunca apaga**. Sem um passo explícito:

- depois da Sprint 2, o workspace teria `hub_snippets` **e** `hub_snippets`, mais
  as seis pastas antigas intactas — e a verificação humana declarada na v1 ("as
  três pastas ausentes") retornaria o resultado errado;
- depois da Sprint 3, `.assistant/skills/` teria **24 pastas**: 12 `hub-ml-*`
  órfãs e 12 `hub-ml-*`, com `description` idêntica duas a duas. É exatamente a
  colisão de roteamento que os forward tests existem para pegar.

**Passo obrigatório em toda sprint que renomeia ou remove:** `databricks
workspace delete` do que saiu, executado **antes** do `--verify`. O critério
humano deixa de ser "vejo as pastas certas" e passa a ser `obsoletos: 0`.

---

## 8. As sprints

| # | Sprint | Objetos | Depende de |
|---|---|---:|---|
| 0 | Fundação: ferramentas | — | §2 decidido |
| 0b | `testing/fixtures` e os 51 `__all__` | 1 | 0 |
| 1 | Padrões e exemplos | — | 0b |
| 2 | Renomeação, limpeza e realocação | — | 1 |
| 4 | `hub_scripts` — **portão de formato** | 7 | 2 |
| 3 | Skills renomeadas | 12 | 4 aprovada |
| 5 | `hub_prompts` (17 interações humanas) | 16 | 4 aprovada |
| 6 | `hub_snippets`: spark e testing | 8 | 4 aprovada |
| 7 | `hub_snippets`: ml núcleo | 16 | 6 |
| 8 | `hub_snippets`: ml com dependência opcional — **os 14 executam**, via `%pip` na sessão | 14 | 6 |
| 9 | `hub_snippets`: constants, visual, display | 13 | 6 |
| 10 | READMEs de topo | 2 | 2–9 |
| 11 | `hub-ml-criar-objeto` | 1 | 1, 4–9 |
| 12 | Auditoria final e fechamento | — | tudo |

A ordem mudou em três pontos após a auditoria: **0b** tira as fixtures do caminho
crítico antes que 23 notebooks as consumam; **4 vem antes de 3**, para que o
portão de formato aconteça o mais cedo possível e a renomeação de skills — a
única que mexe em roteamento certificado — fique isolada depois dele; e **5 sai
do caminho crítico**, por ter dependência humana.

Total de notebooks: **74** — 51 snippets, 7 scripts, 16 prompts.

### Sprint 0 — Fundação: ferramentas

Nada é renomeado. Só o que impede as doze seguintes:

1. **Endurecer a detecção de notebook** num único lugar, usado por
   `publicar_free.py` e pelo smoke test: ignorar BOM, linhas em branco e
   comentário de encoding antes do marcador.
2. **Adaptar `spark_smoke_test.py`**: pular notebook no `walk_packages`, com a
   regra explícita **sem caminho resolvível → importa**; trocar a lista fixa de
   scripts por descoberta automática.
3. **Estender `validate_assistant.check_markdown` aos arquivos `.py`** — hoje
   link quebrado dentro de notebook passa, e serão 74 notebooks cheios de links.
4. Confirmar publicação de `NOTEBOOK` a 4 níveis dentro de pacote.
5. Corrigir o `GUIA_REPLICACAO_TEMPORARIO.md`, que está rastreado no git e afirma
   na linha 3 não estar. Defeito que já existe hoje.

### Sprint 0b — `testing/fixtures` e os 51 `__all__`

Converte **só** `testing/fixtures` para o formato de pasta-por-objeto, antes de
qualquer consumidor, e gera mecanicamente por AST a lista dos 51 `__all__`, que
vira insumo das Sprints 6–9.

Prova o formato num objeto real antes de a Sprint 1 desenhar o template a partir
dele.

### Sprint 1 — Padrões e exemplos

`.assistant/hub_padroes/` com as seis subpastas, a pasta de auditoria, e o
conjunto de exemplos de §5.3 — incluindo as três peças que o
`taxa_resposta_campanha` não cobre. Inclui **uma interação sua no Genie Code**
para o exemplo de notebook de prompt.

**Como você verifica:** lê o exemplo de README e roda o notebook de exemplo. Se o
nível estiver certo, tudo depois segue esse padrão.

### Sprint 2 — Renomeação, limpeza e realocação

**471 ocorrências de `x_*`** nas camadas vivas, por script, com **tabela de
substituição explícita e fechada** — não regra de prefixo. A v1 deixava um
executor mapear os seis prefixos e produzir 43 links para `hub_docs/`,
`hub_config/` e `hub_projects/`, pastas que não existem na arquitetura alvo.

| Prefixo | Ação |
|---|---|
| `hub_snippets`, `hub_scripts`, `hub_prompts` | renomeia para `hub_*` |
| `x_docs`, `x_config`, `x_projects` | **remove**, com reapontamento por destino (§4.3) |
| `hub_lab` (workspace) | renomeia para `hub_lab` |
| prefixo `x_` citado como conceito | reescrito à mão em 6 lugares: 2 regras de `.claude/`, 2 playbooks, 1 skill operacional, README da raiz |

Guardrails: `Ambiente_Antigo/` e `Ajustes_Codex/` **não são tocados**; camadas
append-only só recebem nota de cabeçalho; `Novo_Ambiente_Simulado/` não é
editado, é regenerado.

Em `tools/`: `EXPECTED_X_DIRS` passa de seis para quatro (`hub_padroes`,
`hub_prompts`, `hub_scripts`, `hub_snippets`), com o rótulo impresso acompanhando.

Fecha com **delete remoto** (§7.3) e `obsoletos: 0`.

### Sprint 4 — `hub_scripts`: o portão

Sete objetos, com código que executa. **Antes desse aval, replicar para 51
snippets é multiplicar um formato não aprovado.**

### Sprint 3 — Skills renomeadas

12 pastas para `hub-ml-*`, `name` do frontmatter acompanhando, **162 ocorrências**
nas camadas vivas, README da pasta, `roteiro.md` atualizado.

Renomear não altera nenhuma `description` — verificado: nenhuma das 12 contém
`hub-ml-`, e o roteamento automático segue certificado. Os 12 testes de menção
são refeitos; os 24 positivos e negativos, não. Quatro `SKILL.md` citam sete
outras skills pelo nome no corpo: renome mecânico.

Fecha com **delete remoto das 12 pastas órfãs** antes do `--verify`.

### Sprints 5 a 9 — o conteúdo

- **5 — `hub_prompts` (16).** Fora do caminho crítico: 16 interações suas.
  `novo_projeto.md` precisa de tratamento à parte — ele manda gerar um `AGENTS.md`
  a partir do template de `x_projects`, pasta removida.
- **6 — `spark` (7) e `testing` (1).** Herda material de três notebooks (§4.4).
  `tests/test_core.py` não ganha pasta nem notebook: é suíte de regressão, única
  exceção à regra, registrada para não parecer esquecimento.
- **7 — `ml` núcleo (16).** Os 16 que **não** estão na tabela "Módulos com
  dependência opcional" de `docs/testes/spark/README.md`. Risco próprio: as
  funções desses módulos nunca executaram no Free — o smoke test só testou
  import para `ml`.
- **8 — `ml` com dependência opcional (14).** A lista nominal é exatamente a
  daquela tabela: `train_lgbm`, `train_xgboost`, `train_catboost`, `optuna_lgbm`,
  `lgbm_ranker`, `umap_viz`, `shap_explainer`, `survival_cox`, `kaplan_meier`,
  `autoencoder_anomaly`, `mlp_embeddings`, `tabnet_wrapper`, `arima_wrapper`,
  `prophet_wrapper`. Sem essa lista, a divisão 16/14 é irreconstruível: 22 dos 30
  módulos importam a dependência dentro da função, invisível no topo do arquivo.
- **9 — `constants` (4), `visual` (6), `display` (3).** Variante de notebook de
  §5.1 para objeto sem dados e sem número.

**READMEs, com dono explícito** — a v1 deixava quatro órfãos:

| README | Sprint |
|---|---|
| `hub_scripts/README.md` | 4 |
| `hub_prompts/README.md` | 5 |
| `hub_snippets/README.md`, `spark/`, `testing/` | 6 |
| `ml/README.md` | 7 |
| `constants/`, `visual/`, `display/` | 9 |
| `skills/README.md` | 3 |
| raiz e `.assistant/` | 10 |

### Sprints 10 a 12

**10 — READMEs de topo**, na variante longa, absorvendo o vocabulário e
reapontando os links de `GLOSSARIO.md`.

**11 — `hub-ml-criar-objeto`**, lendo os templates de `.assistant/hub_padroes/` —
que só funciona por causa da decisão §2.1. `EXPECTED_SKILLS` sobe para 13.

**12 — Auditoria final e fechamento.** ADR sobre a mudança de identidade, mais
dois que a auditoria apontou como necessários: o **ADR-0004** descreve o catálogo
que a Sprint 2 dissolve, e o **ADR-0005** cita "6 diretórios de extensão" como
critério de conferência. Ambos imutáveis: precisam de ADRs que os supersedam.

Atualização das regras que o plano contraria: `.claude/rules/genie-code-oficial.md`
e `rules/docs-e-readmes.md` definem `x_` como a convenção do projeto. Sem essa
mudança, a regra canônica passa a descrever o oposto do repositório — **entra na
Sprint 2**, não na 12, para não ficar meses inconsistente.

Os três playbooks de replicação (`checklist-replicacao.md`,
`replicacao-trabalho.md`, `GUIA_REPLICACAO_TEMPORARIO.md`) fixam "174 arquivos",
"12 skills", "6 diretórios `x_`" e "12 pastas `hub-ml-*`". Nenhum número
sobrevive: o total publicado sai de 175 para cerca de 295. Reescritos na Sprint 12.

---

## 9. Custo operacional que cresce

Medido na auditoria: `databricks workspace list` leva ~1,5 s, e há 39 diretórios
sob `.assistant` hoje (~60 s por `--verify`). Depois: ~112 diretórios, ~3 min por
conferência. Em nove sprints, ~27 min só de conferência, mais ~110 s por
publicação contra 4 s hoje.

Nenhum defeito, só fricção — mas **fricção em gate é gate que se pula**. A Sprint
0 acrescenta um `--verify --rapido` que compara contagens por diretório, para uso
durante a execução; o completo continua obrigatório no fechamento da sprint.

---

## 10. O que não está neste plano

| Item | Situação |
|---|---|
| Auditoria de segunda origem da biblioteca | gate aberto, independe desta reestruturação |
| ~~`prophet_wrapper`~~ | **resolvido em 2026-08-17**: `%pip install prophet` instala e ajusta. Sai desta lista |
| Testes funcionais de `ml` no Free | os 16 da Sprint 7 nunca executaram lá; o risco está registrado, a criação da bateria não está no escopo |
| Camada squad | fase seguinte |

---

## 11. O que a auditoria confirmou e deve sobreviver

Registrado para não ser desfeito numa próxima revisão:

- **O desenho do `__init__.py`.** Preserva 226 referências em 59 arquivos; só uma
  referência no repositório usa caminho de arquivo.
- **O diagnóstico do `walk_packages`** (§4.2), confirmado experimentalmente,
  levantado antes de a Sprint 6 existir.
- **O princípio de §7.2**, de não falsificar registro datado, e a distinção entre
  registro e instrumento no `roteiro.md`. Só a aritmética estava errada.
- **A Sprint 4 como portão**, e a razão dela.
- **Declarar as exceções** em vez de deixá-las parecer esquecimento.
- **Os inventários de objeto**: 7/1/30/4/6/3, 7, 16, 12 — todos reproduzidos sem
  divergência.

---

## 12. Registro de execução

| Sprint | Status | Data | Auditoria | Observação |
|---|---|---|---|---|
| 0 | ✅ concluída | 2026-08-16 | dispensada | [relatório](docs/sprints/sprint-0-fundacao.md) |
| 0b | ✅ concluída | 2026-08-16 | dispensada | [relatório](docs/sprints/sprint-0b-fixtures-e-api-publica.md) |
| 1 | ✅ concluída | 2026-08-16 | ✅ 21 achados corrigidos | [relatório](docs/sprints/sprint-1-padroes.md) |
| 2 | ✅ concluída | 2026-08-16 | ✅ 13 quebras corrigidas + ADR-0006 | [relatório](docs/sprints/sprint-2-renomeacao.md) |
| 4 | ✅ concluída | 2026-08-16 | ✅ 9 achados corrigidos | [relatório](docs/sprints/sprint-4-hub-scripts.md) |
| 3 | ✅ concluída | 2026-08-17 | ✅ auditada com a 6 | [relatório](docs/sprints/sprint-3-skills.md) · `@hub-ml-*` confirmado no chat |
| 5 | 🟡 partes 1 e 2 | 2026-08-17 | **pendente** | [relatório](docs/sprints/sprint-5-hub-prompts.md) · as 16 partes 3 dependem de interação humana |
| 6 | ✅ concluída | 2026-08-17 | ✅ contrato de dados virou guarda | [relatório](docs/sprints/sprint-6-snippets-spark.md) |
| 7 | ✅ concluída | 2026-08-17 | ✅ 12 achados corrigidos + guarda de entrada | [relatório](docs/sprints/sprint-7-ml-nucleo.md) |
| 8 | ✅ concluída | 2026-08-17 | ✅ 13 achados corrigidos | [relatório](docs/sprints/sprint-8-ml-dependencia-opcional.md) · os 14 executam, via `%pip` |
| 9 | ✅ concluída | 2026-08-17 | ✅ 13 achados corrigidos | [relatório](docs/sprints/sprint-9-constants-visual-display.md) · fecha a biblioteca |
| 10 | ✅ concluída | 2026-08-17 | ✅ 12 achados corrigidos | [relatório](docs/sprints/sprint-10-readmes-de-topo.md) · glossário absorvido |
| 11 | ✅ concluída | 2026-08-17 | ✅ 19 achados corrigidos | [relatório](docs/sprints/sprint-11-hub-ml-criar-objeto.md) · forward test pendente |
| 12 | ✅ concluída | 2026-08-17 | ✅ 18 achados corrigidos | [relatório](docs/sprints/sprint-12-fechamento.md) · auditoria final do conjunto |

---

### 12.1 Dívida nomeada — notebooks sem saída real colada

O critério §7.1 item 4 exige "todo notebook da sprint executado, com saída real
colada". **Três sprints fecharam sem cumpri-lo**, e a exceção não estava anotada
em lugar nenhum fora da narrativa. Fica aqui, com nome e origem:

| Notebook | Sprint de origem |
|---|---|
| `hub_scripts/doc_coverage/exemplo_doc_coverage.py` | 4 |
| `hub_scripts/naming_checker/exemplo_naming_checker.py` | 4 |
| `hub_scripts/rfv_calculator/exemplo_rfv_calculator.py` | 4 |
| `hub_scripts/schema_to_yaml/exemplo_schema_to_yaml.py` | 4 |
| `hub_snippets/spark/date_features/exemplo_date_features.py` | 6 |
| `hub_snippets/spark/join_diagnostics/exemplo_join_diagnostics.py` | 6 |
| `hub_snippets/spark/null_summary/exemplo_null_summary.py` | 6 |
| `hub_snippets/spark/pit_join/exemplo_pit_join.py` | 6 |
| `hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py` | 6 |
| `hub_snippets/spark/smart_sample/exemplo_smart_sample.py` | 6 |
| `hub_snippets/testing/fixtures/exemplo_fixtures.py` | 6 |

São **11**, e nenhum é das Sprints 7 a 11. O exemplar de `hub_padroes/`, que
era o décimo segundo, foi fechado na auditoria da Sprint 11 — ele é o molde que a
skill manda ler, e não podia ser o primeiro a violar a regra que ela ensina.

#### ✅ Fechada em 2026-08-18

Os onze foram executados **como um job só** no Free, com um driver que roda cada
notebook célula a célula e captura o que cada uma imprime. Cinquenta blocos de
saída real entraram nos onze arquivos, cada um **na célula de markdown que lê o
resultado** — colar no fim do arquivo fecharia a guarda sem fechar a dívida.

O contador foi de `66 com bloco, 11 sem` para `77 com bloco, 0 sem`, e
`check_saida_colada` **foi promovida de aviso a falha**, que era a escada escrita
no docstring dela desde a Sprint 6.

Três armadilhas do caminho, registradas porque a próxima captura vai encontrá-las:

| Armadilha | Sintoma | Correção |
|---|---|---|
| `display()` não escreve em stdout | as tabelas saíam como `DataFrame[coluna: string, ...]` | *shim* que chama `show()`; e o teste é por `hasattr(obj, "show")`, porque **`_jdf` não existe no Spark Connect** |
| split do notebook por regex com `\s*$` | comia a linha em branco depois de cada marcador, alterando 11 arquivos num detalhe que ninguém pediu | `[ 	]*$`, com round-trip provado byte a byte nos 77 notebooks |
| o notebook do `doc_coverage` **cita** os marcadores de célula | split por literal partia o arquivo no meio do código | regex ancorada em início de linha |

A captura também trazia o caminho do workspace com o username; virou
`<username>` antes de entrar em arquivo versionado.

### 12.2 Dívida nomeada — cor redeclarada fora de `constants.colors`

Levantada pela auditoria da Sprint 9, que mostrou que o registro espalhado pelos
notebooks cobria **2 de 12** sítios e chamava de exemplar um módulo que também
copia. Esta tabela é o inventário; as menções nos notebooks apontam para cá.

| Módulo | Importa `colors`? | Hexadecimais que repetem valor oficial | Tipo |
|---|---|---|---|
| `constants/styles` | não | `AZUL_CAIXA`, `TEXTO_PRINCIPAL`, `BG_HEADER`, `BG_SECTION` | cópia idêntica |
| `visual/badge` | não | `AZUL_CAIXA`, `BG_HEADER` | cópia idêntica |
| `visual/divider` | não | `AZUL_CAIXA` | cópia idêntica |
| `visual/index_generator` | não | `AZUL_CAIXA`, `COR_NEUTRO`, `BG_SECTION` | cópia idêntica |
| `visual/kpi_card` | não | `TEXTO_PRINCIPAL`, `BG_HEADER` | cópia idêntica |
| `visual/theme_plotly` | **sim** | `CINZA_ESCURO` | cópia idêntica |
| `display/dataframe_styled` | não | `AZUL_CAIXA`, `VERMELHO` | cópia idêntica |
| `ml/curves_plotly` | não | 7 cores da paleta | **valor divergente** — 6 cores contra 10 |
| `ml/kaplan_meier` | não | 8 cores da paleta | cópia idêntica |
| `ml/performance_monitor` | não | `AZUL_CAIXA`, `VERMELHO`, `LARANJA` | cópia idêntica |
| `ml/umap_viz` | não | 11 cores da paleta | cópia idêntica |
| `ml/vintage_analysis` | não | 10 cores da paleta + a sequencial | cópia idêntica |

**A distinção que decide o custo da etapa 2** está na última coluna. Onze dos
doze são **cópia idêntica**: unificar é substituir literal por import, sem
nenhum efeito visual. Só `ml/curves_plotly` tem **valor divergente** — sua
`PALETA_CATEGORICA` tem seis cores contra as dez da original —, e unificar ali
muda a aparência de todo gráfico que ele produz. É a única linha que precisa de
decisão de produto; as outras onze são higiene.

**E há um caso à parte:** `constants/styles` não é importado por **nenhum**
módulo, e suas oito constantes de estilo são cópia byte a byte de CSS que vive
inline em `visual/badge`, `visual/divider`, `visual/kpi_card`,
`visual/section_header` e `visual/index_generator`. O módulo inteiro é um espelho
morto. Editar `STYLE_SECTION_HEADER` não muda cabeçalho nenhum — e o notebook de
`section_header` chegou a afirmar o contrário.

#### ✅ Higiene fechada em 2026-08-18 · 1 decisão em aberto

Os onze sítios de cópia idêntica passaram a derivar de `constants.colors`.
**Trinta hexadecimais saíram do código**; sobraram os seis da linha divergente,
agora marcada `PENDENTE/DECISAO` no próprio arquivo.

A unificação foi feita sob três provas, e nenhuma delas é opinião:

| Prova | Como |
|---|---|
| valor idêntico | o script aborta se o literal não bater byte a byte com o nome oficial — 14 nomes e 2 paletas conferidos antes da primeira substituição |
| saída idêntica | os oito grupos de função de `visual/` capturados antes e depois: **zero divergências** |
| API pública idêntica | `api_publica.py` regerado nos 51 módulos: **zero `__init__.py` divergentes** |

**A armadilha que a terceira prova pegou.** A forma óbvia — trocar
`AZUL_CAIXA = "#005CA9"` por `from ... import AZUL_CAIXA` — **quebraria a API
pública** de quatro módulos, porque `api_publica.py` exclui do `__all__` o que foi
apenas importado, e esses nomes são reexportados pelos `__init__.py` desde a
Sprint 7. A forma correta é atribuição derivada, `AZUL_CAIXA = colors.AZUL_CAIXA`:
unifica o valor e preserva o contrato.

**A ordem também importa.** Em `ml/kaplan_meier` a lista de oito cores **não** é
`PALETA_CATEGORICA[:8]` — `CINZA_ESCURO` vem por último ali. Fatiar a paleta teria
trocado a cor de quatro curvas em silêncio; nomear preserva a atribuição.

**A decisão que resta é sua:** a `PALETA_CATEGORICA` de `ml/curves_plotly` tem
seis cores. Adotar a oficial não muda gráfico nenhum de até seis séries, e muda
todos os que passam disso — hoje a sétima série recomeça no azul, e passaria a
ser roxo.

`constants/styles` continua sendo espelho morto quanto ao CSS, e agora **diz isso
no próprio docstring**. Suas cores institucionais já derivam de `colors`; unificar
o CSS mexeria na saída de cinco módulos e é decisão de produto, não higiene.

---
