# Template: Especificação de Pipeline ML

> **[N etapas]** stages | **[Modelo]** servido | **[Freq]** scoring | **[SLA]** latência


## Identificação
| Aspecto | Valor |
|---|---|
| Nome do pipeline | [nome] |
| Modelo servido | [nome + versão] |
| Owner | [time/pessoa] |
| Criação | [data] |
| Última atualização | [data] |

## Tabelas

| Camada | Tabela | Descrição | Partição |
|---|---|---|---|
| Bronze | [catalog.schema.table] | [desc] | [col] |
| Silver | [catalog.schema.table] | [desc] | [col] |
| Gold | [catalog.schema.table] | [desc] | [col] |
| Scoring | [catalog.schema.table] | [desc] | [col] |

## Dependências
- Tabelas fonte: [lista]
- Modelo: [MLflow URI]
- Feature Store: [tabela]
- Clusters/Compute: [spec]

## Schedule
| Etapa | Frequência | SLA | Alerta |
|---|---|---|---|
| Bronze | [freq] | [tempo] | [canal] |
| Silver | [freq] | [tempo] | [canal] |
| Gold | [freq] | [tempo] | [canal] |
| Scoring | [freq] | [tempo] | [canal] |

## Validações (Expectations)
| Etapa | Validação | Limiar | Ação |
|---|---|---|---|
| [etapa] | [descrição] | [valor] | [fail/warn/quarantine] |

## Monitoramento
- Drift: [frequência + limiar]
- Performance: [métrica + limiar]
- Volume: [esperado ± tolerância]

---

#### ✅ Checklist de prontidão

| Item | Status |
|---|---|
| Tabelas fonte existem | ✅ / ❌ |
| Modelo registrado no UC | ✅ / ❌ |
| Validações (expectations) definidas | ✅ / ❌ |
| Schedule configurado | ✅ / ❌ |
| Alertas configurados | ✅ / ❌ |
