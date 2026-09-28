# G6 R6 residual publisher — local validation PASS

```text
G6_MINIMAL_PUBLISH_R6_LOCAL_VALIDATION = PASS
R6_FREEZE_SHA = d583c495baed2ab5f2f96453b69232ec3ad30be7
R6_FREEZE_TREE = 31aedaf256cc6ef1eea5a03412825df313eb747d
MANIFEST_SHA256 = 1115e497852c2290dae0c5f1ec247df0de9f19e92e89385cc3f1659855d2cf9e
PUBLISHER_PACKAGE_SHA256 = a4f838c64d5e4f3ad902a401ab52b642e10c8d22eadde9e19e61bb647d16181f
METATESTS = 35/35 PASS
ADVERSARIAL_REQUIRED_CASES = 18
RESIDUAL_OBJECTS = 16
MISSING = 15
OVERWRITE = 1
REMOTE_EXECUTION = NOT_AUTHORIZED
```

The residual manifest is bound to reconciliation evidence SHA-256
`d255398df799f0262872db4b5b327cb4dc3b9be67178746923a009138f702435`.

`domain-context-readme` is excluded because the canonical read-only reconciliation proved it already correct.

The publisher count model is manifest-declared rather than hardcoded.

A legacy argparse description still says "Closed 17-object G6 corrective publisher". It is non-functional text only and is intentionally left unchanged to preserve the frozen executable package digest.
