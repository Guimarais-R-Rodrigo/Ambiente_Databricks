# domain_context — validação estrita de contexto para SER03/SER05

Componente interno candidato do `hub_scripts.skill_execution`; não substitui o preflight ou o Receipt canônicos.

<!-- readme-objeto: 1.0.0 -->

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que faz? | Verifica forma fechada, tipos, calendário UTC e intenção temporal declarada. |
| Quando usar? | Autoria dos perfis sintéticos SER03/SER05 antes de cálculo ou join. |
| Quando evitar? | Para afirmar que um join foi executado ou que uma fonte foi lida. |
| O que exige? | Contexto explícito; nenhuma inferência de defaults de negócio. |
| O que entrega? | Contexto resolvido ou `ContextError`, sem efeito externo. |

[Implementação e fachada](./__init__.py) · [Exemplo sintético](./exemplo_domain_context.py).

## 1. O que é?

Uma validação de metadados com esquema fechado. O contrato temporal é `SER-TEMPORAL-CONTEXT-1`.

## 2. Que problema este recurso resolve?

Evita que desconhecimento de temporalidade vire falsamente “PIT não aplicável”, e evita que os futuros consumidores adotem cortes ou desempates divergentes.

## 3. Quando faz sentido usar?

Nos dois perfis candidatos B1: safra mensal binária e cross-EDA L2. O owner temporal é único; uma futura adoção por feature engineering requer integração e testes próprios.

## 4. Quando não usar?

Para executar Spark, materializar tabelas, avaliar latência variável ou implementar bitemporalidade. Esses casos são recusados pelo perfil, não aproximados.

## 5. Como funciona, intuitivamente?

Primeiro verifica os campos e tipos. Depois exige um instante UTC e temporalidade explícita. Para `NOT_APPLICABLE`, exige motivo e ausência de configuração temporal conflitante. Para `APPLICABLE`, exige fronteira LE/LT e empate rejeitado.

## 6. Exemplo de situação

Uma decisão sintética ocorre em janeiro de 2026. O exemplo declara fronteira LE e atraso constante de um dia. A saída apenas registra essa regra; não seleciona nem cruza linhas.

## 7. O que você precisa antes de usar?

Dicionário JSON de contexto. O relógio de referência e o de disponibilidade precisam ter nomes distintos. O código verifica as declarações, não a veracidade dos metadados de uma fonte externa.

## 8. O que este recurso entrega?

`validate_temporal_context` retorna schema/version, PIT, instante normalizado, motivo, configuração e `join_executed=false`. Entradas não suportadas levantam `ContextError`.

## 9. Como usar este recurso no Hub?

Importe `validate_temporal_context` da [fachada](./__init__.py). O [exemplo](./exemplo_domain_context.py) chama a função com dados sintéticos, sem criar arquivo ou tabela.

## 10. Decisões e configurações que mais importam

UTC, LE versus LT, atraso constante inteiro e empate REJECT são escolhas explícitas do perfil. Atributos adicionais são rejeitados. `loads_strict` rejeita chave JSON duplicada e números não finitos.

## 11. Limitações, riscos e armadilhas

Resolver contexto não comprova cobertura de join nem prontidão ML. Hash de JSON não autentica dados nem usuário. O suporte de manifesto em [release.py](./release.py) confere arquivos declarados, não todas as dependências de bibliotecas externas.

## 12. Quais são as alternativas?

O [preflight SEF existente](../__init__.py) resolve recursos e templates. Este componente fornece verificações de domínio que o complementam. O [Receipt existente](../receipt/__init__.py) continua dono do protocolo L3.

## 13. Como saber se o resultado faz sentido?

Teste UNKNOWN, falta de timezone, fronteira ambígua, atraso variável e empate não declarado. Todos precisam bloquear. Para dados estáticos com motivo explícito, a saída deve continuar sem join.

## 14. Arquivos relacionados e próximos passos

[Schema temporal](./temporal.schema.json), [fachada](./__init__.py), [exemplo](./exemplo_domain_context.py) e [integridade de release](./release.py). O registro da campanha B1 e sua qualificação continuam separados.

## 15. Referências

Comportamento sustentado pelos arquivos locais acima e pelo plano B1 do repositório. Estado: testes de domínio em overlay Linux; integração completa com checkout, renderer e ambiente de campanha ainda pendente.
