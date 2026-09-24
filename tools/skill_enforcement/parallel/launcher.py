from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .contract import RESULT_SCHEMA_VERSION, digest_json, validate_campaign
from .coverage import inventory
from .process import ROOT, fingerprint_paths, run_argv
from .registry import (
    DEFAULT_REGISTRY,
    RegistryError,
    command_template,
    load_registry,
    resolve_command,
)
from .scheduler import decide, detect_cycle
from .verifier import verify_campaign_run

POLICY = ROOT / "ambiente_fonte/.assistant/hub_padroes/skill_enforcement/policy.json"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=20)
    if p.returncode != 0:
        raise RuntimeError("GIT_FAILED:" + " ".join(args) + ":" + (p.stderr or "").strip())
    return p.stdout.strip()


def _repo_status() -> str:
    return _git("status", "--porcelain=v1", "--untracked-files=all")


def _preconditions(campaign: dict, evidence_root: Path) -> list[str]:
    issues: list[str] = []
    try:
        head = _git("rev-parse", "HEAD")
        status = _repo_status()
        shallow = _git("rev-parse", "--is-shallow-repository")
    except RuntimeError as exc:
        return [str(exc)]
    if head != campaign.get("candidate_sha"):
        issues.append("CANDIDATE_HEAD_MISMATCH")
    if status:
        issues.append("WORKTREE_NOT_CLEAN")
    if shallow != "false":
        issues.append("SHALLOW_REPOSITORY")

    repo = ROOT.resolve()
    target = evidence_root.absolute()
    try:
        parent = target.parent.resolve(strict=True)
    except OSError:
        issues.append("EVIDENCE_PARENT_INVALID")
        parent = None
    if parent is not None and (parent.is_relative_to(repo) or repo.is_relative_to(target)):
        issues.append("EVIDENCE_MUST_BE_EXTERNAL")
    if target.exists():
        issues.append("EVIDENCE_DIRECTORY_MUST_BE_NEW")

    try:
        registry = load_registry(DEFAULT_REGISTRY)
    except (OSError, json.JSONDecodeError, RegistryError) as exc:
        issues.append("COMMAND_REGISTRY_INVALID:" + str(exc))
        registry = None
    if registry is not None:
        if digest_json(registry) != campaign.get("command_registry_digest"):
            issues.append("COMMAND_REGISTRY_DIGEST_MISMATCH")
        for task in campaign.get("tasks") or []:
            for command_id in task.get("command_ids") or []:
                row = registry["commands"].get(command_id)
                if row is None:
                    issues.append(f"COMMAND_UNKNOWN:{task.get('task_id')}:{command_id}")
                    continue
                expected_effect = str(task.get("expected_effect", "")).lower()
                if row.get("effects") != expected_effect:
                    issues.append(f"COMMAND_EFFECT_MISMATCH:{task.get('task_id')}:{command_id}")

    actual_coverage = inventory()
    if actual_coverage.get("status") != "PASS":
        issues.append("COVERAGE_NOT_PASS")
    if digest_json(actual_coverage) != campaign.get("coverage_digest"):
        issues.append("COVERAGE_DIGEST_MISMATCH")
    if hashlib.sha256(POLICY.read_bytes()).hexdigest() != campaign.get("policy_before_digest"):
        issues.append("POLICY_DIGEST_MISMATCH")
    return issues


def _blocked_result(
    task: dict,
    campaign: dict,
    status: str,
    wave: int,
    blockers: list[str],
    first_failure: str | None,
) -> dict:
    fp = fingerprint_paths(ROOT, task["protected_paths"])
    now = _utc()
    return {
        "result_schema": RESULT_SCHEMA_VERSION,
        "task_id": task["task_id"],
        "candidate_sha": campaign["candidate_sha"],
        "status": status,
        "effect_state": "NONE",
        "command_records": [],
        "first_failure": first_failure,
        "wave_index": wave,
        "started_at_utc": now,
        "ended_at_utc": now,
        "protected_fingerprint_before": fp,
        "protected_fingerprint_after": fp,
        "issues": [],
        "blocked_by": blockers,
    }


def execute(campaign: dict, evidence_root: Path) -> dict:
    issues = validate_campaign(campaign)
    if issues:
        return {"status": "FAIL", "issues": issues, "results": {}, "verification": None}
    if detect_cycle(campaign["tasks"]):
        return {"status": "FAIL", "issues": ["CAMPAIGN_DAG_CYCLE"], "results": {}, "verification": None}
    pre = _preconditions(campaign, evidence_root)
    if pre:
        return {"status": "FAIL", "issues": pre, "results": {}, "verification": None}

    evidence_root.mkdir(parents=True, exist_ok=False)
    results: dict[str, dict] = {}
    tasks = {t["task_id"]: t for t in campaign["tasks"]}
    first_failure: str | None = None
    global_stop: str | None = None
    wave = 0
    initial_status = _repo_status()

    while len(results) < len(tasks):
        if global_stop is not None:
            for task_id in sorted(set(tasks) - set(results)):
                results[task_id] = _blocked_result(
                    tasks[task_id],
                    campaign,
                    "BLOCKED_GLOBAL_STOP",
                    wave,
                    [global_stop],
                    first_failure,
                )
            break

        states = {k: v["status"] for k, v in results.items()}
        decision = decide(
            campaign["tasks"],
            states,
            limit=campaign["max_parallel"],
            auditor_limit=campaign["max_auditors"],
            resource_limits=campaign.get("resource_limits"),
        )
        for task_id in decision.blocked_dependency:
            task = tasks[task_id]
            blockers = [
                d
                for d in task["depends_on"]
                if states.get(d) not in {"PASS", "NOT_APPLICABLE"}
            ]
            results[task_id] = _blocked_result(
                task,
                campaign,
                "BLOCKED_DEPENDENCY",
                wave,
                blockers,
                first_failure,
            )
        if not decision.ready and decision.blocked_dependency:
            wave += 1
            continue
        if not decision.ready:
            for task_id in decision.pending:
                results[task_id] = _blocked_result(
                    tasks[task_id], campaign, "BLOCKED_RESOURCE", wave, [], first_failure
                )
                results[task_id]["issues"] = ["NO_PROGRESS"]
            break

        def run_task(task_id: str) -> tuple[str, dict]:
            task = tasks[task_id]
            started = _utc()
            task_dir = evidence_root / task_id
            before = fingerprint_paths(ROOT, task["protected_paths"])
            records: list[dict] = []
            status = "PASS"
            task_issues: list[str] = []
            for command_id in task["command_ids"]:
                template = command_template(command_id)
                argv, timeout = resolve_command(command_id)
                row = run_argv(
                    argv,
                    task_dir,
                    command_id.replace(":", "_"),
                    timeout=timeout,
                    command_id=command_id,
                    argv_template=template,
                )
                records.append(row)
                if (
                    row.get("command_started") is not True
                    or row.get("cleanup") not in {"COMPLETE", "COMPLETE_ALREADY_EXITED"}
                    or row["exit_code"] != 0
                ):
                    status = "FAIL"
                    task_issues.append("COMMAND_FAILED:" + command_id)
                    break
            after = fingerprint_paths(ROOT, task["protected_paths"])
            if before != after:
                status = "FAIL"
                task_issues.append("PROTECTED_PATH_MUTATED")
            return task_id, {
                "result_schema": RESULT_SCHEMA_VERSION,
                "task_id": task_id,
                "candidate_sha": campaign["candidate_sha"],
                "status": status,
                "effect_state": "NONE",
                "command_records": records,
                "first_failure": None,
                "wave_index": wave,
                "started_at_utc": started,
                "ended_at_utc": _utc(),
                "protected_fingerprint_before": before,
                "protected_fingerprint_after": after,
                "issues": task_issues,
            }

        wave_results: dict[str, dict] = {}
        with ThreadPoolExecutor(max_workers=len(decision.ready)) as pool:
            futures = [pool.submit(run_task, task_id) for task_id in decision.ready]
            for future in as_completed(futures):
                task_id, row = future.result()
                wave_results[task_id] = row
        for task_id in sorted(wave_results):
            results[task_id] = wave_results[task_id]

        failed = sorted(task_id for task_id, row in wave_results.items() if row["status"] == "FAIL")
        if failed and first_failure is None:
            first_failure = failed[0]
        global_failed = sorted(
            task_id
            for task_id in failed
            if tasks[task_id]["failure_scope"] == "GLOBAL_CAMPAIGN"
        )
        if global_failed:
            global_stop = global_failed[0]
        for row in results.values():
            row["first_failure"] = first_failure

        if _repo_status() != initial_status:
            first_failure = first_failure or "__REPO_MUTATION__"
            global_stop = "__REPO_MUTATION__"
            for row in results.values():
                row["first_failure"] = first_failure
        wave += 1

    verification = verify_campaign_run(campaign, results, evidence_root=evidence_root)
    summary = {
        "schema_version": "SER-PARALLEL-RUN-2",
        "campaign_id": campaign["campaign_id"],
        "candidate_sha": campaign["candidate_sha"],
        "status": (
            "PASS"
            if verification["valid"]
            and all(r["status"] in {"PASS", "NOT_APPLICABLE"} for r in results.values())
            else "FAIL"
        ),
        "first_failure": verification.get("first_failure"),
        "global_stop": global_stop,
        "results": results,
        "verification": verification,
    }
    (evidence_root / "summary.json").write_bytes(
        (json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", required=True, type=Path)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    args = parser.parse_args()
    campaign = json.loads(args.campaign.read_text(encoding="utf-8"))
    summary = execute(campaign, args.evidence_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
