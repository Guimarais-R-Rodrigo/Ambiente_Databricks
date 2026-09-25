# G6 R6 residual publication plan

Source of truth: R5 partial-state reconciliation sanitized evidence SHA-256
`d255398df799f0262872db4b5b327cb4dc3b9be67178746923a009138f702435`.

Already correct and excluded from future material write:
- `domain-context-readme`

Residual manifest:
- 16 total;
- 15 create-if-missing;
- 1 conditional policy overwrite;
- exact ordered IDs are the entries in `g6_publication/manifest.json`.

R6 also removes hardcoded 17/16/1 validation logic. Manifest-declared counts are mechanically checked against actual entry/precondition counts.

No remote write is authorized by this plan.
