# SER04 — hub-ml-validacao-estatistica

Estado: **DOSSIÊ DE PLANEJAMENTO; IMPLEMENTAÇÃO E EXECUÇÃO PENDENTES**. Target preservado: **L3**, `stage_specific`.

## 1. Objetivo e superfície

Executar apenas um catálogo nominal de métodos comprovados, vinculando pergunta, hipótese, população, desenho, parâmetros e resultado. Não converter orientação estatística ampla em promessa de cobertura universal.

Superfícies: test_plan (L2); deterministic_statistics (L3).

## 2. Reuso e inventário de autoria

Matriz SER00 aponta APIs públicas de drift_detection (calculate_psi, calculate_ks, calculate_csi, detect_drift_all_features) e helpers Spark a reconfirmar. PSI/CSI são diagnósticos de distribuição, não testes de hipótese universais. Nenhuma assinatura de teste t/pareado/Wilcoxon é presumida.

Antes de código/perfil executável, registrar path da fachada, símbolo público, assinatura, versão/hash, retorno, exceções, testes existentes e efeitos. Não usar aliases abreviados da matriz como assinatura pronta. Recursos declarados D na SER00 exigem inspeção; runtime continua NOT_RUN até teste.

## 3. Contrato mínimo de entrada

Pergunta/estimando; unidade e grupos; desenho independente/pareado; hipótese/direção quando aplicável; método aprovado e parâmetros; tratamento de ausência/ties; pressupostos; multiplicidade; efeito/incerteza requeridos; origem/ref atual.

Triestado de aplicabilidade e condições de bloqueio são explícitos. Não resolver negócio por default. Campos sem autoridade podem ser usados como exemplo sintético rotulado, mas não como evidência de contexto real.

## 4. Saída e prova

Plano resolvido; tabela de método/parâmetros/estatística/p-value ou índice conforme natureza; efeito/incerteza apenas quando efetivamente calculados; decisões de multiplicidade; Receipt; limites de interpretação.

Cada saída inclui esquema/versão, identidade de input e parâmetros efetivos. O Receipt não herda autenticação humana nem autorização operacional. Postflight, quando exigido, confere a conclusão observada e o efeito, não apenas o hash do Receipt.

## 5. Decisões de autoria antes da fila local

ST-B01 é bloqueio de autoria obrigatório: inventariar assinaturas reais e congelar catálogo método×desenho×output, incluindo método de p-value e tratamento de ties. Não liberar SER04 com “métodos usuais” em texto livre. ST-B02: correção de multiplicidade e efeitos/incerteza são computação somente se houver implementação aprovada; do contrário o escopo correspondente permanece bloqueado.

Esses bloqueios são resolvidos aqui em B1. O agente local não escolhe API, tolerância, fallback ou scope para desbloqueá-los. Se uma decisão mudar o objetivo/estimando/efeito autorizado, ela vai ao usuário antes do freeze.

## 6. Fixture e oráculo propostos

Fixtures de desenho: ST-F01, duas amostras [0,1] e [2,3], com D=1 para KS empírico; p-value só vira oráculo depois de fixados método exato/hipótese e pressupostos. ST-F02, proporções ref=(0.5,0.5), atual=(0.75,0.25): PSI=0.25*ln(3), aproximadamente 0.27465307216702745, para bins já fixos e sem suavização necessária. Resultados são cálculos analíticos da fixture, não thresholds universais. Catálogo final pode usar outras fixtures; precisa de esperado independente por método.

As fixtures desta seção são propostas técnicas novas do plano. Não são dados já existentes no repositório nem resultados de execução. A autoria materializa bytes/digests e demonstra positivo + mutante antes de delegar.

## 7. Casos de domínio

| ID | Caso | Estímulo/erro discriminante | Resultado obrigatório |
|---|---|---|---|
| ST01 | Oráculo por método | Executar rota canônica. | Outputs e parâmetros concordam com oráculo independente. |
| ST02 | Método não suportado | Solicitar método não implementado. | Bloquear sem inventar API. |
| ST03 | População insuficiente | Vazio, só nulos ou tamanho abaixo do requisito do método. | Não produzir conclusão estatística indevida. |
| ST04 | Pareamento/unidade | Pares ausentes/duplicados ou amostras independentes. | Bloquear desenho incoerente; não mudar estimando. |
| ST05 | Pressuposto desconhecido | Marcar premissa ausente como satisfeita. | UNKNOWN bloqueia ou exige alternativa previamente permitida. |
| ST06 | Multiplicidade | Omitir correção requerida ou reduzir família depois do resultado. | Recusar/limitar conclusão; método executado precisa corresponder ao plano. |
| ST07 | Efeito/incerteza | Retornar apenas p-value. | Output incompleto não é ready. |
| ST08 | Bins/ref/threshold | Alterar bins entre cálculo e Receipt. | Binding mismatch. |
| ST09 | Erro de método | Biblioteca ausente/exceção/saída parcial. | Sem Receipt PASS inventado. |
| ST10 | Interpretação causal | Solicitar causalidade ou relevância econômica automática. | Separar conclusão suportada da não demonstrada. |
| ST11 | Ties/zeros | Aplicar método/epsilon não aprovado. | Premissa/parametrização explícita; sem smoothing silencioso. |
| ST12 | Hipótese trocada | Trocar direção depois do p-value. | Invalidar binding e conclusão. |

Cada linha herda setup, evidência e tipo de oráculo de `catalogos/CASOS.json`. Casos com vários parâmetros geram invocações individualmente identificadas; contar uma linha não comprova todas as variantes.

## 8. Campanha local

Um positivo e seus negativos por método do catálogo. Tolerância definida por método antes do freeze; contagens/IDs são exatos, floats de fórmula fechada começam com atol=rtol=1e-12. Aproximação estatística exige perfil separado, nunca mudança de tolerância após FAIL.

Artefatos de autoria previstos: contrato, preflight e runner fino da skill; Receipt/verifier/manifest quando L3; run_enforced/Postflight/finalizer quando L4 e exigidos pelo registry; testes repo-side e fixtures; perfil diagnóstico/certificação; README/TESTES/RESULTADOS/CHECKPOINT. Não criar stub que retorna PASS.

## 9. Free e comportamento

Executar todos os métodos cujo host Free será declarado suportado. Limitar população sintética pequena. Biblioteca importada não é cálculo provado. Método ausente bloqueia somente seu escopo, mas não pode desaparecer do catálogo aprovado.

Roteiro Genie mínimo: ST-G01, ST-G02, ST-G03, ST-G04, ST-G05, ST-G06, ST-G07, ST-G08. Cada caso usa chat novo, prompt/variante fixados, resposta literal e observabilidade classificada. Congelar também dois pedidos negativos vizinhos na geração do perfil comportamental; não escolher os mais fáceis depois do resultado. Contagem de variantes é preenchida no manifesto antes do teste.

## 10. Não promovido e critérios de encerramento

Não autoriza causalidade, significância econômica, decisão de crédito ou teste genérico fora do catálogo. Uma única chamada KS não prova todos os cálculos mencionados no SKILL.md.

Local PASS sem Free/prova de efeito exigida não promove a superfície. Para L4, a etapa L2 da mesma skill precisa estar aceita e seu contrato ser ancestral/verificavelmente equivalente ao consumido. A proposta final explicita suporte por operação/tipo/host/efeito e não muda rollout sem autorização separada.

## 11. Entrega do executor e auditoria

Executor devolve apenas resultados, artefatos, diagnóstico e estado dos efeitos. Auditor de domínio confere fixture/estimando, parâmetro real, semântica temporal/numérica e limites. Auditor de evidência confere IDs, cobertura, calls, runtime, hashes, Receipt/Postflight e autoridade. Finding material bloqueia promoção; discordância não é resolvida por maioria de agentes.
