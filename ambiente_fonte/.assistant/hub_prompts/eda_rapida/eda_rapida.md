# Prompt: perfil rápido de dados

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Use **Add context**/`@` para anexar a
> tabela ou o notebook. Skill recomendada: `@hub-ml-eda-profissional`.

Para entender o conceito, as situações adequadas e os riscos do exemplo, consulte o
[README do objeto](README.md). O guia e o bloco colável continuam neste arquivo.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

## Antes de colar

Preencha `{{TABELA_OU_DF}}`, `{{OBJETIVO}}` e `{{FOCO}}`. Informe também o limite
de custo/tempo. Se a tabela não for conhecida, peça primeiro `/findTables`.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{TABELA_OU_DF}}` | Anexe com `@` ou use `catalog.schema.table`. | Ancora o perfil no recurso real. | `@main.crm.clientes` |
| `{{OBJETIVO}}` | Escreva a decisão que o perfil deve apoiar. | Define quais problemas são materiais. | avaliar uso em campanha |
| `{{FOCO}}` | Liste até três dimensões prioritárias. | Evita uma inspeção larga e superficial. | completude, duplicidade, recência |
| `{{PK_OU_NAO_INFORMADO}}` | Informe a chave candidata ou `NÃO INFORMADO`. | Permite medir unicidade e duplicação. | `id_cliente` |
| `{{COL_DATA_OU_NAO_INFORMADO}}` | Informe a data de evento ou referência. | Delimita cobertura e atualidade. | `dt_referencia` |
| `{{FILTROS_OU_NENHUM}}` | Declare população, período e exclusões. | Torna contagens comparáveis. | ativos em 2026; sem teste |
| `{{TEMPO_CUSTO_OU_NAO_INFORMADO}}` | Defina teto de tempo, volume ou ações. | Controla varreduras e coleta no driver. | até 5 min; sem `toPandas()` |

## Prompt pronto para colar

```text
Use @hub-ml-eda-profissional para produzir um perfil rápido, objetivo e
reprodutível do recurso anexado.

CONTEXTO
- Tabela/DataFrame: {{TABELA_OU_DF}}
- Objetivo de negócio: {{OBJETIVO}}
- Foco: {{FOCO}}
- Chave esperada: {{PK_OU_NAO_INFORMADO}}
- Coluna temporal: {{COL_DATA_OU_NAO_INFORMADO}}
- Filtros/período: {{FILTROS_OU_NENHUM}}
- Limite de execução: {{TEMPO_CUSTO_OU_NAO_INFORMADO}}

MODO DE TRABALHO
1. Confirme que o contexto anexado corresponde ao recurso informado; não invente
   catálogo, schema, colunas, tipos nem regras de negócio.
2. Antes de executar, apresente um plano curto e identifique campos ausentes que
   impedem conclusão confiável.
3. Inspecione schema, volume aproximado, completude, cardinalidade, duplicidade da
   chave, período coberto e distribuição das variáveis relevantes.
4. Para alto volume, use agregações PySpark/Spark SQL e uma amostra declarada apenas
   para visualização; evite `toPandas()` irrestrito e varreduras repetidas.
5. Não exiba valores identificáveis. Masque ou agregue PII e sinalize acesso indevido.
6. Não escreva, altere ou apague dados. Solicite confirmação separada caso alguma
   ação mutável se torne necessária.

CONTRATO DE SAÍDA
- Resumo executivo com até 8 achados priorizados.
- Quadro: dimensão verificada, evidência, severidade, impacto e ação sugerida.
- Código PySpark/Spark SQL executável em células pequenas e comentadas, somente se
  solicitado ou autorizado.
- Limitações, pressupostos, custo estimado e checagens que ficaram pendentes.
- Próximos passos, distinguindo correções obrigatórias de investigações opcionais.

VALIDAÇÃO FINAL
- Declare filtros, período, contagens e amostragem realmente usados.
- Diferencie evidência observada de hipótese.
- Confirme que o código não coleta dados em excesso nem altera a origem.
```

## Exemplo mínimo

Tabela = `@main.crm.clientes`; objetivo = avaliar uso em campanha; foco = completude,
duplicidade e recência; chave = `id_cliente`.

## O que conferir na resposta

- O recurso, o período e o grão usados coincidem com o que foi anexado e preenchido.
- Evidência observada está separada de hipótese, default e recomendação.
- Código, execução e escrita estão rotulados sem apresentar proposta como ação realizada.
- Limitações, validações não executadas e decisões pendentes aparecem explicitamente.

## Limites

- Este formulário não concede acesso, permissão de escrita, execução ou deploy.
- Campo ausente deve permanecer `NÃO INFORMADO`; não invente schema ou regra de negócio.
- Resultado material precisa de validação proporcional ao risco e, quando aplicável,
  revisão humana de negócio, Risco, Compliance ou operação.

## Follow-ups úteis

- “Converta os problemas críticos em checks de qualidade sem executar escrita.”
- “Aprofunde somente as três colunas com maior risco.”
- “Compare este perfil com o período anterior e quantifique a mudança.”
