# `baseline_orchestration` — estabelecer um baseline honesto antes de otimizar

<!-- readme-objeto: 1.0.0 -->

Briefing para estruturar baseline de ml. O prompt organiza o pedido, mas não executa a tarefa sozinho.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para estruturar baseline de ml. |
| Para que serve? | Criar referência simples antes de tuning. |
| Use quando... | Target, cutoff e split já definidos. |
| Evite quando... | Target ou ponto no tempo ainda ambíguos. |
| Precisa de... | Dataset, unidade/chave, target, cutoff, horizonte, split e métrica. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](baseline_orchestration.md) e leia o [notebook de exemplo](exemplo_baseline_orchestration.py).

## 1. O que é?

Briefing para estruturar baseline de ml. O arquivo `baseline_orchestration.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Sem uma referência simples, complexidade pode parecer ganho. O formulário força framing, validação temporal e custo do erro antes do treino.

## 3. Quando faz sentido usar?

Use quando target, cutoff e split já definidos. Criar referência simples antes de tuning.

## 4. Quando não usar?

Evite quando target ou ponto no tempo ainda ambíguos. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Declare o instante da decisão e o que podia ser usado; compare baseline ingênuo e baseline de modelo com split coerente.

## 6. Exemplo de situação

Preencha o briefing com um caso real equivalente ao cenário demonstrado no notebook, mantendo recursos, período e unidade de análise explícitos.

## 7. O que você precisa antes de usar?

Tenha dataset, unidade/chave, target, cutoff, horizonte, split e métrica. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Entrega um pedido estruturado. O contrato do briefing lista os artefatos esperados; confira separadamente o que foi apenas proposto, executado ou validado.

## 9. Como usar este recurso no Hub?

Abra [baseline_orchestration.md](baseline_orchestration.md), preencha os campos e selecione recursos reais. O [notebook](exemplo_baseline_orchestration.py) demonstra o preenchimento. O exemplo sobrescreve `workspace.default.hub_exemplo_clientes`.

## 10. Decisões e configurações que mais importam

Cutoff, horizonte, split, evento positivo, colunas proibidas e métrica.

## 11. Limitações, riscos e armadilhas

Leakage entre splits, preprocessing fora do treino e holdout reutilizado. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use `eda_completa` antes dos dados estarem compreendidos; use `feature_engineering` antes do treino quando faltarem atributos.

## 13. Como saber se o resultado faz sentido?

Reconfira sobreposição entre splits, prevalência e ao menos uma métrica contra a referência ingênua. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](baseline_orchestration.md), o [notebook](exemplo_baseline_orchestration.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

A descrição foi confrontada com [baseline_orchestration.md](baseline_orchestration.md) e [exemplo_baseline_orchestration.py](exemplo_baseline_orchestration.py) na base R11. Para comportamento de plataforma, consulte a documentação oficial atual do Databricks antes de operar em produção.
