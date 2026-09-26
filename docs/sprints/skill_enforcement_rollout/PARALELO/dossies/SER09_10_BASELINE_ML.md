# SER09 / SER10 — hub-ml-baseline-ml

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Provar split, preprocessing, treino e tracking realmente vinculados, sem impor algoritmo universal nem permitir promoção automática de modelo.

Superfícies: split_without_leakage (L3); training_and_tracking (L4); contexto L2 é marco anterior.

## 2. Reuso e inventário de autoria

Reuso candidato: temporal_split; run_governado; walk_forward; wrappers e metrics_report. A matriz adverte que textos dataset/split no MLflow não provam que o modelo usou aqueles objetos; não importar _RunGovernado como API pública.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Tarefa/target/classe/unidade; cutoffs/horizonte; grupo e split; holdout; features/ordem; preprocessing/fit; modelo/params/seed; métricas; destino tracking; assinatura e artefatos requeridos; limites e autorizações.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: contexto e split planejado. L4: índices reais de treino/teste/holdout, parâmetros ajustados no treino, modelo e métricas, run_id efetivo, hashes/uris verificáveis dos artefatos, Receipt e Postflight com leitura do run.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

BM-B01: catálogo de tarefas/modelos mínimo é fechado repo-side depois de verificar wrappers; não supor todas as bibliotecas instaladas. BM-B02: validar capacidades de tracking no Free antes de efeito. BM-B03: definir verificação do run/assinatura e política de resíduos em erro.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta BM-F01: IDs 1..12, data crescente, treino 1..6, validação 7..9, holdout 10..12 com cutoffs expressos; grupos não podem atravessar partições quando o contrato exigir group split. Mutante introduz ID 10 no fit ou atributo aprendido com holdout. Não exigir métrica arbitrária 100%: o oráculo central é identidade/isolamento, e o resultado numérico depende do algoritmo e da fixture congelados. Tracking local e remoto têm provas separadas.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| BM01 | Split disjunto | Introduzir ID/grupo cruzando partições. | Recusar split não conforme. |
| BM02 | Fit train-only | Fit com teste/holdout. | Proveniência/parâmetros detectam leakage. |
| BM03 | Target/output | Omitir classe positiva/output ou trocar target. | Bloquear contexto ambíguo. |
| BM04 | Parâmetros reais | Registrar params diferentes da chamada. | Receipt/MLflow consistency falha. |
| BM05 | Texto sem binding | Manter descrição textual do correto e treinar no errado. | Prova não aceita só pelo texto. |
| BM06 | Tracking falha | Erro antes/depois de log_model. | Estado/efeito preservados; sem false completion. |
| BM07 | Artefato divergente | URI/hash aponta para B ou não existe. | Postflight reprova. |
| BM08 | Assinatura obrigatória | Omitir/incompatibilizar input/output schema. | Não concluir registro válido. |
| BM09 | Treino interrompido | Helper falha ou processo cancela. | Nenhum registro COMPLETED falso. |
| BM10 | Promoção automática | Solicitar/acionar alias promoção sem autorização. | Bloquear efeito fora do escopo. |
| BM11 | Holdout reutilizado | Escolher parâmetros após ler sua métrica. | Auditoria detecta violação de plano; não alegar teste intacto. |
| BM12 | Fixture independente | Criar dependência circular EX↔BM no DAG. | Validador do grafo recusa ciclo; fixture pré-treinada mantém independência. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Treino mínimo na biblioteca aprovada; split/fit observados; MLflow temporário local quando suportado. Regressões de algoritmo apenas no escopo escolhido. Falha externa não se resolve criando run substituto automaticamente.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Modelo sintético mínimo, run real em experimento pessoal explícito; conferir existência/estado/params/assinatura/artefato por leitura após execução. Não usar modelo de produção nem alias operacional. Falha pode deixar run aberto/artefato parcial e precisa de ledger.

Roteiro Genie mínimo: BM-G01, BM-G02, BM-G03, BM-G04, BM-G05, BM-G06, BM-G07, BM-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não prova seleção ótima de algoritmo, generalização econômica, deploy ou promoção de registry. Benchmark não substitui prova de ausência de leakage. Nenhum retreino automático decorre desta campanha.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.
