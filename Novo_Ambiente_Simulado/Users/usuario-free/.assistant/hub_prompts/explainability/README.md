# `explainability` — explicar previsões sem transformar contribuição em causalidade

<!-- readme-objeto: 1.0.0 -->

Briefing para explicabilidade global/local de modelo. O prompt organiza o pedido, mas não executa a tarefa sozinho.

**Antes de executar o preparo:** ele sobrescreve `workspace.default.hub_exemplo_clientes` com `mode("overwrite")`. Esse destino também é usado por EDA, Baseline, Explainability, Novo Projeto, Pipeline e Stat Check: executar um exemplo pode substituir a base de outro. Use o briefing sem executar o preparo quando só precisar do texto.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para explicabilidade global/local de modelo. |
| Para que serve? | Alinhar modelo, população, método e público. |
| Use quando... | Modelo e split podem ser identificados. |
| Evite quando... | Versão do modelo ou população não estão confirmadas. |
| Precisa de... | Modelo/run, dataset/split, target, objetivo, público, método e amostra. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](explainability.md) e leia o [notebook de exemplo](exemplo_explainability.py).

## 1. O que é?

Briefing para explicabilidade global/local de modelo. O arquivo `explainability.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Explicações são fáceis de superinterpretar. O formulário separa performance, contribuição do modelo, associação e efeito causal.

## 3. Quando faz sentido usar?

Use quando modelo e split podem ser identificados. Alinhar modelo, população, método e público.

## 4. Quando não usar?

Evite quando versão do modelo ou população não estão confirmadas. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Fixe modelo e população, escolha a pergunta explicativa e o método, então aplique sanity checks.

## 6. Exemplo de situação

Planejar explicação global e um caso local de um modelo de resposta a campanha, no holdout temporal e na população declarada. O exemplo cita um LightGBM pretendido, mas **não o treina**: até existir artefato verificável, a entrega é plano/código, sem valores SHAP observados.

## 7. O que você precisa antes de usar?

Exija modelo/run verificável, dataset e split, transformação e ordem das features, target/classe positiva, espaço da saída e background quando aplicável. Declare amostra e público. Sem modelo ou população confirmados, mantenha o plano e as lacunas; dependência SHAP não informa presença de PII.

## 8. O que este recurso entrega?

Solicita resumo; achados globais e locais separados; evidência e incerteza; limitações; validações pendentes; e código opcional. Contribuição na previsão não é efeito causal, fairness nem conformidade. Valores só são observados depois de computação e verificação compatíveis com a rota.

## 9. Como usar este recurso no Hub?

Leia [explainability.md](explainability.md). Siga a [skill correspondente](../../skills/hub-ml-explainability/SKILL.md) e consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json): `current_level` descreve a capacidade vigente; `target_level` não autoriza promoção. O perfil `LINEAR_REGRESSION_SYNTHETIC_V1` suporta SHAP linear escalar sintético, com verificador e entradas independentes; não comprova o cenário LightGBM do briefing. O perfil implementado tem escopo e evidência próprios; não equivale a homologação de todo pedido deste briefing.

O [exemplo](exemplo_explainability.py) apenas prepara dados, sobrescrevendo `workspace.default.hub_exemplo_clientes`. Não cria modelo, treino ou SHAP. Instalação, quando necessária, é etapa separada e autorizada. Parte 3: **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

Versão do modelo, split, espaço da saída, explainer/background, amostra e público.

## 11. Limitações, riscos e armadilhas

Explicar versão errada, tratar SHAP como efeito causal ou expor PII. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Para performance, use [Baseline](../baseline_orchestration/README.md) ou [Monitoramento](../monitoramento_modelo/README.md). Para hipóteses estatísticas, use [Stat Check](../stat_check/README.md).

## 13. Como saber se o resultado faz sentido?

Confirme modelo, schema, split, classes, sinal e estabilidade quando aplicável. Separe fatos observados, hipóteses e recomendações.

## 14. Arquivos relacionados e próximos passos

O [briefing](explainability.md), o [notebook](exemplo_explainability.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](explainability.md) define os campos e a entrega; o [notebook](exemplo_explainability.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
