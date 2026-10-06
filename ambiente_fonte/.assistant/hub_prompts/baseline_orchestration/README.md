# `baseline_orchestration` — estabelecer um baseline honesto antes de otimizar

<!-- readme-objeto: 1.0.0 -->

Briefing para estruturar baseline de ml. O prompt organiza o pedido, mas não executa a tarefa sozinho.

**Antes de executar o preparo:** ele sobrescreve `workspace.default.hub_exemplo_clientes` com `mode("overwrite")`. Esse destino também é usado por EDA, Baseline, Explainability, Novo Projeto, Pipeline e Stat Check: executar um exemplo pode substituir a base de outro. Use o briefing sem executar o preparo quando só precisar do texto.

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

Target, cutoff ou split desconhecidos permitem diagnóstico, perguntas e plano condicionado. Não autorizam treino nem a conclusão de ausência de leakage. Não use o briefing para apresentar um baseline como modelo final aprovado.

## 5. Como funciona, intuitivamente?

Declare o instante da decisão e o que podia ser usado; compare baseline ingênuo e baseline de modelo com split coerente.

## 6. Exemplo de situação

O exemplo pede um classificador de resposta a campanha sobre uma fixture de 4.000 linhas, com split temporal, alvo binário e modo **plano e código; não execute**. Preparar a tabela não treina o modelo. O período e a chave declarados ainda devem ser confrontados com a fonte antes de um experimento.

## 7. O que você precisa antes de usar?

Tenha dataset, unidade/chave, target, cutoff, horizonte, split e métrica. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

O briefing solicita framing e pressupostos; candidatos com justificativa; código quando pedido; resultados por split, tempo e segmento; comparação com baseline ingênuo; erros, reprodutibilidade e próximos experimentos. Métricas observadas só são preenchidas após execução real; em modo plano, permanecem `NÃO EXECUTADO`.

## 9. Como usar este recurso no Hub?

Leia [baseline_orchestration.md](baseline_orchestration.md) e confira os efeitos do [exemplo](exemplo_baseline_orchestration.py) antes do preparo. Siga a [skill correspondente](../../skills/hub-ml-baseline-ml/SKILL.md) e consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json): `current_level` descreve a capacidade vigente; `target_level` não autoriza promoção. O perfil `BINARY_TEMPORAL_LOCAL_V1` é uma rota sintética delimitada; tracking pessoal usa autorização própria `SER10-AUTH-1`. O perfil implementado tem escopo e evidência próprios; não equivale a homologação de todo pedido deste briefing. O notebook tradicional não demonstra essas rotas e sua Parte 3 permanece **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

Cutoff, horizonte, split, evento positivo, colunas proibidas e métrica.

## 11. Limitações, riscos e armadilhas

Leakage entre splits, preprocessing fora do treino e holdout reutilizado. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use [EDA completa](../eda_completa/README.md) para compreender a fonte e [Feature Engineering](../feature_engineering/README.md) para especificar atributos antes do treino.

## 13. Como saber se o resultado faz sentido?

Reconfira sobreposição entre splits, prevalência e ao menos uma métrica contra a referência ingênua. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](baseline_orchestration.md), o [notebook](exemplo_baseline_orchestration.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](baseline_orchestration.md) define os campos e a entrega; o [notebook](exemplo_baseline_orchestration.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
