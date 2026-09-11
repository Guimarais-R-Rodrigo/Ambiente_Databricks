# `hub_padroes/` — templates do Hub

Quando cada pessoa cria um objeto com uma organização diferente, a revisão precisa redescobrir onde estão contrato, implementação e exemplo. Um molde reduz essa variação. Ele define a estrutura esperada, mas não certifica a fórmula, a análise ou o acesso aos dados.

> **Candidato para revisão, ainda não oficial.** Este guia não promove os rascunhos nem os exemplares para a biblioteca de produção.

> **HUB · Consulta e contexto explícito.** A pasta de padrões é customizada. Abra ou selecione o arquivo adequado como contexto. A skill `@hub-ml-criar-objeto` pode orientar a criação, mas suas ações continuam sujeitas às permissões e ao modo de aprovação das ferramentas.

---

## Escolha o objeto

Há seis tipos de objeto. `auditoria/` e `output/` são padrões transversais de processo, não novos tipos de produto.

| Quero criar | Necessidade | Molde | Exemplar didático |
|---|---|---|---|
| README | Explicar uma coleção ou fluxo | [README](../../../ambiente_fonte/.assistant/hub_padroes/readme/template.md) | [Exemplo preenchido](../../../ambiente_fonte/.assistant/hub_padroes/readme/exemplo.md) |
| Snippet | Oferecer função ou classe reutilizável | [Snippet](../../../ambiente_fonte/.assistant/hub_padroes/snippet/template.md) | [Taxa de resposta](../../../ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/) |
| Script | Resolver uma tarefa delimitada sobre um recurso | [Script](../../../ambiente_fonte/.assistant/hub_padroes/script/template.md) | [Checagem de campanha](../../../ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/) |
| Prompt | Formular uma demanda para a conversa | [Prompt](../../../ambiente_fonte/.assistant/hub_padroes/prompt/template.md) | [Analisar campanha](../../../ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/) |
| Skill | Orientar um método carregável pelo agente | [Skill](../../../ambiente_fonte/.assistant/hub_padroes/skill/template.md) | [Skill de exemplo](../../../ambiente_fonte/.assistant/hub_padroes/skill/exemplo/) |
| Notebook | Demonstrar uma execução acompanhada | [Notebook](../../../ambiente_fonte/.assistant/hub_padroes/notebook/template.py) | Notebooks das pastas de exemplar acima |

A coluna de molde oferece a estrutura de autoria; a de exemplar mostra uma aplicação didática. Não confunda esses arquivos com helpers ativos destinados a um pipeline real. Um exemplar serve para aprender forma, contrato e revisão.

---

## Fluxo recomendado

Comece pela necessidade, escolha o tipo, leia molde e exemplar, defina o contrato e prepare a demonstração. Depois valide estrutura e conteúdo separadamente. A proposta só entra na biblioteca ou na pasta de descoberta após revisão e aprovação.

### Como ler o template

Abra o arquivo e identifique as seções obrigatórias, os campos substituíveis e os limites. Se usar a Genie Code, selecione o arquivo de fato na interface de contexto. Digitar uma string `@caminho` sem selecionar um recurso existente não comprova que seu conteúdo foi carregado.

### O que preencher

Defina público, problema, entrada, retorno, pré-condições, efeitos, dependências e exemplo. Um contrato descreve a interface e seu significado: tipo, unidade, granularidade, tempo e comportamento diante de entradas inválidas. Um critério de aceite permite conferir se o contrato foi demonstrado, não apenas descrito.

### Duas rotas

**Manual.** Leia o molde, prepare uma proposta no local de trabalho autorizado e confronte cada seção com o exemplar. Não copie mecanicamente o código de domínio apenas porque deseja copiar sua organização.

**Com Genie Code.** Selecione os arquivos reais de template e exemplar e use um pedido como este:

```text
@hub-ml-criar-objeto
Quero planejar um snippet de taxa de resposta por segmento para uma campanha sintetica.
Use o template e o exemplar taxa_resposta_campanha selecionados no contexto.
Antes de escrever arquivos, apresente nome, publico, grao de entrada e saida,
assinatura, tratamento de resposta nula ou fora de 0/1, unidade da taxa,
intervalo de incerteza, dependencias e exemplos de aceite.
Nao altere o algoritmo do exemplar nem proponha retorno escalar em seu lugar.
Apenas explique e planeje nesta etapa; nao execute codigo ou alteracoes.
```

Esse pedido delimita a fase. Confira também as aprovações de ferramentas: uma orientação textual não é um controle de acesso. Se o objetivo posterior exigir uma mudança estatística, trate-a como mudança de comportamento, com justificativa e testes próprios.

### Como criar um exemplo que comprova o contrato

A figura mostra o padrão físico de um snippet: interface, implementação e demonstração têm responsabilidades separadas.

![Fachada pública, implementação e notebook de exemplo em uma pasta de snippet.](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/snippets/png/01_anatomia_pasta.png)

A demonstração deve importar a API, construir os dados, chamar a função e interpretar seu retorno. Uma célula que só importa e termina não prova o contrato. No exemplo acompanhado abaixo, dois contatos respondem entre dez; a taxa e a incerteza têm leitura distinta.

### Como encaminhar a revisão

Confirme forma de pasta, nome de módulo, export público, links e sintaxe. Em seguida, revise o comportamento com dados conhecidos, casos inválidos e limites. Para skills, acrescente testes de seleção por relevância, rejeição de tarefas próximas e seleção explícita. Estrutura aprovada não equivale a algoritmo aprovado.

---

## Como diferenciar os tipos

Um README ensina a usar uma coleção. Um snippet oferece uma API. Um script resolve uma tarefa com contrato próprio, que pode ser diagnóstico ou transformação. Um prompt descreve o pedido; uma skill orienta o método do agente; um notebook demonstra a execução. Não use apenas o tipo da entrada para classificar todos os objetos: formatadores recebem números e RFV transforma dados, por exemplo.

O tema campanha pode aparecer em vários tipos sem duplicação. O snippet calcula taxa por segmento; um script verifica integridade dos dados; o prompt delimita a análise; a skill organiza o método; o notebook evidencia a execução; o README orienta o usuário. Cada um responde a uma pergunta diferente.

---

## Contrato mínimo

Um contrato insuficiente seria “função que calcula taxa”. Isso não informa denominador, grão, unidade, nulos, incerteza nem retorno. O exemplar existente é mais específico e deve ser explicado como é, não substituído por uma assinatura hipotética.

### Exemplo acompanhado: o contrato real de `taxa_resposta_campanha`

A [implementação didática](../../../ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/taxa_resposta_campanha.py) recebe um DataFrame Spark com uma linha por contato e calcula uma linha por segmento. A API pública é reexportada pelo [arquivo `__init__.py`](../../../ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/__init__.py):

```python
taxa_resposta_campanha(
    dados,
    *,
    coluna_segmento,
    coluna_resposta="respondeu",
    z=1.96,
    minimo_para_decisao=100,
)
```

Esse bloco descreve a assinatura, não é uma chamada isolada com variáveis já preparadas. O exemplo executável completo está abaixo. O retorno é um **DataFrame Spark**, não `float`, e contém `segmento`, `contatados`, `respostas`, `taxa_pct`, `ic_inferior_pct`, `ic_superior_pct`, `largura_ic_pp` e `decidivel`.

**Preparar e executar em ambiente didático autorizado.** O exemplo usa o exemplar apenas para estudar o contrato, não o instala na biblioteca de produção. Confirme o caminho pessoal ou compartilhado do Hub:

```python
from pathlib import Path
import sys
from pyspark.sql import SparkSession

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if not (assistant_root / "hub_padroes").is_dir():
    raise FileNotFoundError("Confirme a instalacao do Hub.")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from hub_padroes.snippet.taxa_resposta_campanha import taxa_resposta_campanha

spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
contatos = spark.createDataFrame(
    [("A", 1 if i < 2 else 0) for i in range(10)],
    "segmento string, respondeu int",
)
por_segmento = taxa_resposta_campanha(
    contatos, coluna_segmento="segmento", coluna_resposta="respondeu",
    z=1.96, minimo_para_decisao=100,
)
linha = por_segmento.first().asDict()
assert linha["contatados"] == 10
assert linha["respostas"] == 2
assert linha["taxa_pct"] == 20.0
assert linha["decidivel"] is False
por_segmento.show(truncate=False)
```

**Saída esperada da fixture, não registro de run:** uma linha do segmento A, com 10 contatos, 2 respostas e taxa de 20,00%. A razão correspondente é 0,20, mas a coluna retornada está em escala percentual. Para `z=1,96`, o intervalo de Wilson arredondado é aproximadamente 5,67% a 50,98%, e sua largura calculada antes do arredondamento é 45,32 pontos percentuais.

**Interpretar.** Duas respostas em dez contatos permitem calcular a taxa observada, mas deixam grande incerteza. `decidivel=False` decorre da política local `10 < 100`, não de um teste universal de validade. O limite mínimo não elimina a necessidade de desenho amostral, dependência entre contatos e decisão de negócio. A largura do intervalo não deve ser recalculada pela subtração dos limites já arredondados se você precisa reproduzir exatamente a coluna da função.

**Entrada inválida.** O exemplar recusa resposta nula ou fora de 0/1. Não converte automaticamente falha de registro em não resposta:

```python
invalidos = spark.createDataFrame([("A", None)], "segmento string, respondeu int")
try:
    taxa_resposta_campanha(invalidos, coluna_segmento="segmento")
except ValueError as erro:
    print(erro)
else:
    raise AssertionError("A resposta nula deveria ser recusada pelo contrato.")
```

Também há validação de colunas, `z` e mínimo positivo. Não documente uma rejeição específica de denominador zero que essa API não implementa. Uma base vazia e uma população ausente exigem tratamento e teste próprios; não são equivalentes a passar uma coluna de denominador igual a zero.

**Adaptação planejada.** Para comparar A e B, acrescente contatos do segundo segmento e espere uma linha por grupo, mantendo a unidade percentual. Para alterar o mínimo de decisão, documente a nova política; não altere o número só para produzir `True`. Como exercício, mantenha 20% de resposta e aumente a amostra: observe a mudança na precisão, não apenas na taxa.

O módulo realiza validações e agregações Spark. Nenhuma chamada acima grava uma tabela persistente. A execução em escala e a inclusão num pipeline dependem de revisão adicional, pois este objeto permanece um exemplar de padrões.

### Quando a entrega é um prompt

A mesma demanda não exige copiar o algoritmo para o briefing. Um pedido de análise pode declarar: “compare a taxa por segmento, informe denominador, incerteza, regra para nulos e limitações; não recomende alocação automaticamente”. O prompt define a pergunta e o aceite; o helper fornece a implementação que vier a ser aprovada para uso.

---

## Limites

O exemplar de skill está fora da pasta de descoberta ativa. Copiá-lo para `.assistant/skills/` pode torná-lo disponível ao agente sem a revisão necessária. Uma integração indevida deve ser corrigida pelo fluxo autorizado, não por excluir arquivos arbitrariamente no workspace.

Exemplos de campanha não são biblioteca de produção. Um molde não prova correção estatística, disponibilidade no runtime ou autorização de dados. Não crie um novo tipo de objeto apenas para uma variação de conteúdo que cabe no contrato existente.

Se a importação didática falhar, confira path, disponibilidade de PySpark e o export público. Se o retorno não corresponder ao contrato acima, registre versão, entrada e diferença. Não mude silenciosamente a assinatura ou a lógica apenas para adequá-la ao texto.

---

## Onde continuar

Use os moldes e exemplares específicos na tabela inicial. Para revisão do novo objeto, consulte o [checklist de criação](../../../ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md). Para localização de implementações ativas, abra o [Catálogo de Helpers](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md); para uso do ecossistema, o [guia do `.assistant`](../sprint-02-assistant/README.md).

As fontes do contrato demonstrado são o módulo e seu export linkados acima. Capacidades e limites de execução do agente seguem a [documentação oficial](https://learn.microsoft.com/en-us/azure/databricks/genie-code/agent-mode), consultada em 11/09/2026.
