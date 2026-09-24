# SER05 / SER06 — hub-ml-cross-eda-ml

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L4**, `stage_specific`.

## 1. Objetivo e superfície

Validar grão/cardinalidade/cobertura e realizar join temporal somente quando aplicável, com disponibilidade até a decisão e conclusão fail-closed.

Superfícies: join_diagnostics (L3); point_in_time_join (L4); contexto/preflight L2 antecede ambas.

## 2. Reuso e inventário de autoria

Candidatos: hub_snippets.spark.join_diagnostics::diagnosticar_join e hub_snippets.spark.pit_join::pit_join. A matriz descreve atraso_publicacao_dias constante obrigatório, fuso e empate; verificar assinaturas/retornos atuais antes do adapter.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Fontes A/B e identidades; grão/unidade; chaves; cardinalidade pretendida; período; colunas de decisão, referência e disponibilidade; atraso permitido; timezone; empate; necessidade de PIT; população de saída esperada.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

L2: contexto resolvido sem join material. L4: diagnóstico pré-join, parâmetros, resultado e métricas de cardinalidade/cobertura; disponibilidade observada; Receipt; Postflight vinculado ao output.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

CE-B01: contrato temporal compartilhado é único, consumido por features, com versão própria. CE-B02: latência variável ou bitemporalidade não representável pelo helper atual bloqueia o perfil; não substituir por atraso médio/zero. CE-B03: fechar fronteiras e política de empate antes de executar.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta CE-F01: uma decisão por entidade em 2026-01-10T00:00:00Z. Fonte tem linhas com disponibilidade 2026-01-09, exatamente 2026-01-10 e 2026-01-11. O perfil precisa declarar explicitamente <= ou <; com <=, somente as duas primeiras são elegíveis, e o desempate definido seleciona uma quando a relação esperada é N:1. Fixture independente de cardinalidade contém duas linhas de cada lado na mesma chave: mutante de join 2×2 deve ser detectado quando 1:1 é exigido.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| CE01 | Contexto L2 | Chave/fonte/grão ausente ou ambíguo. | Bloquear antes de join. |
| CE02 | PIT triestado | Tentar converter desconhecido em falso. | Unknown bloqueia; false legítimo tem rota não temporal. |
| CE03 | Cardinalidade | Dados causam multiplicação/perda inesperada. | Diagnóstico/Postflight bloqueiam saída não conforme. |
| CE04 | Disponibilidade futura | Mutante usa linha disponível após a decisão. | Nenhuma linha de futuro aceita. |
| CE05 | Fronteira/fuso/empate | Trocar timezone, igualdade ou desempate. | Output diverge do oráculo e é reprovado. |
| CE06 | Latência variável | Forçar helper de atraso constante. | Recusar capacidade não coberta. |
| CE07 | Bitemporalidade | Usar apenas um relógio. | Bloquear sem overclaim de PIT. |
| CE08 | Replay de join | Reusar Receipt trocando keys/datasets/corte. | Verifier rejeita. |
| CE09 | Finalizer omitido | Omitir Postflight/disponibilidade verificada. | Sem completion L4. |
| CE10 | Join não temporal | Forçar necessidade de PIT. | Não bloquear indevidamente; executar apenas escopo aplicável. |
| CE11 | Nulos e duplicatas | Coalescer nulos como chave igual não autorizada. | Detectar alteração da unidade/cardinalidade. |
| CE12 | PIT cross-skill | Adapter CE e FE interpretam cutoff diferente. | Integração reprova divergência. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

SER05 pode usar contexto/fixtures puras para provar L2 sem Spark. SER06 exige implementação/runtime Spark qualificável; um mock serve a branches do preflight, não a semântica do join. Saídas ordenadas para comparação por IDs; tolerância de timestamp=0 após normalização de timezone do contrato.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Spark real, contagens/IDs/availability comparados antes e depois. Nenhuma tabela permanente é necessária para o positivo mínimo do join read-only. Capturar sessões/fuso e query plan quando ajudar, sem dados de trabalho.

Roteiro Genie mínimo: CE-G01, CE-G02, CE-G03, CE-G04, CE-G05, CE-G06, CE-G07, CE-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Join simples com PIT não aplicável não deve ser forçado a temporal. Latência variável e bitemporalidade permanecem fora até implementation/prova. Não escrever fontes nem destino material para provar apenas diagnóstico.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.
