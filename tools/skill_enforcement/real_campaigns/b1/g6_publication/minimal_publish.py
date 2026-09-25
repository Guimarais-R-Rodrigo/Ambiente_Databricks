from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from tools.notebook_marker import eh_notebook
from tools.project_policy import CORPORATE_RE, normalize_host

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "manifest.json"
EXPECTED_PROFILE = "FREE"
EXPECTED_HOST = "https://dbc-72c8503a-bc27.cloud.databricks.com"
AUTH_SCHEMA = "SER-B1-G6-MINIMAL-PUBLISH-AUTH-2"
FUNCTIONAL_PACKAGE_FILES = ("manifest.json", "minimal_publish.py")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _manifest_sha256() -> str:
    return _sha256_bytes(MANIFEST_PATH.read_bytes())


def _publisher_package_sha256() -> str:
    digest = hashlib.sha256()
    for name in FUNCTIONAL_PACKAGE_FILES:
        path = HERE / name
        data = path.read_bytes()
        digest.update(name.encode("utf-8") + b"\0" + _sha256_bytes(data).encode("ascii") + b"\n")
    return digest.hexdigest()


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _normalize(data: bytes, *, notebook: bool) -> bytes:
    out = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if notebook:
        out = out.rstrip(b"\n") + b"\n"
    return out


def _rendered_path(entry: dict) -> Path:
    return ROOT / entry["rendered_path"]


def _source_path(entry: dict) -> Path:
    return ROOT / entry["source_path"]


def validate_local() -> dict:
    issues: list[str] = []
    try:
        manifest = _load_json(MANIFEST_PATH)
    except Exception as exc:
        return {"status": "FAIL", "issues": ["MANIFEST_UNREADABLE:" + type(exc).__name__]}

    if manifest.get("schema_version") != "SER-B1-G6-MINIMAL-PUBLISH-MANIFEST-1":
        issues.append("MANIFEST_SCHEMA")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        entries = []
        issues.append("ENTRIES_NOT_LIST")
    if len(entries) != 17 or manifest.get("expected_object_count") != 17:
        issues.append("OBJECT_COUNT")
    ids = [e.get("object_id") for e in entries if isinstance(e, dict)]
    if len(ids) != len(set(ids)):
        issues.append("DUPLICATE_OBJECT_ID")
    remotes = [e.get("remote_relative_path") for e in entries if isinstance(e, dict)]
    if len(remotes) != len(set(remotes)):
        issues.append("DUPLICATE_REMOTE_PATH")

    missing = 0
    overwrite = 0
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            issues.append("ENTRY_NOT_OBJECT:" + str(index))
            continue
        if entry.get("order") != index:
            issues.append("ORDER:" + str(entry.get("object_id")))
        if entry.get("object_kind") not in {"FILE", "NOTEBOOK"}:
            issues.append("OBJECT_KIND:" + str(entry.get("object_id")))
            continue
        source = _source_path(entry)
        rendered = _rendered_path(entry)
        if not source.is_file() or not rendered.is_file():
            issues.append("LOCAL_PATH_MISSING:" + str(entry.get("object_id")))
            continue
        source_bytes = source.read_bytes()
        rendered_bytes = rendered.read_bytes()
        if source_bytes != rendered_bytes:
            issues.append("SOURCE_RENDERED_DRIFT:" + str(entry.get("object_id")))
        expected_blob = entry.get("expected_git_blob_sha1")
        if _git_blob_sha1(rendered_bytes) != expected_blob:
            issues.append("GIT_BLOB_MISMATCH:" + str(entry.get("object_id")))

        is_nb = eh_notebook(rendered)
        if entry.get("object_kind") == "NOTEBOOK" and not is_nb:
            issues.append("NOTEBOOK_MARKER_MISSING:" + str(entry.get("object_id")))
        if entry.get("object_kind") == "FILE" and is_nb:
            issues.append("FILE_MARKED_AS_NOTEBOOK:" + str(entry.get("object_id")))
        if entry.get("object_kind") == "NOTEBOOK":
            if not str(entry.get("rendered_path", "")).endswith(".py"):
                issues.append("NOTEBOOK_LOCAL_EXTENSION:" + str(entry.get("object_id")))
            if str(entry.get("remote_relative_path", "")).endswith(".py"):
                issues.append("NOTEBOOK_REMOTE_EXTENSION:" + str(entry.get("object_id")))

        pre = entry.get("precondition") or {}
        if pre.get("kind") == "MISSING":
            missing += 1
        elif pre.get("kind") == "REMOTE_NORMALIZED_SHA256_EQUALS":
            overwrite += 1
            expected_local = entry.get("expected_local_normalized_sha256")
            actual_local = _sha256_bytes(_normalize(rendered_bytes, notebook=is_nb))
            if actual_local != expected_local:
                issues.append("LOCAL_NORMALIZED_SHA256:" + str(entry.get("object_id")))
            if not isinstance(pre.get("sha256"), str) or len(pre["sha256"]) != 64:
                issues.append("REMOTE_PRECONDITION_SHA256:" + str(entry.get("object_id")))
        else:
            issues.append("PRECONDITION_KIND:" + str(entry.get("object_id")))

    if missing != 16 or overwrite != 1:
        issues.append("PRECONDITION_COUNTS")
    if manifest.get("full_republish") is not False:
        issues.append("FULL_REPUBLISH_NOT_FALSE")
    if manifest.get("effect") != "REMOTE_PACKAGE_WRITE":
        issues.append("EFFECT")
    if manifest.get("execution_status") != "NOT_AUTHORIZED":
        issues.append("EMBEDDED_EXECUTION_STATUS")
    if (manifest.get("authorization") or {}).get("external_record_required") is not True:
        issues.append("EXTERNAL_AUTH_RECORD_REQUIRED")

    return {
        "schema_version": "SER-B1-G6-MINIMAL-PUBLISH-LOCAL-VALIDATION-1",
        "status": "PASS" if not issues else "FAIL",
        "issues": sorted(set(issues)),
        "manifest_sha256": _manifest_sha256(),
        "publisher_package_sha256": _publisher_package_sha256(),
        "object_count": len(entries),
        "missing_count": missing,
        "overwrite_count": overwrite,
        "remote_access_performed": False,
        "remote_write_performed": False,
    }


def _run_dbx(profile: str, *args: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["databricks", "--profile", profile, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def _configuration_value(payload: Any, key: str) -> str | None:
    if not isinstance(payload, dict):
        return None
    details = payload.get("details")
    configuration = details.get("configuration") if isinstance(details, dict) else None
    item = configuration.get(key) if isinstance(configuration, dict) else None
    value = item.get("value") if isinstance(item, dict) else None
    return str(value) if value is not None else None


def _resolve_target(profile: str, expected_host: str) -> tuple[str, dict]:
    rc, out, err = _run_dbx(profile, "auth", "describe", "-o", "json")
    if rc != 0:
        raise RuntimeError("AUTH_DESCRIBE_FAILED:" + (err.strip() or out.strip())[:120])
    auth = json.loads(out)
    if isinstance(auth, dict) and str(auth.get("status", "")).lower() == "error":
        raise RuntimeError("AUTH_DESCRIBE_STATUS_ERROR")
    observed_profile = _configuration_value(auth, "profile") or profile
    observed_host = _configuration_value(auth, "host")
    if observed_profile != profile:
        raise RuntimeError("PROFILE_MISMATCH")
    try:
        normalized_observed = normalize_host(str(observed_host))
        normalized_expected = normalize_host(expected_host)
    except ValueError as exc:
        raise RuntimeError("HOST_INVALID") from exc
    if normalized_observed != normalized_expected:
        raise RuntimeError("HOST_MISMATCH")
    rc, out, err = _run_dbx(profile, "current-user", "me", "-o", "json")
    if rc != 0:
        raise RuntimeError("CURRENT_USER_FAILED:" + (err.strip() or out.strip())[:120])
    user = json.loads(out)
    username = user.get("userName") if isinstance(user, dict) else None
    if not isinstance(username, str) or not username.strip():
        raise RuntimeError("CURRENT_USER_UNRESOLVED")
    if CORPORATE_RE.search(username):
        raise RuntimeError("CURRENT_USER_LOOKS_CORPORATE")
    return f"/Users/{username}", {"profile": profile, "host": normalized_expected, "current_user_resolved": True}


def _remote_path(home: str, entry: dict) -> str:
    return home.rstrip("/") + "/" + str(entry["remote_relative_path"]).lstrip("/")


def _export(profile: str, remote_path: str, kind: str) -> bytes:
    fmt = "SOURCE" if kind == "NOTEBOOK" else "RAW"
    rc, out, err = _run_dbx(profile, "workspace", "export", remote_path, "--format", fmt, "-o", "json")
    if rc != 0:
        raise RuntimeError("EXPORT_FAILED:" + (err.strip() or out.strip())[:120])
    payload = json.loads(out)
    content = payload.get("content") if isinstance(payload, dict) else None
    if not isinstance(content, str):
        raise RuntimeError("EXPORT_CONTENT_MISSING")
    return base64.b64decode(content, validate=True)


def _status(profile: str, remote_path: str) -> tuple[int, str, str]:
    return _run_dbx(profile, "workspace", "get-status", remote_path, "-o", "json")


def _parse_workspace_listing(text: str) -> list[dict]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("WORKSPACE_LIST_INVALID_JSON") from exc
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict) and isinstance(payload.get("objects"), list):
        rows = payload["objects"]
    elif payload == {}:
        rows = []
    else:
        raise RuntimeError("WORKSPACE_LIST_UNSUPPORTED_SHAPE")
    if any(not isinstance(row, dict) for row in rows):
        raise RuntimeError("WORKSPACE_LIST_ROW_NOT_OBJECT")
    return rows


def _parent_path(remote_path: str) -> str:
    value = remote_path.rstrip("/")
    if "/" not in value:
        raise RuntimeError("PARENT_UNRESOLVED")
    parent = value.rsplit("/", 1)[0]
    if not parent or parent == value:
        raise RuntimeError("PARENT_UNRESOLVED")
    return parent


def _status_object(profile: str, remote_path: str) -> dict:
    rc, out, err = _status(profile, remote_path)
    if rc != 0:
        raise RuntimeError("GET_STATUS_FAILED:" + (err.strip() or out.strip())[:120])
    try:
        payload = json.loads(out)
    except json.JSONDecodeError as exc:
        raise RuntimeError("GET_STATUS_INVALID_JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("GET_STATUS_NOT_OBJECT")
    return payload


def _assert_parent_directory_exists(profile: str, remote_path: str) -> None:
    parent = _parent_path(remote_path)
    payload = _status_object(profile, parent)
    if payload.get("path") != parent:
        raise RuntimeError("PARENT_STATUS_PATH_MISMATCH")
    if payload.get("object_type") != "DIRECTORY":
        raise RuntimeError("PARENT_NOT_DIRECTORY")


def _prove_absent_via_ancestor(profile: str, remote_path: str, seen: set[str] | None = None) -> None:
    seen = set() if seen is None else seen
    if remote_path in seen:
        raise RuntimeError("MISSING_PROOF_CYCLE")
    seen.add(remote_path)
    parent = _parent_path(remote_path)

    list_rc, list_out, list_err = _run_dbx(profile, "workspace", "list", parent, "-o", "json")
    if list_rc == 0:
        rows = _parse_workspace_listing(list_out)
        observed = {
            str(item.get("path"))
            for item in rows
            if isinstance(item.get("path"), str)
        }
        if remote_path in observed:
            raise RuntimeError("EXPECTED_MISSING_BUT_LISTED")
        return

    parent_rc, _parent_out, _parent_err = _status(profile, parent)
    if parent_rc == 0:
        raise RuntimeError(
            "MISSING_PARENT_LIST_FAILED:" + (list_err.strip() or list_out.strip())[:120]
        )
    if parent in {"/", "/Users"}:
        raise RuntimeError("MISSING_ANCESTOR_NOT_PROVEN")
    _prove_absent_via_ancestor(profile, parent, seen)


def _assert_missing(profile: str, remote_path: str) -> None:
    rc, _out, _err = _status(profile, remote_path)
    if rc == 0:
        raise RuntimeError("EXPECTED_MISSING_BUT_EXISTS")
    _prove_absent_via_ancestor(profile, remote_path)


def _assert_remote_object_type(profile: str, remote_path: str, kind: str) -> None:
    payload = _status_object(profile, remote_path)
    expected = "NOTEBOOK" if kind == "NOTEBOOK" else "FILE"
    if payload.get("path") != remote_path:
        raise RuntimeError("READBACK_STATUS_PATH_MISMATCH")
    if payload.get("object_type") != expected:
        raise RuntimeError("READBACK_OBJECT_TYPE_MISMATCH")
    if kind == "NOTEBOOK" and payload.get("language") != "PYTHON":
        raise RuntimeError("READBACK_NOTEBOOK_LANGUAGE_MISMATCH")


def _assert_stale_hash(profile: str, remote_path: str, entry: dict) -> str:
    remote = _export(profile, remote_path, entry["object_kind"])
    actual = _sha256_bytes(_normalize(remote, notebook=entry["object_kind"] == "NOTEBOOK"))
    expected = entry["precondition"]["sha256"]
    if actual != expected:
        raise RuntimeError("REMOTE_STALE_HASH_PRECONDITION_MISMATCH")
    return actual


def build_import_argv(profile: str, remote_path: str, local_path: Path, entry: dict) -> list[str]:
    argv = ["databricks", "--profile", profile, "workspace", "import", remote_path, "--file", str(local_path)]
    if entry["object_kind"] == "NOTEBOOK":
        argv += ["--format", "SOURCE", "--language", "PYTHON"]
    else:
        argv += ["--format", "RAW"]
    if entry["precondition"]["kind"] == "REMOTE_NORMALIZED_SHA256_EQUALS":
        argv.append("--overwrite")
    return argv


def _run_import(argv: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8")
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def _assert_external_file(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if resolved == ROOT or ROOT in resolved.parents or resolved in ROOT.parents:
        raise RuntimeError(label + "_MUST_BE_EXTERNAL")
    if path.is_symlink():
        raise RuntimeError(label + "_SYMLINK_FORBIDDEN")
    if not resolved.is_file():
        raise RuntimeError(label + "_NOT_FILE")
    return resolved


def _validate_authorization(
    path: Path,
    manifest_sha256: str,
    publisher_package_sha256: str,
    object_ids: list[str],
) -> dict:
    resolved = _assert_external_file(path, "AUTHORIZATION")
    payload = _load_json(resolved)
    issues = []
    if payload.get("schema_version") != AUTH_SCHEMA:
        issues.append("AUTH_SCHEMA")
    if payload.get("decision") != "AUTHORIZED":
        issues.append("AUTH_DECISION")
    if payload.get("manifest_sha256") != manifest_sha256:
        issues.append("AUTH_MANIFEST_BINDING")
    if payload.get("publisher_package_sha256") != publisher_package_sha256:
        issues.append("AUTH_PUBLISHER_PACKAGE_BINDING")
    if payload.get("effect") != "REMOTE_PACKAGE_WRITE":
        issues.append("AUTH_EFFECT")
    target = payload.get("target") or {}
    try:
        target_host = normalize_host(str(target.get("host", "")))
    except ValueError:
        target_host = None
    if target.get("profile") != EXPECTED_PROFILE or target_host != normalize_host(EXPECTED_HOST):
        issues.append("AUTH_TARGET")
    if payload.get("allowed_object_ids") != object_ids:
        issues.append("AUTH_OBJECT_SEQUENCE")
    if payload.get("one_write_attempt") is not True:
        issues.append("AUTH_ONE_WRITE_ATTEMPT")
    if not isinstance(payload.get("authorization_ref"), str) or not payload["authorization_ref"].strip():
        issues.append("AUTH_REF")
    if issues:
        raise RuntimeError("AUTHORIZATION_INVALID:" + ",".join(issues))
    return payload


def _authorization_marker_path(path: Path) -> Path:
    return path.with_name(path.name + ".consumed")


def _consume_write_authorization(path: Path, payload: dict, package_sha256: str) -> str:
    resolved = _assert_external_file(path, "AUTHORIZATION")
    marker = _authorization_marker_path(resolved)
    record = {
        "schema_version": "SER-B1-G6-MINIMAL-PUBLISH-AUTH-CONSUMPTION-1",
        "authorization_ref": payload["authorization_ref"],
        "manifest_sha256": payload["manifest_sha256"],
        "publisher_package_sha256": package_sha256,
        "effect": payload["effect"],
        "consumed": True,
    }
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        fd = os.open(str(marker), flags, 0o600)
    except FileExistsError as exc:
        raise RuntimeError("AUTHORIZATION_ALREADY_CONSUMED") from exc
    with os.fdopen(fd, "wb") as handle:
        handle.write(_json_bytes(record))
    return _sha256_bytes(marker.read_bytes())


def _evidence_dir(path: Path) -> Path:
    resolved = path.resolve()
    if resolved == ROOT or ROOT in resolved.parents or resolved in ROOT.parents:
        raise RuntimeError("EVIDENCE_MUST_BE_EXTERNAL")
    if resolved.exists():
        raise RuntimeError("EVIDENCE_DIR_ALREADY_EXISTS")
    resolved.mkdir(parents=True, exist_ok=False)
    return resolved


def _write_json(path: Path, value: Any) -> None:
    path.write_bytes(_json_bytes(value))


def execute(authorization_record: Path, evidence_dir: Path) -> dict:
    local = validate_local()
    if local["status"] != "PASS":
        return {"status": "FAIL", "phase": "LOCAL_VALIDATION", "issues": local["issues"]}

    manifest = _load_json(MANIFEST_PATH)
    entries = manifest["entries"]
    auth = _validate_authorization(
        authorization_record,
        local["manifest_sha256"],
        local["publisher_package_sha256"],
        [e["object_id"] for e in entries],
    )
    evidence = _evidence_dir(evidence_dir)
    result = {
        "schema_version": "SER-B1-G6-MINIMAL-PUBLISH-RUN-1",
        "status": "RUNNING",
        "manifest_sha256": local["manifest_sha256"],
        "publisher_package_sha256": local["publisher_package_sha256"],
        "authorization_ref": auth["authorization_ref"],
        "authorization_record_sha256": _sha256_bytes(authorization_record.resolve().read_bytes()),
        "authorization_consumed": False,
        "effect": "REMOTE_PACKAGE_WRITE",
        "first_failure": None,
        "records": [],
        "post_write_full_content_verify_required": True,
    }
    _write_json(evidence / "RUN_STATE.json", result)

    try:
        home, target = _resolve_target(EXPECTED_PROFILE, EXPECTED_HOST)
        result["target"] = target
    except Exception as exc:
        result["status"] = "FAIL"
        result["first_failure"] = "TARGET_PRECHECK:" + str(exc)
        _write_json(evidence / "RUN_STATE.json", result)
        return result

    # Complete preflight before the first write.
    try:
        for entry in entries:
            remote = _remote_path(home, entry)
            _assert_parent_directory_exists(EXPECTED_PROFILE, remote)
            if entry["precondition"]["kind"] == "MISSING":
                _assert_missing(EXPECTED_PROFILE, remote)
            else:
                _assert_stale_hash(EXPECTED_PROFILE, remote, entry)
        result["preconditions_confirmed"] = {
            "parent_directories": len(entries),
            "missing_targets": sum(e["precondition"]["kind"] == "MISSING" for e in entries),
            "stale_hash_targets": sum(e["precondition"]["kind"] == "REMOTE_NORMALIZED_SHA256_EQUALS" for e in entries),
        }
        _write_json(evidence / "RUN_STATE.json", result)
    except Exception as exc:
        result["status"] = "FAIL"
        result["first_failure"] = "REMOTE_PRECONDITION:" + str(exc)
        _write_json(evidence / "RUN_STATE.json", result)
        return result

    for entry in entries:
        record = {
            "order": entry["order"],
            "object_id": entry["object_id"],
            "remote_relative_path": entry["remote_relative_path"],
            "object_kind": entry["object_kind"],
            "precondition": entry["precondition"]["kind"],
            "write_started": False,
            "write_exit_code": None,
            "verification": "NOT_RUN",
            "effect_status": "NONE",
        }
        result["records"].append(record)
        _write_json(evidence / "RUN_STATE.json", result)
        remote = _remote_path(home, entry)
        local_path = _rendered_path(entry)
        try:
            # Recheck immediately before each write to close the preflight/write window.
            _assert_parent_directory_exists(EXPECTED_PROFILE, remote)
            if entry["precondition"]["kind"] == "MISSING":
                _assert_missing(EXPECTED_PROFILE, remote)
            else:
                _assert_stale_hash(EXPECTED_PROFILE, remote, entry)

            if result["authorization_consumed"] is False:
                result["authorization_consumption_sha256"] = _consume_write_authorization(
                    authorization_record, auth, local["publisher_package_sha256"]
                )
                result["authorization_consumed"] = True
                _write_json(evidence / "RUN_STATE.json", result)

            argv = build_import_argv(EXPECTED_PROFILE, remote, local_path, entry)
            record["write_started"] = True
            rc, out, err = _run_import(argv)
            record["write_exit_code"] = rc
            if rc != 0:
                record["effect_status"] = "UNKNOWN"
                raise RuntimeError("IMPORT_FAILED:" + (err.strip() or out.strip())[:120])
            record["effect_status"] = "CREATED" if entry["precondition"]["kind"] == "MISSING" else "UPDATED"

            _assert_remote_object_type(EXPECTED_PROFILE, remote, entry["object_kind"])
            remote_bytes = _export(EXPECTED_PROFILE, remote, entry["object_kind"])
            local_bytes = local_path.read_bytes()
            remote_hash = _sha256_bytes(_normalize(remote_bytes, notebook=entry["object_kind"] == "NOTEBOOK"))
            local_hash = _sha256_bytes(_normalize(local_bytes, notebook=entry["object_kind"] == "NOTEBOOK"))
            record["remote_normalized_sha256"] = remote_hash
            record["local_normalized_sha256"] = local_hash
            if remote_hash != local_hash:
                record["verification"] = "FAIL"
                raise RuntimeError("READBACK_HASH_MISMATCH")
            record["verification"] = "PASS"
        except Exception as exc:
            if record["write_started"] and record["effect_status"] == "NONE":
                record["effect_status"] = "UNKNOWN"
            result["status"] = "FAIL"
            result["first_failure"] = entry["object_id"] + ":" + str(exc)
            _write_json(evidence / "RUN_STATE.json", result)
            return result
        _write_json(evidence / "RUN_STATE.json", result)

    result["status"] = "PASS"
    _write_json(evidence / "RUN_STATE.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Closed 17-object G6 corrective publisher")
    parser.add_argument("--validate-local", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--authorization-record", type=Path)
    parser.add_argument("--evidence-dir", type=Path)
    args = parser.parse_args()

    if args.validate_local == args.execute:
        parser.error("choose exactly one of --validate-local or --execute")

    if args.validate_local:
        result = validate_local()
    else:
        if args.authorization_record is None or args.evidence_dir is None:
            parser.error("--execute requires --authorization-record and --evidence-dir")
        result = execute(args.authorization_record, args.evidence_dir)

    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
