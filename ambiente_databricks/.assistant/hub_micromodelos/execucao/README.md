# Execução de Micromodelos

## Preparação por rota

| Rota | Precisa fornecer | Dependência/efeito |
|---|---|---|
| Validar YAML | arquivo, schema e contexto do caso | `jsonschema`, `regex`, `PyYAML`; leitura local |
| Descobrir metadados | sessão Spark, catálogo e escopo autorizados | SELECT allowlisted em `information_schema`; sem registros de negócio |
| Exemplo sintético | arquivos originais do caso | cálculo local/stdout; sem MLflow ou tabela |
| Tracking | política, backend, identidade e autorização específicos | MLflow somente pela API compartilhada; pode persistir recursos |

Na rota Databricks, `snapshot_id` identifica a observação local; não é snapshot transacional entre views. `table_tags=NOT_IMPLEMENTED` e `constraint_comment=NOT_COLLECTED`. `DENIED`, `UNAVAILABLE` ou coleta parcial não provam inexistência. Confira o [adapter](databricks.py) e os limites de [MetadataCollector](metadados.py) antes de interpretar ausência.

Para carregar/validar e calcular fingerprint, use a [receita do contrato](../contratos/README.md#revisar-uma-alteração). O [exemplo de recência](../exemplos/recencia_contato/README.md) é a receita local completa; não existe executor universal de YAML arbitrário.

Biblioteca de contrato, descoberta por metadados e ensaios sintéticos para um micromodelo de domínio.

<!-- readme-objeto: 1.0.0 -->

### Ler um envelope sem consultar Databricks

A receita abaixo usa somente uma fixture em memória, a partir da raiz `.assistant`. Ela observa um schema fictício e não busca tabelas ou registros:

```python
from hub_micromodelos.execucao.metadados import Binding, FixtureProvider, MetadataCollector
fixture = {"fixture_version": "1.0", "synthetic": True,
    "catalog": "catalogo_sintetico", "snapshot_id": "readme_obs_01",
    "streams": [{"operation": "schemas", "scope": [], "status": "OK",
                 "items": [{"name": "demo", "description": None}]}]}
collector = MetadataCollector(FixtureProvider(fixture), Binding("catalogo_sintetico"))
discovery = collector.discover()
envelope = collector.envelope(discovery, {})
assert envelope["mode"] == "METADATA_ONLY"
assert envelope["observation_status"] == "OBSERVED"
assert envelope["catalog_complete"] is False
assert envelope["data_access_authorized"] is False
print(envelope["coverage"], envelope["snapshot_id"], envelope["calls"])
```

`discovery.schemas` contém `status`, `reason`, `items` e `catalog_complete`; `objects` contém apenas schemas solicitados e observados. `details` só aceita candidatas previamente observadas. O envelope reúne `observation_status`, `coverage=ESCOPO_OBSERVADO`, `snapshot_id`, `calls` e limites de autoridade. Mesmo `OBSERVED` não significa catálogo completo. Uma página negada/indisponível produz `DENIED`/`UNAVAILABLE` ou observação parcial; não preencha objetos ausentes por hipótese. `MetadataError`, por exemplo `BINDING_MISMATCH` ou `CANDIDATE_NOT_OBSERVED`, interrompe o fluxo: confira binding/escopo antes de tentar novamente.

Para metadata real, as assinaturas são `DatabricksMetadataProvider(spark, binding)` e `MetadataCollector(provider, binding, limits=None)`, seguidas de `discover(schemas=None)`, `details(candidates)` e `envelope(discovery, details)`. A sessão e o catálogo vêm do caller autorizado; não existe fallback a registros de negócio.

Tracking não tem executor genérico nesta pasta. A [API governada de MLflow](../../hub_snippets/ml/mlflow_run/README.md) exige run/política/efeitos próprios. O exemplo local acima não chama essa API, não gera Receipt de tracking e não aprova um modelo.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Funções Python reutilizáveis do módulo `hub_micromodelos.execucao`. |
| Para que serve? | Validar especificação, calcular assinatura, descobrir metadados, preparar estudo e exemplos. |
| Quando usar? | Depois de definir escopo e permissões; para aprender, use a fixture sintética. |
| Quando evitar? | Quando a origem e a autoridade dos dados ou da decisão ainda não foram definidas. |
| Exige? | Python, `jsonschema`, `regex` e `PyYAML`; Databricks e MLflow só em rotas específicas. |
| Entrega? | Objetos de contrato, descoberta, artefatos e resultados sintéticos explícitos. |

## 1. O que é?

É o código do framework dentro do Hub. A [especificação](especificacao.py) valida o YAML; [assinatura](assinatura.py) identifica a parte material do contrato; os demais módulos implementam as etapas delimitadas abaixo.

## 2. Que problema este recurso resolve?

Permite verificar se um candidato descreve o mesmo micromodelo ao longo do estudo e se suas operações seguem a semântica declarada, sem perder a distinção entre proposta, medição, aceite e publicação.

## 3. Quando faz sentido usar?

No rascunho, valide o contrato e calcule sua assinatura. Na descoberta, use o coletor de metadados. No laboratório, rode a fixture sintética antes de avaliar adaptação a fontes autorizadas.

## 4. Quando não usar?

Não use o ensaio sintético como predição corporativa. Por exemplo, o score didático de recência classifica sete pessoas fictícias; ele não estima desempenho em clientes reais.

## 5. Como funciona, intuitivamente?

O YAML passa pelo schema e pelos invariantes de domínio. A assinatura fixa os campos materiais. O fluxo compõe uma proposta com fontes e regras. O laboratório aplica regras fechadas a fixtures locais e produz contagens reconciliadas.

## 6. Exemplo de situação

Um analista quer entender por que `pessoa_c` não é `FALSE` quando só existe um contato antigo. O [caso de recência](../exemplos/recencia_contato/README.md) mostra a especificação, os eventos sintéticos e o motivo `SOMENTE_CONTATO_ANTIGO`.

## 7. O que você precisa antes de usar?

Para o exemplo local, bastam Python e as dependências da visão rápida. Para Databricks, forneça uma sessão e um catálogo explicitamente autorizados ao [adaptador](databricks.py). Defina entidade, chave lógica, instante e janela antes de analisar registros.

## 8. O que este recurso entrega?

O contrato devolve problemas estruturados; a assinatura devolve SHA-256 do material versionado; o coletor devolve um envelope de metadados; o laboratório devolve especificação, resultado e resumo. O score sintético é força de evidência na escala 0–100, sem interpretação probabilística.

## 9. Como usar este recurso no Hub?

Com a raiz `.assistant` no caminho Python, importe `hub_micromodelos.execucao.especificacao` e `hub_micromodelos.execucao.fluxo`. A entrada [exemplo_execucao.py](exemplo_execucao.py) executa o piloto de recorrência via `python -m hub_micromodelos.execucao.exemplo_execucao`; a demonstração de recência é [executar_exemplo.py](../exemplos/recencia_contato/executar_exemplo.py). Nenhuma delas publica ou grava tabelas.

| Se você precisa... | Use | Efeito da chamada |
|---|---|---|
| carregar e validar YAML | `especificacao.load_document`, `load_schema`, `validate_spec` | Leitura do arquivo informado e lista de problemas; sem consulta a catálogo. |
| identificar mudança material | `assinatura.calculate_spec_fingerprint` | Hash de regras/fontes/saída da especificação; sem execução de dados. |
| coletar metadata com limites | `metadados.MetadataCollector`; `databricks.DatabricksMetadataProvider` com sessão injetada | Consulta apenas a metadata permitida ao ambiente configurado; não concede permissão de registros. |
| propor shortlist ou YAML inicial | `fluxo.discover_opportunities`, `known_objective` | Hipóteses e especificação com incerteza explícita; o CLI de `fluxo.py` usa fixture local. |
| preparar roteiro de estudo | `artefatos.render_artifacts` | Textos de notebook e README `NOT_RUN`; não abre run. |
| conferir o piloto sintético | `execucao.run_greenfield_lab` | Cálculo da fixture fictícia do laboratório; não prova desempenho corporativo. |
| preparar handoff | `entrega.prepare_handoff` | Rascunho `DRAFT_NOT_SUBMITTED`, sem publicação. |
| ver catálogo e impacto | `catalogo.build_catalog`, `impact_by_source` | Inventário derivado das especificações fornecidas. |

O [guia de jornada](../guias/README.md) mostra quando cada chamada faz sentido. O [exemplo de recência](../exemplos/recencia_contato/README.md) usa a biblioteca para validar, assinar, classificar e preparar um handoff didático; sua regra fechada não é um executor genérico de YAML arbitrário.

## 10. Decisões e configurações que mais importam

`fluxo.SCHEMA` e `fluxo.TEMPLATE` apontam para `../contratos/`. `metadados.Limits` restringe páginas e bytes da coleta. O caso de recência fixa limiar inclusivo de sete dias e pesos 0,7/0,3 no YAML; mudar esses valores altera o cálculo e a assinatura.

## 11. Limitações, riscos e armadilhas

Os módulos de execução não certificam o comportamento do Genie. O laboratório `execucao.py` contém uma heurística fechada para sua fixture; a função recusa uma assinatura de perfil diferente. O adaptador Databricks exige sessão injetada e não amplia permissões de acesso.

## 12. Quais são as alternativas?

Para descrever um caso sem executar dados, use a [skill](../../skills/hub-ml-micromodelos/SKILL.md) e os prompts do Hub. Para acompanhar runs de MLflow, use o recurso compartilhado em [mlflow_run](../../hub_snippets/ml/mlflow_run/README.md), que mantém sua própria API.

## 13. Como saber se o resultado faz sentido?

Confira schema e invariantes, compare a assinatura antes e depois de mudanças materiais, conte novamente as três classes e execute o oráculo do [exemplo de recência](../exemplos/recencia_contato/README.md). Uma conferência local não substitui decisão humana sobre finalidade e fontes.

## 14. Arquivos relacionados e próximos passos

`__init__.py` identifica o pacote; [exemplo_execucao.py](exemplo_execucao.py) demonstra o piloto sintético. `especificacao.py`, `assinatura.py`, `metadados.py`, `fluxo.py`, `artefatos.py`, `databricks.py`, `entrega.py`, `catalogo.py` e `execucao.py` preservam as responsabilidades atuais. Veja a [visão geral](../README.md) e o [contrato](../contratos/micromodelo.schema.json).

## 15. Referências

As funções e o JSON Schema desta pasta definem os contratos. Use o guia de jornada para escolher a etapa e o Manual para entender a integração com o Hub. Consulte o [schema](../contratos/micromodelo.schema.json), a [jornada](../guias/README.md) e o [Manual](../../MANUAL_TECNICO_V2.md#micromodelos).
