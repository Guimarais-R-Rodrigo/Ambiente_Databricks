# SER13 / SER14 — hub-ml-pipeline-builder

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Validar especificação operacional e só declarar deploy/write/run quando um executor canônico realizar e verificar a ação no destino autorizado.

Superfícies: pipeline_spec (L2); deploy_or_write (L4/authorization).

## 2. Reuso e inventário de autoria

Matriz registra data_quality_check, schema_to_yaml, naming_checker, safe_display e templates/pipeline_spec.md. São diagnósticos/templates, não executor de deploy. A rota de efeito deve ser implementada/provada antes da SER14.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Ambiente/host; origem/destino; objeto; modo de escrita; incrementalidade; chave; idempotência; permissões observadas; job/schedule quando solicitado; rollback/cleanup; ação exata e autorização; escopo pessoal.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: pipeline_spec validada sem deploy. L4: preflight, authorization binding, tentativa com request hash, IDs/versões remotas, retorno e readback, Receipt/Postflight e estado de resíduo. Não registrar segredo no request.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

PB-B01: escolher a primeira operação real suportada e seu executor após inspeção de capacidade do Free. PB-B02: fechar semântica de idempotência e readback após timeout. PB-B03: autorização de destination/overwrite/schedule é material e fica no formulário único de efeito; não pode ser escolhida pelo worker.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta PB-F01: spec sintética válida para um destino temporário pessoal, com autorização inicialmente ausente. O positivo L2 deve validar a spec e não escrever; o negativo de L4 sem autorização deve bloquear. O positivo real de L4 só será congelado após escolher operação/destino suportados; um servidor mock pode testar protocolo/erro, mas não substitui prova real no Free.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| PB01 | Ambiente/destino | Trocar por corporativo/prod ou destino não autorizado. | Recusar antes de qualquer efeito. |
| PB02 | Permissão desconhecida | Inferir write permission a partir de login. | UNKNOWN bloqueia ação. |
| PB03 | Defaults de operação | Assumir overwrite/schedule/rollback. | Exigir decisão material sem efetuar ação. |
| PB04 | Spec sem execução | Retornar deploy completed. | Postflight reprova false completion. |
| PB05 | Autorização stale | Usar em candidato ou destino B. | Reject anterior à escrita. |
| PB06 | Efeito parcial/timeout | Falhar após criação parcial. | PARTIAL/UNKNOWN, preservar request/result/resíduos. |
| PB07 | Run sem retorno | Objeto/run não encontrado ou sem estado final verificável. | Não declarar concluído. |
| PB08 | Transporte após efeito | Executor tenta repetir POST. | Somente read-only reconciliação; tentativa antiga falha permanece. |
| PB09 | Cleanup falho | Negar delete/falhar limpeza. | Resíduo preservado e declarado; sem rollback completo. |
| PB10 | Capacidade indisponível | Usar dry-run/mock para fechar L4. | Bloquear superfície não comprovada. |
| PB11 | Idempotency key | Mesma key com payload diferente. | Rejeitar colisão; não sobrescrever silenciosamente. |
| PB12 | Validação final observável | Readback difere de spec/bytes aprovados. | Postflight rejeita apesar de exit/HTTP sucesso. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Validar schemas/spec/naming e adapters de autorização; protocolos de efeito em sandbox mock rotulados como mock. Tests de failure-after-write exigem backend real isolado quando essa capacidade for declarada local.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Uma ação sintética mínima aprovada (por exemplo operação de artefato ou job somente se suportada e autorizada), verificada por leitura no destino e com cleanup separado. Não presumir APIs/quotas/permissões do workspace. Falta de capacidade permite encerrar L2 e deixar SER14 bloqueada, não inventar L4.

Roteiro Genie mínimo: PB-G01, PB-G02, PB-G03, PB-G04, PB-G05, PB-G06, PB-G07, PB-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Fora: trabalho/prod, schedules recorrentes não solicitados, overwrite de ativos existentes, concessão de permissão, uso de fontes reais ou ações de infraestrutura sem aprovação. A promoção não pode fundir spec e deploy num único status.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.
