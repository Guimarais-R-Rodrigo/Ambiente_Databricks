# G6 R4 reinvocation — export protocol blocker

```text
PARENT_BOOTSTRAP = PASS
directories_checked = 3
directories_created = 3
extra_created = 0

R4_REINVOCATION = BLOCKED_PRECONDITION
publisher_write_authorization_consumed = false
consumption_marker_present = false
records = 0
writes_started = 0
package_effects = 0
first_failure = REMOTE_PRECONDITION:EXPORT_FAILED
observed_detail = RAW export rejected with directDownload=false
```

No package FILE/NOTEBOOK was written.

The blocker is isolated to FILE export/readback protocol. The R4 code used `RAW` with JSON/base64 output. R5 changes only FILE export to `AUTO` after proving the remote object is a FILE; FILE import remains `RAW`.

The three bootstrap directories now exist and were verified, so directory bootstrap must not be repeated for R5.
