# Backlog de Features (Tier A/B/C)

## Uso
Priorizar investigação/implementação conforme evidência de valor, risco, custo,
disponibilidade e reuso. Tier não autoriza acesso, materialização ou uso em
modelo. RFV, recência e razões são hipóteses de sinal; não são alto sinal ou
baixo risco por definição.

## Critérios a calibrar pelo estudo

| Tier | Interpretação da prioridade | Evidência necessária | Próxima ação proposta |
|---|---|---|---|
| A | Candidata a primeiro ciclo | Disponibilidade temporal, risco e custo compatíveis; valor esperado justificado | Validar premissas e implementar somente no escopo aprovado |
| B | Dependências ou incertezas adicionais | Fonte/semântica, ganho incremental e custo a conferir | Resolver dependências antes da execução |
| C | Exploração de maior incerteza | Hipótese, experimento delimitado, orçamento e critério de parada | Avaliar viabilidade sem prometer sinal |

## Preenchimento
- **feature_name**: mesmo nome da spec.
- **motivo**: hipótese de sinal ou evidência incremental, distinguindo-os.
- **risco**: avaliado com fonte/método; NÃO AVALIADO enquanto faltar disponibilidade.
- **dependencias**: fontes, instante de publicação, joins e decisões pendentes.
- **status**: pendente, em andamento, implementada ou bloqueada com evidência.

| tier | feature_name | motivo/evidência | risco | dependencias | status |
|---|---|---|---|---|---|
| [A/B/C a confirmar] | [feature] | [hipótese ou resultado] | [avaliação ou NÃO AVALIADO] | [fontes/decisões] | [pendente] |

## Exemplos ilustrativos fictícios

| Candidata | Hipótese a testar | Disponibilidade/risco |
|---|---|---|
| `feat_saldo_medio_poupanca_90d` | Saldo histórico pode acrescentar informação ao modelo | NÃO VERIFICADOS; confirmar janela, atraso e autorização |
| `feat_qtd_acessos_app_30d` | Atividade digital pode ter associação com o target | NÃO VERIFICADOS; não equivale a propensão nem efeito causal |
| `feat_razao_saldo_renda` | Razão pode ajudar na segmentação | NÃO VERIFICADOS; conferir denominador, atualização e sensibilidade |
| `feat_woe_segmento` | Codificação pode agregar sinal fora da amostra | Fit só no treino, validação OOT e prevenção de leakage |

Não preencher tier, sinal ou risco do caso real a partir desses exemplos.
