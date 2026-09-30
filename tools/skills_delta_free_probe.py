# Databricks notebook source
"""One-shot synthetic Delta MERGE proof in the caller's Free workspace."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

MARKER = "SKILLS_DELTA_FREE_PROBE_V1"
sys.dont_write_bytecode = True


def widget(name: str) -> str:
    dbutils.widgets.text(name, "", name)
    value = dbutils.widgets.get(name).strip()
    if not value:
        raise ValueError("Required widget absent: " + name)
    return value


def fixture():
    spec = {
        "schema_version": "SER13-SPEC-1", "synthetic": True,
        "operation": "VALIDATE_SPEC", "environment": "LOCAL_SYNTHETIC",
        "scope": "PERSONAL", "source": "synthetic_source",
        "destination": "synthetic_destination", "write_mode": "MERGE",
        "incremental": "BATCH", "primary_keys": ["id"],
        "columns": ["id", "event_at", "value"], "event_time": "event_at",
        "watermark_seconds": None, "idempotency": "MERGE_ON_KEYS",
        "permissions": "UNKNOWN", "schedule": None,
        "rollback": "NOT_APPLICABLE_NO_EFFECT",
    }
    request = {
        "schema_version": "SER13-LOCAL-RUN-1", "synthetic": True,
        "operation": "RUN_LOCAL_SPARK", "spec": spec,
        "prior_rows": [
            {"id": 1, "event_at": "2026-01-01T00:00:00Z", "value": 10},
            {"id": 2, "event_at": "2026-01-01T00:00:00Z", "value": 30},
        ],
        "batch_rows": [
            {"id": 1, "event_at": "2026-01-02T00:00:00Z", "value": 20},
            {"id": 3, "event_at": "2026-01-01T00:00:00Z", "value": 40},
        ],
    }
    expected = [request["batch_rows"][0], request["prior_rows"][1],
                request["batch_rows"][1]]
    return request, expected


def module(path: Path):
    spec = importlib.util.spec_from_file_location("skills_delta_free_probe_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("DELTA_RUNNER_UNAVAILABLE")
    result = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = result
    spec.loader.exec_module(result)
    return result


def hashes(root: Path, runner) -> dict:
    paths = [root / rel for rel in runner.REQUIRED_RELEASE_PATHS]
    paths.append(root / "skills/hub-ml-pipeline-builder/release_manifest.json")
    return {path.relative_to(root).as_posix():
            hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)}


def main():
    root = Path(widget("assistant_root")).resolve()
    if root.name != ".assistant" or not root.is_dir():
        raise ValueError("assistant_root must be published .assistant")
    target_table = widget("target_table")
    expected_principal = widget("expected_principal")
    run_id = widget("run_id")
    nonce = widget("nonce")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from hub_scripts.skill_execution.domain_context import digest
    request, expected_rows = fixture()
    authorization = {
        "authorized": True,
        "effect": "SYNTHETIC_DELTA_PROBE",
        "target_table": target_table,
        "request_digest": digest(request),
        "run_id": run_id,
        "nonce": nonce,
        "cleanup": "DROP_OWNED",
        "expected_principal": expected_principal,
        "expected_catalog": "workspace",
        "expected_schema": "default",
    }
    runner = module(root / "skills/hub-ml-pipeline-builder/scripts/run_delta.py")
    before = hashes(root, runner)
    effect = runner.execute(request, expected_rows, spark, authorization, run_id=run_id)
    after = hashes(root, runner)
    report = {
        "marker": MARKER,
        "status": "BLOCKED" if before != after else effect["status"],
        "effect": effect,
        "published_package_mutated": before != after,
        "assistant_root": str(root),
        "target_table": target_table,
        "genie_homologation": False,
        "business_deployment": False,
    }
    output = json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False)
    print(output)
    dbutils.notebook.exit(output)


main()
