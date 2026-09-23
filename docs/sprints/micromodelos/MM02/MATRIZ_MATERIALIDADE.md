# MM02 — matriz de materialidade do spec fingerprint

## Regra de leitura

Esta matriz é a autoridade documental da MM02 para o algoritmo `mm02-spec-fingerprint-v1`.

Classificações:

- **MATERIAL** — mudança válida altera o fingerprint;
- **EDITORIAL_CANONICALIZED** — entra após canonicalização editorial MM01;
- **CONDITIONAL_MATERIAL** — entra somente quando o próprio contrato MM01 diz que o campo define uma regra customizada;
- **AUDIT_TRAIL** — prova/origem/decisão; não entra;
- **LIFECYCLE** — estado do artefato/processo; não entra;
- **NARRATIVE** — prosa auxiliar sem efeito analítico; não entra.

O documento completo precisa ser válido segundo MM01 antes de a matriz ser aplicada.

## Matriz

| Caminho | Classe | Regra v1 |
|---|---|---|
| `schema_version` | MATERIAL | entra exato |
| `identidade.nome` | LIFECYCLE | não entra; identidade humana é transportada separadamente |
| `identidade.titulo` | NARRATIVE | não entra |
| `identidade.micromodel_version` | LIFECYCLE | não entra |
| `identidade.estado.*` | LIFECYCLE | não entra |
| `negocio.caracteristica` | EDITORIAL_CANONICALIZED | entra |
| `negocio.objetivo` | NARRATIVE | não entra |
| `negocio.definicao_operacional` | EDITORIAL_CANONICALIZED | entra |
| `negocio.uso_pretendido[]` | EDITORIAL_CANONICALIZED | entra como conjunto deduplicado e ordenado canonicamente |
| `negocio.nao_usar_para[]` | EDITORIAL_CANONICALIZED | entra como conjunto deduplicado e ordenado canonicamente |
| `entidade.tipo` | EDITORIAL_CANONICALIZED | entra |
| `entidade.chave_logica` | MATERIAL | entra exato |
| `entidade.granularidade` | EDITORIAL_CANONICALIZED | entra |
| `entidade.populacao_elegivel` | EDITORIAL_CANONICALIZED | entra |
| `entidade.referencia_temporal` | EDITORIAL_CANONICALIZED | entra |
| `fontes[].id` | MATERIAL | entra; estabiliza referências internas |
| `fontes[].catalogo_ref` | MATERIAL | entra exato |
| `fontes[].schema` | MATERIAL | entra exato |
| `fontes[].objeto` | MATERIAL | entra exato |
| `fontes[].tipo_objeto` | MATERIAL | entra exato |
| `fontes[].campos[]` | MATERIAL | entra como conjunto ordenado canonicamente |
| `fontes[].papel` | MATERIAL | entra |
| `fontes[].proveniencia` | AUDIT_TRAIL | não entra |
| `evidencias[].id` | MATERIAL | entra |
| `evidencias[].descricao` | NARRATIVE | não entra |
| `evidencias[].fontes_ref[]` | MATERIAL | entra ordenado |
| `evidencias[].regra` | EDITORIAL_CANONICALIZED | entra |
| `evidencias[].proveniencia` | AUDIT_TRAIL | não entra |
| `contra_evidencias[].id` | MATERIAL | entra |
| `contra_evidencias[].descricao` | NARRATIVE | não entra |
| `contra_evidencias[].fontes_ref[]` | MATERIAL | entra ordenado |
| `contra_evidencias[].regra` | EDITORIAL_CANONICALIZED | entra |
| `contra_evidencias[].proveniencia` | AUDIT_TRAIL | não entra |
| `classificacao.tipo` | MATERIAL | entra |
| `classificacao.semantica.quando_*` | EDITORIAL_CANONICALIZED | entram |
| `classificacao.semantica.proveniencia` | AUDIT_TRAIL | não entra |
| `classificacao.ausencia_evidencia.tratamento` | MATERIAL | entra |
| `classificacao.ausencia_evidencia.resultado_sem_evidencia` | MATERIAL | entra |
| `classificacao.ausencia_evidencia.regra_ref` | MATERIAL | entra quando presente |
| `classificacao.ausencia_evidencia.proveniencia` | AUDIT_TRAIL | não entra |
| `classificacao.limiares[].id` | MATERIAL | entra |
| `classificacao.limiares[].descricao` | NARRATIVE | não entra |
| `classificacao.limiares[].operador` | MATERIAL | entra |
| `classificacao.limiares[].valor` | MATERIAL | entra como número canônico |
| `classificacao.limiares[].unidade` | MATERIAL | entra exato |
| `classificacao.limiares[].proveniencia` | AUDIT_TRAIL | não entra |
| `score.habilitado` | MATERIAL | entra |
| `score.tipo_semantica` | MATERIAL | entra |
| `score.semantica_ref` | CONDITIONAL_MATERIAL | entra somente para `OUTRA_APROVADA`; nos tipos estruturados é audit trail |
| `score.escala.min/max` | MATERIAL | entram como números canônicos |
| `score.normalizacao.metodo` | MATERIAL | entra |
| `score.normalizacao.referencia` | CONDITIONAL_MATERIAL | entra somente para `CUSTOM_APROVADO` |
| `score.normalizacao.proveniencia` | AUDIT_TRAIL | não entra |
| `score.componentes[].id` | MATERIAL | entra |
| `score.componentes[].descricao` | NARRATIVE | não entra |
| `score.componentes[].peso` | MATERIAL | entra como número canônico |
| `score.componentes[].proveniencia` | AUDIT_TRAIL | não entra |
| `score.calibracao.metodo` | EDITORIAL_CANONICALIZED | entra quando calibração existe |
| `score.calibracao.evidencia_ref` | MATERIAL | entra como ID da calibração escolhida |
| `score.calibracao.proveniencia` | AUDIT_TRAIL | não entra |
| `score.proveniencia` | AUDIT_TRAIL | não entra |
| `experimentos[]` | AUDIT_TRAIL | conteúdo observado não entra; ID pode ser referenciado materialmente por calibração |
| `validacao.*` | AUDIT_TRAIL | não entra |
| `saida.estudo.campo_classificacao` | MATERIAL | entra exato |
| `saida.estudo.valores_classificacao` | MATERIAL | entra na ordem contratual |
| `saida.estudo.campo_score` | MATERIAL | entra exato/null |
| `saida.publicacao.estado` | LIFECYCLE | não entra |
| `saida.publicacao.campo_booleano` | MATERIAL | entra quando definido |
| `saida.publicacao.politica_indeterminado.tratamento` | MATERIAL | entra quando definida |
| `saida.publicacao.politica_indeterminado.indeterminado_vira_false` | MATERIAL | entra |
| `saida.publicacao.politica_indeterminado.regra_ref` | MATERIAL | entra |
| `saida.publicacao.politica_indeterminado.proveniencia` | AUDIT_TRAIL | não entra |
| `tracking.*` | LIFECYCLE | não entra; integração futura MM06 |
| `governanca.*` | LIFECYCLE | não entra |
| `publicacao.*` | LIFECYCLE | estado/handoff institucional não entra |
| `proveniencia.*` | AUDIT_TRAIL | não entra |

## Invariantes

1. `spec_fingerprint` identifica conteúdo analítico, não o nome do artefato.
2. aprovação ou nova execução não mudam identidade se a definição não mudou.
3. evidência observada pode evoluir sem alterar a definição que ela testa.
4. alterar regra, população, fonte, janela, peso, threshold, missing, semântica, normalização customizada, calibração escolhida ou saída altera identidade.
5. canonicalização editorial nunca equivale a inferência semântica geral.
6. pontuação inicial/interna, operadores e diacríticos potencialmente semânticos continuam preservados pela autoridade MM01.
7. nenhuma referência é descartada apenas por “parecer metadata”: a classe depende da função contratual do campo.
8. qualquer mudança desta matriz após V1 do algoritmo exige nova versão do algoritmo se puder alterar o preimage de uma especificação válida.

## Casos deliberadamente conservadores

IDs internos de fontes, evidências, contra-evidências, limiares e componentes entram no fingerprint. Embora alguns renames possam ser editorialmente motivados, esses IDs estabilizam a topologia referencial da especificação e podem ser consumidos por artefatos posteriores. A MM02 v1 não tenta provar equivalência de grafos após renomeação.

Essa escolha pode ser revisada apenas por mudança explícita de versão do algoritmo; não por normalização implícita.
