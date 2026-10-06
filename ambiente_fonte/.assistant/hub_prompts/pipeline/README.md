# `pipeline` — desenhar pipeline operável antes de fazer deploy

<!-- readme-objeto: 1.0.0 -->

Briefing para pipeline de dados com Lakeflow quando apropriado. O prompt organiza o pedido, mas não executa a tarefa sozinho.

**Antes de executar o preparo:** ele sobrescreve `workspace.default.hub_exemplo_clientes` com `mode("overwrite")`. Esse destino também é usado por EDA, Baseline, Explainability, Novo Projeto, Pipeline e Stat Check: executar um exemplo pode substituir a base de outro. Use o briefing sem executar o preparo quando só precisar do texto.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Briefing para pipeline de dados com Lakeflow quando apropriado. |
| Para que serve? | Explicitar fontes, destino, modo, chaves, schema, qualidade, SLO e ambientes. |
| Use quando... | Contratos e reprocessamento podem ser descritos. |
| Evite quando... | Origem ainda está incorreta ou ambiente alvo indefinido. |
| Precisa de... | Objetivo, fontes, destinos, modo, chaves, schema, regras, slo e ambientes. |
| Entrega... | Briefing estruturado; evidências dependem da interação real. |

Comece pelo [briefing original](pipeline.md) e leia o [notebook de exemplo](exemplo_pipeline.py).

## 1. O que é?

Briefing para pipeline de dados com Lakeflow quando apropriado. O arquivo `pipeline.md` é a fonte do formulário e do contrato de saída.

## 2. Que problema este recurso resolve?

Automatizar transformação sem idempotência, schema e recuperação apenas repete erros com maior frequência.

## 3. Quando faz sentido usar?

Use quando contratos e reprocessamento podem ser descritos. Explicitar fontes, destino, modo, chaves, schema, qualidade, SLO e ambientes.

## 4. Quando não usar?

Evite quando origem ainda está incorreta ou ambiente alvo indefinido. Gerar texto ou código não valida premissas ausentes.

## 5. Como funciona, intuitivamente?

Comece pelos contratos e chegada; desenhe estado, deduplicação, late data e qualidade antes de bundle/deploy.

## 6. Exemplo de situação

Desenhar uma carga incremental com chave e sequência declaradas, repetição da mesma carga e chegada de coluna nova. Pedir arquitetura e código com casos de replay e schema incompatível. O notebook atual só prepara uma tabela sintética; não cria pipeline nem prova MERGE ou reprocessamento.

## 7. O que você precisa antes de usar?

Tenha objetivo, fontes, destinos, modo, chaves, schema, regras, SLO e ambientes. Use `NÃO INFORMADO` para lacunas em vez de inventar defaults.

## 8. O que este recurso entrega?

Solicita arquitetura proporcional; contratos de input/output e chaves; qualidade, watermark/CDC quando aplicáveis; árvore e configuração; testes; plano de deploy, rollback, observabilidade e custo. Bronze/silver/gold, streaming e bundle são escolhas justificadas, não etapas obrigatórias em qualquer projeto.

## 9. Como usar este recurso no Hub?

Leia e preencha [pipeline.md](pipeline.md) antes de decidir sobre o preparo. Siga a [skill correspondente](../../skills/hub-ml-pipeline-builder/SKILL.md) e consulte a [policy vigente](../../hub_padroes/skill_enforcement/policy.json): `current_level` descreve a capacidade vigente; `target_level` não autoriza promoção. Spec local, runner Spark/Delta e efeitos persistentes são rotas distintas; o efeito exige destino confirmado, autorização e evidência de execução/readback/limpeza. O perfil implementado tem escopo e evidência próprios; não equivale a homologação de todo pedido deste briefing. O aceite de um perfil sintético não autoriza deploy no trabalho.

O [notebook](exemplo_pipeline.py) sobrescreve `workspace.default.hub_exemplo_clientes`, sem criar pipeline real. Parte 3: **NÃO EXECUTADO**.

## 10. Decisões e configurações que mais importam

Batch/streaming/CDC, chave/sequência, schema, expectations, checkpoint, ambientes e rollback.

## 11. Limitações, riscos e armadilhas

Streaming sem necessidade, deploy no catálogo errado e reprocessamento não idempotente. A instrução textual não substitui permissões, revisão nem controles técnicos.

## 12. Quais são as alternativas?

Use [Qualidade](../data_quality/README.md) para regras de dados ou [Novo Projeto](../novo_projeto/README.md) para organizar objetivo e responsáveis.

## 13. Como saber se o resultado faz sentido?

Defina o resultado esperado por caso: replay não duplica; falha parcial preserva estado verificável; schema incompatível bloqueia a carga; destino e ambiente são explícitos. Se persistência ou limpeza não puderem ser conferidas, registre `UNKNOWN`; retry não prova retroativamente o efeito anterior.

## 14. Arquivos relacionados e próximos passos

O [briefing](pipeline.md), o [notebook](exemplo_pipeline.py) e o [catálogo](../README.md) formam o caminho local. O próximo passo depende do diagnóstico, não do simples término da resposta.

## 15. Referências

O [briefing](pipeline.md) define os campos e a entrega; o [notebook](exemplo_pipeline.py) mostra o cenário e o estado da evidência. Confira a rota atual na skill antes de executar. O exemplo conversacional permanece **NÃO EXECUTADO**; a existência de código ou de outro teste não preenche essa lacuna.
