# P2 R7 — fechamento da qualificação local e auditoria

## Candidata qualificada

```text
candidate_sha = 08c2a93c4c9dede1e759abe28c07242b4116f47e
candidate_tree = a2b1b8c805044ff2e1898da3190414afab9140a7
baseline/main = 4ba7f551767d847381df1556ed937116258fa77d
round_id = B1ROUND-70fcaf3b6abd4cb58831d2c09a0c1c38
profile_digest = 26d90b6c6c6512e7b3b486e902d9596ff2fa7c12ff79a42658d3513b463c5143
release_spec_digest = b0610b49a8a1eb2d4bb8ba7246ae69f5436108e7a6813a8effb6c2e0446c3cc0
```

## Gates formais

```text
P2_R7_01_PREFLIGHT = PASS
P2_R7_02_METATESTS = PASS / 24/24 / 0 failures / 0 errors / 0 skips
CLI_PROJECTION_CHECK = PASS
REAL_PREFLIGHT_CLI_CHECK = PASS / 4 of 4
P2_R7_03_PREPARE = PASS
P2_R7_04_CAMPAIGN = PASS
P2_R7_05_PACKAGE = PASS
repo_mutation = false
```

## Ambiente

```text
OS = Windows 10.0.26200
filesystem = NTFS
CPython = 3.12.10
implementation = CPython
isolated = true
architecture = 64bit
machine = AMD64
requirements_dev_sha256 = 5df30220f76f9d3fe34512d03446a405fe703223442db4cf72a29ba72693bd9a
requirements_temas_dev_sha256 = eab43ce8b26d15e11186f735ef885b4b3fe844479894190fdb23d16db4a3a294
```

## Campanha

Todas as seis tasks concluíram PASS:

- `b1.ser03.preflight`;
- `b1.ser05.preflight`;
- `b1.ser03.execute_verify`;
- `b1.ser03.domain_audit`;
- `b1.ser05.domain_audit`;
- `b1.evidence_contract_audit`.

Os 10 command records observados tiveram `exit_code=0`, `WINDOWS_JOB_OBJECT`, nenhum timeout, nenhum descendente residual e cleanup completo. Pico observado: 2 tasks totais e 1 auditor.

## Bundle / auditoria independente

```text
AUDIT_BUNDLE =
SER_B1_P2_R7_08c2a93c4c9d_AUDIT_BUNDLE.zip

sha256 =
ff771504e47ab1b9fa10bcc6c925ceed84508ac2cb173e325e85bf8e09b96deb

size_bytes =
37608

outer_manifest = PASS
share_manifest = PASS
envelope_valid = true
secret_scan = PASS
secret_findings = 0
campaign_verifier_valid = true
campaign_verifier_issues = []
```

A sanitização do SHARE modifica bytes que contêm paths locais. Por desenho RAW permanece privado; portanto hashes RAW de arquivos sanitizados não são rederiváveis diretamente do SHARE público. O envelope RAW/SHARE qualificado registra identidades distintas e passou.

## Estado normativo

```text
R7_FULL_LOCAL_QUALIFICATION = PASS
R7_INDEPENDENT_AUDIT = PASS
G4_LOCAL_CERTIFICATION = PASS
G5_AUDIT = PASS
G6_EXTERNAL = NOT_RUN_REQUIRES_EXPLICIT_AUTHORIZATION
G7_PROMOTION_PROPOSAL = NOT_AUTHORIZED
SER03_L3 = NOT_PROMOTED
SER05_L2 = NOT_PROMOTED
POLICY_CHANGED = false
READY = NOT_AUTHORIZED
MERGE = NOT_AUTHORIZED
```

O PASS pertence ao SHA qualificado acima. Este commit de fechamento é documental e não transporta a certificação para um novo SHA funcional.
