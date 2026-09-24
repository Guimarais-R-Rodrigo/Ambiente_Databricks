# SER03 — hub-ml-analise-safra

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L3**, `stage_specific`.

## 1. Objetivo e superfície

Calcular tabela safra×MOB e incidência no domínio binário efetivamente suportado, preservando denominador, cobertura, periodicidade e significado de cumulatividade.

Superfícies: calendar_derivation (L2); vintage_core (L3).

## 2. Reuso e inventário de autoria

Candidatos de reuso: hub_snippets.ml.vintage_analysis::build_vintage_table e compare_safras; calendário em spark.date_features somente quando necessário e após inspeção. A matriz SER00 descreve pandas, mês/trimestre, MOB não negativo e target 0/1.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Unidade/ID; coorte; data/periodicidade; MOB; target; evento versus acumulado; denominador; cobertura mínima e maturidade; política de duplicidade; domínio binário; limites das comparações.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

Tabela com observações, denominador, taxa e marcador de cobertura/maturidade; preflight; chamada pública com parâmetros; Receipt ligado a população/MOB/estimando/tabela; verifier.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

VF-B01: fixar regra de duplicidade e a representação de ausência da API efetiva. VF-B02: documentar denominador de entrada e de cada célula, sem delegar ao agente escolha entre estoque/coorte/observados. Não adicionar análise monetária por analogia.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixture proposta VF-F01 com target já cumulativo: coorte A contém a1,a2; MOB0=(0,0), MOB1=(1,0), MOB2=(1,ausente). Coorte B contém b1,b2; MOB0=(0,1), MOB1=(0,1). Denominador original de cada coorte=2. Oráculos: A0=0; A1=1/2; A2 incompleta/NaN, nunca zero nem taxa definitiva baseada só em um observado; B0=B1=1/2. Contagens inteiras exatas; comparação de float atol=1e-12, rtol=1e-12; NaN é esperado somente na célula declarada incompleta. Congelar datas mensais concretas na fixture antes da execução.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| VF01 | Tabela conhecida | Executar build_vintage_table. | Tabela, contagens e taxas correspondem ao oráculo manual. |
| VF02 | MOB inválido | MOB negativo, fracionário ou incompatível com datas. | Recusar antes de consolidar taxas. |
| VF03 | Target não binário | Inserir target=2, string ambígua ou null não previsto. | Bloquear domínio inválido. |
| VF04 | Acumulado decrescente | Sequência 0,1,0 para mesma unidade. | Reprovar monotonicidade. |
| VF05 | Unidade duplicada | Duplicar com target conflitante. | Bloquear conflito; sem duplicar denominador. |
| VF06 | Cobertura incompleta | Mutante substitui ausência por zero. | Oráculo reprova; ausência permanece distinguível. |
| VF07 | Denominador trocado | Usar somente N_observados na célula incompleta. | Receipt/resultado não aceitos como taxa comparável. |
| VF08 | Periodicidade misturada | Tratar trimestre como mês no mesmo contrato. | Recusar ou exigir conversão explícita aprovada. |
| VF09 | Safra imatura | Interpretar célula ainda não maturada como definitiva. | Marcar limitação; não ready para a conclusão pedida. |
| VF10 | Replay temporal | Reusar Receipt de outra tabela/período. | Binding mismatch. |
| VF11 | Eventos versus cumulativo | Reusar flag/oráculo de uma na outra. | Detectar incompatibilidade sem dupla acumulação. |
| VF12 | Estimando indevido | Pedir perda monetária a partir apenas do target binário. | Não declarar estimando não calculado. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

pandas com fixtures pequenas e tabela esperada materializada pelo autor a partir do cálculo manual. Acrescentar a variante de evento não cumulativo com oráculo próprio; não usar o mesmo esperado quando a semântica mudar.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Executar o núcleo real no Free e exportar tabela/metadata sem dados reais. Não precisa de modelo de crédito nem de baseline-ML. Comparação de safras imaturas deve conservar sua limitação.

Roteiro Genie mínimo: VF-G01, VF-G02, VF-G03, VF-G04, VF-G05, VF-G06, VF-G07, VF-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Escopo é incidência binária e calendário validado. Fluxo monetário, exposição ponderada, competing risks e inferências de risco de negócio fora do catálogo continuam não suportados.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.
