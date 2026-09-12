# Achados — R04-A

Data: 2026-09-12. Autor e revisor próprio: ChatGPT (A0_light).
Base fixa: `1be947b0a62c3b0b85fa3cd5692f474b9066d85f`.

Os achados abaixo registram diferenças entre uma leitura superficial dos nomes ou
notebooks e o contrato efetivamente implementado. Nesta sprint, limitações são
documentadas e testadas; algoritmos não são alterados silenciosamente para fazer
a implementação caber na explicação.

## A01 — `date_features` contém um calendário fixo restrito embutido

`date_features` não depende apenas da lista opcional `holiday_dates`. A implementação
contém nove feriados nacionais de data fixa, identificados por `MM-dd`, e cria uma
flag separada para as datas fornecidas pelo projeto. Isso não equivale a um calendário
brasileiro completo: feriados móveis e calendários locais precisam ser tratados fora
desse conjunto fixo ou informados explicitamente quando o contrato permitir.

**Tratamento:** README e notebook distinguem `is_feriado_nacional_fixo` de
`is_feriado_calendario` e evitam apresentar o helper como calendário oficial completo.

## A02 — conversão de data depende do modo ANSI e pode sobrescrever colunas de destino

O helper usa `to_date`, portanto a componente de horário não participa das features.
A primeira execução remota com PySpark 4.0.1 mostrou que `bad-date` produz
`CAST_INVALID_INPUT` no modo ANSI, em vez de `NULL`. A documentação atual do Databricks
confirma que `to_date` levanta erro para entrada malformada com ANSI habilitado e pode
retornar `NULL` quando ANSI está desabilitado; para tolerância explícita, recomenda
`try_cast(... AS DATE)`. A implementação também usa `withColumn`: se um nome de feature
já existir, ele pode ser substituído.

**Tratamento:** README e teste foram corrigidos para não prometer tolerância que o helper
não implementa. Nenhuma validação ou conversão funcional nova foi introduzida.

## A03 — cobertura de `join_diagnostics` usa linhas válidas da esquerda

`cobertura_pct_chaves_validas` tem como denominador as linhas da esquerda com chave
válida, não as chaves distintas, nem todas as linhas incluindo chaves nulas. O texto
histórico do notebook usava a expressão “cobertura sobre o total”, que poderia induzir
outra interpretação.

**Tratamento:** prosa corrigida; saída histórica e campo retornado preservados.

## A04 — relação e expansão do join são diagnóstico, não política automática

A multiplicidade da direita é analisada somente para chaves que aparecem na esquerda.
O rótulo `1:N` informa possibilidade de duplicação; não bloqueia o join nem corrige a
modelagem. Em esquerda vazia, a expansão `left` é 1.0 por convenção da implementação.
O helper ainda executa várias ações e joins Spark; não há promessa universal de custo
baixo por tamanho nominal da tabela.

**Tratamento:** README separa interpretação de decisão e remove promessas de desempenho
sem benchmark.

## A05 — `null_summary` mede `NULL`, não toda forma de ausência

O resumo usa `isNull`. Strings vazias, códigos sentinela e outras convenções de ausência
não entram automaticamente no percentual. A função faz contagem da tabela e coleta uma
linha de agregados ao driver para construir o resultado.

**Tratamento:** escopo explicitado no README e comparação com ferramentas de perfil/qualidade.

## A06 — limiares incoerentes não são recusados por `null_summary`

A implementação não exige `0 <= threshold_warn <= threshold_fail <= 100`. O status
testa primeiro o limiar de falha e depois o de alerta. Portanto uma política como
`warn=80`, `fail=20` é aceita e pode produzir vermelho; o helper não valida a coerência
da política fornecida.

**Tratamento:** caso adversarial acrescentado ao suplemento; comportamento caracterizado,
não aprovado como desenho ideal.

## A07 — `null_summary`, `quick_profile` e `data_quality_check` têm contratos diferentes

`null_summary` é um resumo específico de nulos por DataFrame. `quick_profile` cobre um
perfil mais amplo e tem escolhas próprias de amostragem/escopo. `data_quality_check`
(script previsto para R04-B) trabalha com tabela, chaves e regras adicionais, incluindo
validações de limiares. Nomes relacionados não tornam as APIs equivalentes.

**Tratamento:** alternativas são comparadas por finalidade e links apontam para o recurso
já documentado ou para a implementação quando o README ainda não existe.

## A08 — o PSI numérico deriva os cortes da base com erro relativo fixo

`psi_calculator` calcula quantis na população de referência usando `approxQuantile`
com `relativeError=0.01`, deduplica fronteiras e usa bucket próprio para ausentes. Os
cortes não são recalculados a partir da população atual. Isso faz parte do contrato
observado e deve ser registrado ao comparar execuções.

**Tratamento:** README descreve a construção dos buckets, não apenas a fórmula final.

## A09 — CSI categórico pode coletar muitas categorias ao driver

O CSI agrega distribuições por categoria, aplica um limite por população e coleta os
resultados agrupados ao driver. O tipo numérico/categórico é decidido a partir dos tipos
da base; o helper não faz uma validação explícita de paridade de schema entre base e atual.

**Tratamento:** risco de cardinalidade e pré-condição de schema explicitados. O limite
`max_categorias` é tratado como guarda, não como prova de custo baixo.

## A10 — `interpretar_psi` só aplica política calibrada com os dois limiares

Informar apenas um dos dois limiares não ativa uma classificação parcial: a função cai
na interpretação genérica. Quando ambos são informados, exige ordem válida. Limiares
de PSI não são apresentados como universais e `drift_detector` não é tratado como API
ou implementação numericamente idêntica.

**Tratamento:** notebook e README distinguem contratos relacionados e evitam “mesma lógica”.

## A11 — `safe_display` precisa de renderer no uso modular comum

O fallback procura `display` no `globals()` do próprio módulo. Importar o helper em um
notebook não injeta automaticamente o `display` daquele notebook nesse namespace. Por
isso o padrão robusto é `safe_display(df, display_fn=display)` quando se usa a função
como módulo. Sem renderer disponível, a função levanta `RuntimeError`.

**Tratamento:** uso mínimo e teste adversarial reproduzem essa exigência.

## A12 — limitar a prévia não barateia automaticamente o plano upstream

`safe_display` usa `limit(limit + 1).count()` para detectar truncamento e renderiza no
máximo `limit`. Isso limita o volume entregue ao renderer; não garante que transformações
globais anteriores deixem de ser caras.

**Tratamento:** título/prosa do notebook corrigidos para não transformar `limit` em promessa
de custo constante.

## A13 — `smart_sample` usa `n` como teto no modo simples

No caminho sem estratificação, a função calcula uma fração superdimensionada em 20%,
amostra e aplica `limit(n)`. A margem aumenta a chance de alcançar o teto, mas pode
resultar em menos de `n`. Em base já pequena (`<= n`), o próprio DataFrame é devolvido.

**Tratamento:** o README rejeita a ideia de “exatamente n” no modo simples e o teste confere
somente o limite superior.

## A14 — tamanho exato no modo estratificado depende das condições de elegibilidade

Quando a base tem mais que `n` linhas e o número de estratos não excede `n`, a alocação
é construída para somar `n` e reservar ao menos uma linha por estrato. Mais estratos que
`n` são recusados. Esse caminho usa agregação, join e janelas; cardinalidade alta continua
sendo questão de custo. `seed` ajuda na repetição sob mesma entrada/plano, mas não garante
identidade eterna entre versões, particionamentos ou planos diferentes.

**Tratamento:** garantias condicionais e custo estão explícitos; o notebook não generaliza
uma contagem histórica como contrato universal.

## Escopo dos achados

Nenhum achado desta lista autoriza mudança funcional, alteração de API, atualização de
paleta/CSS, publicação ou homologação Databricks. Uma eventual correção de comportamento
funcional deve ter tarefa, testes e aceite próprios.
