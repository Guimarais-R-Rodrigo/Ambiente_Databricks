# Databricks notebook source
"""One-shot owned Delta probe of a verified synthetic Cross PIT feature view."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

MARKER = "SKILLS_FEATURE_MATERIALIZATION_FREE_PROBE_V1"
sys.dont_write_bytecode = True


def widget(name: str) -> str:
    dbutils.widgets.text(name, "", name)
    value = dbutils.widgets.get(name).strip()
    if not value:
        raise ValueError("Required widget absent: " + name)
    return value


def fixture():
    """Pure synthetic inputs; caller can recompute them without a Databricks session."""
    from hub_scripts.skill_execution.domain_context import digest
    facts = [
        {"decision_id": "d1", "entity_id": "a", "decision_at": "2026-01-10T00:00:00.123456Z"},
        {"decision_id": "d2", "entity_id": "b", "decision_at": "2026-01-10T00:00:00.123456Z"},
        {"decision_id": "d3", "entity_id": "c", "decision_at": "2026-01-10T00:00:00.123456Z"},
    ]
    history = [
        {"entity_id": "a", "reference_at": "2026-01-09T00:00:00.123456Z",
         "available_at": "2026-01-10T00:00:00.123456Z", "feature_value": 1000000},
        {"entity_id": "a", "reference_at": "2026-01-10T00:00:00.123456Z",
         "available_at": "2026-01-11T00:00:00.123456Z", "feature_value": 3},
        {"entity_id": "b", "reference_at": "2026-01-01T00:00:00.123456Z",
         "available_at": "2026-01-02T00:00:00.123456Z", "feature_value": 9},
    ]
    datasets = {"facts": facts, "history": history}
    context = {
        "schema_version": "SER05-CONTEXT-1", "profile": "CONTEXT_ONLY_PILOT_V1",
        "synthetic": True,
        "sources": [
            {"id": "facts", "snapshot_id": "synthetic-facts-v1",
             "content_sha256": digest(facts), "grain": "ONE_ROW_PER_ENTITY_DECISION",
             "columns": list(facts[0])},
            {"id": "history", "snapshot_id": "synthetic-history-v1",
             "content_sha256": digest(history), "grain": "FEATURE_HISTORY",
             "columns": list(history[0])},
        ],
        "anchor": "facts", "entity_keys": ["entity_id"],
        "anchor_grain": "ONE_ROW_PER_ENTITY_DECISION", "cardinality": "N:1",
        "decision_at": "2026-01-10T00:00:00.123456Z", "pit": "APPLICABLE",
        "temporal": {"reference_column": "reference_at", "availability_column": "available_at",
                     "lag_kind": "CONSTANT", "lag_days": 1, "boundary": "LE",
                     "timezone": "UTC", "tie_break": "REJECT", "bitemporal": False},
        "null_key_policy": "REJECT", "requested_effect": "NONE",
    }
    return context, datasets, 5


def module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("RUNNER_UNAVAILABLE")
    result = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = result
    spec.loader.exec_module(result)
    return result


def hashes(root: Path, runner) -> dict:
    paths = [root / rel for rel in runner.REQUIRED_RELEASE_PATHS]
    paths += [root / "skills/hub-ml-feature-engineering/release_manifest.json",
              root / "skills/hub-ml-pipeline-builder/release_manifest.json"]
    return {path.relative_to(root).as_posix():
            hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(set(paths))}


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
    context, datasets, window_days = fixture()
    upstream_id, view_id = run_id + "-pit", run_id + "-view"
    view_runner = module(root / "skills/hub-ml-feature-engineering/scripts/run_pit_features.py",
                         "_ser08_free_pit_view")
    runner = module(root / "skills/hub-ml-feature-engineering/scripts/run_pit_materialization.py",
                    "_ser08_free_pit_materialization")
    before = hashes(root, runner)
    prior_timezone = spark.conf.get("spark.sql.session.timeZone")
    view = None
    effect = None
    probe_error = None
    restore_error = None
    try:
        spark.conf.set("spark.sql.session.timeZone", "UTC")
        view = view_runner.compose(context, datasets, spark, window_days=window_days,
                                   upstream_run_id=upstream_id, view_run_id=view_id)
        if view["status"] != "PASS":
            raise RuntimeError("PIT_VIEW_BLOCKED:" + str(view.get("issues")))
        bound = {"expected_context": context, "expected_datasets": datasets,
                 "expected_window_days": window_days,
                 "expected_upstream_run_id": upstream_id, "expected_view_run_id": view_id}
        request = runner.effect_request(view, **bound)
        authorization = {
            "authorized": True, "effect": "SYNTHETIC_FEATURE_MATERIALIZATION_PROBE",
            "target_table": target_table, "request_digest": digest(request),
            "run_id": run_id, "nonce": nonce, "cleanup": "DROP_OWNED",
            "expected_principal": expected_principal,
            "expected_catalog": "workspace", "expected_schema": "default",
        }
        effect = runner.execute(view, spark, authorization, run_id=run_id, **bound)
    except Exception as exc:
        probe_error = type(exc).__name__ + ":" + str(exc)
    finally:
        try:
            spark.conf.set("spark.sql.session.timeZone", prior_timezone)
        except Exception as exc:
            restore_error = type(exc).__name__ + ":" + str(exc)
    after = hashes(root, runner)
    status = effect["status"] if effect is not None else "BLOCKED"
    if status != "UNKNOWN" and (before != after or probe_error or restore_error):
        status = "BLOCKED"
    report = {
        "marker": MARKER, "status": status,
        "effect": effect, "published_package_mutated": before != after,
        "feature_view_sha256": view["feature_view_sha256"] if view and view.get("result") else None,
        "upstream_receipt_id": view["result"]["upstream_receipt_id"] if view and view.get("result") else None,
        "upstream_postflight_id": view["result"]["upstream_postflight_id"] if view and view.get("result") else None,
        "assistant_root": str(root), "target_table": target_table,
        "probe_error": probe_error, "timezone_restoration_error": restore_error,
        "genie_homologation": False, "business_deployment": False,
    }
    output = json.dumps(report, ensure_ascii=False, sort_keys=True, allow_nan=False)
    print(output)
    dbutils.notebook.exit(output)


main()
