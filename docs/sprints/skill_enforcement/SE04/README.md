# SE04 — Execution Receipt formal

## Estado

**IMPLEMENTAÇÃO FUNCIONAL CONSTRUÍDA; gates oficiais local/Free ainda não observados neste ambiente.**

Branch: `sef/SE04-execution-receipt`  
Baseline: `main@216df1544c2b21a8ff94bb5ce51fd84b8a444057`  
Skill piloto: `hub-ml-eda-profissional`  
Contrato: v0.1, `mode="audit"`.

## Objetivo

A SE04 transforma a evidência estrutural da SE03 em um `ExecutionReceiptV1` formal, versionado, verificável e auditável. A pergunta operacional passa a ser:

> existe um Receipt formal `VALID` que vincula este resultado ao trace, input, release e run canônico esperados?

A resposta dessa pergunta continua separada da decisão de bloquear a conclusão. O **postflight fail-closed de produção permanece integralmente reservado à SE05**.

## O que foi implementado

- engine `hub_scripts.skill_execution.receipt`;
- `ExecutionReceiptV1`, `receipt_version="1.0"`;
- serialização JSON canônica determinística e SHA-256;
- `receipt_id = er1:sha256(body)`;
- bindings de trace, input e output;
- binding de manifest, execution contract e runner;
- recursos `resolved`, `called` e `completed`;
- `imported` e `templates_consumed` como `NOT_OBSERVABLE` quando não há instrumentação mecânica suficiente;
- provenance resumida sem copiar payload de negócio;
- verifier com estados `VALID`, `ABSENT`, `MALFORMED`, `INVALID`, `INCOMPATIBLE`, `STALE_REPLAYED` e `UNSUPPORTED_VERSION`;
- emissão do Receipt exclusivamente pelo runner após execução canônica `PASS`;
- `resources_completed` preenchido somente após retorno bem-sucedido da primitive protegida;
- wrapper `run.py::verify_receipt()` para confrontar Receipt com a release corrente;
- release manifest protegendo também o receipt engine;
- suíte adversarial SE04 e suíte de integração com o runner;
- perfil `se04` no certifier local;
- probe determinístico para Databricks Free;
- documentação operacional e guia não técnico.

## Invariantes preservados

- entrypoint canônico continua `skills/hub-ml-eda-profissional/scripts/run.py::run`;
- primitive protegida continua somente `hub_scripts.quick_profile.quick_profile`;
- `ExecutionTraceV0` continua precursor técnico, sem copiar o resultado de negócio;
- `numeric_columns` continua `runtime_derived`; conflito declarado bloqueia;
- falha da primitive não recebe fallback manual;
- `mode="audit"` não mudou;
- E02 histórico não é reclassificado e `GENIE_BEHAVIORAL_SCREENING=MIXED` é preservado;
- nenhum dado corporativo foi introduzido;
- não existe `postflight.py` de produção nesta sprint.

## Reconciliação SE04 × SE05

O Plano Mestre original posiciona a validação final do Receipt dentro do postflight da SE05. A revisão pós-SE03 e o escopo desta sprint exigem que o Receipt seja verificável deterministicamente já na SE04. A reconciliação adotada é:

- **SE04:** constrói, emite e verifica o Receipt como objeto/evidência;
- **SE05:** decide fail-closed se uma conclusão homologada pode ocorrer sem Receipt válido.

Assim, `verify_receipt()` não é um postflight e não bloqueia por si só a apresentação de uma resposta final.

## Limite criptográfico

SHA-256 fornece **tamper evidence + deterministic binding + traceability**. Ele não autentica a origem contra um atacante capaz de alterar arbitrariamente código, release e verifier e recalcular todos os hashes. HMAC, PKI ou attestation externa não foram introduzidos por não existir, nesta sprint, uma âncora de confiança que justificasse essa complexidade.

## Gates ainda necessários antes de release candidate

1. executar o perfil oficial `se04` do certifier em checkout completo e worktree limpa;
2. materializar `Novo_Ambiente_Simulado/` exclusivamente por `tools/render_simulado.py --write` e exigir drift zero;
3. passar snapshot README/estrutura;
4. publicar/verificar por conteúdo no Databricks Free;
5. executar `SE04_FREE_PROBE_V1` e preservar o JSON bruto;
6. somente com esses gates observados, congelar release candidate e abrir PR.

Nenhuma PR deve ser aberta antes desses itens.

## Documentos

- [DESENHO_TECNICO.md](DESENHO_TECNICO.md)
- [THREAT_MODEL.md](THREAT_MODEL.md)
- [TESTES.md](TESTES.md)
- [EVIDENCIAS_LOCAIS.md](EVIDENCIAS_LOCAIS.md)
- [RUNBOOK_FREE.md](RUNBOOK_FREE.md)
- [GUIA_USUARIO.md](GUIA_USUARIO.md)
- [CHECKPOINT.md](CHECKPOINT.md)
