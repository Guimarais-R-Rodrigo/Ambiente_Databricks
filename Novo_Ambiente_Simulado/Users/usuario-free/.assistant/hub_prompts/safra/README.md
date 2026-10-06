# `safra` — comparar safras na mesma maturidade

<!-- readme-objeto: 1.0.0 -->

Briefing para safra/vintage com coorte, idade, numerador, denominador e censura. O prompt organiza o pedido, mas não executa a tarefa sozinho.

**Preparo persistente:** o exemplo sobrescreve `workspace.default.hub_exemplo_safras`. Confira destino e autorização antes de executar; o briefing pode ser estudado sem criar a tabela.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para safra/vintage com coorte, idade, numerador, denominador e censura. |
| Para que serve? | Evitar comparar coortes com maturidade diferente. |
| Use quando... | Coorte, maturidade e evento estão claros. |
| Evite quando... | Célula imatura é tratada como zero ou regra normativa não tem fonte. |
| Precisa de... | Dataset, entidade/chave, safra, idade, evento, denominador, métrica e censura. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](safra.md) e leia o [notebook de exemplo](exemplo_safra.py).

## 1. O que é?

Briefing para safra/vintage com coorte, idade, numerador, denominador e censura. O arquivo `safra.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Safras recentes parecem melhores quando tiveram menos tempo para maturar. Sem denominador e censura a curva pode enganar.

## 3. Quando faz sentido usar?

Use quando coorte, maturidade e evento estão claros. Evitar comparar coortes com maturidade diferente.

## 4. Quando não usar?

Evite quando célula imatura é tratada como zero ou regra normativa não tem fonte. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Crie grade safra×idade, preserve células não observáveis e compare idades equivalentes.

## 6. Exemplo de situação

Compare duas safras de contratação: uma observada até M6 e outra até M3. A comparação comum é M3; M4–M6 da mais recente continuam não observáveis. Não converta ausência de maturação ou cobertura em taxa zero. Esse exemplo de interpretação não é um resultado medido do notebook.

## 7. O que você precisa antes de usar?

Tenha dataset, entidade/chave, safra, idade, evento, denominador, métrica e censura. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Solicita dicionário da métrica e linha do tempo; matriz safra×maturidade com numerador, denominador, volume e taxa; curvas/heatmap; alertas de baixo N; e limitações de censura, composição e dados incompletos. Gráficos e métricas observados dependem de execução real.

## 9. Como usar este recurso no Hub?

Preencha [safra.md](safra.md). Siga a [skill correspondente](../../skills/hub-ml-analise-safra/SKILL.md) e consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json): `current_level` descreve a capacidade vigente; `target_level` não autoriza promoção. O perfil sintético `MONTHLY_BINARY_PILOT_V1` tem contrato delimitado de roster fixo, maturidade e cobertura. O perfil implementado tem escopo e evidência próprios; não equivale a homologação de todo pedido deste briefing.

O [notebook](exemplo_safra.py) sobrescreve `workspace.default.hub_exemplo_safras`. Criar a fixture não executa a análise nem valida norma regulatória. Parte 3: **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

Entrada na coorte, MOB, evento cumulativo, denominador, censura e maturidade comum.

## 11. Limitações, riscos e armadilhas

Somar taxas cumulativas, dupla contagem e atribuir causa a mix/maturação. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use [vintage_analysis](../../hub_snippets/ml/vintage_analysis/README.md) para entender o cálculo reutilizável e [Baseline](../baseline_orchestration/README.md) para discutir uma análise survival apropriada à censura.

## 13. Como saber se o resultado faz sentido?

Reconcilie entidades e recalcule manualmente uma célula completa. No perfil de roster fixo, preserve o denominador da coorte: cobertura `1/2` não autoriza taxa provisória com denominador 1. Uma célula incompleta não recebe taxa final como se tivesse exposição completa. Distinga estimativa rotulada, falta de observação e zero verdadeiro; compare somente maturidade comum.

## 14. Arquivos relacionados e próximos passos

O [briefing](safra.md), o [notebook](exemplo_safra.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](safra.md) define os campos e a entrega; o [notebook](exemplo_safra.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
