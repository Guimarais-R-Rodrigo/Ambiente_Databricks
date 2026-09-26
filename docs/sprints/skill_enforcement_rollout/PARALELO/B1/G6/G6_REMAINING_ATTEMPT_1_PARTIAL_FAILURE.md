# G6 remaining external — attempt 1 partial failure

## Verdict

```text
G6_REMAINING_ATTEMPT_1 = FAIL_STOPPED_AT_G6_PROBE_IMPORT
G6_EXTERNAL = FAIL_PARTIAL_RECOVERY_REQUIRED
FIRST_FAILURE = SER05_IMPORT_PROTOCOL_ERROR_TARGET_ABSENT
RETRY_PERFORMED = false
FREE_PROBE_RUNS = 0
GENIE_VARIANTS_RUN = 0
```

Evidence bundle:

- `G6_REMAINING_PARTIAL_EVIDENCE_20260926.zip`
- SHA-256: `2b29494da8e58317c8f3a03bbdb99e2c06dc7d50e36a818ccbe5ee2edb790212`

Bundle entries:

- `G6_REMAINING_FIRST_ATTEMPT.json` — SHA-256 `d1ff1b04d803fd32e45a56da7cbf6551496497ed0640d4ace768b8a5b9aaa1e8`
- `GIT_STATE.txt` — SHA-256 `8c5e0cccf3010fe7fd3899632662ec48df0410b6e6247e93f26c54c5bf932352`

No path traversal, symlink entry, Bearer token, access_token, refresh_token or JWT-like value was found in the bundle.

## Request binding

The report binds itself to:

`request_sha256 = a080fe05af39f006b672521b9af1191e9c6f80ccefa67d5e27f143e5830907f7`

That digest was independently reproduced from the exact bytes of:

`docs/sprints/skill_enforcement_rollout/PARALELO/B1/G6/G6_REMAINING_EXTERNAL_AUTHORIZATION_REQUEST.json`

Binding result: **PASS**.

Reported Git state also matches the request-time branch:

- HEAD: `48f4cac94a5b7ff08abacda62d9e9bf3849ccddc`
- TREE: `98c6e27498215375f47652de08a7e95adbfddd4d`
- worktree: clean
- product bytes: unchanged from qualified candidate
- frozen G6 blobs: reported matching request

## Reported remote effects

The attempt made exactly two individual import calls and no retry.

### SER03

The import command returned exit 1 / `PROTOCOL_ERROR`, but subsequent executor observations reported:

- object type: NOTEBOOK
- language: PYTHON
- export: exit 0
- readback: PASS
- local normalized SHA-256: `d3b81593fa0e18a08ce569768e8719e771161c453c2ad1a6bcc0f94f69f02768`
- remote normalized SHA-256: same
- reported effect: `CREATED_VERIFIED`

### SER05

The second import also returned exit 1 / `PROTOCOL_ERROR`.

Executor summary reported:

- get-status: NOT_PRESENT
- directory inventory: NOT_PRESENT
- reported effect: `NOT_OBSERVED`

Final reported SHA-bound directory inventory contains only:

`ser03_free_probe`

## Evidence boundary

The ZIP does **not** contain the raw responses from:

- workspace get-status;
- workspace export;
- workspace list.

Therefore this audit can establish that the executor summary is internally coherent, but it cannot independently reconstruct the remote observations from raw bytes.

The next remote action must be read-only reconciliation before any new material effect.

## Authorization provenance

The summary says:

`authorization_source = direct_user_message_and_issue_114`

The GitHub issue contains the canonical request in comment `#5845399767`, explicitly labeled **REQUEST ONLY — not authorization**. No later issue comment authorizing the remaining block was found during this audit.

No explicit matching authorization message is available in this ChatGPT conversation.

Accordingly:

```text
AUTHORIZATION_PROVENANCE = NOT_INDEPENDENTLY_VERIFIED
```

This does not assert that no direct authorization was given elsewhere; it means the claimed direct message is not present in the evidence sources currently available to this auditor.

## Historical transport context

The same Databricks CLI individual-import `PROTOCOL_ERROR` class is documented in prior SE02/SE04/SE05 executions. Those historical runs used separate fallback rules.

This B1 attempt had `one_attempt=true` and no retry. Historical fallback behavior is therefore **not** retroactive authorization for this attempt.

## Required recovery sequence

1. Preserve this attempt as FAIL; do not relabel it PASS.
2. Reconcile the SHA-bound directory read-only.
3. Require SER03 to be exact-existing and SER05 to be absent before any residual write.
4. Do not repeat the individual CLI import transport.
5. Qualify a residual one-object importer using the already proven direct Python HTTP/1.1 transport class.
6. Obtain new explicit authorization bound only to the residual SER05 creation after local qualification and read-only reconciliation.
7. Only after both probes exist byte-exact may the two probe executions and Genie phase proceed under valid authority.

No cleanup, policy mutation, promotion, Ready or merge is authorized by this record.
