![CRM — Missão Modelos Analíticos CRM](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

<a id="hub-scripts"></a>

# Hub Scripts

> Utilitários e diagnósticos de integridade para inspecionar tabelas, schemas e notebooks antes de confiar na modelagem preditiva ou promover artefatos no Databricks.

> **CONTEÚDO CUSTOMIZADO PELO HUB.** `hub_scripts` não é executado automaticamente pela Genie Code. Cada diagnóstico precisa ser importado e chamado por um notebook, tarefa ou pessoa, que também decide como tratar o resultado.

> **Rascunho de sprint 4 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/hub_scripts/README.md`.

---

<a id="neste-guia"></a>

## 🧭 Neste Guia

Um **script** do Hub responde a uma pergunta sobre um recurso endereçado (nome de tabela, caminho de notebook). Um **snippet** transforma um objeto que você já carregou. **Serializar** schema em YAML não é o mesmo que **aprovar** a tabela.

| Para entender... | Vá para... |
|---|---|
| o papel de um Hub Script | [O que é um Script](#o-que-é-um-script-neste-ecossistema) |
| os sete diagnósticos disponíveis | [Catálogo Detalhado](#catálogo-detalhado) |
| como executar uma checagem | [Passo a Passo Operacional](#passo-a-passo-operacional-como-usar-um-script) |
| custo e efeitos de cada utilitário | [O que Acontece Durante a Execução](#o-que-acontece-durante-a-execução) |
| a diferença entre diagnóstico e regra operacional | [Diagnóstico não é Enforcement](#diagnóstico-não-é-enforcement) |
| dúvidas e limitações | [Perguntas Frequentes](#perguntas-frequentes-faq) |

**Primeira checagem:** leia o papel do script, execute o exemplo de `data_quality_check` e só então escolha outro utilitário no catálogo.

---

<a id="o-que-é-um-script-neste-ecossistema"></a>

## 🔍 O que é um Script neste Ecossistema?

Em pipelines, o risco frequentemente está no dado: chave duplicada, nulo na PK, tabela parada no tempo. Treinar em cima disso gasta cluster e produz conclusão frágil.

**No Hub, um script é um diagnóstico importável.** Você aponta o recurso, ele devolve evidência, você decide.

Isso **não** é um `.sh` de terminal nem um job que roda sozinho ao abrir a pasta.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                            O PAPEL DE UM SCRIPT                             │
│                                                                             │
│   Diagnóstico delimitado: uma pergunta técnica configurada                  │
│   Saída estruturada: métricas, status ou violações conferíveis              │
│   Leitura por padrão: não persiste alteração no ativo inspecionado          │
│   Validação prévia: revela risco antes de etapa mais cara                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

A campanha fictícia entra assim: antes de modelar retenção, você pergunta se `event_id` é único e quantos nulos há em `canal`.

---

<a id="arquitetura-e-o-padrão-pasta-de-objeto"></a>

## 🏛️ Arquitetura e o Padrão "Pasta de Objeto"

Cada diagnóstico mora na própria pasta.

![Anatomia da pasta de um Hub Script](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/scripts/png/01_anatomia_pasta.png)

*Leitura da figura: a fachada (`__init__.py`) é o import estável; o módulo é o motor; o `exemplo_*.py` demonstra — não é o que você importa.*

Import público:

```python
from hub_scripts.data_quality_check import data_quality_check
```

Abrir o notebook de exemplo não registra a função na sessão. Alguns exemplos simulam falha de propósito.

---

<a id="catálogo-detalhado"></a>

## 📚 Catálogo Detalhado

Escolha o utilitário pela pergunta e pelo retorno. Perfilamento descreve; qualidade compara com regras; RFV transforma eventos em atributos; schema serializa um contrato; cobertura examina a estrutura de um arquivo. Nem todo script retorna `status`.

![Catálogo dos diagnósticos por pergunta](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/scripts/png/02_catalogo_diagnosticos.png)

A figura agrupa as perguntas, não promete uma ordem obrigatória de execução. Para a campanha, primeiro conhecemos o schema; depois conferimos a chave. Calcular RFV é uma etapa diferente, que exige definir entidade, valor e corte temporal.

![Tipos de retorno dos scripts](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/scripts/png/03_panorama_retornos.png)

O panorama distingue dicionário, DataFrame e texto. `checks` pertence ao dicionário de qualidade; não procure esse campo na string produzida por `schema_to_yaml` ou no DataFrame de RFV.

<a id="preparação-comum-a-campanha-sintética"></a>

### Preparação comum: a campanha sintética

Execute esta célula **uma vez no mesmo notebook Python** das demonstrações Spark. Ela cria somente uma view temporária da sessão, sem tabela persistente, arquivos no workspace ou dados da organização. A criação/substituição da view é um efeito de sessão explícito. Troque o caminho da biblioteca pelo diretório real do seu usuário; ele é a pasta que contém `hub_scripts`.

```python
from pathlib import Path
import sys
from datetime import date, timedelta
from pyspark.sql import SparkSession, functions as F

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if not (assistant_root / "hub_scripts").is_dir():
    raise FileNotFoundError("Localize a pasta .assistant publicada antes do import.")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
linhas = [
    (f"e{i:02d}", f"c{i % 5:02d}", date(2026, 6, 1) + timedelta(days=i),
     None if i == 0 else "email", i % 2, float(i))
    for i in range(20)
]
campanha = spark.createDataFrame(
    linhas,
    "event_id string, id_cliente string, dt_evento date, canal string, "
    "respondeu int, valor_gasto double",
)
campanha.createOrReplaceTempView("vw_campanha_eventos_sintetica")
assert campanha.count() == 20
```

O grão é um evento por linha; `event_id` é a chave candidata, `id_cliente` identifica a entidade e `dt_evento` é uma data. `respondeu` é binário e `valor_gasto` é um valor sintético em reais. `canal` possui exatamente um nulo. Os números abaixo são **oráculos calculáveis da fixture**, não capturas de uma execução em um workspace.

Uma view local não é um objeto persistente do Unity Catalog. Para conversar sobre ela, selecione a célula de preparação/schema com `@` ou Add Context, conforme a interface. Não diga “tabela anexada” sem efetivamente selecionar o recurso. Outra sessão pode não enxergar a view.

<a id="1-qualidade-e-perfilamento-de-dados-data-health"></a>

### 🩺 1. Qualidade e Perfilamento de Dados (Data Health)

<a id="data_quality_check-inspeção-sanitária-pré-modelagem"></a>

#### `data_quality_check` — Inspeção Sanitária Pré-Modelagem

**Problema e escolha.** Use para testar unicidade da chave, nulidade por coluna e, opcionalmente, atualidade. Uma chave candidata é uma hipótese sobre a identificação da linha, não uma garantia da plataforma. Para descobrir quais colunas existem antes de escolher a chave, comece por `quick_profile`.

**Contrato.** A assinatura pública é `data_quality_check(table_name, pk_columns, date_column=None, thresholds=None)`. O primeiro argumento é um nome que `spark.table` resolve na sessão; a lista de chaves não pode estar vazia. `null_warn` e `null_fail` são percentuais entre 0 e 100, em ordem crescente. `freshness_days` é um número não negativo de dias. São decisões locais de monitoramento.

```python
from hub_scripts.data_quality_check import data_quality_check

resultado = data_quality_check(
    table_name="vw_campanha_eventos_sintetica",
    pk_columns=["event_id"],
    date_column=None,
    thresholds={"null_warn": 5.0, "null_fail": 20.0},
)
assert resultado["status"] == "warn"
assert resultado["score"] == 95
assert resultado["checks"]["row_count"] == 20
assert resultado["checks"]["nulls"]["canal"]["count"] == 1
assert resultado["checks"]["nulls"]["canal"]["pct"] == 5.0
print(resultado["checks"]["pk_uniqueness"])
for alerta in resultado["alerts"]:
    print(alerta["severity"], alerta["check"], alerta.get("column"), alerta["message"])
```

**Leitura do retorno.** `checks.row_count` é o total; `checks.pk_uniqueness` contém colunas, linhas duplicadas, linhas com componente nulo e status. `checks.nulls` contém uma entrada por coluna com contagem, percentual e status. O alerta usa `column` para identificar `canal` e `message` para a descrição. Não existe chave superior `metrics`.

O cálculo é `1 / 20 × 100 = 5%`. Como o comparador é inclusivo (`>=`), atingir `null_warn=5` produz aviso. Sem outra falha, o status global é `warn`. O score subtrai 5 por aviso e 25 por falha, limitado inferiormente a zero: `100 − 5 = 95`. Ele **não** é uma probabilidade, uma medida estatística calibrada nem um selo de conformidade do Databricks. `thresholds` mostra os limites efetivamente usados; `alerts` informa o que os violou.

**Custo e efeitos.** Há agregação sobre todas as colunas e contagem distinta da chave. O helper lê e coleta agregados; não remove linhas e não interrompe automaticamente o notebook por retornar `fail`. Mesmo quando o resultado é `pass`, nenhuma regra não configurada foi comprovada.

**Como adaptar.** Substitua o recurso por uma tabela autorizada `catalog.schema.table`; só substitua a chave após definir o grão. Uma política válida para `canal` pode não servir para uma variável indispensável ao modelo. Se uma coluna não existe, corrija o contrato de entrada em vez de retirar a verificação sem explicação.

**Freshness, separadamente.** Idade significa a diferença entre a data corrente do processo Python e a data máxima da coluna. Uma data antiga não implica tabela errada quando a população é uma coorte histórica. Aqui criamos deliberadamente uma data atual para isolar o comportamento; registre `hoje` se guardar o resultado.

```python
hoje = date.today()
base_atual = campanha.withColumn("dt_evento", F.lit(hoje))
base_atual.createOrReplaceTempView("vw_campanha_freshness_atual")
recente = data_quality_check(
    "vw_campanha_freshness_atual", ["event_id"], date_column="dt_evento",
    thresholds={"null_warn": 5.0, "null_fail": 20.0, "freshness_days": 2.0},
)
print(hoje, recente["checks"]["freshness"])
assert recente["checks"]["freshness"]["status"] == "pass"

base_atual.withColumn("dt_evento", F.lit(hoje - timedelta(days=10))).createOrReplaceTempView(
    "vw_campanha_freshness_antiga"
)
antiga = data_quality_check(
    "vw_campanha_freshness_antiga", ["event_id"], date_column="dt_evento",
    thresholds={"freshness_days": 2.0},
)
assert antiga["checks"]["freshness"]["status"] == "fail"
assert antiga["status"] == "fail"
```

Esse exemplo pressupõe execução na mesma data civil da criação; atravessar a meia-noite exige conferir `days_old`. A API atual não recebe uma data de avaliação injetável. Em testes unitários, controle o relógio com mock; não invente um argumento na chamada. O caso com `date_column=None` permanece independente do calendário.

[Implementação e contrato](../../../ambiente_fonte/.assistant/hub_scripts/data_quality_check/data_quality_check.py) · [Notebook específico](../../../ambiente_fonte/.assistant/hub_scripts/data_quality_check/exemplo_data_quality_check.py).

<a id="quick_profile-raio-x-de-schema-e-distribuição"></a>

#### `quick_profile` — Raio-X de Schema e Distribuição

**Problema.** Você ainda não conhece tipos, volume, nulos nem cardinalidade. Perfilamento descreve esses aspectos sem prometer aptidão para um uso de negócio. Não substitui o contrato de PK/freshness do script anterior.

**Interface e entrada.** `quick_profile(table_name, sample_fraction=0.1, max_categories=20, *, seed=42)`. A fração está em `(0, 1]`; escolha 1 para conferir a fixture inteira antes de aprender a amostrar.

```python
from hub_scripts.quick_profile import quick_profile

perfil = quick_profile("vw_campanha_eventos_sintetica", sample_fraction=1.0, seed=42)
assert perfil["total_rows"] == 20
assert perfil["sample_rows"] == 20
nulos_canal = next(x for x in perfil["null_summary_full_table"] if x["column"] == "canal")
assert nulos_canal["null_count"] == 1
assert nulos_canal["null_pct"] == 5.0
print(perfil["dtypes"])
print(perfil["cardinality_sample"])
print(perfil["numeric_summary_sample"])
```

**Interpretar.** `total_rows`, `total_columns` e `null_summary_full_table` descrevem a tabela inteira. `sample_rows` informa o tamanho efetivamente obtido; `cardinality_sample`, `top_values_sample`, `numeric_summary_sample` e `date_range_sample` descrevem a amostra. A cardinalidade é aproximada e o perfil limita quantas colunas entram em alguns resumos. Nem todo campo do schema terá todos os diagnósticos.

**Variação resolvida.** Ao trocar para `sample_fraction=0.5`, o total e a contagem de nulos da tabela continuam 20 e 1. O tamanho e as estatísticas da amostra não precisam ser exatamente metade. Um valor raro ausente nela não prova ausência na população. A semente favorece repetição no mesmo plano, não identidade universal entre runtimes e particionamentos.

**Custo.** O perfil conta e mede nulos na tabela completa, mesmo com fração pequena. `max_categories` limita o que é devolvido, não substitui uma política de leitura. [Código](../../../ambiente_fonte/.assistant/hub_scripts/quick_profile/quick_profile.py) · [Exemplo](../../../ambiente_fonte/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py).

<a id="rfv_calculator-recência-frequência-e-valor"></a>

#### `rfv_calculator` — Recência, Frequência e Valor

**Conceito.** Recência é o tempo desde o último evento até o corte; frequência é quantidade de eventos; valor é soma do montante. Definir a unidade “evento” importa: dois itens da mesma compra não devem virar duas compras sem uma regra explícita.

**Interface.** `rfv_calculator(table_name, col_cliente, col_data, col_valor, dt_referencia, periodos=(30, 60, 90))`. Recebe nomes de colunas e uma data de referência textual. Retorna DataFrame Spark; não cria quintis, personas ou um veredito `pass`.

```python
from hub_scripts.rfv_calculator import rfv_calculator

compras = spark.createDataFrame([
    ("e1", "c1", date(2026, 3, 1), 10.0),
    ("e2", "c1", date(2026, 3, 15), 20.0),
    ("e3", "c1", date(2026, 3, 20), 999.0),
    ("e4", "c2", date(2026, 2, 1), 5.0),
], "event_id string, id_cliente string, dt_evento date, valor_gasto double")
compras.createOrReplaceTempView("vw_campanha_compras_rfv")
rfv = rfv_calculator(
    "vw_campanha_compras_rfv", "id_cliente", "dt_evento", "valor_gasto",
    dt_referencia="2026-03-15", periodos=(30,),
)
# Coleta delimitada: a fixture tem apenas duas entidades.
por_cliente = {r["id_cliente"]: r.asDict() for r in rfv.limit(2).collect()}
assert por_cliente["c1"]["frequencia_total"] == 2
assert por_cliente["c1"]["valor_total"] == 30.0
assert por_cliente["c1"]["recencia"] == 0
assert por_cliente["c2"]["recencia"] == 42
assert por_cliente["c2"]["frequencia_30d"] == 0
print(por_cliente)
```

**Por que esses números?** O evento de 20/03 não estava disponível até 15/03 e fica de fora. Para c1, restam dois eventos somando 30 e o último ocorre no próprio corte. Para c2, há um evento histórico, mas nenhum na janela inclusiva de 30 dias. A saída separa totais históricos das colunas `frequencia_30d` e `valor_30d`.

**Adaptar e revisar.** Escolha períodos coerentes com a decisão, política para estornos, eventos duplicados e moeda. O helper não conhece essas regras. Entidades com somente eventos posteriores ao corte não ganham automaticamente uma linha de zeros. Mais períodos implicam mais agregações/joins; evite converter a população inteira para pandas. [Código](../../../ambiente_fonte/.assistant/hub_scripts/rfv_calculator/rfv_calculator.py) · [Exemplo](../../../ambiente_fonte/.assistant/hub_scripts/rfv_calculator/exemplo_rfv_calculator.py).

<a id="2-estabilidade-e-monitoramento-de-distribuição"></a>

### 📉 2. Estabilidade e Monitoramento de Distribuição

<a id="drift_detector-detecção-de-desvios-de-distribuição"></a>

#### `drift_detector` — Detecção de Desvios de Distribuição

**Problema e conceito.** Comparar a distribuição de uma variável entre duas coortes. PSI soma contribuições das diferenças de proporções nas mesmas faixas; distribuição diferente não prova perda de desempenho do modelo, causalidade ou necessidade de retreino.

**Interface.** `drift_detector(table_name, date_col, date_ref, date_comp, cols=None, method="psi", *, num_bins=10, relative_error=0.001, epsilon=1e-6, warning_threshold=None, critical_threshold=None)`. Apesar do nome `date_col`, a coluna separa coortes por igualdade. Ambas precisam ter linhas; selecione variáveis numéricas, não a própria coluna de coorte.

```python
from hub_scripts.drift_detector import drift_detector

coortes = spark.createDataFrame(
    [("ref", float(i)) for i in range(20)]
    + [("igual", float(i)) for i in range(20)]
    + [("mudou", float(i + 100)) for i in range(20)],
    "coorte string, valor_gasto double",
)
coortes.createOrReplaceTempView("vw_campanha_coortes")
igual = drift_detector(
    "vw_campanha_coortes", "coorte", "ref", "igual", cols=["valor_gasto"],
    num_bins=4, relative_error=0.0,
)
mudou = drift_detector(
    "vw_campanha_coortes", "coorte", "ref", "mudou", cols=["valor_gasto"],
    num_bins=4, relative_error=0.0,
)
assert abs(igual["valor_gasto"]["psi"]) < 1e-12
assert mudou["valor_gasto"]["psi"] > 0
print(mudou["valor_gasto"]["classification"])
print(mudou["valor_gasto"]["buckets"])
```

**Saída e leitura.** O dicionário tem uma entrada por variável, com `psi`, `classification`, `boundaries`, tamanhos das coortes e `buckets`. Em cada bucket, compare contagens, proporções e contribuição ao PSI. Sem ambos os limiares, não presuma classificação de severidade. `epsilon` evita logaritmo de zero; não é um limite de alerta.

**Custo e adaptação.** Quantis, contagens e filtros são executados para as colunas escolhidas; mais variáveis aumentam custo. `relative_error=0` favorece conferência da fixture, não é recomendação universal para tabelas grandes. Calibre limiares usando população, sazonalidade e desempenho; mantenha as mesmas definições nos períodos. [Código](../../../ambiente_fonte/.assistant/hub_scripts/drift_detector/drift_detector.py) · [Exemplo](../../../ambiente_fonte/.assistant/hub_scripts/drift_detector/exemplo_drift_detector.py).

<a id="3-governança-contratos-e-boas-práticas-de-código"></a>

### 📐 3. Governança, Contratos e Boas Práticas de Código

<a id="schema_to_yaml-contratos-de-dados-em-yaml"></a>

#### `schema_to_yaml` — Contratos de Dados em YAML

**Conceito e limite.** Schema descreve nomes, tipos e nulabilidade. Serializá-lo produz uma representação textual; isso não obriga dados futuros a obedecê-lo. Enforcement depende de configuração externa.

**Interface.** `schema_to_dict(table_name, *, include_comments=True, include_stats=False)` e `schema_to_yaml(table_name, include_comments=True, include_stats=False)` compartilham o recurso; devolvem respectivamente dicionário e string.

```python
from hub_scripts.schema_to_yaml import schema_to_dict, schema_to_yaml

contrato = schema_to_dict("vw_campanha_eventos_sintetica", include_stats=False)
texto = schema_to_yaml("vw_campanha_eventos_sintetica", include_stats=False)
assert isinstance(texto, str)
assert any(c["name"] == "event_id" and c["type"] == "string" for c in contrato["columns"])
print(texto)
```

**Interpretação.** Cada entrada de `columns` informa `name`, `type`, `nullable` e comentário quando disponível. `nullable=True` é característica do schema, não contagem observada de nulos. Sem PyYAML, o fallback é JSON, compatível com YAML 1.2; não se deve testar o retorno apenas pela aparência da indentação. Estatísticas opcionais leem dados, ao contrário da consulta de schema.

O helper não grava arquivo. Salvar a string, versionar o contrato e aplicá-lo em um pipeline são decisões separadas. Use o serializador, não concatenação manual de nomes/comentários. [Código](../../../ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/schema_to_yaml.py) · [Exemplo](../../../ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/exemplo_schema_to_yaml.py).

<a id="naming_checker-guardião-de-nomenclatura"></a>

#### `naming_checker` — Guardião de Nomenclatura

**Problema e escolha.** Conferir uma política de nomes, antes de criar outro objeto inconsistente. A convenção snake_case é local; um nome fora dela não é necessariamente inválido no Unity Catalog.

**Interface.** `naming_checker(table_name, *, enforce_prefix=False, allowed_table_prefixes=(), max_col_length=255)` retorna lista de violações, não DataFrame nem score. Para habilitar prefixos, forneça os prefixos aceitos pela equipe.

```python
from hub_scripts.naming_checker import naming_checker

campanha.select(F.col("id_cliente").alias("ClienteID")).createOrReplaceTempView(
    "vw_campanha_nomes"
)
violacoes = naming_checker("vw_campanha_nomes")
assert any(v["object"] == "ClienteID" for v in violacoes)
for violacao in violacoes:
    print(violacao["object"], violacao["severity"], violacao["message"], violacao["policy"])
```

`ClienteID` permite observar a violação de coluna. O nome curto da view também pode gerar aviso de contexto não totalmente qualificado; não o confunda com a coluna. O script lê schema, não conteúdo das linhas, e não renomeia nada. Para tabelas reais, forneça nome de três níveis e revise o impacto de um eventual rename antes de executá-lo. [Código](../../../ambiente_fonte/.assistant/hub_scripts/naming_checker/naming_checker.py) · [Exemplo](../../../ambiente_fonte/.assistant/hub_scripts/naming_checker/exemplo_naming_checker.py).

<a id="doc_coverage-auditoria-estrutural-de-documentação"></a>

#### `doc_coverage` — Auditoria Estrutural de Documentação

**Conceito.** Mede quantas células de código têm Markdown imediatamente antes ou depois. É uma heurística de proximidade, não uma avaliação semântica da explicação. Uma célula dizendo “código abaixo” pode aumentar cobertura sem ensinar.

**Interface e local.** `doc_coverage(notebook_path)` recebe caminho de arquivo exportado `.ipynb`, `.py`, `.sql`, `.scala` ou `.r`. Não recebe URL do notebook e não usa Spark. A demonstração abaixo cria e remove um arquivo **temporário local**, efeito explicitamente limitado ao diretório temporário; não altera o notebook aberto nem o workspace.

```python
import json
import tempfile
from pathlib import Path
from hub_scripts.doc_coverage import doc_coverage

with tempfile.TemporaryDirectory(prefix="hub-doc-coverage-") as pasta:
    arquivo = Path(pasta) / "campanha.ipynb"
    arquivo.write_text(json.dumps({"cells": [
        {"cell_type": "markdown", "source": ["Contamos eventos antes de medir resposta."]},
        {"cell_type": "code", "source": ["n = 20"]},
        {"cell_type": "code", "source": ["taxa = 10 / n"]},
    ]}), encoding="utf-8")
    cobertura = doc_coverage(str(arquivo))
    assert cobertura["total_code_cells"] == 2
    assert cobertura["total_markdown_cells"] == 1
    assert cobertura["coverage_pct"] == 50.0
    assert cobertura["uncovered_cell_indexes"] == [2]
    print(cobertura)
```

A primeira célula de código é vizinha de Markdown; a segunda não. Por isso `1/2 = 50%`. Os índices são baseados em zero. Para melhorar, escreva uma explicação pertinente adjacente à célula 2, não apenas uma célula vazia. Notebook sem código recebe 100% por convenção matemática do helper; isso não homologa a qualidade do documento. [Código](../../../ambiente_fonte/.assistant/hub_scripts/doc_coverage/doc_coverage.py) · [Exemplo](../../../ambiente_fonte/.assistant/hub_scripts/doc_coverage/exemplo_doc_coverage.py).

<a id="passo-a-passo-operacional-como-usar-um-script"></a>

## 🛠️ Passo a Passo Operacional: Como Usar um Script

<a id="exemplo-prático-de-código"></a>

### Exemplo Prático de Código

Depois da preparação comum, compare três cenários sem dependência do calendário. A fixture original tem 5% de nulos. Preencher esse nulo é uma transformação **apenas didática** para construir o cenário `pass`, não uma recomendação para imputar dados reais.

```python
campanha.na.fill({"canal": "email"}).createOrReplaceTempView("vw_campanha_sem_nulos")
campanha.unionByName(campanha.filter(F.col("event_id") == "e00")).createOrReplaceTempView(
    "vw_campanha_duplicada"
)
casos = {
    "pass": "vw_campanha_sem_nulos",
    "warn": "vw_campanha_eventos_sintetica",
    "fail": "vw_campanha_duplicada",
}
for esperado, view in casos.items():
    diagnostico = data_quality_check(view, ["event_id"], date_column=None)
    assert diagnostico["status"] == esperado
    print(view, diagnostico["status"], diagnostico["checks"]["pk_uniqueness"])
```

<a id="como-interpretar-o-retorno"></a>

### Como interpretar o retorno

Para interromper um fluxo, a política consumidora precisa fazê-lo explicitamente. Imprimir `fail` não falha uma tarefa. Este bloco é um padrão de consumo para uma variável `resultado` já produzida acima:

```python
for alerta in resultado["alerts"]:
    print(alerta["severity"], alerta.get("column"), alerta["message"])
if resultado["status"] == "fail":
    raise ValueError("A política deste notebook interrompe neste diagnóstico de falha.")
```

Se o objetivo era apenas investigar, registre a evidência e decida com o responsável pelo dado. Para política recorrente, defina orquestração, critérios de falha e notificações fora do helper.

<a id="leitura-visual-do-veredito"></a>

### Leitura visual do veredito

![Veredito de qualidade e responsabilidade do consumidor](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/scripts/png/05_veredito_data_quality.png)

PASS significa ausência de violação nas verificações feitas; WARN pede investigação; FAIL indica regra de falha violada. Nenhum dos três muda os dados. O caso de duplicata conecta a imagem à chamada: o diagnóstico identifica a violação e o consumidor escolhe entre registrar e interromper.

**Recuperação.** View não encontrada: reexecute a preparação na mesma sessão. Coluna ausente: confronte schema e parâmetros. `ModuleNotFoundError: hub_scripts`: confira o diretório `.assistant`, antes de instalar pacotes. Permissão negada: solicite acesso, sem contorno. Limiares inconsistentes: declare `0 ≤ null_warn ≤ null_fail ≤ 100` e freshness não negativa.

<a id="o-que-acontece-durante-a-execução"></a>

## ⚙️ O que Acontece Durante a Execução?

| Script | Operação principal | Cuidado |
|---|---|---|
| `data_quality_check` | agregado + distinct da chave | scan / shuffle |
| `quick_profile` | volume/nulos completos + amostra | tabela larga |
| `drift_detector` | filtros, quantis, bins | cresce com variáveis |
| `rfv_calculator` | filtros, agregações, joins | períodos × entidades |
| `schema_to_yaml` | schema; agregados se pedidos | persistência externa |
| `naming_checker` | schema | não lê linhas |
| `doc_coverage` | parse de arquivo | sem Spark |

“Distribuído” não significa barato.

---

<a id="diagnóstico-não-é-enforcement"></a>

## 🧭 Diagnóstico não é Enforcement

![Separação entre diagnóstico, política e enforcement](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/scripts/png/04_diagnostico_vs_enforcement.png)

*Leitura da figura: o Hub Script observa; a regra consumidora decide; Lakeflow Jobs / expectations executam política de plataforma.*

- Expectativas de pipeline: documentação oficial de Lakeflow expectations.
- Histórico operacional: event log do pipeline.
- Falha de tarefa e notificação: Lakeflow Jobs.
- O script não envia e-mail nem interrompe outra tarefa. Expectations podem manter, descartar registros ou falhar a atualização conforme a configuração; a simples existência da regra não implica a política mais restritiva.

---

<a id="perguntas-frequentes-faq"></a>

## ❓ Perguntas Frequentes (FAQ)

<a id="1-se-o-script-retornar-statusfail-meus-dados-serão-apagados-ou-modificados"></a>

### 1. Se o script retornar `status="fail"`, meus dados serão apagados ou modificados?

Não pelo script. Ele lê e devolve. Quem falha a tarefa é o `raise` que **você** escreveu.

<a id="2-os-scripts-funcionam-com-tabelas-do-unity-catalog"></a>

### 2. Os scripts funcionam com tabelas do Unity Catalog?

Os que recebem tabela usam a sessão Spark. Prefira `catalog.schema.table`. Formato curto depende do catálogo ativo. Nenhum script contorna ACL.

<a id="3-preciso-rodar-esses-scripts-pelo-terminal-ou-dentro-de-um-notebook"></a>

### 3. Preciso rodar esses scripts pelo terminal ou dentro de um notebook?

Não. São módulos Python. Notebook ou tarefa, com path, dependências e Spark quando exigido.

<a id="4-os-scripts-causam-lentidão-em-tabelas-volumosas"></a>

### 4. Os scripts causam lentidão em tabelas volumosas?

Podem. Distinct, quantis e `groupBy` geram shuffle. Veja o plano Spark.

<a id="5-posso-usar-os-scripts-em-pipelines-automatizados"></a>

### 5. Posso usar os scripts em pipelines automatizados?

Sim, com política explícita. Recorrência e alerta são do orquestrador.

<a id="6-a-genie-code-executa-estes-scripts-automaticamente"></a>

### 6. A Genie Code executa estes scripts automaticamente?

Não. Skill pode **sugerir** o caminho. Importar e chamar são ações explícitas do código consumidor, que pode ser operado por você ou pelo agente autorizado.

---

<a id="continue-explorando"></a>

## 🔗 Continue Explorando

- [Hub Snippets](../sprint-03-snippets/README.md)
- [Agent Skills](../sprint-05-skills/README.md)
- [Hub Prompts](../sprint-06-prompts/README.md)
- [Catálogo de Helpers](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md)
- [Lakeflow expectations](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations)
- [Event log](https://learn.microsoft.com/en-us/azure/databricks/ldp/monitor-event-logs)
- [Notificações de Jobs](https://learn.microsoft.com/en-us/azure/databricks/jobs/notifications)
