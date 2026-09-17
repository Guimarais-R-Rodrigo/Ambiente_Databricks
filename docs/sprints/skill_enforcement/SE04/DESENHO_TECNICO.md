# SE04 — desenho técnico do Execution Receipt

## 1. Arquitetura

Fluxo alvo:

```text
ExecutionTraceV0 + resultado
        ↓
validação de pré-condições de emissão
        ↓
canonical serialization
        ↓
ExecutionReceiptV1
        ↓
verifier determinístico
```

O receipt não copia o payload de negócio. Ele faz binding por digest ao trace e ao output e carrega apenas metadados probatórios necessários à auditoria.

## 2. Localização

- engine de receipt: `ambiente_fonte/.assistant/hub_scripts/skill_execution/receipt.py`;
- emissão: chamada pelo runner `skills/hub-ml-eda-profissional/scripts/run.py` somente após trace `PASS`;
- tooling de auditoria: wrapper/CLI da skill poderá usar o mesmo verifier, sem duplicar lógica;
- schema lógico: documentado aqui e coberto por testes; não cria contrato genérico para todas as skills nesta sprint.

O módulo fica no pacote `skill_execution` porque serialização, binding e verificação são infraestrutura do SEF, mas a implementação V1 permanece parametrizada/congelada para a skill piloto.

## 3. Versionamento

Nome lógico: `ExecutionReceiptV1`  
Campo: `receipt_version = "1.0"`.

Versões desconhecidas são rejeitadas. Não existe fallback silencioso entre versões.

## 4. Serialização canônica

Algoritmo:

```text
JSON UTF-8
sort_keys=true
separators=(",", ":")
ensure_ascii=false
```

O digest de binding usa SHA-256 sobre os bytes dessa serialização. Ordenação de dicionário no runtime não pode alterar o digest.

## 5. Identidade

`run_id` continua vindo do runner/trace.

`receipt_id` é derivado deterministicamente do corpo protegido do receipt:

```text
receipt_id = "er1:" + sha256(canonical_json(receipt_body))
```

O `receipt_id` serve simultaneamente como identidade estável do comprovante e evidência de alteração acidental do corpo. O uso de SHA-256 não é assinatura/autenticação contra atacante capaz de reescrever código e recalcular hashes.

## 6. Schema lógico V1

Campos obrigatórios:

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
provenance_summary
fallback_used
writes_performed
blocking_issue_codes
integrity
```

`release` contém:

- `manifest_name`;
- `manifest_sha256`;
- `contract_git_blob_sha1`;
- `runner_git_blob_sha1`.

`bindings` contém:

- `trace_sha256`;
- `input_sha256`;
- `output_sha256`.

`resources` contém:

- `resolved`;
- `called`;
- `protected_primitive`.

`provenance_summary` contém somente metadados necessários para auditoria, por exemplo `numeric_columns -> {source, conflict}`; valores de negócio não são copiados.

`integrity` contém convenções de serialização/digest e `release_integrity="PASS"`.

## 7. Emissão

Receipt V1 somente é emitido quando todos os requisitos abaixo são verdadeiros:

- trace é mapping V0 conhecido;
- `trace.status == "PASS"`;
- `preflight_status == "PASS"`;
- skill/entrypoint correspondem à skill piloto;
- manifest/contract/runner digests estão presentes;
- `input_digest` e `output_digest` estão presentes;
- output atual confere com `trace.output_digest`;
- `quick_profile` está em `resources_called`;
- `fallback_used is False`;
- `writes_performed is False` no alcance atual;
- `numeric_columns` tem source `runtime_derived` e não está em conflito;
- não há blocking issues.

Falha em qualquer condição produz **ausência de receipt válido**, não receipt `PASS` parcial.

## 8. Verificação

O verifier recebe o payload `{trace, receipt, result}` e expectativas do contexto atual. Ele classifica:

- `VALID`;
- `ABSENT`;
- `MALFORMED`;
- `INVALID`;
- `INCOMPATIBLE`;
- `STALE_REPLAYED`;
- `UNSUPPORTED_VERSION`.

Semântica:

- **MALFORMED**: forma/tipos/campos obrigatórios inválidos;
- **INVALID**: receipt internamente incoerente ou adulterado;
- **INCOMPATIBLE**: receipt íntegro em si, mas incompatível com trace/output/skill/release esperados;
- **STALE_REPLAYED**: receipt/run não corresponde ao run atual explicitamente esperado pelo harness/consumidor;
- **VALID**: todas as verificações pertinentes passam.

A verificação V1 não bloqueia automaticamente a conclusão da skill; essa conexão pertence à SE05.

## 9. Bindings

### Trace

`trace_sha256 = sha256(canonical_json(trace))`.

Qualquer alteração no trace após emissão invalida o binding.

### Output

O receipt copia o `output_digest` já derivado na SE03 e o verifier também recalcula o digest do resultado atual. Isso detecta output alterado, recriado de forma diferente ou receipt reutilizado com outro resultado.

### Release

O receipt vincula o manifest SHA-256 e fingerprints observados de contract/runner. O verifier também compara com as expectativas da release atual quando fornecidas pelo wrapper do runner.

### Input

`input_sha256` é o `input_digest` já derivado pelo runner. O receipt não copia tabela/contexto bruto.

## 10. Replay/staleness

A proteção V1 é deliberadamente explícita e contextual:

- `run_id` participa do receipt;
- o verifier pode receber `expected_run_id`;
- receipt de outro run é `STALE_REPLAYED` quando confrontado com o run atual esperado;
- output/trace bindings impedem reutilização trivial em outro payload.

Sem um nonce externo confiável, armazenamento de estado ou assinatura, a SE04 não alega anti-replay universal. A proteção é suficiente para o harness e consumidores que conhecem o run esperado.

## 11. Provenance

O receipt nunca usa `agent_declared` para legitimar fato que o runner consegue derivar. `numeric_columns` só permite emissão quando a provenance registrada é `runtime_derived` e `conflict=false`.

## 12. Evolução futura

A SE05 poderá consumir `verify_execution_receipt(...)` e exigir `VALID` antes de homologar conclusão. A API é desenhada para permitir esse consumo sem implementar o gate agora.
