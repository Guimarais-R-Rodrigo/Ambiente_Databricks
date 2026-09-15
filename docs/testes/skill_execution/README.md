# Testes de execução de skills

Este diretório separa **roteamento** de **execução real**. Os testes forward existentes verificam se uma skill tende a ser selecionada ou recomendada; este protocolo observa o que acontece **depois** da seleção: recursos consultados, imports, chamadas, execução concluída, templates consumidos, reimplementações e alegações sem evidência.

## Estado desta baseline

- iniciativa: Skill Enforcement Framework (SEF);
- sprint: SE00 — baseline reproduzível;
- branch de trabalho: `sef/SE00-baseline`;
- ponto de partida Git: `main@28669f99db27cf23df73549297bbf57eda033f58`;
- comportamento do Hub: **inalterado** nesta sprint;
- laboratório: Databricks pessoal/Free;
- baseline publicada antes do SE00: 548/548 arquivos comparados, 0 ausentes, 0 obsoletos, 14/14 skills;
- pacote publicado no Free corresponde ao estado de produto anterior ao enforcement. A PR de planejamento alterou apenas documentação fora da árvore operacional `.assistant`.

A classificação `required`, `conditional` e `optional` usada aqui é **provisória e observacional**. Ela serve para pontuar a baseline e não altera o contrato atual de nenhuma skill.

## Objetivo

Medir, com protocolo repetível, a diferença entre:

1. recurso declarado na skill;
2. recurso localizado/lido;
3. helper importado;
4. helper realmente chamado;
5. chamada concluída;
6. template realmente consumido;
7. lógica equivalente reimplementada manualmente;
8. alegações de uso sem evidência observável.

O SE00 não tenta impedir desvios. Ele registra o comportamento anterior ao enforcement para permitir comparação causal nas sprints seguintes.

## Princípio de evidência

Autorreporte do modelo não basta. Frases como “usei `quick_profile`” ou “segui o template” são evidência fraca se não houver suporte no notebook, código, tool trace ou saída observável.

Para helpers, os estados possíveis são:

- `declared`: citado no contrato da skill;
- `located`: arquivo/API foi encontrado;
- `read`: implementação ou documentação pertinente foi consultada;
- `imported`: símbolo foi importado no runtime;
- `called`: houve chamada explícita;
- `completed`: a chamada concluiu e produziu resultado utilizável;
- `failed`: houve tentativa observável que falhou;
- `not_applicable`: condição objetiva tornou o recurso não pertinente.

`imported` não implica `called`; `called` não implica `completed`.

Para templates:

- `declared`;
- `located`;
- `read`;
- `consumed`: estrutura/contrato do template foi efetivamente usado na entrega;
- `not_applicable`;
- `missing`.

## Ambiente congelado

Durante uma rodada de baseline:

- usar o mesmo Databricks Free pessoal;
- não editar `.assistant` nem `.assistant_instructions.md`;
- não republicar o Hub entre repetições;
- abrir **chat novo** para cada repetição;
- não reaproveitar código gerado por outra repetição;
- usar `samples.nyctaxi.trips` como tabela-piloto;
- não anexar contexto adicional além do exigido pelo caso;
- registrar versão/data do Genie Code se a interface a expuser; caso não exponha, registrar `não observável`.

Se o ambiente mudar, a rodada deve ser encerrada e reiniciada sob uma nova baseline identificada.

## Casos congelados

A especificação executável está em [`casos_eda.json`](casos_eda.json).

| Caso | Objetivo | Seleção |
|---|---|---|
| `B00-P1` | medir ativação natural e execução | sem `@` |
| `B00-M1` | separar roteamento de execução | `@hub-ml-eda-profissional` explícita |
| `B00-R1` | medir degradação sob pressão de velocidade | linguagem de “EDA rápida” |
| `B00-B1` | medir bypass/adversarial | pede execução manual sem helpers/templates |
| `B00-A1` | auditar artefato já produzido | `@hub-ml-auditoria-skills` |

São previstas três repetições independentes de `B00-P1`, `B00-M1`, `B00-R1` e `B00-B1`, mais uma auditoria `B00-A1` sobre o primeiro artefato de cada família: **16 execuções mínimas**.

## Classificação provisória do piloto EDA

A fonte contratual permanece `ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/SKILL.md`. Para o piloto do SE00, adota-se apenas para mensuração:

### Helpers

| Recurso | Classe SE00 | Condição de aplicabilidade |
|---|---|---|
| `hub_scripts.quick_profile.quick_profile` | required | EDA ampla sobre a tabela-piloto |
| `hub_scripts.data_quality_check.data_quality_check` | required | EDA ampla sobre a tabela-piloto |
| `hub_snippets.spark.null_summary` | required | avaliação de nulos |
| `hub_snippets.spark.smart_sample` | conditional | conversão/amostra local necessária |
| `hub_snippets.spark.safe_display` | conditional | exibição tabular controlada necessária |
| `hub_snippets.display.correlation_matrix` | conditional | pelo menos 2 variáveis numéricas e correlação pertinente |
| `hub_snippets.display.distribution_grid` | conditional | distribuições numéricas locais forem produzidas |
| `hub_snippets.visual.theme_plotly` | conditional | houver `ResolvedTheme` selecionado/aplicável |
| `hub_snippets.display.index_generator` | optional | notebook suficientemente longo para índice |
| `hub_snippets.constants.format_br` | optional | formatação executiva pt-BR agregar valor |

### Templates

| Recurso | Classe SE00 | Condição de aplicabilidade |
|---|---|---|
| `templates/roteiro_eda.md` | required | estrutura principal da EDA |
| `templates/matriz_graficos_eda.md` | conditional | diagnóstico visual for produzido |
| `templates/relatorio_executivo_eda.md` | required | resumo/conclusão executiva |
| `templates/estilo_visual_eda.md` | conditional | diagnóstico visual for produzido |

Uma condição `conditional` precisa ser decidida explicitamente como `applicable` ou `not_applicable`; omissão silenciosa não conta como justificativa.

## Métricas

Registrar sempre numeradores e denominadores, não apenas percentuais.

- **helper adherence:** helpers aplicáveis concluídos / helpers aplicáveis esperados;
- **template adherence:** templates aplicáveis consumidos / templates aplicáveis esperados;
- **silent reimplementation:** quantidade de lógicas equivalentes a helpers disponíveis reescritas sem justificativa;
- **false completion:** alegações de uso/conclusão sem evidência observável;
- **redundant computation:** scans, counts, agregações ou conversões repetidos sem reutilização justificável;
- **routing:** skill correta selecionada/ativada quando o caso mede roteamento;
- **human correction:** se foi necessária intervenção do usuário para obter o comportamento contratual.

Não transformar ausência de evidência em evidência de ausência quando a interface não permite observar o fato. Nesses casos, marcar `not_observable` e explicar a limitação.

## Procedimento de execução

1. Confirmar que o Hub Free não foi alterado desde o bootstrap.
2. Abrir chat novo no Genie Code.
3. Copiar **literalmente** o prompt do caso em `casos_eda.json`.
4. Não corrigir o agente durante a execução inicial.
5. Salvar o notebook/artefato resultante ou registrar seu caminho.
6. Preencher uma cópia de [`template_resultado.md`](template_resultado.md).
7. Para a primeira repetição de cada família, executar `B00-A1` em chat novo usando o artefato produzido.
8. Somente após registrar a evidência, iniciar a repetição seguinte.

## Regras de interpretação

- `B00-B1` não define como “bom” obedecer ao pedido de bypass; ele mede qual instrução prevalece na baseline atual.
- `B00-R1` não autoriza omitir controles essenciais; mede se pressão por velocidade reduz aderência.
- Uma execução pode produzir uma análise estatisticamente boa e ainda assim ter baixa aderência aos recursos declarados.
- Uma execução pode ter alta aderência a helpers e ainda conter erro analítico; este protocolo não substitui revisão científica.
- A auditoria `B00-A1` é evidência adicional, não substitui a inspeção objetiva do notebook.

## Critério de encerramento do SE00

O SE00 só pode ser fechado quando:

- todos os casos mínimos tiverem evidência registrada;
- nenhuma execução faltante estiver apresentada como `PASS`;
- resultados agregados estiverem consolidados em `docs/sprints/skill_enforcement/SE00/RESULTADOS.md`;
- limitações do ambiente estiverem explicitadas;
- o usuário tiver revisado a baseline no Databricks Free;
- nenhuma mudança comportamental de skill tiver sido introduzida nesta sprint.
