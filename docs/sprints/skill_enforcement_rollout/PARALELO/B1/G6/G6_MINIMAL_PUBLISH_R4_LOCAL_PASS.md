# G6 minimal publisher R4 — adversarial local validation PASS

```text
G6_MINIMAL_PUBLISH_R4_LOCAL_VALIDATION = PASS
R4_FREEZE_SHA = 3ef1f14e728338540a4426f297c90ee2f576ec92
R4_FREEZE_TREE = baecc5498c1a0fef63a7f8dfba21d615ca2b33df
MANIFEST_SHA256 = 57574ddbdadfd344776bcb2b37142248b9af95671d5efd818a4dda6bcae6ae9e
PUBLISHER_PACKAGE_SHA256 = 47f230f2ffef57510d1c92b7d94dac3ded766ccbba81368d4058ef2b78aaf7c9
METATESTS = 33/33 PASS
ADVERSARIAL_REQUIRED_CASES = 15
REMOTE_ACCESS = NOT_RUN
REMOTE_EXECUTION = NOT_AUTHORIZED
```

R3 remains FAIL for explicit coverage gap and was not reexecuted.
R2 remains PASS and was not reexecuted.
R1 remote remains FAIL with zero writes and consumed authorization.

The R4 publisher is the next eligible remote candidate. Any new remote attempt requires a new authorization bound to both the manifest digest and executable publisher package digest.
