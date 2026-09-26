from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools.skill_enforcement.real_campaigns.b1.g6_publication import minimal_publish as base

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "manifest.json"

MANIFEST_SCHEMA = "SER-B1-G6-PROBE-RECOVERY-MANIFEST-1"
AUTH_SCHEMA = "SER-B1-G6-SER05-RESIDUAL-AUTH-1"
EXPECTED_PROFILE = "FREE"
EXPECTED_HOST = "https://dbc-72c8503a-bc27.cloud.databricks.com"
EXPECTED_BASE_HTTP11_PACKAGE_SHA256 = "b4c186b2838bfa04e6d5475d6a7d23561a8957b3fcea9539be612d11e032f0f6"
FUNCTIONAL_PACKAGE_FILES = ("manifest.json", "residual_probe_recovery.py")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _manifest_sha256() -> str:
    return _sha256_bytes(MANIFEST_PATH.read_bytes())


def _recovery_package_sha256() -> str:
    digest = hashlib.sha256()
    for name in FUNCTIONAL_PACKAGE_FILES:
        path = HERE / name
        digest.update(
            name.encode("utf-8")
            + b"\0"
            + _sha256_bytes(path.read_bytes()).encode("ascii")
            + b"\n"
        )
    return digest.hexdigest()


def _source_path(entry: dict) -> Path:
    return ROOT / entry["source_path"]


def _local_normalized_hash(entry: dict) -> str:
    return _sha256_bytes(base._normalize(_source_path(entry).read_bytes(), notebook=True))


def _entries(manifest: dict) -> dict[str, dict]:
    rows = manifest.get("objects")
    if not isinstance(rows, list):
        return {}
    return {
        row.get("object_id"): row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("object_id"), str)
    }


def validate_local() -> dict:
    issues: list[str] = []
    try:
        manifest = _load_json(MANIFEST_PATH)
    except Exception as exc:
        return {
            "schema_version": "SER-B1-G6-PROBE-RECOVERY-LOCAL-1",
            "status": "FAIL",
            "issues": ["MANIFEST_UNREADABLE:" + type(exc).__name__],
            "remote_access_performed": False,
            "remote_write_performed": False,
        }

    if manifest.get("schema_version") != MANIFEST_SCHEMA:
        issues.append("MANIFEST_SCHEMA")
    if manifest.get("execution_status") != "NOT_AUTHORIZED":
        issues.append("MANIFEST_EXECUTION_STATUS")
    if manifest.get("base_http11_publisher_package_sha256") != EXPECTED_BASE_HTTP11_PACKAGE_SHA256:
        issues.append("BASE_HTTP11_DIGEST_DECLARATION")

    target = manifest.get("target") or {}
    if target.get("profile") != EXPECTED_PROFILE or target.get("host") != EXPECTED_HOST:
        issues.append("TARGET_BINDING")

    if manifest.get("remote_root_suffix") != "ser-b1-g6-tests/08c2a93c4c9d":
        issues.append("REMOTE_ROOT_SUFFIX")

    entries = _entries(manifest)
    if set(entries) != {"ser03-free-probe", "ser05-free-probe"}:
        issues.append("OBJECT_SET")
    else:
        ser03 = entries["ser03-free-probe"]
        ser05 = entries["ser05-free-probe"]
        if ser03.get("role") != "REQUIRED_EXACT_EXISTING_READ_ONLY" or ser03.get("write_allowed") is not False:
            issues.append("SER03_ROLE")
        if ser05.get("role") != "RESIDUAL_CREATE_OR_ALREADY_CORRECT" or ser05.get("write_allowed") is not True:
            issues.append("SER05_ROLE")
        for object_id, row in entries.items():
            path = _source_path(row)
            if not path.is_file():
                issues.append("SOURCE_MISSING:" + object_id)
                continue
            if _git_blob_sha1(path.read_bytes()) != row.get("expected_git_blob_sha1"):
                issues.append("SOURCE_GIT_BLOB_MISMATCH:" + object_id)
            if row.get("object_kind") != "NOTEBOOK" or row.get("language") != "PYTHON":
                issues.append("OBJECT_KIND_OR_LANGUAGE:" + object_id)
            if not base.eh_notebook(path):
                issues.append("NOTEBOOK_MARKER_MISSING:" + object_id)

    contract = manifest.get("write_contract") or {}
    expected_contract = {
        "allowed_object_ids": ["ser05-free-probe"],
        "effect": "TEMPORARY_WORKSPACE_OBJECT_CREATE",
        "transport": "PYTHON_HTTP_CLIENT_HTTP11",
        "auth_source": "DATABRICKS_CLI_U2M_TOKEN",
        "endpoint": "POST /api/2.0/workspace/import",
        "format": "SOURCE",
        "language": "PYTHON",
        "overwrite": False,
        "one_write_attempt": True,
        "automatic_retry": False,
        "readback_required": True,
        "mkdir_allowed": False,
        "cleanup_allowed": False,
    }
    if contract != expected_contract:
        issues.append("WRITE_CONTRACT")

    if base._publisher_package_sha256() != EXPECTED_BASE_HTTP11_PACKAGE_SHA256:
        issues.append("BASE_HTTP11_PACKAGE_DRIFT")

    return {
        "schema_version": "SER-B1-G6-PROBE-RECOVERY-LOCAL-1",
        "status": "PASS" if not issues else "FAIL",
        "issues": sorted(set(issues)),
        "manifest_sha256": _manifest_sha256(),
        "recovery_package_sha256": _recovery_package_sha256(),
        "base_http11_publisher_package_sha256": base._publisher_package_sha256(),
        "object_count": len(entries),
        "ser03_local_normalized_sha256": (
            _local_normalized_hash(entries["ser03-free-probe"])
            if "ser03-free-probe" in entries and _source_path(entries["ser03-free-probe"]).is_file()
            else None
        ),
        "ser05_local_normalized_sha256": (
            _local_normalized_hash(entries["ser05-free-probe"])
            if "ser05-free-probe" in entries and _source_path(entries["ser05-free-probe"]).is_file()
            else None
        ),
        "remote_access_performed": False,
        "remote_write_performed": False,
    }


def _remote_root(home: str, manifest: dict) -> str:
    return home.rstrip("/") + "/" + str(manifest["remote_root_suffix"]).strip("/")


def _remote_path(root: str, entry: dict) -> str:
    return root.rstrip("/") + "/" + str(entry["remote_name"]).strip("/")


def _list_exact_root(profile: str, root: str) -> list[dict]:
    payload = base._status_object(profile, root)
    if payload.get("path") != root:
        raise RuntimeError("ROOT_STATUS_PATH_MISMATCH")
    if payload.get("object_type") != "DIRECTORY":
        raise RuntimeError("ROOT_NOT_DIRECTORY")
    rc, out, err = base._run_dbx(profile, "workspace", "list", root, "-o", "json")
    if rc != 0:
        raise RuntimeError("ROOT_LIST_FAILED:" + (err.strip() or out.strip())[:120])
    rows = base._parse_workspace_listing(out)
    return rows


def _remote_notebook_hash(profile: str, path: str) -> str:
    return base._remote_normalized_hash(profile, path, {"object_kind": "NOTEBOOK"})


def _reconcile_remote() -> dict:
    manifest = _load_json(MANIFEST_PATH)
    entries = _entries(manifest)
    home, target = base._resolve_target(EXPECTED_PROFILE, EXPECTED_HOST)
    root = _remote_root(home, manifest)
    rows = _list_exact_root(EXPECTED_PROFILE, root)
    observed = {
        str(row.get("path")): row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }

    ser03 = entries["ser03-free-probe"]
    ser05 = entries["ser05-free-probe"]
    ser03_remote = _remote_path(root, ser03)
    ser05_remote = _remote_path(root, ser05)
    expected_paths = {ser03_remote, ser05_remote}
    unexpected = sorted(set(observed) - expected_paths)
    if unexpected:
        raise RuntimeError("UNEXPECTED_ROOT_OBJECT:" + ",".join(unexpected))

    if ser03_remote not in observed:
        raise RuntimeError("SER03_REQUIRED_OBJECT_MISSING")
    ser03_hash = _remote_notebook_hash(EXPECTED_PROFILE, ser03_remote)
    ser03_local = _local_normalized_hash(ser03)
    if ser03_hash != ser03_local:
        raise RuntimeError("SER03_REQUIRED_OBJECT_DIVERGENT")

    if ser05_remote not in observed:
        ser05_state = "ABSENT"
        ser05_action = "CREATE"
        ser05_hash = None
    else:
        ser05_hash = _remote_notebook_hash(EXPECTED_PROFILE, ser05_remote)
        ser05_local = _local_normalized_hash(ser05)
        if ser05_hash != ser05_local:
            raise RuntimeError("SER05_EXISTING_OBJECT_DIVERGENT")
        ser05_state = "EXACT"
        ser05_action = "ALREADY_CORRECT"

    return {
        "status": "PASS",
        "target": target,
        "remote_root": root,
        "root_object_count": len(observed),
        "ser03": {
            "state": "EXACT",
            "remote_path": ser03_remote,
            "remote_normalized_sha256": ser03_hash,
            "local_normalized_sha256": ser03_local,
        },
        "ser05": {
            "state": ser05_state,
            "action": ser05_action,
            "remote_path": ser05_remote,
            "remote_normalized_sha256": ser05_hash,
            "local_normalized_sha256": _local_normalized_hash(ser05),
        },
        "remote_write_performed": False,
    }


def reconcile() -> dict:
    local = validate_local()
    if local["status"] != "PASS":
        return {
            "schema_version": "SER-B1-G6-PROBE-RECOVERY-RECONCILE-1",
            "status": "FAIL",
            "phase": "LOCAL_VALIDATION",
            "issues": local["issues"],
            "remote_write_performed": False,
        }
    try:
        remote = _reconcile_remote()
    except Exception as exc:
        return {
            "schema_version": "SER-B1-G6-PROBE-RECOVERY-RECONCILE-1",
            "status": "FAIL",
            "phase": "REMOTE_RECONCILIATION",
            "first_failure": str(exc),
            "manifest_sha256": local["manifest_sha256"],
            "recovery_package_sha256": local["recovery_package_sha256"],
            "remote_write_performed": False,
        }
    return {
        "schema_version": "SER-B1-G6-PROBE-RECOVERY-RECONCILE-1",
        "status": "PASS",
        "manifest_sha256": local["manifest_sha256"],
        "recovery_package_sha256": local["recovery_package_sha256"],
        **remote,
    }


def _assert_external_file(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if resolved == ROOT or ROOT in resolved.parents or resolved in ROOT.parents:
        raise RuntimeError(label + "_MUST_BE_EXTERNAL")
    if path.is_symlink():
        raise RuntimeError(label + "_SYMLINK_FORBIDDEN")
    if not resolved.is_file():
        raise RuntimeError(label + "_NOT_FILE")
    return resolved


def _authorization_marker(path: Path) -> Path:
    return path.with_name(path.name + ".consumed")


def _validate_authorization(
    path: Path,
    *,
    manifest_sha256: str,
    recovery_package_sha256: str,
    ser05_source_blob: str,
) -> dict:
    resolved = _assert_external_file(path, "AUTHORIZATION")
    if _authorization_marker(resolved).exists():
        raise RuntimeError("AUTHORIZATION_ALREADY_CONSUMED")
    payload = _load_json(resolved)
    issues = []
    if payload.get("schema_version") != AUTH_SCHEMA:
        issues.append("AUTH_SCHEMA")
    if payload.get("decision") != "AUTHORIZED":
        issues.append("AUTH_DECISION")
    if payload.get("action") != "G6_SER05_RESIDUAL_DIRECT_HTTP11_CREATE":
        issues.append("AUTH_ACTION")
    if payload.get("effect") != "TEMPORARY_WORKSPACE_OBJECT_CREATE":
        issues.append("AUTH_EFFECT")
    if payload.get("one_write_attempt") is not True:
        issues.append("AUTH_ONE_WRITE_ATTEMPT")
    if payload.get("manifest_sha256") != manifest_sha256:
        issues.append("AUTH_MANIFEST_BINDING")
    if payload.get("recovery_package_sha256") != recovery_package_sha256:
        issues.append("AUTH_RECOVERY_PACKAGE_BINDING")
    if payload.get("base_http11_publisher_package_sha256") != EXPECTED_BASE_HTTP11_PACKAGE_SHA256:
        issues.append("AUTH_BASE_HTTP11_BINDING")
    if payload.get("ser05_source_git_blob_sha1") != ser05_source_blob:
        issues.append("AUTH_SER05_SOURCE_BINDING")
    if payload.get("allowed_object_ids") != ["ser05-free-probe"]:
        issues.append("AUTH_OBJECT_SET")
    if payload.get("remote_root_suffix") != "ser-b1-g6-tests/08c2a93c4c9d":
        issues.append("AUTH_REMOTE_ROOT")
    target = payload.get("target") or {}
    if target.get("profile") != EXPECTED_PROFILE or target.get("host") != EXPECTED_HOST:
        issues.append("AUTH_TARGET")
    if not isinstance(payload.get("authorization_ref"), str) or not payload["authorization_ref"].strip():
        issues.append("AUTH_REF")
    if issues:
        raise RuntimeError("AUTHORIZATION_INVALID:" + ",".join(issues))
    return payload


def _consume_authorization(
    path: Path,
    payload: dict,
    *,
    recovery_package_sha256: str,
) -> str:
    resolved = _assert_external_file(path, "AUTHORIZATION")
    marker = _authorization_marker(resolved)
    record = {
        "schema_version": "SER-B1-G6-SER05-RESIDUAL-AUTH-CONSUMPTION-1",
        "authorization_ref": payload["authorization_ref"],
        "action": payload["action"],
        "effect": payload["effect"],
        "recovery_package_sha256": recovery_package_sha256,
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
        return {
            "schema_version": "SER-B1-G6-SER05-RESIDUAL-RUN-1",
            "status": "FAIL",
            "phase": "LOCAL_VALIDATION",
            "issues": local["issues"],
        }

    manifest = _load_json(MANIFEST_PATH)
    entries = _entries(manifest)
    ser05 = entries["ser05-free-probe"]
    try:
        auth = _validate_authorization(
            authorization_record,
            manifest_sha256=local["manifest_sha256"],
            recovery_package_sha256=local["recovery_package_sha256"],
            ser05_source_blob=ser05["expected_git_blob_sha1"],
        )
        evidence = _evidence_dir(evidence_dir)
    except Exception as exc:
        return {
            "schema_version": "SER-B1-G6-SER05-RESIDUAL-RUN-1",
            "status": "FAIL",
            "phase": "AUTH_OR_EVIDENCE_PRECHECK",
            "first_failure": str(exc),
            "authorization_consumed": False,
            "write_started": False,
        }

    result = {
        "schema_version": "SER-B1-G6-SER05-RESIDUAL-RUN-1",
        "status": "RUNNING",
        "manifest_sha256": local["manifest_sha256"],
        "recovery_package_sha256": local["recovery_package_sha256"],
        "base_http11_publisher_package_sha256": local["base_http11_publisher_package_sha256"],
        "authorization_ref": auth["authorization_ref"],
        "authorization_record_sha256": _sha256_bytes(authorization_record.resolve().read_bytes()),
        "authorization_consumed": False,
        "write_started": False,
        "write_exit_code": None,
        "effect_status": "NONE",
        "verification": "NOT_RUN",
        "first_failure": None,
    }
    _write_json(evidence / "RUN_STATE.json", result)

    try:
        first = _reconcile_remote()
        result["preflight"] = first
        _write_json(evidence / "RUN_STATE.json", result)
    except Exception as exc:
        result["status"] = "FAIL"
        result["first_failure"] = "REMOTE_PRECONDITION:" + str(exc)
        _write_json(evidence / "RUN_STATE.json", result)
        return result

    if first["ser05"]["action"] == "ALREADY_CORRECT":
        result["status"] = "PASS"
        result["effect_status"] = "ALREADY_CORRECT"
        result["verification"] = "PASS"
        result["final"] = first
        _write_json(evidence / "RUN_STATE.json", result)
        return result

    try:
        access_token = base._acquire_u2m_access_token(EXPECTED_PROFILE)
    except Exception as exc:
        result["status"] = "FAIL"
        result["first_failure"] = "AUTH_TOKEN:" + str(exc)
        _write_json(evidence / "RUN_STATE.json", result)
        return result

    try:
        current = _reconcile_remote()
        result["prewrite_reconciliation"] = current
        if current["ser05"]["action"] != "CREATE":
            raise RuntimeError("SER05_PREWRITE_ACTION_CHANGED:" + current["ser05"]["action"])
        result["authorization_consumption_sha256"] = _consume_authorization(
            authorization_record,
            auth,
            recovery_package_sha256=local["recovery_package_sha256"],
        )
        result["authorization_consumed"] = True
        _write_json(evidence / "RUN_STATE.json", result)

        result["write_started"] = True
        rc, out, err = base._run_direct_http_import(
            EXPECTED_HOST,
            access_token,
            current["ser05"]["remote_path"],
            _source_path(ser05),
            {"object_kind": "NOTEBOOK"},
            "CREATE",
        )
        result["write_exit_code"] = rc
        if rc != 0:
            result["effect_status"] = "UNKNOWN"
            raise RuntimeError("IMPORT_FAILED:" + (err.strip() or out.strip())[:120])

        remote_hash = _remote_notebook_hash(
            EXPECTED_PROFILE, current["ser05"]["remote_path"]
        )
        local_hash = _local_normalized_hash(ser05)
        result["remote_normalized_sha256"] = remote_hash
        result["local_normalized_sha256"] = local_hash
        if remote_hash != local_hash:
            result["effect_status"] = "UNKNOWN"
            result["verification"] = "FAIL"
            raise RuntimeError("READBACK_HASH_MISMATCH")

        result["effect_status"] = "CREATED"
        result["verification"] = "PASS"
        result["status"] = "PASS"
        result["final"] = _reconcile_remote()
    except Exception as exc:
        if result["write_started"] and result["effect_status"] == "NONE":
            result["effect_status"] = "UNKNOWN"
        result["status"] = "FAIL"
        result["first_failure"] = str(exc)
        _write_json(evidence / "RUN_STATE.json", result)
        return result

    _write_json(evidence / "RUN_STATE.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only reconcile and residual SER05 probe recovery for SER B1 G6"
    )
    parser.add_argument("--validate-local", action="store_true")
    parser.add_argument("--reconcile", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--authorization-record", type=Path)
    parser.add_argument("--evidence-dir", type=Path)
    args = parser.parse_args()

    if sum(bool(x) for x in (args.validate_local, args.reconcile, args.execute)) != 1:
        parser.error("choose exactly one of --validate-local, --reconcile or --execute")

    if args.validate_local:
        result = validate_local()
    elif args.reconcile:
        result = reconcile()
    else:
        if args.authorization_record is None or args.evidence_dir is None:
            parser.error("--execute requires --authorization-record and --evidence-dir")
        result = execute(args.authorization_record, args.evidence_dir)

    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
