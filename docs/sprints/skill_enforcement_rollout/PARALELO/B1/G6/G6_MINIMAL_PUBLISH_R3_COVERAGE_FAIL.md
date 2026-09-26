# G6 minimal publisher R3 — local qualification FAIL on explicit coverage

```text
R3_SHA = a0ac7f66839f7f7e9d73460558208652a9edcf02
R3_TREE = caa114ce7be0d0274151d49b67901891ef67ce8e
validate_local = PASS
publisher_package_sha256 = 47f230f2ffef57510d1c92b7d94dac3ded766ccbba81368d4058ef2b78aaf7c9
metatests = 27/27 PASS
qualification = FAIL
first_failure = ADVERSARIAL_COVERAGE_GAP:WORKSPACE_LIST_INVALID_JSON_NOT_EXPLICITLY_TESTED
remote_access = NOT_RUN
remote_write = NOT_RUN
```

Required explicit cases absent from R3 suite:
- workspace-list invalid JSON;
- workspace-list row not object;
- authorization-record symlink;
- authorization manifest digest drift.

The corresponding guards were implemented; the failure is that the qualification contract required explicit negative regressions. R3 remains FAIL and is not frozen.
