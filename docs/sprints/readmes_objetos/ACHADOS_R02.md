# Achados R02 — documentação dos seis pilotos

Revisão de código, notebook e fontes realizada por ChatGPT, sobre R01
`af1efd14f2a688d3d3cc816ef85f5f1755e8afec`, em 12/09/2026. Autorrevisão técnica
e didática, não auditoria independente. Não houve mudança de algoritmo.

| ID | Objeto | Constatação e evidência | Tratamento nesta sprint |
|---|---|---|---|
| R02-01 | XGBoost | Métricas próximas de dois modelos não excluem vazamento compartilhado; o notebook extrapolava a comparação de uma partição. | Prosa corrigida; métricas históricas preservadas e não recertificadas. |
| R02-02 | XGBoost | `log_mlflow=False` controla logging explícito, não autologging externo; ausência de MLflow com logging habilitado é verificada depois de `fit`. O notebook generalizava falha histórica de configuração para todo serverless Free. | README declara efeito, dependência e momento da falha; notebook delimita a evidência histórica. |
| R02-03 | Isolation Forest | Contaminação numérica define o corte, não garante proporção exata com empates; a ordenação depende dos dados. | Conceito corrigido; teste sintético dedicado no script de evidências. Sem revisão dos rótulos históricos. |
| R02-04 | Isolation Forest | Import de MLflow é obrigatório mesmo com logging falso. `contamination='auto'` não é suportado pelo wrapper completo, embora a biblioteca aceite. | Limites explícitos; não foram usados mocks para simular dependência instalada. |
| R02-05 | Isolation Forest | `stats['score_threshold']` é percentil calculado para diagnóstico; rótulos se relacionam ao corte zero de `decision_function`. `profile_anomalies` usa desvio padronizado global, não atribuição causal/SHAP. | Retorno e interpretação documentados sem prometer explicação causal. |
| R02-06 | Isolation Forest | Default de padronização era descrito como obrigação universal; fraude e anomalia recebiam uma afirmação de baixa interseção sem suporte. | Prosa corrigida; retirada a universalização, mantendo a distinção entre anomalia e fraude. |
| R02-07 | PIT join | Fixture não prova ausência de todo vazamento; filtro em data única não escolhe por si só última versão por chave. Janela limita idade da referência. | Notebook e README delimitam os resultados e a alternativa; implementação preservada. |
| R02-08 | Formatação | Escalas 0.928 e 92.8 diferem por cem, não dez. `fmt_int` usa `.0f`; `fmt_n` converte para float. Ambos perderam uma unidade em 9007199254740993 no teste local. | Prosa corrigida e limite reproduzido; não alterado o cálculo. Não recomendar essas funções para identificadores/precisão arbitrária. |
| R02-09 | Formatação | Texto de unidade desconhecida em `fmt_delta` cai em pp; abreviação pode produzir 1000,0k na fronteira. | Casos de borda documentados e executados; correção funcional exigiria outra tarefa. |
| R02-10 | quick_profile | Fração 1 mantém cardinalidade aproximada, limites de colunas e leituras completas de nulos. Seed tem default 42; sua omissão não significa semente nova a cada chamada. | Prosa corrigida e contrato de alcance explicitado. |
| R02-11 | quick_profile | `top_values_sample` pode expor valores identificáveis; cache/unpersist são efeitos de sessão. Inferência de tipos por substring pode falhar com tipos complexos. | Limites de privacidade, custo e tipos declarados; nenhum acesso a dados reais. |
| R02-12 | eda_rapida | Preparo usa overwrite em tabela persistente; limite de leitura no prompt não protege essa célula. Resposta real permanece não executada. | Avisos antes de executar; bloco colável intacto e sem resposta simulada. |
| R02-13 | eda_rapida | O bloco histórico diz que nenhum job reproduz interação. Documentação atual apresenta tarefa Genie Code para jobs em Beta. | Bloco histórico preservado e contextualizado por nota datada com fonte oficial; tarefa não configurada. |

## Fontes externas e limites

As referências primárias estão junto às afirmações nos seis READMEs. A revisão
consultou documentação oficial de Python, scikit-learn, XGBoost, Apache Spark e
Databricks em 12/09/2026. Página `stable`/`latest` não fixa versão: os metadados
de execução identificam separadamente as bibliotecas efetivamente testadas.

Os achados de código são limites conhecidos e não correções funcionais desta
sprint. O aceite documental não pode ser usado para aprovar esses recursos em
cenários contraindicados, como precisão integral arbitrária ou aprovação
financeira baseada somente em um perfil inicial. Não foi avaliada toda a
biblioteca; o escopo de inspeção aprofundada é o piloto.

## Calibração do template

As quinze perguntas puderam ser preenchidas nos seis objetos sem criar
subseções artificiais. O perfil de formatação tem menos conteúdo que os de
modelagem e integração temporal; não houve quota de palavras. Foram feitas
revisões para retirar repetição e separar conceito, escolha, operação e risco.

Não foi necessária mudança estrutural de template nesta rodada. Mantém-se
`0.1.0-candidata`, para não declarar congelamento editorial antes da avaliação
humana. Os três exemplares da R01 e o checklist continuam referências; nenhum
foi reescrito apenas para demonstrar atividade. Revisão independente e aceite
humano dos textos finais continuam pendentes. R03 não foi iniciada.
