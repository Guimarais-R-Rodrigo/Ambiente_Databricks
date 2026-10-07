# domain_context — validar metadados temporais de perfis suportados

Componente interno para integração de skills, sem leitura de registros ou execução de joins. Não substitui preflight ou Receipt canônicos.

<!-- readme-objeto: 1.0.0 -->

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que faz? | Verifica forma fechada, tipos, calendário UTC e intenção temporal declarada. |
| Quando usar? | Integração de perfis temporais suportados antes de cálculo ou join. |
| Quando evitar? | Para afirmar que um join foi executado ou que uma fonte foi lida. |
| O que exige? | Contexto explícito; nenhuma inferência de defaults de negócio. |
| O que entrega? | Contexto resolvido ou `ContextError`, sem efeito externo. |

[Implementação e fachada](./__init__.py) · [Exemplo sintético](./exemplo_domain_context.py).

## 1. O que é?

Uma validação de metadados com esquema fechado. O contrato temporal é `SER-TEMPORAL-CONTEXT-1`.

## 2. Que problema este recurso resolve?

Evita que desconhecimento de temporalidade vire falsamente “PIT não aplicável”, e evita que os futuros consumidores adotem cortes ou desempates divergentes.

## 3. Quando faz sentido usar?

Usado pelos perfis temporais de [Safra](../../../skills/hub-ml-analise-safra/SKILL.md) e [Cross-EDA](../../../skills/hub-ml-cross-eda-ml/SKILL.md). Outro consumidor, inclusive Feature Engineering, exige integração e testes próprios; não deduza adoção pela semelhança de campos.

## 4. Quando não usar?

Para executar Spark, materializar tabelas, avaliar latência variável ou implementar bitemporalidade. Esses casos são recusados pelo perfil, não aproximados.

## 5. Como funciona, intuitivamente?

Primeiro verifica os campos e tipos. Depois exige um instante UTC e temporalidade explícita. Para `NOT_APPLICABLE`, exige motivo e ausência de configuração temporal conflitante. Para `APPLICABLE`, exige fronteira LE/LT e empate rejeitado.

## 6. Exemplo de situação

Uma decisão sintética ocorre em janeiro de 2026. O exemplo declara fronteira LE e atraso constante de um dia. A saída apenas registra essa regra; não seleciona nem cruza linhas.

## 7. O que você precisa antes de usar?

A assinatura é keyword-only: `validate_temporal_context(*, pit, temporal, decision_at, not_applicable_reason=None)`.

Para `APPLICABLE`, `temporal` deve conter exatamente oito campos:
`reference_column`, `availability_column`, `lag_kind`, `lag_days`, `boundary`,
`timezone`, `tie_break`, `bitemporal`. Os relógios precisam de nomes distintos;
`lag_kind="CONSTANT"`, `lag_days` inteiro de 0 a 36.500 (bool rejeitado),
`boundary="LE"` ou `"LT"`, `timezone="UTC"`, `tie_break="REJECT"` e
`bitemporal=False`. `decision_at` exige instante com offset UTC.

Para `NOT_APPLICABLE`, use `temporal=None` e motivo não vazio, sem espaços
externos, em `not_applicable_reason`. `UNKNOWN` bloqueia. O código verifica a
declaração, não a veracidade dos metadados externos.

Dicionário JSON de contexto. O relógio de referência e o de disponibilidade precisam ter nomes distintos. O código verifica as declarações, não a veracidade dos metadados de uma fonte externa.

## 8. O que este recurso entrega?

`validate_temporal_context` retorna schema/version, PIT, instante normalizado, motivo, configuração e `join_executed=false`. Entradas não suportadas levantam `ContextError`.

## 9. Como usar este recurso no Hub?

Importe da [fachada](__init__.py) e use o [exemplo](exemplo_domain_context.py), que não cria arquivo ou tabela. Chamada ilustrativa de não aplicabilidade:

```python
validate_temporal_context(
    pit="NOT_APPLICABLE", temporal=None,
    decision_at="2026-01-10T00:00:00Z",
    not_applicable_reason="Contexto estático sintético",
)
```

O retorno mantém `join_executed=False`. Para contexto aplicável, siga os oito campos do schema e o exemplo; a validação não seleciona linhas.

## 10. Decisões e configurações que mais importam

UTC, LE versus LT, atraso constante inteiro e empate REJECT são escolhas explícitas do perfil. Atributos adicionais são rejeitados. `loads_strict` rejeita chave JSON duplicada e números não finitos.

## 11. Limitações, riscos e armadilhas

| Código | Interpretação |
|---|---|
| `PIT:UNKNOWN_BLOCKS` | intenção temporal desconhecida |
| `TEMPORAL:CLOCKS_MUST_BE_DISTINCT` | referência e disponibilidade têm mesmo nome |
| `TEMPORAL:VARIABLE_LATENCY_UNSUPPORTED` | atraso variável não suportado |
| `decision_at:UTC_AWARE_REQUIRED` | instante sem offset UTC |
| `lag_days:INTEGER_OUT_OF_RANGE` | inteiro fora do intervalo ou tipo inválido, inclusive bool |

`loads_strict` recebe **texto JSON** e detecta chave duplicada antes de formar o
dict; `validate_temporal_context` recebe dict já construído e não recupera
chaves perdidas. JSON malformado pode lançar `JSONDecodeError`; nem todo erro
de parsing é `ContextError`.

Resolver contexto não comprova cobertura de join nem prontidão ML. Hash de JSON não autentica dados nem usuário. O suporte de manifesto em [release.py](./release.py) confere arquivos declarados, não todas as dependências de bibliotecas externas.

## 12. Quais são as alternativas?

O [preflight SEF existente](../__init__.py) resolve recursos e templates. Este componente fornece verificações de domínio que o complementam. O [Receipt existente](../receipt/__init__.py) continua dono do protocolo L3.

## 13. Como saber se o resultado faz sentido?

Teste UNKNOWN, falta de timezone, fronteira ambígua, atraso variável e empate não declarado. Todos precisam bloquear. Para dados estáticos com motivo explícito, a saída deve continuar sem join.

## 14. Arquivos relacionados e próximos passos

Consulte [schema temporal](temporal.schema.json), [fachada](__init__.py), [exemplo](exemplo_domain_context.py) e [integridade de release](release.py). Registro de desenvolvimento, externo ao pacote: [gates dos perfis sintéticos](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/main/docs/sprints/skill_enforcement_rollout/B1_GATES_POS_MERGE_2026-10-01.md).

## 15. Referências

O contrato `SER-TEMPORAL-CONTEXT-1` é sustentado pela implementação e pelo schema locais. Resolver contexto não comprova execução em dados, promoção de policy nem certificação universal.
