# Leitura dos arquivos de execução de skills

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt14-enforcement-code-map"></a>
<a id="mt14-enforcement-code-map"></a>
### Leitura dos arquivos de execução de skills

Leia cada ficha como uma ligação entre a arquitetura ensinada no capítulo e os bytes de um arquivo concreto. A coluna de papel responde por que o arquivo existe. As entradas e saídas mostram onde os dados entram e o que o chamador recebe. A coluna de efeitos separa calcular um resultado de alterar a sessão, gravar uma tabela ou produzir uma apresentação. Essa separação evita atribuir ao helper tudo que aparece no notebook de demonstração.

Uma fachada é a camada de importação que disponibiliza nomes de outro módulo. Ela pode carregar bibliotecas necessárias no momento do import, embora ainda não chame a função de negócio. Um marcador de pacote apenas estabelece a organização do diretório. Uma implementação contém o algoritmo. Um exemplo é um roteiro de notebook: pode preparar dados, instalar bibliotecas, mostrar resultados e conservar observações históricas. Esses quatro papéis explicam a repetição de nomes entre arquivos sem sugerir quatro versões independentes do mesmo algoritmo.

As fichas complementam a leitura contínua; não substituem a assinatura e a interpretação desenvolvidas nos capítulos. Quando um resultado histórico difere do comportamento atual, a nota identifica a diferença e o cuidado necessário. Uma saída colada no exemplo descreve o ensaio registrado naquela fonte; ela não demonstra uma execução atual. Os nomes citados também não tornam automaticamente uma função interna uma interface pública. Para compor uma chamada, use a fachada indicada e confira o contrato do objeto.

Os links levam ao arquivo correspondente e ao trecho conceitual do manual. Compare sempre helper e exemplo antes de executar células: efeitos pertencem ao corpo que realmente os realiza. As limitações descritas fazem parte da interpretação do resultado, inclusive quando o código devolve números plausíveis.

Este mapa acompanha os vinte e quatro arquivos do núcleo e das primeiras rotas técnicas. Os novos runners B1 têm [mapa próprio](MT-mt14-b1-code-map.md#mt-mod-mt14-b1-code-map). Nos executores de skills, siga os estados e as evidências de cada fase. Disponibilizar um símbolo, chamar um recurso e concluir o fluxo são acontecimentos diferentes. Verifique também o alcance do writer e o efeito de uma falha após alguma escrita.

<a id="mt14-enforcement-code-map-file-001"></a>
#### 1. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/skill_execution/__init__.py) · [MT17: explicação do mecanismo](MT-parte-iv.md#mt17-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_scripts/skill_execution/__init__.py` · SHA-256 `68a7018cd9f326a5730b26be73d2b0d7888eae07c272ff175d507f192b908b00` |
| Papel e motivo técnico | Publicar uma API estável de preflight e consulta de policy. |
| Mecanismo | Reexporta dataclasses, run_preflight e registry de policy via `__all__`; a importação carrega skill_execution.py, mas não chama run_preflight. |
| Nomes disponibilizados | ["SUPPORTED_SCHEMA_VERSIONS", "SUPPORTED_MODES", "SUPPORTED_POLICIES", "PreflightIssue", "PreflightDecision", "PreflightResult", "PreflightContractError", "run_preflight", "EnforcementPolicyError", "EnforcementSurface", "SkillEnforcementPolicy", "load_enforcement_policy_registry", "get_skill_enforcement_policy", "list_skill_enforcement_policies"] |
| Entradas | Import Python do pacote. |
| Saídas | Nomes públicos para consumidores. |
| Efeitos | Importa implementação; nenhuma avaliação de contrato ou dados por si. |
| Dependências e momento de uso | Import relativo .skill_execution; sem backend no import. |
| Como interpretar este arquivo | A fachada do executor publica PreflightResult, run_preflight e consultas de policy a partir de skill_execution.py. Importar esses nomes carrega o módulo, mas não lê contrato nem chama helper protegido. O consumidor deve passar caminho do contrato, raiz da assistência e contexto ao preflight; o registry de policy apenas relata nível e rollout vigentes. |

<a id="mt14-enforcement-code-map-file-002"></a>
#### 2. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/skill_execution/domain_context/__init__.py) · [MT17: explicação do mecanismo](MT-parte-iv.md#mt17-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_scripts/skill_execution/domain_context/__init__.py` · SHA-256 `f8a2450b9eb9934fba2ac3271e32ca4423838adde4e222e2cc38319dca48a66b` |
| Papel e motivo técnico | Ter um dono comum para invariantes sintéticas de tempo, identidade e JSON fechado. |
| Mecanismo | closed/text/integer recusam campos e coerções; loads_strict recusa chave duplicada/NaN; digest usa JSON estrito; validate_temporal_context separa APPLICABLE, NOT_APPLICABLE e UNKNOWN sem join. |
| Nomes disponibilizados | ["TEMPORAL_VERSION", "ContextError", "closed", "text", "integer", "digest", "utc_instant", "month_start", "validate_temporal_context", "loads_strict"] |
| Entradas | Objeto PIT, configuração temporal, decision_at UTC e motivo quando inaplicável. |
| Saídas | Contexto normalizado com join_executed=false ou ContextError. |
| Efeitos | Somente valida/serializa em memória; não lê fontes nem executa PIT. |
| Dependências e momento de uso | json, hashlib, datetime UTC; chamado por safra e cross-EDA. |
| Como interpretar este arquivo | Este pacote concentra validações sintéticas de tempo e identidade: JSON estrito recusa chaves duplicadas e valores não finitos, enquanto validate_temporal_context distingue aplicável, inaplicável e desconhecido. Ele devolve contexto normalizado com join_executed=false; nenhuma fonte é lida nem cruzada. Safra e cross-EDA usam a mesma regra para não transformar um horário declarado em prova de disponibilidade histórica. |

<a id="mt14-enforcement-code-map-file-003"></a>
#### 3. `exemplo_domain_context.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/skill_execution/domain_context/exemplo_domain_context.py) · [MT17: explicação do mecanismo](MT-parte-iv.md#mt17-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_scripts/skill_execution/domain_context/exemplo_domain_context.py` · SHA-256 `53d545307a1694b893aa79d41c388b541ad8d9ddb6d6459ff265b06d8bad0c23` |
| Papel e motivo técnico | Mostrar um contexto PIT sintético aceito sem simular join. |
| Mecanismo | Chama validate_temporal_context com lag constante de um dia e assert join_executed=False; imprime transcrição local datada. |
| Nomes disponibilizados | [] |
| Entradas | Valores literais sintéticos de pit/temporal/decision_at. |
| Saídas | Dicionário normalizado e print histórico. |
| Efeitos | Se executado, import e assert locais; sem Spark, gravação ou promoção. |
| Dependências e momento de uso | Import da fachada domain_context. |
| Como interpretar este arquivo | O exemplo fornece timestamps e lag sintéticos ao validador de contexto e afirma que join_executed permanece false. O print é uma transcrição local histórica, não linha de dados cruzados. A lição é separar coerência de campos temporais da execução real do join: um contexto aprovado só permite passar à próxima etapa. |

<a id="mt14-enforcement-code-map-file-004"></a>
#### 4. `release.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/skill_execution/domain_context/release.py) · [MT18: explicação do mecanismo](MT-parte-iv.md#mt18-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_scripts/skill_execution/domain_context/release.py` · SHA-256 `756b4d647b975ca7e7446a8a173230e320021baa3209f71c58a21bb73d462264` |
| Papel e motivo técnico | Fixar bytes de release do perfil técnico de safra, sem promover seu rollout. |
| Mecanismo | load_sibling importa arquivo por spec; blob calcula Git blob SHA-1; release_integrity exige keys/artifacts exatos, paths sem escape/symlink e fileset igual ao requerido. |
| Nomes disponibilizados | ["load_sibling", "blob", "release_integrity"] |
| Entradas | Diretório de skill e conjunto required_paths; caminho sibling opcional. |
| Saídas | Módulo carregado, digest blob ou manifesto SHA-256 com artifacts observados. |
| Efeitos | Lê arquivos do checkout e executa import sibling quando chamado; não escreve produto. |
| Dependências e momento de uso | importlib.util, sys.modules, pathlib, loads_strict; usado por runner/verifier safra. |
| Como interpretar este arquivo | O módulo carrega um sibling por importlib quando solicitado, calcula SHA-1 no formato Git blob e verifica manifesto da safra contra lista exata de paths obrigatórios. Recusa escapes e symlinks e devolve integridade observada; lê bytes do checkout, mas não grava produto. Acrescentar arquivo ao manifesto pode quebrar a igualdade mesmo com hash correto, diferença importante frente aos verificadores EDA e criar-objeto. |

<a id="mt14-enforcement-code-map-file-005"></a>
#### 5. `exemplo_skill_execution.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/skill_execution/exemplo_skill_execution.py) · [MT17: explicação do mecanismo](MT-parte-iv.md#mt17-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_scripts/skill_execution/exemplo_skill_execution.py` · SHA-256 `da7103c367d90bb310c38c6ab4160d415ed4fe490d1cf60cf81820409a832ee6` |
| Papel e motivo técnico | Demonstrar preflight L2 EDA por import público. |
| Mecanismo | Procura .assistant subindo de __file__, monta contexto literal e chama run_preflight; assert status PASS e writes false. |
| Nomes disponibilizados | [] |
| Entradas | Contrato EDA local e contexto literal com seis campos, sem pk_columns_available. |
| Saídas | Print do PreflightResult ou AssertionError no contrato corrente. |
| Efeitos | Lê contrato e fachadas; confere a presença dos templates sem ler seus bytes; sem helper analítico nem gravação. |
| Dependências e momento de uso | Path(__file__), sys.path, hub_scripts.skill_execution. |
| Como interpretar este arquivo | O exemplo tenta localizar .assistant via __file__, monta contexto literal e afirma PASS de run_preflight. O contrato EDA atual exige pk_columns_available para decidir recurso condicional, mas esse campo falta: pela leitura estática, o preflight bloquearia e o assert falharia. Em notebook Databricks, __file__ também pode não existir. Portanto, a célula serve para estudar intenção histórica, não para prometer PASS corrente. |

<a id="mt14-enforcement-code-map-file-006"></a>
#### 6. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/skill_execution/postflight/__init__.py) · [MT19: explicação do mecanismo](MT-parte-iv.md#mt19-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_scripts/skill_execution/postflight/__init__.py` · SHA-256 `dd4ffda5745985eede929b708bd48735e7bfcc421c3f4c83885f2cb4ca008e27` |
| Papel e motivo técnico | Decidir autorização de conclusão L4 com evidência de execução e handoff. |
| Mecanismo | build_postflight compara Receipt VALID, bindings skill/trace/artifacts, recursos required/conditional, templates carregados e campos handoff; _state precede BLOCKED>FAIL>REVIEW>PASS; verify_postflight reconstrói pf1. |
| Nomes disponibilizados | ["PostflightIssue", "PostflightVerification", "canonical_json_bytes", "sha256_digest", "build_postflight", "verify_postflight"] |
| Entradas | Payload, contrato, verificação independente do Receipt e handoff. |
| Saídas | Postflight V1 com coverage/issues/completion_authorized; verificação VALID/INVALID. |
| Efeitos | Calcula hashes JSON e checa estado em memória; não escreve nem mede verdade externa. |
| Dependências e momento de uso | json/hashlib/dataclasses; chamado pelo finalizador EDA. |
| Como interpretar este arquivo | O Postflight V1 compara Receipt reverificado, skill, trace, artefatos, recursos aplicáveis, templates carregados e handoff. A ordem de estado prioriza BLOCKED, depois FAIL, REVIEW e PASS; só PASS torna completion_authorized=true. verify_postflight reconstrói o comprovante pf1 em memória. Esse módulo decide autorização de conclusão, não executa novamente a análise nem autentica fatos fora do payload. O capítulo MT19 detalha os requisitos e limites desta verificação. |

<a id="mt14-enforcement-code-map-file-007"></a>
#### 7. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/skill_execution/receipt/__init__.py) · [MT18: explicação do mecanismo](MT-parte-iv.md#mt18-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_scripts/skill_execution/receipt/__init__.py` · SHA-256 `c82c20066dee1c5da5bee83ab914f7bd6ecd0508bc5d392f4c9ecaecda0d234a` |
| Papel e motivo técnico | Emitir e reverificar comprovante V1 da rota canônica L3. |
| Mecanismo | Builder exige trace/preflight PASS, primitive called+completed, digests, proveniência numeric_columns runtime_derived e sem fallback/escrita; verifier distingue ABSENT/MALFORMED/INVALID/STALE_REPLAYED/INCOMPATIBLE/VALID. |
| Nomes disponibilizados | ["ReceiptVerification", "canonical_json_bytes", "sha256_digest", "build_execution_receipt", "verify_execution_receipt"] |
| Entradas | Trace, result, skill/entrypoint/primitive esperados; run/release opcionais no verifier. |
| Saídas | Receipt er1: ou None; ReceiptVerification tipado. |
| Efeitos | Hash canônico em memória; imported e templates_consumed permanecem NOT_OBSERVABLE; não executa primitive. |
| Dependências e momento de uso | json/hashlib/dataclasses; EDA/safra usam o pacote. |
| Como interpretar este arquivo | O builder er1 só emite comprovante quando trace, preflight, chamada e conclusão da primitive, digests e proveniência cumprem o contrato. O verificador distingue ausência, formato ruim, incompatibilidade e replay; hash local não é identidade humana. Imports e consumo de template permanecem NOT_OBSERVABLE no Receipt V1, exigindo instrumentação de outra etapa. Ele sela evidência de L3, sem autorizar sozinho a conclusão L4. |

<a id="mt14-enforcement-code-map-file-008"></a>
#### 8. `skill_execution.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/skill_execution/skill_execution.py) · [MT17: explicação do mecanismo](MT-parte-iv.md#mt17-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_scripts/skill_execution/skill_execution.py` · SHA-256 `acce61cd91998ddf22d98807f4ea0859b9a59e83115012f19921f520161d7563` |
| Papel e motivo técnico | Resolver disponibilidade de contrato L2 e ler policy SE07 sem executar helpers. |
| Mecanismo | AST da fachada valida export público; templates relativos são is_file; sete condições decidem applicable/resolved/issues. Registry valida níveis, rollout, surfaces e skill única. |
| Nomes disponibilizados | ["PreflightIssue", "PreflightDecision", "PreflightResult", "PreflightContractError", "run_preflight", "EnforcementPolicyError", "EnforcementSurface", "SkillEnforcementPolicy", "load_enforcement_policy_registry", "get_skill_enforcement_policy", "list_skill_enforcement_policies"] |
| Entradas | contract_path, assistant_root, context; ou policy_path/skill para consulta. |
| Saídas | PreflightResult PASS/BLOCKED ou políticas tipadas/erro; writes_performed=false. |
| Efeitos | Lê contrato, fachadas e policy JSON; confere a presença dos templates sem ler seus bytes; não importa helpers-alvo nem os chama. |
| Dependências e momento de uso | ast/json/dataclasses/pathlib; consumidores EDA, safra, cross-EDA e auditoria. |
| Como interpretar este arquivo | run_preflight lê contrato, confere export de API por AST e presença de templates, depois resolve sete condições sem importar ou chamar os helpers-alvo. Seu PASS significa disponibilidade estática, com writes_performed=false. O mesmo módulo lê policy SE07 e devolve níveis/rollout tipados; target_level é direção, não promoção. Uma fachada encontrada pode continuar sem execução protegida. |

<a id="mt14-enforcement-code-map-file-009"></a>
#### 9. `preflight.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-analise-safra/scripts/preflight.py) · [MT17: explicação do mecanismo](MT-parte-iv.md#mt17-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-analise-safra/scripts/preflight.py` · SHA-256 `3f9505c491c4aa9d78d2d55cfaa02b0f39cd4a1c4b694582ee6ec4fe6aa4e614` |
| Papel e motivo técnico | Bloquear pedido sintético de safra incoerente antes do cálculo. |
| Mecanismo | validate_request fecha perfil mensal binário, roster/MOB0, UTC mês, duplicatas, target cumulativo/evento e monta coverage_grid; preflight só após PASS chama SEF e vincula blobs. |
| Nomes disponibilizados | ["validate_request", "preflight", "main"] |
| Entradas | Request sintético mensal, roster, linhas, corte, max_mob, semantic_mode. |
| Saídas | PASS/BLOCKED com grid, sef e bindings; helper_called=false. |
| Efeitos | Leitura de contrato/fachadas na etapa SEF; não importa pandas nem chama vintage_core. |
| Dependências e momento de uso | domain_context; skill_execution.run_preflight; policy safra L0→L3 audit. |
| Como interpretar este arquivo | O preflight de safra valida perfil mensal binário, roster, mês UTC, MOB desde originação, duplicatas e semântica cumulativa ou de evento. Só depois de pedido coerente consulta o preflight estrutural e registra vínculos; helper_called=false. Um schema pode aceitar os tipos e ainda permitir linha com MOB impossível. PASS prepara o percurso técnico implementado, não mede taxa de safra nem promove a policy atual L0/audit. |

<a id="mt14-enforcement-code-map-file-010"></a>
#### 10. `run.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-analise-safra/scripts/run.py) · [MT18: explicação do mecanismo](MT-parte-iv.md#mt18-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-analise-safra/scripts/run.py` · SHA-256 `47897413f735a21a1942b4f1d93a20e5d5fdbcaf1ac7962ae3a873778dbad609` |
| Papel e motivo técnico | Demonstrar rota técnica L3 mensal/binária integrada, ainda sem promover a skill. |
| Mecanismo | Confere release exato, preflight, import origin da fachada/primitive, chama build_vintage_table, normaliza tabela/coverage, revalida release e emite Receipt V1. |
| Nomes disponibilizados | ["run", "main"] |
| Entradas | Request sintético validado e run_id opcional. |
| Saídas | Payload status/preflight/trace/result/receipt; business_readiness NOT_EVALUATED. |
| Efeitos | Chama pandas/vintage_core e captura stdout em memória; não persiste, não autoriza promoção. |
| Dependências e momento de uso | domain_context.release, pandas, hub_snippets.ml.vintage_analysis, receipt V1. |
| Como interpretar este arquivo | O runner do perfil integrado verifica release e preflight, confirma origem da fachada e da primitive, chama build_vintage_table e emite Receipt V1 após normalizar tabela e cobertura. Ele pode calcular com pandas sobre pedido sintético, mas não persiste nem autoriza promoção da skill, cujo nível corrente é L0. Um Receipt desse piloto demonstra o caminho ensaiado, não prontidão de negócio ou execução em carteira real. |

<a id="mt14-enforcement-code-map-file-011"></a>
#### 11. `verify.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-analise-safra/scripts/verify.py) · [MT18: explicação do mecanismo](MT-parte-iv.md#mt18-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-analise-safra/scripts/verify.py` · SHA-256 `37b2c9af377e890a8e73d82bd7b912b50e051e70da8ee70103d54ccfe8d0d81d` |
| Papel e motivo técnico | Conferir resultado de safra contra pedido/run/oráculo retidos externamente. |
| Mecanismo | Verifica preflight atual, input digest, metadata, tabela linha a linha com isclose, Receipt V1 e release antes/depois. |
| Nomes disponibilizados | ["verify"] |
| Entradas | Payload e expected_request, expected_run_id, expected_table independentes. |
| Saídas | VALID/INVALID com issues; completion_authorized=false. |
| Efeitos | Lê release; não reexecuta vintage_core nem escreve. |
| Dependências e momento de uso | domain_context.digest/release, receipt.verify_execution_receipt. |
| Como interpretar este arquivo | O verificador compara payload com pedido, run_id e tabela esperada retidos de forma independente, além de rever release e Receipt V1. Ele não reexecuta vintage_core e sempre mantém completion_authorized=false. Sem oráculo externo correto, igualdade com uma tabela enviada pelo próprio produtor seria circular; a verificação sintética também não autentica dados corporativos. |

<a id="mt14-enforcement-code-map-file-012"></a>
#### 12. `preflight.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-auditoria-skills/scripts/preflight.py) · [MT14: explicação do mecanismo](MT-parte-iii.md#mt14-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-auditoria-skills/scripts/preflight.py` · SHA-256 `0d65d96261f99db08e8184b460274023883f62888d22c247e922635b4c19c1de` |
| Papel e motivo técnico | Escolher modo OUTPUT/IMPLEMENTACAO e verificar entradas observáveis. |
| Mecanismo | OUTPUT exige producer_skill existente, pedido original e artefato; lê policy se registrada e anota gap se não; IMPLEMENTACAO exige target_skills existentes. |
| Nomes disponibilizados | ["preflight", "main"] |
| Entradas | Contexto audit_mode e campos do modo. |
| Saídas | PASS/BLOCKED, producer_policy, target_skills, blocking_issues/evidence_gaps. |
| Efeitos | Confere existência de `SKILL.md` com `is_file`, sem ler seus bytes. No modo OUTPUT, lê a policy quando encontra a skill produtora; verifier_executed=false, analytics_executed=false, writes=false. |
| Dependências e momento de uso | skill_execution.get_skill_enforcement_policy; nenhuma execução da produtora. |
| Como interpretar este arquivo | O preflight de auditoria escolhe OUTPUT ou IMPLEMENTACAO. OUTPUT requer skill produtora, pedido original e artefato; IMPLEMENTACAO precisa de skills-alvo localizadas. Ele lê policy e pode registrar lacuna se a produtora não estiver no registry, mas não executa verifier nem analytics. PASS libera a classificação posterior, sem dizer que o artefato está conforme. |

<a id="mt14-enforcement-code-map-file-013"></a>
#### 13. `run.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-auditoria-skills/scripts/run.py) · [MT14: explicação do mecanismo](MT-parte-iii.md#mt14-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-auditoria-skills/scripts/run.py` · SHA-256 `497fe2e93de92ab9eb40e515261058b0ac299cc0f5b60cefcb99c3220514a565` |
| Papel e motivo técnico | Produzir classificação de evidência e comprovante próprio da auditoria. |
| Mecanismo | Normaliza escada citado/localizado/lido/importado/chamado/concluido e aplicabilidade; adaptador real só para EDA chama postflight.verify_finalized quando há payload; emite audit-er1 separado de er1. |
| Nomes disponibilizados | ["run", "verify_receipt", "main"] |
| Entradas | Context/evidence e producer_final_payload opcional. |
| Saídas | Trace, resultado e Receipt SE07-AUDIT-RECEIPT-1; producer_canonical_compliance separado. |
| Efeitos | Lê release, preflight e pode executar verifier da EDA; não executa analytics nem grava; audit PASS não implica producer PASS. |
| Dependências e momento de uso | importlib.util, policy/preflight, postflight EDA via adaptador. |
| Como interpretar este arquivo | O runner classifica evidência em citado, localizado, lido, importado, chamado e concluído, preservando NOT_OBSERVABLE quando não há prova. Com payload EDA e adaptador disponível, pode chamar de fato verify_finalized; sem chamada válida, producer_canonical_compliance fica NOT_REVERIFIED ou mais fraco. Seu audit-er1 comprova a própria classificação, não a produtora. Na policy está L3/audit; audit mede sem veto automático do rollout, embora validações possam bloquear o runner. |

<a id="mt14-enforcement-code-map-file-014"></a>
#### 14. `test_validador.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-concierge/tests/test_validador.py) · [MT14: explicação do mecanismo](MT-parte-iii.md#mt14-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-concierge/tests/test_validador.py` · SHA-256 `faeafff22efa4746b78e4e7437d3c84891e8c9cee453ce9703d6a11c15c1997e` |
| Papel e motivo técnico | Detectar regressões do pacote estático Concierge. |
| Mecanismo | Cópia temporária e mutações negativas de frontmatter, links, routes, casos, Python e symlinks; chama validar_pacote. |
| Nomes disponibilizados | ["ValidatorTests"] |
| Entradas | Pacote copiado para tmp e casos sintéticos alterados. |
| Saídas | Asserts de PASS/FAIL estruturais; não avalia escolha em chat. |
| Efeitos | Quando executado, pode criar/remover arquivos temporários de teste, sem escrever produto. |
| Dependências e momento de uso | Biblioteca padrão (`unittest`, `tempfile`, `shutil`, `json` e `Path`) e o validador local do pacote Concierge; não importa nem exige pytest. |
| Como interpretar este arquivo | Os testes copiam o pacote para área temporária, alteram frontmatter, links, rotas, casos, Python e symlinks e esperam falhas específicas do validador. Essa regressão pode escrever somente na cópia de teste; não conversa com um usuário nem mede se a recomendação de skill foi boa. Um PASS estrutural reduz quebras do pacote, mas não substitui forward humano de roteamento. |

<a id="mt14-enforcement-code-map-file-015"></a>
#### 15. `validar_pacote.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-concierge/tests/validar_pacote.py) · [MT14: explicação do mecanismo](MT-parte-iii.md#mt14-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-concierge/tests/validar_pacote.py` · SHA-256 `d224136c44967a8d62a822f4547ec6b442095c20cfc9dd851bb086b67628e4bc` |
| Papel e motivo técnico | Conferir forma local do pacote Concierge sem comportamento conversacional. |
| Mecanismo | Valida raiz, 16 arquivos, frontmatter/seções/rotas, UTF-8/Python AST, links locais contidos e matriz de aceitação 26 casos pendentes. |
| Nomes disponibilizados | ["validate", "main"] |
| Entradas | Path da pasta Concierge. |
| Saídas | Lista de erros/exit code; não seleciona skill no chat. |
| Efeitos | Lê arquivos; AST parse sem importar; sem chamadas Databricks nem escrita de produto. |
| Dependências e momento de uso | pathlib/json/ast; matriz casos_aceite.json. |
| Como interpretar este arquivo | O validador lê pasta, arquivos obrigatórios, frontmatter, seções, rotas, links locais, Python por AST e matriz de casos. Ele devolve erros e código de saída sem importar scripts-alvo ou escolher skill em chat. Uma rota sintaticamente presente pode ainda ser ruim para um pedido real; a ferramenta confere forma e referências, não qualidade da decisão conversacional. |

<a id="mt14-enforcement-code-map-file-016"></a>
#### 16. `_windows_writer.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-criar-objeto/scripts/_windows_writer.py) · [MT14: explicação do mecanismo](MT-parte-iii.md#mt14-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-criar-objeto/scripts/_windows_writer.py` · SHA-256 `794c06ccd6dc48c61a0b766d4bca8cd242fe46c592b238903b2c939548d0487e` |
| Papel e motivo técnico | Impedir troca de ancestrais e overwrite no piloto Windows local NTFS. |
| Mecanismo | PinnedParent fixa diretórios por handles sem SHARE_DELETE, recusa reparse/junction/hardlink e cria destino com CREATE_NEW; não oferece rollback. |
| Nomes disponibilizados | ["PinnedParent"] |
| Entradas | Raiz absoluta, destino relativo; chamada explícita create(). |
| Saídas | fd de arquivo novo e identidades de ancestrais/destino. |
| Efeitos | create abre arquivo real; falha posterior pode deixar bytes parciais; somente apply do runner chama create. |
| Dependências e momento de uso | ctypes/kernel32/msvcrt/os; Windows drive fixo NTFS. |
| Como interpretar este arquivo | PinnedParent abre ancestrais por handles Windows sem SHARE_DELETE, recusa reparse points e hardlinks e cria o destino com CREATE_NEW. É a primitive de escrita estreita chamada pelo apply do piloto create/readme/agregador em NTFS local. Se uma falha ocorrer depois de criar o arquivo, bytes parciais podem restar: create exclusivo evita overwrite, mas não oferece transação nem rollback. |

<a id="mt14-enforcement-code-map-file-017"></a>
#### 17. `object_validation.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-criar-objeto/scripts/object_validation.py) · [MT18: explicação do mecanismo](MT-parte-iv.md#mt18-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-criar-objeto/scripts/object_validation.py` · SHA-256 `48089c6a90dcb66ffa2d7fe8afd070f4bfa7fda4e46557bf2a161be11a69349c` |
| Papel e motivo técnico | Vincular validação estrutural repo-side a candidato/base, sem autenticar humano. |
| Mecanismo | build_receipt exige registro local íntegro, comandos/checks completos, original preservado; verify_receipt exige registro correlato e compara ov1/body/binding. |
| Nomes disponibilizados | ["digest", "build_receipt", "verify_receipt"] |
| Entradas | Local record, receipt e expected_run/base/candidate opcionais. |
| Saídas | Receipt ov1 ou verificação com execution_reverified=false. |
| Efeitos | Hash JSON em memória; não executa validador, notebook ou apply. |
| Dependências e momento de uso | copy/hashlib/json/re; produtor canônico permanece repo-side. |
| Como interpretar este arquivo | O módulo sela o registro local de validação estrutural em receipt ov1 e confere versão, vínculo com candidato/base e hashes. Ele não executa o validador nem autentica a pessoa que aprovou; o próprio retorno mantém execution_reverified=false e human_authority_authenticated=false. Um recibo íntegro comprova correlação de registros locais, não autorização suficiente para chamar apply. |

<a id="mt14-enforcement-code-map-file-018"></a>
#### 18. `preflight.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-criar-objeto/scripts/preflight.py) · [MT14: explicação do mecanismo](MT-parte-iii.md#mt14-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-criar-objeto/scripts/preflight.py` · SHA-256 `edee31045a1749ee962c180f3618bf7807ea6cef575c3968193033b31b6e6c30` |
| Papel e motivo técnico | Fechar tipo, template, sobreposição e destino antes de criar/converter. |
| Mecanismo | Valida seis tipos e create/convert, nomes, paths Windows/Unix, escala README, decisão de capacidade existente; confirma template is_file e destino sem colisão. |
| Nomes disponibilizados | ["preflight", "main"] |
| Entradas | Contexto de intenção com operação/tipo/nome/capacidade/destino. |
| Saídas | PASS/BLOCKED com template.read_status=NOT_OBSERVABLE, destino e issues. |
| Efeitos | Lê paths; não cria, não valida runtime, não executa tools. |
| Dependências e momento de uso | pathlib/PureWindowsPath/json; chamado pelo writer piloto. |
| Como interpretar este arquivo | O preflight resolve operação, tipo de objeto, nome, template, sobreposição de capacidade e destino. Recusa colisões e paths indevidos antes da geração, devolvendo PASS/BLOCKED e template.read_status=NOT_OBSERVABLE. Encontrar o template no disco não demonstra que seus bytes foram consumidos; tampouco cria README ou valida o produto gerado. |

<a id="mt14-enforcement-code-map-file-019"></a>
#### 19. `run.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-criar-objeto/scripts/run.py) · [MT14: explicação do mecanismo](MT-parte-iii.md#mt14-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-criar-objeto/scripts/run.py` · SHA-256 `4eef76769d38a9f88cdbbb60014c19ccb54fc8020c373d2173561cc2f09de985` |
| Papel e motivo técnico | Gerar bytes e aplicar somente create/readme/agregador com confirmação externa exata. |
| Mecanismo | generate valida preflight/release/template/inventário e sela candidato em memória; apply revalida binding/ancestrais, autorização e validação, reserva evidência externa, CREATE_NEW, fsync/reread e estados ESCRITO/INCONCLUSIVE/BLOCKED; verify_evidence só integridade local. |
| Nomes disponibilizados | ["generate", "apply", "verify_evidence", "main"] |
| Entradas | Contexto/documento/base_sha para generate; candidato + registros de autorização/validação + evidence_dir para apply. |
| Saídas | Candidato GERADO ou evidência de ESCRITO/falha; authentication local_integrity_only. |
| Efeitos | generate sem escrita; apply escreve README novo e JSON de evidência externo, podendo deixar parcial; sem overwrite/rollback. |
| Dependências e momento de uso | _windows_writer, receipt canonical JSON, preflight, release manifest, NTFS. |
| Como interpretar este arquivo | generate lê template e contrato, confere release/inventário e monta candidato em memória; apply recebe autorização e validação correlatas, revalida destino/ancestrais e usa o writer CREATE_NEW para README agregador novo, com evidência externa. Pode restar arquivo parcial e estado INCONCLUSIVE, sem rollback. O cabeçalho ainda menciona L2 histórico; policy vigente é L3/audit, porém isso não amplia o escopo de escrita. |

<a id="mt14-enforcement-code-map-file-020"></a>
#### 20. `preflight.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-cross-eda-ml/scripts/preflight.py) · [MT17: explicação do mecanismo](MT-parte-iv.md#mt17-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-cross-eda-ml/scripts/preflight.py` · SHA-256 `02cc1a674b9efb115e8d1d8634d7b0872533c497605d11224d64ea56632b5464` |
| Papel e motivo técnico | Resolver contexto sintético de duas fontes sem executar join. |
| Mecanismo | Valida chaves/âncora/grão 1 linha por entidade-decisão, cardinalidade 1:1 ou N:1, PIT temporal via dono compartilhado; verifica SEF e oferece verify_preflight por recomputação. |
| Nomes disponibilizados | ["validate_context", "preflight", "verify_preflight", "main"] |
| Entradas | Context fechado com duas fontes, snapshots/digests declarados, decision_at/PIT. |
| Saídas | RESOLVED_FOR_L2 ou BLOCKED, join_executed=false, source_identity DECLARED_NOT_READ. |
| Efeitos | Lê contrato/fachadas; não lê bytes das fontes, não mede cobertura e não promove policy L0. |
| Dependências e momento de uso | domain_context, skill_execution.run_preflight; perfil CANDIDATE_NOT_PROMOTED. |
| Como interpretar este arquivo | O preflight cross-EDA resolve pedido sintético de duas fontes, grão de uma linha por entidade-decisão, cardinalidade prevista e relógios point-in-time pelo dono comum. Devolve identidade de fonte DECLARED_NOT_READ e join_executed=false: digest informado é declaração, não hash de bytes lidos. Este arquivo cobre a etapa L2 de uma skill corrente L0/audit; os runners B1 posteriores são módulos distintos. O preflight não mede cobertura real nem autoriza join histórico. |

<a id="mt14-enforcement-code-map-file-021"></a>
#### 21. `postflight.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-eda-profissional/scripts/postflight.py) · [MT19: explicação do mecanismo](MT-parte-iv.md#mt19-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-eda-profissional/scripts/postflight.py` · SHA-256 `43f972435f4fcb8e7a5da3c4407ff9d2a3e076f7c028c2f224bca40037480e0a` |
| Papel e motivo técnico | Transformar payload enforced em conclusão somente após Postflight PASS reverificado. |
| Mecanismo | finalize confere enforcement_entrypoint, Receipt via runner e build_postflight; finalize_or_raise chama verify_finalized e lança CompletionNotAuthorized se não autorizado; verify_finalized confronta claim. |
| Nomes disponibilizados | ["CompletionNotAuthorized", "finalize", "finalize_or_raise", "verify_finalized", "main"] |
| Entradas | Payload L4, handoff, assistant_root opcional. |
| Saídas | Payload final com completion COMPLETED/NOT_COMPLETED ou exceção; verificação. |
| Efeitos | Lê contrato/release/verifier; sem escrita; completed autodeclarado não basta. |
| Dependências e momento de uso | hub_scripts.skill_execution.postflight, EDA run.verify_receipt. |
| Como interpretar este arquivo | O finalizador recebe payload enforced, handoff e Receipt verificado, constrói Postflight e compara o claim de conclusão. finalize_or_raise interrompe se verify_finalized não confirmar autorização; um campo completion=COMPLETED editado no JSON não basta. Ele lê evidências e não escreve resultado. O capítulo MT19 explica a finalização L4 e seus limites. |

<a id="mt14-enforcement-code-map-file-022"></a>
#### 22. `preflight.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-eda-profissional/scripts/preflight.py) · [MT17: explicação do mecanismo](MT-parte-iv.md#mt17-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-eda-profissional/scripts/preflight.py` · SHA-256 `a48d4a3986cd4523bf1c04d0c96b8e2ec7aa413cdef792f97df1d3a1c5e10bae` |
| Papel e motivo técnico | Expor CLI L2 de EDA sem rodar quick_profile. |
| Mecanismo | Converte context-json, chama run_preflight e emite resultado; erro de entrada vira BLOCKED. |
| Nomes disponibilizados | ["preflight", "main"] |
| Entradas | Contexto JSON com condições do contrato. |
| Saídas | PreflightResult serializado e exit 0/2. |
| Efeitos | Lê contrato e fachadas; confere a presença dos templates sem ler seus bytes; não chama EDA nem grava. |
| Dependências e momento de uso | hub_scripts.skill_execution.run_preflight. |
| Como interpretar este arquivo | Este adaptador converte contexto JSON de CLI para run_preflight e serializa PASS/BLOCKED, com erro de entrada tratado como bloqueio. Lê contrato e fachadas, confere a presença dos templates sem ler seus bytes, mas não chama quick_profile nem calcula EDA. Mesmo na skill L4/enforce, PASS aqui é só disponibilidade anterior ao runner; Receipt e Postflight ainda precisam ocorrer. |

<a id="mt14-enforcement-code-map-file-023"></a>
#### 23. `run.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-eda-profissional/scripts/run.py) · [MT18: explicação do mecanismo](MT-parte-iv.md#mt18-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-eda-profissional/scripts/run.py` · SHA-256 `f4153e62a4e11d6d1ecbd6c9ff13821e17dbc6c7f3c00f8fce860d9a2716f641` |
| Papel e motivo técnico | Executar primitive quick_profile sob release e preflight canônicos L3. |
| Mecanismo | Verifica manifest Git blob, deriva numeric_columns do Spark e recusa conflito, chama preflight, marca quick_profile called/completed, digest result e constrói Receipt V1; verify_receipt observa release corrente. |
| Nomes disponibilizados | ["run", "is_canonically_compliant", "verify_receipt", "main"] |
| Entradas | table_name, contexto, sample_fraction, max_categories, seed. |
| Saídas | Payload trace/receipt/result; status BLOCKED/FAIL/PASS. |
| Efeitos | Lê schema Spark e executa quick_profile; pode disparar ações da primitive; não grava diretamente. |
| Dependências e momento de uso | pyspark no runtime, hub_scripts.quick_profile, preflight, receipt V1. |
| Como interpretar este arquivo | O core EDA confere release, observa schema Spark para derivar numeric_columns, recusa conflito com valor declarado e chama preflight. Depois invoca quick_profile, marca called e completed em momentos distintos e emite Receipt V1. A primitive pode disparar ações Spark; o runner não grava diretamente. PASS L3 comprova essa etapa, mas não autoriza COMPLETED sem recursos adicionais e Postflight. |

<a id="mt14-enforcement-code-map-file-024"></a>
#### 24. `run_enforced.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../skills/hub-ml-eda-profissional/scripts/run_enforced.py) · [MT19: explicação do mecanismo](MT-parte-iv.md#mt19-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/skills/hub-ml-eda-profissional/scripts/run_enforced.py` · SHA-256 `9af22d9850ed6c2a7243686fad20f57250f77b6eb1e5030d5c2a045fead071d1` |
| Papel e motivo técnico | Acrescentar evidência de recursos/templates aplicáveis à execução core EDA. |
| Mecanismo | Chama runner L3; importa helper por ID, registra called antes e completed após retorno; lê templates/digests, chama recursos condicionais, acumula gaps/artifacts e marca PENDING_POSTFLIGHT. |
| Nomes disponibilizados | ["CanonicalExecutionBlocked", "run_enforced", "main"] |
| Entradas | table_name, contexto efetivo, parâmetros, display_fn, resolved_theme, strict. |
| Saídas | Payload com artifacts, enforcement_status PASS/INCOMPLETE e completion pendente ou CanonicalExecutionBlocked. |
| Efeitos | Pode executar Spark/renderer via callbacks reais; não persiste; nenhum helper chamado por mera importação. |
| Dependências e momento de uso | EDA run.py, importlib, pyspark, IPython display opcional, resources do contrato. |
| Como interpretar este arquivo | O executor L4 chama o core e, para cada recurso aplicável, importa helper, registra called antes da invocação e completed só após retorno. Lê templates realmente para obter digests e pode chamar callbacks de Spark e renderer; import sozinho não satisfaz cobertura. A normalização deriva pk_columns_available da lista de chaves válidas; sem chave estabelecida, data_quality_check é condicional não aplicável. Quando exigido, o recurso precisa dos insumos e da chamada correspondentes. Com strict=False, uma falha do core mantém NOT_COMPLETED, mas gaps após core PASS podem terminar em PENDING_POSTFLIGHT; os dois ramos não autorizam conclusão: na falha do core, `authorized=false` acompanha `NOT_COMPLETED` e o campo `claim_allowed` está ausente; no ramo pendente após core PASS, `authorized=false` e `claim_allowed=false` acompanham `PENDING_POSTFLIGHT`. A etiqueta isolada não autoriza conclusão, que depende do Postflight. |



<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
