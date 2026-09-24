# SER07 / SER08 — hub-ml-feature-engineering

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Garantir que transformações históricas e fit usam apenas informação permitida, com materialização explicitamente autorizada e conclusão verificada.

Superfícies: point_in_time_features (L4); materialization (L4); L2 temporal/read-only é marco próprio.

## 2. Reuso e inventário de autoria

Candidatos da matriz: pit_join; create_temporal_features; date_features; woe_iv_calculator; rfv_calculator; temporal_split. Revalidar façades, schemas e efeitos; nem todos serão obrigatórios em toda tarefa.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Entidade/grão; cutoff/horizonte; janela e fronteiras; event_time e availability; origem/schema; treino/teste; transformação/fit; destino/modo; intenção de materializar; autorização; idempotência e rollback.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: contrato temporal e intenção. L4: features/linhas/ordem, fit boundary, proveniência, parâmetros, Receipt; se houver efeito aprovado, destino/versionamento e leitura pós-write; Postflight que distingue cálculo de materialização.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

FE-B01: inventariar quais transformadores têm API pública efetiva e suporte ao train-only fit. FE-B02: criar ou selecionar materializer canônico com autorização, verificação e cleanup; sua inexistência impede promover a superfície materialization. FE-B03: não duplicar contrato PIT da CE.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta FE-F01: cutoff no dia 10, janela inclusiva [dia 7, dia 10], evento de valor 2 no dia 8 disponível no dia 8, valor 5 no dia 9 disponível no dia 11, valor 7 no dia 11 disponível no dia 11. Soma elegível=2, não 7 nem 14. Variante de fit: treino x=(0,2), teste x=(100); transformador com média no treino deve registrar mean=1; um fit global altera esse valor e deve ser detectado. São oráculos para operações expressamente incluídas no catálogo final, não imposição de um transformador universal.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| FE01 | Contexto temporal | Cutoff/horizonte/availability ausentes ou contraditórios. | L2 bloqueia. |
| FE02 | Fronteira/futuro | Incluir evento fora da janela/futuro. | Valor/IDs reprovados por oráculo. |
| FE03 | Fonte tardia | Usar event_time ignorando availability. | Excluir evento tardio. |
| FE04 | Fit fora do treino | Ajustar WOE/scaler no conjunto total. | Fit provenance/resultado reprova leakage. |
| FE05 | Ordem/população | Trocar ordem/IDs após cálculo. | Binding mismatch. |
| FE06 | Write sem autoridade | Persistir apesar de missing auth. | Recusar antes da escrita. |
| FE07 | Destino/modo | Trocar path/tabela ou overwrite não autorizado. | Recusar efeito divergente. |
| FE08 | Escrita parcial | Falhar após parte dos dados/metadata. | PARTIAL/UNKNOWN, sem completion; estado preservado. |
| FE09 | Cleanup incompleto | Falhar cleanup/rollback. | Registrar resíduo; não homologar recuperação. |
| FE10 | Materializer ausente | Substituir por spec ou mock. | Bloquear promoção dessa superfície. |
| FE11 | Idempotência | Reexecução após sucesso/efeito desconhecido. | Sem duplicação; seguir regra explícita de reconciliação. |
| FE12 | Disponibilidade partilhada | Alterar timezone/lag só em FE. | Falha de integração temporal. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

L2 independente de Spark; cálculo/fit com backend específico qualificado; efeitos em sandbox temporária exclusiva com snapshots. Não mockar a escrita positiva ao reivindicar materialização real.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Execução temporal real e uma materialização sintética num destino pessoal explícito, com leitura/versionamento e cleanup aprovado. Sem capacidade/destino autorizado, materialization fica BLOCKED, mesmo que features read-only passem.

Roteiro Genie mínimo: FE-G01, FE-G02, FE-G03, FE-G04, FE-G05, FE-G06, FE-G07, FE-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não transforma toda hipótese criativa de feature em algoritmo fixo. Materialização não solicitada não autoriza write; ausência de materializer não é NA para a promoção da superfície. Sem target real de clientes.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.
