---
name: hub-ml-criar-objeto
description: Cria objeto novo do Hub — snippet, script, prompt, README, notebook de exemplo ou skill — aplicando o template correspondente de `.assistant/hub_padroes/`, com a pasta, o `__init__.py`, o módulo e o notebook que o ensina. Use quando pedirem para criar, adicionar, padronizar ou converter um helper, utilitário, prompt, documento ou skill do ecossistema `.assistant`, ou quando perguntarem qual é o formato de um objeto do Hub. Não cobre escrever a lógica de análise em si, nem alterar objeto já existente sem que a conversão para o padrão seja o pedido.
---

# Criar objeto do Hub

Esta skill aplica os moldes de `.assistant/hub_padroes/`. Ela **não** inventa
formato: se o template divergir do que está escrito aqui, o template vence, e a
divergência é defeito a corrigir.

## Escolher o tipo antes de escrever qualquer linha

A lista é **fechada**: seis tipos, e nada fora dela. Escolher errado custa a
reescrita inteira, porque a forma muda.

| O objeto… | é | template |
|---|---|---|
| recebe DataFrame ou valores e devolve resultado | **snippet** | `hub_padroes/snippet/template.md` |
| recebe **nome de tabela** e devolve um veredito | **script** | `hub_padroes/script/template.md` |
| é texto que a pessoa preenche e cola no chat | **prompt** | `hub_padroes/prompt/template.md` |
| explica uma pasta para quem chega | **README** | `hub_padroes/readme/template.md` |
| ensina a usar um objeto, executando | **notebook** | `hub_padroes/notebook/template.py` |
| é instrução que o Genie Code carrega sozinho | **skill** | `hub_padroes/skill/template.md` |

A distinção entre snippet e script é a que mais erra, e ela muda a assinatura:
snippet recebe **dado**, script recebe **nome de tabela**. Na dúvida, pergunte
quem chama a função — se for um notebook passando um DataFrame já carregado, é
snippet.

Confirme o tipo com quem pediu antes de seguir. Se o pedido não couber em nenhum
dos seis, **diga isso** em vez de forçar o mais próximo.

## Ler o template inteiro, sempre

Anexe o template do tipo escolhido com **Add context** ou `@`. Eles não são
auto-descobertos: sem anexar, você está trabalhando de memória, e o formato muda
entre versões.

Leia também o exemplo preenchido que acompanha o template, em
`hub_padroes/<tipo>/<exemplo>/`. Ele mostra a forma completa sobre um caso de CRM
real, e é mais rápido de ler do que a especificação.

## Nomear

| Tipo | Convenção | Motivo |
|---|---|---|
| snippet, script, prompt | `snake_case` | é identificador Python; a pasta vira caminho de import |
| skill | `hub-ml-<tema>`, com hífen | é a plataforma que nomeia, não o Python |

O nome da pasta e o do módulo são **iguais**: `pit_join/pit_join.py`. O validador
reprova qualquer outra combinação.

Verifique antes se o nome já existe. Dois objetos com nomes próximos —
`drift_detection` e `drift_detector` — já convivem na biblioteca, um em
`hub_snippets/ml` e outro em `hub_scripts`, e a distinção entre eles não é óbvia
pelo nome. Não crie um terceiro.

## Montar a pasta

Para snippet e script, três arquivos e nada mais:

```text
hub_snippets/<secao>/<nome>/
├── __init__.py                 # NÃO escreva à mão
├── <nome>.py                   # a implementação
└── exemplo_<nome>.py           # o notebook que ensina
```

O `__init__.py` sai da ferramenta, no repositório:

```bash
python tools/api_publica.py <caminho>/<nome>.py > <caminho>/__init__.py
```

Ela lê o módulo por AST e reexporta **todos** os nomes públicos de nível
superior. A regra é exaustiva, não curada — e isso não é preferência: uma
curadoria plausível de `constants/colors`, que tem 22 nomes, exportaria cinco e
quebraria o import de quem depende, com o sintoma aparecendo sprints depois da
causa.

Sem acesso ao repositório, escreva o `__init__.py` listando **todos** os nomes
sem underscore inicial, e avise que ele precisa ser regenerado pela ferramenta
antes do commit.

## Escrever o módulo

O que o template exige, e que a revisão vai cobrar:

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

## Escrever o notebook, que não é opcional

**Todo snippet e todo script têm o seu**, inclusive os triviais. Um leitor que
encontra notebook em doze pastas e não na décima terceira desconfia da décima
terceira.

O formato está em `hub_padroes/notebook/template.py`. A ordem importa:

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

Se o objeto depende de biblioteca ausente no ambiente, abra o notebook com
`%pip install <lib>` seguido de `%restart_python`. Consulte
`hub_snippets/requirements-optional.txt` antes: três bibliotecas exigem pin, e
essas três juntas na mesma sessão quebram o `import numpy`.

Se um trecho realmente não puder rodar, use o **bloco canônico de não executado**
do template, com o motivo verificado e o erro real citado. Motivo válido é
impedimento do objeto ou do runtime — nunca "não deu tempo" nem "é decisão de
escopo".

## Converter objeto que já existe

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

## Verificar antes de dar por pronto

```text
[ ] o tipo foi confirmado com quem pediu, e é um dos seis
[ ] a pasta tem exatamente os arquivos do padrão, com os nomes certos
[ ] o módulo se chama como a pasta
[ ] o __init__.py saiu da ferramenta, sem edição manual
[ ] se é conversão: assinatura, colunas e casos de borda inalterados
[ ] o notebook executou, e a saída colada é literal
[ ] a seção "quando não usar" existe e é específica
[ ] o README da seção lista o objeto novo
[ ] o catálogo de helpers ganhou a linha correspondente
```

Os quatro primeiros o validador confere sozinho, no repositório:
`python tools/validate_assistant.py`. Os demais são humanos — e o do catálogo é o
mais esquecido: dois objetos ficaram fora dele por uma sprint inteira, e ficaram
indescobríveis pela rota que o README recomenda.

## Usar recursos

- `templates/checklist-objeto-novo.md` — a lista acima em formato para colar numa
  PR ou num chamado, com as verificações de conversão separadas.
