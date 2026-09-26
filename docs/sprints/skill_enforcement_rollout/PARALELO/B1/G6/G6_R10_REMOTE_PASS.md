# G6 R10 remote material PASS — audited handoff

## Verdict

```text
G6_DIRECT_HTTP11_U2M_REMOTE_PACKAGE_WRITE_R10 = PASS
POST_WRITE_FULL_CONTENT_VERIFY = REQUIRED_NOT_RUN
AUTHORIZATION_R10 = CONSUMED
SECOND_WRITE_ATTEMPT = NOT_AUTHORIZED
```

This record incorporates the Codex execution report received on 2026-09-26 and checks it against the frozen R10 publisher, manifest and GitHub authorization contract.

## Frozen identity

- publisher freeze SHA: `b89cc5f1579caf8af6784ca5761c114fb6a6df09`
- publisher freeze tree: `45ddb0252795c6ba70fbbc04740346c1cfd082cc`
- manifest SHA-256: `067e05e6f228efddbf963edf02a0059108a6a58fc97be4441087d23e5be4ca3a`
- publisher package SHA-256: `b4c186b2838bfa04e6d5475d6a7d23561a8957b3fcea9539be612d11e032f0f6`
- authorization ref: `issue#114:comment#5840353763`

## Authorization-record reuse

- existing directory: true
- existing record: true
- record reused: true
- record overwritten: false
- record mutated: false
- semantic validation: PASS
- SHA-256 before: `b25b08c8d66a156b0618a9190e9c2258e311a0381157a888e82c185baa250ab0`
- SHA-256 immediately pre-execute: same
- consumed before execute: false
- consumed after execute: true
- consumption marker present: true

The prior procedural `BLOCKED_PRECONDITION` remains historical and did not consume this authorization.

## Convergent preflight

```text
parent_directories = 16
create_candidates = 15
overwrite_candidates = 1
create_required = 15
overwrite_required = 1
already_correct = 0
material_writes_required = 16
```

The three previously bootstrapped parent directories were verified and were not recreated. `domain-context-readme` remained excluded and was not rewritten.

## Material execution

```text
exit_code = 0
publisher_status = PASS
record_count = 16
writes_started = 16
write_success = 16
verification_pass = 16
already_correct = 0
created = 15
updated = 1
unknown = 0
authorization_consumed = true
```

All sixteen per-object readbacks were reported PASS with remote normalized hash equal to local.

## Frozen-code audit

The frozen publisher is consistent with the reported transport and safety contract:

- U2M token is requested just-in-time with `databricks auth token`;
- the token remains a local variable and is not inserted into the result object;
- material writes use Python stdlib `http.client.HTTPSConnection`;
- each material object invokes one HTTP/1.1 `POST /api/2.0/workspace/import`;
- request payload is JSON with base64 content;
- the material writer contains no automatic retry loop;
- an exception after `write_started` is classified `UNKNOWN` and stops execution;
- the manifest requires a post-write full-content verification.

## Evidence boundary

The Codex report states that the only textual evidence file is the external `RUN_STATE.json` and that it contains neither token fields nor an `Authorization: Bearer` value. The `RUN_STATE.json` bytes were not attached to this ChatGPT conversation, so this repository record does not claim an independent byte-level hash verification of that local evidence file.

## Next gate

Run a separate read-only full verification of the entire rendered package:

```text
tools/publicar_free.py --verify --conteudo
```

Use profile `FREE`, bind the expected host to `https://dbc-72c8503a-bc27.cloud.databricks.com`, and persist a local JSON report with `--relatorio`.

This gate has effect `NONE`: no publication, import, deletion, cleanup, probe, Genie execution, policy mutation, promotion, Ready transition or merge is authorized.
