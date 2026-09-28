# G6 minimal publisher R5 — local validation PASS

```text
G6_MINIMAL_PUBLISH_R5_LOCAL_VALIDATION = PASS
R5_FREEZE_SHA = 66f531dacbbd67ac972812a0057c932183c1aba1
R5_FREEZE_TREE = fcfcc03a7d38cdd4e14a821a382b2a88c1781811
MANIFEST_SHA256 = 57574ddbdadfd344776bcb2b37142248b9af95671d5efd818a4dda6bcae6ae9e
PUBLISHER_PACKAGE_SHA256 = 774c4351e48becb4ccdcf13a375aedec635718c3c2c8dd7eb6f447e47e87ce62
METATESTS = 34/34 PASS
ADVERSARIAL_REQUIRED_CASES = 17
REMOTE_ACCESS = NOT_RUN
REMOTE_EXECUTION = NOT_AUTHORIZED
```

Protocol frozen in R5:
- FILE import = RAW;
- FILE export/readback = AUTO only after object_type=FILE proof;
- stale policy hash checks FILE type before export;
- notebook = SOURCE/PYTHON;
- exact 17-object manifest unchanged.

The previously authorized three parent directories already exist and were verified. They must not be recreated.

The R4 write authorization is not reusable because it is bound to the R4 executable package digest. R5 requires a new explicit remote authorization.
