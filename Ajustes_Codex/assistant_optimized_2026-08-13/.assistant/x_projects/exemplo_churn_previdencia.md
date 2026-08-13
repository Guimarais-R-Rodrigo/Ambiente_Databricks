# Exemplo fictício — churn em previdência privada

> **EXEMPLO PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Nomes, métricas e caminhos abaixo
> são fictícios. Não os interprete como regra de negócio, meta oficial ou recurso real.

## Metadados

- **Status:** ativo
- **Owner técnico:** Analytics CRM
- **Owner de negócio:** Produtos de Previdência
- **Início / revisão:** 2026-03-10 / 2026-08-01
- **Repositório/Git folder:** `/Workspace/Shared/exemplos/churn-previdencia`
- **Ambientes:** dev / stage / prod

## Problema e decisão

- **Problema:** identificar clientes com risco de resgate total nos próximos 90 dias.
- **Decisão:** priorizar contatos de retenção, respeitando regras de elegibilidade.
- **População/unidade:** uma linha por cliente e data de snapshot mensal.
- **Fora de escopo:** decisão automática de oferta e uso de atributos sensíveis.

## Sucesso e guardrails

| Métrica | Definição | Baseline | Alvo exploratório | Janela | Owner |
|---|---|---:|---:|---|---|
| Recall top decil | eventos capturados nos 10% maiores scores | 10% | 30% | holdout temporal | Analytics CRM |
| Cobertura elegível | clientes elegíveis com score válido | não medido | ≥ 98% | mensal | Data Engineering |

Os alvos são apenas exemplos e precisam de validação econômica e operacional.

## Recursos e contratos

| Recurso | Papel | Chaves | Período | Owner | Sensibilidade |
|---|---|---|---|---|---|
| `main_demo.prev.fato_contribuicoes` | histórico de aportes | id_cliente, dt_evento | 24 meses | Prev Data | restrito |
| `main_demo.prev.dim_planos` | atributos do plano | id_plano | atual + histórico | Prev Data | interno |
| `main_demo.crm.dim_clientes` | atributos elegíveis | id_cliente | snapshot mensal | CRM Data | restrito |
| `main_demo.prev.fato_resgates` | construção do target | id_cliente, dt_evento | 24 meses | Prev Data | restrito |

## Tempo e prevenção de leakage

- **Ponto de predição:** último dia de cada mês.
- **Horizonte:** 90 dias após o snapshot.
- **Disponibilidade:** somente eventos confirmados até o fim do snapshot.
- **Proibidas:** informações de tratamento da campanha e eventos posteriores ao cutoff.

## Decisões

| Data | Decisão | Evidência/justificativa | Impacto | Autor |
|---|---|---|---|---|
| 2026-03-15 | Começar com regressão logística e LightGBM | cria baseline interpretável e benchmark tabular | define experimento inicial | Analytics CRM |
| 2026-03-22 | Holdout por safra mensal | simula previsão em período futuro | reduz leakage temporal | Analytics CRM |

## Alternativas descartadas

| Alternativa | Motivo | Condição para revisitar |
|---|---|---|
| split aleatório | mistura snapshots próximos da mesma entidade | somente em teste sintético sem dependência temporal |
| deep learning inicial | complexidade sem baseline estabelecido | ganho robusto após baselines e custo aprovado |

## Riscos e bloqueios

| Prioridade | Risco/bloqueio | Mitigação | Owner | Prazo |
|---|---|---|---|---|
| P0 | timestamp de disponibilidade incompleto | validar lineage e fonte de cada feature | Data Engineering | 2026-08-20 |
| P1 | prevalência baixa | usar PR-AUC e avaliação top-k | Analytics CRM | 2026-08-25 |

## Definition of Done

- [ ] Target revisado com negócio e sem leakage.
- [ ] Joins preservam granularidade por cliente/snapshot.
- [ ] Baseline ingênuo e modelos comparados em holdout temporal.
- [ ] Artefatos MLflow não contêm PII.
- [ ] Nenhuma promoção/deploy sem aprovação separada.

## Estado e próximos passos

**Estado:** EDA concluída; especificação ponto-no-tempo ainda em validação.

1. Validar disponibilidade das features — owner: Data Engineering — 2026-08-20.
2. Executar baseline após aprovação do target — owner: Analytics CRM — 2026-08-28.
