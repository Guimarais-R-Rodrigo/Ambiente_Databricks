# G6 publisher R3 — adversarial audit

Strategy: fix the whole adjacent failure class before another Codex/remote round.

Addressed:
- CLI/API workspace-list JSON variants;
- immediate-parent-missing recursion without free-form error parsing;
- all target parents must already exist as DIRECTORY, so no hidden mkdirs effect;
- FILE import/export uses RAW; only declared notebook uses SOURCE/PYTHON;
- readback object type and notebook language are verified before hash;
- authorization V2 binds manifest + executable publisher package digest + exact ordered object IDs;
- authorization record must live outside repo;
- one-write-attempt is consumed atomically immediately before the first material write, not by read-only preflight;
- target host normalization and corporate-user guard;
- exception after write start becomes UNKNOWN unless a successful effect is already known.

Manifest/object set remains unchanged. No Databricks access occurred.
