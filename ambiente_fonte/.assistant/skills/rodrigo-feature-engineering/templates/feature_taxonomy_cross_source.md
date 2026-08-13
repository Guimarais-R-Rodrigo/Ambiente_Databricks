<!-- Template: taxonomia de features cross-source — Modo B (skill rodrigo-feature-engineering) -->

# 🧬 Família 8 — Features Cross-Source (Interações Inter-Fonte)

> Esta família só existe no **Modo B** (input vindo do Cross-EDA).
> São features que combinam variáveis de fontes DIFERENTES, impossíveis
> de criar com uma fonte isolada.

## Subtipos

### 8.1 Razões cross-source
Features que dividem uma métrica de uma fonte por outra de fonte diferente.

| feature_name | definição | fonte_numerador | fonte_denominador | janela |
|---|---|---|---|---|
| `feat_razao_saldo_renda` | Saldo / renda declarada | [fonte_saldos] | [fonte_cadastro] | snapshot |
| `feat_uso_sobre_limite` | Utilização crédito / limite aprovado | [fonte_transacoes] | [fonte_credito] | 30d |
| `feat_ticket_vs_mediana_segmento` | Ticket médio / mediana do segmento | [fonte_transacoes] | [fonte_segmentacao] | 90d |

### 8.2 Diferenças cross-source
Medir divergência entre mesma métrica em fontes diferentes, ou entre métrica e benchmark.

| feature_name | definição | fonte_A | fonte_B | interpretação |
|---|---|---|---|---|
| `feat_delta_renda_declarada_vs_estimada` | Renda cadastro - renda estimada por modelo | [cadastro] | [bureau] | Divergência indica inconsistência |
| `feat_saldo_vs_media_coorte` | Saldo - média do coorte temporal | [saldos] | [agregado_coorte] | Posição relativa |

### 8.3 Flags de presença/ausência cross-source
Indicadores binários sobre a existência (ou não) de dados em determinada fonte.

| feature_name | definição | fonte | interpretação |
|---|---|---|---|
| `feat_flag_tem_bureau` | 1 se cliente tem registro no bureau | [bureau] | Ausência pode indicar perfil thin-file |
| `feat_flag_tem_transacao_30d` | 1 se cliente transacionou nos últimos 30d | [transacoes] | Proxy de atividade |
| `feat_qtd_fontes_com_dados` | Contagem de fontes com dado para este cliente | [todas] | Proxy de completude |

### 8.4 Combinações temporais cross-source
Features que combinam informação temporal de fontes com frequências diferentes.

| feature_name | definição | fonte_rapida | fonte_lenta | janela |
|---|---|---|---|---|
| `feat_aceleracao_gasto_vs_renda` | Δ gasto 30d / renda fixa | [transacoes] | [cadastro] | 30d vs. snapshot |
| `feat_trend_saldo_vs_mercado` | Tendência saldo cliente / tendência índice | [saldos] | [mercado] | 90d |

## Validação anti-leakage

Para toda feature cross-source, verificar:
- [ ] Ambas as fontes existiam no ponto de referência temporal
- [ ] Nenhuma fonte contém informação pós-evento
- [ ] O join entre fontes não introduz leakage (fonte B não é resultado do target)
- [ ] Missingness na fonte B não é proxy do target

## Quando NÃO criar features cross-source

- Coverage da fonte secundária < 50% (feature terá mais nulos que valores)
- Fontes com temporalidade incompatível (uma é D-0, outra é M-1)
- PSI cross-source acima do limite aprovado (mesma variável medida de forma diferente em cada fonte)
