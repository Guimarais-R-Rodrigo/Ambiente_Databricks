![CRM — Missão Modelos Analíticos CRM](../hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Hub Scripts

> Utilitários e diagnósticos de integridade para inspecionar tabelas, schemas e notebooks antes de confiar na modelagem preditiva ou promover artefatos no Databricks.

> **CONTEÚDO CUSTOMIZADO PELO HUB.** `hub_scripts` não é executado automaticamente pela Genie Code. Cada diagnóstico precisa ser importado e chamado por um notebook, tarefa ou pessoa, que também decide como tratar o resultado.

> **Rascunho de sprint 4 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/hub_scripts/README.md`.

---

## 🧭 Neste Guia

Um **script** do Hub responde a uma pergunta sobre um recurso endereçado (nome de tabela, caminho de notebook). Um **snippet** transforma um objeto que você já carregou. **Serializar** schema em YAML não é o mesmo que **aprovar** a tabela.

| Para entender... | Vá para... |
|---|---|
| o papel de um Hub Script | [O que é um Script](#-o-que-é-um-script-neste-ecossistema) |
| os sete diagnósticos disponíveis | [Catálogo Detalhado](#-catálogo-detalhado) |
| como executar uma checagem | [Passo a Passo Operacional](#️-passo-a-passo-operacional-como-usar-um-script) |
| custo e efeitos de cada utilitário | [O que Acontece Durante a Execução](#️-o-que-acontece-durante-a-execução) |
| a diferença entre diagnóstico e regra operacional | [Diagnóstico não é Enforcement](#-diagnóstico-não-é-enforcement) |
| dúvidas e limitações | [Perguntas Frequentes](#-perguntas-frequentes-faq) |

**Primeira checagem:** leia o papel do script, execute o exemplo de `data_quality_check` e só então escolha outro utilitário no catálogo.

---

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

## 🏛️ Arquitetura e o Padrão "Pasta de Objeto"

Cada diagnóstico mora na própria pasta.

![Anatomia da pasta de um Hub Script](../hub_readmes_visual_assets/readmes/scripts/png/01_anatomia_pasta.png)

*Leitura da figura: a fachada (`__init__.py`) é o import estável; o módulo é o motor; o `exemplo_*.py` demonstra — não é o que você importa.*

Import público:

```python
from hub_scripts.data_quality_check import data_quality_check
```

Abrir o notebook de exemplo não registra a função na sessão. Alguns exemplos simulam falha de propósito.

---

## 📚 Catálogo Detalhado

![Catálogo dos Hub Scripts por pergunta de diagnóstico](../hub_readmes_visual_assets/readmes/scripts/png/02_catalogo_diagnosticos.png)

*Leitura da figura: saúde dos dados, estabilidade e governança técnica respondem a riscos distintos. Escolha pela pergunta, não pelo nome “bonito”.*

![Panorama dos tipos de retorno](../hub_readmes_visual_assets/readmes/scripts/png/03_panorama_retornos.png)

*Leitura da figura: uns devolvem dicionário com status, outros DataFrame ou texto. Interprete o tipo certo.*

### 🩺 1. Qualidade e Perfilamento de Dados (Data Health)

Pergunta: “posso confiar nesta tabela para o próximo passo, segundo as regras que eu configurei?”

#### `data_quality_check` — Inspeção Sanitária Pré-Modelagem

- **Problema:** nulos, PK duplicada, tabela velha.
- **Conceitos.** **Chave candidata:** colunas que deveriam identificar a linha. **Nulidade:** proporção de nulos. **Freshness:** atraso da data máxima em relação a hoje, em dias, se `date_column` for informada. **Limiar:** política *sua*, não da Databricks.
- **Entrada:** `table_name` (string da sessão Spark), `pk_columns` (lista não vazia), `date_column` opcional, `thresholds` opcional com `null_warn`, `null_fail`, `freshness_days`.
- **Interface:** `from hub_scripts.data_quality_check import data_quality_check`.
- **Quando não usar:** para apagar linhas, para “homologar a base inteira”, ou sem SparkSession.

Exemplo acompanhado (20 linhas, 1 nulo em `canal` = 5%):

```python
from hub_scripts.data_quality_check import data_quality_check

resultado = data_quality_check(
    table_name="vw_campanha_eventos_sintetica",
    pk_columns=["event_id"],
    date_column="dt_evento",
    thresholds={"null_warn": 5.0, "null_fail": 20.0, "freshness_days": 90.0},
)
```

**Saída.** Dicionário com `status` (`pass`/`warn`/`fail`), métricas e `alerts` (cada item com `severity`, `check`, `message`). Não há parâmetro `primary_keys` nem `critical_columns`.

**Interpretação.** 5% em `canal` encontra `null_warn=5`. Status `warn` pede leitura do alerta. `fail` exigiria ≥ 20% ou PK nula/duplicada. O script **não** levanta `ValueError` sozinho porque o status foi `fail`; isso é o notebook.

**Limite.** `pass` = as regras configuradas não acharam violação. Não é selo da tabela para qualquer uso.

A view precisa existir na sessão (veja o tutorial do README `.assistant`).

#### `quick_profile` — Raio-X de Schema e Distribuição

- **Problema:** primeira olhada em volume, nulos e cardinalidade.
- **Conceito.** Medidas da **tabela inteira** (contagem, nulos) versus medidas da **amostra** (cardinalidade extra). Nomes `*_sample` e `*_full_table` no retorno existem para não misturar os dois.
- **Quando usar:** exploração inicial. Tabela larga ainda custa scan.
- **Quando não usar:** como substituto de `data_quality_check` (não devolve o mesmo contrato de PK/freshness).

#### `rfv_calculator` — Recência, Frequência e Valor

- **Problema:** atributos brutos de comportamento por entidade até uma data de corte.
- **Conceito.** **Recência:** tempo desde o último evento ≤ corte. **Frequência:** contagem no período. **Valor:** soma configurada. Transação **depois** do corte não entra.
- **Saída:** DataFrame Spark, não um veredito `pass`.
- **Quando não usar:** para criar quintis ou personas automaticamente — isso é política posterior.

Com quatro compras, corte em 15/03: a compra de 20/03 fica de fora. Confira o exemplo em `exemplo_rfv_calculator.py`.

### 📉 2. Estabilidade e Monitoramento de Distribuição

Pergunta: “a distribuição desta variável mudou entre duas coortes da mesma tabela?”

#### `drift_detector` — Detecção de Desvios de Distribuição

- **Conceitos.** **Referência** e **comparação** são valores da coluna de coorte. **PSI** resume mudança de distribuição. Sem política, o número não classifica sozinho “crítico”.
- **Entrada:** tabela, coluna de coorte, valores de referência/comparação, colunas numéricas.
- **Quando não usar:** para afirmar causalidade ou “o modelo piorou”. Drift ≠ performance.
- **Duas coortes iguais** tendem a PSI próximo de zero; uma coorte deslocada eleva o índice. Leia o exemplo do objeto.

### 📐 3. Governança, Contratos e Boas Práticas de Código

#### `schema_to_yaml` — Contratos de Dados em YAML

Inspeciona schema (e estatísticas se pedidas). **Retorna string**; não grava arquivo. Sem PyYAML, o fallback é JSON válido em YAML 1.2. Persistência é sua.

#### `naming_checker` — Guardião de Nomenclatura

Compara nomes de colunas com a política configurada (`snake_case`, prefixos). **Não** lê o conteúdo das linhas. Convenções são do Hub/equipe, não exigência universal do Unity Catalog.

#### `doc_coverage` — Auditoria Estrutural de Documentação

Lê arquivo Jupyter ou fonte Databricks exportada. Mede proximidade Markdown–código. **Não** abre notebook por URL, **não** avalia qualidade semântica, **não** usa Spark.

---

## 🛠️ Passo a Passo Operacional: Como Usar um Script

![Fluxo de execução e resultados de um Hub Script](../hub_readmes_visual_assets/readmes/scripts/png/05_veredito_data_quality.png)

*Leitura da figura: PASS, WARN e FAIL classificam o diagnóstico. Quem age — seguir, revisar ou parar — é a política do notebook ou do Job.*

1. Torne `.assistant` importável (`sys.path`), no **notebook**.
2. Importe a função do pacote `hub_scripts`, não o `exemplo_*.py`.
3. Passe o nome real do recurso e os limiares **escolhidos**.
4. Leia `status` e `alerts` campo a campo.
5. Codifique a reação: `raise`, log ou seguimento.

```python
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from hub_scripts.data_quality_check import data_quality_check

resultado = data_quality_check(
    table_name="vw_campanha_eventos_sintetica",
    pk_columns=["event_id"],
    date_column="dt_evento",
    thresholds={"null_warn": 5.0, "null_fail": 20.0, "freshness_days": 90.0},
)

print(resultado["status"])
for alerta in resultado.get("alerts", []):
    print(alerta["severity"], alerta["check"], alerta["message"])

if resultado["status"] == "fail":
    raise ValueError("A política deste notebook interrompe em fail.")
```

| Estado | Significado | Decisão típica do consumidor |
|---|---|---|
| `pass` | nenhuma regra configurada violada | próximo gate |
| `warn` | atenção | revisar alertas |
| `fail` | regra de falha violada | interromper **se** essa política estiver no código |

```python
{
    "status": "warn",
    "metrics": {"row_count": 20},
    "alerts": [
        {"severity": "warn", "check": "null_rate", "message": "...canal..."}
    ],
}
```

O trecho acima é **forma** ilustrativa; a mensagem exata vem da execução.

**Se não funcionou.** Ver FAQ 1–4 do README `.assistant` sobre path e permissão. Aqui: `pk_columns` vazio levanta `ValueError`; limiares fora de `0 ≤ warn ≤ fail ≤ 100` também.

---

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

## 🧭 Diagnóstico não é Enforcement

![Separação entre diagnóstico, política e enforcement](../hub_readmes_visual_assets/readmes/scripts/png/04_diagnostico_vs_enforcement.png)

*Leitura da figura: o Hub Script observa; a regra consumidora decide; Lakeflow Jobs / expectations executam política de plataforma.*

- Expectativas de pipeline: documentação oficial de Lakeflow expectations.
- Histórico operacional: event log do pipeline.
- Falha de tarefa e notificação: Lakeflow Jobs.
- O script não envia e-mail nem para o job vizinho.

---

## ❓ Perguntas Frequentes (FAQ)

### 1. Se o script retornar `status="fail"`, meus dados serão apagados?

Não pelo script. Ele lê e devolve. Quem falha a tarefa é o `raise` que **você** escreveu.

### 2. Os scripts funcionam com Unity Catalog?

Os que recebem tabela usam a sessão Spark. Prefira `catalog.schema.table`. Formato curto depende do catálogo ativo. Nenhum script contorna ACL.

### 3. Preciso rodar pelo terminal?

Não. São módulos Python. Notebook ou tarefa, com path, dependências e Spark quando exigido.

### 4. Tabelas grandes ficam lentas?

Podem. Distinct, quantis e `groupBy` geram shuffle. Veja o plano Spark.

### 5. Posso usar em pipeline?

Sim, com política explícita. Recorrência e alerta são do orquestrador.

### 6. A Genie Code executa estes scripts automaticamente?

Não. Skill pode **sugerir** o caminho. Importar e chamar é ação sua.

---

## 🔗 Continue Explorando

- [Hub Snippets](../hub_snippets/README.md)
- [Agent Skills](../skills/README.md)
- [Hub Prompts](../hub_prompts/README.md)
- [Catálogo de Helpers](../CATALOGO_HELPERS.md)
- [Lakeflow expectations](https://learn.microsoft.com/en-us/azure/databricks/ldp/expectations)
- [Event log](https://learn.microsoft.com/en-us/azure/databricks/ldp/monitor-event-logs)
- [Notificações de Jobs](https://learn.microsoft.com/en-us/azure/databricks/jobs/notifications)
