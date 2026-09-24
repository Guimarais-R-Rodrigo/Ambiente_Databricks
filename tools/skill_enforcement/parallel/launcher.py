from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .contract import RESULT_SCHEMA_VERSION, validate_campaign
from .process import ROOT, fingerprint_paths, run_argv
from .registry import resolve_command
from .scheduler import decide, detect_cycle
from .verifier import verify_campaign_run

def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()

def execute(campaign: dict, evidence_root: Path) -> dict:
    issues = validate_campaign(campaign)
    if issues:
        return {"status": "FAIL", "issues": issues, "results": {}, "verification": None}
    if detect_cycle(campaign["tasks"]):
        return {"status": "FAIL", "issues": ["CAMPAIGN_DAG_CYCLE"], "results": {}, "verification": None}
    evidence_root.mkdir(parents=True, exist_ok=False)
    results: dict[str, dict] = {}
    tasks = {t["task_id"]: t for t in campaign["tasks"]}
    first_failure: str | None = None
    while len(results) < len(tasks):
        states = {k: v["status"] for k, v in results.items()}
        decision = decide(campaign["tasks"], states, limit=campaign["max_parallel"])
        for task_id in decision.blocked_dependency:
            task = tasks[task_id]
            blockers = [d for d in task["depends_on"] if states.get(d) not in {"PASS", "NOT_APPLICABLE"}]
            fp = fingerprint_paths(ROOT, task["protected_paths"])
            results[task_id] = {
                "result_schema": RESULT_SCHEMA_VERSION, "task_id": task_id,
                "candidate_sha": campaign["candidate_sha"], "status": "BLOCKED_DEPENDENCY",
                "effect_state": "NONE", "command_records": [], "first_failure": first_failure,
                "started_at_utc": _utc(), "ended_at_utc": _utc(),
                "protected_fingerprint_before": fp, "protected_fingerprint_after": fp,
                "issues": [], "blocked_by": blockers,
            }
        if not decision.ready:
            if len(results) < len(tasks):
                for task_id in decision.pending:
                    task = tasks[task_id]
                    fp = fingerprint_paths(ROOT, task["protected_paths"])
                    results[task_id] = {
                        "result_schema": RESULT_SCHEMA_VERSION, "task_id": task_id,
                        "candidate_sha": campaign["candidate_sha"], "status": "BLOCKED_RESOURCE",
                        "effect_state": "NONE", "command_records": [], "first_failure": first_failure,
                        "started_at_utc": _utc(), "ended_at_utc": _utc(),
                        "protected_fingerprint_before": fp, "protected_fingerprint_after": fp,
                        "issues": ["NO_PROGRESS"],
                    }
            break
        def run_task(task_id: str) -> tuple[str, dict]:
            task = tasks[task_id]; started = _utc(); task_dir = evidence_root / task_id
            before = fingerprint_paths(ROOT, task["protected_paths"])
            records = []; status = "PASS"; task_issues=[]
            for command_id in task["command_ids"]:
                argv = resolve_command(command_id)
                row = run_argv(argv, task_dir, command_id.replace(":", "_"))
                records.append(row)
                if row["exit_code"] != 0:
                    status = "FAIL"; task_issues.append("COMMAND_FAILED:" + command_id); break
            after = fingerprint_paths(ROOT, task["protected_paths"])
            if before != after:
                status = "FAIL"; task_issues.append("PROTECTED_PATH_MUTATED")
            return task_id, {
                "result_schema": RESULT_SCHEMA_VERSION, "task_id": task_id,
                "candidate_sha": campaign["candidate_sha"], "status": status,
                "effect_state": "NONE", "command_records": records,
                "first_failure": None, "started_at_utc": started, "ended_at_utc": _utc(),
                "protected_fingerprint_before": before, "protected_fingerprint_after": after,
                "issues": task_issues,
            }
        with ThreadPoolExecutor(max_workers=len(decision.ready)) as pool:
            futures = [pool.submit(run_task, task_id) for task_id in decision.ready]
            for future in as_completed(futures):
                task_id, result = future.result()
                if result["status"] == "FAIL" and first_failure is None:
                    first_failure = task_id
                results[task_id] = result
        if first_failure:
            for row in results.values():
                if row["first_failure"] is None:
                    row["first_failure"] = first_failure
    verification = verify_campaign_run(campaign, results)
    summary = {
        "schema_version": "SER-PARALLEL-RUN-1",
        "campaign_id": campaign["campaign_id"],
        "candidate_sha": campaign["candidate_sha"],
        "status": "PASS" if verification["valid"] and all(r["status"] in {"PASS", "BLOCKED_DEPENDENCY", "NOT_APPLICABLE"} for r in results.values()) else "FAIL",
        "first_failure": first_failure,
        "results": results,
        "verification": verification,
    }
    (evidence_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return summary

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--campaign", required=True, type=Path)
    p.add_argument("--evidence-dir", required=True, type=Path)
    a=p.parse_args()
    campaign=json.loads(a.campaign.read_text(encoding="utf-8"))
    summary=execute(campaign,a.evidence_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
