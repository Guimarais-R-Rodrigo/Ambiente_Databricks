# SE04 — desenho técnico do Execution Receipt

## 1. Fluxo

```text
release íntegra
  → provenance/runtime válido
  → preflight PASS
  → quick_profile chamada
  → quick_profile concluída
  → ExecutionTraceV0 PASS
  → output digest correspondente
  → build_execution_receipt(...)
  → ExecutionReceiptV1
```

O Receipt não copia o payload de negócio. Ele carrega metadados probatórios e digests suficientes para vincular o resultado atual à execução observada.

## 2. Componentes

- engine: `ambiente_fonte/.assistant/hub_scripts/skill_execution/receipt.py`;
- emissor: `skills/hub-ml-eda-profissional/scripts/run.py::run`;
- verifier de baixo nível: `verify_execution_receipt(...)`;
- wrapper de release corrente: `scripts/run.py::verify_receipt(...)`;
- manifest: `skills/hub-ml-eda-profissional/release_manifest.json`;
- testes: `tools/tests/test_skill_enforcement_se04.py` e `test_skill_enforcement_se04_runner.py`;
- probe Free: `tools/skill_enforcement/se04_free_probe.py`.

Nenhum componente implementa postflight obrigatório.

## 3. Versionamento

Nome lógico: `ExecutionReceiptV1`.  
Campo: `receipt_version = "1.0"`.

Versão desconhecida retorna `UNSUPPORTED_VERSION`; não há downgrade silencioso.

## 4. Serialização e digests

Serialização canônica:

```text
JSON UTF-8
sort_keys=true
separators=(",", ":")
ensure_ascii=false
```

Bindings usam SHA-256. Contract e runner continuam identificados pelos `git_blob_sha1` já observados/protegidos pelo release manifest da SE03; o Receipt registra esses fingerprints e o wrapper confronta-os com a release corrente.

## 5. Schema lógico V1

Campos superiores obrigatórios:

```text
receipt_version
receipt_id
run_id
skill
entrypoint
execution_status
canonical_compliance
preflight_status
release
bindings
resources
decisions
templates_consumed
provenance_summary
fallback_used
writes_performed
blocking_issue_codes
integrity
```

### `release`

```text
manifest_name
manifest_sha256
contract_git_blob_sha1
runner_git_blob_sha1
```

### `bindings`

```text
trace_sha256
input_sha256
output_sha256
```

### `resources`

```text
resolved
imported
called
completed
protected_primitive
```

`imported` é `{status: "NOT_OBSERVABLE", items: []}` enquanto não existir instrumentação mecânica capaz de provar import efetivo. O Receipt não converte existência/resolução em import presumido.

### `decisions`

Cópia probatória normalizada das decisões objetivas registradas no trace: `item_id`, `item_type`, `applicable`, `resolved`.

### `templates_consumed`

Também permanece `NOT_OBSERVABLE` nesta sprint. Resolver um arquivo de template no preflight não prova que seu conteúdo foi consumido durante a execução.

### `provenance_summary`

Registra somente `source` e `conflict` por chave. Valores de negócio não são copiados. Para `numeric_columns`, emissão exige `source=runtime_derived` e `conflict=false`.

## 6. Identidade do Receipt

```text
receipt_id = "er1:" + sha256(canonical_json(receipt_body))
```

Modificar qualquer campo protegido sem recalcular o identificador produz `INVALID`. Mesmo que um atacante recalcule um Receipt internamente coerente, o verifier ainda o confronta com trace, output e release atuais; divergências produzem `INCOMPATIBLE`. Isso continua não sendo autenticação criptográfica contra comprometimento completo da release/verifier.

## 7. Emissão

`build_execution_receipt(...)` retorna Receipt somente quando:

- trace V0.1 conhecido;
- skill e entrypoint correspondem à skill piloto;
- `status=PASS`;
- `preflight_status=PASS`;
- run id e digests têm formato válido;
- output atual confere com `output_digest`;
- primitive protegida aparece em `resources_called` **e** `resources_completed`;
- provenance de `numeric_columns` é runtime-derived sem conflito;
- `blocking_issues=[]`;
- `fallback_used=false`;
- `writes_performed=false` no alcance atual.

Qualquer falha retorna `None`; não existe Receipt parcial com canonical compliance `PASS`.

## 8. Verificação

Estados:

- `VALID`: forma, identidade, bindings, run e release compatíveis;
- `ABSENT`: Receipt não existe;
- `MALFORMED`: schema/tipos/campos obrigatórios inválidos;
- `INVALID`: integridade interna do Receipt não fecha, por exemplo `receipt_id` adulterado;
- `INCOMPATIBLE`: Receipt pode ser internamente coerente, mas não corresponde ao trace/output/release esperados;
- `STALE_REPLAYED`: `expected_run_id` não corresponde ao Receipt/trace apresentado;
- `UNSUPPORTED_VERSION`: versão não conhecida.

Somente `VALID` produz `canonical_compliance="PASS"` no objeto de verificação.

## 9. Bindings

- trace: `sha256(canonical_json(trace))`;
- input: reutiliza `input_digest` runtime da SE03;
- output: reutiliza `output_digest` e recalcula o resultado atual durante a verificação;
- manifest: SHA-256 do arquivo atual;
- contract/runner: fingerprints git-blob observados e protegidos pelo manifest.

## 10. `resources_called` × `resources_completed`

`resources_called` significa tentativa efetiva de invocação. `resources_completed` só é preenchido depois do retorno bem-sucedido da primitive. Assim, falha de `quick_profile` não pode parecer conclusão válida apenas porque houve chamada.

## 11. Replay/staleness

O Receipt inclui `run_id`, faz binding ao trace e aceita `expected_run_id` externo no verifier. Isso rejeita reutilização entre runs quando o consumidor conhece o run atual.

A SE04 não alega anti-replay universal sem nonce/estado confiável externo. Introduzir armazenamento de nonce, assinatura ou attestation permanece fora de escopo.

## 12. Relação com SE05

A API foi desenhada para que a SE05 possa futuramente consumir `verify_receipt()` e exigir `VALID`. Nenhuma chamada automática desse tipo foi conectada ao fluxo de conclusão nesta sprint.
