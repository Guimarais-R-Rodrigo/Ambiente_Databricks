# `hub_scripts` — diagnóstico antes de confiar num número

> **EXTENSÃO DO HUB (`hub_`) — não auto-descoberta nem executada pelo Genie Code.**
> Importe explicitamente, depois de acrescentar `.assistant` ao `sys.path`.

Sete utilitários de diagnóstico. Seis se apontam a uma **tabela** do workspace;
`doc_coverage` é a exceção e recebe o caminho de um **notebook**, porque o que ele
avalia é documentação, não dado.

## Para que serve

Use quando a pergunta for **"posso confiar nesta tabela?"** — antes de medir,
não depois. Script recebe **nome de tabela** porque existe para ser apontado a
algo que já está publicado; se o que você quer é uma peça de cálculo dentro de
um fluxo, o lugar é [`hub_snippets`](../hub_snippets/README.md), e a função
recebe `DataFrame`.

## Visão estrutural

Cada script é uma pasta com três arquivos, sempre os mesmos:

```text
hub_scripts/<nome>/
├── __init__.py              # declara a API pública, gerado por ferramenta
├── <nome>.py                # a implementação
└── exemplo_<nome>.py        # notebook que demonstra e ensina
```

## Como usar

```python
import sys

usuario = spark.sql("SELECT current_user()").first()[0]
sys.path.insert(0, f"/Workspace/Users/{usuario}/.assistant")

from hub_scripts.data_quality_check import data_quality_check

veredito = data_quality_check("catalogo.crm.contatos", ["id_cliente"], "dt_referencia")
assert veredito["status"] != "fail", veredito["alerts"]
```

## O que existe aqui

| Script | Em uma linha | Quando usar |
|---|---|---|
| [`data_quality_check`](data_quality_check/) | unicidade da chave, nulos e atualidade | antes de qualquer medição sobre tabela nova |
| [`quick_profile`](quick_profile/) | schema e estatísticas, com a origem de cada número | para conhecer uma tabela sem varrê-la inteira |
| [`drift_detector`](drift_detector/) | PSI entre dois períodos, bins da referência | quando desconfiar que a distribuição mudou |
| [`rfv_calculator`](rfv_calculator/) | recência, frequência e valor, com corte na data de decisão | ao construir features de CRM sem vazamento |
| [`schema_to_yaml`](schema_to_yaml/) | schema como dicionário e como texto escapado | ao documentar ou comparar estrutura |
| [`naming_checker`](naming_checker/) | violações de convenção, rotuladas por origem da regra | ao revisar nomenclatura de uma entrega |
| [`doc_coverage`](doc_coverage/) | quanto do código tem markdown ao lado | para achar notebook que precisa de revisão |

Cada pasta tem um notebook `exemplo_*` que **mostra o erro acontecendo** antes de
mostrar a correção. O mapa por demanda, cobrindo também `hub_snippets`, está no
[catálogo de helpers](../CATALOGO_HELPERS.md).

## Limites e armadilhas

- **`status: "fail"` não significa dado ruim.** Significa que algo precisa de
  decisão humana antes de a medição valer. Os limiares são política local, não
  exigência da plataforma, e vêm declarados na própria saída.
- **Nenhum script filtra ou corrige sozinho.** Helper que remove a linha
  problemática produz relatório limpo e conclusão errada.
- **A sessão Spark é resolvida internamente** com
  `SparkSession.getActiveSession() or ...getOrCreate()`. Não conte com o global
  `spark` de notebook dentro de módulo importado — ele não existe lá, e foi a
  causa da primeira leva de falhas no runtime real.
- **Leituras têm custo.** Cada script faz de uma a três varreduras agregadas,
  e `quick_profile` faz mais se `include_stats` estiver ligado. Barato em milhões
  de linhas não é barato em bilhões: confira o plano antes de apontar para tabela
  grande.
- **Nada aqui substitui** Lakeflow expectations, o event log, monitoramento
  Lakehouse ou políticas do Unity Catalog. São diagnósticos de quem analisa, não
  controles de pipeline.

## Perguntas frequentes

**Por que script recebe nome de tabela e snippet recebe DataFrame?**
Porque o papel é outro. Script roda sozinho, apontado a um objeto publicado, e
devolve veredito. Snippet entra no meio de uma transformação e devolve dado.

**Posso mudar os limiares?**
Sim — são política, não lei. Passe `thresholds` e o valor aplicado volta na
saída, para que quem lê o resultado saiba contra o que foi comparado.

**Qual rodar primeiro numa tabela desconhecida?**
`data_quality_check`, para saber se o grão é o que você supõe, e depois
`quick_profile` com fração declarada. Na ordem inversa você perfila uma base que
pode estar duplicada.

## Onde continuar

- Para criar um script novo: o molde está em
  [`hub_padroes/script/template.md`](../hub_padroes/script/template.md).
- Para o vocabulário do projeto: [glossário](../README.md#glossário).
- Para a biblioteca de cálculo: [`hub_snippets`](../hub_snippets/README.md).
