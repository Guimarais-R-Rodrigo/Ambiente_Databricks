# SER02 — hub-ml-explainability

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L3**, `stage_specific`.

## 1. Objetivo e superfície

Vincular modelo, features, linhas efetivamente explicadas, método e output a uma computação canônica verificável. A interpretação continua metodológica; importância não é causalidade nem demonstra fairness.

Superfícies: model_and_dataset_binding (L2); explanation_computation (L3).

## 2. Reuso e inventário de autoria

A matriz SER00 identifica hub_snippets.ml.shap_explainer: compute_shap, get_feature_importance_shap e plots. A fachada __init__.py foi conferida nesta elaboração. Assinaturas, versões e efeitos precisam ser fixados em B1; ml.explainability_report permanece candidato de reuso, não API assumida.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Identidade/hash do modelo; tarefa e classe/output; método; features ordenadas/dtypes; linhas e ordem do dataset; background; regra e seed de amostragem; output esperado; política de persistência; versões de biblioteca.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

Preflight estruturado; amostra efetiva identificada; argumentos de chamada; shape/valores SHAP/base; versão do método; Receipt ligado a modelo/amostra/output; verifier de integridade e coerência; efeitos de arquivo registrados quando autorizados.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

EX-B01: estratégia para subamostragem Kernel deve impedir nova seleção silenciosa ou retornar os IDs efetivos. Sem isso, bloquear Kernel no escopo candidato, não alegar explicação da população inteira. EX-B02: fechar catálogo por método/output e rejeitar método não suportado. Resolver por inspeção e teste repo-side, não pelo executor.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta EX-F01: modelo linear f(x)=3+2*x1-x2, background de referência [0,0], duas linhas [1,2] e [2,1]. Oráculo analítico: base 3, contribuições [2,-2] e [4,-1], predições 3 e 6. Só usar como oráculo de um método cuja semântica coincida com essa referência; não generalizar para background/método diferentes. Tolerância inicial de desenho para método linear exato: atol=1e-10, rtol=1e-10, a validar e congelar antes da campanha. Kernel aproximado precisa de perfil próprio; não aumentar tolerância após FAIL.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| EX01 | Positivo analítico | Executar rota pública. | Valores/base/shape/linhas correspondem ao oráculo; execução registrada. |
| EX02 | Schema de features | Remover, acrescentar ou permutar feature sem contrato. | Recusar incompatibilidade; não reordenar silenciosamente. |
| EX03 | Compatibilidade método/modelo | Pedir método incompatível ou não aprovado. | Bloquear antes da computação. |
| EX04 | Output multiclasses | Omitir classe/output_index ou fornecer índice inválido. | Exigir seleção inequívoca; nenhuma agregação implícita. |
| EX05 | Linhas efetivas | Receipt declara toda a base em vez da amostra. | Verifier rejeita overclaim. |
| EX06 | Subsample escondida | Helper volta a subamostrar internamente sem identidade. | Bloquear método ou demonstrar IDs efetivos; nunca supor igualdade. |
| EX07 | Dependência necessária | SHAP indisponível/incompatível. | Sem resultado inventado; efeito nenhum. |
| EX08 | Chamada/saída parcial | Omitir call ou trocar shape/inserir NaN indevido. | Runner/verifier recusam prova incompleta. |
| EX09 | Replay de contexto | Reusar Receipt trocando um binding de cada vez. | Todos os bindings materiais detectados. |
| EX10 | Arquivo não autorizado | Acionar save de gráfico. | Persistência bloqueada; paths protegidos íntegros. |
| EX11 | Interpretação sem autoridade | Solicitar conclusão causal/fairness. | Resposta delimita o que não foi demonstrado. |
| EX12 | Mutante de sinal/ordem | Trocar colunas de contribuição ou sinal. | Oráculo independente reprova mesmo com shape válido. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Modelo sintético e dependências qualificadas; não depende da promoção de baseline-ML. Plots/salvamento ficam fora do positivo mínimo e entram como perfil de efeito separado. As famílias transversal/Receipt são obrigatórias e o negativo precisa alcançar o verifier/call pertinente.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Executar fixture numérica pequena no runtime com a mesma lista de features e método aprovado. Registrar dependências reais e comparar valores/shape/IDs. Importar SHAP sem computar não prova execução. Ausência de dependência é BLOCKED_ENVIRONMENT, não PASS de portabilidade.

Roteiro Genie mínimo: EX-G01, EX-G02, EX-G03, EX-G04, EX-G05, EX-G06, EX-G07, EX-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não promove geração universal de relatórios, suporte a qualquer modelo, causalidade, fairness ou persistência arbitrária. Um método bloqueado precisa aparecer nominalmente na matriz de capacidades e no resumo de promoção.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.
