# 05 — Catálogo transversal e qualificação do mecanismo

## 5.1 Como interpretar as obrigações

O documento exibe o catálogo `catalogos/CASOS.json`. Um ID é uma obrigação de prova, não necessariamente um único método unittest: uma obrigação pode exigir positivo, negativo, mutante, variantes de host e probes externos. O número de métodos será obtido pela coleta real e congelado no perfil executável.

Todo caso tem setup, estímulo/mutação, expectativa, classe de oráculo, evidência e aplicabilidade. Os bindings para `test_id` estão vazios nesta entrega porque os testes novos ainda não foram implementados. A release executável exige esses bindings preenchidos e resolvidos. O planejamento não transforma um campo vazio em permissão para o agente local escolher um teste parecido.

Casos condicionais permanecem visíveis. Antes da campanha, o autor resolve a condição com base no escopo. NOT_APPLICABLE exige razão verificável e aprovação prévia; UNKNOWN bloqueia o estágio que depende da condição. Não eliminar negativos de escrita de um L4 materializador porque a escrita não foi autorizada naquele dia: a ausência do gate externo continua pendente.

Para cada negativo, provar também que o positivo correspondente funciona e que a falha ocorreu na fronteira que se pretendia testar. Um erro de import que impede chegar ao validator não prova que o validator rejeitou a entrada maliciosa. Um oráculo que usa a própria implementação sob teste para calcular seu resultado esperado é circular.

## 5.2 Casos transversais das skills

| ID | Obrigação / cenário | Resultado discriminante | Aplicabilidade |
|---|---|---|---|
| `T01` | Schema fechado | Recusar antes do cálculo; não descartar silenciosamente campos. | always |
| `T02` | Campos materiais | Identificar campo ausente; nenhum default material inventado. | always |
| `T03` | Coerência cruzada | Bloquear o contexto; não escolher uma interpretação arbitrária. | always |
| `T04` | Aplicabilidade | UNKNOWN bloqueia etapa material; falso legítimo registra NA com razão. | always |
| `T05` | Defaults não autorizados | Nenhuma decisão material inferida de conveniência. | always |
| `T06` | Contenção de path | Recusar escape antes de escrita. | when_effect_or_path_handling |
| `T07` | Alias de filesystem | Falhar fechado sem escapar da raiz. | when_effect_or_path_handling |
| `T08` | API pública | Recusar/informar incompatibilidade, sem fallback ad hoc. | always |
| `T09` | Chamada canônica | Não emitir prova de execução aceita. | always |
| `T10` | Parâmetros efetivos | Binding mismatch; conclusão bloqueada. | always |
| `T11` | Identidade de input | Divergência detectada; texto não substitui identidade efetiva. | always |
| `T12` | Dependência ausente | BLOCKED_ENVIRONMENT; não sintetizar resultado. | always |
| `T13` | Erro real do helper | Sem Receipt PASS/false completion; erro preservado. | always |
| `T14` | Saída parcial | Falhar na validação de output. | always |
| `T15` | Receipt ausente | Recusar ready/completion protegido. | always |
| `T16` | Record ausente | Não aceitar integridade insuficiente como prova de execução. | when_domain_record_is_required |
| `T17` | Replay | Cada binding trocado deve ser rejeitado independentemente. | always |
| `T18` | Outro domínio | Auditoria/consumidor recusa verifier ou domínio incompatível. | always |
| `T19` | Reseal semântico | Digest coerente não basta; semântica impede falso PASS. | always |
| `T20` | Versão desconhecida | Recusar; não assumir compatibilidade. | always |
| `T21` | Finalizer L4 | Sem completion autorizado. | when_L4 |
| `T22` | Autorização limitada | Recusar efeito não coberto. | when_effect_or_path_handling |
| `T23` | No-write | Nenhuma persistência fora das evidências expressamente aprovadas. | when_effect_or_path_handling |
| `T24` | Destino concorrente | Sem corrupção/sobrescrita; resultado e efeito observados. | when_effect_or_path_handling |
| `T25` | Interrupção | Efeito correto NONE/PARTIAL/UNKNOWN; sem falso concluído. | when_effect_or_path_handling |
| `T26` | Cleanup | Resíduo registrado; nenhuma alegação de rollback completo. | when_effect_or_path_handling |
| `T27` | Host distinto | Verifier não permite overclaim de cobertura. | always |
| `T28` | Package integrity | Digest/release mismatch e bloqueio. | always |
| `T29` | Coleta de testes | Discrepância bloqueia certificado. | always |
| `T30` | Dados não são instruções | Agentes tratam como dado; nenhum comando adicional. | always |
| `T31` | IDs e nomes únicos | Rejeitar colisão sem sobrescrever primeira evidência. | always |
| `T32` | Não determinismo | Detectar variação pertinente; tolerância apenas predefinida. | always |
| `T33` | Não finitos | Falhar; distinguir NaN esperado de saída inválida. | always |
| `T34` | Observabilidade | Classificar nível realmente observado, não PROVEN_EXECUTED. | always |

## 5.3 Metatestes do mecanismo comum

Executar antes de liberar qualquer skill ao novo mecanismo. Esses testes incluem execução real de processos/isolamento quando necessário; fixtures de um summary não comprovam controle de permissões ou cleanup de filhos reais.

| ID | Obrigação / cenário | Resultado discriminante | Aplicabilidade |
|---|---|---|---|
| `M01` | Producer/verifier discordantes | Processo final não pode sair 0; artefato preserva reprovação. | always |
| `M02` | Erro de fase | Checagem de autoria detecta incoerência antes de certificação. | always |
| `M03` | Stdout/stderr | Adaptador lê os dois streams sem perder erros. | always |
| `M04` | Histórico malformado | Recusar classificação benigna de output incompleto. | always |
| `M05` | Falha mesmo nome/causa diferente | Não aceitar apenas pelo nome coincidente. | always |
| `M06` | Missing/duplicate stage | Verifier impede certificado. | always |
| `M07` | Reserva de evidência | Reserva negada; não destruir evidência anterior. | always |
| `M08` | Disco indisponível | REPORTING_FAILURE, sem alegação de artefato completo. | always |
| `M09` | Serialização inválida | Erro estruturado; jamais PASS parcialmente serializado. | always |
| `M10` | Concorrência de dados globais | IDs exclusivos; tentativa de colisão bloqueada; sem mistura. | always |
| `M11` | Capacidade de isolamento | Acesso negado por mecanismo efetivo; detectar mudança residual. | always |
| `M12` | Recursão de agentes | Recusa; limite global observado, não só config. | always |
| `M13` | Lock expirado | Não conceder lock substituto sem confirmar processo/efeito anterior. | always |
| `M14` | Certificado forjado | Cross-verification recusa artefatos inexistentes/inconsistentes. | always |
| `M15` | Troca de fixture | Input digest/ownership mismatch. | always |
| `M16` | Contagem fraudulenta | Comparar IDs, não somente contagem. | always |
| `M17` | Skip não autorizado | Rejeitar sem razão aprovada e sem cobertura alternativa. | always |
| `M18` | Fim de processo incompleto | Sem certificação de conclusão limpa. | always |
| `M19` | Integridade depois do freeze | Sandbox+observação detectam tentativa; no mínimo drift/evento fica bloqueante. | always |
| `M20` | Substituição RAW/SHARE | Gerar derivado distinto; verifier acusa mistura de identidade. | always |
| `M21` | Zip adversarial | Inspeção/extração limitada; nada executado do pacote. | always |
| `M22` | Progresso enganoso | Agregado calculado por regra determinística, não texto LLM. | always |
| `M23` | Mudança de main | Preservar prova antiga e bloquear integração não reconciliada. | always |
| `M24` | Replay de autorização | Reject antes de efeito. | always |
| `M25` | Regra não carregada | Qualification reprova modo efetivo; fallback seguro sem false claim. | always |
| `M26` | Identidade circular | Envelope externo pós-commit; validação detecta auto-referência indevida. | always |
| `M27` | Chamada antes da autorização | Nó material permanece bloqueado. | always |
| `M28` | Retomada pós-efeito desconhecido | Somente reconciliação read-only previamente aprovada. | always |

## 5.4 Integração transversal — SER15/SER16

As obrigações entram progressivamente nos lotes pertinentes. SER16 consolida a prova; não é a primeira ocasião em que se descobre que duas produtoras geram Receipts incompatíveis.

| ID | Obrigação / cenário | Resultado discriminante | Aplicabilidade |
|---|---|---|---|
| `I01` | Catálogo e policy | Reprovar transição não autorizada. | always |
| `I02` | Seis skills integradas | Regressão detectada; lote não integrado. | always |
| `I03` | Receipts entre produtoras | Recusar cross-domain confusion. | always |
| `I04` | Auditor não autocertifica | Não elevar estado. | always |
| `I05` | Temporal compartilhado | Interoperabilidade reprova inconsistência. | always |
| `I06` | Prompts policy-aware | Flag de deriva; não ampliar prompt PSEF por conveniência. | always |
| `I07` | Renderer | Drift detectado e bloqueante. | always |
| `I08` | Snapshot | Conferência usa medição real; certificação bloqueia stale. | always |
| `I09` | Publicação concorrente | Lock exclusivo; nenhuma mistura de manifests. | always |
| `I10` | Mudança pós-policy | Evidência externa afetada invalidada; nova rodada. | always |
| `I11` | Merge/tree | Não transportar certificado; exigir validação do composto. | always |
| `I12` | Rollback | Rollback composto e autorizado; publicação/registro reconciliados. | always |
| `I13` | Matéria excluída | Bloquear overclaim de superfície. | always |
| `I14` | Histórico íntegro | Imutabilidade detecta alteração; manter IDs separados. | always |

## 5.5 Critério mínimo de suficiência

Não liberar um perfil com requisito sem caso, caso sem oráculo, fixture sem versão, mutante sem efeito discriminante ou capacidade externa apresentada como simulada e comprovada ao mesmo tempo. Requisitos de segurança sem teste obrigatório são bloqueio; testes fora de escopo não viram obrigação sem revisão de autoria.

A revisão pré-delegação também verifica se os próprios exemplos do plano contêm afirmações impossíveis: expected count usado como resultado, hash RAW calculado depois de sanitizar, policy esperada obtida da própria candidata, summary que tenta incorporar o seu SHA Git futuro, ou fixture que afirma execução sem chamar a primitive.

## 5.6 Famílias comportamentais

Cada dossiê possui G01–G08 no catálogo. Essas famílias são especificações a transformar em prompts literais na autoria. G03 deve conter pelo menos duas variantes negativas vizinhas, congeladas antes da execução. A resolução final inclui nível mínimo de evidência por caso; texto é suficiente para algumas respostas conceituais, não para alegar uma chamada de ferramenta.

Não alterar o prompt depois de uma resposta ruim e reapresentar a variante como primeira tentativa. Variantes planejadas e tentativas reais têm identidades próprias e permanecem no denominador do relatório.
