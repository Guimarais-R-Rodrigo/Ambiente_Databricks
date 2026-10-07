# MT14 Mapa dos novos executores B1

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt14-b1-code-map"></a>
<a id="mt14-b1-code-map"></a>
### MT14 Mapa dos novos executores B1

Como saber se uma resposta calculou alguma coisa, apenas conferiu um pedido ou deixou um efeito no ambiente? Os arquivos deste apêndice tornam essa pergunta verificável. Eles complementam o [mapa do núcleo](MT-mt14-enforcement-code-map.md#mt14-enforcement-code-map): aqui estão as novas rotas de baseline, cruzamento, explicabilidade, features, monitoramento, pipeline e validação estatística. A leitura pressupõe a diferença entre contrato e instância, desenvolvida em [MT15](MT-parte-iv.md#mt15-1), e entre preflight, Receipt e Postflight, explicada em [MT17](MT-parte-iv.md#mt17-1), [MT18](MT-parte-iv.md#mt18-1) e [MT19](MT-parte-iv.md#mt19-1). O [mapa de campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map) mostra os documentos que essas funções recebem ou consultam.

Um preflight é a conferência anterior à operação. Ele recusa pedidos fora do perfil, resolve recursos e registra o que foi declarado. Um runner executa a rotina permitida e produz resultado acompanhado de rastros. Um verifier confronta esse conjunto com entradas esperadas mantidas separadamente. Essa separação é importante: conferir um resultado contra uma cópia de si mesmo não testa sua correção. Em várias rotas o verifier recalcula um oráculo, isto é, um resultado esperado por caminho diferente; em outras exige que o chamador forneça esse oráculo. As fichas deixam explícita essa responsabilidade, porque o prefixo verify não torna automaticamente uma conferência independente.

Considere o baseline mensal. O pedido informa linhas, datas, feature e classe. O preflight exige condições mais estreitas que a descrição geral de aprendizado de máquina: meses únicos, split fixo e duas classes em cada partição. O runner ajusta o scaler e a regressão apenas no treino, mede validação e holdout e registra quais IDs participaram. O verifier reconstrói as divisões e refaz o ajuste. Esse trabalho custa processamento e pode alterar o autolog da sessão para desativado. Portanto, verificar não é necessariamente uma operação sem dependências ou sem mudanças de sessão, ainda que não publique resultados remotos.

O Receipt é um comprovante estruturado que liga pedido, execução, resultado e release. Seu digest detecta mudanças no corpo ao qual está vinculado; não autentica a pessoa, não demonstra a origem sintética dos dados e não concede permissão para escrever. A release é o conjunto exato de arquivos esperado pelo runner. Conferi-la antes e depois ajuda a detectar troca de código durante a operação. Uma dependência faltante ou origem de importação divergente deve resultar em bloqueio; não é motivo para instalar bibliotecas silenciosamente ou usar outra implementação apenas para obter PASS.

O mesmo cuidado vale para efeitos. A computação local do Pipeline cria uma view temporária e a remove. Sua flag de ausência de escrita significa ausência de persistência, não ausência de atividade Spark. A rota Delta, por outro lado, cria uma tabela, realiza MERGE, repete a operação para verificar idempotência e tenta remover somente o alvo cuja propriedade confirmou. Se a criação foi tentada e a limpeza não ficou comprovada, UNKNOWN conserva a incerteza. Repetir a escrita nesse estado pode agravar um resíduo; a próxima ação é conferir o alvo e o registro existente no ambiente autorizado.

A composição de features ilustra outra fronteira. Primeiro executa e finaliza o cruzamento disponível no instante de decisão, chamado PIT, de point-in-time. Depois projeta as linhas verificadas. Essa projeção conserva os identificadores do Receipt e do Postflight upstream, mas não fabrica um Receipt próprio da Feature Engineering. A materialização é uma terceira rota, com autorização externa e efeito separado. Já Micromodelos aparece somente no mapa de campos: seu contrato L1/audit descreve invariantes estáticas e runtime_gate=false, sem integrar este conjunto de runners protegidos.

Nas assinaturas, argumentos após o asterisco são nomeados obrigatoriamente. None como default significa opção implementada, não ausência de validação; vários runners geram um identificador único quando run_id não é fornecido. Nomes iniciados por sublinhado são auxiliares internos, documentados para manutenção, sem promessa de interface pública estável. As tabelas de retorno indicam o envelope realmente produzido e as de erros conservam códigos do código-fonte. As listas de imports mostram dependências diretas; bibliotecas transitivas dos helpers continuam exigindo conferência do objeto correspondente.

O [owner SER](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/skill_enforcement_rollout/README.md) registra o escopo técnico A de B1 integrado e aceito; isso não promove as skills, mantidas na [policy](../../hub_padroes/skill_enforcement/policy.json) majoritariamente L0/audit, nem comprova orquestração Genie global ou homologação corporativa. Os exemplos das fichas são ilustrativos por inspeção de código, não execuções desta edição. Para conferir a leitura, escolha uma rota e identifique pedido externo, primitive, retorno, efeito e verificador final. Se qualquer elo faltar, registre exatamente essa pendência. A próxima leitura é o contrato específico, seguida da policy corrente e da evidência datada do ambiente em que uma execução futura estiver autorizada.

<a id="mt14-b1-code-map-file-001"></a>
#### hub-ml-baseline-ml/scripts/preflight.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-baseline-ml/scripts/preflight.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-baseline-ml/scripts/preflight.py`; SHA-256 `7ef329053d9a84b55f4a7f261a4d29a6fd08ddc47565370d3fad6cca666e3c52`; lote B1-01. |
| Por que existe | Fixar um baseline binário temporal reproduzível antes de importar o treino. |
| Entradas e preparação | Pedido SER09-REQUEST-1; uma feature; seed 17; threshold 0,5; M; gap 0. Tipos dos valores fixos são exatos, sem bool como inteiro. |
| Mecanismo interno | Fecha as chaves; exige pelo menos 12 meses únicos, no primeiro dia à meia-noite UTC, IDs únicos, feature finita em ±1e9 e target inteiro 0/1. Ordena os meses; calcula tamanhos inteiros 50%/25% e restante; exige ambas as classes em cada partição. Preflight resolve temporal_split e metrics_report e vincula contrato/código por blob. |
| Retorno e interpretação | validate_request: status, issues, profile, request_sha256, partitions_expected ou null; preflight soma sef e, quando disponível, release_bindings. |
| Dependências diretas | from __future__ import annotations; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, integer, text, utc_instant; from hub_scripts.skill_execution.domain_context.release import blob; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-003); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leitura de contrato/bytes locais e resolução estática; nenhum treino, escrita persistente ou chamada analítica. |
| Consumidor/leitor | run._execute, verify.verify e a rota de tracking. |
| Limites e custo | Datas são validadas em UTC; 12 linhas por si não garantem duas classes em cada divisão. A declaração synthetic não prova origem real dos dados. |
| Exemplo e contraexemplo | Ilustrativo: 12 meses únicos com classes alternadas satisfazem a condição das partições; dois registros no mesmo mês provocam ROW:DUPLICATE_MONTH. |
| Exceções e falhas levantadas | ContextError('PARTITION:BOTH_CLASSES_REQUIRED:' + label); ContextError('PROFILE:UNSUPPORTED:' + key); ContextError('REQUEST:SYNTHETIC_NO_EFFECT_ONLY'); ContextError('REQUEST:UNSUPPORTED_PROFILE'); ContextError('ROW:BINARY_TARGET_REQUIRED'); ContextError('ROW:DUPLICATE_ID'); ContextError('ROW:DUPLICATE_MONTH'); ContextError('ROW:FINITE_FEATURE_REQUIRED'); ContextError('ROW:MONTH_START_REQUIRED'); ContextError('ROWS:AT_LEAST_12_REQUIRED'); RuntimeError('SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH') |
| Captura implementada | (ContextError, KeyError, TypeError, ValueError, OverflowError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: validate_request, preflight. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `validate_request(request: object) -> dict` (linhas 21–71) | Fecha as chaves; exige pelo menos 12 meses únicos, no primeiro dia à meia-noite UTC, IDs únicos, feature finita em ±1e9 e target inteiro 0/1. Ordena os meses; calcula tamanhos inteiros 50%/25% e restante; exige ambas as classes em cada partição. Retorno: dict de decisão de domínio, com status PASS/BLOCKED, issues, digest e campos específicos da ficha. |
| `preflight(request: object) -> dict` (linhas 74–90) | Chama validate_request; em PASS resolve contrato por run_preflight, confere origem e registra bindings locais; devolve BLOCKED se domínio ou resolução falharem. Retorno: dict de decisão anterior à execução e bindings/SEF específicos da ficha; sem resultado analítico. |

<a id="mt14-b1-code-map-file-002"></a>
#### hub-ml-baseline-ml/scripts/run.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-baseline-ml/scripts/run.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-baseline-ml/scripts/run.py`; SHA-256 `2864a3747ee4ebba9ec4933db98351fe5546a959b247f3da0fcbca0f47a0df2f`; lote B1-01. |
| Por que existe | Treinar e medir um baseline sintético com evidência de chamada e ajuste restrito ao treino. |
| Entradas e preparação | Pedido validado e run_id opcional; ausência gera UUID. _execute também conserva o objeto Pipeline usado no cálculo. |
| Mecanismo interno | Confere fileset/release, preflight e origem dos helpers. Cria DataFrame pandas; usa temporal_split; compara IDs; desativa autolog; ajusta StandardScaler e LogisticRegression(max_iter=1000) apenas no treino. Mede AUC/Brier nas três partições, grava parâmetros do modelo no resultado, reconfere release e emite Receipt. |
| Retorno e interpretação | _execute retorna (payload, modelo) ou (BLOCKED, None); run expõe só payload. Resultado contém partições, scores, métricas, estatísticas do scaler, coeficiente, intercepto e fit_partition_sha256. |
| Dependências diretas | from __future__ import annotations; import importlib; import json; import sys; import uuid; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, loads_strict; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; import argparse; import mlflow; import mlflow.sklearn; import pandas as pd; from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.linear_model import LogisticRegression; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-003); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Treino/arrays em memória; se MLflow estiver disponível, altera autolog da sessão para desativado. Uma run MLflow ativa é recusada; nenhuma run remota é criada aqui. |
| Consumidor/leitor | verify.py e run_tracking.py, que usa o mesmo modelo retornado por _execute. |
| Limites e custo | Uma feature, classificação binária mensal, split fixo; não seleciona modelo de negócio. Importar não treina; chamar verify também pode refazer o ajuste. |
| Exemplo e contraexemplo | Ilustrativo: run(request, run_id="exemplo-local") produz envelope verificável se dependências e release forem válidas; run_id vazio bloqueia antes do treino. |
| Exceções e falhas levantadas | RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH'); RuntimeError('RELEASE_CHANGED_DURING_EXECUTION'); RuntimeError('SPLIT_PARTITION_BINDING_MISMATCH'); SystemExit(0 if payload['status'] == 'PASS' else 1); ValueError('EXISTING_ACTIVE_MLFLOW_RUN_NOT_OWNED'); ValueError('RUN_ID_REQUIRED') |
| Captura implementada | Exception; ImportError; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: run. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_canonical(module_name: str, symbol: str, implementation: str)` (linhas 37–44) | Importa módulo canônico e recusa origem de fachada/implementação divergente; devolve helper ou helpers originais. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_disable_autolog_before_fit() -> None` (linhas 47–60) | Retorna None após desativar autolog quando MLflow existe; sem MLflow retorna normalmente; run ativa gera ValueError em vez de alterar trabalho alheio. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_execute(request: object, *, run_id: str \| None=None) -> tuple[dict, object \| None]` (linhas 63–152) | Confere fileset/release, preflight e origem dos helpers. Cria DataFrame pandas; usa temporal_split; compara IDs; desativa autolog; ajusta StandardScaler e LogisticRegression(max_iter=1000) apenas no treino. Mede AUC/Brier nas três partições, grava parâmetros do modelo no resultado, reconfere release e emite Receipt. Retorno: tuple(payload, modelo) ou (payload BLOCKED, None); modelo exato fica disponível à rota de tracking. |
| `run(request: object, *, run_id: str \| None=None) -> dict` (linhas 155–157) | Confere fileset/release, preflight e origem dos helpers. Cria DataFrame pandas; usa temporal_split; compara IDs; desativa autolog; ajusta StandardScaler e LogisticRegression(max_iter=1000) apenas no treino. Mede AUC/Brier nas três partições, grava parâmetros do modelo no resultado, reconfere release e emite Receipt. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |

| Interface de linha de comando | Contrato |
|---|---|
| Flag declarada | `parser.add_argument('--request', required=True, type=Path)` |
| Flag declarada | `parser.add_argument('--run-id', required=True)` |
| Saída | JSON em stdout; exit code do estado calculado. Parsing da CLI pode encerrar com erro antes da lógica. Nenhuma CLI foi executada nesta edição. |

<a id="mt14-b1-code-map-file-003"></a>
#### hub-ml-baseline-ml/scripts/run_tracking.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-baseline-ml/scripts/run_tracking.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-baseline-ml/scripts/run_tracking.py`; SHA-256 `48591413936233c4c69445de998a16bad11b4f7ae4c82f6fe4a39abda5850b2b`; lote B1-01. |
| Por que existe | Exercitar tracking MLflow efêmero pessoal do modelo exato calculado, com autorização externa vinculada. |
| Entradas e preparação | request, authorization SER10-AUTH-1, spark e run_id obrigatório; autorização inclui target_experiment, current_user, digest, retention e authorization_id. |
| Mecanismo interno | Copia JSON recusando ciclos/chaves não string; consulta current_user; valida autorização, namespace pessoal novo e request/run. Exige tracking URI databricks, ausência de run ativa e experimento inexistente. Computa/verifica o baseline; cria experimento/run pelo helper governado, registra modelo/assinatura/exemplo, relê conteúdo e predições, chama verify_live, então tenta soft delete de run e experimento com readback. |
| Retorno e interpretação | Payload status/compute/effect/issues/tracking_receipt=null/promotion_authorized=false. PASS exige verificação live válida, ausência de issues e ambos soft-deleted. |
| Dependências diretas | from __future__ import annotations; import importlib; import json; import math; import re; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, loads_strict; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution import run_preflight; import mlflow; import mlflow.sklearn; from pandas import DataFrame; import numpy as np |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-003); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | SQL de identidade, chamadas remotas MLflow, criação e soft delete autorizados, leitura de modelo remoto e alteração de autolog. Efeito não é protegido apenas pelo Receipt de computação. |
| Consumidor/leitor | Operador autorizado; verify_tracking.verify_live durante a run e verify_finalized após limpeza. |
| Limites e custo | Não autentica a pessoa que forneceu a autorização; não usa Registry ou deploy. Timeout após criar sem ID gera UNKNOWN_RESIDUE; jamais presumir que nada foi criado. |
| Exemplo e contraexemplo | Ilustrativo: autorização para outro digest falha AUTH_BINDING_MISMATCH; experimento já existente é recusado em vez de reutilizado. |
| Exceções e falhas levantadas | RuntimeError('EXPERIMENT_SOFT_DELETE_READBACK_MISMATCH'); RuntimeError('HELPER_DID_NOT_CREATE_RUN'); RuntimeError('HELPER_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('HELPER_IMPORT_ORIGIN_MISMATCH'); RuntimeError('INDEPENDENT_LIVE_VERIFICATION_FAILED'); RuntimeError('MODEL_PREDICTION_READBACK_MISMATCH'); RuntimeError('MODEL_SIGNATURE_OR_EXAMPLE_MISSING'); RuntimeError('RELEASE_CHANGED_AFTER_EFFECT'); RuntimeError('RELEASE_CHANGED_BEFORE_EFFECT'); RuntimeError('RUN_READBACK_MISMATCH'); RuntimeError('RUN_SOFT_DELETE_READBACK_MISMATCH'); ValueError('AUTHENTICATED_USER_INVALID'); ValueError('AUTH_BINDING_MISMATCH'); ValueError('AUTH_RECORD_SHAPE_INVALID'); ValueError('BASELINE_COMPUTE_BLOCKED'); ValueError('BASELINE_COMPUTE_VERIFICATION_FAILED'); ValueError('EXISTING_ACTIVE_RUN_NOT_OWNED'); ValueError('EXPERIMENT_ALREADY_EXISTS_NOT_OWNED'); ValueError('EXPLICIT_DATABRICKS_TRACKING_URI_REQUIRED'); ValueError('RUN_ID_REQUIRED'); ValueError('SNAPSHOT_CYCLE'); ValueError('SNAPSHOT_NONSTRING_KEY'); ValueError('SNAPSHOT_NON_JSON_VALUE'); ValueError('TARGET_NOT_FRESH_PERSONAL_NAMESPACE'); ValueError('TRACKING_CONTRACT_BLOCKED') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: run_tracking. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_snapshot(value: object) -> object` (linhas 23–46) | Serializa e relê JSON para desligar referências mutáveis do chamador; devolve cópia, recusando valores não representáveis. A variante de tracking também verifica ciclos e chaves explicitamente. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_helper()` (linhas 49–58) | Resolve run_governado e confere a origem da função decorada via __wrapped__; devolve context manager callable. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_identity(spark) -> str` (linhas 61–65) | Consulta current_user() pelo Spark, recusa nome vazio ou com separadores e devolve string autenticada no runtime. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_authorize(request: object, authorization: object, *, run_id: str, user: str) -> str` (linhas 68–88) | Confere todos os campos da autorização externa contra request/run/usuário e namespace pessoal; devolve target_experiment ou lança ValueError. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `run_tracking(request: object, authorization: object, spark, *, run_id: str) -> dict` (linhas 91–276) | Copia JSON recusando ciclos/chaves não string; consulta current_user; valida autorização, namespace pessoal novo e request/run. Exige tracking URI databricks, ausência de run ativa e experimento inexistente. Computa/verifica o baseline; cria experimento/run pelo helper governado, registra modelo/assinatura/exemplo, relê conteúdo e predições, chama verify_live, então tenta soft delete de run e experimento com readback. Retorno: dict status/issues/compute/effect/tracking_receipt(null)/promotion_authorized(false), após tentativa de limpeza. |

<a id="mt14-b1-code-map-file-004"></a>
#### hub-ml-baseline-ml/scripts/verify.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-baseline-ml/scripts/verify.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-baseline-ml/scripts/verify.py`; SHA-256 `cefe5f9126c50c6918d61f49d288a570e89328458bc9368ef7a2e79b5d09434a`; lote B1-01. |
| Por que existe | Conferir baseline contra pedido independente, treino reproduzido e release atual. |
| Entradas e preparação | payload, expected_request e expected_run_id mantidos pelo chamador, não recuperados do próprio payload. |
| Mecanismo interno | Reconstitui preflight, partições e scaler; refaz LogisticRegression no treino; confere coeficiente/intercepto, scores pela sigmoide, AUC/Brier e sequência de recursos. Verifica Receipt com run/release esperados e reconfere hashes ao fim. |
| Retorno e interpretação | dict com valid, VALID/INVALID, issues, promotion_authorized=false e completion_authorized=false. |
| Dependências diretas | from __future__ import annotations; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution.receipt import verify_execution_receipt; from sklearn.linear_model import LogisticRegression; from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.metrics import roc_auc_score, brier_score_loss |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-003); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leitura local e novo ajuste em memória; desativa autolog e recusa run MLflow ativa; sem escrita remota. |
| Consumidor/leitor | run_tracking antes de publicar qualquer modelo temporário e revisores do payload. |
| Limites e custo | Comparação é específica ao perfil/versões das bibliotecas; não constitui validação externa de negócio nem prova independente da origem dos dados. |
| Exemplo e contraexemplo | Ilustrativo: trocar um ID do holdout causa PARTITION_ID_TARGET_MISMATCH; coeficiente adulterado causa TRAIN_ONLY_FIT_ORACLE_MISMATCH. |
| Exceções e falhas levantadas | RuntimeError('RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH'); ValueError('EXPECTED_REQUEST_INVALID'); ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('PARTITIONS_NOT_OBJECT'); ValueError('PAYLOAD_NOT_CANONICAL_PASS'); ValueError('RESULT_SCHEMA_MISMATCH') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `verify(payload: object, *, expected_request: dict, expected_run_id: str) -> dict` (linhas 16–117) | Reconstitui preflight, partições e scaler; refaz LogisticRegression no treino; confere coeficiente/intercepto, scores pela sigmoide, AUC/Brier e sequência de recursos. Verifica Receipt com run/release esperados e reconfere hashes ao fim. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |

<a id="mt14-b1-code-map-file-005"></a>
#### hub-ml-baseline-ml/scripts/verify_tracking.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-baseline-ml/scripts/verify_tracking.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-baseline-ml/scripts/verify_tracking.py`; SHA-256 `b8dcc6ef9a72caf0566ff487100cfb461a2bf6aacdbb2d250da617e7ef70f92f`; lote B1-01. |
| Por que existe | Separar a observação remota enquanto o modelo existe da consistência verificável após soft delete. |
| Entradas e preparação | Payload, expected_request, expected_authorization, expected_run_id, authenticated_user e client; verify_live admite mlflow_module opcional. |
| Mecanismo interno | verify_live exige PENDING_VERIFICATION e bindings exatos; relê run, experimento, parâmetros, métricas, tags, assinatura/exemplo e modelo, compara probabilidades com cálculo do baseline. verify_finalized exige PASS/limpeza registrada, revalida computação e registros, e consulta experimento por ID para conferir lifecycle deleted. |
| Retorno e interpretação | Resultados valid/status/issues/scope; fase live acrescenta binding/observation e authority_authenticated=false; final declara model_rechecked_after_cleanup=false e historical_live_proof_authenticated=false. |
| Dependências diretas | from __future__ import annotations; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from pandas import DataFrame; import mlflow as mlflow_module |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-003); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leituras remotas MLflow; verificação computacional pode refazer treino e desativar autolog. Não cria nem apaga remoto. |
| Consumidor/leitor | Runner de tracking e operador que encerra o probe efêmero. |
| Limites e custo | A fase final não relê o modelo removido; registro anterior não é assinatura autenticada. Cliente e identidade fornecidos precisam pertencer ao ambiente autorizado. |
| Exemplo e contraexemplo | Ilustrativo: mesmo digest com experimento ainda active falha EXPERIMENT_FINAL_STATE_MISMATCH; relato de assinatura sem modelo live correspondente falha readback. |
| Exceções e falhas levantadas | ValueError('EFFECT_RECORD_SCHEMA_INVALID'); ValueError('EXPLICIT_DATABRICKS_TRACKING_URI_REQUIRED'); ValueError('FINAL_EFFECT_SCHEMA_INVALID'); ValueError('FINAL_PAYLOAD_NOT_CANONICAL_PASS'); ValueError('FINAL_READBACK_SCHEMA_INVALID'); ValueError('FINAL_REMOTE_IDS_INVALID'); ValueError('READBACK_SCHEMA_INVALID'); ValueError('REMOTE_IDS_INVALID'); ValueError('TRACKING_PAYLOAD_NOT_CANONICAL_PASS') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify_live, verify_finalized. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `verify_live(payload: object, *, expected_request: dict, expected_authorization: dict, expected_run_id: str, authenticated_user: str, client, mlflow_module=None) -> dict` (linhas 16–182) | verify_live exige PENDING_VERIFICATION e bindings exatos; relê run, experimento, parâmetros, métricas, tags, assinatura/exemplo e modelo, compara probabilidades com cálculo do baseline. verify_finalized exige PASS/limpeza registrada, revalida computação e registros, e consulta experimento por ID para conferir lifecycle deleted. Retorno: dict valid/status/issues/binding/observation/scope; authority_authenticated=false. |
| `verify_finalized(payload: object, *, expected_request: dict, expected_authorization: dict, expected_run_id: str, authenticated_user: str, client) -> dict` (linhas 185–327) | verify_live exige PENDING_VERIFICATION e bindings exatos; relê run, experimento, parâmetros, métricas, tags, assinatura/exemplo e modelo, compara probabilidades com cálculo do baseline. verify_finalized exige PASS/limpeza registrada, revalida computação e registros, e consulta experimento por ID para conferir lifecycle deleted. Retorno: dict valid/status/issues mais escopo e limites finais; tracking preserva observação histórica sem reler modelo. |

<a id="mt14-b1-code-map-file-006"></a>
#### hub-ml-cross-eda-ml/scripts/run_diagnostic.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-cross-eda-ml/scripts/run_diagnostic.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-cross-eda-ml/scripts/run_diagnostic.py`; SHA-256 `c15c728a901ac5a27211f94f2b4433f4de2a6f7010d240628c7906556e710c1c`; lote B1-01. |
| Por que existe | Medir cardinalidade e cobertura de duas fontes sintéticas estáticas sem executar o join final. |
| Entradas e preparação | context, datasets por source.id, sessão spark e run_id obrigatório. |
| Mecanismo interno | Reusa preflight L2; exige pit NOT_APPLICABLE; _rows liga IDs/esquemas/hashes, até 1.000 linhas por fonte, chaves str/int homogêneas e âncora única. Cria DataFrames Spark, chama diagnosticar_join(amostra_orfas=5), recusa expansão/multiplicidade à direita e emite Receipt para o diagnóstico. |
| Retorno e interpretação | Envelope com diagnostic, source_content_sha256, coverage_measured=true, join_executed=false, pit_executed=false e ml_readiness NOT_EVALUATED. |
| Dependências diretas | from __future__ import annotations; import hashlib; import importlib; import json; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution import run_preflight; from pyspark.sql.types import NumericType; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-007); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Ações Spark sobre dados fornecidos e coleta de diagnóstico; nenhuma gravação persistente; não lê tabela corporativa por nome. |
| Consumidor/leitor | verify_diagnostic e operador que precisa diagnosticar antes de cruzar. |
| Limites e custo | Uma declaração de hash só vira conteúdo conferido quando _rows lê o dataset recebido. PIT aplicável pertence à outra rota. |
| Exemplo e contraexemplo | Ilustrativo: um dataset alterado sem atualizar o contexto causa DATASETS:CONTENT_SHA256_MISMATCH; duplicidade na direita pode contradizer cardinalidade declarada. |
| Exceções e falhas levantadas | RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH'); RuntimeError('RELEASE_CHANGED_DURING_EXECUTION'); ValueError('DATASETS:ANCHOR_KEY_NOT_UNIQUE'); ValueError('DATASETS:BOUNDED_NONEMPTY_ROWS_REQUIRED'); ValueError('DATASETS:CONTENT_SHA256_MISMATCH:' + sid); ValueError('DATASETS:KEY_TYPE_MISMATCH:' + key); ValueError('DATASETS:KEY_TYPE_UNSUPPORTED_OR_MIXED:' + key); ValueError('DATASETS:NULL_KEY_REJECTED'); ValueError('DATASETS:SCHEMA_MISMATCH'); ValueError('DATASETS:SOURCE_IDS_MISMATCH'); ValueError('DIAGNOSTIC_CONTRACT_BLOCKED'); ValueError('L2_PREFLIGHT_BLOCKED:' + ','.join(domain['issues'])); ValueError('OBSERVED_CARDINALITY_CONTRADICTS_CONTEXT'); ValueError('PIT_APPLICABLE_REQUIRES_SER06'); ValueError('RUN_ID_REQUIRED') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: run. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_preflight()` (linhas 43–44) | Carrega o arquivo irmão de preflight via importlib; devolve módulo. Carregar executa código de importação, sem chamar o runner. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_primitive()` (linhas 47–56) | Resolve a primitive canônica pelo módulo e arquivo exatos; devolve callable, sem executar a análise. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_rows(context: dict, datasets: object) -> tuple[list[dict], list[dict], dict]` (linhas 59–93) | Valida datasets, esquema, tipos de chaves, hashes e unicidade da âncora; retorna (left_rows,right_rows,hashes). Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `run(context: object, datasets: object, spark, *, run_id: str) -> dict` (linhas 96–165) | Reusa preflight L2; exige pit NOT_APPLICABLE; _rows liga IDs/esquemas/hashes, até 1.000 linhas por fonte, chaves str/int homogêneas e âncora única. Cria DataFrames Spark, chama diagnosticar_join(amostra_orfas=5), recusa expansão/multiplicidade à direita e emite Receipt para o diagnóstico. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |

<a id="mt14-b1-code-map-file-007"></a>
#### hub-ml-cross-eda-ml/scripts/run_pit.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-cross-eda-ml/scripts/run_pit.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-cross-eda-ml/scripts/run_pit.py`; SHA-256 `1925612cf9d4b7f35516ae776c0c4373a8df7e6d25724b3b2a05e72ce39c95b1`; lote B1-01. |
| Por que existe | Selecionar a feature disponível na data de decisão, preservando uma linha por fato. |
| Entradas e preparação | context APPLICABLE, datasets sintéticos, spark, window_days e run_id; feature_value inteiro entre -1.000.000 e 1.000.000. |
| Mecanismo interno | prepare valida contexto N:1, entity_id, referência/availability fixas, fronteira LE, janela 1–36.500 dias, até 500 fatos e 500 versões, lag constante e ausência de empates. run exige Spark UTC, cria schemas explícitos, chama pit_join com politica_empate="erro", coleta projeção ordenada e verifica cardinalidade/input/release. Emite Receipt e artifacts sem finalizar. |
| Retorno e interpretação | prepare devolve domain/facts/features/source_hashes; run devolve result/records/diagnostic/artifacts/receipt e handoff/postflight null, scope_completion_authorized=false. |
| Dependências diretas | from __future__ import annotations; import importlib; import sys; from datetime import timedelta; from pathlib import Path; from hub_scripts.skill_execution.domain_context import closed, digest, integer, text, utc_instant; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution.postflight import sha256_digest; from hub_scripts.skill_execution import run_preflight; from pyspark.sql.types import StringType, StructField, StructType, TimestampType, LongType; from pyspark.sql import functions as F; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-007); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Computação Spark e collect em memória; sem escrita persistente nem ativação de policy. |
| Consumidor/leitor | verify_pit e compose de Feature Engineering. |
| Limites e custo | Sem bitemporalidade, lag variável ou LT; todas as decisões devem coincidir com corte declarado. Ausência de feature gera null, não zero. |
| Exemplo e contraexemplo | Ilustrativo: disponibilidade posterior ao corte exclui a versão; lag incompatível causa AVAILABLE_AT_CONTRADICTS_CONSTANT_LAG. |
| Exceções e falhas levantadas | RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH'); ValueError('AVAILABLE_AT_CONTRADICTS_CONSTANT_LAG'); ValueError('DATASETS:BOUNDED_NONEMPTY_ROWS_REQUIRED'); ValueError('DATASETS:CONTENT_SHA256_MISMATCH:' + sid); ValueError('DATASETS:SCHEMA_MISMATCH'); ValueError('DATASETS:SOURCE_IDS_MISMATCH'); ValueError('DECISION_AT_CANONICAL_UTC_REQUIRED'); ValueError('FACT_DECISION_OUTSIDE_DECLARED_CUT'); ValueError('FACT_DUPLICATE_ID_OR_GRAIN'); ValueError('FACT_SCHEMA_UNSUPPORTED'); ValueError('FEATURE_CLOCKS_CANONICAL_UTC_REQUIRED'); ValueError('FEATURE_REFERENCE_TIE_REJECTED'); ValueError('FEATURE_SCHEMA_UNSUPPORTED'); ValueError('FEATURE_VALUE_BOUNDED_INT_REQUIRED'); ValueError('INPUT_CHANGED_DURING_EXECUTION'); ValueError('L2_PREFLIGHT_BLOCKED:' + ','.join(domain['issues'])); ValueError('PIT_APPLICABLE_REQUIRED'); ValueError('PIT_CONTRACT_BLOCKED'); ValueError('PIT_LT_UNSUPPORTED_BY_HELPER'); ValueError('PIT_N_TO_ONE_PROFILE_REQUIRED'); ValueError('PIT_PROFILE_COLUMN_NAMES_REQUIRED'); ValueError('PIT_PROFILE_ENTITY_ID_ONLY'); ValueError('POST_JOIN_CARDINALITY_MISMATCH'); ValueError('RELEASE_CHANGED_DURING_EXECUTION'); ValueError('SPARK_UTC_SESSION_REQUIRED') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: prepare, run. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_preflight()` (linhas 43–44) | Carrega o arquivo irmão de preflight via importlib; devolve módulo. Carregar executa código de importação, sem chamar o runner. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_primitive()` (linhas 46–55) | Resolve a primitive canônica pelo módulo e arquivo exatos; devolve callable, sem executar a análise. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `prepare(context: object, datasets: object, *, window_days: int) -> dict` (linhas 57–121) | prepare valida contexto N:1, entity_id, referência/availability fixas, fronteira LE, janela 1–36.500 dias, até 500 fatos e 500 versões, lag constante e ausência de empates. run exige Spark UTC, cria schemas explícitos, chama pit_join com politica_empate="erro", coleta projeção ordenada e verifica cardinalidade/input/release. Emite Receipt e artifacts sem finalizar. Retorno: dict domain/facts/features/source_hashes; inválidos lançam exceção antes do Spark. |
| `run(context: object, datasets: object, spark, *, window_days: int, run_id: str) -> dict` (linhas 123–218) | prepare valida contexto N:1, entity_id, referência/availability fixas, fronteira LE, janela 1–36.500 dias, até 500 fatos e 500 versões, lag constante e ausência de empates. run exige Spark UTC, cria schemas explícitos, chama pit_join com politica_empate="erro", coleta projeção ordenada e verifica cardinalidade/input/release. Emite Receipt e artifacts sem finalizar. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |

<a id="mt14-b1-code-map-file-008"></a>
#### hub-ml-cross-eda-ml/scripts/verify_diagnostic.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-cross-eda-ml/scripts/verify_diagnostic.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-cross-eda-ml/scripts/verify_diagnostic.py`; SHA-256 `7313dac642aebf28a60e944b7f797812d80b20ebb107267e9fdd156c7219d184`; lote B1-01. |
| Por que existe | Comparar o diagnóstico Spark com um oráculo externo confiável. |
| Entradas e preparação | payload; expected_context/datasets/run_id/diagnostic independentes. |
| Mecanismo interno | Revalida contexto/fontes, liga digest do preflight/input, compara resultado inteiro com expected_diagnostic e confere Receipt/release antes e depois. |
| Retorno e interpretação | valid/status/issues/scope e flags completion/promotion false. |
| Dependências diretas | from __future__ import annotations; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution.receipt import verify_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-007); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leituras locais e validação em memória; não executa Spark nem o helper de diagnóstico. |
| Consumidor/leitor | Revisor do perfil estático; não autoriza prontidão ML. |
| Limites e custo | A qualidade do oráculo é responsabilidade externa; copiar diagnostic do payload anularia sua independência. |
| Exemplo e contraexemplo | Ilustrativo: cobertura diferente no oráculo causa TRUSTED_DIAGNOSTIC_ORACLE_MISMATCH mesmo com Receipt íntegro. |
| Exceções e falhas levantadas | ValueError('EXPECTED_CONTEXT_INVALID'); ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('PAYLOAD_NOT_CANONICAL_PASS'); ValueError('RESULT_NOT_OBJECT') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `verify(payload: object, *, expected_context: dict, expected_datasets: dict, expected_run_id: str, expected_diagnostic: dict) -> dict` (linhas 15–69) | Revalida contexto/fontes, liga digest do preflight/input, compara resultado inteiro com expected_diagnostic e confere Receipt/release antes e depois. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |

<a id="mt14-b1-code-map-file-009"></a>
#### hub-ml-cross-eda-ml/scripts/verify_pit.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-cross-eda-ml/scripts/verify_pit.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-cross-eda-ml/scripts/verify_pit.py`; SHA-256 `cbc5640951596bf137675637400a3769f4489c7a39c7b9d344907107d565890c`; lote B1-01. |
| Por que existe | Recalcular PIT em Python e concluir somente o perfil sintético local. |
| Entradas e preparação | payload e expected_context/datasets/window_days/run_id; fontes/oráculo não dependem da saída Spark. |
| Mecanismo interno | _oracle procura por entidade a maior referência elegível entre início da janela e disponibilidade ≤ decisão. verify_result compara linhas, diagnóstico, artifacts e Receipt. finalize copia payload, monta handoff e Postflight; verify_finalized refaz resultado, handoff e Postflight. |
| Retorno e interpretação | verify_result retorna receipt_verification; finalize retorna cópia enriquecida e possível scope_completion_authorized; verify_finalized retorna valid/issues, business_readiness NOT_EVALUATED e promotion false. |
| Dependências diretas | from __future__ import annotations; import copy; import sys; from datetime import timedelta; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, utc_instant; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution.postflight import build_postflight, verify_postflight; from hub_scripts.skill_execution.receipt import verify_execution_receipt; from hub_scripts.skill_execution.domain_context import loads_strict |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-007); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leitura de release e processamento Python; finalize altera somente a cópia do payload, sem Spark/escrita persistente. |
| Consumidor/leitor | Rota PIT direta e composição Feature Engineering, que exige verify_finalized válido. |
| Limites e custo | Finalizar requer payload PASS; não equivale a conclusão de negócio. Oráculo percorre versões por entidade e pode ter custo quadrático no tamanho do fixture. |
| Exemplo e contraexemplo | Ilustrativo: feature futura injetada causa INDEPENDENT_PIT_ORACLE_MISMATCH; handoff alterado depois falha HANDOFF_ORACLE_MISMATCH. |
| Exceções e falhas levantadas | ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('FINALIZE_REQUIRES_PASS'); ValueError('HANDOFF_MISSING'); ValueError('PAYLOAD_NOT_PASS'); ValueError('PAYLOAD_SHAPE_INVALID') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify_result, finalize, verify_finalized. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_runner()` (linhas 18–19) | Carrega o runner irmão por arquivo e devolve módulo para reverificação. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_contract()` (linhas 21–23) | Lê o contrato específico do perfil e devolve dict para Postflight; erro de arquivo/JSON pode propagar ao chamador. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_oracle(context: dict, datasets: dict, *, window_days: int) -> tuple[list[dict], dict]` (linhas 25–65) | Refaz PIT por busca Python independente, sem Spark: escolhe referência elegível máxima e conta categorias de cobertura; retorna (records,diagnostic). Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `verify_result(payload: object, *, expected_context: dict, expected_datasets: dict, expected_window_days: int, expected_run_id: str) -> dict` (linhas 67–120) | _oracle procura por entidade a maior referência elegível entre início da janela e disponibilidade ≤ decisão. verify_result compara linhas, diagnóstico, artifacts e Receipt. finalize copia payload, monta handoff e Postflight; verify_finalized refaz resultado, handoff e Postflight. Retorno: dict valid/status/issues/receipt_verification/scope para PIT, antes da finalização. |
| `finalize(payload: object, *, expected_context: dict, expected_datasets: dict, expected_window_days: int, expected_run_id: str) -> dict` (linhas 122–146) | _oracle procura por entidade a maior referência elegível entre início da janela e disponibilidade ≤ decisão. verify_result compara linhas, diagnóstico, artifacts e Receipt. finalize copia payload, monta handoff e Postflight; verify_finalized refaz resultado, handoff e Postflight. Retorno: cópia profunda do payload com handoff/Postflight e scope_completion_authorized calculado; pode lançar ValueError para payload não PASS. |
| `verify_finalized(payload: object, *, expected_context: dict, expected_datasets: dict, expected_window_days: int, expected_run_id: str) -> dict` (linhas 148–177) | Chama verify_result para reverificar PIT, entradas externas, artifacts e Receipt. Reconstrói o handoff esperado com contexto, hashes das fontes, contagem de decisões e limitações; compara seu digest, chama verify_postflight e exige scope_completion_authorized=true. Agrega divergências em issues, sem Spark ou releitura de modelo. Retorno: dict com valid, status VALID/INVALID, issues, scope=LOCAL_SYNTHETIC_PIT_V1, business_readiness=NOT_EVALUATED e promotion_authorized=false. |

<a id="mt14-b1-code-map-file-010"></a>
#### hub-ml-explainability/scripts/preflight.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-explainability/scripts/preflight.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-explainability/scripts/preflight.py`; SHA-256 `5feafa7b706f4080a2915097ee965ff61e91c06ac9ca356324709a147d269320`; lote B1-02. |
| Por que existe | Vincular pedido de explicabilidade linear a nomes, IDs e números representáveis. |
| Entradas e preparação | Pedido SER02-EXPLAINABILITY-REQUEST-1 com modelo declarado, X, background, feature_names, row_ids e sample_ids. |
| Mecanismo interno | Fecha pedido/modelo; exige regressão linear escalar, 1–100 features, matrizes até 10.000 linhas, uma linha de background, largura/coeficientes coerentes, IDs únicos e sample_ids existentes. _number recusa bool/não finitos/perda inteira float64; resolve o contrato do explicador. |
| Retorno e interpretação | validate_request e preflight retornam PASS/BLOCKED, issues e digest; preflight inclui sef/bindings. main escreve JSON e devolve exit 0/1. |
| Dependências diretas | from __future__ import annotations; import json; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, loads_strict, text; from hub_scripts.skill_execution.domain_context.release import blob; import argparse; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-010); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Somente validação/resolução/leitura local; não calcula SHAP ou treina modelo. |
| Consumidor/leitor | Runner, verifier e CLI de inspeção do pedido. |
| Limites e custo | Forma JSON não liga sozinha o objeto estimador real; _bound_arrays do runner faz essa ligação. sample_ids não reduzem X calculado. |
| Exemplo e contraexemplo | Fixture linear oficial tem duas features/linhas e uma amostra indicada; coefficient com largura distinta é MODEL:COEFFICIENT_WIDTH_MISMATCH. |
| Exceções e falhas levantadas | ContextError('BACKGROUND:SINGLE_ROW_REQUIRED'); ContextError('FEATURES:ORDERED_UNIQUE_NAMES_REQUIRED'); ContextError('MODEL:COEFFICIENT_WIDTH_MISMATCH'); ContextError('MODEL:UNSUPPORTED_PROFILE'); ContextError('REQUEST:SYNTHETIC_READ_ONLY_REQUIRED'); ContextError('REQUEST:UNSUPPORTED_PROFILE'); ContextError('ROWS:UNIQUE_IDS_REQUIRED'); ContextError('SAMPLES:EXPLICIT_ROW_IDS_REQUIRED'); ContextError(label + ':FINITE_EXACT_FLOAT64_REQUIRED'); ContextError(label + ':NONEMPTY_BOUNDED_MATRIX_REQUIRED'); ContextError(label + ':WIDTH_MISMATCH'); RuntimeError('SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH'); SystemExit(main()) |
| Captura implementada | (ContextError, TypeError, ValueError, OverflowError); (OSError, UnicodeError, ValueError); (OverflowError, ValueError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: validate_request, preflight, main. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_number(value, label)` (linhas 24–33) | Converte número para float somente se finito e, quando inteiro, representável sem perda; devolve float no fluxo normal e levanta ContextError(label + ":FINITE_EXACT_FLOAT64_REQUIRED") ao rejeitar a entrada. Retorno: float convertido no fluxo normal; ContextError é exceção levantada, não valor de retorno. |
| `_matrix(value, label, width)` (linhas 36–44) | Confere lista não vazia/limitada, largura e cada número; devolve matriz original validada, sem cópia. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `validate_request(request: object) -> dict` (linhas 47–83) | Fecha pedido/modelo; exige regressão linear escalar, 1–100 features, matrizes até 10.000 linhas, uma linha de background, largura/coeficientes coerentes, IDs únicos e sample_ids existentes. _number recusa bool/não finitos/perda inteira float64 Retorno: dict de decisão de domínio, com status PASS/BLOCKED, issues, digest e campos específicos da ficha. |
| `preflight(request: object) -> dict` (linhas 86–103) | Chama validate_request; em PASS resolve contrato por run_preflight, confere origem e registra bindings locais; devolve BLOCKED se domínio ou resolução falharem. Retorno: dict de decisão anterior à execução e bindings/SEF específicos da ficha; sem resultado analítico. |
| `main() -> int` (linhas 106–116) | Interpreta flags da linha de comando, lê JSON estrito e imprime resposta JSON; retorna exit code 0 no estado aceito e 1 em bloqueio/invalidez. Erros de argparse terminam a CLI. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |

| Interface de linha de comando | Contrato |
|---|---|
| Flag declarada | `parser.add_argument('--request', required=True, type=Path)` |
| Saída | JSON em stdout; exit code do estado calculado. Parsing da CLI pode encerrar com erro antes da lógica. Nenhuma CLI foi executada nesta edição. |

<a id="mt14-b1-code-map-file-011"></a>
#### hub-ml-explainability/scripts/run.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-explainability/scripts/run.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-explainability/scripts/run.py`; SHA-256 `3d5a65625c5cd14f6b9cbf67d3e126b4a465ffc792461b2f78356756d2001d80`; lote B1-02. |
| Por que existe | Calcular atribuições SHAP lineares com identidade de modelo e dados vinculados. |
| Entradas e preparação | request, model, X, background externos e run_id opcional UUID. |
| Mecanismo interno | Confere release/preflight, tipo exato LinearRegression, dimensão/ordem/features e hub_model_id; compara parâmetros e arrays ao pedido; faz cópias float64. Chama compute_shap linear/regression sobre todo X, captura stdout, confere forma/valores, imutabilidade das entradas/modelo e release; emite Receipt. |
| Retorno e interpretação | Envelope result com base_value, shap_values por linha/feature, nomes/IDs, business_readiness NOT_EVALUATED e promotion false. |
| Dependências diretas | from __future__ import annotations; import importlib; import io; import json; import sys; import uuid; from contextlib import redirect_stdout; from pathlib import Path; import numpy as np; from hub_scripts.skill_execution.domain_context import digest, loads_strict; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; import numpy as np; import numpy as np; import numpy as np; from sklearn.linear_model import LinearRegression; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-010); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Computação NumPy/SHAP em memória e captura de stdout; sem treino, plots ou escrita persistente. |
| Consumidor/leitor | verify.py recebe modelo e arrays externos para conferir o resultado. |
| Limites e custo | Requer dependências instaladas; coeficientes escalares apenas. Atribuição é em relação ao background, não causa da decisão nem probabilidade. |
| Exemplo e contraexemplo | Fixture: base ilustrativa 3; linha [2,1] com coeficientes [2,-1] e background zero tem contribuições [4,-1]. Valores aqui são analíticos, não execução. |
| Exceções e falhas levantadas | RuntimeError('CANONICAL_PRIMITIVE_UNAVAILABLE'); RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('INPUT_CHANGED_DURING_EXECUTION'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_OUTPUT_INVALID'); RuntimeError('RECEIPT_IMPORT_ORIGIN_MISMATCH'); RuntimeError('RELEASE_CHANGED_DURING_EXECUTION'); ValueError('INPUT:ARRAY_BINDING_MISMATCH'); ValueError('MODEL:FEATURE_NAMES_ORDER_MISMATCH'); ValueError('MODEL:IDENTITY_BINDING_MISMATCH'); ValueError('MODEL:PARAMETER_BINDING_MISMATCH'); ValueError('MODEL:RAW_SCALAR_OUTPUT_REQUIRED'); ValueError('MODEL:SKLEARN_LINEAR_REGRESSION_REQUIRED'); ValueError('RUN_ID_REQUIRED'); ValueError(label + ':FINITE_ARRAY_REQUIRED'); ValueError(label + ':FLOAT64_OVERFLOW'); ValueError(label + ':FLOAT64_PRECISION_LOSS'); ValueError(label + ':INTEGER_FLOAT64_PRECISION_LOSS'); ValueError(label + ':NUMERIC_ARRAY_REQUIRED') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: run. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_preflight_module()` (linhas 37–38) | Carrega o preflight irmão e devolve seu módulo; nenhuma análise executada nesta função. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_canonical_primitive()` (linhas 41–52) | Importa a primitive esperada e confere arquivo de implementação; devolve callable ou lança erro de origem. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_float64_copy(value, label)` (linhas 55–70) | Confere dtype numérico/finiteza/roundtrip e devolve array float64 independente; overflow ou perda de precisão bloqueiam. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_model_snapshot(model)` (linhas 73–79) | Extrai coeficientes, intercepto, hub_model_id e feature_names_in quando existente; devolve dict para detecção de mutação. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_bound_arrays(request, model, X, background)` (linhas 82–110) | Liga modelo LinearRegression exato e arrays externos ao pedido, conferindo identidade/dimensões/parâmetros; devolve (array, background) em cópias float64. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `run(request: object, *, model, X, background, run_id: str \| None=None) -> dict` (linhas 113–193) | Confere release/preflight, tipo exato LinearRegression, dimensão/ordem/features e hub_model_id; compara parâmetros e arrays ao pedido; faz cópias float64. Chama compute_shap linear/regression sobre todo X, captura stdout, confere forma/valores, imutabilidade das entradas/modelo e release; emite Receipt. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |

<a id="mt14-b1-code-map-file-012"></a>
#### hub-ml-explainability/scripts/verify.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-explainability/scripts/verify.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-explainability/scripts/verify.py`; SHA-256 `873a33f9a0e7f082e24dc5c6d6f9f3769012fd1aa2273e3a0100a02e68eac57e`; lote B1-02. |
| Por que existe | Conferir SHAP por fórmula analítica independente do explicador. |
| Entradas e preparação | payload; expected_request/model/X/background/run_id. |
| Mecanismo interno | Revalida pedido, modelo/arrays e release; calcula base=intercepto+soma(coef×background médio) e contribuição coef×(X−média). _close usa tolerância absoluta/relativa 1e-10; confere metadados, Receipt e release. |
| Retorno e interpretação | valid/status/issues/scope; completion e promotion false. |
| Dependências diretas | from __future__ import annotations; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution.receipt import verify_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-010); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Computação NumPy e leitura local; não chama compute_shap nem faz efeito remoto. |
| Consumidor/leitor | Operador que precisa reverificar a explicação com objetos mantidos fora do payload. |
| Limites e custo | O oráculo só vale para modelo linear escalar desse perfil. Valores matemáticos válidos não comprovam interpretação causal ou representatividade. |
| Exemplo e contraexemplo | Ilustrativo: base_value alterado causa ANALYTIC_ORACLE_MISMATCH; ordem diferente de features pode falhar antes em binding. |
| Exceções e falhas levantadas | RuntimeError('RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH'); ValueError('EXPECTED_REQUEST_INVALID'); ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('PAYLOAD_NOT_CANONICAL_PASS'); ValueError('RESULT_NOT_OBJECT') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_close(actual, expected)` (linhas 16–18) | Devolve bool para número finito próximo ao esperado com rel_tol=abs_tol=1e-10; tipos não numéricos falham. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `verify(payload: object, *, expected_request: dict, expected_model, expected_X, expected_background, expected_run_id: str) -> dict` (linhas 21–85) | Revalida pedido, modelo/arrays e release; calcula base=intercepto+soma(coef×background médio) e contribuição coef×(X−média). _close usa tolerância absoluta/relativa 1e-10; confere metadados, Receipt e release. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |

<a id="mt14-b1-code-map-file-013"></a>
#### hub-ml-feature-engineering/scripts/run.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-feature-engineering/scripts/run.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-feature-engineering/scripts/run.py`; SHA-256 `d80115710f0656a029380529760941cb48a9e3d76078379efd56575136015dfa`; lote B1-02. |
| Por que existe | Construir lag de uma observação por entidade com disponibilidade fixa de um dia. |
| Entradas e preparação | SER07-REQUEST-1/FIXED_LAG_L1_V1, population_id, decision_at, window_days, temporal e rows; run_id opcional UUID. |
| Mecanismo interno | preflight fecha pedido/linhas, valida contexto temporal, decisão UTC, janela 1–365 dias, 2–1.000 linhas, disponibilidade event+1 dia, meia-noite e unicidade. Separa future/unavailable/outside_window. run filtra elegíveis e chama create_temporal_features com lags=[1], rolling_windows=[], calendar_features=false, entity_cols e erro em duplicidade. |
| Retorno e interpretação | Preflight registra eligible_ids/excluded_counts; run emite features(id,entity_id,event_at,lag_1), Receipt e flags fit/materialization/promotion false. |
| Dependências diretas | from __future__ import annotations; import importlib; import io; import json; import sys; import uuid; from contextlib import redirect_stdout; from datetime import timedelta; from pathlib import Path; from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, integer, loads_strict, text, utc_instant, validate_temporal_context; from hub_scripts.skill_execution.domain_context.release import release_integrity; import argparse; from hub_scripts.skill_execution import run_preflight; import pandas as pd; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-015); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | DataFrame pandas e cálculo em memória; sem fit ou materialização; main imprime JSON. |
| Consumidor/leitor | verify.py e leitor que precisa diferenciar seleção temporal de treinamento. |
| Limites e custo | Lag 1 é uma observação anterior, não garantia de dia consecutivo. O helper remove o warm-up com lag ausente; a primeira observação por entidade não vira zero nem feature válida. |
| Exemplo e contraexemplo | Ilustrativo: história ainda indisponível é excluída mesmo com event_at passado; disponibilidade event+2 dias bloqueia o perfil. |
| Exceções e falhas levantadas | ContextError('REQUEST:SYNTHETIC_READ_ONLY_REQUIRED'); ContextError('REQUEST:UNSUPPORTED_PROFILE'); ContextError('ROWS:AVAILABILITY_CONTRADICTS_DECLARED_LAG'); ContextError('ROWS:COUNT_OUT_OF_RANGE'); ContextError('ROWS:DUPLICATE_ID_OR_GRAIN'); ContextError('ROWS:FINITE_NUMERIC_VALUE_REQUIRED'); ContextError('ROWS:MIDNIGHT_UTC_PROFILE_ONLY'); ContextError('ROWS:NO_ELIGIBLE_HISTORY'); ContextError('SEF:BLOCKED'); ContextError('TEMPORAL:FIXED_LAG_PROFILE_REQUIRED'); RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH'); RuntimeError('RELEASE_CHANGED_DURING_EXECUTION'); SystemExit(main()); ValueError('RUN_ID_REQUIRED') |
| Captura implementada | (ContextError, TypeError, ValueError, OverflowError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: preflight, run, main. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `preflight(request: object) -> dict` (linhas 47–107) | preflight fecha pedido/linhas, valida contexto temporal, decisão UTC, janela 1–365 dias, 2–1.000 linhas, disponibilidade event+1 dia, meia-noite e unicidade. Separa future/unavailable/outside_window. run filtra elegíveis e chama create_temporal_features com lags=[1], rolling_windows=[], calendar_features=false, entity_cols e erro em duplicidade. Retorno: dict de decisão anterior à execução e bindings/SEF específicos da ficha; sem resultado analítico. |
| `run(request: object, *, run_id: str \| None=None) -> dict` (linhas 110–178) | preflight fecha pedido/linhas, valida contexto temporal, decisão UTC, janela 1–365 dias, 2–1.000 linhas, disponibilidade event+1 dia, meia-noite e unicidade. Separa future/unavailable/outside_window. run filtra elegíveis e chama create_temporal_features com lags=[1], rolling_windows=[], calendar_features=false, entity_cols e erro em duplicidade. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |
| `main() -> int` (linhas 181–189) | Interpreta flags da linha de comando, lê JSON estrito e imprime resposta JSON; retorna exit code 0 no estado aceito e 1 em bloqueio/invalidez. Erros de argparse terminam a CLI. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |

| Interface de linha de comando | Contrato |
|---|---|
| Flag declarada | `parser.add_argument('--request', required=True, type=Path)` |
| Flag declarada | `parser.add_argument('--run-id', required=True)` |
| Saída | JSON em stdout; exit code do estado calculado. Parsing da CLI pode encerrar com erro antes da lógica. Nenhuma CLI foi executada nesta edição. |

<a id="mt14-b1-code-map-file-014"></a>
#### hub-ml-feature-engineering/scripts/run_pit_features.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-feature-engineering/scripts/run_pit_features.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-feature-engineering/scripts/run_pit_features.py`; SHA-256 `9cf314fc9949cdbb194354cf228a77a0f49ccf68353e2b7202e79107284f036d`; lote B1-02. |
| Por que existe | Compor uma view de features a partir de PIT já executado e finalizado. |
| Entradas e preparação | context, datasets, spark, window_days, upstream_run_id e view_run_id; verifier recebe equivalentes expected_*. |
| Mecanismo interno | compose exige IDs distintos, verifica release FE e contrato; executa Cross PIT uma vez, finalize e verify_finalized; projeta as linhas verificadas e vincula digests de contexto/datasets/receipt/postflight. verify refaz o upstream e a projeção, recusando Receipt FE inventado. |
| Retorno e interpretação | Payload PASS/BLOCKED com upstream_evidence, result/features, feature_view_sha256, fe_manifest_sha256; receipt próprio sempre null. |
| Dependências diretas | from __future__ import annotations; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, text; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-015); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | compose executa Spark upstream; verify apenas confere em Python. A view aqui é projeção em memória, não view persistente no catálogo. |
| Consumidor/leitor | run_pit_materialization prepara efeito somente após verificar essa projeção. |
| Limites e custo | Sem fit/materialização/prontidão de negócio; sem novo Receipt FE. Identidade/digest da release upstream fica vinculada pela evidência aninhada. |
| Exemplo e contraexemplo | Ilustrativo: upstream_run_id igual a view_run_id bloqueia RUN_IDS_MUST_DIFFER; linha projetada alterada falha FEATURE_VIEW_PROJECTION_MISMATCH. |
| Exceções e falhas levantadas | ValueError('EXPECTED_RUN_IDS_MUST_DIFFER'); ValueError('FE_INPUT_CHANGED_DURING_EXECUTION'); ValueError('FE_RELEASE_CHANGED_DURING_EXECUTION'); ValueError('PAYLOAD_NOT_CANONICAL_PASS'); ValueError('PIT_VIEW_CONTRACT_BLOCKED'); ValueError('RUN_IDS_MUST_DIFFER'); ValueError('UPSTREAM_PIT_BLOCKED:' + str(upstream['trace']['blocking_issues'])); ValueError('UPSTREAM_PIT_POSTFLIGHT_INVALID:' + str(upstream_check['issues'])) |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: compose, verify. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_upstream()` (linhas 37–41) | Carrega runner e verifier Cross PIT por arquivo; devolve par de módulos, sem executar PIT. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_projection(upstream: dict, *, context: dict, datasets: dict, window_days: int, view_run_id: str) -> dict` (linhas 43–70) | Projeta linhas de upstream já verificado e conserva hashes/IDs da evidência; devolve resultado FE sem fit ou materialização. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `compose(context: dict, datasets: dict, spark, *, window_days: int, upstream_run_id: str, view_run_id: str) -> dict` (linhas 72–122) | compose exige IDs distintos, verifica release FE e contrato; executa Cross PIT uma vez, finalize e verify_finalized; projeta as linhas verificadas e vincula digests de contexto/datasets/receipt/postflight. verify refaz o upstream e a projeção, recusando Receipt FE inventado. Retorno: dict PASS com upstream_evidence/result/hash da view e receipt null, ou BLOCKED com issues. |
| `verify(payload: object, *, expected_context: dict, expected_datasets: dict, expected_window_days: int, expected_upstream_run_id: str, expected_view_run_id: str) -> dict` (linhas 124–175) | compose exige IDs distintos, verifica release FE e contrato; executa Cross PIT uma vez, finalize e verify_finalized; projeta as linhas verificadas e vincula digests de contexto/datasets/receipt/postflight. verify refaz o upstream e a projeção, recusando Receipt FE inventado. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |

<a id="mt14-b1-code-map-file-015"></a>
#### hub-ml-feature-engineering/scripts/run_pit_materialization.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-feature-engineering/scripts/run_pit_materialization.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-feature-engineering/scripts/run_pit_materialization.py`; SHA-256 `ba8f1efe23a405427498bd297d88c752ddf00ad417cbb91087e592c65d2638be`; lote B1-02. |
| Por que existe | Preparar e materializar efemeramente a projeção PIT verificada em um alvo Delta de propriedade comprovada. |
| Entradas e preparação | Payload de view e entradas expected_* independentes; execute recebe spark, authorization e run_id. A autorização deve vincular o digest de effect_request. |
| Mecanismo interno | effect_request congela entradas e chama FE verify, normaliza linhas/UTC/nulls/int64, constrói pedido e proveniência. execute repete essa conferência, resolve contrato e chama _execute_owned com profile FE_PIT, incluindo hashes de view/fontes/contexto/corte/Receipt/Postflight; reconfere release ao fim. |
| Retorno e interpretação | effect_request retorna pedido SER08-FE-MATERIALIZATION-REQUEST-1; execute retorna efeito Delta com hashes FE, view e upstream_postflight_id, status PASS/BLOCKED/UNKNOWN. |
| Dependências diretas | from __future__ import annotations; import json; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, loads_strict, text, utc_instant; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-015); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Preparação é read-only; execute faz CREATE/MERGE/replay/readback/DROP controlados no engine Delta compartilhado e views temporárias. |
| Consumidor/leitor | Operador autorizado do probe; engine run_delta fornece ciclo de ownership e limpeza. |
| Limites e custo | Sem materialização de negócio; UNKNOWN quando houve tentativa de criar sem comprovação de ausência após limpeza. Não há Receipt novo que autentique o efeito. |
| Exemplo e contraexemplo | Ilustrativo: valor null com available_at não null é NULL_FEATURE_WITH_AVAILABILITY; feature posterior à decisão é rejeitada antes de escrever. |
| Exceções e falhas levantadas | ValueError('AVAILABILITY_TIMESTAMP_NOT_CANONICAL'); ValueError('DECISION_TIMESTAMP_NOT_CANONICAL'); ValueError('DUPLICATE_DECISION_ID'); ValueError('FEATURE_AVAILABLE_AFTER_DECISION'); ValueError('FEATURE_NOT_INT64'); ValueError('FEATURE_ROWS_NOT_LIST'); ValueError('FEATURE_ROW_SHAPE_INVALID'); ValueError('FEATURE_VIEW_INVALID:' + str(checked['issues'])); ValueError('FE_MATERIALIZATION_CONTRACT_BLOCKED'); ValueError('NONCANONICAL_' + label); ValueError('NULL_FEATURE_WITH_AVAILABILITY') |
| Captura implementada | (TypeError, ValueError, OverflowError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: effect_request, execute. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_snapshot(value, label)` (linhas 38–44) | Serializa e relê JSON para desligar referências mutáveis do chamador; devolve cópia, recusando valores não representáveis. A variante de tracking também verifica ciclos e chaves explicitamente. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_modules()` (linhas 47–51) | Carrega módulos FE view e engine Delta por arquivo; devolve o par sem executar o efeito. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_rows(features)` (linhas 54–86) | Confere linhas FE, IDs únicos, UTC canônico, disponibilidade não futura e coerência null/int64; retorna linhas ordenadas. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_bound_request(payload, context, datasets, window_days, upstream_run_id, view_run_id)` (linhas 89–119) | Verifica view FE com entradas independentes, valida linhas e deriva (pedido de efeito, hashes de proveniência); nenhum efeito remoto. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_materialization_preflight()` (linhas 122–125) | Resolve contrato de materialização e devolve dict do preflight; não concede autorização externa. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `effect_request(payload: dict, *, expected_context: dict, expected_datasets: dict, expected_window_days: int, expected_upstream_run_id: str, expected_view_run_id: str) -> dict` (linhas 128–137) | effect_request congela entradas e chama FE verify, normaliza linhas/UTC/nulls/int64, constrói pedido e proveniência. execute repete essa conferência, resolve contrato e chama _execute_owned com profile FE_PIT, incluindo hashes de view/fontes/contexto/corte/Receipt/Postflight; reconfere release ao fim. Retorno: dict SER08-FE-MATERIALIZATION-REQUEST-1 a vincular pelo digest na autorização externa. |
| `execute(payload: dict, spark, authorization: dict, *, run_id: str, expected_context: dict, expected_datasets: dict, expected_window_days: int, expected_upstream_run_id: str, expected_view_run_id: str) -> dict` (linhas 140–178) | effect_request congela entradas e chama FE verify, normaliza linhas/UTC/nulls/int64, constrói pedido e proveniência. execute repete essa conferência, resolve contrato e chama _execute_owned com profile FE_PIT, incluindo hashes de view/fontes/contexto/corte/Receipt/Postflight; reconfere release ao fim. Retorno: dict de efeito PASS/BLOCKED/UNKNOWN; campos de fase, readback, cleanup e hashes detalhados na ficha. |

<a id="mt14-b1-code-map-file-016"></a>
#### hub-ml-feature-engineering/scripts/verify.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-feature-engineering/scripts/verify.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-feature-engineering/scripts/verify.py`; SHA-256 `ec92d734968435b7c79410fe6fc916027b97ba88fdc4311ef87b876319e7a203`; lote B1-02. |
| Por que existe | Conferir o lag fixo com features esperadas fornecidas independentemente. |
| Entradas e preparação | payload, expected_request, expected_run_id e expected_features. |
| Mecanismo interno | Recalcula preflight/eligibilidade, liga metadados/input, compara digest de features ao oráculo do chamador e valida Receipt/release. |
| Retorno e interpretação | valid/status/issues e completion/promotion false. |
| Dependências diretas | from __future__ import annotations; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution.receipt import verify_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-015); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leituras locais e validação em memória; não chama create_temporal_features. |
| Consumidor/leitor | Revisor do perfil FIXED_LAG_L1_V1, não da composição PIT ou materialização. |
| Limites e custo | Não produz o oráculo; expected_features copiado do resultado não é prova independente. |
| Exemplo e contraexemplo | Ilustrativo: trocar lag_1 de uma linha causa TRUSTED_ORACLE_FEATURE_MISMATCH. |
| Exceções e falhas levantadas | ValueError('EXPECTED_REQUEST_INVALID'); ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('PAYLOAD_NOT_CANONICAL_PASS'); ValueError('RESULT_SCHEMA_MISMATCH') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `verify(payload: object, *, expected_request: dict, expected_run_id: str, expected_features: list[dict]) -> dict` (linhas 17–63) | Recalcula preflight/eligibilidade, liga metadados/input, compara digest de features ao oráculo do chamador e valida Receipt/release. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |

<a id="mt14-b1-code-map-file-017"></a>
#### hub-ml-monitoramento-modelo/scripts/preflight.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-monitoramento-modelo/scripts/preflight.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-monitoramento-modelo/scripts/preflight.py`; SHA-256 `b1ab8e5e69731e57f658b757f1e197169c2012e63ef2c60dc4c63614c5582414`; lote B1-03. |
| Por que existe | Separar duas janelas de scores sintéticos antes de medir mudança de distribuição. |
| Entradas e preparação | SER11-REQUEST-1, identidade/versão/população e duas listas reference/current; score pode ser null. |
| Mecanismo interno | Fecha campos; exige n_bins inteiro 4, eps float 1e-6, score_name score; verifica reference_start≤reference_end<current_start≤current_end. Cada janela tem ao menos quatro linhas e duas scores não nulas; IDs são únicos entre janelas, instantes pertencem à janela e scores ficam em [0,1]. Resolve drift_numeric. |
| Retorno e interpretação | validate_request e preflight: status/issues/profile/request_sha256 e helper_called/writes false; preflight soma sef e hashes. |
| Dependências diretas | from __future__ import annotations; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, integer, text, utc_instant; from hub_scripts.skill_execution.domain_context.release import blob; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-021); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Sem chamada analítica ou escrita; lê contrato e código local. |
| Consumidor/leitor | run.py e verify.py do drift, não a rota de performance madura. |
| Limites e custo | Não avalia labels; não há teto de linhas nesse preflight, embora o uso pretendido seja sintético/local. n_bins declarado não garante quatro intervalos distintos quando quantis coincidem. |
| Exemplo e contraexemplo | Ilustrativo: janelas sobrepostas causam WINDOW:NOT_ORDERED_DISJOINT; três scores null em quatro linhas causam WINDOW:TOO_FEW_FINITE_SCORES. |
| Exceções e falhas levantadas | ContextError('PROFILE:SCORE_OR_BINS_UNSUPPORTED'); ContextError('PROFILE:SMOOTHING_UNSUPPORTED'); ContextError('REQUEST:SYNTHETIC_NO_EFFECT_ONLY'); ContextError('REQUEST:UNSUPPORTED_PROFILE'); ContextError('ROW:DUPLICATE_ID'); ContextError('ROW:OUTSIDE_WINDOW'); ContextError('ROW:SCORE_OUT_OF_RANGE'); ContextError('WINDOW:AT_LEAST_FOUR_REQUIRED:' + partition); ContextError('WINDOW:NOT_ORDERED_DISJOINT'); ContextError('WINDOW:TOO_FEW_FINITE_SCORES'); RuntimeError('SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH') |
| Captura implementada | (ContextError, KeyError, TypeError, ValueError, OverflowError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: validate_request, preflight. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `validate_request(request: object) -> dict` (linhas 21–65) | Fecha campos; exige n_bins inteiro 4, eps float 1e-6, score_name score; verifica reference_start≤reference_end<current_start≤current_end. Cada janela tem ao menos quatro linhas e duas scores não nulas; IDs são únicos entre janelas, instantes pertencem à janela e scores ficam em [0,1]. Retorno: dict de decisão de domínio, com status PASS/BLOCKED, issues, digest e campos específicos da ficha. |
| `preflight(request: object) -> dict` (linhas 68–84) | Chama validate_request; em PASS resolve contrato por run_preflight, confere origem e registra bindings locais; devolve BLOCKED se domínio ou resolução falharem. Retorno: dict de decisão anterior à execução e bindings/SEF específicos da ficha; sem resultado analítico. |

<a id="mt14-b1-code-map-file-018"></a>
#### hub-ml-monitoramento-modelo/scripts/preflight_performance.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-monitoramento-modelo/scripts/preflight_performance.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-monitoramento-modelo/scripts/preflight_performance.py`; SHA-256 `3f433df14128f9128ba379f96b37c7bc64a005ee64d6ee6d1fdb4999a2616fff`; lote B1-03. |
| Por que existe | Validar maturação dos rótulos antes de comparar desempenho binário. |
| Entradas e preparação | SER12-REQUEST-1, identidade/população, evaluation_at, política auc_thresholds, reference/current com score e label. |
| Mecanismo interno | Aplica Draft202012Validator e regras adicionais: warning<critical, direção higher, delta absolute, janelas estritamente crescentes/disjuntas, fim atual≤evaluation_at. Exige 4–1.000 linhas por janela, IDs globais únicos, score finito, classes 0 e 1 em ambas, observação≤label_available_at≤evaluation_at; resolve duas primitives. |
| Retorno e interpretação | status/issues/digest e windows(ids,count); preflight soma sef/release_bindings. |
| Dependências diretas | from __future__ import annotations; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, text, utc_instant; from hub_scripts.skill_execution.domain_context.release import blob, loads_strict; from jsonschema import Draft202012Validator; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-021); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leitura de schema/contrato e validação; não consulta labels remotas nem executa métricas. |
| Consumidor/leitor | run_performance.py e verify_performance.py. |
| Limites e custo | Maturação é conferida contra timestamps fornecidos, não autenticada em sistema externo. Falta de jsonschema pode propagar ImportError em validate_request, pois não está entre exceções capturadas ali. |
| Exemplo e contraexemplo | Ilustrativo: rótulo que só estaria disponível amanhã falha ROW:LABEL_NOT_MATURE_OR_PRECEDES_PREDICTION. |
| Exceções e falhas levantadas | ContextError('REQUEST:SCHEMA_INVALID:' + str(errors[0].validator)); ContextError('REQUEST:SYNTHETIC_NO_EFFECT_ONLY'); ContextError('REQUEST:UNSUPPORTED:' + key); ContextError('ROW:BINARY_LABEL_REQUIRED'); ContextError('ROW:DUPLICATE_ID'); ContextError('ROW:INVALID_SCORE'); ContextError('ROW:LABEL_NOT_MATURE_OR_PRECEDES_PREDICTION'); ContextError('ROW:OUTSIDE_WINDOW'); ContextError('ROWS:BOUNDED_AT_LEAST_FOUR:' + name); ContextError('THRESHOLD:AUC_HIGHER_ABSOLUTE_ONLY'); ContextError('THRESHOLD:FINITE_NUMBER_REQUIRED'); ContextError('THRESHOLD:ORDER_INVALID'); ContextError('WINDOW:BOTH_CLASSES_REQUIRED:' + name); ContextError('WINDOW:NOT_DISJOINT_OR_EVALUATION_EARLY'); ContextError('WINDOW:START_NOT_BEFORE_END:' + name); RuntimeError('SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH') |
| Captura implementada | (ContextError, KeyError, TypeError, ValueError, OverflowError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: validate_request, preflight. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `validate_request(request: object) -> dict` (linhas 24–94) | Aplica Draft202012Validator e regras adicionais: warning<critical, direção higher, delta absolute, janelas estritamente crescentes/disjuntas, fim atual≤evaluation_at. Exige 4–1.000 linhas por janela, IDs globais únicos, score finito, classes 0 e 1 em ambas, observação≤label_available_at≤evaluation_at Retorno: dict de decisão de domínio, com status PASS/BLOCKED, issues, digest e campos específicos da ficha. |
| `preflight(request: object) -> dict` (linhas 97–117) | Chama validate_request; em PASS resolve contrato por run_preflight, confere origem e registra bindings locais; devolve BLOCKED se domínio ou resolução falharem. Retorno: dict de decisão anterior à execução e bindings/SEF específicos da ficha; sem resultado analítico. |

<a id="mt14-b1-code-map-file-019"></a>
#### hub-ml-monitoramento-modelo/scripts/run.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-monitoramento-modelo/scripts/run.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-monitoramento-modelo/scripts/run.py`; SHA-256 `d48573638f56c789a5b2f68188c632b30afd0346666161286da91f1afd81620b`; lote B1-03. |
| Por que existe | Medir drift numérico por PSI e KS conservando janelas e ausências. |
| Entradas e preparação | Pedido de drift e run_id opcional UUID; pandas/NumPy e dependências do helper disponíveis. |
| Mecanismo interno | Confere release/preflight e origem de calculate_psi/calculate_ks; converte null em NaN, calcula PSI com quantis da referência, eps e bucket ausente, e KS nas observações finitas. Registra arestas internas únicas, contagens/IDs/ausências e Receipt. |
| Retorno e interpretação | SER11-RESULT-1 com windows, bin_edges_internal, psi, ks_statistic, ks_pvalue, interpretação DISTRIBUTION_DIAGNOSTIC_ONLY, performance_evaluated/action_performed false. |
| Dependências diretas | from __future__ import annotations; import importlib; import json; import sys; import uuid; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, loads_strict; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; import argparse; import pandas as pd; import numpy as np; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-021); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Computação em memória; CLI imprime JSON; sem alertas, retreino ou escrita persistente. |
| Consumidor/leitor | verify.py de drift e leitor que distingue diagnóstico de ação. |
| Limites e custo | Trace agrega PSI e KS sob o item drift_numeric, embora o contrato nomeie calculate_psi. Mudança de distribuição não mede degradação preditiva sem labels. |
| Exemplo e contraexemplo | Ilustrativo: nulls contribuem para bucket de PSI, mas não entram na amostra KS; alterar fronteira de quantil mudaria a interpretação. |
| Exceções e falhas levantadas | RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH'); RuntimeError('RELEASE_CHANGED_DURING_EXECUTION'); SystemExit(0 if payload['status'] == 'PASS' else 1); ValueError('RUN_ID_REQUIRED') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: run. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_canonical()` (linhas 33–40) | Importa módulo canônico e recusa origem de fachada/implementação divergente; devolve helper ou helpers originais. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `run(request: object, *, run_id: str \| None=None) -> dict` (linhas 43–116) | Confere release/preflight e origem de calculate_psi/calculate_ks; converte null em NaN, calcula PSI com quantis da referência, eps e bucket ausente, e KS nas observações finitas. Registra arestas internas únicas, contagens/IDs/ausências e Receipt. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |

| Interface de linha de comando | Contrato |
|---|---|
| Flag declarada | `parser.add_argument('--request', required=True, type=Path)` |
| Flag declarada | `parser.add_argument('--run-id', required=True)` |
| Saída | JSON em stdout; exit code do estado calculado. Parsing da CLI pode encerrar com erro antes da lógica. Nenhuma CLI foi executada nesta edição. |

<a id="mt14-b1-code-map-file-020"></a>
#### hub-ml-monitoramento-modelo/scripts/run_performance.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-monitoramento-modelo/scripts/run_performance.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-monitoramento-modelo/scripts/run_performance.py`; SHA-256 `281b14f137ed279b8bf95f6780da01a09e3db26f9cb0dfa24db37b6e16568d2a`; lote B1-03. |
| Por que existe | Comparar métricas binárias de janelas com labels maduras e produzir diagnóstico local. |
| Entradas e preparação | Pedido SER12 validado e run_id opcional UUID; NumPy e bibliotecas importadas pelos helpers. |
| Mecanismo interno | Resolve calculate_binary_metrics e PerformanceMonitor; calcula AUC, KS percentual e Brier nas duas janelas. Instancia monitor com AUC referência e política dada, adiciona um período atual e obtém status/decisão; não executa a ação sugerida. Emite artifacts/Receipt para posterior finalização. |
| Retorno e interpretação | SER12-RESULT-1 com métricas, política, auc_deterioration, monitor_status, investigation_decision; handoff/postflight null e scope_completion_authorized=false. |
| Dependências diretas | from __future__ import annotations; import importlib; import sys; import uuid; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; import numpy as np; from hub_scripts.skill_execution.postflight import sha256_digest; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-021); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Cálculos em memória e objeto monitor; nenhuma criação de alerta, job, retreino ou escrita. |
| Consumidor/leitor | verify_performance.verify/finalize/verify_finalized. |
| Limites e custo | Um único período é adicionado; consecutive_alert_periods=3 não produz história de três períodos. Decisão crítica é candidata à investigação, não autorização de retreino. |
| Exemplo e contraexemplo | Ilustrativo: queda AUC acima de critical leva ao status crítico no perfil; action_performed permanece false. |
| Exceções e falhas levantadas | RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH:' + symbol); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH:' + symbol); RuntimeError('RECEIPT_IMPORT_ORIGIN_MISMATCH'); RuntimeError('RELEASE_CHANGED_DURING_EXECUTION'); ValueError('RUN_ID_REQUIRED') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: run. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_canonical()` (linhas 46–63) | Importa módulo canônico e recusa origem de fachada/implementação divergente; devolve helper ou helpers originais. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `run(request: object, *, run_id: str \| None=None) -> dict` (linhas 66–167) | Resolve calculate_binary_metrics e PerformanceMonitor; calcula AUC, KS percentual e Brier nas duas janelas. Instancia monitor com AUC referência e política dada, adiciona um período atual e obtém status/decisão; não executa a ação sugerida. Emite artifacts/Receipt para posterior finalização. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |

<a id="mt14-b1-code-map-file-021"></a>
#### hub-ml-monitoramento-modelo/scripts/verify.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-monitoramento-modelo/scripts/verify.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-monitoramento-modelo/scripts/verify.py`; SHA-256 `9956f0ed0f5ea82e8617306773247322c83be4d3263a9b149f39279023f006fe`; lote B1-03. |
| Por que existe | Recalcular drift com contagens independentes e comparar o Receipt. |
| Entradas e preparação | payload, expected_request e expected_run_id externos. |
| Mecanismo interno | Revalida janelas; reconstrói quantis, intervalos com empate à direita e bucket null; calcula PSI por contagem, D pela diferença de distribuições acumuladas empíricas, e p-value por scipy.stats.ks_2samp. Confere metadados/recurso/Receipt/release. |
| Retorno e interpretação | valid/status/issues e completion/promotion false. |
| Dependências diretas | from __future__ import annotations; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; import numpy as np; from scipy.stats import ks_2samp; from hub_scripts.skill_execution.receipt import verify_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-021); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | NumPy/SciPy e processamento local; nenhum Spark ou efeito remoto. |
| Consumidor/leitor | Revisor do resultado DRIFT_NUMERIC_LOCAL_V1. |
| Limites e custo | Oráculo de D é separado do helper; p usa a mesma família SciPy, portanto não é validação estatística independente de toda a biblioteca. Custo de _ks_oracle cresce com pontos×amostras. |
| Exemplo e contraexemplo | Ilustrativo: contar um empate no intervalo esquerdo muda PSI_ORACLE_MISMATCH; contagem de ausentes adulterada falha WINDOW_BINDING_MISMATCH. |
| Exceções e falhas levantadas | RuntimeError('RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH'); ValueError('EXPECTED_REQUEST_INVALID'); ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('PAYLOAD_NOT_CANONICAL_PASS'); ValueError('RESULT_SCHEMA_MISMATCH'); ValueError('WINDOWS_NOT_OBJECT') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_ks_oracle(reference: list[float], current: list[float]) -> float` (linhas 16–19) | Calcula em Python máximo da diferença entre funções de distribuição acumulada empíricas; devolve D float, sem p-value. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `verify(payload: object, *, expected_request: dict, expected_run_id: str) -> dict` (linhas 22–112) | Revalida janelas; reconstrói quantis, intervalos com empate à direita e bucket null; calcula PSI por contagem, D pela diferença de distribuições acumuladas empíricas, e p-value por scipy.stats.ks_2samp. Confere metadados/recurso/Receipt/release. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |

<a id="mt14-b1-code-map-file-022"></a>
#### hub-ml-monitoramento-modelo/scripts/verify_performance.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-monitoramento-modelo/scripts/verify_performance.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-monitoramento-modelo/scripts/verify_performance.py`; SHA-256 `639b001d8ddff865af2fe1825460c21a8a05bf2f2b5dca47780f95d31a0e7890`; lote B1-03. |
| Por que existe | Recalcular métricas e encerrar somente o diagnóstico de desempenho local. |
| Entradas e preparação | payload, expected_request e expected_run_id; threshold externo já validado. |
| Mecanismo interno | _metrics usa pares positivo/negativo com meio ponto em empate para AUC, diferença de distribuições para KS e erro quadrático para Brier. _reported_metrics aceita grade de 4 decimais ou 1 em KS, erro até meia unidade de arredondamento; valores reportados válidos alimentam a política. verify liga metadados/Receipt; finalize constrói handoff/Postflight e verify_finalized os reconfere. |
| Retorno e interpretação | verify: valid/issues/receipt_verification e completion false; finalize: cópia com possível scope_completion_authorized; verify_finalized: escopo LOCAL_SYNTHETIC_MATURE_PERFORMANCE_V1, business_readiness NOT_EVALUATED. |
| Dependências diretas | from __future__ import annotations; import copy; import json; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution.postflight import build_postflight; from hub_scripts.skill_execution.postflight import verify_postflight; from hub_scripts.skill_execution.receipt import verify_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-021); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Cálculo Python e cópia em memória; sem retreino ou efeito persistente. |
| Consumidor/leitor | Operador e revisão da conclusão local de performance. |
| Limites e custo | AUC por pares tem custo quadrático; máximo 1.000 linhas por janela limita este perfil. Finalização não promove policy e não configura monitor recorrente. |
| Exemplo e contraexemplo | Ilustrativo: métrica fora da grade falha RESULT_ORACLE_MISMATCH:metrics; handoff sem limitation material não autoriza Postflight. |
| Exceções e falhas levantadas | RuntimeError('RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH'); ValueError('EXPECTED_REQUEST_INVALID'); ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('FINALIZE_REQUIRES_PASS'); ValueError('HANDOFF_MISSING'); ValueError('PAYLOAD_NOT_CANONICAL_PASS') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify, finalize, verify_finalized. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_metrics(rows: list[dict]) -> dict` (linhas 18–31) | Calcula oráculo bruto de AUC por pares, KS percentual e Brier; devolve dict numérico, sem arredondamento do helper. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_reported_metrics(reported: object, raw: dict) -> bool` (linhas 34–52) | Devolve bool se shape, finitude, grade decimal, limites e erro de arredondamento concordam com métricas brutas. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `verify(payload: object, *, expected_request: dict, expected_run_id: str) -> dict` (linhas 55–154) | _metrics usa pares positivo/negativo com meio ponto em empate para AUC, diferença de distribuições para KS e erro quadrático para Brier. _reported_metrics aceita grade de 4 decimais ou 1 em KS, erro até meia unidade de arredondamento; valores reportados válidos alimentam a política. verify liga metadados/Receipt; finalize constrói handoff/Postflight e verify_finalized os reconfere. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |
| `_contract() -> dict` (linhas 157–158) | Lê o contrato específico do perfil e devolve dict para Postflight; erro de arquivo/JSON pode propagar ao chamador. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_handoff(request: dict, result: dict) -> dict` (linhas 161–172) | Projeta identidade, população, contagens, evaluation_at e limitações em dict para encerramento local. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `finalize(payload: object, *, expected_request: dict, expected_run_id: str) -> dict` (linhas 175–191) | _metrics usa pares positivo/negativo com meio ponto em empate para AUC, diferença de distribuições para KS e erro quadrático para Brier. _reported_metrics aceita grade de 4 decimais ou 1 em KS, erro até meia unidade de arredondamento; valores reportados válidos alimentam a política. verify liga metadados/Receipt; finalize constrói handoff/Postflight e verify_finalized os reconfere. Retorno: cópia profunda do payload com handoff/Postflight e scope_completion_authorized calculado; pode lançar ValueError para payload não PASS. |
| `verify_finalized(payload: object, *, expected_request: dict, expected_run_id: str) -> dict` (linhas 194–217) | Chama verify para reverificar pedido, métricas, política, artifacts e Receipt. Reconstrói o handoff por _handoff(expected_request, result), compara seu digest, chama verify_postflight e exige scope_completion_authorized=true. Agrega divergências em issues; não calcula tracking nem relê modelo. Retorno: dict com valid, status VALID/INVALID, issues, scope=LOCAL_SYNTHETIC_MATURE_PERFORMANCE_V1, business_readiness=NOT_EVALUATED e promotion_authorized=false. |

<a id="mt14-b1-code-map-file-023"></a>
#### hub-ml-pipeline-builder/scripts/preflight.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-pipeline-builder/scripts/preflight.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-pipeline-builder/scripts/preflight.py`; SHA-256 `139d50e09cc90d64539ec263411d9d8f507c4db22b267ee7474f5312b01665c7`; lote B1-04. |
| Por que existe | Conferir especificação sintética de pipeline e carregar seu template sem executá-la. |
| Entradas e preparação | SER13-SPEC-1, operação VALIDATE_SPEC, ambiente LOCAL_SYNTHETIC, escopo PERSONAL; main recebe --request. |
| Mecanismo interno | Valida schema, tipo inteiro exato de watermark, nomes sem whitespace, origem≠destino, chaves/event_time nas colunas, idempotência compatível com APPEND/MERGE e WATERMARK/BATCH. Confere origem do preflight, blobs antes/depois e lê template não vazio; verify_preflight recomputa e compara todo payload. |
| Retorno e interpretação | Payload com spec_validated/template_loaded, bindings, sef; permissions_verified/effects_authorized false, deployment_status NOT_RUN, receipt null; verify_preflight retorna valid/issues. |
| Dependências diretas | from __future__ import annotations; import json; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, loads_strict; from hub_scripts.skill_execution.domain_context.release import blob; import argparse; from jsonschema import Draft202012Validator; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-026); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leituras locais, resolução e stdout na CLI; sem Spark/deploy/escrita. |
| Consumidor/leitor | run_local._validate e operador que revisa uma proposta de pipeline. |
| Limites e custo | Permissões declaradas não são verificadas; APPEND válido como spec não implica suporte no runner local fixo MERGE. |
| Exemplo e contraexemplo | Ilustrativo: MERGE com REJECT_DUPLICATES falha IDEMPOTENCY_MODE_MISMATCH; BATCH exige watermark_seconds null. |
| Exceções e falhas levantadas | SystemExit(main()); ValueError('EVENT_TIME_NOT_IN_SCHEMA'); ValueError('IDEMPOTENCY_MODE_MISMATCH'); ValueError('IDENTIFIER_WHITESPACE_FORBIDDEN'); ValueError('INCREMENTAL_WATERMARK_MISMATCH'); ValueError('KEY_NOT_IN_SCHEMA'); ValueError('PREFLIGHT_IMPORT_ORIGIN_MISMATCH'); ValueError('RELEASE_CHANGED_DURING_PREFLIGHT'); ValueError('SEF_PREFLIGHT_BLOCKED'); ValueError('SOURCE_DESTINATION_MUST_DIFFER'); ValueError('SPEC_SCHEMA_INVALID:' + str(errors[0].validator)); ValueError('TEMPLATE_EMPTY'); ValueError('WATERMARK_INTEGER_REQUIRED') |
| Captura implementada | (OSError, UnicodeError, ValueError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: preflight, verify_preflight, main. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `preflight(request: object) -> dict` (linhas 15–71) | Valida schema, tipo inteiro exato de watermark, nomes sem whitespace, origem≠destino, chaves/event_time nas colunas, idempotência compatível com APPEND/MERGE e WATERMARK/BATCH. Confere origem do preflight, blobs antes/depois e lê template não vazio; verify_preflight recomputa e compara todo payload. Retorno: dict de decisão anterior à execução e bindings/SEF específicos da ficha; sem resultado analítico. |
| `verify_preflight(payload: object, *, expected_request: dict) -> dict` (linhas 74–82) | Valida schema, tipo inteiro exato de watermark, nomes sem whitespace, origem≠destino, chaves/event_time nas colunas, idempotência compatível com APPEND/MERGE e WATERMARK/BATCH. Confere origem do preflight, blobs antes/depois e lê template não vazio; verify_preflight recomputa e compara todo payload. Retorno: dict valid/issues/effects_authorized=false/deployment_status=NOT_RUN. |
| `main() -> int` (linhas 85–96) | Interpreta flags da linha de comando, lê JSON estrito e imprime resposta JSON; retorna exit code 0 no estado aceito e 1 em bloqueio/invalidez. Erros de argparse terminam a CLI. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |

| Interface de linha de comando | Contrato |
|---|---|
| Flag declarada | `parser.add_argument('--request', required=True, type=Path)` |
| Saída | JSON em stdout; exit code do estado calculado. Parsing da CLI pode encerrar com erro antes da lógica. Nenhuma CLI foi executada nesta edição. |

<a id="mt14-b1-code-map-file-024"></a>
#### hub-ml-pipeline-builder/scripts/run_delta.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-pipeline-builder/scripts/run_delta.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-pipeline-builder/scripts/run_delta.py`; SHA-256 `f41fd08f900f65e99ffbba9be66d5fcda6747dc56116cfb37dc4a1df6ca7c115`; lote B1-04. |
| Por que existe | Exercitar ciclo Delta autorizado em tabela sintética nova, com ownership antes da limpeza. |
| Entradas e preparação | execute recebe request/expected_rows/spark/authorization/run_id e compute_payload opcional; _execute_owned compartilhado recebe PIPELINE ou FE_PIT/provenance. |
| Mecanismo interno | Copia request/oráculo/autorização; valida efeito, alvo fechado, digest/run/nonce/principal/catalog/schema; confere release e computação upstream. Consulta identidade runtime, recusa alvo existente, cria tabela com markers, carrega dados, MERGE e replay, relê linhas; FE também lê history/table ID. Confere ownership, faz DROP e verifica ausência; tenta limpeza segura após falha sem repetir DROP incerto. |
| Retorno e interpretação | Registro de efeito SER14 ou SER08 com fase, hashes, criação tentada/confirmada, ownership_checks, cleanup, ausência final e status PASS/BLOCKED/UNKNOWN; não é Receipt novo. |
| Dependências diretas | from __future__ import annotations; import json; import re; import sys; import uuid; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, loads_strict, text; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from pyspark.sql.types import LongType, StringType, StructField, StructType; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-026); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | CREATE TABLE, INSERT/MERGE, replay, SELECT/readback, DESCRIBE, DROP e views temporárias, somente para efeito autorizado. É a superfície de escrita mais sensível deste mapa. |
| Consumidor/leitor | execute do Pipeline e run_pit_materialization de Feature Engineering. |
| Limites e custo | authorized=true no contrato é descrição, não permissão. Falha depois de tentativa de criação sem ausência comprovada gera UNKNOWN. Modelo de marcadores não autentica origem humana; cleanup só no alvo próprio. |
| Exemplo e contraexemplo | Ilustrativo: alvo existente falha TARGET_ALREADY_EXISTS; marker divergente impede DROP; perda de confirmação de DROP deixa DROP_UNCONFIRMED e exige inspeção antes de repetir. |
| Exceções e falhas levantadas | RuntimeError('DELTA_DETAIL_UNAVAILABLE'); RuntimeError('DELTA_HISTORY_UNAVAILABLE'); RuntimeError('DELTA_TABLE_ID_CHANGED'); RuntimeError('DELTA_TABLE_ID_INVALID'); RuntimeError('DELTA_VERSION_INVALID'); RuntimeError('DELTA_VERSION_REGRESSED'); RuntimeError('FE_READBACK_SCHEMA_INVALID'); RuntimeError('FE_READBACK_TYPE_INVALID'); RuntimeError('INITIAL_READBACK_MISMATCH'); RuntimeError('MERGE_READBACK_MISMATCH'); RuntimeError('MERGE_REPLAY_NOT_IDEMPOTENT'); RuntimeError('OWNED_TABLE_ABSENT'); RuntimeError('PROPERTY_RESULT_UNSUPPORTED'); RuntimeError('READBACK_ID_INVALID'); RuntimeError('READBACK_SCHEMA_INVALID'); RuntimeError('RELEASE_CHANGED_DURING_EFFECT'); RuntimeError('TABLE_OWNERSHIP_MARKERS_MISMATCH'); RuntimeError('TABLE_STILL_EXISTS_AFTER_DROP'); ValueError('AUTHORIZATION_SHAPE_INVALID'); ValueError('COMPUTE_RECEIPT_OR_OUTPUT_INVALID:' + str(verified['issues'])); ValueError('DELTA_EXECUTION_CONTRACT_BLOCKED'); ValueError('EFFECT_NOT_AUTHORIZED'); ValueError('EXPECTED_ROWS_NOT_MERGE_ORACLE'); ValueError('FE_EXPECTED_ROWS_MISMATCH'); ValueError('FE_PROFILE_INVALID'); ValueError('FE_PROVENANCE_INVALID'); ValueError('FE_REQUEST_INVALID'); ValueError('FREE_NAMESPACE_REQUIRED'); ValueError('NONCANONICAL_' + label); ValueError('NONCE_INVALID'); ValueError('OWNED_CLEANUP_REQUIRED'); ValueError('PROFILE_UNSUPPORTED'); ValueError('PROVENANCE_DIGEST_INVALID'); ValueError('REQUEST_DIGEST_MISMATCH'); ValueError('RUN_ID_BINDING_INVALID'); ValueError('SESSION_AUTHORITY_MISMATCH'); ValueError('TARGET_ALREADY_EXISTS'); ValueError('TARGET_INVALID'); ValueError('TARGET_OUTSIDE_FREE_SYNTHETIC_NAMESPACE'); ValueError('UTC_SPARK_SESSION_REQUIRED') |
| Captura implementada | (TypeError, ValueError, OverflowError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: execute. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_snapshot(value: object, label: str)` (linhas 46–53) | Serializa e relê JSON para desligar referências mutáveis do chamador; devolve cópia, recusando valores não representáveis. A variante de tracking também verifica ciclos e chaves explicitamente. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_local()` (linhas 55–58) | Carrega runner/verifier locais por arquivo; devolve par de módulos para conferir computação upstream. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_authorization(value: object, *, request: dict, run_id: str, effect_name: str='SYNTHETIC_DELTA_PROBE') -> dict` (linhas 61–86) | Valida autorização exata para o efeito, alvo, nonce, digest/run e principal/namespace esperados; devolve o registro conferido, sem autenticar seu emissor. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_quoted_target(value: str) -> str` (linhas 89–92) | Valida alvo fechado e devolve identificador SQL com cada componente entre crases; rejeita qualquer nome fora do padrão. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_markers(auth: dict, provenance: dict \| None=None) -> dict[str, str]` (linhas 95–106) | Deriva propriedades run_id/request_digest/nonce e proveniência opcional; confere hashes adicionais e devolve dict[str,str]. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_properties(spark, qualified: str) -> dict[str, str]` (linhas 109–117) | Executa SHOW TBLPROPERTIES e devolve mapa key→value; resultado sem essas colunas gera RuntimeError. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_assert_owned(spark, qualified: str, auth: dict, provenance: dict \| None=None) -> None` (linhas 120–126) | Exige tabela existente e todos os marcadores de ownership/proveniência iguais aos autorizados; retorna None ou lança erro, antes de limpar. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_rows(spark, qualified: str, *, profile: str='PIPELINE') -> list[dict]` (linhas 129–157) | Executa SELECT/readback e normaliza linhas pelo profile; retorna lista ordenada, convertendo ID string do Pipeline a int. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_temp_view(spark, rows: list[dict], name: str, *, profile: str='PIPELINE') -> None` (linhas 160–181) | Monta schema explícito PIPELINE ou FE_PIT e cria view temporária; retorna None e altera sessão Spark. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_delta_version(spark, qualified: str) -> int` (linhas 184–191) | Lê última versão DESCRIBE HISTORY, exige inteiro não negativo e devolve int. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_delta_table_id(spark, qualified: str) -> str` (linhas 194–201) | Lê DESCRIBE DETAIL e devolve ID não vazio da tabela Delta, recusando resultado inesperado. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_assert_fe_table_id(spark, qualified: str, expected_id: str \| None) -> None` (linhas 204–206) | Quando expected_id não é None, relê a identidade por _delta_table_id e exige igualdade. Retorna None no fluxo normal; levanta RuntimeError("DELTA_TABLE_ID_CHANGED") se a identidade divergir, evitando operar tabela substituída. Falhas da leitura também podem propagar. Retorno: None no fluxo normal, inclusive quando expected_id=None; divergência levanta RuntimeError. |
| `_execute_owned(request: dict, expected_rows: list[dict], spark, authorization: dict, *, run_id: str, compute_payload: dict \| None=None, profile: str='PIPELINE', provenance: dict \| None=None) -> dict` (linhas 209–429) | Copia request/oráculo/autorização; valida efeito, alvo fechado, digest/run/nonce/principal/catalog/schema; confere release e computação upstream. Consulta identidade runtime, recusa alvo existente, cria tabela com markers, carrega dados, MERGE e replay, relê linhas; FE também lê history/table ID. Confere ownership, faz DROP e verifica ausência; tenta limpeza segura após falha sem repetir DROP incerto. Retorno: dict de efeito Delta, específico a PIPELINE ou FE_PIT, mesmo quando falha; não emite Receipt novo. |
| `execute(request: dict, expected_rows: list[dict], spark, authorization: dict, *, run_id: str, compute_payload: dict \| None=None) -> dict` (linhas 432–436) | Copia request/oráculo/autorização; valida efeito, alvo fechado, digest/run/nonce/principal/catalog/schema; confere release e computação upstream. Consulta identidade runtime, recusa alvo existente, cria tabela com markers, carrega dados, MERGE e replay, relê linhas; FE também lê history/table ID. Confere ownership, faz DROP e verifica ausência; tenta limpeza segura após falha sem repetir DROP incerto. Retorno: dict de efeito PASS/BLOCKED/UNKNOWN; campos de fase, readback, cleanup e hashes detalhados na ficha. |

<a id="mt14-b1-code-map-file-025"></a>
#### hub-ml-pipeline-builder/scripts/run_local.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-pipeline-builder/scripts/run_local.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-pipeline-builder/scripts/run_local.py`; SHA-256 `d740486aacba4c6cc303f3e554577e9875acf35e02c1e8e1b72c2bee3676c341`; lote B1-04. |
| Por que existe | Executar MERGE lógico limitado no Spark e comparar com oráculo Python. |
| Entradas e preparação | SER13-LOCAL-RUN-1/RUN_LOCAL_SPARK com spec, prior_rows (pode vazio), batch_rows (não vazio), spark e run_id. |
| Mecanismo interno | _validate exige spec fixa MERGE/BATCH, id/event_at/value, sem watermark, até 100 IDs; _rows valida tipos/limites/UTC. _merge escolhe evento mais recente e recusa empate diferente. run reproduz por union/window Spark, cria view temporária exclusiva, chama data_quality_check, confere collect e remove view antes do Receipt; finally trata resíduo. |
| Retorno e interpretação | Resultado com rows ordenadas, digests/spec/qualidade/replay_semantics; persistent_write=false/deployment_status NOT_RUN; envelope Receipt. |
| Dependências diretas | from __future__ import annotations; import importlib; import re; import sys; import uuid; from datetime import datetime; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution import run_preflight; from pyspark.sql.types import LongType, StringType, StructField, StructType; from pyspark.sql import Window, functions as F; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-026); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Ações Spark e criação/remoção de view temporária; writes_performed=false significa ausência de escrita persistente, não ausência total de alteração de sessão. |
| Consumidor/leitor | verify_local e execução Delta, que primeiro exige computação verificável. |
| Limites e custo | Não é MERGE Delta remoto; timestamps string têm formato UTC estrito de segundos; output limitado a 100 IDs. Falha de cleanup retorna BLOCKED mesmo após cálculo. |
| Exemplo e contraexemplo | Ilustrativo: mesmo id/event_at com value diferente é EQUAL_EVENT_TIME_CONFLICT; lote mais antigo conserva registro atual. |
| Exceções e falhas levantadas | RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH'); RuntimeError('RELEASE_CHANGED_DURING_EXECUTION'); RuntimeError('SPARK_OUTPUT_MISMATCH'); RuntimeError('TEMP_VIEW_ALREADY_EXISTS'); RuntimeError('TEMP_VIEW_CLEANUP_FAILED'); ValueError('EQUAL_EVENT_TIME_CONFLICT'); ValueError('LOCAL_RUN_CONTRACT_BLOCKED'); ValueError('OUTPUT_ROWS_BOUND_EXCEEDED'); ValueError('QUALITY_CHECK_FAILED'); ValueError('ROWS_BOUNDED_REQUIRED'); ValueError('ROW_EVENT_AT_INVALID'); ValueError('ROW_KEY_INVALID_OR_DUPLICATED'); ValueError('ROW_SCHEMA_INVALID'); ValueError('ROW_VALUE_INVALID'); ValueError('RUN_ID_REQUIRED'); ValueError('RUN_PROFILE_REQUIRES_FIXED_MERGE_SCHEMA'); ValueError('RUN_REQUEST_PROFILE_INVALID'); ValueError('RUN_REQUEST_SCHEMA_INVALID'); ValueError('SPEC_PREFLIGHT_BLOCKED'); ValueError() |
| Captura implementada | Exception; ValueError; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: run. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_preflight()` (linhas 42–43) | Carrega o arquivo irmão de preflight via importlib; devolve módulo. Carregar executa código de importação, sem chamar o runner. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_primitive()` (linhas 46–53) | Resolve a primitive canônica pelo módulo e arquivo exatos; devolve callable, sem executar a análise. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_rows(rows: object, *, allow_empty: bool) -> list[dict]` (linhas 56–76) | Confere até 100 linhas, shape fixo, inteiros limitados, chave única e timestamp UTC; retorna lista original validada. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_validate(request: object) -> tuple[dict, dict]` (linhas 79–98) | Valida envelope de execução local, chama preflight da spec e exige MERGE/BATCH/schema fixo/limites de linhas; devolve (spec, domain). Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_merge(prior: list[dict], batch: list[dict]) -> list[dict]` (linhas 101–109) | Constrói cópia do estado por ID; escolhe evento mais novo, mantém antigo em lote atrasado e recusa empate conflitante; devolve lista ordenada. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `run(request: object, spark, *, run_id: str) -> dict` (linhas 112–217) | _validate exige spec fixa MERGE/BATCH, id/event_at/value, sem watermark, até 100 IDs; _rows valida tipos/limites/UTC. _merge escolhe evento mais recente e recusa empate diferente. run reproduz por union/window Spark, cria view temporária exclusiva, chama data_quality_check, confere collect e remove view antes do Receipt; finally trata resíduo. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |

<a id="mt14-b1-code-map-file-026"></a>
#### hub-ml-pipeline-builder/scripts/verify_local.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-pipeline-builder/scripts/verify_local.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-pipeline-builder/scripts/verify_local.py`; SHA-256 `e7767597006b46ead4557766275b74ab7032fa822ab667784f9f88a10c3fe0fd`; lote B1-04. |
| Por que existe | Vincular o MERGE local a linhas esperadas independentes e ao Receipt. |
| Entradas e preparação | payload; expected_request, expected_rows e expected_run_id. |
| Mecanismo interno | Revalida spec/pedido e expected_rows canônicas ordenadas/únicas; compara resultado completo, qualidade esperada, chamadas/effects no trace, Receipt e release. |
| Retorno e interpretação | valid/status/issues/scope e completion/promotion false. |
| Dependências diretas | from __future__ import annotations; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; from hub_scripts.skill_execution.receipt import verify_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-026); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leituras locais; validações Python, sem Spark e sem execução do MERGE. |
| Consumidor/leitor | Operador do perfil local e run_delta._execute_owned. |
| Limites e custo | As linhas externas são um oráculo confiado; este verifier não recalcula _merge. Engine Delta acrescenta a igualdade com _merge antes de escrever. |
| Exemplo e contraexemplo | Ilustrativo: expected_rows fora de ordem causa EXPECTED_ROWS_NOT_CANONICAL; adulteração de output falha TRUSTED_OUTPUT_ORACLE_MISMATCH. |
| Exceções e falhas levantadas | ValueError('EXPECTED_ROWS_NOT_CANONICAL'); ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('PAYLOAD_NOT_CANONICAL_PASS') |
| Captura implementada | Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `verify(payload: object, *, expected_request: dict, expected_rows: list[dict], expected_run_id: str) -> dict` (linhas 15–72) | Revalida spec/pedido e expected_rows canônicas ordenadas/únicas; compara resultado completo, qualidade esperada, chamadas/effects no trace, Receipt e release. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |

<a id="mt14-b1-code-map-file-027"></a>
#### hub-ml-validacao-estatistica/scripts/preflight.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-validacao-estatistica/scripts/preflight.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-validacao-estatistica/scripts/preflight.py`; SHA-256 `a7f79593a6102775f9717b6af362b207b5d365068cbfbca612a3ddb55878f584`; lote B1-04. |
| Por que existe | Validar comparação KS pré-declarada de duas amostras contínuas independentes sintéticas. |
| Entradas e preparação | SER04-REQUEST-1 com população/unidade/pergunta, hipótese/independência/multiplicidade, alpha, reference/comparison e requested_effect NONE. |
| Mecanismo interno | Fecha pedido; fixa hipótese bicaudal, estimando de diferença máxima entre distribuições acumuladas e comparação única. Exige alpha finito entre 0 e 1, 4–10.000 números por grupo, conversão float64 exata para inteiros e nenhum empate dentro/entre grupos; resolve calculate_ks. |
| Retorno e interpretação | validate_request: status/issues/digest/tamanhos e helper_called/writes false; preflight soma sef/bindings; main retorna 0/1 e imprime JSON. |
| Dependências diretas | from __future__ import annotations; import json; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import ContextError, closed, digest, loads_strict, text; from hub_scripts.skill_execution.domain_context.release import blob; import argparse; from hub_scripts.skill_execution import run_preflight |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-030); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leitura local e validação, nenhuma chamada estatística. |
| Consumidor/leitor | run.py, verify.py e CLI para inspeção antes da estatística. |
| Limites e custo | Independência/IID/continuidade são declarações do desenho, não propriedades provadas pelo parser; perfil não corrige múltiplas comparações. |
| Exemplo e contraexemplo | Fixture [1,2,3,4] versus [5,6,7,8] é exemplo sintético; repetir 4 no segundo grupo gera POOLED_FLOAT64_TIES_UNSUPPORTED. |
| Exceções e falhas levantadas | ContextError('ALPHA:INVALID'); ContextError('POOLED_FLOAT64_TIES_UNSUPPORTED'); ContextError('PROFILE:UNSUPPORTED:' + key); ContextError(key.upper() + ':BOUNDED_SAMPLE_REQUIRED'); ContextError(key.upper() + ':FINITE_NUMBERS_REQUIRED'); ContextError(key.upper() + ':FLOAT64_PRECISION_LOSS'); ContextError(key.upper() + ':FLOAT64_TIES_UNSUPPORTED'); RuntimeError('SEF_PREFLIGHT_IMPORT_ORIGIN_MISMATCH'); SystemExit(main()) |
| Captura implementada | (ContextError, TypeError, ValueError, OverflowError); (OSError, UnicodeError, ValueError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: validate_request, preflight, main. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `validate_request(request: object) -> dict` (linhas 28–61) | Fecha pedido; fixa hipótese bicaudal, estimando de diferença máxima entre distribuições acumuladas e comparação única. Exige alpha finito entre 0 e 1, 4–10.000 números por grupo, conversão float64 exata para inteiros e nenhum empate dentro/entre grupos Retorno: dict de decisão de domínio, com status PASS/BLOCKED, issues, digest e campos específicos da ficha. |
| `preflight(request: object) -> dict` (linhas 64–86) | Chama validate_request; em PASS resolve contrato por run_preflight, confere origem e registra bindings locais; devolve BLOCKED se domínio ou resolução falharem. Retorno: dict de decisão anterior à execução e bindings/SEF específicos da ficha; sem resultado analítico. |
| `main() -> int` (linhas 89–99) | Interpreta flags da linha de comando, lê JSON estrito e imprime resposta JSON; retorna exit code 0 no estado aceito e 1 em bloqueio/invalidez. Erros de argparse terminam a CLI. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |

| Interface de linha de comando | Contrato |
|---|---|
| Flag declarada | `parser.add_argument('--request', required=True, type=Path)` |
| Saída | JSON em stdout; exit code do estado calculado. Parsing da CLI pode encerrar com erro antes da lógica. Nenhuma CLI foi executada nesta edição. |

<a id="mt14-b1-code-map-file-028"></a>
#### hub-ml-validacao-estatistica/scripts/run.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-validacao-estatistica/scripts/run.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-validacao-estatistica/scripts/run.py`; SHA-256 `f6a62f5f96ecc7d9fbf65f9a06c118d335c807560eab28335eda00eadd4228fc`; lote B1-04. |
| Por que existe | Calcular teste KS delimitado e registrar estatística, decisão e limites. |
| Entradas e preparação | request validado e run_id opcional UUID; CLI exige --request e --run-id. |
| Mecanismo interno | Valida release/preflight, origem de calculate_ks e execução canônica; chama helper, exige D/p finitos em [0,1], registra tamanhos, D também como effect_size_D, método SCIPY_KS_2SAMP_AUTO e decisão p≤alpha. Reconferência da release antecede Receipt. |
| Retorno e interpretação | SER04-RESULT-1 com statistic_D, effect_size_D, p_value, decision, confidence_interval null/UNSUPPORTED_IN_PROFILE, diagnostic scope e Receipt. |
| Dependências diretas | from __future__ import annotations; import importlib; import json; import math; import sys; import uuid; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, loads_strict; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; import argparse; from hub_scripts.skill_execution.receipt import build_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-030); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Computação estatística local e saída CLI; sem escrita persistente, publicação ou efeito remoto. |
| Consumidor/leitor | verify.py exige estatística e p-value externos ao resultado. |
| Limites e custo | Não rejeitar H0 não prova igualdade; D é diferença entre distribuições, não efeito causal. Sem intervalo de confiança nem outros testes neste perfil. |
| Exemplo e contraexemplo | Ilustrativo analítico: fixture separada tem D=1 e p bilateral exato 1/35; não foi executada nesta edição. |
| Exceções e falhas levantadas | RuntimeError('CANONICAL_RECEIPT_NOT_ISSUED'); RuntimeError('PRIMITIVE_IMPLEMENTATION_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_IMPORT_ORIGIN_MISMATCH'); RuntimeError('PRIMITIVE_NONFINITE_RESULT'); RuntimeError('PRIMITIVE_RESULT_RANGE'); RuntimeError('RECEIPT_IMPORT_ORIGIN_MISMATCH'); RuntimeError('RELEASE_CHANGED_DURING_EXECUTION'); SystemExit(main()); ValueError('RUN_ID_REQUIRED') |
| Captura implementada | (OSError, UnicodeError, ValueError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: run, main. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `_preflight_module()` (linhas 37–38) | Carrega o preflight irmão e devolve seu módulo; nenhuma análise executada nesta função. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `_canonical_primitive()` (linhas 41–50) | Importa a primitive esperada e confere arquivo de implementação; devolve callable ou lança erro de origem. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |
| `run(request: object, *, run_id: str \| None=None) -> dict` (linhas 53–129) | Valida release/preflight, origem de calculate_ks e execução canônica; chama helper, exige D/p finitos em [0,1], registra tamanhos, D também como effect_size_D, método SCIPY_KS_2SAMP_AUTO e decisão p≤alpha. Reconferência da release antecede Receipt. Retorno: envelope PASS/BLOCKED, preflight, trace, result e receipt; perfis L4 locais acrescentam artifacts/handoff/postflight/flag de conclusão. |
| `main() -> int` (linhas 132–143) | Interpreta flags da linha de comando, lê JSON estrito e imprime resposta JSON; retorna exit code 0 no estado aceito e 1 em bloqueio/invalidez. Erros de argparse terminam a CLI. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |

| Interface de linha de comando | Contrato |
|---|---|
| Flag declarada | `parser.add_argument('--request', required=True, type=Path)` |
| Flag declarada | `parser.add_argument('--run-id', required=True)` |
| Saída | JSON em stdout; exit code do estado calculado. Parsing da CLI pode encerrar com erro antes da lógica. Nenhuma CLI foi executada nesta edição. |

<a id="mt14-b1-code-map-file-029"></a>
#### hub-ml-validacao-estatistica/scripts/verify.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-validacao-estatistica/scripts/verify.py) · [Campos B1](MT-mt15-b1-field-map.md#mt15-b1-field-map)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Identidade | `ambiente_databricks/.assistant/skills/hub-ml-validacao-estatistica/scripts/verify.py`; SHA-256 `fc8291c9c3d990f74c42b6c4629c5c2c204a6f2442e87610b5146549d4b85bd4`; lote B1-04. |
| Por que existe | Conferir o teste KS contra oráculo externo e versão corrente da release. |
| Entradas e preparação | payload; expected_request/run_id/statistic/p_value. main(argv=None) aceita cinco flags obrigatórias de arquivos, ID e números. |
| Mecanismo interno | Revalida pedido/preflight; compara metadados, D/effect_size_D/p com tolerância 1e-12 e decisão derivada do p externo; confere Receipt/release. CLI lê payload/request e recusa oráculo não finito antes da chamada. |
| Retorno e interpretação | valid/status/issues/scope e completion/promotion false; CLI imprime JSON e retorna 0/1. |
| Dependências diretas | from __future__ import annotations; import json; import math; import sys; from pathlib import Path; from hub_scripts.skill_execution.domain_context import digest, loads_strict; from hub_scripts.skill_execution.domain_context.release import load_sibling, release_integrity; import argparse; from hub_scripts.skill_execution.receipt import verify_execution_receipt |
| Dependências vinculadas por release | [Manifesto da família](MT-mt15-b1-field-map.md#mt15-b1-field-map-file-030); contém paths e blobs das dependências diretas/transitivas protegidas. Ler o manifesto não executa seus arquivos. |
| Efeitos | Leituras locais e comparações, sem calculate_ks ou efeito remoto. |
| Consumidor/leitor | Revisor da estatística e do vínculo da execução. |
| Limites e custo | Não constrói o oráculo nem verifica o desenho amostral; a API direta depende de valores esperados confiáveis. Passar valores copiados do payload não é verificação independente. |
| Exemplo e contraexemplo | Ilustrativo: expected_statistic=0 para fixture separada causa TRUSTED_ORACLE_MISMATCH:statistic_D, embora um digest do resultado possa ser íntegro. |
| Exceções e falhas levantadas | RuntimeError('RECEIPT_VERIFIER_IMPORT_ORIGIN_MISMATCH'); SystemExit(main()); ValueError('EXPECTED_REQUEST_INVALID'); ValueError('EXPECTED_RUN_ID_REQUIRED'); ValueError('ORACLE_NONFINITE'); ValueError('PAYLOAD_NOT_CANONICAL_PASS'); ValueError('RESULT_NOT_OBJECT') |
| Captura implementada | (OSError, UnicodeError, ValueError); Exception; não converter ausência de dependência em aprovação. |
| Classificação dos símbolos | Sem sublinhado inicial: verify, main. Nomes com sublinhado são internos; a ausência de sublinhado não assegura API pública suportada ou estável. |

| Símbolo e assinatura real | Mecanismo, retorno e consumo |
|---|---|
| `verify(payload: object, *, expected_request: dict, expected_run_id: str, expected_statistic: float, expected_p_value: float) -> dict` (linhas 17–90) | Revalida pedido/preflight; compara metadados, D/effect_size_D/p com tolerância 1e-12 e decisão derivada do p externo; confere Receipt/release. CLI lê payload/request e recusa oráculo não finito antes da chamada. Retorno: dict de verificação, valid/status/issues e limites de autoridade indicados na ficha. |
| `main(argv: list[str] \| None=None) -> int` (linhas 93–118) | Interpreta flags da linha de comando, lê JSON estrito e imprime resposta JSON; retorna exit code 0 no estado aceito e 1 em bloqueio/invalidez. Erros de argparse terminam a CLI. Retorno: Retorno descrito no mecanismo; sem anotação adicional inferida. |

| Interface de linha de comando | Contrato |
|---|---|
| Flag declarada | `parser.add_argument('--payload', required=True, type=Path)` |
| Flag declarada | `parser.add_argument('--request', required=True, type=Path)` |
| Flag declarada | `parser.add_argument('--run-id', required=True)` |
| Flag declarada | `parser.add_argument('--expected-statistic', required=True, type=float)` |
| Flag declarada | `parser.add_argument('--expected-p-value', required=True, type=float)` |
| Saída | JSON em stdout; exit code do estado calculado. Parsing da CLI pode encerrar com erro antes da lógica. Nenhuma CLI foi executada nesta edição. |


<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
