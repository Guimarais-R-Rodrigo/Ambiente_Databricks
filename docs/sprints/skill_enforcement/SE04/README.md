# SE04 — Execution Receipt formal

> **Nota administrativa — 06/10/2026.** SE04 integrada pela PR #77 em `d74b2fcb`. As pendências de abertura de PR, certificação e merge abaixo descrevem candidatas anteriores. [História SEF](../README.md) e [operação atual SER](../../skill_enforcement_rollout/README.md) distinguem o fechamento histórico da policy vigente. Esta nota não reclassifica resultados nem amplia o escopo certificado.

## Registro histórico preservado

## Estado

**IMPLEMENTAÇÃO FUNCIONAL CONSTRUÍDA; certificação local e homologação determinística no Databricks Free observadas com PASS. Release candidate ainda depende da recertificação final do HEAD documental e da abertura controlada da PR.**

Branch: `sef/SE04-execution-receipt`  
Baseline: `main@216df1544c2b21a8ff94bb5ce51fd84b8a444057`  
Skill piloto: `hub-ml-eda-profissional`  
Contrato: v0.1, `mode="audit"`.

Base de certificação funcional observada: `9d7d09daaf943e857b468a21f6f774560c519f7e`.

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

## Gates observados

No HEAD funcional `9d7d09daaf943e857b468a21f6f774560c519f7e`:

```text
LOCAL_CERTIFICATION = PASS
scope               = FULL_SE04_LOCAL
DERIVED_STALE       = false
failures            = 0
DATABRICKS_FREE     = PASS
```

No Databricks Free, a publicação canônica foi verificada por inventário e por conteúdo, com `557/557` arquivos controlados exportados e comparados. O import individual do probe apresentou `PROTOCOL_ERROR` de transporte; o fallback `workspace import-dir` concluiu com sucesso e o probe remoto foi comparado ao arquivo local antes da execução.

`SE04_FREE_PROBE_V1` terminou com `status=PASS`, `published_package_mutated=false` e `persistent_writes_performed=false`. Todos os nove cenários do probe tiveram `ok=true`, incluindo Receipt válido, tampering, output incompatível, stale/replay, ausência de Receipt em rotas manuais, quebra de integridade da release, conflito de provenance e falha da primitive sem fallback.

## Gates restantes antes de release candidate/merge

1. recertificar o HEAD documental final localmente, sem alterar o produto publicado;
2. confirmar branch sem drift em relação à `main` (`behind_by=0`);
3. somente então abrir a PR da SE04;
4. consumir GitHub Actions uma única vez na candidata de release, conforme a política de créditos;
5. não fazer merge sem aceite humano explícito.

A SE05 continua fora do escopo e não foi iniciada.

## Documentos

- [DESENHO_TECNICO.md](DESENHO_TECNICO.md)
- [THREAT_MODEL.md](THREAT_MODEL.md)
- [TESTES.md](TESTES.md)
- [EVIDENCIAS_LOCAIS.md](EVIDENCIAS_LOCAIS.md)
- [RUNBOOK_FREE.md](RUNBOOK_FREE.md)
- [GUIA_USUARIO.md](GUIA_USUARIO.md)
- [CHECKPOINT.md](CHECKPOINT.md)
