---
name: hub-ml-criar-objeto
description: Cria objeto novo do Hub — snippet, script, prompt, README, notebook de exemplo ou skill — aplicando o template correspondente de `.assistant/hub_padroes/`, com a pasta, o README humano, o `__init__.py` aplicável, o módulo e o notebook que o ensina. Use quando pedirem para criar, adicionar, padronizar ou converter um helper, utilitário, prompt, documento ou skill do ecossistema `.assistant`, ou quando perguntarem qual é o formato de um objeto do Hub. Não cobre escrever a lógica de análise em si, nem alterar objeto já existente sem que a conversão para o padrão seja o pedido.
---

# Criar objeto do Hub

Esta skill aplica os moldes de `.assistant/hub_padroes/`. Ela **não** inventa
formato: se o template divergir do que está escrito aqui, o template vence, e a
divergência é defeito a corrigir.

## Quando esta skill se aplica

**Caso típico:** alguém tem uma lógica que já escreveu duas vezes em notebooks
diferentes e quer transformá-la em objeto do Hub, para que a terceira vez seja um
`import`.

Dois contra-exemplos, para não roubar a vez de quem faz o trabalho de verdade:

- **"Como calculo PSI entre duas safras?"** — é pergunta de estatística, não de
  formato. Vai para `hub-ml-validacao-estatistica` ou
  `hub-ml-monitoramento-modelo`. Esta skill só entra se a pessoa disser que quer
  **guardar** esse cálculo como objeto.
- **"Melhore o `pit_join` para aceitar múltiplas chaves."** — é alteração de
  objeto existente, não criação. Só entra aqui se o pedido for **converter ao
  padrão**; mudar comportamento é trabalho de quem conhece o domínio.

## Executar o preflight SEF L2 antes de criar ou converter

Pedidos puramente explicativos sobre o formato de um objeto permanecem em orientação.
Antes de **criar** ou **converter** qualquer objeto, executar
`scripts/preflight.py::preflight`.

O contexto mínimo deve declarar:

- `operation="create"|"convert"`;
- `object_type` entre os seis tipos fechados;
- `object_name`;
- `type_confirmed=true`;
- `existing_capability_checked=true`;
- `existing_capability_status="not_found"|"found"`.

Quando uma capacidade existente for encontrada, registrar também
`overlap_resolution` como uma decisão explícita. Criar um recorte novo só é
permitido com `create_declared_slice`; decisões como `extend_existing`,
`convert_existing` ou `refuse` bloqueiam a rota de criação de objeto novo.

Para snippet, informar `snippet_section`. As seis seções atuais são aceitas
diretamente; uma seção nova exige `new_snippet_section_authorized=true`.
Essa autorização continua limitada a um único componente de caminho seguro.
Origem, destino e template devem resolver dentro da raiz `.assistant`, inclusive
quando há links ou junctions nos ancestrais; drive-relative, UNC e traversal
não são destinos relativos válidos.
Resolução cíclica ou erro de resolução bloqueia a pré-condição. Um sufixo
inexistente sob cadeia resolvível e contida continua elegível; isso inclui
destino novo por link quebrado interno. A tolerância à ausência não mascara um
arquivo como ancestral nem outro erro revelado pelo caminho efetivo normalizado.
Não é proteção de escrita contra TOCTOU.

Para README, informar `readme_scale="agregador"|"objeto"` e o destino
relativo. Para notebook, informar o destino relativo `.py`.

Em conversão, informar `source_relative`; o preflight valida que a origem
existe e preserva a regra “converter é mover, não mudar comportamento”.
Aliases que resolvem para o mesmo objeto não são movimento. A política para
origem `"."`, relações ancestral/descendente e destino existente permanece
pendente de decisão específica; o PASS L2 nesses casos não autoriza overwrite,
merge, remoção nem execução de conversão.

O preflight:

- resolve o template canônico e o destino antes da escrita;
- valida somente regras de nome realmente definidas nesta skill;
- não cria pasta, arquivo, `__init__.py` ou notebook;
- não executa `api_publica.py`, `validate_assistant.py` ou código analítico;
- retorna `BLOCKED` quando uma decisão obrigatória ainda não existe.

A API e a CLI devolvem diagnóstico estruturado para entradas inválidas; falhas
inesperadas de implementação continuam visíveis como erros. Resolver o path do
template não prova sua leitura: `template.read_status=NOT_OBSERVABLE`.
A contenção é conferida no instante do preflight, sem garantia contra troca
concorrente de links depois da checagem. Este L2 não é um mecanismo de escrita.

## Validação estrutural L3 candidata — rota repo-side com Receipt de domínio

Para `create` de **snippet, script, prompt, notebook e README agregador**, a superfície
`object_validation` possui uma rota determinística candidata separada da escrita.
O produtor canônico é `tools/skill_enforcement/ser01_object_validation.py`, executado
somente em checkout Git completo; ele não viaja com o pacote publicado.

Um PASS precisa emitir `SER01-OBJECT-VALIDATION-RECEIPT-1`. O verifier publicado é
`scripts/object_validation.py::verify_receipt`: confere versão, binding da candidata,
base, run, record local e claims fechados. Ele não reexecuta Git/tools, não autentica
pessoa/executor e não converte hash em assinatura. `runtime_validation` permanece
`NOT_RUN`, inclusive para notebook.

Sem Receipt válido, a skill não pode apresentar `object_validation` como L3 demonstrada
nem declarar o objeto pronto por essa superfície. Onde a rota repo-side não existe,
registrar `NOT_AVAILABLE`/bloqueio; não substituir por validação informal. O Receipt
também não autoriza `apply`: geração, validação, autorização e escrita são gates distintos.

## Piloto determinístico — somente create/readme/agregador

`scripts/run.py` oferece `generate` e `apply` separados. É piloto local;
policy e `current_level=L2` continuam inalterados. O contrato e o preflight L2
acima preservam suas regras; a superfície writer impõe limites adicionais.

`generate(context, document, base_sha=..., assistant_root=...)` chama L2,
lê o template agregador e devolve bytes completos UTF-8/LF em memória.
`document` declara `title`, `identity`, `purpose`, `usage`, `limitations`,
`next_steps` e `items` (`path`, `description`) correspondentes à pasta real.
O binding registra operação/tipo/escala, destino, hash/tamanho dos bytes,
generation_id, base Git, release e template. GERADO não é validado ou escrito.

A validação estrutural depende de `tools/skill_enforcement/validate_create_readme.py`
no repositório: clone descartável completo, overlay exato e validator real.
Essa ferramenta não viaja no produto. O runtime exige seu registro vinculado;
não alega executar `tools/` nem autenticar o emissor do registro local.

`apply(candidate, authorization, validation, assistant_root=...,
evidence_dir=..., evidence_authorized=True)` exige autorização
`AUTHORIZE_CREATE`, authority `external_confirmation_record`, identificador
não vazio e binding exatamente correspondente. Esse artefato prova apresentação
de registro, não identidade humana ou assinatura. Não gerar autorização automática.
O caller precisa autorizar separadamente a persistência em diretório externo
novo de evidência. Sem isso, nenhuma escrita do produto é permitida.

Somente um `README.md` ausente, em pasta real existente, dentro da raiz permitida.
Windows/NTFS local é o envelope suportado quando demonstrado no host; outros
hosts/filesystems bloqueiam. Não suportar symlink/junction nos ancestrais,
hardlink/destino existente, escape, conversão, novos diretórios ou overwrite.
`apply` revalida bindings, bytes, release/template, L2, raiz/ancestrais e ausência;
nunca regenera o conteúdo. Criação exclusiva falha em caso de concorrência.

Evidência diferencia GERADO, validação apresentada, autorização apresentada,
ESCRITO e falha/interrupção. `homologated=False` sempre. Se houver criação
parcial ou erro após a escrita, conservar o efeito e registrar inconclusão;
não apagar nem repetir para sobrescrever. Inspecionar bytes e evidência antes
de uma decisão humana de recuperação. Retry com destino existente bloqueia.
O verifier comprova integridade/coerência dos registros, não autenticidade
humana nem transação universal. Free/Genie e promoção de nível são gates futuros.

## Fluxo

### 1. Escolher o tipo, antes de escrever qualquer linha

A lista é **fechada**: seis tipos, e nada fora dela. Escolher errado custa a
reescrita inteira, porque a forma muda.

| O objeto… | é | template |
|---|---|---|
| recebe DataFrame ou valores e devolve resultado | **snippet** | `hub_padroes/snippet/template.md` |
| recebe o **endereço do que vai diagnosticar** e devolve um veredito | **script** | `hub_padroes/script/template.md` |
| é texto que a pessoa preenche e cola no chat | **prompt** | `hub_padroes/prompt/template.md` |
| explica uma pasta para quem chega | **README** | `hub_padroes/readme/template.md`; escala Objeto: `template_objeto.md` na mesma pasta |
| ensina a usar um objeto, executando | **notebook** | `hub_padroes/notebook/template.py` |
| é instrução que o Genie Code carrega sozinho | **skill** | `hub_padroes/skill/template.md` |

A distinção entre snippet e script é a que mais erra, e ela muda a assinatura:
snippet recebe **dado já carregado**; script recebe o **endereço** — nome de
tabela, tipicamente, ou caminho de arquivo, como faz `hub_scripts.doc_coverage`.
Na dúvida, pergunte quem chama: se for um notebook passando um DataFrame que ele
já tem, é snippet.

`hub_padroes/` tem uma sétima pasta, `auditoria/`. Ela é molde de **processo**,
não tipo de objeto, e não conta entre os seis.

Confirme o tipo com quem pediu antes de seguir. Se o pedido não couber em nenhum
dos seis, **diga isso** em vez de forçar o mais próximo.

### 2. Ler o template inteiro

Anexe o template do tipo escolhido com **Add context** ou `@`. Eles não são
auto-descobertos: sem anexar, você está trabalhando de memória, e o formato muda
entre versões.

Leia também o exemplo preenchido, quando houver — `hub_padroes/README.md` tem a
tabela que diz qual acompanha cada template. Snippet, script, prompt e skill têm
exemplar em pasta própria — que se **lê, e não se copia**: qualquer pasta dentro
de `.assistant/skills/` é auto-descoberta, e uma cópia do exemplar viraria skill
fantasma no chat. README tem um arquivo `exemplo.md`; notebook não tem
exemplar separado, porque os exemplares dos outros tipos já trazem o seu.

Se o tipo for skill, siga também [Estrutura SEF de uma skill](references/estrutura-skill-sef.md):
ela distingue `SKILL.md`, `execution_contract.json`, entrada na policy canônica,
scripts de cada nível e manifesto de release quando aplicável. O preflight L2
confere tipo, nome e destino, mas não gera esses arquivos nem valida a skill pronta.

Os exemplares usam um caso de CRM **sintético**, do domínio da equipe. São
referência de forma — não os importe em trabalho real, e não copie os dados.

### 3. Nomear

| Tipo | Convenção | Motivo |
|---|---|---|
| snippet, script, prompt | `snake_case` | é identificador Python; a pasta vira caminho de import |
| skill | `hub-ml-<tema>`, com hífen | é a plataforma que nomeia, não o Python |

O nome da pasta e o do módulo são **iguais**: `pit_join/pit_join.py`. Não é
convenção estética — é o que faz o import documentado existir. Um
`taxa_nulos/calcula.py` produz uma pasta que ninguém consegue importar pelo
caminho que o catálogo promete.

Antes de escolher, procure o que já existe:

```bash
grep -ri "<demanda>" .assistant/MANUAL_TECNICO.md#catalogo-helpers
```

Se a demanda já estiver coberta, **não crie um objeto novo em silêncio**. Traga a
decisão para quem pediu: estender o existente, criar um recorte declarado, ou
recusar. `hub_snippets.spark.null_summary` e um "taxa de nulos por coluna" são o
mesmo objeto com nomes diferentes.

E confira nomes próximos: `drift_detection` (em `hub_snippets/ml`) e
`drift_detector` (em `hub_scripts`) já convivem, e a distinção entre eles não é
óbvia pelo nome. Não crie um terceiro.

### 4. Montar a pasta

Snippet, dentro de uma das seis seções existentes — `constants`, `display`, `ml`,
`spark`, `testing`, `visual`:

```text
hub_snippets/<secao>/<nome>/
├── README.md                   # conceito, escolha e uso seguro
├── __init__.py                 # NÃO escreva à mão
├── <nome>.py                   # a implementação
└── exemplo_<nome>.py           # o notebook que ensina
```

Script, que **não tem nível de seção**:

```text
hub_scripts/<nome>/
├── README.md
├── __init__.py
├── <nome>.py
└── exemplo_<nome>.py
```

**Não crie seção nova sem decidir com quem pediu.** O `__init__.py` de seção não
reexporta nada — e isso é deliberado: se reexportasse, um módulo com dependência
ausente derrubaria a seção inteira e os irmãos junto. Gerar o `__init__.py` de
uma seção com a ferramenta quebraria essa propriedade.

O `__init__.py` do **objeto** sai da ferramenta, no repositório:

```bash
python tools/api_publica.py <caminho>/<nome>.py > <caminho>/__init__.py
```

Ela lê o módulo por AST e reexporta **todos** os nomes públicos de nível
superior. A regra é exaustiva, não curada — e isso não é preferência: uma
curadoria plausível de `constants/colors`, que tem 22 nomes, exportaria cinco e
quebraria o import de `visual/section_header` e `visual/theme_plotly`, com o
sintoma aparecendo sprints depois da causa.

Sem acesso ao repositório, escreva o `__init__.py` listando **todos** os nomes
sem underscore inicial, e avise que ele precisa ser regenerado pela ferramenta
antes do commit.

### 5. Escrever o módulo

| Elemento | Regra |
|---|---|
| Docstring do módulo | **por que existe**, não o que faz. Se a única frase possível é "calcula X", o objeto talvez não mereça existir |
| Decisão de projeto | toda escolha não óbvia vira comentário com o motivo, não só com a descrição |
| Docstring da função | `Args`, `Returns`, `Raises` e, quando houver armadilha, `Note` |
| Validação de entrada | falhe cedo, com mensagem que diga **o que fazer**, não só o que houve |
| Constante de política | limite calibrável é constante nomeada no topo, nunca embutido no corpo |
| Sessão Spark | `SparkSession.getActiveSession() or ...getOrCreate()` — o global `spark` **não existe** dentro de módulo importado |

O que nunca fazer:

- **Silenciar ambiguidade com valor padrão.** Nulo na coluna de resposta pode ser
  "não respondeu" ou "falha de registro"; tratar como zero enviesa sem rastro.
  Recuse e explique.
- `cache()` ou `persist()` sem proteção: bloqueados em serverless.
- `toPandas()` sem limite verificável.
- Sentinela como `-1` para sinalizar erro. Devolva diagnóstico ou levante.
- Importar biblioteca opcional no topo quando ela puder ser adiada — isso decide
  se o objeto importa ou não no laboratório.

#### Sistema de Temas em objetos visuais

Ao criar um objeto que aceite aparência configurável, não invente `TEMA_*`, paleta local ou JSON paralelo. Consulte `hub_padroes/identidade_visual`, receba/propague um `ResolvedTheme` quando o contrato do objeto exigir theming e reutilize o adaptador/consumidor `_resolvido` existente.

`hub_snippets.constants.colors` continua válido para **compatibilidade legada** e componentes não configuráveis que já dependem dessas constantes; ele não é a fonte de um tema novo. Não altere cálculo, threshold, agregação ou amostragem para fazer uma proposta visual funcionar. Não registre template global como efeito padrão de um objeto novo.

### 6. Escrever o notebook, que não é opcional

**Todo snippet e todo script têm o seu**, inclusive os triviais. Um leitor que
encontra notebook em doze pastas e não na décima terceira desconfia da décima
terceira.

**A primeira linha do arquivo tem de ser exatamente:**

```python
# Databricks notebook source
```

Sem ela o arquivo não é notebook — nem para o Databricks, nem para o validador,
que vai acusar dois erros contraditórios sobre o mesmo arquivo ("módulo extra" e
"falta o notebook"). E a publicação envia o arquivo no formato errado, o que
quebra o import no workspace. É a exigência mais fácil de esquecer e a mais cara.

O resto do formato está em `hub_padroes/notebook/template.py`. A ordem importa:

1. cabeçalho com o **problema real**, não com a descrição da função;
2. tabela "o que este notebook assume do ambiente" — compute, bibliotecas, dados,
   **se escreve algo**, e diferença entre Free e trabalho;
3. o erro acontecendo, quando o objeto tem um erro típico associado;
4. a chamada certa, e **a saída real colada** em bloco de texto;
5. fechamento com "quando **não** usar".

Sobre o item 4, que é onde a maioria falha: **cite o número obtido, não o
pretendido.** "O PSI sai alto" não se confere; "o PSI sai em 2,94" se confere. E
cole a saída **literal**, inclusive feia — se precisar cortar, diga que cortou,
nunca complete.

**O notebook e o módulo têm um contrato que a validação confere.** Ela compara o
que o notebook consome (`resultado["chave"]`) com o que o módulo devolve, e o que
o notebook passa (`fn(arg=...)`) com a assinatura. Um `resultado["taxa"]` para um
módulo que devolve `taxa_nulos_pct` reprova — então escreva o notebook lendo a
assinatura real, não a que você imagina.

Se o objeto depende de biblioteca ausente no ambiente, abra o notebook com
`%pip install <lib>` seguido de `%restart_python`. Consulte
`hub_snippets/requirements-optional.txt` antes: três bibliotecas exigem pin, e
essas três juntas na mesma sessão quebram o `import numpy`.

Se um trecho realmente não puder rodar, use o **bloco canônico de não executado**
do template, com o motivo verificado e o erro real citado. Motivo válido é
impedimento do objeto ou do runtime — nunca "não deu tempo" nem "é decisão de
escopo".

### 7. Converter objeto que já existe

Converter é **mover**. A conversão não muda comportamento: se o módulo antigo
devolve 0% em base vazia, o convertido devolve 0% em base vazia, mesmo que o
template peça "falhe cedo".

| Etapa | O que entra | O que **não** entra |
|---|---|---|
| **1. Mover** | pasta, `__init__.py` gerado, notebook novo, docstring ampliada | nenhuma mudança de assinatura, de valor devolvido ou de comportamento de borda |
| **2. Melhorar** | validação, constante de política, recusa em caso ambíguo | — |

São **commits separados**. Sem essa separação, cada pessoa decide sozinha quanto
do módulo antigo sobrevive, e a diferença só aparece quando algo que funcionava
para de funcionar.

**Não traduza identificador.** Parâmetro, coluna devolvida e nome de função ficam
como estão; docstring, comentário e notebook vão em português. Um módulo com
`threshold_warn` e docstring em português é inconsistente e correto; um com
`limite_alerta` é consistente e quebrado.

### README humano da pasta

Todo snippet, script e prompt novo inclui `README.md` segundo
[`template_objeto.md`](../../hub_padroes/readme/template_objeto.md). O
[checklist editorial](../../hub_padroes/readme/checklist_objeto.md) é o dono da
rubrica didática. Não copie seu conteúdo para esta skill. Leia README e exemplo
seletivamente; nunca carregue todos os documentos como preâmbulo.

Prompts mantêm briefing e exemplo; o README é o terceiro arquivo e não substitui
os guias de preenchimento. Em legados, a transição é controlada no repositório.
A migração documental não altera APIs, regras de negócio ou código executável.

## Usar helpers da biblioteca

O Genie Code **não** descobre `hub_snippets` sozinho: a skill recomenda por
caminho de import, e quem importa é a pessoa, no notebook (ADR-0004). Catálogo
completo em [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda ao escrever o objeto | Módulo |
|---|---|
| Base sintética determinística para o notebook | `hub_snippets.testing.fixtures` |
| Números do notebook no padrão brasileiro | `hub_snippets.constants.format_br` |
| Tema visual configurável e rodapé | `hub_snippets.visual.tema`, `hub_snippets.visual.theme_plotly` |
| Cores institucionais legadas | `hub_snippets.constants.colors` — compatibilidade legada; não é fonte de tema novo |
| Exibir DataFrame grande sem varredura completa | `hub_snippets.spark.safe_display` |

Duas ferramentas do repositório, que não são helpers de notebook e sim de quem
edita: `tools/api_publica.py` gera o `__init__.py`, e
`tools/validate_assistant.py` confere a forma.

## O que nunca fazer

- **Criar objeto para demanda já coberta**, sem trazer a decisão para quem pediu.
- **Inventar sétimo tipo.** Se não couber nos seis, diga que não couber.
- **Escrever o notebook a partir da docstring**, sem ler a assinatura. Foi assim
  que nove notebooks desta biblioteca nasceram quebrados.
- **Colar saída editada** como se fosse literal. Um bloco curado é
  indistinguível de um inventado para quem lê depois.
- **Criar seção nova** em `hub_snippets/` por conta própria.
- **Prometer que o validador confere** o que ele não confere — ver a seção
  seguinte.

## Formato de saída

Entregue, nesta ordem:

1. **O tipo escolhido e por quê**, em uma frase — para quem pediu confirmar.
2. **Os artefatos exigidos pelo molde do tipo**, completos, com o caminho de
   cada um. Snippet e script incluem quatro arquivos; prompt inclui três; README e
   notebook têm um; skill tem `SKILL.md` e apenas os recursos necessários.
3. **O comando** que gera o `__init__.py`, para quem tem o repositório rodar.
4. **A lista do que ficou por fazer** — o notebook precisa ser executado, o
   catálogo precisa da linha, o CHANGELOG precisa da entrada.

Não entregue "um esboço para você completar". Objeto pela metade entra na
biblioteca e fica.

## Verificar antes de dar por pronto

O checklist completo, com um bloco por tipo de objeto, está em
[`templates/checklist-objeto-novo.md`](templates/checklist-objeto-novo.md). Cole
numa PR ou num chamado.

**Sobre o que a ferramenta confere, e o que ela não confere** — importa saber a
diferença antes de confiar:

| Verificação | Quem faz |
|---|---|
| a pasta tem os artefatos exigidos pelo molde, com os nomes do padrão | `validate_assistant.py` |
| o módulo tem o nome da pasta | `validate_assistant.py` |
| o `__init__.py` bate com a API pública do módulo | `validate_assistant.py` |
| o notebook consome chave que o módulo devolve | `validate_assistant.py` |
| o notebook passa argumento que a assinatura aceita | `validate_assistant.py` |
| o notebook tem um bloco de saída (não comprova autenticidade) | `validate_assistant.py`, como **falha** quando ausente |
| README tem versão, seções e links locais e respeita a migração | `readme_objeto_contract.py`, integrado ao validador |
| **o tipo foi confirmado com quem pediu** | **você** |
| **a saída colada é literal, e não editada** | **você** |
| **a demanda já não estava coberta** | **você** |
| **o notebook executou de verdade** | **você** |
| **o catálogo ganhou a linha** | **você** |

As cinco de baixo são as que mais custam quando falham, e nenhuma tem portão.
A do catálogo é a mais esquecida: dois objetos ficaram fora dele por uma sprint
inteira, indescobríveis pela rota que o próprio README recomenda.

## Usar recursos

- [`templates/checklist-objeto-novo.md`](templates/checklist-objeto-novo.md) — o
  checklist canônico, com bloco por tipo e a separação entre o que um terceiro
  verifica e o que é juízo de quem escreveu.
